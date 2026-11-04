"""Content service: serves structured learning content (lessons + practice)
for the Learn → Practice → Test loop.

Lessons are read from the curated JSON content files (backend/app/data/content/<subject>/<topic>.json).
Practice/test questions are served from question_store (trust_status=human_reviewed).
"""
import json
import logging
import os
from typing import Any, Dict, List, Optional

from app.services.question_store import find

logger = logging.getLogger(__name__)

_CONTENT_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "content")

_INDEX: Optional[Dict[str, Dict[str, Any]]] = None


def _index() -> Dict[str, Dict[str, Any]]:
    """Build topic → content-data index (cached)."""
    global _INDEX
    if _INDEX is not None:
        return _INDEX
    index: Dict[str, Dict[str, Any]] = {}
    if not os.path.isdir(_CONTENT_ROOT):
        _INDEX = index
        return index
    for root, _dirs, files in os.walk(_CONTENT_ROOT):
        for fname in sorted(files):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(root, fname)
            try:
                with open(path, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
            except Exception as e:
                logger.warning("Failed to read %s: %s", path, e)
                continue
            topic = data.get("topic") or os.path.splitext(fname)[0]
            index[topic] = data
    _INDEX = index
    return index


def list_topics() -> List[Dict[str, Any]]:
    """List all content topics with counts."""
    out: List[Dict[str, Any]] = []
    for topic, data in _index().items():
        practice = data.get("practice") or []
        questions = data.get("questions") or []
        lessons = data.get("lessons") or []
        out.append({
            "topic": topic,
            "subject": data.get("subject") or "general",
            "pattern": data.get("pattern") or topic,
            "lesson_count": len(lessons),
            "practice_count": len(practice),
            "question_count": len(questions),
            "trust_status": data.get("trust_status") or "human_reviewed",
        })
    out.sort(key=lambda x: x["topic"])
    return out


def get_topic_content(topic: str) -> Optional[Dict[str, Any]]:
    """Return lessons + practice questions for a topic."""
    data = _index().get(topic)
    if not data:
        # try case-insensitive / normalized match
        for key, d in _index().items():
            if key.lower() == topic.lower():
                data = d
                break
    if not data:
        return None
    subject = data.get("subject") or "general"
    pattern = data.get("pattern") or topic
    lessons = data.get("lessons") or []
    # Practice questions from question_store (verified MCQs)
    qs = list(find({"topic": topic, "trust_status": "human_reviewed", "question_type": "mcq"}).prefer_verified().to_list())
    practice = []
    for q in qs:
        practice.append({
            "id": q.get("id"),
            "question": q.get("question") or q.get("text"),
            "options": q.get("options"),
            "correct_answer": q.get("correct_answer") or q.get("answer"),
            "explanation": q.get("explanation"),
            "difficulty": q.get("difficulty"),
            "sub_topic": q.get("sub_topic"),
            "misconception_tags": q.get("misconception_tags") or [],
            "company_tags": q.get("company_tags") or [],
            "frequency_tier": q.get("frequency_tier") or 2,
        })
    return {
        "topic": topic,
        "subject": subject,
        "pattern": pattern,
        "lessons": lessons,
        "practice": practice,
        "trust_status": data.get("trust_status") or "human_reviewed",
    }
