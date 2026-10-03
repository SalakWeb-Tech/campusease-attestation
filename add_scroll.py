with open("app.py", "r") as f:
    src = f.read()

# ---------- 1. Add the scroll_to_top() helper after ICONS ----------
helper_marker = "# ============================================================\n# STYLING\n# ============================================================"

scroll_helper = '''# ============================================================
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


'''

if "def scroll_to_top" not in src and helper_marker in src:
    src = src.replace(helper_marker, scroll_helper + helper_marker, 1)
    print("[1/2] Added scroll_to_top() helper")
else:
    print("[1/2] scroll_to_top() already present or marker missing")

# ---------- 2. Call scroll_to_top() at the start of each step ----------
# We add it right after each "if st.session_state.step == X:" or "elif ..."
calls = [
    (
        'if st.session_state.step == 1:\n    st.markdown("## Sign Up")',
        'if st.session_state.step == 1:\n    scroll_to_top()\n    st.markdown("## Sign Up")'
    ),
    (
        'elif st.session_state.step == 2:\n    st.markdown("## Letter Details")',
        'elif st.session_state.step == 2:\n    scroll_to_top()\n    st.markdown("## Letter Details")'
    ),
    (
        'elif st.session_state.step == 25:\n    st.markdown("## Preview Your Letter")',
        'elif st.session_state.step == 25:\n    scroll_to_top()\n    st.markdown("## Preview Your Letter")'
    ),
    (
        'elif st.session_state.step == 26:\n    st.markdown("## One Last Step")',
        'elif st.session_state.step == 26:\n    scroll_to_top()\n    st.markdown("## One Last Step")'
    ),
    (
        'elif st.session_state.step == 100:\n',
        'elif st.session_state.step == 100:\n    scroll_to_top()\n'
    ),
    (
        'elif st.session_state.step == 99:\n    existing = st.session_state.duplicate_student',
        'elif st.session_state.step == 99:\n    scroll_to_top()\n    existing = st.session_state.duplicate_student'
    ),
]

applied = 0
for old, new in calls:
    if old in src and "scroll_to_top()\n    st.markdown" not in src[src.find(old):src.find(old)+len(old)+50]:
        if old in src:
            # Don't double-add
            if "scroll_to_top()" not in src[src.find(old):src.find(old)+len(old)+80]:
                src = src.replace(old, new, 1)
                applied += 1

print(f"[2/2] Added scroll_to_top() to {applied} step(s)")

with open("app.py", "w") as f:
    f.write(src)

print("\nDone. Run: python3 -m py_compile app.py")
