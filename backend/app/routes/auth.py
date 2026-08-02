from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr
from typing import Optional
import secrets
import logging
from app.models.user import UserCreate, UserLogin, UpdateProfileRequest, ChangePasswordRequest
from app.database import users_collection
from app.middleware.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    set_auth_cookie,
    clear_auth_cookie,
)
from app.middleware.rate_limiter import (
    check_login_rate_limit,
    record_login_failure,
    clear_login_attempts,
)
from app.services.usage import check_and_reset_monthly_usage, get_usage_stats

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    token: str
    new_password: str


@router.post("/register")
async def register(req: UserCreate, response: Response):
    existing = await users_collection.find_one({"email": req.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    now = datetime.now(timezone.utc)
    user_doc = {
        "email": req.email,
        "name": req.name,
        "password_hash": hash_password(req.password),
        "plan": "free",
        "paypal_customer_id": None,
        "interviews_used": 0,
        "resumes_used": 0,
        "aptitude_used": 0,
        "cover_letters_used": 0,
        "monthly_reset_date": now,
        "created_at": now,
    }

    result = await users_collection.insert_one(user_doc)
    user_id = str(result.inserted_id)
    token = create_access_token(user_id)
    set_auth_cookie(response, token)

    return {
        "token": token,
        "user": {"id": user_id, "email": req.email, "name": req.name, "plan": "free"},
    }


@router.post("/login")
async def login(req: UserLogin, response: Response):
    check_login_rate_limit(req.email)

    user = await users_collection.find_one({"email": req.email})
    if not user or not verify_password(req.password, user["password_hash"]):
        record_login_failure(req.email)
        raise HTTPException(status_code=401, detail="Invalid email or password")

    clear_login_attempts(req.email)
    user_id = str(user["_id"])
    token = create_access_token(user_id)
    set_auth_cookie(response, token)

    return {
        "token": token,
        "user": {
            "id": user_id,
            "email": user["email"],
            "name": user["name"],
            "plan": user.get("plan", "free"),
        },
    }


@router.post("/logout")
async def logout(response: Response):
    clear_auth_cookie(response)
    return {"message": "Logged out"}


@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)
    usage = get_usage_stats(user)
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "plan": user.get("plan", "free"),
        "usage": usage,
    }


@router.post("/update-profile")
async def update_profile(req: UpdateProfileRequest, user=Depends(get_current_user)):
    from bson import ObjectId

    updates = {}
    if req.name:
        updates["name"] = req.name
    if req.email:
        existing = await users_collection.find_one({"email": req.email, "_id": {"$ne": ObjectId(user["id"])}})
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        updates["email"] = req.email

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    await users_collection.update_one({"_id": ObjectId(user["id"])}, {"$set": updates})
    return {"message": "Profile updated", "updates": updates}


@router.post("/change-password")
async def change_password(req: ChangePasswordRequest, user=Depends(get_current_user)):
    from bson import ObjectId

    db_user = await users_collection.find_one({"_id": ObjectId(user["id"])})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(req.current_password, db_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"password_hash": hash_password(req.new_password)}}
    )
    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest):
    user = await users_collection.find_one({"email": req.email})
    if not user:
        return {"message": "If an account exists with this email, a reset token has been generated."}

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"reset_token": token, "reset_token_expires": expires_at}},
    )

    logger.info(f"Password reset token for {req.email}: {token}")

    return {"message": "If an account exists with this email, a reset token has been generated."}


@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest):
    user = await users_collection.find_one({"email": req.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")

    stored_token = user.get("reset_token")
    expires_at = user.get("reset_token_expires")

    if not stored_token or stored_token != req.token:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    if expires_at and datetime.now(timezone.utc) > expires_at.replace(tzinfo=timezone.utc):
        raise HTTPException(status_code=400, detail="Reset token has expired")

    if len(req.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"password_hash": hash_password(req.new_password)}, "$unset": {"reset_token": "", "reset_token_expires": ""}},
    )

    return {"message": "Password reset successful. You can now log in."}


class OnboardingData(BaseModel):
    klass: Optional[str] = None
    target_companies: list = []
    skill_self_assessment: dict = {}


@router.get("/onboarding-status")
async def onboarding_status(user=Depends(get_current_user)):
    from bson import ObjectId
    db_user = await users_collection.find_one({"_id": ObjectId(user["id"])})
    onboarding = db_user.get("onboarding", {}) if db_user else {}
    return {
        "completed": onboarding.get("completed", False),
        "class": onboarding.get("class"),
    }


@router.post("/onboarding-complete")
async def onboarding_complete(req: OnboardingData, user=Depends(get_current_user)):
    from bson import ObjectId
    onboarding = {
        "completed": True,
        "class": req.klass,
        "target_companies": req.target_companies,
        "skill_self_assessment": req.skill_self_assessment,
        "completed_at": datetime.now(timezone.utc),
    }
    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"onboarding": onboarding}}
    )
    return {"status": "ok", "onboarding": onboarding}
