"""
Promoted Lesson: Binary Search
==================================

Service-company DSA foundation. Follows the full content contract:

- Stable lesson ID, version, canonical skill ID
- Company relevance classification
- Learning objectives, prerequisites
- Concept explanation, worked example
- Interactive practice, misconception-specific feedback
- Assessment, transfer task, deterministic answer key
- Source/provenance metadata, review state, accessibility metadata
- Estimated time, spaced-repetition metadata

Provenance: Pattern-relevant for service-company coding assessments (TCS, Infosys,
Wipro, Cognizant, Capgemini, Accenture). Not a claim about any private employer
question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "dsa_binary_search_01"
VERSION = "1.0.0"
SKILL_ID = "dsa.binary_search"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 18
XP_REWARD = 140

BINARY_SEARCH_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "data_structures:binary_search",
    "title": "Binary Search",
    "description": "Master binary search - the classic O(log n) search algorithm for sorted arrays.",
    "difficulty": "medium",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["binary_search", "divide_and_conquer", "sorted_array_search"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Explain how binary search works and why it's O(log n).",
        "Implement binary search iteratively and recursively.",
        "Identify when binary search can be applied (sorted data).",
        "Trace binary search execution step by step.",
    ],
    "prerequisites": ["coding.loops_basics", "dsa.arrays"],
    "concept_explanation": {
        "title": "Binary Search",
        "text": (
            "Binary search finds a target value in a sorted array by repeatedly dividing "
            "the search interval in half. Start with the middle element: if it matches the "
            "target, return its index. If the target is smaller, search the left half; if "
            "larger, search the right half. Repeat until found or the interval is empty."
        ),
        "key_formula": "mid = (low + high) / 2; if arr[mid] == target return mid; if arr[mid] > target search left; else search right",
    },
    "worked_example": {
        "title": "Binary search for 7 in [1, 3, 5, 7, 9, 11]",
        "problem": "Find index of 7 in [1, 3, 5, 7, 9, 11].",
        "steps": [
            "low=0, high=5, mid=2. arr[2]=5. 5 < 7, so search right half: low=3.",
            "low=3, high=5, mid=4. arr[4]=9. 9 > 7, so search left half: high=3.",
            "low=3, high=3, mid=3. arr[3]=7. Found! Return index 3.",
        ],
        "answer": 3,
    },
    "interactive_practice": [
        {
            "id": "bs_practice_1",
            "type": "mcq",
            "question": "What is the time complexity of binary search?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
            "correct_index": 1,
            "explanation": "Binary search halves the search space each iteration, giving O(log n) time complexity.",
        },
        {
            "id": "bs_practice_2",
            "type": "mcq",
            "question": "Which condition must be true for binary search to work?",
            "options": ["Array must be sorted", "Array must be unsorted", "Array must contain unique elements", "Array must have even length"],
            "correct_index": 0,
            "explanation": "Binary search requires a sorted array because it relies on comparing values to eliminate half the search space.",
        },
    ],
    "misconception_feedback": {
        "off_by_one": {
            "title": "Common mistake: Off-by-one in boundary updates",
            "text": "When the target is less than mid, set high = mid - 1 (not mid). When greater, set low = mid + 1 (not mid). Including mid causes infinite loops.",
        },
        "unsorted_array": {
            "title": "Common mistake: Binary search on unsorted data",
            "text": "Binary search only works on sorted data. Applying it to unsorted arrays gives incorrect results.",
        },
    },
    "assessment": {"questions": [
        {
            "id": "bs_assess_1",
            "type": "mcq",
            "question": "In binary search for target 7 in [1, 3, 5, 7, 9], what is the first mid index?",
            "options": ["0", "1", "2", "3"],
            "correct_index": 2,
            "explanation": "mid = (0 + 4) / 2 = 2. arr[2] = 5.",
        },
        {
            "id": "bs_assess_2",
            "type": "mcq",
            "question": "If target < arr[mid], which half should be searched next?",
            "options": ["Right half", "Left half", "Both halves", "Neither half"],
            "correct_index": 1,
            "explanation": "If target < arr[mid], the target (if present) must be in the left half.",
        },
    ]},
    "transfer_task": {
        "title": "Real-world: Find first occurrence",
        "problem": (
            "Given a sorted array with duplicates, find the FIRST occurrence of a target value. "
            "For example, in [1, 2, 2, 2, 3], find the first index of 2 (answer: 1)."
        ),
        "steps": [
            "Use binary search but don't stop when you find the target.",
            "When arr[mid] == target, record mid as a candidate and search left (high = mid - 1) to find earlier occurrences.",
            "Return the leftmost occurrence found.",
        ],
        "answer": "int left = 0, right = n - 1, result = -1;\nwhile (left <= right) {\n  int mid = (left + right) / 2;\n  if (arr[mid] == target) { result = mid; right = mid - 1; }\n  else if (arr[mid] < target) left = mid + 1;\n  else right = mid - 1;\n}\nreturn result;",
    },
    "deterministic_answer_key": {
        "bs_practice_1": 1,
        "bs_practice_2": 0,
        "bs_assess_1": 2,
        "bs_assess_2": 1,
        "transfer_task": "int left = 0, right = n - 1, result = -1;\nwhile (left <= right) {\n  int mid = (left + right) / 2;\n  if (arr[mid] == target) { result = mid; right = mid - 1; }\n  else if (arr[mid] < target) left = mid + 1;\n  else right = mid - 1;\n}\nreturn result;",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://en.wikipedia.org/wiki/Binary_search_algorithm",
            "https://www.geeksforgeeks.org/binary-search/",
        ],
        "note": (
            "This preparation path targets commonly reported patterns and role expectations. "
            "It is not a claim about a private employer question bank."
        ),
    },
    "review_state": "human_reviewed",
    "accessibility_metadata": {
        "color_blind_safe": True,
        "screen_reader_friendly": True,
        "font_scale_support": True,
    },
    "spaced_repetition_metadata": {
        "initial_interval_days": 1,
        "ease_factor": 2.5,
        "retention_target": 0.85,
    },
    "steps": [
        {
            "step_id": "discovery",
            "step_type": "discover",
            "title": "Why binary search?",
            "content": "Finding a name in a phone book: you don't start from page 1. You open the middle, check if your target is before or after, and eliminate half the book each time.",
        },
        {
            "step_id": "manipulate",
            "step_type": "manipulate",
            "content": "Array: [1, 3, 5, 7, 9, 11]. Search for 7.\nStart: low=0, high=5. mid = (0+5)/2 = 2. arr[2] = 5.\nSince 5 < 7, search right: low = mid + 1 = 3.\nNext: low=3, high=5. mid = (3+5)/2 = 4. arr[4] = 9.\nSince 9 > 7, search left: high = mid - 1 = 3.\nNext: low=3, high=3. mid = 3. arr[3] = 7. Found!",
            "predict": "If searching for 11 in [1, 3, 5, 7, 9, 11], what is the first mid index?",
        },
        {
            "step_id": "predict",
            "step_type": "predict",
            "content": "Array: [1, 3, 5, 7, 9, 11]. Target: 11. What is the first mid index?",
            "options": ["2", "3", "4", "5"],
            "correct_index": 2,
        },
        {
            "step_id": "break_debug",
            "step_type": "debug",
            "content": "This binary search loops forever. Find the bug:\n\nint left = 0, right = n - 1;\nwhile (left <= right) {\n  int mid = (left + right) / 2;\n  if (arr[mid] == target) return mid;\n  if (arr[mid] < target) left = mid;  // BUG\n  else right = mid - 1;\n}",
            "checks": ["left = mid should be left = mid + 1"],
        },
        {
            "step_id": "transfer",
            "step_type": "transfer",
            "title": "Find first occurrence",
            "problem": "Given [1, 2, 2, 2, 3], find first index of 2.",
            "steps": [
                "Binary search for 2.",
                "When arr[mid] == 2, record mid but keep searching left for earlier occurrences.",
                "Return the leftmost occurrence.",
            ],
            "code": "int left = 0, right = n - 1, result = -1;\nwhile (left <= right) {\n  int mid = (left + right) / 2;\n  if (arr[mid] == target) { result = mid; right = mid - 1; }\n  else if (arr[mid] < target) left = mid + 1;\n  else right = mid - 1;\n}\nreturn result;",
        },
    ],
}
