"""AI Interview service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session
from app.models.assessments import InterviewSession

router_prefix = "/api/v1/ai-interview"

COMPANY_PROFILES = {
    "tcs_nqt": {
        "name": "TCS NQT",
        "description": "TCS National Qualifier Test",
        "topics": ["aptitude", "logical", "verbal", "programming"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
    "tcs_ipa": {
        "name": "TCS IPA",
        "description": "TCS IPA (Intelligent Placement Assessment)",
        "topics": ["aptitude", "logical", "verbal", "cs_fundamentals", "coding"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
    "infytq": {
        "name": "Infosys InfyTQ",
        "description": "Infosys InfyTQ Certification",
        "topics": ["aptitude", "logical", "cs_fundamentals", "coding"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
    "wipro_nlth": {
        "name": "Wipro NLTH",
        "description": "Wipro National Level Talent Hunt",
        "topics": ["aptitude", "logical", "verbal", "coding"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
    "accenture": {
        "name": "Accenture",
        "description": "Accenture Assessment",
        "topics": ["aptitude", "logical", "verbal", "coding"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
    "cognizant_genc": {
        "name": "Cognizant GenC",
        "description": "Cognizant GenC Assessment",
        "topics": ["aptitude", "logical", "verbal", "coding"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
    "capgemini_amcat": {
        "name": "Capgemini",
        "description": "Capgemini Assessment",
        "topics": ["aptitude", "logical", "verbal", "coding"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
    "ibm_entry": {
        "name": "IBM Entry",
        "description": "IBM Entry Level Assessment",
        "topics": ["aptitude", "logical", "verbal", "coding"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
    "amazon_sde": {
        "name": "Amazon SDE",
        "description": "Amazon Software Development Engineer",
        "topics": ["data_structures", "algorithms", "system_design", "coding"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
    "google": {
        "name": "Google",
        "description": "Google Interview",
        "topics": ["data_structures", "algorithms", "system_design", "coding"],
        "difficulty_levels": ["medium", "hard"],
    },
    "microsoft": {
        "name": "Microsoft",
        "description": "Microsoft Interview",
        "topics": ["data_structures", "algorithms", "system_design", "coding"],
        "difficulty_levels": ["medium", "hard"],
    },
    "other": {
        "name": "Other",
        "description": "Other Company Preparation",
        "topics": ["aptitude", "logical", "verbal", "coding"],
        "difficulty_levels": ["easy", "medium", "hard"],
    },
}


def assign_companies(companies: List[str]) -> List[str]:
    """Assign companies based on input."""
    return [c for c in companies if c in COMPANY_PROFILES]


async def start_ai_interview(user_id: str, role: str = "software_engineer", difficulty: str = "medium"):
    """Start an AI interview session."""
    async with get_session() as session:
        interview = InterviewSession(
            user_id=user_id,
            role=role,
            difficulty=difficulty,
            status="in_progress",
        )
        session.add(interview)
        await session.commit()
        await session.refresh(interview)
    return {
        "interview_id": str(interview.id),
        "status": interview.status,
    }


async def get_interview_result(interview_id: str, user_id: str):
    """Get interview results."""
    async with get_session() as session:
        result = await session.execute(
            select(InterviewSession).where(
                InterviewSession.id == interview_id,
                InterviewSession.user_id == user_id,
            )
        )
        interview = result.scalar_one_or_none()
    if not interview:
        return None
    return {
        "interview_id": str(interview.id),
        "status": interview.status,
        "score": interview.score,
        "feedback": interview.feedback,
    }


async def generate_interview_question(
    interview_id: str,
    question_type: str = "coding",
    difficulty: str = "medium",
    topic: Optional[str] = None,
) -> dict:
    """Generate an interview question."""
    return {
        "interview_id": interview_id,
        "question_id": f"q_{interview_id}_{datetime.now(timezone.utc).timestamp()}",
        "question": f"Sample {question_type} question for {difficulty} level",
        "question_type": question_type,
        "difficulty": difficulty,
    }


async def evaluate_answer(
    interview_id: str,
    question_id: str,
    answer: str,
) -> dict:
    """Evaluate an interview answer."""
    return {
        "interview_id": interview_id,
        "question_id": question_id,
        "answer": answer,
        "score": 7,
        "feedback": "Good answer with room for improvement.",
    }


async def generate_interview_tips(
    interview_id: str,
    focus_area: str = "general",
) -> dict:
    """Generate interview tips."""
    return {
        "interview_id": interview_id,
        "focus_area": focus_area,
        "tips": [
            "Practice explaining your thought process out loud",
            "Clarify requirements before coding",
            "Test your solution with edge cases",
        ],
    }

async def COMPANY_PROFILES(user_id: str) -> dict:
    """Stub for COMPANY_PROFILES."""
    return {"user_id": user_id}


async def _mode_cfg(user_id: str) -> dict:
    """Stub for _mode_cfg."""
    return {"user_id": user_id}
