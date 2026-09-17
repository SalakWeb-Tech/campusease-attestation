# template_engine.py
# Loads an HTML template and injects student data + pronouns.

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pronouns import get_pronouns

TEMPLATES_DIR = Path(__file__).parent / "templates"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_template(template_name: str, data: dict) -> str:
    """Render an HTML template with student data + gender pronouns."""
    # 1. Validate gender and fetch pronouns
    pronouns = get_pronouns(data["gender"])

    # 2. Merge pronouns into the data (so templates can use them directly)
    context = {**data, **pronouns}

    # 3. Load and render
    template = env.get_template(template_name)
    return template.render(**context)