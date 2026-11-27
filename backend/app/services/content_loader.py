"""Content loader service — loads versioned content files for the question bank.

Question content lives in versioned files under app/data/content/, loaded into
memory at startup. Never written to MongoDB.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONTENT_ROOT = os.path.join(BACKEND_ROOT, "data", "content")


def load_question(id_: str) -> Optional[dict]:
    """Load a single question by ID from versioned files."""
    _CONTENT_ROOT_DIR = Path(_CONTENT_ROOT)
    for f in _CONTENT_ROOT_DIR.glob("*.json"):
        try:
            with open(f, "r") as fh:
                q = json.load(fh)
                if q.get("id") == id_:
                    return q
        except Exception:
            continue
    return None


def find_one(query: dict) -> Optional[dict]:
    """Find a single question by matching all query fields."""
    _CONTENT_ROOT_DIR = Path(_CONTENT_ROOT)
    for f in _CONTENT_ROOT_DIR.glob("*.json"):
        try:
            with open(f, "r") as fh:
                q = json.load(fh)
            if all(q.get(k) == v for k, v in query.items()):
                return q
        except Exception:
            continue
    return None


def find(query: dict, limit: int = 100) -> list:
    """Find questions matching query filters."""
    results = []
    _CONTENT_ROOT_DIR = Path(_CONTENT_ROOT)
    for f in _CONTENT_ROOT_DIR.glob("*.json"):
        try:
            with open(f, "r") as fh:
                q = json.load(fh)
            if all(q.get(k) == v for k, v in query.items()):
                results.append(q)
        except Exception:
            continue
    return results[:limit]


async def load_all_questions() -> list:
    """Load all questions from versioned files."""
    _CONTENT_ROOT_DIR = Path(_CONTENT_ROOT)
    questions = []
    for f in _CONTENT_ROOT_DIR.glob("*.json"):
        try:
            with open(f, "r") as fh:
                q = json.load(fh)
                questions.append(q)
        except Exception:
            continue
    return questions