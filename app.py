# app.py
# CampusEase Ezigbo — Attestation Letter Generator
# Flow: Signup (no email) → Letter Details → Preview (1 or 2 versions) → Email Verify → Download

import tempfile
import time
from pathlib import Path
from datetime import date, timedelta

import streamlit as st
import os
import urllib.parse
from dotenv import load_dotenv
load_dotenv()

_startup = time.time()

from template_engine import render_letter, render_instructions
from pdf_generator import html_to_pdf, html_to_pdf_with_instructions
from database import find_student, create_student, create_letter_request, check_has_downloaded, get_latest_letter_request, supabase
from email_sender import generate_and_send_code, verify_code

# ============================================================
# CONFIG
# ============================================================

st.markdown(
    """
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
    </script>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(
    page_title="Attestation Letter — CampusEase Ezigbo",
    page_icon="C",
    layout="centered",
)

st._config.set_option("theme.base", "light")

CAMPUSEASE_WHATSAPP = "https://wa.me/2348164961572"
# Force scroll-to-top on every page render (mobile-friendly)
st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] > section:first-child {
            scroll-behavior: auto !important;
        }
    </style>
    <script>
        const main = window.parent.document.querySelector('section.main');
        if (main) main.scrollTo({ top: 0, behavior: 'instant' });
    </script>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# INSTITUTIONS
# ============================================================
INSTITUTIONS = {
    "Michael Okpara University of Agriculture, Umudike (MOUAU)": {
        "addressee_title": "Office of the Registrar,",
        "institution_name": "Michael Okpara University of Agriculture,",
        "campus_location": "P.M.B. 7267, Umudike, Umuahia,\nAbia State, Nigeria.",
    },
    "University of Nigeria, Nsukka (UNN)": {
        "addressee_title": "The Registrar,",
        "institution_name": "University of Nigeria,",
        "campus_location": "Main Campus, Nsukka Road,\nIhe Nsukka 410001, Nsukka,\nEnugu State, Nigeria.",
    },
    "Federal University of Technology, Owerri (FUTO)": {
        "addressee_title": "The Registrar,",
        "institution_name": "Federal University of Technology,",
        "campus_location": "1526, P.M.B., Ihiagwa 460113,\nImo State, Nigeria.",
    },
    "Other (I'll enter my institution details)": None,
}

# ============================================================
# ATTESTER TYPES (who signs the letter)
# ============================================================
ATTESTER_TYPES = [
    "Parent",
    "Guardian",
    "Community Leader",
    "Church Pastor",
    "Imam",
]

# Title options that make sense for each attester type
ATTESTER_TITLES = {
    "Parent": ["Mr.", "Mrs.", "Miss", "Mr. & Mrs.", "Chief", "Dr.", "Prof.",
               "Engr.", "Barr.", "Pastor", "Evang.", "Alhaji", "Hajia"],
    "Guardian": ["Mr.", "Mrs.", "Miss", "Chief", "Dr.", "Prof.", "Engr.",
                 "Barr.", "Pastor", "Evang.", "Alhaji", "Hajia"],
    "Community Leader": ["Chief", "High Chief", "Ozo", "Nze", "Dr.", "Prof.",
                         "Barr.", "Engr.", "Alhaji"],
    "Church Pastor": ["Pastor", "Rev.", "Rev. Fr.", "Very Rev.", "Ven.",
                      "Bishop", "Apostle", "Prophet", "Evang."],
    "Imam": ["Imam", "Sheikh", "Ustaz", "Mallam", "Alhaji"],
}

# Keep the old list available in case anything else references it
PARENT_TITLES = ATTESTER_TITLES["Parent"]

# ============================================================
# HELPERS
# ============================================================
def _ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return (next_month - timedelta(days=1)).day


def _wrap_address(address: str, max_chars: int = 24, max_lines: int = 4) -> str:
    if not address:
        return ""
    raw_lines = [ln.strip() for ln in address.split("\n") if ln.strip()]
    wrapped = []
    for line in raw_lines:
        if len(line) <= max_chars:
            wrapped.append(line)
        else:
            words = line.split()
            current = ""
            for word in words:
                if not current:
                    current = word
                elif len(current) + 1 + len(word) <= max_chars:
                    current += " " + word
                else:
                    wrapped.append(current)
                    current = word
            if current:
                wrapped.append(current)
    if len(wrapped) > max_lines:
        tail = " ".join(wrapped[max_lines - 1:])
        wrapped = wrapped[:max_lines - 1] + [tail]
    return "<br>".join(wrapped)


def _opt_index(options, value, default=0):
    """Safe index lookup with fallback."""
    try:
        return options.index(value)
    except (ValueError, AttributeError):
        return default


ICONS = {
    "cap": '<svg class="icon" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
    "calendar": '<svg class="icon" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    "phone": '<svg class="icon" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "mail": '<svg class="icon" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    "chat": '<svg class="icon" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
    "chart": '<svg class="icon" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>',
    "check": '<svg class="icon" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22,4 12,14.01 9,11.01"/></svg>',
    "arrow-right": '<svg class="icon" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12,5 19,12 12,19"/></svg>',
    "download": '<svg class="icon" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
}

# ============================================================
# SCROLL HELPER — force scroll-to-top on mobile
# ============================================================
import streamlit.components.v1 as components

def scroll_to_top():
    """Scroll the main content area back to the top.
    Called at the start of each step to prevent the mobile issue
    where Streamlit keeps the previous scroll position."""
    components.html(
        """
        <script>
            (function() {
                try {
                    var doc = window.parent.document;
                    var main = doc.querySelector('section.main')
                            || doc.querySelector('[data-testid="stMain"]')
                            || doc.querySelector('[data-testid="stAppViewContainer"]');
                    if (main) {
                        main.scrollTo({ top: 0, left: 0, behavior: 'instant' });
                        main.scrollTop = 0;
                    }
                    if (window.parent) {
                        window.parent.scrollTo({ top: 0, left: 0, behavior: 'instant' });
                    }
                } catch (e) {}
            })();
        </script>
        """,
        height=0,
    )


# ============================================================
# STYLING
# ============================================================
st.markdown(
    """
    <style>
        /* ===== FORCE LIGHT MODE — overrides dark theme ===== */
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
            color: #1A1A1A !important;
        }
        [data-testid="stHeader"], [data-testid="stToolbar"] {
            background-color: #FFFFFF !important;
        }
        input, textarea, select,
        [data-baseweb="input"],
        [data-baseweb="textarea"],
        [data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #1A1A1A !important;
            border-color: #D1D5DB !important;
        }
        [data-testid="stAlert"] {
            background-color: #EEF4FF !important;
            color: #0B1F4B !important;
        }
        h1, h2, h3 { color: #0B1F4B !important; }
        .icon { display: inline-block; width: 16px; height: 16px; vertical-align: -3px; margin-right: 6px; stroke: currentColor; fill: none; }
        .icon-lg { width: 22px; height: 22px; vertical-align: -5px; margin-right: 8px; }
        .brand-header { position: relative; background: linear-gradient(135deg, #0B1F4B 0%, #16336b 55%, #0B1F4B 100%); text-align: center; padding: 34px 20px 30px 20px; border-bottom: 4px solid #F5B301; margin: -1rem -1rem 26px -1rem; border-radius: 0 0 14px 14px; overflow: hidden; box-shadow: 0 6px 20px rgba(11, 31, 75, 0.25); }
        .brand-header h1 { color: #FFFFFF; font-size: 2.3rem; margin: 0; font-weight: 800; letter-spacing: -0.5px; position: relative; z-index: 2; display: inline-flex; align-items: center; gap: 6px; }
        .brand-header h1 span { color: #F5B301; }
        .brand-header h1.gradient-title { background: linear-gradient(180deg, #FFFFFF 0%, #FFF4D6 45%, #F5B301 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent; filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.35)); }
        .brand-header h1.gradient-title span { background: inherit; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
        .brand-header p { color: #F5B301; font-style: italic; font-weight: 600; margin: 8px 0 0 0; font-size: 0.95rem; position: relative; z-index: 2; }
        .sparkle { position: absolute; width: 10px; height: 10px; background: #F5B301; border-radius: 50%; box-shadow: 0 0 10px #F5B301, 0 0 20px rgba(245, 179, 1, 0.6); animation: sparklePop 2s ease-out infinite; z-index: 1; }
        .sparkle.s1 { top: 10%; left: 5%; animation-delay: 0s; }
        .sparkle.s2 { top: 20%; right: 5%; animation-delay: 0.4s; width: 8px; height: 8px; }
        .sparkle.s3 { top: 55%; left: 0%; animation-delay: 0.8s; width: 6px; height: 6px; }
        .sparkle.s4 { top: 60%; right: 0%; animation-delay: 1.2s; width: 12px; height: 12px; }
        .sparkle.s5 { top: 0%; left: 45%; animation-delay: 0.6s; width: 7px; height: 7px; }
        .sparkle.s6 { top: 0%; right: 40%; animation-delay: 1.0s; width: 9px; height: 9px; }
        @keyframes sparklePop { 0% { opacity: 0; transform: scale(0.3) translateY(0); } 40% { opacity: 1; transform: scale(1.15) translateY(-4px); } 100% { opacity: 0; transform: scale(0.4) translateY(-14px); } }
        @keyframes shine { 0% { transform: translateX(-100%); } 100% { transform: translateX(200%); } }
        .brand-header::after { content: ""; position: absolute; top: 0; left: 0; width: 60%; height: 100%; background: linear-gradient(120deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.07) 50%, rgba(255, 255, 255, 0) 100%); animation: shine 5s ease-in-out infinite; pointer-events: none; z-index: 1; }
        .stButton > button { background-color: #0B1F4B; color: #FFFFFF; border: none; border-radius: 8px; padding: 0.7rem 1.2rem; font-weight: 600; width: 100%; }
        .stButton > button:hover { background-color: #F5B301; color: #0B1F4B; }
        .stDownloadButton > button { background-color: #F5B301; color: #0B1F4B; border: none; border-radius: 8px; padding: 0.9rem 1.2rem; font-weight: 700; width: 100%; font-size: 1.05rem; }
        .sig-card { background-color: #F7F9FC; border-left: 4px solid #F5B301; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; }
        .sig-card h4 { margin: 0 0 6px 0; color: #0B1F4B; }
        .sig-card p { margin: 4px 0; font-size: 0.92rem; color: #333; display: flex; align-items: center; }
        .sig-card p .icon { color: #0B1F4B; }
        .brand-footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #E5E9F0; }
        .brand-footer p { color: #0B1F4B; font-weight: 600; margin: 4px 0; }
        .brand-footer .tagline { color: #F5B301; font-style: italic; font-weight: 500; }
        .brand-footer a { color: #0B1F4B; text-decoration: none; font-weight: 700; }
        .brand-footer a:hover { color: #F5B301; }
        .date-caption { display: flex; align-items: center; color: #555; font-size: 0.9rem; margin-top: -4px; }
        .date-caption .icon { color: #0B1F4B; }
        .date-caption strong { color: #0B1F4B; margin-left: 2px; }
        .info-pill { display: flex; align-items: center; background: #EEF4FF; color: #0B1F4B; border-left: 3px solid #F5B301; padding: 8px 14px; border-radius: 6px; font-size: 0.9rem; margin: 8px 0 14px 0; }
        .info-pill .icon { color: #0B1F4B; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================
import base64 as _b64

def _logo_uri():
    p = Path("assets/logo.png")
    if not p.exists():
        return ""
    return f"data:image/png;base64,{_b64.b64encode(p.read_bytes()).decode('utf-8')}"

_logo = _logo_uri()
_logo_tag = f'<img src="{_logo}" alt="CampusEase Ezigbo" style="max-height:180px; max-width:180px; display:block; margin: 0 auto 14px auto; filter: drop-shadow(0 6px 18px rgba(0,0,0,0.45));" />' if _logo else ""

_header_html = f"""<div class="brand-header">
<div class="sparkle s1"></div>
<div class="sparkle s2"></div>
<div class="sparkle s3"></div>
<div class="sparkle s4"></div>
<div class="sparkle s5"></div>
<div class="sparkle s6"></div>
{_logo_tag}
<p style="margin: 0; color: #F5B301; font-style: italic; font-weight: 600; font-size: 0.95rem; position: relative; z-index: 2;">No Stress. No Delay. We've Got You.</p>
</div>"""
st.markdown(_header_html, unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
_defaults = {
    "step": 1,
    "profile": {},
    "pdf_bytes": None,
    "duplicate_student": None,
    "letter_data": None,
    "html_preview": None,
    "letter_body_id": None,
    "letter_layout_name": None,
    "preview_versions": [],
    "active_preview": 0,
    "verification_email": "",
    "verification_code_sent": False,
    "verification_verified": False,
    "form_data": {},  # remembers Letter Details form so Edit pre-fills it
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# ADMIN MODE (?admin=1)
# ============================================================
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

if st.query_params.get("admin") == "1":

    # ---------- LOGIN ----------
    if not st.session_state.get("admin_logged_in", False):
        st.markdown("## Admin Access")
        with st.form("admin_login"):
            _login_email = st.text_input("Admin Email")
            _login_pw = st.text_input("Password", type="password")
            _login_btn = st.form_submit_button("Login")

        if _login_btn:
            if (_login_email.strip().lower() == ADMIN_EMAIL.lower()
                and _login_pw == ADMIN_PASSWORD
                and ADMIN_EMAIL and ADMIN_PASSWORD):
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials.")

        st.stop()

    # ---------- LOGGED IN ----------
    _head1, _head2 = st.columns([3, 1])
    with _head1:
        st.markdown(f"## 🔐 Admin Panel")
        st.caption(f"Logged in as **{ADMIN_EMAIL}**")
    with _head2:
        if st.button("Log out"):
            st.session_state.admin_logged_in = False
            st.session_state.admin_edited = None
            st.session_state.admin_last_search = None
            st.rerun()

    st.markdown("### Find a student")
    st.caption("Enter their phone number or email.")

    _query = st.text_input("Phone or Email", placeholder="08012345678  or  name@email.com")

    if _query.strip():
        _search = _query.strip()

        # Reset edits when search changes
        if st.session_state.get("admin_last_search") != _search:
            st.session_state.admin_edited = None
            st.session_state.admin_last_search = _search

        _student = find_student(phone=_search) or find_student(email=_search.lower())

        if not _student:
            st.warning("No student found with that phone or email.")
            st.stop()

        st.success(f"Found: **{_student['full_name']}** · Phone: {_student.get('phone', '—')}")

        _req = get_latest_letter_request(_student["id"])
        if not _req:
            st.warning("This student has no letter on file yet.")
            st.stop()

        # Pre-fill defaults from stored letter request
        _stored = {
            "student_name": _student["full_name"],
            "gender": _req.get("gender", "Male"),
            "course_name": _req.get("course_name", "") or "",
            "institution_name": _req.get("institution_name", "") or "",
            "campus_location": _req.get("campus_location", "") or "",
            "addressee_title": _req.get("addressee_title", "The Registrar,") or "The Registrar,",
            "parent_title": _req.get("parent_title", "Mr.") or "Mr.",
            "parent_name": _req.get("parent_name", "") or "",
            "parent_address": _req.get("parent_address", "") or "",
            "attester_type": _req.get("attester_type", "Parent") or "Parent",
            "attester_label": _req.get("attester_label", "Parent") or "Parent",
            "letter_date": _req.get("letter_date", "") or "",
        }

        st.markdown("### Edit details")
        with st.form("admin_edit_form"):
            _e_student_name = st.text_input(
                "Student Full Name",
                value=_stored["student_name"],
                key="admin_student_name",
            )
            _e_gender = st.radio(
                "Gender", ["Male", "Female"],
                index=0 if _stored["gender"] == "Male" else 1,
                horizontal=True,
            )
            _e_course = st.text_input("Course / Department", value=_stored["course_name"])
            _e_inst = st.text_input("Institution Name", value=_stored["institution_name"])
            _e_loc = st.text_area("Campus Location", value=_stored["campus_location"], height=80)
            _e_addressee = st.text_input("Addressee", value=_stored["addressee_title"])

            _e_attester = st.selectbox(
                "Attester Type",
                ATTESTER_TYPES,
                index=_opt_index(ATTESTER_TYPES, _stored["attester_type"]),
            )

            _title_opts = ATTESTER_TITLES[_e_attester]
            _e_ptitle = st.selectbox(
                "Attester Title",
                _title_opts,
                index=_opt_index(_title_opts, _stored["parent_title"]),
            )
            _e_pname = st.text_input("Attester Full Name", value=_stored["parent_name"])
            _e_paddr = st.text_area("Attester Address", value=_stored["parent_address"], height=100)
            _e_date = st.text_input("Letter Date", value=_stored["letter_date"])

            _apply = st.form_submit_button("Apply Edits")

        if _apply:
            st.session_state.admin_edited = {
                "student_name": _e_student_name.strip() or _student["full_name"],
                "gender": _e_gender,
                "course_name": _e_course.strip(),
                "institution_name": _e_inst.strip(),
                "campus_location": _e_loc.strip(),
                "addressee_title": _e_addressee.strip(),
                "parent_title": _e_ptitle,
                "parent_name": _e_pname.strip(),
                "parent_address": _e_paddr.strip(),
                "parent_address_wrapped": _wrap_address(_e_paddr.strip()),
                "attester_type": _e_attester,
                "attester_label": _e_attester,
                "letter_date": _e_date,
            }
            # Persist the corrected name back to the students table
            if _e_student_name.strip() and _e_student_name.strip() != _student["full_name"]:
                try:
                    supabase.table("students") \
                        .update({"full_name": _e_student_name.strip()}) \
                        .eq("id", _student["id"]) \
                        .execute()
                    _student["full_name"] = _e_student_name.strip()
                except Exception as _e:
                    st.warning(f"Name saved in letter but not in students table: {_e}")

            st.rerun()

        # Build render data
        if st.session_state.get("admin_edited"):
            _render = dict(st.session_state.admin_edited)
        else:
            _render = dict(_stored)
            _render["parent_address_wrapped"] = _wrap_address(_stored["parent_address"])

        st.markdown("### Preview & Download")
        try:
            _html, _bid, _ln = render_letter(_render)
            st.components.v1.html(_html, height=800, scrolling=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as _tmp:
                _pdf_path = _tmp.name
            _admin_instructions = render_instructions()
            html_to_pdf_with_instructions(_html, _admin_instructions, _pdf_path)
            with open(_pdf_path, "rb") as _fh:
                _pdf_bytes = _fh.read()
            Path(_pdf_path).unlink(missing_ok=True)

            _safe_name = _student["full_name"].replace(" ", "_").replace("/", "_")
            st.download_button(
                "⬇  Download Corrected PDF",
                data=_pdf_bytes,
                file_name=f"{_safe_name}_Attestation.pdf",
                mime="application/pdf",
            )

            st.caption(
                f"💬 After download, send this PDF to the student on WhatsApp. "
                f"Their WhatsApp number is on file."
            )
        except Exception as _err:
            st.error(f"Failed to render letter: {_err}")

    st.stop()

# ============================================================
# STEP 1 — SIGN UP (no email)
# ============================================================
if st.session_state.step == 1:
    scroll_to_top()
    st.markdown("## Sign Up")
    st.caption("Create your profile to generate your free attestation letter.")

    st.markdown("**Full Name**")
    st.markdown(
        '<div style="color:#6B7280;font-size:0.82rem;margin-top:-10px;margin-bottom:6px;">'
        'Format: Surname First-name Last-name &nbsp;•&nbsp; e.g. Salako Oluwatosin Daniel'
        '</div>',
        unsafe_allow_html=True,
    )
    full_name = st.text_input("Full Name", placeholder="Enter your full name", label_visibility="collapsed")

    st.markdown("**Date of birth:**")
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        month_name = st.selectbox(
            "Month",
            ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"],
            label_visibility="collapsed",
        )
    with col3:
        year = st.selectbox("Year", list(range(date.today().year, 1949, -1)), label_visibility="collapsed")

    _month_num_for_days = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ].index(month_name) + 1
    _last_day = _days_in_month(year, _month_num_for_days)

    with col2:
        day = st.selectbox("Day", list(range(1, _last_day + 1)), label_visibility="collapsed")

    phone = st.text_input("Phone Number", placeholder="e.g. 08144832008")

    consent = st.checkbox(
        "I agree that CampusEase Ezigbo may store my information to send me my "
        "attestation letter and future updates (e.g. birthday wishes)."
    )

    st.caption("Your email will be requested later, when you're ready to download.")

    if st.button("Next  →"):
        if not full_name.strip():
            st.error("Please enter your full name.")
        elif not phone.strip():
            st.error("Please enter your phone number.")
        elif not consent:
            st.error("Please tick the consent box to continue.")
        else:
            month_num = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December",
            ].index(month_name) + 1
            phone_clean = phone.strip()

            existing = find_student(phone=phone_clean)

            if existing:
                # Phone exists. Has this person actually downloaded a letter?
                if check_has_downloaded(existing["id"]):
                    # YES — they finished before. Send to Step 99.
                    st.session_state.duplicate_student = existing
                    st.session_state.step = 99
                    st.rerun()
                else:
                    # NO — they started but never finished. Let them continue.
                    st.session_state.profile = {
                        "id": existing["id"],
                        "full_name": existing["full_name"],
                        "dob_day": existing.get("dob_day"),
                        "dob_month": existing.get("dob_month"),
                        "dob_year": existing.get("dob_year"),
                        "phone": existing["phone"],
                    }

                    # Load their last letter request (if any) to pre-fill the form
                    _prev = get_latest_letter_request(existing["id"])
                    if _prev:
                        # Try to match their previous institution name to one of our known options
                        _inst_names = list(INSTITUTIONS.keys())
                        _prev_inst = _prev.get("institution_name", "")
                        _matched_inst = None
                        for _name in _inst_names:
                            _data = INSTITUTIONS.get(_name)
                            if _data and _data.get("institution_name") == _prev_inst:
                                _matched_inst = _name
                                break
                        if not _matched_inst:
                            _matched_inst = _inst_names[0]

                        st.session_state.form_data = {
                            "gender": _prev.get("gender", "Male"),
                            "course_name": _prev.get("course_name", ""),
                            "inst_choice": _matched_inst,
                            "addressee_title": _prev.get("addressee_title", "The Registrar,"),
                            "institution_name": _prev.get("institution_name", ""),
                            "campus_location": _prev.get("campus_location", ""),
                            "attester_type": _prev.get("attester_type", "Parent"),
                            "parent_title": _prev.get("parent_title", "Mr."),
                            "parent_name": _prev.get("parent_name", ""),
                            "parent_address": _prev.get("parent_address", ""),
                        }

                    st.session_state.step = 2
                    st.rerun()
            else:
                # Brand new phone number
                new_row = create_student(
                    full_name=full_name.strip(),
                    dob_day=day,
                    dob_month=month_num,
                    dob_year=year,
                    phone=phone_clean,
                )
                st.session_state.profile = {
                    "id": new_row["id"],
                    "full_name": new_row["full_name"],
                    "dob_day": new_row["dob_day"],
                    "dob_month": new_row["dob_month"],
                    "dob_year": new_row["dob_year"],
                    "phone": new_row["phone"],
                }
                st.session_state.step = 2
                st.rerun()
# ============================================================
# STEP 2 — LETTER DETAILS
# ============================================================

elif st.session_state.step == 2:
    scroll_to_top()
    st.markdown("## Letter Details")
    st.caption(f"Signed in as **{st.session_state.profile['full_name']}**")

    _saved = st.session_state.form_data or {}

        # ---------- RESTORE WIDGET STATE FROM form_data ----------
    # Streamlit clears widget state when they aren't rendered (e.g. during preview).
    # This block restores them so returning users see their previous answers.
    if _saved:
        _widget_defaults = {
            "gender_radio": _saved.get("gender", "Male"),
            "course_name_input": _saved.get("course_name", ""),
            "inst_choice_selectbox": _saved.get("inst_choice", list(INSTITUTIONS.keys())[0]),
            "addressee_title_input": _saved.get("addressee_title", "The Registrar,"),
            "institution_name_input": _saved.get("institution_name", ""),
            "campus_location_textarea": _saved.get("campus_location", ""),
            "attester_type_selectbox": _saved.get("attester_type", "Parent"),
            "parent_title_selectbox": _saved.get("parent_title", "Mr."),
            "parent_name_input": _saved.get("parent_name", ""),
            "parent_address_textarea": _saved.get("parent_address", ""),
        }
        for _k, _v in _widget_defaults.items():
            if _k not in st.session_state:
                st.session_state[_k] = _v

    # ---------- GENDER ----------
    _gender_options = ["Male", "Female"]
    gender = st.radio(
        "Gender",
        _gender_options,
        index=_opt_index(_gender_options, _saved.get("gender", "Male")),
        horizontal=True,
        key="gender_radio",
    )

    # ---------- COURSE ----------
    course_name = st.text_input(
        "Course / Department",
        value=_saved.get("course_name", ""),
        placeholder="e.g. Computer Science",
        key="course_name_input",
    )

    # ---------- INSTITUTION ----------
    st.markdown("### Institution")
    _inst_options = list(INSTITUTIONS.keys())
    inst_choice = st.selectbox(
        "Select your institution",
        _inst_options,
        index=_opt_index(_inst_options, _saved.get("inst_choice", _inst_options[0])),
        key="inst_choice_selectbox",
    )

    if INSTITUTIONS[inst_choice] is None:
        addressee_title = st.text_input(
            "Addressee",
            value=_saved.get("addressee_title", "The Registrar,"),
            key="addressee_title_input",
        )
        institution_name = st.text_input(
            "Institution Name",
            value=_saved.get("institution_name", ""),
            placeholder="e.g. Nnamdi Azikiwe University,",
            key="institution_name_input",
        )
        campus_location = st.text_area(
            "Institution Address / Campus Location",
            value=_saved.get("campus_location", ""),
            placeholder="e.g. P.M.B. 5025, Awka,\nAnambra State, Nigeria.",
            height=100,
            key="campus_location_textarea",
        )
    else:
        details = INSTITUTIONS[inst_choice]
        addressee_title = details["addressee_title"]
        institution_name = details["institution_name"]
        campus_location = details["campus_location"]
        st.markdown(
            f'<div class="info-pill">{ICONS["check"]}Using saved details for <strong>&nbsp;{inst_choice}</strong></div>',
            unsafe_allow_html=True,
        )

    # ---------- WHO IS ATTESTING ----------
    st.markdown("### Who is signing this letter for you?")

    st.info(
        "👤 **This section is about the person who will sign your letter — "
        "NOT you.** Fill in their details, not your own. Their name will appear "
        "at the bottom of your attestation letter."
    )

    attester_type = st.selectbox(
        "Attester Type",
        ATTESTER_TYPES,
        index=_opt_index(ATTESTER_TYPES, _saved.get("attester_type", "Parent")),
        key="attester_type_selectbox",
        help="Choose who will sign this letter — the label will appear under the signature line.",
    )

    _title_options = ATTESTER_TITLES[attester_type]
    _saved_title = _saved.get("parent_title", _title_options[0])
    parent_title = st.selectbox(
        "Attester's Title",
        _title_options,
        index=_opt_index(_title_options, _saved_title),
        key="parent_title_selectbox",
        help="The title that goes before their name (e.g. Mr., Pastor, Chief).",
    )

    parent_name = st.text_input(
        "Attester's Full Name",
        value=_saved.get("parent_name", ""),
        placeholder="e.g. Salako Oluwatosin Daniel",
        key="parent_name_input",
        help="The person who is signing — your father, mother, guardian, pastor, etc.",
    )
    st.caption(
        "⬆️ Enter the full name of the person signing your letter "
        "(e.g. your father, mother, guardian, pastor, or imam)."
    )

    parent_address = st.text_area(
        "Attester's Address",
        value=_saved.get("parent_address", ""),
        placeholder="12 Main Street,\nUmuahia,\nAbia State.",
        height=100,
        key="parent_address_textarea",
        help="Their home or office address, which appears at the top-right of the letter.",
    )

    attester_label = attester_type

    # ---------- DATE ----------
    _today = date.today()
    letter_date = f"{_ordinal(_today.day)} {_today.strftime('%B, %Y')}"
    st.markdown(
        f'<div class="date-caption">{ICONS["calendar"]}Letter date:&nbsp;<strong>{letter_date}</strong>&nbsp;(auto-filled with today\'s date)</div>',
        unsafe_allow_html=True,
    )

    # ---------- NAVIGATION ----------
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("←  Back", key="back_to_step1"):
            st.session_state.step = 1
            st.rerun()
    with col_b:
        if st.button("Preview Letter", key="preview_letter_btn"):
            _missing = []
            if not course_name.strip():
                _missing.append("Course / Department")
            if not institution_name.strip():
                _missing.append("Institution Name")
            if not campus_location.strip():
                _missing.append("Institution Address")
            if not parent_name.strip():
                _missing.append("Attester's Full Name")
            if not parent_address.strip():
                _missing.append("Attester's Address")

            if _missing:
                st.error("Please fill in: " + ", ".join(_missing))
            else:
                data = {
                    "student_name": st.session_state.profile["full_name"],
                    "gender": gender,
                    "course_name": course_name.strip(),
                    "institution_name": institution_name.strip(),
                    "campus_location": campus_location.strip(),
                    "addressee_title": addressee_title.strip(),
                    "parent_title": parent_title,
                    "parent_name": parent_name.strip(),
                    "parent_address": parent_address.strip(),
                    "parent_address_wrapped": _wrap_address(parent_address.strip()),
                    "letter_date": letter_date,
                    "attester_type": attester_type,
                    "attester_label": attester_label,
                }

                st.session_state.form_data = {
                    "gender": gender,
                    "course_name": course_name,
                    "inst_choice": inst_choice,
                    "addressee_title": addressee_title,
                    "institution_name": institution_name,
                    "campus_location": campus_location,
                    "attester_type": attester_type,
                    "parent_title": parent_title,
                    "parent_name": parent_name,
                    "parent_address": parent_address,
                }

                html, body_id, layout_name = render_letter(data)

                st.session_state.preview_versions = [{
                    "html": html,
                    "body_id": body_id,
                    "layout_name": layout_name,
                    "data": data,
                }]
                st.session_state.active_preview = 0
                st.session_state.letter_data = data
                st.session_state.html_preview = html
                st.session_state.letter_body_id = body_id
                st.session_state.letter_layout_name = layout_name

                create_letter_request(
                    student_id=st.session_state.profile["id"],
                    data=data,
                    template_used="template_001.html",
                )

                st.session_state.step = 25
                st.rerun()
# ============================================================
# STEP 25 — PREVIEW (1 or 2 versions, user picks)
# ============================================================
elif st.session_state.step == 25:
    scroll_to_top()
    st.markdown("## Preview Your Letter")

    versions = st.session_state.preview_versions
    num_versions = len(versions)

    if num_versions == 1:
        st.info(
            "**Please review the letter below.** "
            "If it looks good, click **Download**. "
            "Or generate another version to compare side-by-side."
        )
    else:
        st.success("You now have **2 versions** to compare. Pick the one you prefer, then download it.")

    active_idx = st.session_state.active_preview
    active = versions[active_idx]

    if num_versions == 2:
        st.markdown(f"### Currently viewing: **Version {active_idx + 1}**")
        toggle_col1, toggle_col2 = st.columns(2)
        with toggle_col1:
            if st.button(f"{'✅ ' if active_idx == 0 else ''}View Version 1", key="v1_btn"):
                st.session_state.active_preview = 0
                st.rerun()
        with toggle_col2:
            if st.button(f"{'✅ ' if active_idx == 1 else ''}View Version 2", key="v2_btn"):
                st.session_state.active_preview = 1
                st.rerun()

    st.components.v1.html(active["html"], height=800, scrolling=True)
    st.markdown("")

    if num_versions == 1:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("←  Edit Details"):
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.button("Generate Another Version"):
                with st.spinner("Generating another version..."):
                    html2, body_id2, layout2 = render_letter(active["data"])
                versions.append({
                    "html": html2,
                    "body_id": body_id2,
                    "layout_name": layout2,
                    "data": active["data"],
                })
                st.session_state.preview_versions = versions
                st.session_state.active_preview = 1
                st.rerun()
        with col3:
            if st.button("Download PDF  →"):
                st.session_state.step = 26
                st.rerun()
    else:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("←  Edit Details"):
                st.session_state.step = 2
                st.session_state.preview_versions = []
                st.session_state.active_preview = 0
                st.rerun()
        with col2:
            if st.button("Regenerate Both"):
                with st.spinner("Regenerating both versions..."):
                    h1, b1, l1 = render_letter(active["data"])
                    h2, b2, l2 = render_letter(active["data"])
                st.session_state.preview_versions = [
                    {"html": h1, "body_id": b1, "layout_name": l1, "data": active["data"]},
                    {"html": h2, "body_id": b2, "layout_name": l2, "data": active["data"]},
                ]
                st.session_state.active_preview = 0
                st.rerun()
        with col3:
            if st.button(f"Download Version {active_idx + 1}  →"):
                st.session_state.step = 26
                st.rerun()

# ============================================================
# STEP 26 — EMAIL + VERIFICATION CODE
# ============================================================
elif st.session_state.step == 26:
    scroll_to_top()
    st.markdown("## One Last Step")
    st.caption("Enter your email to receive a verification code, then download your letter.")

    if not st.session_state.verification_code_sent:
        st.info(
            "📧 **Why we ask now?** We only ask for your email right before download — "
            "so your account isn't locked until you actually get your letter."
        )
        email_input = st.text_input("Email Address", placeholder="e.g. myemail@gmail.com")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("←  Back to Preview"):
                st.session_state.step = 25
                st.rerun()
        with col2:
            if st.button("Send Verification Code"):
                email_clean = email_input.strip().lower()
                if not email_clean or "@" not in email_clean or "." not in email_clean:
                    st.error("Please enter a valid email address.")
                else:
                    with st.spinner("Sending code..."):
                        result = generate_and_send_code(
                            student_id=st.session_state.profile["id"],
                            email=email_clean,
                        )
                    if result["ok"]:
                        st.session_state.verification_email = email_clean
                        st.session_state.verification_code_sent = True
                        st.rerun()
                    else:
                        st.error(result["error"])
    else:
        st.success(f"✅ Code sent to **{st.session_state.verification_email}**")
        st.caption("Check your inbox (and spam folder). The code expires in 10 minutes.")

        code_input = st.text_input("Enter 6-digit code", max_chars=6, placeholder="123456")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("←  Use a different email"):
                st.session_state.verification_code_sent = False
                st.session_state.verification_email = ""
                st.rerun()
        with col2:
            if st.button("Verify & Download"):
                code_clean = code_input.strip()
                if len(code_clean) != 6 or not code_clean.isdigit():
                    st.error("Please enter the 6-digit code.")
                else:
                    with st.spinner("Verifying..."):
                        result = verify_code(
                            student_id=st.session_state.profile["id"],
                            entered_code=code_clean,
                        )
                    if result["ok"]:
                        st.session_state.verification_verified = True
                        st.session_state.step = 3
                        st.rerun()
                    else:
                        st.error(result["error"])


# ============================================================
# STEP 100 - LOST FILE / RE-ISSUE REQUEST
# ============================================================
elif st.session_state.step == 100:
    scroll_to_top()

    REISSUE_FEE = "500"
    REISSUE_ACCOUNT = "8129632135"
    REISSUE_BANK = "Moniepoint"
    REISSUE_NAME = "Salako Oluwatosin Daniel"
    ADMIN_WHATSAPP = "2348144832008"

    st.markdown("## Request a Re-issue")
    st.caption("You have already generated a letter before. If you lost it, we can re-issue it for a small fee.")

    certified = st.radio(
        "Do you remember the details you used before?",
        ["Yes - I remember my details", "No - I don't remember"],
        key="lost_certified_radio",
    )

    st.markdown("---")

    _def_name = st.session_state.get("lost_name", "") or ""
    _def_phone = st.session_state.get("lost_phone", "") or ""

    if certified.startswith("Yes"):
        st.markdown("### Your details")
        st.caption("Just the basics - we already have the rest on file.")
        lost_name = st.text_input("Full Name", value=_def_name, key="lost_short_name")
        lost_phone = st.text_input("Phone Number", value=_def_phone, key="lost_short_phone")
        lost_email = st.text_input("Your Email", placeholder="e.g. myemail@gmail.com", key="lost_short_email")
        wa_details = "*Name:* " + lost_name.strip() + chr(10) + "*Phone:* " + lost_phone.strip() + chr(10) + "*Email:* " + lost_email.strip().lower() + chr(10)
        _can_forward = bool(lost_name.strip() and lost_phone.strip() and lost_email.strip())
    else:
        st.markdown("### Fill in your details again")
        st.caption("We will use this to regenerate your letter exactly how you had it.")
        lost_name = st.text_input("Full Name", value=_def_name, key="lost_full_name")
        lost_phone = st.text_input("Phone Number", value=_def_phone, key="lost_full_phone")
        lost_email = st.text_input("Your Email", placeholder="e.g. myemail@gmail.com", key="lost_full_email")
        lost_gender = st.radio("Gender", ["Male", "Female"], horizontal=True, key="lost_gender_radio")
        lost_course = st.text_input("Course / Department", placeholder="e.g. Computer Science", key="lost_course_input")

        st.markdown("**Institution**")
        lost_inst_choice = st.selectbox("Select your institution", list(INSTITUTIONS.keys()), key="lost_inst_selectbox")
        if INSTITUTIONS[lost_inst_choice] is None:
            lost_inst_name = st.text_input("Institution Name", placeholder="e.g. Nnamdi Azikiwe University,", key="lost_inst_name_input")
            lost_inst_loc = st.text_area("Institution Address", placeholder="P.M.B. 5025, Awka", height=80, key="lost_inst_loc_textarea")
        else:
            _d = INSTITUTIONS[lost_inst_choice]
            lost_inst_name = _d["institution_name"]
            lost_inst_loc = _d["campus_location"]

        st.markdown("**Who was signing your letter?**")
        lost_attester = st.selectbox("Attester Type", ATTESTER_TYPES, key="lost_attester_selectbox")
        _lost_title_opts = ATTESTER_TITLES[lost_attester]
        lost_attester_title = st.selectbox("Attester Title", _lost_title_opts, key="lost_attester_title_selectbox")
        lost_attester_name = st.text_input("Attester Full Name", placeholder="The person who was signing for you", key="lost_attester_name_input")
        lost_attester_addr = st.text_area("Attester Address", placeholder="12 Main Street, Umuahia", height=80, key="lost_attester_addr_textarea")

        wa_details = (
            "*Name:* " + lost_name.strip() + chr(10) +
            "*Phone:* " + lost_phone.strip() + chr(10) +
            "*Email:* " + lost_email.strip().lower() + chr(10) +
            "*Gender:* " + lost_gender + chr(10) +
            "*Course:* " + lost_course.strip() + chr(10) +
            "*Institution:* " + lost_inst_name.strip() + chr(10) +
            "*Campus:* " + lost_inst_loc.strip() + chr(10) +
            "*Attester Type:* " + lost_attester + chr(10) +
            "*Attester Title:* " + lost_attester_title + chr(10) +
            "*Attester Name:* " + lost_attester_name.strip() + chr(10) +
            "*Attester Address:* " + lost_attester_addr.strip() + chr(10)
        )
        _can_forward = all([
            lost_name.strip(), lost_phone.strip(), lost_email.strip(),
            lost_course.strip(), lost_inst_name.strip(),
            lost_attester_name.strip(), lost_attester_addr.strip(),
        ])

    st.markdown("---")
    st.markdown("### Payment")
    st.markdown(
        "<div style='background:#FFF8E1;border-left:4px solid #F5B301;padding:18px 22px;border-radius:8px;margin:12px 0;'>"
        "<p style='margin:0 0 12px 0;color:#0B1F4B;font-weight:700;font-size:1.05rem;'>Transfer N500 to:</p>"
        "<p style='margin:4px 0;color:#333;'><strong>Account Number:</strong> " + REISSUE_ACCOUNT + "</p>"
        "<p style='margin:4px 0;color:#333;'><strong>Bank:</strong> " + REISSUE_BANK + "</p>"
        "<p style='margin:4px 0;color:#333;'><strong>Account Name:</strong> " + REISSUE_NAME + "</p>"
        "<p style='margin:4px 0;color:#333;'><strong>Amount:</strong> N" + REISSUE_FEE + "</p>"
        "<p style='margin:12px 0 0 0;color:#444;font-size:0.88rem;font-style:italic;'>After payment, forward the message below to our WhatsApp.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Forward to WhatsApp")
    _wa_message = (
        "*LOST LETTER - RE-ISSUE REQUEST*" + chr(10) + chr(10) +
        wa_details + chr(10) +
        "_I confirm I have paid N" + REISSUE_FEE + " to your " + REISSUE_BANK + " account._" + chr(10) + chr(10) +
        "_I will send the payment receipt in this chat._"
    )
    st.caption("This is what will be sent. Fill the form above first.")
    st.code(_wa_message, language=None)

    _wa_url = "https://wa.me/" + ADMIN_WHATSAPP + "?text=" + urllib.parse.quote(_wa_message)

    if _can_forward:
        st.link_button("Forward to WhatsApp", _wa_url, use_container_width=True)
        st.caption("Tap the button above - WhatsApp will open with the message ready to send.")
    else:
        st.button("Forward to WhatsApp", disabled=True, use_container_width=True)
        st.caption("Fill in all required fields above to enable the forward button.")

    st.markdown("")
    if st.button("Back", key="lost_back_btn"):
        st.session_state.step = 99
        st.rerun()

# ============================================================
# STEP 3 — DOWNLOAD + LINK
# ============================================================
elif st.session_state.step == 3:
    versions = st.session_state.preview_versions
    active_html = versions[st.session_state.active_preview]["html"]

    if st.session_state.pdf_bytes is None:
        with st.spinner("Preparing your PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp_path = tmp.name
            _instructions_html = render_instructions()
            html_to_pdf_with_instructions(active_html, _instructions_html, tmp_path)
            with open(tmp_path, "rb") as f:
                st.session_state.pdf_bytes = f.read()
            Path(tmp_path).unlink(missing_ok=True)

    st.markdown(
        f'## {ICONS["check"].replace("icon", "icon icon-lg")}Your Attestation Letter is Ready',
        unsafe_allow_html=True,
    )

    # Pick the right word for the warning
    _attester_word = (st.session_state.form_data.get("attester_type") or "parent").lower()
    st.warning(
        f"**Important:** Download the PDF, print it, and have your **{_attester_word}** "
        "**sign above the signature line** before you submit it to your institution. "
        "An unsigned letter is not valid."
    )

    if st.session_state.pdf_bytes:
        safe_name = st.session_state.profile["full_name"].replace(" ", "_").replace("/", "_")
        st.download_button(
            label="⬇  Download Attestation Letter (PDF)",
            data=st.session_state.pdf_bytes,
            file_name=f"{safe_name}_Attestation.pdf",
            mime="application/pdf",
        )

    st.markdown("---")

    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0B1F4B 0%, #16336b 100%); border-radius: 12px; padding: 22px 24px; text-align: center; margin: 20px 0; border: 2px solid #F5B301;">
            <h3 style="color: #F5B301; margin: 0 0 8px 0; font-size: 1.2rem;">Stay Connected</h3>
            <p style="color: #FFFFFF; margin: 6px 0 16px 0; font-size: 0.95rem;">Follow our WhatsApp channel for admission tips, new tools, and updates from CampusEase Ezigbo.</p>
            <a href="https://whatsapp.com/channel/0029VbDkig1FcowDr9yhaO3h" target="_blank" style="display: inline-block; background: #F5B301; color: #0B1F4B; padding: 12px 28px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 1rem;">Follow us on WhatsApp</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Connect with us")
    st.markdown(
        f"""
        <div class="sig-card">
            <h4>Salako Oluwatosin Daniel</h4>
            <p><strong>&nbsp;Founder, CampusEase Ezigbo</strong></p>
            <p>{ICONS['phone']}08164961572</p>
            <p>{ICONS['mail']}salakwebtech@gmail.com</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="sig-card">
            <h4>CampusEase Ezigbo</h4>
            <p><strong>&nbsp;Trusted Student Services</strong></p>
            <p>{ICONS['cap']}Clearance &nbsp;•&nbsp; Payments &nbsp;•&nbsp; Registration</p>
            <p>{ICONS['chart']}Project &amp; Data Analysis</p>
            <p>{ICONS['chat']}WhatsApp: 08144832008</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="brand-footer">
            <p><a href="{CAMPUSEASE_WHATSAPP}" target="_blank">Chat with us on WhatsApp</a></p>
            <p class="tagline">No Stress. No Delay. We've Got You.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Generate another letter"):
        for k, v in _defaults.items():
            st.session_state[k] = v
        st.session_state.form_data = {}
        st.rerun()

# ============================================================
# STEP 99 — DUPLICATE FOUND
# ============================================================
elif st.session_state.step == 99:
    scroll_to_top()
    existing = st.session_state.duplicate_student or {}
    st.markdown("## You've already generated a letter")
    st.warning(
        f"We found an existing record for **{existing.get('full_name', 'this person')}**. "
        "Each student can generate one attestation letter to prevent abuse."
    )

    if st.button("📄 I lost my letter — Request a re-issue", use_container_width=True, key="lost_letter_btn"):
        st.session_state.lost_name = existing.get("full_name", "")
        st.session_state.lost_phone = existing.get("phone", "")
        st.session_state.step = 100
        st.rerun()

    st.markdown("---")


    st.markdown("### Want to generate for a friend?")
    st.caption("Enter their details below — one letter per person.")

    with st.form("friend_form"):
        friend_name = st.text_input("Friend's Full Name")
        friend_phone = st.text_input("Friend's Phone Number")
        friend_consent = st.checkbox("Friend consents to us storing this data.")
        submit = st.form_submit_button("Continue")

    if submit:
        if not (friend_name.strip() and friend_phone.strip()):
            st.error("Please fill in all fields.")
        elif not friend_consent:
            st.error("Please confirm your friend consents.")
        else:
            friend_existing = find_student(phone=friend_phone.strip())

            if friend_existing:
                if check_has_downloaded(friend_existing["id"]):
                    st.error("That friend has also already downloaded a letter.")
                else:
                    # Friend started but never finished — resume them
                    st.session_state.profile = {
                        "id": friend_existing["id"],
                        "full_name": friend_existing["full_name"],
                        "dob_day": friend_existing.get("dob_day"),
                        "dob_month": friend_existing.get("dob_month"),
                        "dob_year": friend_existing.get("dob_year"),
                        "phone": friend_existing["phone"],
                    }

                    # Load their last letter request (if any) to pre-fill the form
                    _prev = get_latest_letter_request(friend_existing["id"])
                    if _prev:
                        _inst_names = list(INSTITUTIONS.keys())
                        _prev_inst = _prev.get("institution_name", "")
                        _matched_inst = None
                        for _name in _inst_names:
                            _data = INSTITUTIONS.get(_name)
                            if _data and _data.get("institution_name") == _prev_inst:
                                _matched_inst = _name
                                break
                        if not _matched_inst:
                            _matched_inst = _inst_names[0]

                        st.session_state.form_data = {
                            "gender": _prev.get("gender", "Male"),
                            "course_name": _prev.get("course_name", ""),
                            "inst_choice": _matched_inst,
                            "addressee_title": _prev.get("addressee_title", "The Registrar,"),
                            "institution_name": _prev.get("institution_name", ""),
                            "campus_location": _prev.get("campus_location", ""),
                            "attester_type": _prev.get("attester_type", "Parent"),
                            "parent_title": _prev.get("parent_title", "Mr."),
                            "parent_name": _prev.get("parent_name", ""),
                            "parent_address": _prev.get("parent_address", ""),
                        }

                    st.session_state.duplicate_student = None
                    st.session_state.step = 2
                    st.rerun()
            else:
                # Brand new friend
                new_row = create_student(
                    full_name=friend_name.strip(),
                    dob_day=1, dob_month=1, dob_year=2000,
                    phone=friend_phone.strip(),
                )
                st.session_state.profile = {
                    "id": new_row["id"],
                    "full_name": new_row["full_name"],
                    "dob_day": new_row["dob_day"],
                    "dob_month": new_row["dob_month"],
                    "dob_year": new_row["dob_year"],
                    "phone": new_row["phone"],
                }
                st.session_state.duplicate_student = None
                st.session_state.step = 2
                st.rerun()



# --- Load time indicator ---
st.caption(f"⏱️ Load time: {time.time() - _startup:.2f}s")