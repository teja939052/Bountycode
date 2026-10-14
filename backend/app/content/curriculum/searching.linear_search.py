"""Lesson module — Linear Search"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'searching.linear_search',
            'module_id': 'searching.linear.linear_search',
            'title': 'Linear Search',
            'description': 'Check every item one by one.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Linear Search'],
            'srs_concept_tag': 'searching.linear.linear_search',
            'domain': 'searching',
            'captain_byte': {
            'intro': 'Welcome to Linear Search. This is a core searching concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Linear Search. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Linear Search',
            'narration': 'Check every item one by one.',
            'setting': 'linear_search',
            'character': 'Captain Byte',
            'intro_text': 'Check every item one by one.'
        },
            'steps': {
            'discover': {
            'prompt': 'You have a guest list of 20 names. Find Priya without sorting.',
            'question': 'What is the simplest guaranteed way?',
            'options': ['Check each name', 'Guess randomly', 'Start from end', 'Use binary search'],
            'interaction_kind': 'mcq_read'
        },
            'manipulate': {
            'prompt': 'A list has 8 positions, one contains 1. Find the index by checking sequentially.',
            'answer': '0 <= i < 8',
            'hint': 'Increment index by 1 each step and stop when value is 1.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'For a list of length 20 where the target is absent, how many comparisons does linear search make?',
            'answer': '20',
            'options': ['1', '10', '20', 'log(20)'],
            'interaction_kind': 'mcq_bottleneck'
        },
            'build': {
            'prompt': 'Return the index of target in cards, or -1 if missing.',
            'answer': 'for i in range(len(cards)):\n    if cards[i] == target:\n        return i\nreturn -1',
            'explanation': 'Iterate once, return on first match.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'Why does this fail when target is at index 0?\nfor i in range(1, len(cards)):',
            'broken_code': 'for i in range(1, len(cards)):\n    if cards[i] == target:\n        print(i)',
            'expected_failure': 'Starts at 1 and never checks index 0.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the off-by-one that skips the first element.',
            'correct_code': 'for i in range(len(cards)):\n    if cards[i] == target:\n        print(i)\n        break',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'What is the worst-case time complexity of linear search?',
            'answer': 'O(n)',
            'alternative': ['Linear time', 'n checks'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Count how many times target appears in items without using count().',
            'answer': 'count = 0\nfor x in items:\n    if x == target:\n        count += 1\nprint(count)',
            'explanation': 'Same sequential scan, increment a counter instead of returning early.',
            'interaction_kind': 'code_build'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Which loop bound guarantees every element is checked?',
            'answer': 'range(len(cards))',
            'options': ['range(1, len(cards))', 'range(len(cards)-1)', 'range(len(cards)+1)'],
            'explanation': 'Start at 0, stop at len.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }, {
            'kind': 'numeric',
            'prompt': 'If n=50 and target is absent, how many comparisons?',
            'answer': '50',
            'explanation': 'Worst case inspects every element.',
            'difficulty': 'medium',
            'company_tags': ['tcs']
        }],
            'proof': [{
            'id': 'p1-explain_why_linear_search_needs_no_sorte',
            'prompt': 'Explain why linear search needs no sorted input.',
            'answer_format': 'text',
            'correct': 'It compares sequentially and never relies on ordering.',
            'explanation': 'Ordering is irrelevant when you inspect every element.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'coding_state_trace_error',
            'signature': 'Student loses track of index boundaries during search.',
            'reteach_route': 'visual_state',
            'reteach_action': 'trace_state_step_by_step'
        }],
            'srs_key_points': ['Linear search checks every element sequentially.', 'Worst case is O(n); best case is O(1).', 'Use when data is small or unsorted and simplicity matters.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'searching',
            'competency_id': 'linear_search',
            'unlocks_next': [],
            'tower_badge': 'searching_linear_search'
        }
        }

SLUG = 'searching.linear_search'
