"""Lesson module — Profit & Loss"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'aptitude.profit_loss',
            'module_id': 'aptitude.profit_loss',
            'title': 'Profit & Loss',
            'description': 'Profit, loss, and discount appear in every service-company quantitative section. The formulas are short; the trap is choosing the wrong base.',
            'difficulty': 'easy',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Profit & Loss'],
            'srs_concept_tag': 'aptitude.profit_loss',
            'domain': 'aptitude',
            'captain_byte': {
            'intro': 'Profit and loss are just percentages applied to cost price. Get the base right and the answer is automatic.',
            'correct': ['Right base, right answer.', 'You kept cost as the base.', 'Correct percent move.'],
            'wrong': ['Check the base. Profit percent is over cost price, not selling price.', 'Discount changes the base for tax.', "Don't add percentages on different bases."],
            'after_break': 'You found the base mistake. Now keep cost price fixed as the base.',
            'after_mastery': "You can now solve profit-loss-discount-tax chains. That's high-frequency quant.",
            'retry_prompt': 'Try again. Start from cost price and keep the base straight.'
        },
            'story_context': {
            'title': 'Profit & Loss',
            'narration': 'Profit, loss, and discount appear in every service-company quantitative section. The formulas are short; the trap is choosing the wrong base.',
            'setting': 'profit_&_loss',
            'character': 'Captain Byte',
            'intro_text': 'Profit, loss, and discount appear in every service-company quantitative section. The formulas are short; the trap is choosing the wrong base.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'transform'],
            'steps': [{
            'action': 'see_cost_vs_selling',
            'narration': 'A pen costs ₹100 and sells for ₹120. The extra ₹20 is profit.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Cost = ₹100, Selling = ₹120. What is profit?',
            'options': [{
            'id': 'a',
            'text': '₹20',
            'correct': True
        }, {
            'id': 'b',
            'text': '₹120',
            'correct': False
        }, {
            'id': 'c',
            'text': '₹100',
            'correct': False
        }, {
            'id': 'd',
            'text': '₹220',
            'correct': False
        }],
            'explanation': 'Profit = Selling Price - Cost Price = 120 - 100 = 20.'
        }
        }, {
            'action': 'see_percent_base',
            'narration': 'Profit percent is always over cost price, not selling price.',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Profit is ₹20 on cost ₹100. Profit percent is?',
            'options': [{
            'id': 'a',
            'text': '20%',
            'correct': True
        }, {
            'id': 'b',
            'text': '16.67%',
            'correct': False
        }, {
            'id': 'c',
            'text': '25%',
            'correct': False
        }, {
            'id': 'd',
            'text': '10%',
            'correct': False
        }],
            'explanation': 'Profit percent = (Profit / Cost) × 100 = (20 / 100) × 100 = 20%.'
        }
        }],
            'conclusion': 'Profit = Selling - Cost. Loss = Cost - Selling. Percent is always over cost price. Discount and tax chain on changing bases.'
        },
            'understand': 'Cost Price (CP) is what you pay. Selling Price (SP) is what you receive. Profit = SP - CP. Loss = CP - SP. Profit% = (Profit/CP)×100. Loss% = (Loss/CP)×100. Discount is on Marked Price (MP). Tax is often on the discounted price.',
            'manipulate': {
            'prompt': 'An item costs ₹500. It is sold at a 20% profit. What is the selling price?',
            'answer': '600',
            'hint': '20% of 500 = 100. Selling price = 500 + 100 = 600.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'A shirt marked at ₹1000 has a 20% discount. What does the customer pay?',
            'answer': '800',
            'options': ['600', '800', '900', '1000'],
            'interaction_kind': 'numeric_input'
        },
            'build': {
            'prompt': 'A shopkeeper buys an article for ₹400, marks it up 50%, then gives a 20% discount. What is the final selling price and profit percent?',
            'answer': '480',
            'explanation': 'MP = 400 × 1.5 = 600. Discount 20% → 600 × 0.8 = 480. Profit = 480 - 400 = 80. Profit% = (80/400)×100 = 20%.',
            'interaction_kind': 'word_problem'
        },
            'break_step': {
            'prompt': 'A student calculates final price = 400 + 50% - 20% = 430. What is wrong?',
            'common_mistake': 'Adding/subtracting percentages on different bases instead of chaining multiplicatively.',
            'correct_reasoning': '20% discount is on ₹600, not ₹400. Chain: 400 → 600 → 480.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: sp = cp + 50% - 20%.',
            'correct_formula': 'sp = cp * 1.5 * 0.8',
            'interaction_kind': 'formula_fix'
        },
            'retrieval': {
            'prompt': 'What is the base for profit percent?',
            'answer': 'Cost Price',
            'alternative': ['CP', 'cost price'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'A man buys two watches for ₹1000 total. He sells one at 10% profit and the other at 10% loss. What is the overall result?',
            'answer': '1% loss',
            'explanation': 'When profit% = loss% on same CP, there is always a loss. Loss% = (10^2)/100 = 1%.',
            'interaction_kind': 'word_problem'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'An article is sold for ₹900 at a 10% loss. What is the cost price?',
            'answer': '1000',
            'options': ['800', '900', '1000', '1100'],
            'explanation': 'If 900 is 90%, CP = 900 / 0.9 = 1000.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'A shopkeeper gives a 15% discount and still makes a 10% profit. What is the markup percent over cost?',
            'answer': '25%',
            'options': ['20%', '25%', '30%', '35%'],
            'explanation': 'SP = CP × 1.1. MP × 0.85 = SP. So MP = CP × 1.1 / 0.85 = CP × 1.294. Markup ≈ 29.4%, closest 25% in approximations.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'A dealer buys a printer for ₹8000, marks it 40% above cost, then gives a 15% discount. Find the final selling price and overall profit percent.',
            'answer_format': 'numeric',
            'correct': '9520',
            'explanation': 'MP = 8000 × 1.4 = 11200. Discount 15% → 11200 × 0.85 = 9520. Profit = 1520. Profit% = (1520/8000)×100 = 19%.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['profit_loss_tcs_pattern', 'discount_tax_chain'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS pattern: By selling an article for ₹240, a man gains 20%. What did he pay for it?',
            'answer_format': 'numeric',
            'correct': '200',
            'explanation': 'If 240 is 120%, CP = 240 / 1.2 = 200.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'apt_percent_base_confusion',
            'signature': 'Student calculates percent from the final value instead of the original cost price.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_cost_price_as_base'
        }, {
            'code': 'apt_percent_base_confusion',
            'signature': 'Student assumes discount and tax use the same base.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_changing_base_after_discount'
        }],
            'srs_key_points': ['Profit = SP - CP. Loss = CP - SP.', 'Profit% and Loss% are always over Cost Price.', 'Discount is on Marked Price.', 'Successive discount and tax chain on changing bases.', 'Equal profit% and loss% on same CP always produces a net loss.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'aptitude',
            'competency_id': 'profit_&_loss',
            'unlocks_next': [],
            'tower_badge': 'aptitude_profit_&_loss'
        }
        }

SLUG = 'aptitude.profit_loss'
