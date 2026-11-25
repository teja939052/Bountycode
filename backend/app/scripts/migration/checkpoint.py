"""Checkpoint persistence for resumable imports.

Checkpoints are stored as JSON files under backend/data/migration_checkpoints/.
Each domain has its own checkpoint file. On resume, the importer reads the
checkpoint and skips already-processed documents.
"""

import json
import os
from datetime import datetime, timezone
from typing import Optional

from app.scripts.migration.types import Checkpoint

CHECKPOINT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "backend", "data", "migration_checkpoints"
)


def _ensure_dir() -> None:
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)


def _path(domain: str) -> str:
    return os.path.join(CHECKPOINT_DIR, f"{domain}.json")


def save(domain: str, checkpoint: Checkpoint) -> None:
    _ensure_dir()
    checkpoint.updated_at = datetime.now(timezone.utc).isoformat()
    with open(_path(domain), "w", encoding="utf-8") as f:
        json.dump(checkpoint.to_dict(), f, indent=2)


def load(domain: str) -> Optional[Checkpoint]:
    path = _path(domain)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Checkpoint.from_dict(data)


def mark_completed(domain: str, processed_count: int, last_id: Optional[str] = None) -> None:
    cp = load(domain) or Checkpoint(domain=domain)
    cp.processed_count = processed_count
    cp.last_processed_id = last_id
    cp.completed = True
    save(domain, cp)


def mark_in_progress(domain: str, processed_count: int, last_id: Optional[str] = None) -> None:
    cp = load(domain) or Checkpoint(domain=domain)
    cp.processed_count = processed_count
    cp.last_processed_id = last_id
    cp.completed = False
    save(domain, cp)


def clear(domain: str) -> None:
    path = _path(domain)
    if os.path.exists(path):
        os.remove(path)
