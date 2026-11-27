"""Exam memory routes — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from app.middleware.auth import get_current_user, require_admin
from app.database import get_session
from app.services.gamification import record_practice
import hashlib
import json
import logging
import re
from pathlib import Path

router = APIRouter(prefix="/api/v1/exam-memories", tags=["exam-memories"])

VERIFY_THRESHOLD = 5
DAILY_SUBMIT_CAP = 5
MIN_QUESTION_LENGTH = 15

BACKEND_ROOT = Path(__file__).resolve().parents[2]
APPROVED_BANK = BACKEND_ROOT / "app" / "data" / "exam_memory_approved.json"

EXAMS = {
    "tcs_nqt": "TCS NQT",
    "tcs_ipa": "TCS IPA",
    "infytq": "Infosys InfyTQ",
    "wipro_nlth": "Wipro NLTH",
    "accenture": "Accenture",
    "cognizant_genc": "Cognizant GenC",
    "capgemini_amcat": "Capgemini",
    "ibm_entry": "IBM",
    "amazon_sde": "Amazon SDE",
    "google": "Google",
    "microsoft": "Microsoft",
    "other": "Other",
}

SECTIONS = {
    "tcs_nqt": ["aptitude", "logical", "verbal", "cs_fundamentals", "coding"],
    "tcs_ipa": ["aptitude", "logical", "verbal", "cs_fundamentals", "coding"],
    "infytq": ["aptitude", "logical", "cs_fundamentals", "coding"],
    "wipro_nlth": ["aptitude", "logical", "verbal", "coding"],
    "accenture": ["aptitude", "logical", "verbal", "coding"],
    "cognizant_genc": ["aptitude", "logical", "verbal", "coding"],
    "capgemini_amcat": ["aptitude", "logical", "verbal", "coding"],
    "ibm_entry": ["aptitude", "logical", "verbal", "coding"],
}
GENERIC_SECTIONS = ["aptitude", "logical", "verbal", "cs_fundamentals", "coding", "other"]


def _iso(v):
    return v.isoformat() if isinstance(v, datetime) else (v or "")


def _normalize(text: str) -> str:
    if not text:
        return ""
    t = text.lower()
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[^a-z0-9%+\-/>\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _fingerprint(exam: str, section: str, text: str) -> str:
    norm = _normalize(text)
    if not norm:
        return ""
    return hashlib.sha1(f"{exam}|{section}|{norm[:120]}".encode("utf-8")).hexdigest()


@router.post("")
async def submit_exam_memory(body: dict, user=Depends(get_current_user)):
    """Submit a remembered exam question. Dedupes by canonical fingerprint."""
    exam = str(body.get("exam", "")).strip().lower()
    if exam not in EXAMS:
        raise HTTPException(status_code=400, detail=f"exam must be one of {list(EXAMS.keys())}")
    section = str(body.get("section", "")).strip().lower()
    if section not in SECTIONS.get(exam, GENERIC_SECTIONS):
        raise HTTPException(status_code=400, detail=f"section must be one of {SECTIONS.get(exam, GENERIC_SECTIONS)} for exam '{exam}'")
    question_text = str(body.get("question_text", "")).strip()
    if len(question_text) < MIN_QUESTION_LENGTH:
        raise HTTPException(status_code=400, detail=f"question_text must be at least {MIN_QUESTION_LENGTH} characters")
    topic = str(body.get("topic", "")).strip()[:80]
    fmt = str(body.get("format", "mcq")).strip().lower() or "mcq"
    if fmt not in ("mcq", "code", "verbal"):
        raise HTTPException(status_code=400, detail="format must be mcq, code, or verbal")
    options = body.get("options") if isinstance(body.get("options"), list) else []
    options = [str(o).strip()[:500] for o in options if str(o).strip()][:8]
    known_answer = str(body.get("known_answer", "")).strip()[:1000]
    notes = str(body.get("notes", "")).strip()[:1000]

    today = datetime.now(timezone.utc).date().isoformat()
    async with get_session() as session:
        from app.models.exam_memory import ExamMemory
        count_result = await session.execute(
            select(func.count()).select_from(ExamMemory).where(
                ExamMemory.user_id == user["id"],
                ExamMemory.day == today
            )
        )
        count = count_result.scalar_one() or 0
        if count >= DAILY_SUBMIT_CAP:
            raise HTTPException(status_code=429, detail=f"Daily submission limit reached ({DAILY_SUBMIT_CAP}/day)")

        fp = _fingerprint(exam, section, question_text)
        now = datetime.now(timezone.utc)
        uid = user["id"]

        if fp:
            result = await session.execute(
                select(ExamMemory).where(ExamMemory.fingerprint == fp)
            )
            existing = result.scalar_one_or_none()
            if existing:
                reporters = set(existing.reporters or [])
                if uid in reporters:
                    existing.question_text = question_text
                    existing.options = options
                    existing.known_answer = known_answer
                    existing.notes = notes
                    existing.updated_at = now
                    await session.commit()
                    return {"id": str(existing.id), "duplicate": True, "note": "Already reported by you; updated your recollection."}
                reporters.add(uid)
                new_count = len(reporters)
                status = "verified_crowd" if new_count >= VERIFY_THRESHOLD else existing.status
                if status == "verified_crowd" and existing.status != "verified_crowd":
                    status = "verified_crowd"
                await session.execute(
                    update(ExamMemory)
                    .where(ExamMemory.id == existing.id)
                    .values(
                        report_count=new_count,
                        reporters=list(reporters),
                        status=status,
                        question_text=question_text,
                        options=options,
                        known_answer=known_answer,
                        notes=notes,
                        updated_at=now,
                    )
                )
                refreshed = await session.execute(
                    select(ExamMemory).where(ExamMemory.id == existing.id)
                )
                refreshed = refreshed.scalar_one()
                reward = None
                if uid not in existing.rewarded_reporters:
                    reward = await _reward_submission(uid, exam, section)
                    if reward:
                        await session.execute(
                            update(ExamMemory)
                            .where(ExamMemory.id == existing.id)
                            .values(rewarded_reporters=[*existing.rewarded_reporters, uid])
                        )
                return {
                    **_serialize(refreshed), "duplicate": True,
                    "reward": reward,
                    "verified_crowd": status == "verified_crowd",
                    "note": (f"{VERIFY_THRESHOLD} independent reports reached — flagged for review."
                             if status == "verified_crowd" else
                             f"{new_count}/{VERIFY_THRESHOLD} independent reports so far."),
                }

        memory_id = str(uuid.uuid4())
        doc = ExamMemory(
            id=memory_id,
            user_id=uid,
            exam=exam,
            section=section,
            topic=topic,
            question_text=question_text,
            format=fmt,
            options=options,
            known_answer=known_answer,
            notes=notes,
            fingerprint=fp,
            reporters=[uid],
            report_count=1,
            status="new",
            day=today,
            created_at=now,
            updated_at=now,
        )
        session.add(doc)
        await session.commit()
        reward = await _reward_submission(uid, exam, section)
        return {
            "id": memory_id,
            "exam": exam,
            "section": section,
            "topic": topic,
            "question_text": question_text,
            "format": fmt,
            "options": options,
            "known_answer": known_answer,
            "notes": notes,
            "fingerprint": fp,
            "reporters": [uid],
            "report_count": 1,
            "status": "new",
            "day": today,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "duplicate": False,
            "reward": reward,
            "note": "Submitted for review. 5+ independent reports auto-flag this for the admin queue.",
        }