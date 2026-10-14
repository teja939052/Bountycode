"""Lesson module — Sentence Correction"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'verbal.sentence_correction',
            'module_id': 'verbal.sentence_correction',
            'title': 'Sentence Correction',
            'description': 'Sentence correction tests grammar and clarity under time pressure. It appears in the English section of TCS NQT and Infosys.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Sentence Correction'],
            'srs_concept_tag': 'verbal.sentence_correction',
            'domain': 'verbal',
            'captain_byte': {
            'intro': 'Sentence correction is pattern matching for grammar. Find the part that breaks the rule.',
            'correct': ['Correct error identified.', 'Right grammar rule.', 'Fixed sentence flows.'],
            'wrong': ['Check subject-verb agreement.', 'Check tense consistency.', 'Check preposition use.'],
            'after_break': 'You found the grammar break. Now fix it without changing meaning.',
            'after_mastery': "You can now spot and fix grammar errors fast. That's placement-ready verbal skill.",
            'retry_prompt': 'Try again. Read the sentence aloud and listen for the awkward part.'
        },
            'story_context': {
            'title': 'Sentence Correction',
            'narration': 'Sentence correction tests grammar and clarity under time pressure. It appears in the English section of TCS NQT and Infosys.',
            'setting': 'sentence_correction',
            'character': 'Captain Byte',
            'intro_text': 'Sentence correction tests grammar and clarity under time pressure. It appears in the English section of TCS NQT and Infosys.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_error',
            'narration': "Find the error in: 'The list of items are on the table.'",
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Which part is wrong?',
            'options': [{
            'id': 'a',
            'text': 'The list of items are',
            'correct': True
        }, {
            'id': 'b',
            'text': 'on the table',
            'correct': False
        }, {
            'id': 'c',
            'text': 'No error',
            'correct': False
        }, {
            'id': 'd',
            'text': 'The list',
            'correct': False
        }],
            'explanation': "'List' is singular, so the verb should be 'is', not 'are'."
        }
        }, {
            'action': 'see_correction',
            'narration': "Corrected sentence: 'The list of items is on the table.'",
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What is the correction?',
            'options': [{
            'id': 'a',
            'text': 'is',
            'correct': True
        }, {
            'id': 'b',
            'text': 'are',
            'correct': False
        }, {
            'id': 'c',
            'text': 'was',
            'correct': False
        }, {
            'id': 'd',
            'text': 'were',
            'correct': False
        }],
            'explanation': "Use 'is' to match the singular subject 'list'."
        }
        }],
            'conclusion': 'Errors usually hide in subject-verb agreement, tense, prepositions, or modifiers. Read the sentence aloud; the wrong part sounds awkward.'
        },
            'understand': 'Common error types: subject-verb agreement, tense sequence, preposition choice, modifier placement, and parallel structure. The subject is the true doer of the action; ignore prepositional phrases between subject and verb.',
            'manipulate': {
            'prompt': "Correct: 'She don't like coffee.'",
            'answer': "She doesn't like coffee.",
            'hint': "Third-person singular present needs 'doesn't'.",
            'interaction_kind': 'text_fix'
        },
            'predict': {
            'prompt': "Find the error: 'Each of the students have submitted their assignments.'",
            'answer': 'have',
            'options': ['Each', 'have', 'their', 'No error'],
            'interaction_kind': 'mcq_identify'
        },
            'build': {
            'prompt': "Correct the sentence: 'The manager, along with his team, are attending the conference.'",
            'answer': 'is attending',
            'explanation': "'Manager' is the subject; 'along with his team' is parenthetical. Singular subject takes 'is'.",
            'interaction_kind': 'text_fix'
        },
            'break_step': {
            'prompt': "A student says 'The manager... are attending' is correct because 'team' is plural. What is wrong?",
            'common_mistake': "Ignoring that the subject is 'manager', not 'team'.",
            'correct_reasoning': "Parenthetical phrases do not change subject number. 'Manager' is singular.",
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix: 'The manager, along with his team, are attending.'",
            'correct_reasoning': "Use 'is' because the subject 'manager' is singular.",
            'interaction_kind': 'text_fix'
        },
            'retrieval': {
            'prompt': "What is the subject-verb agreement rule for 'each of'?",
            'answer': "Singular verb: 'Each of the students is'.",
            'alternative': ['Each takes a singular verb'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': "Correct: 'Neither the teacher nor the students were present.'",
            'answer': 'was present',
            'explanation': "With 'neither...nor', the verb agrees with the nearer subject. 'Students' is nearer, so plural 'were' is actually acceptable, but formal grammar often prefers proximity rule: 'students were' is correct.",
            'interaction_kind': 'text_fix'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': "Find the error: 'The news are broadcast at 6 PM.'",
            'answer': 'are',
            'options': ['The news', 'are', 'broadcast', 'No error'],
            'explanation': "'News' is uncountable singular. Use 'is'.",
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': "Correct: 'If I was you, I would accept the offer.'",
            'answer': 'were',
            'options': ['was', 'were', 'am', 'be'],
            'explanation': "Subjunctive mood uses 'were' for hypotheticals.",
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "Correct the sentence: 'The committee have decided to postpone the meeting.'",
            'answer_format': 'text',
            'correct': 'has decided',
            'explanation': "'Committee' is a collective singular noun in American English. Use 'has'.",
            'time_limit_seconds': 60,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'infosys',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['infosys_english_grammar', 'infosys_sentence_ordering'],
            'proof_questions': [{
            'id': 'infy-p1',
            'prompt': 'Infosys pattern: Choose the correct sentence.',
            'answer_format': 'text',
            'correct': 'The data shows a clear trend.',
            'explanation': "'Data' as a collective singular takes a singular verb in formal English.",
            'time_limit_seconds': 60,
            'company_tags': ['infosys']
        }]
        }],
            'misconceptions': [{
            'code': 'verbal_grammar_agreement',
            'signature': 'Student ignores subject-verb agreement with collective nouns or inverted clauses.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_subject_verb_pairs'
        }, {
            'code': 'verbal_tense_misuse',
            'signature': 'Student mixes tenses in reported speech or conditional clauses.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_direct_indirect_mapping'
        }],
            'srs_key_points': ['Subject-verb agreement: singular subject + singular verb.', "'Each', 'every', 'neither...nor' take singular verbs.", 'Parenthetical phrases do not change subject number.', "Subjunctive mood uses 'were' for hypotheticals.", 'Tense must be consistent in clauses.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'verbal',
            'competency_id': 'sentence_correction',
            'unlocks_next': [],
            'tower_badge': 'verbal_sentence_correction'
        }
        }

SLUG = 'verbal.sentence_correction'
