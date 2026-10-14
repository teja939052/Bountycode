"""Lesson module — Recursion — Function Calls Itelf"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'coding.recursion',
            'module_id': 'coding.recursion',
            'title': 'Recursion — Function Calls Itelf',
            'description': 'Recursion simplifies problems with self-similar structure. It appears in every coding interview.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Recursion'],
            'srs_concept_tag': 'coding.recursion',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Recursion solves problems by breaking them into smaller copies of the same problem. Always include a base case.',
            'correct': ['Right base case.', 'Correct recursive step.', 'Right termination.'],
            'wrong': ['Every recursive function needs a base case.', 'Recursion is not always better than iteration.', 'Trace the call stack to verify termination.'],
            'after_break': 'You found the recursion error. Now fix the base case or step.',
            'after_mastery': "You can now reason recursively. That's coding interview skill.",
            'retry_prompt': 'Try again. Check the base case first.'
        },
            'story_context': {
            'title': 'Recursion — Function Calls Itelf',
            'narration': 'Recursion simplifies problems with self-similar structure. It appears in every coding interview.',
            'setting': 'recursion',
            'character': 'Captain Byte',
            'intro_text': 'Recursion simplifies problems with self-similar structure. It appears in every coding interview.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'transform'],
            'steps': [{
            'action': 'see_factorial',
            'narration': 'factorial(5) = 5 × factorial(4) until factorial(0) = 1.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What is factorial(3)?',
            'options': [{
            'id': 'a',
            'text': '5',
            'correct': False
        }, {
            'id': 'b',
            'text': '6',
            'correct': True
        }, {
            'id': 'c',
            'text': '9',
            'correct': False
        }, {
            'id': 'd',
            'text': '3',
            'correct': False
        }],
            'explanation': '3 × 2 × 1 = 6.'
        }
        }, {
            'action': 'see_call_stack',
            'narration': 'factorial(3) calls factorial(2) calls factorial(1) calls factorial(0).',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'How many function calls for factorial(3) including the base?',
            'options': [{
            'id': 'a',
            'text': '2',
            'correct': False
        }, {
            'id': 'b',
            'text': '3',
            'correct': False
        }, {
            'id': 'c',
            'text': '4',
            'correct': True
        }, {
            'id': 'd',
            'text': '5',
            'correct': False
        }],
            'explanation': 'factorial(3), factorial(2), factorial(1), factorial(0) = 4 calls.'
        }
        }],
            'conclusion': 'Recursion needs a base case and a smaller subproblem. Each call waits for the inner call. Too many calls can cause stack overflow.'
        },
            'understand': 'Recursion solves a problem by solving a smaller instance of the same problem. Base case stops recursion. Recursive step reduces the problem. Call stack stores waiting calls.',
            'manipulate': {
            'prompt': 'Write a recursive function factorial(n).',
            'answer': 'def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)',
            'hint': 'Base case: n == 0 returns 1. Step: n * factorial(n-1).',
            'interaction_kind': 'code_build'
        },
            'predict': {
            'prompt': 'What does this print?\ndef f(n):\n    if n == 0: return\n    print(n)\n    f(n-1)\nf(3)',
            'answer': '3 2 1',
            'options': ['3 2 1', '1 2 3', '3', 'Error'],
            'interaction_kind': 'trace_challenge'
        },
            'build': {
            'prompt': 'Write a recursive function fibonacci(n) that returns the nth Fibonacci number.',
            'answer': 'def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)',
            'explanation': 'Base cases: 0 and 1. Step: sum of two previous numbers.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'A student writes factorial(n) without a base case. What happens?',
            'common_mistake': 'Infinite recursion until stack overflow.',
            'correct_reasoning': 'Without a base case, recursion never stops.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: def factorial(n): return n * factorial(n-1)',
            'correct_reasoning': 'Add base case: if n == 0: return 1.',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'What are the two parts of a recursive function?',
            'answer': 'Base case and recursive step',
            'alternative': ['base case', 'recursive case'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Write a recursive function sum_digits(n) that returns the sum of digits of n.',
            'answer': 'def sum_digits(n):\n    if n == 0:\n        return 0\n    return n % 10 + sum_digits(n // 10)',
            'explanation': 'Base case: n == 0 returns 0. Step: last digit + sum of remaining.',
            'interaction_kind': 'code_build'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'What is the base case for factorial?',
            'answer': 'n == 0 returns 1',
            'options': ['n == 1 returns 1', 'n == 0 returns 1', 'n < 0 returns 0', 'No base case needed'],
            'explanation': 'factorial(0) = 1 by definition.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'What happens if a recursive function has no base case?',
            'answer': 'Stack overflow',
            'options': ['Returns 0', 'Stack overflow', 'Returns None', 'Runs once'],
            'explanation': 'Infinite recursion exhausts the call stack.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'Write a recursive function that reverses a string.',
            'answer_format': 'text',
            'correct': 'def reverse(s):\n    if len(s) <= 1:\n        return s\n    return reverse(s[1:]) + s[0]',
            'explanation': 'Base case: empty or single char. Step: reverse rest + first char.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_recursion', 'tcs_recursion_questions'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: Write a recursive function to compute GCD.',
            'answer_format': 'text',
            'correct': 'def gcd(a, b):\n    if b == 0:\n        return a\n    return gcd(b, a % b)',
            'explanation': 'Euclidean algorithm: gcd(a, b) = gcd(b, a mod b).',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'coding_loop_boundary_error',
            'signature': 'Student writes recursive code without a base case.',
            'reteach_route': 'bug_surgery',
            'reteach_action': 'show_base_case_necessity'
        }, {
            'code': 'coding_complexity_misconception',
            'signature': 'Student thinks recursion is always the best solution.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_iteration_versus_recursion_tradeoffs'
        }],
            'srs_key_points': ['Recursion solves smaller instances of the same problem.', 'Base case stops recursion.', 'Recursive step reduces the problem.', 'Call stack stores waiting calls.', 'Too many calls cause stack overflow.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding',
            'competency_id': 'recursion',
            'unlocks_next': [],
            'tower_badge': 'coding_recursion'
        }
        }

SLUG = 'coding.recursion'
