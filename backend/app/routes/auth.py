from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr
from typing import Optional
import secrets
import logging
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.services.email import send_email, welcome_email
from app.models.user import UserCreate, UserLogin, UpdateProfileRequest, ChangePasswordRequest
from app.database import users_collection
from app.middleware.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    optional_get_current_user,
    PasswordValidator,
    set_auth_cookie,
    clear_auth_cookie,
)
from app.services.audit_log import log_audit
from app.middleware.rate_limiter import (
    check_login_rate_limit,
    record_login_failure,
    clear_login_attempts,
)
from app.services.usage import check_and_reset_monthly_usage, get_usage_stats
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    token: str
    new_password: str


class VerifyEmailRequest(BaseModel):
    token: str


@router.post("/register")
async def register(req: UserCreate, response: Response, request: Request = None):
    existing = await users_collection.find_one({"email": req.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    valid, msg = PasswordValidator.validate(req.password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)
    # Best-effort geolocation for the admin dashboard (country breakdown).
    country = "unknown"
    client_ip = None
    if request is not None:
        country = (
            request.headers.get("CF-IPCountry")
            or request.headers.get("x-vercel-ip-country")
            or request.headers.get("X-Country")
            or "unknown"
        ).upper()
        client_ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            or (request.client.host if request.client else None)
        )

    now = datetime.now(timezone.utc)
    user_doc = {
        "email": req.email,
        "name": req.name,
        "password_hash": hash_password(req.password),
        "plan": "free",
        "country": country,
        "ip": client_ip,
        "paypal_customer_id": None,
        "email_verified": False,
        "email_verification_token": secrets.token_urlsafe(32),
        "email_verification_expires": now + timedelta(hours=24),
        "interviews_used": 0,
        "resumes_used": 0,
        "aptitude_used": 0,
        "cover_letters_used": 0,
        "monthly_reset_date": now,
        "created_at": now,
        "last_active": now,
    }

    result = await users_collection.insert_one(user_doc)
    user_id = str(result.inserted_id)

    # Fire-and-forget lifecycle email (must not block or fail the signup).
    try:
        asyncio.create_task(send_email(req.email, *welcome_email(req.name)))
    except Exception:
        pass

    token = create_access_token(user_id)
    refresh_token, refresh_jti = create_refresh_token(user_id)
    set_auth_cookie(response, token)
    set_auth_cookie(response, refresh_token, cookie_name="pp_refresh_token", max_age=settings.JWT_REFRESH_EXPIRY_DAYS * 86400)
    await users_collection.update_one(
        {"_id": result.inserted_id},
        {"$set": {"refresh_jti": refresh_jti}},
    )

    return {
        "token": token,
        "user": {"id": user_id, "email": req.email, "name": req.name, "plan": "free"},
    }


@router.post("/login")
async def login(req: UserLogin, response: Response, request: Request):
    check_login_rate_limit(req.email)

    user = await users_collection.find_one({"email": req.email})
    pw_hash = user.get("password_hash") if user else None
    if not user or not pw_hash or not verify_password(req.password, pw_hash):
        record_login_failure(req.email)
        raise HTTPException(status_code=401, detail="Invalid email or password")

    try:
        clear_login_attempts(req.email)
        user_id = str(user["_id"])
        token = create_access_token(user_id)
        refresh_token, refresh_jti = create_refresh_token(user_id)
        set_auth_cookie(response, token)
        set_auth_cookie(response, refresh_token, cookie_name="pp_refresh_token", max_age=settings.JWT_REFRESH_EXPIRY_DAYS * 86400)
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"refresh_jti": refresh_jti, "last_active": datetime.now(timezone.utc)}},
        )
        await log_audit(user_id, "auth.login", "session", ip_address=(request.client.host if request.client else None))
    except Exception as e:
        logger.exception("login error: %s", repr(e))
        raise HTTPException(status_code=500, detail="Login session error. Contact support.")

    return {
        "token": token,
        "user": {
            "id": user_id,
            "email": user.get("email") or "",
            "name": user.get("name") or "",
            "plan": user.get("plan", "free"),
        },
    }


@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    from bson import ObjectId

    refresh_token = request.cookies.get("pp_refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        jti = payload.get("jti")
        user_id = payload.get("user_id")
        if not jti or not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # The issued jti must match the server-tracked current refresh jti.
        # This makes stolen refresh tokens unusable once the user rotates them
        # (logout / password change / next refresh).
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user or not user.get("refresh_jti") or user["refresh_jti"] != jti:
            raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

        # Rotate: mint a new jti and invalidate the old one.
        new_access_token = create_access_token(user_id)
        new_refresh_token, new_jti = create_refresh_token(user_id)
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"refresh_jti": new_jti, "last_active": datetime.now(timezone.utc)}},
        )
        set_auth_cookie(response, new_access_token)
        set_auth_cookie(response, new_refresh_token, cookie_name="pp_refresh_token", max_age=settings.JWT_REFRESH_EXPIRY_DAYS * 86400)
        await log_audit(user_id, "auth.refresh", "session", ip_address=(request.client.host if request.client else None))
        return {"token": new_access_token}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
async def logout(response: Response, user=Depends(optional_get_current_user)):
    # Revoke the server-side refresh jti so a stolen refresh token can no
    # longer be rotated. Done best-effort: if there's no valid access token
    # we still clear the cookies client-side.
    if user:
        from bson import ObjectId as _ObjectId
        await users_collection.update_one(
            {"_id": _ObjectId(user["id"])},
            {"$unset": {"refresh_jti": ""}},
        )
        await log_audit(user["id"], "auth.logout", "session")

    clear_auth_cookie(response)
    response.delete_cookie(key="pp_refresh_token", path="/")
    return {"message": "Logged out"}


@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)
    usage = get_usage_stats(user)
    plan = user.get("plan", "free")
    # is_admin/role are now server-authoritative (owner emails only) via _finalize_user
    uid = user.get("id")
    if not uid:
        raise HTTPException(status_code=404, detail="User identity missing from token")
    return {
        "id": uid,
        "email": user.get("email") or "",
        "name": user.get("name") or "",
        "plan": plan,
        "usage": usage,
        "is_admin": user.get("is_admin", False),
        "role": user.get("role"),
    }


@router.get("/me/state")
async def get_user_state(user=Depends(get_current_user)):
    """Canonical aggregate student state for the Home screen.

    One request returns readiness, per-category scores, journey progress
    (DSA / CS / Interview / Resume rings), streak, level and the Next Best
    Action. Each piece is fetched independently and fails soft — a degraded
    analytics sub-service never breaks the Home screen (it just omits that field).
    """
    uid = user.get("id")
    if not uid:
        raise HTTPException(status_code=404, detail="User identity missing from token")

    plan = user.get("plan", "free")
    state = {
        "id": uid,
        "name": user.get("name") or "",
        "plan": plan,
        "level": user.get("level", 1),
        "xp": user.get("xp", 0),
        "streak": user.get("streak", 0),
        "readiness": None,
        "categories": {},
        "next_mission": None,
        "weak_areas": [],
    }

    # Readiness + per-category scores (async, fail-soft)
    try:
        from app.services.skill_assessment import get_readiness_score, get_weak_areas
        readiness = await get_readiness_score(uid)
        if readiness:
            state["readiness"] = readiness.get("overall")
            cats = {}
            for name, cat in (readiness.get("categories") or {}).items():
                try:
                    cats[name] = round(float(cat.get("score", 0)))
                except (TypeError, ValueError):
                    continue
            state["categories"] = cats

            # Derive a Next Best Action from the weakest available category
            cat_map = readiness.get("categories") or {}
            scored = []
            for name, cat in cat_map.items():
                try:
                    scored.append((name, float(cat.get("score", 0))))
                except (TypeError, ValueError):
                    continue
            if scored:
                scored.sort(key=lambda kv: kv[1])
                weakest = scored[0][0]
                state["next_mission"] = _MISSION_BY_CATEGORY.get(weakest)
    except Exception:
        pass

    # Weak areas (top 3)
    try:
        weak = await get_weak_areas(uid, top_n=3)
        if weak:
            state["weak_areas"] = [
                {"category": w.get("category_name") or w.get("category", ""),
                 "skill": w.get("skill", ""), "score": w.get("score", 0)}
                for w in weak
            ]
    except Exception:
        pass

    return state


_MISSION_BY_CATEGORY = {
    "dsa": {"label": "Solve a DSA problem", "to": "/problems", "minutes": 12},
    "cs_fundamentals": {"label": "CS Fundamentals drill", "to": "/coding", "minutes": 15},
    "interview": {"label": "Book a mock interview", "to": "/interview-booking", "minutes": 30},
    "resume": {"label": "Optimize your resume", "to": "/ats", "minutes": 10},
    "coding": {"label": "Solve a coding challenge", "to": "/coding", "minutes": 20},
    "aptitude": {"label": "Take an aptitude test", "to": "/aptitude", "minutes": 20},
    "projects": {"label": "Generate a project", "to": "/project-generator", "minutes": 25},
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

    valid, msg = PasswordValidator.validate(req.new_password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    db_user = await users_collection.find_one({"_id": ObjectId(user["id"])})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(req.current_password, db_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"password_hash": hash_password(req.new_password)},
         "$unset": {"refresh_jti": ""}},
    )
    await log_audit(user["id"], "auth.change_password", "user")
    return {"message": "Password changed successfully", "relogin_required": True}


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

    reset_link = f"{settings.CORS_ORIGINS.split(',')[0].strip()}/reset-password?token={token}&email={req.email}"
    
    if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:
        try:
            msg = MIMEMultipart()
            msg["From"] = settings.SMTP_FROM
            msg["To"] = req.email
            msg["Subject"] = "Reset your PlacementPro password"
            body = f"""Hi {user.get('name', '')},

Click the link below to reset your password. This link expires in 15 minutes.

{reset_link}

If you didn't request this, ignore this email.
"""
            msg.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            logger.error(f"Failed to send reset email: {e}")
    else:
        logger.warning(f"SMTP not configured. Reset link for {req.email}: {reset_link}")

    return {"message": "If an account exists with this email, a reset link has been sent."}


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

    if len(req.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    valid, msg = PasswordValidator.validate(req.new_password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"password_hash": hash_password(req.new_password)},
         "$unset": {"reset_token": "", "reset_token_expires": "", "refresh_jti": ""}},
    )
    await log_audit(str(user["_id"]), "auth.reset_password", "user")

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


@router.post("/verify-email")
async def verify_email(req: VerifyEmailRequest):
    user = await users_collection.find_one({"email_verification_token": req.token})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    expires_at = user.get("email_verification_expires")
    if expires_at and datetime.now(timezone.utc) > expires_at.replace(tzinfo=timezone.utc):
        raise HTTPException(status_code=400, detail="Verification token has expired")

    await users_collection.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {"email_verified": True, "email_verification_token": None, "email_verification_expires": None}},
    )
    return {"message": "Email verified successfully"}
