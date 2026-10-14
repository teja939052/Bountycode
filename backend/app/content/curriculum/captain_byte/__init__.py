"""Captain Byte speech library — deterministic and prebuilt. No LLM, ever.

Every lesson reaches the client as a six-key speech block (the format already
used by `content/curriculum/flagship/*.py`):

    intro           long scene-setter read when the lesson opens
    correct[]       two praise lines
    wrong[]         two diagnostic lines, each naming the actual mistake
    after_break     spoken after the student breaks working code
    after_mastery   spoken once the concept is proven
    retry_prompt    the nudge shown after a failed attempt

Resolution order (first hit wins):

    1. exact canonical skill id          "quant.percentages"
    2. domain fallback                   "quant" -> the shared quant voice
    3. title keyword                     "percentages" in the lesson title
    4. generic

This module is inert until a wrapper imports it — adding content here can
never break a running route.
"""
from typing import Any, Dict, List, Optional

from ._text import KEYS, PREAMBLE, block, line
from .aliases import SLUG_SKILL, SRS_SKILL, skill_for_lesson, skill_for_slug
from .aptitude import APTITUDE, DOMAIN_APTITUDE
from .company import COMPANY, DOMAIN_COMPANY
from .cs_core import CS_CORE, DOMAIN_CS
from .engineering import DOMAIN_ENGINEERING, ENGINEERING
from .interview import INTERVIEW, DOMAIN_INTERVIEW
from .journey import DOMAIN_JOURNEY
from .placement import PLACEMENT, DOMAIN_PLACEMENT
from .programming import DOMAIN_PROGRAMMING, PROGRAMMING

GENERIC: Dict[str, Any] = {
    "intro": line("“Let’s master this. Follow the steps, and I’ll guide you.”"),
    "correct": [
        line("“Nice work. That’s the move.”"),
        line("“Clean. You did it deliberately, not by luck.”"),
    ],
    "wrong": [
        line("“Stop. Read the step again — what is it actually asking?”"),
        line("“Close. Name the assumption you just made before you try again.”"),
    ],
    "after_break": line("“You found the broken assumption. Now repair it.”"),
    "after_mastery": line("“You’ve got it. I’m removing the training wheels.”"),
    "retry_prompt": line("“Try again. Slow down and show me the reasoning.”"),
}

#: skill-id prefix -> the bank that owns it
BANKS: Dict[str, Dict[str, Dict[str, Any]]] = {
    "placement": PLACEMENT,
    "aptitude": APTITUDE,
    "quant": APTITUDE,
    "reason": APTITUDE,
    "verbal": APTITUDE,
    "cs_fundamentals": CS_CORE,
    "company": COMPANY,
    "interview": INTERVIEW,
    "code": PROGRAMMING,
    "dsa": PROGRAMMING,
    "backend": ENGINEERING,
    "data": ENGINEERING,
    "engineering": ENGINEERING,
    "sd": ENGINEERING,
    "creative": ENGINEERING,
}

#: skill-id prefix -> fallback block when a skill has no authored entry
DOMAIN_FALLBACK: Dict[str, Dict[str, Any]] = {
    "placement": DOMAIN_PLACEMENT,
    "aptitude": DOMAIN_APTITUDE,
    "quant": DOMAIN_APTITUDE,
    "reason": DOMAIN_APTITUDE,
    "verbal": DOMAIN_APTITUDE,
    "cs_fundamentals": DOMAIN_CS,
    "company": DOMAIN_COMPANY,
    "interview": DOMAIN_INTERVIEW,
    "code": DOMAIN_PROGRAMMING,
    "dsa": DOMAIN_PROGRAMMING,
    "backend": DOMAIN_ENGINEERING,
    "data": DOMAIN_ENGINEERING,
    "engineering": DOMAIN_ENGINEERING,
    "sd": DOMAIN_ENGINEERING,
    "creative": DOMAIN_ENGINEERING,
    # Not a skill domain: the voice used when a journey action carries no
    # skill of its own (continue / explore / first visit).
    "journey": DOMAIN_JOURNEY,
}


def skill_bank() -> Dict[str, Dict[str, Any]]:
    """Flat view of every authored skill entry — used by audits and tests."""
    flat: Dict[str, Dict[str, Any]] = {}
    for bank in BANKS.values():
        flat.update(bank)
    return flat


def resolve(
    skill_id: Optional[str] = None,
    title: Optional[str] = None,
    difficulty: Optional[str] = None,
    slug: Optional[str] = None,
) -> Dict[str, Any]:
    """Return a complete six-key speech block for a lesson.

    Resolution order, most specific first:

        1. ``skill_id``    exact canonical skill   "quant.percentages"
        2. ``slug``        alias table             "variables_state"
        3. domain          "quant" -> shared quant voice
        4. ``title``       keyword sweep
        5. generic

    ``difficulty`` is accepted for callers that already have it; it never
    rewrites authored prose, so it is intentionally unused here.
    """
    skill = (skill_id or "").strip()
    if not skill:
        skill = skill_for_slug(slug or "")
    lower_heading = (title or "").strip().lower()

    # 1. exact canonical skill id
    if skill:
        bank = BANKS.get(skill.split(".")[0])
        if bank and skill in bank:
            return _normalize(bank[skill])

    # 2. domain fallback
    if "." in skill:
        fallback = DOMAIN_FALLBACK.get(skill.split(".")[0])
        if fallback:
            return _normalize(fallback)

    # 3. title keyword sweep across every authored entry
    if lower_heading:
        for bank in BANKS.values():
            for key, authored in bank.items():
                words = key.split(".")[-1].replace("_", " ").split()
                if words and all(w in lower_heading for w in words):
                    return _normalize(authored)

    # 4. generic — still six keys, still a valid speech block
    return _normalize(GENERIC)


def captain_byte_for(
    skill_id: Optional[str] = None,
    title: Optional[str] = None,
    difficulty: Optional[str] = None,
    level: Optional[int] = None,
    slug: Optional[str] = None,
) -> Dict[str, Any]:
    """Public entry point.

    ``level`` tints the opening line on the very first level of a world
    (day one) and on the capstone (level 32) — the two moments where a
    generic opening reads wrong.
    """
    block_out = resolve(skill_id=skill_id, title=title, difficulty=difficulty, slug=slug)
    if level in (1, 32):
        body = block_out["intro"].split("\n", 1)[-1].strip("“”")
        if level == 1:
            tail = " This is your first step here — take it slowly, I’m not going anywhere."
        else:
            tail = " This is the capstone of this world. Prove it holds without me."
        block_out["intro"] = line("“" + body + tail + "”")
    return block_out


def resolve_authored(
    skill_id: Optional[str] = None,
    slug: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Strict resolution used by the mentor service.

    Fallback order, exactly:

        1. canonical_skill exact match        "quant.percentages"
        1b. srs_concept_tag alias             "programming_fundamentals:loops"
        2. lesson_slug alias match            "loops"
        3. world-level authored fallback      "quant" -> the shared voice
        4. None  -> caller omits speech rather than serving filler

    Returns None instead of GENERIC: generic copy is a bug, not a fallback.
    """
    skill = (skill_id or "").strip()

    # 1. canonical skill exact match
    if skill:
        bank = BANKS.get(skill.split(".")[0])
        if bank and skill in bank:
            return _normalize(bank[skill])

    # 1b. srs_concept_tag alias — "programming_fundamentals:variables" is the
    #     one skill key every lesson actually ships with.
    srs = SRS_SKILL.get(skill, "")
    if srs:
        bank = BANKS.get(srs.split(".")[0])
        if bank and srs in bank:
            return _normalize(bank[srs])

    # 2. lesson slug alias match
    aliased = skill_for_slug(slug or "")
    if aliased:
        bank = BANKS.get(aliased.split(".")[0])
        if bank and aliased in bank:
            return _normalize(bank[aliased])

    # 3. world-level authored fallback
    if "." in skill:
        fallback = DOMAIN_FALLBACK.get(skill.split(".")[0])
        if fallback:
            return _normalize(fallback)
    if aliased and "." in aliased:
        fallback = DOMAIN_FALLBACK.get(aliased.split(".")[0])
        if fallback:
            return _normalize(fallback)

    # 4. no speech block
    return None


def is_generic_block(block: Any) -> bool:
    """True when a shipped `captain_byte` is the placeholder, not authored prose.

    Several lessons were published with the library's generic block baked in;
    callers use this to tell 'shipped speech' from 'shipped filler'.
    """
    if not isinstance(block, dict):
        return True
    intro = block.get("intro")
    return not isinstance(intro, str) or intro == GENERIC["intro"]


def speech_for_lesson(lesson: Dict[str, Any], slug: Optional[str] = None) -> Dict[str, Any]:
    """Resolve the speech block for a raw lesson dict (registry entry).

    Returns a complete six-key block. Callers should prefer the lesson's own
    authored ``captain_byte`` when it has one — this exists for the lessons
    that ship without one.
    """
    skill = skill_for_lesson(lesson, slug=slug)
    return captain_byte_for(
        skill_id=skill,
        title=lesson.get("title", ""),
        level=None,
        slug=slug or lesson.get("slug"),
    )


def _normalize(authored: Dict[str, Any]) -> Dict[str, Any]:
    """Guarantee all six keys exist and every value carries the banner."""
    out: Dict[str, Any] = {}
    for key in KEYS:
        value = authored.get(key)
        if value is None:
            value = GENERIC[key]
        if key in ("correct", "wrong"):
            items = value if isinstance(value, (list, tuple)) else [value]
            items = [line(str(i)) for i in items] or list(GENERIC[key])
            while len(items) < 2:
                items.append(GENERIC[key][len(items)])
            out[key] = items
        else:
            out[key] = line(str(value))
    return out


__all__ = [
    "GENERIC",
    "BANKS",
    "DOMAIN_FALLBACK",
    "PREAMBLE",
    "SLUG_SKILL",
    "SRS_SKILL",
    "captain_byte_for",
    "resolve",
    "resolve_authored",
    "skill_bank",
    "skill_for_lesson",
    "speech_for_lesson",
]
