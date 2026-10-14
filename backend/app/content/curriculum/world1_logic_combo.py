"""World 1 lesson — and / or / not"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'world1_logic_combo',
            'module_id': 'world1:booleans',
            'title': 'and / or / not',
            'description': 'Master and / or / not: and needs both; or needs one; not inverts. Parentheses group logic.',
            'difficulty': 'beginner',
            'est_minutes': 12,
            'xp_reward': 120,
            'skills_taught': ['booleans'],
            'srs_concept_tag': 'world1:booleans',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Welcome to and / or / not. and needs both; or needs one; not inverts. Parentheses group logic.',
            'correct': ['Nice!', 'Exactly right!', 'Clean.'],
            'wrong': ['Review the step and try again.', 'Close — look at what changed.', 'Think about the mental model.'],
            'after_break': 'You found the broken assumption. Now fix it.',
            'after_mastery': "You've mastered and / or / not. On to the next challenge.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'and / or / not',
            'narration': 'Learn booleans through the complete teaching loop.',
            'setting': 'world1_foundations',
            'character': 'Captain Byte',
            'intro_text': 'and needs both; or needs one; not inverts. Parentheses group logic.'
        },
            'steps': {
            'discover': {
            'prompt': 'Observe how booleans works in this example.',
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Understand the core principle of booleans.',
            'explanation': 'and needs both; or needs one; not inverts. Parentheses group logic.',
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
            'prompt': 'Write a function using booleans.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with this booleans usage?',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the booleans bug.',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'Recall the key rule for booleans.',
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Apply booleans to a new problem.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Practice 1: booleans basic',
            'answer': 'A',
            'explanation': 'Basic application.',
            'difficulty': 'easy',
            'company_tags': []
        }, {
            'kind': 'mcq',
            'prompt': 'Practice 2: booleans intermediate',
            'answer': 'B',
            'explanation': 'Intermediate application.',
            'difficulty': 'medium',
            'company_tags': []
        }, {
            'kind': 'numeric',
            'prompt': 'Practice 3: booleans numeric',
            'answer': '42',
            'explanation': 'Numeric application.',
            'difficulty': 'medium',
            'company_tags': []
        }],
            'proof': [{
            'id': 'logic_combo-p1',
            'prompt': 'Prove you understand booleans.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests booleans understanding.',
            'time_limit_seconds': 60,
            'company_tags': []
        }, {
            'id': 'logic_combo-p2',
            'prompt': 'Apply booleans to a new context.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests booleans transfer.',
            'time_limit_seconds': 60,
            'company_tags': []
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'world1_logic_combo_mistake',
            'signature': 'Common mistake in booleans',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_correct_process'
        }],
            'srs_key_points': ['Core principle of booleans', 'Common pitfall in booleans', 'When to apply booleans'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding_foundations',
            'competency_id': 'booleans',
            'unlocks_next': [],
            'tower_badge': 'world1_logic_combo'
        }
        }

SLUG = 'world1_logic_combo'
