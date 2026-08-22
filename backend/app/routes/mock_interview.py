from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/interview", tags=["mock-interview"])


# Request/Response models
class StartInterviewRequest(BaseModel):
    """Request to start a mock interview."""
    job_role: str = Field("sde", description="Target job role (sde, backend, frontend, fullstack)")
    company: str = Field("startup", description="Target company (startup, tcs, infosys, amazon, google)")
    interview_type: str = Field("technical", description="Interview type: technical/behavioral")
    difficulty: str = Field("medium", description="Difficulty: easy/medium/hard")


class AnswerSubmit(BaseModel):
    """Submit an interview answer."""
    interview_id: str = Field(..., description="Interview session ID")
    question: str = Field(..., description="Question text")
    answer: str = Field(..., description="Candidate's answer")
    time_taken: int = Field(0, ge=0, description="Time taken in seconds")
    is_follow_up: bool = Field(False, description="Whether this is a follow-up question")


class InterviewResult(BaseModel):
    """Interview result with score breakdown."""
    interview_id: str
    overall_score: float
    category_scores: Dict[str, float]
    feedback: str
    strengths: List[str]
    improvements: List[str]
    follow_up_questions: List[str]


# Interview question banks
TECHNICAL_QUESTIONS = {
    "sde": {
        "easy": [
            {
                "id": "tech_1",
                "question": "Write a function to reverse a string.",
                "topic": "Programming",
                "sub_topic": "String manipulation",
            },
            {
                "id": "tech_2",
                "question": "Find the maximum element in an array.",
                "topic": "Arrays",
                "sub_topic": "Basic search",
            },
        ],
        "medium": [
            {
                "id": "tech_3",
                "question": "Given an array of integers, find the pivot index where left sum equals right sum.",
                "topic": "Arrays",
                "sub_topic": "Pivot index",
            },
            {
                "id": "tech_4",
                "question": "Implement a stack using classes.",
                "topic": "OOP",
                "sub_topic": "Stack implementation",
            },
        ],
        "hard": [
            {
                "id": "tech_5",
                "question": "Design a rate limiter. Discuss algorithms and time/space complexity.",
                "topic": "System Design",
                "sub_topic": "Rate limiter design",
            },
        ],
    },
    "backend": {
        "easy": [
            {
                "id": "backend_1",
                "question": "Write a SQL query to find the second highest salary.",
                "topic": "DBMS",
                "sub_topic": "Aggregate functions",
            },
        ],
        "medium": [
            {
                "id": "backend_2",
                "question": "Design a connection pool for database connections.",
                "topic": "System Design",
                "sub_topic": "Connection pooling",
            },
        ],
    },
}

BEHAVIORAL_QUESTIONS = {
    "sde": {
        "easy": [
            {
                "id": "beh_1",
                "question": "Tell me about yourself.",
                "topic": "Introduction",
                "sub_topic": "Personal introduction",
            },
            {
                "id": "beh_2",
                "question": "Why do you want to work at this company?",
                "topic": "Company fit",
                "sub_topic": "Motivation",
            },
        ],
        "medium": [
            {
                "id": "beh_3",
                "question": "Tell me about a time you faced a conflict in a team project. How did you handle it?",
                "topic": "Conflict resolution",
                "sub_topic": "STAR method",
            },
            {
                "id": "beh_4",
                "question": "Describe a time you had to meet a tight deadline. What was your approach?",
                "topic": "Time management",
                "sub_topic": "Deadline pressure",
            },
        ],
    },
}


class StartInterview:
    """Mock interview session manager."""
    
    def __init__(self, job_role: str, company: str, interview_type: str, difficulty: str):
        self.job_role = job_role
        self.company = company
        self.interview_type = interview_type
        self.difficulty = difficulty
        self.questions = self._get_questions()
        self.current_question_index = 0
        self.answers = []
        self.session_start = datetime.now(timezone.utc)
    
    def _get_questions(self) -> List[Dict]:
        """Get questions based on interview type."""
        if self.interview_type == "technical":
            return TECHNICAL_QUESTIONS.get(self.job_role, {}).get(self.difficulty, [])
        else:
            return BEHAVIORAL_QUESTIONS.get(self.job_role, {}).get(self.difficulty, [])
    
    def get_current_question(self) -> Optional[Dict]:
        """Get the current question."""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
    
    def submit_answer(self, answer: str, time_taken: int) -> Dict:
        """Submit an answer and get the next question."""
        self.answers.append({
            "question_id": self.questions[self.current_question_index]["id"] if self.current_question_index < len(self.questions) else "unknown",
            "question": self.get_current_question()["question"] if self.get_current_question() else "",
            "answer": answer,
            "time_taken": time_taken,
        })
        
        self.current_question_index += 1
        
        next_question = self.get_current_question()
        
        return {
            "answered": True,
            "was_last": self.current_question_index >= len(self.questions),
            "next_question": {
                "id": next_question["id"] if next_question else None,
                "question": next_question["question"] if next_question else "",
                "topic": next_question["topic"] if next_question else "",
                "sub_topic": next_question["sub_topic"] if next_question else "",
            } if next_question else None,
            "total_questions": len(self.questions),
        }
    
    def get_result(self) -> InterviewResult:
        """Calculate interview result with scores."""
        # Simple scoring based on answer quality indicators
        total_questions = len(self.answers)
        if total_questions == 0:
            return InterviewResult(
                interview_id=self._generate_id(),
                overall_score=0.0,
                category_scores={},
                feedback="No answers provided.",
                strengths=[],
                improvements=["Practice answering interview questions"],
                follow_up_questions=[],
            )
        
        # Score based on answer length and content indicators
        scores = []
        for ans in self.answers:
            answer_text = ans["answer"]
            # Simple scoring: longer answers tend to be more complete
            length_score = min(len(answer_text) / 50, 1.0)  # Normalize to 0-1
            content_score = 0.8 if len(answer_text) > 50 else 0.5  # Basic content check
            overall = (length_score + content_score) / 2
            scores.append(overall)
        
        overall_score = sum(scores) / len(scores) if scores else 0.0
        
        # Category scores based on question topics
        category_scores = self._calculate_category_scores(scores, total_questions)
        
        # Generate feedback
        strengths = self._identify_strengths(scores)
        improvements = self._identify_improvements(scores)
        
        # Generate follow-up questions based on weak areas
        follow_up_questions = self._generate_follow_ups(category_scores)
        
        return InterviewResult(
            interview_id=self._generate_id(),
            overall_score=round(overall_score, 2),
            category_scores=category_scores,
            feedback=self._generate_feedback(overall_score, strengths, improvements),
            strengths=strengths,
            improvements=improvements,
            follow_up_questions=follow_up_questions,
        )
    
    def _generate_id(self) -> str:
        return f"interview_{self.job_role}_{self.company}_{datetime.now(timezone.utc).timestamp()}"
    
    def _calculate_category_scores(self, scores: List[float], total: int) -> Dict[str, float]:
        """Calculate scores by category based on question topics."""
        # Simplified: return overall score for now
        return {"overall": round(sum(scores) / len(scores), 2) if scores else 0.0}
    
    def _identify_strengths(self, scores: List[float]) -> List[str]:
        """Identify strengths based on scores."""
        strong = [s for s in scores if s >= 0.7]
        if not strong:
            return ["Showing effort - keep practicing!"]
        
        strengths = []
        if len(strong) / len(scores) > 0.5:
            strengths.append("Good overall performance")
        return strengths
    
    def _identify_improvements(self, scores: List[float]) -> List[str]:
        """Identify areas for improvement."""
        weak = [s for s in scores if s < 0.5]
        improvements = []
        
        if weak:
            improvements.append("Practice structuring answers more clearly")
        if len([s for s in scores if s < 0.7]) / len(scores) > 0.5:
            improvements.append("Provide more detailed examples in answers")
        
        return improvements or ["Continue practicing to improve confidence"]
    
    def _generate_feedback(self, score: float, strengths: List[str], improvements: List[str]) -> str:
        """Generate personalized feedback."""
        parts = []
        
        if score >= 0.75:
            parts.append("Strong performance! ")
        elif score >= 0.5:
            parts.append("Good effort! ")
        else:
            parts.append("Keep practicing! ")
        
        if strengths:
            parts.append(" ".join(strengths))
        
        if improvements:
            parts.append("Focus on: " + ", ".join(strimprovements))
        
        parts.append("Continue practicing with mock interviews.")
        
        return " ".join(parts)
    
    def _generate_follow_ups(self, category_scores: Dict[str, float]) -> List[str]:
        """Generate follow-up questions based on weak areas."""
        follow_ups = []
        
        for category, score in category_scores.items():
            if score < 0.6:
                if category == "Programming":
                    follow_ups.append("Can you explain your thought process for this problem?")
                elif category == "System Design":
                    follow_ups.append("How would you scale this design?")
                elif category == "DBMS":
                    follow_ups.append("What indexes would you add?")
                else:
                    follow_ups.append("Any alternative approaches?")
        
        return follow_ups if follow_ups else ["Would you like to try another question?"]


# Create interview session factory
_interview_sessions: Dict[str, StartInterview] = {}


@router.post("/start")
async def start_mock_interview(
    req: StartInterviewRequest,
    user=Depends(get_current_user)
):
    """
    Start a mock interview session.
    
    Generates a set of interview questions based on the target role,
    company, interview type, and difficulty level.
    """
    # Create a new interview session
    session = StartInterview(
        job_role=req.job_role,
        company=req.company,
        interview_type=req.interview_type,
        difficulty=req.difficulty
    )
    
    # Store session
    session_id = session._generate_id()
    _interview_sessions[session_id] = session
    
    # Get first question
    current_question = session.get_current_question()
    
    if not current_question:
        raise HTTPException(
            status_code=400,
            detail="No questions available for the selected role/difficulty"
        )
    
    return {
        "interview_id": session_id,
        "role": req.job_role,
        "company": req.company,
        "interview_type": req.interview_type,
        "difficulty": req.difficulty,
        "total_questions": len(session.questions),
        "current_question_index": 1,
        "question": {
            "id": current_question["id"],
            "question": current_question["question"],
            "topic": current_question["topic"],
            "sub_topic": current_question["sub_topic"],
        },
        "instructions": "You have 5 minutes to answer this question. Provide a detailed response.",
        "message": f"Mock {req.interview_type} interview started for {req.job_role} at {req.company}",
    }


@router.post("/{interview_id}/answer")
async def submit_interview_answer(
    interview_id: str,
    req: AnswerSubmit,
    user=Depends(get_current_user)
):
    """
    Submit an answer and get the next question or interview result.
    """
    session = _interview_sessions.get(interview_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    # Submit the answer
    result = session.submit_answer(req.answer, req.time_taken)
    
    # If this was the last question, get the final result
    if result["was_last"]:
        interview_result = session.get_result()
        # Remove the session after completion
        del _interview_sessions[interview_id]
        
        return {
            "interview_id": interview_id,
            "status": "completed",
            "result": {
                "overall_score": interview_result.overall_score,
                "category_scores": interview_result.category_scores,
                "feedback": interview_result.feedback,
                "strengths": interview_result.strengths,
                "improvements": interview_result.improvements,
                "follow_up_questions": interview_result.follow_up_questions,
            },
            "message": "Interview session completed.",
        }
    else:
        # Return the next question
        next_question = session.get_current_question()
        
        return {
            "interview_id": interview_id,
            "status": "in_progress",
            "question": {
                "id": next_question["id"] if next_question else None,
                "question": next_question["question"] if next_question else "",
                "topic": next_question["topic"] if next_question else "",
                "sub_topic": next_question["sub_topic"] if next_question else "",
            } if next_question else None,
            "is_last": result["was_last"],
            "total_questions": len(session.questions),
            "message": "Answer recorded. Moving to next question.",
        }


@router.get("/{interview_id}/result")
async def get_interview_result(
    interview_id: str,
    user=Depends(get_current_user)
):
    """Get the interview result for a completed session."""
    session = _interview_sessions.get(interview_id)
    if not session:
        # Session might be completed, try to get from stored results
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Interview session not found or completed")
    
    interview_result = session.get_result()
    return {
        "interview_id": interview_id,
        "result": {
            "overall_score": interview_result.overall_score,
            "category_scores": interview_result.category_scores,
            "feedback": interview_result.feedback,
            "strengths": interview_result.strengths,
            "improvements": interview_result.improvements,
            "follow_up_questions": interview_result.follow_up_questions,
        }
    }


@router.get("/available-roles")
async def get_available_roles():
    """Get available job roles for interviews."""
    return {
        "roles": ["sde", "backend", "frontend", "fullstack", "devops"],
        "companies": ["startup", "tcs", "infosys", "amazon", "google", "microsoft"],
        "interview_types": ["technical", "behavioral"],
        "difficulties": ["easy", "medium", "hard"],
    }


@router.get("/questions/{role}/{type}/{difficulty}")
async def get_sample_questions(
    role: str,
    interview_type: str,
    difficulty: str,
    user=Depends(get_current_user)
):
    """Get sample questions for a role/type/difficulty without starting a session."""
    if interview_type == "technical":
        questions = TECHNICAL_QUESTIONS.get(role, {}).get(difficulty, [])
    else:
        questions = BEHAVIORAL_QUESTIONS.get(role, {}).get(difficulty, [])
    
    return {
        "role": role,
        "type": interview_type,
        "difficulty": difficulty,
        "questions": questions,
    }