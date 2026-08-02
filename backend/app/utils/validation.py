"""Shared validation helpers for backend routes."""
import re


def validate_email(email: str) -> bool:
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email))


def validate_password(pw: str) -> bool:
    return (
        len(pw) >= 8
        and bool(re.search(r"[A-Z]", pw))
        and bool(re.search(r"[a-z]", pw))
        and bool(re.search(r"[0-9]", pw))
    )


def validate_required(value, field_name: str = "field"):
    if value is None:
        return f"{field_name} is required"
    if isinstance(value, str) and not value.strip():
        return f"{field_name} is required"
    return None
