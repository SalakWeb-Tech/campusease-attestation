# pdf_generator.py
# Uses Playwright (headless Chromium) to convert HTML → A4 PDF.

from pathlib import Path
from playwright.sync_api import sync_playwright


def html_to_pdf(html_content: str, output_path: str) -> str:
    """Render HTML string as A4 PDF and save to output_path."""
    output_path = str(Path(output_path).resolve())

    with sync_playwright() as p:
        browser = p.chromium.launch()
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