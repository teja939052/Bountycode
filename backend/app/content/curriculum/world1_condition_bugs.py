"""World 1 lesson — Break: Wrong Condition"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'world1_condition_bugs',
            'module_id': 'world1:control_flow',
            'title': 'Break: Wrong Condition',
            'description': 'Master Break: Wrong Condition: Inverted logic, off-by-one boundaries, and missing edge cases cause wrong conditions.',
            'difficulty': 'beginner',
            'est_minutes': 12,
            'xp_reward': 120,
            'skills_taught': ['control_flow'],
            'srs_concept_tag': 'world1:control_flow',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Welcome to Break: Wrong Condition. Inverted logic, off-by-one boundaries, and missing edge cases cause wrong conditions.',
            'correct': ['Nice!', 'Exactly right!', 'Clean.'],
            'wrong': ['Review the step and try again.', 'Close — look at what changed.', 'Think about the mental model.'],
            'after_break': 'You found the broken assumption. Now fix it.',
            'after_mastery': "You've mastered Break: Wrong Condition. On to the next challenge.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'Break: Wrong Condition',
            'narration': 'Learn control_flow through the complete teaching loop.',
            'setting': 'world1_foundations',
            'character': 'Captain Byte',
            'intro_text': 'Inverted logic, off-by-one boundaries, and missing edge cases cause wrong conditions.'
        },
            'steps': {
            'discover': {
            'prompt': 'Observe how control_flow works in this example.',
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Understand the core principle of control_flow.',
            'explanation': 'Inverted logic, off-by-one boundaries, and missing edge cases cause wrong conditions.',
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
            'prompt': 'Write a function using control_flow.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with this control_flow usage?',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the control_flow bug.',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'Recall the key rule for control_flow.',
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Apply control_flow to a new problem.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Practice 1: control_flow basic',
            'answer': 'A',
            'explanation': 'Basic application.',
            'difficulty': 'easy',
            'company_tags': []
        }, {
            'kind': 'mcq',
            'prompt': 'Practice 2: control_flow intermediate',
            'answer': 'B',
            'explanation': 'Intermediate application.',
            'difficulty': 'medium',
            'company_tags': []
        }, {
            'kind': 'numeric',
            'prompt': 'Practice 3: control_flow numeric',
            'answer': '42',
            'explanation': 'Numeric application.',
            'difficulty': 'medium',
            'company_tags': []
        }],
            'proof': [{
            'id': 'condition_bugs-p1',
            'prompt': 'Prove you understand control_flow.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests control_flow understanding.',
            'time_limit_seconds': 60,
            'company_tags': []
        }, {
            'id': 'condition_bugs-p2',
            'prompt': 'Apply control_flow to a new context.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests control_flow transfer.',
            'time_limit_seconds': 60,
            'company_tags': []
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'world1_condition_bugs_mistake',
            'signature': 'Common mistake in control_flow',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_correct_process'
        }],
            'srs_key_points': ['Core principle of control_flow', 'Common pitfall in control_flow', 'When to apply control_flow'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding_foundations',
            'competency_id': 'control_flow',
            'unlocks_next': [],
            'tower_badge': 'world1_condition_bugs'
        }
        }

SLUG = 'world1_condition_bugs'
