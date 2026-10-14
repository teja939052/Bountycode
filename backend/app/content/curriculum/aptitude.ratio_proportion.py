"""Lesson module — Ratio & Proportion"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'aptitude.ratio_proportion',
            'module_id': 'aptitude.ratio_proportion',
            'title': 'Ratio & Proportion',
            'description': 'Ratio and proportion are foundational for every quantitative section in TCS, Infosys, and Wipro. They unlock mixtures, partnerships, and scaling problems.',
            'difficulty': 'easy',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Ratio & Proportion'],
            'srs_concept_tag': 'aptitude.ratio_proportion',
            'domain': 'aptitude',
            'captain_byte': {
            'intro': 'Ratios are just relationships between quantities. Proportions say two relationships are equal. Master both and half of quant becomes mechanical.',
            'correct': ["That's the relationship.", 'You compared the right parts.', 'Correct proportion.'],
            'wrong': ['Ratios compare parts, not totals.', 'Check whether you are equating the right pairs.', "Don't cross-multiply blindly."],
            'after_break': 'You found the broken assumption. Now fix the relation and the answer falls out.',
            'after_mastery': "You can now compare, scale, and mix quantities. That's placement-ready ratio skill.",
            'retry_prompt': 'Try again. Keep the relationship structure before calculating.'
        },
            'story_context': {
            'title': 'Ratio & Proportion',
            'narration': 'Ratio and proportion are foundational for every quantitative section in TCS, Infosys, and Wipro. They unlock mixtures, partnerships, and scaling problems.',
            'setting': 'ratio_&_proportion',
            'character': 'Captain Byte',
            'intro_text': 'Ratio and proportion are foundational for every quantitative section in TCS, Infosys, and Wipro. They unlock mixtures, partnerships, and scaling problems.'
        },
            'steps': {
            'discover': {
            'prompt': 'A recipe uses 2 cups flour for 3 cups water. If you use 8 cups flour, how many cups water?',
            'question': 'Is the answer 12 because 8/2 = 4 and 3*4 = 12?',
            'options': ['Yes', 'No', 'Only if flour is doubled twice', 'Cannot say'],
            'interaction_kind': 'mcq_read'
        },
            'understand': 'A ratio a:b compares quantities. A proportion states a:b = c:d. Cross-multiplication works only when the relation is truly proportional. Scaling multiplies both sides by the same factor.',
            'manipulate': {
            'prompt': 'If A/B = 3/4 and B = 20, what is A?',
            'answer': '15',
            'hint': 'Cross multiply: A = 3 * B / 4.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'If 5 workers finish a job in 12 days, 10 workers take about how many days (assuming linear)?',
            'answer': '6',
            'options': ['24', '12', '6', '3'],
            'interaction_kind': 'mcq_bottleneck'
        },
            'build': {
            'prompt': 'Write a function scaled_quantity(original_a, original_b, new_a) returning new_b keeping the same ratio.',
            'answer': 'def scaled_quantity(original_a, original_b, new_a):\n    return new_a * original_b / original_a',
            'explanation': 'Keep the ratio constant by cross multiplication.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'Why is `new_b = new_a * original_a / original_b` wrong?',
            'broken_code': 'new_b = new_a * original_a / original_b',
            'expected_failure': 'Inverts the ratio relationship.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the ratio inversion.',
            'correct_code': 'new_b = new_a * original_b / original_a',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'What does it mean for two ratios to be in proportion?',
            'answer': 'Their cross products are equal.',
            'alternative': ['a*d = b*c'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'If 7 machines make 210 widgets in 5 days, how many widgets do 10 machines make in 7 days?',
            'answer': '420',
            'explanation': 'Machine-days are constant: 7*5 = 35 machine-days per 210 widgets.',
            'interaction_kind': 'numeric_input'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'If 3:4 :: 6:x, what is x?',
            'answer': '8',
            'options': ['6', '7', '8', '9'],
            'explanation': 'Cross multiply: 3*x = 4*6.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }, {
            'kind': 'numeric',
            'prompt': 'A:B = 5:7, B=14. Find A.',
            'answer': '10',
            'explanation': 'A = 5*14/7.',
            'difficulty': 'medium',
            'company_tags': ['tcs']
        }],
            'proof': [{
            'id': 'p1-state_the_condition_for_two_ratios_to_be',
            'prompt': 'State the condition for two ratios to be in proportion.',
            'answer_format': 'text',
            'correct': 'Cross products are equal.',
            'explanation': 'a/b = c/d implies a*d = b*c.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['ratio_partnership', 'ratio_mixture'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: A:B = 3:4, B:C = 5:6, C:D = 4:5. Find A:D.',
            'answer_format': 'text',
            'correct': '1:2',
            'explanation': 'Chain ratios: A=3×5×4=60, B=4×5×4=80, C=4×6×4=96, D=5×6×5=150. A:D = 60:150 = 2:5.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'apt_ratio_interpretation_error',
            'signature': 'Student inverts ratio or confuses part-to-part with part-to-whole.',
            'reteach_route': 'visual_state',
            'reteach_action': 'show_ratio_as_division'
        }],
            'srs_key_points': ['Ratio compares two quantities; proportion equates two ratios.', 'Cross-multiply to test or solve proportions.', 'Scaling preserves the ratio.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'aptitude',
            'competency_id': 'ratio_&_proportion',
            'unlocks_next': [],
            'tower_badge': 'aptitude_ratio_&_proportion'
        }
        }

SLUG = 'aptitude.ratio_proportion'
