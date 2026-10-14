"""
Concept Clarity Slice: Heap / Priority Queue
=============================================

A heap is a complete binary tree where every parent obeys the heap property:
in a max-heap, parent >= children; in a min-heap, parent <= children.
The smallest/largest element is always at the root, so extraction is O(1)
and insertion is O(log n).

Misconceptions attacked:
  1. "Heap is a sorted structure" — no; only the root is ordered
  2. "Heap sort is the same as heapify" — heapify builds a heap; heap sort uses it
  3. "Heap is only for sorting" — it is also for Dijkstra, event loops, and scheduling
"""
from typing import Dict, Any

HEAP_SLICE: Dict[str, Any] = {
    "lesson_id": "heap_scheduler",
    "module_id": "dsa:heap",
    "title": "The Task Scheduler",
    "description": "Learn heaps by scheduling tasks by priority with a min-heap.",
    "difficulty": "medium",
    "est_minutes": 16,
    "xp_reward": 260,
    "skills_taught": ["heap", "priority_queue", "binary_heap", "greedy"],
    "srs_concept_tag": "dsa:heap",
    "story_context": {
        "title": "The Task Scheduler",
        "narration": (
            "The task board holds jobs with priority numbers. The scheduler always "
            "executes the smallest priority first. It does not sort the whole board; "
            "it only cares about the top task."
        ),
        "setting": "task_board",
        "character": "Foreman Brin",
        "intro_text": (
            "Every task has a priority. I pull the smallest priority from the top, "
            "and when a new task arrives I sift it into place."
        ),
    },
    "discovery": {
        "title": "Top Task Only",
        "steps": [
            {
                "action": "inspect_heap",
                "narration": (
                    "The heap stores [3, 9, 5]. The smallest value is at index 0. "
                    "Children of 0 are at 1 and 2."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "heap = [3, 9, 5]\nprint('Smallest:', heap[0])\nprint('Left child:', heap[1] if len(heap) > 1 else None)\nprint('Right child:', heap[2] if len(heap) > 2 else None)",
                    "expected_output": "Smallest: 3\nLeft child: 9\nRight child: 5",
                    "hint": "For index i, children are at 2*i+1 and 2*i+2.",
                },
            },
        ],
    },
    "manipulation": {
        "title": "Push and Pop",
        "steps": [
            {
                "action": "push",
                "narration": "Push 2 into the heap and sift it up until the parent is smaller.",
                "interaction": {
                    "type": "code",
                    "starter_code": "heap = [3, 9, 5]\n\ndef push(val):\n    # TODO: append and sift up\n    pass\n\npush(2)\nprint(heap)\n",
                    "solution": "heap = [3, 9, 5]\n\ndef push(val):\n    heap.append(val)\n    i = len(heap) - 1\n    while i > 0:\n        parent = (i - 1) // 2\n        if heap[parent] <= heap[i]:\n            break\n        heap[parent], heap[i] = heap[i], heap[parent]\n        i = parent\n\npush(2)\nprint(heap)\n",
                    "expected_output": "[2, 3, 5, 9]\n",
                    "hint": "Swap with parent while child is smaller than parent.",
                },
            },
        ],
    },
    "code": {
        "title": "Min-Heap with Push and Pop",
        "starter_code": "class MinHeap:\n    def __init__(self):\n        self.heap = []\n\n    def push(self, val):\n        # TODO\n        pass\n\n    def pop(self):\n        # TODO: remove and return smallest\n        pass\n\nh = MinHeap()\nfor x in [5, 3, 8, 1]: h.push(x)\nprint(h.pop())\nprint(h.pop())\n",
        "solution": "class MinHeap:\n    def __init__(self):\n        self.heap = []\n\n    def push(self, val):\n        self.heap.append(val)\n        i = len(self.heap) - 1\n        while i > 0:\n            parent = (i - 1) // 2\n            if self.heap[parent] <= self.heap[i]:\n                break\n            self.heap[parent], self.heap[i] = self.heap[i], self.heap[parent]\n            i = parent\n\n    def pop(self):\n        if not self.heap:\n            return None\n        smallest = self.heap[0]\n        last = self.heap.pop()\n        if self.heap:\n            self.heap[0] = last\n            self._sift_down(0)\n        return smallest\n\n    def _sift_down(self, i):\n        n = len(self.heap)\n        while True:\n            left = 2 * i + 1\n            right = 2 * i + 2\n            smallest = i\n            if left < n and self.heap[left] < self.heap[smallest]:\n                smallest = left\n            if right < n and self.heap[right] < self.heap[smallest]:\n                smallest = right\n            if smallest == i:\n                break\n            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]\n            i = smallest\n\nh = MinHeap()\nfor x in [5, 3, 8, 1]: h.push(x)\nprint(h.pop())\nprint(h.pop())\n",
        "expected_output": "1\n3\n",
    },
    "checks": [
        r"def push\(",
        r"def pop\(",
        r"_sift_down\(",
    ],
    "success": {
        "before": "You search the whole board for the top task.",
        "after": "You always know the top task is at index 0.",
        "title": "Task Scheduler — you can push and pop with a min-heap.",
        "lesson": "Heaps keep the best candidate at the top without sorting everything.",
        "next": "Try Dijkstra or top-k problems next.",
    },
}
