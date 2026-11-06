from app.routes.academy_plan import build_plan


def test_plan_prioritizes_lowest_diagnostic_skills():
    profile = {"target_role": "software_engineer", "target_companies": ["tcs"], "daily_minutes": 60}
    diagnostic = {"overall_score": 50, "skills": [
        {"domain": "programming_fundamentals", "score": 75},
        {"domain": "arrays_hashing", "score": 20},
        {"domain": "sql", "score": 45},
        {"domain": "computer_science", "score": 60},
    ]}
    plan = build_plan(profile, diagnostic)
    assert plan["curriculum"][0]["domain"] == "arrays_hashing"
    assert plan["curriculum"][0]["priority"] == "high"
    assert plan["diagnostic_completed"] is True


def test_plan_respects_daily_time_budget():
    plan = build_plan({"target_role": "undecided", "daily_minutes": 30}, None)
    assert sum(item["estimated_minutes"] for item in plan["daily_tasks"]) <= 30


def test_plan_uses_beginner_foundation_when_no_diagnostic_exists():
    plan = build_plan({"target_role": "undecided", "daily_minutes": 60}, None)
    assert plan["diagnostic_completed"] is False
    assert plan["daily_tasks"][0]["skill_level"] == "not_assessed"
    assert "diagnostic" in plan["personalization_note"].lower()


def test_role_changes_recommended_curriculum():
    data = build_plan({"target_role": "data_analyst", "daily_minutes": 90}, None)
    assert "sql" in [item["domain"] for item in data["curriculum"]]
    assert "quantitative_aptitude" in [item["domain"] for item in data["curriculum"]]
