"""Reconciliation reports — compare source MongoDB counts with imported counts.

All reports are redacted — no personal data, password hashes, or tokens
are included in reconciliation output.
"""

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.scripts.migration.checkpoint import load
from app.scripts.migration.reader import MongoReader
from app.scripts.migration.types import ImportResult

logger = logging.getLogger(__name__)


class ReconciliationReport:
    def __init__(self, session: AsyncSession, reader: MongoReader):
        self.session = session
        self.reader = reader
        self.domain_reports: list[dict] = []

    async def reconcile_domain(
        self,
        domain: str,
        imported_count: int,
        source_collections: list[str],
    ) -> dict:
        source_count = 0
        for coll in source_collections:
            try:
                count = await self.reader.collection_count(coll)
                source_count += count
            except Exception as exc:
                logger.warning("Could not count %s: %s", coll, exc)

        skipped = max(0, source_count - imported_count)
        match = source_count == imported_count

        report = {
            "domain": domain,
            "source_count": source_count,
            "imported_count": imported_count,
            "skipped_count": skipped,
            "match": match,
            "collections": source_collections,
        }
        self.domain_reports.append(report)
        return report

    async def build(self) -> dict:
        total_source = 0
        total_imported = 0
        total_skipped = 0
        all_match = True

        for report in self.domain_reports:
            total_source += report["source_count"]
            total_imported += report["imported_count"]
            total_skipped += report["skipped_count"]
            if not report["match"]:
                all_match = False

        return {
            "total_source_count": total_source,
            "total_imported_count": total_imported,
            "total_skipped_count": total_skipped,
            "all_match": all_match,
            "domains": self.domain_reports,
        }

    def redact(self, data: Any) -> Any:
        if isinstance(data, dict):
            redacted = {}
            for k, v in data.items():
                k_lower = k.lower()
                if any(s in k_lower for s in ("password", "token", "secret", "key", "email", "hash")):
                    redacted[k] = "[REDACTED]"
                else:
                    redacted[k] = self.redact(v)
            return redacted
        if isinstance(data, list):
            return [self.redact(item) for item in data]
        return data


async def run_reconciliation(
    session: AsyncSession,
    reader: MongoReader,
    domain_results: dict[str, ImportResult],
) -> dict:
    report = ReconciliationReport(session, reader)

    domain_collections = {
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

    for domain, result in domain_results.items():
        collections = domain_collections.get(domain, [])
        await report.reconcile_domain(domain, result.imported_count, collections)

    return await report.build()
