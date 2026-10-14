"""Mentor service — the single backend resolver for Captain Byte speech.

Captain Byte is a curriculum narrator with a job, not a chatbot. He speaks at
moments of uncertainty, insight, correction and achievement — never as
decoration on utility screens.

This module is the ONLY place authored speech is turned into a mentor payload.
Pages, routes and engines call :func:`resolve_captain_byte`; nothing imports
the content library directly.

Contract
--------
    canonical_skill exact match
    -> lesson_slug alias match
    -> authored world-level fallback
    -> no speech block

Deterministic by construction:

    state event -> deterministic mood -> deterministic authored block

Guarantees
----------
* Read-only. No database access, no collection, no writes of any kind.
* Never calls an LLM. Never returns a random quote.
* Never returns generic filler — generic copy is treated as a bug, so an
  unresolved moment returns ``block: None`` instead of a fake message.
* Does not award XP, coins, mastery or SRS state. The mentor library is
  content: it reads canonical learning state, it never writes it.
"""
from typing import Any, Dict, Optional

from app.content.curriculum.captain_byte import (
    is_generic_block,
    resolve_authored,
)

__all__ = [
    "MOMENTS",
    "MOOD_BY_MOMENT",
    "PHASE_BY_MOMENT",
    "mentor_block_for_lesson",
    "resolve_captain_byte",
]

#: The deterministic moment vocabulary. One canonical list for the whole app.
MOMENTS = (
    "intro",
    "correct_1",
    "correct_2",
    "wrong_1",
    "wrong_2",
    "after_break",
    "after_mastery",
    "retry_prompt",
)

#: moment -> authored slot inside the library's six-key block
_SLOT: Dict[str, tuple] = {
    "intro": ("intro", None),
    "correct_1": ("correct", 0),
    "correct_2": ("correct", 1),
    "wrong_1": ("wrong", 0),
    "wrong_2": ("wrong", 1),
    "after_break": ("after_break", None),
    "after_mastery": ("after_mastery", None),
    "retry_prompt": ("retry_prompt", None),
}

#: Base mood per moment. These are values from the real ``MentorMood`` union
#: in frontend/src/design-system/Mentor.tsx — never invent a mood outside it.
MOOD_BY_MOMENT: Dict[str, str] = {
    "intro": "welcome",
    "correct_1": "proud",
    "correct_2": "proud",
    "wrong_1": "encouraging",
    "wrong_2": "correcting",
    "after_break": "serious",
    "after_mastery": "celebrating",
    "retry_prompt": "encouraging",
}

#: moment -> the useMentor phase this belongs to.
PHASE_BY_MOMENT: Dict[str, str] = {
    "intro": "intro",
    "correct_1": "success",
    "correct_2": "success",
    "wrong_1": "correcting",
    "wrong_2": "correcting",
    "after_break": "repair",
    "after_mastery": "mastery",
    "retry_prompt": "active",
}

#: Short call-to-action shown under the speech bubble, by moment.
_CTA: Dict[str, str] = {
    "intro": "Begin",
    "correct_1": "Continue",
    "correct_2": "Continue",
    "wrong_1": "Try again",
    "wrong_2": "Try again",
    "after_break": "Repair it",
    "after_mastery": "Next",
    "retry_prompt": "Try again",
}

_BANNER = "\N{COMPASS} **Captain Byte**\n"


def _mood_for(moment: str, learner_state: Optional[Dict[str, Any]]) -> str:
    """Deterministic mood: state event -> mood. No randomness anywhere."""
    base = MOOD_BY_MOMENT.get(moment, "thinking")
    state = learner_state or {}

    mistakes = int(state.get("mistake_count") or 0)

    # Repeated failure on the same skill is concern, not cheerfulness.
    if moment.startswith("wrong") and mistakes >= 2:
        return "serious"

    # Timed assessment and retests want calm, even-handed delivery.
    if state.get("timed") or state.get("retest"):
        if moment in ("intro", "retry_prompt"):
            return "thinking"

    # Debugging and diagnosis read as explanation, not celebration.
    if state.get("stage") == "debug" and moment in ("intro", "wrong_1", "wrong_2"):
        return "explaining"

    # First contact with a new world gets the welcome mood.
    if moment == "intro" and state.get("new_world"):
        return "welcome"

    return base


def _split(text: str) -> tuple:
    """Split authored prose into (title, body) on the first sentence."""
    body = text
    if body.startswith(_BANNER):
        body = body[len(_BANNER):]
    body = body.strip()
    if ". " in body:
        head, rest = body.split(". ", 1)
        title = head.rstrip(".") + "."
        body = rest.strip()
    else:
        title, body = body, ""
    return title, body


def mentor_block_for_lesson(
    lesson: Dict[str, Any], slug: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Full six-key authored block for a served lesson, or None.

    This is the lesson-level sibling of :func:`resolve_captain_byte`. Both go
    through this one adapter so no caller reaches into the content library.
    Returns None when the lesson already carries authored speech, so callers
    leave a trusted ``captain_byte`` untouched.

    ``slug`` is the registry key when the caller has it — several lessons are
    known only by that key, not by ``lesson_id``.
    """
    if not isinstance(lesson, dict):
        return None

    existing = lesson.get("captain_byte")
    if existing and not is_generic_block(existing):
        return None

    skill = (
        lesson.get("canonical_skill")
        or (lesson.get("srs_concept_tag") or "").strip()
        or " ".join(lesson.get("skills") or lesson.get("skills_taught") or []).strip()
    )
    key = slug or lesson.get("slug") or lesson.get("lesson_id") or ""
    return resolve_authored(skill_id=skill, slug=key)


def resolve_captain_byte(
    *,
    canonical_skill: Optional[str] = None,
    lesson_slug: Optional[str] = None,
    moment: str = "intro",
    learner_state: Optional[Dict[str, Any]] = None,
    mission_result: Optional[Dict[str, Any]] = None,
    target_context: Optional[Dict[str, Any]] = None,
    fallback_block: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Return one authored Captain Byte block for a canonical learning moment.

    Parameters
    ----------
    canonical_skill:
        Canonical skill id, e.g. ``quant.percentages``. Preferred key.
    lesson_slug:
        Lesson slug, used only when ``canonical_skill`` is absent or
        unresolvable — this is the alias path for shipped lessons.
    moment:
        One of :data:`MOMENTS`.
    learner_state:
        Read-only view of learner context (``mistake_count``, ``stage``,
        ``timed``, ``retest``, ``new_world``). Drives the mood only.
    mission_result / target_context:
        Accepted so callers have one call site regardless of context. Used
        for mood refinement and the CTA; never persisted.
    fallback_block:
        An already-authored six-key block (a lesson's own ``captain_byte``).
        Used only when skill and slug both fail. Generic blocks are ignored.

    Returns
    -------
    A payload carrying the canonical ``moment``/``block`` plus the
    ``mood``/``message``/``phase`` triple the frontend ``Mentor`` component
    consumes. When nothing resolves, ``block`` is None and ``message`` is
    empty — never generic filler.
    """
    if moment not in _SLOT:
        moment = "intro"

    # Two shapes of skill arrive here: the authored dotted id
    # ("dsa.binary_search") and SRS-style tags ("programming_fundamentals:loops",
    # "dsa:binary_search"). Try the tag as shipped first — that is the key the
    # alias table uses — then the dotted form. Normalising up front would hide
    # the tag from its own lookup table.
    skill = (canonical_skill or "").strip()
    dotted = skill.replace(":", ".", 1) if (":" in skill and "." not in skill) else skill

    authored = resolve_authored(skill_id=skill, slug=lesson_slug)
    if authored is None and dotted != skill:
        authored = resolve_authored(skill_id=dotted, slug=lesson_slug)
    # Last authored option: the lesson's own speech, which is trusted content
    # for that lesson and already written in the six-key shape.
    if authored is None and isinstance(fallback_block, dict) and not is_generic_block(fallback_block):
        authored = fallback_block
    mood = _mood_for(moment, learner_state)

    payload: Dict[str, Any] = {
        "character": "captain_byte",
        "moment": moment,
        "mood": mood,
        "phase": PHASE_BY_MOMENT.get(moment, "active"),
        "block": None,
        "message": "",
        "title": "",
        "body": "",
        "cta": _CTA.get(moment, ""),
    }
    if not authored:
        return payload

    key, index = _SLOT[moment]
    slot = authored.get(key)
    if index is not None:
        items = slot if isinstance(slot, list) else []
        slot = items[index] if index < len(items) else (items[-1] if items else None)

    if not isinstance(slot, str) or not slot:
        return payload

    title, body = _split(slot)
    payload["block"] = slot
    payload["message"] = body or title
    payload["title"] = title
    payload["body"] = body

    # Mastery and completion CTAs may be overridden by the caller's result.
    if mission_result and moment == "after_mastery":
        weak = mission_result.get("weak_pattern") or mission_result.get("weak_pattern_tag")
        if weak:
            payload["title"] = "You proved it under pressure."
            payload["body"] = "Still weak in one place: %s. Keep that warm." % weak

    if target_context:
        company = target_context.get("target_company") or target_context.get("company")
        if company and moment == "intro":
            payload["body"] = (payload["body"] + " %s tests this." % company).strip()

    return payload
