"""
Visual Dry Runs — Step-by-step algorithm visualization.
Shows how algorithms execute with variable states at each step.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List, Dict, Any
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import curated_questions_collection
from app.services.ai import chat_completion, parse_json

router = APIRouter(prefix="/api/visualizations", tags=["visualizations"])

# Pre-built visualization templates for common algorithms
VISUALIZATION_TEMPLATES = {
    "two_sum": {
        "type": "array",
        "description": "Hash map lookup visualization",
        "steps_template": [
            {"step": 1, "action": "Initialize hash map", "state": {"hashmap": "{}", "i": "0"}},
            {"step": 2, "action": "Check if complement exists", "state": {"hashmap": "{2: 0}", "i": "1", "complement": "7"}},
            {"step": 3, "action": "Found match! Return indices", "state": {"result": "[0, 1]"}},
        ]
    },
    "binary_search": {
        "type": "array",
        "description": "Binary search on sorted array",
        "steps_template": [
            {"step": 1, "action": "Initialize pointers", "state": {"low": "0", "high": "n-1"}},
            {"step": 2, "action": "Calculate mid", "state": {"mid": "(low+high)/2"}},
            {"step": 3, "action": "Compare and adjust", "state": {"low": "updated", "high": "updated"}},
        ]
    },
    "bubble_sort": {
        "type": "array",
        "description": "Bubble sort visualization",
        "steps_template": [
            {"step": 1, "action": "Compare adjacent elements", "state": {"i": "0", "j": "0", "arr": "current"}},
            {"step": 2, "action": "Swap if out of order", "state": {"swapped": "true/false"}},
        ]
    },
    "merge_sort": {
        "type": "tree",
        "description": "Divide and conquer visualization",
        "steps_template": [
            {"step": 1, "action": "Split array", "state": {"left": "subarray", "right": "subarray"}},
            {"step": 2, "action": "Recursively sort halves", "state": {}},
            {"step": 3, "action": "Merge sorted halves", "state": {"merged": "result"}},
        ]
    },
    "bfs": {
        "type": "graph",
        "description": "Breadth-first search visualization",
        "steps_template": [
            {"step": 1, "action": "Enqueue start node", "state": {"queue": "[start]", "visited": "{}"}},
            {"step": 2, "action": "Dequeue and process", "state": {"current": "node", "queue": "updated"}},
            {"step": 3, "action": "Enqueue unvisited neighbors", "state": {"queue": "updated", "visited": "updated"}},
        ]
    },
    "dfs": {
        "type": "graph",
        "description": "Depth-first search visualization",
        "steps_template": [
            {"step": 1, "action": "Push start node to stack", "state": {"stack": "[start]", "visited": "{}"}},
            {"step": 2, "action": "Pop and process", "state": {"current": "node", "stack": "updated"}},
            {"step": 3, "action": "Push unvisited neighbors", "state": {"stack": "updated"}},
        ]
    },
    "linked_list_reverse": {
        "type": "linked_list",
        "description": "Linked list reversal visualization",
        "steps_template": [
            {"step": 1, "action": "Initialize prev=None, curr=head", "state": {"prev": "None", "curr": "1"}},
            {"step": 2, "action": "Reverse pointer", "state": {"prev": "1", "curr": "2", "next": "3"}},
        ]
    },
    "sliding_window": {
        "type": "window",
        "description": "Sliding window visualization",
        "steps_template": [
            {"step": 1, "action": "Initialize window", "state": {"window": "[start..end]", "sum": "current_sum"}},
            {"step": 2, "action": "Slide window right", "state": {"window": "updated", "sum": "updated"}},
        ]
    },
}


@router.get("/templates")
async def get_visualization_templates():
    """Get all available visualization templates."""
    templates = []
    for key, template in VISUALIZATION_TEMPLATES.items():
        templates.append({
            "id": key,
            "type": template["type"],
            "description": template["description"],
        })
    return {"templates": templates}


@router.post("/generate/{question_id}")
async def generate_visualization(
    question_id: str,
    test_case_input: str,
    user=Depends(get_current_user),
):
    """Generate a step-by-step visualization for a problem's execution."""
    collection = curated_questions_collection()

    try:
        q_oid = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await collection.find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    title = question.get("question_title", "Unknown")
    statement = question.get("statement", "")
    topics = question.get("topics", [])
    solution = question.get("solution", {})
    solution_code = solution.get("code", "")

    prompt = f"""You are an algorithm visualization expert. Generate a step-by-step dry run for this coding problem.

Problem: {title}
Statement: {statement}
Topics: {', '.join(topics)}
Solution Code:
```python
{solution_code}
```

Input for this run: {test_case_input}

Generate a detailed step-by-step execution trace in this EXACT JSON format:
{{
  "title": "{title}",
  "algorithm": "name of the algorithm used",
  "input": "{test_case_input}",
  "steps": [
    {{
      "step": 1,
      "line": <line number in code>,
      "action": "description of what this line does",
      "variables": {{"var1": "value1", "var2": "value2"}},
      "highlight": "which part of the code to highlight",
      "explanation": "why this step is important"
    }}
  ],
  "output": "final output of the algorithm",
  "complexity": {{
    "time": "O(n)",
    "space": "O(1)"
  }},
  "key_insights": ["insight1", "insight2"]
}}

Make the steps clear, educational, and easy to follow. Show variable states at each step."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=True,
            max_tokens=2000,
        )
        visualization = parse_json(result)
    except Exception as e:
        visualization = {
            "title": title,
            "algorithm": "Unknown",
            "input": test_case_input,
            "steps": [
                {"step": 1, "action": "Initialize variables", "variables": {}, "explanation": "Start the algorithm"}
            ],
            "output": "N/A",
            "complexity": {"time": "O(n)", "space": "O(1)"},
            "key_insights": ["Visualization generation failed. Please try again."],
        }

    return visualization


@router.get("/algorithm/{algorithm_name}")
async def get_algorithm_explanation(algorithm_name: str):
    """Get detailed explanation of an algorithm with visualization."""
    algorithms = {
        "binary_search": {
            "name": "Binary Search",
            "description": "Efficient search algorithm that works on sorted arrays by repeatedly dividing the search interval in half.",
            "time_complexity": "O(log n)",
            "space_complexity": "O(1)",
            "when_to_use": ["Sorted array", "Search space reduction", "Finding boundaries"],
            "key_concept": "Eliminate half the search space at each step",
            "visualization": {
                "type": "array",
                "example": "Search for 7 in [1,2,3,4,5,6,7,8,9,10]",
                "steps": [
                    {"low": 0, "high": 9, "mid": 4, "value": 5, "action": "5 < 7, search right"},
                    {"low": 5, "high": 9, "mid": 7, "value": 8, "action": "8 > 7, search left"},
                    {"low": 5, "high": 6, "mid": 5, "value": 6, "action": "6 < 7, search right"},
                    {"low": 6, "high": 6, "mid": 6, "value": 7, "action": "Found! Return index 6"},
                ]
            }
        },
        "two_pointer": {
            "name": "Two Pointers",
            "description": "Use two pointers to traverse an array, often from opposite ends or same direction.",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "when_to_use": ["Sorted array", "Pair problems", "Palindrome check"],
            "key_concept": "Move pointers based on comparison with target",
            "visualization": {
                "type": "array",
                "example": "Two Sum in [2,7,11,15], target=9",
                "steps": [
                    {"left": 0, "right": 3, "sum": 17, "action": "17 > 9, move right pointer left"},
                    {"left": 0, "right": 2, "sum": 13, "action": "13 > 9, move right pointer left"},
                    {"left": 0, "right": 1, "sum": 9, "action": "Found! Return [0,1]"},
                ]
            }
        },
        "sliding_window": {
            "name": "Sliding Window",
            "description": "Maintain a window of elements and slide it across the array/string.",
            "time_complexity": "O(n)",
            "space_complexity": "O(k)",
            "when_to_use": ["Subarray problems", "Substring problems", "Fixed/variable window"],
            "key_concept": "Expand window, shrink when constraint violated",
            "visualization": {
                "type": "window",
                "example": "Max sum subarray of size 3 in [2,1,5,1,3,2], k=3",
                "steps": [
                    {"window": [0,2], "elements": [2,1,5], "sum": 8, "action": "Initial window"},
                    {"window": [1,3], "elements": [1,5,1], "sum": 7, "action": "Slide right, sum decreases"},
                    {"window": [2,4], "elements": [5,1,3], "sum": 9, "action": "New max!"},
                    {"window": [3,5], "elements": [1,3,2], "sum": 6, "action": "Slide right, sum decreases"},
                ]
            }
        },
        "dynamic_programming": {
            "name": "Dynamic Programming",
            "description": "Solve complex problems by breaking them into overlapping subproblems and storing solutions.",
            "time_complexity": "O(n) to O(n*m)",
            "space_complexity": "O(n) to O(n*m)",
            "when_to_use": ["Optimal substructure", "Overlapping subproblems", "Counting problems"],
            "key_concept": "Build solutions from smaller subproblems using memoization or tabulation",
            "visualization": {
                "type": "dp_table",
                "example": "Fibonacci(5) with memoization",
                "steps": [
                    {"call": "fib(5)", "memo": "{}", "action": "Compute fib(5)"},
                    {"call": "fib(4)", "memo": "{}", "action": "Need fib(4)"},
                    {"call": "fib(3)", "memo": "{}", "action": "Need fib(3)"},
                    {"call": "fib(2)", "memo": "{}", "action": "Base case, return 1"},
                    {"call": "fib(1)", "memo": "{2:1}", "action": "Base case, return 1"},
                    {"call": "fib(3)", "memo": "{1:1, 2:1}", "action": "fib(3) = 2, store"},
                    {"call": "fib(2)", "memo": "{1:1, 2:1, 3:2}", "action": "Already computed, return 1"},
                    {"call": "fib(4)", "memo": "{1:1, 2:1, 3:2}", "action": "fib(4) = 3, store"},
                    {"call": "fib(3)", "memo": "{1:1, 2:1, 3:2, 4:3}", "action": "Already computed, return 2"},
                    {"call": "fib(5)", "memo": "{1:1, 2:1, 3:2, 4:3}", "action": "fib(5) = 5"},
                ]
            }
        },
        "bfs": {
            "name": "Breadth-First Search",
            "description": "Traverse graph level by level using a queue.",
            "time_complexity": "O(V + E)",
            "space_complexity": "O(V)",
            "when_to_use": ["Shortest path in unweighted graph", "Level-order traversal", "Connected components"],
            "key_concept": "Process all nodes at current depth before moving to next",
            "visualization": {
                "type": "graph",
                "example": "BFS on graph: 0-1, 0-2, 1-3, 2-3",
                "steps": [
                    {"queue": [0], "visited": {0}, "level": 0, "action": "Start at node 0"},
                    {"queue": [1,2], "visited": {0,1,2}, "level": 1, "action": "Process 0, enqueue neighbors"},
                    {"queue": [2,3], "visited": {0,1,2,3}, "level": 2, "action": "Process 1, enqueue 3"},
                    {"queue": [3], "visited": {0,1,2,3}, "level": 2, "action": "Process 2, no new neighbors"},
                ]
            }
        },
        "dfs": {
            "name": "Depth-First Search",
            "description": "Traverse graph as deep as possible before backtracking.",
            "time_complexity": "O(V + E)",
            "space_complexity": "O(V)",
            "when_to_use": ["Cycle detection", "Topological sort", "Connected components"],
            "key_concept": "Go deep first, then backtrack",
            "visualization": {
                "type": "graph",
                "example": "DFS on graph: 0-1, 0-2, 1-3, 2-3",
                "steps": [
                    {"stack": [0], "visited": {0}, "action": "Start at node 0"},
                    {"stack": [0,1], "visited": {0,1}, "action": "Visit 1"},
                    {"stack": [0,1,3], "visited": {0,1,3}, "action": "Visit 3"},
                    {"stack": [0], "visited": {0,1,3}, "action": "Backtrack to 0"},
                    {"stack": [0,2], "visited": {0,1,2,3}, "action": "Visit 2"},
                ]
            }
        },
    }

    if algorithm_name.lower() not in algorithms:
        raise HTTPException(status_code=404, detail=f"Algorithm '{algorithm_name}' not found")

    return algorithms[algorithm_name.lower()]


@router.get("/algorithms")
async def list_algorithms():
    """List all available algorithm visualizations."""
    algorithms = []
    for key, algo in [
        ("binary_search", "Binary Search"),
        ("two_pointer", "Two Pointers"),
        ("sliding_window", "Sliding Window"),
        ("dynamic_programming", "Dynamic Programming"),
        ("bfs", "Breadth-First Search"),
        ("dfs", "Depth-First Search"),
    ]:
        algorithms.append({
            "id": key,
            "name": algo,
            "description": VISUALIZATION_TEMPLATES.get(key, {}).get("description", ""),
        })
    return {"algorithms": algorithms}
