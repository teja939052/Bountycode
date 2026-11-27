-- Academy onboarding, diagnostic, and personalized plan state.
-- Question and lesson source content remains versioned in repository files.

CREATE TABLE IF NOT EXISTS academy_learner_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_role VARCHAR(80) NOT NULL DEFAULT 'undecided',
    target_companies JSONB NOT NULL DEFAULT '[]'::jsonb,
    assessment_track VARCHAR(80) NOT NULL DEFAULT 'service_company_core',
    assessment_date DATE,
    experience_level VARCHAR(40) NOT NULL DEFAULT 'absolute_beginner',
    preferred_language VARCHAR(30) NOT NULL DEFAULT 'cpp',
    daily_minutes INTEGER NOT NULL DEFAULT 60,
    weekly_days INTEGER NOT NULL DEFAULT 5,
    device_type VARCHAR(30) NOT NULL DEFAULT 'laptop',
    local_runtime_available BOOLEAN NOT NULL DEFAULT TRUE,
    accessibility_needs TEXT NOT NULL DEFAULT '',
    placement_date DATE,
    learning_preference VARCHAR(40) NOT NULL DEFAULT 'mixed',
    timezone VARCHAR(80) NOT NULL DEFAULT 'Asia/Kolkata',
    onboarding_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_academy_learner_profiles_user_id UNIQUE (user_id)
);

CREATE INDEX IF NOT EXISTS ix_academy_learner_profiles_user_id
    ON academy_learner_profiles(user_id);

CREATE TABLE IF NOT EXISTS academy_diagnostic_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    diagnostic_id VARCHAR(160) NOT NULL,
    question_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    answers JSONB NOT NULL DEFAULT '[]'::jsonb,
    status VARCHAR(30) NOT NULL DEFAULT 'in_progress',
    result JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    CONSTRAINT uq_academy_diagnostic_sessions_user_diagnostic UNIQUE (user_id, diagnostic_id)
);

CREATE INDEX IF NOT EXISTS ix_academy_diagnostic_sessions_user_id
    ON academy_diagnostic_sessions(user_id);
CREATE INDEX IF NOT EXISTS ix_academy_diagnostic_sessions_status
    ON academy_diagnostic_sessions(status);
CREATE INDEX IF NOT EXISTS ix_academy_diagnostic_sessions_completed_at
    ON academy_diagnostic_sessions(completed_at);

CREATE TABLE IF NOT EXISTS academy_learning_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_academy_learning_plans_user_id UNIQUE (user_id)
);

CREATE INDEX IF NOT EXISTS ix_academy_learning_plans_user_id
    ON academy_learning_plans(user_id);
