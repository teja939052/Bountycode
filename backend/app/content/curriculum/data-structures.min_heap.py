"""Lesson module — Min Heap"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'data-structures.min_heap',
            'module_id': 'data-structures.heap.min_heap',
            'title': 'Min Heap',
            'description': 'Parent is smaller than children; root is minimum.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Min Heap'],
            'srs_concept_tag': 'data-structures.heap.min_heap',
            'domain': 'data-structures',
            'captain_byte': {
            'intro': 'Welcome to Min Heap. This is a core data-structures concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Min Heap. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Min Heap',
            'narration': 'Parent is smaller than children; root is minimum.',
            'setting': 'min_heap',
            'character': 'Captain Byte',
            'intro_text': 'Parent is smaller than children; root is minimum.'
        },
            'steps': {

        },
            'practice': [],
            'proof': [],
            'company_variants': [],
            'misconceptions': [{
            'code': 'coding_array_index_error',
            'signature': 'Student mishandles pointers/indices in data structure operations.',
            'reteach_route': 'bug_surgery',
            'reteach_action': 'show_array_index_visual'
        }],
            'srs_key_points': ['Min Heap'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'data-structures',
            'competency_id': 'min_heap',
            'unlocks_next': [],
            'tower_badge': 'data-structures_min_heap'
        }
        }

SLUG = 'data-structures.min_heap'
