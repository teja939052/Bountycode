"""Database indexing strategy for optimal performance and scalability.

PostgreSQL indexes are defined declaratively in SQLAlchemy models and managed
via Alembic migrations. This module is retained for import compatibility only.
"""

import logging

logger = logging.getLogger(__name__)


async def create_all_indexes(db):
    """No-op: PostgreSQL indexes are managed by SQLAlchemy/Alembic, not MongoDB."""
    logger.info("PostgreSQL indexes are managed declaratively via models + Alembic")
    return None
