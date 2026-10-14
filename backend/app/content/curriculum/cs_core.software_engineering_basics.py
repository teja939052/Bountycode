"""Lesson module — Software Engineering Basics"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'cs_core.software_engineering_basics',
            'module_id': 'cs_core.software_engineering_basics',
            'title': 'Software Engineering Basics',
            'description': 'Software engineering fundamentals are asked in every technical interview. Know SDLC, testing, and design basics.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Software Engineering'],
            'srs_concept_tag': 'cs_core.software_engineering_basics',
            'domain': 'cs_core',
            'captain_byte': {
            'intro': 'Software engineering is systematic development. SDLC guides the process. Testing ensures quality.',
            'correct': ['Right phase.', 'Correct model.', 'Right testing type.'],
            'wrong': ['SDLC has multiple models.', 'Testing is part of engineering, not an afterthought.', 'Agile is iterative; waterfall is sequential.'],
            'after_break': 'You found the SE error. Now fix the model or phase.',
            'after_mastery': "You can now reason about software engineering. That's interview-ready CS skill.",
            'retry_prompt': 'Try again. Check the SDLC phase before answering.'
        },
            'story_context': {
            'title': 'Software Engineering Basics',
            'narration': 'Software engineering fundamentals are asked in every technical interview. Know SDLC, testing, and design basics.',
            'setting': 'software_engineering',
            'character': 'Captain Byte',
            'intro_text': 'Software engineering fundamentals are asked in every technical interview. Know SDLC, testing, and design basics.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_sdlc',
            'narration': 'SDLC phases: Requirements, Design, Implementation, Testing, Deployment, Maintenance.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Which phase comes after Design?',
            'options': [{
            'id': 'a',
            'text': 'Requirements',
            'correct': False
        }, {
            'id': 'b',
            'text': 'Implementation',
            'correct': True
        }, {
            'id': 'c',
            'text': 'Testing',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Deployment',
            'correct': False
        }],
            'explanation': 'Implementation (coding) follows Design.'
        }
        }, {
            'action': 'see_testing',
            'narration': 'Unit, integration, system, acceptance — testing levels.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Which testing checks individual components?',
            'options': [{
            'id': 'a',
            'text': 'Unit testing',
            'correct': True
        }, {
            'id': 'b',
            'text': 'Integration testing',
            'correct': False
        }, {
            'id': 'c',
            'text': 'System testing',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Acceptance testing',
            'correct': False
        }],
            'explanation': 'Unit testing checks individual components in isolation.'
        }
        }],
            'conclusion': 'SDLC guides development. Testing has multiple levels. Agile is iterative. Waterfall is sequential. Version control tracks changes.'
        },
            'understand': 'SDLC models: Waterfall, Agile, Spiral, Iterative. Testing levels: unit, integration, system, acceptance. Version control tracks code changes. Code review improves quality.',
            'manipulate': {
            'prompt': 'What is the purpose of unit testing?',
            'answer': 'Test individual components in isolation',
            'hint': 'Think smallest testable unit.',
            'interaction_kind': 'short_answer'
        },
            'predict': {
            'prompt': 'Which SDLC model is iterative?',
            'answer': 'Agile',
            'options': ['Waterfall', 'Agile', 'Both', 'Neither'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': 'List the six SDLC phases in order.',
            'answer': 'Requirements, Design, Implementation, Testing, Deployment, Maintenance',
            'explanation': 'Standard waterfall order.',
            'interaction_kind': 'ordering'
        },
            'break_step': {
            'prompt': 'A student says testing happens after deployment. What is wrong?',
            'common_mistake': 'Confusing deployment with testing phase.',
            'correct_reasoning': 'Testing happens before deployment in standard SDLC.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: testing happens after deployment.',
            'correct_reasoning': 'Testing happens before deployment.',
            'interaction_kind': 'mcq_diagnose'
        },
            'retrieval': {
            'prompt': 'What does SDLC stand for?',
            'answer': 'Software Development Life Cycle',
            'alternative': ['software development lifecycle'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'A team needs fast releases and customer feedback. Which model?',
            'answer': 'Agile',
            'explanation': 'Agile supports iterative releases and continuous feedback.',
            'interaction_kind': 'mcq_classify'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Which testing level tests the full system?',
            'answer': 'System testing',
            'options': ['Unit testing', 'Integration testing', 'System testing', 'Acceptance testing'],
            'explanation': 'System testing validates the complete integrated system.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'Which SDLC model is sequential?',
            'answer': 'Waterfall',
            'options': ['Waterfall', 'Agile', 'Spiral', 'Iterative'],
            'explanation': 'Waterfall is linear and sequential.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'Explain the difference between unit testing and integration testing.',
            'answer_format': 'text',
            'correct': 'Unit tests individual components. Integration tests interactions between components.',
            'explanation': 'Unit is isolated. Integration checks combined behavior.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_sdlc', 'tcs_testing_basics'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: What is the difference between black-box and white-box testing?',
            'answer_format': 'text',
            'correct': 'Black-box tests functionality without internal knowledge. White-box tests internal structures.',
            'explanation': 'Black-box = functional. White-box = structural.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'cs_core_normalization_misconception',
            'signature': 'Student thinks testing is only manual and not part of engineering.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_testing_as_engineering_activity'
        }, {
            'code': 'cs_core_process_thread_confusion',
            'signature': 'Student thinks only waterfall model exists.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_multiple_sdlc_models'
        }],
            'srs_key_points': ['SDLC guides software development.', 'Waterfall is sequential. Agile is iterative.', 'Testing levels: unit, integration, system, acceptance.', 'Version control tracks code changes.', 'Code review improves quality.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'cs_core',
            'competency_id': 'software_engineering',
            'unlocks_next': [],
            'tower_badge': 'cs_core_software_engineering'
        }
        }

SLUG = 'cs_core.software_engineering_basics'
