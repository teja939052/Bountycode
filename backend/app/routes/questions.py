from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Dict, Any
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, question_answers_collection,
    users_collection, solved_problems_collection
)
from app.models.question import SubmitAnswer, QuestionSubmission, QuestionVote
from app.services.ai import chat_completion, parse_json, assign_companies
from app.services.gamification import record_practice
from app.services.usage import check_and_reset_monthly_usage
from app.services.code_executor import CodeExecutionEngine
from app.services.cache import cache
import random

router = APIRouter(prefix="/api/questions", tags=["question-bank"])
code_engine = CodeExecutionEngine()


def serialize_question(q):
    q["id"] = str(q.pop("_id"))
    if not q.get("companies"):
        company = q.get("company")
        if isinstance(company, list):
            q["companies"] = company
        elif isinstance(company, str) and company:
            q["companies"] = [company]
        else:
            q["companies"] = assign_companies()
    return q


def _question_title(q: dict) -> str:
    return q.get("question") or q.get("question_title", "")


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


@router.get("/browse")
async def browse_questions(
    company: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    sub_topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("frequency"),  # frequency, difficulty, companies, acceptance, newest, alphabetical
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    """Browse questions with advanced sorting and filtering."""
    query = {}
    if company:
        query["company"] = {"$in": [company, company.title(), company.upper()]}
    if role:
        query["role"] = {"$in": [role, role.lower(), role.upper()]}
    if topic:
        query["topic"] = topic
    if sub_topic:
        query["sub_topic"] = sub_topic
    if difficulty:
        query["difficulty"] = difficulty
    if type:
        query["type"] = type
    if search:
        query["$text"] = {"$search": search}

    # Build sort
    if sort == "difficulty":
        sort_stage = [("difficulty", 1), ("frequency", -1)]
    elif sort == "companies":
        sort_stage = [("company", -1), ("frequency", -1)]
    elif sort == "acceptance":
        sort_stage = [("acceptance_rate", -1), ("total_submissions", -1)]
    elif sort == "newest":
        sort_stage = [("created_at", -1)]
    elif sort == "alphabetical":
        sort_stage = [("question_title", 1)]
    else:  # Default: frequency (most practiced first)
        sort_stage = [("frequency", -1)]

    collection = curated_questions_collection()
    total = await collection.count_documents(query)
    skip = (page - 1) * limit

    cursor = collection.find(query).skip(skip).limit(limit).sort(sort_stage)
    questions = []
    async for q in cursor:
        questions.append(serialize_question(q))

    return {
        "questions": questions,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "sort": sort,
    }


@router.get("/filters")
async def get_filters():
    cache_key = "question_filters_v2"
    cached = cache.get(cache_key)
    if cached:
        return cached

    collection = curated_questions_collection()

    companies = await collection.distinct("company")
    roles = await collection.distinct("role")
    topics = await collection.distinct("topic")
    sub_topics = await collection.distinct("sub_topic")
    types = await collection.distinct("type")
    difficulties = await collection.distinct("difficulty")

    result = {
        "companies": sorted(companies),
        "roles": sorted(roles),
        "topics": sorted(topics),
        "sub_topics": sorted(sub_topics),
        "types": sorted(types),
        "difficulties": sorted(difficulties),
    }

    cache.set(cache_key, result, ttl=300)
    return result


@router.get("/stats")
async def get_my_stats(user=Depends(get_current_user)):
    collection = question_answers_collection()
    uid = user["id"]

    total_attempted = await collection.count_documents({"user_id": uid})
    pipeline = [
        {"$match": {"user_id": uid}},
        {"$group": {
            "_id": "$topic",
            "avg_score": {"$avg": "$score"},
            "count": {"$sum": 1},
            "correct": {"$sum": {"$cond": ["$is_correct", 1, 0]}}},
        },
        {"$sort": {"avg_score": 1}},
    ]
    topic_stats = []
    async for doc in collection.aggregate(pipeline):
        topic_stats.append({
            "topic": doc["_id"],
            "avg_score": round(doc["avg_score"], 1),
            "count": doc["count"],
            "accuracy": round(doc["correct"] / doc["count"] * 100, 1) if doc["count"] > 0 else 0,
        })

    weak_areas = [t for t in topic_stats if t["avg_score"] < 6][:5]
    strong_areas = [t for t in topic_stats if t["avg_score"] >= 7][:5]

    return {
        "total_attempted": total_attempted,
        "topic_stats": topic_stats,
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
    }


@router.post("/submit")
async def submit_question(req: QuestionSubmission, user=Depends(get_current_user)):
    doc = req.model_dump()
    doc["submitted_by"] = user["id"]
    doc["upvotes"] = 0
    doc["downvotes"] = 0
    doc["reported"] = False
    doc["created_at"] = datetime.now(timezone.utc)
    doc["updated_at"] = datetime.now(timezone.utc)
    result = await curated_questions_collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


@router.post("/upvote")
async def upvote_question(req: QuestionVote, user=Depends(get_current_user)):
    try:
        q_oid = ObjectId(req.question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await curated_questions_collection.find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    delta = req.vote
    await curated_questions_collection.update_one(
        {"_id": q_oid},
        {"$inc": {"upvotes": max(0, delta), "downvotes": max(0, -delta)}, "$set": {"updated_at": datetime.now(timezone.utc)}},
    )
    return {
        "question_id": req.question_id,
        "upvotes": (question.get("upvotes", 0) + delta),
        "downvotes": question.get("downvotes", 0),
    }


@router.post("/answer")
async def submit_answer(req: SubmitAnswer, user=Depends(get_current_user)):
    qid = req.question_id
    try:
        q_oid = ObjectId(qid)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    collection = curated_questions_collection()
    question = await collection.find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    answer_collection = question_answers_collection()
    previous = await answer_collection.find({
        "user_id": user["id"],
        "question_id": qid,
    }).sort("created_at", -1).limit(3).to_list(3)

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
Company: {', '.join(question.get('company', []))}
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

    await collection.update_one(
        {"_id": q_oid},
        {"$inc": {"practice_count": 1, "frequency": 1}},
    )

    await record_practice(user["id"], "question_bank", score)

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
    }


@router.get("/{question_id}/solved")
async def is_question_solved(question_id: str, user=Depends(get_current_user)):
    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

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
    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await curated_questions_collection().find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    code = payload.get("code", "")
    language = payload.get("language", "python")
    if not code.strip():
        raise HTTPException(status_code=400, detail="Code is required")

    hidden_cases = question.get("hidden_test_cases", [])
    if not hidden_cases:
        raise HTTPException(status_code=400, detail="No hidden test cases available for this problem")

    results = []
    all_passed = True
    passed_count = 0

    for idx, case in enumerate(hidden_cases):
        stdin = case.get("input", "")
        expected = case.get("expected", case.get("expected_output", "")).strip()
        execution = await code_engine.execute_code(code, language, stdin, timeout=5)

        if execution["success"]:
            actual = execution["stdout"].strip()
            passed = actual == expected
            if passed:
                passed_count += 1
            else:
                all_passed = False
        else:
            actual = execution.get("error", "Execution failed")
            passed = False
            all_passed = False

        results.append({
            "test_case_index": idx + 1,
            "passed": passed,
            "is_hidden": True,
            "input": "[HIDDEN]",
            "expected": "[HIDDEN]",
            "actual": "[HIDDEN]" if not execution["success"] else "[HIDDEN]",
            "error": execution.get("error") if not execution["success"] else None,
            "execution_time": execution.get("execution_time", 0),
        })

    total = len(hidden_cases)
    score = round(passed_count / total * 100, 1) if total else 0
    summary = f"{passed_count}/{total} hidden test cases passed"

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
    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await curated_questions_collection().find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    q = serialize_question(question)
    plan = user.get("plan", "free")

    visible_cases = question.get("visible_test_cases", [])
    hidden_cases = question.get("hidden_test_cases", [])

    q["statement"] = question.get("statement", question.get("question", ""))
    q["examples"] = question.get("examples", [])
    q["constraints"] = question.get("constraints", [])
    q["visible_test_cases"] = visible_cases
    q["hidden_test_cases"] = hidden_cases if plan in ("pro", "lifetime") else []

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
        {"user_id": user["id"]}
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
    """Get a random question for quick practice."""
    query: Dict[str, Any] = {}
    if type:
        query["type"] = type
    if difficulty:
        query["difficulty"] = difficulty
    if topic:
        query["topic"] = topic
    if company:
        query["company"] = {"$in": [company, company.title(), company.upper()]}

    collection = curated_questions_collection()

    if exclude_solved:
        solved = await solved_problems_collection.find({"user_id": user["id"]}).to_list(1000)
        solved_ids = [str(s["question_id"]) for s in solved if "question_id" in s]
        if solved_ids:
            from bson import ObjectId as BsonObjectId
            try:
                query["_id"] = {"$nin": [BsonObjectId(qid) for qid in solved_ids]}
            except Exception:
                pass

    all_questions = await collection.find(query).to_list(200)
    if not all_questions:
        return {"question": None, "message": "No questions found for the given filters"}

    question = random.choice(all_questions)
    question["id"] = str(question.pop("_id"))

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
    """Get solution with progressive hints. Unlocks next hint tier on request."""
    hint_level = payload.get("hint_level", 1)

    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await curated_questions_collection().find_one({"_id": q_oid})
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
