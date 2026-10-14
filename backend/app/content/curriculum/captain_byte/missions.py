"""Captain Byte mission narration — brief and consequence lines.

Narration only: threat framing before a mission, forward commitment after
the verdict. No questions, no answers, no company claims — those live in
the banks under the trust pipeline. Keyed by mission domain; the journey
voice covers anything without a domain.
"""
from typing import Any, Dict

from ._text import line

#: domain -> {brief, consequence_mastery, consequence_repair}
MISSION_LINES: Dict[str, Dict[str, Any]] = {
    "aptitude": {
        "brief": "“Round one eliminates most candidates on speed, not knowledge. "
                 "Ninety seconds a question. Commit fast, verify faster.”",
        "consequence_mastery": "“Proved under time. In two days you face a harder transfer — "
                               "same skill, unfamiliar skin.”",
        "consequence_repair": "“Not yet. A repair mission lands before you advance — "
                              "the trap you missed, rebuilt.”",
    },
    "reasoning": {
        "brief": "“Draw before you solve. One misread constraint sinks the whole set — "
                 "the diagram is the answer half-written.”",
        "consequence_mastery": "“Clean elimination. In two days the constraints get meaner.”",
        "consequence_repair": "“Not yet. Rebuild the diagram habit first — repair before advancing.”",
    },
    "verbal": {
        "brief": "“The passage decides, not your memory of the topic. Answer from "
                 "evidence, once, and move on.”",
        "consequence_mastery": "“Precise under time. In two days a denser passage.”",
        "consequence_repair": "“Not yet. Evidence discipline first — repair before advancing.”",
    },
    "coding": {
        "brief": "“One or two easy problems. Predict the output before you run it — "
                 "tracing is the skill being tested.”",
        "consequence_mastery": "“Hidden tests passed first try. In two days a new shape, same skill.”",
        "consequence_repair": "“Not yet. Trace more, assume less — repair before advancing.”",
    },
    "cs_core": {
        "brief": "“Explain the mechanism, not the definition. The first follow-up "
                 "cracks anything memorised.”",
        "consequence_mastery": "“Held under follow-ups. In two days a scenario you haven't seen.”",
        "consequence_repair": "“Not yet. Mechanism first — repair before advancing.”",
    },
    "company_quest": {
        "brief": "“Same engine, their weightage. The interface and the clock cause "
                 "failures too — treat both as the test.”",
        "consequence_mastery": "“Pattern cleared. The full mock is unlocked.”",
        "consequence_repair": "“Not yet. Pattern drill tomorrow, then you re-attempt.”",
    },
}


def mission_line(domain: str, kind: str) -> str:
    """One authored narration line. kind: brief | consequence_mastery |
    consequence_repair. Falls back to the journey voice; never generic."""
    from .journey import DOMAIN_JOURNEY

    entry = MISSION_LINES.get((domain or "").strip())
    if entry and entry.get(kind):
        return line(entry[kind])
    # Journey voice fallback (authored, never generic).
    from .journey import DOMAIN_JOURNEY

    if kind == "brief":
        return DOMAIN_JOURNEY["intro"]
    return DOMAIN_JOURNEY["after_mastery"]
