"""Captain Byte speeches for the journey itself.

Not a skill domain — the voice used when a learner lands on Today/Journey and
the next action carries no skill of its own (continue, explore, first visit).
Without this the journey would ship an empty mentor, which reads as a bug.
"""
from typing import Any, Dict

from ._text import block

DOMAIN_JOURNEY: Dict[str, Any] = block(
    "“Start with the mission in front of you. It sits in the gap between what "
    "you can already do and what the next unlock needs — that gap is where "
    "capability actually grows, and it is the only thing worth working today.”",
    [
        "“Good. Keep the pace — steady beats intense.”",
        "“Nice. That moved the gap closer.”",
    ],
    [
        "“Stop. Read the mission again — you answered a different question.”",
        "“Careful — the answer is close, but it isn’t the one asked.”",
    ],
    "“You found the broken assumption. Name it, then repair it.”",
    "“You’ve got it. That unlock is earned — take the next one on your own.”",
    "“Try again. Slow down and show me the reasoning.”",
)

#: skill-id prefix -> authored journey voice (step 3 of resolve_authored)
DOMAIN_FALLBACK_ENTRY: Dict[str, Dict[str, Any]] = {"journey": DOMAIN_JOURNEY}
