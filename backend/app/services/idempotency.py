"""Idempotency key system to prevent duplicate payments and API calls."""

import logging
import hashlib
from datetime import datetime, timedelta

from app.utils.timeutil import utcnow
from typing import Optional, Any, Dict
from enum import Enum

logger = logging.getLogger(__name__)


class IdempotencyStatus(str, Enum):
    """Status of an idempotent operation."""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class IdempotencyManager:
    """Manages idempotency keys to ensure safe retries and prevent duplicates."""

    def __init__(self, db=None):
        self.db = db
        self.ttl_seconds = 86400  # 24 hours
        self.collection_name = "idempotency_keys"

    async def create_key(
        self,
        user_id: str,
        operation_type: str,
        operation_data: Dict[str, Any],
    ) -> str:
        """Create an idempotency key for an operation."""
        # Generate key from user_id + operation_type + hash of data
        data_hash = hashlib.sha256(
            str(operation_data).encode()
        ).hexdigest()[:16]
        
        idempotency_key = f"{user_id}_{operation_type}_{data_hash}"
        
        return idempotency_key

    async def record_operation(
        self,
        idempotency_key: str,
        user_id: str,
        operation_type: str,
        status: IdempotencyStatus,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> bool:
        """Record an operation with its result."""
        if not self.db:
            logger.warning("Idempotency manager not connected to database")
            return False

        try:
            collection = self.db[self.collection_name]
            
            # Check if already exists
            existing = await collection.find_one({"idempotency_key": idempotency_key})
            
            if existing:
                logger.warning(f"Idempotency key already recorded: {idempotency_key}")
                return False  # Already processed

            await collection.insert_one({
                "idempotency_key": idempotency_key,
                "user_id": user_id,
                "operation_type": operation_type,
                "status": status.value,
                "result": result,
                "error": error,
                "created_at": utcnow(),
                "expires_at": utcnow() + timedelta(seconds=self.ttl_seconds),
            })

            logger.info(f"Recorded idempotent operation: {idempotency_key}")
            return True

        except Exception as e:
            logger.error(f"Failed to record idempotency key: {e}")
            return False

    async def get_operation_result(
        self,
        idempotency_key: str,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve cached result for idempotency key."""
        if not self.db:
            return None

        try:
            collection = self.db[self.collection_name]
            
            operation = await collection.find_one(
                {"idempotency_key": idempotency_key},
            )
            
            if not operation:
                return None

            # Check if expired
            if operation.get("expires_at") < utcnow():
                await collection.delete_one({"idempotency_key": idempotency_key})
                return None

            return {
                "status": operation.get("status"),
                "result": operation.get("result"),
                "error": operation.get("error"),
            }

        except Exception as e:
            logger.error(f"Failed to retrieve idempotency result: {e}")
            return None

    async def has_duplicate_request(
        self,
        idempotency_key: str,
    ) -> bool:
        """Check if request with this key has already been processed."""
        result = await self.get_operation_result(idempotency_key)
        return result is not None


# Global idempotency manager
_idempotency_manager: Optional[IdempotencyManager] = None


async def init_idempotency_manager(db):
    """Initialize global idempotency manager."""
    global _idempotency_manager
    _idempotency_manager = IdempotencyManager(db)
    
    # Create TTL index for automatic expiration
    try:
        collection = db["idempotency_keys"]
        await collection.create_index("expires_at", expireAfterSeconds=0)
        logger.info("Idempotency manager initialized with TTL index")
    except Exception as e:
        logger.warning(f"Failed to create TTL index: {e}")


def get_idempotency_manager() -> IdempotencyManager:
    """Get global idempotency manager."""
    if _idempotency_manager is None:
        raise RuntimeError("Idempotency manager not initialized")
    return _idempotency_manager
