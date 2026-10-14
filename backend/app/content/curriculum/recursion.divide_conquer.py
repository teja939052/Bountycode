"""Lesson module — Divide and Conquer"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'recursion.divide_conquer',
            'module_id': 'recursion.divide.divide_conquer',
            'title': 'Divide and Conquer',
            'description': 'Split problem, solve subproblems, combine results.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Divide and Conquer'],
            'srs_concept_tag': 'recursion.divide.divide_conquer',
            'domain': 'recursion',
            'captain_byte': {
            'intro': 'Welcome to Divide and Conquer. This is a core recursion concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Divide and Conquer. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Divide and Conquer',
            'narration': 'Split problem, solve subproblems, combine results.',
            'setting': 'divide_and_conquer',
            'character': 'Captain Byte',
            'intro_text': 'Split problem, solve subproblems, combine results.'
        },
            'steps': {

        },
            'practice': [],
            'proof': [],
            'company_variants': [],
            'misconceptions': [{
            'code': 'coding_loop_boundary_error',
            'signature': 'Student forgets the base case or misjudges recursion depth.',
            'reteach_route': 'bug_surgery',
            'reteach_action': 'show_loop_boundary'
        }],
            'srs_key_points': ['Divide and Conquer'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'recursion',
            'competency_id': 'divide_and_conquer',
            'unlocks_next': [],
            'tower_badge': 'recursion_divide_and_conquer'
        }
        }

SLUG = 'recursion.divide_conquer'
