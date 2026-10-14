"""Lesson module — Blood Relations"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'aptitude.blood_relations',
            'module_id': 'aptitude.blood_relations',
            'title': 'Blood Relations',
            'description': 'Blood Relations is a high-weight reasoning topic in TCS NQT, Infosys, and Wipro. It tests your ability to map family trees quickly under time pressure.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Blood Relations'],
            'srs_concept_tag': 'aptitude.blood_relations',
            'domain': 'aptitude',
            'captain_byte': {
            'intro': "Blood Relations is a mapping problem. Let's build a family tree in your head.",
            'correct': ['Tree built!', 'Correct relationship!', 'You mapped it right!'],
            'wrong': ["Redraw the tree. Maternal = mother's side.", 'Check gender: aunt vs uncle.'],
            'after_break': "The gender/maternal-paternal trap is common. Let's fix it.",
            'after_mastery': 'You now map family trees fast. This saves minutes in every reasoning section.',
            'retry_prompt': 'Try again. Build the tree step by step.'
        },
            'story_context': {
            'title': 'Blood Relations',
            'narration': 'Blood Relations is a high-weight reasoning topic in TCS NQT, Infosys, and Wipro. It tests your ability to map family trees quickly under time pressure.',
            'setting': 'blood_relations',
            'character': 'Captain Byte',
            'intro_text': 'Blood Relations is a high-weight reasoning topic in TCS NQT, Infosys, and Wipro. It tests your ability to map family trees quickly under time pressure.'
        },
            'steps': {
            'discover': {
            'prompt': 'Read this family description. Who is X to Y?',
            'question': "A is B's father. B is C's mother. How is A related to C?",
            'options': ['Grandfather', 'Father', 'Uncle', 'Brother'],
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': "Blood Relations uses a family tree. Father → child → grandchild. Maternal = mother's side. Paternal = father's side.",
            'explanation': "A is B's father (generation +1). B is C's mother (generation +1). A is C's grandfather (maternal).",
            'interaction_kind': 'read_explanation'
        },
            'manipulate': {
            'prompt': "A is B's brother. B is C's father. How is A related to C?",
            'answer': 'Uncle',
            'hint': "A is one generation above C on the father's side.",
            'interaction_kind': 'mcq_classify'
        },
            'predict': {
            'prompt': "If A is B's sister and B is C's mother, what is A to C?",
            'answer': 'Aunt',
            'options': ['Mother', 'Aunt', 'Sister', 'Cousin'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': 'Draw the tree: A is father of B and C. B is mother of D. C is father of E. How are D and E related?',
            'answer': 'Cousins',
            'explanation': "D is B's child, E is C's child. B and C are siblings. So D and E are cousins.",
            'interaction_kind': 'mcq_classify'
        },
            'break_step': {
            'prompt': 'A student says D and E are siblings. What is wrong?',
            'common_mistake': 'Confusing cousins with siblings.',
            'correct_reasoning': 'D and E have different parents (B and C), who are siblings. So D and E are cousins.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix this: 'B and C are married, so D and E are siblings.'",
            'correct_reasoning': 'B and C are siblings (both children of A), not married. D and E are cousins.',
            'interaction_kind': 'mcq_diagnose'
        },
            'retrieval': {
            'prompt': 'What is the difference between maternal and paternal?',
            'answer': "Maternal = mother's side. Paternal = father's side.",
            'alternative': ["Mother's side vs father's side"],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'A has a daughter B and a son C. B has a daughter D. C has a son E. How is D related to E?',
            'answer': 'Cousins',
            'explanation': "D is B's daughter, E is C's son. B and C are siblings. D and E are first cousins.",
            'interaction_kind': 'mcq_classify'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': "A is B's uncle. B is C's father. How is A related to C?",
            'answer': 'Great-uncle',
            'options': ['Uncle', 'Grandfather', 'Great-uncle', 'Brother'],
            'explanation': "A is B's uncle (father's brother). B is C's father. So A is C's great-uncle.",
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': "A is B's father's father. B has a daughter C. How is A related to C?",
            'answer_format': 'text',
            'correct': 'grandfather',
            'explanation': "A is B's grandfather. C is B's daughter. So A is C's great-grandfather.",
            'time_limit_seconds': 60,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': "TCS: Pointing to a photograph, A said 'He is the son of my father's brother.' How is A related to the person?",
            'answer_format': 'text',
            'correct': 'cousin',
            'explanation': "My father's brother = my uncle. His son = my cousin.",
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'apt_ratio_interpretation_error',
            'signature': 'Student mixes up maternal/paternal or gender of relations.',
            'reteach_route': 'worked_example',
            'reteach_action': 'draw_family_tree'
        }],
            'srs_key_points': ["Maternal = mother's side. Paternal = father's side.", 'Father/mother → child → grandchild (generation +1 each).', 'Siblings share parents. Cousins have parents who are siblings.', "Uncle/aunt = parent's sibling.", "Great-uncle/aunt = grandparent's sibling."],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'aptitude',
            'competency_id': 'blood_relations',
            'unlocks_next': [],
            'tower_badge': 'aptitude_blood_relations'
        }
        }

SLUG = 'aptitude.blood_relations'
