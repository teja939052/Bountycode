from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from enum import Enum
import json


# ──────────────────────────────────────────────────────────────────
# Lock Types
# ──────────────────────────────────────────────────────────────────
class LockType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    CODE_EXPRESSION = "code_expression"
    CONCEPT_CHECK = "concept_check"
    RUNTIME = "runtime"
    PREDICTION = "prediction"
    ARRANGE = "arrange"
    FILL_THE_LOCK = "fill_the_lock"
    FIX_THE_BUG = "fix_the_bug"


# ──────────────────────────────────────────────────────────────────
# Hint Levels (deterministic, no AI)
# ──────────────────────────────────────────────────────────────────
class HintLevel(BaseModel):
    id: int = Field(default=1, ge=1)
    text: str
    reveals: Optional[str] = None  # What this hint reveals (for tutor)
    is_final: bool = False  # Last hint before solution


# ──────────────────────────────────────────────────────────────────
# Misconception Types
# ──────────────────────────────────────────────────────────────────
class MisconceptionType(str, Enum):
    WRONG_BOUNDARY = "wrong_boundary"
    OFF_BY_ONE = "off_by_one"
    INCORRECT_MIDPOINT = "incorrect_midpoint"
    DOES_NOT_HANDLE_DUPLICATES = "does_not_handle_duplicates"
    OFF_BY_ONE_INDEX = "off_by_one_index"
    INCORRECT_TERMINATION = "incorrect_termination"
    INFINITE_LOOP = "infinite_loop"
    MISSED_EDGE_CASE = "missed_edge_case"


# ──────────────────────────────────────────────────────────────────
# Accepted Code Expressions (for LockType.CODE_EXPRESSION)
# ──────────────────────────────────────────────────────────────────
class AcceptedExpression(BaseModel):
    pattern: str  # e.g. "(low + high) // 2"
    description: str  # e.g. "integer midpoint, floor division"


# ──────────────────────────────────────────────────────────────────
# Lock Definition (The "Key")
# ──────────────────────────────────────────────────────────────────
class LockDefinition(BaseModel):
    id: str  # e.g. "identify-sorted-property"
    type: LockType
    label: str  # Human-readable, e.g. "Identify the Sorted Property"
    description: str
    accepted: Optional[List[str]] = None  # Accepted values/patterns
    rejected: Optional[List[str]] = None  # Common wrong patterns
    hint_text: str  # Hint shown when lock is active
    misconception: Optional[MisconceptionType] = None  # Associated misconception
    hint_graph_index: Optional[int] = None  # Index into hint graph


# ──────────────────────────────────────────────────────────────────
# Problem (The Challenge)
# ──────────────────────────────────────────────────────────────────
class ProblemBase(BaseModel):
    id: str  # e.g. "binary-search-001"
    title: str
    description: str
    mode: str  # "predict" | "arrange" | "fill_the_lock" | "fix_the_bug" | "full_coding" | "oa"
    difficulty: str  # "easy" | "medium" | "hard"

    # --- Lock Definition (The "Key") ---
    locks: List[LockDefinition] = Field(default_factory=list)

    # --- Reference Solution (Deterministic, not executed remotely) ---
    reference_solution: Optional[str] = None  # Canonical solution code
    reference_output: Optional[str] = None  # Expected output for given tests

    # --- Test Cases (Precomputed, used by Behavioral Judge) ---
    test_cases: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Precomputed {{input, expected}} pairs. Never executed remotely.",
    )

    # --- Hint Graph ---
    hint_graph: List[HintLevel] = Field(
        default_factory=list,
        description="Progressive hints. Deterministic, no AI.",
    )

    # --- Misconception Map ---
    misconceptions: List[MisconceptionType] = Field(
        default_factory=list,
        description="Common mistakes students make for this problem.",
    )

    # --- Learning Objective ---
    learning_goal: str  # e.g. "understand search-space reduction"

    # --- Complexity (Reference) ---
    time_complexity: str = "O(log n)"
    space_complexity: str = "O(1)"

    # --- Challenge Type Hints ---
    estimated_xp: int = 10
    mastery_impact: float = 0.05  # e.g. +5% mastery when passed


# ──────────────────────────────────────────────────────────────────
# Problem In / Out
# ──────────────────────────────────────────────────────────────────
class ProblemCreate(ProblemBase):
    pass


class ProblemRead(ProblemBase):
    id: str

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────────────────────────
# Student Submission
# ──────────────────────────────────────────────────────────────────
class StudentCodeSubmission(BaseModel):
    problem_id: str
    language: str  # "python" | "javascript" | "cpp" | "java"
    code: str
    stdin: str = ""  # Optional input for runtime
    attempt_number: int = 1  # For SRS / misconception tracking


# ──────────────────────────────────────────────────────────────────
# Judge Result (What the engine returns)
# ──────────────────────────────────────────────────────────────────
class JudgeResult(BaseModel):
    success: bool
    mode: str  # "static" | "behavioral" | "runtime"
    message: str
    passed_tests: int = 0
    total_tests: int = 0
    score: float = 0.0  # percentage
    xp_awarded: int = 0
    mastery_gain: float = 0.0
    lock_unlocked: Optional[str] = None  # Lock ID if just unlocked
    hint_index: Optional[int] = None  # Next hint to show
    misconception: Optional[MisconceptionType] = None
    hint_text: Optional[str] = None  # Tutor message


# ──────────────────────────────────────────────────────────────────
# SRS (Spaced Repetition) Entry
# ──────────────────────────────────────────────────────────────────
class SRSEntry(BaseModel):
    problem_id: str
    student_id: str
    last_attempt: str  # ISO datetime
    correct: bool
    easiness_factor: float = 2.5  # SuperMemo default
    repetition_interval: int = 1  # days
    due_date: str  # ISO datetime
    times_shown: int = 0
    times_correct: int = 0