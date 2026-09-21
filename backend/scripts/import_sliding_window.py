"""Import sliding_window.json through the verification pipeline.

Run from backend/:
  python scripts/import_sliding_window.py

Converts each problem to the canonical question format, runs auto_verify,
and reports per-problem pass/fail against hidden test cases.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from app.services.question_store import load_all, _questions, _is_servable
from app.services.auto_verify import verify_question, _run_python_tests


def load_sliding_window():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "app", "data", "lessons", "sliding_window.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Solution wrappers: map problem ID to (function_name, args, wrapper_code)
WRAPPER_MAP = {
    "sw_001": {
        "fn": "max_avg_subarray",
        "args": "nums, k",
        "call": "max_avg_subarray([1,12,-5,-6,50,3], 4)",
        "expected": "12.75",
    },
    "sw_002": {
        "fn": "max_sum_subarray",
        "args": "arr, k",
        "call": "max_sum_subarray([2,1,5,1,3,2], 3)",
        "expected": "9",
    },
    "sw_003": {
        "fn": "length_of_longest_substring",
        "args": "s",
        "call": 'length_of_longest_substring("abcabcbb")',
        "expected": "3",
    },
    "sw_004": {
        "fn": "longest_substring_k_distinct",
        "args": "s, k",
        "call": 'longest_substring_k_distinct("eceba", 2)',
        "expected": "3",
    },
    "sw_005": {
        "fn": "min_window",
        "args": "s, t",
        "call": 'min_window("ADOBECODEBANC", "ABC")',
        "expected": "BANC",
    },
}


def _wrap_solution(prob_id: str, raw_code: str) -> str:
    """Wrap raw solution code into a callable function for test execution."""
    info = WRAPPER_MAP.get(prob_id)
    if not info:
        return raw_code

    # Check if code already has a def
    if "def " in raw_code:
        return raw_code

    # Wrap in function
    lines = raw_code.strip().split("\n")
    # Remove leading 'return' and add it back after wrapping
    body_lines = []
    for line in lines:
        body_lines.append("    " + line)

    wrapped = f"def {info['fn']}({info['args']}):\n" + "\n".join(body_lines)
    return wrapped


def _parse_test_input(raw: str) -> str:
    """Parse test input string into newline-separated format for _split_calls.

    Examples:
      '[1,12,-5,-6,50,3] 4' -> '[1,12,-5,-6,50,3]\\n4'
      '"abcabcbb"' -> '"abcabcbb"'
      '"ADOBECODEBANC" "ABC"' -> '"ADOBECODEBANC"\\n"ABC"'
      '"eceba" 2' -> '"eceba"\\n2'
      '"a" "a"' -> '"a"\\n"a"'
    """
    raw = raw.strip()
    import re
    tokens = re.findall(r'"[^"]*"|\[[^\]]*\]|\S+', raw)
    return "\n".join(tokens)


def convert_problem(sw_prob: dict) -> dict:
    """Convert a sliding_window.json problem to canonical question format."""
    # Extract solution code from editorial
    editorial = sw_prob.get("editorial", {})
    optimized = editorial.get("optimized", {})
    raw_code = optimized.get("code", "")

    # Wrap in proper function if needed
    solution_code = _wrap_solution(sw_prob["id"], raw_code)

    # Convert test cases to canonical format
    all_test_cases = []
    for tc in sw_prob.get("test_cases", []):
        parsed_input = _parse_test_input(tc["input"])
        all_test_cases.append({
            "input": parsed_input,
            "output": tc["expected"],
            "hidden": False,
        })
    for tc in sw_prob.get("hidden_test_cases", []):
        parsed_input = _parse_test_input(tc["input"])
        all_test_cases.append({
            "input": parsed_input,
            "output": tc["expected"],
            "hidden": True,
        })

    # Convert examples
    examples = []
    for ex in sw_prob.get("examples", []):
        examples.append({
            "input": ex["input"],
            "output": ex["output"],
        })

    return {
        "id": sw_prob["id"],
        "question": sw_prob["title"],
        "question_title": sw_prob["title"],
        "type": "coding",
        "difficulty": sw_prob.get("difficulty", "medium"),
        "topic": "sliding-window",
        "sub_topic": "arrays",
        "statement": sw_prob.get("statement", ""),
        "constraints": sw_prob.get("constraints", []),
        "examples": examples,
        "test_cases": all_test_cases,
        "solution": {"code": solution_code, "language": "python"},
        "hints": sw_prob.get("hints", []),
        "approach": editorial.get("approach", ""),
        "time_complexity": sw_prob.get("time_complexity", "O(n)"),
        "space_complexity": sw_prob.get("space_complexity", "O(1)"),
        "common_mistakes": editorial.get("common_mistakes", []),
        "tips": editorial.get("edge_cases", []),
        "companies": sw_prob.get("company_tags", []),
        "trust_status": "unverified",
    }


def main():
    data = load_sliding_window()
    problems = data.get("problems", [])

    print(f"{'='*80}")
    print(f"SLIDING WINDOW IMPORT — {len(problems)} problems")
    print(f"{'='*80}")
    print()

    results = []
    for prob in problems:
        q = convert_problem(prob)
        # Run verification
        verify_question(q)

        # Run solution against ALL test cases (visible + hidden)
        test_result = _run_python_tests(q)

        results.append({
            "id": prob["id"],
            "title": prob["title"],
            "difficulty": prob["difficulty"],
            "trust_status": q.get("trust_status", "unknown"),
            "tests_passed": test_result[2],
            "tests_total": test_result[3],
            "all_pass": test_result[0],
            "reason": test_result[1],
            "companies": prob.get("company_tags", []),
        })

    # Print table
    print(f"{'ID':<10} {'Title':<45} {'Diff':<8} {'Trust':<18} {'Tests':<8} {'Result':<8}")
    print("-" * 100)
    for r in results:
        status_icon = "PASS" if r["all_pass"] else "FAIL"
        print(f"{r['id']:<10} {r['title'][:44]:<45} {r['difficulty']:<8} {r['trust_status']:<18} {r['tests_passed']}/{r['tests_total']:<5} {status_icon}")

    print("-" * 100)
    passed = sum(1 for r in results if r["all_pass"])
    total = len(results)
    print(f"TOTAL: {passed}/{total} problems pass all tests")

    # Problems that failed
    failed = [r for r in results if not r["all_pass"]]
    if failed:
        print()
        print("FAILURES:")
        for r in failed:
            print(f"  {r['id']}: {r['reason'][:80]}")

    return results


if __name__ == "__main__":
    main()
