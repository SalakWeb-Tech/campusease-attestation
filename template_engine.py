# template_engine.py
# Combines a random layout + a random body, and injects student data + pronouns.

import os
import random
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

from pronouns import get_pronouns
from letter_bodies import LETTER_BODIES

TEMPLATES_DIR = Path(__file__).parent / "templates"
LAYOUTS_DIR = TEMPLATES_DIR / "layouts"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


def _body_to_html(body_text: str) -> str:
    """Convert a plain-text body (with blank lines between paragraphs)
    into HTML paragraphs."""
    paragraphs = [p.strip() for p in body_text.strip().split("\n\n") if p.strip()]
    return "\n".join(f"<p>{p}</p>" for p in paragraphs)


def _pick_layout_name() -> str:
    """Return a random layout filename."""
    files = sorted([f for f in os.listdir(LAYOUTS_DIR) if f.endswith(".html")])
    if not files:
        raise RuntimeError("No layouts found in templates/layouts/")
    return random.choice(files)


def render_letter(data: dict, body_id: int = None, layout_name: str = None) -> tuple:
    """Render a full letter by combining a random body + a random layout.

    If body_id and layout_name are given, uses them (for consistency across previews).
    Otherwise, picks randomly.

    Returns (html_string, body_id_used, layout_name_used).
    """
    # 1. Get pronouns for the selected gender
    pronouns = get_pronouns(data["gender"])
    context = {
        **data,
        **pronouns,
        # Bold the student's name wherever {{student_name}} is used in a body
        "student_name": f"<strong>{data['student_name']}</strong>",
    }

    # 2. Pick a body (or use the given one)
    if body_id is None:
        chosen = random.choice(LETTER_BODIES)
    else:
        chosen = next((b for b in LETTER_BODIES if b["id"] == body_id), LETTER_BODIES[0])

    body_text = chosen["body"]

    # 3. Render the body text with Jinja (pronouns + student data)
    body_rendered = Template(body_text).render(**context)

    # 4. Convert to HTML paragraphs
    body_html = _body_to_html(body_rendered)

    # 5. Pick a layout (or use the given one)
    if layout_name is None:
        layout_name = _pick_layout_name()

    layout = env.get_template(f"layouts/{layout_name}")

    # 6. Render the layout with body_content and all context
    html = layout.render(**context, body_content=body_html)

    return html, chosen["id"], layout_name