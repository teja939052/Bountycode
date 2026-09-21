from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

VALID_QUESTION_TYPES = {"coding", "aptitude", "behavioral", "system_design", "hr", "sql", "gd", "group_discussion"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}


class MCQOption(BaseModel):
    text: str = Field(default="", max_length=1024)
    is_correct: bool = False
    misconception_tag: Optional[str] = Field(default=None, max_length=128)
    repair_hint: Optional[str] = Field(default=None, max_length=1024)


class SQLSchemaMetadata(BaseModel):
    schema_ddl: str = Field(default="", max_length=20000)
    seed_inserts: str = Field(default="", max_length=20000)
    expected_query: str = Field(default="", max_length=20000)
    enforce_order: bool = False


class CuratedQuestion(BaseModel):
    id: Optional[str] = None
    type: str = Field(default="coding", max_length=32)
    company: List[str] = Field(default_factory=list, max_length=10)
    role: str = Field(default="SDE", max_length=64)
    difficulty: str = Field(default="medium", max_length=16)
    topic: str = Field(default="", max_length=128)
    sub_topic: str = Field(default="", max_length=128)
    question: str = Field(default="", max_length=10000)
    options: List[Union[str, Dict[str, Any]]] = Field(default_factory=list, max_length=10)
    correct_answer: str = Field(default="", max_length=512)
    explanation: str = Field(default="", max_length=5000)
    hints: List[str] = Field(default_factory=list, max_length=10)
    solution: Dict[str, Any] = Field(default_factory=dict)
    frequency: int = Field(default=0, ge=0)
    source: str = Field(default="User Submitted", max_length=128)
    submitted_by: Optional[str] = None
    upvotes: int = Field(default=0, ge=0)
    downvotes: int = Field(default=0, ge=0)
    reported: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    sql_schema: Optional[SQLSchemaMetadata] = None
    test_cases: List[Dict[str, Any]] = Field(default_factory=list)
    trust_status: str = Field(default="unverified", max_length=32)
    is_executable: bool = Field(default=False)


class QuestionFilter(BaseModel):
    company: Optional[str] = Field(default=None, max_length=128)
    role: Optional[str] = Field(default=None, max_length=64)
    topic: Optional[str] = Field(default=None, max_length=128)
    sub_topic: Optional[str] = Field(default=None, max_length=128)
    difficulty: Optional[str] = Field(default=None, max_length=16)
    type: Optional[str] = Field(default=None, max_length=32)
    search: Optional[str] = Field(default=None, max_length=256)
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)


class SubmitAnswer(BaseModel):
    question_id: str = Field(..., min_length=1, max_length=64)
    answer: str = Field(..., min_length=1, max_length=50000)
    time_taken: Optional[int] = Field(default=None, ge=0, le=3600)


class AnswerFeedback(BaseModel):
    question_id: str
    answer: str
    score: int = Field(ge=1, le=10)
    is_correct: bool
    feedback: str
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    better_approach: Optional[str] = None
    xp_gained: int = Field(default=0, ge=0)


class QuestionSubmission(BaseModel):
    type: str = Field(..., min_length=1, max_length=32)
    company: List[str] = Field(default_factory=list, max_length=10)
    role: str = Field(default="SDE", max_length=64)
    difficulty: str = Field(default="medium", max_length=16)
    topic: str = Field(default="", max_length=128)
    sub_topic: str = Field(default="", max_length=128)
    question: str = Field(..., min_length=10, max_length=10000)
    options: List[str] = Field(default_factory=list, max_length=10)
    correct_answer: str = Field(default="", max_length=512)
    explanation: str = Field(default="", max_length=5000)
    hints: List[str] = Field(default_factory=list, max_length=10)
    solution: Dict[str, Any] = Field(default_factory=dict)


class QuestionVote(BaseModel):
    question_id: str = Field(..., min_length=1, max_length=64)
    vote: int = Field(..., ge=-1, le=1)
    reason: Optional[str] = Field(default=None, max_length=500,
                                  description="Optional report reason (stored with downvotes)")
