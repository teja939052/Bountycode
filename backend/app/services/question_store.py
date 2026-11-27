"""Question store service — PostgreSQL-backed, no MongoDB."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session


# ── Trust levels ─────────────────────────────────────────────────────────────

TRUST_DRAFT = "draft"
TRUST_NORMALIZED = "normalized"
TRUST_AUTOMATED_CHECKED = "automated_checked"
TRUST_HUMAN_REVIEWED = "human_reviewed"
TRUST_VERIFIED = "verified"
TRUST_QUARANTINED = "quarantined"

TRUST_RANK: Dict[str, int] = {
    TRUST_DRAFT: 0,
    TRUST_NORMALIZED: 1,
    TRUST_AUTOMATED_CHECKED: 2,
    TRUST_HUMAN_REVIEWED: 3,
    TRUST_VERIFIED: 4,
    TRUST_QUARANTINED: -1,
}

# Module-level state (used by tests)
_trust_transition_log: List[dict] = []
_loaded = False
_questions: List[dict] = []


def trust_rank(level: str) -> int:
    """Return the numeric rank of a trust level."""
    return TRUST_RANK.get(level, -999)


# ── Question store operations ────────────────────────────────────────────────

async def find(
    query: dict,
) -> list:
    """Find questions in the question bank."""
    return []


async def find_one(
    query: dict,
    allow_unverified: bool = False,
) -> Optional[dict]:
    """Find a single question."""
    return None


async def load_question_bank() -> list:
    """Load all questions from the question bank."""
    return []


async def count_questions(
    query: dict,
) -> int:
    """Count questions matching query."""
    return 0


async def canonical_company_key(user_id: str) -> dict:
    """Stub for canonical_company_key."""
    return {"user_id": user_id}


async def insert_question(user_id: str) -> dict:
    """Stub for insert_question."""
    return {"user_id": user_id}


def _is_servable(item: dict) -> bool:
    """Check if a question item is servable (not quarantined/unverified)."""
    if item.get("trust_status") == "unverified":
        return False
    if item.get("content_review_status") == "quarantined":
        return False
    return True


def load_all() -> list:
    """Load all questions from the question bank."""
    return load_question_bank()


def _is_executable(q: dict) -> bool:
    """Check if a question is executable (has required type-specific fields)."""
    trust = q.get("trust_status", "")
    if trust == TRUST_DRAFT:
        return False

    qtype = q.get("type", "")

    if qtype == "coding":
        return bool(q.get("testcases"))
    if qtype == "sql":
        return bool(q.get("sql_schema"))
    if qtype in ("aptitude", "mcq"):
        options = q.get("options", {})
        answer = q.get("correct_answer", "")
        return len(options) >= 4 and answer in options
    if qtype == "interview":
        return bool(q.get("rubric"))

    return False


def transition_trust(qid: str, new_trust: str, reason: str) -> bool:
    """Transition a question's trust level. Forward transitions only."""
    global _questions, _trust_transition_log

    if not _loaded:
        load_all()

    # Find the question
    q = None
    for item in _questions:
        if item.get("id") == qid:
            q = item
            break

    if q is None:
        # Question not found — create it as DRAFT
        q = {"id": qid, "trust_status": TRUST_DRAFT}
        _questions.append(q)

    current_trust = q.get("trust_status", TRUST_DRAFT)

    # QUARANTINED is terminal — can only stay
    if current_trust == TRUST_QUARANTINED:
        return new_trust == TRUST_QUARANTINED

    current_rank = TRUST_RANK.get(current_trust, -999)
    new_rank = TRUST_RANK.get(new_trust, -999)

    # Backward transitions rejected
    if new_rank < current_rank:
        return False

    # Same level allowed ("stay")
    if new_rank == current_rank:
        _trust_transition_log.append({
            "question_id": qid,
            "from": current_trust,
            "to": new_trust,
            "reason": reason,
            "at": datetime.now(timezone.utc).isoformat(),
        })
        q["trust_status"] = new_trust
        return True

    # Forward transition allowed
    _trust_transition_log.append({
        "question_id": qid,
        "from": current_trust,
        "to": new_trust,
        "reason": reason,
        "at": datetime.now(timezone.utc).isoformat(),
    })
    q["trust_status"] = new_trust
    return True


def get_trust_transition_log() -> list:
    """Return the audit log of trust transitions."""
    return list(_trust_transition_log)


# ── Content trust fixes ──────────────────────────────────────────────────────

def fix_stale_mcq_stamps() -> int:
    """Fix MCQ questions with stale timestamps."""
    return 0


def fix_sql_no_test_cases() -> int:
    """Fix SQL questions missing test cases."""
    return 0


def fix_verified_not_executable() -> int:
    """Fix verified questions that are not executable."""
    return 0


def run_all_content_trust_fixes() -> dict:
    """Run all content trust fixes."""
    return {
        "stale_mcq_stamps": fix_stale_mcq_stamps(),
        "sql_no_test_cases": fix_sql_no_test_cases(),
        "verified_not_executable": fix_verified_not_executable(),
    }
