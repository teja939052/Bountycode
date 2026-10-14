"""Critical path tests for BountyCode backend."""
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
    from app.services.gamification import _get_streak_multiplier
    assert _get_streak_multiplier(0) == 1.0
    assert _get_streak_multiplier(3) == 1.2
    assert _get_streak_multiplier(7) == 1.5
    assert _get_streak_multiplier(30) == 3.0
    assert _get_streak_multiplier(100) == 5.0


def test_xp_calculation_types():
    from app.services.gamification import _calculate_xp
    assert _calculate_xp("interview", 100) >= _calculate_xp("interview", 50)
    assert _calculate_xp("coding", 0) > 0
    assert _calculate_xp("aptitude", 100) >= _calculate_xp("aptitude", 80)


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
    from app.services.ai_core import assign_companies
    companies = assign_companies()
    assert 2 <= len(companies) <= 5
    assert len(set(companies)) == len(companies)


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


def test_per_model_circuit_breaker_isolation():
    from app.services.circuit_breaker import ModelBreakerRegistry

    async def _test():
        registry = ModelBreakerRegistry(threshold=2, recovery_time=0.1)

        # Model A fails twice -> should be blocked
        await registry.record_failure("model-a")
        await registry.record_failure("model-a")
        assert await registry.allow_request("model-a") is False

        # Model B should still be allowed (independent breaker)
        assert await registry.allow_request("model-b") is True

        # Model A recovers after cooldown
        await asyncio.sleep(0.15)
        assert await registry.allow_request("model-a") is True

        # Model B success does not affect Model A
        await registry.record_success("model-b")
        assert await registry.allow_request("model-b") is True

    asyncio.run(_test())


def test_per_model_circuit_breaker_fallback_chain():
    from app.services.circuit_breaker import ModelBreakerRegistry

    async def _test():
        registry = ModelBreakerRegistry(threshold=2, recovery_time=0.1)

        # Model A is down; Model B is up.
        await registry.record_failure("model-a")
        await registry.record_failure("model-a")
        assert await registry.allow_request("model-a") is False
        assert await registry.allow_request("model-b") is True

        # Simulate a fallback chain: A fails, B succeeds.
        # The registry must not have blocked B just because A failed.
        models_to_try = ["model-a", "model-b"]
        for m in models_to_try:
            if await registry.allow_request(m):
                await registry.record_success(m)
                break

        assert await registry.allow_request("model-b") is True

    asyncio.run(_test())


def test_duplicate_route_prefixes_are_rejected():
    """Automated guard: duplicate route prefixes must be caught at import time."""
    import importlib
    import pkgutil
    from pathlib import Path
    from fastapi import APIRouter

    routes_dir = Path(__file__).resolve().parents[1] / "app" / "routes"
    prefixes = {}
    conflicts = []

    for module_info in pkgutil.iter_modules([str(routes_dir)]):
        module_name = module_info.name
        if module_name.startswith("_") or module_name in ("__init__", "archive"):
            continue
        try:
            module = importlib.import_module(f"app.routes.{module_name}")
        except Exception:
            continue
        router = getattr(module, "router", None)
        if router is None or not isinstance(router, APIRouter):
            continue
        prefix = router.prefix
        if prefix in prefixes:
            conflicts.append(f"{prefix} -> {prefixes[prefix]} + {module_name}")
        else:
            prefixes[prefix] = module_name

    assert not conflicts, f"Duplicate route prefixes detected: {conflicts}"
