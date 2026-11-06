"""Learner onboarding profile for the personalized Bountycode Academy.

The profile is learner-owned configuration, not a score or a placement guarantee.
Only authenticated users can read or update their own profile.
"""
from datetime import date, datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.middleware.auth import get_current_user
from app.database import get_collection

router = APIRouter(prefix="/api/v1/academy/profile", tags=["academy-profile"])
_profiles = lambda: get_collection("academy_learner_profiles")

ALLOWED_ROLES = {
    "software_engineer", "full_stack_developer", "backend_developer",
    "frontend_developer", "qa_engineer", "data_analyst", "devops_engineer",
    "support_engineer", "undecided",
}
ALLOWED_LEVELS = {"absolute_beginner", "beginner", "intermediate", "advanced"}
ALLOWED_LANGUAGES = {"c", "cpp", "java", "python", "javascript"}
ALLOWED_PREFERENCES = {"visual", "reading", "hands_on", "examples_first", "mixed"}


class LearnerProfileInput(BaseModel):
    target_role: str = "undecided"
    target_companies: List[str] = Field(default_factory=list, max_length=8)
    experience_level: str = "absolute_beginner"
    preferred_language: str = "cpp"
    daily_minutes: int = Field(default=60, ge=15, le=480)
    placement_date: Optional[date] = None
    learning_preference: str = "mixed"
    timezone: str = "Asia/Kolkata"

    @field_validator("target_role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_ROLES:
            raise ValueError("Choose a supported target role.")
        return value

    @field_validator("experience_level")
    @classmethod
    def validate_level(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_LEVELS:
            raise ValueError("Choose a supported experience level.")
        return value

    @field_validator("preferred_language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_LANGUAGES:
            raise ValueError("Choose a supported programming language.")
        return value

    @field_validator("learning_preference")
    @classmethod
    def validate_preference(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_PREFERENCES:
            raise ValueError("Choose a supported learning preference.")
        return value

    @field_validator("target_companies")
    @classmethod
    def normalize_companies(cls, values: List[str]) -> List[str]:
        normalized = []
        for item in values:
            company = item.strip().lower().replace(" ", "_")
            if not company or len(company) > 40:
                raise ValueError("Company identifiers must be 1–40 characters.")
            if company not in normalized:
                normalized.append(company)
        return normalized

    @field_validator("placement_date")
    @classmethod
    def validate_placement_date(cls, value: Optional[date]) -> Optional[date]:
        if value and value < date.today():
            raise ValueError("Placement date must be today or in the future.")
        return value


def _serialize(doc: Optional[dict]) -> dict:
    if not doc:
        return {"profile": None, "onboarding_complete": False}
    result = {key: value for key, value in doc.items() if key not in {"_id", "user_id"}}
    return {"profile": result, "onboarding_complete": bool(doc.get("onboarding_complete"))}


@router.get("")
async def get_learner_profile(user=Depends(get_current_user)):
    doc = await _profiles().find_one({"user_id": user["id"]})
    return {"success": True, "data": _serialize(doc)}


@router.put("")
async def save_learner_profile(payload: LearnerProfileInput, user=Depends(get_current_user)):
    now = datetime.now(timezone.utc).isoformat()
    profile = payload.model_dump(mode="json")
    profile.update({
        "user_id": user["id"],
        "onboarding_complete": True,
        "updated_at": now,
    })
    await _profiles().update_one(
        {"user_id": user["id"]},
        {"$set": profile, "$setOnInsert": {"created_at": now}},
        upsert=True,
    )
    return {"success": True, "data": _serialize(profile)}
