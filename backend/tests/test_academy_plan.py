from pathlib import Path

from app.routes.academy_plan import DOMAIN_ENTRY_LESSON, build_plan
from app.services.service_company_sprint import load_sprint


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


def test_plan_only_includes_tracks_for_selected_companies():
    profile = {"target_role": "software_engineer", "target_companies": ["tcs"], "daily_minutes": 60}
    catalog = [
        {"id": "tcs_nqt", "company_id": "tcs", "name": "TCS NQT"},
        {"id": "infosys_infytq", "company_id": "infosys", "name": "Infosys InfyTQ"},
    ]
    plan = build_plan(profile, None, catalog)
    assert [track["company_id"] for track in plan["company_preparation"]] == ["tcs"]


def test_ongoing_practice_evidence_updates_diagnostic_priority():
    profile = {"target_role": "software_engineer", "daily_minutes": 60}
    diagnostic = {"skills": [
        {"domain": "programming_fundamentals", "score": 30},
        {"domain": "arrays_hashing", "score": 70},
        {"domain": "sql", "score": 60},
        {"domain": "computer_science", "score": 60},
    ]}
    evidence = {
        "programming_fundamentals": {"score": 82, "total_attempts": 12},
        "arrays_hashing": {"score": 25, "total_attempts": 8},
    }
    plan = build_plan(profile, diagnostic, adaptive_skills=evidence)
    assert plan["curriculum"][0]["domain"] == "arrays_hashing"
    programming = next(item for item in plan["curriculum"] if item["domain"] == "programming_fundamentals")
    assert programming["diagnostic_score"] == 30
    assert programming["adaptive_score"] == 82
    assert programming["effective_score"] == 82



def test_plan_places_unmastered_prerequisites_before_dependent_skills():
    profile = {"target_role": "software_engineer", "daily_minutes": 90}
    diagnostic = {"skills": [
        {"domain": "programming_fundamentals", "score": 25},
        {"domain": "arrays_hashing", "score": 15},
        {"domain": "computer_science", "score": 70},
        {"domain": "sql", "score": 75},
    ]}
    plan = build_plan(profile, diagnostic)
    domains = [item["domain"] for item in plan["curriculum"]]
    assert domains.index("programming_fundamentals") < domains.index("arrays_hashing")
    arrays = next(item for item in plan["curriculum"] if item["domain"] == "arrays_hashing")
    assert arrays["prerequisite_status"] == "needs_foundation"


def test_plan_does_not_block_on_a_reasonably_strong_prerequisite():
    profile = {"target_role": "software_engineer", "daily_minutes": 60}
    diagnostic = {"skills": [
        {"domain": "programming_fundamentals", "score": 75},
        {"domain": "arrays_hashing", "score": 20},
        {"domain": "computer_science", "score": 60},
        {"domain": "sql", "score": 60},
    ]}
    plan = build_plan(profile, diagnostic)
    assert plan["curriculum"][0]["domain"] == "arrays_hashing"
    arrays = plan["curriculum"][0]
    assert arrays["prerequisite_status"] == "complete"



def test_learning_preference_shapes_the_daily_study_routine():
    profile = {
        "target_role": "software_engineer",
        "experience_level": "beginner",
        "preferred_language": "java",
        "learning_preference": "hands_on",
        "daily_minutes": 60,
    }
    plan = build_plan(profile, None)

    assert plan["experience_level"] == "beginner"
    assert plan["preferred_language"] == "java"
    assert plan["learning_preference"] == "hands_on"
    assert "guided tasks" in plan["learning_strategy"]
    assert plan["study_routine"][1]["label"] == "Attempt a guided exercise"
    assert sum(step["minutes"] for step in plan["study_routine"]) <= 60


def test_plan_exposes_a_transparent_level_path_and_assessment_track():
    plan = build_plan({
        "target_role": "software_engineer",
        "assessment_track": "tcs_foundation",
        "daily_minutes": 60,
    }, {"overall_score": 72, "skills": [{"domain": "programming_fundamentals", "score": 72}]})

    assert plan["assessment_track"] == "tcs_foundation"
    assert plan["assessment_track_label"] == "TCS Foundation"
    assert plan["current_level"] == 3
    assert len(plan["level_path"]) == 6
    assert plan["level_path"][3]["status"] == "current"
    assert plan["next_action"] == plan["daily_tasks"][0]
    assert plan["assessment_blueprint"]["duration_minutes"] == 75
    assert plan["assessment_readiness"]["mock_ready"] is True
    assert plan["weekly_minutes"] == 300


def test_reading_preference_creates_a_reading_first_routine():
    plan = build_plan({
        "target_role": "undecided",
        "learning_preference": "reading",
        "daily_minutes": 45,
    }, None)

    assert plan["study_routine"][1]["label"] == "Read the concept explanation"
    assert "common misconceptions" in plan["learning_strategy"]
    assert sum(step["minutes"] for step in plan["study_routine"]) <= 45



def test_new_programming_plan_starts_with_variables_foundation():
    plan = build_plan({
        "target_role": "software_engineer",
        "daily_minutes": 60,
        "learning_preference": "mixed",
    }, None)

    first_programming_skill = next(
        item for item in plan["curriculum"]
        if item["domain"] == "programming_fundamentals"
    )
    assert first_programming_skill["lesson_slug"] == "variables_basics"



def test_personalized_plan_starts_each_subject_at_a_foundation_lesson():
    from app.routes.academy_plan import LESSON_BY_DOMAIN

    assert LESSON_BY_DOMAIN["programming_fundamentals"] == "variables_basics"
    assert LESSON_BY_DOMAIN["quantitative_aptitude"] == "number_systems"
    assert LESSON_BY_DOMAIN["logical_reasoning"] == "number_series"
    assert LESSON_BY_DOMAIN["verbal_ability"] == "vocabulary_cloze"
    assert LESSON_BY_DOMAIN["computer_science"] == "oops_basics"
    assert LESSON_BY_DOMAIN["sql"] == "dbms_basics"


def test_all_personalized_lesson_links_exist_in_catalog():
    lesson_dir = Path(__file__).parents[1] / "app" / "data" / "lessons"
    available = {path.stem for path in lesson_dir.glob("*.json")}
    sprint_slugs = {
        slug
        for sprint in load_sprint().get("sprints", [])
        for slug in sprint.get("lessons", [])
    }
    assert not (sprint_slugs - available)
    assert not ({*DOMAIN_ENTRY_LESSON.values()} - available)
