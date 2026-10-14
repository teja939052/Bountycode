"""Lesson module — Vocabulary — Synonyms & Antonyms"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'verbal.vocabulary',
            'module_id': 'verbal.vocabulary',
            'title': 'Vocabulary — Synonyms & Antonyms',
            'description': 'Vocabulary questions test word meanings quickly. They appear in the English section of TCS NQT and Infosys.',
            'difficulty': 'easy',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Vocabulary'],
            'srs_concept_tag': 'verbal.vocabulary',
            'domain': 'verbal',
            'captain_byte': {
            'intro': 'Vocabulary is meaning matching. Read the sentence, then pick the word that fits the context.',
            'correct': ['Right word.', 'Context matches meaning.', 'Correct synonym/antonym.'],
            'wrong': ['Read the whole sentence before choosing.', 'Check whether the word is positive or negative.', 'Eliminate words that change the meaning.'],
            'after_break': 'You found the wrong meaning. Now match the word to the sentence context.',
            'after_mastery': "You can now match vocabulary quickly. That's placement-ready verbal skill.",
            'retry_prompt': 'Try again. Read the full sentence and match the tone.'
        },
            'story_context': {
            'title': 'Vocabulary — Synonyms & Antonyms',
            'narration': 'Vocabulary questions test word meanings quickly. They appear in the English section of TCS NQT and Infosys.',
            'setting': 'vocabulary',
            'character': 'Captain Byte',
            'intro_text': 'Vocabulary questions test word meanings quickly. They appear in the English section of TCS NQT and Infosys.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_synonym',
            'narration': "Find the synonym of 'rapid' in context.",
            'interaction': {
            'type': 'choose_outcome',
            'prompt': "Choose the synonym of 'rapid'.",
            'options': [{
            'id': 'a',
            'text': 'Slow',
            'correct': False
        }, {
            'id': 'b',
            'text': 'Quick',
            'correct': True
        }, {
            'id': 'c',
            'text': 'Late',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Heavy',
            'correct': False
        }],
            'explanation': "'Rapid' means quick."
        }
        }, {
            'action': 'see_antonym',
            'narration': "Find the antonym of 'ancient' in context.",
            'interaction': {
            'type': 'choose_outcome',
            'prompt': "Choose the antonym of 'ancient'.",
            'options': [{
            'id': 'a',
            'text': 'Old',
            'correct': False
        }, {
            'id': 'b',
            'text': 'Modern',
            'correct': True
        }, {
            'id': 'c',
            'text': 'Historic',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Ancient',
            'correct': False
        }],
            'explanation': "'Modern' is opposite of 'ancient'."
        }
        }],
            'conclusion': 'Synonyms match meaning. Antonyms oppose meaning. Always check sentence context before choosing.'
        },
            'understand': 'Vocabulary questions test synonym, antonym, and context meaning. Read the full sentence. Eliminate words that change tone or factual meaning. Prefixes and suffixes often hint at meaning.',
            'manipulate': {
            'prompt': "Choose the synonym of 'benevolent'.",
            'answer': 'Kind',
            'hint': 'Bene- means good. -volent means wishing.',
            'interaction_kind': 'mcq_classify'
        },
            'predict': {
            'prompt': "Choose the antonym of 'transient'.",
            'answer': 'Permanent',
            'options': ['Temporary', 'Permanent', 'Fleeting', 'Brief'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': "Fill in the blank: 'The CEO delivered a ___ speech that inspired the team.' (choose between dull, rousing, mediocre)",
            'answer': 'Rousing',
            'explanation': "Inspired implies positive tone. 'Rousing' fits.",
            'interaction_kind': 'mcq_classify'
        },
            'break_step': {
            'prompt': "A student chooses 'rapid' as an antonym of 'slow'. What is wrong?",
            'common_mistake': 'Confusing synonym with antonym.',
            'correct_reasoning': "'Rapid' means quick, which is similar to fast, not opposite of slow.",
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix: choose 'rapid' as antonym of 'slow'.",
            'correct_reasoning': 'Antonym of slow is fast or quick. Rapid is a synonym.',
            'interaction_kind': 'mcq_diagnose'
        },
            'retrieval': {
            'prompt': 'What is an antonym?',
            'answer': 'A word with opposite meaning',
            'alternative': ['opposite meaning'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': "Choose the word closest in meaning to 'ephemeral'.",
            'answer': 'Fleeting',
            'explanation': "'Ephemeral' means short-lived. 'Fleeting' matches.",
            'interaction_kind': 'mcq_classify'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': "Synonym of 'gloomy'?",
            'answer': 'Dark',
            'options': ['Bright', 'Dark', 'Cheerful', 'Light'],
            'explanation': "'Gloomy' means dark or depressing.",
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': "Antonym of 'benevolent'?",
            'answer': 'Malevolent',
            'options': ['Kind', 'Malevolent', 'Generous', 'Helpful'],
            'explanation': "'Malevolent' means wishing harm; opposite of benevolent.",
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "Choose the word that best fits: 'The ___ evidence cleared the suspect.' (inculpatory, exculpatory, culpable)",
            'answer_format': 'text',
            'correct': 'exculpatory',
            'explanation': "'Exculpatory' means clearing from guilt.",
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'infosys',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['infosys_vocabulary', 'infosys_synonyms_antonyms'],
            'proof_questions': [{
            'id': 'infy-p1',
            'prompt': "Infosys: Choose the synonym of 'pragmatic'.",
            'answer_format': 'text',
            'correct': 'practical',
            'explanation': "'Pragmatic' means dealing with things practically.",
            'time_limit_seconds': 60,
            'company_tags': ['infosys']
        }]
        }],
            'misconceptions': [{
            'code': 'verbal_vocabulary_context',
            'signature': 'Student picks a synonym without checking sentence context.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_context_before_meaning'
        }, {
            'code': 'verbal_vocabulary_context',
            'signature': 'Student chooses a word that sounds similar but means something different.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'highlight_similar_sounding_different_meaning'
        }],
            'srs_key_points': ['Synonym = same meaning. Antonym = opposite meaning.', 'Read the full sentence before choosing.', 'Prefixes and suffixes hint at meaning.', 'Eliminate words that change tone.', 'Context decides meaning, not dictionary alone.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'verbal',
            'competency_id': 'vocabulary',
            'unlocks_next': [],
            'tower_badge': 'verbal_vocabulary'
        }
        }

SLUG = 'verbal.vocabulary'
