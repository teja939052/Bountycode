"""Structured content loader.

Reads human-reviewed learning content from backend/app/data/content/<subject>/<topic>.json
and inserts each question into question_store via insert_question() (idempotent by id).
Content is tagged trust_status=human_reviewed so it passes the Content Trust Rule
and prefer_verified() filtering.

Content file schema:
{
  "topic": "percentages",
  "subject": "quantitative_aptitude",
  "pattern": "percentages",
  "lessons": [ {id, title, concept, formula, worked_example, mistakes[]} ],
  "practice": [ {id, question, options{}, correct_answer, explanation, difficulty, misconception_tags[]} ],
  "questions": [ {id, question, options{}, correct_answer, explanation, difficulty, misconception_tags[], company_tags[], frequency_tier} ]
}
"""
import json
import logging
import os
from typing import Any, Dict, List

from app.services.question_store import insert_question

logger = logging.getLogger(__name__)

_CONTENT_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "content")

_SEEN_IDS: set[str] = set()


def _load_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_content_file(path: str) -> Dict[str, int]:
    """Load one content JSON file into question_store. Returns counts."""
    data = _load_file(path)
    topic = data.get("topic") or os.path.splitext(os.path.basename(path))[0]
    subject = data.get("subject") or "general"
    pattern = data.get("pattern") or topic
    inserted = 0
    skipped = 0

    items: List[Dict[str, Any]] = []
    items.extend(data.get("practice") or [])
    items.extend(data.get("questions") or [])

    for item in items:
        qid = item.get("id")
        if not qid or qid in _SEEN_IDS:
            skipped += 1
            continue
        _SEEN_IDS.add(qid)
        doc = {
            "id": qid,
            "question": item.get("question") or item.get("text"),
            "options": item.get("options"),
            "correct_answer": item.get("correct_answer") or item.get("answer"),
            "explanation": item.get("explanation"),
            "difficulty": item.get("difficulty") or "medium",
            "topic": topic,
            "sub_topic": item.get("sub_topic") or topic,
            "pattern": pattern,
            "subject": subject,
            "question_type": item.get("question_type") or "mcq",
            "company_tags": item.get("company_tags") or [],
            "frequency_tier": item.get("frequency_tier") or 2,
            "misconception_tags": item.get("misconception_tags") or [],
            "trust_status": "human_reviewed",
            "source": item.get("source") or "bountycode_original",
            "type": "mcq",
        }
        insert_question(doc)
        inserted += 1

    logger.info("Content %s: inserted=%d skipped=%d", topic, inserted, skipped)
    return {"topic": topic, "inserted": inserted, "skipped": skipped}


def load_all_content() -> Dict[str, Any]:
    """Load every content JSON file under _CONTENT_ROOT."""
    results: List[Dict[str, int]] = []
    if not os.path.isdir(_CONTENT_ROOT):
        logger.warning("Content root missing: %s", _CONTENT_ROOT)
        return {"root": _CONTENT_ROOT, "files": 0, "results": results}
    for root, _dirs, files in os.walk(_CONTENT_ROOT):
        for fname in sorted(files):
            if not fname.endswith(".json"):
                continue
            results.append(load_content_file(os.path.join(root, fname)))
    return {"root": _CONTENT_ROOT, "files": len(results), "results": results}
