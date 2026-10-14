"""AI Tutor Service — pedagogical AI modes inside the learning loop.

Modes:
- TEACH: introduce a concept with minimal explanation and an example
- GUIDE: prompt the learner toward the next step without giving the answer
- DIAGNOSE: identify the likely misconception from learner behavior
- DEBUG: help the learner find their own bug
- REFACTOR: suggest cleaner approaches after a working solution
- REFLECT: summarize what the learner just demonstrated

All tutor actions must include:
- mode
- target concept or artifact
- prompt or hint text
- evidence tag to record afterward
- follow-up suggestion
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from app.services.ai_core import chat_completion

logger = logging.getLogger(__name__)

TUTOR_SYSTEM_PROMPT = """You are BountyCode's AI tutor.
Operate inside the learning architecture.
Stay concise.
Do not reveal the final answer unless explicitly in REFACTOR or REFLECT mode.
Always tie guidance back to the current concept and the learner's recorded evidence.
"""


async def tutor_act(
    mode: str,
    *,
    concept_id: Optional[str] = None,
    learner_state: Optional[Dict[str, Any]] = None,
    context: Optional[Dict[str, Any]] = None,
    learner_message: Optional[str] = None,
    solution: Optional[str] = None,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a tutor response for the requested mode.

    Args:
        mode: One of TEACH, GUIDE, DIAGNOSE, DEBUG, REFACTOR, REFLECT.
        concept_id: Optional concept identifier.
        learner_state: Optional canonical learner state.
        context: Optional extra lesson/interaction context.
        learner_message: Optional learner question or submission text.
        solution: Optional learner code/solution artifact.
        error: Optional runtime/test error for DEBUG mode.

    Returns:
        Dict with mode, target, prompt, evidence_tag, follow_up.
    """
    if mode not in {"TEACH", "GUIDE", "DIAGNOSE", "DEBUG", "REFACTOR", "REFLECT"}:
        raise ValueError(f"Unsupported tutor mode: {mode}")

    context = context or {}
    if learner_state:
        context.setdefault("learner_state", learner_state)

    messages = [{"role": "system", "content": TUTOR_SYSTEM_PROMPT}]

    if mode == "TEACH":
        messages.append({
            "role": "user",
            "content": (
                f"Teach concept: {concept_id}\n"
                f"Learner state: {learner_state}\n"
                "Give a short explanation plus one concrete example."
            ),
        })
    elif mode == "GUIDE":
        messages.append({
            "role": "user",
            "content": (
                f"Guide the learner through concept: {concept_id}\n"
                f"Context: {context}\n"
                f"Learner message: {learner_message}\n"
                "Provide a hint or next-step question only. Do not give the answer."
            ),
        })
    elif mode == "DIAGNOSE":
        messages.append({
            "role": "user",
            "content": (
                f"Diagnose the misconception for concept: {concept_id}\n"
                f"Learner state: {learner_state}\n"
                f"Context: {context}\n"
                "Return the likely misconception and one targeted repair step."
            ),
        })
    elif mode == "DEBUG":
        messages.append({
            "role": "user",
            "content": (
                f"Debug help for concept: {concept_id}\n"
                f"Solution: {solution}\n"
                f"Error: {error}\n"
                "Ask questions that help the learner locate the bug themselves."
            ),
        })
    elif mode == "REFACTOR":
        messages.append({
            "role": "user",
            "content": (
                f"Refactor suggestion for concept: {concept_id}\n"
                f"Solution: {solution}\n"
                "Suggest improvements without changing behavior."
            ),
        })
    elif mode == "REFLECT":
        messages.append({
            "role": "user",
            "content": (
                f"Reflection for concept: {concept_id}\n"
                f"Context: {context}\n"
                "Summarize what the learner demonstrated and one next action."
            ),
        })

    try:
        response = await chat_completion(messages, temperature=0.6, max_tokens=600)
    except Exception as exc:
        logger.warning("AI tutor fallback triggered for mode=%s concept=%s: %s", mode, concept_id, exc)
        response = _fallback_response(mode, concept_id)

    evidence_tag = f"{mode.lower()}:{concept_id or 'general'}"
    follow_up = _suggest_follow_up(mode, concept_id)

    return {
        "mode": mode,
        "target": concept_id,
        "prompt": response,
        "evidence_tag": evidence_tag,
        "follow_up": follow_up,
    }


def _fallback_response(mode: str, concept_id: Optional[str]) -> str:
    if mode == "TEACH":
        return f"Start with the definition of {concept_id}, then try one small example."
    if mode == "GUIDE":
        return "What do you expect this line to do? Run it once and compare."
    if mode == "DIAGNOSE":
        return "Check the common misconception for this concept and retry with one changed input."
    if mode == "DEBUG":
        return "Print the intermediate values and compare them with your expected trace."
    if mode == "REFACTOR":
        return "Aim for shorter variable names, fewer branches, and one clear return path."
    if mode == "REFLECT":
        return "You completed this concept. Next, apply it to a slightly harder problem."
    return "Continue with the next step in the lesson."


def _suggest_follow_up(mode: str, concept_id: Optional[str]) -> Optional[str]:
    if mode == "TEACH":
        return f"predict:{concept_id}"
    if mode == "GUIDE":
        return f"solve:{concept_id}"
    if mode == "DIAGNOSE":
        return f"repair:{concept_id}"
    if mode == "DEBUG":
        return f"fix:{concept_id}"
    if mode == "REFACTOR":
        return f"transfer:{concept_id}"
    if mode == "REFLECT":
        return f"next_concept"
    return None
