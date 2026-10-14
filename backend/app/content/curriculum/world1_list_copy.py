"""World 1 lesson — Slicing, Aliasing, Copying"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'world1_list_copy',
            'module_id': 'world1:arrays',
            'title': 'Slicing, Aliasing, Copying',
            'description': 'Master Slicing, Aliasing, Copying: b = a aliases; b = a[:] copies. Slice aliases the original.',
            'difficulty': 'beginner',
            'est_minutes': 12,
            'xp_reward': 120,
            'skills_taught': ['arrays'],
            'srs_concept_tag': 'world1:arrays',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Welcome to Slicing, Aliasing, Copying. b = a aliases; b = a[:] copies. Slice aliases the original.',
            'correct': ['Nice!', 'Exactly right!', 'Clean.'],
            'wrong': ['Review the step and try again.', 'Close — look at what changed.', 'Think about the mental model.'],
            'after_break': 'You found the broken assumption. Now fix it.',
            'after_mastery': "You've mastered Slicing, Aliasing, Copying. On to the next challenge.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'Slicing, Aliasing, Copying',
            'narration': 'Learn arrays through the complete teaching loop.',
            'setting': 'world1_foundations',
            'character': 'Captain Byte',
            'intro_text': 'b = a aliases; b = a[:] copies. Slice aliases the original.'
        },
            'steps': {
            'discover': {
            'prompt': 'Observe how arrays works in this example.',
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Understand the core principle of arrays.',
            'explanation': 'b = a aliases; b = a[:] copies. Slice aliases the original.',
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
            'prompt': 'Write a function using arrays.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with this arrays usage?',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the arrays bug.',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'Recall the key rule for arrays.',
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Apply arrays to a new problem.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Practice 1: arrays basic',
            'answer': 'A',
            'explanation': 'Basic application.',
            'difficulty': 'easy',
            'company_tags': []
        }, {
            'kind': 'mcq',
            'prompt': 'Practice 2: arrays intermediate',
            'answer': 'B',
            'explanation': 'Intermediate application.',
            'difficulty': 'medium',
            'company_tags': []
        }, {
            'kind': 'numeric',
            'prompt': 'Practice 3: arrays numeric',
            'answer': '42',
            'explanation': 'Numeric application.',
            'difficulty': 'medium',
            'company_tags': []
        }],
            'proof': [{
            'id': 'list_copy-p1',
            'prompt': 'Prove you understand arrays.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests arrays understanding.',
            'time_limit_seconds': 60,
            'company_tags': []
        }, {
            'id': 'list_copy-p2',
            'prompt': 'Apply arrays to a new context.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests arrays transfer.',
            'time_limit_seconds': 60,
            'company_tags': []
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'world1_list_copy_mistake',
            'signature': 'Common mistake in arrays',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_correct_process'
        }],
            'srs_key_points': ['Core principle of arrays', 'Common pitfall in arrays', 'When to apply arrays'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding_foundations',
            'competency_id': 'arrays',
            'unlocks_next': [],
            'tower_badge': 'world1_list_copy'
        }
        }

SLUG = 'world1_list_copy'
