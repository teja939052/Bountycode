"""
Lifecycle email engine.

Retention is the #1 ARR lever: a churned user never compounds into revenue.
These emails fire at the prime conversion moments — welcome (signup),
trial-start, and limit-hit (the exact instant a free user feels the pain).

SMTP is optional. When unconfigured (dev/test), every email is appended to
data/email_outbox.log so the flow is observable and never crashes the app.
A failed send is logged but NEVER propagates to the caller (a broken email
must not break a signup or a feature action).
"""
from __future__ import annotations

import os
import asyncio
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime, timezone

from app.config import get_settings

settings = get_settings()

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
OUTBOX_PATH = os.path.join(_DATA_DIR, "email_outbox.log")

FRONTEND_URL = settings.CORS_ORIGINS.split(",")[0].strip().rstrip("/") if settings.CORS_ORIGINS else "http://localhost:5173"
PRICING_URL = f"{FRONTEND_URL}/pricing"


def _brand() -> str:
    return (
        '<p style="font-family:monospace;color:#38bdf8;font-size:18px;font-weight:bold;'
        'margin:0 0 16px">PlacementPro</p>'
    )


def _button(label: str, url: str) -> str:
    return (
        f'<a href="{url}" style="display:inline-block;background:#38bdf8;color:#0b1020;'
        f'font-weight:bold;text-decoration:none;padding:12px 22px;border-radius:10px;'
        f'font-family:sans-serif;font-size:15px">{label}</a>'
    )


def _wrap(inner: str) -> str:
    return (
        "<div style='max-width:520px;margin:0 auto;padding:24px;"
        "background:#0b1020;color:#e5e7eb;font-family:sans-serif'>"
        f"{_brand()}{inner}"
        "<p style='margin-top:24px;font-size:12px;color:#64748b'>"
        "You received this because you signed up at PlacementPro.</p>"
        "</div>"
    )


def welcome_email(name: str):
    subject = "Welcome to PlacementPro — your first AI interview is 60 seconds away"
    inner = (
        f"<h1 style='font-size:20px;margin:0 0 12px'>Hi {name or 'there'}, you're in.</h1>"
        "<p style='line-height:1.5'>PlacementPro gives you unlimited AI mock interviews, "
        "resume optimization, and 53 company-specific prep kits. Most users land their "
        "first actionable feedback within 5 minutes.</p>"
        "<p style='margin:20px 0'>" + _button("Start your first interview", f"{FRONTEND_URL}/interview") + "</p>"
        "<p style='line-height:1.5;color:#94a3b8'>Free includes 3 interviews + 3 resume reviews a month. "
        "When you're ready for unlimited, " + _button("see Pro plans", PRICING_URL) + "</p>"
    )
    return subject, _wrap(inner)


def trial_started_email(name: str, days: int = 7):
    subject = f"Your PlacementPro Pro trial is live — {days} days of unlimited practice"
    inner = (
        f"<h1 style='font-size:20px;margin:0 0 12px'>Hi {name or 'there'}, you now have Pro.</h1>"
        "<p style='line-height:1.5'>Everything is unlocked for the next "
        f"{days} days: unlimited AI interviews, resume optimization, system design, "
        "coding challenges, and salary negotiation coaching.</p>"
        "<p style='margin:20px 0'>" + _button("Make the most of Pro", f"{FRONTEND_URL}/dashboard") + "</p>"
        "<p style='line-height:1.5;color:#94a3b8'>We'll remind you before it ends. "
        "No card was charged. " + _button("Keep Pro after the trial", PRICING_URL) + "</p>"
    )
    return subject, _wrap(inner)


def limit_reached_email(name: str, feature: str):
    feature_label = feature.replace("_", " ").title()
    subject = f"You've hit your free {feature_label} limit — upgrade to keep going"
    inner = (
        f"<h1 style='font-size:20px;margin:0 0 12px'>Hi {name or 'there'}, that's your last free one.</h1>"
        f"<p style='line-height:1.5'>You just used your free <b>{feature_label}</b> for this month. "
        "The users who improve fastest are the ones who practice without limits.</p>"
        "<p style='margin:20px 0'>" + _button("Unlock unlimited — Upgrade to Pro", PRICING_URL) + "</p>"
        "<p style='line-height:1.5;color:#94a3b8'>Pro is $19/mo (yearly $99). Your monthly limits reset, "
        "but your progress doesn't have to wait.</p>"
    )
    return subject, _wrap(inner)


def trial_expired_email(name: str):
    subject = "Your PlacementPro trial ended — keep your momentum with Pro"
    inner = (
        f"<h1 style='font-size:20px;margin:0 0 12px'>Hi {name or 'there'}, your trial just ended.</h1>"
        "<p style='line-height:1.5'>You had unlimited practice for a week. Users who keep a daily "
        "streak are the ones who walk into real interviews calm and prepared.</p>"
        "<p style='margin:20px 0'>" + _button("Continue with Pro — $19/mo", PRICING_URL) + "</p>"
        "<p style='line-height:1.5;color:#94a3b8'>Yearly is $99 (less than $8.25/mo). No gap in your progress.</p>"
    )
    return subject, _wrap(inner)


async def send_email(to: str, subject: str, html: str, text: str | None = None) -> bool:
    if not to:
        return False

    # Always log (audit trail + dev visibility) before attempting SMTP.
    try:
        os.makedirs(_DATA_DIR, exist_ok=True)
        with open(OUTBOX_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.now(timezone.utc).isoformat()} TO:{to} SUBJ:{subject} ---\n{html}\n")
    except Exception:
        pass

    if not settings.SMTP_HOST:
        return True  # dev/test fallback: logged only

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to
        msg.set_content(text or "View this email in your browser.")
        msg.add_alternative(html, subtype="html")
        await asyncio.to_thread(_smtp_send, msg)
        return True
    except Exception as exc:  # never break the caller
        try:
            with open(OUTBOX_PATH, "a", encoding="utf-8") as f:
                f.write(f"\n[SMTP ERROR] {datetime.now(timezone.utc).isoformat()} {exc!r}\n")
        except Exception:
            pass
        return False


def _smtp_send(msg: EmailMessage) -> None:
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
        if settings.SMTP_PORT == 465:
            ctx = ssl.create_default_context()
            server.starttls(context=ctx)
        elif settings.SMTP_PORT not in (25,):
            server.starttls()
        if settings.SMTP_USER:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
