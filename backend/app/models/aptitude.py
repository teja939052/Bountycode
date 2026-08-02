from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AptitudeCategory(BaseModel):
    id: str
    name: str
    description: str
    question_count: int = 0


class AptitudeQuestion(BaseModel):
    id: str
    category: str
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    difficulty: str = "medium"
    time_limit: int = 60


class AptitudeTest(BaseModel):
    id: str
    user_id: str
    category: str
    questions: List[AptitudeQuestion] = []
    answers: List[Optional[str]] = []
    score: int = 0
    total_questions: int = 0
    time_taken: int = 0
    status: str = "in_progress"
    created_at: datetime


class StartAptitudeTest(BaseModel):
    category: str = "quantitative"
    difficulty: str = "medium"
    question_count: int = 20


class SubmitAptitudeAnswer(BaseModel):
    test_id: str
    question_index: int
    answer: str


class AptitudeResult(BaseModel):
    test_id: str
    category: str
    score: int
    total_questions: int
    percentage: float
    time_taken: int
    questions: List[dict] = []
    weak_areas: List[str] = []
    strong_areas: List[str] = []
