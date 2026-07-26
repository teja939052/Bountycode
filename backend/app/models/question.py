from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CuratedQuestion(BaseModel):
    id: Optional[str] = None
    type: str = "coding"  # coding | aptitude | behavioral | system_design | hr
    company: List[str] = []
    role: str = "SDE"
    difficulty: str = "medium"
    topic: str = ""
    sub_topic: str = ""
    question: str = ""
    options: List[str] = []
    correct_answer: str = ""
    explanation: str = ""
    hints: List[str] = []
    solution: Dict[str, Any] = {}
    frequency: int = 0
    source: str = "User Submitted"
    submitted_by: Optional[str] = None
    upvotes: int = 0
    downvotes: int = 0
    reported: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class QuestionFilter(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    topic: Optional[str] = None
    sub_topic: Optional[str] = None
    difficulty: Optional[str] = None
    type: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    limit: int = 20


class SubmitAnswer(BaseModel):
    question_id: str
    answer: str = Field(min_length=1)
    time_taken: Optional[int] = None


class AnswerFeedback(BaseModel):
    question_id: str
    answer: str
    score: int
    is_correct: bool
    feedback: str
    strengths: List[str] = []
    improvements: List[str] = []
    better_approach: Optional[str] = None
    xp_gained: int = 0


class QuestionSubmission(BaseModel):
    type: str
    company: List[str] = []
    role: str = "SDE"
    difficulty: str = "medium"
    topic: str = ""
    sub_topic: str = ""
    question: str
    options: List[str] = []
    correct_answer: str = ""
    explanation: str = ""
    hints: List[str] = []
    solution: Dict[str, Any] = {}


class QuestionVote(BaseModel):
    question_id: str
    vote: int = Field(..., ge=-1, le=1)
