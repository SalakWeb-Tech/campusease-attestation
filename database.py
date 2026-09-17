# database.py
# Supabase helpers: duplicate check + insert student + insert letter request.

import os
from dotenv import load_dotenv

load_dotenv()

# On Streamlit Cloud, secrets come from st.secrets; locally, from .env
try:
    import streamlit as st
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))
except Exception:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY.")

from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def find_student(phone: str = None, email: str = None):
    """Return the existing student row if phone OR email matches, else None."""
    result = None
    if phone:
        r = supabase.table("students").select("*").eq("phone", phone).limit(1).execute()
        if r.data:
            result = r.data[0]
    if not result and email:
        r = supabase.table("students").select("*").eq("email", email).limit(1).execute()
        if r.data:
            result = r.data[0]
    return result


def create_student(full_name, dob_day, dob_month, dob_year, phone, email):
    """Insert a new student and return the row (with id)."""
    payload = {
        "full_name": full_name,
        "dob_day": dob_day,
        "dob_month": dob_month,
        "dob_year": dob_year,
        "phone": phone,
        "email": email,
    }
    r = supabase.table("students").insert(payload).execute()
    return r.data[0]


def create_letter_request(student_id, data: dict, template_used: str):
    """Insert a letter request record."""
    payload = {
        "student_id": student_id,
        "gender": data["gender"],
        "course_name": data["course_name"],
        "institution_name": data["institution_name"],
        "campus_location": data["campus_location"],
        "addressee_title": data["addressee_title"],
        "parent_title": data["parent_title"],
        "parent_name": data["parent_name"],
        "parent_address": data["parent_address"],
        "letter_date": data["letter_date"],
        "template_used": template_used,
    }
    r = supabase.table("letter_requests").insert(payload).execute()
    return r.data[0]