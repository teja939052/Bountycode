from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    question_answers_collection,
    solved_problems_collection,
    users_collection,
)
from app.models.question import SubmitAnswer
from app.services.ai import chat_completion, parse_json, assign_companies
from app.services.gamification import record_practice
from app.services.usage import check_and_reset_monthly_usage
from app.services.code_executor import CodeExecutionEngine
from app.services.cache import cache
from app.services import question_store
from app.services.explanation_cache import get_or_create_explanation, get_cached_explanation
import random

router = APIRouter(prefix="", tags=["question-solve"])
code_engine = CodeExecutionEngine()


def _question_title(q: dict) -> str:
    return q.get("question") or q.get("question_title", "")


def _explain_compiler_error(error_message: str, source_code: str, language: str) -> str:
    error_lower = error_message.lower()
    if "compile" in error_lower or "syntax" in error_lower:
        return "Your code has a syntax error that stopped compilation before it could run. Check your syntax carefully."
    elif "timeout" in error_lower or "timelimit" in error_lower or "time limit" in error_lower:
        return "Your code exceeded the time limit. Try a more efficient algorithm."
    elif "memory" in error_lower or "mle" in error_lower or "out of memory" in error_lower:
        return "Your code exceeded the memory limit. Try using less memory-intensive data structures."
    elif "runtime" in error_lower or "exception" in error_lower or "error" in error_lower:
        return "Your code crashed during execution. Check for division by zero, null references, or out-of-bounds access."
    else:
        return "Your code failed to produce the expected output. Review your algorithm logic and edge cases."


def _is_correct_answer(user_ans: str, correct: str, q_type: str) -> bool:
    if not correct:
        return False
    if q_type == "aptitude":
        u = user_ans.lower().strip()
        c = correct.lower().strip()
        if u == c:
            return True
        try:
            return abs(float(u) - float(c)) / max(abs(float(c)), 1e-6) < 0.02
        except Exception:
            return False
    return bool(user_ans.strip())


@router.post("/answer")
async def submit_answer(req: SubmitAnswer, user=Depends(get_current_user)):
    await check_and_reset_monthly_usage(user)
    qid = req.question_id
    question = question_store.find_one({"id": qid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    answer_collection = question_answers_collection()
    previous = await answer_collection.find(
        {"user_id": user["id"], "question_id": qid},
    ).sort("created_at", -1).limit(3).to_list(3)

    previous_text = ""
    if previous:
        previous_text = "\n\nPrevious attempts:\n" + "\n".join(
            f"- Score: {p.get('score', 'N/A')}/10 | Feedback: {p.get('feedback', 'N/A')[:100]}"
            for p in previous
        )

    q_type = question.get("type", "coding")
    correct = question.get("correct_answer", "")
    is_correct = _is_correct_answer(req.answer, correct, q_type)

    prompt = f"""You are a placement interview coach. A student attempted this question:

Question: {_question_title(question)}
Topic: {question.get('topic', '')}
Company: {', '.join(question.get('companies', []))}
Type: {q_type}
{previous_text}

Student's answer:
{req.answer}

Evaluate the answer and respond in this exact JSON format:
{{
  "score": <1-10>,
  "is_correct": {"true" if is_correct else "false"},
  "feedback": "<2-3 sentence summary>",
  "strengths": ["<strength1>", "<strength2>"],
  "improvements": ["<improvement1>", "<improvement2>"],
  "better_approach": "<better approach if applicable, or null>",
  "time_complexity": "O(n)" or "O(n log n)" etc — the optimal time complexity for this problem,
  "space_complexity": "O(1)" or "O(n)" etc — the optimal space complexity,
  "algorithm": "<name of the best algorithm/approach, e.g. 'Two Pointers', 'Binary Search', 'DP'>",
  "graph_nodes": [
    {{"id": "<step_name>", "label": "<short label>", "type": "start|process|decision|end", "x": <0-100>, "y": <0-100>}},
    ...
  ],
  "graph_edges": [
    {{"from": "<step_id>", "to": "<step_id>", "label": "<condition or >" }},
    ...
  ]
}}

For graph_nodes/graph_edges: describe the algorithm as a flowchart. Include 4-8 nodes max.
- "start" nodes: entry point
- "process" nodes: main operations
- "decision" nodes: conditionals/branches
- "end" nodes: return/output
Be direct, constructive, and specific. If the answer is vague, say so. If it's wrong, explain why."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=False,
            max_tokens=1500,
        )
        feedback = parse_json(result)
    except Exception:
        feedback = {
            "score": 5 if req.answer.strip() else 0,
            "is_correct": is_correct,
            "feedback": "We couldn't evaluate your answer right now. Please try again.",
            "strengths": [],
            "improvements": ["Try providing a more detailed answer with code examples"],
            "better_approach": None,
        }

    score = feedback.get("score", 5)

    answer_doc = {
        "user_id": user["id"],
        "question_id": qid,
        "answer": req.answer,
        "score": score,
        "is_correct": feedback.get("is_correct", is_correct),
        "feedback": feedback.get("feedback", ""),
        "strengths": feedback.get("strengths", []),
        "improvements": feedback.get("improvements", []),
        "better_approach": feedback.get("better_approach"),
        "time_complexity": feedback.get("time_complexity"),
        "space_complexity": feedback.get("space_complexity"),
        "algorithm": feedback.get("algorithm"),
        "graph_nodes": feedback.get("graph_nodes"),
        "graph_edges": feedback.get("graph_edges"),
        "time_taken": req.time_taken,
        "created_at": datetime.now(timezone.utc),
    }
    await answer_collection.insert_one(answer_doc)

    await record_practice(user["id"], "question_bank", score)

    explanation = None
    if score < 7:
        try:
            explanation = await get_or_create_explanation(question, q_type)
        except Exception:
            explanation = None

    return {
        "question_id": qid,
        "score": score,
        "is_correct": feedback.get("is_correct", is_correct),
        "feedback": feedback.get("feedback", ""),
        "strengths": feedback.get("strengths", []),
        "improvements": feedback.get("improvements", []),
        "better_approach": feedback.get("better_approach"),
        "time_complexity": feedback.get("time_complexity"),
        "space_complexity": feedback.get("space_complexity"),
        "algorithm": feedback.get("algorithm"),
        "graph_nodes": feedback.get("graph_nodes"),
        "graph_edges": feedback.get("graph_edges"),
        "explanation": explanation,
    }


@router.post("/{question_id}/explanation")
async def get_question_explanation(question_id: str, body: dict = None, user=Depends(get_current_user)):
    question = question_store.find_one({"id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    language = (body or {}).get("language", "python") if body else "python"
    existing = await get_cached_explanation(question_id, language)
    if existing:
        return {"question_id": question_id, "explanation": existing, "cached": True}
    explanation = await get_or_create_explanation(question, language)
    return {
        "question_id": question_id,
        "explanation": explanation,
        "cached": False,
    }


@router.get("/{question_id}/solved")
async def is_question_solved(question_id: str, user=Depends(get_current_user)):
    solved = await solved_problems_collection.find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })
    return {"solved": bool(solved)}


@router.post("/{question_id}/submit")
async def submit_code_for_question(
    question_id: str,
    payload: Dict[str, Any],
    user=Depends(get_current_user),
):
    await check_and_reset_monthly_usage(user)
    question = question_store.find_one({"id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    code = payload.get("code", "")
    language = payload.get("language", "python")
    if not code.strip():
        raise HTTPException(status_code=400, detail="Code is required")
    if len(code) > 120000:
        raise HTTPException(status_code=400, detail="Code is too large")

    hidden_cases = question.get("hidden_test_cases", [])
    if not hidden_cases:
        raise HTTPException(status_code=400, detail="No hidden test cases available for this problem")

    normalized_cases = [
        {
            "input": case.get("input", ""),
            "expected": case.get("expected", case.get("expected_output", "")),
            "is_hidden": True,
        }
        for case in hidden_cases
    ]
    execution_result = await code_engine.execute_against_test_cases(
        source_code=code,
        language=language,
        test_cases=normalized_cases,
    )

    if not execution_result.get("success", False):
        raw_error = execution_result.get("error", "Failed to execute test cases")
        error_explanation = _explain_compiler_error(raw_error, code, language)
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": raw_error,
                "error_explanation": error_explanation,
            },
        )

    results = execution_result.get("results", [])
    all_passed = execution_result.get("all_passed", False)
    passed_count = execution_result.get("passed_count", 0)
    total = execution_result.get("total_count", len(hidden_cases))
    score = execution_result.get("score", 0)
    summary = execution_result.get("summary", f"{passed_count}/{total} hidden test cases passed")

    if all_passed:
        await solved_problems_collection.update_one(
            {"user_id": user["id"], "question_id": question_id},
            {"$set": {
                "user_id": user["id"],
                "question_id": question_id,
                "code": code,
                "language": language,
                "solved_at": datetime.now(timezone.utc),
            }},
            upsert=True,
        )
        xp_gained = 50
        await record_practice(user["id"], "coding", score)
    else:
        xp_gained = 0

    return {
        "success": True,
        "all_passed": all_passed,
        "passed_count": passed_count,
        "total_count": total,
        "score": score,
        "summary": summary,
        "results": results,
        "xp_gained": xp_gained,
        "solved": all_passed,
    }


@router.get("/{question_id}")
async def get_question_detail(question_id: str, user=Depends(get_current_user)):
    question = question_store.find_one({"id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    q = dict(question)
    plan = user.get("plan", "free")

    visible_cases = question.get("visible_test_cases", [])
    hidden_cases = question.get("hidden_test_cases", [])

    q["statement"] = question.get("statement", question.get("question", ""))
    q["examples"] = question.get("examples", [])
    q["constraints"] = question.get("constraints", [])
    q["visible_test_cases"] = visible_cases
    q["hidden_test_cases"] = hidden_cases if plan in ("pro", "lifetime") else []
    q["dsa_guide"] = question.get("dsa_guide", {"approach": "", "data_structures": [], "patterns": [], "tips": []})

    hints = question.get("hints", [])
    solved = await solved_problems_collection.find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })
    if plan in ("pro", "lifetime") or solved:
        q["hints"] = hints
        q["solution"] = question.get("solution", {})
    else:
        q["hints"] = hints[:1] if hints else []
        q["solution"] = {"locked": True, "message": "Solve this problem or upgrade to Pro to unlock the solution"}

    return q


@router.get("/recent")
async def get_recent_answers(
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    collection = question_answers_collection()
    cursor = collection.find(
        {"user_id": user["id"]},
    ).sort("created_at", -1).limit(limit)

    answers = []
    async for a in cursor:
        a["id"] = str(a.pop("_id"))
        answers.append(a)

    return {"answers": answers}


@router.get("/random")
async def get_random_question(
    type: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    exclude_solved: bool = Query(True),
    user=Depends(get_current_user),
):
    await check_and_reset_monthly_usage(user)
    query: Dict[str, Any] = {}
    if type:
        query["type"] = type
    if difficulty:
        query["difficulty"] = difficulty
    if topic:
        query["topic"] = topic
    if company:
        query["company"] = {"$in": [company, company.title(), company.upper()]}

    cache_key = f"{type or '*'}:{difficulty or '*'}:{topic or '*'}:{company or '*'}:{'1' if exclude_solved else '0'}"
    cached_id = await cache.get("random_question", cache_key)
    if cached_id:
        cached_question = question_store.find_one({"id": str(cached_id)})
        if cached_question:
            question = dict(cached_question)
            plan = user.get("plan", "free")
            solved = await solved_problems_collection.find_one({
                "user_id": user["id"],
                "question_id": question["id"],
            })
            question["solved"] = bool(solved)
            if plan not in ("pro", "lifetime") and not solved:
                question["solution"] = {"locked": True, "message": "Solve this problem or upgrade to Pro to unlock the solution"}
                question["hidden_test_cases"] = []
                hints = question.get("hints", [])
                question["hints"] = hints[:1] if hints else []
            return {"question": question}

    solved_ids = set()
    if exclude_solved:
        solved = await solved_problems_collection.find({"user_id": user["id"]}, {"question_id": 1}).to_list(1000)
        solved_ids = {str(s["question_id"]) for s in solved if s.get("question_id")}

    candidates = question_store.find(query).to_list()
    if exclude_solved and solved_ids:
        candidates = [q for q in candidates if q["id"] not in solved_ids]

    if not candidates:
        return {"question": None, "message": "No questions found for the given filters"}

    question = random.choice(candidates)
    await cache.set("random_question", cache_key, question["id"], ttl=45)

    plan = user.get("plan", "free")
    solved = await solved_problems_collection.find_one({
        "user_id": user["id"],
        "question_id": question["id"],
    })
    question["solved"] = bool(solved)

    if plan not in ("pro", "lifetime") and not solved:
        question["solution"] = {"locked": True, "message": "Solve this problem or upgrade to Pro to unlock the solution"}
        question["hidden_test_cases"] = []
        hints = question.get("hints", [])
        question["hints"] = hints[:1] if hints else []

    return {"question": question}


@router.post("/{question_id}/solution")
async def get_question_solution(
    question_id: str,
    payload: Dict[str, Any],
    user=Depends(get_current_user),
):
    hint_level = payload.get("hint_level", 1)
    question = question_store.find_one({"id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    plan = user.get("plan", "free")
    solved = await solved_problems_collection.find_one({
        "user_id": user["id"],
        "question_id": question_id,
    })

    hints = question.get("hints", [])
    solution = question.get("solution", {})

    if plan in ("pro", "lifetime") or solved:
        visible_hints = hints
        visible_solution = solution
    else:
        visible_hints = hints[:hint_level] if hint_level <= len(hints) else hints
        visible_solution = {"locked": True, "message": "Solve this problem or upgrade to Pro to unlock the full solution"}

    return {
        "question_id": question_id,
        "hint_level": hint_level,
        "total_hints": len(hints),
        "hints": visible_hints,
        "solution": visible_solution,
        "unlocked": plan in ("pro", "lifetime") or bool(solved),
    }