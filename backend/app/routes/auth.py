from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status as http_status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
import secrets
import logging
import asyncio
import httpx
from app.services.email import send_email, welcome_email, password_reset_email
from app.models.user import UserCreate, UserLogin, UpdateProfileRequest, ChangePasswordRequest
from app.database import get_session, get_session_no_commit
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
from app.services.postgres_auth import PostgresAuthService
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
async def register(
    req: UserCreate,
    response: Response,
    request: Request = None,
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)

    existing = await auth_service.get_user_by_email(req.email)
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

    user, created = await auth_service.create_user(
        email=req.email,
        password_hash=hash_password(req.password),
        name=req.name,
        country=country,
        ip=client_ip,
    )
    user_id = str(user.id)

    # Fire-and-forget lifecycle email (must not block or fail the signup).
    try:
        asyncio.create_task(send_email(req.email, *welcome_email(req.name)))
    except Exception:
        pass

    token = create_access_token(user_id)
    refresh_token, refresh_jti = create_refresh_token(user_id)
    set_auth_cookie(response, token)
    set_auth_cookie(response, refresh_token, cookie_name="pp_refresh_token", max_age=settings.JWT_REFRESH_EXPIRY_DAYS * 86400)

    await auth_service.set_refresh_jti(user.id, refresh_jti)

    # Beta funnel: track signup completion
    try:
        from app.services.analytics_service import track_event
        asyncio.create_task(track_event(
            event="beta_signup_complete",
            path="/api/v1/auth/register",
            user_id=user_id,
            meta={"email": req.email, "name": req.name},
        ))
    except Exception:
        pass

    return {
        "token": token,
        "user": {"id": user_id, "email": req.email, "name": req.name, "plan": "free"},
    }


@router.post("/login")
async def login(
    req: UserLogin,
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)
    check_login_rate_limit(req.email)

    user = await auth_service.get_user_by_email(req.email)
    pw_hash = user.password_hash if user else None
    if not user or not pw_hash or not verify_password(req.password, pw_hash):
        record_login_failure(req.email)
        raise HTTPException(status_code=401, detail="Invalid email or password")

    try:
        clear_login_attempts(req.email)
        user_id = str(user.id)
        token = create_access_token(user_id)
        refresh_token, refresh_jti = create_refresh_token(user_id)
        set_auth_cookie(response, token)
        set_auth_cookie(response, refresh_token, cookie_name="pp_refresh_token", max_age=settings.JWT_REFRESH_EXPIRY_DAYS * 86400)
        await auth_service.set_refresh_jti(user.id, refresh_jti)
        await log_audit(user_id, "auth.login", "session", ip_address=(request.client.host if request.client else None))
    except Exception as e:
        logger.exception("login error: %s", repr(e))
        raise HTTPException(status_code=500, detail="Login session error. Contact support.")

    return {
        "token": token,
        "user": {
            "id": user_id,
            "email": user.email or "",
            "name": user.name or "",
            "plan": user.plan,
        },
    }


@router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)

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
        user = await auth_service.get_user_by_id(UUID(user_id))
        if not user or not user.refresh_jti or user.refresh_jti != jti:
            raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

        # Rotate: mint a new jti and invalidate the old one.
        new_access_token = create_access_token(user_id)
        new_refresh_token, new_jti = create_refresh_token(user_id)
        await auth_service.set_refresh_jti(user.id, new_jti)
        set_auth_cookie(response, new_access_token)
        set_auth_cookie(response, new_refresh_token, cookie_name="pp_refresh_token", max_age=settings.JWT_REFRESH_EXPIRY_DAYS * 86400)
        await log_audit(user_id, "auth.refresh", "session", ip_address=(request.client.host if request.client else None))
        return {"token": new_access_token}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
async def logout(
    response: Response,
    user=Depends(optional_get_current_user),
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)
    # Revoke the server-side refresh jti so a stolen refresh token can no
    # longer be rotated. Done best-effort: if there's no valid access token
    # we still clear the cookies client-side.
    if user:
        await auth_service.clear_refresh_jti(UUID(user["id"]))
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
        "diamonds": user.get("diamonds", 0),
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
}


@router.post("/update-profile")
async def update_profile(
    req: UpdateProfileRequest,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)
    updates = {}
    if req.name:
        updates["name"] = req.name
    if req.email:
        existing = await auth_service.get_user_by_email(req.email)
        if existing and str(existing.id) != user["id"]:
            raise HTTPException(status_code=400, detail="Email already in use")
        updates["email"] = req.email

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    await auth_service.update_user(UUID(user["id"]), updates)
    return {"message": "Profile updated", "updates": updates}


@router.post("/change-password")
async def change_password(
    req: ChangePasswordRequest,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)
    valid, msg = PasswordValidator.validate(req.new_password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    db_user = await auth_service.get_user_by_id(UUID(user["id"]))
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(req.current_password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    await auth_service.update_user(
        UUID(user["id"]),
        {
            "password_hash": hash_password(req.new_password),
            "refresh_jti": None,
        },
    )
    await log_audit(user["id"], "auth.change_password", "user")
    return {"message": "Password changed successfully", "relogin_required": True}


@router.post("/forgot-password")
async def forgot_password(
    req: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)

    user = await auth_service.get_user_by_email(req.email)
    if not user:
        return {"message": "If an account exists with this email, a reset link has been sent."}

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

    await auth_service.set_reset_token(user.id, token, expires_at)

    frontend_origin = settings.CORS_ORIGINS.split(",")[0].strip().rstrip("/")
    reset_link = f"{frontend_origin}/reset-password?token={token}&email={req.email}"

    subject, html = password_reset_email(user.name, reset_link)
    await send_email(req.email, subject, html)

    return {"message": "If an account exists with this email, a reset link has been sent."}


@router.post("/reset-password")
async def reset_password(
    req: ResetPasswordRequest,
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)

    user = await auth_service.get_user_by_email(req.email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")

    stored_token = user.reset_token
    expires_at = user.reset_token_expires

    if not stored_token or stored_token != req.token:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    if expires_at and datetime.now(timezone.utc) > expires_at.replace(tzinfo=timezone.utc):
        raise HTTPException(status_code=400, detail="Reset token has expired")

    if len(req.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    valid, msg = PasswordValidator.validate(req.new_password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    await auth_service.update_user(
        user.id,
        {
            "password_hash": hash_password(req.new_password),
            "reset_token": None,
            "reset_token_expires": None,
            "refresh_jti": None,
        },
    )
    await log_audit(str(user.id), "auth.reset_password", "user")

    return {"message": "Password reset successful. You can now log in."}


class OnboardingData(BaseModel):
    klass: Optional[str] = None
    target_companies: list = []
    skill_self_assessment: dict = {}
    career_goals: list[str] = []
    tech_interests: list[str] = []


@router.get("/onboarding-status")
async def onboarding_status(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session_no_commit),
):
    auth_service = PostgresAuthService(session)
    db_user = await auth_service.get_user_by_id(UUID(user["id"]))
    onboarding = db_user.onboarding if db_user else {}
    return {
        "completed": onboarding.get("completed", False),
        "class": onboarding.get("class"),
        "career_goals": onboarding.get("career_goals", []),
        "tech_interests": onboarding.get("tech_interests", []),
    }


@router.post("/onboarding-complete")
async def onboarding_complete(
    req: OnboardingData,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)
    onboarding = {
        "completed": True,
        "class": req.klass,
        "target_companies": req.target_companies,
        "skill_self_assessment": req.skill_self_assessment,
        "career_goals": req.career_goals,
        "tech_interests": req.tech_interests,
        "completed_at": datetime.now(timezone.utc),
    }
    await auth_service.update_onboarding(UUID(user["id"]), onboarding)

    # Beta funnel: track onboarding completion
    try:
        from app.services.analytics_service import track_event
        asyncio.create_task(track_event(
            event="beta_onboarding_complete",
            path="/api/v1/auth/onboarding-complete",
            user_id=user["id"],
            meta={"klass": req.klass, "target_companies": req.target_companies},
        ))
    except Exception:
        pass

    return {"status": "ok", "onboarding": onboarding}


@router.post("/verify-email")
async def verify_email(
    req: VerifyEmailRequest,
    session: AsyncSession = Depends(get_session),
):
    auth_service = PostgresAuthService(session)

    user = await auth_service.verify_email_token(req.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    await auth_service.mark_email_verified(user.id)
    return {"message": "Email verified successfully"}


@router.get("/google")
async def google_login():
    """Redirect user to Google OAuth consent page."""
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=501, detail="Google OAuth not configured")
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    scope = "openid email profile"
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope={scope}"
        "&access_type=offline"
        "&prompt=consent"
    )
    return RedirectResponse(url=auth_url)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Handle Google OAuth callback — exchange code, find/create user, set cookies, redirect."""
    auth_service = PostgresAuthService(session)
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=501, detail="Google OAuth not configured")
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    token_data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    }
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data=token_data,
            timeout=30,
        )
        token_resp.raise_for_status()
        token_info = token_resp.json()
    access_token = token_info.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    async with httpx.AsyncClient() as client:
        user_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        user_resp.raise_for_status()
        google_user = user_resp.json()
    google_email = google_user.get("email", "").lower()
    google_name = google_user.get("name", google_email.split("@")[0])
    if not google_email:
        raise HTTPException(status_code=400, detail="Google account has no email")

    existing = await auth_service.get_user_by_email(google_email)
    now = datetime.now(timezone.utc)
    if existing:
        user_id = str(existing.id)
        await auth_service.update_user(
            existing.id,
            {"last_active": now, "google_id": google_user.get("id")},
        )
    else:
        user, created = await auth_service.create_user(
            email=google_email,
            password_hash=None,
            name=google_name,
            google_id=google_user.get("id"),
            country="unknown",
            ip=None,
        )
        user_id = str(user.id)

    access_token_jwt = create_access_token(user_id)
    refresh_token, refresh_jti = create_refresh_token(user_id)
    set_auth_cookie(response, access_token_jwt)
    set_auth_cookie(response, refresh_token, cookie_name="pp_refresh_token", max_age=settings.JWT_REFRESH_EXPIRY_DAYS * 86400)
    await auth_service.set_refresh_jti(UUID(user_id), refresh_jti)
    frontend_origin = settings.CORS_ORIGINS.split(",")[0].strip()
    redirect = RedirectResponse(
        url=f"{frontend_origin}/?auth=success",
        status_code=http_status.HTTP_303_SEE_OTHER,
    )
    redirect.headers.__dict__["_list"] = response.headers.__dict__.get("_list", [])
    return redirect
