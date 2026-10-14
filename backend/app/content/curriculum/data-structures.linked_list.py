"""Lesson module — Linked List"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'data-structures.linked_list',
            'module_id': 'data-structures.linked-list.linked_list',
            'title': 'Linked List',
            'description': 'Nodes connected by pointers; O(1) insert/delete at head.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Linked List'],
            'srs_concept_tag': 'data-structures.linked-list.linked_list',
            'domain': 'data-structures',
            'captain_byte': {
            'intro': 'Welcome to Linked List. This is a core data-structures concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Linked List. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Linked List',
            'narration': 'Nodes connected by pointers; O(1) insert/delete at head.',
            'setting': 'linked_list',
            'character': 'Captain Byte',
            'intro_text': 'Nodes connected by pointers; O(1) insert/delete at head.'
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
            'srs_key_points': ['Linked List'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'data-structures',
            'competency_id': 'linked_list',
            'unlocks_next': [],
            'tower_badge': 'data-structures_linked_list'
        }
        }

SLUG = 'data-structures.linked_list'
