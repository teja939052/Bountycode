"""World 1 lesson — Timed Placement: Decide + Loop"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'world1_decision_oa',
            'module_id': 'world1:decisions',
            'title': 'Timed Placement: Decide + Loop',
            'description': 'Master Timed Placement: Decide + Loop: Solve timed decision problems under placement conditions.',
            'difficulty': 'beginner',
            'est_minutes': 12,
            'xp_reward': 120,
            'skills_taught': ['decisions'],
            'srs_concept_tag': 'world1:decisions',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Welcome to Timed Placement: Decide + Loop. Solve timed decision problems under placement conditions.',
            'correct': ['Nice!', 'Exactly right!', 'Clean.'],
            'wrong': ['Review the step and try again.', 'Close — look at what changed.', 'Think about the mental model.'],
            'after_break': 'You found the broken assumption. Now fix it.',
            'after_mastery': "You've mastered Timed Placement: Decide + Loop. On to the next challenge.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'Timed Placement: Decide + Loop',
            'narration': 'Learn decisions through the complete teaching loop.',
            'setting': 'world1_foundations',
            'character': 'Captain Byte',
            'intro_text': 'Solve timed decision problems under placement conditions.'
        },
            'steps': {
            'discover': {
            'prompt': 'Observe how decisions works in this example.',
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Understand the core principle of decisions.',
            'explanation': 'Solve timed decision problems under placement conditions.',
            'interaction_kind': 'read_explanation'
        },
            'manipulate': {
            'prompt': 'Modify the example and observe the change.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'Predict the output before running.',
            'interaction_kind': 'numeric_input'
        },
            'build': {
            'prompt': 'Write a function using decisions.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with this decisions usage?',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the decisions bug.',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'Recall the key rule for decisions.',
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Apply decisions to a new problem.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Practice 1: decisions basic',
            'answer': 'A',
            'explanation': 'Basic application.',
            'difficulty': 'easy',
            'company_tags': []
        }, {
            'kind': 'mcq',
            'prompt': 'Practice 2: decisions intermediate',
            'answer': 'B',
            'explanation': 'Intermediate application.',
            'difficulty': 'medium',
            'company_tags': []
        }, {
            'kind': 'numeric',
            'prompt': 'Practice 3: decisions numeric',
            'answer': '42',
            'explanation': 'Numeric application.',
            'difficulty': 'medium',
            'company_tags': []
        }],
            'proof': [{
            'id': 'decision_oa-p1',
            'prompt': 'Prove you understand decisions.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests decisions understanding.',
            'time_limit_seconds': 60,
            'company_tags': []
        }, {
            'id': 'decision_oa-p2',
            'prompt': 'Apply decisions to a new context.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests decisions transfer.',
            'time_limit_seconds': 60,
            'company_tags': []
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'world1_decision_oa_mistake',
            'signature': 'Common mistake in decisions',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_correct_process'
        }],
            'srs_key_points': ['Core principle of decisions', 'Common pitfall in decisions', 'When to apply decisions'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding_foundations',
            'competency_id': 'decisions',
            'unlocks_next': [],
            'tower_badge': 'world1_decision_oa'
        }
        }

SLUG = 'world1_decision_oa'
