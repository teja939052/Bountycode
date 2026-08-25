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
    "tcs_nqt_full": {
        "name": "TCS NQT Full Simulation",
        "description": (
            "The exact 190-minute gauntlet: Foundation (Part A) then Advanced "
            "(Part B). LOCKED like the real thing - once you leave a question, "
            "you cannot return."
        ),
        "cutoff_pct": 65,
        "negative_marks": 0.0,
        "xp_per_question": 10,
        "locked": True,
        "sections": [
            {
                "name": "Numerical Ability",
                "category": "quantitative",
                "questions": 15,
                "minutes": 25,
                "part": "Part A - Foundation",
            },
            {
                "name": "Reasoning Ability",
                "category": "logical",
                "questions": 15,
                "minutes": 25,
                "part": "Part A - Foundation",
            },
            {
                "name": "Verbal Ability",
                "category": "verbal",
                "questions": 12,
                "minutes": 20,
                "part": "Part A - Foundation",
            },
            {
                "name": "Professional Email Writing",
                "special": "email",
                "minutes": 6,
                "part": "Part A - Foundation",
            },
            {
                "name": "Advanced Aptitude",
                "category": "quantitative",
                "questions": 10,
                "difficulty": "hard",
                "minutes": 24,
                "part": "Part B - Advanced",
            },
            {
                "name": "Advanced Coding",
                "special": "coding",
                "count": 2,
                "minutes": 90,
                "part": "Part B - Advanced",
            },
        ],
    },
}

# Subjective/special task definitions for tcs_nqt_full.
EMAIL_TASK_PROMPT = (
    "You lead a four-member team delivering a module to a client on Friday. "
    "On Wednesday evening you discover a defect that will push delivery back "
    "by one full day.\n\n"
    "Write a professional email to your project manager (Mr. Sharma) informing "
    "them of the delay. Cover: what happened, the impact, your recovery plan, "
    "and the revised commitment.\n\nKeep it between 120 and 180 words."
)

CODING_TASKS = [
    {
        "id_suffix": "c1",
        "difficulty_label": "Easy-Medium (35 min)",
        "prompt": (
            "Rotate Array\n\n"
            "Given an array arr[] of n integers and an integer k, rotate the "
            "array to the right by k steps. n can be up to 10^5, k up to 10^9.\n\n"
            "Example:\narr = [1,2,3,4,5,6,7], k = 3\nResult: [5,6,7,1,2,3,4]\n\n"
            "Aim for O(n) time, O(1) extra space."
        ),
        "expected_approach": (
            "Reversal algorithm: reverse whole array, then reverse first k and "
            "last n-k segments. Or cyclic replacement."
        ),
    },
    {
        "id_suffix": "c2",
        "difficulty_label": "Medium-Hard (55 min)",
        "prompt": (
            "Minimum Platforms\n\n"
            "Given arrival[] and departure[] times of n trains (same day, "
            "n up to 5*10^4), find the minimum number of platforms the station "
            "needs so no train waits.\n\n"
            "Example:\narr = [900, 940, 950, 1100, 1500, 1800]\ndep = [910, 1200, 1120, 1130, 1900, 2000]\nAnswer: 3\n\n"
            "Aim for O(n log n) using sorting / two pointers."
        ),
        "expected_approach": (
            "Sort arrivals and departures independently; sweep with two "
            "pointers counting overlapping intervals; track the maximum."
        ),
    },
]

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


def _special_question(exam_id: str, special: str, idx: int = 0) -> Dict:
    """Build a subjective task item (email writing / coding). No answer key."""
    if special == "email":
        return {
            "id": f"{exam_id}-email-1",
            "question": EMAIL_TASK_PROMPT,
            "options": [],
            "special": "email",
            "category": "email",
            "sub_category": "Professional Email Writing",
            "difficulty": "medium",
            "time_limit": 360,
        }
    task = CODING_TASKS[min(idx, len(CODING_TASKS) - 1)]
    return {
        "id": f"{exam_id}-{task['id_suffix']}",
        "question": task["prompt"],
        "options": [],
        "special": "coding",
        "expected_approach": task["expected_approach"],  # stripped from client copy
        "difficulty_label": task["difficulty_label"],
        "category": "coding",
        "sub_category": f"Coding Task {idx + 1}",
        "difficulty": "easy-medium" if idx == 0 else "hard",
        "time_limit": 2100 if idx == 0 else 3300,
    }


def _sanitize_for_client(questions: List[Dict]) -> List[Dict]:
    """Strip internal keys (grading hints) before sending to the client."""
    return [
        {k: v for k, v in q.items() if k != "expected_approach"}
        for q in questions
    ]


async def _grade_special(
    kind: str, prompt: str, response: str, expected: str = ""
) -> Dict:
    """Grade an email/coding task. AI rubric with deterministic fallback."""
    text = (response or "").strip()
    if not text:
        return {"score": 0, "feedback": "Left blank."}

    def _heuristic() -> Dict:
        words = len(text.split())
        if kind == "email":
            ok = words >= 80 and any(
                w in text.lower()
                for w in ("regards", "sincerely", "thank", "apolog", "dear")
            )
            score = 65 if ok else 40
            feedback = (
                "Offline estimate: structure looks professional."
                if ok
                else "Offline estimate: add a greeting, apology/impact line, and sign-off."
            )
        else:
            looks_like_code = len(text) > 150 and any(
                w in text for w in ("for", "while", "def", "int", "return", "=")
            )
            score = 50 if looks_like_code else 25
            feedback = (
                "Offline estimate: code-like attempt recorded."
                if looks_like_code
                else "Offline estimate: submission too short to look like a solution."
            )
        return {"score": score, "feedback": feedback}

    try:
        from app.services.ai import chat_completion, parse_json

        rubric = (
            "You grade a TCS NQT professional-email-writing task. "
            "Score professionalism, completeness (cause, impact, recovery plan, "
            "revised commitment), tone, and word discipline."
            if kind == "email"
            else "You grade a TCS NQT advanced-coding submission written in plain "
            "pseudocode/real code without execution. Score correctness of approach, "
            "complexity awareness, and edge-case handling."
        )
        instruction = f"""{rubric}

TASK GIVEN TO CANDIDATE:
{prompt[:1500]}
{('EXPECTED APPROACH: ' + expected[:400]) if expected else ''}

CANDIDATE RESPONSE:
{text[:3000]}

Return STRICT JSON only:
{{"score": <0-100 integer>, "feedback": "<one actionable sentence>"}}"""

        raw = await chat_completion(
            [{"role": "user", "content": instruction}],
            use_cache=False,
            temperature=0.2,
            max_tokens=250,
        )
        data = parse_json(raw)
        score = max(0, min(100, int(data.get("score") or 0)))
        return {"score": score, "feedback": str(data.get("feedback", ""))[:400]}
    except Exception:
        return _heuristic()


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
            "locked": bool(cfg.get("locked")),
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
        special = s_def.get("special")
        start_idx = index_offset
        picked_ids: List[str] = []

        if special:
            count = s_def.get("count", 1)
            for i in range(count):
                q = _special_question(req.exam_id, special, i)
                flat_questions.append(q)
                question_ids.append(q["id"])
                picked_ids.append(q["id"])
                index_offset += 1
            client_picked = []
        else:
            pool = _load_pool(s_def["category"])
            want_difficulty = s_def.get("difficulty")
            if want_difficulty:
                hard_pool = [q for q in pool if q.get("difficulty") == want_difficulty]
                if len(hard_pool) >= s_def["questions"]:
                    pool = hard_pool
            n = min(s_def["questions"], len(pool))
            picked = random.sample(pool, n) if n > 0 else []

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
                picked_ids.append(q["id"])
                index_offset += 1

        section_meta.append({
            "name": s_def["name"],
            "category": s_def.get("category"),
            "special": special,
            "part": s_def.get("part", ""),
            "start_index": start_idx,
            "end_index": index_offset - 1,
            "question_ids": picked_ids,
        })
        sections_for_client.append({
            "name": s_def["name"],
            "special": special,
            "part": s_def.get("part", ""),
            "start_index": start_idx,
            "end_index": index_offset - 1,
            "count": index_offset - start_idx,
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
        "locked": bool(cfg.get("locked")),
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
        "locked": bool(cfg.get("locked")),
        "sections": sections_for_client,
        "questions": _sanitize_for_client(flat_questions),
        "total_questions": len(flat_questions),
        "total_minutes": total_minutes,
        "negative_marks": cfg["negative_marks"],
        "ends_at": ends_at.isoformat(),
        "message": (
            f"{cfg['name']} started — {len(flat_questions)} questions in {total_minutes} minutes."
            + (
                " This paper is LOCKED: once you move past a question, you cannot return."
                if cfg.get("locked")
                else ""
            )
        ),
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

    # Locked (TCS NQT) mode: forward-only navigation.
    if test.get("locked"):
        existing_idx = [
            a.get("question_index", -1) for a in test.get("answers", [])
        ]
        frontier = max(existing_idx) if existing_idx else -1
        if question_index < frontier:
            raise HTTPException(
                status_code=400,
                detail="This paper is LOCKED — you cannot return to an earlier question.",
            )

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
    subjective: Dict[str, List[Dict]] = {}
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

        # Subjective tasks (email / coding) are AI-graded, kept out of MCQ stats.
        special = full_q.get("special")
        if special:
            if given is None or str(given).strip() == "":
                skipped += 1
                stats["skipped"] += 1
                subjective.setdefault(sec_name, []).append({
                    "label": full_q.get("sub_category", special),
                    "score": 0,
                    "feedback": "Left blank.",
                })
                continue
            grade = await _grade_special(
                special,
                full_q.get("question", ""),
                str(given),
                full_q.get("expected_approach", "") if special == "coding" else "",
            )
            subjective.setdefault(sec_name, []).append({
                "label": full_q.get(
                    "difficulty_label", full_q.get("sub_category", special)
                ),
                "score": grade["score"],
                "feedback": grade["feedback"],
            })
            continue

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
        "subjective": {
            name: {
                "avg_score": round(sum(g["score"] for g in items) / len(items)),
                "items": items,
            }
            for name, items in subjective.items()
        },
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
