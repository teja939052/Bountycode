from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
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
    cover_letters_used: int = 0
    monthly_reset_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)
