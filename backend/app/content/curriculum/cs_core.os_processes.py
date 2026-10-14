"""Lesson module — Processes vs Threads"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'cs_core.os_processes',
            'module_id': 'cs_core.os_basics.os_processes',
            'title': 'Processes vs Threads',
            'description': 'Processes are isolated; threads share memory.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Processes vs Threads'],
            'srs_concept_tag': 'cs_core.os_basics.os_processes',
            'domain': 'cs_core',
            'captain_byte': {
            'intro': 'Welcome to Processes vs Threads. This is a core cs_core concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Processes vs Threads. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Processes vs Threads',
            'narration': 'Processes are isolated; threads share memory.',
            'setting': 'processes_vs_threads',
            'character': 'Captain Byte',
            'intro_text': 'Processes are isolated; threads share memory.'
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
            'srs_key_points': ['Processes vs Threads'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'cs_core',
            'competency_id': 'processes_vs_threads',
            'unlocks_next': [],
            'tower_badge': 'cs_core_processes_vs_threads'
        }
        }

SLUG = 'cs_core.os_processes'
