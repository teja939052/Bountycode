#!/usr/bin/env python3
"""Content Authoring CLI — interactive tool for creating and validating questions.

Usage:
    python backend/scripts/content_author.py              # interactive mode
    python backend/scripts/content_author.py --dry-run     # validate without saving
    python backend/scripts/content_author.py --template coding  # generate template
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.content_verification import ContentVerifier


def generate_template(qtype: str) -> Dict[str, Any]:
    """Generate a question template for a given type."""
    base = {
        "type": qtype,
        "companies": [],
        "role": "SDE",
        "difficulty": "medium",
        "topic": "",
        "sub_topic": "",
        "question": "",
        "explanation": "",
        "hints": [],
        "frequency": 0,
        "source": "manual",
    }

    if qtype == "coding":
        base.update({
            "solution": {
                "code": "def solve():\n    # your solution\n    pass",
                "language": "python",
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
            },
            "test_cases": [
                {"input": "", "expected": ""},
            ],
        })
    elif qtype in ("mcq", "aptitude", "logical", "verbal"):
        base.update({
            "options": [
                {"id": "a", "text": "", "correct": True},
                {"id": "b", "text": "", "correct": False},
            ],
            "correct_answer": "a",
        })
    return base


def interactive_author() -> Dict[str, Any]:
    """Interactively author a question."""
    print("=" * 50)
    print("Content Authoring Tool")
    print("=" * 50)

    qtype = input("Question type (coding/mcq/aptitude/logical/verbal): ").strip().lower()
    if qtype not in ("coding", "mcq", "aptitude", "logical", "verbal"):
        print(f"Unknown type: {qtype}")
        sys.exit(1)

    q = generate_template(qtype)

    q["question"] = input("Question text: ").strip()
    q["topic"] = input("Topic: ").strip()
    q["sub_topic"] = input("Sub-topic (optional): ").strip()
    q["difficulty"] = input("Difficulty (easy/medium/hard) [medium]: ").strip() or "medium"

    companies = input("Companies (comma-separated, e.g. TCS,Infosys): ").strip()
    q["companies"] = [c.strip() for c in companies.split(",") if c.strip()]

    hints = input("Hints (one per line, empty line to finish):\n")
    hint_list = []
    while hints.strip():
        hint_list.append(hints.strip())
        hints = input()
    q["hints"] = hint_list

    if qtype == "coding":
        print("Solution code (end with EOF on its own line):")
        lines = []
        while True:
            line = input()
            if line == "EOF":
                break
            lines.append(line)
        q["solution"]["code"] = "\n".join(lines)

        print("Test cases (input|expected, empty line to finish):")
        tcs = []
        while True:
            line = input().strip()
            if not line:
                break
            parts = line.split("|", 1)
            tcs.append({
                "input": parts[0],
                "expected": parts[1] if len(parts) > 1 else "",
            })
        q["test_cases"] = tcs
    else:
        q["correct_answer"] = input("Correct answer: ").strip()

    q["explanation"] = input("Explanation: ").strip()

    return q


async def verify_question(q: Dict[str, Any]) -> Dict[str, Any]:
    """Verify a question and return the report."""
    verifier = ContentVerifier()
    return await verifier.verify(q)


def main():
    parser = argparse.ArgumentParser(description="Content Authoring CLI")
    parser.add_argument("--dry-run", action="store_true", help="Validate without saving")
    parser.add_argument("--template", choices=["coding", "mcq", "aptitude", "logical", "verbal"],
                        help="Generate a template")
    parser.add_argument("--verify-file", type=str, help="Verify questions from a JSON file")
    parser.add_argument("--output", type=str, help="Output file for template")
    args = parser.parse_args()

    if args.template:
        tmpl = generate_template(args.template)
        output = json.dumps(tmpl, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Template written to {args.output}")
        else:
            print(output)
        return

    if args.verify_file:
        with open(args.verify_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        questions = data if isinstance(data, list) else [data]
        import asyncio
        verifier = ContentVerifier()
        report = asyncio.run(verifier.verify_batch(questions))
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
        return

    # Interactive mode
    q = interactive_author()

    if args.dry_run:
        print("\n--- Dry Run: Validation Only ---")
        import asyncio
        report = asyncio.run(verify_question(q))
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    else:
        # Append to questions_bank.json
        bank_path = os.path.join(
            os.path.dirname(__file__), "..", "app", "data", "questions_bank.json"
        )
        try:
            with open(bank_path, "r", encoding="utf-8") as f:
                bank = json.load(f)
        except Exception:
            bank = []

        # Assign id
        if not q.get("id"):
            q["id"] = f"authored_{len(bank):06d}"

        # Verify before saving
        import asyncio
        report = asyncio.run(verify_question(q))
        print("\n--- Verification Report ---")
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))

        if report.get("recommendation") == "REJECT":
            print("\nQuestion REJECTED. Fix issues and try again.")
            sys.exit(1)

        bank.append(q)
        with open(bank_path, "w", encoding="utf-8") as f:
            json.dump(bank, f, indent=2, ensure_ascii=False)
        print(f"\nQuestion saved to {bank_path} (id: {q['id']})")


if __name__ == "__main__":
    main()
