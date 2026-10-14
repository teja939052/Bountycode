"""Lesson module — Speed, Distance & Time"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'aptitude.speed_distance_time',
            'module_id': 'aptitude.speed_distance_time',
            'title': 'Speed, Distance & Time',
            'description': 'Speed, distance, and time are core quantitative topics tested in TCS, Infosys, and Wipro. The formulas are simple; the trap is unit conversion and relative speed.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Speed Distance Time'],
            'srs_concept_tag': 'aptitude.speed_distance_time',
            'domain': 'aptitude',
            'captain_byte': {
            'intro': 'Speed = distance / time. Relative speed changes when objects move toward or away from each other.',
            'correct': ['Right formula.', 'Correct relative speed.', 'Right unit conversion.'],
            'wrong': ['Average speed is not the mean of speeds.', 'Toward each other: add speeds. Same direction: subtract.', 'Keep units consistent.'],
            'after_break': 'You found the speed error. Now fix the formula or relative-speed direction.',
            'after_mastery': "You can now solve speed-distance-time problems. That's placement-ready quant skill.",
            'retry_prompt': 'Try again. Write the formula before calculating.'
        },
            'story_context': {
            'title': 'Speed, Distance & Time',
            'narration': 'Speed, distance, and time are core quantitative topics tested in TCS, Infosys, and Wipro. The formulas are simple; the trap is unit conversion and relative speed.',
            'setting': 'speed_distance_time',
            'character': 'Captain Byte',
            'intro_text': 'Speed, distance, and time are core quantitative topics tested in TCS, Infosys, and Wipro. The formulas are simple; the trap is unit conversion and relative speed.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'transform'],
            'steps': [{
            'action': 'see_formula',
            'narration': 'A car travels 120 km in 2 hours. What is its speed?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Speed = ?',
            'options': [{
            'id': 'a',
            'text': '60 km/h',
            'correct': True
        }, {
            'id': 'b',
            'text': '120 km/h',
            'correct': False
        }, {
            'id': 'c',
            'text': '2 km/h',
            'correct': False
        }, {
            'id': 'd',
            'text': '240 km/h',
            'correct': False
        }],
            'explanation': 'Speed = distance / time = 120 / 2 = 60 km/h.'
        }
        }, {
            'action': 'see_relative',
            'narration': 'Two trains move toward each other at 40 km/h and 60 km/h. Closing speed?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What is their closing speed?',
            'options': [{
            'id': 'a',
            'text': '100 km/h',
            'correct': True
        }, {
            'id': 'b',
            'text': '20 km/h',
            'correct': False
        }, {
            'id': 'c',
            'text': '50 km/h',
            'correct': False
        }, {
            'id': 'd',
            'text': '40 km/h',
            'correct': False
        }],
            'explanation': 'Toward each other: add speeds. 40 + 60 = 100 km/h.'
        }
        }],
            'conclusion': 'Speed = distance / time. Average speed = total distance / total time. Relative speed adds toward each other, subtracts same direction.'
        },
            'understand': 'Speed = distance / time. Average speed is total distance divided by total time, not the arithmetic mean of speeds. Relative speed toward each other adds; same direction subtracts.',
            'manipulate': {
            'prompt': 'A man walks 10 km at 5 km/h and returns 10 km at 4 km/h. What is his average speed?',
            'answer': '4.44',
            'hint': 'Total distance = 20 km. Total time = 10/5 + 10/4 = 2 + 2.5 = 4.5 h. Average = 20 / 4.5.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'Two trains 200 km apart move toward each other at 50 km/h and 30 km/h. When do they meet?',
            'answer': '2.5',
            'options': ['2', '2.5', '3', '4'],
            'interaction_kind': 'numeric_input'
        },
            'build': {
            'prompt': 'A boat goes 30 km downstream in 3 hours and returns in 5 hours. Find the stream speed if still-water speed is 12 km/h.',
            'answer': '3',
            'explanation': 'Downstream speed = 10 km/h. Upstream speed = 6 km/h. Stream = (10 - 6)/2 = 2. Wait: still water = (down+up)/2 = 8. Stream = (down-up)/2 = 2.',
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': 'A student computes average speed as (40 + 60) / 2 = 50 km/h for equal distances. What is wrong?',
            'common_mistake': 'Using arithmetic mean instead of total distance / total time.',
            'correct_reasoning': 'Average speed = total distance / total time. For equal distances, harmonic mean applies.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: average speed = (speed1 + speed2) / 2.',
            'correct_reasoning': 'Use total distance / total time.',
            'interaction_kind': 'formula_fix'
        },
            'retrieval': {
            'prompt': 'What is the formula for average speed?',
            'answer': 'Total distance / total time',
            'alternative': ['not the mean of speeds'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'A plane flies 600 km with a 40 km/h tailwind and returns against it. Still-air speed is 160 km/h. Find total time.',
            'answer': '7.5',
            'explanation': 'With wind: 200 km/h → 3 h. Against wind: 120 km/h → 5 h. Total = 8 h.',
            'interaction_kind': 'numeric_input'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'A car covers 240 km in 4 hours. Speed?',
            'answer': '60 km/h',
            'options': ['40', '60', '80', '100'],
            'explanation': '240 / 4 = 60.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'Two trains 300 km apart move toward each other at 60 and 40 km/h. Meeting time?',
            'answer': '3',
            'options': ['2', '3', '4', '5'],
            'explanation': 'Closing speed = 100 km/h. Time = 300 / 100 = 3 h.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'A bus travels 150 km at 50 km/h and returns at 30 km/h. Find the average speed.',
            'answer_format': 'numeric',
            'correct': '37.5',
            'explanation': 'Total distance = 300 km. Total time = 3 + 5 = 8 h. Average = 300 / 8 = 37.5 km/h.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_sdt_boats', 'tcs_sdt_trains'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: A train passes a pole in 12 seconds and a platform 300m long in 27 seconds. Find train length.',
            'answer_format': 'numeric',
            'correct': '240',
            'explanation': 'Let length = L. Speed = L/12. (L+300)/speed = 27. Solve: L = 240m.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'apt_rate_work_relationship',
            'signature': 'Student averages speeds instead of using total distance / total time.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_weighted_by_time'
        }, {
            'code': 'apt_rate_work_relationship',
            'signature': 'Student adds speeds when objects move toward each other.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_approach_versus_separation'
        }],
            'srs_key_points': ['Speed = distance / time.', 'Average speed = total distance / total time.', 'Toward each other: add speeds. Same direction: subtract.', 'Stream speed = (downstream - upstream) / 2.', 'Keep units consistent.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'aptitude',
            'competency_id': 'speed_distance_time',
            'unlocks_next': [],
            'tower_badge': 'aptitude_speed_distance_time'
        }
        }

SLUG = 'aptitude.speed_distance_time'
