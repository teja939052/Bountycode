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

logger = logging.getLogger(__name__)
settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)
COOKIE_NAME = "pp_token"
USER_CACHE_TTL = 300


class PasswordValidator:
    """Password strength validation."""
    
    @staticmethod
    def validate(password: str) -> tuple[bool, str]:
        """Validate password strength."""
        if len(password) < settings.PASSWORD_MIN_LENGTH:
            return False, f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long"
        
        if settings.PASSWORD_REQUIRE_NUMBER and not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        
        if settings.PASSWORD_REQUIRE_SPECIAL and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is valid"


import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    pwd_bytes = plain_password.encode('utf-8')[:72]
    hash_bytes = hashed_password.encode('utf-8')
    try:
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        return False


def create_access_token(user_id: str) -> str:
    """Create a JWT access token."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_EXPIRY_DAYS)
    payload = {
        "user_id": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Create a JWT refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_EXPIRY_DAYS)
    payload = {
        "user_id": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def _user_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch a user doc from an authenticated payload, or raise 401."""
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
    user["id"] = str(user["_id"])
    if "password_hash" in user:
        user["password_hash"] = None
    return user


async def get_current_user_ws(
    websocket: WebSocket,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """Authenticate a WebSocket connection from a query `token` param or the
    `pp_token` cookie. Returns the user dict or raises a 401 HTTPException
    (callers convert to close codes)."""
    raw = token
    if not raw:
        cookies = websocket.cookies
        raw = cookies.get(COOKIE_NAME)
    if not raw:
        raise HTTPException(status_code=401, detail="Missing token")
    payload = decode_token(raw)
    return await _user_from_payload(payload)


def set_auth_cookie(response: Response, token: str):
    """Set auth cookie with security flags."""
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.CORS_ORIGINS.startswith("https"),
        samesite="lax",
        max_age=settings.JWT_EXPIRY_DAYS * 86400,
        path="/",
    )


def clear_auth_cookie(response: Response):
    """Clear auth cookie."""
    response.delete_cookie(key=COOKIE_NAME, path="/")


def _extract_token(request: Request, credentials: HTTPAuthorizationCredentials = None) -> str:
    """Extract token from request (header or cookie)."""
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
    """Get current authenticated user with caching."""
    try:
        token = _extract_token(request, credentials)
        payload = decode_token(token)
        
        # Ensure this is an access token
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        # Check cache first
        cache_key = f"user:{user_id}"
        cached_user = await cache.get("auth", cache_key)
        if cached_user:
            return cached_user

        # Fetch from database
        try:
            user = await users_collection().find_one({"_id": ObjectId(user_id)})
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid user ID")

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Prepare user object for caching
        user["id"] = str(user["_id"])
        # Remove sensitive data
        if "password_hash" in user:
            user["password_hash"] = None
        
        await cache.set("auth", cache_key, user, ttl=USER_CACHE_TTL)
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")


async def optional_get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get current user if authenticated, otherwise None."""
    try:
        return await get_current_user(request, credentials)
    except HTTPException:
        return None


async def get_current_user_with_plan(user=Depends(get_current_user)):
    """Get current user with plan information."""
    return user


def require_plan(required_plan: str):
    """Dependency factory for plan-based access control."""
    async def dependency(user=Depends(get_current_user)):
        plan = user.get("plan", "free")
        plan_hierarchy = {"free": 0, "premium": 1, "pro": 2, "enterprise": 3}
        if plan_hierarchy.get(plan, 0) < plan_hierarchy.get(required_plan, 0):
            raise HTTPException(
                status_code=403,
                detail=f"This feature requires a {required_plan} plan or higher"
            )
        return user
    return dependency
