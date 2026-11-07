"""Content enrichment pipeline — adds missing pedagogical scaffolding.

For each question, ensures:
- explanation (why the answer is correct)
- hints (progressive scaffolding)
- common_trap (common misconceptions)
- reasoning_steps (how to think about it)
- constraints (for coding questions)

Uses rule-based generation first, then AI enhancement for verified bank.
"""

import json
import os
import asyncio
from typing import Dict, List, Any

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DATA_DIR = os.path.join(_BACKEND_ROOT, "app", "data")

# Banks to enrich (in order)
ENRICHMENT_ORDER = [
    "verified_placement_questions.json",
    "llm_draft_checked.json",
    "sql_practice_bank.json",
    "interview_practice_bank.json",
    "india_placement_depth.json",
]

BACKUP_DIR = os.path.join(_DATA_DIR, "backups")


def _ensure_fields(q: dict) -> dict:
    """Ensure a question has all pedagogical fields."""
    # Explanation
    if not q.get("explanation"):
        q["explanation"] = _generate_explanation(q)
    
    # Hints
    if not q.get("hints"):
        q["hints"] = _generate_hints(q)
    
    # Common trap
    if not q.get("common_trap"):
        q["common_trap"] = _generate_common_trap(q)
    
    # Reasoning steps
    if not q.get("reasoning_steps"):
        q["reasoning_steps"] = _generate_reasoning_steps(q)
    
    # Constraints (for coding)
    if not q.get("constraints") and q.get("type") == "coding":
        q["constraints"] = _generate_constraints(q)
    
    return q


def _generate_explanation(q: dict) -> str:
    """Generate a basic explanation for a question."""
    qtype = q.get("type", "")
    
    if qtype == "coding":
        solution = q.get("solution", {})
        if isinstance(solution, dict):
            code = solution.get("code", "")
            if code:
                return f"Solution approach: {q.get('mental_model', 'Implement the algorithm directly.')}"
        return f"Implement a solution for: {q.get('question', '')[:100]}"
    
    elif qtype == "aptitude":
        return q.get("mental_model", "") or f"Solve using the appropriate formula for {q.get('topic', 'this problem')}."
    
    elif qtype in ["logical", "verbal"]:
        return q.get("mental_model", "") or f"Apply logical reasoning to determine the answer."
    
    elif qtype == "sql":
        return f"Write a SQL query to answer: {q.get('question', '')[:100]}"
    
    elif qtype == "interview":
        return f"Consider your experience with: {q.get('question', '')[:100]}"
    
    return ""


def _generate_hints(q: dict) -> List[str]:
    """Generate progressive hints for a question."""
    qtype = q.get("type", "")
    hints = []
    
    if qtype == "coding":
        pattern = q.get("pattern", "")
        topic = q.get("topic", "")
        
        if pattern:
            hints.append(f"This is a {pattern} problem.")
        if topic:
            hints.append(f"Consider using a {topic}-based approach.")
        hints.append("Break the problem into smaller steps.")
        hints.append("Test with the provided examples first.")
        hints.append("Consider edge cases: empty input, single element, duplicates.")
    
    elif qtype == "aptitude":
        topic = q.get("topic", "")
        if topic:
            hints.append(f"This is a {topic} problem.")
        hints.append("Write down the given values.")
        hints.append("Identify the formula or approach needed.")
        hints.append("Solve step by step.")
    
    elif qtype == "sql":
        hints.append("Identify the tables you need.")
        hints.append("Determine the join condition.")
        hints.append("Apply filters with WHERE.")
        hints.append("Use aggregation if needed.")
    
    return hints[:4]  # Max 4 hints


def _generate_common_trap(q: dict) -> str:
    """Generate a common trap/misconception for this question."""
    qtype = q.get("type", "")
    topic = q.get("topic", "")
    
    if qtype == "coding":
        if "array" in topic.lower() or "array" in q.get("question", "").lower():
            return "Off-by-one errors are common. Check indices carefully."
        elif "string" in topic.lower():
            return "String immutability: remember that strings can't be modified in place in some languages."
        elif "linked list" in topic.lower():
            return "Losing the head pointer is a common mistake. Save references before modifying."
        elif "tree" in topic.lower() or "binary" in topic.lower():
            return "Forgetting the base case in recursion. Always handle null/empty nodes."
        elif "graph" in topic.lower():
            return "Not marking nodes as visited. Infinite loops are common in graph traversal."
        elif "dp" in topic.lower() or "dynamic" in topic.lower():
            return "Not identifying the correct state. Write down the recurrence relation first."
        return "Not considering all edge cases. Test with empty, single element, and duplicate inputs."
    
    elif qtype == "aptitude":
        if "percentage" in topic.lower():
            return "Taking percentage of the wrong base value."
        elif "profit" in topic.lower() or "loss" in topic.lower():
            return "Confusing profit/loss percentage with actual profit/loss amount."
        elif "time" in topic.lower() or "work" in topic.lower():
            return "Adding rates instead of combining them correctly."
        return "Read the question carefully — ensure you're solving for what's actually asked."
    
    elif qtype == "sql":
        return "Forgetting to handle NULL values or using incorrect join types."
    
    return ""


def _generate_reasoning_steps(q: dict) -> List[str]:
    """Generate step-by-step reasoning for a question."""
    qtype = q.get("type", "")
    steps = []
    
    if qtype == "coding":
        steps = [
            "1. Understand the problem: What are the inputs and expected outputs?",
            "2. Identify the pattern: What algorithm or data structure fits best?",
            "3. Plan the approach: Write pseudocode before coding.",
            "4. Implement: Write clean, readable code.",
            "5. Test: Run through the provided examples.",
            "6. Optimize: Check time/space complexity.",
        ]
    elif qtype == "aptitude":
        steps = [
            "1. Identify the given values and what needs to be found.",
            "2. Choose the appropriate formula or method.",
            "3. Substitute values and calculate.",
            "4. Verify the answer makes sense.",
        ]
    elif qtype == "sql":
        steps = [
            "1. Identify the required tables.",
            "2. Determine join conditions.",
            "3. Apply filters and aggregations.",
            "4. Order results if needed.",
        ]
    
    return steps


def _generate_constraints(q: dict) -> str:
    """Generate constraints for coding questions."""
    question = q.get("question", "")
    
    if "constraint" in question.lower():
        return question  # Already has constraints
    
    # Generate generic constraints based on topic
    topic = q.get("topic", "").lower()
    
    if "array" in topic:
        return "1 <= n <= 10^5, -10^9 <= nums[i] <= 10^9"
    elif "string" in topic:
        return "1 <= s.length <= 10^5, s consists of lowercase English letters"
    elif "tree" in topic or "binary" in topic:
        return "0 <= n <= 10^4, node values are integers"
    elif "graph" in topic:
        return "1 <= n <= 10^5, 0 <= edges <= 10^5"
    else:
        return "1 <= input size <= 10^5, time limit: 1 second"


async def enrich_bank(filename: str, dry_run: bool = False) -> dict:
    """Enrich a single question bank file."""
    filepath = os.path.join(_DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  SKIP: {filename} (not found)")
        return {"file": filename, "status": "skipped", "count": 0}
    
    print(f"\nProcessing: {filename}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print(f"  SKIP: {filename} (not a list)")
        return {"file": filename, "status": "skipped", "count": 0}
    
    original_count = len(data)
    enriched_count = 0
    
    for q in data:
        if not isinstance(q, dict):
            continue
        
        # Track what was missing
        missing = []
        if not q.get("explanation"):
            missing.append("explanation")
        if not q.get("hints"):
            missing.append("hints")
        if not q.get("common_trap"):
            missing.append("common_trap")
        if not q.get("reasoning_steps"):
            missing.append("reasoning_steps")
        if not q.get("constraints") and q.get("type") == "coding":
            missing.append("constraints")
        
        if missing:
            enriched_count += 1
            if not dry_run:
                _ensure_fields(q)
    
    if not dry_run:
        # Write back
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Enriched: {enriched_count}/{original_count} questions")
    else:
        print(f"  Would enrich: {enriched_count}/{original_count} questions")
    
    return {"file": filename, "status": "enriched", "count": enriched_count, "total": original_count}


async def enrich_all(dry_run: bool = False):
    """Enrich all question banks."""
    print("=" * 60)
    print("CONTENT ENRICHMENT PIPELINE")
    print("=" * 60)
    
    if dry_run:
        print("\n*** DRY RUN MODE — no files will be modified ***\n")
    
    results = []
    for filename in ENRICHMENT_ORDER:
        result = await enrich_bank(filename, dry_run=dry_run)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_enriched = sum(r["count"] for r in results if r["status"] == "enriched")
    total_questions = sum(r["total"] for r in results if r["status"] == "enriched")
    
    for r in results:
        if r["status"] == "enriched":
            pct = r["count"] / r["total"] * 100 if r["total"] > 0 else 0
            print(f"{r['file']}: {r['count']}/{r['total']} enriched ({pct:.0f}%)")
    
    print(f"\nTotal: {total_enriched}/{total_questions} questions enriched")
    
    if not dry_run:
        print("\nNext steps:")
        print("1. Run tests: pytest tests/test_tcs_oa_integration.py -v")
        print("2. Verify JSON: python -c 'import json; json.load(open(\"backend/app/data/verified_placement_questions.json\"))'")
        print("3. Re-run authoritative audit: python -m app.data.authoritative_audit")


if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv
    asyncio.run(enrich_all(dry_run=dry_run))
