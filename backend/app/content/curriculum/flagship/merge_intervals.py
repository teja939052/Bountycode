"""
Flagship Lesson — Merge Intervals
 ===================================

 Gold-standard interactive lesson for the intervals pattern.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "merge_intervals"

LESSON: Dict[str, Any] = {
    "lesson_id": "merge_intervals_overlap_merge",
    "module_id": "dsa:intervals:merge",
    "title": "The Overlap Merge",
    "description": "Merge overlapping intervals and handle insertion in O(n log n).",
    "difficulty": "intermediate",
    "est_minutes": 16,
    "xp_reward": 130,
    "skills_taught": ["intervals", "merge_intervals", "sorting"],
    "srs_concept_tag": "dsa:intervals:merge",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Overlap Merge only works because intervals are sorted by start. "
            "You compare the current interval to the previous one. If they overlap, merge them. "
            "If not, start a new group. Sorting first makes the rest trivial.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You merged only the overlapping runs.”",
            "🧭 **Captain Byte**\n“Clean. Sorting first makes the merge pass trivial.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t scan unsorted. Sort by start first.”",
            "🧭 **Captain Byte**\n“You merged non-overlapping intervals. Check the end of the previous.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the wrong assumption. Now merge only when current.start <= prev.end.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any interval overlap problem.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Sort by start, then merge only overlapping runs.”",
    },
    "story_context": {
        "title": "The Overlap Merge",
        "narration": (
            "The Overlap Merge only works because intervals are sorted by start. "
            "You compare the current interval to the previous one. If they overlap, merge them. "
            "If not, start a new group."
        ),
        "setting": "overlap_merge",
        "character": "Captain Byte",
        "intro_text": (
            "Interval problems become easy once you realize the only comparison that matters "
            "is current.start vs previous.end. Sort first, then merge in one pass."
        ),
    },
    "discovery": {
        "title": "Find the Overlap",
        "visual_primitives": ["compare", "transform", "trace"],
        "steps": [
            {
                "action": "sort_first",
                "narration": "Sorting by start guarantees that overlapping intervals appear consecutively.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "intervals = [[5, 7], [1, 3], [2, 6]]\nintervals.sort(key=lambda x: x[0])\nprint(intervals)",
                    "expected_output": "[[1, 3], [2, 6], [5, 7]]",
                    "hint": "Sort by the first element of each interval.",
                },
            },
            {
                "action": "overlap_rule",
                "narration": "If current.start <= previous.end, the intervals overlap. Merge by extending the previous end.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "prev = [1, 3], current = [2, 6]. Do they overlap?",
                    "options": [
                        {"id": "a", "text": "Yes — merge to [1, 6]", "correct": True},
                        {"id": "b", "text": "No — keep both", "correct": False},
                        {"id": "c", "text": "Yes — merge to [2, 6]", "correct": False},
                        {"id": "d", "text": "Depends on length", "correct": False},
                    ],
                    "explanation": "2 <= 3, so they overlap. The merged interval is [min(1,2), max(3,6)] = [1, 6].",
                },
            },
            {
                "action": "new_group",
                "narration": "If current.start > previous.end, the intervals do not overlap. Start a new merged group.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "prev = [1, 3], current = [4, 7]. What should you do?",
                    "options": [
                        {"id": "a", "text": "Merge to [1, 7]", "correct": False},
                        {"id": "b", "text": "Start a new group — no overlap", "correct": True},
                        {"id": "c", "text": "Skip current", "correct": False},
                        {"id": "d", "text": "Swap them", "correct": False},
                    ],
                    "explanation": "4 > 3, so there is a gap. They stay separate.",
                },
            },
            {
                "action": "insert_case",
                "narration": "Inserting a new interval is the same merge pass plus one extra interval.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def insert(intervals, newInterval):\n    intervals.append(newInterval)\n    intervals.sort(key=lambda x: x[0])\n    merged = []\n    for interval in intervals:\n        if not merged or interval[0] > merged[-1][1]:\n            merged.append(interval)\n        else:\n            merged[-1][1] = max(merged[-1][1], interval[1])\n    return merged\nprint(insert([[1, 3], [6, 9]], [2, 5]))",
                    "expected_output": "[[1, 5], [6, 9]]",
                    "hint": "After sorting, [2, 5] overlaps [1, 3] and becomes [1, 5].",
                },
            },
        ],
        "conclusion": (
            "Interval problems reduce to: sort by start, then merge when current.start <= previous.end. "
            "Insertion is the same algorithm with one extra interval added first."
        ),
    },
    "prediction": {
        "title": "Before You Merge",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict the merged result.”",
        "question": "Given [[1, 3], [2, 6], [8, 10], [15, 18]], what is the first merge step?",
        "options": [
            {"id": "a", "text": "Merge [1,3] and [2,6] into [1,6]", "correct": True, "explanation": "2 <= 3, so they overlap. max(3,6) = 6."},
            {"id": "b", "text": "Merge all into one interval", "correct": False, "explanation": "[8,10] and [15,18] do not overlap with the first group."},
            {"id": "c", "text": "Keep all four intervals separate", "correct": False, "explanation": "[1,3] and [2,6] do overlap."},
            {"id": "d", "text": "Merge [2,6] and [8,10]", "correct": False, "explanation": "8 > 6, so they do not overlap."},
        ],
        "explanation": "The first two intervals overlap because 2 <= 3. They merge to [1, 6].",
    },
    "explain": {
        "title": "Explain the Merge Rule",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why does sorting by start make interval merging correct?”",
        "prompt": "Why does sorting by start make interval merging correct?",
        "answer_format": "short_answer",
        "keywords": ["sort", "start", "consecutive", "overlap", "previous", "end", "order", "guarantee"],
        "min_words": 10,
        "model_answer": (
            "Sorting by start guarantees that if interval i overlaps with any earlier interval, "
            "it must overlap with the immediately previous one in the sorted order. "
            "Therefore, comparing only to the last merged interval is sufficient."
        ),
        "intention": "The explanation must connect sorted order to the single-pass merge guarantee.",
    },
    "guided_build": {
        "title": "Write the Merger",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the merge pass.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Merge Intervals",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Sort by start, then merge overlapping runs.”",
                "description": "Given an array of intervals, merge all overlapping intervals.",
                "starter_code": "def merge(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = []\n    for interval in intervals:\n        if not merged or interval[0] > merged[-1][1]:\n            merged.append(interval)\n        else:\n            merged[-1][1] = max(merged[-1][1], interval[1])\n    return merged\n",
                "function_name": "merge",
                "signature": "def merge(intervals: List[List[int]]) -> List[List[int]]:",
                "test_cases": [
                    {"input": [[[1, 3], [2, 6], [8, 10], [15, 18]]], "expected": [[1, 6], [8, 10], [15, 18]]},
                    {"input": [[[1, 4], [4, 5]]], "expected": [[1, 5]]},
                ],
                "hidden_test_cases": [
                    {"input": [[[1, 4], [0, 4]]], "expected": [[0, 4]]},
                    {"input": [[[1, 4], [2, 3]]], "expected": [[1, 4]]},
                    {"input": [[[1, 4], [5, 6]]], "expected": [[1, 4], [5, 6]]},
                ],
                "diamonds": 45,
                "scaffolded_hints": [
                    {"level": 1, "text": "Sort intervals by their start value."},
                    {"level": 2, "text": "If current.start <= last.end, merge by extending last.end."},
                    {"level": 3, "text": "Otherwise append current as a new interval."},
                ],
            },
            {
                "step_order": 2,
                "title": "Insert Interval",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Add one interval, then merge as usual.”",
                "description": "Insert a new interval into a sorted non-overlapping list and merge if necessary.",
                "starter_code": "def insert(intervals, newInterval):\n    result = []\n    i = 0\n    while i < len(intervals) and intervals[i][1] < newInterval[0]:\n        result.append(intervals[i])\n        i += 1\n    while i < len(intervals) and intervals[i][0] <= newInterval[1]:\n        newInterval[0] = min(newInterval[0], intervals[i][0])\n        newInterval[1] = max(newInterval[1], intervals[i][1])\n        i += 1\n    result.append(newInterval)\n    while i < len(intervals):\n        result.append(intervals[i])\n        i += 1\n    return result\n",
                "function_name": "insert",
                "signature": "def insert(intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:",
                "test_cases": [
                    {"input": [[[1, 3], [6, 9]], [2, 5]], "expected": [[1, 5], [6, 9]]},
                    {"input": [[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]], "expected": [[1, 2], [3, 10], [12, 16]]},
                ],
                "hidden_test_cases": [
                    {"input": [[], [5, 7]], "expected": [[5, 7]]},
                    {"input": [[[1, 5]], [6, 8]], "expected": [[1, 5], [6, 8]]},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Add all non-overlapping intervals before newInterval first."},
                    {"level": 2, "text": "Merge all intervals that overlap with newInterval."},
                    {"level": 3, "text": "Append the merged interval, then add the rest."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Meeting Rooms II",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same intervals, different question. How many meeting rooms?”",
        "description": (
            "Given an array of meeting time intervals, return the minimum number of conference rooms required."
        ),
        "function_name": "min_meeting_rooms",
        "signature": "def min_meeting_rooms(intervals: List[List[int]]) -> int:",
        "description_full": (
            "Return the minimum number of conference rooms required.\n\n"
            "Example:\n"
            "  min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) -> 2\n\n"
            "Hint: use a min-heap of end times."
        ),
        "test_cases": [
            {"input": [[[0, 30], [5, 10], [15, 20]]], "expected": 2},
            {"input": [[[7, 10], [2, 4]]], "expected": 1},
        ],
        "hidden_test_cases": [
            {"input": [[[0, 5], [1, 2], [2, 3], [3, 4]]], "expected": 2},
            {"input": [[[1, 10], [2, 3], [3, 4], [4, 5]]], "expected": 2},
        ],
        "time_limit_minutes": 8,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Sort intervals by start time."},
            {"level": 2, "text": "Use a min-heap to track the earliest ending meeting."},
            {"level": 3, "text": "If the current start is >= earliest end, reuse that room; else add a new room."},
        ],
    },
    "assessment": {
        "title": "Overlap Merge Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove you can merge and count rooms. Timed.”",
        "description": "Merge intervals, explain the sort guarantee, and fix an insertion bug.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "intervals = [[1, 3], [2, 6], [8, 10]]\nintervals.sort()\nmerged = []\nfor interval in intervals:\n    if not merged or interval[0] > merged[-1][1]:\n        merged.append(interval)\n    else:\n        merged[-1][1] = max(merged[-1][1], interval[1])\nprint(merged)",
                "answer_format": "single_choice",
                "expected_answer": "[[1, 6], [8, 10]]",
                "options": [
                    {"id": "a", "text": "[[1, 6], [8, 10]]", "correct": True},
                    {"id": "b", "text": "[[1, 3], [2, 6], [8, 10]]", "correct": False},
                    {"id": "c", "text": "[[1, 10]]", "correct": False},
                    {"id": "d", "text": "[[1, 3], [2, 6], [8, 10]]", "correct": False},
                ],
                "explanation": "[1,3] and [2,6] overlap, merging to [1,6]. [8,10] stays separate.",
            },
            {
                "type": "concept",
                "question": "Why must intervals be sorted by start time before merging?",
                "answer_format": "short_answer",
                "keywords": ["sort", "start", "consecutive", "overlap", "previous", "order", "guarantee"],
                "explanation": "Sorting guarantees that any overlapping intervals appear consecutively.",
            },
            {
                "type": "debug",
                "code": "def merge(intervals):\n    merged = []\n    for interval in intervals:\n        if not merged or interval[0] > merged[-1][1]:\n            merged.append(interval)\n        else:\n            merged[-1][1] = max(merged[-1][1], interval[1])\n    return merged\n# input is unsorted",
                "error": "merge([[5, 7], [1, 3], [2, 6]]) returns [[5, 7], [1, 6]] instead of [[1, 6], [5, 7]].",
                "question": "Fix the missing sort step.",
                "fix": "intervals.sort(key=lambda x: x[0])",
                "explanation": "Without sorting, overlapping intervals may not be adjacent, so the merge pass misses them.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Missed Overlap",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I removed the sort. Find the broken assumption.”",
        "story": (
            "A programmer merged intervals without sorting first. On [[5, 7], [1, 3], [2, 6]], "
            "the result was [[5, 7], [1, 6]] — [1, 3] and [2, 6] were never adjacent. "
            "What assumption is wrong?"
        ),
        "buggy_code": "def merge(intervals):\n    merged = []\n    for interval in intervals:\n        if not merged or interval[0] > merged[-1][1]:\n            merged.append(interval)\n        else:\n            merged[-1][1] = max(merged[-1][1], interval[1])\n    return merged\n",
        "expected_output": "[[1, 6], [5, 7]]",
        "actual_output": "[[5, 7], [1, 6]] — missed the [1,3] + [2,6] overlap",
        "diagnosis": {
            "question": "Which assumption makes this merger miss overlaps?",
            "options": [
                {"id": "a", "text": "It assumes intervals are already sorted by start", "correct": True, "why": "Without sorting, overlapping intervals may not be consecutive in the input."},
                {"id": "b", "text": "It uses > instead of >=", "correct": False, "why": "The comparison operator is correct for non-overlapping detection."},
                {"id": "c", "text": "It appends instead of replacing", "correct": False, "why": "Appending new intervals is correct when they don't overlap."},
                {"id": "d", "text": "It doesn't handle empty input", "correct": False, "why": "Empty input would return [], which is correct."},
            ],
        },
        "fix": "intervals.sort(key=lambda x: x[0])",
        "fixed_code": "def merge(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = []\n    for interval in intervals:\n        if not merged or interval[0] > merged[-1][1]:\n            merged.append(interval)\n        else:\n            merged[-1][1] = max(merged[-1][1], interval[1])\n    return merged\n",
        "explanation": (
            "Sorting by start guarantees that overlapping intervals are consecutive. "
            "Without sorting, the merge pass only compares to the last appended interval, missing overlaps elsewhere."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:intervals:merge",
        "concept_name": "Merge Intervals",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "sort intervals by start time",
            "compare current.start to previous.end",
            "merge when overlapping",
            "start new group when separated",
        ],
        "spaced_fields": [
            "sort_by_start",
            "overlap_condition",
            "merge_extend_end",
            "new_group",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "merge_intervals",
        "unlocks_next": ["interval_patterns"],
        "tower_badge": "overlap_merge",
        "world_node": {
            "level": 17,
            "title": "The Overlap Merge",
            "color": "teal",
            "icon": "🔗",
            "description": "Merge overlapping intervals in O(n log n) after sorting",
        },
    },
}
