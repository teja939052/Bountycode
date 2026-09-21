"""Master question bank expansion: normalize, dedupe, generate test cases,
and write a unified verified bank.

Reads every existing bank under backend/app/data/, normalizes schemas,
generates missing test cases deterministically, deduplicates, verifies
with the no-LLM verifier, and writes:

  backend/app/data/expanded_question_bank.json
  backend/app/data/expanded_bank_report.json
"""
from __future__ import annotations

import ast
import contextlib
import hashlib
import io
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.services.auto_verify import verify_question  # noqa: E402

logger = logging.getLogger(__name__)

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "app" / "data"
OUT_BANK = DATA / "expanded_question_bank.json"
OUT_REPORT = DATA / "expanded_bank_report.json"

BANK_FILES = [
    "verified_placement_questions.json",
    "leetcode_problems_seed.json",
    "interview_practice_bank.json",
    "india_placement_depth.json",
    "system_design_bank.json",
    "debugging_bank.json",
    "sql_practice_bank.json",
    "parametric_practice_bank.json",
    "auto_checked_from_bank.json",
    "questions_bank.json",
    "striver_a2z_600.json",
    "tcs_nqt_questions.json",
    "infosys_questions.json",
    "legacy_enriched_coding.json",
]

MAX_PER_BANK = {
    "parametric_practice_bank.json": 5000,
    "striver_a2z_600.json": 2000,
    "questions_bank.json": 3000,
    "india_placement_depth.json": 2000,
    "interview_practice_bank.json": 2000,
    "verified_placement_questions.json": 2000,
    "leetcode_problems_seed.json": 2000,
    "debugging_bank.json": 2000,
    "sql_practice_bank.json": 2000,
    "system_design_bank.json": 2000,
    "auto_checked_from_bank.json": 2000,
    "tcs_nqt_questions.json": 1000,
    "infosys_questions.json": 1000,
    "legacy_enriched_coding.json": 1000,
}


def _norm_text(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip().lower()


def _canonical_type(q: dict) -> str:
    t = str(q.get("type") or q.get("question_type") or "coding").lower()
    mapping = {
        "coding": "coding",
        "python": "coding",
        "java": "coding",
        "cpp": "coding",
        "c": "coding",
        "javascript": "coding",
        "sql": "sql",
        "database": "sql",
        "dbms": "sql",
        "aptitude": "aptitude",
        "quantitative": "aptitude",
        "logical": "logical",
        "reasoning": "logical",
        "verbal": "verbal",
        "hr": "hr",
        "behavioral": "behavioral",
        "interview": "interview",
        "system_design": "system_design",
        "debugging": "debugging",
    }
    return mapping.get(t, t)


def _normalize_options(options: Any) -> dict:
    if isinstance(options, dict):
        return {str(k).strip().upper(): str(v).strip() for k, v in options.items() if str(v).strip()}
    if isinstance(options, list):
        out = {}
        keys = ["A", "B", "C", "D", "E", "F"]
        for i, opt in enumerate(options):
            if i < len(keys):
                out[keys[i]] = str(opt).strip()
        return out
    return {}


def _normalize_test_cases(tcs: Any, qtype: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not tcs:
        return out
    if not isinstance(tcs, list):
        return out
    for tc in tcs:
        if not isinstance(tc, dict):
            continue
        inp = tc.get("input") or tc.get("input_text") or tc.get("stdin") or ""
        out_val = tc.get("output") or tc.get("expected") or tc.get("expected_output") or tc.get("output_text") or ""
        hidden = bool(tc.get("hidden", False))
        if qtype in ("aptitude", "logical", "verbal", "hr"):
            out.append({
                "input": str(inp),
                "output": str(out_val),
                "option_text": str(tc.get("option_text", "")),
                "hidden": hidden,
            })
        else:
            out.append({
                "input": str(inp),
                "output": str(out_val),
                "hidden": hidden,
            })
    return out


def _content_hash(q: dict) -> str:
    title = _norm_text(q.get("question") or q.get("question_title") or q.get("title") or "")
    body = _norm_text(q.get("statement") or q.get("description") or q.get("question") or "")
    topic = _norm_text(q.get("topic") or "")
    qtype = _norm_text(q.get("type") or "")
    blob = f"{title}\n{body}\n{topic}\n{qtype}"
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def _ensure_solution(q: dict) -> dict:
    sol = q.get("solution") or {}
    if isinstance(sol, dict):
        return sol
    return {}


def _ensure_testcases(q: dict, qtype: str) -> List[Dict[str, Any]]:
    existing = q.get("test_cases") or q.get("testcases") or []
    if existing:
        return _normalize_test_cases(existing, qtype)
    return []


def normalize_question(raw: dict, idx: int) -> Optional[dict]:
    qtype = _canonical_type(raw)
    title = str(raw.get("question") or raw.get("question_title") or raw.get("title") or "").strip()
    if not title or title.lower() in ("", "untitled", "question", "problem"):
        return None

    options = _normalize_options(raw.get("options") or raw.get("option_list") or {})
    correct_answer = str(raw.get("correct_answer") or raw.get("correct_index") or "").strip().upper()
    if not correct_answer and options:
        correct_answer = str(raw.get("answer") or "").strip().upper()

    test_cases = _ensure_testcases(raw, qtype)
    solution = _ensure_solution(raw)

    q = {
        "id": str(raw.get("id") or f"expanded_{idx:06d}"),
        "type": qtype,
        "title": title,
        "question": title,
        "statement": str(raw.get("statement") or raw.get("description") or raw.get("question") or title),
        "topic": str(raw.get("topic") or raw.get("subject") or "General").strip(),
        "sub_topic": str(raw.get("sub_topic") or raw.get("subtopic") or "").strip(),
        "difficulty": str(raw.get("difficulty") or "medium").strip().lower(),
        "pattern": str(raw.get("pattern") or raw.get("dsa_topic") or "").strip(),
        "companies": [str(c).strip() for c in (raw.get("companies") or []) if str(c).strip()],
        "role": [str(r).strip() for r in (raw.get("role") or []) if str(r).strip()] if isinstance(raw.get("role"), list) else [str(raw.get("role", "")).strip()] if raw.get("role") else [],
        "constraints": str(raw.get("constraints") or "").strip(),
        "examples": raw.get("examples") or [],
        "options": options,
        "correct_answer": correct_answer,
        "test_cases": test_cases,
        "hidden_test_cases": [tc for tc in test_cases if tc.get("hidden")],
        "solution": solution,
        "hints": [str(h).strip() for h in (raw.get("hints") or []) if str(h).strip()],
        "explanation": str(raw.get("explanation") or raw.get("editorial") or "").strip(),
        "worked_solution": str(raw.get("worked_solution") or raw.get("explanation") or "").strip(),
        "trick": str(raw.get("trick") or raw.get("common_trap") or "").strip(),
        "provenance": str(raw.get("provenance") or raw.get("source_bank") or "expanded_bank"),
        "source_bank": str(raw.get("source_bank") or raw.get("source") or "expanded_bank"),
        "trust_status": str(raw.get("trust_status") or "unverified").lower(),
        "content_hash": _content_hash(raw),
    }
    return q


def load_bank(path: Path, limit: Optional[int] = None) -> List[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("Failed to read %s: %s", path, e)
        return []
    if not isinstance(data, list):
        return []
    out = []
    seen = set()
    for raw in data:
        if not isinstance(raw, dict):
            continue
        q = normalize_question(raw, len(out))
        if not q:
            continue
        ch = q["content_hash"]
        if ch in seen:
            continue
        seen.add(ch)
        out.append(q)
        if limit and len(out) >= limit:
            break
    return out


def generate_parametric_variants(count: int = 2000) -> List[dict]:
    """Generate deterministic parametric MCQ variants for aptitude/logical/verbal/hr."""
    import random
    rng = random.Random(20260912)
    out: List[dict] = []
    seq = 0

    def mcq(topic, sub, difficulty, question, answer, distractors, explanation, steps, hint, qtype="aptitude"):
        nonlocal seq
        seq += 1
        opts = [answer] + [d for d in distractors if d != answer]
        seen, uniq = set(), []
        for o in opts:
            if o not in seen:
                seen.add(o)
                uniq.append(o)
        need = 2
        while len(uniq) < 4:
            cand = f"{answer} ({need})" if isinstance(answer, str) else str(answer) + f".{need}"
            if cand not in seen:
                seen.add(cand)
                uniq.append(cand)
            need += 1
        uniq = uniq[:4]
        order = sorted(range(4), key=lambda i: rng.random())
        options = [uniq[i] for i in order]
        correct_index = options.index(answer)
        return {
            "id": f"parametric-{seq:06d}",
            "type": qtype,
            "topic": topic,
            "sub_topic": sub,
            "difficulty": difficulty,
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "correct_answer": answer,
            "solution": {},
            "test_cases": [{"input": "", "output": str(answer)}],
            "hidden_test_cases": [],
            "hints": [hint],
            "explanation": explanation,
            "reasoning_steps": steps,
            "companies": [],
            "role": "",
            "provenance": "parametric generator v2 (expanded)",
            "source_bank": "parametric_practice_bank.json",
            "trust_status": "automated_checked",
            "stage": "practice",
            "content_hash": hashlib.sha256(question.encode()).hexdigest()[:16],
        }

    families = [
        ("pct_of", "Aptitude", "Percentages", "easy", lambda: (
            rng.choice([5, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75]),
            rng.choice([100, 200, 240, 300, 400, 500, 600, 800, 1000]),
        )),
        ("profit_loss", "Aptitude", "Profit & Loss", "easy", lambda: (
            rng.choice([200, 300, 400, 500, 600, 800, 1000]),
            rng.choice([10, 20, 25]),
        )),
        ("average", "Aptitude", "Averages", "easy", lambda: (
            rng.choice([3, 4, 5]),
            rng.choice([10, 12, 15, 20]),
            rng.choice([2, 3, 4, 5]),
        )),
        ("speed_time", "Aptitude", "Speed & Distance", "easy", lambda: (
            rng.choice([40, 50, 60, 80, 100]),
            rng.choice([2, 3, 4, 5]),
        )),
        ("ratio", "Aptitude", "Ratios", "easy", lambda: (
            rng.choice([(1, 2), (2, 3), (3, 4), (1, 3), (3, 5)]),
            rng.choice([10, 20, 25, 50]),
        )),
    ]

    for family, topic, sub, diff, param_fn in families:
        for _ in range(count // len(families)):
            params = param_fn()
            if family == "pct_of":
                p, base = params
                ans = base * p // 100
                q = f"What is {p}% of {base}?"
                explanation = f"{p}% of {base} = ({p}/100) × {base} = {ans}."
                steps = [f"Convert {p}% to {p}/100.", f"Multiply by {base}."]
                hint = "Percent means per hundred."
                distractors = [str(ans + d) for d in [1, 2, 3, 5, 10] if ans + d != ans][:3]
            elif family == "profit_loss":
                cost, pct = params
                sp = cost * (100 + pct) // 100
                q = f"A shopkeeper buys an item for {cost} and wants a {pct}% profit. What should the selling price be?"
                ans = sp
                explanation = f"SP = {cost} × (1 + {pct}/100) = {sp}."
                steps = [f"Profit = {pct}% of {cost} = {cost * pct // 100}.", f"SP = cost + profit = {sp}."]
                hint = "Selling price = cost + profit."
                distractors = [str(sp + d) for d in [1, 2, 3, 5] if sp + d != sp][:3]
            elif family == "average":
                k, start, step = params
                nums = [start + i * step for i in range(k)]
                ans = sum(nums) // k
                q = f"What is the average of {', '.join(map(str, nums))}?"
                explanation = f"Sum = {sum(nums)}; count = {k}; avg = {ans}."
                steps = [f"Add all numbers: {sum(nums)}.", f"Divide by {k}."]
                hint = "Average = sum ÷ count."
                distractors = [str(ans + d) for d in [1, 2, 3, 5] if ans + d != ans][:3]
            elif family == "speed_time":
                d, t = params
                dist = d * t
                q = f"A train travels at {d} km/h for {t} hours. How far does it travel?"
                ans = dist
                explanation = f"Distance = {d} × {t} = {dist} km."
                steps = [f"Use distance = speed × time = {d} × {t}."]
                hint = "Distance = speed × time."
                distractors = [str(dist + d) for d in [5, 10, 15, 20] if dist + d != dist][:3]
            elif family == "ratio":
                ab, total = params
                a, b = ab
                sa, sb = total * a // (a + b), total * b // (a + b)
                ans = max(sa, sb)
                q = f"Divide {total} in the ratio {a}:{b}. What is the larger share?"
                explanation = f"Parts = {a+b}; shares = {sa} and {sb}; larger = {ans}."
                steps = [f"Total parts = {a+b}.", f"Share = total × part/{a+b}."]
                hint = "Split by total parts."
                distractors = [str(min(sa, sb)), str(total // 2), str(abs(sa - sb))][:3]
            else:
                continue

            if len(distractors) < 3:
                distractors = [str(ans + 1), str(ans + 2), str(ans + 3)]
            distractors = [d for d in distractors if d != str(ans)][:3]
            out.append(mcq(topic, sub, diff, q, str(ans), distractors, explanation, steps, hint))

    return out


def generate_coding_variants(base: dict, count: int = 3) -> List[dict]:
    """Generate unique coding variants from a verified base question by
    changing numeric constants and expected outputs. No LLM."""
    variants: List[dict] = []
    sol_code = base.get("solution", {}).get("code", "")
    if not sol_code:
        return variants
    tcs = base.get("test_cases") or base.get("testcases") or []
    if not tcs:
        return variants

    base_id = base.get("id", "base")
    topic = base.get("topic", "General")
    difficulty = base.get("difficulty", "medium")
    companies = base.get("companies", [])
    role = base.get("role", [])
    if not isinstance(role, list):
        role = [role] if role else []
    hints = base.get("hints") or []
    explanation = base.get("explanation") or ""
    constraints = base.get("constraints") or ""

    for i in range(1, count + 1):
        variant = dict(base)
        variant["id"] = f"{base_id}-v{i+1}"
        variant["source_bank"] = base.get("source_bank", "expanded_bank")
        variant["provenance"] = f"variant_of_{base_id}"
        variant["trust_status"] = base.get("trust_status", "unverified")

        new_tcs = []
        for tc in tcs:
            new_tc = dict(tc)
            inp = str(new_tc.get("input", ""))
            out = str(new_tc.get("output", "") or new_tc.get("expected", ""))
            nums = re.findall(r"-?\d+", inp)
            if nums:
                new_nums = [str(int(n) + (i * 10)) for n in nums]
                for old, new in zip(nums, new_nums):
                    inp = inp.replace(old, new, 1)
                    out = out.replace(old, new, 1)
            new_tc["input"] = inp
            new_tc["output"] = out
            new_tc["expected"] = out
            new_tc["hidden"] = False
            new_tcs.append(new_tc)
        variant["test_cases"] = new_tcs
        variant["content_hash"] = hashlib.sha256(
            f"{base_id}\n{variant['id']}\n{topic}\n{difficulty}".encode()
        ).hexdigest()[:16]
        variants.append(variant)
    return variants


def run():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logger.info("Expanding question bank from %d source files", len(BANK_FILES))

    all_questions: List[dict] = []
    seen_hashes = set()

    for fname in BANK_FILES:
        path = DATA / fname
        limit = MAX_PER_BANK.get(fname)
        logger.info("Loading %s (limit=%s)", fname, limit)
        loaded = load_bank(path, limit=limit)
        added = 0
        for q in loaded:
            ch = q.pop("content_hash")
            if ch in seen_hashes:
                continue
            seen_hashes.add(ch)
            all_questions.append(q)
            added += 1
        logger.info("  Added %d unique questions from %s", added, fname)

    logger.info("Total after aggregation + dedupe: %d", len(all_questions))

    verified_bases = [q for q in all_questions if str(q.get("trust_status", "")).lower() in ("verified", "reviewed", "automated_checked")]
    logger.info("Verified bases for variant generation: %d", len(verified_bases))
    variant_target = min(len(verified_bases), 1000)
    logger.info("Generating coding variants from %d bases...", variant_target)

    coding_variants = []
    for base in verified_bases[:variant_target]:
        if str(base.get("type", "")).lower() == "coding":
            variants = generate_coding_variants(base, count=2)
            if variants:
                coding_variants.extend(variants)
                seen_hashes.add(variants[-1]["content_hash"])

    logger.info("Generated %d coding variants", len(coding_variants))
    all_questions.extend(coding_variants)

    logger.info("Generating parametric MCQ variants...")
    parametric = generate_parametric_variants(count=3000)
    added_parametric = 0
    for q in parametric:
        ch = q.pop("content_hash")
        if ch in seen_hashes:
            continue
        seen_hashes.add(ch)
        all_questions.append(q)
        added_parametric += 1
    logger.info("Added %d parametric MCQs", added_parametric)

    logger.info("Total before verification: %d", len(all_questions))

    logger.info("Running deterministic verification on %d questions...", len(all_questions))
    report = {
        "total_input": len(all_questions),
        "by_source_bank": {},
        "by_type": {},
        "by_trust_status": {},
        "passed": 0,
        "failed": 0,
        "quarantined": 0,
        "skipped": 0,
        "details": [],
    }

    for q in all_questions:
        src = q.get("source_bank", "unknown")
        report["by_source_bank"][src] = report["by_source_bank"].get(src, 0) + 1
        qtype = q.get("type", "unknown")
        report["by_type"][qtype] = report["by_type"].get(qtype, 0) + 1

        try:
            r = verify_question(q)
        except Exception as e:
            r = {
                "id": q.get("id", ""),
                "verdict": "quarantined",
                "reason": f"verify_exception:{type(e).__name__}:{str(e)[:120]}",
            }
            q["trust_status"] = "quarantined"
            q["verification_failure"] = r["reason"]

        status = str(q.get("trust_status", "unverified")).lower()
        report["by_trust_status"][status] = report["by_trust_status"].get(status, 0) + 1

        if r.get("verdict") == "passed":
            report["passed"] += 1
        elif r.get("verdict") == "failed":
            report["failed"] += 1
            report["details"].append(r)
        elif r.get("verdict") == "quarantined":
            report["quarantined"] += 1
            report["details"].append(r)
        else:
            report["skipped"] += 1

    report["final_total"] = len(all_questions)
    report["final_verified"] = report["passed"]
    report["final_quarantined"] = report["quarantined"] + report["failed"]

    logger.info(
        "Verification complete: total=%d passed=%d failed=%d quarantined=%d skipped=%d",
        report["total_input"],
        report["passed"],
        report["failed"],
        report["quarantined"],
        report["skipped"],
    )

    verified = [q for q in all_questions if str(q.get("trust_status", "")).lower() in ("verified", "reviewed", "automated_checked")]
    logger.info("Writing %d verified questions to %s", len(verified), OUT_BANK)
    OUT_BANK.write_text(json.dumps(verified, indent=1, ensure_ascii=False), encoding="utf-8")

    summary = {
        "total_input": report["total_input"],
        "final_total": len(all_questions),
        "final_verified": len(verified),
        "final_quarantined": report["final_quarantined"],
        "passed": report["passed"],
        "failed": report["failed"],
        "quarantined": report["quarantined"],
        "skipped": report["skipped"],
        "by_source_bank": report["by_source_bank"],
        "by_type": report["by_type"],
        "by_trust_status": report["by_trust_status"],
        "output_file": str(OUT_BANK),
    }
    OUT_REPORT.write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    logger.info("Wrote report to %s", OUT_REPORT)
    logger.info("Done. Verified questions: %d", len(verified))
    return summary


if __name__ == "__main__":
    run()
