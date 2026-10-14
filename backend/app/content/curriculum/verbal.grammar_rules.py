"""Lesson module — Grammar Rules — Tenses and Voice"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'verbal.grammar_rules',
            'module_id': 'verbal.grammar_rules',
            'title': 'Grammar Rules — Tenses and Voice',
            'description': 'Grammar rules form the backbone of English proficiency tests in TCS, Infosys, and Wipro.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Grammar Rules'],
            'srs_concept_tag': 'verbal.grammar_rules',
            'domain': 'verbal',
            'captain_byte': {
            'intro': 'Grammar keeps sentences consistent. Tense marks time. Voice marks who acts and who receives.',
            'correct': ['Correct tense.', 'Right voice.', 'Consistent time.'],
            'wrong': ['Keep tense consistent in one sentence.', 'Passive voice swaps subject and object.', "Use 'be' + past participle for passive."],
            'after_break': 'You found the grammar error. Now fix the tense or voice.',
            'after_mastery': "You can now apply grammar rules fast. That's placement-ready verbal skill.",
            'retry_prompt': 'Try again. Check tense consistency first.'
        },
            'story_context': {
            'title': 'Grammar Rules — Tenses and Voice',
            'narration': 'Grammar rules form the backbone of English proficiency tests in TCS, Infosys, and Wipro.',
            'setting': 'grammar_rules',
            'character': 'Captain Byte',
            'intro_text': 'Grammar rules form the backbone of English proficiency tests in TCS, Infosys, and Wipro.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_tense',
            'narration': "Identify the tense: 'She writes code every day.'",
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What tense is this?',
            'options': [{
            'id': 'a',
            'text': 'Past',
            'correct': False
        }, {
            'id': 'b',
            'text': 'Present Simple',
            'correct': True
        }, {
            'id': 'c',
            'text': 'Future',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Present Continuous',
            'correct': False
        }],
            'explanation': "'Writes' with 'every day' is Present Simple."
        }
        }, {
            'action': 'see_voice',
            'narration': "Active: 'The cat chased the mouse.' Passive: 'The mouse was chased by the cat.'",
            'interaction': {
            'type': 'choose_outcome',
            'prompt': "Convert to passive: 'The chef cooked the meal.'",
            'options': [{
            'id': 'a',
            'text': 'The meal was cooked by the chef.',
            'correct': True
        }, {
            'id': 'b',
            'text': 'The chef was cooked by the meal.',
            'correct': False
        }, {
            'id': 'c',
            'text': 'The meal is cooked by the chef.',
            'correct': False
        }, {
            'id': 'd',
            'text': 'The chef is cooking the meal.',
            'correct': False
        }],
            'explanation': "Passive swaps subject and object and uses 'be' + past participle."
        }
        }],
            'conclusion': 'Tense marks time. Voice marks who acts. Active: subject acts. Passive: subject receives. Keep tense consistent within a sentence.'
        },
            'understand': "Tenses: Past, Present, Future, each with Simple, Continuous, Perfect, Perfect Continuous. Voice: Active (subject acts), Passive (subject receives). Passive uses 'be' + past participle.",
            'manipulate': {
            'prompt': "Change to passive: 'The dog bit the mailman.'",
            'answer': 'The mailman was bitten by the dog.',
            'hint': "Swap subject and object. Use past tense of 'be' + past participle.",
            'interaction_kind': 'text_fix'
        },
            'predict': {
            'prompt': "Choose the correct tense: 'By next year, I ___ my degree.'",
            'answer': 'will have completed',
            'options': ['complete', 'will complete', 'will have completed', 'am completing'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': "Rewrite in active voice: 'The letter was mailed by Rama.'",
            'answer': 'Rama mailed the letter.',
            'explanation': "Swap subject and object, remove 'by'.",
            'interaction_kind': 'text_fix'
        },
            'break_step': {
            'prompt': "A student writes 'The meal was cook by the chef.' What is wrong?",
            'common_mistake': "Using base verb instead of past participle after 'was'.",
            'correct_reasoning': "Passive requires past participle: 'was cooked'.",
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix: 'The meal was cook by the chef.'",
            'correct_reasoning': "Use 'was cooked' (past participle).",
            'interaction_kind': 'text_fix'
        },
            'retrieval': {
            'prompt': 'What is the structure of passive voice?',
            'answer': 'Be + past participle',
            'alternative': ['subject + be + past participle'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': "Rewrite in passive: 'They will build the bridge next year.'",
            'answer': 'The bridge will be built next year.',
            'explanation': 'Future passive: will + be + past participle.',
            'interaction_kind': 'text_fix'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': "Choose the correct passive: 'The cake ___ by the baker.' (bake)",
            'answer': 'was baked',
            'options': ['baked', 'was baked', 'is baked', 'has baked'],
            'explanation': 'Past passive: was + past participle.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': "Identify the tense: 'I have been waiting since morning.'",
            'answer': 'Present Perfect Continuous',
            'options': ['Present Perfect', 'Present Perfect Continuous', 'Past Continuous', 'Future Perfect'],
            'explanation': "'Have been waiting' indicates Present Perfect Continuous.",
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "Rewrite in passive voice: 'The committee will approve the plan tomorrow.'",
            'answer_format': 'text',
            'correct': 'The plan will be approved tomorrow.',
            'explanation': 'Future passive: will + be + past participle.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'infosys',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['infosys_grammar_tenses', 'infosys_voice_rules'],
            'proof_questions': [{
            'id': 'infy-p1',
            'prompt': "Infosys: Choose the correct tense: 'By 2025, India ___ the largest digital economy.'",
            'answer_format': 'text',
            'correct': 'will have become',
            'explanation': 'Future perfect: will + have + past participle.',
            'time_limit_seconds': 90,
            'company_tags': ['infosys']
        }]
        }],
            'misconceptions': [{
            'code': 'verbal_tense_misuse',
            'signature': 'Student mixes past and present in the same sentence.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_tense_timeline'
        }, {
            'code': 'verbal_grammar_agreement',
            'signature': 'Student does not know when to use active vs passive voice.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_subject_object_swap'
        }],
            'srs_key_points': ['Tense marks time: Past, Present, Future.', 'Passive voice: be + past participle.', 'Active voice: subject acts.', 'Passive voice: subject receives.', 'Keep tense consistent within a sentence.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'verbal',
            'competency_id': 'grammar_rules',
            'unlocks_next': [],
            'tower_badge': 'verbal_grammar_rules'
        }
        }

SLUG = 'verbal.grammar_rules'
