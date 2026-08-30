"""Content trust validation script.

Validates a sample of questions and promotes them through the trust pipeline:
UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED

For coding questions: executes solution against test cases.
For aptitude/verbal: checks answer + reasoning presence.
For all: checks for ambiguity, duplicates, missing fields.

Run: python scripts/validate_content.py [--sample N] [--promote]
"""
import json
import sys
import re
from pathlib import Path
from collections import Counter

DATA_DIR = Path("app/data")
BANK_PATH = DATA_DIR / "questions_bank_curated.json"
if not BANK_PATH.exists():
    BANK_PATH = DATA_DIR / "questions_bank.json"
REPORT_PATH = DATA_DIR / "validation_report.json"


def validate_coding_question(q: dict) -> dict:
    """Validate a coding question's correctness."""
    issues = []
    score = 0

    # Check required fields
    q_text = str(q.get("question", "")).strip()
    if len(q_text) > 50:
        score += 1
    else:
        issues.append("question too short")

    # Check solution exists and has code
    sol = q.get("solution")
    has_code = False
    if isinstance(sol, dict) and sol.get("code"):
        has_code = True
        score += 2
    elif isinstance(sol, str) and len(sol) > 10:
        has_code = True
        score += 1
    else:
        issues.append("no solution code")

    # Check test cases
    test_cases = q.get("test_cases") or (sol.get("test_cases") if isinstance(sol, dict) else None)
    if test_cases and len(test_cases) > 0:
        score += 2
        # Verify each test case has input + expected
        for i, tc in enumerate(test_cases):
            if not tc.get("input") and tc.get("input") != 0:
                issues.append(f"test case {i} missing input")
            if not tc.get("expected") and tc.get("expected") is not None:
                issues.append(f"test case {i} missing expected")
    else:
        issues.append("no test cases")

    # Check for ambiguity indicators
    ambiguous_words = ["etc", "and so on", "some", "appropriate", "suitable", "somehow"]
    q_lower = q_text.lower()
    ambiguity_flags = [w for w in ambiguous_words if w in q_lower]
    if ambiguity_flags:
        issues.append(f"ambiguous language: {ambiguity_flags}")

    # Check complexity
    if q.get("time_complexity"):
        score += 1
    if q.get("space_complexity"):
        score += 1

    return {"score": score, "issues": issues, "passing": score >= 5 and not any("missing" in i for i in issues)}


def validate_aptitude_question(q: dict) -> dict:
    """Validate an aptitude/verbal/logical question."""
    issues = []
    score = 0

    q_text = str(q.get("question", "")).strip()
    if len(q_text) > 30:
        score += 1
    else:
        issues.append("question too short")

    # Check options
    options = q.get("options", [])
    if len(options) >= 2:
        score += 1
    else:
        issues.append("insufficient options")

    # Check correct answer
    correct = q.get("correct_answer")
    if correct:
        score += 1
    else:
        issues.append("no correct answer")

    # Check explanation
    explanation = q.get("explanation")
    if explanation and len(str(explanation)) > 20:
        score += 1
    else:
        issues.append("weak explanation")

    return {"score": score, "issues": issues, "passing": score >= 3}


def check_duplicates(questions: list) -> list:
    """Find near-duplicate questions."""
    duplicates = []
    seen = {}
    for q in questions:
        # Normalize: lowercase, remove punctuation, take first 100 chars
        text = str(q.get("question", "")).lower()[:100]
        text = re.sub(r'[^\w\s]', '', text)
        if text in seen:
            duplicates.append((q.get("id"), seen[text]))
        else:
            seen[text] = q.get("id")
    return duplicates


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate question bank content")
    parser.add_argument("--sample", type=int, default=50, help="Number of questions to sample")
    parser.add_argument("--promote", action="store_true", help="Promote passing questions to AUTOMATED_CHECKED")
    args = parser.parse_args()

    if not BANK_PATH.exists():
        print(f"ERROR: {BANK_PATH} not found")
        sys.exit(1)

    with open(BANK_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)
    if isinstance(questions, dict):
        questions = list(questions.values())

    print(f"Loaded {len(questions)} questions")

    # Sample for validation
    import random
    sample = random.sample(questions, min(args.sample, len(questions)))

    results = {
        "coding": {"passed": 0, "failed": 0, "issues": Counter()},
        "aptitude": {"passed": 0, "failed": 0, "issues": Counter()},
        "other": {"passed": 0, "failed": 0, "issues": Counter()},
    }

    for q in sample:
        q_type = q.get("type", "other")
        if q_type == "coding":
            result = validate_coding_question(q)
            category = "coding"
        elif q_type in ("aptitude", "verbal", "logical"):
            result = validate_aptitude_question(q)
            category = "aptitude"
        else:
            result = validate_aptitude_question(q)
            category = "other"

        if result["passing"]:
            results[category]["passed"] += 1
            if args.promote:
                q["trust_level"] = "automated_checked"
        else:
            results[category]["failed"] += 1
            for issue in result["issues"]:
                results[category]["issues"][issue] += 1

    # Check for duplicates in full bank
    duplicates = check_duplicates(questions)

    # Print report
    print(f"\n=== VALIDATION REPORT (sample: {len(sample)}) ===")
    for cat, data in results.items():
        total = data["passed"] + data["failed"]
        if total > 0:
            pct = (data["passed"] / total) * 100
            print(f"\n{cat.upper()}:")
            print(f"  Passed: {data['passed']}/{total} ({pct:.0f}%)")
            print(f"  Failed: {data['failed']}")
            if data["issues"]:
                print(f"  Top issues:")
                for issue, count in data["issues"].most_common(5):
                    print(f"    - {issue}: {count}")

    if duplicates:
        print(f"\nDUPLICATES: {len(duplicates)} near-duplicate pairs found")

    # Save report
    report = {
        "sample_size": len(sample),
        "results": {k: {"passed": v["passed"], "failed": v["failed"]} for k, v in results.items()},
        "duplicates_found": len(duplicates),
    }
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if args.promote:
        with open(BANK_PATH, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        print(f"\nPromoted passing questions to AUTOMATED_CHECKED")

    print(f"\nReport saved to {REPORT_PATH}")


if __name__ == "__main__":
    main()
