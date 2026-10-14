"""Lesson module — Logarithms"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'aptitude.logarithms',
            'module_id': 'aptitude.logarithms',
            'title': 'Logarithms',
            'description': 'Logarithms simplify large multiplications and appear in algorithmic complexity and quantitative sections.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Logarithms'],
            'srs_concept_tag': 'aptitude.logarithms',
            'domain': 'aptitude',
            'captain_byte': {
            'intro': "A logarithm answers: 'What power of the base gives this number?'",
            'correct': ['Right base.', 'Correct log rule.', 'Right power.'],
            'wrong': ['log_b(x) asks: b^? = x.', 'Keep the base consistent.', 'log(xy) = log x + log y.'],
            'after_break': 'You found the log error. Now fix the base or rule.',
            'after_mastery': "You can now use logarithms. That's placement-ready quant skill.",
            'retry_prompt': 'Try again. Write the definition before applying rules.'
        },
            'story_context': {
            'title': 'Logarithms',
            'narration': 'Logarithms simplify large multiplications and appear in algorithmic complexity and quantitative sections.',
            'setting': 'logarithms',
            'character': 'Captain Byte',
            'intro_text': 'Logarithms simplify large multiplications and appear in algorithmic complexity and quantitative sections.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'transform'],
            'steps': [{
            'action': 'see_definition',
            'narration': 'log2(8) = 3 because 2^3 = 8.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What is log10(1000)?',
            'options': [{
            'id': 'a',
            'text': '2',
            'correct': False
        }, {
            'id': 'b',
            'text': '3',
            'correct': True
        }, {
            'id': 'c',
            'text': '10',
            'correct': False
        }, {
            'id': 'd',
            'text': '1000',
            'correct': False
        }],
            'explanation': '10^3 = 1000, so log10(1000) = 3.'
        }
        }, {
            'action': 'see_rule',
            'narration': 'log(10 × 100) = log 10 + log 100 = 1 + 2 = 3.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'log(2 × 8) with base 2?',
            'options': [{
            'id': 'a',
            'text': '3',
            'correct': True
        }, {
            'id': 'b',
            'text': '4',
            'correct': False
        }, {
            'id': 'c',
            'text': '2',
            'correct': False
        }, {
            'id': 'd',
            'text': '1',
            'correct': False
        }],
            'explanation': 'log2(2) + log2(8) = 1 + 3 = 4? Wait: 2×8=16, log2(16)=4.'
        }
        }],
            'conclusion': 'log_b(x) asks what power of b gives x. log(xy) = log x + log y. log(x/y) = log x - log y.'
        },
            'understand': 'log_b(x) = y means b^y = x. Common bases: base 10, base e, base 2. Rules: log(xy) = log x + log y. log(x/y) = log x - log y. log(x^n) = n log x.',
            'manipulate': {
            'prompt': 'Compute log2(32).',
            'answer': '5',
            'hint': '2^5 = 32.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'If log10(x) = 3, what is x?',
            'answer': '1000',
            'options': ['10', '100', '1000', '10000'],
            'interaction_kind': 'numeric_input'
        },
            'build': {
            'prompt': 'Simplify: log(100) + log(10) - log(2).',
            'answer': 'log(500)',
            'explanation': 'log(100) + log(10) = log(1000). log(1000) - log(2) = log(500).',
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': 'A student computes log(6) as log(2) + log(3) = 1 + 1.5 = 2.5. What is wrong?',
            'common_mistake': 'Using wrong base or incorrect log values.',
            'correct_reasoning': 'log(2) ≈ 0.301, log(3) ≈ 0.477. Sum ≈ 0.778, not 2.5.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: log(2) + log(3) = 2.5.',
            'correct_reasoning': 'Use correct base and values: log10(2) + log10(3) ≈ 0.778.',
            'interaction_kind': 'formula_fix'
        },
            'retrieval': {
            'prompt': 'What does log_b(x) mean?',
            'answer': 'The power of b that gives x',
            'alternative': ['b^y = x'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'If log2(x) = 6, what is x?',
            'answer': '64',
            'explanation': '2^6 = 64.',
            'interaction_kind': 'numeric_input'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'log10(100) = ?',
            'answer': '2',
            'options': ['1', '2', '10', '100'],
            'explanation': '10^2 = 100.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'log2(8) = ?',
            'answer': '3',
            'options': ['2', '3', '4', '8'],
            'explanation': '2^3 = 8.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'Simplify: log(x^2) + log(y^3) - log(xy).',
            'answer_format': 'text',
            'correct': 'log(x y^2)',
            'explanation': 'log(x^2) = 2log x, log(y^3) = 3log y, log(xy) = log x + log y. Sum = log x + 3log y.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_logarithms', 'tcs_log_rules'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: If log2(x) = 5, what is x?',
            'answer_format': 'numeric',
            'correct': '32',
            'explanation': '2^5 = 32.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'apt_rate_work_relationship',
            'signature': 'Student thinks log is the same as root or square root.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_exponent_versus_log'
        }, {
            'code': 'apt_percent_base_confusion',
            'signature': 'Student applies log rules with the wrong base.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_base_consistency'
        }],
            'srs_key_points': ['log_b(x) asks: b^? = x.', 'log(xy) = log x + log y.', 'log(x/y) = log x - log y.', 'log(x^n) = n log x.', 'Keep the base consistent.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'aptitude',
            'competency_id': 'logarithms',
            'unlocks_next': [],
            'tower_badge': 'aptitude_logarithms'
        }
        }

SLUG = 'aptitude.logarithms'
