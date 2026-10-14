"""Lesson module — Microsoft — Growth Mindset + Technical"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'company.microsoft',
            'module_id': 'company.microsoft',
            'title': 'Microsoft — Growth Mindset + Technical',
            'description': "Microsoft interviews test growth mindset, collaboration, and technical depth in DSA, system design, and coding. Satya Nadella's era emphasizes learning agility.",
            'difficulty': 'hard',
            'est_minutes': 60,
            'xp_reward': 100,
            'skills_taught': ['Microsoft Interview'],
            'srs_concept_tag': 'company.microsoft',
            'domain': 'company',
            'captain_byte': {
            'intro': "Microsoft values growth mindset and collaboration. Let's prepare both.",
            'correct': ['Growth mindset!', 'Collaborative!', 'Technical depth!'],
            'wrong': ['Show learning from failure.', 'Emphasize teamwork over hero culture.'],
            'after_break': "Microsoft expects you to learn from mistakes. Let's build that story.",
            'after_mastery': "You're Microsoft-ready. Prove it with DSA + collaboration stories.",
            'retry_prompt': 'Refine your story with more learning.'
        },
            'story_context': {
            'title': 'Microsoft — Growth Mindset + Technical',
            'narration': "Microsoft interviews test growth mindset, collaboration, and technical depth in DSA, system design, and coding. Satya Nadella's era emphasizes learning agility.",
            'setting': 'microsoft_interview',
            'character': 'Captain Byte',
            'intro_text': "Microsoft interviews test growth mindset, collaboration, and technical depth in DSA, system design, and coding. Satya Nadella's era emphasizes learning agility."
        },
            'steps': {
            'discover': {
            'prompt': 'Microsoft interview has 3-4 rounds: Phone Screen (coding), Onsite (DSA + system design + behavioral).',
            'question': "What is Microsoft's core cultural value under Satya Nadella?",
            'options': ['Growth Mindset', 'Move Fast', 'Disagree and Commit', 'Customer Obsession'],
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': "Growth mindset = belief that abilities can be developed. Microsoft asks: 'Tell me about a time you learned something difficult.'",
            'explanation': 'Microsoft values learning agility over raw IQ. They want to see how you handle failure and feedback.',
            'interaction_kind': 'read_explanation'
        },
            'manipulate': {
            'prompt': "Match the Microsoft value to the question: 'Tell me about a time you received critical feedback' → ?",
            'matches': {
            'Critical feedback': 'Growth mindset',
            'Team conflict': 'Collaboration + diversity',
            'Ambiguous project': 'Ambiguity tolerance',
            'Mistake and recovery': 'Learning agility'
        },
            'interaction_kind': 'match_relationships'
        },
            'predict': {
            'prompt': "Microsoft asks 'Describe a time you failed'. What are they testing?",
            'answer': 'Growth mindset + learning agility',
            'options': ['Technical skill', 'Growth mindset + learning agility', 'Culture fit', 'Leadership'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': 'Write a growth mindset story: a time you learned a difficult technology under pressure.',
            'answer': 'S: Production system needed real-time analytics. T: I owned the pipeline. A: Learned Kafka in 3 days, built the pipeline, added monitoring. R: Reduced reporting lag from 24h to 5 min.',
            'explanation': 'Shows rapid learning, ownership, and measurable impact.',
            'interaction_kind': 'text_input'
        },
            'break_step': {
            'prompt': "What is wrong with 'I failed a project but learned from it'?",
            'common_mistake': 'Vague. No specific failure, no specific learning, no metric.',
            'correct_reasoning': 'Microsoft wants: specific failure, specific learning, specific improvement.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': "Improve: 'I made a mistake in a project and learned to be more careful.'",
            'improved_answer': 'I shipped a bug that affected 10K users. I learned to add integration tests and staged rollouts. Now my team has 95% test coverage and zero production bugs in 6 months.',
            'interaction_kind': 'text_input'
        },
            'retrieval': {
            'prompt': "What is Microsoft's 'growth mindset' principle?",
            'answer': 'Abilities can be developed through dedication and hard work.',
            'alternative': ['Learn and improve continuously'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Write a collaboration story: a time you resolved a technical disagreement with a peer.',
            'answer': 'S: Two engineers disagreed on DB schema. T: I was the tech lead. A: I proposed a benchmark, ran both designs, showed trade-offs. R: Team agreed on the better design, shipped in 1 sprint.',
            'explanation': 'Shows collaboration, data-driven decisions, and leadership.',
            'interaction_kind': 'text_input'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': "Microsoft value: 'Disagree and commit' means what?",
            'answer': 'Debate openly, then commit fully to the decision',
            'options': ['Always agree', 'Debate then commit', 'Avoid conflict', 'Follow orders'],
            'explanation': 'Healthy debate + full commitment = Disagree and Commit.',
            'difficulty': 'easy',
            'company_tags': ['microsoft']
        }],
            'proof': [{
            'id': 'ms-p1',
            'prompt': 'Timed Microsoft simulation: Tell me about a time you had to learn something new quickly. 3 min to answer.',
            'answer_format': 'text',
            'correct': 'any STAR story with rapid learning',
            'explanation': 'Microsoft values learning agility. Show concrete learning steps.',
            'time_limit_seconds': 180,
            'company_tags': ['microsoft']
        }],
            'company_variants': [{
            'company': 'microsoft',
            'role': 'sde',
            'difficulty': 'medium',
            'proof_questions': []
        }],
            'misconceptions': [],
            'srs_key_points': ['Microsoft values growth mindset above all.', 'Learning agility > raw IQ.', 'Have STAR stories for: failure, feedback, ambiguity, collaboration.', 'Quantify learning: time to competency, impact of new skill.', 'Collaboration > hero culture.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'company',
            'competency_id': 'microsoft_interview',
            'unlocks_next': [],
            'tower_badge': 'company_microsoft_interview'
        }
        }

SLUG = 'company.microsoft'
