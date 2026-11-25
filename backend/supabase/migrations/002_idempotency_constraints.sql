-- BountyCode — Idempotency Constraints
-- Migration: 002_idempotency_constraints
--
-- Adds database-enforced idempotency to assessment and learning writes.
-- Uses partial unique indexes (WHERE idempotency_key IS NOT NULL) so that
-- attempts without an idempotency key (retries, legacy writes) are not
-- falsely collided, while any provided key is enforced unique per user.
--
-- Dual-database safety: these indexes apply only to PostgreSQL-owned tables.
-- MongoDB collections are untouched.

-- ═════════════════════════════════════════════════════════════════════════════
-- LEARNING DOMAIN — idempotency on learning_attempts
-- ═════════════════════════════════════════════════════════════════════════════

ALTER TABLE learning_attempts
    ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(255);

CREATE UNIQUE INDEX IF NOT EXISTS uq_learning_attempts_idempotency
    ON learning_attempts (user_id, idempotency_key)
    WHERE idempotency_key IS NOT NULL;

-- ═════════════════════════════════════════════════════════════════════════════
-- GAMIFICATION DOMAIN — idempotency on xp_event_ledger
-- ═════════════════════════════════════════════════════════════════════════════

ALTER TABLE xp_event_ledger
    ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(255);

CREATE UNIQUE INDEX IF NOT EXISTS uq_xp_event_ledger_idempotency
    ON xp_event_ledger (user_id, idempotency_key)
    WHERE idempotency_key IS NOT NULL;

-- ═════════════════════════════════════════════════════════════════════════════
-- ASSESSMENTS DOMAIN — idempotency on assessment writes
-- ═════════════════════════════════════════════════════════════════════════════

ALTER TABLE assessment_attempts
    ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(255);

CREATE UNIQUE INDEX IF NOT EXISTS uq_assessment_attempts_idempotency
    ON assessment_attempts (user_id, idempotency_key)
    WHERE idempotency_key IS NOT NULL;

ALTER TABLE responses
    ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(255);

CREATE UNIQUE INDEX IF NOT EXISTS uq_responses_idempotency
    ON responses (section_id, question_id, idempotency_key)
    WHERE idempotency_key IS NOT NULL;

ALTER TABLE coding_submissions
    ADD COLUMN IF NOT EXISTS idempotency_key VARCHAR(255);

CREATE UNIQUE INDEX IF NOT EXISTS uq_coding_submissions_idempotency
    ON coding_submissions (user_id, question_id, idempotency_key)
    WHERE idempotency_key IS NOT NULL;
