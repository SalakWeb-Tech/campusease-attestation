def html_to_pdf_with_instructions(letter_html: str, instructions_html: str, output_path: str):
    """Convert the letter + instructions HTML to a single PDF with 2 pages.
    Page 1 = letter, Page 2 = instructions.
    Both HTML strings are complete HTML documents."""
    import tempfile
    from pathlib import Path
    from pypdf import PdfWriter, PdfReader

    # Render each HTML into its own PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix="_letter.pdf") as f1:
        letter_pdf = f1.name
    with tempfile.NamedTemporaryFile(delete=False, suffix="_instructions.pdf") as f2:
        instructions_pdf = f2.name

    html_to_pdf(letter_html, letter_pdf)
    html_to_pdf(instructions_html, instructions_pdf)

    # Merge page 1 (letter) + page 2 (instructions)
    writer = PdfWriter()
    writer.append(PdfReader(letter_pdf))
    writer.append(PdfReader(instructions_pdf))
    writer.write(output_path)
    writer.close()

    # Cleanup temp files
    Path(letter_pdf).unlink(missing_ok=True)
    Path(instructions_pdf).unlink(missing_ok=True)# pdf_generator.py
# Uses Playwright (headless Chromium) to convert HTML -> A4 PDF.
# Auto-shrinks content so every letter fits on ONE page.
# Auto-installs the Chromium browser binary on first run (Streamlit Cloud).

import os
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

_MARKER = Path("/tmp/.playwright_ready")

if not _MARKER.exists():
    try:
        subprocess.run(
            ["playwright", "install", "chromium"],
            check=True, capture_output=True, timeout=300,
        )
        _MARKER.touch()
    except Exception:
        try:
            subprocess.run(
                ["python", "-m", "playwright", "install", "chromium"],
                check=True, capture_output=True, timeout=300,
            )
            _MARKER.touch()
        except Exception:
            pass


def html_to_pdf(html_content: str, output_path: str) -> str:
    """Render HTML as a single-page A4 PDF. Auto-shrinks to fit."""
    output_path = str(Path(output_path).resolve())

    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")

        # Auto-fit to one page: reduce font-size, then scale if needed
        page.evaluate("""() => {
            const MAX_HEIGHT_PX = 1080;
            const body = document.body;

            // Try reducing the base font size first
            let attempts = 0;
            while (body.scrollHeight > MAX_HEIGHT_PX && attempts < 40) {
                const current = parseFloat(getComputedStyle(body).fontSize);
                if (current <= 9) break;
                body.style.fontSize = (current - 0.5) + 'px';
                attempts++;
            }

            // If still too tall, scale the whole body down
            if (body.scrollHeight > MAX_HEIGHT_PX) {
                const scale = MAX_HEIGHT_PX / body.scrollHeight;
                body.style.transform = 'scale(' + scale + ')';
                body.style.transformOrigin = 'top left';
                body.style.width = (100 / scale) + '%';
            }
        }""")

        page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={"top": "10mm", "right": "12mm", "bottom": "10mm", "left": "12mm"},
        )
        browser.close()

    return output_path
