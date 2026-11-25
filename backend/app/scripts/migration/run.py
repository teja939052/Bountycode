"""CLI entry point for the MongoDB → PostgreSQL migration engine.

Usage:
    python -m app.scripts.migration run --dry-run
    python -m app.scripts.migration run --domain identity
    python -m app.scripts.migration run --domain learning
    python -m app.scripts.migration run --all
    python -m app.scripts.migration run --domain identity --batch-size 50
    python -m app.scripts.migration run --checkpoint-clear identity
"""

import argparse
import asyncio
import json
import logging
import sys
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_engine, get_session_factory
from app.scripts.migration.checkpoint import clear as clear_checkpoint
from app.scripts.migration.domains import DOMAIN_COLLECTIONS, DOMAIN_ORDER, import_domain, import_identity
from app.scripts.migration.reader import MongoReader
from app.scripts.migration.reconciliation import run_reconciliation
from app.scripts.migration.types import ImportResult, ImportStatus

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("migration")


def _writer_cls_for_domain(domain: str) -> type:
    from app.scripts.migration.writer import WRITERS

    table_map = {
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
    table = table_map.get(domain)
    if not table:
        raise ValueError(f"Unknown domain: {domain}")
    return WRITERS[table]


async def _import_all(
    session: AsyncSession,
    reader: MongoReader,
    dry_run: bool,
    batch_size: int,
    domains: list[str],
) -> dict[str, ImportResult]:
    results: dict[str, ImportResult] = {}
    for domain in domains:
        logger.info("=== Importing domain: %s ===", domain)
        if domain not in DOMAIN_COLLECTIONS or not DOMAIN_COLLECTIONS[domain]:
            logger.info("Domain %s has no MongoDB collections — skipping", domain)
            results[domain] = ImportResult(
                domain=domain,
                status=ImportStatus.SKIPPED,
                error_messages=["No MongoDB collections configured — content comes from files"],
            )
            continue
        if domain == "identity":
            result = await import_identity(
                session, reader, batch_size=batch_size, dry_run=dry_run
            )
        else:
            writer_cls = _writer_cls_for_domain(domain)
            result = await import_domain(
                domain,
                session,
                reader,
                writer_cls,
                batch_size=batch_size,
                dry_run=dry_run,
            )
        results[domain] = result
        logger.info(
            "Domain %s: %s — imported=%d failed=%d quarantined=%d duplicates=%d",
            domain,
            result.status.value,
            result.imported_count,
            result.failed_count,
            result.quarantined_count,
            result.duplicate_count,
        )
        if result.error_messages:
            for err in result.error_messages[:5]:
                logger.warning("  error: %s", err)
    return results


async def run_migration(
    dry_run: bool = False,
    domain: Optional[str] = None,
    batch_size: int = 100,
    checkpoint_clear: Optional[str] = None,
) -> dict:
    if checkpoint_clear:
        clear_checkpoint(checkpoint_clear)
        logger.info("Cleared checkpoint for domain: %s", checkpoint_clear)
        return {"checkpoint_cleared": checkpoint_clear}

    reader = MongoReader(synthetic=True)  # Synthetic mode — MongoDB not running locally
    await reader.connect()

    try:
        factory = get_session_factory()
        async with factory() as session:
            domains = [domain] if domain else DOMAIN_ORDER
            results = await _import_all(
                session, reader, dry_run=dry_run,
                batch_size=batch_size, domains=domains,
            )

            if not dry_run:
                reconciliation = await run_reconciliation(
                    session, reader, results
                )
            else:
                reconciliation = {"dry_run": True, "message": "No reconciliation in dry-run mode"}

            return {
                "domains": {k: v.to_dict() for k, v in results.items()},
                "reconciliation": reconciliation,
            }
    finally:
        await reader.disconnect()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MongoDB → PostgreSQL migration engine (Phase 6)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run the migration")
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry-run mode — read source counts only, no writes",
    )
    run_parser.add_argument(
        "--domain",
        type=str,
        default=None,
        help="Import a single domain (e.g., identity, learning, assessments)",
    )
    run_parser.add_argument(
        "--all",
        action="store_true",
        help="Import all domains (default if --domain not specified)",
    )
    run_parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for reading/writing (default: 100)",
    )
    run_parser.add_argument(
        "--checkpoint-clear",
        type=str,
        default=None,
        help="Clear checkpoint for a domain and exit",
    )

    args = parser.parse_args()

    if args.command == "run":
        if args.checkpoint_clear:
            asyncio.run(run_migration(checkpoint_clear=args.checkpoint_clear))
            return

        result = asyncio.run(
            run_migration(
                dry_run=args.dry_run,
                domain=args.domain,
                batch_size=args.batch_size,
            )
        )
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
