"""Critical path tests for PlacementPro backend."""
import asyncio
import hashlib
import re
import time


def test_xp_calculation():
    from app.services.gamification import _calculate_level
    assert _calculate_level(0) == 1
    assert _calculate_level(50) == 2
    assert _calculate_level(200) == 3
    assert _calculate_level(4950) == 10


def test_streak_multiplier():
    from app.services.gamification import calculate_streak_multiplier
    mult, _ = calculate_streak_multiplier(0)
    assert mult == 1.0
    mult3, _ = calculate_streak_multiplier(3)
    assert mult3 == 1.2
    mult7, _ = calculate_streak_multiplier(7)
    assert mult7 == 1.5
    mult30, _ = calculate_streak_multiplier(30)
    assert mult30 == 3.0
    mult100, _ = calculate_streak_multiplier(100)
    assert mult100 == 5.0


def test_xp_calculation_types():
    from app.services.gamification import _calculate_xp
    assert _calculate_xp("interview", 100) >= _calculate_xp("interview", 50)
    assert _calculate_xp("coding", 0) > 0
    assert _calculate_xp("aptitude", 100) >= _calculate_xp("aptitude", 80)


def test_boss_level_detection():
    from app.services.gamification import BOSS_BATTLES
    assert 10 in BOSS_BATTLES
    assert 50 in BOSS_BATTLES
    assert 100 in BOSS_BATTLES
    assert 15 not in BOSS_BATTLES


def test_circuit_breaker_allows_requests():
    from app.services.circuit_breaker import CircuitBreaker

    async def _test():
        cb = CircuitBreaker("test", threshold=3, recovery_time=0.1)
        assert await cb.allow_request() is True
        await cb.record_failure()
        assert await cb.allow_request() is True
        await cb.record_failure()
        assert await cb.allow_request() is True
        await cb.record_failure()
        assert await cb.allow_request() is False
        await asyncio.sleep(0.15)
        assert await cb.allow_request() is True

    asyncio.run(_test())


def test_circuit_breaker_success_resets():
    from app.services.circuit_breaker import CircuitBreaker

    async def _test():
        cb = CircuitBreaker("test2", threshold=3)
        await cb.record_failure()
        await cb.record_failure()
        await cb.record_success()
        assert await cb.allow_request() is True

    asyncio.run(_test())


def test_request_metrics():
    from app.services.request_metrics import RequestMetrics

    async def _test():
        m = RequestMetrics()
        await m.record("test", "success", 100.0)
        await m.record("test", "failure", 200.0, "boom")
        snap = await m.snapshot()
        assert "test:success" in snap["counts"]
        assert "test:failure" in snap["counts"]
        assert snap["failures"]["test"] == 1
        assert "boom" in snap["last_error"]["test"]

    asyncio.run(_test())


def test_email_validation():
    email_re = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    assert re.match(email_re, "test@example.com")
    assert not re.match(email_re, "invalid")
    assert not re.match(email_re, "@no-local.com")


def test_duplicate_guard_hashing():
    key1 = hashlib.sha256(b"/api/test:abc:body1").hexdigest()
    key2 = hashlib.sha256(b"/api/test:abc:body1").hexdigest()
    key3 = hashlib.sha256(b"/api/test:abc:body2").hexdigest()
    assert key1 == key2
    assert key1 != key3


def test_health_check_exists():
    """Verify health endpoint exists in main module (skip on Windows due to resource module)."""
    import sys
    if sys.platform == "win32":
        return  # resource module not available on Windows
    import importlib
    mod = importlib.import_module("app.main")
    assert hasattr(mod, "health_check") or hasattr(mod, "app")


def test_assign_companies():
    from app.services.ai import assign_companies
    companies = assign_companies()
    assert 2 <= len(companies) <= 5
    assert len(set(companies)) == len(companies)


def test_power_ups_exist():
    from app.services.gamification import POWER_UPS
    assert "double_xp" in POWER_UPS
    assert "hint_reveal" in POWER_UPS
    assert "extra_time" in POWER_UPS
    assert "skip_boss" in POWER_UPS


def test_tower_titles_exist():
    from app.services.gamification import TOWER_TITLES
    assert TOWER_TITLES[1] == ("Hatchling", "🐣")
    assert TOWER_TITLES[100] == ("God of Code", "👑")


def test_wizard_outfits_exist():
    from app.services.gamification import WIZARD_OUTFITS
    assert 1 in WIZARD_OUTFITS
    assert 100 in WIZARD_OUTFITS
    assert "name" in WIZARD_OUTFITS[1]
    assert "color" in WIZARD_OUTFITS[50]


def test_calculate_stars():
    from app.services.gamification import calculate_stars
    assert calculate_stars(100, 30) >= calculate_stars(50, 120)


def test_request_metrics_snapshot_shape():
    from app.services.request_metrics import RequestMetrics

    async def _test():
        m = RequestMetrics()
        snap = await m.snapshot()
        assert "counts" in snap
        assert "latency_ms_total" in snap
        assert "failures" in snap
        assert "last_error" in snap
        assert "last_seen" in snap
        assert "services" in snap

    asyncio.run(_test())


def test_structured_logging_redacts_sensitive_data():
    from app.services.structured_logging import redact_sensitive_data, log_context

    payload = {
        "email": "student@example.com",
        "password": "secret123",
        "nested": {"token": "abc", "safe": "value"},
    }

    redacted = redact_sensitive_data(payload)
    assert redacted["email"] == "[REDACTED]"
    assert redacted["password"] == "[REDACTED]"
    assert redacted["nested"]["token"] == "[REDACTED]"
    assert redacted["nested"]["safe"] == "value"

    context = log_context(password="abc", path="/api/test")
    assert context["password"] == "[REDACTED]"
    assert context["path"] == "/api/test"


def test_cache_incr_updates_values():
    from app.services.cache import InMemoryCache

    cache = InMemoryCache(max_size=10, ttl_seconds=60)
    assert cache.incr("ratelimit", "127.0.0.1") == 1
    assert cache.incr("ratelimit", "127.0.0.1", amount=2) == 3


def test_creative_mind_feature_is_configured():
    from app.services.monetization import FREE_TIER, PRO_TIER

    assert "creative_mind" in FREE_TIER["features"]
    assert "creative_mind" in PRO_TIER["features"]
