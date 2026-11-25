"""Per-domain import orchestration.

Each domain import function coordinates:
1. Read from MongoDB source (MongoReader)
2. Transform (transformers module)
3. Map legacy IDs → PostgreSQL UUIDs (UserIdentityMap)
4. Write to PostgreSQL (writer module)
5. Track checkpoints for resumption
"""

import logging
import time
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.scripts.migration.checkpoint import mark_completed, mark_in_progress, load
from app.scripts.migration.reader import MongoReader
from app.scripts.migration.transformers import TRANSFORMERS
from app.scripts.migration.types import ImportResult, ImportStatus
from app.scripts.migration.writer import PostgresWriter, UserWriter, WRITERS

logger = logging.getLogger(__name__)

DOMAIN_ORDER = [
    "identity",
    "gamification",
    "skills",
    "content",
    "gamification_events",
    "skill_states",
    "learning_attempts",
    "learning_evidence",
    "mastery_snapshots",
    "srs_cards",
    "repair_missions",
    "assessment_definitions",
    "assessment_attempts",
    "responses",
    "coding_submissions",
    "execution_results",
    "oa_sessions",
    "interviews",
    "company_assessment_metadata",
    "career_profiles",
    "resumes",
    "analytics",
    "audit_logs",
]

DOMAIN_COLLECTIONS = {
    "identity": ["users"],
    "gamification": ["gamification"],
    "gamification_events": ["gamification_events"],
    "skills": ["skill_graphs"],
    "learning_attempts": ["learning_events"],
    "coding_submissions": ["coding_challenges", "submissions"],
    "assessment_attempts": ["aptitude_tests", "company_mock_tests"],
    "oa_sessions": ["oa_sessions"],
    "interviews": ["interviews", "interview_bookings", "interview_chat_sessions"],
    "career_profiles": ["career_profiles"],
    "resumes": ["resumes"],
    "payments": ["payments"],
    "repair_missions": ["repair_missions"],
    "srs_cards": ["srs_cards"],
    "analytics": ["analytics_events", "analytics_rollups"],
    "audit_logs": ["audit_logs"],
    "coupons": ["coupons"],
}

DOMAIN_WRITERS = {
    "identity": "users",
    "gamification": "gamification_profiles",
    "gamification_events": "xp_event_ledger",
    "skills": "skills",
    "learning_attempts": "learning_attempts",
    "coding_submissions": "coding_submissions",
    "execution_results": "execution_results",
    "assessment_attempts": "assessment_attempts",
    "oa_sessions": "oa_sessions",
    "interviews": "interview_sessions",
    "career_profiles": "career_profiles",
    "resumes": "resumes",
    "payments": "payments",
    "repair_missions": "repair_missions",
    "srs_cards": "srs_cards",
    "analytics": "analytics_events",
    "audit_logs": "audit_logs",
    "coupons": "coupons",
}


async def import_domain(
    domain: str,
    session: AsyncSession,
    reader: MongoReader,
    writer_cls: type[PostgresWriter],
    batch_size: int = 100,
    dry_run: bool = False,
) -> ImportResult:
    start = time.time()
    result = ImportResult(domain=domain, status=ImportStatus.IN_PROGRESS)

    collections = DOMAIN_COLLECTIONS.get(domain, [])
    if not collections:
        result.status = ImportStatus.FAILED
        result.error_messages.append(f"No collections configured for domain {domain}")
        return result

    checkpoint = load(domain)
    after_id = checkpoint.last_processed_id if checkpoint else None

    if dry_run:
        logger.info("DRY-RUN: would import domain %s from collections %s", domain, collections)
        for coll in collections:
            count = await reader.collection_count(coll)
            result.source_count += count
        result.status = ImportStatus.COMPLETED
        result.duration_seconds = time.time() - start
        return result

    writer: PostgresWriter = writer_cls(session)

    total_imported = 0
    total_failed = 0
    total_quarantined = 0
    total_duplicates = 0
    all_errors: list[str] = []

    for coll_name in collections:
        transformer = TRANSFORMERS.get(coll_name)
        if not transformer:
            logger.warning("No transformer for collection %s — skipping", coll_name)
            continue

        table = DOMAIN_WRITERS.get(domain)
        if not table:
            logger.warning("No writer table for domain %s — skipping", domain)
            continue

        async for batch in reader.find_all(coll_name, batch_size=batch_size, after_id=after_id):
            result.source_count += len(batch)
            records_to_write: list[dict] = []

            for doc in batch:
                legacy_id = str(doc.get("_id", ""))
                if not legacy_id:
                    total_quarantined += 1
                    continue

                if domain == "identity":
                    existing = await writer.resolve_postgres_user_id(legacy_id)
                    if existing:
                        total_duplicates += 1
                        continue

                try:
                    data, quarantine_reason = transformer(doc)
                except Exception as exc:
                    logger.exception("Transform failed for %s/%s", coll_name, legacy_id)
                    total_quarantined += 1
                    all_errors.append(f"{coll_name}/{legacy_id}: transform error: {exc}")
                    continue

                if quarantine_reason:
                    total_quarantined += 1
                    all_errors.append(f"{coll_name}/{legacy_id}: {quarantine_reason}")
                    continue

                if domain == "identity":
                    try:
                        user = await writer.write_record(table, data)
                        await writer.create_identity_map(legacy_id, user.id)
                        total_imported += 1
                    except Exception as exc:
                        total_failed += 1
                        all_errors.append(f"{coll_name}/{legacy_id}: write error: {exc}")
                        await session.rollback()
                    continue

                mongo_user_id = doc.get("user_id")
                pg_user_id: Optional[UUID] = None
                if mongo_user_id:
                    pg_user_id = await writer.resolve_postgres_user_id(str(mongo_user_id))
                    if pg_user_id:
                        data["user_id"] = pg_user_id

                try:
                    await writer.write_record(table, data)
                    total_imported += 1
                except Exception as exc:
                    total_failed += 1
                    all_errors.append(f"{coll_name}/{legacy_id}: write error: {exc}")
                    await session.rollback()

            if batch:
                last_doc = batch[-1]
                after_id = str(last_doc.get("_id", after_id))
                mark_in_progress(domain, total_imported, after_id)

    result.imported_count = total_imported
    result.failed_count = total_failed
    result.quarantined_count = total_quarantined
    result.duplicate_count = total_duplicates
    result.error_messages = all_errors[:50]
    result.duration_seconds = time.time() - start

    if total_failed > 0 and total_imported == 0:
        result.status = ImportStatus.FAILED
    else:
        result.status = ImportStatus.COMPLETED

    mark_completed(domain, total_imported, after_id)
    return result


async def import_identity(
    session: AsyncSession,
    reader: MongoReader,
    batch_size: int = 100,
    dry_run: bool = False,
) -> ImportResult:
    return await import_domain(
        domain="identity",
        session=session,
        reader=reader,
        writer_cls=UserWriter,
        batch_size=batch_size,
        dry_run=dry_run,
    )
