"""Unified learning adapter — translates every existing content format into
the canonical LessonDefinition / LessonStep schema consumed by the existing
lesson runtime, study engine, mastery engine, and gamification system.

This file does NOT remove or modify any existing content source. It adds a
translation layer so every content system can be served through the same
canonical endpoints and state machines.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from app.content.lesson_definitions import (
    LessonDefinition,
    LessonStep,
    STEP_TYPES,
    TownDefinition,
    WorldDefinition,
)
from app.content.cfic_curriculum import (
    ConceptGraph,
    ConceptNode,
    ConceptFrame,
    ConceptContent,
    get_cfic_graph,
    get_cfic_content,
    _CFIC_NODES,
    _CFIC_EDGES,
    _CFIC_FRAMES,
)
from app.data.worlds_data import WORLD_REGISTRY, World, Town, Level
from app.content.scrimba_lessons import LESSONS as SCRIMBA_LESSONS
from app.content.curriculum.registry import LESSON_REGISTRY, get_lesson_dict
from app.data.study_materials import ALL_ARTICLES_BY_ID as STUDY_LIBRARY


# ─── Helpers ────────────────────────────────────────────────────────────

def _first(d: Dict[str, Any], *keys: str, default: Any = "") -> Any:
    for k in keys:
        if k in d and d[k] not in (None, "", []):
            return d[k]
    return default


def _as_step(step_type: str, payload: Dict[str, Any]) -> LessonStep:
    """Normalize one interaction payload into a canonical LessonStep."""
    kwargs: Dict[str, Any] = {"step_type": step_type}

    for field in [
        "title", "content", "visual", "interaction", "prompt", "template",
        "hint", "question", "explanation", "function_name", "signature",
        "description", "starter", "placeholder", "language", "context",
        "success_condition", "scaffold_prompt", "target_variable",
        "failure_description", "fix_steps", "passing_score", "max_attempts",
    ]:
        if field in payload:
            kwargs[field] = payload[field]

    for field in ["values", "languages", "starter_code", "signatures",
                  "test_cases", "repair_steps"]:
        if field in payload:
            kwargs[field] = payload[field]

    if "correct_index" in payload:
        kwargs["answer"] = str(payload["correct_index"])
    if "correct_diagnosis" in payload:
        kwargs["answer"] = str(payload["correct_diagnosis"])
    if "answer" in payload:
        kwargs["answer"] = str(payload["answer"])

    if "options" in payload:
        raw_options = payload["options"]
        if raw_options and isinstance(raw_options[0], str):
            answer = kwargs.get("answer", "")
            kwargs["options"] = [
                {"id": str(i), "text": opt, "correct": str(i) == answer}
                for i, opt in enumerate(raw_options)
            ]
        else:
            kwargs["options"] = raw_options

    return LessonStep(**kwargs)


# ─── CFIC → canonical lesson ───────────────────────────────────────────

def cfic_concept_to_lesson(content: ConceptContent) -> LessonDefinition:
    """Convert one CFIC concept into a canonical LessonDefinition."""
    node = content.concept
    frames = sorted(content.frames, key=lambda f: f.frame_order)

    steps: List[LessonStep] = []

    for frame in frames:
        ft = frame.frame_type
        if ft == "predict" and frame.predict:
            steps.append(_as_step("predict", {
                "title": "Predict",
                "prompt": frame.predict.prompt,
                "question": frame.predict.prompt,
                "options": frame.predict.options or [],
                "answer": str(frame.predict.correct_index),
                "explanation": frame.predict.explanation,
                "language": "python",
            }))
        elif ft == "visualize" and frame.visualize:
            steps.append(_as_step("discover", {
                "title": "Visualize",
                "content": frame.visualize.trace_description,
                "visual": "\n".join(
                    f"{c.get('step', 'step')}: {c.get('change', '')}"
                    for c in frame.visualize.key_state_changes
                ),
                "language": "python",
            }))
        elif ft == "manipulate" and frame.manipulate:
            steps.append(_as_step("manipulate", {
                "title": "Manipulate",
                "prompt": frame.manipulate.scaffold_prompt,
                "template": frame.manipulate.starter_code,
                "starter": frame.manipulate.starter_code,
                "hint": frame.manipulate.hint,
                "function_name": frame.manipulate.target_variable,
                "language": frame.manipulate.language or "python",
            }))
        elif ft == "break" and frame.break_frame:
            steps.append(_as_step("break", {
                "title": "Break",
                "content": frame.break_frame.failure_description,
                "buggy_code": frame.break_frame.buggy_code,
                "options": frame.break_frame.diagnosis_options or [],
                "answer": str(frame.break_frame.correct_diagnosis),
                "fix_steps": frame.break_frame.fix_steps,
                "language": frame.break_frame.language or "python",
            }))
        elif ft == "transfer" and frame.transfer:
            steps.append(_as_step("transfer", {
                "title": "Transfer",
                "prompt": frame.transfer.prompt,
                "starter": frame.transfer.starter_code,
                "function_name": "transfer_task",
                "test_cases": frame.transfer.test_cases or [],
                "hidden_tests": frame.transfer.hidden_tests,
                "language": frame.transfer.language or "python",
                "passing_score": 70,
                "max_attempts": 3,
            }))

    return LessonDefinition(
        id=f"cfic::{node.concept_id}",
        title=node.title,
        icon="🧠",
        kind="level",
        order=0,
        concept=node.concept_id,
        mental_model=node.mental_model,
        canonical_skill=node.concept_id,
        estimated_minutes=node.estimated_minutes,
        diamonds=node.diamonds_reward,
        why_this_matters=node.why_it_matters,
        engineering_context=node.engineering_context,
        builds_toward=node.why_it_matters,
        unlocks=", ".join(node.unlocks),
        steps=steps,
    )


def get_cfic_lessons() -> List[LessonDefinition]:
    """Return all CFIC concepts as canonical lessons, ordered by prerequisite."""
    graph = get_cfic_graph()
    out: List[LessonDefinition] = []
    seen = set()
    nodes = {n.concept_id: n for n in graph.nodes}

    def walk(concept_id: str) -> None:
        if concept_id in seen:
            return
        seen.add(concept_id)
        for edge in graph.edges:
            if edge.to_concept == concept_id:
                walk(edge.from_concept)
        content = get_cfic_content(concept_id)
        if content:
            out.append(cfic_concept_to_lesson(content))

    for node in graph.nodes:
        walk(node.concept_id)

    return out


# ─── World legacy → canonical lesson ───────────────────────────────────

def worlds_data_level_to_lesson(level: Level, world: World, town: Town) -> LessonDefinition:
    """Convert a legacy worlds_data.py Level into a canonical LessonDefinition."""
    steps: List[LessonStep] = []

    if getattr(level, "discovery", None):
        steps.append(_as_step("discover", {
            "title": "Discover",
            "content": str(level.discovery),
            "language": "python",
        }))

    if getattr(level, "manipulation", None):
        steps.append(_as_step("manipulate", {
            "title": "Manipulate",
            "prompt": str(level.manipulation),
            "template": getattr(level, "starter_code", "") or "",
            "starter": getattr(level, "starter_code", "") or "",
            "language": getattr(level, "language", "python") or "python",
        }))

    if getattr(level, "challenge", None):
        steps.append(_as_step("build", {
            "title": "Build",
            "prompt": str(level.challenge),
            "function_name": getattr(level, "function_name", "") or "",
            "signature": getattr(level, "signature", "") or "",
            "test_cases": getattr(level, "test_cases", []) or [],
            "hidden_tests": getattr(level, "hidden_tests", 0) or 0,
            "language": getattr(level, "language", "python") or "python",
            "passing_score": getattr(level, "passing_score", 70) or 70,
            "max_attempts": getattr(level, "max_attempts", 3) or 3,
        }))

    if not steps:
        steps.append(LessonStep(
            step_type="discover",
            title=str(getattr(level, "title", level.id)),
            content=str(getattr(level, "description", "")),
            language="python",
        ))

    return LessonDefinition(
        id=f"worlds::{world.id}::{town.id}::{level.id}",
        title=str(getattr(level, "title", level.id)),
        icon=getattr(level, "icon", "📄") or "📄",
        kind="level",
        order=getattr(level, "order", 0) or 0,
        concept=getattr(level, "concept", "") or "",
        mental_model=getattr(level, "mental_model", "") or "",
        canonical_skill=getattr(level, "concept", "") or level.id,
        estimated_minutes=getattr(level, "estimated_minutes", 12) or 12,
        diamonds=getattr(level, "diamonds", 50) or 50,
        location=getattr(level, "location", "") or "",
        unlocks=getattr(level, "unlocks", "") or "",
        steps=steps,
    )


def get_worlds_data_lessons() -> List[LessonDefinition]:
    """Convert all worlds_data.py levels into canonical lessons."""
    out: List[LessonDefinition] = []
    for world in WORLD_REGISTRY.values():
        for town in world.towns:
            for level in town.levels:
                out.append(worlds_data_level_to_lesson(level, world, town))
    return out


# ─── Scrimba → canonical lesson ────────────────────────────────────────

def get_scrimba_lessons() -> List[LessonDefinition]:
    """Convert scrimba slide lessons into canonical LessonDefinitions."""
    out: List[LessonDefinition] = []
    for lesson in SCRIMBA_LESSONS:
        lesson_id = _first(lesson, "lesson_id", "id", default=str(len(out)))
        title = _first(lesson, "title", "name", default=f"Lesson {lesson_id}")
        slides = lesson.get("slides", []) or []
        snippets = lesson.get("snippets", {}) or {}

        steps: List[LessonStep] = []
        for idx, slide in enumerate(slides):
            slide_type = str(slide.get("type", "text")).lower()
            if slide_type in ("code", "editor", "run"):
                steps.append(_as_step("manipulate", {
                    "title": slide.get("title", f"Slide {idx + 1}"),
                    "content": slide.get("content", "") or slide.get("body", ""),
                    "starter": snippets.get(str(idx), "") or slide.get("code", "") or "",
                    "language": _first(slide, "language", "lang", default="python"),
                }))
            else:
                steps.append(_as_step("discover", {
                    "title": slide.get("title", f"Slide {idx + 1}"),
                    "content": slide.get("content", "") or slide.get("body", ""),
                    "language": "python",
                }))

        if not steps:
            steps.append(LessonStep(
                step_type="discover",
                title=title,
                content=lesson.get("description", "") or "",
                language="python",
            ))

        out.append(LessonDefinition(
            id=f"scrimba::{lesson_id}",
            title=title,
            icon="📝",
            kind="level",
            order=lesson.get("order", len(out)),
            concept="scrimba",
            mental_model=lesson.get("description", "") or "",
            canonical_skill=f"scrimba:{lesson_id}",
            estimated_minutes=lesson.get("estimated_minutes", 10) or 10,
            diamonds=lesson.get("diamonds", 20) or 20,
            steps=steps,
        ))
    return out


# ─── Study materials/articles → canonical lesson ───────────────────────

def get_study_material_lessons() -> List[LessonDefinition]:
    """Convert study_materials articles into canonical LessonDefinitions."""
    out: List[LessonDefinition] = []
    for key, article in (STUDY_LIBRARY or {}).items():
        if not isinstance(article, dict):
            continue
        sections = article.get("sections", []) or []
        steps: List[LessonStep] = []
        for section in sections:
            steps.append(_as_step("discover", {
                "title": section.get("heading", "") or section.get("title", ""),
                "content": section.get("body", "") or section.get("content", ""),
                "language": "python",
            }))
        if not steps:
            steps.append(LessonStep(
                step_type="discover",
                title=article.get("title", key),
                content=article.get("content", "") or article.get("body", ""),
                language="python",
            ))
        out.append(LessonDefinition(
            id=f"article::{key}",
            title=article.get("title", key),
            icon="📚",
            kind="level",
            order=len(out),
            concept="article",
            mental_model=article.get("title", key),
            canonical_skill=f"article:{key}",
            estimated_minutes=article.get("estimated_minutes", 8) or 8,
            diamonds=article.get("diamonds", 15) or 15,
            steps=steps,
        ))
    return out


# ─── Vertical slice registry → canonical lesson ────────────────────────

def _flatten_vertical_slice(lesson: Dict[str, Any]) -> List[LessonStep]:
    """Flatten a vertical-slice dict (discovery / prediction / guided_build / …)
    into a single step list the catalog can render."""
    steps: List[LessonStep] = []

    discovery = lesson.get("discovery") or {}
    for i, raw in enumerate(discovery.get("steps", []) or []):
        interaction = raw.get("interaction") or {}
        if not isinstance(interaction, dict):
            interaction = {}
        payload: Dict[str, Any] = {
            "step_type": "discover",
            "title": discovery.get("title", lesson.get("title", "")),
            "content": raw.get("narration", "") or "",
            "interaction": interaction.get("type", ""),
        }
        if interaction.get("type") == "inspect_code":
            payload.update({
                "content": raw.get("narration", "") or "",
                "starter": interaction.get("code", ""),
                "hint": interaction.get("hint", ""),
            })
        elif interaction.get("type") == "choose_outcome":
            payload.update({
                "question": interaction.get("prompt", ""),
                "options": interaction.get("options", []),
                "explanation": interaction.get("explanation", ""),
            })
        steps.append(_as_step("discover", payload))

    prediction = lesson.get("prediction") or {}
    if prediction:
        steps.append(_as_step("predict", {
            "title": prediction.get("title", "Predict"),
            "question": prediction.get("question", ""),
            "options": prediction.get("options", []),
            "explanation": prediction.get("explanation", ""),
        }))

    explain = lesson.get("explain") or {}
    if explain:
        steps.append(_as_step("manipulate", {
            "title": explain.get("title", "Explain"),
            "content": explain.get("prompt", ""),
            "hint": explain.get("model_answer", ""),
        }))

    guided = lesson.get("guided_build") or {}
    for raw in guided.get("steps", []) or []:
        sc = raw.get("starter_code") or raw.get("starter") or ""
        starter_code_dict: Dict[str, str] = sc if isinstance(sc, dict) else ({"python": sc} if sc else {})
        hints = raw.get("scaffolded_hints") or raw.get("repair_steps") or []
        repair_steps_list: List[Dict[str, Any]] = []
        for h in hints:
            if isinstance(h, dict):
                repair_steps_list.append({"trigger": "wrong_answer", "hint": h.get("text", h.get("hint", ""))})
            else:
                repair_steps_list.append({"trigger": "wrong_answer", "hint": str(h)})
        steps.append(_as_step("build", {
            "title": raw.get("title", ""),
            "description": raw.get("description", ""),
            "function_name": raw.get("function_name", ""),
            "signature": raw.get("signature", ""),
            "starter_code": starter_code_dict,
            "test_cases": raw.get("test_cases", []),
            "repair_steps": repair_steps_list,
            "passing_score": 70,
            "max_attempts": 3,
        }))

    transfer = lesson.get("transfer_challenge") or {}
    if transfer:
        sc = transfer.get("starter_code") or transfer.get("starter") or ""
        starter_code_dict = sc if isinstance(sc, dict) else ({"python": sc} if sc else {})
        transfer_hints = transfer.get("scaffolded_hints") or transfer.get("repair_steps") or []
        repair_steps_list = []
        for h in transfer_hints:
            if isinstance(h, dict):
                repair_steps_list.append({"trigger": "wrong_answer", "hint": h.get("text", h.get("hint", ""))})
            else:
                repair_steps_list.append({"trigger": "wrong_answer", "hint": str(h)})
        steps.append(_as_step("transfer", {
            "title": transfer.get("title", "Transfer"),
            "description": transfer.get("description_full", transfer.get("description", "")),
            "function_name": transfer.get("function_name", ""),
            "signature": transfer.get("signature", ""),
            "starter_code": starter_code_dict,
            "test_cases": transfer.get("test_cases", []),
            "repair_steps": repair_steps_list,
            "passing_score": 70,
            "max_attempts": 3,
        }))

    brk = lesson.get("break") or {}
    if brk:
        steps.append(_as_step("break", {
            "title": brk.get("title", "Break"),
            "content": brk.get("story", ""),
            "interaction": "select-value",
            "question": (brk.get("diagnosis") or {}).get("question", ""),
            "options": (brk.get("diagnosis") or {}).get("options", []),
            "explanation": brk.get("explanation", ""),
        }))

    assessment = lesson.get("assessment") or {}
    for q in assessment.get("questions", []) or []:
        q_type = q.get("type", "concept")
        if q_type == "code_tracing":
            steps.append(_as_step("mastery", {
                "title": assessment.get("title", "Mastery"),
                "description": assessment.get("description", ""),
                "content": q.get("code", ""),
                "question": q.get("question", ""),
                "options": q.get("options", []),
                "explanation": q.get("explanation", ""),
            }))
        elif q_type == "concept":
            steps.append(_as_step("mastery", {
                "title": assessment.get("title", "Mastery"),
                "description": assessment.get("description", ""),
                "question": q.get("question", ""),
                "options": q.get("options", []),
                "explanation": q.get("explanation", ""),
            }))
        elif q_type == "debug":
            steps.append(_as_step("mastery", {
                "title": assessment.get("title", "Mastery"),
                "description": assessment.get("description", ""),
                "content": q.get("code", ""),
                "question": q.get("question", ""),
                "explanation": q.get("explanation", ""),
            }))

    return steps


def get_vertical_slice_lessons() -> List[LessonDefinition]:
    """Convert LESSON_REGISTRY dict lessons into canonical LessonDefinitions."""
    out: List[LessonDefinition] = []
    for slug, lesson in LESSON_REGISTRY.items():
        if not isinstance(lesson, dict):
            continue
        raw_steps = lesson.get("steps", []) or []
        if raw_steps:
            steps: List[LessonStep] = []
            for raw in raw_steps:
                if not isinstance(raw, dict):
                    continue
                st = str(raw.get("step_type", raw.get("type", "discover"))).lower()
                if st not in STEP_TYPES:
                    st = "discover"
                steps.append(_as_step(st, raw))
        else:
            steps = _flatten_vertical_slice(lesson)

        if not steps:
            steps.append(LessonStep(
                step_type="discover",
                title=lesson.get("title", slug),
                content=lesson.get("content", "") or lesson.get("description", ""),
                language="python",
            ))

        out.append(LessonDefinition(
            id=f"slice::{slug}",
            title=lesson.get("title", slug),
            icon=lesson.get("icon", "📘") or "📘",
            kind="level",
            order=lesson.get("order", len(out)) or len(out),
            concept=lesson.get("concept", slug) or slug,
            mental_model=lesson.get("mental_model", "") or "",
            canonical_skill=lesson.get("canonical_skill", slug) or slug,
            estimated_minutes=lesson.get("estimated_minutes", 12) or 12,
            diamonds=lesson.get("diamonds", 50) or 50,
            why_this_matters=lesson.get("why_this_matters", "") or "",
            unlocks=lesson.get("unlocks", "") or "",
            steps=steps,
        ))
    return out


# ─── Company-prep lessons → canonical lesson ─────────────────────────────

def get_company_lessons() -> List[LessonDefinition]:
    """Load company-prep lessons from app/data/lessons/*.json into the catalog."""
    out: List[LessonDefinition] = []
    lessons_dir = os.path.join(os.path.dirname(__file__), "..", "data", "lessons")
    if not os.path.isdir(lessons_dir):
        return out
    for fname in sorted(os.listdir(lessons_dir)):
        if not fname.endswith(".json"):
            continue
        slug = fname[:-5]
        path = os.path.join(lessons_dir, fname)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        raw_steps = data.get("steps", []) or []
        steps: List[LessonStep] = []
        for raw in raw_steps:
            if not isinstance(raw, dict):
                continue
            st = str(raw.get("step_type", raw.get("type", "discover"))).lower()
            if st not in STEP_TYPES:
                st = "discover"
            steps.append(_as_step(st, raw))
        if not steps:
            steps.append(LessonStep(
                step_type="discover",
                title=data.get("title", slug),
                content=data.get("content", "") or data.get("description", ""),
                language="python",
            ))
        out.append(LessonDefinition(
            id=f"company_lesson::{slug}",
            title=data.get("title", slug),
            icon="🏢",
            kind="level",
            order=len(out),
            concept=data.get("domain") or data.get("pattern") or slug,
            mental_model=data.get("description", "") or "",
            canonical_skill=data.get("pattern") or data.get("domain") or slug,
            estimated_minutes=int(data.get("duration_min") or data.get("estimated_minutes") or 15),
            diamonds=int(data.get("xp_reward") or data.get("diamonds") or 50),
            why_this_matters=data.get("description", "") or "",
            unlocks="",
            steps=steps,
        ))
    return out


# ─── Unified lesson catalog ─────────────────────────────────────────────

class UnifiedLessonCatalog:
    """Single entry point that returns canonical LessonDefinitions from every
    existing content source.  No content is removed or rewritten; this is a
    translation layer only."""

    def __init__(self) -> None:
        self._cache: Optional[List[LessonDefinition]] = None
        self._intuition_cache: Optional[dict] = None

    def reload(self) -> None:
        self._cache = None
        self._intuition_cache = None

    def _load_intuition_registry(self) -> dict:
        if self._intuition_cache is not None:
            return self._intuition_cache
        try:
            import json, os
            path = os.path.join(os.path.dirname(__file__), "..", "data", "metaphor_registry.json")
            with open(path, "r", encoding="utf-8") as f:
                self._intuition_cache = json.load(f)
        except Exception:
            self._intuition_cache = {}
        return self._intuition_cache

    def all_lessons(self) -> List[LessonDefinition]:
        if self._cache is not None:
            return self._cache
        seen: set = set()
        out: List[LessonDefinition] = []

        def add(lessons: List[LessonDefinition]) -> None:
            for lesson in lessons:
                if lesson.id not in seen:
                    seen.add(lesson.id)
                    out.append(lesson)

        add(get_vertical_slice_lessons())
        add(get_cfic_lessons())
        add(get_worlds_data_lessons())
        add(get_scrimba_lessons())
        add(get_study_material_lessons())
        add(get_company_lessons())

        out.sort(key=lambda l: (l.order, l.id))
        self._cache = out
        return out

    def get(self, lesson_id: str) -> Optional[LessonDefinition]:
        return next((l for l in self.all_lessons() if l.id == lesson_id), None)

    def resolve(self, raw_id: str) -> Optional[LessonDefinition]:
        """Resolve a raw identifier to a canonical LessonDefinition.

        Accepts:
        - exact catalog ID (e.g. ``slice::variables``, ``cfic::loops``)
        - canonical skill (e.g. ``backend.rest``)
        - concept slug (e.g. ``loops``)
        - company lesson slug (e.g. ``arrays_basics``)

        Returns the first matching LessonDefinition, or None.
        """
        if not raw_id:
            return None
        lesson = self.get(raw_id)
        if lesson is not None:
            return lesson
        for candidate in self.all_lessons():
            if candidate.canonical_skill == raw_id:
                return candidate
            if candidate.concept == raw_id:
                return candidate
        for prefix in ("cfic::", "company_lesson::", "slice::", "scrimba::", "article::", "worlds::"):
            candidate_id = f"{prefix}{raw_id}"
            lesson = self.get(candidate_id)
            if lesson is not None:
                return lesson
        return None

    def get_by_skill(self, canonical_skill: str) -> List[LessonDefinition]:
        return [l for l in self.all_lessons() if l.canonical_skill == canonical_skill]

    def get_by_concept(self, concept: str) -> List[LessonDefinition]:
        return [l for l in self.all_lessons() if l.concept == concept]

    def domains(self) -> List[str]:
        return sorted({l.concept for l in self.all_lessons() if l.concept})

    def skill_tags(self) -> List[str]:
        return sorted({l.canonical_skill for l in self.all_lessons() if l.canonical_skill})

    def metaphor_for(self, lesson_id: str) -> dict:
        """Return the metaphor + misconception cards for a lesson, if any."""
        lesson = self.get(lesson_id)
        if not lesson:
            return {}
        registry = self._load_intuition_registry()
        concept = (lesson.concept or "").lower()
        canonical_skill = (lesson.canonical_skill or "").lower()
        entry = registry.get(concept) or registry.get(canonical_skill) or {}
        return entry

    def intuition_status(self, lesson_id: str) -> dict:
        """Return intuition gate info for a lesson."""
        metaphor = self.metaphor_for(lesson_id)
        return {
            "has_metaphor": bool(metaphor.get("metaphor")),
            "has_misconceptions": len(metaphor.get("misconceptions", [])) >= 2,
            "physical": metaphor.get("physical", ""),
            "action": metaphor.get("action", ""),
            "example": metaphor.get("example", ""),
        }


unified_catalog = UnifiedLessonCatalog()
