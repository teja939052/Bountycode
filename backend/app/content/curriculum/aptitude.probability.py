"""Lesson module — Probability"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'aptitude.probability',
            'module_id': 'aptitude.probability',
            'title': 'Probability',
            'description': 'Probability is fundamental to quantitative aptitude and appears in TCS, Infosys, and Wipro.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Probability'],
            'srs_concept_tag': 'aptitude.probability',
            'domain': 'aptitude',
            'captain_byte': {
            'intro': 'Probability = favorable outcomes / total outcomes. Keep it between 0 and 1.',
            'correct': ['Right count.', 'Correct total.', 'Valid probability.'],
            'wrong': ['Count favorable outcomes only.', 'Total outcomes = all possible results.', 'Probability is between 0 and 1.'],
            'after_break': 'You found the counting error. Now fix the favorable/total split.',
            'after_mastery': "You can now compute probabilities. That's placement-ready quant skill.",
            'retry_prompt': 'Try again. Count favorable and total separately.'
        },
            'story_context': {
            'title': 'Probability',
            'narration': 'Probability is fundamental to quantitative aptitude and appears in TCS, Infosys, and Wipro.',
            'setting': 'probability',
            'character': 'Captain Byte',
            'intro_text': 'Probability is fundamental to quantitative aptitude and appears in TCS, Infosys, and Wipro.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'transform'],
            'steps': [{
            'action': 'see_die',
            'narration': 'A fair die has 6 faces. Probability of 4 is 1/6.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What is P(6) on a fair die?',
            'options': [{
            'id': 'a',
            'text': '1/6',
            'correct': True
        }, {
            'id': 'b',
            'text': '1/5',
            'correct': False
        }, {
            'id': 'c',
            'text': '1/2',
            'correct': False
        }, {
            'id': 'd',
            'text': '1',
            'correct': False
        }],
            'explanation': 'One favorable outcome out of 6 total.'
        }
        }, {
            'action': 'see_coin',
            'narration': 'Two coins tossed. Probability of two heads?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'P(HH) for two fair coins?',
            'options': [{
            'id': 'a',
            'text': '1/2',
            'correct': False
        }, {
            'id': 'b',
            'text': '1/3',
            'correct': False
        }, {
            'id': 'c',
            'text': '1/4',
            'correct': True
        }, {
            'id': 'd',
            'text': '1/8',
            'correct': False
        }],
            'explanation': 'HH is 1 of 4 equally likely outcomes.'
        }
        }],
            'conclusion': 'Probability = favorable / total. For multiple events, check independence and mutual exclusivity.'
        },
            'understand': 'Probability = favorable outcomes / total outcomes. Independent events: P(A and B) = P(A) × P(B). Mutually exclusive: P(A or B) = P(A) + P(B). Conditional probability: P(A|B) = P(A and B) / P(B).',
            'manipulate': {
            'prompt': 'A bag has 3 red and 2 blue balls. Probability of red?',
            'answer': '0.6',
            'hint': 'Favorable = 3. Total = 5.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'Two dice rolled. Probability of sum = 7?',
            'answer': '1/6',
            'options': ['1/6', '1/12', '1/36', '5/36'],
            'interaction_kind': 'numeric_input'
        },
            'build': {
            'prompt': 'A box has 5 defective and 15 good items. Probability of picking 2 good items without replacement?',
            'answer': '21/38',
            'explanation': 'First good: 15/20. Second good: 14/19. Multiply: 210/380 = 21/38.',
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': 'A student computes P(A or B) as P(A) + P(B) = 0.6 for overlapping events. What is wrong?',
            'common_mistake': 'Adding probabilities of non-mutually-exclusive events.',
            'correct_reasoning': 'Use P(A or B) = P(A) + P(B) - P(A and B).',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: P(A or B) = P(A) + P(B) for overlapping events.',
            'correct_reasoning': 'Subtract the intersection: P(A or B) = P(A) + P(B) - P(A and B).',
            'interaction_kind': 'formula_fix'
        },
            'retrieval': {
            'prompt': 'What is the formula for probability?',
            'answer': 'Favorable outcomes / total outcomes',
            'alternative': ['favorable / total'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'A coin is tossed 3 times. Probability of exactly 2 heads?',
            'answer': '3/8',
            'explanation': '3 choose 2 = 3 favorable out of 8 total.',
            'interaction_kind': 'numeric_input'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'A card drawn from 52 cards. P(King)?',
            'answer': '1/13',
            'options': ['1/4', '1/13', '1/52', '4/52'],
            'explanation': '4 kings out of 52 cards = 1/13.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'Two dice rolled. P(sum is prime)?',
            'answer': '5/36',
            'options': ['1/6', '5/36', '1/4', '1/3'],
            'explanation': 'Prime sums: 2,3,5,7,11. Count favorable outcomes.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'A bag has 4 white and 6 black balls. Two drawn without replacement. P(both black)?',
            'answer_format': 'text',
            'correct': '1/3',
            'explanation': 'First black: 6/10. Second black: 5/9. Multiply: 30/90 = 1/3.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_probability', 'tcs_prob_questions'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: A coin tossed 5 times. P(exactly 3 heads)?',
            'answer_format': 'text',
            'correct': '5/16',
            'explanation': '5C3 = 10 favorable out of 32 total = 5/16.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'apt_rate_work_relationship',
            'signature': 'Student computes a probability greater than 1.',
            'reteach_route': 'bug_surgery',
            'reteach_action': 'show_favorable_over_total'
        }, {
            'code': 'apt_rate_work_relationship',
            'signature': 'Student adds probabilities of non-mutually-exclusive events.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_inclusion_exclusion'
        }],
            'srs_key_points': ['Probability = favorable / total.', 'Independent: multiply probabilities.', 'Mutually exclusive: add probabilities.', 'Without replacement: update total after each draw.', 'Probability is between 0 and 1.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'aptitude',
            'competency_id': 'probability',
            'unlocks_next': [],
            'tower_badge': 'aptitude_probability'
        }
        }

SLUG = 'aptitude.probability'
