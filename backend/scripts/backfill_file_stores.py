"""One-time backfill: file stores -> Mongo (§1.1 migration).

Idempotent: every insert is skip-if-exists (unique indexes / pre-checks).
Files remain as seed/export artifacts; request code no longer writes them.

  question_reports.json  -> question_reports
  served_quarantine.json -> served_quarantine   (file `id` -> `question_id`)
  data/invoices/*.json   -> invoices            (keyed by invoice_id)
  tranche_staging/*.json -> content_tranches    (keyed by tranche_id)
  tranche_promoted.json  -> NOT migrated (question content; Residency Rule:
                           stays a versioned file, loaded at startup)
"""
import asyncio
import json
import os
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))
DATA = BACKEND_ROOT / "app" / "data"


def _read_list(path: Path) -> list:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"  skip {path.name}: {e}")
        return []


async def main() -> None:
    from app.database import (
        question_reports_collection as reports,
        served_quarantine_collection as quar,
        invoices_collection as invs,
        content_tranches_collection as tranches,
    )
    stats = {}

    # 1. reports
    rows = _read_list(DATA / "question_reports.json")
    n = 0
    for r in rows:
        if not isinstance(r, dict) or not r.get("question_id") or not r.get("user_id"):
            continue
        try:
            await reports.update_one(
                {"user_id": r["user_id"], "question_id": r["question_id"]},
                {"$setOnInsert": {
                    "question_id": r["question_id"], "user_id": r["user_id"],
                    "reason": str(r.get("reason", ""))[:500],
                    "day": r.get("day", ""), "created_at": r.get("created_at", "")}},
                upsert=True)
            n += 1
        except Exception as e:
            print(f"  report insert err: {e}")
            break
    stats["reports"] = n

    # 2. quarantine (file `id` -> `question_id`)
    rows = _read_list(DATA / "served_quarantine.json")
    n = 0
    for r in rows:
        if not isinstance(r, dict) or not r.get("id"):
            continue
        try:
            await quar.update_one(
                {"question_id": str(r["id"])},
                {"$setOnInsert": {
                    "question_id": str(r["id"]),
                    "reason": str(r.get("reason", "backfill"))[:300],
                    "title": str(r.get("title", ""))[:80]}},
                upsert=True)
            n += 1
        except Exception as e:
            print(f"  quarantine insert err: {e}")
            break
    stats["quarantine"] = n

    # 3. invoices
    inv_dir = DATA / "invoices"
    n = 0
    if inv_dir.is_dir():
        for fn in sorted(os.listdir(inv_dir)):
            if not fn.endswith(".json"):
                continue
            try:
                inv = json.loads((inv_dir / fn).read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  invoice parse err {fn}: {e}")
                continue
            if not isinstance(inv, dict) or not inv.get("invoice_id"):
                continue
            try:
                await invs.update_one(
                    {"invoice_id": inv["invoice_id"]},
                    {"$setOnInsert": inv}, upsert=True)
                n += 1
            except Exception as e:
                print(f"  invoice insert err: {e}")
                break
    stats["invoices"] = n

    # 4. tranche stages
    stage_dir = DATA / "tranche_staging"
    n = 0
    if stage_dir.is_dir():
        for fn in sorted(os.listdir(stage_dir)):
            if not fn.endswith(".json"):
                continue
            tid = fn[:-5]
            try:
                body = json.loads((stage_dir / fn).read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  stage parse err {fn}: {e}")
                continue
            if not isinstance(body, dict):
                continue
            try:
                body = dict(body)
                body["tranche_id"] = tid
                await tranches.update_one(
                    {"tranche_id": tid}, {"$set": body}, upsert=True)
                n += 1
            except Exception as e:
                print(f"  stage insert err: {e}")
                break
    stats["tranches"] = n

    print("BACKFILL:", stats)
    try:
        from app.database import get_client
        get_client().close()
    except Exception:
        pass


asyncio.run(main())
