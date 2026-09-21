#!/usr/bin/env python3
"""Interview-300 triage: classify interview questions into keep / rewrite / quarantine."""

import re
import json
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent.parent / "app" / "data"
PY_BANK = BASE / "interview_question_bank.py"
JSON_BANK = BASE / "interview_practice_bank.json"
TRIAGE_OUTPUT = BASE / "interview_triage_report.json"


def classify_py_question(q: dict) -> str:
    """Classify a Python bank question (has expected_answer, no explanation)."""
    qid = q.get("id", "unknown")
    question = q.get("question", "") or ""
    expected = q.get("expected_answer", "") or ""
    test_cases = q.get("test_cases", []) or []
    common_mistakes = q.get("common_mistakes", []) or []
    
    # Quarantine: empty or near-empty
    if not question or len(question.strip()) < 20:
        return "quarantine", "Empty question"
    
    # Quarantine: placeholder/template text
    placeholder_patterns = [
        r"interview question \d+",
        r"technical interview question \d+",
        r"^\s*$",
    ]
    for pattern in placeholder_patterns:
        if re.search(pattern, question, re.IGNORECASE):
            return "quarantine", "Placeholder/template question"
    
    # Quarantine: nonsensical or garbage
    if len(expected) < 10 and len(test_cases) == 0 and len(common_mistakes) == 0:
        return "quarantine", "No substantive content"
    
    # Rewrite: has question but missing expected_answer
    if not expected or len(expected.strip()) < 20:
        return "rewrite", "Missing or short expected_answer"
    
    # Keep: has question + expected_answer with substance
    if len(question) >= 20 and len(expected) >= 20:
        return "keep", "High quality: question + expected_answer present"
    
    # Default rewrite
    return "rewrite", "Needs improvement"


def classify_json_question(q: dict) -> str:
    """Classify a JSON bank question (has solution.explanation, testcases, etc.)."""
    qid = q.get("id", "unknown")
    question = q.get("question", "") or ""
    correct_answer = q.get("correct_answer", "") or ""
    solution = q.get("solution", {}) or {}
    explanation = solution.get("explanation", "") or ""
    testcases = q.get("testcases", []) or []
    hints = q.get("hints", []) or []
    
    # Quarantine: empty or near-empty
    if not question or len(question.strip()) < 20:
        return "quarantine", "Empty question"
    
    # Quarantine: placeholder/template text
    placeholder_patterns = [
        r"interview question \d+",
        r"technical interview question \d+",
        r"^\s*$",
    ]
    for pattern in placeholder_patterns:
        if re.search(pattern, question, re.IGNORECASE):
            return "quarantine", "Placeholder/template question"
    
    # Keep: has question + correct_answer + explanation
    if (len(question) >= 20 and 
        len(correct_answer) >= 20 and 
        len(explanation) >= 20):
        return "keep", "High quality: question + answer + explanation"
    
    # Rewrite: has question but missing components
    if not correct_answer or len(correct_answer) < 20:
        return "rewrite", "Missing or short correct_answer"
    
    if not explanation or len(explanation) < 20:
        return "rewrite", "Missing or short explanation"
    
    # Keep if has question + answer (explanation optional)
    if len(question) >= 20 and len(correct_answer) >= 20:
        return "keep", "Good: question + answer present"
    
    return "rewrite", "Needs improvement"


def main():
    print("=== Interview-300 Triage ===\n")
    
    py_questions = []
    json_questions = []
    
    # Load Python bank
    if PY_BANK.exists():
        print(f"Loading Python bank from {PY_BANK}...")
        text = PY_BANK.read_text()
        
        # Extract dicts using regex
        dict_pattern = re.compile(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', re.DOTALL)
        matches = dict_pattern.findall(text)
        
        for match in matches:
            try:
                q = {}
                id_match = re.search(r'"id":\s*"([^"]+)"', match)
                question_match = re.search(r'"question":\s*"([^"]+)"', match)
                expected_match = re.search(r'"expected_answer":\s*"([^"]+)"', match)
                test_cases_match = re.search(r'"test_cases":\s*(\[.*?\])', match, re.DOTALL)
                common_mistakes_match = re.search(r'"common_mistakes":\s*(\[.*?\])', match, re.DOTALL)
                
                if id_match and question_match:
                    q["id"] = id_match.group(1)
                    q["question"] = question_match.group(1)
                    q["expected_answer"] = expected_match.group(1) if expected_match else ""
                    q["test_cases"] = []
                    q["common_mistakes"] = []
                    if test_cases_match:
                        try:
                            q["test_cases"] = json.loads(test_cases_match.group(1))
                        except:
                            pass
                    if common_mistakes_match:
                        try:
                            q["common_mistakes"] = json.loads(common_mistakes_match.group(1))
                        except:
                            pass
                    py_questions.append(q)
            except Exception as e:
                continue
        
        print(f"Parsed {len(py_questions)} questions from Python bank")
    else:
        print(f"Python bank not found at {PY_BANK}")
    
    # Load JSON bank
    if JSON_BANK.exists():
        print(f"Loading JSON bank from {JSON_BANK}...")
        try:
            json_questions = json.loads(JSON_BANK.read_text())
            print(f"Loaded {len(json_questions)} questions from JSON bank")
        except Exception as e:
            print(f"Error loading JSON bank: {e}")
    
    total = len(py_questions) + len(json_questions)
    print(f"\nTotal questions: {total}")
    
    # Triage Python bank
    py_results = {"keep": [], "rewrite": [], "quarantine": []}
    for q in py_questions:
        status, reason = classify_py_question(q)
        py_results[status].append({
            "id": q.get("id", "unknown"),
            "question": q.get("question", "")[:100],
            "bank": "python",
            "reason": reason
        })
    
    # Triage JSON bank
    json_results = {"keep": [], "rewrite": [], "quarantine": []}
    for q in json_questions:
        status, reason = classify_json_question(q)
        json_results[status].append({
            "id": q.get("id", "unknown"),
            "question": q.get("question", "")[:100],
            "bank": "json",
            "reason": reason
        })
    
    # Combine results
    triage_results = {
        "keep": py_results["keep"] + json_results["keep"],
        "rewrite": py_results["rewrite"] + json_results["rewrite"],
        "quarantine": py_results["quarantine"] + json_results["quarantine"],
        "stats": {
            "total": total,
            "py_total": len(py_questions),
            "json_total": len(json_questions),
            "keep": len(py_results["keep"]) + len(json_results["keep"]),
            "rewrite": len(py_results["rewrite"]) + len(json_results["rewrite"]),
            "quarantine": len(py_results["quarantine"]) + len(json_results["quarantine"]),
            "py_keep": len(py_results["keep"]),
            "py_rewrite": len(py_results["rewrite"]),
            "py_quarantine": len(py_results["quarantine"]),
            "json_keep": len(json_results["keep"]),
            "json_rewrite": len(json_results["rewrite"]),
            "json_quarantine": len(json_results["quarantine"]),
        }
    }
    
    # Calculate percentages
    if total > 0:
        triage_results["stats"]["keep_pct"] = round(triage_results["stats"]["keep"] / total * 100, 1)
        triage_results["stats"]["rewrite_pct"] = round(triage_results["stats"]["rewrite"] / total * 100, 1)
        triage_results["stats"]["quarantine_pct"] = round(triage_results["stats"]["quarantine"] / total * 100, 1)
    
    # Save report
    TRIAGE_OUTPUT.write_text(json.dumps(triage_results, indent=2))
    
    # Print summary
    stats = triage_results["stats"]
    print(f"\n=== Triage Results ===")
    print(f"Total questions: {stats['total']}")
    print(f"Python bank: {stats['py_total']}")
    print(f"JSON bank: {stats['json_total']}")
    print(f"\nKeep: {stats['keep']} ({stats.get('keep_pct', 0)}%)")
    print(f"  Python: {stats['py_keep']}")
    print(f"  JSON: {stats['json_keep']}")
    print(f"\nRewrite: {stats['rewrite']} ({stats.get('rewrite_pct', 0)}%)")
    print(f"  Python: {stats['py_rewrite']}")
    print(f"  JSON: {stats['json_rewrite']}")
    print(f"\nQuarantine: {stats['quarantine']} ({stats.get('quarantine_pct', 0)}%)")
    print(f"  Python: {stats['py_quarantine']}")
    print(f"  JSON: {stats['json_quarantine']}")
    print(f"\nReport saved to: {TRIAGE_OUTPUT}")
    
    # Print samples
    print(f"\n=== Sample Keep (Python) ===")
    for q in py_results["keep"][:3]:
        print(f"  {q['id']}: {q['question'][:60]}...")
    
    print(f"\n=== Sample Keep (JSON) ===")
    for q in json_results["keep"][:3]:
        print(f"  {q['id']}: {q['question'][:60]}...")
    
    print(f"\n=== Sample Rewrite ===")
    for q in triage_results["rewrite"][:3]:
        print(f"  {q['id']}: {q['question'][:60]}...")
        print(f"    Reason: {q['reason']}")
    
    print(f"\n=== Sample Quarantine ===")
    for q in triage_results["quarantine"][:3]:
        print(f"  {q['id']}: {q['question'][:60]}...")
        print(f"    Reason: {q['reason']}")


if __name__ == "__main__":
    main()
