# app.py
# CampusEase Ezigbo — Attestation Letter Generator
# Phase 1: Signup → Letter Details → Generate → Download → Link

import tempfile
from pathlib import Path
from datetime import date

import streamlit as st

from template_engine import render_template
from pdf_generator import html_to_pdf
from database import find_student, create_student, create_letter_request

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="Attestation Letter — CampusEase Ezigbo",
    page_icon="C",
    layout="centered",
)

CAMPUSEASE_WHATSAPP = "https://wa.me/2348164961572"

# ============================================================
# INSTITUTIONS (Registrar address blocks)
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
# PARENT / GUARDIAN TITLES
# ============================================================
PARENT_TITLES = [
    "Mr.", "Mrs.", "Miss", "Mr. & Mrs.",
    "Chief", "Dr.", "Prof.", "Engr.", "Barr.", "Arc.", "Surv.",
    "Pastor", "Rev.", "Rev. Fr.", "Very Rev.", "Ven.",
    "Evang.", "Apostle", "Bishop", "Prophet",
    "Imam", "Alhaji", "Hajia",
]

# ============================================================
# ICONS (inline SVG — Lucide-style, no emojis)
# ============================================================
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
# BRAND STYLING
# ============================================================
st.markdown(
    """
    <style>
        .stApp { background-color: #ffffff; }
        h1, h2, h3 { color: #0B1F4B !important; }

        /* Icon base styles */
        .icon {
            display: inline-block;
            width: 16px;
            height: 16px;
            vertical-align: -3px;
            margin-right: 6px;
            stroke: currentColor;
            fill: none;
        }
        .icon-lg { width: 22px; height: 22px; vertical-align: -5px; margin-right: 8px; }

/* ---------- NAVY BRAND HEADER ---------- */
.brand-header {
    position: relative;
    background: linear-gradient(135deg, #0B1F4B 0%, #16336b 55%, #0B1F4B 100%);
    text-align: center;
    padding: 34px 20px 30px 20px;
    border-bottom: 4px solid #F5B301;
    margin: -1rem -1rem 26px -1rem;
    border-radius: 0 0 14px 14px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(11, 31, 75, 0.25);
}

.brand-header h1 {
    color: #FFFFFF;
    font-size: 2.3rem;
    margin: 0;
    font-weight: 800;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 2;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.brand-header h1 span { color: #F5B301; }
.brand-header p {
    color: #F5B301;
    font-style: italic;
    font-weight: 600;
    margin: 8px 0 0 0;
    font-size: 0.95rem;
    position: relative;
    z-index: 2;
}

/* Animated rejoicing graduate */
.grad-wrap {
    position: relative;
    display: inline-block;
    width: 90px;
    height: 90px;
    margin-bottom: 6px;
    z-index: 2;
}
.grad-wrap svg {
    width: 100%;
    height: 100%;
    overflow: visible;
}

/* Jump / rejoice animation */
@keyframes rejoice {
    0%   { transform: translateY(0) rotate(0deg); }
    25%  { transform: translateY(-10px) rotate(-4deg); }
    50%  { transform: translateY(0) rotate(0deg); }
    75%  { transform: translateY(-6px) rotate(4deg); }
    100% { transform: translateY(0) rotate(0deg); }
}
.grad-figure {
    animation: rejoice 1.6s ease-in-out infinite;
    transform-origin: 50% 90%;
}

/* Gold sparkles popping around the graduate */
@keyframes sparklePop {
    0%   { opacity: 0; transform: scale(0.3) translateY(0); }
    40%  { opacity: 1; transform: scale(1.15) translateY(-4px); }
    100% { opacity: 0; transform: scale(0.4) translateY(-14px); }
}
.sparkle {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #F5B301;
    border-radius: 50%;
    box-shadow: 0 0 10px #F5B301, 0 0 20px rgba(245, 179, 1, 0.6);
    animation: sparklePop 2s ease-out infinite;
    z-index: 1;
}
.sparkle.s1 { top: 10%; left: 5%;  animation-delay: 0s;   }
.sparkle.s2 { top: 20%; right: 5%; animation-delay: 0.4s; width: 8px; height: 8px; }
.sparkle.s3 { top: 55%; left: 0%;  animation-delay: 0.8s; width: 6px; height: 6px; }
.sparkle.s4 { top: 60%; right: 0%; animation-delay: 1.2s; width: 12px; height: 12px; }
.sparkle.s5 { top: 0%;  left: 45%; animation-delay: 0.6s; width: 7px; height: 7px; }
.sparkle.s6 { top: 0%;  right: 40%; animation-delay: 1.0s; width: 9px; height: 9px; }

/* Gentle shine sweep across the header */
@keyframes shine {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(200%); }
}
.brand-header::after {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 60%;
    height: 100%;
    background: linear-gradient(
        120deg,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0.07) 50%,
        rgba(255, 255, 255, 0) 100%
    );
    animation: shine 5s ease-in-out infinite;
    pointer-events: none;
    z-index: 1;
}
        .stButton > button {
            background-color: #0B1F4B;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 0.7rem 1.2rem;
            font-weight: 600;
            width: 100%;
        }
        .stButton > button:hover { background-color: #F5B301; color: #0B1F4B; }

        .stDownloadButton > button {
            background-color: #F5B301;
            color: #0B1F4B;
            border: none;
            border-radius: 8px;
            padding: 0.9rem 1.2rem;
            font-weight: 700;
            width: 100%;
            font-size: 1.05rem;
        }

        .sig-card {
            background-color: #F7F9FC;
            border-left: 4px solid #F5B301;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 12px;
        }
        .sig-card h4 { margin: 0 0 6px 0; color: #0B1F4B; }
        .sig-card p {
            margin: 4px 0;
            font-size: 0.92rem;
            color: #333;
            display: flex;
            align-items: center;
        }
        .sig-card p .icon { color: #0B1F4B; }

        .brand-footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #E5E9F0;
        }
        .brand-footer p { color: #0B1F4B; font-weight: 600; margin: 4px 0; }
        .brand-footer .tagline {
            color: #F5B301;
            font-style: italic;
            font-weight: 500;
        }
        .brand-footer a {
            color: #0B1F4B;
            text-decoration: none;
            font-weight: 700;
        }
        .brand-footer a:hover { color: #F5B301; }

        .date-caption {
            display: flex;
            align-items: center;
            color: #555;
            font-size: 0.9rem;
            margin-top: -4px;
        }
        .date-caption .icon { color: #0B1F4B; }
        .date-caption strong { color: #0B1F4B; margin-left: 2px; }

        .info-pill {
            display: flex;
            align-items: center;
            background: #EEF4FF;
            color: #0B1F4B;
            border-left: 3px solid #F5B301;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 0.9rem;
            margin: 8px 0 14px 0;
        }
        .info-pill .icon { color: #0B1F4B; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    f"""
    <div class="brand-header">
        <h1>{ICONS['cap'].replace('class="icon"', 'class="icon icon-lg"')}Campus<span>Ease</span> Ezigbo</h1>
        <p>No Stress. No Delay. We've Got You.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================
if "step" not in st.session_state:
    st.session_state.step = 1
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
if "duplicate_student" not in st.session_state:
    st.session_state.duplicate_student = None

# ============================================================
# STEP 1 — SIGN UP
# ============================================================
if st.session_state.step == 1:
    st.markdown("## Sign Up")
    st.caption("Create your profile to generate your free attestation letter.")

    st.markdown("**Full Name**")
    st.markdown(
        '<div style="color:#6B7280;font-size:0.82rem;margin-top:-10px;margin-bottom:6px;">'
        'Format: Surname First-name Last-name &nbsp;•&nbsp; e.g. Salako Oluwatosin Daniel'
        '</div>',
        unsafe_allow_html=True,
    )
    full_name = st.text_input(
        "Full Name",
        placeholder="Enter your full name",
        label_visibility="collapsed",
    )

    st.markdown("**Date of birth:**")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        month_name = st.selectbox(
            "Month",
            ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"],
            label_visibility="collapsed",
        )
    with col2:
        day = st.selectbox("Day", list(range(1, 32)), label_visibility="collapsed")
    with col3:
        year = st.selectbox(
            "Year", list(range(date.today().year, 1949, -1)),
            label_visibility="collapsed",
        )

    phone = st.text_input("Phone Number", placeholder="e.g. 08144832008")
    email = st.text_input("Email", placeholder="e.g. myemail@gmail.com")

    consent = st.checkbox(
        "I agree that CampusEase Ezigbo may store my information to send me my "
        "attestation letter and future updates (e.g. birthday wishes)."
    )

    if st.button("Next  →"):
        if not full_name.strip():
            st.error("Please enter your full name.")
        elif not phone.strip():
            st.error("Please enter your phone number.")
        elif not email.strip() or "@" not in email:
            st.error("Please enter a valid email address.")
        elif not consent:
            st.error("Please tick the consent box to continue.")
        else:
            month_num = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December",
            ].index(month_name) + 1

            phone_clean = phone.strip()
            email_clean = email.strip().lower()

            existing = find_student(phone=phone_clean, email=email_clean)
            if existing:
                st.session_state.duplicate_student = existing
                st.session_state.step = 99
                st.rerun()
            else:
                new_row = create_student(
                    full_name=full_name.strip(),
                    dob_day=day,
                    dob_month=month_num,
                    dob_year=year,
                    phone=phone_clean,
                    email=email_clean,
                )
                st.session_state.profile = {
                    "id": new_row["id"],
                    "full_name": new_row["full_name"],
                    "dob_day": new_row["dob_day"],
                    "dob_month": new_row["dob_month"],
                    "dob_year": new_row["dob_year"],
                    "phone": new_row["phone"],
                    "email": new_row["email"],
                }
                st.session_state.step = 2
                st.rerun()

# ============================================================
# STEP 2 — LETTER DETAILS
# ============================================================
elif st.session_state.step == 2:
    st.markdown("## Letter Details")
    st.caption(f"Signed in as **{st.session_state.profile['full_name']}**")

    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

    course_name = st.text_input("Course / Department", placeholder="e.g. Computer Science")

    st.markdown("### Institution")
    inst_choice = st.selectbox("Select your institution", list(INSTITUTIONS.keys()))

    if INSTITUTIONS[inst_choice] is None:
        addressee_title = st.text_input("Addressee", value="The Registrar,")
        institution_name = st.text_input(
            "Institution Name", placeholder="e.g. Nnamdi Azikiwe University,"
        )
        campus_location = st.text_area(
            "Institution Address / Campus Location",
            placeholder="e.g. P.M.B. 5025, Awka,\nAnambra State, Nigeria.",
            height=100,
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

    st.markdown("### Parent / Guardian")
    parent_title = st.selectbox("Title", PARENT_TITLES)
    parent_name = st.text_input("Parent Full Name", placeholder="e.g. Ochiabuto Joseph")
    parent_address = st.text_area(
        "Parent Address",
        placeholder="12 Main Street,\nUmuahia,\nAbia State.",
        height=100,
    )

    letter_date = date.today().strftime("%d %B %Y")
    st.markdown(
        f'<div class="date-caption">{ICONS["calendar"]}Letter date:&nbsp;<strong>{letter_date}</strong>&nbsp;(auto-filled with today\'s date)</div>',
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("←  Back"):
            st.session_state.step = 1
            st.rerun()
    with col_b:
        if st.button("Generate My Letter"):
            required = [course_name, institution_name, campus_location,
                        parent_name, parent_address]
            if not all(x.strip() for x in required):
                st.error("Please fill in all fields.")
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
                    "letter_date": letter_date,
                }

                html = render_template("template_001.html", data)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp_path = tmp.name

                html_to_pdf(html, tmp_path)

                with open(tmp_path, "rb") as f:
                    st.session_state.pdf_bytes = f.read()

                Path(tmp_path).unlink(missing_ok=True)

                Path(tmp_path).unlink(missing_ok=True)

                create_letter_request(
                    student_id=st.session_state.profile["id"],
                    data=data,
                    template_used="template_001.html",
                )

                st.session_state.step = 3
                st.rerun()

# ============================================================
# STEP 3 — DOWNLOAD + LINK
# ============================================================
elif st.session_state.step == 3:
    st.markdown(
        f'## {ICONS["check"].replace("icon", "icon icon-lg")}Your Attestation Letter is Ready',
        unsafe_allow_html=True,
    )
    st.caption("Download it, print it, and get your parent/guardian to sign it.")

    if st.session_state.pdf_bytes:
        st.download_button(
            label="Download Attestation Letter (PDF)",
            data=st.session_state.pdf_bytes,
            file_name=f"{st.session_state.profile['full_name'].replace(' ', '_')}_Attestation.pdf",
            mime="application/pdf",
        )

    st.markdown("---")
    st.markdown("### Connect with us")

    st.markdown(
        f"""
        <div class="sig-card">
            <h4>Salako Oluwatosin Daniel</h4>
            <p><strong>&nbsp;Founder, CampusEase Ezigbo</strong></p>
            <p>{ICONS['phone']}08164961572, 08144832008</p>
            <p>{ICONS['mail']}daniel@campusease.ng</p>
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
            <p>{ICONS['chat']}WhatsApp: 08164961572, 08144832008</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="brand-footer">
            <p>{ICONS['arrow-right']}<a href="{CAMPUSEASE_WHATSAPP}" target="_blank">Chat with us on WhatsApp</a></p>
            <p class="tagline">No Stress. No Delay. We've Got You.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Generate another letter"):
        st.session_state.step = 1
        st.session_state.profile = {}
        st.session_state.pdf_bytes = None
        st.rerun()