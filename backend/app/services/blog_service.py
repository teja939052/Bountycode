"""Blog / interview-question service.

Articles are curated, human-reviewed explanations (coddy.tech style): a short
answer, an optional runnable code snippet, and a ``related_topic`` that links
to the practice/exam content so readers can immediately drill the concept.
"""
import json
import logging
import os
from typing import Any, Dict, List, Optional

from app.services.content_loader import _CONTENT_ROOT

logger = logging.getLogger(__name__)

_BLOG_ROOT = os.path.join(_CONTENT_ROOT, "blogs")
_INDEX: Optional[Dict[str, Dict[str, Any]]] = None


def _index() -> Dict[str, Dict[str, Any]]:
    global _INDEX
    if _INDEX is not None:
        return _INDEX
    index: Dict[str, Dict[str, Any]] = {}
    if not os.path.isdir(_BLOG_ROOT):
        _INDEX = index
        return index
    for root, _dirs, files in os.walk(_BLOG_ROOT):
        for fname in sorted(files):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(root, fname)
            try:
                with open(path, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
            except Exception as e:
                logger.warning("Failed to read blog %s: %s", path, e)
                continue
            slug = data.get("slug") or os.path.splitext(fname)[0]
            index[slug] = data
    _INDEX = index
    return index


def list_blogs(tag: Optional[str] = None) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for slug, data in _index().items():
        if tag and tag not in (data.get("tags") or []):
            continue
        out.append({
            "slug": slug,
            "title": data.get("title"),
            "excerpt": data.get("excerpt"),
            "topic": data.get("topic"),
            "tags": data.get("tags") or [],
            "related_topic": data.get("related_topic"),
            "author": data.get("author") or "BountyCode Team",
            "updated_at": data.get("updated_at"),
        })
    out.sort(key=lambda x: (x["topic"] or "", x["title"] or ""))
    return out


def get_blog(slug: str) -> Optional[Dict[str, Any]]:
    data = _index().get(slug)
    if not data:
        return None
    return {
        "slug": slug,
        "title": data.get("title"),
        "excerpt": data.get("excerpt"),
        "body": data.get("body"),
        "code": data.get("code"),
        "language": data.get("language") or "python",
        "topic": data.get("topic"),
        "tags": data.get("tags") or [],
        "related_topic": data.get("related_topic"),
        "author": data.get("author") or "BountyCode Team",
        "updated_at": data.get("updated_at"),
        "trust_status": "human_reviewed",
    }
