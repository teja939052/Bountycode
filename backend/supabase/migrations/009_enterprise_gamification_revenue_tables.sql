-- BountyCode — Enterprise, Gamification, and Revenue Tables
-- Migration: 009_enterprise_gamification_revenue_tables
--
-- Adds tables defined in SQLAlchemy models but missing from earlier migrations:
--   cohorts          (enterprise domain)
--   skill_graphs     (enterprise domain)
--   gamification     (gamification domain)
--   revenue_events   (operations domain)

-- ═══════════════════════════════════════════════════════════════════════════════
-- ENTERPRISE DOMAIN — cohorts
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS cohorts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    institution VARCHAR(255) NOT NULL,
    admin_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    student_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_cohorts_admin_id ON cohorts(admin_id);
CREATE INDEX IF NOT EXISTS ix_cohorts_institution ON cohorts(institution);

-- ═══════════════════════════════════════════════════════════════════════════════
-- ENTERPRISE DOMAIN — skill_graphs
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS skill_graphs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    overall_score INTEGER NOT NULL DEFAULT 0,
    diamonds INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 1,
    streak INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_skill_graphs_user_id ON skill_graphs(user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- GAMIFICATION DOMAIN — gamification
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS gamification (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    xp INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 1,
    diamonds INTEGER NOT NULL DEFAULT 0,
    streak INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_gamification_user_id ON gamification(user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- OPERATIONS DOMAIN — revenue_events
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS revenue_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    event_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_revenue_events_user_id ON revenue_events(user_id);
CREATE INDEX IF NOT EXISTS ix_revenue_events_event_type ON revenue_events(event_type);
CREATE INDEX IF NOT EXISTS ix_revenue_events_created_at ON revenue_events(created_at);
