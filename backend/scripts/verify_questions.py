"""Phase 2 — Verification: Execute solutions against test cases.

For each trusted question, runs the solution code against visible test cases
and verifies the output matches expected results.
"""
import json
import sys
import traceback
from pathlib import Path

TRUSTED_PATH = Path("app/data/questions_trusted.json")


def execute_solution(code: str, test_input: list):
    """Execute solution code with test input and return output."""
    # Create a namespace for execution
    namespace = {}
    
    # Add ListNode class for linked list problems
    list_node_class = """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def array_to_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def list_to_array(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result
"""
    exec(list_node_class, namespace)
    exec(code, namespace)

    # Find the function (assume it's the first def)
    func_name = None
    for line in code.split("\n"):
        if line.strip().startswith("def "):
            func_name = line.strip().split("(")[0].replace("def ", "").strip()
            break

    if not func_name or func_name not in namespace:
        return None, f"Function {func_name} not found"

    func = namespace[func_name]

    # Convert array inputs to linked lists if function expects ListNode
    converted_input = []
    for inp in test_input:
        if isinstance(inp, list) and len(inp) > 0 and isinstance(inp[0], (int, float)):
            # Check if function name suggests linked list
            if "list" in func_name.lower() or "node" in func_name.lower() or "linked" in func_name.lower():
                converted_input.append(namespace["array_to_list"](inp))
            else:
                converted_input.append(inp)
        else:
            converted_input.append(inp)

    # Call with test input
    try:
        if isinstance(converted_input, list):
            result = func(*converted_input)
        else:
            result = func(converted_input)
        
        # Convert linked list result back to array for comparison
        if hasattr(result, 'next') or hasattr(result, 'val'):
            result = namespace["list_to_array"](result)
        
        return result, None
    except Exception as e:
        return None, str(e)


def verify_question(q: dict) -> dict:
    """Verify a single question by executing its solution."""
    results = {
        "id": q["id"],
        "title": q["title"],
        "passed": 0,
        "failed": 0,
        "errors": [],
    }

    solution_code = q.get("solution", {}).get("code", "")
    test_cases = q.get("test_cases", [])

    for i, tc in enumerate(test_cases):
        inp = tc.get("input")
        expected = tc.get("expected")
        desc = tc.get("description", f"test {i}")

        actual, error = execute_solution(solution_code, inp)

        if error:
            results["failed"] += 1
            results["errors"].append(f"{desc}: {error}")
        elif actual == expected:
            results["passed"] += 1
        else:
            results["failed"] += 1
            results["errors"].append(f"{desc}: expected {expected}, got {actual}")

    return results


def main():
    if not TRUSTED_PATH.exists():
        print(f"ERROR: {TRUSTED_PATH} not found")
        return

    with open(TRUSTED_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    print(f"Verifying {len(questions)} questions...\n")

    total_passed = 0
    total_failed = 0
    all_verified = True

    for q in questions:
        result = verify_question(q)
        status = "✓ VERIFIED" if result["failed"] == 0 else "✗ FAILED"
        print(f"{status}: {q['id']} - {q['title']} ({result['passed']}/{result['passed'] + result['failed']} tests)")

        if result["errors"]:
            for err in result["errors"][:3]:
                print(f"    - {err}")

        total_passed += result["passed"]
        total_failed += result["failed"]
        if result["failed"] > 0:
            all_verified = False

    print(f"\n{'='*50}")
    print(f"Results: {total_passed} passed, {total_failed} failed")

    if all_verified:
        print(f"\n✓ All {len(questions)} questions VERIFIED")
        # Update trust status
        for q in questions:
            q["trust_status"] = "verified"
            q["verified_at"] = "2026-08-30"
        with open(TRUSTED_PATH, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        print("Updated trust_status to 'verified'")
    else:
        print(f"\n✗ Some questions need fixes before verification")

    return all_verified


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
