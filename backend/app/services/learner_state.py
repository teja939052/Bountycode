"""Canonical learner state service.

Unifies:
- skill_graph_collection (skill_assessment)
- srs_collection (spaced repetition)
- gamification_collection (diamonds, streak, level)
- learning_events (canonical evidence)
- repair_missions / user_weaknesses (closed-loop repair)
- concept_mastery (if present)

This is the single source of truth for the frontend personalization layer.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.database import (
    skill_graph_collection,
    srs_collection,
    gamification_collection,
    learning_events_collection,
    repair_missions_collection,
    user_weaknesses_collection,
)

logger = logging.getLogger(__name__)


async def get_learner_state(user_id: str) -> Dict[str, Any]:
    """Return the canonical learner state for personalization.

    Missing domains are omitted or returned as empty structures.
    No domain failure may break the whole payload.
    """
    state: Dict[str, Any] = {
        "id": user_id,
        "persona": None,
        "goal": None,
        "target_company": None,
        "target_role": None,
        "skills": {},
        "categories": {},
        "overall_score": 0.0,
        "weak_areas": [],
        "misconceptions": [],
        "srs": {
            "due_cards": 0,
            "total_cards": 0,
            "mastered_concepts": 0,
        },
        "gamification": {
            "level": 1,
            "diamonds": 0,
            "streak": 0,
            "last_practice_date": None,
        },
        "evidence": {
            "total_events": 0,
            "recent_event_count": 0,
            "last_event_at": None,
        },
        "repair": {
            "open_repairs": 0,
            "recent_repairs": [],
        },
        "readiness": {
            "overall": 0.0,
            "categories": {},
            "company": None,
        },
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    # Skill graph (authoritative for skills/categories/weak_areas/readiness)
    try:
        skill_graph = await skill_graph_collection.find_one({"user_id": user_id})
        if skill_graph:
            state["categories"] = _safe_dict(skill_graph.get("categories", {}))
            state["overall_score"] = float(skill_graph.get("overall_score", 0) or 0)
            state["readiness"]["overall"] = state["overall_score"]
            state["readiness"]["categories"] = {
                k: float((v or {}).get("score", 0) or 0)
                for k, v in state["categories"].items()
            }
            state["weak_areas"] = _derive_weak_areas(state["categories"])
    except Exception as exc:
        logger.warning("Failed to load skill graph for %s: %s", user_id, exc)

    # Gamification
    try:
        gdoc = await gamification_collection.find_one({"user_id": user_id})
        if gdoc:
            state["gamification"] = {
                "level": int(gdoc.get("level", 1) or 1),
                "diamonds": int(gdoc.get("diamonds", 0) or 0),
                "streak": int(gdoc.get("streak", 0) or 0),
                "last_practice_date": gdoc.get("last_practice_date"),
            }
    except Exception as exc:
        logger.warning("Failed to load gamification for %s: %s", user_id, exc)

    # SRS
    try:
        srs_cursor = srs_collection.find({"user_id": user_id})
        srs_docs = await srs_cursor.to_list(length=500)
        now = datetime.now(timezone.utc)
        due = 0
        mastered = 0
        for doc in srs_docs:
            nr = doc.get("next_review")
            if isinstance(nr, str):
                try:
                    nr_dt = datetime.fromisoformat(nr.replace("Z", "+00:00"))
                    if nr_dt <= now:
                        due += 1
                except Exception:
                    pass
            if doc.get("repetitions", 0) >= 4 and doc.get("lapses", 1) <= 1:
                mastered += 1
        state["srs"] = {
            "due_cards": due,
            "total_cards": len(srs_docs),
            "mastered_concepts": mastered,
        }
    except Exception as exc:
        logger.warning("Failed to load SRS for %s: %s", user_id, exc)

    # Learning events
    try:
        events_count = await learning_events_collection.count_documents({"user_id": user_id})
        recent_cursor = learning_events_collection.find(
            {"user_id": user_id, "created_at": {"$gte": _days_ago(7)}}
        ).limit(1)
        recent_docs = await recent_cursor.to_list(length=1)
        last_event = recent_docs[0].get("created_at") if recent_docs else None
        state["evidence"] = {
            "total_events": int(events_count or 0),
            "recent_event_count": 0,
            "last_event_at": _iso(last_event),
        }
    except Exception as exc:
        logger.warning("Failed to load learning events for %s: %s", user_id, exc)

    # Repair
    try:
        open_repairs = await repair_missions_collection.count_documents(
            {"user_id": user_id, "status": {"$nin": ["completed", "cancelled"]}}
        )
        recent_repairs_cursor = repair_missions_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(5)
        recent_repairs = await recent_repairs_cursor.to_list(length=5)
        state["repair"] = {
            "open_repairs": int(open_repairs or 0),
            "recent_repairs": [
                {
                    "id": str(r.get("_id")),
                    "concept": r.get("concept"),
                    "status": r.get("status"),
                    "created_at": _iso(r.get("created_at")),
                }
                for r in recent_repairs
            ],
        }
    except Exception as exc:
        logger.warning("Failed to load repair state for %s: %s", user_id, exc)

    # Weaknesses / misconceptions
    try:
        weakness_cursor = user_weaknesses_collection.find({"user_id": user_id}).limit(50)
        weaknesses = await weakness_cursor.to_list(length=50)
        state["misconceptions"] = [
            {
                "concept": w.get("concept"),
                "code": w.get("misconception_code"),
                "count": int(w.get("count", 0) or 0),
                "last_seen": _iso(w.get("last_seen")),
            }
            for w in weaknesses
        ]
    except Exception as exc:
        logger.warning("Failed to load weaknesses for %s: %s", user_id, exc)

    return state


def _safe_dict(value: Any) -> Dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    return value


def _derive_weak_areas(categories: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
    weak: List[Dict[str, Any]] = []
    for cat_id, cat_data in categories.items():
        if not isinstance(cat_data, dict):
            continue
        skills = cat_data.get("skills") or {}
        if not isinstance(skills, dict):
            continue
        for skill_name, skill_data in skills.items():
            if not isinstance(skill_data, dict):
                continue
            attempts = int(skill_data.get("attempts", 0) or 0)
            if attempts <= 0:
                continue
            score = float(skill_data.get("score", 0) or 0)
            weak.append({
                "category": cat_id,
                "category_name": cat_data.get("name", cat_id),
                "skill": skill_name,
                "score": score,
                "attempts": attempts,
            })
    weak.sort(key=lambda item: item.get("score", 0))
    return weak[:top_n]


def _days_ago(days: int) -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None) - __import__("datetime").timedelta(days=days)


def _iso(value: Any) -> Optional[str]:
    if not value:
        return None
    try:
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)
    except Exception:
        return None
