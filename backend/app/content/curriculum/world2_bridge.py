"""
World-2 → rich lesson bridge.

The generic LessonService / lesson routes serve any lesson dict looked up by
slug. The rich ``LessonContent`` shape is what ``LessonPage.tsx`` renders.

World 2's lessons are authored as flat ``LessonDefinition.steps[]``. This
module adapts each such lesson into the rich shape, reusing the same
adaptation logic as World 1 where possible.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from app.content.lesson_definitions import LessonDefinition, LessonStep
from app.content.world_registry import get_lesson_by_id, ALL_WORLDS


def _step_of_type(lesson: LessonDefinition, step_type: str) -> Optional[LessonStep]:
    for s in lesson.steps:
        if s.step_type == step_type:
            return s
    return None


def _steps_of_type(lesson: LessonDefinition, *types: str) -> list[LessonStep]:
    return [s for s in lesson.steps if s.step_type in types]


def _option_list(step: Optional[LessonStep]) -> list[Dict[str, Any]]:
    if not step:
        return []
    out = []
    for i, opt in enumerate(step.options or []):
        out.append({
            "id": opt.get("id", f"o{i}"),
            "text": opt.get("text", ""),
            "correct": bool(opt.get("correct", False)),
            "explanation": step.explanation,
        })
    return out


def _starter_code(step: LessonStep, function_name: str) -> str:
    """Build a starter function skeleton from the authored signature."""
    sig = (step.signature or f"def {function_name}() -> list:").strip()
    if not sig.endswith(":"):
        sig += ":"
    body_note = step.placeholder or (
        f"# your implementation here\n    pass"
    )
    return f"{sig}\n    {body_note}"


def _build_step(step: LessonStep, idx: int) -> Dict[str, Any]:
    fn = step.function_name or f"solve"
    hints = []
    if step.hint:
        hints.append({"level": 1, "text": step.hint})
    if step.fix_steps:
        for j, fix in enumerate(step.fix_steps, start=1):
            hints.append({"level": j + 1, "text": fix})
    if not hints:
        hints.append({"level": 1, "text": step.description or "Think step by step."})

    starter = step.starter_code.get("python") if step.starter_code else (step.starter or f"# your implementation here\n    pass")
    sig = step.signatures.get("python") if step.signatures else (step.signature or f"def {fn}() -> list:")

    is_debug = bool(step.buggy_code and step.fix_steps)

    return {
        "step_order": idx + 1,
        "title": step.title,
        "description": step.description,
        "starter_code": starter,
        "function_name": fn,
        "signature": sig,
        "test_cases": step.test_cases,
        "hidden_test_cases": [],
        "hidden_tests": step.hidden_tests,
        "xp": 50,
        "scaffolded_hints": hints,
        "repair_steps": step.repair_steps,
        "passing_score": step.passing_score,
        "max_attempts": step.max_attempts,
        "is_debug": is_debug,
        "buggy_code": step.buggy_code if is_debug else "",
        "languages": step.languages,
        "starter_code_per_language": step.starter_code,
        "signatures_per_language": step.signatures,
    }


def _discovery_step(step: LessonStep, idx: int) -> Dict[str, Any]:
    interaction_type = "reveal_value" if step.interaction else "inspect_type"
    interaction: Dict[str, Any] = {
        "type": interaction_type,
        "prompt": step.prompt or step.content or "What do you observe?",
    }
    if step.template:
        interaction["code"] = step.template
    if step.answer:
        interaction["reveal_after"] = step.answer
    return {
        "action": f"{step.step_type}_{idx + 1}",
        "room_name": step.title,
        "room_value": step.visual or step.content,
        "narration": f"{step.content} {step.hint or ''}".strip(),
        "interaction": interaction,
    }


def _adapt(lesson: LessonDefinition) -> Dict[str, Any]:
    """Convert a LessonDefinition into the rich LessonContent shape."""
    discover_steps = _steps_of_type(lesson, "discover", "manipulate")
    build_steps = _steps_of_type(lesson, "build", "debug")
    predict_step = _step_of_type(lesson, "predict")
    break_step = _step_of_type(lesson, "break")
    retrieve_steps = _steps_of_type(lesson, "retrieve")
    transfer_step = _step_of_type(lesson, "transfer")

    story_context = {
        "title": lesson.title,
        "narration": lesson.tutor_explain or lesson.mental_model,
        "setting": lesson.location or "World 2 — Problem Solver",
        "character": lesson.npc or "Mentor",
        "intro_text": f"{lesson.npc_line} {lesson.tutor_discover}".strip(),
    }

    prediction = {
        "title": "Before You Code",
        "question": (predict_step.question if predict_step else "What happens next?"),
        "code": (predict_step.template if predict_step else ""),
        "options": _option_list(predict_step),
        "explanation": (
            (predict_step.explanation if predict_step else "")
            or (predict_step.answer if predict_step else "")
        ),
    }

    guided_build = {
        "title": "Build It Yourself",
        "steps": [_build_step(s, i) for i, s in enumerate(build_steps)],
    }
    if not guided_build["steps"]:
        guided_build["steps"] = [{
            "step_order": 1,
            "title": lesson.title,
            "description": "Write a short program that applies what you learned.",
            "starter_code": "def solve():\n    pass",
            "function_name": "solve",
            "signature": "def solve() -> list:",
            "test_cases": [],
            "hidden_test_cases": [],
            "xp": 50,
            "scaffolded_hints": [{"level": 1, "text": "Reflect on the mental model before you begin."}],
        }]

    if transfer_step:
        transfer = {
            "title": transfer_step.title,
            "description": transfer_step.content,
            "function_name": transfer_step.function_name or "solve",
            "signature": transfer_step.signature or f"def {transfer_step.function_name or 'solve'}() -> list:",
            "starter_code": _starter_code(transfer_step, transfer_step.function_name or "solve"),
            "description_full": transfer_step.content or transfer_step.answer,
            "test_cases": transfer_step.test_cases,
            "hidden_test_cases": [],
            "hidden_tests": transfer_step.hidden_tests,
            "xp": 90,
            "scaffolded_hints": [{"level": 1, "text": transfer_step.hint or "Apply the concept to this new context."}],
            "repair_steps": transfer_step.repair_steps,
            "passing_score": transfer_step.passing_score,
            "max_attempts": transfer_step.max_attempts,
            "languages": transfer_step.languages,
            "starter_code_per_language": transfer_step.starter_code,
            "signatures_per_language": transfer_step.signatures,
        }
        if transfer_step.options:
            transfer["options"] = transfer_step.options
    elif build_steps:
        src = build_steps[-1]
        fn = src.function_name or "solve"
        transfer = {
            "title": f"Apply It Somewhere New",
            "description": (
                f"Same idea, fresh situation. Use what you just practised to "
                f"complete the challenge: {src.description or lesson.title}."
            ),
            "function_name": fn,
            "signature": src.signature or f"def {fn}() -> list:",
            "starter_code": _starter_code(src, fn),
            "description_full": (
                f"Re-implement {fn} for a new set of inputs. This ensures you "
                f"can transfer the skill beyond the guided exercise."
            ),
            "test_cases": src.test_cases,
            "hidden_test_cases": [],
            "hidden_tests": src.hidden_tests,
            "xp": 90,
            "scaffolded_hints": [{"level": 1, "text": src.hint or "Refactor your guided solution into a fresh function."}],
            "repair_steps": src.repair_steps,
            "passing_score": src.passing_score,
            "max_attempts": src.max_attempts,
            "languages": src.languages,
            "starter_code_per_language": src.starter_code,
            "signatures_per_language": src.signatures,
        }
    else:
        transfer = {
            "title": "Transfer: Explain to a Friend",
            "description": "New context: describe how this idea applies to a real program.",
            "function_name": "solve",
            "signature": "def solve() -> list:",
            "starter_code": "def solve():\n    pass",
            "description_full": (
                f"Write or describe how '{lesson.concept}' solves a "
                f"fresh problem that was not in the lesson. {lesson.why_this_matters}"
            ),
            "test_cases": [],
            "hidden_test_cases": [],
            "xp": 60,
            "scaffolded_hints": [{"level": 1, "text": lesson.mental_model}],
        }
        if break_step and break_step.options:
            transfer["options"] = break_step.options

    assessment_q: list[Dict[str, Any]] = []
    for s in _steps_of_type(lesson, "debug"):
        if s.buggy_code and s.fix_steps:
            assessment_q.append({
                "type": "debug",
                "code": s.buggy_code,
                "error": "The code is broken.",
                "question": s.description or "Fix the bug.",
                "fix": s.fix_steps[0],
                "explanation": s.explanation or " ".join(s.fix_steps),
            })
    if retrieve_steps:
        r = retrieve_steps[0]
        words = [w for w in (r.answer or "").lower().split() if len(w) > 2][:3] or [lesson.concept]
        assessment_q.append({
            "type": "concept",
            "question": r.prompt or f"What is the key idea of {lesson.concept}?",
            "answer_format": "short_answer",
            "keywords": words,
            "explanation": r.answer or lesson.mental_model,
        })
    if break_step and break_step.question and break_step.options:
        correct_text = next((o.get("text", "") for o in break_step.options if o.get("correct")), "")
        words = [w for w in (correct_text or "").lower().split() if len(w) > 2][:3] or [lesson.concept]
        assessment_q.append({
            "type": "concept",
            "question": break_step.question,
            "answer_format": "short_answer",
            "keywords": words,
            "explanation": break_step.explanation,
        })
    if not assessment_q:
        assessment_q.append({
            "type": "concept",
            "question": f"Explain what '{lesson.concept}' means in your own words.",
            "answer_format": "short_answer",
            "keywords": [lesson.concept] if lesson.concept else ["idea"],
            "explanation": lesson.mental_model,
        })

    key_points = [
        lesson.mental_model,
        lesson.tutor_explain or lesson.why_this_matters,
    ]
    key_points = [k for k in key_points if k]

    skills = [lesson.canonical_skill, lesson.concept]
    skills = [s for s in skills if s]

    return {
        "lesson_id": lesson.id,
        "module_id": f"world2:{lesson.id}",
        "title": lesson.title,
        "description": lesson.why_this_matters,
        "difficulty": "beginner",
        "est_minutes": lesson.estimated_minutes,
        "xp_reward": lesson.xp,
        "skills_taught": skills,
        "srs_concept_tag": lesson.canonical_skill or lesson.concept,
        "story_context": story_context,
        "discovery": {
            "title": "Look, Touch, Predict",
            "steps": [_discovery_step(s, i) for i, s in enumerate(discover_steps)],
            "conclusion": lesson.tutor_explain or lesson.why_this_matters,
        },
        "prediction": prediction,
        "guided_build": guided_build,
        "transfer_challenge": transfer,
        "assessment": {
            "title": f"{lesson.title} — Final Check",
            "description": "Prove you can recall and apply what you learned.",
            "questions": assessment_q,
            "mastery_threshold": 70,
            "xp": lesson.xp,
        },
        "srs_enrollment": {
            "concept_id": lesson.canonical_skill or lesson.concept or lesson.id,
            "concept_name": lesson.concept or lesson.title,
            "review_intervals": [1, 3, 7, 14, 30],
            "key_points": key_points,
            "spaced_fields": [lesson.concept] if lesson.concept else [lesson.id],
        },
        "world_progression": {
            "world_id": "world2_problem_solver",
            "competency_id": lesson.concept or lesson.id,
            "unlocks_next": [],
            "tower_badge": f"world2_{lesson.id}",
            "world_node": {
                "level": lesson.order,
                "title": lesson.title,
                "color": "blue",
                "icon": lesson.icon or "📄",
                "description": lesson.mental_model,
            },
        },
    }


def adapt_world2_lesson(lesson_id: str) -> Optional[Dict[str, Any]]:
    """Return the rich LessonContent for a World-2 lesson id, or None."""
    lesson = get_lesson_by_id(lesson_id)
    if lesson is None:
        return None
    # Verify it's actually a World 2 lesson by checking the world_id
    for world_id, world in ALL_WORLDS.items():
        if world_id == "problem_solver":
            for town in world.towns:
                for l in town.lessons:
                    if l.id == lesson_id:
                        return _adapt(lesson)
    return None


def world2_lesson_slugs() -> list[str]:
    """All World-2 lesson ids (the slugs served by the rich lesson route)."""
    world = ALL_WORLDS.get("problem_solver")
    if world is None:
        return []
    return sorted(l.id for town in world.towns for l in town.lessons)
