"""Database indexing strategy for optimal performance and scalability."""

import logging

logger = logging.getLogger(__name__)


async def create_all_indexes(db):
    """
    Create all recommended indexes for optimal database performance.
    Call this during application startup in lifespan.
    
    Index strategy focused on:
    - Query performance (find operations)
    - Sorting efficiency
    - Aggregation pipeline optimization
    - TTL for temporary data
    """
    
    indexes_config = {
        # Users collection
        "users": [
            ({"email": 1}, {"unique": True}),
            ({"created_at": -1}, {}),
            ({"tier": 1, "created_at": -1}, {}),
            ({"is_active": 1, "last_login": -1}, {}),
            ({"referrer_id": 1}, {}),  # For referral tracking
        ],
        
        # Interview sessions
        "interviews": [
            ({"user_id": 1, "created_at": -1}, {}),
            ({"status": 1, "created_at": -1}, {}),
            ({"score": -1}, {}),  # For leaderboards
            ({"company": 1, "score": -1}, {}),
        ],
        
        # Resumes
        "resumes": [
            ({"user_id": 1, "created_at": -1}, {}),
            ({"ats_score": -1}, {}),
            ({"version": 1}, {}),
        ],
        
        # Questions/Problems
        "questions": [
            ({"difficulty": 1, "topic": 1}, {}),
            ({"company": 1, "difficulty": 1}, {}),
            ({"tags": 1}, {}),
            ({"solved_count": -1}, {}),
            ({"created_at": -1}, {}),
        ],
        
        # User progress/submissions
        "submissions": [
            ({"user_id": 1, "question_id": 1}, {}),
            ({"user_id": 1, "created_at": -1}, {}),
            ({"status": 1, "created_at": -1}, {}),
        ],
        
        # Gamification data
        "user_gamification": [
            ({"user_id": 1}, {"unique": True}),
            ({"xp": -1}, {}),  # For leaderboards
            ({"level": -1, "xp": -1}, {}),
            ({"streak": -1}, {}),
        ],
        
        # Company mocks
        "company_mocks": [
            ({"user_id": 1, "company": 1}, {}),
            ({"user_id": 1, "created_at": -1}, {}),
        ],
        
        # Billing/payments
        "billing_transactions": [
            ({"user_id": 1, "created_at": -1}, {}),
            ({"status": 1, "created_at": -1}, {}),
            ({"transaction_id": 1}, {"unique": True}),
            ({"payment_method": 1}, {}),
        ],
        
        # Feature flags
        "feature_flags": [
            ({"name": 1}, {"unique": True}),
            ({"status": 1}, {}),
        ],
        
        # Usage tracking
        "usage_logs": [
            ({"user_id": 1, "date": -1}, {}),
            ({"feature": 1, "date": -1}, {}),
            ({"created_at": -1}, {"expireAfterSeconds": 7776000}),  # 90 days TTL
        ],
        
        # Error logs
        "error_logs": [
            ({"request_id": 1}, {"unique": True}),
            ({"error_code": 1, "created_at": -1}, {}),
            ({"created_at": -1}, {"expireAfterSeconds": 2592000}),  # 30 days TTL
        ],
        
        # Idempotency keys
        "idempotency_keys": [
            ({"idempotency_key": 1}, {"unique": True}),
            ({"user_id": 1, "operation_type": 1}, {}),
            ({"expires_at": 1}, {"expireAfterSeconds": 0}),  # TTL
        ],
        
        # Referral data
        "referrals": [
            ({"referrer_id": 1, "created_at": -1}, {}),
            ({"referred_user_id": 1}, {"unique": True}),
            ({"status": 1}, {}),
        ],
        
        # Application tracking
        "applications": [
            ({"user_id": 1, "created_at": -1}, {}),
            ({"company": 1, "status": 1}, {}),
            ({"date_applied": -1}, {}),
        ],
        
        # Learning progress
        "learning_progress": [
            ({"user_id": 1, "module_id": 1}, {}),
            ({"user_id": 1, "language": 1}, {}),
            ({"user_id": 1, "completed_at": -1}, {}),
        ],
        
        # Community posts/discussions
        "community_posts": [
            ({"user_id": 1, "created_at": -1}, {}),
            ({"topic": 1, "created_at": -1}, {}),
            ({"upvotes": -1}, {}),
            ({"created_at": -1}, {}),
        ],
        
        # Analytics events
        "analytics_events": [
            ({"user_id": 1, "event_type": 1, "timestamp": -1}, {}),
            ({"event_type": 1, "timestamp": -1}, {}),
            ({"timestamp": -1}, {"expireAfterSeconds": 15552000}),  # 180 days TTL
        ],
    }
    
    try:
        for collection_name, indexes in indexes_config.items():
            collection = db[collection_name]
            
            for index_fields, options in indexes:
                try:
                    await collection.create_index(index_fields, **options)
                    logger.debug(f"Created index on {collection_name}: {index_fields}")
                except Exception as e:
                    logger.warning(f"Index creation warning for {collection_name}: {e}")
        
        logger.info(f"Successfully created indexes for {len(indexes_config)} collections")
        
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")
        raise


async def analyze_slow_queries(db):
    """
    Analyze and log slow queries for optimization.
    Should be run periodically or on-demand.
    """
    try:
        # Query system profiler data
        profile_db = db["system.profile"]
        
        # Find queries that took more than 100ms
        slow_queries = await profile_db.find({
            "millis": {"$gt": 100}
        }).limit(10).to_list(None)
        
        if slow_queries:
            logger.warning(f"Found {len(slow_queries)} slow queries (>100ms)")
            for query in slow_queries:
                logger.warning(f"Slow query: {query.get('command')} ({query.get('millis')}ms)")
        
    except Exception as e:
        logger.warning(f"Slow query analysis failed: {e}")


# Database connection optimization parameters
MONGODB_CONNECTION_SETTINGS = {
    "maxPoolSize": 50,  # Max connections in pool
    "minPoolSize": 10,  # Min connections kept alive
    "maxIdleTimeMS": 10000,  # Close idle connections after 10s
    "waitQueueTimeoutMS": 10000,  # Timeout for waiting for pool connection
    "retryWrites": True,  # Automatically retry failed writes
    "serverSelectionTimeoutMS": 5000,  # Timeout for server selection
    "socketTimeoutMS": 30000,  # Socket timeout
}

# Recommended MongoDB connection pool sizing
POOL_SIZING_GUIDE = """
Formula: connections_per_server = (CPU_COUNT * 2) + 1

Examples:
- 1 CPU: 3 connections
- 2 CPU: 5 connections
- 4 CPU: 9 connections
- 8 CPU: 17 connections

Current config: minPoolSize=10, maxPoolSize=50
This is suitable for 4-8 CPU applications.
"""
