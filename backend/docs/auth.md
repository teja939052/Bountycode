# Authentication & Authorization Model

## Overview

BountyCode uses a cookie-based auth model. JWT tokens never touch JavaScript
or URL query strings. All privilege decisions are server-authoritative.

## Token Lifecycle

1. **Access token** — short-lived JWT stored in an httpOnly cookie (`pp_token`).
2. **Refresh token** — longer-lived JWT stored in an httpOnly cookie
   (`pp_refresh_token`). Each user document tracks a single `refresh_jti`.
3. **Rotation** — `/refresh` rotates both tokens and updates `refresh_jti`.
   Logout / password change also clears `refresh_jti`, invalidating stolen
   refresh tokens.
4. **Revocation** — server-side `refresh_jti` comparison prevents reuse of
   old refresh tokens.

## WebSocket Auth

The `/ws` endpoint authenticates exclusively via the httpOnly `pp_token` cookie.
JWT tokens are never accepted via query string to prevent leakage in server
logs and browser history.

## Admin Authorization

`is_admin` / `role` are derived **ONLY** from the `ADMIN_EMAILS` config.
Subscription plan (`free`, `pro`, `lifetime`) never grants admin rights.

- `_finalize_user()` computes `is_admin = email.lower() in _admin_emails()`.
- The result is recomputed on every request; it is never cached.
- Admin routes check `user.get("role") == "admin" or user.get("is_admin") is True`.

## Security Layers

- httpOnly + secure + SameSite cookies
- Rate limiting (IP-based, Redis-backed when available)
- Login lockout after 5 failed attempts (15 min)
- Duplicate request guard (2-second window)
- CSP, HSTS, X-Frame-Options, X-Content-Type-Options headers
- Structured JSON logging with sensitive-data redaction
- Request ID tracing (`X-Request-ID`)
