#!/usr/bin/env python3
"""Generate a secure JWT secret and other random credentials."""

import secrets
import string
import sys


def generate_secret(length: int = 32) -> str:
    """Generate a cryptographically secure random string."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_-+=<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def main():
    """Generate and print secrets."""
    print("=" * 60)
    print("PlacementPro - Secure Secret Generator")
    print("=" * 60)
    print()
    
    jwt_secret = generate_secret(32)
    print(f"JWT_SECRET={jwt_secret}")
    
    mongo_password = generate_secret(16)
    print(f"MONGO_ROOT_PASSWORD={mongo_password}")
    
    # Generate a session key
    session_key = generate_secret(24)
    print(f"SESSION_KEY={session_key}")
    
    print()
    print("=" * 60)
    print("IMPORTANT: Copy these values to your .env file")
    print("Never commit .env files to version control!")
    print("=" * 60)


if __name__ == "__main__":
    main()
