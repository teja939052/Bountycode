"""Migrate dead TCS NQT Python question banks into the live JSON question store.

Reads:
  backend/app/data/tcs_nqt_quantitative.py
  backend/app/data/tcs_nqt_reasoning.py
  backend/app/data/tcs_nqt_verbal.py
  backend/app/data/pseudocode_bank.py

Writes:
  backend/app/data/questions/tcs_nqt_all.json

After running, add the output file to the question store loader so the
2,472 questions become available to students through the existing trust
pipeline (unverified -> reviewed -> verified).
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve backend root
# ---------------------------------------------------------------------------
BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

# ---------------------------------------------------------------------------
# Import dead Python banks
# ---------------------------------------------------------------------------
from app.data.tcs_nqt_quantitative import TCS_NQT_QUANTITATIVE  # noqa: E402
from app.data.tcs_nqt_reasoning import TCS_NQT_REASONING  # noqa: E402
from app.data.tcs_nqt_verbal import TCS_NQT_VERBAL  # noqa: E402
from app.data.pseudocode_bank import PSEUDOCODE_QUESTIONS  # noqa: E402


# ---------------------------------------------------------------------------
# Pattern mapping: subtopic -> 75-pattern taxonomy
# ---------------------------------------------------------------------------
QUANT_SUBTOPIC_TO_PATTERN = {
    "Age Problem": "Age Problems",
    "Arrangements": "Arrangement Constraints",
    "Average Speed": "Relative Speed",
    "Bar Graph": "Data Interpretation",
    "Basic SI": "Simple Interest",
    "Boats and Streams": "Boats & Streams",
    "CP and SP with Ratio": "Profit/Loss Transformation",
    "Cards": "Probability",
    "Circle": "Geometry",
    "Combined Work": "Combined Work",
    "Compound Interest Approximation": "Compound Interest",
    "Conditional": "Probability",
    "Dice": "Cube/Dice",
    "Discount on Marked Price": "Discount Calculation",
    "Divisibility": "Number Systems",
    "Efficiency and Wages": "Work-Rate Composition",
    "Election Votes": "Percentage",
    "False Weights": "Mixture & Alligation",
    "General": "General Practice",
    "General Practice": "General Practice",
    "Group Average": "Weighted Average",
    "Income Ratio": "Ratio Scaling",
    "LCM and HCF": "Number Systems",
    "Mixture Percentage": "Mixture & Alligation",
    "Mixture Ratio": "Mixture & Alligation",
    "Partnership": "Partnership",
    "Percentage Point": "Percentage Increase/Decrease",
    "Pie Chart": "Data Interpretation",
    "Pipes and Cisterns": "Pipes & Cisterns",
    "Population Change": "Successive Percentage Change",
    "Practice": "General Practice",
    "Rate of Interest": "Simple Interest",
    "Relative Speed": "Relative Speed",
    "Repeated Dilution": "Mixture & Alligation",
    "Replacement": "Average Replacement",
    "Reverse Percentage": "Reverse Percentage",
    "Selection": "Permutation & Combination",
    "Successive Percentage Change": "Successive Percentage Change",
    "Successive Profit": "Successive Percentage Change",
    "Trains": "Train Crossing",
    "Two Articles Profit and Loss": "Profit/Loss Transformation",
    "Unit Digit": "Number Systems",
    "Volume": "Geometry",
    "Work and Wages": "Work-Rate Composition",
}

REASONING_SUBTOPIC_TO_PATTERN = {
    "Alphabet Shift": "Coding-Decoding Transformation",
    "Alphabetical Pattern": "Sequence Detection (Alphabet Series)",
    "Alternating Series": "Sequence Detection",
    "Angle Between Hands": "Clock Problems",
    "Basic Counting": "Data Sufficiency",
    "Basic Sufficiency": "Data Sufficiency",
    "Basic Syllogism": "Syllogism Set Logic",
    "Cardinal Directions": "Direction Graph",
    "Circular Arrangement": "Arrangement Constraints (Circular)",
    "Complex Family Relations": "Blood-Relation Graph",
    "Day Calculation": "Calendar",
    "Difference Pattern": "Sequence Detection",
    "Family Tree": "Blood-Relation Graph",
    "Fibonacci-like": "Sequence Detection",
    "General": "General Practice",
    "General Practice": "General Practice",
    "Generation Chain": "Blood-Relation Graph",
    "Implicit Assumption": "Statement-Assumption",
    "Leap Year Day Calculation": "Calendar",
    "Letter Analogy": "Analogy",
    "Linear Arrangement": "Arrangement Constraints (Linear)",
    "Logical Puzzle": "Logical Puzzle",
    "Multiple Constraint": "Arrangement Constraints",
    "Multiple Turns": "Direction Graph",
    "Multiplication Pattern": "Sequence Detection",
    "Negative Statement": "Statement-Conclusion",
    "Number Analogy": "Analogy",
    "Number Coding": "Coding-Decoding (Number Mapping)",
    "Number-to-Word Coding": "Coding-Decoding Transformation",
    "Opposite Faces": "Cube/Dice",
    "Perfect Square/Cube Pattern": "Sequence Detection",
    "Photo Identification": "Visual Reasoning",
    "Practice": "General Practice",
    "Reverse Alphabet Pattern": "Coding-Decoding Transformation",
    "Reversed Alphabet": "Coding-Decoding Transformation",
    "Statement Based Relation": "Blood-Relation Graph",
    "Sun Direction": "Direction Graph",
    "Truth/Lie Puzzle": "Truth/Lie Puzzle",
    "Two-Stage Series": "Sequence Detection",
    "Universal Affirmation": "Syllogism Set Logic",
    "Water Image": "Visual Reasoning",
    "Word Analogy": "Analogy",
    "Word Coding": "Coding-Decoding Transformation",
    "Word-to-Word Coding": "Coding-Decoding Transformation",
}

VERBAL_SUBTOPIC_TO_PATTERN = {
    "Articles": "Article Usage",
    "Author's Purpose": "Reading Comprehension (Tone/Attitude)",
    "Cause-Effect Sequence": "Cause-Effect",
    "Cause-Effect with 'Because'": "Cause-Effect",
    "Contextual Antonym": "Vocabulary in Context",
    "Contextual Synonym": "Vocabulary in Context",
    "Double Blank - Cause Effect": "Para Jumbles (Cause-Effect)",
    "Double Blank - Definition Example": "Para Jumbles (Problem-Solution)",
    "Factual Detail Recall": "Reading Comprehension (Main Idea)",
    "General": "General Practice",
    "General Practice": "General Practice",
    "Idiomatic Expressions": "Vocabulary in Context",
    "Inference Question": "Reading Comprehension (Inference)",
    "Inference-Based Recall": "Reading Comprehension (Inference)",
    "Logical Sequence": "Sentence Correction (Redundancy/Wordiness)",
    "Main Idea Identification": "Reading Comprehension (Main Idea)",
    "Meeting Reschedule Request": "Sentence Correction (Redundancy/Wordiness)",
    "Modifiers and Parallelism": "Parallelism",
    "Practice": "General Practice",
    "Preposition Usage": "Preposition",
    "Pronoun Agreement": "Pronoun-Antecedent Agreement",
    "Sequence of Events Recall": "Reading Comprehension (Main Idea)",
    "Single Blank - Contrast Words": "Single Blank - Contrast Words",
    "Subject-Verb Agreement": "Subject-Verb Agreement",
    "Subject-Verb Agreement with Collective Nouns": "Subject-Verb Agreement",
    "Tense Consistency": "Tense Consistency",
    "Vocabulary - Positive/Negative Context": "Vocabulary in Context",
    "Vocabulary in Context": "Vocabulary in Context",
    "Vocabulary in Context Recall": "Vocabulary in Context",
    "Work From Home Request": "Sentence Correction (Redundancy/Wordiness)",
}

PSEUDO_SUBTOPIC_TO_PATTERN = {
    "2D Array": "Array Mutation",
    "Array Indexing": "Array Mutation",
    "Array Passing to Function": "Function Flow",
    "Array Search": "Array Mutation",
    "Array Traversal": "Array Mutation",
    "Base Case": "Recursion Tracing",
    "Binary Search": "Binary Search",
    "Break Statement": "Loop-State Tracking",
    "Bubble Sort": "Sorting",
    "Bubble Sort Pass": "Sorting",
    "Call by Value": "Function Flow",
    "Continue Statement": "Loop-State Tracking",
    "Decrement Loop": "Loop-State Tracking",
    "Factorial": "Recursion Tracing",
    "Fibonacci": "Recursion Tracing",
    "For Loop": "Loop-State Tracking",
    "If-Else": "Condition Evaluation",
    "Increment/Decrement": "Loop-State Tracking",
    "Linear Search": "Array Mutation",
    "Logical OR": "Condition Evaluation",
    "Logical Operators": "Condition Evaluation",
    "Nested If": "Condition Evaluation",
    "Nested Loops": "Nested-Loop Counting",
    "Pointer Arithmetic": "Pointer Tracing",
    "Pointer to Pointer": "Pointer Tracing",
    "Practice": "General Practice",
    "Recursive Call": "Recursion Tracing",
    "Return Value": "Function Flow",
    "Selection Sort": "Sorting",
    "Step Value": "Loop-State Tracking",
    "String Comparison": "String Operations",
    "String Concatenation": "String Operations",
    "String Copy": "String Operations",
    "String Length": "String Operations",
    "String Operations": "String Operations",
    "Switch Case": "Condition Evaluation",
    "Ternary Operator": "Condition Evaluation",
    "While Loop": "Loop-State Tracking",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
COMPANIES = ["TCS", "Infosys", "Wipro", "Cognizant", "Capgemini", "Accenture"]


def _company_relevance(question_tags, domain):
    """Company relevance for TCS NQT prep content."""
    base = {
        "TCS": 0.9,
        "Infosys": 0.85,
        "Wipro": 0.85,
        "Cognizant": 0.8,
        "Capgemini": 0.75,
        "Accenture": 0.75,
    }
    tags = [t.lower() for t in (question_tags or [])]
    for company in base:
        if company.lower() in tags:
            base[company] = 0.95
    return base


def _map_difficulty(value):
    if isinstance(value, int):
        if value <= 1:
            return "easy"
        if value == 2:
            return "medium"
        return "hard"
    return str(value).lower() if value else "medium"


def _extract_explanation(q):
    """Pull explanation from multiple possible fields."""
    for key in ("explanation", "speed_trick", "misconception"):
        value = q.get(key)
        if isinstance(value, dict):
            parts = []
            if value.get("name"):
                parts.append(str(value["name"]))
            if value.get("formula"):
                parts.append(str(value["formula"]))
            if value.get("steps"):
                parts.extend(str(s) for s in value["steps"])
            if value.get("desc"):
                parts.append(str(value["desc"]))
            if parts:
                return "\n".join(parts)
        elif isinstance(value, str) and value.strip():
            return value
    return ""


def _extract_hints(q):
    hints = []
    speed_trick = q.get("speed_trick")
    if isinstance(speed_trick, dict) and speed_trick.get("steps"):
        hints.extend(str(s) for s in speed_trick["steps"][:3])
    if q.get("misconception") and isinstance(q["misconception"], dict):
        desc = q["misconception"].get("desc")
        if desc:
            hints.append(str(desc))
    return hints[:5]


def _to_canonical(q, index, domain, subtopic_to_pattern):
    subtopic = q.get("subtopic", "")
    pattern = subtopic_to_pattern.get(subtopic, subtopic)

    options = q.get("options", []) or []
    correct_index = q.get("correct_index")
    correct_answer = ""
    if isinstance(correct_index, int) and 0 <= correct_index < len(options):
        correct_answer = str(options[correct_index])
    if not correct_answer:
        correct_answer = str(q.get("correct_answer") or "")

    return {
        "id": f"{domain.lower().replace(' ', '_').replace('-', '_')}_{index:04d}",
        "question": q.get("question", ""),
        "pattern": pattern,
        "skill": subtopic,
        "domain": domain,
        "difficulty": _map_difficulty(q.get("difficulty")),
        "difficulty_calibrated": False,
        "company_relevance": _company_relevance(q.get("company_tags"), domain),
        "time_estimate_sec": int(q.get("time_estimate_seconds") or 90),
        "time_limit_sec": int(q.get("time_estimate_seconds") or 90) + 30,
        "question_type": "MCQ",
        "content": {
            "question": q.get("question", ""),
            "options": [str(o) for o in options],
            "correct_answer": correct_answer,
            "explanation": _extract_explanation(q),
        },
        "hints": _extract_hints(q),
        "common_mistakes": [str(m) for m in (q.get("common_mistakes") or [])],
        "prerequisites": [],
        "follow_up_patterns": [],
        "verified": False,
        "verified_by": None,
        "verified_at": None,
        "source": "TCS NQT candidate report",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "trust_status": "unverified",
        "type": "aptitude" if domain == "Quantitative Aptitude" else (
            "logical" if domain == "Logical Reasoning" else (
            "verbal" if domain == "Verbal" else (
            "cs_fundamentals" if domain == "Programming Logic" else "aptitude"
        ))),
        "topic": q.get("topic", domain),
        "sub_topic": subtopic,
    }


def migrate():
    questions = []

    for idx, q in enumerate(TCS_NQT_QUANTITATIVE):
        questions.append(_to_canonical(q, idx, "Quantitative Aptitude", QUANT_SUBTOPIC_TO_PATTERN))

    offset = len(TCS_NQT_QUANTITATIVE)
    for idx, q in enumerate(TCS_NQT_REASONING):
        questions.append(_to_canonical(q, offset + idx, "Logical Reasoning", REASONING_SUBTOPIC_TO_PATTERN))

    offset += len(TCS_NQT_REASONING)
    for idx, q in enumerate(TCS_NQT_VERBAL):
        questions.append(_to_canonical(q, offset + idx, "Verbal", VERBAL_SUBTOPIC_TO_PATTERN))

    offset += len(TCS_NQT_VERBAL)
    for idx, q in enumerate(PSEUDOCODE_QUESTIONS):
        questions.append(_to_canonical(q, offset + idx, "Programming Logic", PSEUDO_SUBTOPIC_TO_PATTERN))

    return questions


def main():
    out_path = BACKEND_ROOT / "app" / "data" / "questions" / "tcs_nqt_all.json"
    print(f"Migrating TCS NQT banks to: {out_path}")

    questions = migrate()
    print(f"Migrated {len(questions)} questions")

    # Summary by domain
    from collections import Counter
    domain_counts = Counter(q["domain"] for q in questions)
    print("Domain breakdown:")
    for domain, count in sorted(domain_counts.items()):
        print(f"  {domain}: {count}")

    # Write JSON
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    size_kb = out_path.stat().st_size / 1024
    print(f"Wrote {size_kb:.1f} KB")
    print("Migration complete.")


if __name__ == "__main__":
    main()
