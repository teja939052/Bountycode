"""
Cache decorator for FastAPI routes.
Usage: @cached(ttl=300, key_prefix="questions")
"""
import functools
from app.services.cache import cache


def cached(ttl: int = 300, key_prefix: str = ""):
    """Cache route response in UnifiedCache. TTL in seconds."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key_parts = [key_prefix or func.__name__]
            for arg in args:
                if isinstance(arg, (str, int, float, bool)):
                    key_parts.append(str(arg))
            for k, v in sorted(kwargs.items()):
                if k != "current_user" and isinstance(v, (str, int, float, bool)):
                    key_parts.append(f"{k}={v}")
            cache_key = ":".join(key_parts)

            cached_result = await cache.get("resp", cache_key)
            if cached_result is not None:
                return cached_result

            result = await func(*args, **kwargs)

            if isinstance(result, (dict, list)):
                await cache.set("resp", cache_key, result, ttl=ttl)

            return result
        return wrapper
    return decorator


async def invalidate_prefix(prefix: str):
    """Clear all cached responses matching a prefix (namespace 'resp')."""
    await cache.clear_namespace(f"resp:{prefix}")


async def invalidate_questions_cache():
    """Clear all question bank cached responses."""
    await invalidate_prefix("questions")


async def invalidate_gamification_cache():
    """Clear gamification-related cached responses."""
    await invalidate_prefix("gamification")
