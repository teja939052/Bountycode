"""World 1 lesson — Walk a String"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'world1_string_walk',
            'module_id': 'world1:strings',
            'title': 'Walk a String',
            'description': 'Master Walk a String: Iterate over characters with for. Convert char to int with ord() or int().',
            'difficulty': 'beginner',
            'est_minutes': 12,
            'xp_reward': 120,
            'skills_taught': ['strings'],
            'srs_concept_tag': 'world1:strings',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Welcome to Walk a String. Iterate over characters with for. Convert char to int with ord() or int().',
            'correct': ['Nice!', 'Exactly right!', 'Clean.'],
            'wrong': ['Review the step and try again.', 'Close — look at what changed.', 'Think about the mental model.'],
            'after_break': 'You found the broken assumption. Now fix it.',
            'after_mastery': "You've mastered Walk a String. On to the next challenge.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'Walk a String',
            'narration': 'Learn strings through the complete teaching loop.',
            'setting': 'world1_foundations',
            'character': 'Captain Byte',
            'intro_text': 'Iterate over characters with for. Convert char to int with ord() or int().'
        },
            'steps': {
            'discover': {
            'prompt': 'Observe how strings works in this example.',
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Understand the core principle of strings.',
            'explanation': 'Iterate over characters with for. Convert char to int with ord() or int().',
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
            'prompt': 'Write a function using strings.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with this strings usage?',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the strings bug.',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'Recall the key rule for strings.',
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Apply strings to a new problem.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Practice 1: strings basic',
            'answer': 'A',
            'explanation': 'Basic application.',
            'difficulty': 'easy',
            'company_tags': []
        }, {
            'kind': 'mcq',
            'prompt': 'Practice 2: strings intermediate',
            'answer': 'B',
            'explanation': 'Intermediate application.',
            'difficulty': 'medium',
            'company_tags': []
        }, {
            'kind': 'numeric',
            'prompt': 'Practice 3: strings numeric',
            'answer': '42',
            'explanation': 'Numeric application.',
            'difficulty': 'medium',
            'company_tags': []
        }],
            'proof': [{
            'id': 'string_walk-p1',
            'prompt': 'Prove you understand strings.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests strings understanding.',
            'time_limit_seconds': 60,
            'company_tags': []
        }, {
            'id': 'string_walk-p2',
            'prompt': 'Apply strings to a new context.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests strings transfer.',
            'time_limit_seconds': 60,
            'company_tags': []
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'world1_string_walk_mistake',
            'signature': 'Common mistake in strings',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_correct_process'
        }],
            'srs_key_points': ['Core principle of strings', 'Common pitfall in strings', 'When to apply strings'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding_foundations',
            'competency_id': 'strings',
            'unlocks_next': [],
            'tower_badge': 'world1_string_walk'
        }
        }

SLUG = 'world1_string_walk'
