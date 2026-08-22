"""Tests for authentication routes."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import users_collection
from app.middleware.rate_limiter import clear_login_attempts


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

