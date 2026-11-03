"""Deterministic scoring engine. Pure functions: normalize then score."""
import re
from typing import Any, Dict, Optional


def normalize_answer(raw: Any, qtype: str = "mcq") -> Optional[str]:
    if raw is None:
        return None
    if isinstance(raw, bool):
        return "true" if raw else "false"
    s = str(raw).strip()
    if s == "":
        return None
    if qtype in ("mcq", "output", "trace", "debug", "fix"):
        m = re.match(r"^[A-Za-z0-9_-]+$", s)
        if m:
            return s.upper() if len(s) == 1 and s.isalpha() else s
        return s
    if qtype == "numeric":
        try:
            return str(float(s))
        except ValueError:
            return None
    return s


def _correct(q: dict) -> Any:
    return q.get("correct_answer") or q.get("answer") or q.get("correct_index")


def score_question(q: dict, raw_answer: Any, time_spent: Optional[float] = None) -> Dict[str, Any]:
    qtype = (q.get("question_type") or q.get("type") or "mcq").lower()
    if qtype in ("output", "output_prediction"):
        qtype = "mcq"
    if qtype in ("trace", "tracing"):
        qtype = "trace"
    if qtype in ("debug", "find_bug", "find-the-bug"):
        qtype = "debug"
    if qtype in ("fix", "choose_fix", "choose-the-fix"):
        qtype = "fix"
    ua = normalize_answer(raw_answer, qtype)
    ca_raw = _correct(q)
    ca = normalize_answer(ca_raw, qtype)
    is_correct = False
    if ua is not None and ca is not None:
        if qtype in ("mcq", "trace", "debug", "fix"):
            is_correct = (ua == ca)
        elif qtype == "numeric":
            try:
                ua_f = float(ua)
                ca_f = float(ca)
                tol = q.get("tolerance")
                if tol is None:
                    is_correct = (ua_f == ca_f)
                else:
                    is_correct = abs(ua_f - ca_f) <= float(tol)
            except (ValueError, TypeError):
                is_correct = False
        elif qtype == "sequence":
            ua_seq = [x.strip().upper() for x in str(raw_answer).split(",") if x.strip()]
            ca_seq = [str(x).strip().upper() for x in (ca_raw if isinstance(ca_raw, list) else [ca_raw])]
            is_correct = (ua_seq == ca_seq)
        else:
            is_correct = (ua == ca)
    return {
        "question_id": q.get("id"),
        "pattern": q.get("topic") or q.get("pattern"),
        "difficulty": q.get("difficulty"),
        "question_type": qtype,
        "user_answer": raw_answer,
        "normalized_answer": ua,
        "correct_answer": ca_raw,
        "is_correct": bool(is_correct),
        "time_spent": time_spent,
    }
