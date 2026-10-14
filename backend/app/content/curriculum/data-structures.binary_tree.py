"""Lesson module — Binary Tree"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'data-structures.binary_tree',
            'module_id': 'data-structures.tree.binary_tree',
            'title': 'Binary Tree',
            'description': 'Each node has at most two children.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Binary Tree'],
            'srs_concept_tag': 'data-structures.tree.binary_tree',
            'domain': 'data-structures',
            'captain_byte': {
            'intro': 'Welcome to Binary Tree. This is a core data-structures concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Binary Tree. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Binary Tree',
            'narration': 'Each node has at most two children.',
            'setting': 'binary_tree',
            'character': 'Captain Byte',
            'intro_text': 'Each node has at most two children.'
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
            'srs_key_points': ['Binary Tree'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'data-structures',
            'competency_id': 'binary_tree',
            'unlocks_next': [],
            'tower_badge': 'data-structures_binary_tree'
        }
        }

SLUG = 'data-structures.binary_tree'
