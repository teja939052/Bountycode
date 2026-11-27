"""Audit logging service for admin actions. PostgreSQL-backed."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session, RepositoryBase
from app.models.operations import AuditLog

logger = logging.getLogger(__name__)


class AuditLogRepository(RepositoryBase):
    """Repository for audit log entries."""

    async def create(self, user_id: str, action: str, resource: str,
                     resource_id: Optional[str] = None,
                     details: Optional[Dict[str, Any]] = None,
                     ip_address: Optional[str] = None) -> AuditLog:
        doc = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address or "unknown",
            timestamp=datetime.now(timezone.utc),
        )
        self.session.add(doc)
        await self.flush()
        return doc

    async def get_by_user(self, user_id: str, limit: int = 50, offset: int = 0) -> list:
        result = await self.session.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_by_action(self, action: str, limit: int = 50, offset: int = 0) -> list:
        result = await self.session.execute(
            select(AuditLog)
            .where(AuditLog.action == action)
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_recent(self, limit: int = 50) -> list:
        result = await self.session.execute(
            select(AuditLog)
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()



async def log_audit(
    user_id: str,
    action: str,
    resource: str,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
) -> None:
    """Log an admin action to the audit logs."""
    try:
        async with get_session() as session:
            repo = AuditLogRepository(session)
            await repo.create(user_id, action, resource, resource_id, details, ip_address)
    except Exception as e:
        logger.warning(f"Failed to log audit entry: {e}")


async def get_audit_logs(
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list:
    """Retrieve audit logs with optional filtering."""
    async with get_session() as session:
        repo = AuditLogRepository(session)
        query = select(AuditLog)

        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        if action:
            query = query.where(AuditLog.action == action)

        result = await session.execute(
            query.order_by(AuditLog.timestamp.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()