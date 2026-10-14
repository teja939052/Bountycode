"""World 1 lesson — Compose Small Functions"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'world1_compose_reuse',
            'module_id': 'world1:functions',
            'title': 'Compose Small Functions',
            'description': 'Master Compose Small Functions: Factor repetition into helpers. Small functions compose; one big function does not.',
            'difficulty': 'beginner',
            'est_minutes': 12,
            'xp_reward': 120,
            'skills_taught': ['functions'],
            'srs_concept_tag': 'world1:functions',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Welcome to Compose Small Functions. Factor repetition into helpers. Small functions compose; one big function does not.',
            'correct': ['Nice!', 'Exactly right!', 'Clean.'],
            'wrong': ['Review the step and try again.', 'Close — look at what changed.', 'Think about the mental model.'],
            'after_break': 'You found the broken assumption. Now fix it.',
            'after_mastery': "You've mastered Compose Small Functions. On to the next challenge.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'Compose Small Functions',
            'narration': 'Learn functions through the complete teaching loop.',
            'setting': 'world1_foundations',
            'character': 'Captain Byte',
            'intro_text': 'Factor repetition into helpers. Small functions compose; one big function does not.'
        },
            'steps': {
            'discover': {
            'prompt': 'Observe how functions works in this example.',
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Understand the core principle of functions.',
            'explanation': 'Factor repetition into helpers. Small functions compose; one big function does not.',
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
            'id': 'compose_reuse-p1',
            'prompt': 'Prove you understand functions.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests functions understanding.',
            'time_limit_seconds': 60,
            'company_tags': []
        }, {
            'id': 'compose_reuse-p2',
            'prompt': 'Apply functions to a new context.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests functions transfer.',
            'time_limit_seconds': 60,
            'company_tags': []
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'world1_compose_reuse_mistake',
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
            'tower_badge': 'world1_compose_reuse'
        }
        }

SLUG = 'compose_reuse'
