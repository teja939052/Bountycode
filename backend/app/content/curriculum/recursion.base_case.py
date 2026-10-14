"""Lesson module — Base Case"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'recursion.base_case',
            'module_id': 'recursion.base.base_case',
            'title': 'Base Case',
            'description': 'The stopping condition that ends recursion.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Base Case'],
            'srs_concept_tag': 'recursion.base.base_case',
            'domain': 'recursion',
            'captain_byte': {
            'intro': 'Welcome to Base Case. This is a core recursion concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Base Case. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Base Case',
            'narration': 'The stopping condition that ends recursion.',
            'setting': 'base_case',
            'character': 'Captain Byte',
            'intro_text': 'The stopping condition that ends recursion.'
        },
            'steps': {

        },
            'practice': [],
            'proof': [],
            'company_variants': [],
            'misconceptions': [{
            'code': 'coding_loop_boundary_error',
            'signature': 'Student forgets the base case or misjudges recursion depth.',
            'reteach_route': 'bug_surgery',
            'reteach_action': 'show_loop_boundary'
        }],
            'srs_key_points': ['Base Case'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'recursion',
            'competency_id': 'base_case',
            'unlocks_next': [],
            'tower_badge': 'recursion_base_case'
        }
        }

SLUG = 'recursion.base_case'
