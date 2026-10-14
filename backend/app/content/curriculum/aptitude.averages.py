"""Lesson module — Averages"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'aptitude.averages',
            'module_id': 'aptitude.averages',
            'title': 'Averages',
            'description': 'Average problems appear in every service-company quantitative section. They test your ability to handle weighted sums and missing values — a core data interpretation skill.',
            'difficulty': 'easy',
            'est_minutes': 18,
            'xp_reward': 100,
            'skills_taught': ['Averages'],
            'srs_concept_tag': 'aptitude.averages',
            'domain': 'aptitude',
            'captain_byte': {
            'intro': "Averages aren't just mean — they're weighted sums in disguise. Let's see why.",
            'correct': ['Spot on!', 'Exactly!', 'You nailed it!'],
            'wrong': ['Think about the total sum and total count.', 'Remember: average = total sum / total count.'],
            'after_break': "The trap was assuming simple average. Let's fix it.",
            'after_mastery': "You now see averages as weighted sums. That's a permanent advantage.",
            'retry_prompt': "Try again. You're close."
        },
            'story_context': {
            'title': 'Averages',
            'narration': 'Average problems appear in every service-company quantitative section. They test your ability to handle weighted sums and missing values — a core data interpretation skill.',
            'setting': 'averages',
            'character': 'Captain Byte',
            'intro_text': 'Average problems appear in every service-company quantitative section. They test your ability to handle weighted sums and missing values — a core data interpretation skill.'
        },
            'steps': {
            'discover': {
            'prompt': 'Read this problem. What is the average?',
            'question': 'Find the average of 10, 20, 30, 40, 50.',
            'options': ['25', '30', '35', '40'],
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'Average = Sum of all values ÷ Number of values.',
            'explanation': 'Sum = 10+20+30+40+50 = 150. Count = 5. Average = 150/5 = 30.',
            'interaction_kind': 'read_explanation'
        },
            'manipulate': {
            'prompt': 'Find the average of 5, 15, 25, 35.',
            'answer': '20',
            'hint': 'Sum = 80, count = 4, average = 20',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'If a 6th number 60 is added to the set, what is the new average?',
            'answer': '30',
            'options': ['25', '30', '35', '40'],
            'interaction_kind': 'numeric_input'
        },
            'build': {
            'prompt': 'A student scored 80, 90, 70 in 3 subjects. What is the average?',
            'answer': '80',
            'explanation': '(80+90+70)/3 = 240/3 = 80.',
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': 'A student calculates (80+90+70)/2 = 120. What is wrong?',
            'common_mistake': 'Dividing by 2 instead of 3 (wrong count).',
            'correct_reasoning': 'There are 3 subjects, so divide by 3: 240/3 = 80.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix this: average = (80+90+70)/2',
            'correct_formula': 'average = (80+90+70)/3',
            'interaction_kind': 'formula_fix'
        },
            'retrieval': {
            'prompt': 'What is the formula for average?',
            'answer': 'Sum of values / Count of values',
            'alternative': ['Total sum ÷ number of items'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'The average of 5 numbers is 20. A 6th number is added and the new average is 25. What is the 6th number?',
            'answer': '50',
            'explanation': 'Old sum = 5×20 = 100. New sum = 6×25 = 150. 6th number = 150-100 = 50.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Average of first 10 natural numbers?',
            'answer': '5.5',
            'options': ['5', '5.5', '6', '6.5'],
            'explanation': 'Sum = 55, count = 10, average = 5.5.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'The average of 8 numbers is 15. If each number is multiplied by 2, what is the new average?',
            'answer_format': 'numeric',
            'correct': '30',
            'explanation': 'If each value doubles, the average doubles: 15 × 2 = 30.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: Average of 3 consecutive even numbers is 14. Find the largest.',
            'answer_format': 'numeric',
            'correct': '16',
            'explanation': 'Numbers are 12, 14, 16. Average = 14. Largest = 16.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'apt_average_denominator_error',
            'signature': 'Student averages numbers without weighting by count.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_weighted_sum'
        }],
            'srs_key_points': ['Average = Total sum ÷ Count.', 'Adding a value changes the average based on how far it is from the current average.', 'If all values are multiplied by k, the average is multiplied by k.', 'Missing value = (New average × New count) - Old sum.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'aptitude',
            'competency_id': 'averages',
            'unlocks_next': [],
            'tower_badge': 'aptitude_averages'
        }
        }

SLUG = 'aptitude.averages'
