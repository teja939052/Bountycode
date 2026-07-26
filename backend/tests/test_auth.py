"""Tests for authentication routes."""

import pytest
from httpx import AsyncClient
from app.main import app
from app.database import users_collection


@pytest.fixture
async def client():
    """Create a test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def clean_db():
    """Clean the database before and after tests."""
    await users_collection().delete_many({})
    yield
    await users_collection().delete_many({})


@pytest.mark.asyncio
async def test_register(client, clean_db):
    """Test user registration."""
    response = await client.post(
        "/api/auth/register",
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
    # First registration
    await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    
    # Second registration with same email
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User 2",
            "password": "SecurePass123!"
        }
    )
    
    assert response.status_code == 400
    assert "Email already registered" in response.text


@pytest.mark.asyncio
async def test_login(client, clean_db):
    """Test user login."""
    # Register user
    await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    
    # Login
    response = await client.post(
        "/api/auth/login",
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
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    
    # Login with wrong password
    response = await client.post(
        "/api/auth/login",
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
    register_response = await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    
    token = register_response.json()["token"]
    
    # Get user info
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "usage" in data


@pytest.mark.asyncio
async def test_logout(client, clean_db):
    """Test logout."""
    response = await client.post("/api/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out"
    # Check that cookie was cleared
    assert "Set-Cookie" in response.headers


@pytest.mark.asyncio
async def test_rate_limiting_login(client, clean_db):
    """Test login rate limiting."""
    # Register user
    await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
    )
    
    # Attempt login with wrong password multiple times
    for _ in range(5):
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPassword123!"
            }
        )
        assert response.status_code == 401
    
    # 6th attempt should be rate limited
    response = await client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!"
        }
    )
    assert response.status_code == 429
    assert "locked" in response.text.lower()
