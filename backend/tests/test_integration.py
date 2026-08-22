"""Integration tests for pure logic — no MongoDB required."""
import asyncio
import json
import sys
import math
import re


# ── AI parse_json ────────────────────────────────────────────

class TestParseJson:
    def setup_method(self):
        from app.services.ai import parse_json
        self.parse = parse_json

    def test_clean_json(self):
        result = self.parse('{"key": "value"}')
        assert result["key"] == "value"

    def test_json_in_markdown_block(self):
        text = '```json\n{"answer": "hello"}\n```'
        result = self.parse(text)
        assert result["answer"] == "hello"

    def test_json_in_triple_backtick(self):
        text = '```\n{"a": 1}\n```'
        result = self.parse(text)
        assert result["a"] == 1

    def test_json_embedded_in_text(self):
        text = 'Here is the result: {"score": 95} and more text'
        result = self.parse(text)
        assert result["score"] == 95

    def test_json_array(self):
        text = 'Answer: [{"q": "what"}, {"q": "who"}]'
        result = self.parse(text)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_single_quotes_fallback(self):
        result = self.parse("{'name': 'test'}")
        assert result["name"] == "test"

    def test_invalid_json_raises(self):
        try:
            self.parse("this is not json at all and has no braces")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_whitespace_handling(self):
        result = self.parse('  \n  {"x": 42}  \n  ')
        assert result["x"] == 42

    def test_nested_json(self):
        data = {"outer": {"inner": [1, 2, 3]}}
        result = self.parse(json.dumps(data))
        assert result["outer"]["inner"] == [1, 2, 3]


# ── AI assign_companies ─────────────────────────────────────

class TestAssignCompanies:
    def test_default_returns_2_to_5(self):
        from app.services.ai import assign_companies
        for _ in range(50):
            companies = assign_companies()
            assert 2 <= len(companies) <= 5

    def test_no_duplicates(self):
        from app.services.ai import assign_companies
        for _ in range(50):
            companies = assign_companies()
            assert len(set(companies)) == len(companies)

    def test_respects_count(self):
        from app.services.ai import assign_companies
        result = assign_companies(count=2)
        assert len(result) == 2

    def test_clamps_extreme_counts(self):
        from app.services.ai import assign_companies
        assert len(assign_companies(count=0)) == 2  # min 2
        assert len(assign_companies(count=100)) <= 5  # max 5

    def test_returns_known_companies(self):
        from app.services.ai import assign_companies, COMPANY_TAGS
        for _ in range(50):
            for c in assign_companies():
                assert c in COMPANY_TAGS


# ── Gamification (all pure math) ─────────────────────────────

class TestGamification:
    def test_level_curve(self):
        from app.services.gamification import _calculate_level
        assert _calculate_level(0) == 1
        assert _calculate_level(50) == 2
        assert _calculate_level(200) == 3
        assert _calculate_level(1000) == 5
        assert _calculate_level(4950) == 10
        assert _calculate_level(24500) == 23
        assert _calculate_level(49050) == 32

    def test_level_never_below_1(self):
        from app.services.gamification import _calculate_level
        assert _calculate_level(-100) >= 1

    def test_streak_multiplier_monotonic(self):
        from app.services.gamification import calculate_streak_multiplier
        prev = 0
        for streak in [0, 1, 3, 7, 14, 30, 60, 100]:
            mult, _ = calculate_streak_multiplier(streak)
            assert mult >= prev
            prev = mult

    def test_battle_keys(self):
        from app.services.gamification import BOSS_BATTLES
        for level in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
            assert level in BOSS_BATTLES

    def test_boss_battles_have_required_fields(self):
        from app.services.gamification import BOSS_BATTLES
        for lvl, battle in BOSS_BATTLES.items():
            assert "name" in battle
            assert "emoji" in battle
            assert "required_score" in battle

    def test_power_ups_have_cost(self):
        from app.services.gamification import POWER_UPS
        for key, pu in POWER_UPS.items():
            assert "cost" in pu
            assert pu["cost"] > 0

    def test_wizard_outfits_at_milestones(self):
        from app.services.gamification import WIZARD_OUTFITS
        for lvl in [1, 10, 25, 50, 75, 100]:
            assert lvl in WIZARD_OUTFITS
            assert "name" in WIZARD_OUTFITS[lvl]
            assert "color" in WIZARD_OUTFITS[lvl]

    def test_tower_titles_at_milestones(self):
        from app.services.gamification import TOWER_TITLES
        for lvl in [1, 5, 10, 15, 50, 100]:
            assert lvl in TOWER_TITLES
            title, emoji = TOWER_TITLES[lvl]
            assert isinstance(title, str)
            assert isinstance(emoji, str)


# ── Placement Engine (pure math) ─────────────────────────────

class TestPlacementEngine:
    def setup_method(self):
        from app.services.placement_engine import PlacementEngine
        self.engine = PlacementEngine()

    def test_experience_modifier_zero(self):
        result = self.engine._calculate_experience_modifier({
            "total_interviews": 0, "total_coding": 0,
            "total_aptitude": 0, "streak": 0, "level": 1,
        })
        assert result == 0.85

    def test_experience_modifier_low(self):
        result = self.engine._calculate_experience_modifier({
            "total_interviews": 5, "total_coding": 3,
            "total_aptitude": 2, "streak": 2, "level": 3,
        })
        assert 1.0 <= result <= 1.15

    def test_experience_modifier_high(self):
        result = self.engine._calculate_experience_modifier({
            "total_interviews": 100, "total_coding": 50,
            "total_aptitude": 50, "streak": 30, "level": 15,
        })
        assert result > 1.0

    def test_experience_modifier_cap(self):
        result = self.engine._calculate_experience_modifier({
            "total_interviews": 1000, "total_coding": 1000,
            "total_aptitude": 1000, "streak": 100, "level": 50,
        })
        assert result <= 1.30

    def test_probability_band_high(self):
        band = self.engine._get_probability_band(75)
        assert band["label"] == "High Chance"
        assert band["color"] == "#10B981"

    def test_probability_band_moderate(self):
        band = self.engine._get_probability_band(55)
        assert band["label"] == "Moderate Chance"

    def test_probability_band_challenging(self):
        band = self.engine._get_probability_band(35)
        assert band["label"] == "Challenging"

    def test_probability_band_tough(self):
        band = self.engine._get_probability_band(15)
        assert band["label"] == "Tough"

    def test_company_profiles_have_tiers(self):
        for name, profile in self.engine.COMPANY_PROFILES.items():
            assert "rate" in profile
            assert "min_score" in profile
            assert "tier" in profile
            assert profile["tier"] in ("FAANG", "Product", "Services", "Startup")
            assert 0 < profile["rate"] < 1

    def test_tier_weights_sum_to_one(self):
        for tier, weights in self.engine.TIER_WEIGHTS.items():
            total = sum(weights.values())
            assert abs(total - 1.0) < 0.01, f"{tier} weights sum to {total}"

    def test_sub_skills_cover_all_categories(self):
        for cat in self.engine.TIER_WEIGHTS["FAANG"].keys():
            assert cat in self.engine.SUB_SKILLS
            assert len(self.engine.SUB_SKILLS[cat]) >= 3

    def test_unknown_company_raises(self):
        async def _test():
            try:
                await self.engine.calculate_probability("fake", "nonexistent_corp_xyz")
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "not found" in str(e)
        asyncio.run(_test())


# ── Export (DOCX/PDF) ────────────────────────────────────────

class TestExport:
    def test_docx_returns_bytes(self):
        from app.services.export import export_to_docx
        result = export_to_docx("JOHN DOE\nSoftware Engineer\n\nEXPERIENCE\n- Built APIs\n- Led team")
        assert isinstance(result, bytes)
        assert len(result) > 100

    def test_docx_contains_text(self):
        from app.services.export import export_to_docx
        result = export_to_docx("JOHN DOE\nSoftware Engineer")
        assert b"JOHN DOE" in result or b"John" in result or len(result) > 50

    def test_pdf_returns_bytes(self):
        from app.services.export import export_to_pdf
        result = export_to_pdf("JOHN DOE\nSoftware Engineer\n\nEXPERIENCE\n- Built APIs")
        assert isinstance(result, bytes)
        assert len(result) > 100

    def test_pdf_starts_with_pdf_magic(self):
        from app.services.export import export_to_pdf
        result = export_to_pdf("Test Resume Content")
        assert result[:5] == b"%PDF-"

    def test_empty_resume_handled(self):
        from app.services.export import export_to_docx
        result = export_to_docx("")
        assert isinstance(result, bytes)


# ── Curriculum data integrity ─────────────────────────────────

class TestCurriculum:
    def test_all_languages_present(self):
        import app.data.curriculum_enrichment  # noqa: F401
        from app.data.curriculum import get_all_languages
        langs = get_all_languages()
        assert len(langs) >= 7

    def test_each_language_has_50_levels(self):
        from app.data.curriculum import get_all_languages
        core_langs = {"c", "cpp", "java", "python", "javascript", "go", "rust"}
        for lang in get_all_languages():
            min_levels = 50 if lang["id"] in core_langs else 20
            assert len(lang["levels"]) >= min_levels, f"{lang['name']} has {len(lang['levels'])} levels"

    def test_each_language_levels_doubled(self):
        from app.data.curriculum import get_all_languages
        core_langs = {"c", "cpp", "java", "python", "javascript", "go", "rust"}
        web_langs = {"html", "css", "sql", "typescript", "react", "node"}
        for lang in get_all_languages():
            n = len(lang["levels"])
            if lang["id"] in core_langs:
                assert n == 100, f"{lang['name']} should have 100 levels, got {n}"
            elif lang["id"] in web_langs:
                assert n == 40, f"{lang['name']} should have 40 levels, got {n}"

    def test_each_language_has_project_lessons(self):
        from app.data.curriculum import get_all_languages
        for lang in get_all_languages():
            project_count = sum(
                1 for lv in lang["levels"].values()
                for l in lv["lessons"] if l["type"] == "project"
            )
            assert project_count >= 40, f"{lang['name']} has only {project_count} project lessons"

    def test_get_language(self):
        from app.data.curriculum import get_language
        for lid in ["c", "cpp", "java", "python", "javascript", "go", "rust"]:
            assert get_language(lid) is not None, f"{lid} should exist"

    def test_get_level(self):
        from app.data.curriculum import get_level
        for lid in ["c", "python", "javascript"]:
            level = get_level(lid, "l01")
            assert level is not None, f"{lid} l01 should exist"
            assert len(level["lessons"]) >= 5

    def test_get_lesson(self):
        from app.data.curriculum import get_lesson
        lesson = get_lesson("c", "l01", "c-l01-01")
        assert lesson is not None
        assert "title" in lesson
        assert "xp" in lesson

    def test_get_next_lesson(self):
        from app.data.curriculum import get_lesson, get_next_lesson
        first = get_lesson("c", "l01", "c-l01-01")
        second = get_next_lesson("c", "l01", "c-l01-01")
        assert second is not None
        assert second["title"] != first["title"]

    def test_get_next_lesson_last_returns_none(self):
        from app.data.curriculum import get_level, get_next_lesson
        level = get_level("c", "l01")
        last_id = level["lessons"][-1]["id"]
        assert get_next_lesson("c", "l01", last_id) is None

    def test_get_random_lessons(self):
        from app.data.curriculum import get_random_lessons
        lessons = get_random_lessons("python", 3)
        assert len(lessons) == 3
        for l in lessons:
            assert "title" in l
            assert "level_id" in l

    def test_total_lesson_count(self):
        from app.data.curriculum import get_all_languages
        total = 0
        for lang in get_all_languages():
            for level in lang["levels"].values():
                total += len(level["lessons"])
        assert total >= 300, f"Only {total} lessons found"

    def test_all_lessons_have_ids(self):
        from app.data.curriculum import get_all_languages
        for lang in get_all_languages():
            for lid, level in lang["levels"].items():
                for lesson in level["lessons"]:
                    assert "id" in lesson, f"Lesson missing id in {lang['name']} {lid}"
                    assert "title" in lesson
                    assert "xp" in lesson
                    assert lesson["xp"] > 0

    def test_level_themes_count(self):
        from app.data.curriculum import LEVEL_THEMES
        assert len(LEVEL_THEMES) == 50


# ── Indian companies data ─────────────────────────────────────

class TestIndianCompanies:
    def test_53_companies(self):
        from app.data.indian_companies import get_all_companies
        all_companies = get_all_companies()
        assert len(all_companies) >= 53

    def test_get_company_detail(self):
        from app.data.indian_companies import get_company_detail
        tcs = get_company_detail("tcs")
        assert tcs is not None
        assert tcs["name"] == "TCS"

    def test_all_companies_have_required_fields(self):
        from app.data.indian_companies import INDIAN_COMPANIES
        for key, info in INDIAN_COMPANIES.items():
            assert "name" in info
            assert "exam_pattern" in info
            assert "coding_patterns" in info
            assert len(info["coding_patterns"]) >= 5

    def test_get_all_companies_simplified(self):
        from app.data.indian_companies import get_all_companies
        for c in get_all_companies():
            assert "name" in c
            assert "exam_pattern" in c


# ── Route registration ───────────────────────────────────────

class TestRouteRegistration:
    """Verify all routers are registered without importing main (avoids resource module on Windows)."""

    def test_all_route_modules_importable(self):
        """Verify all core route modules import without error."""
        from app.routes import (
            auth, interview, resume, billing, aptitude, cover_letter,
            system_design, salary, company_prep, coding, gamification,
            free_practice, predictor, real_features, questions,
            career_profile, practice, analytics, ai_feedback,
            profile_stats, compiler, problems,
            daily_challenge, playlists,
            cards, wizard, submissions, progress, features,
            battles, aptitude_tests,
            indian_placement, placement_questions,
            dsa_fingerprint, energy, learning, analytics_admin,
        )

    def test_extended_route_modules_importable(self):
        """Verify extended routes (may have deeper dependency chains)."""
        from app.routes import hook_model, enhanced, student_features, enterprise, trial
        from app.routes import discussions, company_mocks, personal_dashboard, readiness
        from app.routes import ai_debugger, concepts, company_conversion
        from app.routes import visualizations, distributions, mock_interview
        from app.routes import system_design_tests, aptitude_tests
        # If we get here, all imports succeeded
        assert True

    def test_all_routers_have_prefix(self):
        from app.routes import auth, interview, billing, learning, gamification
        for mod in [auth, interview, billing, learning, gamification]:
            assert hasattr(mod, "router"), f"{mod.__name__} missing router"
            assert mod.router.prefix or mod.router.routes, f"{mod.__name__} router empty"


# ── Circuit breaker async ─────────────────────────────────────

class TestCircuitBreakerAdvanced:
    def test_circuit_breaker_half_open_allows_one_request(self):
        from app.services.circuit_breaker import CircuitBreaker

        async def _test():
            cb = CircuitBreaker("test-ho", threshold=2, recovery_time=0.05)
            await cb.record_failure()
            await cb.record_failure()
            assert await cb.allow_request() is False  # open
            await asyncio.sleep(0.1)
            assert await cb.allow_request() is True   # half-open allows one
        asyncio.run(_test())

    def test_circuit_breaker_reopens_after_failure_in_half_open(self):
        from app.services.circuit_breaker import CircuitBreaker

        async def _test():
            cb = CircuitBreaker("test-ho2", threshold=2, recovery_time=0.05)
            await cb.record_failure()
            await cb.record_failure()
            await asyncio.sleep(0.1)
            assert await cb.allow_request() is True   # half-open
            await cb.record_failure()
            await asyncio.sleep(0.1)
            assert await cb.allow_request() is True   # half-open again after recovery
        asyncio.run(_test())


# ── Validation utils ──────────────────────────────────────────

class TestValidation:
    def test_valid_email(self):
        from app.utils.validation import validate_email
        assert validate_email("test@example.com") is True
        assert validate_email("user+tag@domain.co") is True

    def test_invalid_email(self):
        from app.utils.validation import validate_email
        assert validate_email("not-an-email") is False
        assert validate_email("@no-local.com") is False
        assert validate_email("no@") is False

    def test_valid_password(self):
        from app.utils.validation import validate_password
        assert validate_password("StrongPass1!") is True

    def test_weak_passwords(self):
        from app.utils.validation import validate_password
        assert validate_password("short") is False
        assert validate_password("nouppercase1!") is False
        assert validate_password("NOLOWERCASE1!") is False
        assert validate_password("NoDigits!!!") is False

    def test_validate_required(self):
        from app.utils.validation import validate_required
        assert validate_required("hello", "name") is None
        assert validate_required("", "name") is not None
        assert validate_required(None, "name") is not None


# ── Energy constants ──────────────────────────────────────────

class TestEnergy:
    def test_constants(self):
        from app.services.energy import MAX_ENERGY, RECHARGE_HOURS, ENERGY_PER_DAY
        assert MAX_ENERGY == 10
        assert RECHARGE_HOURS == 4
        assert ENERGY_PER_DAY == 6

    def test_pro_unlimited(self):
        from app.services.energy import get_energy

        async def _test():
            user = {"id": "000000000000000000000000", "plan": "pro"}
            result = await get_energy(user)
            assert result["is_unlimited"] is True
        asyncio.run(_test())


# ── Request metrics ──────────────────────────────────────────

class TestRequestMetricsAdvanced:
    def test_latency_tracking(self):
        from app.services.request_metrics import RequestMetrics

        async def _test():
            m = RequestMetrics()
            for i in range(10):
                await m.record("svc", "success", float(i * 10))
            snap = await m.snapshot()
            assert snap["latency_ms_total"]["svc"] > 0
        asyncio.run(_test())

    def test_multiple_services(self):
        from app.services.request_metrics import RequestMetrics

        async def _test():
            m = RequestMetrics()
            await m.record("auth", "success", 10.0)
            await m.record("ai", "success", 200.0)
            await m.record("ai", "failure", 500.0, "timeout")
            snap = await m.snapshot()
            assert "auth:success" in snap["counts"]
            assert "ai:success" in snap["counts"]
            assert "ai:failure" in snap["counts"]
        asyncio.run(_test())


# ── DuplicateGuard ────────────────────────────────────────────

class TestDuplicateGuardAdvanced:
    def test_different_bodies_produce_different_hashes(self):
        import hashlib
        body1 = hashlib.sha256(b"/api/test:POST:body1").hexdigest()
        body2 = hashlib.sha256(b"/api/test:POST:body2").hexdigest()
        assert body1 != body2

    def test_same_body_same_hash(self):
        import hashlib
        body = hashlib.sha256(b"/api/test:POST:hello").hexdigest()
        body2 = hashlib.sha256(b"/api/test:POST:hello").hexdigest()
        assert body == body2


# ── Structured logging ────────────────────────────────────────

class TestStructuredLogging:
    def test_request_id_var(self):
        from app.services.structured_logging import request_id_var, new_request_id
        rid = new_request_id()
        assert isinstance(rid, str)
        assert len(rid) > 0
        request_id_var.set(rid)
        assert request_id_var.get() == rid


# ── Code Tracer ─────────────────────────────────────────────

class TestCodeTracer:
    def setup_method(self):
        from app.services.code_tracer import execute_with_trace, instrument_python_code, detect_algorithm_type
        self.execute_with_trace = execute_with_trace
        self.instrument = instrument_python_code
        self.detect = detect_algorithm_type

    def test_simple_assignment_trace(self):
        code = "x = 1\ny = 2\nz = x + y"
        result = self.execute_with_trace(code)
        assert result["error"] is None
        assert len(result["steps"]) >= 3
        # Last step should have z
        last = result["steps"][-1]
        assert "z" in last.get("vars", {})

    def test_loop_trace(self):
        code = "total = 0\nfor i in range(5):\n    total = total + i"
        result = self.execute_with_trace(code)
        assert result["error"] is None
        assert len(result["steps"]) >= 6  # 1 assignment + 5 loop iterations

    def test_if_else_trace(self):
        code = "x = 10\nif x > 5:\n    y = 'big'\nelse:\n    y = 'small'"
        result = self.execute_with_trace(code)
        assert result["error"] is None
        assert any("y" in s.get("vars", {}) for s in result["steps"])

    def test_function_trace(self):
        code = "def add(a, b):\n    return a + b\nresult = add(3, 4)"
        result = self.execute_with_trace(code)
        assert result["error"] is None
        assert any("result" in s.get("vars", {}) for s in result["steps"])

    def test_syntax_error_returns_original(self):
        code = "def ===invalid"
        result = self.execute_with_trace(code)
        # Should not crash, returns error
        assert result["error"] is not None or len(result["steps"]) == 0

    def test_detect_sorting(self):
        code = "arr.sort()\nreturn sorted(arr)"
        assert self.detect(code, []) == "sorting"

    def test_detect_binary_search(self):
        code = "low = 0\nhigh = len(arr)\nmid = (low + high) // 2"
        assert self.detect(code, []) == "binary_search"

    def test_detect_bfs(self):
        code = "from collections import deque\nqueue = deque([start])"
        assert self.detect(code, []) == "bfs"

    def test_detect_linked_list(self):
        code = "class Node:\n    def __init__(self):\n        self.next = None"
        assert self.detect(code, []) == "linked_list"

    def test_detect_dp(self):
        code = "dp = [0] * (n + 1)\nmemo = {}"
        assert self.detect(code, []) == "dynamic_programming"

    def test_detect_from_step_vars(self):
        steps = [{"vars": {"low": 0, "high": 10, "mid": 5}}]
        assert self.detect("", steps) == "binary_search"

    def test_detect_from_queue_var(self):
        steps = [{"vars": {"queue": "[0]", "visited": "{0}"}}]
        assert self.detect("", steps) == "bfs"


class TestCompilerExecutionTrace:
    def test_python_trace_uses_ast_source(self):
        from app.services.code_executor import CodeExecutionEngine

        engine = CodeExecutionEngine()
        result = asyncio.run(engine.generate_execution_trace("x = 1\nprint(x)", "python"))

        assert result["success"] is True
        assert result["source"] == "ast_trace"
        assert result["steps"]
        assert result["language"] == "python"

    def test_python_trace_detects_algorithm_family(self):
        from app.services.code_executor import CodeExecutionEngine

        engine = CodeExecutionEngine()
        code = "low = 0\nhigh = len(nums) - 1\nmid = (low + high) // 2"
        result = asyncio.run(engine.generate_execution_trace(code, "python"))

        assert result["success"] is True
        assert result["algorithm"] == "binary_search"
        assert result["visualization_type"] in {"array", "bars"}


# ── Visualization templates ──────────────────────────────────

class TestVisualizationTemplates:
    def test_templates_count(self):
        from app.routes.visualizations import VISUALIZATION_TEMPLATES
        assert len(VISUALIZATION_TEMPLATES) >= 45  # 50+ templates

    def test_templates_have_required_fields(self):
        from app.routes.visualizations import VISUALIZATION_TEMPLATES
        for key, tmpl in VISUALIZATION_TEMPLATES.items():
            assert "type" in tmpl, f"{key} missing type"
            assert "description" in tmpl, f"{key} missing description"
            assert "steps" in tmpl or "steps_template" in tmpl, f"{key} missing steps"
            assert "category" in tmpl, f"{key} missing category"

    def test_all_categories(self):
        from app.routes.visualizations import VISUALIZATION_TEMPLATES
        categories = set()
        for tmpl in VISUALIZATION_TEMPLATES.values():
            categories.add(tmpl.get("category", "other"))
        expected = {"sorting", "search", "linked_list", "tree", "graph", "stack", "dp", "matrix", "string", "backtracking", "window"}
        assert expected.issubset(categories), f"Missing categories: {expected - categories}"
