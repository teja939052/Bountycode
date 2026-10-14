"""Lesson module — Queue"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'data-structures.queue',
            'module_id': 'data-structures.queue.queue',
            'title': 'Queue',
            'description': 'FIFO structure; enqueue at back, dequeue at front.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Queue'],
            'srs_concept_tag': 'data-structures.queue.queue',
            'domain': 'data-structures',
            'captain_byte': {
            'intro': 'Welcome to Queue. This is a core data-structures concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Queue. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Queue',
            'narration': 'FIFO structure; enqueue at back, dequeue at front.',
            'setting': 'queue',
            'character': 'Captain Byte',
            'intro_text': 'FIFO structure; enqueue at back, dequeue at front.'
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
            'srs_key_points': ['Queue'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'data-structures',
            'competency_id': 'queue',
            'unlocks_next': [],
            'tower_badge': 'data-structures_queue'
        }
        }

SLUG = 'data-structures.queue'
