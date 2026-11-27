-- BountyCode — Coupon and Discussion Tables
-- Migration: 010_coupons_discussion_tables
--
-- Adds tables defined in SQLAlchemy models but missing from earlier migrations:
--   coupons, coupon_usage (coupon domain)
--   discussion_posts, discussion_replies (community domain)

-- ═══════════════════════════════════════════════════════════════════════════════
-- COUPON DOMAIN — coupons
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS coupons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    discount_type VARCHAR(20) NOT NULL DEFAULT 'percentage',
    discount_value INTEGER NOT NULL DEFAULT 0,
    min_purchase INTEGER DEFAULT 0,
    max_discount INTEGER,
    usage_limit INTEGER DEFAULT NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    per_user_limit INTEGER DEFAULT 1,
    valid_from TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_until TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    applicable_plans JSONB NOT NULL DEFAULT '[]'::jsonb,
    applicable_tiers JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_coupons_code ON coupons(code);
CREATE INDEX IF NOT EXISTS ix_coupons_is_active ON coupons(is_active);
CREATE INDEX IF NOT EXISTS ix_coupons_valid_from ON coupons(valid_from);
CREATE INDEX IF NOT EXISTS ix_coupons_valid_until ON coupons(valid_until);

-- ═══════════════════════════════════════════════════════════════════════════════
-- COUPON DOMAIN — coupon_usage
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS coupon_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coupon_id UUID NOT NULL REFERENCES coupons(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    used_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    order_id VARCHAR(100),
    discount_applied INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS ix_coupon_usage_coupon_id ON coupon_usage(coupon_id);
CREATE INDEX IF NOT EXISTS ix_coupon_usage_user_id ON coupon_usage(user_id);
CREATE INDEX IF NOT EXISTS ix_coupon_usage_used_at ON coupon_usage(used_at);

-- ═══════════════════════════════════════════════════════════════════════════════
-- COMMUNITY DOMAIN — discussion_posts
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS discussion_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id VARCHAR(160) NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    code TEXT,
    language VARCHAR(50),
    discussion_type VARCHAR(50) NOT NULL DEFAULT 'solution',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_discussion_posts_question_id ON discussion_posts(question_id);
CREATE INDEX IF NOT EXISTS ix_discussion_posts_user_id ON discussion_posts(user_id);
CREATE INDEX IF NOT EXISTS ix_discussion_posts_created_at ON discussion_posts(created_at);

-- ═══════════════════════════════════════════════════════════════════════════════
-- COMMUNITY DOMAIN — discussion_replies
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS discussion_replies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES discussion_posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_discussion_replies_post_id ON discussion_replies(post_id);
CREATE INDEX IF NOT EXISTS ix_discussion_replies_user_id ON discussion_replies(user_id);
CREATE INDEX IF NOT EXISTS ix_discussion_replies_created_at ON discussion_replies(created_at);
