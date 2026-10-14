"""Lesson module — BFS"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'data-structures.bfs',
            'module_id': 'data-structures.graph.bfs',
            'title': 'BFS',
            'description': 'Breadth-first search explores level by level.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['BFS'],
            'srs_concept_tag': 'data-structures.graph.bfs',
            'domain': 'data-structures',
            'captain_byte': {
            'intro': 'Welcome to BFS. This is a core data-structures concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered BFS. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'BFS',
            'narration': 'Breadth-first search explores level by level.',
            'setting': 'bfs',
            'character': 'Captain Byte',
            'intro_text': 'Breadth-first search explores level by level.'
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
            'srs_key_points': ['BFS'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'data-structures',
            'competency_id': 'bfs',
            'unlocks_next': [],
            'tower_badge': 'data-structures_bfs'
        }
        }

SLUG = 'data-structures.bfs'
