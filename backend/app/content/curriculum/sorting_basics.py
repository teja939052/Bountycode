"""
Promoted Lesson: Sorting Basics
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

Provenance: Pattern-relevant for service-company technical aptitude (TCS, Infosys,
Wipro, Cognizant, Capgemini, Accenture). Not a claim about any private employer
question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "dsa_sorting_basics_01"
VERSION = "1.0.0"
SKILL_ID = "dsa.sorting"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 18
XP_REWARD = 130

SORTING_BASICS_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "data_structures:sorting_basics",
    "title": "Sorting Basics",
    "description": "Master fundamental sorting algorithms: selection sort, insertion sort, and bubble sort with complexity analysis.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["sorting", "selection_sort", "insertion_sort", "bubble_sort", "time_complexity"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Explain selection sort, insertion sort, and bubble sort algorithms.",
        "Implement each sorting algorithm correctly.",
        "Analyze time and space complexity of each sorting algorithm.",
        "Identify which sorting algorithm to use based on input size and characteristics.",
    ],
    "prerequisites": ["coding.loops_basics", "dsa.arrays"],
    "concept_explanation": {
        "title": "Sorting Fundamentals",
        "text": (
            "Sorting arranges elements in a specific order (ascending or descending). "
            "It's a fundamental operation that makes searching, duplicate detection, "
            "and data analysis much more efficient. Different algorithms trade off "
            "simplicity, speed, and memory usage."
        ),
        "key_formula": "Selection Sort: O(n²) | Insertion Sort: O(n²) | Bubble Sort: O(n²)",
    },
    "worked_example": {
        "title": "Selection sort [64, 25, 12, 22, 11]",
        "problem": "Sort [64, 25, 12, 22, 11] using selection sort.",
        "steps": [
            "Find minimum (11) in unsorted part, swap with position 0: [11, 25, 12, 22, 64]",
            "Find minimum (12) in unsorted part [25, 12, 22, 64], swap with position 1: [11, 12, 25, 22, 64]",
            "Find minimum (22) in unsorted part [25, 22, 64], swap with position 2: [11, 12, 22, 25, 64]",
            "25 is already in place: [11, 12, 22, 25, 64]",
            "64 is last element, already sorted: [11, 12, 22, 25, 64]",
        ],
        "answer": [11, 12, 22, 25, 64],
    },
    "interactive_practice": [
        {
            "id": "sort_practice_1",
            "type": "mcq",
            "question": "What is the time complexity of selection sort?",
            "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
            "correct_index": 2,
            "explanation": "Selection sort always scans the remaining unsorted portion to find the minimum, giving O(n²) comparisons regardless of input order.",
        },
        {
            "id": "sort_practice_2",
            "type": "mcq",
            "question": "Which sorting algorithm is best for nearly sorted data?",
            "options": ["Selection sort", "Insertion sort", "Bubble sort", "All are equal"],
            "correct_index": 1,
            "explanation": "Insertion sort runs in O(n) on nearly sorted data because each element is already near its correct position.",
        },
    ],
    "misconception_feedback": {
        "stable_sort": {
            "title": "Common mistake: Confusing stable and unstable sorts",
            "text": "Selection sort is NOT stable - it can change the relative order of equal elements. Insertion sort IS stable - it preserves the relative order of equal elements.",
        },
        "best_case_selection": {
            "title": "Common mistake: Selection sort best case",
            "text": "Selection sort is always O(n²) even on already-sorted input because it always scans to find the minimum.",
        },
    },
    "assessment": {
        "questions": [
            {
                "id": "sort_assess_1",
                "type": "mcq",
                "question": "After one pass of selection sort on [64, 25, 12, 22, 11], what is the array?",
                "options": ["11, 25, 12, 22, 64", "64, 25, 12, 22, 11", "11, 25, 22, 12, 64", "12, 22, 25, 64, 11"],
                "correct_index": 0,
                "explanation": "Selection sort finds the minimum (11) and swaps it with position 0: [11, 25, 12, 22, 64].",
            },
            {
                "id": "sort_assess_2",
                "type": "mcq",
                "question": "Insertion sort on [64, 25, 12, 22, 11] - after first pass (i=1), what is the array?",
                "options": ["25, 64, 12, 22, 11", "12, 25, 64, 22, 11", "12, 25, 64, 22, 11", "64, 12, 25, 22, 11"],
                "correct_index": 0,
                "explanation": "Insertion sort takes element at i=1 (25) and inserts it in the correct position among [64]: [25, 64, 12, 22, 11].",
            },
        ],
    },
    "transfer_task": {
        "title": "Real-world: Sort student records",
        "problem": (
            "Sort an array of student objects by their score in descending order. "
            "Each student has a name and score field."
        ),
        "steps": [
            "Use sort with custom comparator comparing scores.",
            "Sort in descending order (highest score first).",
        ],
        "code": "students.sort((a, b) => b.score - a.score);",
    },
    "deterministic_answer_key": {
        "sort_practice_1": 2,
        "sort_practice_2": 1,
        "sort_assess_1": 0,
        "sort_assess_2": 0,
        "transfer_task": "students.sort((a, b) => b.score - a.score);",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://en.wikipedia.org/wiki/Sorting_algorithm",
            "https://www.geeksforgeeks.org/sorting-algorithms/",
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
            "title": "Why sorting?",
            "content": "Sorting arranges elements in a specific order (ascending or descending). It's a fundamental operation that makes searching, duplicate detection, and data analysis much more efficient.",
        },
        {
            "step_id": "manipulate",
            "step_type": "manipulate",
            "content": "Array: [64, 25, 12, 22, 11]\nFind minimum (11) in unsorted part, swap with position 0: [11, 25, 12, 22, 64]\nFind minimum (12) in unsorted part [25, 12, 22, 64], swap with position 1: [11, 12, 25, 22, 64]\nContinue until sorted.",
            "predict": "After sorting [64, 25, 12, 22, 11] with selection sort, what is the first element?",
        },
        {
            "step_id": "predict",
            "step_type": "predict",
            "content": "After first pass of selection sort on [64, 25, 12, 22, 11], what is the array?",
            "options": ["11, 25, 12, 22, 64", "64, 25, 12, 22, 11", "11, 25, 22, 12, 64", "12, 22, 25, 64, 11"],
            "correct_index": 0,
        },
        {
            "step_id": "break_debug",
            "step_type": "debug",
            "content": "Selection sort finds minimum but puts it in wrong position:\n\nfor i = 0 to n-1:\n    min_idx = i\n    for j = i+1 to n-1:\n        if arr[j] < arr[min_idx]:\n            min_idx = j\n  swap(arr[min_idx], arr[i])  // WRONG: swapped arguments!",
            "checks": ["swap arguments are swapped: should be swap(arr[i], arr[min_idx])"],
        },
        {
            "step_id": "transfer",
            "step_type": "transfer",
            "title": "Real-world: Sort student records",
            "problem": (
                "Sort an array of student objects by their score in descending order. "
                "Each student has a name and score field."
            ),
            "steps": [
                "Use sort with custom comparator comparing scores.",
                "Sort in descending order (highest score first).",
            ],
            "code": "students.sort((a, b) => b.score - a.score);",
        },
    ],
}
