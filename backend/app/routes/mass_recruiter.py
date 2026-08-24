"""
Mass Recruitor Exam Simulator — NQT-style sectioned papers for Indian service
companies. Builds timed multi-section exams from the aptitude question banks,
applies per-company negative marking, and stores results in the shared
`aptitude_tests` collection so history/stats/readiness pick them up.
"""
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.database import (
    aptitude_tests_collection,
    aptitude_leaderboard_collection,
)
from app.middleware.auth import get_current_user
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/mass-recruiter", tags=["mass-recruiter"])


def _section(name: str, category: str, questions: int, minutes: int) -> Dict:
    return {
        "name": name,
        "category": category,
        "questions": questions,
        "minutes": minutes,
    }


# Realistic section structures inspired by public NQT/InfyTQ/NLTH/GenC patterns.
EXAM_CONFIGS: Dict[str, Dict] = {
    "tcs_nqt": {
        "name": "TCS NQT",
        "description": "Foundation pattern: numerical, verbal and reasoning ability.",
        "cutoff_pct": 65,
        "negative_marks": 0.0,
        "xp_per_question": 10,
        "sections": [
            _section("Numerical Ability", "quantitative", 20, 25),
            _section("Verbal Ability", "verbal", 15, 15),
            _section("Reasoning Ability", "logical", 15, 20),
        ],
    },
    "infosys_infytq": {
        "name": "Infosys InfyTQ",
        "description": "Aptitude gate: quant-heavy mix with strong reasoning filter.",
        "cutoff_pct": 65,
        "negative_marks": 0.25,
        "xp_per_question": 10,
        "sections": [
            _section("Quantitative Aptitude", "quantitative", 15, 20),
            _section("Logical Reasoning", "logical", 10, 15),
            _section("Verbal Ability", "verbal", 10, 12),
        ],
    },
    "wipro_nlth": {
        "name": "Wipro NLTH",
        "description": "Elite NTH pattern: balanced trio under tight time pressure.",
        "cutoff_pct": 60,
        "negative_marks": 0.0,
        "xp_per_question": 10,
        "sections": [
            _section("Quantitative Aptitude", "quantitative", 14, 16),
            _section("Reasoning Ability", "logical", 14, 16),
            _section("Verbal Ability", "verbal", 12, 14),
        ],
    },
    "accenture": {
        "name": "Accenture",
        "description": "Cognitive + technical screen with negative marking.",
        "cutoff_pct": 60,
        "negative_marks": 0.25,
        "xp_per_question": 12,
        "sections": [
            _section("Quantitative Aptitude", "quantitative", 15, 18),
            _section("Logical Reasoning", "logical", 15, 18),
            _section("Verbal Ability", "verbal", 12, 14),
        ],
    },
    "cognizant_genc": {
        "name": "Cognizant GenC",
        "description": "GenC screening: speed round across all three abilities.",
        "cutoff_pct": 60,
        "negative_marks": 0.0,
        "xp_per_question": 10,
        "sections": [
            _section("Quantitative Aptitude", "quantitative", 12, 14),
            _section("Reasoning Ability", "logical", 12, 14),
            _section("Verbal Ability", "verbal", 12, 14),
        ],
    },
}

_POOL_ATTRS = [
    ("APTITUDE_PROBLEMS", "scripts.aptitude_problems"),
    ("APTITUDE_BATCH2", "scripts.aptitude_batch2"),
    ("APTITUDE_BATCH3", "scripts.aptitude_batch3"),
    ("APTITUDE_BATCH4", "scripts.aptitude_batch4"),
    ("APTITUDE_FINAL", "scripts.aptitude_final"),
    ("APTITUDE_EXTRA", "scripts.aptitude_extra"),
    ("APTITUDE_FINAL_BATCH", "scripts.aptitude_final_batch"),
    ("APTITUDE_ULTRA", "scripts.aptitude_ultra"),
    ("APTITUDE_ULTIMATE", "scripts.aptitude_ultimate"),
]

_CATEGORY_SUBS = {
    "quantitative": ["Percentages", "Profit and Loss", "Time and Work",
                     "Speed Distance Time", "Averages", "Simple Interest",
                     "Compound Interest", "Ratios", "Number Systems",
                     "Permutations", "Probability", "Mixture and Alligation"],
    "logical": ["Series", "Coding-Decoding", "Blood Relations",
                "Seating Arrangement", "Syllogisms", "Puzzles",
                "Direction Sense", "Clock Problems"],
    "verbal": ["Synonyms", "Antonyms", "Grammar", "Reading Comprehension",
               "Sentence Correction", "Idioms and Phrases",
               "One Word Substitution"],
}


def _load_pool(category: str) -> List[Dict]:
    """Load all aptitude questions matching a top-level category."""
    import importlib

    pool: List[Dict] = []
    for attr, module_name in _POOL_ATTRS:
        try:
            items = getattr(importlib.import_module(module_name), attr)
        except Exception:
            continue
        for q in items:
            if q.get("category") == category or q.get("sub_category", "") in _CATEGORY_SUBS.get(category, []):
                pool.append(q)
    return pool


class StartExam(BaseModel):
    exam_id: str


@router.get("/exams")
async def list_exams():
    """Available company exam blueprints."""
    exams = []
    for exam_id, cfg in EXAM_CONFIGS.items():
        total_q = sum(s["questions"] for s in cfg["sections"])
        total_min = sum(s["minutes"] for s in cfg["sections"])
        exams.append({
            "exam_id": exam_id,
            "name": cfg["name"],
            "description": cfg["description"],
            "total_questions": total_q,
            "total_minutes": total_min,
            "sections": [
                {"name": s["name"], "questions": s["questions"], "minutes": s["minutes"]}
                for s in cfg["sections"]
            ],
            "negative_marks": cfg["negative_marks"],
            "cutoff_pct": cfg["cutoff_pct"],
        })
    return {"exams": exams}


@router.post("/start")
async def start_exam(req: StartExam, user=Depends(get_current_user)):
    """Build a sectioned exam paper. Answers are NOT revealed during the exam."""
    cfg = EXAM_CONFIGS.get(req.exam_id)
    if not cfg:
        raise HTTPException(status_code=400, detail="Unknown exam_id")

    sections_for_client = []
    flat_questions = []  # ordered across sections, sent to client without answers
    question_ids: List[str] = []
    section_meta = []

    index_offset = 0
    for s_def in cfg["sections"]:
        pool = _load_pool(s_def["category"])
        n = min(s_def["questions"], len(pool))
        picked = random.sample(pool, n) if n > 0 else []

        start_idx = index_offset
        for q in picked:
            flat_questions.append({
                "id": q["id"],
                "question": q["question"],
                "options": q["options"],
                "category": q.get("category", s_def["category"]),
                "sub_category": q.get("sub_category", ""),
                "difficulty": q.get("difficulty", "medium"),
                "time_limit": q.get("time_limit", 60),
            })
            question_ids.append(q["id"])
            index_offset += 1

        section_meta.append({
            "name": s_def["name"],
            "category": s_def["category"],
            "start_index": start_idx,
            "end_index": index_offset - 1,
            "question_ids": [q["id"] for q in picked],
        })
        sections_for_client.append({
            "name": s_def["name"],
            "start_index": start_idx,
            "end_index": index_offset - 1,
            "count": len(picked),
            "minutes": s_def["minutes"],
        })

    if not flat_questions:
        raise HTTPException(status_code=500, detail="No questions available for this exam")

    now = datetime.now(timezone.utc)
    total_minutes = sum(s["minutes"] for s in cfg["sections"])
    ends_at = now + timedelta(minutes=total_minutes)

    test_doc = {
        "user_id": user["id"],
        "category": "mass_recruiter",
        "config": "mass_recruiter",
        "config_name": cfg["name"],
        "exam_id": req.exam_id,
        "sections": section_meta,
        "negative_marks": cfg["negative_marks"],
        "cutoff_pct": cfg["cutoff_pct"],
        "xp_per_question": cfg["xp_per_question"],
        "questions": flat_questions,
        "question_ids": question_ids,
        "answers": [],
        "status": "in_progress",
        "score": 0,
        "total_questions": len(flat_questions),
        "correct_answers": 0,
        "time_limit_minutes": total_minutes,
        "started_at": now,
        "ends_at": ends_at,
        "completed_at": None,
        "xp_earned": 0,
    }

    result = await aptitude_tests_collection().insert_one(test_doc)
    test_id = str(result.inserted_id)

    return {
        "test_id": test_id,
        "exam_id": req.exam_id,
        "exam_name": cfg["name"],
        "sections": sections_for_client,
        "questions": flat_questions,
        "total_questions": len(flat_questions),
        "total_minutes": total_minutes,
        "negative_marks": cfg["negative_marks"],
        "ends_at": ends_at.isoformat(),
        "message": f"{cfg['name']} started — {len(flat_questions)} questions in {total_minutes} minutes.",
    }


@router.post("/{test_id}/answer")
async def record_answer(
    test_id: str,
    question_index: int,
    answer: Optional[str] = None,
    marked: bool = False,
    time_taken: Optional[float] = None,
    user=Depends(get_current_user),
):
    """Save-or-update an answer. Exam mode: correctness is NOT revealed."""
    try:
        t_oid = ObjectId(test_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid test ID")

    test = await aptitude_tests_collection().find_one(
        {"_id": t_oid, "user_id": user["id"]}
    )
    if not test:
        raise HTTPException(status_code=404, detail="Exam not found")
    if test["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Exam is not in progress")
    if datetime.now(timezone.utc) > test["ends_at"]:
        await aptitude_tests_collection().update_one(
            {"_id": t_oid}, {"$set": {"status": "timed_out"}}
        )
        raise HTTPException(status_code=400, detail="Time is up!")

    entry = {
        "question_index": question_index,
        "question_id": test["question_ids"][question_index],
        "answer": answer,
        "marked": bool(marked),
        "time_taken": time_taken,
        "submitted_at": datetime.now(timezone.utc),
    }

    existing = test.get("answers", [])
    updated = [a for a in existing if a.get("question_index") != question_index]
    updated.append(entry)
    updated.sort(key=lambda a: a.get("question_index", 0))

    await aptitude_tests_collection().update_one(
        {"_id": t_oid}, {"$set": {"answers": updated}}
    )
    return {"recorded": True}


@router.post("/{test_id}/complete")
async def complete_exam(test_id: str, user=Depends(get_current_user)):
    """Grade with negative marking, produce section breakdown."""
    try:
        t_oid = ObjectId(test_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid test ID")

    test = await aptitude_tests_collection().find_one(
        {"_id": t_oid, "user_id": user["id"]}
    )
    if not test:
        raise HTTPException(status_code=404, detail="Exam not found")
    if test["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Exam already completed")

    id_to_q = {q["id"]: q for q in test.get("questions", [])}
    answers_by_index = {
        a.get("question_index"): a for a in test.get("answers", [])
    }

    negative = float(test.get("negative_marks", 0) or 0)
    correct = 0
    wrong = 0
    skipped = 0
    section_stats: Dict[str, Dict] = {}
    weak_areas: List[Dict] = []

    for idx, qid in enumerate(test["question_ids"]):
        full_q = id_to_q.get(qid, {})
        sec_name = next(
            (
                s["name"]
                for s in test.get("sections", [])
                if s["start_index"] <= idx <= s["end_index"]
            ),
            "General",
        )
        stats = section_stats.setdefault(
            sec_name, {"correct": 0, "wrong": 0, "skipped": 0, "total": 0}
        )
        stats["total"] += 1

        sub_cat = full_q.get("sub_category") or full_q.get("category") or "Unknown"
        sub_stats = next(
            (w for w in weak_areas if w["category"] == sub_cat), None
        )

        ans = answers_by_index.get(idx)
        given = (ans or {}).get("answer")
        if given is None or str(given).strip() == "":
            skipped += 1
            stats["skipped"] += 1
            if sub_stats is None:
                weak_areas.append({"category": sub_cat, "correct": 0, "total": 1})
            else:
                sub_stats["total"] += 1
            continue

        is_correct = (
            str(given).strip().lower()
            == str(full_q.get("correct_answer", "")).strip().lower()
        )
        if is_correct:
            correct += 1
            stats["correct"] += 1
            if sub_stats is None:
                weak_areas.append({"category": sub_cat, "correct": 1, "total": 1})
            else:
                sub_stats["correct"] += 1
                sub_stats["total"] += 1
        else:
            wrong += 1
            stats["wrong"] += 1
            if sub_stats is None:
                weak_areas.append({"category": sub_cat, "correct": 0, "total": 1})
            else:
                sub_stats["total"] += 1

    total = test["total_questions"]
    net_score = round(correct - (wrong * negative), 2)
    pct = round(correct / max(total, 1) * 100, 1)
    time_taken = 0
    if test.get("started_at"):
        time_taken = (datetime.now(timezone.utc) - test["started_at"]).total_seconds()

    xp_earned = max(int(correct * test.get("xp_per_question", 10)), 0)
    cutoff = float(test.get("cutoff_pct", 60))
    passed = pct >= cutoff

    await aptitude_tests_collection().update_one(
        {"_id": t_oid},
        {"$set": {
            "status": "completed",
            "score": pct,
            "net_score": net_score,
            "passed_cutoff": passed,
            "correct_answers": correct,
            "wrong_answers": wrong,
            "skipped_answers": skipped,
            "section_stats": section_stats,
            "time_taken": round(time_taken),
            "completed_at": datetime.now(timezone.utc),
            "xp_earned": xp_earned,
        }},
    )

    try:
        await record_practice(user["id"], "aptitude", pct)
    except Exception:
        pass

    # Leaderboard update mirrors aptitude_tests behavior
    try:
        lb = aptitude_leaderboard_collection()
        existing = await lb.find_one({"user_id": user["id"]})
        if existing:
            new_total = existing.get("total_tests", 0) + 1
            await lb.update_one(
                {"user_id": user["id"]},
                {"$set": {
                    "best_score": max(existing.get("best_score", 0), pct),
                    "avg_score": ((existing.get("avg_score", 0) * existing.get("total_tests", 0)) + pct) / new_total,
                    "total_tests": new_total,
                    "total_correct": existing.get("total_correct", 0) + correct,
                    "total_questions": existing.get("total_questions", 0) + total,
                    "last_test_at": datetime.now(timezone.utc),
                }},
            )
        else:
            await lb.insert_one({
                "user_id": user["id"],
                "user_name": user.get("name", "User"),
                "best_score": pct,
                "avg_score": pct,
                "total_tests": 1,
                "total_correct": correct,
                "total_questions": total,
                "last_test_at": datetime.now(timezone.utc),
            })
    except Exception:
        pass

    weak_areas = [
        {
            "category": w["category"],
            "accuracy": round(w["correct"] / max(w["total"], 1) * 100, 1),
            "solved": w["correct"],
            "total": w["total"],
        }
        for w in weak_areas
        if w["total"] > 0 and w["correct"] / max(w["total"], 1) < 0.6
    ]

    return {
        "test_id": test_id,
        "exam_name": test.get("config_name", "Mass Recruiter Exam"),
        "score": pct,
        "net_score": net_score,
        "passed_cutoff": passed,
        "cutoff_pct": cutoff,
        "correct_answers": correct,
        "wrong_answers": wrong,
        "skipped_answers": skipped,
        "negative_marks": negative,
        "total_questions": total,
        "time_taken": round(time_taken),
        "xp_earned": xp_earned,
        "section_stats": section_stats,
        "weak_areas": weak_areas[:8],
        "message": (
            f"Cleared the {cutoff:.0f}% cutoff."
            if passed
            else f"Below the {cutoff:.0f}% cutoff — drill the weak areas and re-run."
        ),
    }


@router.get("/history")
async def get_exam_history(
    limit: int = 20,
    user=Depends(get_current_user),
):
    """Past mass-recruiter exam attempts."""
    cursor = (
        aptitude_tests_collection()
        .find(
            {"user_id": user["id"], "category": "mass_recruiter", "status": "completed"},
            {"questions": 0, "answers": 0},
        )
        .sort("completed_at", -1)
        .limit(max(1, min(limit, 50)))
    )
    exams = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        exams.append(doc)
    return {"exams": exams, "total": len(exams)}
