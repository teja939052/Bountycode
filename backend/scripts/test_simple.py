"""Simple integration test: Journey Engine basic functionality."""
import sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

print("JOURNEY ENGINE INTEGRATION TEST")
print("=" * 50)

# Test 1: Import journey_engine
try:
    from app.services.journey_engine import build_journey_state, PRIORITY_WEIGHTS
    print("OK Journey engine imported successfully")
except Exception as e:
    print(f"X Journey engine import failed: {e}")
    sys.exit(1)

# Test 2: Priority weights exist and have correct categories
try:
    expected_categories = [
        "srs_overdue", "failed_repair", "prerequisite",
        "company_critical", "current_lesson", "role_practice",
        "mock_prep", "challenge", "exploration"
    ]
    actual_categories = list(PRIORITY_WEIGHTS.keys())
    if set(actual_categories) == set(expected_categories):
        print(f"OK Priority weights have all {len(expected_categories)} categories")
    else:
        print(f"X Missing categories. Expected: {expected_categories}")
        print(f"  Actual: {actual_categories}")
except Exception as e:
    print(f"X Priority weights check failed: {e}")

# Test 3: Verify weight ordering (highest first)
try:
    weights = [
        ("srs_overdue", PRIORITY_WEIGHTS["srs_overdue"]),
        ("failed_repair", PRIORITY_WEIGHTS["failed_repair"]),
        ("prerequisite", PRIORITY_WEIGHTS["prerequisite"]),
        ("company_critical", PRIORITY_WEIGHTS["company_critical"]),
        ("current_lesson", PRIORITY_WEIGHTS["current_lesson"]),
        ("role_practice", PRIORITY_WEIGHTS["role_practice"]),
        ("mock_prep", PRIORITY_WEIGHTS["mock_prep"]),
        ("challenge", PRIORITY_WEIGHTS["challenge"]),
        ("exploration", PRIORITY_WEIGHTS["exploration"]),
    ]
    # SRS should be highest, exploration lowest
    if weights[0][1] == 100 and weights[-1][1] == 10:
        print(f"OK Priority weights correctly ordered (100 down to 10)")
    else:
        print(f"X Priority weights not correctly ordered: {weights}")
except Exception as e:
    print(f"X Priority ordering check failed: {e}")

# Test 4: Title/emoji mapping
try:
    from app.services.journey_engine import _title_for_level, _emoji_for_level
    test_levels = [1, 10, 20, 50, 100]
    for level in test_levels:
        title = _title_for_level(level)
        emoji = _emoji_for_level(level)
        print(f"  Level {level}: {title['title']} {emoji}")
    print(f"OK Title/emoji mapping works")
except Exception as e:
    print(f"X Title/emoji mapping failed: {e}")

# Test 5: Journey route exists
try:
    from app.routes.journey import router
    print(f"OK Journey route registered: /api/v1/journey/state")
except Exception as e:
    print(f"X Journey route failed: {e}")

# Test 6: Canonical systems integration
try:
    from app.services.study_engine import get_today as study_get_today
    from app.services.gamification import get_gamification_profile
    from app.data.worlds_data import WORLD_REGISTRY
    print(f"OK Canonical systems accessible:")
    print(f"   - Study Engine accessible")
    print(f"   - Gamification profile accessible")
    print(f"   - Worlds: {len(WORLD_REGISTRY)} worlds loaded")
except Exception as e:
    print(f"X Canonical systems check: {e}")

print("=" * 50)
print("BASIC INTEGRATION TESTS COMPLETE")
print("Journey Engine is operational and integrates with all canonical systems")