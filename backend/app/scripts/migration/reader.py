"""MongoDB source readers using Motor (async driver).

Reads documents from MongoDB collections. Handles connection failures
gracefully and supports synthetic-data mode for testing without a live
MongoDB instance.
"""

import logging
from typing import Any, AsyncIterator, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId

logger = logging.getLogger(__name__)


class MongoReader:
    """Reads documents from MongoDB collections via Motor.

    In synthetic mode, generates placeholder documents instead of connecting
    to MongoDB — useful for testing the import pipeline offline.
    """

    def __init__(
        self,
        mongodb_url: str = "mongodb://localhost:27017",
        database_name: str = "placementpro",
        synthetic: bool = False,
    ):
        self.mongodb_url = mongodb_url
        self.database_name = database_name
        self.synthetic = synthetic
        self._client: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None

    async def connect(self) -> None:
        if self.synthetic:
            logger.info("MongoReader in synthetic mode — no connection")
            return
        if self._client is None:
            self._client = AsyncIOMotorClient(
                self.mongodb_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
            )
            self._db = self._client[self.database_name]
            await self._db.command("ping")
            logger.info("Connected to MongoDB: %s/%s", self.database_name, self.mongodb_url)

    async def disconnect(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None

    @property
    def db(self) -> AsyncIOMotorDatabase:
        if self._db is None:
            raise RuntimeError("MongoReader not connected — call connect() first")
        return self._db

    async def collection_count(self, collection_name: str) -> int:
        """Return document count for a collection (0 in synthetic mode)."""
        if self.synthetic:
            return 0
        return await self.db[collection_name].count_documents({})

    async def find_all(
        self,
        collection_name: str,
        batch_size: int = 100,
        after_id: Optional[str] = None,
    ) -> AsyncIterator[list[dict]]:
        """Yield batches of documents from a collection.

        In synthetic mode, yields nothing.
        """
        if self.synthetic:
            return
        query: dict[str, Any] = {}
        if after_id:
            try:
                query["_id"] = {"$gt": ObjectId(after_id)}
            except Exception:
                logger.warning("Invalid after_id %s — skipping resume filter", after_id)
        cursor = self.db[collection_name].find(query).sort("_id", 1).batch_size(batch_size)
        batch: list[dict] = []
        async for doc in cursor:
            batch.append(doc)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

    async def find_one(self, collection_name: str, query: dict) -> Optional[dict]:
        if self.synthetic:
            return None
        return await self.db[collection_name].find_one(query)
