-- BountyCode — Add Auth Columns to Users Table
-- Migration: 005_add_auth_columns_to_users
--
-- Adds columns needed for PostgreSQL-based authentication:
-- refresh_jti, reset_token, email verification, Google OAuth, etc.

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS country VARCHAR(100);

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS ip VARCHAR(45);

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS last_active TIMESTAMPTZ;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS refresh_jti VARCHAR(255);

CREATE INDEX IF NOT EXISTS ix_users_refresh_jti ON users (refresh_jti) WHERE refresh_jti IS NOT NULL;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255);

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMPTZ;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE NOT NULL;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR(255);

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS email_verification_expires TIMESTAMPTZ;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS google_id VARCHAR(255);

CREATE INDEX IF NOT EXISTS ix_users_google_id ON users (google_id) WHERE google_id IS NOT NULL;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS onboarding JSONB DEFAULT '{}'::jsonb NOT NULL;
