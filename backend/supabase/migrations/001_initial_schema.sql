-- BountyCode — Initial PostgreSQL Schema
-- Migration: 001_initial_schema
-- Created via Supabase CLI — single schema-migration authority
-- This migration creates all core application tables.
--
-- NOTE: Question content (statements, answers, test cases) stays in Git
-- per the Residency Rule. This migration only stores metadata.

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- IDENTITY DOMAIN
-- ============================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    plan VARCHAR(50) NOT NULL DEFAULT 'free',
    paypal_customer_id VARCHAR(255),
    paypal_order_id VARCHAR(255),
    plan_pending VARCHAR(50),
    interviews_used INTEGER NOT NULL DEFAULT 0,
    resumes_used INTEGER NOT NULL DEFAULT 0,
    aptitude_used INTEGER NOT NULL DEFAULT 0,
    mock_interviews_used INTEGER NOT NULL DEFAULT 0,
    monthly_reset_date TIMESTAMPTZ,
    daily_usage JSONB NOT NULL DEFAULT '{}'::jsonb,
    all_time_usage JSONB NOT NULL DEFAULT '{}'::jsonb,
    honor INTEGER NOT NULL DEFAULT 0,
    uid VARCHAR(255) UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_users_email ON users(email);
CREATE INDEX ix_users_uid ON users(uid);
CREATE INDEX ix_users_plan ON users(plan);

CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    bio TEXT,
    skills JSONB NOT NULL DEFAULT '[]'::jsonb,
    experience VARCHAR(100),
    portfolio_urls JSONB NOT NULL DEFAULT '[]'::jsonb,
    github_username VARCHAR(255),
    leetcode_username VARCHAR(255),
    target_company VARCHAR(255),
    target_role VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_user_profiles_user_id ON user_profiles(user_id);

CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    revoked_at TIMESTAMPTZ
);

CREATE INDEX ix_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX ix_user_sessions_expires_at ON user_sessions(expires_at);

CREATE TABLE refresh_tokens (
    jti VARCHAR(255) PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    revoked_at TIMESTAMPTZ,
    replaced_by_jti VARCHAR(255)
);

CREATE INDEX ix_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX ix_refresh_tokens_expires_at ON refresh_tokens(expires_at);

CREATE TABLE user_identity_map (
    legacy_mongo_id VARCHAR(255) PRIMARY KEY,
    postgres_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- LEARNING DOMAIN
-- ============================================================

CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    topic VARCHAR(100) NOT NULL,
    sub_topic VARCHAR(100),
    difficulty VARCHAR(50) NOT NULL,
    prerequisites JSONB NOT NULL DEFAULT '[]'::jsonb,
    content_version VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_skills_topic ON skills(topic);
CREATE INDEX ix_skills_difficulty ON skills(difficulty);
CREATE INDEX ix_skills_is_active ON skills(is_active);

CREATE TABLE skill_prerequisites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    prerequisite_skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(skill_id, prerequisite_skill_id)
);

CREATE INDEX ix_skill_prerequisites_skill_id ON skill_prerequisites(skill_id);
CREATE INDEX ix_skill_prerequisites_prerequisite_id ON skill_prerequisites(prerequisite_skill_id);

CREATE TABLE learner_skill_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    score INTEGER NOT NULL DEFAULT 0,
    mastery_level VARCHAR(50) NOT NULL DEFAULT 'beginner',
    total_attempts INTEGER NOT NULL DEFAULT 0,
    last_practiced TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, skill_id)
);

CREATE INDEX ix_learner_skill_state_user_id ON learner_skill_state(user_id);
CREATE INDEX ix_learner_skill_state_skill_id ON learner_skill_state(skill_id);

CREATE TABLE learning_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE SET NULL,
    question_id VARCHAR(255) NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL,
    evidence_type VARCHAR(50) NOT NULL,
    passing_score INTEGER NOT NULL DEFAULT 7,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    attempt_number INTEGER NOT NULL DEFAULT 1,
    passed BOOLEAN NOT NULL DEFAULT FALSE,
    attempt_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ix_learning_attempts_question_id ON learning_attempts(question_id);
CREATE INDEX ix_learning_attempts_activity_type ON learning_attempts(activity_type);
CREATE INDEX ix_learning_attempts_created_at ON learning_attempts(created_at);

CREATE TABLE learning_evidence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID NOT NULL REFERENCES learning_attempts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE SET NULL,
    evidence_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    evidence_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_learning_evidence_user_id ON learning_evidence(user_id);
CREATE INDEX ix_learning_evidence_attempt_id ON learning_evidence(attempt_id);
CREATE INDEX ix_learning_evidence_created_at ON learning_evidence(created_at);

CREATE TABLE mastery_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    mastery_level VARCHAR(50) NOT NULL,
    evidence_count INTEGER NOT NULL DEFAULT 0,
    score_at_snapshot INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_mastery_snapshots_user_id ON mastery_snapshots(user_id);
CREATE INDEX ix_mastery_snapshots_skill_id ON mastery_snapshots(skill_id);

CREATE TABLE review_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    problem_id VARCHAR(255) NOT NULL,
    next_review TIMESTAMPTZ NOT NULL,
    difficulty VARCHAR(50) NOT NULL DEFAULT 'medium',
    interval INTEGER NOT NULL DEFAULT 1,
    repetitions INTEGER NOT NULL DEFAULT 0,
    ease_factor INTEGER NOT NULL DEFAULT 250,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, problem_id)
);

CREATE INDEX ix_review_cards_user_id ON review_cards(user_id);
CREATE INDEX ix_review_cards_next_review ON review_cards(next_review);

CREATE TABLE repair_missions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'open',
    tier VARCHAR(50) NOT NULL DEFAULT 'repair',
    estimated_minutes INTEGER NOT NULL DEFAULT 10,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX ix_repair_missions_user_id ON repair_missions(user_id);
CREATE INDEX ix_repair_missions_skill_id ON repair_missions(skill_id);
CREATE INDEX ix_repair_missions_status ON repair_missions(status);

CREATE TABLE remediation_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repair_mission_id UUID NOT NULL REFERENCES repair_missions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    passed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_remediation_attempts_repair_mission_id ON remediation_attempts(repair_mission_id);
CREATE INDEX ix_remediation_attempts_user_id ON remediation_attempts(user_id);

-- ============================================================
-- CONTENT DOMAIN
-- ============================================================

CREATE TABLE content_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    version VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_content_packages_name ON content_packages(name);

CREATE TABLE content_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    package_id UUID NOT NULL REFERENCES content_packages(id) ON DELETE CASCADE,
    version VARCHAR(100) NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    file_paths JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(package_id, version)
);

CREATE INDEX ix_content_versions_package_id ON content_versions(package_id);

CREATE TABLE question_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id VARCHAR(255) UNIQUE NOT NULL,
    topic VARCHAR(100) NOT NULL,
    sub_topic VARCHAR(100),
    difficulty VARCHAR(50) NOT NULL,
    companies JSONB NOT NULL DEFAULT '[]'::jsonb,
    provenance VARCHAR(100),
    trust_status VARCHAR(50) NOT NULL DEFAULT 'unverified',
    quality_score INTEGER,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_question_metadata_question_id ON question_metadata(question_id);
CREATE INDEX ix_question_metadata_topic ON question_metadata(topic);
CREATE INDEX ix_question_metadata_difficulty ON question_metadata(difficulty);
CREATE INDEX ix_question_metadata_trust_status ON question_metadata(trust_status);

CREATE TABLE trust_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id VARCHAR(255) NOT NULL REFERENCES question_metadata(question_id) ON DELETE CASCADE,
    from_status VARCHAR(50) NOT NULL,
    to_status VARCHAR(50) NOT NULL,
    reviewed_by VARCHAR(255),
    review_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_trust_records_question_id ON trust_records(question_id);
CREATE INDEX ix_trust_records_created_at ON trust_records(created_at);

CREATE TABLE assessment_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    assessment_type VARCHAR(50) NOT NULL,
    company_tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    topic_tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    difficulty VARCHAR(50) NOT NULL,
    time_limit_minutes INTEGER NOT NULL DEFAULT 60,
    question_count INTEGER NOT NULL DEFAULT 10,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_assessment_definitions_name ON assessment_definitions(name);
CREATE INDEX ix_assessment_definitions_type ON assessment_definitions(assessment_type);
CREATE INDEX ix_assessment_definitions_difficulty ON assessment_definitions(difficulty);

CREATE TABLE assessment_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    definition_id UUID NOT NULL REFERENCES assessment_definitions(id) ON DELETE CASCADE,
    variant_id VARCHAR(255) UNIQUE NOT NULL,
    question_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    content_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_assessment_variants_definition_id ON assessment_variants(definition_id);

-- ============================================================
-- ASSESSMENTS DOMAIN
-- ============================================================

CREATE TABLE assessment_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assessment_id UUID NOT NULL REFERENCES assessment_definitions(id) ON DELETE CASCADE,
    variant_id VARCHAR(255),
    score INTEGER,
    status VARCHAR(50) NOT NULL DEFAULT 'in_progress',
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX ix_assessment_attempts_user_id ON assessment_attempts(user_id);
CREATE INDEX ix_assessment_attempts_assessment_id ON assessment_attempts(assessment_id);
CREATE INDEX ix_assessment_attempts_status ON assessment_attempts(status);
CREATE INDEX ix_assessment_attempts_started_at ON assessment_attempts(started_at);

CREATE TABLE assessment_sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID NOT NULL REFERENCES assessment_attempts(id) ON DELETE CASCADE,
    section_type VARCHAR(50) NOT NULL,
    score INTEGER,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX ix_assessment_sections_attempt_id ON assessment_sections(attempt_id);
CREATE INDEX ix_assessment_sections_section_type ON assessment_sections(section_type);

CREATE TABLE responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id UUID NOT NULL REFERENCES assessment_sections(id) ON DELETE CASCADE,
    question_id VARCHAR(255) NOT NULL,
    answer TEXT,
    is_correct BOOLEAN,
    score INTEGER,
    time_taken_seconds INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_responses_section_id ON responses(section_id);
CREATE INDEX ix_responses_question_id ON responses(question_id);

CREATE TABLE coding_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id VARCHAR(255) NOT NULL,
    code TEXT NOT NULL,
    language VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    execution_result JSONB NOT NULL DEFAULT '{}'::jsonb,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_coding_submissions_user_id ON coding_submissions(user_id);
CREATE INDEX ix_coding_submissions_question_id ON coding_submissions(question_id);
CREATE INDEX ix_coding_submissions_status ON coding_submissions(status);
CREATE INDEX ix_coding_submissions_submitted_at ON coding_submissions(submitted_at);

CREATE TABLE execution_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID NOT NULL REFERENCES coding_submissions(id) ON DELETE CASCADE,
    test_case_id VARCHAR(255) NOT NULL,
    passed BOOLEAN NOT NULL DEFAULT FALSE,
    expected TEXT,
    actual TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_execution_results_submission_id ON execution_results(submission_id);
CREATE INDEX ix_execution_results_test_case_id ON execution_results(test_case_id);

CREATE TABLE oa_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    blueprint JSONB NOT NULL DEFAULT '{}'::jsonb,
    mode VARCHAR(50) NOT NULL DEFAULT 'calm',
    integrity_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(50) NOT NULL DEFAULT 'in_progress',
    questions JSONB NOT NULL DEFAULT '[]'::jsonb,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX ix_oa_sessions_user_id ON oa_sessions(user_id);
CREATE INDEX ix_oa_sessions_company ON oa_sessions(company);
CREATE INDEX ix_oa_sessions_status ON oa_sessions(status);
CREATE INDEX ix_oa_sessions_started_at ON oa_sessions(started_at);

CREATE TABLE interview_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    interview_type VARCHAR(50) NOT NULL,
    company VARCHAR(100),
    difficulty VARCHAR(50) NOT NULL DEFAULT 'medium',
    status VARCHAR(50) NOT NULL DEFAULT 'in_progress',
    score INTEGER,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX ix_interview_sessions_user_id ON interview_sessions(user_id);
CREATE INDEX ix_interview_sessions_company ON interview_sessions(company);
CREATE INDEX ix_interview_sessions_status ON interview_sessions(status);
CREATE INDEX ix_interview_sessions_started_at ON interview_sessions(started_at);

CREATE TABLE company_assessment_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    assessment_type VARCHAR(50) NOT NULL,
    assessment_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ix_company_assessment_metadata_company ON company_assessment_metadata(company);

-- ============================================================
-- GAMIFICATION DOMAIN
-- ============================================================

CREATE TABLE gamification_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    xp INTEGER NOT NULL DEFAULT 0,
    diamonds INTEGER NOT NULL DEFAULT 0,
    coins INTEGER NOT NULL DEFAULT 0,
    stars INTEGER NOT NULL DEFAULT 0,
    streak INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 1,
    badges JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_gamification_profiles_xp ON gamification_profiles(xp DESC);
CREATE INDEX ix_gamification_profiles_level_xp ON gamification_profiles(level DESC, xp DESC);

CREATE TABLE xp_event_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES gamification_profiles(user_id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL,
    xp_awarded INTEGER NOT NULL,
    diamonds_awarded INTEGER NOT NULL DEFAULT 0,
    event_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    reward_policy_version VARCHAR(50) NOT NULL DEFAULT 'v1',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_xp_event_ledger_user_id ON xp_event_ledger(user_id);
CREATE INDEX ix_xp_event_ledger_activity_type ON xp_event_ledger(activity_type);
CREATE INDEX ix_xp_event_ledger_created_at ON xp_event_ledger(created_at DESC);

-- Constraint: xp_awarded must be non-negative
ALTER TABLE xp_event_ledger ADD CONSTRAINT ck_xp_event_ledger_xp_nonnegative CHECK (xp_awarded >= 0);

CREATE TABLE badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    badge_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    criteria JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_badges_badge_id ON badges(badge_id);
CREATE INDEX ix_badges_is_active ON badges(is_active);

CREATE TABLE user_badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_id VARCHAR(100) NOT NULL,
    earned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, badge_id)
);

CREATE INDEX ix_user_badges_user_id ON user_badges(user_id);
CREATE INDEX ix_user_badges_badge_id ON user_badges(badge_id);

CREATE TABLE streak_records (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    last_practice_date VARCHAR(10),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- CAREER DOMAIN
-- ============================================================

CREATE TABLE career_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    bio TEXT,
    skills JSONB NOT NULL DEFAULT '[]'::jsonb,
    experience VARCHAR(100),
    portfolio_urls JSONB NOT NULL DEFAULT '[]'::jsonb,
    target_company VARCHAR(255),
    target_role VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE portfolio_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    url VARCHAR(500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_portfolio_projects_user_id ON portfolio_projects(user_id);

CREATE TABLE resume_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    storage_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER,
    ats_score INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_resume_metadata_user_id ON resume_metadata(user_id);

CREATE TABLE uploaded_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    storage_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    file_size INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_uploaded_files_user_id ON uploaded_files(user_id);

-- ============================================================
-- OPERATIONS DOMAIN
-- ============================================================

CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event VARCHAR(100) NOT NULL,
    path VARCHAR(500),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    meta JSONB NOT NULL DEFAULT '{}'::jsonb,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    date VARCHAR(10) NOT NULL,
    hour INTEGER NOT NULL
);

CREATE INDEX ix_analytics_events_event ON analytics_events(event);
CREATE INDEX ix_analytics_events_date ON analytics_events(date);
CREATE INDEX ix_analytics_events_user_id ON analytics_events(user_id);
CREATE INDEX ix_analytics_events_timestamp ON analytics_events(timestamp DESC);

-- TTL replacement: analytics events older than 180 days are cleaned
-- by application-managed scheduled job (not PostgreSQL TTL)

CREATE TABLE analytics_rollups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bucket VARCHAR(100) NOT NULL,
    date VARCHAR(10) NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    unique_users INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(bucket, date)
);

CREATE INDEX ix_analytics_rollups_bucket ON analytics_rollups(bucket);
CREATE INDEX ix_analytics_rollups_date ON analytics_rollups(date);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action VARCHAR(100) NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ip_address VARCHAR(45),
    event_metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX ix_audit_logs_action ON audit_logs(action);
CREATE INDEX ix_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX ix_audit_logs_timestamp ON audit_logs(timestamp DESC);

-- Audit logs older than 1 year cleaned by scheduled job

CREATE TABLE billing_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    paypal_order_id VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_billing_records_user_id ON billing_records(user_id);
CREATE INDEX ix_billing_records_status ON billing_records(status);
CREATE INDEX ix_billing_records_created_at ON billing_records(created_at DESC);

-- ============================================================
-- COMMENTS
-- ============================================================

COMMENT ON TABLE users IS 'Core user accounts — migrated from MongoDB users collection';
COMMENT ON TABLE gamification_profiles IS 'Gamification state — single source of truth for XP/level/streak';
COMMENT ON TABLE xp_event_ledger IS 'Append-only XP ledger — profile.xp == sum(xp_awarded) must reconcile';
COMMENT ON TABLE learning_evidence IS 'Immutable learning evidence — never overwritten';
COMMENT ON TABLE question_metadata IS 'Question metadata only — content lives in Git (Residency Rule)';
COMMENT ON TABLE user_identity_map IS 'Legacy MongoDB ObjectId → PostgreSQL UUID mapping';
