# pdf_generator.py
# Uses Playwright (headless Chromium) to convert HTML -> A4 PDF.
# Auto-installs the Chromium browser binary on first run
# (needed for Streamlit Cloud, where the binary is not pre-installed).

import os
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

# --- Ensure Chromium is installed (runs once per container) ---
_MARKER = Path("/tmp/.playwright_ready")

if not _MARKER.exists():
    try:
        subprocess.run(
            ["playwright", "install", "chromium"],
            check=True,
            capture_output=True,
            timeout=300,
        )
        _MARKER.touch()
    except Exception as e:
        # Fallback: try python -m approach
        try:
            subprocess.run(
                ["python", "-m", "playwright", "install", "chromium"],
                check=True,
                capture_output=True,
                timeout=300,
            )
            _MARKER.touch()
        except Exception:
            pass  # will fail at launch time with clearer error


def html_to_pdf(html_content: str, output_path: str) -> str:
    """Render HTML string as A4 PDF and save to output_path."""
    output_path = str(Path(output_path).resolve())

    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()

    return output_path