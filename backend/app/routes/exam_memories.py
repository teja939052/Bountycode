"""
Exam memory crowd-sourcing loop (ethical content moat).

Students who just took a real assessment can submit questions they remember.
These submissions are STUDENT STATE (like question_reports) and live in Mongo
as recollection instances — they are never served to other students directly.
Content enters the servable bank ONLY through the trust pipeline:

    new -> verified_crowd (≥ VERIFY_THRESHOLD independent reports)
         -> approved (human admin sign-off = HUMAN_REVIEWED stamp)
         -> written to app/data/exam_memory_approved.json
         -> loaded at startup by question_store as a verified extra bank.

Residency Rule (AGENTS.md): the *approved* canonical question content lives in
the file bank, never in Mongo. Mongo holds the student recollections plus the
review status/dedup counters only.
"""
from datetime import datetime, timezone, timedelta
import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from app.middleware.auth import get_current_user, require_admin
from app.database import exam_memories_collection, users_collection
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/exam-memories", tags=["exam-memories"])

# Independent reports on the same canonical fingerprint needed to auto-flag a
# recollection as verified_crowd (PrepInsta/FACE Prep model: multiple students
# independently report the same question => high confidence). Configurable per
# deployment; 5 matches the spec'd "5+ students report the same question".
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

MOCK_KEYS = {"id", "question", "options", "correct_index", "correct_answer", "reasoning_steps"}


def _iso(v):
    return v.isoformat() if isinstance(v, datetime) else (v or "")


def _normalize(text: str) -> str:
    """Normalize recollection text for fingerprinting: lowercase, strip
    punctuation, collapse whitespace. Robust to copy/paste variance."""
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
    # First 120 chars are discriminating enough for dedup; the full normalized
    # text is kept on the doc for human review.
    return hashlib.sha1(f"{exam}|{section}|{norm[:120]}".encode("utf-8")).hexdigest()


def _serialize(m) -> dict:
    m.pop("_id", None)
    return {
        "id": str(m.get("memory_id", "")),
        "exam": m.get("exam", ""),
        "exam_name": EXAMS.get(m.get("exam", ""), m.get("exam", "")),
        "section": m.get("section", ""),
        "topic": m.get("topic", ""),
        "question_text": m.get("question_text", ""),
        "format": m.get("format", "mcq"),
        "options": m.get("options", []),
        "known_answer": m.get("known_answer", ""),
        "notes": m.get("notes", ""),
        "status": m.get("status", "new"),
        "report_count": m.get("report_count", 1),
        "created_at": _iso(m.get("created_at")),
        "updated_at": _iso(m.get("updated_at")),
    }


async def _reward_submission(user_id: str, exam: str, section: str) -> dict:
    """Law-compliant contributor reward. The ONLY writer of Diamonds/coins is
    record_practice() (Gamification Law #1); badges are string IDs hydrated on
    read (Law #6). Ours is just the per-submission award call."""
    try:
        res = await record_practice(
            user_id,
            "exam_memory",
            score=8,
            metadata={
                "action": "submit_exam_memory",
                "exam": exam,
                "section": section,
            },
        )
        return {
            "xp_gained": res.get("xp_gained", 0),
            "coins_earned": res.get("coins_earned", 0),
            "new_badges": [
                {"id": b.get("id"), "name": b.get("name"), "icon": b.get("icon")}
                for b in (res.get("new_badges") or [])
            ],
            "new_streak": res.get("new_streak"),
            "level_up": res.get("level_up", False),
        }
    except Exception as exc:
        logging.getLogger(__name__).warning(
            f"exam_memory reward skipped for user {user_id}: {exc}"
        )
        return {}


async def _find_section_or_400(req_body: dict) -> str:
    section = str(req_body.get("section", "")).strip().lower()
    exam = str(req_body.get("exam", "")).strip().lower()
    allowed = SECTIONS.get(exam, GENERIC_SECTIONS)
    if section not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"section must be one of {allowed} for exam '{exam}'",
        )
    return section


@router.post("")
async def submit_exam_memory(body: dict, user=Depends(get_current_user)):
    """Submit a remembered exam question. Dedupes by canonical fingerprint;
    the 5th independent report auto-flags the recollection as verified_crowd.
    Content is never served from here — admin approval promotes it to the
    file-based bank via the trust pipeline."""
    exam = str(body.get("exam", "")).strip().lower()
    if exam not in EXAMS:
        raise HTTPException(status_code=400, detail=f"exam must be one of {list(EXAMS.keys())}")
    section = await _find_section_or_400(body)
    question_text = str(body.get("question_text", "")).strip()
    if len(question_text) < MIN_QUESTION_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"question_text must be at least {MIN_QUESTION_LENGTH} characters",
        )
    topic = str(body.get("topic", "")).strip()[:80]
    fmt = str(body.get("format", "mcq")).strip().lower() or "mcq"
    if fmt not in ("mcq", "code", "verbal"):
        raise HTTPException(status_code=400, detail="format must be mcq, code, or verbal")
    options = body.get("options") if isinstance(body.get("options"), list) else []
    options = [str(o).strip()[:500] for o in options if str(o).strip()][:8]
    known_answer = str(body.get("known_answer", "")).strip()[:1000]
    notes = str(body.get("notes", "")).strip()[:1000]

    # Per-user daily cap (spam blunting; no email verification exists — P3).
    today = datetime.now(timezone.utc).date().isoformat()
    if await exam_memories_collection.count_documents(
            {"user_id": user["id"], "day": today}) >= DAILY_SUBMIT_CAP:
        raise HTTPException(status_code=429, detail=f"Daily submission limit reached ({DAILY_SUBMIT_CAP}/day)")

    fp = _fingerprint(exam, section, question_text)
    now = datetime.now(timezone.utc)
    uid = user["id"]

    if fp:
        existing = await exam_memories_collection.find_one({"fingerprint": fp})
        if existing:
            reporters = set(existing.get("reporters", []))
            if uid in reporters:
                # Same student re-submitting: update their recollection text
                # but do not inflate the report count.
                await exam_memories_collection.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {
                        "question_text": question_text,
                        "options": options,
                        "known_answer": known_answer,
                        "notes": notes,
                        "updated_at": now,
                    }},
                )
                refreshed = await exam_memories_collection.find_one({"_id": existing["_id"]})
                return {**_serialize(refreshed), "duplicate": True,
                        "note": "Already reported by you; updated your recollection."}
            reporters.add(uid)
            new_count = len(reporters)
            status = "verified_crowd" if new_count >= VERIFY_THRESHOLD else existing.get("status", "new")
            if status == "verified_crowd" and existing.get("status") != "verified_crowd":
                status = "verified_crowd"
            await exam_memories_collection.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "report_count": new_count,
                    "reporters": list(reporters),
                    "status": status,
                    "question_text": question_text,
                    "options": options,
                    "known_answer": known_answer,
                    "notes": notes,
                    "updated_at": now,
                }},
            )
            refreshed = await exam_memories_collection.find_one({"_id": existing["_id"]})
            if uid not in existing.get("rewarded_reporters", []):
                reward = await _reward_submission(uid, exam, section)
                if reward:
                    await exam_memories_collection.update_one(
                        {"_id": existing["_id"]},
                        {"$addToSet": {"rewarded_reporters": uid}},
                    )
            else:
                reward = None
            return {**_serialize(refreshed), "duplicate": True,
                    "reward": reward,
                    "verified_crowd": status == "verified_crowd",
                    "note": (f"{VERIFY_THRESHOLD} independent reports reached — flagged for review."
                             if status == "verified_crowd" else
                             f"{new_count}/{VERIFY_THRESHOLD} independent reports so far.")}

    doc = {
        "user_id": uid,
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
        "created_at": now,
        "updated_at": now,
    }
    res = await exam_memories_collection.insert_one(doc)
    doc["_id"] = res.inserted_id
    memory_id = str(res.inserted_id)
    await exam_memories_collection.update_one(
        {"_id": res.inserted_id}, {"$set": {"memory_id": memory_id}})
    doc["memory_id"] = memory_id
    reward = await _reward_submission(uid, exam, section)
    return {**_serialize(doc), "duplicate": False,
            "reward": reward,
            "note": "Submitted for review. 5+ independent reports auto-flag this for the admin queue."}


@router.get("/mine")
async def my_exam_memories(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    """Submissions by the current user (newest first)."""
    total = await exam_memories_collection.count_documents({"user_id": user["id"]})
    cursor = exam_memories_collection.find({"user_id": user["id"]}) \
        .sort("created_at", -1).skip((page - 1) * limit).limit(limit)
    rows = []
    async for m in cursor:
        rows.append(_serialize(m))
    return {"memories": rows, "total": total, "page": page, "pages": (total + limit - 1) // limit}


@router.get("/heatmap")
async def exam_memories_heatmap(
    days: int = Query(7, ge=1, le=30),
    user=Depends(get_current_user),
):
    """Real-question heatmap for the last N days: exam x section submission
    volume + the most-reported recollections.

    Content trust rule: recollections still under review (new/verified_crowd)
    are aggregated as COUNTS ONLY — their raw text is never exposed to other
    students. Only human-approved recollections (status == approved, stamped by
    a reviewer) return their question text.
    """
    since = datetime.now(timezone.utc) - timedelta(days=days)
    q = {
        "created_at": {"$gte": since},
        "status": {"$in": ["new", "verified_crowd", "approved"]},
    }
    total = await exam_memories_collection.count_documents(q)

    by_section = []
    cursor = exam_memories_collection.aggregate([
        {"$match": q},
        {"$group": {
            "_id": {"exam": "$exam", "section": "$section"},
            "submissions": {"$sum": 1},
            "reports": {"$sum": "$report_count"},
            "verified_crowd": {
                "$sum": {"$cond": [{"$eq": ["$status", "verified_crowd"]}, 1, 0]}
            },
            "approved": {
                "$sum": {"$cond": [{"$eq": ["$status", "approved"]}, 1, 0]}
            },
        }},
        {"$sort": {"submissions": -1}},
        {"$limit": 30},
    ])
    async for row in cursor:
        by_section.append({
            "exam": row["_id"]["exam"],
            "exam_name": EXAMS.get(row["_id"]["exam"], row["_id"]["exam"]),
            "section": row["_id"]["section"],
            "submissions": row["submissions"],
            "reports": row["reports"],
            "verified_crowd": row["verified_crowd"],
            "approved": row["approved"],
        })

    by_exam = {}
    for row in by_section:
        acc = by_exam.setdefault(row["exam"], {
            "exam": row["exam"],
            "exam_name": row["exam_name"],
            "submissions": 0,
            "reports": 0,
            "verified_crowd": 0,
            "approved": 0,
        })
        acc["submissions"] += row["submissions"]
        acc["reports"] += row["reports"]
        acc["verified_crowd"] += row["verified_crowd"]
        acc["approved"] += row["approved"]
    by_exam = sorted(by_exam.values(), key=lambda r: r["submissions"], reverse=True)

    hot: list = []
    hot_cursor = exam_memories_collection.find(q) \
        .sort("report_count", -1).limit(20)
    async for m in hot_cursor:
        attested = max(
            (m.get("report_count") or 1),
            len(m.get("reporters") or []),
        )
        row = {
            "memory_id": str(m.get("memory_id", "")) or str(m["_id"]),
            "exam": m.get("exam", ""),
            "exam_name": EXAMS.get(m.get("exam", ""), m.get("exam", "")),
            "section": m.get("section", ""),
            "topic": m.get("topic", ""),
            "report_count": attested,
            "status": m.get("status", "new"),
            "reviewed": m.get("status") == "approved",
        }
        if m.get("status") == "approved":
            # Human-reviewed content only: expose the recollection text.
            row["question_text"] = m.get("question_text", "")
        hot.append(row)
        if len(hot) >= 10:
            break

    return {
        "window_days": days,
        "since": since.isoformat(),
        "total_submissions": total,
        "by_section": by_section,
        "by_exam": by_exam,
        "hot_questions": hot,
        "verify_threshold": VERIFY_THRESHOLD,
    }


@router.get("/config")
async def exam_memories_config(user=Depends(get_current_user)):
    """Menu of supported exams + sections for the submission form."""
    return {
        "exams": [{"id": k, "name": v} for k, v in EXAMS.items()],
        "sections": GENERIC_SECTIONS,
        "verify_threshold": VERIFY_THRESHOLD,
        "daily_cap": DAILY_SUBMIT_CAP,
    }


# ---------------------------------------------------------------------------
# Admin review (human sign-off = HUMAN_REVIEWED stamp)
# ---------------------------------------------------------------------------
def _require_review_fields(body: dict):
    correct_index = body.get("correct_index")
    if correct_index is None and "correct_answer" not in body:
        raise HTTPException(status_code=400, detail="correct_index (or correct_answer) is required to promote")
    reasoning = body.get("reasoning", body.get("reasoning_steps", ""))
    if not str(reasoning).strip() and not (body.get("known_answer") or ""):
        raise HTTPException(status_code=400, detail="reasoning (verification trail) is required to promote")


async def _write_approved_bank(new_items: list) -> int:
    existing = []
    if APPROVED_BANK.exists():
        try:
            existing = json.loads(APPROVED_BANK.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except Exception:
            existing = []
    have = {str(q.get("id")) for q in existing if isinstance(q, dict)}
    added = 0
    for item in new_items:
        if str(item.get("id")) not in have:
            existing.append(item)
            have.add(str(item.get("id")))
            added += 1
    APPROVED_BANK.write_text(json.dumps(existing, indent=1), encoding="utf-8")
    return added


@router.get("/admin/review")
async def admin_exam_memories(
    status: Optional[str] = Query(None),
    exam: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    admin=Depends(require_admin),
):
    """Admin review queue. Filter by status (new | verified_crowd | approved |
    dismissed). Verified_crowd items are the priority queue."""
    query = {}
    if status and status in ("new", "verified_crowd", "approved", "dismissed"):
        query["status"] = status
    if exam and exam in EXAMS:
        query["exam"] = exam
    total = await exam_memories_collection.count_documents(query)
    cursor = exam_memories_collection.find(query) \
        .sort("created_at", 1).skip((page - 1) * limit).limit(limit)
    rows = []
    async for m in cursor:
        row = _serialize(m)
        row["reporters"] = m.get("reporters", [])
        row["reviewed_by"] = m.get("reviewed_by", "")
        row["reviewed_at"] = _iso(m.get("reviewed_at"))
        rows.append(row)
    return {
        "memories": rows,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "threshold": VERIFY_THRESHOLD,
    }


@router.post("/admin/{memory_id}/promote")
async def promote_exam_memory(memory_id: str, body: dict, admin=Depends(require_admin)):
    """Admin promotes a recollection into the servable bank.

    The admin identity IS the HUMAN_REVIEWED stamp (No-LLM Bank Rule): they
    supply/confirm the correct answer + an independent reasoning trail. The
    curated item is appended to exam_memory_approved.json (served at startup),
    never stored as served content in Mongo.
    """
    m = await exam_memories_collection.find_one({"memory_id": memory_id})
    if not m:
        raise HTTPException(status_code=404, detail="Memory not found")
    await _require_review_fields(body)

    correct_index = body.get("correct_index")
    correct_answer = body.get("correct_answer", m.get("known_answer", ""))
    reasoning = str(body.get("reasoning", "")).strip() or str(m.get("known_answer", "")).strip()

    now = datetime.now(timezone.utc)
    reviewer = f"{admin.get('email', '')}:{now.date().isoformat()}"

    import uuid as _uuid
    qid = f"exam-memory-{_uuid.uuid4().hex[:12]}"
    item = {
        "id": qid,
        "type": body.get("type", "aptitude"),
        "topic": m.get("topic") or body.get("topic", ""),
        "sub_topic": body.get("sub_topic", ""),
        "difficulty": body.get("difficulty", "medium"),
        "question": m.get("question_text", ""),
        "options": m.get("options", []),
        "correct_index": correct_index if correct_index is not None else 0,
        "correct_answer": correct_answer,
        "reasoning_steps": reasoning,
        "explanation": reasoning,
        "companies": [m.get("exam", "").replace("_", "-")],
        "provenance": f"student-memory:{m.get('exam', '')}:{m.get('section', '')}",
        "source_bank": "exam_memory_approved.json",
        "trust_status": "reviewed",
        "review_method": "admin_human_review_exam_memory_v1",
        "reviewed_by": reviewer,
        "reviewed_at": now.isoformat(),
        "verified_by_takers": max(
            (m.get("report_count") or 1),
            len(m.get("reporters") or []),
        ),
    }
    if item["topic"]:
        item["topic"] = item["topic"]
    if item["correct_index"] and isinstance(item["correct_index"], str):
        try:
            item["correct_index"] = int(item["correct_index"])
        except ValueError:
            raise HTTPException(status_code=400, detail="correct_index must be an integer")

    added = await _write_approved_bank([item])

    await exam_memories_collection.update_one(
        {"_id": m["_id"]},
        {"$set": {
            "status": "approved",
            "reviewed_by": reviewer,
            "reviewed_at": now,
            "promoted_question_id": qid,
            "updated_at": now,
        }},
    )
    try:
        from app.services.response_cache import invalidate_questions_cache
        await invalidate_questions_cache()
    except Exception:
        pass
    return {
        "memory_id": memory_id,
        "status": "approved",
        "promoted_question_id": qid,
        "added": added,
        "note": "Reviewed by human admin. Served after backend restart (in-memory bank reloads from file).",
    }


@router.post("/admin/{memory_id}/dismiss")
async def dismiss_exam_memory(memory_id: str, body: dict, admin=Depends(require_admin)):
    """Dismiss a recollection (duplicate, fabricated, off-topic, incomplete)."""
    reason = str(body.get("reason", "")).strip()[:500]
    if not reason:
        raise HTTPException(status_code=400, detail="reason is required to dismiss")
    m = await exam_memories_collection.find_one({"memory_id": memory_id})
    if not m:
        raise HTTPException(status_code=404, detail="Memory not found")
    now = datetime.now(timezone.utc)
    await exam_memories_collection.update_one(
        {"_id": m["_id"]},
        {"$set": {
            "status": "dismissed",
            "dismiss_reason": reason,
            "dismissed_by": admin.get("email", ""),
            "dismissed_at": now,
            "updated_at": now,
        }},
    )
    return {"memory_id": memory_id, "status": "dismissed", "reason": reason}