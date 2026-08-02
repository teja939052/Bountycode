import json
import hashlib
import time
from typing import Optional, Any
from collections import OrderedDict
import asyncio


class InMemoryCache:
    """In-memory cache with TTL and LRU eviction. Fallback when Redis is unavailable."""

    def __init__(self, max_size: int = 2000, ttl_seconds: int = 3600):
        self.cache: OrderedDict[str, dict] = OrderedDict()
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.hits = 0
        self.misses = 0

    def _make_key(self, namespace: str, key: str) -> str:
        return f"{namespace}:{key}"

    def get(self, namespace: str, key: str) -> Optional[Any]:
        full_key = self._make_key(namespace, key)
        if full_key in self.cache:
            entry = self.cache[full_key]
            ttl = entry.get("ttl", self.ttl_seconds)
            if time.time() - entry["timestamp"] < ttl:
                self.hits += 1
                self.cache.move_to_end(full_key)
                return entry["value"]
            else:
                del self.cache[full_key]
        self.misses += 1
        return None

    def set(self, namespace: str, key: str, value: Any, ttl: int = None):
        full_key = self._make_key(namespace, key)
        if full_key in self.cache:
            self.cache.move_to_end(full_key)
        else:
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
        self.cache[full_key] = {
            "value": value,
            "timestamp": time.time(),
            "ttl": ttl or self.ttl_seconds,
        }

    def incr(self, namespace: str, key: str, amount: int = 1, ttl: int = None) -> int:
        full_key = self._make_key(namespace, key)
        current = self.cache.get(full_key)
        current_value = 0
        if current is not None:
            ttl = current.get("ttl", ttl or self.ttl_seconds)
            if time.time() - current["timestamp"] < ttl:
                try:
                    current_value = int(current["value"])
                except (TypeError, ValueError):
                    current_value = 0
            else:
                del self.cache[full_key]
        next_value = current_value + amount
        self.cache[full_key] = {
            "value": next_value,
            "timestamp": time.time(),
            "ttl": ttl or self.ttl_seconds,
        }
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
        return next_value

    def delete(self, namespace: str, key: str):
        full_key = self._make_key(namespace, key)
        if full_key in self.cache:
            del self.cache[full_key]

    def clear_namespace(self, namespace: str):
        keys_to_delete = [k for k in self.cache.keys() if k.startswith(f"{namespace}:")]
        for key in keys_to_delete:
            del self.cache[key]

    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total * 100, 1) if total > 0 else 0,
        }


class RedisCache:
    """Redis-based distributed cache for production."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.client = None
        self.connected = False
        self.hits = 0
        self.misses = 0

    async def connect(self):
        try:
            import redis.asyncio as aioredis
            self.client = aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
            )
            await self.client.ping()
            self.connected = True
        except Exception as e:
            print(f"Redis connection failed: {e}. Using in-memory fallback.")
            self.connected = False

    async def disconnect(self):
        if self.client:
            await self.client.close()
            self.client = None
            self.connected = False

    async def get(self, namespace: str, key: str) -> Optional[Any]:
        if not self.connected:
            return None
        try:
            full_key = f"{namespace}:{key}"
            value = await self.client.get(full_key)
            if value:
                self.hits += 1
                return json.loads(value)
            self.misses += 1
            return None
        except Exception:
            self.misses += 1
            return None

    async def set(self, namespace: str, key: str, value: Any, ttl: int = 3600):
        if not self.connected:
            return
        try:
            full_key = f"{namespace}:{key}"
            await self.client.setex(full_key, ttl, json.dumps(value, default=str))
        except Exception:
            pass

    async def incr(self, namespace: str, key: str, amount: int = 1, ttl: int = 3600) -> int:
        if not self.connected:
            return amount
        try:
            full_key = f"{namespace}:{key}"
            next_value = await self.client.incrby(full_key, amount)
            if next_value == amount:
                await self.client.expire(full_key, ttl)
            return int(next_value)
        except Exception:
            return amount

    async def delete(self, namespace: str, key: str):
        if not self.connected:
            return
        try:
            full_key = f"{namespace}:{key}"
            await self.client.delete(full_key)
        except Exception:
            pass

    async def clear_namespace(self, namespace: str):
        if not self.connected:
            return
        try:
            keys = await self.client.keys(f"{namespace}:*")
            if keys:
                await self.client.delete(*keys)
        except Exception:
            pass

    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "connected": self.connected,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total * 100, 1) if total > 0 else 0,
        }


class UnifiedCache:
    """Unified cache that tries Redis first, falls back to in-memory."""

    def __init__(self, redis_url: str = None):
        self.redis = RedisCache(redis_url) if redis_url else None
        self.memory = InMemoryCache()
        self.initialized = False

    async def initialize(self, redis_url: str = None):
        if redis_url and not self.redis:
            self.redis = RedisCache(redis_url)
        if self.redis:
            await self.redis.connect()
        self.initialized = True

    async def get(self, namespace: str, key: str) -> Optional[Any]:
        # Try Redis first
        if self.redis and self.redis.connected:
            value = await self.redis.get(namespace, key)
            if value is not None:
                return value

        # Fallback to memory
        return self.memory.get(namespace, key)

    async def set(self, namespace: str, key: str, value: Any, ttl: int = 3600):
        # Set in both
        if self.redis and self.redis.connected:
            await self.redis.set(namespace, key, value, ttl)
        self.memory.set(namespace, key, value, ttl)

    async def incr(self, namespace: str, key: str, amount: int = 1, ttl: int = 3600) -> int:
        if self.redis and self.redis.connected:
            try:
                return await self.redis.incr(namespace, key, amount, ttl)
            except Exception:
                pass
        return self.memory.incr(namespace, key, amount, ttl)

    async def delete(self, namespace: str, key: str):
        if self.redis and self.redis.connected:
            await self.redis.delete(namespace, key)
        self.memory.delete(namespace, key)

    async def clear_namespace(self, namespace: str):
        if self.redis and self.redis.connected:
            await self.redis.clear_namespace(namespace)
        self.memory.clear_namespace(namespace)

    def stats(self) -> dict:
        return {
            "redis": self.redis.stats() if self.redis else None,
            "memory": self.memory.stats(),
        }


# Global cache instance
cache = UnifiedCache()


async def get_cache():
    return cache


async def init_cache(redis_url: str = None):
    await cache.initialize(redis_url)
    return cache
