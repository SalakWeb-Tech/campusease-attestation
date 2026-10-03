# email_sender.py
import os
import smtplib
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from database import supabase

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def is_email_used(email: str) -> bool:
    """Return True if this email has already downloaded a letter."""
    try:
        r = supabase.table("downloads").select("id").eq("email", email.lower()).execute()
        return bool(r.data)
    except Exception:
        return False


def generate_and_send_code(student_id: str, email: str) -> dict:
    """Generate 6-digit code, store in DB, send via email."""
    email = email.lower().strip()

    if is_email_used(email):
        return {"ok": False, "error": "This email has already been used to download a letter."}

    code = f"{secrets.randbelow(1000000):06d}"
    code_hash = _hash_code(code)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    # Invalidate old codes for this student
    supabase.table("verification_codes").delete().eq("student_id", student_id).eq("verified", False).execute()

    # Insert new code
    supabase.table("verification_codes").insert({
        "student_id": student_id,
        "email": email,
        "code_hash": code_hash,
        "expires_at": expires_at.isoformat(),
    }).execute()

    # Send email
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "CampusEase — Your Verification Code"
        msg["From"] = f"CampusEase Ezigbo <{SMTP_EMAIL}>"
        msg["To"] = email

        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 520px; margin: 0 auto;">
            <div style="background: #0B1F4B; padding: 24px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="color: #F5B301; margin: 0; font-size: 22px;">CampusEase Ezigbo</h1>
                <p style="color: #FFF; margin: 6px 0 0 0; font-size: 13px;">No Stress. No Delay. We've Got You.</p>
            </div>
            <div style="background: #FFF; padding: 28px; border: 1px solid #E5E9F0; border-top: none; border-radius: 0 0 8px 8px;">
                <p style="color: #333; font-size: 15px;">Your verification code to download your attestation letter:</p>
                <div style="text-align: center; margin: 24px 0;">
                    <span style="display: inline-block; font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #0B1F4B; background: #EEF4FF; padding: 16px 32px; border-radius: 8px; border-left: 4px solid #F5B301;">
                        {code}
                    </span>
                </div>
                <p style="color: #666; font-size: 13px;">This code expires in <strong>10 minutes</strong>. Do not share it with anyone.</p>
                <p style="color: #666; font-size: 13px;">If you did not request this, please ignore this email.</p>
            </div>
        </div>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": f"Failed to send email: {e}"}


def verify_code(student_id: str, entered_code: str) -> dict:
    """Verify the 6-digit code. Returns {ok: True} or {ok: False, error: ...}."""
    now = datetime.now(timezone.utc).isoformat()

    r = supabase.table("verification_codes") \
        .select("*") \
        .eq("student_id", student_id) \
        .eq("verified", False) \
        .gt("expires_at", now) \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()

    if not r.data:
        return {"ok": False, "error": "No active code. Please request a new one."}

    row = r.data[0]

    if row["attempts"] >= 3:
        return {"ok": False, "error": "Too many wrong attempts. Please request a new code."}

    if _hash_code(entered_code) != row["code_hash"]:
        supabase.table("verification_codes").update(
            {"attempts": row["attempts"] + 1}
        ).eq("id", row["id"]).execute()
        remaining = 3 - (row["attempts"] + 1)
        return {"ok": False, "error": f"Invalid code. {remaining} attempt(s) left."}

    # Success — mark verified and record the download lock
    supabase.table("verification_codes").update({"verified": True}).eq("id", row["id"]).execute()

    try:
        supabase.table("downloads").insert({
            "email": row["email"],
            "student_id": student_id,
        }).execute()
    except Exception:
        return {"ok": False, "error": "This email has already been used."}

    return {"ok": True, "email": row["email"]}
