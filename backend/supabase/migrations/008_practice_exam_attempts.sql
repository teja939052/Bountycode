-- Durable deterministic practice exams.
-- Trusted question content and answer keys remain in versioned repository files;
-- this table stores only selected IDs and learner-submitted answers.
CREATE TABLE IF NOT EXISTS practice_exam_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic VARCHAR(255),
    category VARCHAR(255),
    difficulty VARCHAR(50),
    duration_minutes INTEGER NOT NULL DEFAULT 20,
    question_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    answers JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(30) NOT NULL DEFAULT 'in_progress',
    score INTEGER,
    correct INTEGER,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_practice_exam_attempts_user_id
    ON practice_exam_attempts(user_id);
CREATE INDEX IF NOT EXISTS ix_practice_exam_attempts_status
    ON practice_exam_attempts(status);
CREATE INDEX IF NOT EXISTS ix_practice_exam_attempts_topic
    ON practice_exam_attempts(topic);
