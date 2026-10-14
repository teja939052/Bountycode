"""Lesson module — TCP vs UDP"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'cs_core.tcp_udp',
            'module_id': 'cs_core.networking_basics.tcp_udp',
            'title': 'TCP vs UDP',
            'description': 'Connection-oriented vs connectionless transport.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['TCP vs UDP'],
            'srs_concept_tag': 'cs_core.networking_basics.tcp_udp',
            'domain': 'cs_core',
            'captain_byte': {
            'intro': 'Welcome to TCP vs UDP. This is a core cs_core concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered TCP vs UDP. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'TCP vs UDP',
            'narration': 'Connection-oriented vs connectionless transport.',
            'setting': 'tcp_vs_udp',
            'character': 'Captain Byte',
            'intro_text': 'Connection-oriented vs connectionless transport.'
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
            'srs_key_points': ['TCP vs UDP'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'cs_core',
            'competency_id': 'tcp_vs_udp',
            'unlocks_next': [],
            'tower_badge': 'cs_core_tcp_vs_udp'
        }
        }

SLUG = 'cs_core.tcp_udp'
