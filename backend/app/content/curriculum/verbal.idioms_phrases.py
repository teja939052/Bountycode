"""Lesson module — Idioms and Phrases"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'verbal.idioms_phrases',
            'module_id': 'verbal.idioms_phrases',
            'title': 'Idioms and Phrases',
            'description': 'Idioms and phrases test idiomatic English understanding, which appears in TCS NQT and Infosys English sections.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Idioms and Phrases'],
            'srs_concept_tag': 'verbal.idioms_phrases',
            'domain': 'verbal',
            'captain_byte': {
            'intro': 'Idioms are fixed expressions with figurative meanings. Learn them as chunks, not word by word.',
            'correct': ['Right idiom.', 'Context fits meaning.', 'Correct usage.'],
            'wrong': ['Idioms are figurative, not literal.', 'Check whether the context is positive or negative.', 'Learn common collocations.'],
            'after_break': 'You found the wrong idiom. Now match the meaning to the context.',
            'after_mastery': "You can now use and recognize idioms. That's placement-ready verbal skill.",
            'retry_prompt': "Try again. Match the idiom's meaning to the sentence context."
        },
            'story_context': {
            'title': 'Idioms and Phrases',
            'narration': 'Idioms and phrases test idiomatic English understanding, which appears in TCS NQT and Infosys English sections.',
            'setting': 'idioms_and_phrases',
            'character': 'Captain Byte',
            'intro_text': 'Idioms and phrases test idiomatic English understanding, which appears in TCS NQT and Infosys English sections.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_common_idiom',
            'narration': "'Break the ice' means to start a conversation in a social setting.",
            'interaction': {
            'type': 'choose_outcome',
            'prompt': "What does 'break the ice' mean?",
            'options': [{
            'id': 'a',
            'text': 'Start a conversation',
            'correct': True
        }, {
            'id': 'b',
            'text': 'Damage something',
            'correct': False
        }, {
            'id': 'c',
            'text': 'Cool down',
            'correct': False
        }, {
            'id': 'd',
            'text': 'End a meeting',
            'correct': False
        }],
            'explanation': "'Break the ice' figuratively means to start a conversation."
        }
        }, {
            'action': 'see_context',
            'narration': "'Spill the beans' means to reveal a secret. It fits a surprise-party context.",
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Choose the idiom for revealing a secret.',
            'options': [{
            'id': 'a',
            'text': 'Spill the beans',
            'correct': True
        }, {
            'id': 'b',
            'text': 'Break the ice',
            'correct': False
        }, {
            'id': 'c',
            'text': 'Hit the sack',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Bite the bullet',
            'correct': False
        }],
            'explanation': "'Spill the beans' means to reveal a secret."
        }
        }],
            'conclusion': 'Idioms are figurative. Learn them as fixed chunks. Match meaning to context. Common themes: action, emotion, time, decision.'
        },
            'understand': 'Idioms are fixed phrases with non-literal meanings. Context determines which idiom fits. Common categories: actions, emotions, time, decisions, and social interactions.',
            'manipulate': {
            'prompt': "Replace 'to reveal a secret' with an idiom.",
            'answer': 'spill the beans',
            'hint': 'Think of beans spilling from a container.',
            'interaction_kind': 'mcq_classify'
        },
            'predict': {
            'prompt': "Choose the best idiom: 'After the interview, he ___ and went home.'",
            'answer': 'breathed a sigh of relief',
            'options': ['breathed a sigh of relief', 'broke the ice', 'spilled the beans', 'hit the sack'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': "Use 'bite the bullet' in a sentence about facing a difficult situation.",
            'answer': 'I had to bite the bullet and give the presentation.',
            'explanation': "'Bite the bullet' means to face something unpleasant bravely.",
            'interaction_kind': 'short_answer'
        },
            'break_step': {
            'prompt': "A student uses 'break the ice' for ending a meeting. What is wrong?",
            'common_mistake': 'Literal interpretation instead of figurative.',
            'correct_reasoning': "'Break the ice' means to start, not end, a conversation.",
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix: 'break the ice' for ending a meeting.",
            'correct_reasoning': "Use 'wrap up' or 'close the meeting' for ending.",
            'interaction_kind': 'mcq_diagnose'
        },
            'retrieval': {
            'prompt': "What does 'hit the sack' mean?",
            'answer': 'Go to bed',
            'alternative': ['go to sleep'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': "Choose the idiom: 'She ___ and told everyone the surprise party.'",
            'answer': 'spilled the beans',
            'explanation': 'Revealing a secret = spill the beans.',
            'interaction_kind': 'mcq_classify'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': "What does 'bite the bullet' mean?",
            'answer': 'Face something unpleasant',
            'options': ['Chew something', 'Face something unpleasant', 'Run away', 'Give up'],
            'explanation': 'To accept something difficult bravely.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': "Choose: 'The meeting was dull until John ___ with a joke.'",
            'answer': 'broke the ice',
            'options': ['broke the ice', 'spilled the beans', 'hit the sack', 'bit the bullet'],
            'explanation': 'Starting a conversation in a social setting.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "Choose the idiom that means 'to work very hard'.",
            'answer_format': 'text',
            'correct': 'work like a dog',
            'explanation': "'Work like a dog' means to work extremely hard.",
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'infosys',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['infosys_idioms', 'infosys_phrases'],
            'proof_questions': [{
            'id': 'infy-p1',
            'prompt': "Infosys: Choose the idiom for 'to reveal a secret'.",
            'answer_format': 'text',
            'correct': 'spill the beans',
            'explanation': "'Spill the beans' means to reveal a secret.",
            'time_limit_seconds': 60,
            'company_tags': ['infosys']
        }]
        }],
            'misconceptions': [{
            'code': 'verbal_vocabulary_context',
            'signature': 'Student interprets idioms literally instead of figuratively.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_figurative_meaning'
        }, {
            'code': 'verbal_vocabulary_context',
            'signature': 'Student picks an idiom that fits grammatically but not contextually.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_context_driven_selection'
        }],
            'srs_key_points': ['Idioms are figurative, not literal.', 'Learn idioms as fixed chunks.', 'Match meaning to context.', 'Common themes: action, emotion, time, decision.', 'Context decides which idiom fits.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'verbal',
            'competency_id': 'idioms_and_phrases',
            'unlocks_next': [],
            'tower_badge': 'verbal_idioms_and_phrases'
        }
        }

SLUG = 'verbal.idioms_phrases'
