"""World 1 lesson — World-1 Exam: Perform + Explain"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'world1_capstone_oa',
            'module_id': 'world1:capstone',
            'title': 'World-1 Exam: Perform + Explain',
            'description': 'Master World-1 Exam: Perform + Explain: Solve 4 unseen timed placement-style problems unaided, then explain one solution.',
            'difficulty': 'beginner',
            'est_minutes': 12,
            'xp_reward': 120,
            'skills_taught': ['capstone'],
            'srs_concept_tag': 'world1:capstone',
            'domain': 'coding',
            'captain_byte': {
            'intro': 'Welcome to World-1 Exam: Perform + Explain. Solve 4 unseen timed placement-style problems unaided, then explain one solution.',
            'correct': ['Nice!', 'Exactly right!', 'Clean.'],
            'wrong': ['Review the step and try again.', 'Close — look at what changed.', 'Think about the mental model.'],
            'after_break': 'You found the broken assumption. Now fix it.',
            'after_mastery': "You've mastered World-1 Exam: Perform + Explain. On to the next challenge.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'World-1 Exam: Perform + Explain',
            'narration': 'Learn capstone through the complete teaching loop.',
            'setting': 'world1_foundations',
            'character': 'Captain Byte',
            'intro_text': 'Solve 4 unseen timed placement-style problems unaided, then explain one solution.'
        },
            'steps': {
            'discover': {
            'prompt': 'Observe how capstone works in this example.',
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Understand the core principle of capstone.',
            'explanation': 'Solve 4 unseen timed placement-style problems unaided, then explain one solution.',
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
            'prompt': 'Write a function using capstone.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with this capstone usage?',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the capstone bug.',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'Recall the key rule for capstone.',
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Apply capstone to a new problem.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Practice 1: capstone basic',
            'answer': 'A',
            'explanation': 'Basic application.',
            'difficulty': 'easy',
            'company_tags': []
        }, {
            'kind': 'mcq',
            'prompt': 'Practice 2: capstone intermediate',
            'answer': 'B',
            'explanation': 'Intermediate application.',
            'difficulty': 'medium',
            'company_tags': []
        }, {
            'kind': 'numeric',
            'prompt': 'Practice 3: capstone numeric',
            'answer': '42',
            'explanation': 'Numeric application.',
            'difficulty': 'medium',
            'company_tags': []
        }],
            'proof': [{
            'id': 'capstone_oa-p1',
            'prompt': 'Prove you understand capstone.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests capstone understanding.',
            'time_limit_seconds': 60,
            'company_tags': []
        }, {
            'id': 'capstone_oa-p2',
            'prompt': 'Apply capstone to a new context.',
            'answer_format': 'text',
            'correct': 'Correct',
            'explanation': 'Tests capstone transfer.',
            'time_limit_seconds': 60,
            'company_tags': []
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'world1_capstone_oa_mistake',
            'signature': 'Common mistake in capstone',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_correct_process'
        }],
            'srs_key_points': ['Core principle of capstone', 'Common pitfall in capstone', 'When to apply capstone'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'coding_foundations',
            'competency_id': 'capstone',
            'unlocks_next': [],
            'tower_badge': 'world1_capstone_oa'
        }
        }

SLUG = 'world1_capstone_oa'
