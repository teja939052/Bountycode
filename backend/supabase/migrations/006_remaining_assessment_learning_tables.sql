-- BountyCode — Remaining Assessment/Learning Tables
-- Migration: 006_remaining_assessment_learning_tables
--
-- Adds tables still referenced by active routes but not yet in PostgreSQL:
--   interview_bookings   (scheduled mock interviews)
--   solved_problems      (daily challenge problem history)
--   daily_challenges_users (per-user daily challenge state)
--   question_answers     (question answer records)

CREATE TABLE interview_bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company VARCHAR(100),
    role VARCHAR(100),
    interview_type VARCHAR(50) NOT NULL DEFAULT 'technical',
    status VARCHAR(50) NOT NULL DEFAULT 'scheduled',
    scheduled_at TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 30,
    score INTEGER,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_interview_bookings_user_id ON interview_bookings(user_id);
CREATE INDEX ix_interview_bookings_status ON interview_bookings(status);
CREATE INDEX ix_interview_bookings_scheduled_at ON interview_bookings(scheduled_at);

CREATE TABLE solved_problems (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    problem_id VARCHAR(255) NOT NULL,
    problem_type VARCHAR(50) NOT NULL DEFAULT 'coding',
    status VARCHAR(50) NOT NULL DEFAULT 'solved',
    score INTEGER,
    language VARCHAR(50),
    time_taken_seconds INTEGER,
    attempts INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_solved_problems_user_id ON solved_problems(user_id);
CREATE INDEX ix_solved_problems_problem_id ON solved_problems(problem_id);
CREATE INDEX ix_solved_problems_status ON solved_problems(status);

CREATE TABLE daily_challenges_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    challenge_date DATE NOT NULL,
    challenge_type VARCHAR(50) NOT NULL DEFAULT 'coding',
    status VARCHAR(50) NOT NULL DEFAULT 'in_progress',
    score INTEGER,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, challenge_date)
);

CREATE INDEX ix_daily_challenges_users_user_id ON daily_challenges_users(user_id);
CREATE INDEX ix_daily_challenges_users_date ON daily_challenges_users(challenge_date);

CREATE TABLE question_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id VARCHAR(255) NOT NULL,
    answer TEXT,
    is_correct BOOLEAN,
    score INTEGER,
    time_taken_seconds INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_question_answers_user_id ON question_answers(user_id);
CREATE INDEX ix_question_answers_question_id ON question_answers(question_id);
