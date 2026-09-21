"""Re-stage tranches from gate-passing items only (deterministic, no LLM).

- Drops exact duplicates of served content (merging them would create dupes).
- Holds thin-statement items in needs_enrichment.json for human authoring.
- Re-chunks survivors into 500s (same seed) and rewrites staging + tranche log.
- Backs up prior staging to tranche_staging_backup/.
"""
import json
import random
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from scripts.auto_promote import run_gates, _norm_title  # noqa: E402

PARAM = BASE / "app" / "data" / "parametric_practice_bank.json"
AUTO = BASE / "app" / "data" / "auto_checked_from_bank.json"
STAGE_DIR = BASE / "app" / "data" / "tranche_staging"
BACKUP_DIR = BASE / "app" / "data" / "tranche_staging_backup"
LOG = BASE / "app" / "data" / "tranche_log.json"
HELD = BASE / "app" / "data" / "needs_enrichment.json"
SIZE, SEED = 500, 20260912


def main():
    from app.services import question_store as qs
    qs.load_all()
    served = qs.find().only_verified().to_list()
    served_ids = {str(q.get("id")) for q in served}
    served_titles = {_norm_title(q.get("question")) for q in served}
    index = {}
    for src in (PARAM, AUTO):
        for q in json.loads(src.read_text(encoding="utf-8")):
            if isinstance(q, dict) and q.get("id"):
                index[str(q["id"])] = q

    # Old staged order (deterministic seed shuffle, same as promote_tranche.py)
    pool_ids = [i for i in list(index) if index[i].get("trust_status") in
                ("automated_checked", "parametric")]
    rng = random.Random(SEED)
    rng.shuffle(pool_ids)

    clean, dropped_dup, held = [], [], []
    for qid in pool_ids:
        res = run_gates(index[qid], served_ids, served_titles)
        if res["all_pass"]:
            clean.append(qid)
        elif set(res["gates"]) and res["gates"].get("duplicate", {}).get("pass") is False \
                and all(v["pass"] for k, v in res["gates"].items() if k != "duplicate"):
            dropped_dup.append(qid)
        else:
            held.append({"id": qid,
                         "reasons": {k: v["detail"] for k, v in res["gates"].items() if not v["pass"]}})

    BACKUP_DIR.mkdir(exist_ok=True)
    for p in STAGE_DIR.glob("tranche-*.json"):
        shutil.copy(p, BACKUP_DIR / p.name)
        p.unlink()
    tranches = []
    for n in range(0, len(clean), SIZE):
        chunk = clean[n:n + SIZE]
        tid = f"tranche-{n // SIZE + 1:02d}"
        body = {"tranche": tid, "size": len(chunk), "staged": chunk,
                "seed": SEED, "status": "staged-pending-human-signoff",
                "auto_gates": {"passed": len(chunk), "failed": 0, "failures": []}}
        (STAGE_DIR / f"{tid}.json").write_text(json.dumps(body, indent=1), encoding="utf-8")
        tranches.append({"tranche": tid, "size": len(chunk), "staged": len(chunk), "rejected": 0})
    HELD.write_text(json.dumps({"count": len(held), "items": held}, indent=1), encoding="utf-8")
    LOG.write_text(json.dumps({
        "date": datetime.now(timezone.utc).isoformat(),
        "pool": len(clean), "tranche_size": SIZE, "seed": SEED,
        "staged_total": len(clean), "rejected_total": 0,
        "dropped_duplicates": len(dropped_dup), "held_for_enrichment": len(held),
        "human_signoff": None, "serving_merged": False,
        "note": ("Restaged: gate-clean only. Duplicates dropped (already served); "
                 "thin items held in needs_enrichment.json for human authoring."),
        "tranches": tranches,
    }, indent=1), encoding="utf-8")
    print(f"CLEAN {len(clean)} DROPPED_DUP {len(dropped_dup)} HELD {len(held)} "
          f"TRANCHES {len(tranches)}")


if __name__ == "__main__":
    main()
