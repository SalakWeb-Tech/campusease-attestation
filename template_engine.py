# template_engine.py
# Combines a random layout + a random body, and injects student data + pronouns.
# Bodies tagged with "requires" only appear when the parent's title matches.

import base64
import os
import random
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

from pronouns import get_pronouns
from letter_bodies import LETTER_BODIES

TEMPLATES_DIR = Path(__file__).parent / "templates"
LAYOUTS_DIR = TEMPLATES_DIR / "layouts"
ASSETS_DIR = Path(__file__).parent / "assets"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)

CHRISTIAN_TITLES = {
    "Pastor", "Rev.", "Rev. Fr.", "Very Rev.", "Ven.",
    "Evang.", "Apostle", "Bishop", "Prophet",
}

MUSLIM_TITLES = {
    "Imam", "Alhaji", "Hajia",
}


def _body_to_html(body_text: str) -> str:
    paragraphs = [p.strip() for p in body_text.strip().split("\n\n") if p.strip()]
    return "\n".join(f"<p>{p}</p>" for p in paragraphs)


def _pick_layout_name() -> str:
    files = sorted([f for f in os.listdir(LAYOUTS_DIR) if f.endswith(".html")])
    if not files:
        raise RuntimeError("No layouts found in templates/layouts/")
    return random.choice(files)


def _eligible_bodies(parent_title: str) -> list:
    if parent_title in CHRISTIAN_TITLES:
        return [b for b in LETTER_BODIES if b.get("requires") in (None, "christian")]
    if parent_title in MUSLIM_TITLES:
        return [b for b in LETTER_BODIES if b.get("requires") in (None, "muslim")]
    return [b for b in LETTER_BODIES if b.get("requires") is None]


def _get_logo_data_uri() -> str:
    logo_path = ASSETS_DIR / "logo.png"
    if not logo_path.exists():
        return ""
    with open(logo_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def render_letter(data: dict, body_id: int = None, layout_name: str = None) -> tuple:
    pronouns = get_pronouns(data["gender"])
    context = {
        **data,
        **pronouns,
        "student_name": f"<strong>{data['student_name']}</strong>",
        "logo_data_uri": _get_logo_data_uri(),
    }

    eligible = _eligible_bodies(data.get("parent_title", ""))

    if body_id is not None:
        chosen = next((b for b in eligible if b["id"] == body_id), None)
        if chosen is None:
            chosen = random.choice(eligible)
    else:
        chosen = random.choice(eligible)

    body_text = chosen["body"]
    body_rendered = Template(body_text).render(**context)
    body_html = _body_to_html(body_rendered)

    if layout_name is None:
        layout_name = _pick_layout_name()

    layout = env.get_template(f"layouts/{layout_name}")
    html = layout.render(**context, body_content=body_html)

    return html, chosen["id"], layout_name