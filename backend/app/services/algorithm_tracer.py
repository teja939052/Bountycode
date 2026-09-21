"""Algorithm trace generator — OFFLINE AUTHORING TOOL ONLY.

Generates visual_trace JSON documents for the AlgorithmTracer frontend component.
Covers core DSA patterns with step-by-step array state, pointer positions,
variable values, and descriptions.

This is NOT called at runtime. Traces are pre-authored as JSON files and
loaded directly by the frontend. Use as:

    python -m app.services.algorithm_tracer --algo sliding_window_max --array 2,1,5,1,3,2 --k 3

The output is a visual_trace JSON document that can be saved to a file and
imported into the question bank or lesson system.

NO external dependencies beyond stdlib. Pure computation.
"""
from __future__ import annotations

import json
import sys
from typing import Any


# ---------------------------------------------------------------------------
# Trace generators (same logic as before, but output visual_trace format)
# ---------------------------------------------------------------------------

def _sliding_window_max_sum(arr: list[int], k: int, questions: list[dict] | None = None) -> dict[str, Any]:
    """Generate visual_trace for sliding window maximum sum of size k."""
    steps: list[dict[str, Any]] = []
    n = len(arr)
    if n < k or k <= 0:
        return {"kind": "visual_trace", "algorithm": "sliding_window_max", "version": "1.0", "initial": {}, "steps": []}

    window_sum = sum(arr[:k])
    max_sum = window_sum

    initial = {
        "step": 0,
        "description": f"Initial array of size {n}, window size k={k}",
        "array": arr[:],
        "pointers": {"left": 0, "right": k - 1},
        "highlight": list(range(k)),
        "window": {"start": 0, "end": k - 1},
        "variables": {"k": k, "window_sum": window_sum, "max_sum": max_sum},
    }

    steps.append({
        "step": 1,
        "description": f"Initialize window of size {k}. Sum = {window_sum}",
        "array": arr[:],
        "pointers": {"left": 0, "right": k - 1},
        "highlight": list(range(k)),
        "window": {"start": 0, "end": k - 1},
        "variables": {"left": 0, "right": k - 1, "window_sum": window_sum, "max_sum": max_sum},
        "codeLine": 1,
    })

    for i in range(k, n):
        removed = arr[i - k]
        added = arr[i]
        window_sum = window_sum - removed + added
        max_sum = max(max_sum, window_sum)
        left = i - k + 1
        right = i

        steps.append({
            "step": len(steps) + 1,
            "description": f"Slide: remove arr[{i-k}]={removed}, add arr[{i}]={added}. Sum = {window_sum}, Max = {max_sum}",
            "array": arr[:],
            "pointers": {"left": left, "right": right},
            "highlight": list(range(left, right + 1)),
            "window": {"start": left, "end": right},
            "variables": {"left": left, "right": right, "window_sum": window_sum, "max_sum": max_sum},
            "codeLine": 4,
        })

    return {
        "kind": "visual_trace",
        "algorithm": "sliding_window_max",
        "version": "1.0",
        "title": f"Sliding Window Max Sum (k={k})",
        "initial": initial,
        "steps": steps,
        "questions": questions or [],
    }


def _two_sum(arr: list[int], target: int, questions: list[dict] | None = None) -> dict[str, Any]:
    """Generate visual_trace for two-pointer approach on sorted array."""
    steps: list[dict[str, Any]] = []
    left, right = 0, len(arr) - 1

    initial = {
        "step": 0,
        "description": f"Sorted array, target = {target}",
        "array": arr[:],
        "pointers": {"left": 0, "right": right},
        "highlight": [0, right],
        "variables": {"left": 0, "right": right, "target": target},
    }

    steps.append({
        "step": 1,
        "description": f"Start: left=0, right={right}. Target = {target}",
        "array": arr[:],
        "pointers": {"left": 0, "right": right},
        "highlight": [0, right],
        "variables": {"left": 0, "right": right, "current_sum": arr[0] + arr[right]},
        "codeLine": 1,
    })

    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            steps.append({
                "step": len(steps) + 1,
                "description": f"Found! arr[{left}]={arr[left]} + arr[{right}]={arr[right]} = {target}",
                "array": arr[:],
                "pointers": {"left": left, "right": right},
                "highlight": [left, right],
                "variables": {"left": left, "right": right, "current_sum": current_sum},
                "codeLine": 3,
            })
            break
        elif current_sum < target:
            steps.append({
                "step": len(steps) + 1,
                "description": f"Sum {current_sum} < {target}, move left pointer right",
                "array": arr[:],
                "pointers": {"left": left, "right": right},
                "highlight": [left, right],
                "variables": {"left": left, "right": right, "current_sum": current_sum},
                "codeLine": 5,
            })
            left += 1
        else:
            steps.append({
                "step": len(steps) + 1,
                "description": f"Sum {current_sum} > {target}, move right pointer left",
                "array": arr[:],
                "pointers": {"left": left, "right": right},
                "highlight": [left, right],
                "variables": {"left": left, "right": right, "current_sum": current_sum},
                "codeLine": 7,
            })
            right -= 1

    return {
        "kind": "visual_trace",
        "algorithm": "two_sum",
        "version": "1.0",
        "title": f"Two Sum (target={target})",
        "initial": initial,
        "steps": steps,
        "questions": questions or [],
    }


def _binary_search(arr: list[int], target: int, questions: list[dict] | None = None) -> dict[str, Any]:
    """Generate visual_trace for binary search."""
    steps: list[dict[str, Any]] = []
    low, high = 0, len(arr) - 1

    initial = {
        "step": 0,
        "description": f"Sorted array, target = {target}",
        "array": arr[:],
        "pointers": {"low": 0, "high": high},
        "highlight": list(range(len(arr))),
        "variables": {"low": 0, "high": high, "target": target},
    }

    steps.append({
        "step": 1,
        "description": f"Start: low=0, high={high}. Target = {target}",
        "array": arr[:],
        "pointers": {"low": 0, "high": high},
        "highlight": list(range(len(arr))),
        "variables": {"low": 0, "high": high, "mid": "N/A"},
        "codeLine": 1,
    })

    while low <= high:
        mid = (low + high) // 2
        steps.append({
            "step": len(steps) + 1,
            "description": f"mid = ({low}+{high})//2 = {mid}. arr[{mid}] = {arr[mid]}",
            "array": arr[:],
            "pointers": {"low": low, "high": high},
            "highlight": [mid],
            "variables": {"low": low, "high": high, "mid": mid},
            "codeLine": 3,
        })

        if arr[mid] == target:
            steps.append({
                "step": len(steps) + 1,
                "description": f"Found target {target} at index {mid}!",
                "array": arr[:],
                "pointers": {"low": low, "high": high},
                "highlight": [mid],
                "variables": {"low": low, "high": high, "mid": mid},
                "codeLine": 5,
            })
            break
        elif arr[mid] < target:
            steps.append({
                "step": len(steps) + 1,
                "description": f"arr[{mid}]={arr[mid]} < {target}, search right half",
                "array": arr[:],
                "pointers": {"low": low, "high": high},
                "highlight": list(range(mid + 1, high + 1)),
                "variables": {"low": low, "high": high, "mid": mid},
                "codeLine": 7,
            })
            low = mid + 1
        else:
            steps.append({
                "step": len(steps) + 1,
                "description": f"arr[{mid}]={arr[mid]} > {target}, search left half",
                "array": arr[:],
                "pointers": {"low": low, "high": high},
                "highlight": list(range(low, mid)),
                "variables": {"low": low, "high": high, "mid": mid},
                "codeLine": 9,
            })
            high = mid - 1

    return {
        "kind": "visual_trace",
        "algorithm": "binary_search",
        "version": "1.0",
        "title": f"Binary Search (target={target})",
        "initial": initial,
        "steps": steps,
        "questions": questions or [],
    }


def _bubble_sort(arr: list[int], questions: list[dict] | None = None) -> dict[str, Any]:
    """Generate visual_trace for bubble sort."""
    steps: list[dict[str, Any]] = []
    a = arr[:]
    n = len(a)

    initial = {
        "step": 0,
        "description": f"Unsorted array of size {n}",
        "array": a[:],
        "pointers": {},
        "highlight": [],
        "variables": {"n": n},
    }

    steps.append({
        "step": 1,
        "description": f"Starting bubble sort on array of size {n}",
        "array": a[:],
        "pointers": {},
        "highlight": [],
        "variables": {"n": n, "passes": 0},
        "codeLine": 1,
    })

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            steps.append({
                "step": len(steps) + 1,
                "description": f"Compare arr[{j}]={a[j]} and arr[{j+1}]={a[j+1]}",
                "array": a[:],
                "pointers": {},
                "highlight": [j, j + 1],
                "variables": {"i": i, "j": j, "pass": i + 1},
                "codeLine": 3,
            })
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                steps.append({
                    "step": len(steps) + 1,
                    "description": f"Swap! Array now: [{', '.join(map(str, a))}]",
                    "array": a[:],
                    "pointers": {},
                    "highlight": [j, j + 1],
                    "variables": {"i": i, "j": j, "swapped": True},
                    "codeLine": 5,
                })
        if not swapped:
            steps.append({
                "step": len(steps) + 1,
                "description": "No swaps in this pass - array is sorted!",
                "array": a[:],
                "pointers": {},
                "highlight": [],
                "variables": {"i": i, "pass": i + 1, "done": True},
                "codeLine": 7,
            })
            break

    return {
        "kind": "visual_trace",
        "algorithm": "bubble_sort",
        "version": "1.0",
        "title": f"Bubble Sort (n={n})",
        "initial": initial,
        "steps": steps,
        "questions": questions or [],
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

GENERATORS = {
    "sliding_window_max": _sliding_window_max_sum,
    "two_sum": _two_sum,
    "binary_search": _binary_search,
    "bubble_sort": _bubble_sort,
}


def generate_trace(algorithm: str, input_data: dict, questions: list[dict] | None = None) -> dict[str, Any]:
    """Generate a visual_trace JSON document for an algorithm.

    This is an OFFLINE authoring tool. Output is a self-contained JSON
    document that can be saved and loaded by the frontend directly.

    Args:
        algorithm: Algorithm identifier
        input_data: Algorithm-specific input parameters
        questions: Optional interactive questions to embed

    Returns:
        A visual_trace dict conforming to visual_trace_schema.json
    """
    gen = GENERATORS.get(algorithm)
    if not gen:
        return {"kind": "visual_trace", "algorithm": algorithm, "version": "1.0", "initial": {}, "steps": [], "error": f"Unknown algorithm: {algorithm}"}

    # Map input_data to function parameters
    if algorithm == "sliding_window_max":
        return gen(arr=input_data.get("array", input_data.get("arr", [4, 2, 8, 5, 1])),
                   k=input_data.get("k", 3), questions=questions)
    elif algorithm == "two_sum":
        return gen(arr=sorted(input_data.get("array", input_data.get("arr", [2, 7, 11, 15]))),
                   target=input_data.get("target", 9), questions=questions)
    elif algorithm == "binary_search":
        return gen(arr=input_data.get("array", input_data.get("arr", [1, 3, 5, 7, 9, 11, 13])),
                   target=input_data.get("target", 7), questions=questions)
    elif algorithm == "bubble_sort":
        return gen(arr=input_data.get("array", input_data.get("arr", [64, 34, 25, 12, 22, 11, 90])),
                   questions=questions)
    else:
        return gen(**input_data, questions=questions)


# ---------------------------------------------------------------------------
# CLI: python -m app.services.algorithm_tracer --algo X --arg val ...
# ---------------------------------------------------------------------------

def _parse_args() -> tuple[str, dict]:
    """Parse simple CLI args: --algo name --key value ..."""
    args = sys.argv[1:]
    algorithm = "sliding_window_max"
    input_data: dict[str, Any] = {}
    i = 0
    while i < len(args):
        if args[i] == "--algo" and i + 1 < len(args):
            algorithm = args[i + 1]
            i += 2
        elif args[i].startswith("--") and i + 1 < len(args):
            key = args[i][2:]
            val = args[i + 1]
            # Try to parse as JSON/Python literal
            try:
                val = json.loads(val)
            except (json.JSONDecodeError, ValueError):
                try:
                    val = eval(val)
                except Exception:
                    pass
            input_data[key] = val
            i += 2
        else:
            i += 1
    return algorithm, input_data


if __name__ == "__main__":
    algo, data = _parse_args()
    trace = generate_trace(algo, data)
    print(json.dumps(trace, indent=2))
