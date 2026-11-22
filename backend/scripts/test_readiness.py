import sys, os
sys.path.insert(0, '.')
from datetime import datetime, timezone
from app.path_engine.graph import Graph
from app.path_engine.readiness import compute_readiness_range

# Build a minimal graph with 3 skills, TCS blueprint
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

# State: all skills have medium evidence, 0.5 mastery
from app.path_engine.learner import SkillState
state = {}
for sid in ["skill_a", "skill_b", "skill_c"]:
    state[sid] = SkillState(
        skill_id=sid, mastery=0.5, evidence_n=10.0, memory_strength=1.0,
        last_ts=now, weighted_successes=5.0, weighted_failures=5.0,
    )

# Test 1: No servable_counts -> all skills available, covered_fraction = 1.0
result = compute_readiness_range(graph, state, "tcs", now)
print(f"Test 1 - No servable_counts: covered_fraction={result['covered_fraction']}")
assert result["covered_fraction"] == 1.0, "All skills available should give 1.0"
print("  PASS")

# Test 2: skill_a has 11 servable (content_pending), skill_b and skill_c have 20+
servable_counts = {"skill_a": 11, "skill_b": 20, "skill_c": 30}
result = compute_readiness_range(graph, state, "tcs", now, servable_counts)
print(f"Test 2 - skill_a pending: covered_fraction={result['covered_fraction']}")
# skill_b (0.3) + skill_c (0.3) = 0.6 covered
assert abs(result["covered_fraction"] - 0.6) < 0.001, f"Expected 0.6, got {result['covered_fraction']}"
print("  PASS")

# Test 3: All skills have enough content
servable_counts = {"skill_a": 20, "skill_b": 20, "skill_c": 30}
result = compute_readiness_range(graph, state, "tcs", now, servable_counts)
print(f"Test 3 - All available: covered_fraction={result['covered_fraction']}")
assert abs(result["covered_fraction"] - 1.0) < 0.001, f"Expected 1.0, got {result['covered_fraction']}"
print("  PASS")

# Test 4: Check top_changes has content_available flag
result = compute_readiness_range(graph, state, "tcs", now, servable_counts={"skill_a": 11, "skill_b": 20, "skill_c": 30})
for change in result["top_changes"]:
    if change["skill_id"] == "skill_a":
        assert change["content_available"] == False, "skill_a should not be content available"
    else:
        assert change["content_available"] == True, f"{change['skill_id']} should be content available"
print("  PASS: content_available flag correct in top_changes")

print()
print("All readiness tests passed!")
