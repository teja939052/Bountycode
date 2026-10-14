"""Runtime contract test for the single Captain Byte mentor resolver.

Asserts the client contract end to end through real code paths — the journey
builder, the lesson service and the resolver itself — not fixtures.

Covers: journey mentor, lesson intro, correct_1/2, wrong_1/2, after_break,
after_mastery, slug-alias resolution, and that no new state writer exists.
"""
import asyncio
import inspect
import sys

import pytest

from app.content.curriculum.registry import LESSON_REGISTRY
from app.content.curriculum.captain_byte import GENERIC, is_generic_block
from app.services.mentor_service import (
    MOMENTS,
    MOOD_BY_MOMENT,
    PHASE_BY_MOMENT,
    mentor_block_for_lesson,
    resolve_captain_byte,
)

#: The real MentorMood union — frontend/src/design-system/Mentor.tsx.
#: A mood outside this list silently renders as no mood.
MENTOR_MOODS = {
    "welcome", "briefing", "explaining", "correcting", "encouraging",
    "proud", "celebrating", "serious", "thinking", "stuck", "handoff",
}

#: Real useMentor phases — frontend/src/hooks/useMentor.ts.
MENTOR_PHASES = {
    "idle", "loading", "intro", "active", "correcting", "repair",
    "success", "mastery", "boss", "stuck", "complete",
}


def _mentor(moment, skill="code.loops", **kw):
    out = resolve_captain_byte(canonical_skill=skill, moment=moment, **kw)
    assert out["block"], f"{moment}: mentor returned no block"
    assert out["block"] != GENERIC["intro"], f"{moment}: generic copy leaked"
    assert out["message"].strip(), f"{moment}: empty message"
    assert out["mood"] in MENTOR_MOODS, f"{moment}: unknown mood {out['mood']!r}"
    assert out["phase"] in MENTOR_PHASES, f"{moment}: unknown phase {out['phase']!r}"
    assert out["moment"] == moment
    assert out["character"] == "captain_byte"
    return out


def test_journey_state_carries_a_non_generic_mentor():
    """1. build_journey_state returns a mentor with real authored speech."""
    from app.services.journey_engine import build_journey_state

    state = asyncio.run(build_journey_state("mentor_contract_probe"))
    mentor = state.get("mentor")
    assert isinstance(mentor, dict), "journey_state has no mentor field"
    assert mentor.get("block"), "journey mentor block is empty"
    assert not is_generic_block({"intro": mentor["block"]}), "journey mentor is generic"
    assert mentor["moment"] == "intro"
    assert mentor["mood"] in MENTOR_MOODS
    assert mentor["phase"] in MENTOR_PHASES
    assert mentor["body"] or mentor["title"], "journey mentor explains nothing"


def test_lesson_intro_carries_a_mentor():
    """2. The served lesson response carries an intro mentor with a block."""
    from app.services.lesson import LessonService

    lesson = next(
        l for l in LESSON_REGISTRY.values() if l.get("srs_concept_tag")
    )
    served = LessonService(lesson).get_lesson()

    mentor = served.get("mentor")
    assert isinstance(mentor, dict), "lesson response has no mentor"
    assert mentor["moment"] == "intro"
    assert mentor["block"], "lesson intro block is empty"
    assert not is_generic_block({"intro": mentor["block"]}), "lesson intro is generic"

    # captain_byte must be authored for every served lesson, not the placeholder.
    assert not is_generic_block(served.get("captain_byte")), (
        "a served lesson still ships the generic captain_byte"
    )


def test_correct_and_wrong_moments():
    """3-6. correct_1/2 and wrong_1/2 each resolve to authored speech."""
    c1 = _mentor("correct_1")
    c2 = _mentor("correct_2")
    w1 = _mentor("wrong_1")
    w2 = _mentor("wrong_2")

    # Repeated praise and repeated failure must be distinct lines.
    assert c1["block"] != c2["block"], "correct_1 and correct_2 are identical"
    assert w1["block"] != w2["block"], "wrong_1 and wrong_2 are identical"

    # Failure lines must name something, not congratulate.
    for w in (w1, w2):
        assert w["mood"] in {"encouraging", "correcting", "serious", "explaining"}, (
            f"wrong moment used mood {w['mood']!r}"
        )
    assert c1["mood"] in {"proud", "celebrating", "welcome"}


def test_after_break_and_after_mastery():
    """7-8. Repair and mastery moments resolve to authored speech."""
    brk = _mentor("after_break")
    mast = _mentor("after_mastery")

    assert brk["phase"] == "repair"
    assert brk["mood"] in {"serious", "correcting", "thinking", "explaining"}

    assert mast["phase"] == "mastery"
    assert mast["mood"] in {"proud", "celebrating", "encouraging"}


def test_slug_alias_resolution():
    """Slug aliases reach authored content for lessons with no canonical skill."""
    # Short registry slug path.
    by_slug = resolve_captain_byte(lesson_slug="loops", moment="intro")
    assert by_slug["block"], "slug alias 'loops' did not resolve"

    # The 13 lessons that ship without a canonical skill.
    silent = [
        "variables_state", "control_flow", "loops", "arrays", "strings",
        "functions", "sorting", "complexity", "program_io", "assignment_boxes",
        "types_values", "expressions_order", "trace_mini",
    ]
    for slug in silent:
        out = resolve_captain_byte(lesson_slug=slug, moment="intro")
        assert out["block"], f"slug alias {slug!r} did not resolve"

    # Every served lesson still resolves — either through the adapter or by
    # keeping speech it already ships. Losing speech is the only failure.
    lose_speech = [
        l.get("lesson_id")
        for l in LESSON_REGISTRY.values()
        if not mentor_block_for_lesson(l)
        and is_generic_block(l.get("captain_byte"))
    ]
    assert not lose_speech, f"lessons that would lose speech: {lose_speech}"

    # And no served lesson may answer its intro with an empty mentor.
    from app.services.lesson import LessonService

    empty = [
        lid for lid, l in LESSON_REGISTRY.items()
        if not LessonService(l).get_lesson()["mentor"]["block"]
    ]
    assert not empty, f"lessons with an empty intro mentor: {empty}"


def test_no_new_state_writer():
    """10. The mentor library is content: it reads state, never writes it."""
    import app.services.mentor_service as mentor_service

    src = inspect.getsource(mentor_service)
    for forbidden in (
        "app.database", "insert_one", "update_one", "delete_one",
        "record_practice", "find_one_and_update", "gamification_collection",
        "srs_collection", "httpx", "openrouter", "chat_completion",
    ):
        assert forbidden not in src, f"mentor_service references {forbidden!r}"

    # The payload is speech only — no reward or progression fields.
    payload = resolve_captain_byte(canonical_skill="code.loops", moment="after_mastery")
    for field in (
        "xp", "xp_gained", "diamonds", "coins", "mastery", "mastery_unlocked",
        "srs", "level", "streak", "badge",
    ):
        assert field not in payload, f"mentor payload leaks {field!r}"

    # Every moment is a member of the single canonical vocabulary.
    assert set(MOMENTS) == {
        "intro", "correct_1", "correct_2", "wrong_1", "wrong_2",
        "after_break", "after_mastery", "retry_prompt",
    }
    bad_moods = set(MOOD_BY_MOMENT.values()) - MENTOR_MOODS
    assert not bad_moods, f"moods outside the MentorMood union: {bad_moods}"
    assert set(PHASE_BY_MOMENT.values()) <= MENTOR_PHASES


def test_resolver_is_deterministic():
    """Same state event -> same mood and same block, every time."""
    first = resolve_captain_byte(
        canonical_skill="code.loops", moment="wrong_1",
        learner_state={"mistake_count": 3},
    )
    second = resolve_captain_byte(
        canonical_skill="code.loops", moment="wrong_1",
        learner_state={"mistake_count": 3},
    )
    assert first == second, "resolver is not deterministic"

    # Repeated failure escalates the mood instead of cheering.
    assert first["mood"] == "serious", first["mood"]
