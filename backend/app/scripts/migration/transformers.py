"""Domain-specific transformers — MongoDB document → PostgreSQL-ready dict.

Each transformer:
- Converts ObjectIds to strings (deferred to identity mapping for UUIDs)
- Converts datetimes to Python datetime objects (timezone-aware)
- Handles missing and nullable fields
- Converts enumerated values to canonical strings
- Handles JSONB structures
- Preserves original timestamps where valid
- Returns (transformed_dict, quarantine_reason) — quarantine_reason is None if valid
"""

import logging
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID, uuid4

from bson import ObjectId

logger = logging.getLogger(__name__)


def _to_iso(val: Any) -> Optional[str]:
    if val is None:
        return None
    if isinstance(val, datetime):
        if val.tzinfo is None:
            val = val.replace(tzinfo=timezone.utc)
        return val.isoformat()
    if isinstance(val, str):
        return val
    return None


def _to_datetime(val: Any) -> Optional[datetime]:
    if val is None:
        return None
    if isinstance(val, datetime):
        if val.tzinfo is None:
            return val.replace(tzinfo=timezone.utc)
        return val
    if isinstance(val, str):
        try:
            return datetime.fromisoformat(val).replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


def _to_str(val: Any) -> Optional[str]:
    if val is None:
        return None
    if isinstance(val, ObjectId):
        return str(val)
    return str(val)


def _to_bool(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes", "on")
    return bool(val)


def _to_int(val: Any, default: int = 0) -> int:
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


def _to_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def _to_list(val: Any, default: Optional[list] = None) -> list:
    if val is None:
        return default if default is not None else []
    if isinstance(val, list):
        return val
    return [val]


def _to_dict(val: Any, default: Optional[dict] = None) -> dict:
    if val is None:
        return default if default is not None else {}
    if isinstance(val, dict):
        return val
    return {}


def transform_user(doc: dict) -> tuple[dict, Optional[str]]:
    reasons: list[str] = []
    email = doc.get("email")
    if not email:
        reasons.append("missing email")
    password_hash = doc.get("password_hash")
    if not password_hash:
        reasons.append("missing password_hash")
    name = doc.get("name") or doc.get("full_name") or "Unknown"
    if reasons:
        return {}, "; ".join(reasons)
    data: dict = {
        "email": email.lower().strip(),
        "password_hash": password_hash,
        "name": name,
        "plan": doc.get("plan", "free"),
        "paypal_customer_id": doc.get("paypal_customer_id"),
        "paypal_order_id": doc.get("paypal_order_id"),
        "plan_pending": doc.get("plan_pending"),
        "interviews_used": _to_int(doc.get("interviews_used"), 0),
        "resumes_used": _to_int(doc.get("resumes_used"), 0),
        "aptitude_used": _to_int(doc.get("aptitude_used"), 0),
        "mock_interviews_used": _to_int(doc.get("mock_interviews_used"), 0),
        "monthly_reset_date": _to_datetime(doc.get("monthly_reset_date")),
        "daily_usage": _to_dict(doc.get("daily_usage")),
        "all_time_usage": _to_dict(doc.get("all_time_usage")),
        "honor": _to_int(doc.get("honor"), 0),
        "uid": doc.get("uid"),
        "created_at": _to_datetime(doc.get("created_at")),
        "updated_at": _to_datetime(doc.get("updated_at")),
    }
    return data, None


def transform_gamification_profile(doc: dict) -> tuple[dict, Optional[str]]:
    reasons: list[str] = []
    user_id = doc.get("user_id")
    if not user_id:
        reasons.append("missing user_id")
    if reasons:
        return {}, "; ".join(reasons)
    return {
        "user_id": _to_str(user_id),
        "xp": _to_int(doc.get("xp"), 0),
        "level": _to_int(doc.get("level"), 1),
        "streak": _to_int(doc.get("streak"), 0),
        "combo": _to_int(doc.get("combo"), 0),
        "coins": _to_int(doc.get("coins"), 0),
        "stars": _to_int(doc.get("stars"), 0),
        "badges": _to_list(doc.get("badges")),
        "bosses_defeated": _to_list(doc.get("bosses_defeated")),
        "weekly_xp": _to_int(doc.get("weekly_xp"), 0),
        "monthly_xp": _to_int(doc.get("monthly_xp"), 0),
        "last_practice_date": _to_datetime(doc.get("last_practice_date")),
        "created_at": _to_datetime(doc.get("created_at")),
        "updated_at": _to_datetime(doc.get("updated_at")),
    }, None


def transform_xp_event(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    return {
        "user_id": _to_str(user_id),
        "activity_type": doc.get("activity_type", "unknown"),
        "score": _to_float(doc.get("score"), 0.0),
        "xp_awarded": _to_int(doc.get("xp_awarded"), 0),
        "diamonds_awarded": _to_int(doc.get("diamonds_awarded"), 0),
        "event_metadata": _to_dict(doc.get("metadata")),
        "reward_policy_version": doc.get("reward_policy_version", "2026.1"),
        "created_at": _to_datetime(doc.get("created_at")),
    }, None


def transform_skill(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    skill_name = doc.get("name") or doc.get("skill_name")
    if not skill_name:
        return {}, "missing skill name"
    return {
        "user_id": _to_str(user_id),
        "name": skill_name,
        "topic": doc.get("topic", "general"),
        "sub_topic": doc.get("sub_topic"),
        "difficulty": doc.get("difficulty", "medium"),
        "prerequisites": _to_list(doc.get("prerequisites")),
        "content_version": doc.get("content_version", "v1.0"),
        "is_active": _to_bool(doc.get("is_active", True)),
        "mastery_level": _to_int(doc.get("mastery_level"), 0),
        "xp": _to_int(doc.get("xp"), 0),
        "created_at": _to_datetime(doc.get("created_at")),
        "updated_at": _to_datetime(doc.get("updated_at")),
    }, None


def transform_learning_attempt(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    return {
        "user_id": _to_str(user_id),
        "skill_id": doc.get("skill_id"),
        "question_id": doc.get("question_id", ""),
        "activity_type": doc.get("activity_type", "practice"),
        "score": _to_int(doc.get("score"), 0),
        "evidence_type": doc.get("evidence_type", "independent"),
        "passed": _to_bool(doc.get("passed", False)),
        "passing_score": _to_int(doc.get("passing_score"), 7),
        "max_attempts": _to_int(doc.get("max_attempts"), 3),
        "attempt_number": _to_int(doc.get("attempt_number"), 1),
        "idempotency_key": doc.get("idempotency_key"),
        "attempt_metadata": _to_dict(doc.get("metadata")),
        "created_at": _to_datetime(doc.get("created_at")),
    }, None


def transform_coding_submission(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    question_id = doc.get("question_id") or doc.get("challenge_id")
    if not question_id:
        return {}, "missing question_id"
    execution_result = _to_dict(doc.get("execution_result"))
    protected_keys = {"expected", "hidden_tests", "test_cases", "answer_key"}
    for key in protected_keys:
        execution_result.pop(key, None)
    return {
        "user_id": _to_str(user_id),
        "question_id": _to_str(question_id),
        "code": doc.get("code", ""),
        "language": doc.get("language", "python"),
        "status": doc.get("status", "pending"),
        "score": _to_float(doc.get("score")),
        "execution_result": execution_result,
        "idempotency_key": doc.get("idempotency_key"),
        "submitted_at": _to_datetime(doc.get("submitted_at")) or _to_datetime(doc.get("created_at")),
    }, None


def transform_assessment_attempt(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    assessment_id = doc.get("assessment_id") or doc.get("test_id")
    if not assessment_id:
        return {}, "missing assessment_id"
    return {
        "user_id": _to_str(user_id),
        "assessment_id": _to_str(assessment_id),
        "variant_id": doc.get("variant_id"),
        "score": _to_float(doc.get("score")),
        "status": doc.get("status", "in_progress"),
        "idempotency_key": doc.get("idempotency_key"),
        "started_at": _to_datetime(doc.get("started_at")),
        "completed_at": _to_datetime(doc.get("completed_at")),
    }, None


def transform_oa_session(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    return {
        "user_id": _to_str(user_id),
        "company": doc.get("company", ""),
        "role": doc.get("role", ""),
        "blueprint": _to_dict(doc.get("blueprint")),
        "mode": doc.get("mode", "calm"),
        "integrity_enabled": _to_bool(doc.get("integrity_enabled", False)),
        "status": doc.get("status", "in_progress"),
        "questions": _to_list(doc.get("questions")),
        "idempotency_key": doc.get("idempotency_key"),
        "started_at": _to_datetime(doc.get("started_at")),
        "completed_at": _to_datetime(doc.get("completed_at")),
    }, None


def transform_interview_session(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    questions = _to_list(doc.get("questions"))
    for q in questions:
        if isinstance(q, dict):
            q.pop("api_key", None)
            q.pop("provider_secret", None)
    return {
        "user_id": _to_str(user_id),
        "interview_type": doc.get("interview_type", "technical"),
        "company": doc.get("company"),
        "role": doc.get("role"),
        "difficulty": doc.get("difficulty", "medium"),
        "status": doc.get("status", "in_progress"),
        "score": _to_float(doc.get("score")),
        "questions": questions,
        "idempotency_key": doc.get("idempotency_key"),
        "started_at": _to_datetime(doc.get("started_at")),
        "completed_at": _to_datetime(doc.get("completed_at")),
    }, None


def transform_career_profile(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    return {
        "user_id": _to_str(user_id),
        "bio": doc.get("bio"),
        "skills": _to_list(doc.get("skills")),
        "experience": doc.get("experience"),
        "portfolio_urls": _to_list(doc.get("portfolio_urls")),
        "github_username": doc.get("github_username"),
        "leetcode_username": doc.get("leetcode_username"),
        "target_company": doc.get("target_company"),
        "target_role": doc.get("target_role"),
        "created_at": _to_datetime(doc.get("created_at")),
        "updated_at": _to_datetime(doc.get("updated_at")),
    }, None


def transform_resume(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    return {
        "user_id": _to_str(user_id),
        "original_filename": doc.get("original_filename") or doc.get("filename"),
        "file_path": doc.get("file_path") or doc.get("storage_url"),
        "file_size_bytes": _to_int(doc.get("file_size_bytes"), 0),
        "content_type": doc.get("content_type", "application/pdf"),
        "analysis": _to_dict(doc.get("analysis")),
        "ats_score": _to_float(doc.get("ats_score")),
        "created_at": _to_datetime(doc.get("created_at")),
        "updated_at": _to_datetime(doc.get("updated_at")),
    }, None


def transform_payment(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    return {
        "user_id": _to_str(user_id),
        "amount": _to_float(doc.get("amount"), 0.0),
        "currency": doc.get("currency", "USD"),
        "status": doc.get("status", "pending"),
        "transaction_id": doc.get("transaction_id") or doc.get("payment_id"),
        "paypal_order_id": doc.get("paypal_order_id"),
        "created_at": _to_datetime(doc.get("created_at")),
        "updated_at": _to_datetime(doc.get("updated_at")),
    }, None


def transform_analytics_event(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    if not user_id:
        return {}, "missing user_id"
    return {
        "user_id": _to_str(user_id),
        "event_type": doc.get("event_type", "unknown"),
        "event_data": _to_dict(doc.get("event_data")),
        "created_at": _to_datetime(doc.get("created_at")),
    }, None


def transform_audit_log(doc: dict) -> tuple[dict, Optional[str]]:
    user_id = doc.get("user_id")
    return {
        "user_id": _to_str(user_id),
        "action": doc.get("action", "unknown"),
        "resource": doc.get("resource", "unknown"),
        "timestamp": _to_datetime(doc.get("timestamp")) or _to_datetime(doc.get("created_at")),
        "metadata": _to_dict(doc.get("metadata")),
    }, None


TRANSFORMERS = {
    "users": transform_user,
    "gamification": transform_gamification_profile,
    "gamification_events": transform_xp_event,
    "skill_graphs": transform_skill,
    "learning_events": transform_learning_attempt,
    "coding_challenges": transform_coding_submission,
    "submissions": transform_coding_submission,
    "aptitude_tests": transform_assessment_attempt,
    "company_mock_tests": transform_assessment_attempt,
    "oa_sessions": transform_oa_session,
    "interviews": transform_interview_session,
    "interview_bookings": lambda d: (
        {
            "user_id": _to_str(d.get("user_id")),
            "company": d.get("company", ""),
            "role": d.get("role", ""),
            "interview_type": d.get("interview_type", "technical"),
            "scheduled_at": _to_datetime(d.get("scheduled_at")),
            "status": d.get("status", "scheduled"),
            "created_at": _to_datetime(d.get("created_at")),
        },
        None if d.get("user_id") else "missing user_id",
    ),
    "interview_chat_sessions": transform_interview_session,
    "career_profiles": transform_career_profile,
    "resumes": transform_resume,
    "payments": transform_payment,
    "repair_missions": transform_interview_session,
    "srs_cards": transform_skill,
    "analytics_events": transform_analytics_event,
    "analytics_rollups": lambda d: (
        {
            "rollup_key": d.get("rollup_key", "unknown"),
            "metrics": _to_dict(d.get("metrics")),
            "period_start": _to_datetime(d.get("period_start")),
            "period_end": _to_datetime(d.get("period_end")),
            "created_at": _to_datetime(d.get("created_at")),
        },
        None if d.get("rollup_key") else "missing rollup_key",
    ),
    "audit_logs": transform_audit_log,
    "coupons": lambda d: (
        {
            "code": d.get("code", ""),
            "discount_type": d.get("discount_type", "percentage"),
            "value": _to_float(d.get("value"), 0.0),
            "valid_until": _to_datetime(d.get("valid_until")),
            "usage_limit": _to_int(d.get("usage_limit")),
            "usage_count": _to_int(d.get("usage_count"), 0),
            "is_active": _to_bool(d.get("is_active", True)),
            "created_at": _to_datetime(d.get("created_at")),
        },
        None if d.get("code") else "missing code",
    ),
}
