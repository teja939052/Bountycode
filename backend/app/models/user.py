from pydantic import BaseModel, EmailStr, Field, field_serializer
from typing import Optional
from datetime import datetime

from app.utils.timeutil import utcnow


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    plan: str


class UserInDB(BaseModel):
    email: str
    name: str
    password_hash: str
    plan: str = "free"
    paypal_customer_id: Optional[str] = None
    paypal_order_id: Optional[str] = None
    plan_pending: Optional[str] = None
    interviews_used: int = 0
    resumes_used: int = 0
    aptitude_used: int = 0
    mock_interviews_used: int = 0
    monthly_reset_date: Optional[datetime] = None
    daily_usage: dict = {}
    all_time_usage: dict = {}
    created_at: datetime = Field(default_factory=utcnow)

    @field_serializer("created_at")
    def _serialize_created_at(self, v: datetime) -> str:
        return v.isoformat() if v else None


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class UserTier(BaseModel):
    """Lightweight tier + quota tracking model for content paywall gating.

    Injected into routes that serve premium content (compiler, question bank,
    mock interviews) to enforce free-tier limits and intercept upgrades.
    """
    tier_name: str = "free"
    valid_until: Optional[datetime] = None
    interview_tokens: int = 0
    compilation_limit_today: int = 5
    last_compilation_reset: datetime = Field(default_factory=utcnow)
    question_bank_limit: int = 5
    interviews_limit: int = 3
    daily_reset_date: Optional[datetime] = None
