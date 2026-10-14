"""Lesson module — Directions"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'reasoning.directions',
            'module_id': 'reasoning.directions',
            'title': 'Directions',
            'description': 'Direction sense is a high-frequency reasoning topic in TCS NQT, Infosys, and Wipro. It tests spatial rotation under time pressure.',
            'difficulty': 'easy',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Directions'],
            'srs_concept_tag': 'reasoning.directions',
            'domain': 'reasoning',
            'captain_byte': {
            'intro': 'Direction problems are just rotations. Start from a facing, then turn left or right by 90 degrees.',
            'correct': ['Correct turn.', 'You rotated the facing right.', 'Right direction.'],
            'wrong': ['Rotate from the current facing, not from north.', 'Left/right depends on the current direction.', 'Draw the turn before answering.'],
            'after_break': 'You found the rotation error. Now fix the facing and re-turn.',
            'after_mastery': "You can now track any walk with turns. That's placement-ready direction sense.",
            'retry_prompt': 'Try again. Update the facing after every turn.'
        },
            'story_context': {
            'title': 'Directions',
            'narration': 'Direction sense is a high-frequency reasoning topic in TCS NQT, Infosys, and Wipro. It tests spatial rotation under time pressure.',
            'setting': 'directions',
            'character': 'Captain Byte',
            'intro_text': 'Direction sense is a high-frequency reasoning topic in TCS NQT, Infosys, and Wipro. It tests spatial rotation under time pressure.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'transform', 'compare'],
            'steps': [{
            'action': 'see_facing',
            'narration': 'A man faces north. He turns 90 degrees right. Which way does he face?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Facing north, turn right 90 degrees. New facing?',
            'options': [{
            'id': 'a',
            'text': 'East',
            'correct': True
        }, {
            'id': 'b',
            'text': 'West',
            'correct': False
        }, {
            'id': 'c',
            'text': 'South',
            'correct': False
        }, {
            'id': 'd',
            'text': 'North',
            'correct': False
        }],
            'explanation': 'Right from north is east.'
        }
        }, {
            'action': 'see_turn_chain',
            'narration': 'Facing north → right → right → left. Final facing?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'N → right → right → left. Final facing?',
            'options': [{
            'id': 'a',
            'text': 'East',
            'correct': True
        }, {
            'id': 'b',
            'text': 'North',
            'correct': False
        }, {
            'id': 'c',
            'text': 'West',
            'correct': False
        }, {
            'id': 'd',
            'text': 'South',
            'correct': False
        }],
            'explanation': 'N → E → S → E.'
        }
        }],
            'conclusion': 'Track the current facing after every turn. Left and right are relative to current facing, not fixed north.'
        },
            'understand': 'Start from a facing direction. A left turn subtracts 90 degrees. A right turn adds 90 degrees. After multiple turns, update the facing each time. Final position and facing are determined by the net turn.',
            'manipulate': {
            'prompt': 'A woman faces south. She turns 180 degrees. Which way does she face?',
            'answer': 'North',
            'hint': '180 degrees reverses the direction.',
            'interaction_kind': 'mcq_classify'
        },
            'predict': {
            'prompt': 'A boy walks 10 km north, turns right, walks 5 km, turns left, walks 10 km. Where is he relative to start?',
            'answer': 'North',
            'options': ['North', 'South', 'East', 'West'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': 'A man walks 5 km east, turns 135 degrees right, walks 5 km. Find his final facing and displacement direction.',
            'answer': 'South-East',
            'explanation': 'East + right 135° = South-East direction.',
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': 'A student says facing north + right turn = west. What is wrong?',
            'common_mistake': 'Mirroring left/right instead of rotating from current facing.',
            'correct_reasoning': 'Right from north is east. Right from east is south.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the turn sequence: north → right = west.',
            'correct_reasoning': 'Right from north is east, not west.',
            'interaction_kind': 'mcq_diagnose'
        },
            'retrieval': {
            'prompt': 'What is the result of facing north and turning 180 degrees?',
            'answer': 'South',
            'alternative': ['opposite direction', 'reverse'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'A dog runs 20m east, turns left, runs 30m, turns right, runs 15m. Which direction is the dog facing now?',
            'answer': 'East',
            'explanation': 'Start east. Left turn → north. Right turn → east.',
            'interaction_kind': 'mcq_classify'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Facing west, turn left. New facing?',
            'answer': 'South',
            'options': ['North', 'South', 'East', 'West'],
            'explanation': 'Left from west is south.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'A man faces north, turns 270 degrees right. Final facing?',
            'answer': 'West',
            'options': ['North', 'East', 'South', 'West'],
            'explanation': '3 right turns from north = west.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'A woman walks 15m north, turns left 90 degrees, walks 20m, turns right 90 degrees, walks 10m. Which direction is she facing?',
            'answer_format': 'text',
            'correct': 'north',
            'explanation': 'N → left → W → right → N.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_direction_shadow', 'tcs_direction_sun'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: A man faces east, turns 225 degrees clockwise. Final facing?',
            'answer_format': 'text',
            'correct': 'south-west',
            'explanation': '225° clockwise from east = south-west.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'reasoning_ordering_error',
            'signature': 'Student mirrors left/right instead of rotating with the facing direction.',
            'reteach_route': 'time_travel',
            'reteach_action': 'step_through_facing_rotation'
        }, {
            'code': 'reasoning_ordering_error',
            'signature': 'Student confuses north/south when turning from east or west.',
            'reteach_route': 'visual_state',
            'reteach_action': 'show_cardinal_rotation'
        }],
            'srs_key_points': ['Left turn = -90°. Right turn = +90°.', 'Update facing after every turn.', '180° reverses direction.', '270° right = 90° left.', 'Relative directions depend on current facing, not fixed north.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'reasoning',
            'competency_id': 'directions',
            'unlocks_next': [],
            'tower_badge': 'reasoning_directions'
        }
        }

SLUG = 'reasoning.directions'
