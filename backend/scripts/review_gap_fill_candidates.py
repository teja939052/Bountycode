"""Review helper for exam_pattern_2026_gap_fill candidates.

Lists / promotes ONLY the 43 gap-fill rows in verified_question_bank.json.
Uses the real trust statuses: automated_checked -> reviewed (servable).
Never writes "human_verified" (does not exist; would stay unservable).

Human review is mandatory. This tool records reviewer identity; it does not
decide content quality.

Usage:
  python scripts/review_gap_fill_candidates.py --list
  python scripts/review_gap_fill_candidates.py --show tcs26-pseudo-001
  python scripts/review_gap_fill_candidates.py --promote id1,id2 --reviewer "Name <email>"
  python scripts/review_gap_fill_candidates.py --promote all --reviewer "Name <email>" --i-reviewed-every-question

After promote: restart uvicorn (question_store.load_all is once-per-process).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BANK = BASE / "app" / "data" / "verified_question_bank.json"
SOURCE_BANK = "exam_pattern_2026_gap_fill"
FORBIDDEN_REVIEWERS = {"", "class_b_pipeline", "pipeline", "system", "auto", "mock", "none", "human_verified"}
SERVABLE = {"verified", "reviewed"}


def _load() -> list:
    with BANK.open(encoding="utf-8") as f:
        return json.load(f)


def _save(rows: list) -> None:
    tmp = BANK.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
        f.write("\n")
    tmp.replace(BANK)


def gap_rows(rows: list) -> list:
    return [q for q in rows if q.get("source_bank") == SOURCE_BANK]


def cmd_list() -> int:
    rows = gap_rows(_load())
    await_review = [q for q in rows if q.get("trust_status") == "automated_checked"]
    reviewed = [q for q in rows if q.get("trust_status") == "reviewed"]
    servable = [q for q in rows if str(q.get("trust_status", "")).lower() in SERVABLE]
    print(f"gap_fill_total: {len(rows)}")
    print(f"awaiting_review (automated_checked): {len(await_review)}")
    print(f"reviewed: {len(reviewed)}")
    print(f"servable_gap_fill: {len(servable)}")
    for q in rows:
        status = q.get("trust_status")
        marker = "SERVE" if status in SERVABLE else "HOLD "
        who = q.get("reviewed_by") or "-"
        print(f"  [{marker}] {q.get('id')}: {status} | {q.get('type')} | {who}")
    return 0


def cmd_show(qid: str) -> int:
    rows = {str(q.get("id")): q for q in gap_rows(_load())}
    q = rows.get(qid)
    if not q:
        print(f"not found in gap-fill set: {qid}", file=sys.stderr)
        return 1
    print(json.dumps(q, indent=2, ensure_ascii=False))
    return 0


def cmd_promote(ids: list[str], reviewer: str, confirm_all: bool) -> int:
    reviewer = (reviewer or "").strip()
    if reviewer.lower() in FORBIDDEN_REVIEWERS:
        print("refused: --reviewer must be a real human identity (not pipeline/system/empty)", file=sys.stderr)
        return 2

    rows = _load()
    gap = gap_rows(rows)
    by_id = {str(q.get("id")): q for q in gap}

    if len(ids) == 1 and ids[0].lower() == "all":
        if not confirm_all:
            print(
                "refused: --promote all requires --i-reviewed-every-question",
                file=sys.stderr,
            )
            return 2
        targets = list(by_id.keys())
    else:
        targets = [i.strip() for i in ids if i.strip()]

    now = datetime.now(timezone.utc).isoformat()
    promoted, skipped, failed = [], [], []

    for qid in targets:
        q = by_id.get(qid)
        if not q:
            failed.append((qid, "not_in_gap_fill_set"))
            continue
        status = str(q.get("trust_status", "")).lower()
        if status == "reviewed":
            skipped.append((qid, "already_reviewed"))
            continue
        if status != "automated_checked":
            failed.append((qid, f"unexpected_status:{status}"))
            continue
        q["trust_status"] = "reviewed"
        q["reviewed_by"] = reviewer
        q["reviewed_at"] = now
        q["review_method"] = "human_review_gap_fill_v1"
        promoted.append(qid)

    if failed and not promoted and not skipped:
        print(json.dumps({"promoted": 0, "failed": failed}, indent=2))
        return 1

    if promoted:
        _save(rows)

    report = {
        "promoted": len(promoted),
        "promoted_ids": promoted,
        "skipped": skipped,
        "failed": failed,
        "reviewer": reviewer,
        "reviewed_at": now,
        "note": "trust_status=reviewed (servable after backend restart). "
        "Do NOT use human_verified — not a real status.",
        "restart_required": bool(promoted),
    }
    print(json.dumps(report, indent=2))
    return 0 if not failed else 1


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--list", action="store_true")
    p.add_argument("--show", metavar="ID")
    p.add_argument("--promote", metavar="CSV|all")
    p.add_argument("--reviewer", default="")
    p.add_argument("--i-reviewed-every-question", action="store_true")
    args = p.parse_args()

    if args.list:
        return cmd_list()
    if args.show:
        return cmd_show(args.show)
    if args.promote:
        ids = [args.promote] if "," not in args.promote else args.promote.split(",")
        return cmd_promote(ids, args.reviewer, args.i_reviewed_every_question)

    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
