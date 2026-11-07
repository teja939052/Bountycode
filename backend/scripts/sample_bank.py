"""Deterministic sampling audit (no LLM, no network, seeded RNG).

Samples 30 items per parametric family, applies coded checks:
oracle recompute + language + input sanity + edge checks.
Verdicts: PASS | FIX | REJECT. Writes sampling_report.json.
"""
import json
import random
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from scripts.verify_parametric_bank import recompute  # noqa: E402

BANK = BASE / "app" / "data" / "parametric_practice_bank.json"
OUT = BASE / "app" / "data" / "sampling_report.json"
SEED = 20260912
PER_FAMILY = 30
PLACEHOLDERS = {"result", "tree", "grid", "coordinates", "minutes", "grouped",
                "distance", "count", "sum", "order", "node", "updated", "chunked"}


def check_language(q):
    issues = []
    text = q.get("question", "")
    if not text or len(text.strip()) < 12:
        issues.append("too_short")
    if not text.strip().endswith(("?", ".", ":", '"')):
        issues.append("no_terminal_punct")
    if re.search(r"todo|implement|placeholder|lorem", text, re.I):
        issues.append("placeholder_text")
    opts = q.get("options", [])
    if len(opts) != 4 or len(set(opts)) != 4 or any(not str(o).strip() for o in opts):
        issues.append("bad_options")
    if str(q.get("correct_answer", "")) not in (q.get("explanation") or ""):
        issues.append("answer_not_in_explanation")
    if str(q.get("correct_answer", "")).strip().lower() in PLACEHOLDERS:
        issues.append("placeholder_answer")
    return issues


def check_inputs(q):
    issues = []
    text = q.get("question", "")
    nums = list(map(int, re.findall(r"-?\d+", text)))
    fam = q.get("provenance", "")
    if "/0" in text or "divide by 0" in text.lower():
        issues.append("div_by_zero")
    if any(v < 0 for v in nums) and any(k in fam for k in
            ["pct_of", "profit_loss", "ratio", "average", "std", "si", "ci", "prob"]):
        issues.append("negative_input")
    if "letter" in fam.lower():
        letters = re.findall(r"[A-Z]", text)
        if len(letters) < 3:
            issues.append("short_series")
    elif "series" in fam or "Series" in text:
        if len(nums) < 3:
            issues.append("short_series")
    return issues


def check_edge(q):
    issues = []
    try:
        vals = re.findall(r"-?[\d.]+", str(q.get("correct_answer", "")))
        for v in vals:
            if abs(float(v)) >= 1e9:
                issues.append("answer_magnitude")
                break
    except Exception:
        issues.append("answer_unparseable")
    ci = q.get("correct_index")
    if not isinstance(ci, int) or not 0 <= ci < 4:
        issues.append("bad_index")
    return issues


def main():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    fams: dict = {}
    for q in bank:
        prov = q.get("provenance", "")
        fam = prov.split("(")[1].split(")")[0] if "(" in prov else "?"
        fams.setdefault(fam, []).append(q)
    report = {"seed": SEED, "per_family": PER_FAMILY, "families": {}, "items": []}
    for fam in sorted(fams):
        pool = fams[fam]
        rng = random.Random(f"{SEED}:{fam}")
        sample = rng.sample(pool, min(PER_FAMILY, len(pool)))
        summary = {"sampled": len(sample), "pass": 0, "fix": 0, "reject": 0, "issues": {}}
        for q in sample:
            try:
                exp = recompute(q)
            except Exception as e:
                exp = f"ERROR:{e}"
            reasons = []
            if exp is None or exp != q.get("correct_answer"):
                verdict = "REJECT"
                reasons.append(f"oracle_mismatch:{exp!r}")
            else:
                lang = check_language(q)
                inps = check_inputs(q)
                edge = check_edge(q)
                if lang or inps or edge:
                    # oracle passes but wording/inputs need generator fix
                    if "placeholder_answer" in lang or "bad_options" in lang:
                        verdict = "REJECT"
                    else:
                        verdict = "FIX"
                    reasons += lang + inps + edge
                else:
                    verdict = "PASS"
            summary[verdict.lower() if verdict in ("PASS", "FIX", "REJECT") else "fix"] += 0  # noop guard
            summary[{"PASS": "pass", "FIX": "fix", "REJECT": "reject"}[verdict]] += 1
            for r in reasons:
                summary["issues"][r] = summary["issues"].get(r, 0) + 1
            report["items"].append({"id": q["id"], "family": fam,
                                    "verdict": verdict, "reasons": reasons})
        report["families"][fam] = summary
    OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    tp = sum(f["pass"] for f in report["families"].values())
    tf = sum(f["fix"] for f in report["families"].values())
    tr = sum(f["reject"] for f in report["families"].values())
    print(f"SAMPLED {tp+tf+tr} PASS={tp} FIX={tf} REJECT={tr}")
    for fam, s in report["families"].items():
        if s["fix"] or s["reject"]:
            print(fam, s)


if __name__ == "__main__":
    main()
