"""World 1 lesson — Break: The Silent Forge"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'world1_function_bugs',
            'module_id': 'world1:functions',
            'title': 'Break: The Silent Forge',
            'description': 'Master Break: The Silent Forge: Missing return, wrong argument order, shadowing, parameter mutation.',
            'difficulty': 'beginner',
            'est_minutes': 12,
            'xp_reward': 120,
            'skills_taught': ['functions'],
            'srs_concept_tag': 'world1:functions',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Welcome to Break: The Silent Forge. Missing return, wrong argument order, shadowing, parameter mutation.',
            'correct': ['Nice!', 'Exactly right!', 'Clean.'],
            'wrong': ['Review the step and try again.', 'Close — look at what changed.', 'Think about the mental model.'],
            'after_break': 'You found the broken assumption. Now fix it.',
            'after_mastery': "You've mastered Break: The Silent Forge. On to the next challenge.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'Break: The Silent Forge',
            'narration': 'Learn functions through the complete teaching loop.',
            'setting': 'world1_foundations',
            'character': 'Captain Byte',
            'intro_text': 'Missing return, wrong argument order, shadowing, parameter mutation.'
        },
            'steps': {
            'discover': {
            'prompt': 'Observe how functions works in this example.',
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Understand the core principle of functions.',
            'explanation': 'Missing return, wrong argument order, shadowing, parameter mutation.',
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
            'prompt': 'Write a function using functions.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with this functions usage?',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the functions bug.',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'Recall the key rule for functions.',
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Apply functions to a new problem.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Practice 1: functions basic',
            'answer': 'A',
            'explanation': 'Basic application.',
            'difficulty': 'easy',
            'company_tags': []
        }, {
            'kind': 'mcq',
            'prompt': 'Practice 2: functions intermediate',
            'answer': 'B',
            'explanation': 'Intermediate application.',
            'difficulty': 'medium',
            'company_tags': []
        }, {
            'kind': 'numeric',
            'prompt': 'Practice 3: functions numeric',
            'answer': '42',
            'explanation': 'Numeric application.',
            'difficulty': 'medium',
            'company_tags': []
        }],
            'proof': [{
            'id': 'function_bugs-p1',
            'prompt': 'Prove you understand functions.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests functions understanding.',
            'time_limit_seconds': 60,
            'company_tags': []
        }, {
            'id': 'function_bugs-p2',
            'prompt': 'Apply functions to a new context.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests functions transfer.',
            'time_limit_seconds': 60,
            'company_tags': []
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'world1_function_bugs_mistake',
            'signature': 'Common mistake in functions',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_correct_process'
        }],
            'srs_key_points': ['Core principle of functions', 'Common pitfall in functions', 'When to apply functions'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding_foundations',
            'competency_id': 'functions',
            'unlocks_next': [],
            'tower_badge': 'world1_function_bugs'
        }
        }

SLUG = 'world1_function_bugs'
