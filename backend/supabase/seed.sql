-- BountyCode — Synthetic Seed Data for Local Development
-- Migration: 002_seed_data
-- Idempotent: uses ON CONFLICT DO NOTHING / ON CONFLICT DO UPDATE
-- No real credentials, no production data, no PII.
--
-- Run with: npx supabase db reset --local

-- ============================================================
-- IDENTITY FIXTURES
-- ============================================================

INSERT INTO users (id, email, password_hash, name, plan, interviews_used, resumes_used, aptitude_used, honor, uid) VALUES
  ('11111111-1111-1111-1111-111111111111', 'alice@test.dev', '$2b$12$testhashplaceholder', 'Alice Student', 'free', 0, 0, 0, 0, 'uid_0001'),
  ('22222222-2222-2222-2222-222222222222', 'bob@test.dev',   '$2b$12$testhashplaceholder', 'Bob Student',   'free', 1, 0, 2, 50, 'uid_0002'),
  ('33333333-3333-3333-3333-333333333333', 'carol@test.dev', '$2b$12$testhashplaceholder', 'Carol Student', 'pro',   3, 1, 5, 200, 'uid_0003'),
  ('44444444-4444-4444-4444-444444444444', 'dave@test.dev', '$2b$12$testhashplaceholder', 'Dave Student',  'free', 0, 0, 1, 0,  'uid_0004'),
  ('55555555-5555-5555-5555-555555555555', 'eve@test.dev',   '$2b$12$testhashplaceholder', 'Eve Student',   'pro',   5, 2, 8, 400, 'uid_0005')
ON CONFLICT (email) DO UPDATE SET
  name = EXCLUDED.name,
  plan = EXCLUDED.plan,
  honor = EXCLUDED.honor;

INSERT INTO user_profiles (user_id, bio, skills, experience, portfolio_urls, github_username, leetcode_username, target_company, target_role) VALUES
  ('11111111-1111-1111-1111-111111111111', 'Learning DSA for placements', '["python","algorithms"]', 'Student', '[]', 'alice_dev', 'alice_leetcode', 'Google', 'Software Engineer'),
  ('22222222-2222-2222-2222-222222222222', 'Preparing for TCS Ninja', '["sql","java"]', 'Student', '[]', 'bob_dev', NULL, 'TCS', 'Software Engineer'),
  ('33333333-3333-3333-3333-333333333333', 'Targeting FAANG', '["python","system_design"]', 'Student', '[]', 'carol_dev', 'carol_leetcode', 'Amazon', 'Software Engineer'),
  ('44444444-4444-4444-4444-444444444444', 'Basic aptitude practice', '[]', 'Student', '[]', NULL, NULL, NULL, NULL),
  ('55555555-5555-5555-5555-555555555555', 'Experienced developer', '["python","go","system_design"]', 'Mid-level', '[]', 'eve_dev', 'eve_leetcode', 'Meta', 'Senior Software Engineer')
ON CONFLICT (user_id) DO UPDATE SET
  bio = EXCLUDED.bio,
  skills = EXCLUDED.skills,
  target_company = EXCLUDED.target_company,
  target_role = EXCLUDED.target_role;

INSERT INTO gamification_profiles (user_id, xp, diamonds, coins, stars, streak, level, badges) VALUES
  ('11111111-1111-1111-1111-111111111111', 250, 100, 50, 10, 3, 2, '[]'),
  ('22222222-2222-2222-2222-222222222222', 500, 200, 100, 20, 5, 3, '["first_steps"]'),
  ('33333333-3333-3333-3333-333333333333', 1200, 500, 250, 50, 10, 6, '["first_steps","streak_starter"]'),
  ('44444444-4444-4444-4444-444444444444', 100, 50, 25, 5, 1, 1, '[]'),
  ('55555555-5555-5555-5555-555555555555', 2000, 800, 400, 80, 15, 9, '["first_steps","streak_starter","speed_demon"]')
ON CONFLICT (user_id) DO UPDATE SET
  xp = EXCLUDED.xp,
  streak = EXCLUDED.streak,
  level = EXCLUDED.level;

INSERT INTO streak_records (user_id, current_streak, longest_streak, last_practice_date) VALUES
  ('11111111-1111-1111-1111-111111111111', 3, 5, '2026-11-20'),
  ('22222222-2222-2222-2222-222222222222', 5, 7, '2026-11-21'),
  ('33333333-3333-3333-3333-333333333333', 10, 14, '2026-11-22'),
  ('44444444-4444-4444-4444-444444444444', 1, 1, '2026-11-20'),
  ('55555555-5555-5555-5555-555555555555', 15, 20, '2026-11-23')
ON CONFLICT (user_id) DO UPDATE SET
  current_streak = EXCLUDED.current_streak,
  longest_streak = EXCLUDED.longest_streak,
  last_practice_date = EXCLUDED.last_practice_date;

-- ============================================================
-- SKILL FIXTURES
-- ============================================================

INSERT INTO skills (id, name, topic, sub_topic, difficulty, prerequisites, content_version, is_active) VALUES
  ('aaaaaaaa-1111-1111-1111-111111111111', 'two_pointers', 'arrays', NULL, 'easy', '[]', 'v1.0', true),
  ('bbbbbbbb-2222-2222-2222-222222222222', 'sliding_window', 'arrays', NULL, 'medium', '["aaaaaaaa-1111-1111-1111-111111111111"]', 'v1.0', true),
  ('cccccccc-3333-3333-3333-333333333333', 'binary_search', 'arrays', NULL, 'easy', '[]', 'v1.0', true),
  ('dddddddd-4444-4444-4444-444444444444', 'hash_map', 'arrays', NULL, 'medium', '[]', 'v1.0', true),
  ('eeeeeeee-5555-5555-5555-555555555555', 'dfs', 'trees', NULL, 'medium', '[]', 'v1.0', true),
  ('ffffffff-6666-6666-6666-666666666666', 'bfs', 'trees', NULL, 'medium', '["eeeeeeee-5555-5555-5555-555555555555"]', 'v1.0', true),
  ('11111111-aaaa-1111-1111-111111111111', 'percentages', 'aptitude', 'quant', 'easy', '[]', 'v1.0', true),
  ('22222222-bbbb-2222-2222-222222222222', 'profit_loss', 'aptitude', 'quant', 'easy', '[]', 'v1.0', true),
  ('33333333-cccc-3333-3333-333333333333', 'time_work', 'aptitude', 'quant', 'medium', '[]', 'v1.0', true)
ON CONFLICT (name) DO UPDATE SET
  topic = EXCLUDED.topic,
  difficulty = EXCLUDED.difficulty,
  prerequisites = EXCLUDED.prerequisites;

-- ============================================================
-- LEARNING FIXTURES
-- ============================================================

INSERT INTO learner_skill_state (user_id, skill_id, score, mastery_level, total_attempts, last_practiced) VALUES
  ('11111111-1111-1111-1111-111111111111', 'aaaaaaaa-1111-1111-1111-111111111111', 70, 'intermediate', 3, '2026-11-20 10:00:00+00'),
  ('22222222-2222-2222-2222-222222222222', 'aaaaaaaa-1111-1111-1111-111111111111', 40, 'beginner', 5, '2026-11-21 10:00:00+00'),
  ('33333333-3333-3333-3333-333333333333', 'aaaaaaaa-1111-1111-1111-111111111111', 90, 'master', 10, '2026-11-22 10:00:00+00'),
  ('44444444-4444-4444-4444-444444444444', 'aaaaaaaa-1111-1111-1111-111111111111', 20, 'beginner', 1, '2026-11-20 10:00:00+00'),
  ('55555555-5555-5555-5555-555555555555', 'aaaaaaaa-1111-1111-1111-111111111111', 85, 'advanced', 8, '2026-11-23 10:00:00+00')
ON CONFLICT (user_id, skill_id) DO UPDATE SET
  score = EXCLUDED.score,
  mastery_level = EXCLUDED.mastery_level,
  total_attempts = EXCLUDED.total_attempts,
  last_practiced = EXCLUDED.last_practiced;

INSERT INTO review_cards (user_id, problem_id, next_review, difficulty, interval, repetitions, ease_factor) VALUES
  ('11111111-1111-1111-1111-111111111111', 'prob_alice_1', '2026-11-21 10:00:00+00', 'medium', 1, 1, 250),
  ('22222222-2222-2222-2222-222222222222', 'prob_bob_1', '2026-11-22 10:00:00+00', 'easy', 2, 2, 300),
  ('33333333-3333-3333-3333-333333333333', 'prob_carol_1', '2026-11-25 10:00:00+00', 'hard', 7, 5, 200),
  ('44444444-4444-4444-4444-444444444444', 'prob_dave_1', '2026-11-21 10:00:00+00', 'easy', 1, 1, 250),
  ('55555555-5555-5555-5555-555555555555', 'prob_eve_1', '2026-11-24 10:00:00+00', 'medium', 3, 3, 250)
ON CONFLICT (user_id, problem_id) DO UPDATE SET
  next_review = EXCLUDED.next_review,
  interval = EXCLUDED.interval,
  repetitions = EXCLUDED.repetitions,
  ease_factor = EXCLUDED.ease_factor;

-- ============================================================
-- GAMIFICATION XP EVENTS FIXTURES
-- ============================================================

INSERT INTO xp_event_ledger (user_id, activity_type, score, xp_awarded, diamonds_awarded, event_metadata, reward_policy_version) VALUES
  ('11111111-1111-1111-1111-111111111111', 'practice', 8, 50, 20, '{"role":"sde","topic":"arrays","question_id":"prob_alice_1"}', 'v1'),
  ('22222222-2222-2222-2222-222222222222', 'practice', 6, 30, 10, '{"role":"sde","topic":"arrays","question_id":"prob_bob_1"}', 'v1'),
  ('33333333-3333-3333-3333-333333333333', 'practice', 9, 60, 25, '{"role":"sde","topic":"arrays","question_id":"prob_carol_1"}', 'v1'),
  ('44444444-4444-4444-4444-444444444444', 'practice', 5, 25, 5,  '{"role":"sde","topic":"arrays","question_id":"prob_dave_1"}', 'v1'),
  ('55555555-5555-5555-5555-555555555555', 'practice', 7, 45, 15, '{"role":"sde","topic":"arrays","question_id":"prob_eve_1"}', 'v1')
ON CONFLICT DO NOTHING;

-- ============================================================
-- BADGE FIXTURES
-- ============================================================

INSERT INTO badges (badge_id, name, description, criteria, is_active) VALUES
  ('first_steps', 'First Steps', 'Complete your first practice question', '{"type":"first_attempt"}', true),
  ('streak_starter', 'Streak Starter', 'Practice for 3 consecutive days', '{"type":"streak","min_days":3}', true),
  ('speed_demon', 'Speed Demon', 'Solve a question in under 2 minutes', '{"type":"speed","max_seconds":120}', true)
ON CONFLICT (badge_id) DO NOTHING;

-- ============================================================
-- REPAIR MISSION FIXTURES
-- ============================================================

INSERT INTO repair_missions (user_id, skill_id, title, description, status, tier, estimated_minutes) VALUES
  ('22222222-2222-2222-2222-222222222222', 'cccccccc-3333-3333-3333-333333333333', 'Binary Search Repair', 'Improve binary search accuracy through guided practice', 'open', 'repair', 15),
  ('44444444-4444-4444-4444-444444444444', 'aaaaaaaa-1111-1111-1111-111111111111', 'Two Pointers Repair', 'Strengthen two pointers fundamentals', 'in_progress', 'repair', 20)
ON CONFLICT DO NOTHING;

-- ============================================================
-- ASSESSMENT FIXTURES
-- ============================================================

INSERT INTO assessment_definitions (id, name, assessment_type, company_tags, topic_tags, difficulty, time_limit_minutes, question_count, is_active) VALUES
  ('aaaaaaaa-0000-0000-0000-000000000001', 'TCS Ninja Aptitude', 'aptitude', '["TCS"]', '["quant","reasoning"]', 'medium', 60, 20, true),
  ('bbbbbbbb-0000-0000-0000-000000000002', 'Google Coding Screen', 'coding', '["Google"]', '["arrays","trees"]', 'medium', 45, 2, true)
ON CONFLICT DO NOTHING;
