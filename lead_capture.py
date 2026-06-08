"""lead_capture — durable lead pipeline shared across the fleet.

On a booking submission: (1) EMAIL the lead to the owner's Gmail (primary, guaranteed delivery),
and (2) best-effort store it in the fleet Supabase `leads` table. Both wrapped so a failure
never breaks the request. Secrets come from env vars (set on Render), never committed.

Env: GMAIL_ADDRESS, GMAIL_APP_PASSWORD, LEAD_NOTIFY_EMAIL,
     LEADS_SUPABASE_URL, LEADS_SUPABASE_KEY (service_role)."""
import os, ssl, json, smtplib, urllib.request
from email.message import EmailMessage

GMAIL_USER = os.environ.get("GMAIL_ADDRESS", "")
GMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD", "")
NOTIFY = os.environ.get("LEAD_NOTIFY_EMAIL", "") or GMAIL_USER
SB_URL = os.environ.get("LEADS_SUPABASE_URL", "").rstrip("/")
SB_KEY = os.environ.get("LEADS_SUPABASE_KEY", "")
_CORE = ("name", "email", "phone", "company", "message", "source")


def _email(site, lead):
    if not (GMAIL_USER and GMAIL_PASS and NOTIFY):
        return False
    msg = EmailMessage()
    who = lead.get("name") or lead.get("email") or lead.get("phone") or "inquiry"
    msg["Subject"] = f"🍩 New {site} booking: {who}"
    msg["From"] = GMAIL_USER
    msg["To"] = NOTIFY
    if lead.get("email") and "@" in lead["email"]:
        msg["Reply-To"] = lead["email"]
    body = "\n".join(f"{k}: {v}" for k, v in lead.items() if v and k != "ip")
    msg.set_content(f"New booking request from {site}:\n\n{body}\n")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(), timeout=15) as s:
        s.login(GMAIL_USER, GMAIL_PASS)
        s.send_message(msg)
    return True


def _store(site, lead):
    if not (SB_URL and SB_KEY):
        return False
    row = {"site": site}
    for k in _CORE:
        if lead.get(k):
            row[k] = lead[k]
    extra = {k: v for k, v in lead.items() if k not in _CORE and k != "ip" and v}
    if extra:
        row["meta"] = extra
    req = urllib.request.Request(
        f"{SB_URL}/rest/v1/leads", data=json.dumps(row).encode(), method="POST",
        headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
                 "Content-Type": "application/json", "Prefer": "return=minimal"})
    urllib.request.urlopen(req, timeout=10)
    return True


def capture(site, lead):
    """Email + store a lead. Returns {emailed, stored}; never raises."""
    out = {"emailed": False, "stored": False}
    try:
        out["emailed"] = _email(site, lead)
    except Exception as e:
        print(f"[lead_capture] email failed: {str(e)[:140]}")
    try:
        out["stored"] = _store(site, lead)
    except Exception as e:
        print(f"[lead_capture] store failed: {str(e)[:140]}")
    return out
