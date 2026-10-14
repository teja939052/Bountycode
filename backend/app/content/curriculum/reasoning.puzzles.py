"""Lesson module — Puzzles"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'reasoning.puzzles',
            'module_id': 'reasoning.puzzles',
            'title': 'Puzzles',
            'description': 'Puzzles test logical thinking and constraint satisfaction. They appear in TCS NQT and Infosys reasoning sections.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Puzzles'],
            'srs_concept_tag': 'reasoning.puzzles',
            'domain': 'reasoning',
            'captain_byte': {
            'intro': 'Puzzles are constrained logic. List constraints, then test candidates.',
            'correct': ['Valid candidate.', 'You checked all constraints.', 'Right deduction.'],
            'wrong': ['List every constraint first.', 'Eliminate candidates that violate any constraint.', 'Use a table if needed.'],
            'after_break': 'You found the missed constraint. Now rebuild the candidate set.',
            'after_mastery': "You can now solve logical puzzles. That's placement-ready reasoning skill.",
            'retry_prompt': 'Try again. Write down all constraints before testing candidates.'
        },
            'story_context': {
            'title': 'Puzzles',
            'narration': 'Puzzles test logical thinking and constraint satisfaction. They appear in TCS NQT and Infosys reasoning sections.',
            'setting': 'puzzles',
            'character': 'Captain Byte',
            'intro_text': 'Puzzles test logical thinking and constraint satisfaction. They appear in TCS NQT and Infosys reasoning sections.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_constraints',
            'narration': 'Four people sit in a row. A sits left of B. C is between A and D. D is at the right end.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What is the order?',
            'options': [{
            'id': 'a',
            'text': 'A C D B',
            'correct': False
        }, {
            'id': 'b',
            'text': 'A C B D',
            'correct': False
        }, {
            'id': 'c',
            'text': 'A C D B',
            'correct': False
        }, {
            'id': 'd',
            'text': 'A C B D',
            'correct': False
        }],
            'explanation': 'This is a sample puzzle. Fix D at right. C between A and D. A left of B.'
        }
        }],
            'conclusion': 'List all constraints. Fix any absolute positions. Test candidates against every constraint. Eliminate violators.'
        },
            'understand': 'Puzzles use absolute and relative constraints. Common patterns: seating, ranking, assignment, and scheduling. Use tables or diagrams to track possibilities.',
            'manipulate': {
            'prompt': 'A is taller than B. C is shorter than A. B is taller than D. Who is the tallest?',
            'answer': 'A',
            'hint': 'A > B, A > C, B > D. So A is tallest.',
            'interaction_kind': 'mcq_classify'
        },
            'predict': {
            'prompt': 'Five people sit in a line. P is left of Q. R is between P and S. T is at the right end. Who is second from right?',
            'answer': 'S',
            'options': ['P', 'Q', 'R', 'S'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': 'Four people have different heights. A is taller than B. C is shorter than D. B is taller than C. D is not the tallest. Rank them.',
            'answer': 'A > D > B > C',
            'explanation': 'From constraints: A > B, A > C, B > C, D > C, D not tallest → A tallest, D second, B third, C fourth.',
            'interaction_kind': 'ordering'
        },
            'break_step': {
            'prompt': 'A student says B is tallest because B > D. What is wrong?',
            'common_mistake': 'Ignoring that A > B.',
            'correct_reasoning': 'A > B, so B cannot be tallest.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: B is tallest.',
            'correct_reasoning': 'A is tallest because A > B and A > C.',
            'interaction_kind': 'mcq_diagnose'
        },
            'retrieval': {
            'prompt': 'What is the first step in solving a puzzle?',
            'answer': 'List all constraints',
            'alternative': ['write down constraints', 'identify absolute positions'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Three people have different amounts of money. A has more than B. C has less than A. B has more than C. Who has the least?',
            'answer': 'C',
            'explanation': 'A > B > C or A > C and B > C. Either way, C is lowest.',
            'interaction_kind': 'mcq_classify'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'A is taller than B. C is shorter than B. Who is tallest?',
            'answer': 'A',
            'options': ['A', 'B', 'C', 'Cannot determine'],
            'explanation': 'A > B > C.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'P is left of Q. R is right of Q. Who is in the middle?',
            'answer': 'Q',
            'options': ['P', 'Q', 'R', 'Cannot determine'],
            'explanation': 'P-Q-R.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'Four people A, B, C, D have different ranks. A is higher than B. C is lower than A. D is higher than C but lower than B. Find the ranking.',
            'answer_format': 'text',
            'correct': 'A > B > D > C',
            'explanation': 'Apply all constraints to order.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_puzzles', 'tcs_constraint_satisfaction'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': "TCS: Five people sit around a table. A is right of B. C is opposite D. E is left of A. Find E's position.",
            'answer_format': 'text',
            'correct': 'E is left of A',
            'explanation': 'Use fixed references and relative positions.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'reasoning_assumption_error',
            'signature': 'Student assumes minimum values without proving feasibility.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_feasibility_check'
        }, {
            'code': 'reasoning_constraint_omission',
            'signature': 'Student ignores one constraint while solving.',
            'reteach_route': 'bug_surgery',
            'reteach_action': 'show_constraint_table'
        }],
            'srs_key_points': ['List all constraints first.', 'Fix absolute positions when given.', 'Test candidates against every constraint.', 'Use tables or diagrams.', 'Eliminate violators immediately.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'reasoning',
            'competency_id': 'puzzles',
            'unlocks_next': [],
            'tower_badge': 'reasoning_puzzles'
        }
        }

SLUG = 'reasoning.puzzles'
