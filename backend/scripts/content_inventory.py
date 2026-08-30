"""Phase 0: Content Inventory.

Classifies every question in the bank:
- COMPLETE: has full problem statement + solution + tests
- SHELL: title-only, metadata without substance
- INCOMPLETE: partial content (has some fields but not all)
- DUPLICATE: exact or near-duplicate of another question
- MALFORMED: missing critical fields or unreadable

Outputs an honest inventory report.
"""
import json
import re
from pathlib import Path
from collections import Counter
from datetime import datetime

BANK_PATH = Path("app/data/questions_bank_curated.json")
if not BANK_PATH.exists():
    BANK_PATH = Path("app/data/questions_bank.json")
REPORT_PATH = Path("app/data/inventory_report.json")


def classify_question(q: dict) -> dict:
    """Classify a single question."""
    issues = []
    scores = {"content": 0, "solution": 0, "tests": 0, "pedagogy": 0}

    # --- Content check ---
    q_text = str(q.get("question", "")).strip()
    text_len = len(q_text)

    if text_len > 200:
        scores["content"] = 3
    elif text_len > 100:
        scores["content"] = 2
    elif text_len > 50:
        scores["content"] = 1
    else:
        issues.append(f"question_too_short ({text_len} chars)")

    # Check for constraints/examples in question
    has_constraints = any(kw in q_text.lower() for kw in ["constraint", "input", "output", "example"])
    if has_constraints:
        scores["content"] += 1

    # --- Solution check ---
    sol = q.get("solution")
    if isinstance(sol, dict) and sol.get("code"):
        code = str(sol["code"]).strip()
        if len(code) > 50:
            scores["solution"] = 3
        elif len(code) > 20:
            scores["solution"] = 2
        else:
            scores["solution"] = 1
            issues.append("solution_too_short")
    elif isinstance(sol, str) and len(sol) > 30:
        scores["solution"] = 1
    else:
        issues.append("no_solution")

    # --- Test check ---
    test_cases = q.get("test_cases") or (sol.get("test_cases") if isinstance(sol, dict) else None)
    if test_cases and len(test_cases) >= 2:
        scores["tests"] = 3
        # Verify each test has input + expected
        for i, tc in enumerate(test_cases):
            if not tc.get("input") and tc.get("input") != 0:
                issues.append(f"test_{i}_missing_input")
            if tc.get("expected") is None:
                issues.append(f"test_{i}_missing_expected")
    elif test_cases and len(test_cases) == 1:
        scores["tests"] = 1
        issues.append("only_one_test")
    else:
        issues.append("no_test_cases")

    # --- Pedagogy check ---
    if q.get("explanation") and len(str(q.get("explanation"))) > 30:
        scores["pedagogy"] += 1
    else:
        issues.append("weak_explanation")

    if q.get("hints") and len(q.get("hints", [])) >= 2:
        scores["pedagogy"] += 1

    if q.get("difficulty") in ("easy", "medium", "hard"):
        scores["pedagogy"] += 1

    if q.get("topic"):
        scores["pedagogy"] += 1

    # --- Classification ---
    total_score = sum(scores.values())

    if total_score >= 10 and scores["content"] >= 3 and scores["solution"] >= 2 and scores["tests"] >= 2:
        classification = "COMPLETE"
    elif total_score >= 6 and scores["content"] >= 2:
        classification = "INCOMPLETE"
    elif scores["content"] <= 1:
        classification = "SHELL"
    else:
        classification = "INCOMPLETE"

    return {
        "classification": classification,
        "scores": scores,
        "total_score": total_score,
        "issues": issues,
        "text_length": text_len,
    }


def find_duplicates(questions: list) -> dict:
    """Find exact and near-duplicates. Returns id -> canonical_id mapping."""
    # Group by normalized first 100 chars of question text
    groups = {}
    for q in questions:
        text = str(q.get("question", "")).lower()[:100]
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if text not in groups:
            groups[text] = []
        groups[text].append(q.get("id"))

    # Map duplicates to first (canonical) id
    duplicates = {}
    for text, ids in groups.items():
        if len(ids) > 1:
            canonical = ids[0]
            for dup_id in ids[1:]:
                duplicates[dup_id] = canonical

    return duplicates


def main():
    if not BANK_PATH.exists():
        print(f"ERROR: {BANK_PATH} not found")
        return

    with open(BANK_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)
    if isinstance(questions, dict):
        questions = list(questions.values())

    print(f"Loaded {len(questions)} questions")

    # Classify each question
    classifications = Counter()
    by_type = {}
    complete_questions = []
    shell_questions = []
    incomplete_questions = []

    for q in questions:
        result = classify_question(q)
        q_type = q.get("type", "unknown")
        classifications[result["classification"]] += 1

        if q_type not in by_type:
            by_type[q_type] = Counter()
        by_type[q_type][result["classification"]] += 1

        if result["classification"] == "COMPLETE":
            complete_questions.append({
                "id": q.get("id"),
                "topic": q.get("topic"),
                "type": q_type,
                "difficulty": q.get("difficulty"),
                "score": result["total_score"],
            })
        elif result["classification"] == "SHELL":
            shell_questions.append(q.get("id"))
        else:
            incomplete_questions.append(q.get("id"))

    # Find duplicates
    duplicates = find_duplicates(questions)
    duplicate_ids = set(duplicates.keys())

    # Remove duplicates from complete list
    unique_complete = [q for q in complete_questions if q["id"] not in duplicate_ids]

    # --- Report ---
    print(f"\n=== CONTENT INVENTORY ===")
    print(f"Total questions: {len(questions)}")
    print(f"\nBy classification:")
    for cls, count in classifications.most_common():
        print(f"  {cls:12s}: {count}")

    print(f"\nBy type:")
    for q_type, cls_counts in by_type.items():
        print(f"  {q_type}:")
        for cls, count in cls_counts.most_common():
            print(f"    {cls:12s}: {count}")

    print(f"\nDuplicates found: {len(duplicates)}")
    print(f"Unique complete questions: {len(unique_complete)}")

    # Show top complete questions by topic
    topic_counts = Counter(q["topic"] for q in unique_complete)
    print(f"\nComplete questions by topic:")
    for topic, count in topic_counts.most_common(20):
        print(f"  {topic:30s}: {count}")

    # Save report
    report = {
        "generated_at": datetime.now().isoformat(),
        "total_questions": len(questions),
        "classifications": dict(classifications),
        "duplicates_found": len(duplicates),
        "unique_complete": len(unique_complete),
        "shell_count": len(shell_questions),
        "incomplete_count": len(incomplete_questions),
        "by_type": {k: dict(v) for k, v in by_type.items()},
        "complete_by_topic": dict(topic_counts.most_common(30)),
        "sample_complete": unique_complete[:20],
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to {REPORT_PATH}")

    # Honest summary
    print(f"\n{'='*60}")
    print(f"HONEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total records: {len(questions)}")
    print(f"Unique complete problems: {len(unique_complete)}")
    print(f"Shell/metadata-only: {len(shell_questions)}")
    print(f"Incomplete: {len(incomplete_questions)}")
    print(f"Duplicates removed: {len(duplicates)}")
    print(f"\nMarketable as 'verified': 0 (none have been correctness-verified yet)")
    print(f"Potentially usable: {len(unique_complete)} (have full problem + solution + tests)")


if __name__ == "__main__":
    main()
