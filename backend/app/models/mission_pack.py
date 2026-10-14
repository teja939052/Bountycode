"""Mission Pack — canonical content production unit for BountyCode.

A Mission Pack is the atomic teaching unit for one placement-relevant pattern.
It is the ONLY way new teaching content enters the platform.

Pack anatomy:
  - concept / why_it_matters / prerequisites
  - misconceptions with reteach routes
  - captain_byte moments
  - 9-step teaching loop (discover → transfer)
  - practice set
  - timed placement proof
  - SRS enrollment
  - company variants

Production rules:
  - One pack = one pattern.
  - Every pack must be usable by the unified lesson player, practice mode, assessment, and company prep.
  - Authors edit the data files; the renderer is generic.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════
# Models
# ═══════════════════════════════════════════════════════════════

class CaptainByteMoment(BaseModel):
    intro: str = ""
    correct: List[str] = []
    wrong: List[str] = []
    after_break: str = ""
    after_mastery: str = ""
    retry_prompt: str = ""


class MisconceptionEntry(BaseModel):
    code: str
    signature: str
    reteach_route: str
    reteach_action: str


class PracticeItem(BaseModel):
    kind: str  # "mcq" | "numeric" | "code" | "fill_blank"
    prompt: str
    answer: Any
    options: Optional[List[str]] = None
    explanation: str = ""
    difficulty: str = "medium"
    company_tags: List[str] = []


class ProofQuestion(BaseModel):
    id: str
    prompt: str
    answer_format: str  # "mcq" | "numeric" | "code" | "text"
    options: Optional[List[str]] = None
    correct: Any = ""
    explanation: str = ""
    time_limit_seconds: int = 60
    company_tags: List[str] = []


class CompanyVariant(BaseModel):
    company: str
    role: str
    difficulty: str = "medium"
    extra_practice: List[str] = []
    proof_questions: List[ProofQuestion] = []


class MissionPack(BaseModel):
    """Canonical content unit for one placement pattern."""

    id: str
    title: str
    domain: str  # "aptitude" | "reasoning" | "verbal" | "coding" | "cs_core" | "behavioral" | "system_design"
    concept: str
    skill_id: str  # e.g. "aptitude.percentages"
    tags: List[str] = []

    # Depth metadata
    difficulty: str = "medium"
    estimated_minutes: int = 20
    mastery_threshold: int = 75

    # Teaching content
    why_it_matters: str = ""
    prerequisites: List[str] = []
    misconceptions: List[MisconceptionEntry] = []
    captain_byte: CaptainByteMoment = Field(default_factory=CaptainByteMoment)

    # 9-step loop
    discover: Dict[str, Any] = Field(default_factory=dict)
    understand: Any = None
    manipulate: Dict[str, Any] = Field(default_factory=dict)
    predict: Dict[str, Any] = Field(default_factory=dict)
    build: Dict[str, Any] = Field(default_factory=dict)
    break_step: Dict[str, Any] = Field(default_factory=dict)
    debug: Dict[str, Any] = Field(default_factory=dict)
    retrieval: Dict[str, Any] = Field(default_factory=dict)
    transfer: Dict[str, Any] = Field(default_factory=dict)

    # Practice + assessment
    practice: List[PracticeItem] = []
    proof: List[ProofQuestion] = []

    # Company variants
    company_variants: List[CompanyVariant] = []

    # SRS
    srs_key_points: List[str] = []
    srs_review_intervals: List[int] = [1, 3, 7, 14, 30]
