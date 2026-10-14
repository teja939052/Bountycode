"""Lesson module — Stack"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'data-structures.stack',
            'module_id': 'data-structures.stack.stack',
            'title': 'Stack',
            'description': 'LIFO structure; push/pop at top.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Stack'],
            'srs_concept_tag': 'data-structures.stack.stack',
            'domain': 'data-structures',
            'captain_byte': {
            'intro': 'Welcome to Stack. This is a core data-structures concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Stack. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Stack',
            'narration': 'LIFO structure; push/pop at top.',
            'setting': 'stack',
            'character': 'Captain Byte',
            'intro_text': 'LIFO structure; push/pop at top.'
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
            'srs_key_points': ['Stack'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'data-structures',
            'competency_id': 'stack',
            'unlocks_next': [],
            'tower_badge': 'data-structures_stack'
        }
        }

SLUG = 'data-structures.stack'
