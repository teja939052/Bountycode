from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.models.aptitude import StartAptitudeTest, SubmitAptitudeAnswer
from app.database import users_collection, aptitude_collection
from app.middleware.auth import get_current_user
from app.services.ai import generate_aptitude_questions, evaluate_aptitude_answer
from app.services.usage import check_and_reset_monthly_usage, can_use_feature
from app.config import get_settings
from bson import ObjectId

router = APIRouter(prefix="/api/v1/aptitude", tags=["aptitude"])
settings = get_settings()

APTITUDE_CATEGORIES = {
    # Quantitative Aptitude
    "quantitative": "Quantitative Aptitude - Math, Numbers, Statistics",
    "quant-shortcuts": "Quant Shortcuts - Vedic Math, Approximation, Speed Tricks",
    
    # Logical Reasoning
    "logical": "Logical Reasoning - Patterns, Sequences, Deductions",
    "syllogisms": "Syllogisms - Venn Diagrams, Logical Deduction",
    "blood-relations": "Blood Relations - Family Trees, Coded Relations",
    "direction-sense": "Direction Sense - Distance, Shadow, Map Problems",
    "coding-decoding": "Coding-Decoding - Letter/Number/Symbol Patterns",
    "series-completion": "Series Completion - Number/Letter/Figure Series",
    "analogies": "Analogies - Word/Number/Figure Relationships",
    "puzzles": "Logical Puzzles - Seating, Scheduling, Constraints",
    
    # Verbal Ability
    "verbal": "Verbal Ability - Grammar, Vocabulary, Comprehension",
    "reading-comprehension": "Reading Comprehension - Passages, Inference, Tone",
    "para-jumbles": "Para Jumbles - Sentence Reordering, Coherence",
    "sentence-correction": "Sentence Correction - Grammar, Parallelism, Modifiers",
    "vocabulary": "Vocabulary - Synonyms, Antonyms, Analogies, Cloze",
    "fill-in-blanks": "Fill in the Blanks - Single/Double, Context Clues",
    "critical-reasoning": "Critical Reasoning - Assumptions, Inferences, Arguments",
    
    # Technical
    "technical": "Technical MCQs - Programming, CS Fundamentals",
    "data-interpretation": "Data Interpretation - Charts, Graphs, Tables",
}


@router.get("/categories")
async def get_categories():
    return {
        "categories": [
            {
                "id": cat_id,
                "name": cat_name.split(" - ")[0],
                "description": cat_name.split(" - ")[1] if " - " in cat_name else "",
            }
            for cat_id, cat_name in APTITUDE_CATEGORIES.items()
        ]
    }


@router.post("/start")
async def start_aptitude_test(req: StartAptitudeTest, user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)

    if not can_use_feature(user, "aptitude"):
        raise HTTPException(
            status_code=403,
            detail=f"Free tier limit reached ({getattr(settings, 'FREE_TIER_APTITUDE_LIMIT', 5)} aptitude tests/month). Upgrade to Pro for unlimited.",
        )

    if req.category not in APTITUDE_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category. Choose from: {list(APTITUDE_CATEGORIES.keys())}")

    result = await generate_aptitude_questions(req.category, req.difficulty, req.question_count)

    questions = result.get("questions", []) if isinstance(result, dict) else result

    if not questions:
        raise HTTPException(status_code=500, detail="Failed to generate aptitude questions")

    test_doc = {
        "user_id": user["id"],
        "category": req.category,
        "questions": questions,
        "answers": [None] * len(questions),
        "score": 0,
        "total_questions": len(questions),
        "time_taken": 0,
        "status": "in_progress",
        "created_at": datetime.now(timezone.utc),
    }

    result = await aptitude_collection.insert_one(test_doc)
    test_id = str(result.inserted_id)

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$inc": {"aptitude_used": 1}},
    )

    return {
        "test_id": test_id,
        "category": req.category,
        "questions": [
            {
                "index": i,
                "question": q["question"],
                "options": q["options"],
                "time_limit": q.get("time_limit", 60),
                "companies": q.get("companies", []),
            }
            for i, q in enumerate(questions)
        ],
        "total_questions": len(questions),
    }


@router.post("/answer")
async def submit_aptitude_answer(req: SubmitAptitudeAnswer, user=Depends(get_current_user)):
    try:
        test = await aptitude_collection.find_one({"_id": ObjectId(req.test_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid test ID")

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    if test["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if test.get("status") == "completed":
        raise HTTPException(status_code=400, detail="Test already completed")

    if req.question_index < 0 or req.question_index >= len(test["questions"]):
        raise HTTPException(status_code=400, detail="Invalid question index")

    questions = test["questions"]
    answers = test.get("answers", [None] * len(questions))
    answers[req.question_index] = req.answer

    await aptitude_collection.update_one(
        {"_id": ObjectId(req.test_id)},
        {"$set": {"answers": answers}},
    )

    correct = questions[req.question_index]["correct_answer"]
    is_correct = str(req.answer).strip().upper() == str(correct).strip().upper()

    return {
        "is_correct": is_correct,
        "correct_answer": correct,
        "explanation": questions[req.question_index]["explanation"],
        "question_index": req.question_index,
        "total_answered": sum(1 for a in answers if a is not None),
    }


@router.post("/{test_id}/complete")
async def complete_aptitude_test(test_id: str, time_taken: int = 0, user=Depends(get_current_user)):
    try:
        test = await aptitude_collection.find_one({"_id": ObjectId(test_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid test ID")

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    if test["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    questions = test["questions"]
    answers = test.get("answers", [None] * len(questions))

    score = 0
    for i, q in enumerate(questions):
        if answers[i] is not None and str(answers[i]).strip().upper() == str(q["correct_answer"]).strip().upper():
            score += 1

    percentage = (score / len(questions)) * 100 if questions else 0

    weak_areas = []
    strong_areas = []
    category_scores = {}

    for i, q in enumerate(questions):
        cat = q.get("category", "general")
        if cat not in category_scores:
            category_scores[cat] = {"correct": 0, "total": 0}
        category_scores[cat]["total"] += 1
        if answers[i] is not None and str(answers[i]).strip().upper() == str(q["correct_answer"]).strip().upper():
            category_scores[cat]["correct"] += 1

    for cat, s in category_scores.items():
        cat_pct = (s["correct"] / s["total"]) * 100 if s["total"] > 0 else 0
        if cat_pct < 50:
            weak_areas.append(cat)
        elif cat_pct >= 80:
            strong_areas.append(cat)

    await aptitude_collection.update_one(
        {"_id": ObjectId(test_id)},
        {
            "$set": {
                "score": score,
                "time_taken": time_taken,
                "status": "completed",
                "weak_areas": weak_areas,
                "strong_areas": strong_areas,
            }
        },
    )

    return {
        "test_id": test_id,
        "score": score,
        "total_questions": len(questions),
        "percentage": round(percentage, 1),
        "time_taken": time_taken,
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
        "questions": [
            {
                "question": q["question"],
                "options": q["options"],
                "your_answer": answers[i],
                "correct_answer": q["correct_answer"],
                "is_correct": answers[i] is not None and str(answers[i]).strip().upper() == str(q["correct_answer"]).strip().upper(),
                "explanation": q["explanation"],
                "companies": q.get("companies", []),
            }
            for i, q in enumerate(questions)
        ],
    }


@router.get("/history")
async def get_aptitude_history(user=Depends(get_current_user)):
    cursor = aptitude_collection.find(
        {"user_id": user["id"], "status": "completed"}
    ).sort("created_at", -1).limit(20)

    tests = []
    async for doc in cursor:
        tests.append({
            "id": str(doc["_id"]),
            "category": doc.get("category", ""),
            "score": doc.get("score", 0),
            "total_questions": doc.get("total_questions", 0),
            "percentage": round((doc.get("score", 0) / doc.get("total_questions", 1)) * 100, 1),
            "time_taken": doc.get("time_taken", 0),
            "created_at": doc.get("created_at"),
        })

    return {"tests": tests}
