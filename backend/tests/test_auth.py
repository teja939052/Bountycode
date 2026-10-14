"""Tests for authentication routes."""

import pytest
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import users_collection
from app.middleware.rate_limiter import clear_login_attempts
from app.config import get_settings

settings = get_settings()


@pytest.fixture
async def client():
    """Create a test client."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
async def clean_db():
    """Clean the database and rate limiter before and after tests."""
    clear_login_attempts("test@example.com")
    try:
        await users_collection().delete_many({"email": "test@example.com"})
    except Exception:
        pass
    yield
    clear_login_attempts("test@example.com")
    try:
        await users_collection().delete_many({"email": "test@example.com"})
    except Exception:
        pass


def _db_available() -> bool:
    try:
        from app.database import get_client
        import asyncio

        async def _ping():
            await get_client().admin.command("ping")

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(_ping())
        finally:
            loop.close()
        return True
    except Exception:
        return False


needs_db = pytest.mark.skipif(not _db_available(), reason="MongoDB unreachable")


@pytest.mark.asyncio
async def test_register(client, clean_db):
    """Test user registration."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["plan"] == "free"


@pytest.mark.asyncio
async def test_register_duplicate_email(client, clean_db):
    """Test registration with duplicate email."""
    email = "dup_test@example.com"
    await users_collection().delete_many({"email": email})
    clear_login_attempts(email)

    # First registration
    r1 = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    assert r1.status_code == 200
    
    # Second registration with same email
    r2 = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "name": "Test User 2",
            "password": "SecurePass123!"
        }
    )
    
    assert r2.status_code == 400
    assert "Email already registered" in r2.text
    await users_collection().delete_many({"email": email})


@pytest.mark.asyncio
async def test_login(client, clean_db):
    """Test user login."""
    # Register user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, clean_db):
    """Test login with invalid credentials."""
    # Register user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    
    # Login with wrong password
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!"
        }
    )
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.text


@pytest.mark.asyncio
async def test_get_me(client, clean_db):
    """Test getting current user."""
    # Register user
    reg_email = "getme_test@example.com"
    await users_collection().delete_many({"email": reg_email})
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": reg_email,
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    assert register_response.status_code == 200
    token = register_response.json().get("token")
    
    # Get user info with cookie or bearer token
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"} if token else {}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == reg_email
    assert data["name"] == "Test User"
    assert "usage" in data
    await users_collection().delete_many({"email": reg_email})


@pytest.mark.asyncio
async def test_logout(client, clean_db):
    """Test logout."""
    response = await client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out"
    # Check that cookie was cleared
    assert "Set-Cookie" in response.headers


@pytest.mark.asyncio
async def test_rate_limiting_login(client, clean_db):
    """Test login rate limiting."""
    # Register user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    
    # Attempt login with wrong password multiple times until rate limit / lockout
    last_status = None
    for i in range(6):
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": f"WrongPassword{i}!"
            }
        )
        last_status = response.status_code
    
    assert last_status == 429


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test health endpoint returns 200."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_questions_browse_requires_auth(client):
    """Test questions browse requires authentication."""
    response = await client.get("/api/v1/questions/browse")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_gamification_profile_requires_auth(client):
    """Test gamification profile requires authentication."""
    response = await client.get("/api/v1/gamification/profile")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_with_token(client, clean_db):
    """Test protected route with valid token."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "route_test@example.com",
            "name": "Route Test",
            "password": "SecurePass123!"
        }
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "route_test@example.com",
            "password": "SecurePass123!"
        }
    )
    assert login_resp.status_code == 200
    token = login_resp.json().get("token")
    
    # Access protected route
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "route_test@example.com"
    
    # Cleanup
    await users_collection().delete_many({"email": "route_test@example.com"})


@needs_db
@pytest.mark.asyncio
async def test_refresh_token_revocation_survives_restart(client, clean_db):
    """Refresh token revocation must survive server restart.
    
    Flow:
    1. Register + login
    2. Extract refresh token
    3. Revoke by setting refresh_revoked_at (simulating logout)
    4. Attempt refresh with old token
    5. Must be rejected with 401
    """
    email = "revoke_test@example.com"
    await users_collection().delete_many({"email": email})
    clear_login_attempts(email)

    # Register + login
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "name": "Revoke Test", "password": "SecurePass123!"},
    )
    assert reg.status_code == 200
    user_id = reg.json()["user"]["id"]

    # Extract refresh token from cookies
    refresh_cookie = reg.cookies.get("pp_refresh_token")
    assert refresh_cookie, "Refresh token cookie missing after registration"

    # Simulate logout/revocation by setting refresh_revoked_at in DB
    revoked_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    await users_collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"refresh_revoked_at": revoked_at}},
    )

    # Attempt refresh with the old cookie
    resp = await client.post("/api/v1/auth/refresh", cookies={"pp_refresh_token": refresh_cookie})
    assert resp.status_code == 401, f"Expected 401 after revocation, got {resp.status_code}"

    await users_collection().delete_many({"email": email})


@needs_db
@pytest.mark.asyncio
async def test_refresh_token_rotation_invalidates_old_token(client, clean_db):
    """After refresh, old refresh token must be invalid."""
    email = "rotate_test@example.com"
    await users_collection().delete_many({"email": email})
    clear_login_attempts(email)

    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "name": "Rotate Test", "password": "SecurePass123!"},
    )
    assert reg.status_code == 200
    user_id = reg.json()["user"]["id"]

    old_refresh = reg.cookies.get("pp_refresh_token")
    assert old_refresh

    # First refresh
    r1 = await client.post("/api/v1/auth/refresh", cookies={"pp_refresh_token": old_refresh})
    assert r1.status_code == 200
    new_refresh = r1.cookies.get("pp_refresh_token")
    assert new_refresh
    assert new_refresh != old_refresh

    # Old refresh token must now be invalid
    r2 = await client.post("/api/v1/auth/refresh", cookies={"pp_refresh_token": old_refresh})
    assert r2.status_code == 401

    await users_collection().delete_many({"email": email})


