import sys, os
sys.path.insert(0, '.')
from datetime import datetime, timezone
from app.path_engine.graph import Graph
from app.path_engine.planner import plan, get_content_pending, CONTENT_PENDING_THRESHOLD

# Build a minimal graph with 3 skills
data = {
    "skills": {
        "skill_a": {"id": "skill_a", "name": "Skill A", "section": "coding",
                    "question_topics": ["arrays"], "lesson_ids": []},
        "skill_b": {"id": "skill_b", "name": "Skill B", "section": "coding",
                    "question_topics": ["sorting"], "lesson_ids": []},
        "skill_c": {"id": "skill_c", "name": "Skill C", "section": "coding",
                    "question_topics": ["hashing"], "lesson_ids": []},
    },
    "edges": [],
    "blueprints": {
        "tcs": {"skill_a": 0.4, "skill_b": 0.3, "skill_c": 0.3},
    },
}
graph = Graph(data)

now = datetime(2026, 1, 11, tzinfo=timezone.utc)

# State: all skills have medium evidence, low mastery
state = {}
for sid in ["skill_a", "skill_b", "skill_c"]:
    from app.path_engine.learner import SkillState
    state[sid] = SkillState(
        skill_id=sid, mastery=0.3, evidence_n=10.0, memory_strength=1.0,
        last_ts=now, weighted_successes=3.0, weighted_failures=7.0,
    )

# Test 1: skill_a has 11 servable (below threshold) -> should NOT be planned
servable_counts_11 = {"skill_a": 11, "skill_b": 20, "skill_c": 30}
actions = plan(graph, state, "tcs", days_left=1, slots_per_day=5, now=now,
               seed=42, servable_counts=servable_counts_11)
planned_skills = {a.skill_id for a in actions}
print(f"Test 1 - skill_a at 11 servable: planned={planned_skills}")
assert "skill_a" not in planned_skills, f"skill_a (11 servable) should NOT be planned!"
assert "skill_b" in planned_skills, "skill_b (20 servable) should be planned"
assert "skill_c" in planned_skills, "skill_c (30 servable) should be planned"
print("  PASS: skill_a excluded at 11 servable")

# Test 2: skill_a has 12 servable (at threshold) -> SHOULD be planned
servable_counts_12 = {"skill_a": 12, "skill_b": 20, "skill_c": 30}
actions = plan(graph, state, "tcs", days_left=1, slots_per_day=5, now=now,
               seed=42, servable_counts=servable_counts_12)
planned_skills = {a.skill_id for a in actions}
print(f"Test 2 - skill_a at 12 servable: planned={planned_skills}")
assert "skill_a" in planned_skills, f"skill_a (12 servable) SHOULD be planned!"
print("  PASS: skill_a included at 12 servable")

# Test 3: get_content_pending
pending = get_content_pending({"skill_a": 11, "skill_b": 20, "skill_c": 5})
print(f"Test 3 - content pending: {pending}")
assert "skill_a" in pending, "skill_a (11) should be pending"
assert pending["skill_a"]["missing"] == 1, "skill_a missing should be 1"
assert "skill_b" not in pending, "skill_b (20) should NOT be pending"
assert "skill_c" in pending, "skill_c (5) should be pending"
assert pending["skill_c"]["missing"] == 7, "skill_c missing should be 7"
print("  PASS: get_content_pending works correctly")

print()
print("All coverage mask tests passed!")
