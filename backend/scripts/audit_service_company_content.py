#!/usr/bin/env python3
"""Read-only quality audit for Bountycode's service-company content.

This tool never edits, promotes or deletes content. It reports structural and
obvious consistency defects for human triage. A clean report is NOT proof that
an answer is correct; independent domain review is still required.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1] / "app" / "data"
PLACEHOLDER_PATTERNS = (
    re.compile(r"\bhint\s*\d+\s+for\b", re.I),
    re.compile(r"\bexample\s+for\b", re.I),
    re.compile(r"\bunderstand problem\b", re.I),
    re.compile(r"\bchoose approach\b", re.I),
    re.compile(r"\bimplement\.\s*test\.\s*return result\b", re.I),
    re.compile(r"\bsolve .{0,50} using an efficient approach\b", re.I),
)
SKIP_PARTS = {"candidates", "backups", "dead_collections_20260916", "__pycache__"}


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def _looks_like_bank(path: Path, root: Path = ROOT) -> bool:
    rel = path.relative_to(root)
    if any(part in SKIP_PARTS for part in rel.parts):
        return False
    if rel.parts and rel.parts[0] == "lessons":
        return False
    return (
        "content" in rel.parts
        or "generated" in rel.parts
        or "questions" in rel.parts
        or "verified" in path.name.lower()
        or path.name in {"questions_bank.json", "expanded_question_bank.json"}
    )


def _items_from(payload: Any) -> Iterable[dict]:
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict) and (item.get("question") or item.get("title")):
                yield item
        return
    if not isinstance(payload, dict):
        return
    for key in ("practice", "questions", "items"):
        values = payload.get(key)
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict) and (item.get("question") or item.get("title")):
                    yield item


def _item_id(item: dict) -> str:
    return str(item.get("id") or item.get("question_id") or item.get("question_uid") or "")


def _question_text(item: dict) -> str:
    return str(item.get("question") or item.get("title") or item.get("prompt") or "")


def _options(item: dict) -> list[str]:
    options = item.get("options") or item.get("multiple_choice_options") or []
    if isinstance(options, dict):
        return [str(options[key]) for key in sorted(options)]
    if isinstance(options, list):
        return [str(value) for value in options]
    return []


def audit_item(path: Path, item: dict, root: Path = ROOT) -> list[dict]:
    issues: list[dict] = []
    item_id = _item_id(item) or "<missing-id>"
    text = _question_text(item)
    joined = " ".join(
        [text, str(item.get("explanation") or ""), " ".join(map(str, item.get("hints") or [])),
         " ".join(map(str, item.get("reasoning_steps") or []))]
    )
    add = lambda severity, code, detail: issues.append({
        "file": str(path.relative_to(root)),
        "item_id": item_id,
        "severity": severity,
        "code": code,
        "detail": detail,
    })

    if not _item_id(item):
        add("error", "missing_stable_id", "Question has no stable id/question_id.")
    if len(text.strip()) < 30:
        add("warning", "thin_prompt", f"Prompt has only {len(text.strip())} characters.")
    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(joined)
        if match:
            add("error", "template_filler", f"Placeholder-like text found: {match.group(0)!r}.")
            break

    options = _options(item)
    answer = item.get("correct_answer", item.get("answer"))
    correct_index = item.get("correct_index")
    if options:
        if len(options) < 2:
            add("error", "too_few_options", "MCQ has fewer than two options.")
        if len({value.strip().casefold() for value in options}) != len(options):
            add("error", "duplicate_options", "MCQ contains duplicate option text.")
        if correct_index is not None:
            try:
                idx = int(correct_index)
                if idx < 0 or idx >= len(options):
                    add("error", "answer_index_out_of_range", f"correct_index={correct_index!r}, options={len(options)}.")
            except (TypeError, ValueError):
                add("error", "answer_index_invalid", f"correct_index is not an integer: {correct_index!r}.")
        elif answer is not None:
            if isinstance(item.get("options"), dict):
                if str(answer).strip().upper() not in {key.upper() for key in item["options"]}:
                    if str(answer).strip().casefold() not in {v.strip().casefold() for v in options}:
                        add("error", "answer_not_in_options", "correct_answer matches neither an option key nor option text.")
            elif str(answer).strip().casefold() not in {v.strip().casefold() for v in options}:
                add("error", "answer_not_in_options", "correct_answer is not one of the option texts.")
        else:
            add("error", "missing_answer_key", "MCQ has no correct_answer or correct_index.")

    explanation = str(item.get("explanation") or "")
    if options and len(explanation.strip()) < 35:
        add("warning", "thin_explanation", "MCQ explanation is missing or too short to teach the reasoning.")

    qtype = str(item.get("type") or item.get("question_type") or "").lower()
    solution = item.get("solution") or {}
    solution_code = solution.get("code") if isinstance(solution, dict) else None
    if qtype in {"coding", "sql", "debugging"} or solution_code:
        cases = item.get("hidden_test_cases") or item.get("hidden_testcases") or item.get("testcases") or item.get("test_cases") or []
        if not isinstance(cases, list) or len(cases) < 2:
            add("error", "insufficient_code_tests", "Coding item needs at least two concrete test cases.")
        else:
            for index, case in enumerate(cases):
                if not isinstance(case, dict) or "input" not in case or not any(k in case for k in ("expected", "expected_output", "output")):
                    add("error", "malformed_code_test", f"Test case {index + 1} must include input and expected output.")
                    break
        solution = item.get("solution") or {}
        code = solution.get("code") if isinstance(solution, dict) else ""
        if code and not cases:
            add("error", "solution_without_oracle", "Solution exists but no expected-output test oracle is supplied.")

    trust = str(item.get("trust_status") or "").lower()
    if trust in {"verified", "reviewed", "human_reviewed", "trusted"}:
        has_review = bool(item.get("review_evidence") or item.get("human_review"))
        has_validation = bool(item.get("verification_evidence") or item.get("validation_report") or item.get("verification"))
        if not has_review:
            add("high", "trust_claim_without_review_evidence", f"trust_status={trust!r} has no attached human-review evidence.")
        if trust in {"verified", "trusted"} and not has_validation:
            add("high", "trust_claim_without_validation_evidence", f"trust_status={trust!r} has no attached independent-validation evidence.")

    companies = item.get("companies") or item.get("company_tags") or []
    if isinstance(companies, str):
        companies = [companies]
    provenance = item.get("provenance") or item.get("source") or ""
    if companies and not provenance:
        add("warning", "company_claim_without_provenance", "Company tags exist but no provenance/source label is recorded.")

    return issues


def audit(root: Path = ROOT) -> dict:
    all_issues: list[dict] = []
    seen: dict[str, list[str]] = defaultdict(list)
    scanned_files = 0
    scanned_items = 0
    unreadable_files: list[dict] = []

    for path in sorted(root.rglob("*.json")):
        if not _looks_like_bank(path, root):
            continue
        try:
            payload = _load_json(path)
        except Exception as exc:
            unreadable_files.append({"file": str(path.relative_to(root)), "error": str(exc)})
            continue
        scanned_files += 1
        for item in _items_from(payload):
            scanned_items += 1
            item_id = _item_id(item)
            if item_id:
                seen[item_id].append(str(path.relative_to(root)))
            all_issues.extend(audit_item(path, item, root))

    for item_id, locations in seen.items():
        if len(locations) > 1:
            all_issues.append({
                "file": "; ".join(locations),
                "item_id": item_id,
                "severity": "high",
                "code": "duplicate_id_across_files",
                "detail": f"Stable ID appears {len(locations)} times across content files.",
            })

    counts = Counter(issue["severity"] for issue in all_issues)
    return {
        "root": str(root),
        "files_scanned": scanned_files,
        "items_scanned": scanned_items,
        "issues": all_issues,
        "severity_counts": dict(counts),
        "unreadable_files": unreadable_files,
        "limitations": [
            "This is a read-only structural audit, not a semantic proof of every answer.",
            "Code outputs and mathematical reasoning still require independent execution or domain review.",
            "Company-pattern alignment and provenance require human review against dated primary sources.",
            "A clean audit does not promote content into the trusted student-serving pool.",
        ],
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Bountycode content audit",
        "",
        f"- Files scanned: {report['files_scanned']}",
        f"- Items scanned: {report['items_scanned']}",
        f"- Issues: {len(report['issues'])}",
        f"- Severity counts: {report['severity_counts']}",
        "",
        "## Issues",
        "",
        "| Severity | File | Item ID | Code | Detail |",
        "|---|---|---|---|---|",
    ]
    for issue in report["issues"]:
        detail = issue["detail"].replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {issue['severity']} | {issue['file']} | {issue['item_id']} | {issue['code']} | {detail} |"
        )
    if not report["issues"]:
        lines.append("| — | — | — | — | No structural issues were detected. This is not proof of semantic correctness. |")
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in report["limitations"])
    if report["unreadable_files"]:
        lines.extend(["", "## Unreadable files", ""])
        lines.extend(f"- {item['file']}: {item['error']}" for item in report["unreadable_files"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    report = audit(args.root)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
