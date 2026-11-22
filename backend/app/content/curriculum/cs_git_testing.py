"""
Promoted Lesson: Git and Testing
================================

Service-company technical foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company technical aptitude.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "cs_git_testing_01"
VERSION = "1.0.0"
SKILL_ID = "cs.git_testing"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 12
XP_REWARD = 100

GIT_TESTING_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "computer_science:git_testing",
    "title": "Git and Testing",
    "description": "Master version control basics (commit, branch, merge) and testing fundamentals (unit tests, assertions).",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["git_commit", "git_branch", "git_merge", "unit_testing", "assertions"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Explain git commit, branch, and merge.",
        "Write a basic unit test with assertions.",
        "Distinguish between testing and debugging.",
        "Explain why version control matters in teams.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "Git and Testing",
        "text": (
            "Git tracks changes to code over time. A commit saves a snapshot; a branch creates "
            "a parallel line of development; merge combines branches. Testing verifies code "
            "behavior — unit tests check individual functions in isolation using assertions."
        ),
        "key_formula": "git commit → git branch → git merge. assert condition, message.",
    },
    "worked_example": {
        "title": "Unit test for add function",
        "code": "def add(a, b):\n    return a + b\n\ndef test_add():\n    assert add(2, 3) == 5\n    assert add(-1, 1) == 0\n    print(\"All tests passed\")\ntest_add()",
        "explanation": "assert checks that add(2,3) equals 5. If not, AssertionError is raised.",
    },
    "interactive_practice": [
        {
            "id": "gt_practice_1",
            "type": "mcq",
            "question": "What does git commit do?",
            "options": ["Downloads code", "Saves a snapshot", "Deletes a branch", "Merges branches"],
            "correct_index": 1,
            "explanation": "git commit saves a snapshot of staged changes to the repository history.",
        },
        {
            "id": "gt_practice_2",
            "type": "mcq",
            "question": "What does assert do in a test?",
            "options": ["Prints output", "Checks a condition", "Starts a server", "Deletes data"],
            "correct_index": 1,
            "explanation": "assert verifies a condition is True; raises AssertionError if False.",
        },
    ],
    "misconception_feedback": {
        "testing_vs_debugging": {
            "title": "Common mistake: Confusing testing and debugging",
            "text": "Testing finds bugs (verify behavior). Debugging fixes bugs (find root cause).",
        },
    },
    "assessment": [
        {
            "id": "gt_assess_1",
            "type": "mcq",
            "question": "What does git merge do?",
            "options": ["Deletes commits", "Combines branches", "Renames branches", "Pushes to server"],
            "correct_index": 1,
            "explanation": "git merge combines changes from one branch into another.",
        },
        {
            "id": "gt_assess_2",
            "type": "mcq",
            "question": "Unit tests test what?",
            "options": ["Whole system", "Individual functions", "User interface", "Database only"],
            "correct_index": 1,
            "explanation": "Unit tests verify individual functions or units in isolation.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Test a multiply function",
        "problem": (
            "Write unit tests for: def multiply(a, b): return a * b. "
            "Test positive, negative, and zero cases."
        ),
        "code": "def multiply(a, b):\n    return a * b\n\ndef test_multiply():\n    assert multiply(3, 4) == 12\n    assert multiply(-2, 5) == -10\n    assert multiply(0, 100) == 0\n    print(\"All multiply tests passed\")\ntest_multiply()",
    },
    "deterministic_answer_key": {
        "gt_practice_1": 1,
        "gt_practice_2": 1,
        "gt_assess_1": 1,
        "gt_assess_2": 1,
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://git-scm.com/docs",
            "https://docs.python.org/3/library/unittest.html",
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
        "initial_interval_days": 2,
        "ease_factor": 2.5,
        "retention_target": 0.85,
    },
}
