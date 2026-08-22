"""Tests for cache service (InMemoryCache and RedisCache fallback)."""

import asyncio
import time
import pytest
from app.services.cache import InMemoryCache, RedisCache


class TestInMemoryCache:
    """Tests for the in-memory cache implementation."""

    def test_set_and_get(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        cache.set("test", "key1", "value1")
        assert cache.get("test", "key1") == "value1"

    def test_get_missing_returns_none(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        assert cache.get("test", "nonexistent") is None

    def test_namespace_isolation(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        cache.set("ns1", "key", "value1")
        cache.set("ns2", "key", "value2")
        assert cache.get("ns1", "key") == "value1"
        assert cache.get("ns2", "key") == "value2"

    def test_ttl_expiry(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=1)
        cache.set("test", "key", "value", ttl=1)
        assert cache.get("test", "key") == "value"
        time.sleep(1.1)
        assert cache.get("test", "key") is None

    def test_custom_ttl(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        cache.set("test", "key", "value", ttl=2)
        assert cache.get("test", "key") == "value"
        time.sleep(2.1)
        assert cache.get("test", "key") is None

    def test_lru_eviction_when_full(self):
        cache = InMemoryCache(max_size=3, ttl_seconds=3600)
        cache.set("test", "key1", "value1")
        cache.set("test", "key2", "value2")
        cache.set("test", "key3", "value3")
        cache.set("test", "key4", "value4")  # Should evict key1
        assert cache.get("test", "key1") is None
        assert cache.get("test", "key4") == "value4"

    def test_lru_keep_recently_accessed(self):
        cache = InMemoryCache(max_size=3, ttl_seconds=3600)
        cache.set("test", "key1", "value1")
        cache.set("test", "key2", "value2")
        cache.set("test", "key3", "value3")
        _ = cache.get("test", "key1")  # Access key1 to move it to end
        cache.set("test", "key4", "value4")  # Should evict key2
        assert cache.get("test", "key1") == "value1"
        assert cache.get("test", "key2") is None
        assert cache.get("test", "key4") == "value4"

    def test_delete_key(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        cache.set("test", "key", "value")
        cache.delete("test", "key")
        assert cache.get("test", "key") is None

    def test_clear_namespace(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        cache.set("ns1", "key1", "value1")
        cache.set("ns2", "key2", "value2")
        cache.clear_namespace("ns1")
        assert cache.get("ns1", "key1") is None
        assert cache.get("ns2", "key2") == "value2"

    def test_incr_creates_new_key(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        result = cache.incr("test", "counter")
        assert result == 1

    def test_incr_increments_existing(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        cache.set("test", "counter", 5)
        result = cache.incr("test", "counter")
        assert result == 6

    def test_incr_with_amount(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        cache.set("test", "counter", 10)
        result = cache.incr("test", "counter", amount=5)
        assert result == 15

    def test_stats_tracking(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        cache.set("test", "key1", "value1")
        cache.get("test", "key1")  # hit
        cache.get("test", "key1")  # hit
        cache.get("test", "missing")  # miss
        stats = cache.stats()
        assert stats["hits"] == 2
        assert stats["misses"] == 1
        assert stats["size"] == 1

    def test_overwrite_existing_key(self):
        cache = InMemoryCache(max_size=100, ttl_seconds=3600)
        cache.set("test", "key", "value1")
        cache.set("test", "key", "value2")
        assert cache.get("test", "key") == "value2"


class TestRedisCacheFallback:
    """Tests for Redis cache fallback behavior."""

    @pytest.mark.asyncio
    async def test_redis_connection_failure(self, mocker):
        mock_redis_module = mocker.patch("redis.asyncio")
        mock_redis_module.from_url.side_effect = Exception("Connection refused")

        cache = RedisCache(redis_url="redis://localhost:6379/0")
        await cache.connect()

        assert cache.connected is False

    @pytest.mark.asyncio
    async def test_redis_get_when_disconnected(self, mocker):
        mock_redis_module = mocker.patch("redis.asyncio")
        mock_redis_module.from_url.side_effect = Exception("Connection refused")

        cache = RedisCache(redis_url="redis://localhost:6379/0")
        await cache.connect()

        result = await cache.get("test", "key")
        assert result is None

    @pytest.mark.asyncio
    async def test_redis_set_when_disconnected(self, mocker):
        mock_redis_module = mocker.patch("redis.asyncio")
        mock_redis_module.from_url.side_effect = Exception("Connection refused")

        cache = RedisCache(redis_url="redis://localhost:6379/0")
        await cache.connect()

        await cache.set("test", "key", "value")
        result = await cache.get("test", "key")
        assert result is None
