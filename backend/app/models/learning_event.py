"""Canonical LearningEvent model.

Every meaningful learning/assessment action emits exactly one event through
this schema.  This is the single longitudinal evidence layer that backs
the Evidence Graph.

Sources that emit events:
    lesson, practice, oa_question, oa_complete, mock_oa, interview_answer,
    interview_complete, repair, retest, srs_review, daily_challenge

The event is written by study_engine.record_activity() (the canonical
completion sink) or by dedicated emitters in oa.py / interview.py /
questions_solve.py that call _emit_learning_event().
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ─── Diagnosis codes ──────────────────────────────────────────────────────
#
# Structured labels for WHY a student succeeded or failed, derived from
# observable evidence — never from psychological inference.

CONCEPT_GAP = "CONCEPT_GAP"
PATTERN_RECOGNITION = "PATTERN_RECOGNITION"
IMPLEMENTATION_ERROR = "IMPLEMENTATION_ERROR"
EDGE_CASE_FAILURE = "EDGE_CASE_FAILURE"
COMPLEXITY_ERROR = "COMPLEXITY_ERROR"
TIME_MANAGEMENT = "TIME_MANAGEMENT"
CARELESS_ERROR = "CARELESS_ERROR"
DEBUGGING = "DEBUGGING"
KNOWLEDGE_RECALL = "KNOWLEDGE_RECALL"
TRANSFER_FAILURE = "TRANSFER_FAILURE"
COMMUNICATION_DEPTH = "COMMUNICATION_DEPTH"
TRADEOFF_REASONING = "TRADEOFF_REASONING"
REQUIREMENT_MISREAD = "REQUIREMENT_MISREAD"

ALL_DIAGNOSIS_CODES = {
    CONCEPT_GAP,
    PATTERN_RECOGNITION,
    IMPLEMENTATION_ERROR,
    EDGE_CASE_FAILURE,
    COMPLEXITY_ERROR,
    TIME_MANAGEMENT,
    CARELESS_ERROR,
    DEBUGGING,
    KNOWLEDGE_RECALL,
    TRANSFER_FAILURE,
    COMMUNICATION_DEPTH,
    TRADEOFF_REASONING,
    REQUIREMENT_MISREAD,
}


class LearningEventIn(BaseModel):
    """Input schema for writing a LearningEvent.

    All fields except user_id and activity_type are optional — sources
    populate what they have.  skill_id, diagnosis_codes, mastery_before/after
    are filled by the emitter or the record_activity pipeline.
    """

    activity_type: str = Field(
        ..., description="learn | review | practice | challenge | "
        "oa_question | oa_complete | mock_oa | interview_answer | "
        "interview_complete | repair | retest | srs_review | "
        "daily_challenge"
    )
    source: str = Field(..., description="lesson | practice | oa | interview | "
        "repair | retest | srs | gamification | daily_challenge | "
        "question_bank")
    skill_id: Optional[str] = Field(None, description="Canonical skill ID "
        "(domain.subskill). Mapped from the source's naming scheme.")
    subskill_id: Optional[str] = None
    question_id: Optional[str] = None
    assessment_id: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    passed: bool = False
    score: Optional[float] = None
    time_spent_seconds: int = 0
    hints_used: int = 0
    attempt_number: int = 1
    mastery_before: Optional[float] = None
    mastery_after: Optional[float] = None
    diagnosis_codes: List[str] = Field(default_factory=list,
        description="Structured WHY codes — see ALL_DIAGNOSIS_CODES")
    repair_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LearningEvent(LearningEventIn):
    """Persisted learning event."""

    id: str
    user_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"extra": "ignore"}


class LearningEventOut(BaseModel):
    """Serialized event for API responses."""

    id: str
    user_id: str
    timestamp: datetime
    activity_type: str
    source: str
    skill_id: Optional[str] = None
    subskill_id: Optional[str] = None
    question_id: Optional[str] = None
    assessment_id: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    passed: bool
    score: Optional[float] = None
    time_spent_seconds: int = 0
    hints_used: int = 0
    attempt_number: int = 1
    mastery_before: Optional[float] = None
    mastery_after: Optional[float] = None
    diagnosis_codes: List[str] = Field(default_factory=list)
    repair_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
