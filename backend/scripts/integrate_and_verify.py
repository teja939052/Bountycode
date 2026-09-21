"""Integrate worlds 9-12 and verify judge execution in one process."""
import sys
sys.path.insert(0, ".")

from app.content.worlds_7_to_9 import get_world_9
from app.content.worlds_10_to_12 import get_world_10, get_world_11, get_world_12
from app.models.world import (
    Boss, Build, Checks, Code, Debug, Discover, Level, Manipulate, Predict,
    Retrieval, Story, Success, Town, Transfer, Tutor, World, Reward,
)
from app.data.worlds_data import WORLD_REGISTRY
from app.routes.worlds import judge_level, _level_by_id, _all_level_ids, _is_unlocked


def _first(iterable, default=""):
    for item in iterable:
        if item:
            return item
    return default


def _convert_lesson(lesson: Any, world_id: str) -> Level | Boss:
    is_boss = getattr(lesson, "kind", "level") == "boss"
    level_cls = Boss if is_boss else Level

    story = Story(
        location=lesson.concept or "",
        npc="",
        line=lesson.mental_model or lesson.title or "",
    )

    tutor = Tutor(
        name="Byte",
        avatar="🧮",
        discover=lesson.mental_model or "",
        explain=lesson.why_this_matters or lesson.builds_toward or "",
    )

    steps = lesson.steps or []
    discover = _first((_lesson_step_to_discover(s) for s in steps if s.step_type == "discover"), Discover())
    manipulate = _first((_lesson_step_to_manipulate(s) for s in steps if s.step_type == "manipulate"), Manipulate())
    predict = _first((_lesson_step_to_predict(s) for s in steps if s.step_type == "predict"), None)
    build = _first((_lesson_step_to_build(s) for s in steps if s.step_type in ("build", "mastery")), None)
    debug = _first((_lesson_step_to_debug(s) for s in steps if s.step_type == "debug"), None)
    retrieval = _first((_lesson_step_to_retrieval(s) for s in steps if s.step_type == "retrieve"), None)
    transfer = _first((_lesson_step_to_transfer(s) for s in steps if s.step_type == "transfer"), None)

    code_step = _first((s for s in steps if s.step_type in ("build", "mastery")), None)
    starter = ""
    placeholder = ""
    language = "python"
    if code_step:
        starter = code_step.starter or (code_step.starter_code.get("python", "") if isinstance(code_step.starter_code, dict) else "") or ""
        placeholder = code_step.placeholder or ""
        language = code_step.language or "python"
    code = Code(
        prompt=code_step.description or code_step.title or "" if code_step else "",
        starter=starter,
        placeholder=placeholder,
        language=language,
    )

    checks = _extract_checks(lesson)
    hints = _extract_hints(lesson)
    success = _extract_success(lesson, is_boss)
    reward = _extract_reward(lesson)

    return level_cls(
        id=lesson.id,
        title=lesson.title,
        kind="boss" if is_boss else "level",
        icon=lesson.icon or "",
        order=getattr(lesson, "order", 0),
        concept=lesson.concept or "",
        mental_model=lesson.mental_model or "",
        canonical_skill=lesson.canonical_skill or "",
        maps_to_competency=None,
        story=story,
        tutor=tutor,
        discover=discover,
        understand=None,
        manipulate=manipulate,
        predict=predict,
        build=build,
        break_step=None,
        debug=debug,
        code=code,
        checks=checks,
        hints=hints,
        retrieval=retrieval,
        transfer=transfer,
        mastery_threshold=80 if is_boss else None,
        estimated_minutes=getattr(lesson, "estimated_minutes", None),
        reward=reward,
        success=success,
        unlocks=getattr(lesson, "unlocks", None),
    )


def _convert_town(town: Any, world_id: str) -> Town:
    levels = []
    for lesson in (town.lessons or []):
        levels.append(_convert_lesson(lesson, world_id))
    boss = None
    if levels and levels[-1].kind == "boss":
        boss = levels[-1]
    return Town(
        id=town.id,
        name=town.name,
        icon=town.icon or "",
        description=town.description or "",
        order=getattr(town, "order", 0),
        mental_model=getattr(town, "mental_model", ""),
        canonical_skills=getattr(town, "canonical_skills", []),
        competencies=getattr(town, "competencies", []),
        levels=levels,
        boss=boss,
    )


def _convert_world(wd: Any) -> World:
    towns = [_convert_town(t, wd.id) for t in (wd.towns or [])]
    return World(
        id=wd.id,
        name=wd.name,
        subtitle=wd.subtitle or "",
        description=wd.description or "",
        icon=wd.icon or "",
        order=getattr(wd, "order", 0),
        theme=getattr(wd, "theme", ""),
        recommended_roles=[],
        prerequisites=[],
        towns=towns,
        completion_reward=None,
    )


# Helper functions from worlds_data
def _lesson_step_to_discover(step: Any) -> Discover:
    return Discover(
        visual=step.content or "",
        interaction="read" if step.step_type == "discover" else "",
        prompt=step.prompt or step.title or "",
        answer=step.answer or "",
    )


def _lesson_step_to_manipulate(step: Any) -> Manipulate:
    return Manipulate(
        type=step.step_type or "",
        template=step.template or "",
        answer=step.answer or "",
        hint=step.hint or "",
    )


def _lesson_step_to_predict(step: Any) -> Predict:
    options = []
    for opt in (step.options or []):
        if isinstance(opt, dict):
            options.append(opt.get("text", ""))
        else:
            options.append(str(opt))
    return Predict(
        prompt=step.question or step.title or "",
        answer=_first(options),
        explanation=step.explanation or "",
    )


def _lesson_step_to_build(step: Any) -> Build:
    return Build(
        prompt=step.description or step.title or "",
        starter=step.starter or (step.starter_code.get("python", "") if isinstance(step.starter_code, dict) else "") or "",
        placeholder=step.placeholder or "",
        language=step.language or "python",
    )


def _lesson_step_to_debug(step: Any) -> Debug:
    return Debug(
        prompt=step.description or step.title or "",
        buggy_code=step.buggy_code or "",
        fix_steps=step.fix_steps or [],
        answer=step.answer or "",
    )


def _lesson_step_to_retrieval(step: Any) -> Retrieval:
    return Retrieval(
        prompt=step.question or step.title or "",
        answer=step.answer or step.prompt or "",
        explanation=step.explanation or "",
    )


def _lesson_step_to_transfer(step: Any) -> Transfer:
    return Transfer(
        prompt=step.question or step.title or "",
        answer=step.answer or "",
        context=step.context or step.content or "",
    )


def _extract_checks(lesson: Any) -> Checks:
    required_patterns = []
    for step in (lesson.steps or []):
        if step.step_type in ("build", "mastery") and step.test_cases:
            for tc in step.test_cases:
                expected = tc.get("expected", "")
                if expected:
                    required_patterns.append(str(expected))
                    break
            if required_patterns:
                break
    return Checks(required_patterns=required_patterns[:3])


def _extract_success(lesson: Any, is_boss: bool = False) -> Success:
    diamonds = getattr(lesson, "diamonds", 50)
    if is_boss:
        diamonds = getattr(lesson, "diamonds", 100)
    return Success(
        world_reaction=f"Completed: {lesson.title}",
        reward_text=f"+{diamonds} Diamonds",
        byte_line=None,
        diamonds=diamonds,
    )


def _extract_reward(lesson: Any) -> Reward:
    diamonds = getattr(lesson, "diamonds", 50)
    kind = getattr(lesson, "kind", "level")
    if kind == "boss":
        diamonds = getattr(lesson, "diamonds", 100)
    return Reward(diamonds=diamonds)


def _extract_hints(lesson: Any) -> list[str]:
    hints = []
    for step in (lesson.steps or []):
        if step.hint:
            hints.append(step.hint)
        if step.explanation:
            hints.append(step.explanation)
    if not hints:
        hints = ["Review the concept and try again.", "Check your implementation against the requirements."]
    return hints[:5]


def integrate_worlds_9_12():
    worlds = {
        "ai_engineering": get_world_9(),
        "production": get_world_10(),
        "projects": get_world_11(),
        "creative": get_world_12(),
    }

    added = []
    for wid, wd in worlds.items():
        if not wd:
            print(f"Skipping {wid}: not found")
            continue

        converted = _convert_world(wd)
        WORLD_REGISTRY[wid] = converted
        total_levels = sum(len(t.levels) for t in converted.towns)
        boss_count = sum(1 for t in converted.towns for l in t.levels if l.kind == "boss")
        added.append((wid, converted.name, total_levels, boss_count))
        print(f"Added {wid}: {converted.name}, {len(converted.towns)} towns, {total_levels} levels, {boss_count} bosses")

    return added


if __name__ == "__main__":
    integrate_worlds_9_12()
    print(f"\nWORLD_REGISTRY now has {len(WORLD_REGISTRY)} worlds")
