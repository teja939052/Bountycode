"""Evidence aggregator service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def aggregate_evidence(user_id: str) -> dict:
    """Aggregate learning evidence for user."""
    async with get_session() as session:
        from app.models.learning_evidence import LearningEvidence
        from sqlalchemy import select
        result = await session.execute(
            select(LearningEvidence).where(LearningEvidence.user_id == user_id)
        )
        evidence = result.scalars().all()
    return {
        "user_id": user_id,
        "evidence_count": len(evidence),
        "evidence": [{"id": str(e.id), "type": e.evidence_type, "created_at": e.created_at.isoformat() if e.created_at else None} for e in evidence],
    }


async def record_evidence(
    user_id: str,
    evidence_type: str,
    evidence_data: dict,
) -> dict:
    """Record learning evidence."""
    async with get_session() as session:
        from app.models.learning_evidence import LearningEvidence
        evidence = LearningEvidence(
            user_id=user_id,
            evidence_type=evidence_type,
            evidence_data=evidence_data,
            created_at=datetime.now(timezone.utc),
        )
        session.add(evidence)
        await session.commit()
    return {"user_id": user_id, "evidence_id": str(evidence.id), "recorded": True}