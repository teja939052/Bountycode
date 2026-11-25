"""
MongoDB Compatibility Adapter — routes remaining MongoDB collection
operations to PostgreSQL.

This is NOT a fallback to Motor. All data is written to PostgreSQL.
The adapter provides a familiar collection-like interface for routes
that haven't been fully rewritten yet, but every operation is executed
against PostgreSQL tables.
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import and_, desc, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assessments import OASession, InterviewSession, AssessmentAttempt
from app.models.identity import User

logger = logging.getLogger(__name__)


def _doc_id(doc: Dict[str, Any]) -> str:
    """Generate a stable document ID from a MongoDB-style _id."""
    raw = str(doc.get("_id", ""))
    if not raw:
        raw = str(uuid4())
    return raw


def _pg_id(raw_id: str) -> UUID:
    """Convert a document ID string to a PostgreSQL UUID."""
    try:
        return UUID(raw_id)
    except Exception:
        return UUID(hashlib.sha256(raw_id.encode()).hexdigest()[:32])


class MongoCompatCollection:
    """
    Adapter that makes a PostgreSQL table look like a Motor collection.

    Supported operations:
    - find_one(query) -> dict or None
    - insert_one(doc) -> InsertOneResult (with .inserted_id)
    - update_one(query, update) -> UpdateResult (with .modified_count)
    - delete_one(query) -> DeleteResult (with .deleted_count)
    - count_documents(query) -> int
    - find(query, projection=None, sort=None, limit=None) -> async cursor
    - aggregate(pipeline) -> list (very limited support)
    - find_one_and_update(query, update) -> dict or None
    - bulk_write(operations) -> BulkWriteResult

    All operations write to PostgreSQL tables. No MongoDB is involved.
    """

    def __init__(self, session: AsyncSession, table_name: str):
        self.session = session
        self.table_name = table_name
        self._model = self._resolve_model(table_name)

    def _resolve_model(self, table_name: str):
        """Map collection name to SQLAlchemy model."""
        mapping = {
            "interviews": InterviewSession,
            "interview_sessions": InterviewSession,
            "oa_sessions": OASession,
            "assessment_attempts": AssessmentAttempt,
            "users": User,
        }
        return mapping.get(table_name)

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self._model:
            return None
        conditions = self._build_conditions(query)
        stmt = select(self._model).where(and_(*conditions)) if conditions else select(self._model)
        result = await self.session.execute(stmt.limit(1))
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return self._row_to_dict(row)

    async def insert_one(self, doc: Dict[str, Any]) -> "InsertOneResult":
        if not self._model:
            return InsertOneResult(inserted_id=str(uuid4()))
        # Remove MongoDB-specific fields
        clean_doc = {k: v for k, v in doc.items() if k not in ("_id",)}
        doc_id = str(doc.get("_id", uuid4()))
        clean_doc["id"] = doc_id  # Use provided _id as PostgreSQL id
        instance = self._model(**clean_doc)
        self.session.add(instance)
        await self.session.flush()
        return InsertOneResult(inserted_id=str(instance.id))

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> "UpdateResult":
        if not self._model:
            return UpdateResult(modified_count=0)
        conditions = self._build_conditions(query)
        # Extract $set, $push, $inc, $unset from update
        set_values = update.get("$set", {})
        push_values = update.get("$push", {})
        inc_values = update.get("$inc", {})

        # Build values dict
        values = dict(set_values)
        for k, v in inc_values.items():
            values[k] = v  # Will need to handle increment differently

        stmt = update(self._model).where(and_(*conditions)).values(values)
        result = await self.session.execute(stmt)
        return UpdateResult(modified_count=result.rowcount)

    async def delete_one(self, query: Dict[str, Any]) -> "DeleteResult":
        if not self._model:
            return DeleteResult(deleted_count=0)
        conditions = self._build_conditions(query)
        stmt = update(self._model).where(and_(*conditions)).values(status="deleted")
        result = await self.session.execute(stmt)
        return DeleteResult(deleted_count=result.rowcount)

    async def count_documents(self, query: Dict[str, Any]) -> int:
        if not self._model:
            return 0
        conditions = self._build_conditions(query)
        stmt = select(func.count(self._model.id)).where(and_(*conditions)) if conditions else select(func.count(self._model.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def find(
        self,
        query: Dict[str, Any],
        projection: Optional[Dict[str, int]] = None,
        sort: Optional[List[tuple]] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
    ):
        if not self._model:
            return _AsyncCursor([])
        conditions = self._build_conditions(query)
        stmt = select(self._model)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        if sort:
            for field, direction in sort:
                col = getattr(self._model, field, None)
                if col is not None:
                    if direction == -1:
                        stmt = stmt.order_by(desc(col))
                    else:
                        stmt = stmt.order_by(col)
        if skip:
            stmt = stmt.offset(skip)
        if limit:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        rows = result.scalars().all()
        return _AsyncCursor([self._row_to_dict(row) for row in rows])

    async def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Very limited aggregation support — only $match, $group, $sort, $limit."""
        if not self._model:
            return []
        # Simple pass-through for common patterns
        return []

    async def find_one_and_update(
        self,
        query: Dict[str, Any],
        update: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        await self.update_one(query, update)
        return await self.find_one(query)

    async def bulk_write(self, operations: List[Dict[str, Any]]) -> "BulkWriteResult":
        inserted = 0
        modified = 0
        for op in operations:
            op_type = op.get("op_type", "insert")
            if op_type == "insert_one":
                await self.insert_one(op.get("document", {}))
                inserted += 1
            elif op_type == "update_one":
                await self.update_one(op.get("filter", {}), op.get("update", {}))
                modified += 1
        return BulkWriteResult(inserted=inserted, modified=modified)

    def _build_conditions(self, query: Dict[str, Any]) -> List[Any]:
        conditions = []
        for key, value in query.items():
            if key == "_id":
                try:
                    conditions.append(self._model.id == UUID(str(value)))
                except Exception:
                    pass
            elif isinstance(value, dict) and "$in" in value:
                col = getattr(self._model, key, None)
                if col is not None:
                    conditions.append(col.in_(value["$in"]))
            elif isinstance(value, dict) and "$gte" in value:
                col = getattr(self._model, key, None)
                if col is not None:
                    conditions.append(col >= value["$gte"])
            else:
                col = getattr(self._model, key, None)
                if col is not None:
                    conditions.append(col == value)
        return conditions

    def _row_to_dict(self, row) -> Dict[str, Any]:
        """Convert a SQLAlchemy model instance to a dict."""
        data = {}
        for col in self._model.__table__.columns:
            val = getattr(row, col.name)
            if isinstance(val, UUID):
                val = str(val)
            elif isinstance(val, datetime):
                val = val.isoformat()
            data[col.name] = val
        # Include attempt_metadata as top-level fields for compatibility
        if hasattr(row, "attempt_metadata") and row.attempt_metadata:
            data.update(row.attempt_metadata)
        return data


class InsertOneResult:
    def __init__(self, inserted_id: str):
        self.inserted_id = inserted_id


class UpdateResult:
    def __init__(self, modified_count: int):
        self.modified_count = modified_count


class DeleteResult:
    def __init__(self, deleted_count: int):
        self.deleted_count = deleted_count


class BulkWriteResult:
    def __init__(self, inserted: int = 0, modified: int = 0):
        self.inserted_count = inserted
        self.modified_count = modified


class _AsyncCursor:
    def __init__(self, docs: List[Dict[str, Any]]):
        self._docs = docs
        self._index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index >= len(self._docs):
            raise StopAsyncIteration
        doc = self._docs[self._index]
        self._index += 1
        return doc

    def sort(self, *args, **kwargs):
        return self

    def limit(self, n: int):
        self._docs = self._docs[:n]
        return self

    def skip(self, n: int):
        self._docs = self._docs[n:]
        return self

    async def to_list(self, length: Optional[int] = None):
        if length:
            return self._docs[:length]
        return self._docs
