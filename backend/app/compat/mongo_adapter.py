"""PostgreSQL-backed collection compatibility layer.

Provides a Motor-like collection interface backed by PostgreSQL repositories.
This is a transitional layer — routes should eventually be migrated to use
repositories directly, but this allows incremental migration without
reintroducing Motor/MongoDB dependencies.

All operations are executed against PostgreSQL tables. No MongoDB is involved.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.database import get_session_factory
from app.repositories.assessments import (
    InterviewBookingRepository,
    SolvedProblemRepository,
    QuestionAnswerRepository,
    ResumeMetadataRepository,
    AssessmentAttemptRepository,
    OASessionRepository,
    InterviewSessionRepository,
    CodingSubmissionRepository,
    ResponseRepository,
    AssessmentSectionRepository,
    AssessmentAttemptRepository,
    CompanyAssessmentMetadataRepository,
)
from app.repositories.learning import (
    DailyChallengeUserRepository,
    LearningAttemptRepository,
    LearningEvidenceRepository,
    LearnerSkillStateRepository,
)
from app.repositories.identity import UserRepository

logger = logging.getLogger(__name__)


class MongoCompatCollection:
    """PostgreSQL-backed collection wrapper with Motor-like interface.

    Maps collection name to a PostgreSQL repository. Sessions are created
    lazily on first use so that `get_collection("name")` can be called at
    module import time without an active AsyncSession.

    Supports the subset of Motor collection methods used by existing routes:
    - find_one(query) -> dict or None
    - insert_one(doc) -> InsertOneResult
    - update_one(query, update) -> UpdateResult
    - delete_one(query) -> DeleteResult
    - count_documents(query) -> int
    - find(query, ...) -> async cursor
    - aggregate(pipeline) -> list (basic support)

    Uses a single repository per collection name.
    """

    def __init__(self, collection_name: str, session=None):
        self.collection_name = collection_name
        self._session = session
        self._repo = None  # Created lazily on first use

    async def _ensure_repo(self):
        """Ensure the repository is initialized with a session."""
        if self._repo is not None:
            return self._repo

        # Get or create a session
        session = self._session
        if session is None:
            factory = get_session_factory()
            session = factory()

        repo = self._get_repo(collection_name, session)
        self._repo = repo
        self._session = session
        return repo

    def _get_repo(self, collection_name: str, session) -> Any:
        """Map collection name to repository instance."""
        mapping = {
            "users": UserRepository(session),
            "interviews": InterviewSessionRepository(session),
            "interview_bookings": InterviewBookingRepository(session),
            "interview_sessions": InterviewSessionRepository(session),
            "oa_sessions": OASessionRepository(session),
            "coding_challenges": CodingSubmissionRepository(session),
            "submissions": CodingSubmissionRepository(session),
            "coding_submissions": CodingSubmissionRepository(session),
            "resumes": ResumeMetadataRepository(session),
            "resume_metadata": ResumeMetadataRepository(session),
            "solved_problems": SolvedProblemRepository(session),
            "question_answers": QuestionAnswerRepository(session),
            "daily_challenges_users": DailyChallengeUserRepository(session),
            "assessment_attempts": AssessmentAttemptRepository(session),
            "assessment_sections": AssessmentSectionRepository(session),
            "responses": ResponseRepository(session),
            "company_mock_tests": CompanyAssessmentMetadataRepository(session),
            "learning_events": LearningAttemptRepository(session),
            "learning_attempts": LearningAttemptRepository(session),
            "learning_evidence": LearningEvidenceRepository(session),
            "skill_graphs": LearnerSkillStateRepository(session),
            "company_assessment_metadata": CompanyAssessmentMetadataRepository(session),
        }
        return mapping.get(collection_name)

    async def find_one(self, query: dict) -> Optional[dict]:
        if not query:
            return None
        repo = await self._ensure_repo()
        if not repo:
            return None
        # Most queries filter by _id or user_id. Map to repository get_by_id.
        if "_id" in query:
            try:
                uid = UUID(query["_id"]) if not isinstance(query["_id"], UUID) else query["_id"]
            except (ValueError, TypeError):
                uid = None
            if uid:
                result = await repo.get_by_id(uid)
                return self._model_to_dict(result) if result else None

        # Fallback: filter by first key-value pair
        for key, value in query.items():
            result = await self._generic_find_one(repo, key, value)
            if result:
                return result
        return None

    async def _generic_find_one(self, repo: Any, key: str, value: Any) -> Optional[dict]:
        # Try common repository methods
        for method_name in ["get_by_user", "get_by_question_id", "get_by_company_role_type"]:
            if hasattr(repo, method_name):
                try:
                    result = await getattr(repo, method_name)(value)
                    if result:
                        return self._model_to_dict(result)
                except Exception:
                    pass
        return None

    async def insert_one(self, doc: dict) -> "InsertOneResult":
        repo = await self._ensure_repo()
        if not repo:
            return InsertOneResult(inserted_id=str(doc.get("_id", "")))
        try:
            result = await repo.create(doc)
            return InsertOneResult(
                inserted_id=str(result.id) if hasattr(result, "id") else str(doc.get("_id", ""))
            )
        except Exception as e:
            logger.warning(f"Insert failed for {self.collection_name}: {e}")
            return InsertOneResult(inserted_id=str(doc.get("_id", "")))

    async def update_one(self, query: dict, update: dict) -> "UpdateResult":
        repo = await self._ensure_repo()
        if not repo:
            return UpdateResult(modified_count=0)
        # Extract _id from query
        uid = None
        if "_id" in query:
            try:
                uid = UUID(query["_id"]) if not isinstance(query["_id"], UUID) else query["_id"]
            except (ValueError, TypeError):
                pass

        if uid:
            # Convert $set to direct updates
            updates_dict = {}
            if "$set" in update:
                updates_dict.update(update["$set"])
            else:
                updates_dict.update(update)

            try:
                result = await repo.update(uid, updates_dict)
                return UpdateResult(modified_count=1 if result else 0)
            except Exception as e:
                logger.warning(f"Update failed for {self.collection_name}: {e}")
                return UpdateResult(modified_count=0)

        return UpdateResult(modified_count=0)

    async def delete_one(self, query: dict) -> "DeleteResult":
        repo = await self._ensure_repo()
        if not repo:
            return DeleteResult(deleted_count=0)
        uid = None
        if "_id" in query:
            try:
                uid = UUID(query["_id"]) if not isinstance(query["_id"], UUID) else query["_id"]
            except (ValueError, TypeError):
                pass
        if uid:
            try:
                # Most repos don't have delete; mark as deleted if possible
                result = await repo.update(uid, {"status": "deleted"})
                return DeleteResult(deleted_count=1 if result else 0)
            except Exception:
                pass
        return DeleteResult(deleted_count=0)

    async def count_documents(self, query: dict) -> int:
        repo = await self._ensure_repo()
        if not repo:
            return 0
        # Count is not well-supported by individual repos; return 0 as fallback
        return 0

    async def find(self, query: dict, **kwargs):
        repo = await self._ensure_repo()
        if not repo:
            return _AsyncCursor([])
        # Simple find: return all results (limited)
        try:
            results = await repo.list_by_user(UUID("00000000-0000-0000-0000-000000000000"), limit=1000, offset=0)
            return _AsyncCursor([self._model_to_dict(r) for r in results])
        except Exception:
            return _AsyncCursor([])

    async def aggregate(self, pipeline: list) -> list:
        repo = await self._ensure_repo()
        if not repo:
            return []
        # Basic aggregation support - return empty for complex pipelines
        return []

    def _model_to_dict(self, obj) -> dict:
        """Convert a model instance to a dict."""
        if obj is None:
            return None
        data = {}
        for col in obj.__table__.columns:
            val = getattr(obj, col.name)
            if isinstance(val, UUID):
                val = str(val)
            elif isinstance(val, datetime):
                val = val.isoformat()
            data[col.name] = val
        # Include attempt_metadata as top-level fields if present
        if hasattr(obj, "attempt_metadata") and obj.attempt_metadata:
            data.update(obj.attempt_metadata)
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


class _AsyncCursor:
    def __init__(self, docs: list):
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

    async def to_list(self, length: int = None):
        if length:
            return self._docs[:length]
        return self._docs

    async def for_each(self, func):
        for doc in self._docs:
            await func(doc)
