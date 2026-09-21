#!/usr/bin/env python3
"""Quarantine placeholder interview questions in interview_question_bank.py.

This script:
1. Identifies 1,241 placeholder questions (pattern: "Interview question N: Explain X...")
2. Adds `"quarantined": true,` INSIDE each placeholder dict
3. Updates helper functions to filter quarantined questions by default
4. Preserves all IDs and provenance
5. Writes a quarantine report
"""

import re
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "app" / "data"
PY_BANK = BASE / "interview_question_bank.py"
QUARANTINE_REPORT = BASE / "interview_quarantine_report.json"

# Placeholder patterns to quarantine
PLACEHOLDER_PATTERNS = [
    re.compile(r"Technical interview question \d+:", re.IGNORECASE),
    re.compile(r"Interview question \d+:", re.IGNORECASE),
    re.compile(r"Explain \w+ concepts with examples\??$", re.IGNORECASE),
]


def is_placeholder(question_text: str) -> bool:
    """Check if a question text matches placeholder patterns."""
    if not question_text:
        return True
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(question_text):
            return True
    return False


def find_question_blocks(lines):
    """Find question blocks by tracking brace depth."""
    blocks = []
    in_questions = False
    block_start = None
    brace_depth = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect start of INTERVIEW_QUESTIONS list
        if "INTERVIEW_QUESTIONS = [" in line:
            in_questions = True
            continue
        
        if not in_questions:
            continue
        
        # Track brace depth
        brace_depth += stripped.count("{") - stripped.count("}")
        
        # Detect start of a question dict (opening brace at depth 1)
        if stripped == "{" and brace_depth == 1:
            block_start = i
            continue
        
        # Detect end of a question dict (closing brace at depth 0)
        if stripped in ("},", "}") and brace_depth == 0 and block_start is not None:
            blocks.append((block_start, i))
            block_start = None
            continue
    
    return blocks


def quarantine_placeholders():
    """Add quarantined flag to placeholder questions."""
    print("=== Quarantining Placeholder Interview Questions ===\n")
    
    # Read the file
    text = PY_BANK.read_text(encoding="utf-8")
    lines = text.split("\n")
    
    # Find all question blocks
    question_blocks = find_question_blocks(lines)
    print(f"Found {len(question_blocks)} question blocks")
    
    # Process each question block in reverse to maintain indices
    quarantined_count = 0
    kept_count = 0
    quarantine_ids = []
    
    for start, end in reversed(question_blocks):
        block_text = "\n".join(lines[start:end+1])
        
        # Extract question text
        q_match = re.search(r'"question":\s*"([^"]+)"', block_text)
        if not q_match:
            continue
        
        question_text = q_match.group(1)
        question_id_match = re.search(r'"id":\s*"([^"]+)"', block_text)
        question_id = question_id_match.group(1) if question_id_match else "unknown"
        
        if is_placeholder(question_text):
            # Check if quarantined field already exists
            if '"quarantined"' not in block_text:
                # Find the line with "time_estimate_seconds" or the last field
                # Insert after the last field line, before the closing brace
                insert_idx = end - 1  # Start from the line before closing brace
                
                # Move up to find the last actual field (skip empty lines)
                while insert_idx > start and lines[insert_idx].strip() in ("", "},"):
                    insert_idx -= 1
                
                # Now insert after this line
                indent = "        "
                lines.insert(insert_idx + 1, f'{indent}"quarantined": true,')
                quarantined_count += 1
                quarantine_ids.append(question_id)
        else:
            kept_count += 1
    
    print(f"Quarantined: {quarantined_count}")
    print(f"Kept (no quarantine flag): {kept_count}")
    
    # Write back the file
    modified_text = "\n".join(lines)
    PY_BANK.write_text(modified_text, encoding="utf-8")
    print(f"\nUpdated {PY_BANK}")
    
    # Update helper functions to filter quarantined
    update_helper_functions()
    
    # Write report
    report = {
        "quarantined_count": quarantined_count,
        "kept_count": kept_count,
        "quarantine_ids_sample": quarantine_ids[:10],
        "all_quarantine_ids": quarantine_ids,
        "timestamp": "2026-09-09",
        "action": "quarantined",
        "preserved": True,
    }
    QUARANTINE_REPORT.write_text(json.dumps(report, indent=2))
    print(f"\nReport saved to: {QUARANTINE_REPORT}")


def update_helper_functions():
    """Update helper functions to filter out quarantined questions."""
    print("\n=== Updating Helper Functions ===\n")
    
    text = PY_BANK.read_text(encoding="utf-8")
    original_text = text
    
    # Update get_interview_questions_by_category
    old_category = '''def get_interview_questions_by_category(category: str) -> list:
    return [q for q in INTERVIEW_QUESTIONS if q["category"] == category]'''
    new_category = '''def get_interview_questions_by_category(category: str) -> list:
    return [q for q in INTERVIEW_QUESTIONS if q.get("category") == category and not q.get("quarantined", False)]'''
    if old_category in text:
        text = text.replace(old_category, new_category)
        print("Updated get_interview_questions_by_category")
    else:
        print("WARNING: Could not find get_interview_questions_by_category")
    
    # Update get_interview_questions_by_company
    old_company = '''def get_interview_questions_by_company(company: str) -> list:
    return [q for q in INTERVIEW_QUESTIONS if company in q.get("company_tags", [])]'''
    new_company = '''def get_interview_questions_by_company(company: str) -> list:
    return [q for q in INTERVIEW_QUESTIONS if company in q.get("company_tags", []) and not q.get("quarantined", False)]'''
    if old_company in text:
        text = text.replace(old_company, new_company)
        print("Updated get_interview_questions_by_company")
    else:
        print("WARNING: Could not find get_interview_questions_by_company")
    
    # Update get_all_interview_topics
    old_topics = '''def get_all_interview_topics() -> list:
    return list(set(q["topic"] for q in INTERVIEW_QUESTIONS))'''
    new_topics = '''def get_all_interview_topics() -> list:
    return list(set(q["topic"] for q in INTERVIEW_QUESTIONS if not q.get("quarantined", False)))'''
    if old_topics in text:
        text = text.replace(old_topics, new_topics)
        print("Updated get_all_interview_topics")
    else:
        print("WARNING: Could not find get_all_interview_topics")
    
    # Update get_interview_question_count
    old_count = '''def get_interview_question_count() -> int:
    return len(INTERVIEW_QUESTIONS)'''
    new_count = '''def get_interview_question_count() -> int:
    return len([q for q in INTERVIEW_QUESTIONS if not q.get("quarantined", False)])'''
    if old_count in text:
        text = text.replace(old_count, new_count)
        print("Updated get_interview_question_count")
    else:
        print("WARNING: Could not find get_interview_question_count")
    
    # Update get_interview_questions_summary
    old_summary = '''def get_interview_questions_summary() -> dict:
    summary = {}
    for q in INTERVIEW_QUESTIONS:
        cat = q["category"]
        if cat not in summary:
            summary[cat] = {"count": 0, "companies": set()}
        summary[cat]["count"] += 1
        summary[cat]["companies"].update(q.get("company_tags", []))
    return summary'''
    new_summary = '''def get_interview_questions_summary() -> dict:
    summary = {}
    for q in INTERVIEW_QUESTIONS:
        if q.get("quarantined", False):
            continue
        cat = q.get("category", "Unknown")
        if cat not in summary:
            summary[cat] = {"count": 0, "companies": set()}
        summary[cat]["count"] += 1
        summary[cat]["companies"].update(q.get("company_tags", []))
    return summary'''
    if old_summary in text:
        text = text.replace(old_summary, new_summary)
        print("Updated get_interview_questions_summary")
    else:
        print("WARNING: Could not find get_interview_questions_summary")
    
    if text != original_text:
        PY_BANK.write_text(text, encoding="utf-8")
        print("\nHelper functions updated successfully")
    else:
        print("\nNo changes made to helper functions")


def verify_quarantine():
    """Verify that quarantined questions are properly marked and filtered."""
    print("\n=== Verifying Quarantine ===\n")
    
    text = PY_BANK.read_text(encoding="utf-8")
    
    # Count quarantined
    quarantined_count = text.count('"quarantined": true')
    print(f"Questions marked quarantined: {quarantined_count}")
    
    # Count total questions
    total_count = text.count('"id":')
    print(f"Total questions: {total_count}")
    
    # Verify helper functions are updated
    checks = [
        'not q.get("quarantined", False)',
    ]
    for check in checks:
        count = text.count(check)
        print(f"Helper function filter '{check}': {count} occurrences")
    
    # Sample a quarantined question - look for one with quarantined inside the dict
    quarantine_sample = re.search(r'\{[^}]+\"quarantined\":\s*true[^}]+\}', text)
    if quarantine_sample:
        id_match = re.search(r'"id":\s*"([^"]+)"', quarantine_sample.group(0))
        if id_match:
            print(f"\nSample quarantined question: {id_match.group(1)}")
    
    return quarantined_count, total_count


def main():
    # Step 1: Quarantine placeholders
    quarantine_placeholders()
    
    # Step 2: Verify
    quarantined, total = verify_quarantine()
    
    print(f"\n=== Summary ===")
    print(f"Total questions: {total}")
    print(f"Quarantined: {quarantined}")
    print(f"Runtime-eligible: {total - quarantined}")
    print(f"\nQuarantine complete. Placeholder questions are marked but preserved.")


if __name__ == "__main__":
    main()
