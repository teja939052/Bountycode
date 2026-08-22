# Redis Production Configuration

## Current State
Redis is installed as a dependency (`redis[hiredis]==5.0.0`) and used for:
- Distributed rate limiting (replaces in-memory deques)
- Session cache (JWT blacklist / refresh token jti)
- AI response caching (1-hour TTL)
- General purpose cache namespace

The application gracefully falls back to in-memory cache when Redis is unavailable.

## Production Setup

### 1. Redis Server
```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Verify
redis-cli ping
# → PONG
```

### 2. Environment Variables
```env
REDIS_URL=redis://localhost:6379/0
```

For managed Redis (Upstash, Redis Cloud, ElastiCache):
```env
REDIS_URL=redis://default:password@redis-host:6379/0
```

### 3. Connection Pooling
The `RedisCache` class in `services/cache.py` uses `redis.asyncio` with:
- `socket_connect_timeout=5`
- `socket_timeout=5`
- `retry_on_timeout=True`

For production, consider adding:
```python
# In services/cache.py RedisCache.connect()
self.client = aioredis.from_url(
    self.redis_url,
    encoding="utf-8",
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True,
    max_connections=20,  # Add this
    health_check_interval=30,  # Add this
)
```

### 4. Rate Limiting with Redis
Enable Redis-backed rate limiting in production:
```python
# In middleware/rate_limiter.py
RateLimiterMiddleware(app, use_redis=True)  # Pass True in production
```

### 5. Monitoring
- Redis `INFO` command for memory/connections
- Set `maxmemory` and `maxmemory-policy` (e.g., `allkeys-lru`)
- Monitor hit rate via `cache.stats()`

### 6. Security
- Bind Redis to localhost or private network only
- Use Redis AUTH in production
- Enable TLS for managed Redis (use `rediss://` scheme)
