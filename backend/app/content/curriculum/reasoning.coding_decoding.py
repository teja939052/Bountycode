"""Lesson module — Coding-Decoding"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'reasoning.coding_decoding',
            'module_id': 'reasoning.coding_decoding',
            'title': 'Coding-Decoding',
            'description': 'Coding-decoding tests pattern substitution under time pressure. It appears in TCS NQT and Infosys reasoning sections.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Coding-Decoding'],
            'srs_concept_tag': 'reasoning.coding_decoding',
            'domain': 'reasoning',
            'captain_byte': {
            'intro': 'Coding-decoding is pattern substitution. Find the rule, then apply it.',
            'correct': ['Pattern found.', 'Right substitution.', 'Correct code.'],
            'wrong': ['Write the pattern table first.', 'Check the shift direction.', 'Verify with a second example.'],
            'after_break': 'You found the wrong rule. Now rebuild the pattern table and reapply.',
            'after_mastery': "You can now decode patterns fast. That's placement-ready reasoning skill.",
            'retry_prompt': 'Try again. Write the pattern table before coding.'
        },
            'story_context': {
            'title': 'Coding-Decoding',
            'narration': 'Coding-decoding tests pattern substitution under time pressure. It appears in TCS NQT and Infosys reasoning sections.',
            'setting': 'coding-decoding',
            'character': 'Captain Byte',
            'intro_text': 'Coding-decoding tests pattern substitution under time pressure. It appears in TCS NQT and Infosys reasoning sections.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_shift',
            'narration': 'A is coded as C, B as D. What is the rule?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'If A→C, B→D, what is C→?',
            'options': [{
            'id': 'a',
            'text': 'E',
            'correct': True
        }, {
            'id': 'b',
            'text': 'F',
            'correct': False
        }, {
            'id': 'c',
            'text': 'D',
            'correct': False
        }, {
            'id': 'd',
            'text': 'G',
            'correct': False
        }],
            'explanation': 'Each letter shifts +2. C + 2 = E.'
        }
        }, {
            'action': 'see_reverse',
            'narration': 'CODE becomes EDOC. What is the rule?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'If CODE → EDOC, what is the rule?',
            'options': [{
            'id': 'a',
            'text': 'Reverse the word',
            'correct': True
        }, {
            'id': 'b',
            'text': 'Shift +1',
            'correct': False
        }, {
            'id': 'c',
            'text': 'Shift -1',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Swap pairs',
            'correct': False
        }],
            'explanation': 'The word is reversed, not shifted.'
        }
        }],
            'conclusion': 'Coding-decoding uses substitution rules: shift, reverse, alternate, or custom mapping. Always verify the rule with a second example.'
        },
            'understand': 'Common coding rules: fixed shift, reverse word, alternate letters, opposite letters (A↔Z), and custom maps. Build a pattern table from given examples, then apply it to the target.',
            'manipulate': {
            'prompt': 'If A=1, B=2, C=3, what is DOG?',
            'answer': '4 15 7',
            'hint': 'Map each letter to its position: D=4, O=15, G=7.',
            'interaction_kind': 'pattern_map'
        },
            'predict': {
            'prompt': 'If CAT is coded as 3120, what is the rule?',
            'answer': 'position_sum',
            'options': ['position_sum', 'reverse', 'shift+1', 'product'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': "Code 'HELLO' with rule: A↔Z, B↔Y, C↔X (opposite letters).",
            'answer': 'SVOOL',
            'explanation': 'H=8 ↔ S=19, E=5 ↔ V=22, L=13 ↔ O=15, L=13 ↔ O=15, O=15 ↔ L=12.',
            'interaction_kind': 'pattern_map'
        },
            'break_step': {
            'prompt': 'A student decodes ABC with rule +2 as BCD, but the answer is CDE. What is wrong?',
            'common_mistake': 'Applying the rule once instead of to each letter.',
            'correct_reasoning': 'A+2=C, B+2=D, C+2=E.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix: 'ABC +2 = BCD'.",
            'correct_reasoning': 'A+2=C, B+2=D, C+2=E → CDE.',
            'interaction_kind': 'mcq_diagnose'
        },
            'retrieval': {
            'prompt': 'Name two common coding-decoding rules.',
            'answer': 'Fixed shift, reverse word',
            'alternative': ['shift', 'reverse', 'opposite letters', 'alternate letters'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'If PEN is coded as 161420, what is PAPER?',
            'answer': '161216518',
            'explanation': 'P=16, E=5, N=14. Same mapping: P=16, A=1, P=16, E=5, R=18.',
            'interaction_kind': 'pattern_map'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'If A→C, B→D, C→E, what is Z→?',
            'answer': 'B',
            'options': ['A', 'B', 'C', 'D'],
            'explanation': 'Z + 2 wraps to B.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': "If 'HELLO' becomes 'SVOOL', what is the rule?",
            'answer': 'Opposite letters',
            'options': ['Shift +1', 'Reverse', 'Opposite letters', 'Alternate'],
            'explanation': 'H↔S, E↔V, L↔O, L↔O, O↔L.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "If 'BOOK' is coded as 'CPPL', what is the rule and what is 'PAGE'?",
            'answer_format': 'text',
            'correct': 'shift+1',
            'explanation': 'Each letter shifts +1. P→Q, A→B, G→H, E→F.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'infosys',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['infosys_coding_decoding', 'infosys_pattern_substitution'],
            'proof_questions': [{
            'id': 'infy-p1',
            'prompt': "Infosys: If 'ALPHA' becomes 'BQMIB', what is 'BETA'?",
            'answer_format': 'text',
            'correct': 'CFUB',
            'explanation': 'Apply the same shift pattern from ALPHA→BQMIB.',
            'time_limit_seconds': 90,
            'company_tags': ['infosys']
        }]
        }],
            'misconceptions': [{
            'code': 'reasoning_sequence_inference',
            'signature': 'Student assumes a fixed +1/+2 shift without verifying the pattern.',
            'reteach_route': 'bug_surgery',
            'reteach_action': 'show_pattern_table'
        }, {
            'code': 'reasoning_ordering_error',
            'signature': 'Student reverses the whole word instead of applying the coding rule.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_rule_before_reverse'
        }],
            'srs_key_points': ['Build a pattern table from given examples.', 'Verify the rule with a second example before applying.', 'Common rules: shift, reverse, opposite letters, alternate.', 'Letter positions: A=1, B=2, ..., Z=26.', 'Opposite letters: A↔Z, B↔Y, C↔X.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'reasoning',
            'competency_id': 'coding-decoding',
            'unlocks_next': [],
            'tower_badge': 'reasoning_coding_decoding'
        }
        }

SLUG = 'reasoning.coding_decoding'
