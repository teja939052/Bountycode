"""Lesson module — Reading Comprehension"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'verbal.reading_comprehension',
            'module_id': 'verbal.reading_comprehension',
            'title': 'Reading Comprehension',
            'description': 'Reading comprehension measures how fast and accurately you can extract meaning from a passage. It is a staple of TCS NQT, Infosys, and Wipro English sections.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Reading Comprehension'],
            'srs_concept_tag': 'verbal.reading_comprehension',
            'domain': 'verbal',
            'captain_byte': {
            'intro': 'Reading comprehension is evidence hunting. Every answer must be justified by a line in the passage.',
            'correct': ['Answer is in the passage.', 'You linked claim to evidence.', 'Right inference.'],
            'wrong': ['Stick to the passage. Do not bring outside facts.', 'Find the sentence that supports the answer.', 'Inference must follow from the passage, not outside knowledge.'],
            'after_break': 'You found the broken assumption. Now stick to passage evidence only.',
            'after_mastery': "You can now read fast and answer accurately. That's placement-ready RC skill.",
            'retry_prompt': 'Try again. Find the exact sentence that supports your answer.'
        },
            'story_context': {
            'title': 'Reading Comprehension',
            'narration': 'Reading comprehension measures how fast and accurately you can extract meaning from a passage. It is a staple of TCS NQT, Infosys, and Wipro English sections.',
            'setting': 'reading_comprehension',
            'character': 'Captain Byte',
            'intro_text': 'Reading comprehension measures how fast and accurately you can extract meaning from a passage. It is a staple of TCS NQT, Infosys, and Wipro English sections.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_main_idea',
            'narration': 'Read the passage. What is the main idea?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What is the main idea of the passage?',
            'options': [{
            'id': 'a',
            'text': 'Urban farming reduces food miles.',
            'correct': True
        }, {
            'id': 'b',
            'text': 'Cities should ban cars.',
            'correct': False
        }, {
            'id': 'c',
            'text': 'Rural areas are declining.',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Technology harms society.',
            'correct': False
        }],
            'explanation': 'The passage focuses on urban farming as a way to reduce distance from farm to consumer.'
        }
        }, {
            'action': 'see_inference',
            'narration': 'The passage says urban farms use 90% less transport. What can you infer?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What can be inferred from the passage?',
            'options': [{
            'id': 'a',
            'text': 'Urban farms lower carbon footprint.',
            'correct': True
        }, {
            'id': 'b',
            'text': 'All cities should become farms.',
            'correct': False
        }, {
            'id': 'c',
            'text': 'Rural farming is obsolete.',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Transport is the only cost.',
            'correct': False
        }],
            'explanation': 'Less transport implies lower emissions, but the passage does not claim rural farming is obsolete.'
        }
        }],
            'conclusion': 'RC answers are either directly stated or logically inferred from the passage. Never use outside knowledge.'
        },
            'understand': 'Reading comprehension asks for main idea, specific detail, inference, or tone. Every answer must be grounded in the passage. Direct questions are verbatim or lightly paraphrased. Inference questions require one logical step from the text.',
            'manipulate': {
            'prompt': "Passage: 'Urban farms reduce transport distance by 90%.' Question: What is the passage mainly about?",
            'answer': 'Reducing transport distance through urban farming',
            'hint': 'Look for the central theme, not a side detail.',
            'interaction_kind': 'short_answer'
        },
            'predict': {
            'prompt': "If the passage mentions 'food miles' and 'local consumption', what is the likely tone?",
            'answer': 'Supportive',
            'options': ['Critical', 'Supportive', 'Neutral', 'Sarcastic'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': 'Write a 2-sentence summary of a passage about urban farming reducing transport emissions.',
            'answer': 'Urban farming brings food production closer to consumers. This reduces transport distance and associated emissions.',
            'explanation': 'Summary captures main idea and key supporting detail.',
            'interaction_kind': 'short_answer'
        },
            'break_step': {
            'prompt': "A student answers 'All cities should become farms' for an inference question. What is wrong?",
            'common_mistake': 'Taking a specific claim and generalizing beyond the passage.',
            'correct_reasoning': 'The passage mentions urban farms, not universal conversion of cities.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix: infer 'All cities should become farms' from 'Urban farms reduce transport'.",
            'correct_reasoning': 'Inference must be one logical step from the passage. Universal claims require universal evidence.',
            'interaction_kind': 'mcq_diagnose'
        },
            'retrieval': {
            'prompt': 'What are the four main RC question types?',
            'answer': 'Main idea, detail, inference, tone',
            'alternative': ['main idea', 'specific detail', 'inference', 'tone'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'A new passage says remote work cuts commuting emissions. Which inference is valid?',
            'answer': 'Remote work can reduce urban congestion.',
            'explanation': 'Less commuting implies fewer cars on the road.',
            'interaction_kind': 'mcq_classify'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'According to the passage, what reduces food miles?',
            'answer': 'Urban farming',
            'options': ['Rural farming', 'Urban farming', 'Importing food', 'Supermarkets'],
            'explanation': 'The passage directly links urban farming to reduced transport distance.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': "The author's tone toward urban farming is best described as?",
            'answer': 'Optimistic',
            'options': ['Critical', 'Optimistic', 'Neutral', 'Sarcastic'],
            'explanation': 'The passage presents benefits without strong negatives, suggesting optimism.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "A passage states: 'Local food systems cut average transport from 1500 km to 150 km.' What conclusion is best supported?",
            'answer_format': 'text',
            'correct': 'Local systems reduce transport distance by 90%',
            'explanation': 'This is a direct numerical inference from the passage.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'infosys',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['infosys_rc_passages', 'infosys_inference_hard'],
            'proof_questions': [{
            'id': 'infy-p1',
            'prompt': 'Infosys pattern: Passage discusses renewable energy adoption. Which inference is valid?',
            'answer_format': 'text',
            'correct': 'Renewable adoption is growing but faces infrastructure challenges.',
            'explanation': 'Valid inference must be directly supported by passage statements.',
            'time_limit_seconds': 90,
            'company_tags': ['infosys']
        }]
        }],
            'misconceptions': [{
            'code': 'verbal_inference_error',
            'signature': 'Student rushes and picks an option that sounds familiar rather than provable from the passage.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_evidence_based_answer'
        }, {
            'code': 'verbal_inference_error',
            'signature': 'Student uses real-world knowledge instead of passage evidence.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'highlight_passage_scope_only'
        }],
            'srs_key_points': ['Main idea is the central theme, not a detail.', 'Specific detail questions require exact passage support.', 'Inference needs one logical step from the text.', "Tone is the author's attitude, not the student's opinion.", 'Never use outside knowledge in RC.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'verbal',
            'competency_id': 'reading_comprehension',
            'unlocks_next': [],
            'tower_badge': 'verbal_reading_comprehension'
        }
        }

SLUG = 'verbal.reading_comprehension'
