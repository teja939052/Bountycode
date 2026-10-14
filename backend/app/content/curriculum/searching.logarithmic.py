"""Lesson module — Logarithmic Thinking"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'searching.logarithmic',
            'module_id': 'searching.binary.logarithmic',
            'title': 'Logarithmic Thinking',
            'description': 'Each step eliminates half the possibilities.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Logarithmic Thinking'],
            'srs_concept_tag': 'searching.binary.logarithmic',
            'domain': 'searching',
            'captain_byte': {
            'intro': 'Welcome to Logarithmic Thinking. This is a core searching concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Logarithmic Thinking. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Logarithmic Thinking',
            'narration': 'Each step eliminates half the possibilities.',
            'setting': 'logarithmic_thinking',
            'character': 'Captain Byte',
            'intro_text': 'Each step eliminates half the possibilities.'
        },
            'steps': {

        },
            'practice': [],
            'proof': [],
            'company_variants': [],
            'misconceptions': [{
            'code': 'coding_state_trace_error',
            'signature': 'Student loses track of index boundaries during search.',
            'reteach_route': 'visual_state',
            'reteach_action': 'trace_state_step_by_step'
        }],
            'srs_key_points': ['Logarithmic Thinking'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'searching',
            'competency_id': 'logarithmic_thinking',
            'unlocks_next': [],
            'tower_badge': 'searching_logarithmic_thinking'
        }
        }

SLUG = 'searching.logarithmic'
