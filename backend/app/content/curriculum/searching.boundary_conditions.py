"""Lesson module — Boundary Conditions"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'searching.boundary_conditions',
            'module_id': 'searching.binary.boundary_conditions',
            'title': 'Boundary Conditions',
            'description': 'Handle empty, single-item, and missing-target cases.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Boundary Conditions'],
            'srs_concept_tag': 'searching.binary.boundary_conditions',
            'domain': 'searching',
            'captain_byte': {
            'intro': 'Welcome to Boundary Conditions. This is a core searching concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Boundary Conditions. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Boundary Conditions',
            'narration': 'Handle empty, single-item, and missing-target cases.',
            'setting': 'boundary_conditions',
            'character': 'Captain Byte',
            'intro_text': 'Handle empty, single-item, and missing-target cases.'
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
            'srs_key_points': ['Boundary Conditions'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'searching',
            'competency_id': 'boundary_conditions',
            'unlocks_next': [],
            'tower_badge': 'searching_boundary_conditions'
        }
        }

SLUG = 'searching.boundary_conditions'
