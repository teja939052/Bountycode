"""Lesson module — Variables — The Named Box"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'coding.variables',
            'module_id': 'coding.variables',
            'title': 'Variables — The Named Box',
            'description': 'Variables are the foundation of every programming language. Understanding assignment, state, and reassignment is prerequisite for all coding interview problems.',
            'difficulty': 'easy',
            'est_minutes': 25,
            'xp_reward': 100,
            'skills_taught': ['Variables'],
            'srs_concept_tag': 'coding.variables',
            'domain': 'coding',
            'captain_byte': {
            'intro': "A variable is a named box in memory. Assignment stores a value; reassignment overwrites it. Let's trace the boxes.",
            'correct': ['Exactly right!', 'You traced it perfectly!', 'Box by box!'],
            'wrong': ['Remember: = is assignment, not equality.', 'Think about what each line leaves in memory.'],
            'after_break': 'Now you see why the output changed.',
            'after_mastery': 'You now think in terms of memory state. This is the foundation of every coding interview.',
            'retry_prompt': 'Trace again. Watch each box.'
        },
            'story_context': {
            'title': 'Variables — The Named Box',
            'narration': 'Variables are the foundation of every programming language. Understanding assignment, state, and reassignment is prerequisite for all coding interview problems.',
            'setting': 'variables',
            'character': 'Captain Byte',
            'intro_text': 'Variables are the foundation of every programming language. Understanding assignment, state, and reassignment is prerequisite for all coding interview problems.'
        },
            'steps': {
            'discover': {
            'prompt': 'Read this code. What does it print?',
            'question': 'x = 5\nprint(x)\nx = 10\nprint(x)',
            'answer': '5\n10',
            'interaction_kind': 'predict_output'
        },
            'understand': {
            'prompt': 'A variable is a named box in memory. = means assignment, not equality. Reassignment overwrites.',
            'explanation': 'x = 5 creates box x with value 5. x = 10 overwrites box x with value 10. The old value 5 is gone.',
            'interaction_kind': 'read_explanation'
        },
            'manipulate': {
            'prompt': 'Trace: a = 5; b = a; a = 10; print(b). What does this print?',
            'answer': '5',
            'hint': 'b stored the value of a when a was 5.',
            'interaction_kind': 'state_trace'
        },
            'predict': {
            'prompt': 'What does this print?\nx = 5\ny = x\nx = 10\nprint(y)',
            'answer': '5',
            'options': ['5', '10', '15', 'Error'],
            'interaction_kind': 'predict_output'
        },
            'build': {
            'prompt': 'Write code to swap two variables using a temporary variable.',
            'answer': 'temp = a\na = b\nb = temp',
            'explanation': "temp holds a's value while a gets b's value, then b gets temp (original a).",
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with this code?\na = 5\nb = 10\na = b\nb = a\nprint(a, b)',
            'broken_code': 'a = 5\nb = 10\na = b\nb = a\nprint(a, b)',
            'expected_failure': 'Both print 10. The swap failed because a was overwritten before b could read it.',
            'interaction_kind': 'break_and_debug'
        },
            'debug': {
            'prompt': 'Fix the swap using a temporary variable.',
            'answer': 'temp = a\na = b\nb = temp',
            'broken_code': 'a = 5\nb = 10\na = b\nb = a',
            'interaction_kind': 'code_debug'
        },
            'retrieval': {
            'prompt': 'What happens when you assign a variable to another variable?',
            'answer': "The value is copied. Later changes to the first variable don't affect the second.",
            'alternative': ['Value is copied, not linked'],
            'interaction_kind': 'recall_check'
        },
            'transfer': {
            'prompt': 'Write code to swap two variables WITHOUT a temporary variable (use arithmetic or tuple unpacking).',
            'answer': 'a = a + b\nb = a - b\na = a - b',
            'alternative': ['a, b = b, a'],
            'explanation': 'Tuple unpacking is Pythonic: a, b = b, a.',
            'interaction_kind': 'code_transfer'
        }
        },
            'practice': [{
            'kind': 'code',
            'prompt': 'What does this print?\nx = 10\ny = x + 5\nprint(y)',
            'answer': '15',
            'explanation': 'y = 10 + 5 = 15.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'Trace and predict output:\na = 3\nb = a\na = a + 2\nprint(b)',
            'answer_format': 'code',
            'correct': '3',
            'explanation': "b stored a's value (3) before a was updated.",
            'time_limit_seconds': 45,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'easy',
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS NQT pattern: What is the output?\nx = 5\ny = x\nx = x + 1\nprint(x, y)',
            'answer_format': 'code',
            'correct': '6 5',
            'explanation': 'y kept the old value 5. x became 6.',
            'time_limit_seconds': 45,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'coding_state_trace_error',
            'signature': 'Student thinks print() returns the printed value.',
            'reteach_route': 'memory_board',
            'reteach_action': 'show_variable_unchanged_after_print'
        }, {
            'code': 'coding_state_trace_error',
            'signature': 'Student thinks source code shows output.',
            'reteach_route': 'visual_state',
            'reteach_action': 'highlight_source_vs_output'
        }],
            'srs_key_points': ['Variable = named box in memory.', '= is assignment, not equality.', 'Reassignment overwrites the old value.', "Assignment copies the current value; later rebinding doesn't rewrite earlier copies.", 'Python tuple unpacking: a, b = b, a for swapping.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding',
            'competency_id': 'variables',
            'unlocks_next': [],
            'tower_badge': 'coding_variables'
        }
        }

SLUG = 'coding.variables'
