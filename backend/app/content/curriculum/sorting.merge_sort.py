"""Lesson module — Merge Sort"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'sorting.merge_sort',
            'module_id': 'sorting.merge.merge_sort',
            'title': 'Merge Sort',
            'description': 'Divide the list, sort halves, merge back.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Merge Sort'],
            'srs_concept_tag': 'sorting.merge.merge_sort',
            'domain': 'sorting',
            'captain_byte': {
            'intro': 'Welcome to Merge Sort. This is a core sorting concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Merge Sort. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Merge Sort',
            'narration': 'Divide the list, sort halves, merge back.',
            'setting': 'merge_sort',
            'character': 'Captain Byte',
            'intro_text': 'Divide the list, sort halves, merge back.'
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
            'srs_key_points': ['Merge Sort'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'sorting',
            'competency_id': 'merge_sort',
            'unlocks_next': [],
            'tower_badge': 'sorting_merge_sort'
        }
        }

SLUG = 'sorting.merge_sort'
