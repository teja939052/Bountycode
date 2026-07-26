"""
Conversion features: company mock tests, gap analysis, alumni experiences,
placement drive alerts — all zero-LLM, pure data/logic.
"""

from __future__ import annotations

import math
import random
import re
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from bson import ObjectId

from app.config import get_settings
from app.database import (
    curated_questions_collection,
    company_mock_tests_collection,
    question_answers_collection,
    skill_graph_collection,
    gamification_collection,
    alumni_experiences_collection,
    placement_drives_collection,
    users_collection,
    aptitude_collection,
    coding_challenges_collection,
)
from app.services.placement_engine import PlacementEngine

settings = get_settings()
engine = PlacementEngine()

# ── Company mock paper blueprints ──────────────────────────────────────────
# Mirrors real campus papers for services cos; lighter for product/FAANG.
MOCK_BLUEPRINTS: Dict[str, Dict[str, Any]] = {
    "tcs": {
        "name": "TCS NQT Style",
        "duration_minutes": 60,
        "sections": [
            {"type": "aptitude", "count": 15, "topics": ["Percentages", "Profit and Loss", "Time and Work", "Speed Distance Time", "Averages", "Ratios", "Probability"]},
            {"type": "aptitude", "count": 5, "topics": None},  # logical/verbal mixed
        ],
        "passing_score": 60,
        "tier": "Services",
    },
    "infosys": {
        "name": "Infosys InfyTQ Style",
        "duration_minutes": 60,
        "sections": [
            {"type": "aptitude", "count": 12, "topics": None},
            {"type": "coding", "count": 2, "topics": None},
        ],
        "passing_score": 65,
        "tier": "Services",
    },
    "wipro": {
        "name": "Wipro NLTH Style",
        "duration_minutes": 75,
        "sections": [
            {"type": "aptitude", "count": 15, "topics": None},
            {"type": "coding", "count": 1, "topics": None},
        ],
        "passing_score": 60,
        "tier": "Services",
    },
    "accenture": {
        "name": "Accenture Assessment Style",
        "duration_minutes": 90,
        "sections": [
            {"type": "aptitude", "count": 12, "topics": None},
            {"type": "coding", "count": 2, "topics": None},
            {"type": "behavioral", "count": 2, "topics": None},
        ],
        "passing_score": 65,
        "tier": "Services",
        "pro_only": True,
    },
    "cognizant": {
        "name": "Cognizant GenC Style",
        "duration_minutes": 60,
        "sections": [
            {"type": "aptitude", "count": 14, "topics": None},
            {"type": "coding", "count": 1, "topics": None},
        ],
        "passing_score": 60,
        "tier": "Services",
        "pro_only": True,
    },
    "hcl": {
        "name": "HCL Aptitude + Coding",
        "duration_minutes": 60,
        "sections": [
            {"type": "aptitude", "count": 12, "topics": None},
            {"type": "coding", "count": 2, "topics": None},
        ],
        "passing_score": 60,
        "tier": "Services",
        "pro_only": True,
    },
    "capgemini": {
        "name": "Capgemini Exceller Style",
        "duration_minutes": 60,
        "sections": [
            {"type": "aptitude", "count": 12, "topics": None},
            {"type": "coding", "count": 1, "topics": None},
        ],
        "passing_score": 60,
        "tier": "Services",
        "pro_only": True,
    },
    "google": {
        "name": "Google-Style Screening",
        "duration_minutes": 90,
        "sections": [
            {"type": "coding", "count": 3, "topics": None},
            {"type": "behavioral", "count": 2, "topics": None},
        ],
        "passing_score": 70,
        "tier": "FAANG",
        "pro_only": True,
    },
    "amazon": {
        "name": "Amazon OA Style",
        "duration_minutes": 90,
        "sections": [
            {"type": "coding", "count": 2, "topics": None},
            {"type": "behavioral", "count": 3, "topics": None},
        ],
        "passing_score": 70,
        "tier": "FAANG",
        "pro_only": True,
    },
    "microsoft": {
        "name": "Microsoft OA Style",
        "duration_minutes": 90,
        "sections": [
            {"type": "coding", "count": 2, "topics": None},
            {"type": "system_design", "count": 1, "topics": None},
        ],
        "passing_score": 70,
        "tier": "FAANG",
        "pro_only": True,
    },
    "meta": {
        "name": "Meta Coding Screen",
        "duration_minutes": 75,
        "sections": [
            {"type": "coding", "count": 2, "topics": None},
            {"type": "behavioral", "count": 2, "topics": None},
        ],
        "passing_score": 70,
        "tier": "FAANG",
        "pro_only": True,
    },
}

# Points each correctly solved company-tagged question contributes to skill score
POINTS_PER_CORRECT = {
    "aptitude": 1.5,
    "coding": 3.0,
    "behavioral": 2.0,
    "system_design": 3.0,
    "dsa": 3.0,
}

# Map question type → skill graph category
TYPE_TO_SKILL = {
    "aptitude": "aptitude",
    "coding": "dsa",
    "behavioral": "behavioral",
    "system_design": "system_design",
}


def free_companies() -> List[str]:
    raw = getattr(settings, "FREE_TIER_COMPANIES", "tcs,infosys,wipro")
    return [c.strip().lower() for c in raw.split(",") if c.strip()]


def is_premium(user: dict) -> bool:
    return user.get("plan") in ("pro", "lifetime")


def normalize_answer(text: str) -> str:
    """Normalize answers for auto-grading (no LLM)."""
    if not text:
        return ""
    t = text.lower().strip()
    t = re.sub(r"[$,₹,%]", "", t)
    t = re.sub(r"\s+", " ", t)
    t = t.replace("percent", "%").replace("percentage", "%")
    # Strip trailing units commonly used
    for unit in (" liters", " litres", " days", " hours", " km/h", " m/s", " men", " years", " kg"):
        if t.endswith(unit):
            t = t[: -len(unit)].strip()
    return t


def answers_match(user_ans: str, correct: str) -> bool:
    if not correct:
        return False
    u = normalize_answer(user_ans)
    c = normalize_answer(correct)
    if not u or not c:
        return False
    if u == c:
        return True
    # Numeric tolerance
    try:
        u_num = float(re.sub(r"[^\d.\-]", "", u.split()[0]))
        c_num = float(re.sub(r"[^\d.\-]", "", c.split()[0]))
        if c_num == 0:
            return abs(u_num) < 1e-6
        return abs(u_num - c_num) / abs(c_num) < 0.02
    except (ValueError, IndexError):
        pass
    # Substring containment for longer answers
    if len(c) > 3 and (c in u or u in c):
        return True
    return False


def _make_mcq_options(correct: str, seed: str) -> List[str]:
    """Generate 4 MCQ options with the correct answer included (deterministic)."""
    if not correct:
        return []
    rng = random.Random(seed)
    options = [correct]
    # Simple distractors
    distractors = [
        f"None of these",
        f"Cannot be determined",
        f"Data insufficient",
    ]
    # Try numeric distractors
    nums = re.findall(r"[\d.]+", correct)
    if nums:
        try:
            base = float(nums[0])
            for mult in (0.8, 1.2, 1.5, 0.5, 2.0):
                alt = correct.replace(nums[0], str(round(base * mult, 2) if base * mult % 1 else int(base * mult)), 1)
                if alt != correct and alt not in options:
                    options.append(alt)
                if len(options) >= 4:
                    break
        except ValueError:
            pass
    for d in distractors:
        if len(options) >= 4:
            break
        if d not in options:
            options.append(d)
    while len(options) < 4:
        options.append(f"Option {len(options) + 1}")
    options = options[:4]
    rng.shuffle(options)
    return options


async def list_mock_companies(user: dict) -> List[Dict[str, Any]]:
    """List available company mock tests with free/pro gating."""
    premium = is_premium(user)
    free = set(free_companies())
    result = []
    for company_id, bp in MOCK_BLUEPRINTS.items():
        locked = (not premium) and (company_id not in free or bp.get("pro_only"))
        # Count available questions
        q_count = await curated_questions_collection.count_documents(
            {"company": {"$regex": f"^{re.escape(company_id)}$", "$options": "i"}}
        )
        # Also try title-case
        if q_count == 0:
            q_count = await curated_questions_collection.count_documents(
                {"company": company_id.title()}
            )
        total_qs = sum(s["count"] for s in bp["sections"])
        result.append({
            "id": company_id,
            "name": company_id.upper() if len(company_id) <= 4 else company_id.title(),
            "paper_name": bp["name"],
            "duration_minutes": bp["duration_minutes"],
            "question_count": total_qs,
            "passing_score": bp["passing_score"],
            "tier": bp["tier"],
            "bank_size": q_count,
            "locked": locked,
            "pro_only": bool(bp.get("pro_only")) or company_id not in free,
        })
    # Sort: unlocked first, then services, then others
    result.sort(key=lambda x: (x["locked"], 0 if x["tier"] == "Services" else 1, x["name"]))
    return result


async def _pick_questions(
    company: str,
    q_type: str,
    count: int,
    topics: Optional[List[str]] = None,
    exclude_ids: Optional[set] = None,
) -> List[dict]:
    """Pick questions from the company-tagged bank, falling back to any company."""
    exclude_ids = exclude_ids or set()
    company_variants = [company, company.title(), company.upper(), company.capitalize()]

    query: Dict[str, Any] = {
        "type": q_type,
        "company": {"$in": company_variants},
    }
    if topics:
        query["topic"] = {"$in": topics}

    cursor = curated_questions_collection.find(query).limit(count * 3)
    pool = []
    async for q in cursor:
        qid = str(q["_id"])
        if qid not in exclude_ids:
            pool.append(q)

    # Fallback: any company same type
    if len(pool) < count:
        fallback_q: Dict[str, Any] = {"type": q_type}
        if topics:
            fallback_q["topic"] = {"$in": topics}
        cursor = curated_questions_collection.find(fallback_q).limit(count * 4)
        async for q in cursor:
            qid = str(q["_id"])
            if qid not in exclude_ids and q not in pool:
                pool.append(q)
            if len(pool) >= count * 2:
                break

    rng = random.Random(f"{company}-{q_type}-{datetime.now(timezone.utc).date().isoformat()}")
    rng.shuffle(pool)
    return pool[:count]


async def start_company_mock(user: dict, company: str) -> Dict[str, Any]:
    """Assemble a timed company mock paper from the curated bank. No LLM."""
    company = company.lower().strip()
    if company not in MOCK_BLUEPRINTS:
        raise ValueError(f"No mock paper for '{company}'. Available: {', '.join(MOCK_BLUEPRINTS)}")

    bp = MOCK_BLUEPRINTS[company]
    premium = is_premium(user)
    free = free_companies()

    if not premium:
        if company not in free or bp.get("pro_only"):
            raise PermissionError(
                f"Company mock for {company.title()} is Pro-only. Free tier: {', '.join(c.title() for c in free)}."
            )
        used = user.get("company_mocks_used", 0)
        limit = getattr(settings, "FREE_TIER_COMPANY_MOCK_LIMIT", 1)
        if used >= limit:
            raise PermissionError(
                f"Free tier allows {limit} company mock test(s) per month. Upgrade to Pro for unlimited mocks."
            )

    # Assemble questions
    selected: List[dict] = []
    seen: set = set()
    for section in bp["sections"]:
        picks = await _pick_questions(
            company, section["type"], section["count"], section.get("topics"), seen
        )
        for q in picks:
            seen.add(str(q["_id"]))
            selected.append(q)

    if not selected:
        raise ValueError(
            f"No questions in bank for {company.title()}. Run seed_questions.py first."
        )

    # Build client-safe question list (no answers)
    paper_questions = []
    answer_key = {}
    for i, q in enumerate(selected):
        qid = str(q["_id"])
        correct = q.get("answer") or ""
        options = q.get("options") or _make_mcq_options(correct, qid) if q.get("type") == "aptitude" else []
        item = {
            "index": i,
            "question_id": qid,
            "question_title": q.get("question_title", ""),
            "topic": q.get("topic", ""),
            "type": q.get("type", "aptitude"),
            "difficulty": q.get("difficulty", "medium"),
            "company": q.get("company", company.title()),
            "options": options,
            "question_link": q.get("question_link"),
            "has_auto_grade": bool(correct) and q.get("type") == "aptitude",
        }
        paper_questions.append(item)
        answer_key[str(i)] = {
            "question_id": qid,
            "correct_answer": correct,
            "type": q.get("type"),
            "topic": q.get("topic"),
        }

    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user["id"],
        "company": company,
        "paper_name": bp["name"],
        "duration_minutes": bp["duration_minutes"],
        "passing_score": bp["passing_score"],
        "questions": paper_questions,
        "answer_key": answer_key,  # server-only; stripped from responses until complete
        "answers": {},
        "status": "in_progress",
        "score": None,
        "percentage": None,
        "section_scores": {},
        "started_at": now,
        "expires_at": now + timedelta(minutes=bp["duration_minutes"] + 5),
        "completed_at": None,
        "created_at": now,
    }
    result = await company_mock_tests_collection.insert_one(doc)
    test_id = str(result.inserted_id)

    # Increment free-tier counter
    if not premium:
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {"$inc": {"company_mocks_used": 1}},
        )

    return {
        "test_id": test_id,
        "company": company.title(),
        "paper_name": bp["name"],
        "duration_minutes": bp["duration_minutes"],
        "passing_score": bp["passing_score"],
        "total_questions": len(paper_questions),
        "questions": paper_questions,
        "expires_at": doc["expires_at"].isoformat(),
        "started_at": now.isoformat(),
    }


async def submit_mock_answer(
    user_id: str,
    test_id: str,
    question_index: int,
    answer: str,
) -> Dict[str, Any]:
    """Save one answer during an in-progress mock (no grading yet for UX speed)."""
    try:
        oid = ObjectId(test_id)
    except Exception:
        raise ValueError("Invalid test ID")

    test = await company_mock_tests_collection.find_one({"_id": oid, "user_id": user_id})
    if not test:
        raise ValueError("Mock test not found")
    if test.get("status") != "in_progress":
        raise ValueError("Test already completed")

    now = datetime.now(timezone.utc)
    expires = test.get("expires_at")
    if expires and expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires and now > expires:
        # Auto-complete on timeout
        return await complete_company_mock(user_id, test_id, auto=True)

    await company_mock_tests_collection.update_one(
        {"_id": oid},
        {"$set": {f"answers.{question_index}": answer}},
    )
    return {"saved": True, "question_index": question_index}


async def complete_company_mock(
    user_id: str,
    test_id: str,
    answers: Optional[Dict[str, str]] = None,
    auto: bool = False,
) -> Dict[str, Any]:
    """Grade the mock (aptitude auto-grade, others attempt credit) and feed skill graph."""
    try:
        oid = ObjectId(test_id)
    except Exception:
        raise ValueError("Invalid test ID")

    test = await company_mock_tests_collection.find_one({"_id": oid, "user_id": user_id})
    if not test:
        raise ValueError("Mock test not found")
    if test.get("status") == "completed" and not auto:
        return _serialize_result(test)

    stored_answers = dict(test.get("answers") or {})
    if answers:
        for k, v in answers.items():
            stored_answers[str(k)] = v

    answer_key = test.get("answer_key") or {}
    section_correct: Dict[str, int] = {}
    section_total: Dict[str, int] = {}
    topic_stats: Dict[str, Dict[str, int]] = {}
    graded = []
    correct_count = 0
    total = len(test.get("questions") or [])

    for idx_str, key in answer_key.items():
        q_type = key.get("type", "aptitude")
        topic = key.get("topic", "General")
        user_ans = stored_answers.get(idx_str, stored_answers.get(int(idx_str) if idx_str.isdigit() else idx_str, ""))
        section_total[q_type] = section_total.get(q_type, 0) + 1
        topic_stats.setdefault(topic, {"correct": 0, "total": 0})
        topic_stats[topic]["total"] += 1

        is_correct = False
        if q_type == "aptitude" and key.get("correct_answer"):
            is_correct = answers_match(str(user_ans or ""), key["correct_answer"])
        elif user_ans and str(user_ans).strip():
            # Non-aptitude: credit attempt as partial (0.5) — still store as attempted
            is_correct = False  # strict: only aptitude auto-grades as correct

        if is_correct:
            correct_count += 1
            section_correct[q_type] = section_correct.get(q_type, 0) + 1
            topic_stats[topic]["correct"] += 1

        graded.append({
            "index": int(idx_str) if idx_str.isdigit() else idx_str,
            "question_id": key.get("question_id"),
            "type": q_type,
            "topic": topic,
            "user_answer": user_ans,
            "correct_answer": key.get("correct_answer") if q_type == "aptitude" else None,
            "is_correct": is_correct,
            "attempted": bool(user_ans and str(user_ans).strip()),
        })

    percentage = round((correct_count / total) * 100, 1) if total else 0
    section_scores = {}
    for t, tot in section_total.items():
        c = section_correct.get(t, 0)
        section_scores[t] = {
            "correct": c,
            "total": tot,
            "percentage": round((c / tot) * 100, 1) if tot else 0,
        }

    weak_topics = sorted(
        [
            {"topic": t, "accuracy": round(s["correct"] / s["total"] * 100, 1), "total": s["total"]}
            for t, s in topic_stats.items() if s["total"] > 0
        ],
        key=lambda x: x["accuracy"],
    )[:5]

    strong_topics = sorted(
        [w for w in [
            {"topic": t, "accuracy": round(s["correct"] / s["total"] * 100, 1), "total": s["total"]}
            for t, s in topic_stats.items() if s["total"] > 0
        ] if w["accuracy"] >= 70],
        key=lambda x: -x["accuracy"],
    )[:5]

    now = datetime.now(timezone.utc)
    update = {
        "answers": stored_answers,
        "graded": graded,
        "status": "completed",
        "score": correct_count,
        "total": total,
        "percentage": percentage,
        "section_scores": section_scores,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "passed": percentage >= test.get("passing_score", 60),
        "completed_at": now,
    }
    await company_mock_tests_collection.update_one({"_id": oid}, {"$set": update})

    # Feed skill graph from mock results
    await _apply_mock_to_skills(user_id, test.get("company", ""), section_scores, percentage)

    # Concrete gap analysis vs this company
    gap = await compute_gap_analysis(user_id, test.get("company", ""), mock_percentage=percentage)

    test.update(update)
    result = _serialize_result(test)
    result["gap_analysis"] = gap
    return result


def _serialize_result(test: dict) -> Dict[str, Any]:
    return {
        "test_id": str(test["_id"]),
        "company": test.get("company", "").title(),
        "paper_name": test.get("paper_name"),
        "status": test.get("status"),
        "score": test.get("score"),
        "total": test.get("total") or len(test.get("questions") or []),
        "percentage": test.get("percentage"),
        "passed": test.get("passed"),
        "passing_score": test.get("passing_score"),
        "section_scores": test.get("section_scores", {}),
        "weak_topics": test.get("weak_topics", []),
        "strong_topics": test.get("strong_topics", []),
        "graded": test.get("graded", []),
        "completed_at": test.get("completed_at"),
    }


async def _apply_mock_to_skills(
    user_id: str,
    company: str,
    section_scores: Dict[str, Dict],
    overall_pct: float,
):
    """Update skill graph from mock test performance (no LLM)."""
    graph = await skill_graph_collection.find_one({"user_id": user_id})
    if not graph:
        categories = {
            "dsa": {"name": "DSA", "score": 0, "skills": {}},
            "system_design": {"name": "System Design", "score": 0, "skills": {}},
            "behavioral": {"name": "Behavioral", "score": 0, "skills": {}},
            "aptitude": {"name": "Aptitude", "score": 0, "skills": {}},
            "resume": {"name": "Resume", "score": 0, "skills": {}},
        }
        graph = {"user_id": user_id, "categories": categories, "overall_score": 0}
        await skill_graph_collection.insert_one(graph)

    categories = graph.get("categories", {})
    for q_type, scores in section_scores.items():
        skill = TYPE_TO_SKILL.get(q_type, q_type)
        if skill not in categories:
            categories[skill] = {"name": skill.replace("_", " ").title(), "score": 0, "skills": {}}
        pct = scores.get("percentage", 0)
        current = categories[skill].get("score", 0)
        # Blend: 70% existing + 30% new mock signal
        new_score = round(current * 0.7 + pct * 0.3, 1) if current > 0 else pct
        categories[skill]["score"] = min(100, new_score)
        # Track company-specific sub-score
        skills = categories[skill].setdefault("skills", {})
        company_key = f"company_{company.lower()}"
        skills[company_key] = {
            "score": pct,
            "attempts": skills.get(company_key, {}).get("attempts", 0) + 1,
            "last_mock": overall_pct,
        }

    overall = round(
        sum(c.get("score", 0) for c in categories.values()) / max(len(categories), 1), 1
    )
    await skill_graph_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "categories": categories,
            "overall_score": overall,
            "updated_at": datetime.now(timezone.utc),
        }},
        upsert=True,
    )

    # Gamification counters
    await gamification_collection.update_one(
        {"user_id": user_id},
        {
            "$inc": {
                "total_aptitude": 1 if "aptitude" in section_scores else 0,
                "total_coding": 1 if "coding" in section_scores else 0,
                "xp": max(10, int(overall_pct / 2)),
            },
            "$set": {"updated_at": datetime.now(timezone.utc)},
        },
        upsert=True,
    )


async def compute_gap_analysis(
    user_id: str,
    company: str,
    target_probability: float = 75.0,
    mock_percentage: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Concrete gap analysis: 'Solve X more TCS aptitude problems to move 60% → 75%'.
    Zero LLM — pure math on skill graph + company weights + bank sizes.
    """
    company = company.lower().strip()
    # Resolve company profile
    if company not in engine.COMPANY_PROFILES:
        matches = [c for c in engine.COMPANY_PROFILES if company in c or c in company]
        if not matches:
            raise ValueError(f"Unknown company '{company}'")
        company = matches[0]

    profile = engine.COMPANY_PROFILES[company]
    weights = engine.TIER_WEIGHTS[profile["tier"]]

    # Current probability
    prediction = await engine.calculate_probability(user_id, company)
    current_prob = prediction["current_probability"]
    skill_scores = prediction["skill_scores"]

    if mock_percentage is not None:
        # Blend mock signal into displayed current for this session
        current_prob = round(current_prob * 0.7 + mock_percentage * 0.3, 1)

    gap_to_target = max(0, target_probability - current_prob)
    actions: List[Dict[str, Any]] = []

    # Rank skills by (weight * deficit)
    min_bar = profile["min_score"] * 10
    skill_priorities = []
    for skill, weight in weights.items():
        score = skill_scores.get(skill, 0)
        deficit = max(0, max(min_bar, 70) - score)
        impact = deficit * weight
        skill_priorities.append((skill, weight, score, deficit, impact))
    skill_priorities.sort(key=lambda x: -x[4])

    remaining_gap = gap_to_target
    for skill, weight, score, deficit, impact in skill_priorities:
        if remaining_gap <= 0.5:
            break
        if deficit < 1:
            continue

        q_type = {
            "dsa": "coding",
            "aptitude": "aptitude",
            "behavioral": "behavioral",
            "system_design": "system_design",
            "resume": None,
        }.get(skill)

        points_each = POINTS_PER_CORRECT.get(skill, 2.0)
        # Probability gain per skill point ≈ weight * 0.8 (matches placement_engine what-if)
        prob_per_skill_point = weight * 0.8
        skill_points_needed = min(deficit, remaining_gap / max(prob_per_skill_point, 0.01))
        problems_needed = max(1, math.ceil(skill_points_needed / points_each))

        # Cap by bank size
        bank_count = 0
        if q_type:
            bank_count = await curated_questions_collection.count_documents({
                "type": q_type,
                "company": {"$in": [company, company.title(), company.upper()]},
            })
            if bank_count == 0:
                bank_count = await curated_questions_collection.count_documents({"type": q_type})

        problems_needed = min(problems_needed, max(bank_count, problems_needed))
        projected_boost = round(min(remaining_gap, problems_needed * points_each * prob_per_skill_point), 1)
        projected_prob = round(min(99.0, current_prob + projected_boost + (target_probability - current_prob - remaining_gap)), 1)

        if skill == "resume":
            action_text = f"Run ATS optimizer and fix all critical issues to raise resume score from {score:.0f} → {min(100, score + skill_points_needed):.0f}"
            problems_needed = 1
            link = "/ats"
        else:
            type_label = (q_type or skill).replace("_", " ")
            action_text = (
                f"Solve {problems_needed} more {company.title()} {type_label} problems "
                f"to move from {current_prob:.0f}% → {min(99, current_prob + projected_boost):.0f}% at {company.title()}"
            )
            link = f"/company-mocks?company={company}" if q_type == "aptitude" else f"/question-bank?company={company.title()}&type={q_type}"

        actions.append({
            "skill": skill,
            "priority": "critical" if weight >= 0.25 and deficit > 15 else "high" if deficit > 10 else "medium",
            "current_score": round(score, 1),
            "target_score": round(min(100, score + skill_points_needed), 1),
            "problems_to_solve": problems_needed,
            "bank_available": bank_count,
            "projected_boost_pct": projected_boost,
            "from_probability": round(current_prob, 1),
            "to_probability": round(min(99.0, current_prob + projected_boost), 1),
            "action": action_text,
            "link": link,
            "company_weight": weight,
        })
        remaining_gap -= projected_boost

    # Summary headline
    if actions:
        top = actions[0]
        headline = top["action"]
    elif current_prob >= target_probability:
        headline = f"You're at {current_prob:.0f}% for {company.title()} — already at/above your {target_probability:.0f}% target. Keep a practice streak."
    else:
        headline = f"Complete a {company.title()} mock test to unlock a precise action plan."

    return {
        "company": company.title(),
        "company_tier": profile["tier"],
        "current_probability": round(current_prob, 1),
        "target_probability": target_probability,
        "gap_pct": round(max(0, target_probability - current_prob), 1),
        "headline": headline,
        "actions": actions,
        "skill_scores": skill_scores,
        "skill_weights": weights,
        "mock_percentage": mock_percentage,
    }


async def get_dashboard_insights(user_id: str) -> Dict[str, Any]:
    """
    Weak-area breakdown + top company probabilities + matched drives.
    Built from data already stored (mocks, aptitude, question answers, skill graph).
    """
    # Weak areas from skill graph
    graph = await skill_graph_collection.find_one({"user_id": user_id})
    categories = (graph or {}).get("categories", {})
    weak_areas = []
    for cat_id, cat in categories.items():
        score = cat.get("score", 0)
        if score < 60:
            weak_areas.append({
                "skill": cat_id,
                "name": cat.get("name", cat_id.replace("_", " ").title()),
                "score": score,
                "severity": "critical" if score < 40 else "high" if score < 50 else "medium",
            })
    weak_areas.sort(key=lambda x: x["score"])

    # Weak topics from question answers + mock tests
    topic_pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {
            "_id": "$topic",
            "avg_score": {"$avg": "$score"},
            "count": {"$sum": 1},
            "correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}},
        }},
        {"$match": {"count": {"$gte": 1}}},
        {"$sort": {"avg_score": 1}},
        {"$limit": 5},
    ]
    weak_topics = []
    async for doc in question_answers_collection.aggregate(topic_pipeline):
        if doc["_id"]:
            weak_topics.append({
                "topic": doc["_id"],
                "avg_score": round(doc.get("avg_score") or 0, 1),
                "accuracy": round((doc["correct"] / doc["count"]) * 100, 1) if doc["count"] else 0,
                "attempts": doc["count"],
            })

    # Recent mock weak topics
    recent_mocks = company_mock_tests_collection.find(
        {"user_id": user_id, "status": "completed"}
    ).sort("completed_at", -1).limit(3)
    mock_weak = []
    async for m in recent_mocks:
        for wt in m.get("weak_topics") or []:
            mock_weak.append({**wt, "company": m.get("company", "").title()})

    # Top company probabilities (free companies always, more if data exists)
    companies_to_check = free_companies() + ["accenture", "amazon", "google"]
    company_probs = []
    for c in companies_to_check[:6]:
        try:
            if c not in engine.COMPANY_PROFILES:
                continue
            pred = await engine.calculate_probability(user_id, c)
            company_probs.append({
                "company": c.title(),
                "probability": pred["current_probability"],
                "tier": pred["company_tier"],
                "band": pred.get("probability_band", {}),
            })
        except Exception:
            continue
    company_probs.sort(key=lambda x: -x["probability"])

    # Matched drives
    drives = await match_placement_drives(user_id, limit=5)

    # Concrete top action
    top_action = None
    if company_probs:
        top_co = company_probs[0]["company"]
        try:
            gap = await compute_gap_analysis(user_id, top_co.lower(), target_probability=75)
            if gap.get("actions"):
                top_action = gap["actions"][0]
        except Exception:
            pass

    return {
        "weak_areas": weak_areas[:5],
        "weak_topics": weak_topics,
        "mock_weak_topics": mock_weak[:5],
        "company_probabilities": company_probs,
        "matched_drives": drives,
        "top_action": top_action,
        "overall_score": (graph or {}).get("overall_score", 0),
    }


# ── Alumni experiences ─────────────────────────────────────────────────────

ALUMNI_SEED = [
    {
        "company": "tcs",
        "role": "Assistant System Engineer",
        "year": 2025,
        "campus": "NIT Trichy",
        "rounds": [
            {"name": "NQT Aptitude", "duration": "80 min", "what_happened": "Quant + Logical + Verbal. Quant was moderate — profit/loss and time-work dominated. Cutoff felt ~65%."},
            {"name": "Technical Interview", "duration": "25 min", "what_happened": "OOPs basics, one SQL join question, and 'explain any project'. They care more about clarity than depth."},
            {"name": "HR / Managerial", "duration": "15 min", "what_happened": "Relocation, bond, night shifts. Be honest about location preference."},
        ],
        "outcome": "selected",
        "tips": [
            "Drill TCS previous papers — pattern barely changes year to year",
            "Know your resume projects cold; they will pick one line and dig",
            "Don't bluff on tech stack you listed",
        ],
        "difficulty": 4,
        "tags": ["campus", "nqt", "services"],
    },
    {
        "company": "infosys",
        "role": "Systems Engineer",
        "year": 2025,
        "campus": "VIT Vellore",
        "rounds": [
            {"name": "InfyTQ / Online Test", "duration": "3 hrs", "what_happened": "Aptitude + 2 coding (arrays + strings). Python allowed. Partial scoring helped."},
            {"name": "Technical + HR combined", "duration": "30 min", "what_happened": "DSA basics (stack vs queue), one puzzle, then 'why Infosys' and notice period."},
        ],
        "outcome": "selected",
        "tips": [
            "Practice 50 Infosys-tagged aptitude questions before the test",
            "Coding: focus on edge cases; they run hidden tests",
            "Have a clean 60-second intro ready",
        ],
        "difficulty": 5,
        "tags": ["campus", "infytq", "services"],
    },
    {
        "company": "wipro",
        "role": "Project Engineer",
        "year": 2024,
        "campus": "SRM Chennai",
        "rounds": [
            {"name": "NLTH Online", "duration": "128 min", "what_happened": "Aptitude heavy. Verbal was surprisingly hard (para jumbles). One coding question on arrays."},
            {"name": "Interview", "duration": "20 min", "what_happened": "Mostly HR + light tech. Asked about SDLC and one C program (factorial)."},
        ],
        "outcome": "selected",
        "tips": [
            "Verbal ability decides cutoffs more than people expect",
            "Keep coding solutions brute-force-first, optimize if time left",
        ],
        "difficulty": 4,
        "tags": ["campus", "nlth", "services"],
    },
    {
        "company": "accenture",
        "role": "Associate Software Engineer",
        "year": 2025,
        "campus": "Manipal",
        "rounds": [
            {"name": "Cognitive + Technical Assessment", "duration": "90 min", "what_happened": "Pseudo-code, MS Office, cloud basics, critical reasoning. Not pure quant."},
            {"name": "Communication Assessment", "duration": "30 min", "what_happened": "Read sentences, repeat, open questions. Accent-neutral clarity matters."},
            {"name": "Interview", "duration": "25 min", "what_happened": "Situation questions + one coding logic on paper."},
        ],
        "outcome": "selected",
        "tips": [
            "Practice pseudo-code output tracing",
            "Communication round eliminates many — rehearse aloud",
        ],
        "difficulty": 5,
        "tags": ["campus", "services"],
    },
    {
        "company": "amazon",
        "role": "SDE-1",
        "year": 2025,
        "campus": "Off-campus",
        "rounds": [
            {"name": "Online OA", "duration": "90 min", "what_happened": "2 coding (medium). One was sliding window, one graph BFS. Leadership principles quiz after."},
            {"name": "Phone Screen", "duration": "45 min", "what_happened": "1 coding + LP story (Customer Obsession)."},
            {"name": "Loop (3 rounds)", "duration": "3 hrs", "what_happened": "2 coding, 1 LP deep-dive. Bar raiser asked a failure story for 20 minutes."},
        ],
        "outcome": "selected",
        "tips": [
            "Prepare 6–8 STAR stories mapped to Leadership Principles",
            "Talk out loud while coding — silence is a red flag",
            "Know time/space of every solution",
        ],
        "difficulty": 8,
        "tags": ["off-campus", "faang", "sde"],
    },
    {
        "company": "google",
        "role": "SWE",
        "year": 2024,
        "campus": "Off-campus",
        "rounds": [
            {"name": "Recruiter screen", "duration": "20 min", "what_happened": "Resume walkthrough, role fit, timeline."},
            {"name": "Phone + Onsite", "duration": "multiple", "what_happened": "4 coding rounds, heavy on graphs/DP. One system design lite for L3."},
        ],
        "outcome": "rejected",
        "tips": [
            "Speed on mediums matters as much as correctness",
            "Practice explaining trade-offs in 30 seconds",
            "Rejection is common — iterate on weak pattern (mine was DP)",
        ],
        "difficulty": 9,
        "tags": ["off-campus", "faang"],
    },
    {
        "company": "microsoft",
        "role": "SDE",
        "year": 2025,
        "campus": "Off-campus",
        "rounds": [
            {"name": "Codility OA", "duration": "60 min", "what_happened": "2 problems. One string, one tree."},
            {"name": "Interviews (4)", "duration": "4 hrs", "what_happened": "Coding + design + behavioral. AA (As Appropriate) culture questions."},
        ],
        "outcome": "selected",
        "tips": [
            "Clean code style is judged harder than at Amazon",
            "Prepare 'tell me about a conflict' thoroughly",
        ],
        "difficulty": 8,
        "tags": ["off-campus", "faang"],
    },
    {
        "company": "cognizant",
        "role": "GenC",
        "year": 2024,
        "campus": "Anna University",
        "rounds": [
            {"name": "Communication + Aptitude", "duration": "90 min", "what_happened": "Spoken English + quant. Soft cutoff on communication."},
            {"name": "Technical Interview", "duration": "20 min", "what_happened": "Java basics, one program, DBMS keys."},
        ],
        "outcome": "selected",
        "tips": [
            "Don't skip the communication practice",
            "Revise DBMS + OOPs one-pagers the night before",
        ],
        "difficulty": 4,
        "tags": ["campus", "services"],
    },
]


async def ensure_alumni_seeded():
    count = await alumni_experiences_collection.count_documents({})
    if count > 0:
        return count
    docs = []
    now = datetime.now(timezone.utc)
    for exp in ALUMNI_SEED:
        docs.append({**exp, "created_at": now, "verified": True})
    if docs:
        await alumni_experiences_collection.insert_many(docs)
    return len(docs)


async def list_alumni_experiences(
    company: Optional[str] = None,
    role: Optional[str] = None,
    limit: int = 20,
    user: Optional[dict] = None,
) -> Dict[str, Any]:
    await ensure_alumni_seeded()
    query: Dict[str, Any] = {}
    if company:
        query["company"] = company.lower()
    if role:
        query["role"] = {"$regex": role, "$options": "i"}

    premium = is_premium(user) if user else False
    free = set(free_companies())

    cursor = alumni_experiences_collection.find(query).sort("year", -1).limit(limit)
    experiences = []
    locked_count = 0
    async for doc in cursor:
        co = doc.get("company", "")
        locked = (not premium) and co not in free
        item = {
            "id": str(doc["_id"]),
            "company": co.title(),
            "role": doc.get("role"),
            "year": doc.get("year"),
            "campus": doc.get("campus"),
            "outcome": doc.get("outcome"),
            "difficulty": doc.get("difficulty"),
            "tags": doc.get("tags", []),
            "locked": locked,
        }
        if locked:
            # Teaser only
            rounds = doc.get("rounds") or []
            item["rounds_teaser"] = [{"name": r.get("name"), "duration": r.get("duration")} for r in rounds]
            item["tips_count"] = len(doc.get("tips") or [])
            locked_count += 1
        else:
            item["rounds"] = doc.get("rounds", [])
            item["tips"] = doc.get("tips", [])
        experiences.append(item)

    return {
        "experiences": experiences,
        "total": len(experiences),
        "locked_count": locked_count,
        "pro_unlocks_all": not premium,
    }


# ── Placement drives ───────────────────────────────────────────────────────

DRIVES_SEED = [
    {"company": "tcs", "role": "Assistant System Engineer", "tier": "Services", "location": "Pan India", "eligibility": {"min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE", "EEE"], "graduation_years": [2025, 2026], "max_backlogs": 0}, "package_lpa": 3.6, "deadline_days": 14, "apply_url": "https://www.tcs.com/careers", "tags": ["campus", "nqt"]},
    {"company": "infosys", "role": "Systems Engineer", "tier": "Services", "location": "Mysore / Pan India", "eligibility": {"min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE"], "graduation_years": [2025, 2026], "max_backlogs": 0}, "package_lpa": 3.6, "deadline_days": 10, "apply_url": "https://www.infosys.com/careers", "tags": ["campus"]},
    {"company": "wipro", "role": "Project Engineer", "tier": "Services", "location": "Pan India", "eligibility": {"min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE", "EEE", "EIE"], "graduation_years": [2025, 2026], "max_backlogs": 1}, "package_lpa": 3.5, "deadline_days": 12, "apply_url": "https://careers.wipro.com", "tags": ["campus", "nlth"]},
    {"company": "accenture", "role": "Associate Software Engineer", "tier": "Services", "location": "Bangalore / Hyderabad / Chennai", "eligibility": {"min_cgpa": 6.5, "branches": ["CSE", "IT", "ECE"], "graduation_years": [2025, 2026], "max_backlogs": 0}, "package_lpa": 4.5, "deadline_days": 8, "apply_url": "https://www.accenture.com/in-en/careers", "tags": ["campus"]},
    {"company": "cognizant", "role": "GenC", "tier": "Services", "location": "Pan India", "eligibility": {"min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE", "EEE"], "graduation_years": [2025, 2026], "max_backlogs": 0}, "package_lpa": 4.0, "deadline_days": 15, "apply_url": "https://careers.cognizant.com", "tags": ["campus"]},
    {"company": "amazon", "role": "SDE Intern", "tier": "FAANG", "location": "Bangalore / Hyderabad", "eligibility": {"min_cgpa": 7.0, "branches": ["CSE", "IT"], "graduation_years": [2026, 2027], "max_backlogs": 0}, "package_lpa": 12.0, "deadline_days": 20, "apply_url": "https://www.amazon.jobs", "tags": ["internship", "oa"]},
    {"company": "microsoft", "role": "SDE Intern", "tier": "FAANG", "location": "Hyderabad / Bangalore", "eligibility": {"min_cgpa": 7.5, "branches": ["CSE", "IT"], "graduation_years": [2026, 2027], "max_backlogs": 0}, "package_lpa": 14.0, "deadline_days": 18, "apply_url": "https://careers.microsoft.com", "tags": ["internship"]},
    {"company": "flipkart", "role": "SDE-1", "tier": "Product", "location": "Bangalore", "eligibility": {"min_cgpa": 7.0, "branches": ["CSE", "IT"], "graduation_years": [2025, 2026], "max_backlogs": 0}, "package_lpa": 21.0, "deadline_days": 9, "apply_url": "https://www.flipkartcareers.com", "tags": ["product"]},
    {"company": "capgemini", "role": "Analyst", "tier": "Services", "location": "Pan India", "eligibility": {"min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE", "EEE"], "graduation_years": [2025, 2026], "max_backlogs": 0}, "package_lpa": 4.0, "deadline_days": 11, "apply_url": "https://www.capgemini.com/careers", "tags": ["campus"]},
    {"company": "hcl", "role": "Graduate Engineer Trainee", "tier": "Services", "location": "Noida / Chennai", "eligibility": {"min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE"], "graduation_years": [2025, 2026], "max_backlogs": 0}, "package_lpa": 4.25, "deadline_days": 16, "apply_url": "https://www.hcltech.com/careers", "tags": ["campus"]},
]


async def ensure_drives_seeded():
    count = await placement_drives_collection.count_documents({})
    if count > 0:
        # Refresh deadlines relative to today for demo freshness
        return count
    now = datetime.now(timezone.utc)
    docs = []
    for d in DRIVES_SEED:
        docs.append({
            **d,
            "company": d["company"].lower(),
            "deadline": now + timedelta(days=d.pop("deadline_days")),
            "is_active": True,
            "created_at": now,
        })
    if docs:
        await placement_drives_collection.insert_many(docs)
    return len(docs)


async def match_placement_drives(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Filter drives to companies user is eligible for + likely to clear.
    Uses profile fields if present; otherwise probability-based ranking.
    """
    await ensure_drives_seeded()
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    profile = (user or {}).get("profile") or {}
    cgpa = profile.get("cgpa")
    branch = (profile.get("branch") or "").upper()
    grad_year = profile.get("graduation_year")
    backlogs = profile.get("backlogs", 0)

    now = datetime.now(timezone.utc)
    cursor = placement_drives_collection.find({
        "is_active": True,
        "deadline": {"$gte": now},
    }).sort("deadline", 1).limit(50)

    matched = []
    async for drive in cursor:
        elig = drive.get("eligibility") or {}
        reasons = []
        eligible = True

        if cgpa is not None and elig.get("min_cgpa") and cgpa < elig["min_cgpa"]:
            eligible = False
            reasons.append(f"CGPA {cgpa} < required {elig['min_cgpa']}")
        elif elig.get("min_cgpa"):
            reasons.append(f"Meets CGPA ≥ {elig['min_cgpa']}")

        if branch and elig.get("branches") and branch not in [b.upper() for b in elig["branches"]]:
            eligible = False
            reasons.append(f"Branch {branch} not in {elig['branches']}")
        elif branch and elig.get("branches"):
            reasons.append(f"Branch {branch} eligible")

        if grad_year and elig.get("graduation_years") and grad_year not in elig["graduation_years"]:
            eligible = False
            reasons.append(f"Grad year {grad_year} not targeted")

        if elig.get("max_backlogs") is not None and backlogs > elig["max_backlogs"]:
            eligible = False
            reasons.append(f"Backlogs {backlogs} > max {elig['max_backlogs']}")

        # Probability
        company = drive.get("company", "")
        probability = None
        likely = False
        try:
            if company in engine.COMPANY_PROFILES:
                pred = await engine.calculate_probability(user_id, company)
                probability = pred["current_probability"]
                likely = probability >= 40
        except Exception:
            probability = None

        deadline = drive.get("deadline")
        days_left = (deadline - now).days if deadline else None

        matched.append({
            "id": str(drive["_id"]),
            "company": company.title(),
            "role": drive.get("role"),
            "tier": drive.get("tier"),
            "location": drive.get("location"),
            "package_lpa": drive.get("package_lpa"),
            "deadline": deadline.isoformat() if deadline else None,
            "days_left": days_left,
            "apply_url": drive.get("apply_url"),
            "tags": drive.get("tags", []),
            "eligible": eligible if (cgpa or branch or grad_year) else True,  # unknown profile → show all
            "likely_to_clear": likely,
            "probability": probability,
            "match_reasons": reasons,
            "eligibility": elig,
        })

    # Rank: eligible + likely first, then by deadline
    matched.sort(key=lambda x: (
        0 if x["eligible"] else 1,
        0 if x["likely_to_clear"] else 1,
        x["days_left"] if x["days_left"] is not None else 999,
    ))
    return matched[:limit]


async def get_mock_history(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    cursor = company_mock_tests_collection.find(
        {"user_id": user_id, "status": "completed"}
    ).sort("completed_at", -1).limit(limit)
    history = []
    async for t in cursor:
        history.append({
            "test_id": str(t["_id"]),
            "company": t.get("company", "").title(),
            "paper_name": t.get("paper_name"),
            "percentage": t.get("percentage"),
            "passed": t.get("passed"),
            "score": t.get("score"),
            "total": t.get("total"),
            "completed_at": t.get("completed_at"),
        })
    return history
