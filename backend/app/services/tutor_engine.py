"""Tutor Engine — finite-state tutor trees for deterministic, zero-AI teaching.

Design:
- Trees are JSON files under `backend/app/data/tutor_trees/`.
- Each node is a dialogue step with a `move` type and explicit options.
- The only branching signal is the student's chosen option, which maps to a
  misconception code. No free text is accepted anywhere.
- Moves are selected by `TutorMoveSelector`, a pure-rules module.
- Personalization is string interpolation against a student profile, not LLM generation.
"""

from __future__ import annotations

import json
import logging
import random
import string
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.database import tutor_sessions_collection, learning_events_collection

logger = logging.getLogger(__name__)

_TUTOR_DIR = Path(__file__).parent.parent / "data" / "tutor_trees"
_trees: Dict[str, Dict[str, Any]] = {}
_loaded = False


def _load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_tutor_trees() -> Dict[str, Dict[str, Any]]:
    """Load all tutor trees into memory. Safe to call multiple times."""
    global _trees, _loaded
    if _loaded:
        return _trees
    if not _TUTOR_DIR.exists():
        logger.warning("Tutor trees directory not found: %s", _TUTOR_DIR)
        return {}
    for path in sorted(_TUTOR_DIR.glob("*.json")):
        try:
            data = _load_json(path)
            tree_id = data.get("id") or path.stem
            _trees[tree_id] = data
        except Exception as exc:
            logger.debug("Failed to load tutor tree %s: %s", path, exc)
    _loaded = True
    logger.info("Tutor trees loaded: %d trees", len(_trees))
    return _trees


def get_tutor_tree(tree_id: str) -> Dict[str, Any]:
    if not _trees:
        load_tutor_trees()
    return _trees.get(tree_id, {})


def get_tree_for_atom(atom_id: str) -> Dict[str, Any]:
    """Find the tutor tree attached to an atom_id."""
    for tree in _trees.values():
        if tree.get("atom_id") == atom_id:
            return tree
    return {}


def start_tutor_session(user_id: str, atom_id: str, tree_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new tutor session and return the first rendered node."""
    tree = get_tutor_tree(tree_id)
    if not tree:
        raise ValueError(f"Tutor tree not found: {tree_id}")

    session_id = _make_session_id()
    node = render_node(tree, tree.get("start", {}), profile, session_id)

    session = {
        "session_id": session_id,
        "user_id": user_id,
        "atom_id": atom_id,
        "tree_id": tree_id,
        "profile": profile,
        "current_node": node,
        "history": [],
        "misconception_codes": [],
        "teach_back_attempts": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "last_node_shown_at": datetime.now(timezone.utc).isoformat(),
    }
    tutor_sessions_collection.insert_one(session)
    return _sanitize_session(session)


async def advance_tutor_session(session_id: str, option_index: int, profile: Dict[str, Any]) -> Dict[str, Any]:
    """Advance a tutor session by student's chosen option index."""
    session = tutor_sessions_collection.find_one({"session_id": session_id})
    if not session:
        raise ValueError("Tutor session not found")

    current_node = session.get("current_node", {})
    opts = current_node.get("opts", [])
    if option_index < 0 or option_index >= len(opts):
        raise ValueError("Invalid option index")

    chosen = opts[option_index]
    misconception_code = chosen.get("code", "unknown")
    next_node_id = chosen.get("to", "done")

    tree = get_tutor_tree(session.get("tree_id", ""))
    next_node = render_node(tree, tree.get(next_node_id, {}), profile, session_id) if next_node_id != "done" else {
        "move": "advance",
        "say": "Session complete.",
        "opts": [],
    }

    history_entry = {
        "from_node": current_node.get("move"),
        "chosen_text": chosen.get("t"),
        "misconception_code": misconception_code,
        "to_node": next_node_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Calculate dwell time on the previous node
    dwell_seconds = 0.0
    last_shown = session.get("last_node_shown_at")
    if last_shown:
        try:
            last_dt = datetime.fromisoformat(last_shown)
            dwell_seconds = (datetime.now(timezone.utc) - last_dt).total_seconds()
        except Exception:
            dwell_seconds = 0.0

    if misconception_code not in ("resolved",):
        session["misconception_codes"].append(misconception_code)

    session["current_node"] = next_node
    session["history"].append(history_entry)
    session["updated_at"] = datetime.now(timezone.utc).isoformat()
    session["last_node_shown_at"] = datetime.now(timezone.utc).isoformat()

    if next_node.get("move") == "teach_back":
        session["teach_back_attempts"] = session.get("teach_back_attempts", 0) + 1

    # Log learning event
    try:
        learning_events_collection.insert_one({
            "session_id": session_id,
            "user_id": session.get("user_id"),
            "atom_id": session.get("atom_id"),
            "tree_id": session.get("tree_id"),
            "node": current_node.get("move"),
            "option_chosen": chosen.get("t"),
            "misconception_code": misconception_code,
            "move_used": current_node.get("move"),
            "dwell_seconds": round(dwell_seconds, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    except Exception as exc:
        logger.debug("Failed to log tutor learning event: %s", exc)

    tutor_sessions_collection.update_one({"session_id": session_id}, {"$set": session})
    return _sanitize_session(session)


def render_node(tree: Dict[str, Any], node: Dict[str, Any], profile: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """Render a tutor tree node with profile interpolation and parametric values."""
    if not node:
        return {"move": "advance", "say": "Session complete.", "opts": []}

    rendered: Dict[str, Any] = dict(node)

    if rendered.get("move") == "hint_ladder":
        hints = node.get("hints", [])
        rendered["hints"] = [_interpolate(h, profile) for h in hints]
        rendered["say"] = _interpolate(node.get("say", ""), profile)

    elif rendered.get("move") == "teach_back":
        rendered["say"] = _interpolate(node.get("say", ""), profile)
        cards = node.get("cards", [])
        random.seed(session_id)
        shuffled = list(range(len(cards)))
        random.shuffle(shuffled)
        rendered["cards"] = [_interpolate(cards[i], profile) for i in shuffled]
        rendered["correct_order"] = shuffled

    else:
        rendered["say"] = _interpolate(node.get("say", ""), profile)
        opts = node.get("opts", [])
        rendered["opts"] = [
            {
                "t": _interpolate(opt.get("t", ""), profile),
                "to": opt.get("to", "done"),
                "code": opt.get("code"),
            }
            for opt in opts
        ]

    return rendered


def _interpolate(text: str, profile: Dict[str, Any]) -> str:
    if not isinstance(text, str):
        return text
    try:
        return text.format_map(_SafeDict(profile))
    except Exception:
        return text


class _SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def _make_session_id() -> str:
    return "tutor_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=12))


def _sanitize_session(session: Dict[str, Any]) -> Dict[str, Any]:
    if not session:
        return {}
    return {
        "session_id": session.get("session_id"),
        "user_id": session.get("user_id"),
        "atom_id": session.get("atom_id"),
        "tree_id": session.get("tree_id"),
        "current_node": session.get("current_node"),
        "history": session.get("history", []),
        "misconception_codes": session.get("misconception_codes", []),
        "teach_back_attempts": session.get("teach_back_attempts", 0),
    }
