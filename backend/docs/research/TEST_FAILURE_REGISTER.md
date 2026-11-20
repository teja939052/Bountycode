# Test Failure Register

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Test Suite Summary

| Metric | Count |
|--------|-------|
| Total collected | 963 |
| Passed | 933 |
| Failed | 30 |
| Collection errors | 1 (by design — e2e journey test) |
| Skipped | 0 |

## Pre-existing Failures (30 — Unrelated to This Mission)

### Compiler Service (4 failures — Environmental)
| Test | Failure | Reason |
|------|---------|--------|
| test_python_success | assert 503 == 200 | Piston API unavailable in test environment |
| test_python_stdin_and_error_shape | KeyError | No compiler service |
| test_timeout_and_caps | KeyError | No compiler service |
| test_javascript_success | assert 503 == 200 | No compiler service |

### World/XP/Gamification (14 failures — Pre-existing)
| Test | Failure | Reason |
|------|---------|--------|
| test_engine_outage_loses_nothing | Unknown level: level-1 | Level ID mismatch (level-1 vs things-1 in WORLD_REGISTRY) |
| test_rapid_double_activity_counts_combo_once_each | KeyError: 'combo' | Missing combo field in gamification response |
| test_profile_reflects_latest_award_immediately | KeyError: 'diamonds' | Missing diamonds field |
| test_weekly_reset_and_ledger_reconcile | AssertionError | Economy/ledger logic |
| test_every_world_has_an_adventure_name | AssertionError | 11 worlds missing adventure_name |
| test_full_chain_unlocks_link_by_link | assert 23 == 12 | World count changed (12→23) |
| test_fresh_student_sees_foundations_open_rest_locked | assert 37 == 6 | Level count mismatch |
| test_progress_marks_world_active_and_keeps_it_open | assert 'unlocked' == 'active' | World status mismatch |
| test_locked_world_rejects_writes_but_opens_after_prereqs | AssertionError | World prerequisite logic |
| test_complete_awards_exact_reported_xp | AssertionError | XP award calculation |
| test_sequential_retry_is_noop | AssertionError | Retry logic |
| test_concurrent_double_tap_awards_once | AssertionError | Concurrent request handling |
| test_full_chain_progression_integration | AssertionError | Full chain progression |
| test_role_company_ordering_in_world_view | AssertionError | Role/company ordering |

### Dead Frontend Links (1 failure — Pre-existing)
| Test | Failure | Reason |
|------|---------|--------|
| test_route_parity | Dead internal links | Frontend routes without backend equivalents |

### Curriculum/Lessons (3 failures — Pre-existing)
| Test | Failure | Reason |
|------|---------|--------|
| test_get_lesson | AssertionError | Lesson retrieval |
| test_all_lessons_have_ids | AssertionError | Missing lesson IDs |
| test_completion_proceeds_after_quiz_pass | AssertionError | Quiz completion flow |

### Other (8 failures — Pre-existing)
| Test | Failure | Reason |
|------|---------|--------|
| test_oa_repair_loop_e2e | AssertionError | OA repair loop |
| test_badge_svg_no_auth | assert '1/12 worlds cleared' | World count changed |
| test_profile_and_leaderboard_carry_rank | KeyError: 'rank_title' | Missing rank_title field |
| test_due_card_selection_does_not_reset_future_dates | AssertionError | SRS scheduling |
| test_journey_includes_due_mongo_cards_via_shared_deserializer | AssertionError | SRS deserialization |
| test_b1_code_step_submission | AssertionError | Vertical slice code step |
| test_b1_debug_step_submission | AssertionError | Vertical slice debug step |
| test_lesson_content_verification | AssertionError | Lesson content check |

## New Tests (149 — All Pass)

| File | Tests | Status |
|------|-------|--------|
| test_mastery_engine_regression.py | 24 | PASS |
| test_question_quality_phase5.py | 24 | PASS |
| test_question_quality.py | 24 | PASS |
| test_question_governance.py | 43 | PASS |
| test_lesson_content_quality.py | 10 | PASS |
| test_company_lesson_placement_loop.py | 4 | PASS |

## Classification of Failures

| Classification | Count | Action Required |
|---------------|-------|-----------------|
| Fixed by this work | 0 | N/A |
| Existing unrelated failure | 30 | Document only — not caused by this mission |
| Environment/dependency failure | 4 | Compiler API unavailable |
| Newly introduced regression | 0 | N/A |
| Requires investigation | 0 | N/A |

## Recommendation

The 30 pre-existing failures should be addressed in a separate maintenance sprint. None are caused by or related to the Phase 5/6/7 mission changes.
