"""MongoDB compatibility adapter package.

Routes remaining MongoDB collection operations to PostgreSQL tables.
Not a Motor fallback — all writes go to PostgreSQL.
"""

from app.compat.mongo_adapter import (
    MongoCompatCollection,
    InsertOneResult,
    UpdateResult,
    DeleteResult,
    BulkWriteResult,
)

__all__ = [
    "MongoCompatCollection",
    "InsertOneResult",
    "UpdateResult",
    "DeleteResult",
    "BulkWriteResult",
]
