"""Structured, trust-preserving content loader.

Files under backend/app/data/content are authored artifacts, not automatically
human-reviewed simply because they are present in the repository. The loader
preserves trust only when the corresponding review/verification evidence is
present; otherwise items remain UNVERIFIED and cannot pass question_store's
student-serving gate.

Question content stays in versioned files and the in-memory question store.
This loader never writes question content to MongoDB.

For promotion evidence, a human review record must include reviewer,
reviewed_at and decision="approved". A trusted/verified item additionally
requires validation evidence with status="passed", method, checked_at and
evidence_id. These fields record an approval trail; they do not replace actual
human review or independent answer verification.

Content file schema:
{
  "topic": "percentages",
  "subject": "quantitative_aptitude",
  "pattern": "percentages",
  "trust_status": "unverified | automated_checked | human_reviewed | verified",
  "review_evidence": {"reviewer": "...", "reviewed_at": "...", "decision": "approved"},
  "verification_evidence": {"status": "passed", "method": "...", "checked_at": "...", "evidence_id": "..."},
  "practice": [ {id, question, options, correct_answer, explanation, difficulty} ],
  "questions": [ {id, question, options, correct_answer, explanation, difficulty} ]
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



def _evidence(record: Dict[str, Any], item: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = item.get(key) or record.get(key) or {}
    return value if isinstance(value, dict) else {}


def _has_human_review(record: Dict[str, Any], item: Dict[str, Any]) -> bool:
    evidence = _evidence(record, item, "review_evidence")
    return bool(
        str(evidence.get("reviewer") or "").strip()
        and str(evidence.get("reviewed_at") or "").strip()
        and str(evidence.get("decision") or "").strip().lower() == "approved"
    )


def _has_independent_validation(record: Dict[str, Any], item: Dict[str, Any]) -> bool:
    evidence = _evidence(record, item, "verification_evidence")
    return bool(
        str(evidence.get("status") or "").strip().lower() == "passed"
        and str(evidence.get("method") or "").strip()
        and str(evidence.get("checked_at") or "").strip()
        and str(evidence.get("evidence_id") or "").strip()
    )


def resolve_trust_status(record: Dict[str, Any], item: Dict[str, Any]) -> str:
    """Map an authored trust claim to the question_store status safely.

    Metadata-only labels are not evidence. In particular, the legacy value
    "human_reviewed" is not accepted without a reviewer and approved decision.
    "verified"/"trusted" additionally require a recorded independent validation.
    """
    raw = str(item.get("trust_status") or record.get("trust_status") or "unverified")
    status = raw.strip().lower().replace("-", "_")

    if status in {"reviewed", "human_reviewed"}:
        return "reviewed" if _has_human_review(record, item) else "unverified"

    if status in {"verified", "trusted"}:
        if _has_human_review(record, item) and _has_independent_validation(record, item):
            return "verified"
        return "unverified"

    if status == "automated_checked":
        return "automated_checked" if _has_independent_validation(record, item) else "unverified"

    if status in {"unverified", "needs_review", "quarantined"}:
        return status

    # Unknown labels are never interpreted as permission to serve.
    return "unverified"


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
        trust_status = resolve_trust_status(data, item)
        if trust_status not in {"verified", "reviewed"}:
            untrusted += 1
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
            "trust_status": trust_status,
            "source": item.get("source") or data.get("source") or "unspecified",
            "provenance": item.get("provenance") or data.get("provenance"),
            "review_evidence": _evidence(data, item, "review_evidence"),
            "verification_evidence": _evidence(data, item, "verification_evidence"),
            "type": "mcq",
        }
        insert_question(doc)
        inserted += 1

    logger.info("Content %s: inserted=%d skipped=%d", topic, inserted, skipped)
    return {"topic": topic, "inserted": inserted, "skipped": skipped, "untrusted": untrusted}


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
