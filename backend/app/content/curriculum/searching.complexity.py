"""Lesson module — Worst-Case Complexity"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'searching.complexity',
            'module_id': 'searching.linear.complexity',
            'title': 'Worst-Case Complexity',
            'description': 'Understand how search time grows with input size.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Worst-Case Complexity'],
            'srs_concept_tag': 'searching.linear.complexity',
            'domain': 'searching',
            'captain_byte': {
            'intro': 'Welcome to Worst-Case Complexity. This is a core searching concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Worst-Case Complexity. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Worst-Case Complexity',
            'narration': 'Understand how search time grows with input size.',
            'setting': 'worst-case_complexity',
            'character': 'Captain Byte',
            'intro_text': 'Understand how search time grows with input size.'
        },
            'steps': {

        },
            'practice': [],
            'proof': [],
            'company_variants': [],
            'misconceptions': [{
            'code': 'coding_state_trace_error',
            'signature': 'Student loses track of index boundaries during search.',
            'reteach_route': 'visual_state',
            'reteach_action': 'trace_state_step_by_step'
        }],
            'srs_key_points': ['Worst-Case Complexity'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'searching',
            'competency_id': 'worst-case_complexity',
            'unlocks_next': [],
            'tower_badge': 'searching_worst_case_complexity'
        }
        }

SLUG = 'searching.complexity'
