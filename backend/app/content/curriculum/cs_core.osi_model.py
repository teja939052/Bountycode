"""Lesson module — OSI Model"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'cs_core.osi_model',
            'module_id': 'cs_core.networking_basics.osi_model',
            'title': 'OSI Model',
            'description': 'Seven layers from physical to application.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['OSI Model'],
            'srs_concept_tag': 'cs_core.networking_basics.osi_model',
            'domain': 'cs_core',
            'captain_byte': {
            'intro': 'Welcome to OSI Model. This is a core cs_core concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered OSI Model. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'OSI Model',
            'narration': 'Seven layers from physical to application.',
            'setting': 'osi_model',
            'character': 'Captain Byte',
            'intro_text': 'Seven layers from physical to application.'
        },
            'steps': {

        },
            'practice': [],
            'proof': [],
            'company_variants': [],
            'misconceptions': [{
            'code': 'cs_core_process_thread_confusion',
            'signature': 'Student confuses related cs_core concepts.',
            'reteach_route': 'visual_state',
            'reteach_action': 'trace_state_step_by_step'
        }],
            'srs_key_points': ['OSI Model'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'cs_core',
            'competency_id': 'osi_model',
            'unlocks_next': [],
            'tower_badge': 'cs_core_osi_model'
        }
        }

SLUG = 'cs_core.osi_model'
