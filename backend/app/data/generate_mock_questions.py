import json

with open('verified_placement_questions.json', 'r') as f:
    verified_data = json.load(f)

# Pick 5 aptitude, 5 verbal, 3 logical, 2 coding
apt_qs = [q for q in verified_data if q.get('type') == 'aptitude'][:5]
verbal_qs = [q for q in verified_data if q.get('type') == 'verbal'][:5]
log_qs = [q for q in verified_data if q.get('type') == 'logical'][:3]
coding_qs = [q for q in verified_data if q.get('type') == 'coding'][:2]

def map_q(q):
    """Map a verified question to mock_tests.json format."""
    return {
        "id": q.get("id"),
        "title": q.get("title", q.get("question", ""))[:60],
        "pattern": q.get("pattern", "misc"),
        "difficulty": q.get("difficulty", "medium"),
        "type": q.get("type", "aptitude"),
    }

print("=== APTITUDE ===")
for q in apt_qs:
    print(json.dumps(map_q(q), indent=2))

print("\n=== VERBAL ===")
for q in verbal_qs:
    print(json.dumps(map_q(q), indent=2))

print("\n=== LOGICAL ===")
for q in log_qs:
    print(json.dumps(map_q(q), indent=2))

print("\n=== CODING ===")
for q in coding_qs:
    print(json.dumps(map_q(q), indent=2))
