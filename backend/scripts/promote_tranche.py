"""Tranche promotion stager (deterministic, no LLM, no network).

Stages AUTOMATED_CHECKED candidates (parametric 6600 + bank autocheck 645)
in tranches of 500 for HUMAN sign-off. Re-verifies every item with the
independent oracle. Refuses to flip trust_status without HUMAN_SIGNOFF
env var ("Name:YYYY-MM-DD"); even with sign-off it writes staged tranche
files + log and never merges into served verified banks automatically.

Outputs: app/data/tranche_log.json, app/data/tranche_staging/*.json
"""
import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from scripts.verify_parametric_bank import recompute as recompute_param  # noqa: E402
from scripts.autocheck_bank import check_one as check_coding  # noqa: E402

PARAM = BASE / "app" / "data" / "parametric_practice_bank.json"
AUTO = BASE / "app" / "data" / "auto_checked_from_bank.json"
SAMPLING = BASE / "app" / "data" / "sampling_report.json"
LOG = BASE / "app" / "data" / "tranche_log.json"
STAGE_DIR = BASE / "app" / "data" / "tranche_staging"
SIZE = 500
SEED = 20260912


def verify_item(item: dict):
    prov = item.get("provenance", "")
    if "parametric generator" in prov or "code_output" in prov or item.get("id", "").startswith("parametric-"):
        try:
            exp = recompute_param(item)
        except Exception as e:
            return False, f"oracle_error:{e}"[:120]
        if exp is None:
            return False, "oracle_unresolvable"
        if exp != item.get("correct_answer"):
            return False, f"oracle_mismatch:{exp!r}"[:160]
        return True, "oracle_recompute_pass"
    # bank-autocheck shape: solution + testcases/hidden_testcases
    tcs = list(item.get("testcases", [])) + list(item.get("hidden_testcases", []))
    fake = {"id": item.get("id"), "solution": item.get("solution"),
            "test_cases": [{"input": t.get("input", ""),
                            "output": t.get("expected", t.get("output", ""))} for t in tcs]}
    ok, reason, p, total = check_coding(fake)
    return ok, (f"exec_pass:{p}/{total}" if ok else reason[:160])


def main():
    param = json.loads(PARAM.read_text(encoding="utf-8"))
    auto = json.loads(AUTO.read_text(encoding="utf-8")) if AUTO.exists() else []
    sampling = json.loads(SAMPLING.read_text(encoding="utf-8")) if SAMPLING.exists() else {}
    dirty = [f for f, s in sampling.get("families", {}).items() if s.get("reject", 0) > 0]
    if dirty:
        print(f"HOLD: families with rejects: {dirty}")
        return

    pool = [i for i in param + auto
            if i.get("trust_status") in ("automated_checked", "parametric")]
    rng = random.Random(SEED)
    order = list(range(len(pool)))
    rng.shuffle(order)
    pool = [pool[i] for i in order]

    signoff = os.environ.get("HUMAN_SIGNOFF", "").strip()
    STAGE_DIR.mkdir(exist_ok=True)
    tranches = []
    promoted_total, rejected_total = 0, 0
    for n in range(0, len(pool), SIZE):
        chunk = pool[n:n + SIZE]
        staged, rejected = [], []
        for item in chunk:
            ok, why = verify_item(item)
            (staged if ok else rejected).append(item["id"])
        tid = f"tranche-{n // SIZE + 1:02d}"
        body = {"tranche": tid, "size": len(chunk), "staged": staged,
                "rejected": rejected, "seed": SEED,
                "status": "staged-pending-human-signoff",
                "human_signoff": signoff or None,
                "review_method": "oracle_recompute_plus_sampling_v1",
                "created_at": datetime.now(timezone.utc).isoformat()}
        if signoff and not rejected:
            body["status"] = "human-signed-off"
        (STAGE_DIR / f"{tid}.json").write_text(json.dumps(body, indent=1), encoding="utf-8")
        promoted_total += len(staged)
        rejected_total += len(rejected)
        tranches.append({k: body[k] for k in
                         ("tranche", "size", "status") } | {"staged": len(staged), "rejected": len(rejected)})
        print(f"{tid}: staged={len(staged)} rejected={len(rejected)} status={body['status']}")
    LOG.write_text(json.dumps({
        "date": datetime.now(timezone.utc).isoformat(),
        "pool": len(pool), "tranche_size": SIZE, "seed": SEED,
        "staged_total": promoted_total, "rejected_total": rejected_total,
        "human_signoff": signoff or None,
        "serving_merged": False,
        "note": ("Staged only. Merge into served verified banks requires human "
                 "review per Content Trust Pipeline; serving gate unchanged."),
        "tranches": tranches,
    }, indent=1), encoding="utf-8")
    print(f"STAGED {promoted_total}/{len(pool)} rejected={rejected_total} signoff={'yes' if signoff else 'no'}")


if __name__ == "__main__":
    main()
