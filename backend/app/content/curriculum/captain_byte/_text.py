"""Shared formatting helpers for the Captain Byte speech banks.

Kept in its own module so every bank can import it without importing the
package root (which imports the banks).
"""
from typing import Any, Dict, List

PREAMBLE = "🧭 **Captain Byte**\n"

KEYS = ("intro", "correct", "wrong", "after_break", "after_mastery", "retry_prompt")


def line(text: str) -> str:
    """Prefix authored prose with the Captain Byte banner, once."""
    if text.startswith("🧭"):
        return text
    return PREAMBLE + text


def block(
    intro: str,
    correct: List[str],
    wrong: List[str],
    after_break: str,
    after_mastery: str,
    retry_prompt: str,
) -> Dict[str, Any]:
    """Build one six-key speech block from authored prose."""
    return {
        "intro": line(intro),
        "correct": [line(c) for c in correct],
        "wrong": [line(w) for w in wrong],
        "after_break": line(after_break),
        "after_mastery": line(after_mastery),
        "retry_prompt": line(retry_prompt),
    }
