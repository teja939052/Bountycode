"""Lesson module — Simple & Compound Interest"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'aptitude.interest',
            'module_id': 'aptitude.interest',
            'title': 'Simple & Compound Interest',
            'description': 'Simple and compound interest appear frequently in TCS, Infosys, and Wipro quantitative sections.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Interest'],
            'srs_concept_tag': 'aptitude.interest',
            'domain': 'aptitude',
            'captain_byte': {
            'intro': 'Interest is money on money. Simple interest grows linearly. Compound interest grows exponentially.',
            'correct': ['Right formula.', 'Correct compounding.', 'Right time conversion.'],
            'wrong': ['Simple interest = P × R × T / 100.', 'Compound interest uses (1 + R/100)^n.', 'Convert months to years before applying the rate.'],
            'after_break': 'You found the interest error. Now fix the formula or time unit.',
            'after_mastery': "You can now solve interest problems. That's placement-ready quant skill.",
            'retry_prompt': 'Try again. Write the formula before calculating.'
        },
            'story_context': {
            'title': 'Simple & Compound Interest',
            'narration': 'Simple and compound interest appear frequently in TCS, Infosys, and Wipro quantitative sections.',
            'setting': 'interest',
            'character': 'Captain Byte',
            'intro_text': 'Simple and compound interest appear frequently in TCS, Infosys, and Wipro quantitative sections.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'transform'],
            'steps': [{
            'action': 'see_simple',
            'narration': '₹1000 at 10% simple interest for 2 years earns ₹200 interest.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What is the simple interest?',
            'options': [{
            'id': 'a',
            'text': '200',
            'correct': True
        }, {
            'id': 'b',
            'text': '100',
            'correct': False
        }, {
            'id': 'c',
            'text': '220',
            'correct': False
        }, {
            'id': 'd',
            'text': '1200',
            'correct': False
        }],
            'explanation': 'SI = 1000 × 10 × 2 / 100 = 200.'
        }
        }, {
            'action': 'see_compound',
            'narration': '₹1000 at 10% compound interest for 2 years becomes ₹1210.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What is the amount after 2 years?',
            'options': [{
            'id': 'a',
            'text': '1210',
            'correct': True
        }, {
            'id': 'b',
            'text': '1200',
            'correct': False
        }, {
            'id': 'c',
            'text': '1100',
            'correct': False
        }, {
            'id': 'd',
            'text': '1220',
            'correct': False
        }],
            'explanation': 'A = 1000 × (1.1)^2 = 1210.'
        }
        }],
            'conclusion': 'Simple interest = P×R×T/100. Compound interest = P(1+R/100)^n. Convert time units to years.'
        },
            'understand': 'Simple interest is calculated on the original principal. Compound interest is calculated on the accumulated amount. CI = A - P. Time must be in years; months must be divided by 12.',
            'manipulate': {
            'prompt': 'Find SI on ₹5000 at 12% for 3 years.',
            'answer': '1800',
            'hint': 'SI = 5000 × 12 × 3 / 100.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'What is CI on ₹2000 at 10% for 2 years?',
            'answer': '420',
            'options': ['400', '420', '440', '460'],
            'interaction_kind': 'numeric_input'
        },
            'build': {
            'prompt': 'A sum doubles in 5 years at simple interest. Find the rate.',
            'answer': '20',
            'explanation': 'If SI = P, then P = P × R × 5 / 100 → R = 20%.',
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': 'A student computes CI on ₹1000 at 10% for 2 years as ₹200. What is wrong?',
            'common_mistake': 'Using simple interest formula for compound interest.',
            'correct_reasoning': 'CI = P(1+R/100)^n - P = 1000 × 1.21 - 1000 = 210.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: CI = P × R × T / 100.',
            'correct_reasoning': 'Use A = P(1 + R/100)^n, then CI = A - P.',
            'interaction_kind': 'formula_fix'
        },
            'retrieval': {
            'prompt': 'What is the formula for compound interest?',
            'answer': 'A = P(1 + R/100)^n',
            'alternative': ['amount formula', 'CI = A - P'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Find the difference between CI and SI on ₹1000 at 10% for 2 years.',
            'answer': '10',
            'explanation': 'SI = 200, CI = 210. Difference = 10.',
            'interaction_kind': 'numeric_input'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'SI on ₹2000 at 5% for 4 years?',
            'answer': '400',
            'options': ['200', '400', '500', '800'],
            'explanation': '2000 × 5 × 4 / 100 = 400.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'CI on ₹1000 at 10% for 2 years?',
            'answer': '210',
            'options': ['200', '210', '220', '230'],
            'explanation': 'A = 1000 × 1.1^2 = 1210. CI = 1210 - 1000 = 210.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'A sum becomes ₹2420 in 2 years at compound interest. If the rate is 10%, find the principal.',
            'answer_format': 'numeric',
            'correct': '2000',
            'explanation': 'P × (1.1)^2 = 2420 → P = 2420 / 1.21 = 2000.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_si_ci', 'tcs_installments'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: The difference between CI and SI on ₹1000 at 10% for 2 years is?',
            'answer_format': 'numeric',
            'correct': '10',
            'explanation': 'CI - SI = P(R/100)^2 for 2 years.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'apt_rate_work_relationship',
            'signature': 'Student computes compound interest with simple interest formula.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_year_by_year_growth'
        }, {
            'code': 'apt_rate_work_relationship',
            'signature': 'Student uses months as years without converting the rate.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_time_unit_conversion'
        }],
            'srs_key_points': ['SI = P × R × T / 100.', 'CI = P(1 + R/100)^n - P.', 'Amount = P(1 + R/100)^n.', 'Convert months to years: months / 12.', 'For 2 years, CI - SI = P(R/100)^2.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'aptitude',
            'competency_id': 'interest',
            'unlocks_next': [],
            'tower_badge': 'aptitude_interest'
        }
        }

SLUG = 'aptitude.interest'
