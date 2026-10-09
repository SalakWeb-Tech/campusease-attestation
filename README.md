---
title: CampusEase Attestation
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
---

# CampusEase Ezigbo — Attestation Letter Generator

An automated attestation letter generator for Nigerian university freshers.

## Features

- Fast, free attestation letter generation
- Personalised attester (Parent, Guardian, Pastor, Imam)
- Automatic pronouns (he/she, him/her)
- Compare two letter versions
- Email verification before download
- 2-page PDF (letter + instructions)
- Hidden admin panel

## Tech Stack

- Streamlit (frontend + backend)
- Supabase (PostgreSQL)
- Playwright (PDF)
- Jinja2 (templates)
- Gmail SMTP (email)

## Local Development

1. Clone this repository
2. Create venv: `python3 -m venv venv && source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Add `.env` with credentials
5. Run: `streamlit run app.py`
