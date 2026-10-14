"""Lesson module — Call Stack"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'recursion.call_stack',
            'module_id': 'recursion.base.call_stack',
            'title': 'Call Stack',
            'description': 'How recursive calls are tracked in memory.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Call Stack'],
            'srs_concept_tag': 'recursion.base.call_stack',
            'domain': 'recursion',
            'captain_byte': {
            'intro': 'Welcome to Call Stack. This is a core recursion concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Call Stack. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Call Stack',
            'narration': 'How recursive calls are tracked in memory.',
            'setting': 'call_stack',
            'character': 'Captain Byte',
            'intro_text': 'How recursive calls are tracked in memory.'
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
            'srs_key_points': ['Call Stack'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'recursion',
            'competency_id': 'call_stack',
            'unlocks_next': [],
            'tower_badge': 'recursion_call_stack'
        }
        }

SLUG = 'recursion.call_stack'
