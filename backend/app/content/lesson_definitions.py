"""Generic LessonDefinition engine — the teaching algorithm as data.

The engine is *subject-agnostic*.  It knows the teaching loop:

    discover → manipulate → predict → build → break → debug → retrieve → transfer → prove mastery

but it does NOT know *what* is being taught.  That comes from content files
like ``world1_foundations.py`` which fill in the steps for each lesson.

This means adding a new lesson is a *content* task, not an *engineering* task.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ─── Teaching step types ────────────────────────────────────────────
# Every lesson is a sequence of these steps.  The frontend renderer reads
# ``step_type`` and renders the appropriate interaction.

STEP_TYPES = [
    "discover",     # Set the scene — what are we looking at?
    "manipulate",   # Interactive sandbox — change something, see what happens
    "predict",      # Multiple choice — what will happen before seeing the answer
    "build",        # Write code / create something — hidden tests verify
    "break",        # Deliberately inject bad input — observe failure
    "debug",        # Given buggy code + failing tests — find and fix
    "retrieve",     # No notes — recall from memory
    "transfer",     # New context — apply the idea somewhere unfamiliar
    "mastery",      # Timed mastery trial — prove independent competence
]


class LessonStep(BaseModel):
    """One step in a lesson's teaching loop."""
    step_type: str  # one of STEP_TYPES
    title: str
    content: str = ""
    # --- discover ---
    visual: str = ""
    interaction: str = ""  # "select-value" | "memory-box" | "toggle" | ...
    prompt: str = ""
    values: Optional[List[Any]] = None  # choices for select-value
    answer: str = ""
    # --- manipulate ---
    template: str = ""
    hint: str = ""
    # --- predict ---
    question: str = ""
    options: List[Dict[str, Any]] = Field(default_factory=list)  # [{id, text, correct}]
    explanation: str = ""
    # --- build / debug ---
    function_name: str = ""
    signature: str = ""
    description: str = ""
    starter: str = ""
    placeholder: str = ""
    language: str = "python"
    # Multi-language support: list of available languages for this lesson
    languages: List[str] = Field(default_factory=lambda: ["python", "java", "cpp", "c"])
    # Starter code per language: {language: code_string}
    starter_code: Dict[str, str] = Field(default_factory=dict)
    # Signatures per language: {language: signature_string}
    signatures: Dict[str, str] = Field(default_factory=dict)
    test_cases: List[Dict[str, Any]] = Field(default_factory=list)
    hidden_tests: int = 0
    buggy_code: str = ""
    fix_steps: List[str] = Field(default_factory=list)
    # --- retrieve / transfer ---
    context: str = ""


class LessonDefinition(BaseModel):
    """A single lesson — the atomic unit of teaching.

    ``canonical_skill`` maps this lesson to the mastery graph so completion
    updates the right skill node.  ``mental_model`` is the one-sentence insight
    the student should carry forward.
    """
    id: str
    title: str
    icon: str = "📄"
    kind: str = "level"  # "level" | "boss"
    order: int = 0
    concept: str = ""
    mental_model: str = ""
    canonical_skill: str = ""
    estimated_minutes: int = 12
    xp: int = 50
    # Narrative wrapper
    location: str = ""
    npc: str = ""
    npc_line: str = ""
    tutor_discover: str = ""
    tutor_explain: str = ""
    # The teaching loop
    steps: List[LessonStep] = Field(default_factory=list)
    # Mastery evidence — what the student can DO after this lesson
    mastery_evidence: List[str] = Field(default_factory=list)
    # Engineering context — why this matters in real engineering
    why_this_matters: str = "This concept is fundamental to building real software systems."
    engineering_context: str = "Engineers use this concept daily when building and maintaining production systems."
    # Job readiness — what career skill this builds toward
    builds_toward: str = "Software Engineering fundamentals"
    # Unlock consequence
    unlocks: str = ""


class TownDefinition(BaseModel):
    id: str
    name: str
    icon: str = "🏠"
    description: str = ""
    order: int = 0
    mental_model: str = ""
    canonical_skills: List[str] = Field(default_factory=list)
    competencies: List[str] = Field(default_factory=list)
    lessons: List[LessonDefinition] = Field(default_factory=list)


class WorldDefinition(BaseModel):
    id: str
    name: str
    subtitle: str = ""
    description: str = ""
    icon: str = "🌍"
    order: int = 0
    theme: str = "default"
    towns: List[TownDefinition] = Field(default_factory=list)
