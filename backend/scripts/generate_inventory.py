"""Generate a fresh question-level inventory from all source files.

This script scans every question JSON file under backend/app/data/ and
backend/app/content/, normalizes each question onto a canonical schema,
and produces a machine-readable inventory with trust status, executability,
duplicate clusters, and recommended actions.

Usage:
    python backend/scripts/generate_inventory.py
"""

import json
import os
import re
import subprocess
import sys
import hashlib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = BACKEND_ROOT / "app" / "data"
CONTENT_DIR = BACKEND_ROOT / "app" / "content"

OUTPUT_DIR = BACKEND_ROOT / "docs" / "research"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INVENTORY_PATH = OUTPUT_DIR / "question_inventory.json"
COVERAGE_PATH = OUTPUT_DIR / "topic_coverage_report.json"
TRUST_PATH = OUTPUT_DIR / "trust_state_audit.json"
DUPLICATE_PATH = OUTPUT_DIR / "duplicate_audit.json"

# Canonical field mapping: source_field -> canonical_field
CANONICAL_MAP = {
    "id": ["id", "_id", "question_id"],
    "title": ["title", "question_title"],
    "question": ["question", "statement", "description"],
    "type": ["type", "question_type"],
    "difficulty": ["difficulty"],
    "topic": ["topic", "subject"],
    "sub_topic": ["sub_topic", "subtopic"],
    "companies": ["companies", "company", "company_tags"],
    "roles": ["roles", "role"],
    "trust_status": ["trust_status", "trust", "review_status", "status"],
    "provenance": ["provenance", "source_bank", "source", "source_type"],
    "solution": ["solution"],
    "test_cases": ["test_cases", "testcases", "visible_test_cases", "hidden_testcases"],
    "options": ["options"],
    "correct_answer": ["correct_answer", "correct_index"],
    "explanation": ["explanation", "worked_solution"],
    "rubric": ["rubric", "evaluation_criteria"],
    "sql_schema": ["sql_schema", "schema_ddl"],
    "buggy_code": ["buggy_code"],
    "correct_code": ["correct_code"],
}

TRUST_RANK = {
    "verified": 3, "reviewed": 2, "human_reviewed": 2, "trusted": 3,
    "automated_checked": 1, "automated_checked": 1,
    "needs_review": 1, "unverified": 0, "quarantined": -1,
}

MCQ_TYPES = {"aptitude", "logical", "verbal", "hr", "behavioral", "cs_fundamentals", "cs", "mcq"}
CODING_TYPES = {"coding", "code"}
SQL_TYPES = {"sql"}
DEBUG_TYPES = {"debugging"}
INTERVIEW_TYPES = {"interview", "system_design", "gd", "group_discussion", "behavioral", "hr"}


def _get_field(q: dict, aliases: list[str], default=None):
    for alias in aliases:
        if alias in q and q[alias] is not None:
            return q[alias]
    return default


def _normalize_id(q: dict, idx: int) -> str:
    qid = _get_field(q, ["id", "_id", "question_id"])
    if qid:
        return str(qid)
    return f"gen_{idx:06d}"


def _normalize_companies(q: dict) -> list[str]:
    companies = _get_field(q, ["companies", "company", "company_tags"], [])
    if isinstance(companies, str):
        companies = [companies]
    if not isinstance(companies, list):
        companies = []
    return [str(c).strip() for c in companies if str(c).strip()]


def _normalize_roles(q: dict) -> list[str]:
    roles = _get_field(q, ["roles", "role"], [])
    if isinstance(roles, str):
        roles = [roles]
    if not isinstance(roles, list):
        roles = []
    return [str(r).strip() for r in roles if str(r).strip()]


def _normalize_test_cases(q: dict) -> list:
    tcs = _get_field(q, ["test_cases", "testcases", "visible_test_cases", "hidden_testcases"], [])
    if not isinstance(tcs, list):
        tcs = []
    return tcs


def _normalize_options(q: dict):
    opts = _get_field(q, ["options"], None)
    if opts is None:
        return None
    if isinstance(opts, dict):
        return opts
    if isinstance(opts, list):
        return {chr(65 + i): str(o) for i, o in enumerate(opts)}
    return None


def _is_executable(q: dict) -> bool:
    qtype = str(_get_field(q, ["type", "question_type"], "coding")).lower()
    if qtype in CODING_TYPES | SQL_TYPES | DEBUG_TYPES:
        tcs = _normalize_test_cases(q)
        if not tcs:
            return False
        if qtype in SQL_TYPES and not _get_field(q, ["sql_schema", "schema_ddl"], None):
            return False
        return True
    if qtype in MCQ_TYPES:
        opts = _normalize_options(q)
        correct = str(_get_field(q, ["correct_answer", "correct_index"], "")).strip().upper()
        if isinstance(opts, dict) and len(opts) >= 4:
            return correct in ("A", "B", "C", "D")
        if isinstance(opts, list) and len(opts) >= 4:
            return bool(correct)
        return False
    if qtype in INTERVIEW_TYPES:
        return bool(_get_field(q, ["rubric", "evaluation_criteria", "worked_solution"], None))
    tcs = _normalize_test_cases(q)
    return len(tcs) > 0 or bool(_get_field(q, ["correct_answer", "answer"], None))


def _detect_duplicate_key(q: dict) -> str:
    """Normalized title key for duplicate detection."""
    title = str(_get_field(q, ["title", "question_title", "question", "statement"], "")).strip()
    key = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()[:80]
    return key


def _missing_fields(q: dict) -> list[str]:
    """Return list of missing canonical fields based on question type."""
    missing = []
    qtype = str(_get_field(q, ["type", "question_type"], "coding")).lower()

    if not _get_field(q, ["question", "title", "question_title", "statement", "description"], None):
        missing.append("question_text")
    if not _get_field(q, ["difficulty"], None):
        missing.append("difficulty")
    if not _get_field(q, ["topic"], None):
        missing.append("topic")
    if not _get_field(q, ["provenance", "source_bank", "source"], None):
        missing.append("provenance")

    if qtype in CODING_TYPES:
        if not _get_field(q, ["solution"], None):
            missing.append("solution")
        if not _normalize_test_cases(q):
            missing.append("test_cases")
        if not _get_field(q, ["constraints"], None):
            missing.append("constraints")
        if not _get_field(q, ["examples"], None):
            missing.append("examples")
    elif qtype in SQL_TYPES:
        if not _get_field(q, ["sql_schema", "schema_ddl"], None):
            missing.append("sql_schema")
        if not _normalize_test_cases(q):
            missing.append("test_cases")
        if not _get_field(q, ["correct_answer"], None):
            missing.append("correct_answer")
    elif qtype in MCQ_TYPES:
        opts = _normalize_options(q)
        if not opts or len(opts) < 4:
            missing.append("options")
        correct = str(_get_field(q, ["correct_answer", "correct_index"], "")).strip().upper()
        if correct not in ("A", "B", "C", "D"):
            missing.append("correct_answer")
        if not _get_field(q, ["explanation", "worked_solution"], None):
            missing.append("explanation")
    elif qtype in INTERVIEW_TYPES:
        if not _get_field(q, ["rubric", "evaluation_criteria", "worked_solution"], None):
            missing.append("rubric_or_evaluation_criteria")
        if not _get_field(q, ["explanation"], None):
            missing.append("explanation")

    return missing


def _recommended_action(q: dict, is_duplicate: bool, dup_count: int) -> str:
    """Determine recommended action for a question."""
    qtype = str(_get_field(q, ["type", "question_type"], "coding")).lower()
    trust = str(_get_field(q, ["trust_status", "trust", "review_status", "status"], "unverified")).lower()
    missing = _missing_fields(q)
    executable = _is_executable(q)

    if trust == "quarantined":
        return "QUARANTINE"
    if is_duplicate and dup_count > 1:
        return "REMOVE_DUPLICATE"
    if trust in ("unverified", "needs_review") and missing:
        return "REVIEW"
    if trust == "automated_checked" and not executable:
        return "REPAIR"
    if missing:
        return "REPAIR"
    if trust == "unverified":
        return "REVIEW"
    if executable and trust in ("verified", "reviewed", "trusted", "human_reviewed"):
        return "KEEP"
    return "REVIEW"


def _compute_hash(q: dict) -> str:
    """Content hash for duplicate detection beyond title."""
    title = str(_get_field(q, ["title", "question_title", "question", "statement"], "")).strip()
    body = str(_get_field(q, ["question", "description", "statement"], "")).strip()
    content = f"{title}|{body}".lower()
    return hashlib.md5(content.encode("utf-8")).hexdigest()[:12]


def scan_directory(directory: Path, label: str) -> list[dict]:
    """Scan all JSON files in a directory for questions."""
    results = []
    if not directory.exists():
        return results

    for json_file in sorted(directory.rglob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  SKIP {json_file}: {e}", file=sys.stderr)
            continue

        items = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and isinstance(data.get("questions"), list):
            items = data["questions"]
        elif isinstance(data, dict):
            # Check for nested question lists
            for v in data.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    items = v
                    break

        rel_path = json_file.relative_to(BACKEND_ROOT)
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            qid = _normalize_id(item, idx)
            qtype = str(_get_field(item, ["type", "question_type"], "coding")).lower()
            title = str(_get_field(item, ["title", "question_title", "question", "statement"], "")).strip()
            question_text = str(_get_field(item, ["question", "description", "statement"], title)).strip()
            topic = str(_get_field(item, ["topic", "subject"], "General")).strip()
            sub_topic = str(_get_field(item, ["sub_topic", "subtopic"], "")).strip()
            difficulty = str(_get_field(item, ["difficulty"], "medium")).strip().lower()
            companies = _normalize_companies(item)
            roles = _normalize_roles(item)
            trust = str(_get_field(item, ["trust_status", "trust", "review_status", "status"], "unverified")).strip().lower()
            provenance = str(_get_field(item, ["provenance", "source_bank", "source", "source_type"], label)).strip()
            solution = _get_field(item, ["solution"], None)
            test_cases = _normalize_test_cases(item)
            options = _normalize_options(item)
            correct = _get_field(item, ["correct_answer", "correct_index"], None)
            explanation = _get_field(item, ["explanation", "worked_solution"], "")
            rubric = _get_field(item, ["rubric", "evaluation_criteria"], None)
            sql_schema = _get_field(item, ["sql_schema", "schema_ddl"], None)

            results.append({
                "canonical_question_id": qid,
                "source_file": str(rel_path),
                "source_bank_owner": label,
                "question_type": qtype,
                "title": title,
                "question_text": question_text[:200],
                "topic": topic,
                "sub_topic": sub_topic,
                "difficulty": difficulty,
                "companies": companies,
                "roles": roles,
                "trust_status": trust,
                "provenance": provenance,
                "has_solution": bool(solution and (isinstance(solution, dict) and bool(solution.get("code")) or bool(solution))),
                "test_case_count": len(test_cases),
                "has_options": bool(options),
                "option_count": len(options) if options else 0,
                "has_correct_answer": bool(correct),
                "has_explanation": bool(explanation),
                "has_rubric": bool(rubric),
                "has_sql_schema": bool(sql_schema),
                "content_hash": _compute_hash(item),
                "missing_fields": _missing_fields(item),
                "executable": _is_executable(item),
                "recommended_action": "",  # filled after dedup
            })

    return results


def _get_git_sha() -> str:
    """Return the current git commit SHA, or 'unknown' if not available."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=BACKEND_ROOT.parent,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()[:12]
    except Exception:
        pass
    return "unknown"


def main():
    print("=== BountyCode Question Bank Inventory Generator ===\n")

    all_questions = []

    # Scan data directory
    print(f"Scanning {DATA_DIR}...")
    data_questions = scan_directory(DATA_DIR, "question_store")
    all_questions.extend(data_questions)
    print(f"  Found {len(data_questions)} questions in data/")

    # Scan content directory
    print(f"Scanning {CONTENT_DIR}...")
    content_questions = scan_directory(CONTENT_DIR, "quiz_service")
    all_questions.extend(content_questions)
    print(f"  Found {len(content_questions)} questions in content/")

    print(f"\nTotal raw questions: {len(all_questions)}")

    # Deduplicate by normalized title key
    seen: dict[str, list[dict]] = defaultdict(list)
    for q in all_questions:
        key = _detect_duplicate_key(q)
        if key:
            seen[key].append(q)

    # Mark duplicates and set recommended actions
    for key, group in seen.items():
        if len(group) > 1:
            # Sort by trust rank then quality
            group.sort(key=lambda q: (TRUST_RANK.get(q["trust_status"], 0), q["test_case_count"]), reverse=True)
            for i, q in enumerate(group):
                q["duplicate_cluster"] = key
                q["is_duplicate"] = True
                q["dup_cluster_size"] = len(group)
        else:
            group[0]["duplicate_cluster"] = None
            group[0]["is_duplicate"] = False
            group[0]["dup_cluster_size"] = 1

    # Set recommended actions
    for q in all_questions:
        q["recommended_action"] = _recommended_action(
            q, q.get("is_duplicate", False), q.get("dup_cluster_size", 1)
        )

    # Compute statistics
    total = len(all_questions)
    servable = sum(1 for q in all_questions if q["trust_status"] in ("verified", "reviewed", "trusted", "human_reviewed") and q["executable"])
    by_type = defaultdict(int)
    by_trust = defaultdict(int)
    by_topic = defaultdict(int)
    by_difficulty = defaultdict(int)
    actions = defaultdict(int)
    duplicate_clusters = 0
    dup_questions = 0

    for q in all_questions:
        by_type[q["question_type"]] += 1
        by_trust[q["trust_status"]] += 1
        by_topic[q["topic"]] += 1
        by_difficulty[q["difficulty"]] += 1
        actions[q["recommended_action"]] += 1
        if q.get("is_duplicate"):
            dup_questions += 1

    duplicate_clusters = sum(1 for g in seen.values() if len(g) > 1)

    git_sha = _get_git_sha()
    now = datetime.now(timezone.utc).isoformat()

    # Write inventory
    inventory = {
        "generated_at": now,
        "git_commit_sha": git_sha,
        "script_version": "1.0.0",
        "total_raw": total,
        "unique_titles": len(seen),
        "duplicate_clusters": duplicate_clusters,
        "duplicate_questions": dup_questions,
        "servable": servable,
        "not_servable": total - servable,
        "by_type": dict(by_type),
        "by_trust": dict(by_trust),
        "by_topic": dict(by_topic),
        "by_difficulty": dict(by_difficulty),
        "recommended_actions": dict(actions),
        "sources_included": ["backend/app/data/", "backend/app/content/"],
        "sources_excluded": ["backend/app/data/backups/"],
        "runtime_serving_rules": {
            "servable_trust_statuses": ["verified", "reviewed"],
            "trust_lifecycle": ["unverified", "needs_review", "automated_checked", "reviewed", "verified"],
            "coding_requires_test_cases": True,
            "sql_requires_schema": True,
            "mcq_requires_valid_options_and_answer": True,
            "interview_requires_rubric": True,
        },
        "questions": all_questions,
    }

    with open(INVENTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)

    print(f"\n=== INVENTORY SUMMARY ===")
    print(f"Total raw questions: {total}")
    print(f"Unique titles: {len(seen)}")
    print(f"Duplicate clusters: {duplicate_clusters}")
    print(f"Questions in duplicate clusters: {dup_questions}")
    print(f"Servable: {servable}")
    print(f"Not servable: {total - servable}")
    print(f"\nBy type: {dict(by_type)}")
    print(f"By trust: {dict(by_trust)}")
    print(f"By difficulty: {dict(by_difficulty)}")
    print(f"Recommended actions: {dict(actions)}")
    print(f"\nInventory written to {INVENTORY_PATH}")

    # Topic coverage report
    coverage = {
        "generated_at": inventory["generated_at"],
        "by_topic": {},
    }
    for topic, count in sorted(by_topic.items(), key=lambda x: -x[1]):
        topic_servable = sum(1 for q in all_questions if q["topic"] == topic and q["trust_status"] in ("verified", "reviewed", "trusted", "human_reviewed") and q["executable"])
        coverage["by_topic"][topic] = {
            "total": count,
            "servable": topic_servable,
            "by_difficulty": dict(sorted(
                ((d, sum(1 for q in all_questions if q["topic"] == topic and q["difficulty"] == d))
                 for d in by_difficulty),
                key=lambda x: -x[1]
            )),
        }
    with open(COVERAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(coverage, f, indent=2, ensure_ascii=False)
    print(f"Topic coverage written to {COVERAGE_PATH}")

    # Trust state audit
    trust_audit = {
        "generated_at": inventory["generated_at"],
        "by_trust": {},
    }
    for trust, count in sorted(by_trust.items(), key=lambda x: -TRUST_RANK.get(x[0], 0)):
        trust_exec = sum(1 for q in all_questions if q["trust_status"] == trust and q["executable"])
        trust_audit["by_trust"][trust] = {
            "total": count,
            "executable": trust_exec,
            "not_executable": count - trust_exec,
        }
    with open(TRUST_PATH, "w", encoding="utf-8") as f:
        json.dump(trust_audit, f, indent=2, ensure_ascii=False)
    print(f"Trust state audit written to {TRUST_PATH}")

    # Duplicate audit
    dup_audit = {
        "generated_at": inventory["generated_at"],
        "total_clusters": duplicate_clusters,
        "clusters": [],
    }
    for key, group in sorted(seen.items(), key=lambda x: -len(x[1])):
        if len(group) > 1:
            dup_audit["clusters"].append({
                "key": key,
                "size": len(group),
                "questions": [
                    {
                        "id": q["canonical_question_id"],
                        "source_file": q["source_file"],
                        "trust_status": q["trust_status"],
                        "executable": q["executable"],
                        "recommended_action": q["recommended_action"],
                    }
                    for q in group
                ],
            })
    with open(DUPLICATE_PATH, "w", encoding="utf-8") as f:
        json.dump(dup_audit, f, indent=2, ensure_ascii=False)
    print(f"Duplicate audit written to {DUPLICATE_PATH}")


if __name__ == "__main__":
    main()
