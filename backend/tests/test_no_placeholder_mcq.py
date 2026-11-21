"""Guard: no served MCQ may contain a placeholder option or a broken answer key.

Regression for: 80 "verified" aptitude/logical/verbal questions were served
with options "Option 1".."Option 4" and an answer key of "A" (all 80).
Needs no database: it reads the same in-memory store the API serves from.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services import question_store as qs  # noqa: E402

PLACEHOLDER = re.compile(r"Option [A-D0-9]+", re.IGNORECASE)
MCQ_TYPES = ("aptitude", "logical", "verbal", "cs_fundamentals")


@pytest.fixture(scope="module")
def served():
    qs.load_all()
    out = {}
    for t in MCQ_TYPES:
        out[t] = qs.find({"type": t}).only_verified().to_list(10000)
    return out


def _option_list(q):
    o = q.get("options")
    return list(o.values()) if isinstance(o, dict) else list(o or [])


@pytest.mark.parametrize("qtype", MCQ_TYPES)
def test_no_placeholder_options_served(served, qtype):
    bad = [q["id"] for q in served[qtype]
           if _option_list(q) and any(PLACEHOLDER.fullmatch(str(v).strip()) for v in _option_list(q))]
    assert not bad, f"{len(bad)} served {qtype} items have placeholder options: {bad[:10]}"


@pytest.mark.parametrize("qtype", ("aptitude", "logical", "verbal"))
def test_answer_key_matches_option_text(served, qtype):
    bad = []
    for q in served[qtype]:
        opts = [str(o).strip() for o in _option_list(q)]
        idx = q.get("correct_index")
        ok = (isinstance(idx, int) and 0 <= idx < len(opts)
              and opts[idx] == str(q.get("correct_answer")).strip())
        if not ok:
            bad.append(q["id"])
    assert not bad, f"{len(bad)} served {qtype} items have an answer key that does not match: {bad[:10]}"


@pytest.mark.parametrize("qtype", ("aptitude", "logical", "verbal"))
def test_answer_position_is_not_constant(served, qtype):
    positions = {q.get("correct_index") for q in served[qtype]}
    if len(served[qtype]) >= 10:
        assert len(positions) > 1, f"every served {qtype} answer sits at the same position"
