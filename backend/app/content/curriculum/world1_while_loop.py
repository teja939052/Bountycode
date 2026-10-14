"""World 1 lesson — Controlled Repetition"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'world1_while_loop',
            'module_id': 'world1:loops',
            'title': 'Controlled Repetition',
            'description': 'Master Controlled Repetition: while repeats while a condition is true. The condition must change or the loop never ends.',
            'difficulty': 'beginner',
            'est_minutes': 12,
            'xp_reward': 120,
            'skills_taught': ['loops'],
            'srs_concept_tag': 'world1:loops',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Welcome to Controlled Repetition. while repeats while a condition is true. The condition must change or the loop never ends.',
            'correct': ['Nice!', 'Exactly right!', 'Clean.'],
            'wrong': ['Review the step and try again.', 'Close — look at what changed.', 'Think about the mental model.'],
            'after_break': 'You found the broken assumption. Now fix it.',
            'after_mastery': "You've mastered Controlled Repetition. On to the next challenge.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'Controlled Repetition',
            'narration': 'Learn loops through the complete teaching loop.',
            'setting': 'world1_foundations',
            'character': 'Captain Byte',
            'intro_text': 'while repeats while a condition is true. The condition must change or the loop never ends.'
        },
            'steps': {
            'discover': {
            'prompt': 'Observe how loops works in this example.',
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Understand the core principle of loops.',
            'explanation': 'while repeats while a condition is true. The condition must change or the loop never ends.',
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
            'prompt': 'Write a function using loops.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with this loops usage?',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the loops bug.',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'Recall the key rule for loops.',
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Apply loops to a new problem.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Practice 1: loops basic',
            'answer': 'A',
            'explanation': 'Basic application.',
            'difficulty': 'easy',
            'company_tags': []
        }, {
            'kind': 'mcq',
            'prompt': 'Practice 2: loops intermediate',
            'answer': 'B',
            'explanation': 'Intermediate application.',
            'difficulty': 'medium',
            'company_tags': []
        }, {
            'kind': 'numeric',
            'prompt': 'Practice 3: loops numeric',
            'answer': '42',
            'explanation': 'Numeric application.',
            'difficulty': 'medium',
            'company_tags': []
        }],
            'proof': [{
            'id': 'while_loop-p1',
            'prompt': 'Prove you understand loops.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests loops understanding.',
            'time_limit_seconds': 60,
            'company_tags': []
        }, {
            'id': 'while_loop-p2',
            'prompt': 'Apply loops to a new context.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests loops transfer.',
            'time_limit_seconds': 60,
            'company_tags': []
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'world1_while_loop_mistake',
            'signature': 'Common mistake in loops',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_correct_process'
        }],
            'srs_key_points': ['Core principle of loops', 'Common pitfall in loops', 'When to apply loops'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding_foundations',
            'competency_id': 'loops',
            'unlocks_next': [],
            'tower_badge': 'world1_while_loop'
        }
        }

SLUG = 'world1_while_loop'
