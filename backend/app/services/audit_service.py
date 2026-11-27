"""Audit service — PostgreSQL-backed, replaces MongoDB collection operations."""
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session, RepositoryBase
from app.models.audit_log import AuditLog

logger = logging.getLogger(__name__)