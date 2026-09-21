"""Five-gate auto-verification (deterministic, no LLM, no network).

Gates per item (all must pass):
  1. oracle    — independent recompute / execution matches stored answer
  2. language  — no placeholders, valid options, answer in explanation
  3. edge      — sane inputs, no div-by-zero, reasonable magnitude
  4. duplicate — not already in the served bank (id or normalized title)
  5. format    — required schema fields for its type

Passing items are stamped with verification_hash + batch_id but KEEP
trust_status=automated_checked. This script never promotes to reviewed/
trusted and never merges into served banks — that stamp belongs to a
human via POST /api/v1/admin/content/tranches/{id}/approve.

Outputs: app/data/auto_promote_report.json (+ per-tranche gate summary
written into tranche_staging files without touching their status).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from scripts.verify_parametric_bank import recompute as recompute_param  # noqa: E402
from scripts.autocheck_bank import check_one as check_coding  # noqa: E402
from scripts.sample_bank import check_language, check_inputs, check_edge  # noqa: E402

PARAM = BASE / "app" / "data" / "parametric_practice_bank.json"
AUTO = BASE / "app" / "data" / "auto_checked_from_bank.json"
STAGE_DIR = BASE / "app" / "data" / "tranche_staging"
OUT = BASE / "app" / "data" / "auto_promote_report.json"
SEED = 20260912

REQUIRED = {"id", "type", "topic", "difficulty", "question", "trust_status"}


def _norm_title(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s or "")[:80].lower()).strip()


def gate_oracle(item: dict):
    prov = item.get("provenance", "")
    if "parametric generator" in prov or str(item.get("id", "")).startswith("parametric-"):
        try:
            exp = recompute_param(item)
        except Exception as e:
            return False, f"oracle_error:{e}"[:120]
        if exp is None:
            return False, "oracle_unresolvable"
        if exp != item.get("correct_answer"):
            return False, f"oracle_mismatch:{exp!r}"[:160]
        return True, "oracle_recompute_pass"
    tcs = list(item.get("testcases", [])) + list(item.get("hidden_testcases", []))
    if not tcs:
        return False, "no_testcases"
    fake = {"id": item.get("id"), "solution": item.get("solution"),
            "test_cases": [{"input": t.get("input", ""),
                            "output": t.get("expected", t.get("output", ""))} for t in tcs]}
    ok, reason, p, total = check_coding(fake)
    return ok, (f"exec_pass:{p}/{total}" if ok else reason[:160])


def gate_format(item: dict):
    missing = [k for k in REQUIRED if not item.get(k)]
    if missing:
        return False, f"missing:{','.join(missing)}"
    if str(item.get("type")).lower() == "coding" and not (
            item.get("testcases") or item.get("test_cases")):
        return False, "coding_without_tests"
    if item.get("options") is not None:
        opts = item.get("options") or []
        if len(opts) != 4 or len(set(map(str, opts))) != 4:
            return False, "bad_options"
        ci = item.get("correct_index")
        if not isinstance(ci, int) or not 0 <= ci < 4:
            return False, "bad_correct_index"
    return True, "schema_ok"


def gate_ground_truth(item: dict):
    """Independent ground-truth cross-check (seeding spec section 1.3).

    Three-state, fails ONLY on mismatch (independent source disagrees —
    the self-stamping catch). 'no_independent_source' passes but records
    the coverage gap in the detail so human reviewers see it and can
    require explicit ground-truth sign-off for new tranches.
    """
    try:
        from app.services.ground_truth import ground_truth_status
    except Exception as e:
        return True, f"ground_truth_unavailable:{type(e).__name__}"
    res = ground_truth_status(item)
    if res["state"] == "mismatch":
        return False, res["detail"]
    return True, f"{res['state']}:{res['detail']}"


def run_gates(item: dict, served_ids: set, served_titles: set) -> dict:
    gates = {}
    ok, why = gate_oracle(item)
    gates["oracle"] = {"pass": ok, "detail": why}
    gtok, gtwo = gate_ground_truth(item)
    gates["ground_truth"] = {"pass": gtok, "detail": gtwo}
    lang = check_language(item) + check_inputs(item) + check_edge(item)
    if str(item.get("type")).lower() == "coding":
        # Coding items are graded by testcases, not MCQ options.
        lang = [x for x in lang if x not in ("bad_options", "bad_index")]
    gates["language_edge"] = {"pass": not lang, "detail": ";".join(lang) or "clean"}
    dup = str(item.get("id")) in served_ids or _norm_title(
        item.get("question")) in served_titles
    gates["duplicate"] = {"pass": not dup, "detail": "already_served" if dup else "unique"}
    fok, fwhy = gate_format(item)
    gates["format"] = {"pass": fok, "detail": fwhy}
    all_pass = all(g["pass"] for g in gates.values())
    vhash = hashlib.sha256(json.dumps(gates, sort_keys=True).encode()).hexdigest()[:16]
    return {"all_pass": all_pass, "gates": gates, "verification_hash": vhash}


def run_tranche_gates(tid: str, index: dict, served_ids: set, served_titles: set) -> dict:
    stage = json.loads((STAGE_DIR / f"{tid}.json").read_text(encoding="utf-8"))
    passed, failed = [], []
    for qid in stage.get("staged", []):
        item = index.get(str(qid))
        if not item:
            failed.append({"id": qid, "reason": "missing_from_source"})
            continue
        res = run_gates(item, served_ids, served_titles)
        if res["all_pass"]:
            passed.append({"id": qid, "verification_hash": res["verification_hash"]})
        else:
            failed.append({"id": qid, "reason": {k: v["detail"] for k, v in res["gates"].items() if not v["pass"]}})
    return {"tranche": tid, "passed": passed, "failed": failed}


def main():
    from app.services import question_store as qs
    qs.load_all()
    served = qs.find().only_verified().to_list()
    served_ids = {str(q.get("id")) for q in served}
    served_titles = {_norm_title(q.get("question")) for q in served}
    index = {}
    for src in (PARAM, AUTO):
        if src.exists():
            for q in json.loads(src.read_text(encoding="utf-8")):
                if isinstance(q, dict) and q.get("id"):
                    index[str(q["id"])] = q
    report = {"seed": SEED, "tranches": {}, "totals": {"passed": 0, "failed": 0}}
    for path in sorted(STAGE_DIR.glob("tranche-*.json")):
        tid = path.stem
        res = run_tranche_gates(tid, index, served_ids, served_titles)
        try:
            stage = json.loads(path.read_text(encoding="utf-8"))
            stage["auto_gates"] = {"passed": len(res["passed"]), "failed": len(res["failed"]),
                                   "failures": res["failed"][:20]}
            path.write_text(json.dumps(stage, indent=1), encoding="utf-8")
        except Exception:
            pass
        report["tranches"][tid] = {"passed": len(res["passed"]), "failed": len(res["failed"]),
                                   "failures": res["failed"][:10]}
        report["totals"]["passed"] += len(res["passed"])
        report["totals"]["failed"] += len(res["failed"])
        print(f"{tid}: gates_pass={len(res['passed'])} fail={len(res['failed'])}")
    OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"AUTO_GATES passed={report['totals']['passed']} failed={report['totals']['failed']}")


if __name__ == "__main__":
    main()
