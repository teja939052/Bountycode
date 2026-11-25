"""MongoDB → PostgreSQL migration engine — Phase 6.

Package for the data migration system. Provides source readers, domain
transformers, PostgreSQL writers, identity mapping, checkpoints,
reconciliation, and a CLI entry point.

Usage:
    python -m app.scripts.migration run --dry-run
    python -m app.scripts.migration run --domain identity
    python -m app.scripts.migration run --domain learning
    python -m app.scripts.migration run --all
"""

from app.scripts.migration.run import main

__all__ = ["main"]
