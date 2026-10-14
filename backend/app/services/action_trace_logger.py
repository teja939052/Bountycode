"""Action Trace Logger for interactions.

Logs granular learner actions to learning_events for diagnosis.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.database import learning_events_collection
from app.services.misconception_diagnosis import diagnose_misconception

logger = logging.getLogger(__name__)


def log_interaction_action(
    user_id: str,
    atom_id: str,
    session_id: str,
    interaction_type: str,
    action: str,
    data: Dict[str, Any],
    misconception_codes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Log a single interaction action and return diagnosis if available."""
    event = {
        "session_id": session_id,
        "user_id": user_id,
        "atom_id": atom_id,
        "interaction_type": interaction_type,
        "action": action,
        "data": data,
        "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    }
    
    try:
        learning_events_collection.insert_one(event)
    except Exception as exc:
        logger.debug("Failed to log interaction action: %s", exc)
    
    diagnosis = {
        "misconception_code": None,
        "confidence": 0.0,
        "evidence_count": 0,
        "reteach_route": None,
    }
    
    if misconception_codes and (action.endswith("_wrong") or action.endswith("_confused")):
        # Accumulate evidence from recent action trace for this user + concept
        recent_trace = _get_recent_trace(user_id, atom_id, session_id)
        recent_trace.append({"type": action, "data": data})
        
        diagnosis = diagnose_misconception(
            action_trace=recent_trace,
            concept=atom_id,
            misconception_codes=misconception_codes or [],
        )
    
    return diagnosis


def _get_recent_trace(user_id: str, atom_id: str, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch recent action trace entries for evidence accumulation."""
    try:
        from app.database import learning_events_collection
        cursor = learning_events_collection.find(
            {
                "user_id": user_id,
                "atom_id": atom_id,
                "session_id": session_id,
                "action": {"$regex": "_wrong$|_confused$"},
            }
        ).sort("timestamp", -1).limit(limit)
        
        trace = []
        for doc in cursor:
            trace.append({
                "type": doc.get("action", ""),
                "data": doc.get("data", {}),
            })
        return trace
    except Exception as exc:
        logger.debug("Failed to get recent trace: %s", exc)
        return []
