import logging
import os
import re
import importlib.util
import sys
import contextlib
from typing import Optional, Any, List, Dict
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

_questions: list[dict] = []
_loaded = False


def _load_from_module(filepath: str, var_names: list[str]) -> list[dict]:
    """Import a Python data file and extract list variables."""
    results = []
    try:
        spec = importlib.util.spec_from_file_location("_qstore_mod", filepath)
        if not spec or not spec.loader:
            return results
        mod = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(None):
            spec.loader.exec_module(mod)
        for name in var_names:
            data = getattr(mod, name, None)
            if isinstance(data, list):
                results.extend(data)
            elif isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list):
                        results.extend(v)
    except Exception as e:
        logger.warning("Failed to load %s: %s", filepath, e)
    return results


def _assign_id(q: dict, idx: int) -> dict:
    """Ensure every question has a string id."""
    if "_id" in q:
        q["id"] = str(q.pop("_id"))
    elif "id" not in q:
        q["id"] = f"q_{idx:06d}"
    else:
        q["id"] = str(q["id"])

    if "company" in q and isinstance(q["company"], list):
        q["companies"] = q["company"]
    elif "company" in q and isinstance(q["company"], str):
        q["companies"] = [q["company"]]
    elif "companies" not in q:
        q["companies"] = []

    if "type" not in q:
        q["type"] = "coding"
    if "difficulty" not in q:
        q["difficulty"] = "medium"
    if "topic" not in q:
        q["topic"] = "General"
    if "sub_topic" not in q:
        q["sub_topic"] = ""
    if "frequency" not in q:
        q["frequency"] = 0
    if "hints" not in q:
        q["hints"] = []
    if "solution" not in q:
        q["solution"] = {}
    if "explanation" not in q:
        q["explanation"] = ""
    if "dsa_guide" not in q:
        q["dsa_guide"] = {"approach": "", "data_structures": [], "patterns": [], "tips": []}
    return q


def load_all():
    global _questions, _loaded
    if _loaded:
        return
    _questions = []
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    idx = 0

    # 1. seed_questions_mega.py
    mega_path = os.path.join(base, "seed_questions_mega.py")
    if os.path.exists(mega_path):
        items = _load_from_module(mega_path, ["questions"])
        for q in items:
            if isinstance(q, dict) and q.get("question"):
                _questions.append(_assign_id(dict(q), idx))
                idx += 1
        logger.info("Loaded %d from seed_questions_mega.py", len(items))

    # 2. seed_questions_v2.py
    v2_path = os.path.join(base, "seed_questions_v2.py")
    if os.path.exists(v2_path):
        items = _load_from_module(v2_path, ["questions"])
        for q in items:
            if isinstance(q, dict) and q.get("question"):
                _questions.append(_assign_id(dict(q), idx))
                idx += 1
        logger.info("Loaded %d from seed_questions_v2.py", len(items))

    # 3. seed_questions_2000.py
    s2k_path = os.path.join(base, "seed_questions_2000.py")
    if os.path.exists(s2k_path):
        items = _load_from_module(s2k_path, ["questions"])
        for q in items:
            if isinstance(q, dict) and q.get("question"):
                _questions.append(_assign_id(dict(q), idx))
                idx += 1
        logger.info("Loaded %d from seed_questions_2000.py", len(items))

    # 4. seed_questions.py (legacy)
    sq_path = os.path.join(base, "seed_questions.py")
    if os.path.exists(sq_path):
        items = _load_from_module(sq_path, ["questions"])
        for q in items:
            if isinstance(q, dict) and q.get("question"):
                _questions.append(_assign_id(dict(q), idx))
                idx += 1
        logger.info("Loaded %d from seed_questions.py", len(items))

    # 5. massive_questions.py (3400+ generated questions)
    massive_path = os.path.join(base, "massive_questions.py")
    if os.path.exists(massive_path):
        items = _load_from_module(massive_path, ["questions"])
        for q in items:
            if isinstance(q, dict):
                _questions.append(_assign_id(dict(q), idx))
                idx += 1
        logger.info("Loaded %d from massive_questions.py", len(items))

    _loaded = True
    logger.info("QuestionStore loaded %d questions total", len(_questions))


def _match(q: dict, query: dict) -> bool:
    for key, value in query.items():
        if key == "_id":
            if q.get("id") != str(value):
                return False
        elif key == "company":
            if isinstance(value, dict) and "$in" in value:
                q_companies = [c.lower() for c in q.get("companies", [])]
                if not any(v.lower() in q_companies for v in value["$in"]):
                    return False
            else:
                q_companies = [c.lower() for c in q.get("companies", [])]
                if value.lower() not in q_companies:
                    return False
        elif key == "$text":
            search = value.get("$search", "").lower()
            if search and search not in q.get("question", "").lower() and search not in q.get("explanation", "").lower():
                return False
        elif key == "type":
            qv = q.get("type", "")
            if isinstance(value, list):
                if qv not in value:
                    return False
            elif qv != value:
                return False
        elif key == "difficulty":
            qv = q.get("difficulty", "")
            if isinstance(value, dict) and "$in" in value:
                if qv not in value["$in"]:
                    return False
            elif qv != value:
                return False
        elif key == "topic":
            if isinstance(value, dict) and "$in" in value:
                if q.get("topic", "") not in value["$in"]:
                    return False
            elif q.get("topic", "") != value:
                return False
        elif key == "sub_topic":
            if q.get("sub_topic", "") != value:
                return False
        elif key == "role":
            q_roles = [r.lower() for r in q.get("role", [])] if isinstance(q.get("role"), list) else [str(q.get("role", "")).lower()]
            if isinstance(value, dict) and "$in" in value:
                if not any(v.lower() in q_roles for v in value["$in"]):
                    return False
            elif value.lower() not in q_roles:
                return False
        elif key == "_id" and "$nin" in value:
            val_id = q.get("id", "")
            if val_id in [str(v) for v in value["$nin"]]:
                return False
        else:
            if q.get(key) != value:
                return False
    return True


def count_documents(query: Optional[dict] = None) -> int:
    load_all()
    if not query:
        return len(_questions)
    return sum(1 for q in _questions if _match(q, query))


def find_one(query: dict) -> Optional[dict]:
    load_all()
    for q in _questions:
        if _match(q, query):
            return dict(q)
    return None


def find(query: Optional[dict] = None):
    load_all()
    return QuestionCursor(_questions, query)


def distinct(field: str) -> list:
    load_all()
    values = set()
    for q in _questions:
        val = q.get(field)
        if isinstance(val, list):
            for v in val:
                if v:
                    values.add(str(v).strip())
        elif val:
            values.add(str(val).strip())
    return sorted(values)


class QuestionCursor:
    def __init__(self, questions: list, query: Optional[dict] = None):
        self._all = [q for q in questions if _match(q, query)] if query else list(questions)
        self._skip_amount = 0
        self._limit_amount = None
        self._sort_spec = None

    def skip(self, n: int):
        self._skip_amount = n
        return self

    def limit(self, n: int):
        self._limit_amount = n
        return self

    def sort(self, sort_by):
        self._sort_spec = sort_by
        return self

    def to_list(self, length: Optional[int] = None) -> list[dict]:
        items = self._apply_sort()
        items = items[self._skip_amount:]
        if self._limit_amount:
            items = items[:self._limit_amount]
        if length is not None:
            items = items[:length]
        return [dict(q) for q in items]

    def __aiter__(self):
        return self._AsyncIterator(self)

    def _apply_sort(self):
        if not self._sort_spec:
            return self._all
        items = list(self._all)
        for key, direction in self._sort_spec:
            items.sort(key=lambda q, k=key: q.get(k, "") or "", reverse=(direction == -1))
        return items

    class _AsyncIterator:
        def __init__(self, cursor):
            self._items = cursor.to_list()
            self._idx = 0

        def __aiter__(self):
            return self

        async def __anext__(self):
            if self._idx >= len(self._items):
                raise StopAsyncIteration
            val = self._items[self._idx]
            self._idx += 1
            return val


def get_filters() -> dict:
    load_all()
    companies = set()
    roles = set()
    topics = set()
    sub_topics = set()
    types = set()
    difficulties = set()

    for q in _questions:
        for c in q.get("companies", []):
            if c:
                companies.add(c.strip())
        r = q.get("role", "")
        if isinstance(r, list):
            for rr in r:
                if rr:
                    roles.add(rr.strip())
        elif r:
            roles.add(r.strip())
        t = q.get("topic", "")
        if t:
            topics.add(t.strip())
        st = q.get("sub_topic", "")
        if st:
            sub_topics.add(st.strip())
        tp = q.get("type", "")
        if tp:
            types.add(tp.strip())
        d = q.get("difficulty", "")
        if d:
            difficulties.add(d.strip())

    return {
        "companies": sorted(companies),
        "roles": sorted(roles),
        "topics": sorted(topics),
        "sub_topics": sorted(sub_topics),
        "types": sorted(types),
        "difficulties": sorted(difficulties),
    }
