"""Authentication middleware and utilities for PlacementPro.

Provides JWT-based authentication with httpOnly cookies, password hashing,
WebSocket auth, and plan-based access control dependencies.
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import WebSocket
from app.config import get_settings
from app.database import users_collection
from app.services.cache import cache
from bson import ObjectId
import re
import secrets

logger = logging.getLogger(__name__)
settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)
COOKIE_NAME = "pp_token"
USER_CACHE_TTL = 300


def _admin_emails() -> set:
    """Return the set of owner/admin email addresses from config.

    Parses the comma-separated ADMIN_EMAILS environment variable and returns
    a normalized set of lowercase email strings.

    Returns:
        set: Lowercased, stripped admin email addresses.
    """
    emails = settings.ADMIN_EMAILS or ""
    return {e.strip().lower() for e in emails.split(",") if e.strip()}


def _finalize_user(user: Dict[str, Any]) -> Dict[str, Any]:
    """Strip sensitive fields and compute server-authoritative role/is_admin.

    Admin status is derived ONLY from ADMIN_EMAILS (the owner). Subscription
    plan never grants admin rights — so Pro/Lifetime customers cannot escalate
    to admin. Role/is_admin is recomputed on every request (never cached).

    Args:
        user: Raw user document from MongoDB.

    Returns:
        Dict[str, Any]: Sanitized user dict with 'id', 'is_admin', and 'role' fields.
    """
    user["id"] = str(user["_id"])
    if "password_hash" in user:
        user["password_hash"] = None
    is_admin = user.get("email", "").lower() in _admin_emails()
    user["is_admin"] = is_admin
    user["role"] = "admin" if is_admin else None
    return user


class PasswordValidator:
    """Password strength validation against configured security policies."""

    @staticmethod
    def validate(password: str) -> tuple[bool, str]:
        """Validate a password against configured security rules.

        Checks minimum length, required numbers, and required special characters
        based on Settings.

        Args:
            password: Plain-text password to validate.

        Returns:
            tuple[bool, str]: (is_valid, message) where message describes the result.
        """
        if len(password) < settings.PASSWORD_MIN_LENGTH:
            return False, f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long"
        
        if settings.PASSWORD_REQUIRE_NUMBER and not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        
        if settings.PASSWORD_REQUIRE_SPECIAL and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is valid"


import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain-text password (truncated to 72 bytes for bcrypt).

    Returns:
        str: Bcrypt-hashed password string.
    """
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash.

    Args:
        plain_password: User-provided plain-text password.
        hashed_password: Stored bcrypt hash.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    pwd_bytes = plain_password.encode('utf-8')[:72]
    hash_bytes = hashed_password.encode('utf-8')
    try:
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        return False


def create_access_token(user_id: str) -> str:
    """Create a short-lived JWT access token.

    Args:
        user_id: MongoDB user ID to embed in the token payload.

    Returns:
        str: Encoded JWT access token string.
    """
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_EXPIRY_DAYS)
    payload = {
        "user_id": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> tuple:
    """Create a rotating JWT refresh token with a server-side jti.

    The jti enables server-side revocation if needed.

    Args:
        user_id: MongoDB user ID to embed in the token payload.

    Returns:
        tuple[str, str]: (encoded JWT refresh token, jti string).
    """
    jti = secrets.token_urlsafe(16)
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_EXPIRY_DAYS)
    payload = {
        "user_id": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
        "jti": jti,
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, jti


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token.

    Args:
        token: Raw JWT string from the Authorization header or cookie.

    Returns:
        Dict[str, Any]: Decoded token payload.

    Raises:
        HTTPException: 401 if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def _user_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch a user document from an authenticated payload, or raise 401.

    Args:
        payload: Decoded JWT payload dict.

    Returns:
        Dict[str, Any]: Sanitized user document with id, is_admin, and role.

    Raises:
        HTTPException: 401 if token type is wrong, user_id is missing, user not found,
            or the user ID is invalid.
    """
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    try:
        user = await users_collection().find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid user ID")
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return _finalize_user(user)


async def get_current_user_ws(
    websocket: WebSocket,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Authenticate a WebSocket connection from a query `token` param or the
    `pp_token` cookie. Returns the user dict or raises a 401 HTTPException
    (callers convert to close codes).

    Args:
        websocket: The incoming WebSocket connection.
        token: Optional JWT token passed as a query parameter.

    Returns:
        Dict[str, Any]: Sanitized user document.

    Raises:
        HTTPException: 401 if no valid token is provided.
    """
    raw = token
    if not raw:
        cookies = websocket.cookies
        raw = cookies.get(COOKIE_NAME)
    if not raw:
        raise HTTPException(status_code=401, detail="Missing token")
    payload = decode_token(raw)
    return await _user_from_payload(payload)


def set_auth_cookie(response: Response, token: str, max_age: int = None, cookie_name: str = COOKIE_NAME):
    """Set the authentication httpOnly cookie on the response.

    Args:
        response: FastAPI Response object to modify.
        token: JWT token string to store.
        max_age: Cookie max-age in seconds (defaults to JWT expiry days).
        cookie_name: Name of the cookie (default: 'pp_token').
    """
    response.set_cookie(
        key=cookie_name,
        value=token,
        httponly=True,
        secure=settings.CORS_ORIGINS.split(",")[0].strip().startswith("https"),
        samesite="lax",
        max_age=max_age or (settings.JWT_EXPIRY_DAYS * 86400),
        path="/",
    )


def clear_auth_cookie(response: Response, cookie_name: str = COOKIE_NAME):
    """Clear the authentication cookie from the response.

    Args:
        response: FastAPI Response object to modify.
        cookie_name: Name of the cookie to delete (default: 'pp_token').
    """
    response.delete_cookie(key=cookie_name, path="/")


def _extract_token(request: Request, credentials: HTTPAuthorizationCredentials = None) -> str:
    """Extract JWT token from the request (Authorization header or cookie).

    Args:
        request: Incoming FastAPI Request.
        credentials: Optional HTTPBearer credentials from the request header.

    Returns:
        str: Raw JWT token string.

    Raises:
        HTTPException: 401 if no token is found in header or cookie.
    """
    if credentials and credentials.credentials:
        return credentials.credentials
    token = request.cookies.get(COOKIE_NAME)
    if token:
        return token
    raise HTTPException(status_code=401, detail="Not authenticated")


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get current authenticated user with caching.

    Only the user document is cached; is_admin/role are recomputed on every
    request via _finalize_user so privilege changes are never served stale.

    Args:
        request: Incoming FastAPI Request.
        credentials: HTTPBearer credentials from the Authorization header.

    Returns:
        Dict[str, Any]: Sanitized user document with id, is_admin, and role.

    Raises:
        HTTPException: 401 if the token is missing, invalid, or the user does not exist.
    """
    try:
        token = _extract_token(request, credentials)
        payload = decode_token(token)

        # Ensure this is an access token
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        # Check cache first (raw doc only — no derived privileges cached)
        cache_key = f"user:{user_id}"
        cached_user = await cache.get("auth", cache_key)
        if cached_user:
            return _finalize_user(cached_user)

        # Fetch from database
        try:
            user = await users_collection().find_one({"_id": ObjectId(user_id)})
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid user ID")

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Null the password hash before caching
        if "password_hash" in user:
            user["password_hash"] = None
        await cache.set("auth", cache_key, user, ttl=USER_CACHE_TTL)
        return _finalize_user(user)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")


async def optional_get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get current user if authenticated, otherwise None.

    Useful for public routes that behave differently for logged-in users.

    Args:
        request: Incoming FastAPI Request.
        credentials: Optional HTTPBearer credentials.

    Returns:
        Dict[str, Any] | None: Sanitized user document, or None if not authenticated.
    """
    try:
        return await get_current_user(request, credentials)
    except HTTPException:
        return None


async def get_current_user_with_plan(user=Depends(get_current_user)):
    """Get current user with plan information.

    Args:
        user: Authenticated user dict from get_current_user dependency.

    Returns:
        Dict[str, Any]: User document including plan field.
    """
    return user


def require_plan(required_plan: str):
    """Dependency factory for plan-based access control.

    Args:
        required_plan: Minimum plan tier required ('free', 'premium', 'pro', 'enterprise').

    Returns:
        Callable: FastAPI dependency that raises 403 if the user's plan is too low.

    Raises:
        HTTPException: 403 if the user's plan is below the required tier.
    """
    def dependency(user=Depends(get_current_user)):
        plan = user.get("plan", "free")
        plan_hierarchy = {"free": 0, "premium": 1, "pro": 2, "enterprise": 3}
        if plan_hierarchy.get(plan, 0) < plan_hierarchy.get(required_plan, 0):
            raise HTTPException(
                status_code=403,
                detail=f"This feature requires a {required_plan} plan or higher"
            )
        return user
    return dependency
