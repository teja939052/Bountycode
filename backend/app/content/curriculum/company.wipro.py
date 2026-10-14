"""Lesson module — Wipro NLTH — Complete Preparation"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'company.wipro',
            'module_id': 'company.wipro',
            'title': 'Wipro NLTH — Complete Preparation',
            'description': 'Wipro NLTH (National Level Tech Hunt) is a mass-recruitment test. It tests quant, reasoning, and coding with a focus on speed and accuracy.',
            'difficulty': 'medium',
            'est_minutes': 100,
            'xp_reward': 100,
            'skills_taught': ['Wipro NLTH'],
            'srs_concept_tag': 'company.wipro',
            'domain': 'company',
            'captain_byte': {
            'intro': "Wipro NLTH is speed + accuracy. Let's master the patterns.",
            'correct': ['Wipro pattern!', 'On track!', 'Speed building!'],
            'wrong': ['Focus on quant and reasoning first.', 'Coding is only 1 question but high marks.'],
            'after_break': "Wipro loves time-speed-distance. Let's master it.",
            'after_mastery': "You're NLTH-ready. Prove it under timed conditions.",
            'retry_prompt': 'Review the pattern and retry.'
        },
            'story_context': {
            'title': 'Wipro NLTH — Complete Preparation',
            'narration': 'Wipro NLTH (National Level Tech Hunt) is a mass-recruitment test. It tests quant, reasoning, and coding with a focus on speed and accuracy.',
            'setting': 'wipro_nlth',
            'character': 'Captain Byte',
            'intro_text': 'Wipro NLTH (National Level Tech Hunt) is a mass-recruitment test. It tests quant, reasoning, and coding with a focus on speed and accuracy.'
        },
            'steps': {
            'discover': {
            'prompt': 'Wipro NLTH sections: Quant (50 Q, 60 min), Reasoning (40 Q, 40 min), Coding (1 Q, 30 min), Verbal (20 Q, 20 min). Total ~150 min.',
            'question': 'Which section has the most questions?',
            'options': ['Quant', 'Reasoning', 'Coding', 'Verbal'],
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Wipro NLTH pattern: high volume, moderate difficulty. Time management is critical. Quant has 50 questions in 60 min = 1.2 min per question.',
            'explanation': 'Wipro tests breadth over depth. You need speed + basic accuracy. Negative marking: 1/4 per wrong answer.',
            'interaction_kind': 'read_explanation'
        },
            'manipulate': {
            'prompt': 'Match the pattern to the section: Time/Speed/Distance → ? Syllogism → ? Synonyms → ?',
            'matches': {
            'Time/Speed/Distance': 'Quant',
            'Syllogism': 'Reasoning',
            'Synonyms': 'Verbal',
            'Two Pointers': 'Coding'
        },
            'interaction_kind': 'match_relationships'
        },
            'predict': {
            'prompt': 'Wipro has 50 Quant questions in 60 min. If you spend 2 min per question, how many minutes left?',
            'answer': '-40',
            'options': ['0', '-40', '40', '20'],
            'interaction_kind': 'numeric_input'
        },
            'build': {
            'prompt': 'Build a strategy for Wipro NLTH: 50 Quant in 60 min. What is max time per question?',
            'answer': '1.2',
            'explanation': '60 min = 3600 seconds. 3600/50 = 72 seconds = 1.2 min per question.',
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': 'A student spends 3 min per Quant question. What is wrong?',
            'common_mistake': "Wipro Quant is speed-based. 3 min per question means you won't finish.",
            'correct_reasoning': 'Max time per Quant question is 1.2 min. Practice speed.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Fix this strategy: 'Solve all Quant questions carefully, no time limit.'",
            'correct_strategy': 'Quant: 1 min/question, skip hard ones, return later. Accuracy > 70%.',
            'interaction_kind': 'word_problem'
        },
            'retrieval': {
            'prompt': "What is Wipro NLTH's negative marking?",
            'answer': '1/4 mark deducted per wrong answer',
            'alternative': ['Minus 0.25 per wrong'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Wipro Reasoning has 40 questions in 40 min. What is max time per question in seconds?',
            'answer': '60',
            'explanation': '40 min = 2400 seconds. 2400/40 = 60 seconds per question.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Wipro: How many total questions?',
            'answer': '111',
            'options': ['100', '111', '120', '90'],
            'explanation': '50 Quant + 40 Reasoning + 20 Verbal + 1 Coding = 111.',
            'difficulty': 'easy',
            'company_tags': ['wipro']
        }],
            'proof': [{
            'id': 'wipro-p1',
            'prompt': 'Timed Wipro simulation: 15 mixed quant/reasoning questions in 18 minutes. Score ≥ 10 to pass.',
            'answer_format': 'mcq',
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct': '0',
            'explanation': 'Simulated Wipro pattern.',
            'time_limit_seconds': 1080,
            'company_tags': ['wipro']
        }],
            'company_variants': [{
            'company': 'wipro',
            'role': 'sde',
            'difficulty': 'medium',
            'proof_questions': []
        }],
            'misconceptions': [],
            'srs_key_points': ['Wipro NLTH: 111 questions, ~150 min.', 'Quant: 50 Q in 60 min (1.2 min/Q).', 'Reasoning: 40 Q in 40 min (1 min/Q).', 'Negative marking: -1/4 per wrong.', 'Speed is critical. Practice with timers.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'company',
            'competency_id': 'wipro_nlth',
            'unlocks_next': [],
            'tower_badge': 'company_wipro_nlth'
        }
        }

SLUG = 'company.wipro'
