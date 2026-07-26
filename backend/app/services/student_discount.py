"""
Student discount service — 50% off for .edu / .ac.in / .edu.in emails.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from bson import ObjectId
from app.database import users_collection, discounts_collection
from app.config import get_settings

settings = get_settings()

_STUDENT_DOMAINS = [
    r"\.edu$",
    r"\.edu\.[a-z]{2}$",
    r"\.ac\.in$",
    r"\.ac\.uk$",
    r"\.ac\.au$",
    r"\.edu\.au$",
    r"\.edu\.uk$",
    r"\.edu\.in$",
]

_DISCOUNT_PERCENT = 50
_DISCOUNT_DURATION_DAYS = 365


def _is_student_email(email: str) -> bool:
    if not email:
        return False
    domain = email.split("@")[-1].lower() if "@" in email else ""
    return any(re.search(p, domain) for p in _STUDENT_DOMAINS)


async def verify_student_discount(user_id: str, email: str) -> Dict[str, Any]:
    if not _is_student_email(email):
        return {
            "eligible": False,
            "reason": "Email must be from an educational institution (.edu, .ac.in, etc.)",
        }

    existing = await discounts_collection.find_one({
        "user_id": user_id,
        "type": "student",
        "status": "active",
    })
    if existing:
        return {
            "eligible": True,
            "discount_percent": _DISCOUNT_PERCENT,
            "message": "Student discount already active",
        }

    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user_id,
        "type": "student",
        "email": email,
        "discount_percent": _DISCOUNT_PERCENT,
        "status": "active",
        "expires_at": now + timedelta(days=_DISCOUNT_DURATION_DAYS),
        "created_at": now,
    }
    await discounts_collection.insert_one(doc)

    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"student_discount_active": True, "student_email": email}},
    )

    return {
        "eligible": True,
        "discount_percent": _DISCOUNT_PERCENT,
        "message": f"{_DISCOUNT_PERCENT}% student discount applied for {_DISCOUNT_DURATION_DAYS} days",
    }


async def get_student_discount_status(user_id: str) -> Dict[str, Any]:
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"active": False}

    if not user.get("student_discount_active"):
        return {"active": False}

    discount = await discounts_collection.find_one({
        "user_id": user_id,
        "type": "student",
        "status": "active",
    })
    if not discount:
        return {"active": False}

    now = datetime.now(timezone.utc)
    expires = discount.get("expires_at")
    if expires and expires < now:
        await discounts_collection.update_one(
            {"_id": discount["_id"]},
            {"$set": {"status": "expired"}},
        )
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"student_discount_active": False}},
        )
        return {"active": False, "expired": True}

    return {
        "active": True,
        "discount_percent": discount.get("discount_percent", _DISCOUNT_PERCENT),
        "expires_at": expires.isoformat() if expires else None,
    }
