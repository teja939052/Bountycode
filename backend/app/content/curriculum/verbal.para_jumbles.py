"""Lesson module — Para Jumbles"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'verbal.para_jumbles',
            'module_id': 'verbal.para_jumbles',
            'title': 'Para Jumbles',
            'description': 'Para jumbles test logical sequencing and coherence. They are a staple of TCS NQT and Infosys English sections.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Para Jumbles'],
            'srs_concept_tag': 'verbal.para_jumbles',
            'domain': 'verbal',
            'captain_byte': {
            'intro': 'Para jumbles are sentence puzzles. Find the opening, then follow the links.',
            'correct': ['Correct order.', 'You found the link.', 'Right sequence.'],
            'wrong': ['Find the opening sentence first.', 'Follow pronouns and connectors.', 'Eliminate options that break the flow.'],
            'after_break': 'You found the broken link. Now rebuild the chain.',
            'after_mastery': "You can now order paragraphs fast. That's placement-ready verbal skill.",
            'retry_prompt': 'Try again. Identify the opening sentence first.'
        },
            'story_context': {
            'title': 'Para Jumbles',
            'narration': 'Para jumbles test logical sequencing and coherence. They are a staple of TCS NQT and Infosys English sections.',
            'setting': 'para_jumbles',
            'character': 'Captain Byte',
            'intro_text': 'Para jumbles test logical sequencing and coherence. They are a staple of TCS NQT and Infosys English sections.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_opening',
            'narration': 'Which sentence opens a paragraph about climate change?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Choose the opening sentence.',
            'options': [{
            'id': 'a',
            'text': 'Climate change is accelerating.',
            'correct': True
        }, {
            'id': 'b',
            'text': 'Therefore, emissions must fall.',
            'correct': False
        }, {
            'id': 'c',
            'text': 'For example, glaciers are melting.',
            'correct': False
        }, {
            'id': 'd',
            'text': 'However, policies remain weak.',
            'correct': False
        }],
            'explanation': 'The opening states the main idea. The others depend on it.'
        }
        }, {
            'action': 'see_link',
            'narration': "Sentence B mentions 'this trend'. Which sentence does 'this' refer to?",
            'interaction': {
            'type': 'choose_outcome',
            'prompt': "Which sentence does 'this trend' refer to?",
            'options': [{
            'id': 'a',
            'text': 'Climate change is accelerating.',
            'correct': True
        }, {
            'id': 'b',
            'text': 'Emissions must fall.',
            'correct': False
        }, {
            'id': 'c',
            'text': 'Glaciers are melting.',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Policies remain weak.',
            'correct': False
        }],
            'explanation': "'This trend' refers to the main idea stated in the opening."
        }
        }],
            'conclusion': 'Find the opening sentence first. Then follow pronouns, connectors, and examples. Eliminate options that break the logical flow.'
        },
            'understand': "A paragraph has an opening, body, and closing. Openers state the main idea. Connecters like 'however', 'therefore', 'for example' signal transitions. Pronouns like 'this', 'that', 'such' refer back to earlier sentences.",
            'manipulate': {
            'prompt': "Arrange: [A] 'However, the costs are high.' [B] 'Solar energy is promising.' [C] 'It requires rare materials.' [D] 'Therefore, research is ongoing.'",
            'answer': 'B A C D',
            'hint': 'Opening: Solar energy is promising. However = contrast. It = solar. Therefore = conclusion.',
            'interaction_kind': 'ordering'
        },
            'predict': {
            'prompt': 'Which sentence likely opens a paragraph about remote work?',
            'answer': 'Remote work is transforming how companies hire.',
            'options': ['Therefore, offices are empty.', 'Remote work is transforming how companies hire.', 'For example, productivity rose.', 'However, collaboration suffers.'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': "Order these sentences about AI: [1] 'AI can automate repetitive tasks.' [2] 'This raises ethical questions.' [3] 'However, bias in data is a risk.' [4] 'Therefore, regulation is needed.'",
            'answer': '1 3 2 4',
            'explanation': 'Opening → contrast → pronoun reference → conclusion.',
            'interaction_kind': 'ordering'
        },
            'break_step': {
            'prompt': "A student orders: 'Therefore...' → 'AI can automate...' → 'However...' → 'This raises...'. What is wrong?",
            'common_mistake': 'Starting with a connector instead of the opening.',
            'correct_reasoning': 'Open with the main idea, then use connectors.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix: 'Therefore...' cannot be the first sentence.",
            'correct_reasoning': 'Move the opening sentence first.',
            'interaction_kind': 'ordering'
        },
            'retrieval': {
            'prompt': 'What are the three parts of a paragraph?',
            'answer': 'Opening, body, closing',
            'alternative': ['introduction', 'development', 'conclusion'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': "Order: [A] 'Consequently, cities are investing in rail.' [B] 'Traffic congestion is rising.' [C] 'Public transit reduces cars.' [D] 'Moreover, it cuts emissions.'",
            'answer': 'B C D A',
            'explanation': 'Problem → solution → benefit → consequence.',
            'interaction_kind': 'ordering'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Which sentence opens a paragraph about renewable energy?',
            'answer': 'Renewable energy is growing faster than fossil fuels.',
            'options': ['Therefore, coal is declining.', 'Renewable energy is growing faster than fossil fuels.', 'For example, solar capacity doubled.', 'However, storage remains a challenge.'],
            'explanation': 'Opening states the main idea.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': "In 'AI is powerful. However, it is biased.', what does 'it' refer to?",
            'answer': 'AI',
            'options': ['AI', 'power', 'bias', 'data'],
            'explanation': "'It' refers to the subject of the previous sentence: AI.",
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "Order these sentences about online education: [A] 'It offers flexibility.' [B] 'Online education is expanding.' [C] 'However, self-discipline is required.' [D] 'Thus, students must manage time well.'",
            'answer_format': 'text',
            'correct': 'B A C D',
            'explanation': 'Opening → elaboration → contrast → consequence.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'infosys',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['infosys_para_jumbles', 'infosys_sentence_ordering'],
            'proof_questions': [{
            'id': 'infy-p1',
            'prompt': 'Infosys: Arrange sentences about cloud computing.',
            'answer_format': 'text',
            'correct': 'correct_order',
            'explanation': 'Opening → body → closing.',
            'time_limit_seconds': 90,
            'company_tags': ['infosys']
        }]
        }],
            'misconceptions': [{
            'code': 'verbal_inference_error',
            'signature': 'Student picks the first option because it sounds like an opening.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_opening_versus_continuation'
        }, {
            'code': 'verbal_vocabulary_context',
            'signature': 'Student ignores pronouns and connectors that bind sentences.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'highlight_pronoun_references'
        }],
            'srs_key_points': ['Opening states the main idea.', 'Follow pronouns and connectors.', "'However', 'therefore', 'for example' signal transitions.", 'Eliminate options that break logical flow.', 'Closing often summarizes or concludes.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'verbal',
            'competency_id': 'para_jumbles',
            'unlocks_next': [],
            'tower_badge': 'verbal_para_jumbles'
        }
        }

SLUG = 'verbal.para_jumbles'
