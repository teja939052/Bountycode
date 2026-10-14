"""Lesson module — Permutations & Combinations"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'aptitude.permutation_combination',
            'module_id': 'aptitude.permutation_combination',
            'title': 'Permutations & Combinations',
            'description': 'Permutations and combinations are core to probability and counting. They appear in TCS, Infosys, and Wipro quantitative sections.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Permutations and Combinations'],
            'srs_concept_tag': 'aptitude.permutation_combination',
            'domain': 'aptitude',
            'captain_byte': {
            'intro': 'Permutation cares about order. Combination does not. Count carefully.',
            'correct': ['Right formula.', 'Correct counting.', 'Right division for identical items.'],
            'wrong': ['Order matters: permutation. Order does not matter: combination.', 'Divide by factorial for identical items.', 'Use nPr when arranging, nCr when selecting.'],
            'after_break': 'You found the counting error. Now fix the formula or division.',
            'after_mastery': "You can now count arrangements and selections. That's placement-ready quant skill.",
            'retry_prompt': 'Try again. Ask: does order matter?'
        },
            'story_context': {
            'title': 'Permutations & Combinations',
            'narration': 'Permutations and combinations are core to probability and counting. They appear in TCS, Infosys, and Wipro quantitative sections.',
            'setting': 'permutations_and_combinations',
            'character': 'Captain Byte',
            'intro_text': 'Permutations and combinations are core to probability and counting. They appear in TCS, Infosys, and Wipro quantitative sections.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'transform'],
            'steps': [{
            'action': 'see_permutation',
            'narration': 'Arrange 3 books on a shelf. How many orders?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'How many arrangements of 3 books?',
            'options': [{
            'id': 'a',
            'text': '3',
            'correct': False
        }, {
            'id': 'b',
            'text': '6',
            'correct': True
        }, {
            'id': 'c',
            'text': '9',
            'correct': False
        }, {
            'id': 'd',
            'text': '1',
            'correct': False
        }],
            'explanation': '3! = 3 × 2 × 1 = 6.'
        }
        }, {
            'action': 'see_combination',
            'narration': 'Choose 2 fruits from 3. Order does not matter.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'How many ways to choose 2 from 3?',
            'options': [{
            'id': 'a',
            'text': '3',
            'correct': True
        }, {
            'id': 'b',
            'text': '6',
            'correct': False
        }, {
            'id': 'c',
            'text': '9',
            'correct': False
        }, {
            'id': 'd',
            'text': '1',
            'correct': False
        }],
            'explanation': '3C2 = 3!/(2!1!) = 3.'
        }
        }],
            'conclusion': 'Permutation = order matters. Combination = order does not matter. Divide by factorial for identical items.'
        },
            'understand': 'nPr = n! / (n-r)!. nCr = n! / (r!(n-r)!). Permutation for arrangements. Combination for selections. Identical items require division by factorial of repeats.',
            'manipulate': {
            'prompt': 'How many 3-digit numbers can be formed from 1,2,3,4 without repetition?',
            'answer': '24',
            'hint': 'Permutation: 4P3 = 4!/(4-3)! = 24.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'How many ways to choose 2 from 5?',
            'answer': '10',
            'options': ['5', '10', '20', '25'],
            'interaction_kind': 'numeric_input'
        },
            'build': {
            'prompt': "Find the number of arrangements of the letters in 'AAB'.",
            'answer': '3',
            'explanation': "3!/2! = 3. Two A's are identical.",
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': 'A student computes 3P2 as 3 × 2 = 6 and 3C2 as 3 × 2 = 6. What is wrong?',
            'common_mistake': 'Using the same formula for permutation and combination.',
            'correct_reasoning': '3P2 = 6. 3C2 = 3!/(2!1!) = 3.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: 3C2 = 6.',
            'correct_reasoning': 'Use nCr = n! / (r!(n-r)!) = 3.',
            'interaction_kind': 'formula_fix'
        },
            'retrieval': {
            'prompt': 'What is the formula for nPr?',
            'answer': 'n! / (n-r)!',
            'alternative': ['permutation formula'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'How many ways can 4 people sit in a row if two particular people must sit together?',
            'answer': '12',
            'explanation': 'Treat the pair as one unit: 3! × 2! = 12.',
            'interaction_kind': 'numeric_input'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': '5P3 = ?',
            'answer': '60',
            'options': ['10', '20', '60', '120'],
            'explanation': '5!/(5-3)! = 5×4×3 = 60.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': '5C3 = ?',
            'answer': '10',
            'options': ['10', '20', '60', '120'],
            'explanation': '5!/(3!2!) = 10.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "How many arrangements of 'SUCCESS'?",
            'answer_format': 'numeric',
            'correct': '420',
            'explanation': "7 letters with 3 S's and 2 C's: 7!/(3!2!) = 420.",
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_permutations', 'tcs_combinations'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: How many ways can 3 people be selected from 5?',
            'answer_format': 'numeric',
            'correct': '10',
            'explanation': '5C3 = 10.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'apt_ratio_interpretation_error',
            'signature': 'Student uses combination formula when order matters.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_order_matters_versus_does_not'
        }, {
            'code': 'apt_ratio_interpretation_error',
            'signature': 'Student counts arrangements twice by swapping identical items.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_division_by_factorial_for_identical_items'
        }],
            'srs_key_points': ['Permutation = order matters.', 'Combination = order does not matter.', 'nPr = n! / (n-r)!.', 'nCr = n! / (r!(n-r)!).', 'Divide by factorial for identical items.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'aptitude',
            'competency_id': 'permutations_and_combinations',
            'unlocks_next': [],
            'tower_badge': 'aptitude_permutations_and_combinations'
        }
        }

SLUG = 'aptitude.permutation_combination'
