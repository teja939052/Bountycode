-- BountyCode — Additional Idempotency Columns
-- Migration: 003_additional_idempotency
--
-- Adds idempotency_key to OASession and InterviewSession tables.
-- Uses partial unique indexes (WHERE idempotency_key IS NOT NULL).

ALTER TABLE oa_sessions
    ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(255);

CREATE UNIQUE INDEX IF NOT EXISTS uq_oa_sessions_idempotency
    ON oa_sessions (user_id, idempotency_key)
    WHERE idempotency_key IS NOT NULL;

ALTER TABLE interview_sessions
    ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(255);

CREATE UNIQUE INDEX IF NOT EXISTS uq_interview_sessions_idempotency
    ON interview_sessions (user_id, idempotency_key)
    WHERE idempotency_key IS NOT NULL;
