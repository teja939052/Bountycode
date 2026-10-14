"""Lesson module — Counting Matches"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'searching.counting',
            'module_id': 'searching.linear.counting',
            'title': 'Counting Matches',
            'description': 'Count how many times a value appears.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Counting Matches'],
            'srs_concept_tag': 'searching.linear.counting',
            'domain': 'searching',
            'captain_byte': {
            'intro': 'Welcome to Counting Matches. This is a core searching concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Counting Matches. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Counting Matches',
            'narration': 'Count how many times a value appears.',
            'setting': 'counting_matches',
            'character': 'Captain Byte',
            'intro_text': 'Count how many times a value appears.'
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
            'srs_key_points': ['Counting Matches'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'searching',
            'competency_id': 'counting_matches',
            'unlocks_next': [],
            'tower_badge': 'searching_counting_matches'
        }
        }

SLUG = 'searching.counting'
