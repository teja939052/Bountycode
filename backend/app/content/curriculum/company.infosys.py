"""Lesson module — Infosys InfyTQ — Complete Preparation"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'company.infosys',
            'module_id': 'company.infosys',
            'title': 'Infosys InfyTQ — Complete Preparation',
            'description': 'Infosys InfyTQ is the gateway for campus placements. It tests quant, reasoning, verbal, and hands-on coding with a focus on problem-solving speed.',
            'difficulty': 'medium',
            'est_minutes': 110,
            'xp_reward': 100,
            'skills_taught': ['Infosys InfyTQ'],
            'srs_concept_tag': 'company.infosys',
            'domain': 'company',
            'captain_byte': {
            'intro': "Infosys InfyTQ is speed + accuracy. Let's build both.",
            'correct': ['Infosys pattern!', 'On track!', 'Speed building!'],
            'wrong': ['Focus on accuracy first, then speed.', 'Infosys loves percentages and data interpretation.'],
            'after_break': "Infosys has tricky DI sets. Let's master them.",
            'after_mastery': "You're InfyTQ-ready. Prove it under timed conditions.",
            'retry_prompt': 'Review the pattern and retry.'
        },
            'story_context': {
            'title': 'Infosys InfyTQ — Complete Preparation',
            'narration': 'Infosys InfyTQ is the gateway for campus placements. It tests quant, reasoning, verbal, and hands-on coding with a focus on problem-solving speed.',
            'setting': 'infosys_infytq',
            'character': 'Captain Byte',
            'intro_text': 'Infosys InfyTQ is the gateway for campus placements. It tests quant, reasoning, verbal, and hands-on coding with a focus on problem-solving speed.'
        },
            'steps': {
            'discover': {
            'prompt': 'Infosys InfyTQ sections: Quantitative (20 Q), Reasoning (15 Q), Verbal (20 Q), Coding (1 hands-on). Total ~90 min.',
            'question': 'Which section has hands-on coding?',
            'options': ['Quant', 'Reasoning', 'Verbal', 'Coding'],
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Infosys pattern: high weight on DI (Data Interpretation) in Quant. Reasoning has puzzles and coding-decoding. Verbal hasReading Comprehension + grammar.',
            'explanation': 'Infosys DI sets have 5 questions per table. Speed comes from mastering the table-reading pattern.',
            'interaction_kind': 'read_explanation'
        },
            'manipulate': {
            'prompt': 'Match the pattern to the section: DI Table → ? Coding-Decoding → ? RC → ?',
            'matches': {
            'DI Table': 'Quant',
            'Coding-Decoding': 'Reasoning',
            'RC': 'Verbal',
            'Arrays': 'Coding'
        },
            'interaction_kind': 'match_relationships'
        },
            'predict': {
            'prompt': 'Infosys DI sets often have 5 questions per table. If you spend 3 min per table, can you finish 4 tables in 20 min?',
            'answer': 'No',
            'options': ['Yes', 'No', 'Maybe', 'Depends'],
            'interaction_kind': 'mcq_bottleneck'
        },
            'build': {
            'prompt': 'Build a 2-week plan for Infosys: daily 2 hours. Focus on DI and coding.',
            'answer': 'Week 1: DI + Reasoning. Week 2: Verbal + Coding + mocks.',
            'explanation': 'DI has highest pattern density. Coding is only 1 question but high marks.',
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': "A student skips Verbal because 'it's easy'. What is wrong?",
            'common_mistake': 'Verbal has 20 questions and a cutoff. Skipping it risks disqualification.',
            'correct_reasoning': 'Verbal cutoff is typically 80%+. Easy marks, but you need to attempt.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix this plan: 'Only study Quant and skip Verbal.'",
            'correct_plan': 'Quant (35%) + Reasoning (25%) + Verbal (25%) + Coding (15%). All sections matter.',
            'interaction_kind': 'word_problem'
        },
            'retrieval': {
            'prompt': "What is Infosys InfyTQ's coding section format?",
            'answer': '1 hands-on coding problem, 45 min, 2 test cases, Python/Java/C++',
            'alternative': ['1 problem, 45 min, compile on 2 test cases'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': "You have 45 min for 1 coding problem. Allocate time: read (5 min), plan (10 min), code (25 min), test (5 min). What's left?",
            'answer': '0',
            'explanation': '5+10+25+5 = 45. No buffer. Practice to reduce coding time.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Infosys: How many questions in Quant?',
            'answer': '20',
            'options': ['15', '20', '25', '30'],
            'explanation': 'Infosys Quant has 20 questions.',
            'difficulty': 'easy',
            'company_tags': ['infosys']
        }],
            'proof': [{
            'id': 'infy-p1',
            'prompt': 'Timed Infosys simulation: 8 DI questions in 12 minutes. Score ≥ 6 to pass.',
            'answer_format': 'mcq',
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct': '0',
            'explanation': 'Simulated Infosys DI pattern.',
            'time_limit_seconds': 720,
            'company_tags': ['infosys']
        }],
            'company_variants': [{
            'company': 'infosys',
            'role': 'sde',
            'difficulty': 'medium',
            'proof_questions': []
        }],
            'misconceptions': [],
            'srs_key_points': ['Infosys InfyTQ: 4 sections, ~90 min.', 'DI sets have 5 questions per table.', 'Coding: 1 hands-on problem, 45 min, 2 test cases.', 'Verbal has 20 questions and a cutoff.', 'Speed comes from pattern familiarity, not raw IQ.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'company',
            'competency_id': 'infosys_infytq',
            'unlocks_next': [],
            'tower_badge': 'company_infosys_infytq'
        }
        }

SLUG = 'company.infosys'
