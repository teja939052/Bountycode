-- BountyCode — Add score column to coding_submissions
-- Migration: 004_add_score_to_coding_submissions

ALTER TABLE coding_submissions
    ADD COLUMN IF NOT EXISTS score INTEGER;
