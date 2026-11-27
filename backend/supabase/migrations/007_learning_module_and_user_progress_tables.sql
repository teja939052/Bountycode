-- BountyCode — Learning Module and User Learning Progress Tables
-- Migration: 007_learning_module_and_user_progress_tables
--
-- Adds tables for learning module persistence:
--   learning_modules   (lesson definitions)
--   user_learning_progress (per-user progress on modules)

CREATE TABLE learning_modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    difficulty VARCHAR(50) NOT NULL DEFAULT 'beginner',
    estimated_time_minutes INTEGER NOT NULL DEFAULT 15,
    steps JSONB NOT NULL DEFAULT '[]'::jsonb,
    xp_reward INTEGER NOT NULL DEFAULT 50,
    badge_reward VARCHAR(100),
    company_tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    topic VARCHAR(100) NOT NULL DEFAULT 'general',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_learning_modules_question_id ON learning_modules(question_id);
CREATE INDEX idx_learning_modules_topic ON learning_modules(topic);
CREATE INDEX idx_learning_modules_difficulty ON learning_modules(difficulty);

CREATE TABLE user_learning_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    module_id UUID NOT NULL REFERENCES learning_modules(id) ON DELETE CASCADE,
    completed_steps JSONB NOT NULL DEFAULT '[]'::jsonb,
    current_step INTEGER NOT NULL DEFAULT 1,
    xp_earned INTEGER NOT NULL DEFAULT 0,
    badge_unlocked VARCHAR(100),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    UNIQUE(user_id, module_id)
);

CREATE INDEX idx_user_learning_progress_user_id ON user_learning_progress(user_id);
CREATE INDEX idx_user_learning_progress_module_id ON user_learning_progress(module_id);
