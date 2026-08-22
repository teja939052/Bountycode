from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class StartInterview(BaseModel):
    job_role: str
    company: str = "general"
    interview_type: str = "mixed"
    difficulty: str = "medium"


class SubmitAnswer(BaseModel):
    interview_id: str
    question: str
    answer: str
    time_taken: int = 0
    is_follow_up: bool = False
    question_type: Optional[str] = None


class QuestionFeedback(BaseModel):
    score: int
    breakdown: Dict[str, int] = {}
    strengths: List[str] = []
    improvements: List[str] = []
    better_answer: str = ""
    reaction: str = ""
    follow_up_suggested: bool = False


class QARecord(BaseModel):
    question: str
    answer: str
    question_type: str = ""
    difficulty: str = "medium"
    score: int = 0
    breakdown: Dict[str, int] = {}
    feedback: Optional[QuestionFeedback] = None
    is_follow_up: bool = False
    company: str = "general"
    time_taken: int = 0


class InterviewResult(BaseModel):
    interview_id: str
    job_role: str
    company: str
    overall_score: float
    score_breakdown: Dict[str, float] = {}
    questions: List[QARecord] = []
    total_questions: int = 0
    difficulty_progression: List[str] = []
    strength_areas: List[str] = []
    improvement_areas: List[str] = []
    readiness_score: float = 0
