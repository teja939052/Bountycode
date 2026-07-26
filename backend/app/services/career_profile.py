"""
Career Profile service — the single source of truth for all application data.
Powers the Apply Copilot concept without requiring a browser extension.
"""

from __future__ import annotations

import re
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from bson import ObjectId

from app.config import get_settings
from app.database import users_collection, career_profiles_collection, resumes_collection
from app.services.ai import chat_completion, parse_json
from app.services.resume_parser import extract_text_from_pdf

logger = logging.getLogger(__name__)
settings = get_settings()


# ── AI parsing prompt ────────────────────────────────────────────────────────

_PROFILE_PARSE_PROMPT = """
You are an expert resume parser. Extract structured career data from the resume text below.

Return ONLY valid JSON with this exact schema:
{
  "full_name": "",
  "contact": {
    "email": "", "phone": "", "location": "", "linkedin": "", "github": "", "website": ""
  },
  "summary": "",
  "skills": [""],
  "experience": [
    {
      "title": "", "company": "", "location": "", "start_date": "", "end_date": "",
      "current": false, "bullets": [""]
    }
  ],
  "education": [
    {
      "school": "", "degree": "", "field": "", "start_year": "", "end_year": "",
      "gpa": "", "highlights": [""]
    }
  ],
  "projects": [
    {
      "name": "", "description": "", "tech_stack": [""], "link": "", "highlights": [""]
    }
  ],
  "certifications": [
    {
      "name": "", "issuer": "", "date": "", "expiry": "", "credential_id": ""
    }
  ]
}

Rules:
- Fill every field; use "" if not found.
- Normalize dates to YYYY or YYYY-MM.
- Bullets should be single action verbs + result.
- Skills should be individual tokens (e.g. "Python", "React", "AWS").
- Do NOT hallucinate. If unsure, leave blank.
"""


# ── Core helpers ─────────────────────────────────────────────────────────────

def _serialize_profile(doc: dict) -> Dict[str, Any]:
    if not doc:
        return {}
    doc["id"] = str(doc.pop("_id"))
    return doc


async def _get_or_create_profile(user_id: str) -> dict:
    existing = await career_profiles_collection.find_one({"user_id": user_id})
    if existing:
        return existing
    doc = {
        "user_id": user_id,
        "full_name": "",
        "contact": {},
        "summary": "",
        "skills": [],
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": [],
        "custom_sections": {},
        "source": "manual",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = await career_profiles_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


# ── Public API ───────────────────────────────────────────────────────────────

async def get_profile(user_id: str) -> Dict[str, Any]:
    doc = await _get_or_create_profile(user_id)
    return _serialize_profile(doc)


async def update_profile(user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    doc = await _get_or_create_profile(user_id)
    allowed_fields = {
        "full_name", "contact", "summary", "skills",
        "experience", "education", "projects", "certifications", "custom_sections",
    }
    updates = {k: v for k, v in payload.items() if k in allowed_fields and v is not None}
    updates["updated_at"] = datetime.now(timezone.utc)

    if updates:
        await career_profiles_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": updates},
        )

    refreshed = await career_profiles_collection.find_one({"_id": doc["_id"]})
    return _serialize_profile(refreshed)


async def parse_resume_to_profile(
    user_id: str,
    pdf_bytes: Optional[bytes] = None,
    resume_text: Optional[str] = None,
    resume_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Parse a resume (PDF or raw text) into a structured Career Profile.
    Uses AI extraction when text is ambiguous; falls back to regex heuristics.
    """
    text = resume_text
    source = "manual"
    if pdf_bytes:
        text = extract_text_from_pdf(pdf_bytes)
        source = "resume_upload"

    if not text or not text.strip():
        raise ValueError("No resume text provided")

    # Try AI parse
    parsed: Dict[str, Any] = {}
    try:
        result = await chat_completion(
            messages=[
                {"role": "system", "content": _PROFILE_PARSE_PROMPT},
                {"role": "user", "content": text},
            ],
            use_cache=True,
            max_tokens=3000,
        )
        parsed = parse_json(result) or {}
    except Exception as exc:
        logger.warning("AI profile parse failed, using heuristics: %s", exc)
        parsed = _heuristic_parse(text)

    # Merge into profile
    profile_payload = {
        "full_name": parsed.get("full_name", ""),
        "contact": parsed.get("contact", {}),
        "summary": parsed.get("summary", ""),
        "skills": parsed.get("skills", []),
        "experience": parsed.get("experience", []),
        "education": parsed.get("education", []),
        "projects": parsed.get("projects", []),
        "certifications": parsed.get("certifications", []),
        "source": source,
        "resume_id": resume_id,
        "updated_at": datetime.now(timezone.utc),
    }

    doc = await _get_or_create_profile(user_id)
    await career_profiles_collection.update_one(
        {"_id": doc["_id"]},
        {"$set": profile_payload},
    )
    refreshed = await career_profiles_collection.find_one({"_id": doc["_id"]})
    return _serialize_profile(refreshed)


async def append_section_item(
    user_id: str,
    section: str,
    item: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Append a single item to a profile section (experience, education, project, certification).
    Used by Apply Copilot and manual entry.
    """
    doc = await _get_or_create_profile(user_id)
    section_key = section.lower().rstrip("s") + "s"  # normalize plurals
    if section_key not in {"experiences", "education", "projects", "certifications"}:
        raise ValueError(f"Unsupported section: {section}")

    await career_profiles_collection.update_one(
        {"_id": doc["_id"]},
        {"$push": {section_key: item}},
    )
    refreshed = await career_profiles_collection.find_one({"_id": doc["_id"]})
    return _serialize_profile(refreshed)


async def delete_section_item(
    user_id: str,
    section: str,
    index: int,
) -> Dict[str, Any]:
    doc = await _get_or_create_profile(user_id)
    section_key = section.lower().rstrip("s") + "s"
    if section_key not in {"experiences", "education", "projects", "certifications"}:
        raise ValueError(f"Unsupported section: {section}")

    section_items = doc.get(section_key, [])
    if index < 0 or index >= len(section_items):
        raise ValueError("Index out of range")

    await career_profiles_collection.update_one(
        {"_id": doc["_id"]},
        {"$unset": {f"{section_key}.{index}": 1}},
    )
    # MongoDB leaves a null hole; pull nulls
    await career_profiles_collection.update_one(
        {"_id": doc["_id"]},
        {"$pull": {section_key: None}},
    )
    refreshed = await career_profiles_collection.find_one({"_id": doc["_id"]})
    return _serialize_profile(refreshed)


# ── Heuristic fallback parser ────────────────────────────────────────────────

_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
_PHONE_RE = re.compile(r"(\+?\d[\d\-\(\) ]{7,}\d)")
_URL_RE = re.compile(r"https?://\S+|github\.com/\S+|linkedin\.com/in/\S+")


def _heuristic_parse(text: str) -> Dict[str, Any]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    emails = _EMAIL_RE.findall(text)
    phones = _PHONE_RE.findall(text)
    urls = _URL_RE.findall(text)

    contact = {
        "email": emails[0] if emails else "",
        "phone": phones[0] if phones else "",
        "location": "",
        "linkedin": next((u for u in urls if "linkedin" in u), ""),
        "github": next((u for u in urls if "github" in u), ""),
        "website": next((u for u in urls if not any(x in u for x in ["linkedin", "github"])), ""),
    }

    # Very rough section extraction
    skills: List[str] = []
    experience: List[Dict[str, Any]] = []
    education: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []

    lower = text.lower()
    for keyword, target in [
        ("python", "Python"), ("javascript", "JavaScript"), ("java", "Java"),
        ("react", "React"), ("node", "Node.js"), ("sql", "SQL"),
        ("aws", "AWS"), ("docker", "Docker"), ("kubernetes", "Kubernetes"),
        ("fastapi", "FastAPI"), ("django", "Django"), ("flask", "Flask"),
        ("mongodb", "MongoDB"), ("postgresql", "PostgreSQL"), ("redis", "Redis"),
        ("git", "Git"), ("ci/cd", "CI/CD"), ("microservices", "Microservices"),
        ("tensorflow", "TensorFlow"), ("pytorch", "PyTorch"), ("machine learning", "Machine Learning"),
    ]:
        if keyword in lower and target not in skills:
            skills.append(target)

    return {
        "full_name": lines[0] if lines else "",
        "contact": contact,
        "summary": "",
        "skills": skills[:20],
        "experience": experience,
        "education": education,
        "projects": projects,
        "certifications": [],
    }
