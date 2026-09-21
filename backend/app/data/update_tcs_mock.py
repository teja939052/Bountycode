import json

# Load mock_tests.json
with open('../../app/content/curriculum/mock_tests.json', 'r') as f:
    mock_tests = json.load(f)

# Load verified questions
with open('../data/verified_placement_questions.json', 'r') as f:
    verified = json.load(f)

apt_qs = [q for q in verified if q.get('type') == 'aptitude'][:5]
verbal_qs = [q for q in verified if q.get('type') == 'verbal'][:5]
log_qs = [q for q in verified if q.get('type') == 'logical'][:3]
coding_qs = [q for q in verified if q.get('type') == 'coding'][:2]

def map_q(q):
    return {
        "id": q.get("id"),
        "title": q.get("title", q.get("question", ""))[:60],
        "pattern": q.get("pattern", "misc"),
        "difficulty": q.get("difficulty", "medium"),
        "type": q.get("type", "aptitude"),
        "trust_status": q.get("trust_status", "verified"),
        "provenance": q.get("provenance", "verified_placement_questions.json"),
        "source_bank": q.get("source_bank", "verified_placement_questions.json"),
    }

# Build new TCS mock
mock_tests['tcs'] = {
    "mock_config": {
        "name": "TCS NQT Mock Test",
        "description": "Abridged TCS NQT 2026-pattern simulation (15 questions). Full NQT = Foundation 65Q/75min (Numerical 20 + Verbal 25 + Reasoning 20) + Advanced Aptitude 15Q/25min + Advanced Coding 2 problems/90min with partial marks, 190 min total, no negative marking, sections lock permanently.",
        "total_questions": 15,
        "time_limit_minutes": 95,
        "pattern_version": "2026-abridged",
        "full_pattern": {
            "foundation": {"questions": 65, "minutes": 75, "sections": {"numerical_ability": {"questions": 20, "minutes": 25}, "verbal_ability": {"questions": 25, "minutes": 25}, "reasoning_ability": {"questions": 20, "minutes": 25}}},
            "advanced_aptitude": {"questions": 15, "minutes": 25},
            "advanced_coding": {"problems": 2, "minutes": 90, "partial_marks": True},
            "total_minutes": 190,
            "negative_marking": False,
            "section_switching": False,
            "back_navigation": False
        },
        "sections": [
            {
                "name": "Numerical Ability",
                "type": "aptitude",
                "count": 5,
                "time_minutes": 20,
                "questions": [map_q(q) for q in apt_qs]
            },
            {
                "name": "Verbal Ability",
                "type": "verbal",
                "count": 5,
                "time_minutes": 20,
                "questions": [map_q(q) for q in verbal_qs]
            },
            {
                "name": "Reasoning Ability",
                "type": "logical",
                "count": 3,
                "time_minutes": 15,
                "questions": [map_q(q) for q in log_qs]
            },
            {
                "name": "Coding Problems",
                "type": "coding",
                "count": 2,
                "time_minutes": 40,
                "questions": [map_q(q) for q in coding_qs]
            }
        ],
        "patterns": [
            "percentages", "time-work", "profit-loss", "ratio-proportion", "speed-distance-time",
            "synonym", "antonym", "sentence-correction",
            "series", "coding-decoding", "seating",
            "hashing", "dynamic programming"
        ],
        "content_trust": {
            "aptitude": "verified_placement_questions.json — independent correct_answer + options per question",
            "verbal": "verified_placement_questions.json — independent correct_answer + options per question",
            "logical": "verified_placement_questions.json — independent correct_answer + options per question",
            "coding": "verified_placement_questions.json — independent visible_testcases + hidden_testcases per question"
        }
    },
    "booking_slots": {
        "duration_minutes": 40,
        "slots_per_day": 15,
        "available_hours": [
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "13:00",
            "14:00"
        ]
    },
    "total_questions": 15,
    "patterns_covered": [
        "percentages", "time-work", "profit-loss", "ratio-proportion", "speed-distance-time",
        "synonym", "antonym", "sentence-correction",
        "series", "coding-decoding", "seating",
        "hashing", "dynamic programming"
    ],
    "avg_quality": 32.0
}

# Write back
with open('../../app/content/curriculum/mock_tests.json', 'w') as f:
    json.dump(mock_tests, f, indent=2, ensure_ascii=False)

print('Updated mock_tests.json TCS section')
print(f'Total questions: {sum(s["count"] for s in mock_tests["tcs"]["mock_config"]["sections"])}')
for s in mock_tests['tcs']['mock_config']['sections']:
    print(f'  {s["name"]}: {s["count"]} questions, type={s["type"]}')
