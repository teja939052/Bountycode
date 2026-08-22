"""Tests for password hashing, verification, and JWT token handling."""

import pytest
from datetime import datetime, timezone, timedelta
from app.middleware.auth import (
    hash_password,
    verify_password,
    PasswordValidator,
    create_access_token,
    create_refresh_token,
    decode_token,
    _finalize_user,
)
from app.config import get_settings


class TestHashPassword:
    """Tests for password hashing."""

    def test_hash_password_returns_bcrypt_string(self):
        hashed = hash_password("SecurePass123!")
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    def test_hash_password_different_each_time(self):
        h1 = hash_password("SecurePass123!")
        h2 = hash_password("SecurePass123!")
        assert h1 != h2


class TestVerifyPassword:
    """Tests for password verification."""

    def test_verify_correct_password(self):
        hashed = hash_password("SecurePass123!")
        assert verify_password("SecurePass123!", hashed) is True

    def test_verify_incorrect_password(self):
        hashed = hash_password("SecurePass123!")
        assert verify_password("WrongPassword!", hashed) is False

    def test_verify_empty_password(self):
        hashed = hash_password("SecurePass123!")
        assert verify_password("", hashed) is False

    def test_verify_with_invalid_hash(self):
        assert verify_password("password", "not_a_valid_hash") is False


class TestPasswordValidator:
    """Tests for password strength validation."""

    def test_valid_password(self):
        valid, msg = PasswordValidator.validate("SecurePass123!")
        assert valid is True

    def test_password_too_short(self):
        valid, msg = PasswordValidator.validate("Short1!")
        assert valid is False

    def test_password_missing_number(self):
        valid, msg = PasswordValidator.validate("SecurePass!")
        assert valid is False

    def test_password_missing_special(self):
        valid, msg = PasswordValidator.validate("SecurePass123")
        assert valid is False

    def test_password_missing_both_number_and_special(self):
        valid, msg = PasswordValidator.validate("SecurePass")
        assert valid is False

    def test_exactly_minimum_length(self):
        valid, msg = PasswordValidator.validate("Pass1!23")
        assert valid is True


class TestCreateAccessToken:
    """Tests for JWT access token creation."""

    def test_token_contains_user_id(self):
        token = create_access_token("user123")
        payload = decode_token(token)
        assert payload["user_id"] == "user123"

    def test_token_has_correct_type(self):
        token = create_access_token("user123")
        payload = decode_token(token)
        assert payload["type"] == "access"

    def test_token_has_expiry(self):
        before = datetime.now(timezone.utc)
        token = create_access_token("user123")
        payload = decode_token(token)
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        assert exp > before
        assert exp < before + timedelta(days=8)


class TestCreateRefreshToken:
    """Tests for JWT refresh token creation."""

    def test_refresh_token_contains_jti(self):
        token, jti = create_refresh_token("user123")
        payload = decode_token(token)
        assert payload["jti"] == jti

    def test_refresh_token_has_correct_type(self):
        token, _ = create_refresh_token("user123")
        payload = decode_token(token)
        assert payload["type"] == "refresh"

    def test_refresh_tokens_are_unique(self):
        _, jti1 = create_refresh_token("user123")
        _, jti2 = create_refresh_token("user123")
        assert jti1 != jti2


class TestDecodeToken:
    """Tests for JWT token decoding."""

    def test_decode_valid_token(self):
        token = create_access_token("user123")
        payload = decode_token(token)
        assert payload["user_id"] == "user123"

    def test_decode_invalid_token_raises(self):
        with pytest.raises(Exception) as exc_info:
            decode_token("not_a_valid_token")
        assert "Invalid or expired" in str(exc_info.value)

    def test_decode_wrong_secret_raises(self, mocker):
        from app.config import get_settings
        original_secret = get_settings().JWT_SECRET
        token = create_access_token("user123")
        try:
            mocker.patch.object(get_settings(), "JWT_SECRET", "different_secret")
            with pytest.raises(Exception):
                decode_token(token)
        finally:
            mocker.patch.object(get_settings(), "JWT_SECRET", original_secret)


class TestFinalizeUser:
    """Tests for user payload sanitization and admin role computation."""

    def test_strips_password_hash(self):
        user = {
            "_id": "507f1f77bcf86cd799439011",
            "email": "test@example.com",
            "password_hash": "hashed_password",
        }
        result = _finalize_user(user)
        assert result.get("password_hash") is None

    def test_sets_id_from_object_id(self):
        from bson import ObjectId
        user = {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "email": "test@example.com",
        }
        result = _finalize_user(user)
        assert result["id"] == "507f1f77bcf86cd799439011"

    def test_sets_admin_for_admin_email(self):
        user = {
            "_id": "507f1f77bcf86cd799439011",
            "email": "sridevi72901@gmail.com",
        }
        result = _finalize_user(user)
        assert result["is_admin"] is True
        assert result["role"] == "admin"

    def test_no_admin_for_non_admin_email(self):
        user = {
            "_id": "507f1f77bcf86cd799439011",
            "email": "regular@example.com",
        }
        result = _finalize_user(user)
        assert result.get("is_admin") is False
        assert result.get("role") is None

    def test_admin_email_case_insensitive(self):
        user = {
            "_id": "507f1f77bcf86cd799439011",
            "email": "SRIDEVI72901@GMAIL.COM",
        }
        result = _finalize_user(user)
        assert result["is_admin"] is True
        assert result["role"] == "admin"

    def test_preserves_other_fields(self):
        user = {
            "_id": "507f1f77bcf86cd799439011",
            "email": "test@example.com",
            "name": "Test User",
            "plan": "pro",
            "xp": 100,
        }
        result = _finalize_user(user)
        assert result["name"] == "Test User"
        assert result["plan"] == "pro"
        assert result["xp"] == 100
