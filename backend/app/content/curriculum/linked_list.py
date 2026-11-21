"""
Promoted Lesson: Linked Lists
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

LESSON_ID = "dsa_linked_list_01"
VERSION = "1.0.0"
SKILL_ID = "dsa.linked_list"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 18
XP_REWARD = 140

LINKED_LIST_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "data_structures:linked_list_basics",
    "title": "Linked Lists",
    "description": "Master linked list fundamentals: node structure, traversal, insertion, deletion, and comparison with arrays.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["linked_list", "node_traversal", "insertion", "deletion", "array_vs_linked_list"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Explain linked list structure (nodes with data and next pointer).",
        "Implement insertion and deletion at head, tail, and specific positions.",
        "Compare linked list vs array trade-offs.",
        "Implement basic linked list traversal and search.",
    ],
    "prerequisites": ["coding.loops_basics", "dsa.arrays"],
    "concept_explanation": {
        "title": "What is a Linked List?",
        "text": (
            "A linked list is a linear data structure where elements (nodes) are not stored "
            "in contiguous memory. Each node contains data and a pointer (reference) to the "
            "next node. The first node is called the head, and the last node points to null/nullptr."
        ),
        "key_formula": "node = { data: value, next: next_node_or_null }",
    },
    "worked_example": {
        "title": "Insert at beginning of linked list",
        "problem": "Insert value 5 at the beginning of list [10, 20, 30].",
        "steps": [
            "Create new node with data = 5.",
            "Set new_node.next = current head (10).",
            "Update head to point to new node (5).",
            "Result: [5, 10, 20, 30].",
        ],
        "answer": "[5, 10, 20, 30]",
    },
    "interactive_practice": [
        {
            "id": "ll_practice_1",
            "type": "mcq",
            "question": "In a linked list, each node contains:",
            "options": ["Only data", "Only next pointer", "Data and next pointer", "Data, next pointer, and previous pointer"],
            "correct_index": 2,
            "explanation": "A singly linked list node contains data and a next pointer to the next node.",
        },
        {
            "id": "ll_practice_2",
            "type": "mcq",
            "question": "What is the time complexity to insert at the beginning of a linked list?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "correct_index": 0,
            "explanation": "Insertion at the beginning is O(1) - create node, point it to current head, update head pointer.",
        },
    ],
    "misconception_feedback": {
        "array_vs_linked_list": {
            "title": "Common mistake: Arrays vs linked lists access",
            "text": "Arrays allow O(1) random access by index. Linked lists require O(n) traversal to reach a specific position.",
        },
        "memory_layout": {
            "title": "Common mistake: Memory layout",
            "text": "Arrays store elements contiguously; linked list nodes can be scattered in memory, connected via pointers.",
        },
    },
    "assessment": {"questions": [
        {
            "id": "ll_assess_1",
            "type": "mcq",
            "question": "Which operation is O(1) for linked list but O(n) for array?",
            "options": ["Access element at index i", "Insert at beginning", "Delete last element", "Search for value"],
            "correct_index": 1,
            "explanation": "Insert at beginning is O(1) for linked list (just update head pointer) but O(n) for array (shift all elements).",
        },
        {
            "id": "ll_assess_2",
            "type": "mcq",
            "question": "What does the 'next' pointer of the last node point to?",
            "options": ["First node (head)", "None/null", "Itself", "Random node"],
            "correct_index": 1,
            "explanation": "The last node's next pointer is null/None, indicating the end of the list.",
        },
    ]},
    "transfer_task": {
        "title": "Real-world: Implement undo functionality",
        "problem": (
            "Implement an undo feature for a text editor using a linked list. "
            "Each text state is a node. When user presses undo, move to previous state."
        ),
        "steps": [
            "Each text state is a node with data (text content) and next pointer.",
            "Maintain a 'current' pointer to current state.",
            "Undo: move current pointer to previous node (requires doubly linked list or maintain history stack).",
        ],
        "answer": "Use a doubly linked list where each node has prev and next pointers. To undo, move current = current.prev.",
    },
    "deterministic_answer_key": {
        "ll_practice_1": 2,
        "ll_practice_2": 0,
        "ll_assess_1": 1,
        "ll_assess_2": 1,
        "transfer_task": "Use a doubly linked list where each node has prev and next pointers. To undo, move current = current.prev.",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://en.wikipedia.org/wiki/Linked_list",
            "https://www.geeksforgeeks.org/data-structures/linked-list/",
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
            "title": "Why linked lists?",
            "content": "Arrays store elements contiguously. Linked lists store nodes anywhere in memory, connected by pointers. This makes insertion/deletion efficient but access slower.",
        },
        {
            "step_id": "manipulate",
            "step_type": "manipulate",
            "content": "Node structure: { data: value, next: next_node }\nHead -> [data: 10, next: node2] -> [data: 20, next: node3] -> [data: 30, next: null]\n\nTo insert 5 at beginning: create node(5), set its next to current head, update head to new node.",
            "predict": "After inserting 5 at beginning of [10, 20, 30], what is the new head's data?",
        },
        {
            "step_id": "predict",
            "step_type": "predict",
            "content": "After inserting 5 at beginning of linked list [10, 20, 30], what is head.data?",
            "options": ["10", "20", "30", "5"],
            "correct_index": 3,
        },
        {
            "step_id": "break_debug",
            "step_type": "debug",
            "content": "Linked list insertion has a bug:\n\nnew_node.next = head\nhead = new_node\nnew_node.next = head  // BUG: overwrites the just-set next!\n",
            "checks": ["Order matters: set new_node.next = head BEFORE setting head = new_node"],
        },
        {
            "step_id": "transfer",
            "step_type": "transfer",
            "title": "Undo functionality",
            "problem": "Implement undo using linked list where each node stores a text state.",
            "steps": [
                "Each node stores text state and prev pointer (doubly linked list).",
                "Current pointer points to current state.",
                "To undo: current = current.prev.",
            ],
            "code": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.prev = None\n        self.next = None\n\ncurrent = head  # current state\n# To undo:\ncurrent = current.prev",
        },
    ],
}
