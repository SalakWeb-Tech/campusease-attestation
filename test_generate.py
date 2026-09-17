# test_generate.py
# Quick test: sample data → render template → generate PDF.

from pathlib import Path
from template_engine import render_template
from pdf_generator import html_to_pdf

# --- Sample data (this is what the form will collect later) ---
sample_data = {
    "student_name": "Victor Ochiabuto",
    "gender": "Male",                       # "Male" or "Female"
    "course_name": "Computer Science",
    "institution_name": "University of Nigeria, Nsukka",
    "campus_location": "Enugu State",
    "parent_title": "Mr.",
    "parent_name": "Ochiabuto Joseph",
    "parent_address": "12 Main Street,\nUmuahia,\nAbia State.",
    "letter_date": "16th September 2026",
    "addressee_title": "The Registrar,",
}

# --- Render HTML ---
html = render_template("template_001.html", sample_data)

# --- Generate PDF ---
output_dir = Path("generated")
output_dir.mkdir(exist_ok=True)
output_pdf = output_dir / "test_letter.pdf"

html_to_pdf(html, str(output_pdf))

print(f"✅ PDF created: {output_pdf.resolve()}")