"""Lesson module — Bubble Sort"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'sorting.bubble_sort',
            'module_id': 'sorting.bubble.bubble_sort',
            'title': 'Bubble Sort',
            'description': 'Repeatedly swap adjacent out-of-order elements.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Bubble Sort'],
            'srs_concept_tag': 'sorting.bubble.bubble_sort',
            'domain': 'sorting',
            'captain_byte': {
            'intro': 'Welcome to Bubble Sort. This is a core sorting concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Bubble Sort. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Bubble Sort',
            'narration': 'Repeatedly swap adjacent out-of-order elements.',
            'setting': 'bubble_sort',
            'character': 'Captain Byte',
            'intro_text': 'Repeatedly swap adjacent out-of-order elements.'
        },
            'steps': {

        },
            'practice': [],
            'proof': [],
            'company_variants': [],
            'misconceptions': [{
            'code': 'coding_loop_boundary_error',
            'signature': 'Student mishandles loop boundaries during sorting.',
            'reteach_route': 'bug_surgery',
            'reteach_action': 'show_loop_boundary'
        }],
            'srs_key_points': ['Bubble Sort'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'sorting',
            'competency_id': 'bubble_sort',
            'unlocks_next': [],
            'tower_badge': 'sorting_bubble_sort'
        }
        }

SLUG = 'sorting.bubble_sort'
