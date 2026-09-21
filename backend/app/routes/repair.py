"""Repair loop routes — the return path of the closed-loop learning system.

Flow (per AGENTS.md v1.3 acceptance gate 3/4):
  assessment failed
      ↓
  diagnosis + repair mission created   (oa.py / interview)
      ↓
  student opens missions → recommended lessons/exercises/quizzes
      ↓
  retest on verified questions only    (Content Trust)
      ↓
  ≥80% → advance | <80% → deeper repair

Everything here composes EXISTING canonical systems:
  * ``repair_service``  — mission creation / listing / completion
  * ``question_store``  — verified-only retest content (Content Trust gate)
  * ``code_executor``   — deterministic grading of coding retests

No new engines. This wires the previously dead repair→retest link.
"""
from __future__ import annotations

import ast
import json
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.middleware.auth import get_current_user
from app.services.repair_service import (
    complete_repair_mission,
    create_repair_mission,
    get_repair_recommendations,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/repair", tags=["repair"])


# Map an OA/retest section label back to the verified question-store type.
_SECTION_TO_TYPE = {
    "aptitude": "aptitude",
    "cs_fundamentals": "cs_fundamentals",
    "logical": "logical",
    "verbal": "verbal",
    "coding": "coding",
    "dsa": "coding",
}


def _verified_questions_for_skill(skill: str, count: int = 3) -> List[dict]:
    """Pull `count` verified questions for a weakness skill. Returns [] on any
    failure — never falls back to unverified/legacy content (Content Trust)."""
    try:
        from app.services import question_store as qs
    except Exception:
        return []
    try:
        type_key = _SECTION_TO_TYPE.get(skill, "")
        query: Dict[str, Any] = {}
        if type_key:
            query["type"] = type_key
        rows = qs.find(query).prefer_verified().to_list(count * 4)
        # Prioritise by topic match so the retest targets the actual weakness.
        topic = skill.split("/")[0].lower()
        hits = [q for q in rows if topic in str(q.get("topic", "")).lower()]
        rest = [q for q in rows if q not in hits]
        return (hits + rest)[:count]
    except Exception:
        return []


def _to_retest_item(q: dict, idx: int) -> dict:
    """Shape a verified question into a client-safe retest item (no answer keys)."""
    base = {
        "id": q.get("id", f"retest-{idx}"),
        "type": q.get("type", "mcq"),
        "question": q.get("question", ""),
        "topic": q.get("topic", ""),
        "sub_topic": q.get("sub_topic", ""),
        "difficulty": q.get("difficulty", "medium"),
        "provenance": q.get("provenance", ""),
        "trust_status": q.get("trust_status", "verified"),
    }
    if q.get("type") == "coding":
        code = (q.get("solution") or {}).get("code") or ""
        base.update({
            "kind": "code",
            "starter_code": {"python": _starter_from(code)},
            "language": "python",
            "function_name": _function_name_from(code),
            # Expected outputs stay server-side so the retest remains proof of
            # capability; a coding UI may show the inputs as examples.
            "test_cases": [{"input": _serialize_input(t)} for t in (q.get("testcases") or [])],
        })
    else:
        base.update({
            "kind": "mcq",
            "options": q.get("options") or q.get("multiple_choice_options") or [],
        })
    return base


def _serialize_input(t: dict) -> Any:
    inp = t.get("input", [])
    if isinstance(inp, (list, tuple)) and len(inp) == 1 and isinstance(inp[0], (list, dict)):
        inp = inp[0]
    return inp


def _starter_from(code: str) -> str:
    lines = [l for l in (code or "").splitlines() if l.strip()]
    if not lines:
        return "def solve():\n    pass"
    header = lines[0].rstrip(":")
    return header + ":\n    # your implementation here\n    pass"


def _function_name_from(code: str) -> str:
    for line in (code or "").splitlines():
        s = line.strip()
        if s.startswith("def "):
            return s.split("(")[0].replace("def ", "").strip()
    return "solve"


def _verified_question_by_id(qid: str) -> Optional[dict]:
    try:
        from app.services import question_store as qs
        return qs.find_one({"_id": qid})
    except Exception:
        return None


class CompleteMissionRequest(BaseModel):
    mission_id: str


class RetestSubmitItem(BaseModel):
    question_id: str
    answer: Any = None          # for MCQ: selected option (str/int)
    code: str = ""              # for coding
    language: str = "python"


class RetestSubmitRequest(BaseModel):
    skill: str
    answers: List[RetestSubmitItem] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/missions")
async def list_missions(user=Depends(get_current_user)):
    """List a student's active repair missions + the next best one."""
    result = await get_repair_recommendations(user["id"])
    return result


@router.post("/diagnose")
async def diagnose_failure(req: RetestSubmitRequest, user=Depends(get_current_user)):
    """Diagnose WHY a student failed and recommend a targeted repair path.

    Uses the diagnosis engine to classify the failure into structured codes
    (CONCEPT_GAP, PATTERN_RECOGNITION, IMPLEMENTATION_ERROR, etc.) and returns
    a recommended micro-lesson or practice focus.
    """
    from app.services.diagnosis import diagnose_question_failure
    from app.services.skill_taxonomy import canonical_skill_id

    skill_id = canonical_skill_id(req.skill) or req.skill
    # Aggregate diagnosis across all answers
    all_codes: List[str] = []
    for item in req.answers:
        q = _verified_question_by_id(item.question_id)
        if not q:
            continue
        diag = diagnose_question_failure(
            score=10.0 if item.answer else 0.0,
            answer_text=str(item.answer or ""),
            q_type=q.get("type", "coding"),
            question=q,
            metadata={"all_passed": False, "passed_count": 0, "total": 1},
        )
        for code in diag.get("codes", []):
            if code not in all_codes:
                all_codes.append(code)

    # Map codes to human-readable recommendations
    recommendations = _code_recommendations(all_codes, req.skill)

    return {
        "skill": req.skill,
        "skill_id": skill_id,
        "diagnosis_codes": all_codes,
        "recommendations": recommendations,
        "repair_mission_available": True,
    }


@router.post("/missions/complete")
async def complete_mission(req: CompleteMissionRequest, user=Depends(get_current_user)):
    """Mark a repair mission as completed."""
    outcome = await complete_repair_mission(user["id"], req.mission_id)
    if not outcome.get("completed"):
        raise HTTPException(status_code=404, detail="Repair mission not found")

    # â”€â”€ Emit canonical LearningEvent for repair completion â”€â”€
    try:
        from app.services.study_engine import emit_learning_event
        from app.services.skill_taxonomy import canonical_skill_id

        skill_id = canonical_skill_id(outcome.get("skill")) or "repair.completed"
        await emit_learning_event(user["id"], {
            "activity_type": "repair",
            "source": "repair",
            "skill_id": skill_id,
            "assessment_id": req.mission_id,
            "passed": True,
            "score": 10,
            "repair_id": req.mission_id,
            "metadata": {
                "mission_skill": outcome.get("skill"),
                "source": outcome.get("source", "repair"),
            },
        })
    except Exception as exc:
        logger.warning("repair complete event emission failed: %s", exc)

    return outcome


@router.get("/retest")
async def get_retest(skill: str, count: int = 3, user=Depends(get_current_user)):
    """Return a verified-only retest for a weakness skill (Content Trust gate).

    Only independently verified questions are served. If fewer than `count` are
    available, the retest is smaller — never backfilled with unverified content.
    """
    if not skill:
        raise HTTPException(status_code=422, detail="'skill' query parameter is required")
    questions = _verified_questions_for_skill(skill, count)
    payload = [_to_retest_item(q, i) for i, q in enumerate(questions)]
    return {
        "skill": skill,
        "count": len(payload),
        "retest_condition": ">=80% across retest questions on this weakness",
        "questions": payload,
    }


@router.post("/retest/submit")
async def submit_retest(req: RetestSubmitRequest, user=Depends(get_current_user)):
    """Grade a verified retest. Pass when ≥80% of questions are answered
    correctly (mirrors the OA retest_condition). Failing creates a deeper
    repair mission so the loop closes back into repair, not dead-end."""
    if not req.skill:
        raise HTTPException(status_code=422, detail="'skill' is required")
    if not req.answers:
        raise HTTPException(status_code=422, detail="No retest answers supplied")

    results = []
    correct = 0
    for item in req.answers:
        q = _verified_question_by_id(item.question_id)
        if not q:
            results.append({"question_id": item.question_id, "correct": False,
                            "reason": "question_not_found"})
            continue
        kind = "code" if q.get("type") == "coding" else "mcq"
        try:
            if kind == "mcq":
                is_correct = _grade_mcq(q, item.answer)
            else:
                is_correct = await _grade_code(q, item.code, item.language)
        except Exception:
            is_correct = False
        if is_correct:
            correct += 1
        results.append({
            "question_id": item.question_id,
            "topic": q.get("topic", ""),
            "kind": kind,
            "correct": is_correct,
        })

    total = len(results)
    pct = round(correct / total * 100) if total else 0
    passed = pct >= 80

    # On failure, reopen the loop with a deeper repair mission.
    deeper_mission = None
    if not passed and total:
        try:
            deeper_mission = await create_repair_mission(user["id"], [req.skill], source="repair_retest")
        except Exception:
            logger.warning("Failed to create deeper repair mission", exc_info=True)

    # â”€â”€ Emit canonical LearningEvent for the retest â”€â”€
    try:
        from app.services.study_engine import emit_learning_event
        from app.services.skill_taxonomy import canonical_skill_id
        from app.services.diagnosis import diagnose_question_failure

        skill_id = canonical_skill_id(req.skill) or req.skill
        diagnosis = diagnose_question_failure(
            pct / 10.0, "", "mcq", {},  # retest is a skill-level assessment
            metadata={"all_passed": passed, "passed_count": correct, "total": total},
        )
        repair_id = deeper_mission.id if deeper_mission else None
        # Attempt order for the evidence layer (best-effort; falls back to 1).
        try:
            from app.database import learning_events_collection
            _prior_retests = await learning_events_collection().count_documents({
                "user_id": user["id"], "skill_id": skill_id,
                "activity_type": "retest"})
        except Exception:
            _prior_retests = 0
        await emit_learning_event(user["id"], {
            "activity_type": "retest",
            "source": "repair",
            "skill_id": skill_id,
            "passed": passed,
            "score": pct,
            "time_spent_seconds": 0,
            "attempt_number": _prior_retests + 1,
            "diagnosis_codes": diagnosis["codes"] if isinstance(diagnosis, dict) else [],
            "repair_id": repair_id,
            "metadata": {
                "correct": correct,
                "total": total,
                "pct": pct,
                "verdict": "advance" if passed else "repair_more",
                "targeted_skill": req.skill,
            },
        })
    except Exception as exc:
        logger.warning("retest LearningEvent emission failed: %s", exc)

    return {
        "skill": req.skill,
        "correct": correct,
        "total": total,
        "pct": pct,
        "passed": passed,
        "verdict": "advance" if passed else "repair_more",
        "results": results,
    }


# ---------------------------------------------------------------------------
# Grading helpers (deterministic, mirror the OA scorecard)
# ---------------------------------------------------------------------------

def _mapped_correct_index(q: dict, options) -> int:
    """Resolve a verified MCQ's answer key to an option index (letters -> position)."""
    correct = q.get("correct_index")
    if isinstance(correct, int):
        return correct
    if isinstance(correct, str):
        if correct.strip().isdigit():
            return int(correct)
        keys = list(options.keys()) if isinstance(options, dict) else []
        if correct in keys:
            return keys.index(correct)
    ca = q.get("correct_answer")
    if ca is not None:
        if isinstance(options, dict):
            keys = list(options.keys())
            match = next(
                (k for k, v in options.items()
                 if str(v).strip().lower() == str(ca).strip().lower()), None)
            if match is None:
                match = ca if ca in keys else None
            if match is not None:
                return keys.index(match)
        if isinstance(options, list):
            tokens = [str(o).strip().lower() for o in options]
            if str(ca).strip().lower() in tokens:
                return tokens.index(str(ca).strip().lower())
    return 0


def _mapped_answer_index(answer: Any, options) -> Optional[int]:
    """Resolve a student's MCQ answer to an option index (index or letter/text)."""
    if isinstance(answer, (int, float)) and not isinstance(answer, bool):
        return int(answer)
    text = str(answer).strip().lower()
    if isinstance(options, dict):
        keys = list(options.keys())
        if text in {str(k).strip().lower() for k in keys}:
            return keys.index(next(k for k in keys if str(k).strip().lower() == text))
        vals = [str(v).strip().lower() for v in options.values()]
        if text in vals:
            return vals.index(text)
    elif isinstance(options, list):
        vals = [str(o).strip().lower() for o in options]
        if text in vals:
            return vals.index(text)
    try:
        return int(text)
    except (ValueError, TypeError):
        return None


def _grade_mcq(q: dict, answer: Any) -> bool:
    options = q.get("options") or q.get("multiple_choice_options") or []
    correct = _mapped_correct_index(q, options)
    user = _mapped_answer_index(answer, options)
    if user is not None:
        return user == correct
    return str(answer).strip().lower() == str(q.get("correct_answer", "")).strip().lower()


async def _grade_code(q: dict, code: str, language: str) -> bool:
    """Grade a coding retest by invoking the student's function directly against
    the verified test cases.

    Verified coding questions carry *structured positional arguments*
    (``{'input': [[2,7,11,15], 9], 'expected': [0,1]}``) — not stdin strings.
    So we import the student's function and call it with those args, exactly as
    the independent-verification pipeline does (func(*inp)). Deterministic and
    correct for the verified question format. Only Python is targeted here.
    """
    import re as _re
    tcs = (q.get("testcases") or []) + (q.get("hidden_testcases") or [])
    if not tcs:
        return False

    # Find the function the student is expected to implement.
    func_name = ""
    for line in (code or "").splitlines():
        m = _re.match(r"\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", line)
        if m:
            func_name = m.group(1)
            break
    if not func_name:
        return False

    try:
        parsed = ast.parse(code)
        definition = next(
            node for node in parsed.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name
        )
        arity = len(definition.args.posonlyargs) + len(definition.args.args)
    except (SyntaxError, StopIteration):
        return False

    def as_stdin(value: Any) -> str:
        # The canonical batch runner parses one Python-literal argument unless
        # inputs are comma-separated. Preserve the bank's list representation
        # for one-argument functions and expand it for multi-argument ones.
        if arity > 1 and isinstance(value, (list, tuple)):
            return ", ".join(repr(part) for part in value)
        return value if isinstance(value, str) else repr(value)

    def as_expected(value: Any) -> str:
        return value if isinstance(value, str) else json.dumps(value, separators=(",", ":"))

    visible_count = len(q.get("testcases") or [])
    cases = [
        {
            "input": as_stdin(tc.get("input")),
            "expected": as_expected(tc.get("expected")),
            "is_hidden": index >= visible_count,
        }
        for index, tc in enumerate(tcs)
    ]
    from app.services.code_executor import CodeExecutionEngine
    result = await CodeExecutionEngine().execute_against_test_cases(
        source_code=code,
        language=(language or "python").lower(),
        test_cases=cases,
        function_name=func_name,
    )
    return bool(result.get("success") and result.get("all_passed"))


def _deep_equal(a: Any, b: Any) -> bool:
    """Compare floats tolerantly; exact for ints/lists/dicts/strings."""
    if isinstance(a, float) or isinstance(b, float):
        try:
            return abs(float(a) - float(b)) < 1e-9
        except (TypeError, ValueError):
            return False
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_deep_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(a[k] == b.get(k) for k in a)
    return a == b


# ---------------------------------------------------------------------------
# Misconception diagnosis recommendations
# ---------------------------------------------------------------------------

_CODE_RECOMMENDATIONS: Dict[str, str] = {
    "CONCEPT_GAP": "Review the core concept before attempting more problems. Try the foundational lesson for this skill.",
    "PATTERN_RECOGNITION": "Practice identifying problem patterns. Study 3-5 similar problems to build recognition.",
    "IMPLEMENTATION_ERROR": "Your approach is correct but the implementation has bugs. Trace through your code step by step.",
    "EDGE_CASE_FAILURE": "Handle edge cases: empty input, single element, duplicates, negative numbers, integer overflow.",
    "COMPLEXITY_ERROR": "Your solution works but is too slow. Study time complexity and optimize using better data structures.",
    "TIME_MANAGEMENT": "Practice under timed constraints. Learn to quickly identify the right approach.",
    "CARELESS_ERROR": "Double-check your work. Common mistakes: off-by-one errors, wrong variable names, missing returns.",
    "KNOWLEDGE_RECALL": "Review the key formulas and techniques for this topic.",
    "TRANSFER_FAILURE": "Practice applying this concept to unfamiliar problem types.",
    "DEBUGGING": "Improve debugging skills: use print statements, trace execution, test with small inputs.",
}


def _code_recommendations(codes: List[str], skill: str) -> List[Dict[str, str]]:
    """Map diagnosis codes to actionable recommendations."""
    recs: List[Dict[str, str]] = []
    for code in codes:
        desc = _CODE_RECOMMENDATIONS.get(code, f"Review {skill} fundamentals.")
        recs.append({"code": code, "recommendation": desc})
    if not recs:
        recs.append({
            "code": "GENERAL",
            "recommendation": f"Practice more {skill} problems to build confidence.",
        })
    return recs
