"""Shared types for the migration engine."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ImportStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class DomainStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class ImportResult:
    """Result of importing a single domain."""

    domain: str
    status: ImportStatus
    source_count: int = 0
    imported_count: int = 0
    skipped_count: int = 0
    quarantined_count: int = 0
    duplicate_count: int = 0
    failed_count: int = 0
    error_messages: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "status": self.status.value,
            "source_count": self.source_count,
            "imported_count": self.imported_count,
            "skipped_count": self.skipped_count,
            "quarantined_count": self.quarantined_count,
            "duplicate_count": self.duplicate_count,
            "failed_count": self.failed_count,
            "error_messages": self.error_messages,
            "duration_seconds": self.duration_seconds,
        }

    @property
    def success_rate(self) -> float:
        if self.source_count == 0:
            return 1.0
        return self.imported_count / self.source_count


@dataclass
class Checkpoint:
    """Persistent checkpoint for resumable imports."""

    domain: str
    last_processed_id: Optional[str] = None
    processed_count: int = 0
    completed: bool = False
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "last_processed_id": self.last_processed_id,
            "processed_count": self.processed_count,
            "completed": self.completed,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Checkpoint":
        return cls(
            domain=data["domain"],
            last_processed_id=data.get("last_processed_id"),
            processed_count=data.get("processed_count", 0),
            completed=data.get("completed", False),
            updated_at=data.get("updated_at"),
        )


@dataclass
class QuarantineRecord:
    """A record that could not be imported and was quarantined."""

    collection: str
    document_id: str
    reason: str
    redacted_data: dict

    def to_dict(self) -> dict:
        return {
            "collection": self.collection,
            "document_id": self.document_id,
            "reason": self.reason,
            "redacted_data": self.redacted_data,
        }
