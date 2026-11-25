"""PostgreSQL compatibility adapter package.

Routes remaining MongoDB collection operations to PostgreSQL tables.
Not a Motor fallback — all writes go to PostgreSQL tables.
"""

from app.compat.mongo_adapter import (
    MongoCompatCollection,
    InsertOneResult,
    UpdateResult,
    DeleteResult,
    _AsyncCursor,
)

__all__ = [
    "MongoCompatCollection",
    "InsertOneResult",
    "UpdateResult",
    "DeleteResult",
    "_AsyncCursor",
]
