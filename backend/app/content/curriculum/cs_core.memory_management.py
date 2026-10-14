"""Lesson module — Memory Management"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'cs_core.memory_management',
            'module_id': 'cs_core.os_basics.memory_management',
            'title': 'Memory Management',
            'description': 'Stack vs heap allocation and pointers.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Memory Management'],
            'srs_concept_tag': 'cs_core.os_basics.memory_management',
            'domain': 'cs_core',
            'captain_byte': {
            'intro': 'Welcome to Memory Management. This is a core cs_core concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Memory Management. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Memory Management',
            'narration': 'Stack vs heap allocation and pointers.',
            'setting': 'memory_management',
            'character': 'Captain Byte',
            'intro_text': 'Stack vs heap allocation and pointers.'
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
            'srs_key_points': ['Memory Management'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'cs_core',
            'competency_id': 'memory_management',
            'unlocks_next': [],
            'tower_badge': 'cs_core_memory_management'
        }
        }

SLUG = 'cs_core.memory_management'
