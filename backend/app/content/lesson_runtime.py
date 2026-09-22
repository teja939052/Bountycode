"""Canonical runtime lesson model.

This is the single source of truth for lesson step representation.
All lesson content formats (LessonDefinition, LevelBase, etc.) are
adapted TO this model, never duplicated.

The 9-step teaching loop:
  discover → manipulate → predict → build → break → debug → retrieve → transfer → mastery
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RuntimeLessonStep(BaseModel):
    """One step in the canonical lesson runtime."""
    step_type: str  # discover, manipulate, predict, build, break, debug, retrieve, transfer, mastery
    title: str
    content: str = ""
    # Interaction
    interaction_type: str = ""  # select-value, reveal, code, text, none
    choices: List[Dict[str, Any]] = Field(default_factory=list)  # {text, correct, explanation}
    answer: str = ""
    # Code
    function_name: str = ""
    signature: str = ""
    starter_code: str = ""
    language: str = "python"
    test_cases: List[Dict[str, Any]] = Field(default_factory=list)
    hidden_tests: int = 0
    # Break/Debug
    buggy_code: str = ""
    expected_failure: str = ""
    fix_steps: List[str] = Field(default_factory=list)
    # Hints/Repair
    hints: List[Dict[str, Any]] = Field(default_factory=list)
    repair_steps: List[Dict[str, Any]] = Field(default_factory=list)
    passing_score: int = 70
    max_attempts: int = 3
    # Metadata
    diamonds: int = 0
    canonical_skill: str = ""
    # UI hints
    is_debug: bool = False


class RuntimeLesson(BaseModel):
    """Canonical lesson representation for the runtime."""
    lesson_id: str
    title: str
    description: str
    xp_reward: int
    steps: List[RuntimeLessonStep]
    srs_concept_tag: str = ""
    world_progression: Dict[str, Any] = Field(default_factory=dict)
    story_context: Dict[str, Any] = Field(default_factory=dict)
    discovery_conclusion: str = ""
    prediction: Dict[str, Any] = Field(default_factory=dict)
    guided_build: Dict[str, Any] = Field(default_factory=dict)
    transfer_challenge: Dict[str, Any] = Field(default_factory=dict)
    assessment: Dict[str, Any] = Field(default_factory=dict)

    def step_types(self) -> List[str]:
        return [s.step_type for s in self.steps]

    def steps_of_type(self, step_type: str) -> List[RuntimeLessonStep]:
        return [s for s in self.steps if s.step_type == step_type]

    def first_of_type(self, step_type: str) -> Optional[RuntimeLessonStep]:
        for s in self.steps:
            if s.step_type == step_type:
                return s
        return None


def from_lesson_definition(lesson: Any) -> RuntimeLesson:
    """Adapt a LessonDefinition to RuntimeLesson."""
    steps: List[RuntimeLessonStep] = []
    for s in lesson.steps:
        step = RuntimeLessonStep(
            step_type=s.step_type,
            title=s.title,
            content=s.content,
            interaction_type=s.interaction or "",
            choices=s.options or [],
            answer=s.answer or "",
            function_name=s.function_name or "",
            signature=s.signature or "",
            starter_code=s.starter_code.get("python", "") if s.starter_code else (s.starter or ""),
            language=s.language or "python",
            test_cases=s.test_cases or [],
            hidden_tests=s.hidden_tests or 0,
            buggy_code=s.buggy_code or "",
            expected_failure="",
            fix_steps=s.fix_steps or [],
            hints=[{"text": h} for h in s.hints] if s.hints else [],
            repair_steps=s.repair_steps or [],
            passing_score=s.passing_score or 70,
            max_attempts=s.max_attempts or 3,
            diamonds=lesson.diamonds or 50,
            canonical_skill=s.canonical_skill or lesson.concept or "",
            is_debug=bool(s.buggy_code and s.fix_steps),
        )
        steps.append(step)

    return RuntimeLesson(
        lesson_id=lesson.id,
        title=lesson.title,
        description=lesson.why_this_matters or lesson.mental_model or "",
        xp_reward=lesson.diamonds or 50,
        steps=steps,
        srs_concept_tag=lesson.canonical_skill or lesson.concept or lesson.id,
        world_progression={
            "world_id": getattr(lesson, "world_id", ""),
            "competency_id": lesson.concept or lesson.id,
            "unlocks_next": [lesson.unlocks] if lesson.unlocks else [],
            "tower_badge": f"world_{lesson.id}",
        },
        story_context={
            "title": lesson.title,
            "narration": lesson.tutor_explain or lesson.mental_model,
            "setting": lesson.location or "",
            "character": lesson.npc or "Mentor",
            "intro_text": f"{lesson.npc_line} {lesson.tutor_discover}".strip(),
        },
        discovery_conclusion=lesson.tutor_explain or lesson.why_this_matters or "",
        prediction={},
        guided_build={},
        transfer_challenge={},
        assessment={},
    )


def from_level_base(level: Any) -> RuntimeLesson:
    """Adapt a LevelBase to RuntimeLesson."""
    steps: List[RuntimeLessonStep] = []

    # Discover
    if hasattr(level, "discover") and level.discover:
        steps.append(RuntimeLessonStep(
            step_type="discover",
            title=level.discover.title or level.title,
            content=level.discover.content or "",
            interaction_type=level.discover.interaction or "",
            choices=level.discover.values or [],
            answer=level.discover.answer or "",
        ))

    # Manipulate
    if hasattr(level, "manipulate") and level.manipulate:
        steps.append(RuntimeLessonStep(
            step_type="manipulate",
            title=level.manipulate.title or "Manipulate",
            content=level.manipulate.content or "",
            interaction_type="code",
            function_name=getattr(level.manipulate, "function_name", "") or "",
            signature=getattr(level.manipulate, "signature", "") or "",
            starter_code=getattr(level.manipulate, "starter", "") or "",
            language=getattr(level.manipulate, "language", "python") or "python",
            test_cases=getattr(level.manipulate, "test_cases", []) or [],
            hidden_tests=getattr(level.manipulate, "hidden_tests", 0) or 0,
            hints=[{"text": level.manipulate.hint}] if level.manipulate.hint else [],
            repair_steps=getattr(level.manipulate, "repair_steps", []) or [],
            passing_score=getattr(level.manipulate, "passing_score", 70) or 70,
            max_attempts=getattr(level.manipulate, "max_attempts", 3) or 3,
            diamonds=level.success.diamonds if hasattr(level, "success") and level.success else 50,
            canonical_skill=level.canonical_skill or level.concept or "",
        ))

    # Predict
    if hasattr(level, "predict") and level.predict:
        steps.append(RuntimeLessonStep(
            step_type="predict",
            title=level.predict.title or "Predict",
            content=level.predict.question or "",
            interaction_type="multiple_choice",
            choices=level.predict.options or [],
            answer=next((o.text for o in (level.predict.options or []) if o.correct), ""),
            explanation=level.predict.explanation or "",
        ))

    # Build
    if hasattr(level, "build") and level.build:
        steps.append(RuntimeLessonStep(
            step_type="build",
            title=level.build.title or "Build",
            content=level.build.description or "",
            interaction_type="code",
            function_name=level.build.function_name or "",
            signature=level.build.signature or "",
            starter_code=level.build.starter or "",
            language=level.build.language or "python",
            test_cases=level.build.test_cases or [],
            hidden_tests=getattr(level.build, "hidden_tests", 0) or 0,
            hints=getattr(level.build, "hints", []) or [],
            repair_steps=getattr(level.build, "repair_steps", []) or [],
            passing_score=getattr(level.build, "passing_score", 70) or 70,
            max_attempts=getattr(level.build, "max_attempts", 3) or 3,
            diamonds=level.success.diamonds if hasattr(level, "success") and level.success else 50,
            canonical_skill=level.canonical_skill or level.concept or "",
        ))

    # Break
    if hasattr(level, "break_step") and level.break_step:
        steps.append(RuntimeLessonStep(
            step_type="break",
            title=level.break_step.title or "Break",
            content=level.break_step.prompt or "",
            interaction_type="predict_failure",
            buggy_code=level.break_step.broken_code or "",
            expected_failure=level.break_step.expected_failure or "",
            answer=level.break_step.expected_failure or "",
            canonical_skill=level.canonical_skill or level.concept or "",
        ))

    # Debug
    if hasattr(level, "debug") and level.debug:
        steps.append(RuntimeLessonStep(
            step_type="debug",
            title=level.debug.title or "Debug",
            content=level.debug.prompt or "Fix the bug.",
            interaction_type="code",
            buggy_code=level.debug.buggy_code or "",
            fix_steps=level.debug.fix_steps or [],
            function_name=getattr(level.debug, "function_name", "") or "",
            signature=getattr(level.debug, "signature", "") or "",
            starter_code="",  # Student writes fix from scratch
            language="python",
            test_cases=getattr(level.debug, "test_cases", []) or [],
            hidden_tests=getattr(level.debug, "hidden_tests", 0) or 0,
            hints=[{"text": f} for f in level.debug.fix_steps] if level.debug.fix_steps else [],
            repair_steps=getattr(level.debug, "repair_steps", []) or [],
            passing_score=getattr(level.debug, "passing_score", 70) or 70,
            max_attempts=getattr(level.debug, "max_attempts", 3) or 3,
            diamonds=level.success.diamonds if hasattr(level, "success") and level.success else 50,
            canonical_skill=level.canonical_skill or level.concept or "",
            is_debug=True,
        ))

    # Retrieve
    if hasattr(level, "retrieval") and level.retrieval:
        steps.append(RuntimeLessonStep(
            step_type="retrieve",
            title=level.retrieval.title or "Recall",
            content=level.retrieval.prompt or "",
            interaction_type="text",
            answer=level.retrieval.answer or "",
            explanation=level.retrieval.explanation or "",
            canonical_skill=level.canonical_skill or level.concept or "",
        ))

    # Transfer
    if hasattr(level, "transfer") and level.transfer:
        steps.append(RuntimeLessonStep(
            step_type="transfer",
            title=level.transfer.title or "Transfer",
            content=level.transfer.prompt or "",
            interaction_type="code",
            function_name=level.transfer.function_name or "",
            signature=level.transfer.signature or "",
            starter_code=getattr(level.transfer, "starter", "") or "",
            language="python",
            test_cases=level.transfer.test_cases or [],
            hidden_tests=getattr(level.transfer, "hidden_tests", 0) or 0,
            hints=getattr(level.transfer, "hints", []) or [],
            repair_steps=getattr(level.transfer, "repair_steps", []) or [],
            passing_score=getattr(level.transfer, "passing_score", 70) or 70,
            max_attempts=getattr(level.transfer, "max_attempts", 3) or 3,
            diamonds=level.success.diamonds if hasattr(level, "success") and level.success else 50,
            canonical_skill=level.canonical_skill or level.concept or "",
        ))

    # Mastery
    steps.append(RuntimeLessonStep(
        step_type="mastery",
        title=f"{level.title} — Prove It",
        content=level.build.description if hasattr(level, "build") and level.build else "",
        interaction_type="code",
        function_name=getattr(level.build, "function_name", "") if hasattr(level, "build") and level.build else "",
        signature=getattr(level.build, "signature", "") if hasattr(level, "build") and level.build else "",
        starter_code=getattr(level.build, "starter", "") if hasattr(level, "build") and level.build else "",
        language="python",
        test_cases=getattr(level.build, "test_cases", []) if hasattr(level, "build") and level.build else [],
        hidden_tests=getattr(level.build, "hidden_tests", 0) if hasattr(level, "build") and level.build else 0,
        hints=getattr(level.build, "hints", []) if hasattr(level, "build") and level.build else [],
        repair_steps=getattr(level.build, "repair_steps", []) if hasattr(level, "build") and level.build else [],
        passing_score=getattr(level.build, "passing_score", 70) if hasattr(level, "build") and level.build else 70,
        max_attempts=getattr(level.build, "max_attempts", 3) if hasattr(level, "build") and level.build else 3,
        diamonds=level.success.diamonds if hasattr(level, "success") and level.success else 50,
        canonical_skill=level.canonical_skill or level.concept or "",
    ))

    return RuntimeLesson(
        lesson_id=level.id,
        title=level.title,
        description=level.mental_model or "",
        xp_reward=level.success.diamonds if hasattr(level, "success") and level.success else 50,
        steps=steps,
        srs_concept_tag=level.canonical_skill or level.concept or level.id,
        world_progression={
            "world_id": getattr(level, "world_id", ""),
            "competency_id": level.concept or level.id,
            "unlocks_next": [level.unlocks] if level.unlocks else [],
            "tower_badge": f"world_{level.id}",
        },
        story_context={
            "title": level.title,
            "narration": getattr(level, "tutor_explain", "") or level.mental_model,
            "setting": getattr(level, "location", "") or "",
            "character": getattr(level, "npc", "") or "Mentor",
            "intro_text": f"{getattr(level, 'npc_line', '')} {getattr(level, 'tutor_discover', '')}".strip(),
        },
        discovery_conclusion=getattr(level, "tutor_explain", "") or level.mental_model,
        prediction={},
        guided_build={},
        transfer_challenge={},
        assessment={},
    )
