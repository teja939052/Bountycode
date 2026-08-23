"""Company OA Simulator — flagship Placement Simulation Engine component.

Implements the blueprint described in the A-grade PlacementPro plan:

    MOCK OA  ──▶  SCORE ENGINE  ──▶  SKILL DIAGNOSTICS  ──▶  READINESS  ──▶  NEXT MISSIONS

Key design principles (from the research doc):
- Blueprint Engine: company/role/exam-style drives question-type distribution.
- Deterministic: question selection, scoring, time analysis, readiness all run WITHOUT AI.
- AI is OPTIONAL: only used for deeper coding explanation / nuanced feedback if available.
- Hidden test-case coding grading reuses the existing CodeExecutionEngine.
- Integrity Mode: opt-in browser signals recorded and surfaced (not "cheat detection").
- Time Intelligence: per-question timing produces actionable test-taking strategy advice.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from bson import ObjectId

from app.middleware.auth import get_current_user
from app.database import oa_sessions_collection, integrity_events_collection
from app.data.aptitude_question_bank import (
    get_questions_by_category,
    get_random_questions,
)
from app.data.behavioral_question_bank import get_random_question, get_questions_by_category
from app.config import get_settings

router = APIRouter(prefix="/api/v1/oa", tags=["oa"])
settings = get_settings()

# ---------------------------------------------------------------------------
# Blueprint Engine — company/role/exam-style → question-type distribution
# Each value is the weight (percentage) of questions of that type in the OA.
# ---------------------------------------------------------------------------
OA_BLUEPRINTS: Dict[str, Dict[str, float]] = {
    # Generic software engineer fresher OA
    "swe": {
        "coding": 0.25,
        "dsa": 0.15,
        "cs_fundamentals": 0.20,
        "aptitude": 0.25,
        "behavioral": 0.10,
        "situational": 0.05,
    },
    "amazon": {
        "coding": 0.40,
        "dsa": 0.30,
        "behavioral": 0.20,
        "aptitude": 0.10,
    },
    "google": {
        "coding": 0.30,
        "dsa": 0.45,
        "cs_fundamentals": 0.15,
        "behavioral": 0.10,
    },
    "microsoft": {
        "coding": 0.35,
        "dsa": 0.30,
        "cs_fundamentals": 0.20,
        "behavioral": 0.15,
    },
    "meta": {
        "coding": 0.35,
        "dsa": 0.35,
        "behavioral": 0.15,
        "cs_fundamentals": 0.15,
    },
    "tcs": {
        "aptitude": 0.40,
        "coding": 0.25,
        "cs_fundamentals": 0.20,
        "behavioral": 0.15,
    },
    "infosys": {
        "aptitude": 0.45,
        "coding": 0.25,
        "cs_fundamentals": 0.20,
        "behavioral": 0.10,
    },
    "wipro": {
        "aptitude": 0.40,
        "coding": 0.30,
        "cs_fundamentals": 0.20,
        "behavioral": 0.10,
    },
    "general": {
        "coding": 0.25,
        "dsa": 0.15,
        "cs_fundamentals": 0.20,
        "aptitude": 0.25,
        "behavioral": 0.10,
        "situational": 0.05,
    },
}

# Section metadata: human labels + default time budget (minutes) per question.
SECTION_META = {
    "coding": {"label": "Coding", "minutes": 25, "kind": "code"},
    "dsa": {"label": "DSA", "minutes": 12, "kind": "mcq"},
    "cs_fundamentals": {"label": "CS Fundamentals", "minutes": 8, "kind": "mcq"},
    "aptitude": {"label": "Aptitude", "minutes": 5, "kind": "mcq"},
    "behavioral": {"label": "Behavioral", "minutes": 10, "kind": "text"},
    "situational": {"label": "Situational", "minutes": 6, "kind": "mcq"},
}

# Aptitude bank sub-categories used to fill cs_fundamentals / dsa / situational
APT_BANK_MAP = {
    "dsa": "technical",
    "cs_fundamentals": "technical",
    "aptitude": "quantitative",
    "situational": "logical",
}

BEHAVIORAL_CATS = ["leadership", "teamwork", "growth", "conflict", "situational", "problem_solving", "amazon_leadership"]

OA_FREE_LIMIT = 1  # mirrors FREE_TIER_COMPANY_MOCK_LIMIT


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class StartOARequest(BaseModel):
    company: str = Field("general", description="Company blueprint key (amazon/google/tcs/...)")
    role: str = Field("swe", description="Target role key (swe/...); currently drives blueprint selection")
    total_questions: int = Field(20, ge=5, le=40, description="Total number of questions")
    duration_minutes: int = Field(90, ge=10, le=180, description="Total OA duration in minutes")
    mode: str = Field("calm", description="calm | pressure | boss")
    integrity: bool = Field(False, description="Enable opt-in integrity signal tracking")


class SubmitOAItem(BaseModel):
    question_uid: str = Field(..., description="Unique question id within the session")
    answer: Any = Field(..., description="MCQ option index/string, code string, or text response")
    language: Optional[str] = Field(None, description="Language for coding answers")
    time_taken: int = Field(0, ge=0, description="Seconds spent on this question")
    test_cases: Optional[List[dict]] = Field(None, description="Client-run test case results for coding (optional)")


class SubmitOABatch(BaseModel):
    session_id: str
    items: List[SubmitOAItem] = Field(default_factory=list)


class IntegritySignal(BaseModel):
    session_id: str
    event: str = Field(..., description="tab_hidden|fullscreen_exit|copy_paste|blur|focus")
    at: float = Field(..., description="Client timestamp (epoch seconds)")
    detail: Optional[str] = ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _resolve_blueprint(company: str, role: str) -> Dict[str, float]:
    key = (company or "general").lower().strip()
    if key in OA_BLUEPRINTS:
        return OA_BLUEPRINTS[key]
    if role and role.lower() in OA_BLUEPRINTS:
        return OA_BLUEPRINTS[role.lower()]
    return OA_BLUEPRINTS["general"]


def _distribute(total: int, blueprint: Dict[str, float]) -> Dict[str, int]:
    """Distribute total questions across sections by blueprint weight (largest remainder)."""
    raw = {sec: blueprint[sec] * total for sec in blueprint}
    floor = {sec: int(v) for sec, v in raw.items()}
    assigned = sum(floor.values())
    remainder = sorted(blueprint.keys(), key=lambda s: raw[s] - floor[s], reverse=True)
    i = 0
    while assigned < total:
        floor[remainder[i % len(remainder)]] += 1
        assigned += 1
        i += 1
    # drop zero-count sections
    return {sec: n for sec, n in floor.items() if n > 0}


async def _build_questions(dist: Dict[str, int]) -> List[dict]:
    """Build the OA question list deterministically from existing banks."""
    out: List[dict] = []
    for sec, count in dist.items():
        meta = SECTION_META.get(sec, {"label": sec, "minutes": 8, "kind": "mcq"})
        if meta["kind"] == "mcq":
            cat = APT_BANK_MAP.get(sec, "quantitative")
            qs = get_random_questions(cat, count)
            if not qs:
                qs = get_questions_by_category(cat)[:count]
            for idx, q in enumerate(qs[:count]):
                out.append({
                    "question_uid": f"{sec}-{idx}",
                    "section": sec,
                    "section_label": meta["label"],
                    "kind": "mcq",
                    "question": q.get("question", ""),
                    "options": q.get("options", []),
                    "time_limit": meta["minutes"] * 60,
                    "difficulty": q.get("difficulty", "medium"),
                    "topic": q.get("topic", ""),
                    "_correct_index": q.get("correct_index", q.get("correct_answer", 0)),
                    "_explanation": q.get("explanation", ""),
                })
        elif meta["kind"] == "code":
            # Coding: pull from coding_challenges_collection; fall back to template if empty
            from app.database import coding_challenges_collection
            items = []
            try:
                cursor = coding_challenges_collection.find({}).limit(count)
                async for d in cursor:
                    items.append(d)
            except Exception:
                items = []
            for idx in range(count):
                if idx < len(items):
                    c = items[idx]
                    out.append({
                        "question_uid": f"{sec}-{idx}",
                        "section": sec,
                        "section_label": meta["label"],
                        "kind": "code",
                        "question": c.get("title", c.get("question", "Solve the coding problem")),
                        "description": c.get("description", c.get("prompt", "")),
                        "starter_code": c.get("starter_code", {}),
                        "language": c.get("language", "python"),
                        "test_cases": c.get("test_cases", []),
                        "time_limit": meta["minutes"] * 60,
                        "difficulty": c.get("difficulty", "medium"),
                        "topic": c.get("topic", "arrays"),
                    })
                else:
                    # Template fallback so the OA always has enough questions
                    out.append({
                        "question_uid": f"{sec}-{idx}",
                        "section": sec,
                        "section_label": meta["label"],
                        "kind": "code",
                        "question": "Two Sum: return indices of two numbers that add up to target.",
                        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                        "starter_code": {"python": "def two_sum(nums, target):\n    # your code here\n    pass"},
                        "language": "python",
                        "test_cases": [
                            {"input": "[2,7,11,15] 9", "expected": "[0,1]"},
                            {"input": "[3,2,4] 6", "expected": "[1,2]", "is_hidden": True},
                        ],
                        "time_limit": meta["minutes"] * 60,
                        "difficulty": "easy",
                        "topic": "arrays",
                    })
        else:  # text (behavioral / situational)
            for idx in range(count):
                q = get_random_question(BEHAVIORAL_CATS[idx % len(BEHAVIORAL_CATS)])
                if not q:
                    q = {}
                # Convert STARFramework dataclass to a plain dict for MongoDB safety
                star = q.get("star_framework", {})
                if hasattr(star, "__dataclass_fields__"):
                    star = asdict(star)
                out.append({
                    "question_uid": f"{sec}-{idx}",
                    "section": sec,
                    "section_label": meta["label"],
                    "kind": "text",
                    "question": q.get("title", q.get("question", "Describe a challenge you overcame.")),
                    "star_framework": star,
                    "tips": q.get("tips", []),
                    "time_limit": meta["minutes"] * 60,
                    "difficulty": q.get("difficulty", "medium"),
                    "topic": q.get("category", sec),
                })
    return out


def _score_mcq(item: SubmitOAItem, qdef: dict) -> float:
    correct = qdef.get("_correct_index", 0)
    if isinstance(correct, str):
        try:
            correct = int(correct)
        except Exception:
            correct = 0
    try:
        user_ans = int(item.answer)
    except Exception:
        user_ans = -1
    return 100.0 if user_ans == correct else 0.0


def _score_text(item: SubmitOAItem, qdef: dict) -> float:
    """Deterministic STAR rubric (no AI): presence of Situation/Task/Action/Result markers."""
    text = (item.answer or "").strip()
    if not text:
        return 0.0
    low = text.lower()
    markers = ["situation", "task", "action", "result", "impact", "outcome", "learned", "team", "i "]
    hits = sum(1 for m in markers if m in low)
    length_score = min(1.0, len(text) / 400.0)
    return round(min(100.0, (hits / len(markers)) * 70 + length_score * 30), 1)


async def _score_code(item: SubmitOAItem, qdef: dict):
    """Grade coding via existing CodeExecutionEngine (hidden test cases) when available."""
    from app.services.code_executor import CodeExecutionEngine
    engine = CodeExecutionEngine()
    tcs = item.test_cases or qdef.get("test_cases", [])
    if not tcs:
        return 0.0, {"note": "no test cases"}
    try:
        result = await engine.execute_against_test_cases(
            source_code=item.answer,
            language=item.language or qdef.get("language", "python"),
            test_cases=tcs,
            function_name=qdef.get("function_name", "") or "",
        )
    except Exception as e:
        return 0.0, {"error": str(e)}
    if not result.get("success"):
        return 0.0, result
    cases = result.get("results", [])
    if not cases:
        passed = result.get("passed", 0)
        total = result.get("total", len(tcs))
        return round(100.0 * passed / max(total, 1), 1), result
    passed = sum(1 for c in cases if c.get("passed"))
    return round(100.0 * passed / max(len(cases), 1), 1), result


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@router.get("/blueprints")
async def list_blueprints():
    """Return available company/role OA blueprints."""
    return {
        "blueprints": {
            k: {"distribution": v, "sections": list(v.keys())}
            for k, v in OA_BLUEPRINTS.items()
        }
    }


@router.post("/{company}/start")
async def start_oa(company: str, req: StartOARequest, user=Depends(get_current_user)):
    """Start a company OA simulation. Returns the full question set + timer config."""
    if user.get("plan") == "free":
        # count this month's OA attempts
        from app.database import usage_collection
        start_month = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        used = await oa_sessions_collection.count_documents({
            "user_id": user["id"], "created_at": {"$gte": start_month}
        })
        if used >= OA_FREE_LIMIT:
            raise HTTPException(
                status_code=403,
                detail=f"Free tier OA limit reached ({OA_FREE_LIMIT}). Upgrade to Pro for unlimited company OAs.",
            )

    blueprint = _resolve_blueprint(company, req.role)
    dist = _distribute(req.total_questions, blueprint)
    questions = await _build_questions(dist)

    # Per-question timing budget + pressure-mode penalties
    pressure = req.mode == "pressure"
    for q in questions:
        if pressure:
            q["time_limit"] = int(q["time_limit"] * 0.7)
        q.pop("_correct_index", None)
        q.pop("_explanation", None)

    now = datetime.now(timezone.utc)
    session_doc = {
        "user_id": user["id"],
        "company": company.lower(),
        "role": req.role,
        "blueprint": blueprint,
        "mode": req.mode,
        "integrity_enabled": req.integrity,
        "questions": questions,
        "status": "in_progress",
        "answers": {},
        "integrity_signals": [],
        "started_at": now,
        "duration_minutes": req.duration_minutes,
        "ends_at": now + timedelta(minutes=req.duration_minutes),
        "created_at": now,
    }
    res = await oa_sessions_collection.insert_one(session_doc)
    session_id = str(res.inserted_id)

    # Build client-safe payload (no answer keys exposed)
    safe_questions = []
    for q in questions:
        safe = {k: v for k, v in q.items() if not k.startswith("_")}
        safe_questions.append(safe)

    return {
        "session_id": session_id,
        "company": company.lower(),
        "mode": req.mode,
        "blueprint": blueprint,
        "duration_minutes": req.duration_minutes,
        "ends_at": session_doc["ends_at"].isoformat(),
        "integrity_enabled": req.integrity,
        "total_questions": len(safe_questions),
        "questions": safe_questions,
    }


@router.post("/answer")
async def submit_oa_answer(req: SubmitOABatch, user=Depends(get_current_user)):
    """Submit one or more OA answers. Records answers + timing for scoring at completion."""
    try:
        sess = await oa_sessions_collection.find_one({"_id": ObjectId(req.session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    if not sess:
        raise HTTPException(status_code=404, detail="OA session not found")
    if sess["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    if sess.get("status") == "completed":
        raise HTTPException(status_code=400, detail="OA already completed")

    # Index question defs by uid
    qdefs = {q["question_uid"]: q for q in sess["questions"]}
    stored = dict(sess.get("answers", {}))
    for item in req.items:
        qdef = qdefs.get(item.question_uid)
        if not qdef:
            continue
        stored[item.question_uid] = {
            "answer": item.answer,
            "language": item.language,
            "time_taken": item.time_taken,
            "test_cases": item.test_cases,
            "section": qdef["section"],
            "kind": qdef["kind"],
            "difficulty": qdef.get("difficulty", "medium"),
            "topic": qdef.get("topic", ""),
        }
    await oa_sessions_collection.update_one(
        {"_id": ObjectId(req.session_id)},
        {"$set": {"answers": stored, "updated_at": datetime.now(timezone.utc)}},
    )
    return {"received": len(req.items), "session_id": req.session_id}


@router.post("/integrity")
async def record_integrity_signal(req: IntegritySignal, user=Depends(get_current_user)):
    """Opt-in integrity signal recording (tab visibility, fullscreen, copy/paste, blur)."""
    try:
        sess = await oa_sessions_collection.find_one({"_id": ObjectId(req.session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    if not sess or sess["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Session not found")
    if not sess.get("integrity_enabled"):
        return {"recorded": False, "note": "integrity mode not enabled for this session"}
    signal = {
        "event": req.event,
        "at": req.at,
        "detail": req.detail,
        "user_id": user["id"],
        "session_id": req.session_id,
        "created_at": datetime.now(timezone.utc),
    }
    await integrity_events_collection.insert_one(signal)
    await oa_sessions_collection.update_one(
        {"_id": ObjectId(req.session_id)},
        {"$push": {"integrity_signals": signal}},
    )
    return {"recorded": True}


@router.post("/{session_id}/complete")
async def complete_oa(session_id: str, user=Depends(get_current_user)):
    """Grade the OA, produce the scorecard, update readiness, and surface next missions."""
    try:
        sess = await oa_sessions_collection.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    if not sess:
        raise HTTPException(status_code=404, detail="OA session not found")
    if sess["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    qdefs = {q["question_uid"]: q for q in sess["questions"]}
    answers = sess.get("answers", {})

    section_scores: Dict[str, List[float]] = {}
    section_times: Dict[str, List[int]] = {}
    topic_times: Dict[str, List[int]] = {}
    per_question = []

    for uid, ans in answers.items():
        qdef = qdefs.get(uid, {})
        kind = ans.get("kind", "mcq")
        if kind == "mcq":
            score = _score_mcq(
                SubmitOAItem(question_uid=uid, answer=ans.get("answer", -1)), qdef
            )
        elif kind == "text":
            score = _score_text(
                SubmitOAItem(question_uid=uid, answer=ans.get("answer", "")), qdef
            )
        else:  # code
            score, _ = await _score_code(
                SubmitOAItem(
                    question_uid=uid,
                    answer=ans.get("answer", ""),
                    language=ans.get("language"),
                    test_cases=ans.get("test_cases"),
                ),
                qdef,
            )
        sec = ans.get("section", "other")
        section_scores.setdefault(sec, []).append(score)
        t = int(ans.get("time_taken", 0))
        section_times.setdefault(sec, []).append(t)
        topic_times.setdefault(ans.get("topic", "misc"), []).append(t)
        per_question.append({
            "question_uid": uid,
            "section": sec,
            "section_label": qdef.get("section_label", sec),
            "score": score,
            "time_taken": t,
            "difficulty": ans.get("difficulty", "medium"),
            "topic": ans.get("topic", ""),
        })

    # Section averages
    section_avg = {}
    for sec, scores in section_scores.items():
        section_avg[sec] = round(sum(scores) / len(scores), 1) if scores else 0.0

    # Overall = blueprint-weighted average
    blueprint = sess.get("blueprint", {})
    if blueprint:
        overall = sum(section_avg.get(s, 0) * w for s, w in blueprint.items())
    else:
        overall = round(sum(section_avg.values()) / max(len(section_avg), 1), 1)
    overall = round(min(100.0, max(0.0, overall)), 1)

    # Time Intelligence
    time_intel = _build_time_intelligence(section_times, topic_times, sess.get("duration_minutes", 90))

    # Strong / weak areas
    strong = sorted(section_avg.items(), key=lambda x: x[1], reverse=True)[:2]
    weak = sorted(section_avg.items(), key=lambda x: x[1])[:3]

    # Verdict
    if overall >= 75:
        verdict = "INTERVIEW READY"
    elif overall >= 55:
        verdict = "NEEDS PREPARATION"
    else:
        verdict = "NOT READY"

    # Integrity summary
    signals = sess.get("integrity_signals", [])
    integrity_summary = {}
    for s in signals:
        integrity_summary[s.get("event", "unknown")] = integrity_summary.get(s.get("event", "unknown"), 0) + 1

    result = {
        "session_id": session_id,
        "company": sess.get("company"),
        "mode": sess.get("mode"),
        "overall_readiness": overall,
        "verdict": verdict,
        "section_scores": {SECTION_META.get(s, {}).get("label", s): v for s, v in section_avg.items()},
        "section_scores_raw": section_avg,
        "strong_areas": [SECTION_META.get(s, {}).get("label", s) for s, _ in strong],
        "weak_areas": [SECTION_META.get(s, {}).get("label", s) for s, _ in weak],
        "time_intelligence": time_intel,
        "questions_answered": len(per_question),
        "total_questions": len(sess["questions"]),
        "integrity_signals": integrity_summary,
        "scorecard": per_question,
        "next_missions": _next_missions(weak, topic_times),
    }

    await oa_sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"status": "completed", "result": result, "completed_at": datetime.now(timezone.utc)}},
    )

    # Feed readiness (best-effort, non-blocking)
    try:
        await _update_readiness(user["id"], sess.get("company"), overall, section_avg)
    except Exception:
        pass

    return result


@router.get("/{session_id}/result")
async def get_oa_result(session_id: str, user=Depends(get_current_user)):
    try:
        sess = await oa_sessions_collection.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    if not sess:
        raise HTTPException(status_code=404, detail="OA session not found")
    if sess["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    if sess.get("status") != "completed":
        raise HTTPException(status_code=400, detail="OA not completed yet")
    return sess.get("result", {})


@router.get("/history")
async def get_oa_history(user=Depends(get_current_user)):
    cursor = oa_sessions_collection.find(
        {"user_id": user["id"]},
        {"questions": 0, "answers": 0, "integrity_signals": 0},
    ).sort("created_at", -1).limit(20)
    out = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        out.append(doc)
    return {"sessions": out}


# ---------------------------------------------------------------------------
# Time Intelligence + Next Missions
# ---------------------------------------------------------------------------
def _build_time_intelligence(section_times: Dict[str, List[int]], topic_times: Dict[str, List[int]], total_min: int):
    intel = {"by_section": {}, "advice": []}
    for sec, times in section_times.items():
        avg = round(sum(times) / max(len(times), 1) / 60.0, 1)
        intel["by_section"][SECTION_META.get(sec, {}).get("label", sec)] = {
            "avg_minutes": avg,
            "total_minutes": round(sum(times) / 60.0, 1),
            "questions": len(times),
        }
    # Topic-level slow spots
    topic_avgs = {t: sum(v) / max(len(v), 1) for t, v in topic_times.items()}
    if topic_avgs:
        fast = min(topic_avgs, key=lambda k: topic_avgs[k])
        slow = max(topic_avgs, key=lambda k: topic_avgs[k])
        if topic_avgs[slow] > 0 and topic_avgs[slow] >= 1.8 * max(topic_avgs[fast], 1):
            intel["advice"].append(
                f"You spend {round(topic_avgs[slow] / max(topic_avgs[fast], 1), 1)}x longer "
                f"on {slow} problems. Consider abandoning after ~12 min if stuck."
            )
    intel["advice"].append(
        "Allocate time by section weight; autosave is on — don't re-edit submitted answers."
    )
    return intel


def _next_missions(weak: List[tuple], topic_times: Dict[str, List[int]]):
    missions = []
    for sec, _ in weak:
        label = SECTION_META.get(sec, {}).get("label", sec)
        missions.append(f"Practice 10 {label} questions (target 75%+ accuracy)")
    # Add slow-topic mission
    if topic_times:
        slow = max(topic_times, key=lambda k: sum(topic_times[k]) / max(len(topic_times[k]), 1))
        missions.append(f"Drill {slow} timed sets — you lose the most time here")
    if not missions:
        missions.append("Take a harder-pressure OA to validate consistency")
    return missions[:4]


async def _update_readiness(user_id: str, company: str, overall: float, section_avg: Dict[str, float]):
    """Best-effort: store OA outcomes as a readiness signal for the existing readiness engine."""
    from app.database import skill_graph_collection
    col = skill_graph_collection()
    doc = await col.find_one({"user_id": user_id})
    if not doc:
        doc = {"user_id": user_id, "categories": {}, "oa_outcomes": []}
    outcomes = doc.get("oa_outcomes", [])
    outcomes.append({
        "company": company,
        "overall": overall,
        "sections": section_avg,
        "at": datetime.now(timezone.utc).isoformat(),
    })
    # Keep last 20
    outcomes = outcomes[-20:]
    cats = doc.get("categories", {})
    for sec, score in section_avg.items():
        key = sec
        prev = cats.get(key, {})
        prev_score = prev.get("score", 0)
        # exponential moving average toward OA result
        new_score = round(prev_score * 0.6 + score * 0.4, 1)
        cats[key] = {"score": new_score, "source": "oa"}
    await col.update_one(
        {"user_id": user_id},
        {"$set": {"categories": cats, "oa_outcomes": outcomes}},
        upsert=True,
    )
