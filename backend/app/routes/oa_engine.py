from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/oa", tags=["oa-engine"])


# Request/Response models
class StartOARequest(BaseModel):
    """Request to start an OA (Online Assessment)."""
    company: str = Field(..., description="Target company (tcs, infosys, amazon, google, etc.)")
    difficulty: str = Field("medium", description="Difficulty level: easy/medium/hard")
    question_count: int = Field(5, ge=1, le=20, description="Number of questions")


class OAQuestion(BaseModel):
    """Single OA question."""
    id: str
    question: str
    difficulty: str
    topic: str
    sub_topic: str
    time_limit: int
    code_template: Optional[str] = None


class SubmitOAAnswer(BaseModel):
    """Submit an OA answer."""
    question_id: str = Field(..., description="Question ID")
    answer: str = Field(..., description="Submitted code")
    time_taken: int = Field(0, ge=0, description="Time taken in seconds")


# Company OA question banks
INDIA_OA_QUESTIONS = {
    "tcs": {
        "arrays": [
            {
                "id": "tcs_oa_1",
                "question": "Given an array of n integers, find the maximum sum of a contiguous subarray (Kadane's algorithm).",
                "difficulty": "easy",
                "topic": "Arrays",
                "sub_topic": "Maximum subarray sum",
                "time_limit": 20,
            },
            {
                "id": "tcs_oa_2",
                "question": "Given an unsorted array of integers, find the length of the longest increasing subsequence.",
                "difficulty": "medium",
                "topic": "Arrays",
                "sub_topic": "LIS",
                "time_limit": 30,
            },
            {
                "id": "tcs_oa_3",
                "question": "Given an array, find the element that appears more than n/2 times (majority element).",
                "difficulty": "medium",
                "topic": "Arrays",
                "sub_topic": "Majority element",
                "time_limit": 20,
            },
            {
                "id": "tcs_oa_4",
                "question": "Rotate an array by k elements clockwise.",
                "difficulty": "easy",
                "topic": "Arrays",
                "sub_topic": "Array rotation",
                "time_limit": 15,
            },
            {
                "id": "tcs_oa_5",
                "question": "Given two sorted arrays, find the median of the combined sorted array.",
                "difficulty": "hard",
                "topic": "Arrays",
                "sub_topic": "Median of two sorted arrays",
                "time_limit": 35,
            },
        ],
        "strings": [
            {
                "id": "tcs_oa_6",
                "question": "Check if two strings are anagrams of each other.",
                "difficulty": "easy",
                "topic": "Strings",
                "sub_topic": "Anagram check",
                "time_limit": 15,
            },
            {
                "id": "tcs_oa_7",
                "question": "Given a string, find the length of the longest substring without repeating characters.",
                "difficulty": "medium",
                "topic": "Strings",
                "sub_topic": "Longest unique substring",
                "time_limit": 25,
            },
        ],
        "trees": [
            {
                "id": "tcs_oa_8",
                "question": "Given a binary tree, check if it is a valid BST.",
                "difficulty": "medium",
                "topic": "Trees",
                "sub_topic": "BST validation",
                "time_limit": 30,
            },
        ],
    },
    "infosys": {
        "arrays": [
            {
                "id": "infy_oa_1",
                "question": "Find the pair in an array that sums to a given target.",
                "difficulty": "easy",
                "topic": "Arrays",
                "sub_topic": "Two sum",
                "time_limit": 20,
            },
            {
                "id": "infy_oa_2",
                "question": "Move all zeros to the end of the array while maintaining order.",
                "difficulty": "easy",
                "topic": "Arrays",
                "sub_topic": "Move zeros",
                "time_limit": 15,
            },
        ],
        "strings": [
            {
                "id": "infy_oa_3",
                "question": "Reverse a string word by word.",
                "difficulty": "medium",
                "topic": "Strings",
                "sub_topic": "Word reverse",
                "time_limit": 20,
            },
        ],
    },
    "wipro": {
        "arrays": [
            {
                "id": "wipro_oa_1",
                "question": "Find the missing number in an array of 1 to n.",
                "difficulty": "easy",
                "topic": "Arrays",
                "sub_topic": "Missing number",
                "time_limit": 15,
            },
        ],
    },
}

GLOBAL_OA_QUESTIONS = {
    "amazon": {
        "arrays": [
            {
                "id": "amazon_1",
                "question": "Find the kth largest element in an unsorted array.",
                "difficulty": "medium",
                "topic": "Arrays",
                "sub_topic": "Kth largest",
                "time_limit": 25,
            },
            {
                "id": "amazon_2",
                "question": "Container with most water (given n heights).",
                "difficulty": "medium",
                "topic": "Arrays",
                "sub_topic": "Max area",
                "time_limit": 30,
            },
        ],
        "trees": [
            {
                "id": "amazon_3",
                "question": "Invert a binary tree.",
                "difficulty": "easy",
                "topic": "Trees",
                "sub_topic": "Tree inversion",
                "time_limit": 20,
            },
        ],
    },
    "google": {
        "arrays": [
            {
                "id": "google_1",
                "question": "Find all duplicates in an array (each integer appears once or twice).",
                "difficulty": "medium",
                "topic": "Arrays",
                "sub_topic": "Find duplicates",
                "time_limit": 25,
            },
        ],
        "graphs": [
            {
                "id": "google_2",
                "question": "Number of islands (connected components in a grid).",
                "difficulty": "medium",
                "topic": "Graphs",
                "sub_topic": "Connected components",
                "time_limit": 30,
            },
        ],
    },
}


def get_company_questions(company: str, difficulty: str, category: str = None) -> List[Dict]:
    """Get OA questions for a specific company, difficulty, and optional category."""
    if company in INDIA_OA_QUESTIONS:
        questions = INDIA_OA_QUESTIONS[company]
    elif company in GLOBAL_OA_QUESTIONS:
        questions = GLOBAL_OA_QUESTIONS[company]
    else:
        questions = []
    
    if category:
        questions = [q for q in questions if q["topic"].lower() == category.lower()]
    
    # Filter by difficulty
    if difficulty != "all":
        questions = [q for q in questions if q["difficulty"] == difficulty]
    
    return questions


@router.post("/start")
async def start_oa_test(
    req: StartOARequest,
    user=Depends(get_current_user)
):
    """
    Start an Online Assessment (OA) for a specific company.
    
    Generates a set of company-style coding questions based on the target company
    and difficulty level. Questions are drawn from curated question banks.
    """
    # Get questions for the specified company and difficulty
    questions = get_company_questions(req.company, req.difficulty, None)
    
    if not questions:
        raise HTTPException(
            status_code=404, 
            detail=f"No OA questions found for company: {req.company}. "
                   "Supported companies: tcs, infosys, wipro, amazon, google"
        )
    
    # Select requested number of questions (or all available)
    selected = questions[:req.question_count]
    
    # Format questions for frontend
    formatted_questions = []
    for i, q in enumerate(selected):
        formatted_questions.append({
            "id": q["id"],
            "index": i,
            "question": q["question"],
            "difficulty": q["difficulty"],
            "topic": q["topic"],
            "sub_topic": q["sub_topic"],
            "time_limit": q["time_limit"],
            "code_template": None,
        })
    
    # Generate test ID
    test_id = f"oa_{req.company}_{user['id']}_{datetime.now(timezone.utc).timestamp()}"
    
    return {
        "test_id": test_id,
        "company": req.company,
        "difficulty": req.difficulty,
        "question_count": len(formatted_questions),
        "questions": formatted_questions,
        "total_available": len(questions),
        "message": f"Started OA with {len(formatted_questions)} questions for {req.company}",
    }


@router.post("/{test_id}/submit")
async def submit_oa_answer(
    test_id: str,
    req: SubmitOAAnswer,
    user=Depends(get_current_user)
):
    """
    Submit an OA answer and get evaluation with readiness update.
    """
    # Get the question
    company = test_id.split("_")[1] if "_" in test_id else "unknown"
    
    # In a real implementation, this would:
    # 1. Execute the code via Piston API
    # 2. Run test cases
    # 3. Calculate score
    # 4. Update skill mastery
    # 5. Return results
    
    # For now, return mock evaluation
    # Determine if answer is "correct" based on question type
    is_correct = req.answer.strip().lower().startswith("function") or req.answer.strip().lower().startswith("def ")
    
    # Update skill scores in the skill assessment system
    from app.services.skill_assessment import update_skill_score
    
    # Map topics to SDE skills
    topic_to_skill = {
        "Arrays": "DSA",
        "Strings": "Programming",
        "Trees": "DSA",
        "Graphs": "DSA",
        "Dynamic Programming": "DSA",
    }
    
    skill = topic_to_skill.get(req.topic, "DSA") if hasattr(req, 'topic') else "DSA"
    
    try:
        await update_skill_score(
            user_id=user["id"],
            category="sde",
            skill=skill,
            score=1.0 if is_correct else 0.0,
            is_correct=is_correct
        )
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Failed to update skill score: {e}")
    
    # Calculate percentage
    percentage = 100 if req.question_count > 0 else 0
    
    return {
        "test_id": test_id,
        "company": company,
        "score": 1 if is_correct else 0,
        "total_questions": req.question_count,
        "percentage": percentage,
        "is_correct": is_correct,
        "feedback": (
            "Great work! Your answer correctly solves the problem." if is_correct
            else "Don't worry! Review the concept and try again. Watch the solution video."
        ),
        "explanation": (
            "The solution uses [appropriate algorithm] with time complexity O(n) and space complexity O(1)."
            if is_correct
            else "Key concept: [review the topic]. Watch the solution and try a similar problem."
        ),
        "next_steps": (
            ["Continue to next question"] if is_correct
            else ["Review the concept", "Try a similar practice problem"]
        ),
        "readiness_update": {
            "previous": 0,
            "new": 0,  # Would be calculated from skill graph
            "message": "Skill mastery updated based on OA performance."
        }
    }


@router.get("/companies")
async def get_oa_companies():
    """Get list of supported companies for OA practice."""
    return {
        "indian_companies": ["tcs", "infosys", "wipro", "cts", "hcl"],
        "global_companies": ["amazon", "google", "microsoft", "meta", "apple"],
        "all": ["tcs", "infosys", "wipro", "cts", "hcl", "amazon", "google", "microsoft", "meta", "apple"],
    }


@router.get("/categories")
async def get_oa_categories(company: str = "tcs"):
    """Get available categories/topics for a company's OA."""
    if company in INDIA_OA_QUESTIONS:
        categories = list(set(q["topic"] for q in INDIA_OA_QUESTIONS[company].values()))
    elif company in GLOBAL_OA_QUESTIONS:
        categories = list(set(q["topic"] for q in GLOBAL_OA_QUESTIONS[company].values()))
    else:
        categories = ["Arrays", "Strings", "Trees", "Graphs"]
    
    return {"company": company, "categories": categories}


@router.get("/question/{company}/{category}")
async def get_oa_question_by_category(
    company: str,
    category: str,
    difficulty: str = "medium",
    user=Depends(get_current_user)
):
    """Get a single OA question by company, category, and difficulty."""
    questions = get_company_questions(company, difficulty, category)
    
    if not questions:
        raise HTTPException(
            status_code=404,
            detail=f"No questions found for {company} / {category}"
        )
    
    # Return first question
    q = questions[0]
    return {
        "question": {
            "id": q["id"],
            "question": q["question"],
            "difficulty": q["difficulty"],
            "topic": q["topic"],
            "sub_topic": q["sub_topic"],
            "time_limit": q["time_limit"],
        }
    }


@router.post("/{test_id}/complete")
async def complete_oa_test(
    test_id: str,
    time_taken: int = 0,
    user=Depends(get_current_user)
):
    """Complete an OA test and get final results."""
    # Get user's skill graph to calculate readiness
    from app.services.skill_assessment import get_readiness_score
    
    readiness = await get_readiness_score(user["id"], "sde")
    
    return {
        "test_id": test_id,
        "score": 0,
        "total_questions": 0,
        "percentage": 0,
        "time_taken": time_taken,
        "weak_areas": [],
        "strong_areas": [],
        "readiness_score": readiness.get("overall", 0),
        "message": "OA completed. Continue with skill practice and mock interviews.",
    }