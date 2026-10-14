"""Lesson module — Cloze Test"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'verbal.cloze_test',
            'module_id': 'verbal.cloze_test',
            'title': 'Cloze Test',
            'description': 'Cloze tests measure grammar, vocabulary, and coherence. They are common in TCS NQT and Infosys English sections.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Cloze Test'],
            'srs_concept_tag': 'verbal.cloze_test',
            'domain': 'verbal',
            'captain_byte': {
            'intro': 'Cloze tests hide missing words in a passage. Choose words that keep grammar and meaning coherent.',
            'correct': ['Contextually correct.', 'Grammar and meaning fit.', 'Right word choice.'],
            'wrong': ['Read the whole passage before filling blanks.', 'Check tense and meaning together.', 'Eliminate words that break coherence.'],
            'after_break': 'You found the wrong word. Now fix the blank and re-read for flow.',
            'after_mastery': "You can now complete cloze passages fast. That's placement-ready verbal skill.",
            'retry_prompt': 'Try again. Read the surrounding sentences before choosing.'
        },
            'story_context': {
            'title': 'Cloze Test',
            'narration': 'Cloze tests measure grammar, vocabulary, and coherence. They are common in TCS NQT and Infosys English sections.',
            'setting': 'cloze_test',
            'character': 'Captain Byte',
            'intro_text': 'Cloze tests measure grammar, vocabulary, and coherence. They are common in TCS NQT and Infosys English sections.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_blank',
            'narration': 'The cat sat on the ___. (mat, runs, quickly)',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Choose the correct word.',
            'options': [{
            'id': 'a',
            'text': 'mat',
            'correct': True
        }, {
            'id': 'b',
            'text': 'runs',
            'correct': False
        }, {
            'id': 'c',
            'text': 'quickly',
            'correct': False
        }, {
            'id': 'd',
            'text': 'the',
            'correct': False
        }],
            'explanation': "Noun needed after 'the'. 'Mat' fits."
        }
        }, {
            'action': 'see_flow',
            'narration': 'She ___ to the store, ___ some milk, and ___ home. (walked, bought, walked)',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Fill all blanks with the correct tense.',
            'options': [{
            'id': 'a',
            'text': 'walked, buy, walked',
            'correct': False
        }, {
            'id': 'b',
            'text': 'walked, bought, walked',
            'correct': True
        }, {
            'id': 'c',
            'text': 'walks, buys, walks',
            'correct': False
        }, {
            'id': 'd',
            'text': 'walking, buying, walking',
            'correct': False
        }],
            'explanation': 'Past tense is needed for all three actions.'
        }
        }],
            'conclusion': 'Cloze tests check grammar, vocabulary, and coherence. Read the whole passage. Check tense and meaning together.'
        },
            'understand': 'Cloze passages hide words. Each blank needs a word that is grammatically correct and contextually coherent. Check tense, part of speech, and passage meaning.',
            'manipulate': {
            'prompt': "Fill: 'The ___ team won the ___ match.' (our, over)",
            'answer': 'our, overall',
            'hint': "Possessive adjective, then adverb meaning 'in general'.",
            'interaction_kind': 'fill_blank'
        },
            'predict': {
            'prompt': "Fill: 'She is ___ in mathematics.' (interest, interesting, interested)",
            'answer': 'interested',
            'options': ['interest', 'interesting', 'interested', 'interests'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': "Fill: 'The ___ of the project was delayed due to ___ planning.' (completion, inadequate)",
            'answer': 'completion, inadequate',
            'explanation': 'Noun then adjective describing planning.',
            'interaction_kind': 'fill_blank'
        },
            'break_step': {
            'prompt': "A student fills 'The cat sat on the runs.' What is wrong?",
            'common_mistake': 'Choosing a verb where a noun is required.',
            'correct_reasoning': "'On the' requires a noun. 'Runs' is a verb.",
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix: 'The cat sat on the runs.'",
            'correct_reasoning': "Use a noun: 'The cat sat on the mat.'",
            'interaction_kind': 'text_fix'
        },
            'retrieval': {
            'prompt': 'What should you check before filling a cloze blank?',
            'answer': 'Grammar and context',
            'alternative': ['part of speech', 'tense', 'passage meaning'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': "Fill: 'The ___ results ___ the hypothesis.' (amazing, confirm)",
            'answer': 'amazing, confirm',
            'explanation': 'Adjective then verb matching plural subject.',
            'interaction_kind': 'fill_blank'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': "Fill: 'He is ___ than his brother.' (tall, taller, tallest)",
            'answer': 'taller',
            'options': ['tall', 'taller', 'tallest', 'more tall'],
            'explanation': 'Comparative degree for two people.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': "Fill: 'The news ___ breaking.' (is, are, were, has)",
            'answer': 'is',
            'options': ['is', 'are', 'were', 'has'],
            'explanation': "'News' is singular uncountable.",
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "Fill: 'Despite ___ weather, the event was a ___.' (rain, success)",
            'answer_format': 'text',
            'correct': 'rain, success',
            'explanation': 'Noun then noun expressing outcome.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'infosys',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['infosys_cloze_test', 'infosys_english_blanks'],
            'proof_questions': [{
            'id': 'infy-p1',
            'prompt': "Infosys: Fill the blank with the correct word: 'The committee ___ decided on the proposal.' (has, have, is, are)",
            'answer_format': 'text',
            'correct': 'has',
            'explanation': "'Committee' is singular collective noun.",
            'time_limit_seconds': 60,
            'company_tags': ['infosys']
        }]
        }],
            'misconceptions': [{
            'code': 'verbal_vocabulary_context',
            'signature': 'Student picks a word that fits grammatically but breaks passage meaning.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_context_coherence'
        }, {
            'code': 'verbal_tense_misuse',
            'signature': 'Student ignores tense consistency across blanks.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_tense_chain_across_sentences'
        }],
            'srs_key_points': ['Read the whole passage first.', 'Check part of speech for each blank.', 'Keep tense consistent.', 'Choose words that preserve meaning.', 'Eliminate options that break grammar or coherence.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'verbal',
            'competency_id': 'cloze_test',
            'unlocks_next': [],
            'tower_badge': 'verbal_cloze_test'
        }
        }

SLUG = 'verbal.cloze_test'
