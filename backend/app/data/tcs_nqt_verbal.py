TCS_NQT_VERBAL = [
    {
        "id": "tcs_v_sc_001",
        "topic": "Sentence Completion",
        "subtopic": "Single Blank - Contrast Words",
        "difficulty": 2,
        "time_estimate_seconds": 25,
        "question": "Despite his _______ schedule, the manager always found time to _______ his team\u00e2\u20ac\u2122s concerns.",
        "options": [
            "flexible, ignore",
            "hectic, address",
            "relaxed, dismiss",
            "busy, create"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Missing the contrast signaled by 'Despite' - choosing logically inconsistent pairs",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Contrast Word Detection",
            "steps": [
                "Identify contrast word: 'Despite'",
                "First blank should be negative (challenging schedule)",
                "Second blank should be positive (addressing concerns)",
                "Only option with negative-positive pair: hectic, address"
            ]
        },
        "alternative_methods": [
            {
                "name": "Elimination by logic",
                "example": "Flexible schedule wouldn't prevent addressing concerns (illogical)"
            }
        ],
        "common_mistakes": [
            "Ignoring contrast words like despite, although, however"
        ]
    },
    {
        "id": "tcs_v_sc_002",
        "topic": "Sentence Completion",
        "subtopic": "Double Blank - Cause Effect",
        "difficulty": 2,
        "time_estimate_seconds": 25,
        "question": "Because of the _______ rainfall, the farmers faced _______ crop yields this season.",
        "options": [
            "abundant, excellent",
            "scanty, poor",
            "heavy, improved",
            "adequate, decreased"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M2",
            "desc": "Missing causal relationship - choosing pairs that don't show cause-effect",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Cause-Effect Pairing",
            "steps": [
                "Identify cause indicator: 'Because of'",
                "First blank describes rainfall amount",
                "Second blank describes result on crops",
                "Logical pair: less rainfall -> poor yields"
            ]
        },
        "alternative_methods": [
            {
                "name": "Logical consistency check",
                "example": "Scanty rainfall logically leads to poor crop yields"
            }
        ],
        "common_mistakes": [
            "Choosing pairs where both words are positive or both negative without logical connection"
        ]
    },
    {
        "id": "tcs_v_sc_003",
        "topic": "Sentence Completion",
        "subtopic": "Vocabulary in Context",
        "difficulty": 3,
        "time_estimate_seconds": 30,
        "question": "The CEO's _______ approach to problem-solving often led to innovative solutions that bypassed traditional bottlenecks.",
        "options": [
            "conservative",
            "unorthodox",
            "meticulous",
            "bureaucratic"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M3",
            "desc": "Choosing words that don't fit the context of innovation and bypassing bottlenecks",
            "distractor_index": 2
        },
        "speed_trick": {
            "name": "Context Clue Analysis",
            "steps": [
                "Context: led to innovative solutions, bypassed traditional bottlenecks",
                "Need word meaning: unconventional, creative",
                "Unorthodox means contrary to what is usual"
            ]
        },
        "alternative_methods": [
            {
                "name": "Root word analysis",
                "example": "Un- (not) + orthodox (traditional) = not traditional"
            }
        ],
        "common_mistakes": [
            "Choosing familiar words without checking context fit"
        ]
    },
    {
        "id": "tcs_v_sc_004",
        "topic": "Sentence Completion",
        "subtopic": "Idiomatic Expressions",
        "difficulty": 2,
        "time_estimate_seconds": 25,
        "question": "After months of investigation, the detective finally _______ the truth behind the mysterious disappearance.",
        "options": [
            "came across",
            "came up with",
            "came down with",
            "came upon"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M4",
            "desc": "Confusing similar phrasal verbs with different meanings",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Phrasal Verb Meaning",
            "steps": [
                "Came across = found by chance",
                "Came up with = thought of, invented",
                "Came down with = became ill",
                "Came upon = found unexpectedly",
                "Context: after investigation, found truth -> came across"
            ]
        },
        "alternative_methods": [
            {
                "name": "Process of elimination",
                "example": "Came up with doesn't fit (investigation leads to discovery, not invention)"
            }
        ],
        "common_mistakes": [
            "Choosing phrasal verbs based on similarity rather than meaning"
        ]
    },
    {
        "id": "tcs_v_sc_005",
        "topic": "Sentence Completion",
        "subtopic": "Double Blank - Definition Example",
        "difficulty": 3,
        "time_estimate_seconds": 30,
        "question": "Her _______ nature made her _______ in social situations where diplomacy was required.",
        "options": [
            "tactless, successful",
            "diplomatic, effective",
            "oblivious, uncomfortable",
            "pretentious, admired"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M5",
            "desc": "Missing the logical connection between nature and outcome in social situations",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Trait-Outcome Matching",
            "steps": [
                "Nature affects social situation outcome",
                "Diplomatic nature leads to effectiveness in diplomacy-required situations",
                "Only logical pair: diplomatic, effective"
            ]
        },
        "alternative_methods": [
            {
                "name": "Context elimination",
                "example": "Tactless nature would not lead to success in diplomacy-required situations"
            }
        ],
        "common_mistakes": [
            "Choosing pairs that sound good but lack logical relationship"
        ]
    },
    {
        "id": "tcs_v_pr_001",
        "topic": "Passage Recall",
        "subtopic": "Factual Detail Recall",
        "difficulty": 2,
        "time_estimate_seconds": 60,
        "question": "Based on the passage you just read, what was the primary reason for the company's decision to implement remote work policy?",
        "options": [
            "To reduce office rental costs",
            "To improve employee work-life balance",
            "To comply with new government regulations",
            "To access talent from different geographical locations"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M6",
            "desc": "Recalling secondary details instead of the primary reason stated in passage",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Primary Purpose Identification",
            "steps": [
                "While reading passage, identify main idea/topic sentence",
                "Look for keywords indicating reason/purpose: 'because', 'due to', 'in order to'",
                "Primary reason is usually stated early or in conclusion"
            ]
        },
        "alternative_methods": [
            {
                "name": "Eliminate specific examples",
                "example": "Cost reduction might be mentioned but isn't the primary strategic reason"
            }
        ],
        "common_mistakes": [
            "Focusing on examples or details instead of main purpose"
        ]
    },
    {
        "id": "tcs_v_pr_002",
        "topic": "Passage Recall",
        "subtopic": "Inference-Based Recall",
        "difficulty": 3,
        "time_estimate_seconds": 75,
        "question": "What can be inferred about the author's attitude toward technological advancement in education from the passage?",
        "options": [
            "The author is completely opposed to technology in education",
            "The author believes technology should supplement but not replace traditional teaching",
            "The author thinks technology will make teachers obsolete within 5 years",
            "The author is indifferent to technological changes in education"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M7",
            "desc": "Making extreme inferences not supported by moderate language in passage",
            "distractor_index": 2
        },
        "speed_trick": {
            "name": "Moderate Language Detection",
            "steps": [
                "Look for qualifying words: 'should', 'can', 'may', 'often'",
                "Avoid extremes: 'completely', 'always', 'never', 'obsolete'",
                "Inference should match tone of passage"
            ]
        },
        "alternative_methods": [
            {
                "name": "Tone analysis",
                "example": "Passage shows balanced view, not extreme opposition or enthusiasm"
            }
        ],
        "common_mistakes": [
            "Making inferences that go beyond what the passage supports"
        ]
    },
    {
        "id": "tcs_v_pr_003",
        "topic": "Passage Recall",
        "subtopic": "Vocabulary in Context Recall",
        "difficulty": 2,
        "time_estimate_seconds": 60,
        "question": "In the passage, the word 'pertinent' most nearly means:",
        "options": [
            "relevant",
            "apparent",
            "essential",
            "urgent"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M8",
            "desc": "Choosing synonyms that don't fit the specific context where word appears",
            "distractor_index": 2
        },
        "speed_trick": {
            "name": "Contextual Vocabulary",
            "steps": [
                "Reread the sentence where word appears",
                "Substitute each option and see which fits logically",
                "Pertinent = relevant to the matter at hand"
            ]
        },
        "alternative_methods": [
            {
                "name": "Process of elimination",
                "example": "Apparent means visible, essential means necessary, urgent means immediate"
            }
        ],
        "common_mistakes": [
            "Choosing words based on general meaning without context check"
        ]
    },
    {
        "id": "tcs_v_ew_001",
        "topic": "Email Writing",
        "subtopic": "Meeting Reschedule Request",
        "difficulty": 2,
        "time_estimate_seconds": 540,
        "question": "You need to reschedule a team meeting originally planned for tomorrow at 10 AM due to an urgent client visit. Write a formal email to your team members requesting to reschedule the meeting.",
        "options": [
            "Subject: Meeting Rescheduling Request\n\nDear Team,\n\nI hope this email finds you well. I am writing to inform you that our team meeting scheduled for tomorrow at 10 AM needs to be rescheduled due to an urgent client visit that requires my immediate presence.\n\nPlease let me know your availability for either later today or the day after tomorrow. I will share the updated meeting invite once I have consensus on the new time.\n\nThank you for your understanding and flexibility.\n\nBest regards,\n[Your Name]",
            "Subject: Meeting Tomorrow\n\nHey team,\n\nJust wanted to let you know that we might need to change tomorrow's meeting time because I have something come up. Let me know when you're free.\n\nThanks!\n[Your Name]",
            "Subject: Urgent: Meeting Change\n\nDear Team Members,\n\nThis is to inform you that the meeting scheduled for tomorrow at 10 AM has been cancelled due to personal reasons. Please do not attend.\n\nRegards,\n[Your Name]",
            "Subject: Meeting Reschedule\n\nDear Team,\n\nI am writing to request that we reschedule our meeting. The reason is that I have a client visit. Please suggest alternative times.\n\nSincerely,\n[Your Name]"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M9",
            "desc": "Missing key email components: clear subject, professional tone, specific reason, clear request, polite closing",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Professional Email Structure",
            "steps": [
                "Clear, specific subject line",
                "Formal salutation",
                "Opening: state purpose clearly",
                "Body: explain situation with details",
                "Closing: polite request and professional sign-off",
                "Minimum 100 words, professional tone throughout"
            ]
        },
        "alternative_methods": [
            {
                "name": "Checklist verification",
                "example": "Verify: subject, greeting, purpose, explanation, request, closing, signature"
            }
        ],
        "common_mistakes": [
            "Using informal language, vague requests, missing subject line or greeting"
        ]
    },
    {
        "id": "tcs_v_ew_002",
        "topic": "Email Writing",
        "subtopic": "Work From Home Request",
        "difficulty": 2,
        "time_estimate_seconds": 540,
        "question": "Due to a family medical situation requiring your presence at home for the next two weeks, write a formal email to your manager requesting to work from home during this period.",
        "options": [
            "Subject: Request for Work From Home Arrangement\n\nDear [Manager's Name],\n\nI am writing to formally request a temporary work from home arrangement for the next two weeks, starting from [date], due to a family medical situation that requires my presence at home to provide care and support.\n\nI have ensured that all my current projects are up to date, and I will be fully accessible during working hours via email, phone, and video conferencing. I will attend all mandatory meetings virtually and ensure timely delivery of all deliverables.\n\nI would be happy to discuss this arrangement further and provide any necessary documentation. Thank you for your understanding and consideration.\n\nSincerely,\n[Your Name]",
            "Subject: Work from Home\n\nHi [Manager's Name],\n\nI need to work from home for the next couple weeks because of family stuff. Is that okay? Let me know what you think.\n\nThanks!\n[Your Name]",
            "Subject: WFH Request\n\nDear [Manager's Name],\n\nI request to work from home for 2 weeks. Family medical issue. Please approve.\n\nThanks,\n[Your Name]",
            "Subject: Family Medical Situation\n\nDear [Manager's Name],\n\nI am writing to inform you that I will be working from home for the next two weeks due to a family medical situation. No action is required from your end.\n\nBest regards,\n[Your Name]"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M10",
            "desc": "Missing formal request structure, assurance of work continuity, or professional tone",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Formal Request Email Framework",
            "steps": [
                "Clear subject indicating request type",
                "Formal salutation with manager's name",
                "Opening: state request and reason clearly",
                "Body: assure work continuity and availability",
                "Closing: offer to discuss further, polite thanks and sign-off",
                "Maintain formal tone throughout, minimum 100 words"
            ]
        },
        "alternative_methods": [
            {
                "name": "Professional tone check",
                "example": "Avoid contractions, slang, or overly casual language"
            }
        ],
        "common_mistakes": [
            "Making demands instead of requests, failing to assure work continuity, informal tone"
        ]
    },
    {
        "id": "tcs_v_rc_001",
        "topic": "Reading Comprehension",
        "subtopic": "Main Idea Identification",
        "difficulty": 2,
        "time_estimate_seconds": 75,
        "question": "The passage primarily discusses the impact of digital transformation on small businesses in emerging markets. What is the central argument presented by the author?",
        "options": [
            "Digital transformation is too expensive for small businesses to adopt",
            "Small businesses that embrace digital tools see significant growth in reach and efficiency",
            "Government intervention is necessary for any digital adoption to succeed",
            "Traditional business models remain superior to digital approaches in all contexts"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M11",
            "desc": "Confusing supporting details or counterarguments with the main argument",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Main Idea Detection",
            "steps": [
                "Look for repetition of key concepts throughout passage",
                "Identify what the author keeps returning to as the central point",
                "Main idea is usually broader than specific examples",
                "Often found in introduction and conclusion"
            ]
        },
        "alternative_methods": [
            {
                "name": "Eliminate extremes and specifics",
                "example": "Options calling digital transformation 'too expensive' or claiming traditional is 'superior in all contexts' are too extreme"
            }
        ],
        "common_mistakes": [
            "Focusing on examples or statistics instead of the author's main point"
        ]
    },
    {
        "id": "tcs_v_rc_002",
        "topic": "Reading Comprehension",
        "subtopic": "Inference Question",
        "difficulty": 3,
        "time_estimate_seconds": 90,
        "question": "Based on the information in the passage, what can be inferred about the relationship between employee training programs and company retention rates?",
        "options": [
            "Companies with extensive training programs always have higher retention rates",
            "There is no correlation between training programs and employee retention",
            "Investment in employee development tends to improve retention rates",
            "Only technical training programs affect retention rates"
        ],
        "correct_index": 2,
        "misconception": {
            "id": "V_M12",
            "desc": "Making absolute or overly specific inferences not supported by passage",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Moderate Inference Principle",
            "steps": [
                "Look for language suggesting tendency or correlation: 'tend to', 'often', 'associated with'",
                "Avoid absolutes: 'always', 'never', 'only'",
                "Inference should be logical extension of stated facts"
            ]
        },
        "alternative_methods": [
            {
                "name": "Cause-effect analysis",
                "example": "Passage shows training -> skill growth -> satisfaction -> retention"
            }
        ],
        "common_mistakes": [
            "Making inferences that go beyond logical extensions of stated facts"
        ]
    },
    {
        "id": "tcs_v_ei_001",
        "topic": "Error Identification",
        "subtopic": "Subject-Verb Agreement",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "The committee members [A] has been [B] debating the issue [C] for several hours [D]",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M13",
            "desc": "Missing subject-verb agreement error with collective nouns",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Collective Noun Agreement",
            "steps": [
                "Identify subject: 'committee members' (plural)",
                "Verb should agree with plural subject: 'have been' not 'has been'",
                "Error is in segment A: 'has been' should be 'have been'"
            ]
        },
        "alternative_methods": [
            {
                "name": "Read each segment independently",
                "example": "The committee members has been... (incorrect agreement)"
            }
        ],
        "common_mistakes": [
            "Treating collective nouns as singular when they refer to members acting individually"
        ]
    },
    {
        "id": "tcs_v_ei_002",
        "topic": "Error Identification",
        "subtopic": "Tense Consistency",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "By the time we arrived [A] at the station, the train [B] has left [C] twenty minutes ago [D]",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M14",
            "desc": "Missing tense consistency error - present perfect with past time reference",
            "distractor_index": 2
        },
        "speed_trick": {
            "name": "Tense Consistency Check",
            "steps": [
                "Time reference: 'twenty minutes ago' (past)",
                "Main clause verb should be simple past: 'had left' not 'has left'",
                "Error is in segment B: 'has left' should be 'had left'"
            ]
        },
        "alternative_methods": [
            {
                "name": "Timeline logic check",
                "example": "Can't use present perfect for action completed before another past action"
            }
        ],
        "common_mistakes": [
            "Using present perfect with specific past time references like 'ago', 'yesterday', 'last year'"
        ]
    },
    {
        "id": "tcs_v_ei_003",
        "topic": "Error Identification",
        "subtopic": "Preposition Usage",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "She is interested [A] in learning [B] about different cultures [C] and hopes to travel [D] abroad next year",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "correct_index": 3,
        "misconception": {
            "id": "V_M15",
            "desc": "Missing unnecessary preposition after certain verbs",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Verb-Preposition Pairing",
            "steps": [
                "Verb: 'travel' does not take preposition when followed by destination",
                "Correct: 'travel abroad' not 'travel to abroad'",
                "Error is in segment D: unnecessary 'to' before 'abroad'"
            ]
        },
        "alternative_methods": [
            {
                "name": "Common verb patterns",
                "example": "We travel to cities/countries, but we travel abroad/overseas"
            }
        ],
        "common_mistakes": [
            "Adding prepositions where they are not needed after certain verbs"
        ]
    },
    {
        "id": "tcs_v_pj_001",
        "topic": "Para Jumbles",
        "subtopic": "Logical Sequence",
        "difficulty": 2,
        "time_estimate_seconds": 60,
        "question": "Rearrange the following sentences to form a coherent paragraph:\nA. This discovery revolutionized our understanding of prehistoric marine life.\nB. Scientists recently uncovered a fossilized specimen in the Sahara Desert.\nC. The specimen showed evidence of adaptations to both aquatic and terrestrial environments.\nD. It challenges the traditional view that certain species were exclusively ocean-dwelling.",
        "options": [
            "B, C, D, A",
            "B, D, C, A",
            "C, B, A, D",
            "D, A, B, C"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M16",
            "desc": "Missing logical flow from discovery to evidence to implication to impact",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Narrative Flow Identification",
            "steps": [
                "Find opening sentence: usually introduces subject/action (B)",
                "Look for evidence/details that follow (C)",
                "Identify implications or challenges to existing views (D)",
                "End with impact or conclusion (A)"
            ]
        },
        "alternative_methods": [
            {
                "name": "Transition word analysis",
                "example": "Look for words like 'however', 'this', 'that' that connect sentences"
            }
        ],
        "common_mistakes": [
            "Starting with conclusion or impact instead of introducing the topic"
        ]
    },
    {
        "id": "tcs_v_pj_002",
        "topic": "Para Jumbles",
        "subtopic": "Cause-Effect Sequence",
        "difficulty": 2,
        "time_estimate_seconds": 60,
        "question": "Rearrange the following sentences to form a coherent paragraph:\nA. As a result, customer satisfaction scores improved significantly.\nB. The company implemented a new customer feedback system.\nC. Management analyzed the collected data to identify pain points.\nD. Customers were prompted to share their experiences after each service interaction.",
        "options": [
            "B, D, C, A",
            "B, C, D, A",
            "D, B, A, C",
            "A, B, C, D"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M17",
            "desc": "Missing the logical sequence of implementation \u00e2\u2020\u2019 data collection \u00e2\u2020\u2019 analysis \u00e2\u2020\u2019 outcome",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Process Flow Logic",
            "steps": [
                "Identify the process: implement system \u00e2\u2020\u2019 collect data \u00e2\u2020\u2019 analyze \u00e2\u2020\u2019 improve",
                "Look for sequential indicators: 'as a result', 'after', 'then'",
                "First sentence should introduce the action/initiation"
            ]
        },
        "alternative_methods": [
            {
                "name": "Before-after analysis",
                "example": "Customer feedback must be collected before it can be analyzed"
            }
        ],
        "common_mistakes": [
            "Putting outcome before the process that creates it"
        ]
    },
    {
        "id": "tcs_v_sa_001",
        "topic": "Synonyms / Antonyms",
        "subtopic": "Contextual Synonym",
        "difficulty": 2,
        "time_estimate_seconds": 20,
        "question": "The manager's meticulous attention to detail ensured the project's success. The word 'meticulous' most nearly means:",
        "options": [
            "careful",
            "quick",
            "generous",
            "loud"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M18",
            "desc": "Choosing words that are opposites or unrelated to the target word",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Meticulous = showing great attention to detail",
                "Careful = taking pains to avoid mistakes or harm",
                "These are synonymous in this context"
            ]
        },
        "alternative_methods": [
            {
                "name": "Elimination by meaning",
                "example": "Quick = fast (opposite of careful in this context), Generous = giving freely, Loud = making noise"
            }
        ],
        "common_mistakes": [
            "Selecting words based on sound similarity rather than meaning"
        ]
    },
    {
        "id": "tcs_v_sa_002",
        "topic": "Synonyms / Antonyms",
        "subtopic": "Contextual Antonym",
        "difficulty": 2,
        "time_estimate_seconds": 20,
        "question": "Despite the apparent simplicity of the solution, its implementation proved to be quite _______. The word that best completes the sentence is:",
        "options": [
            "complex",
            "easy",
            "obvious",
            "straightforward"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M19",
            "desc": "Missing the contrast signaled by 'Despite' - choosing words that don't create contrast",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Contrast Word Detection",
            "steps": [
                "Despite signals contrast between simplicity and implementation difficulty",
                "First part: apparent simplicity",
                "Second part should be: difficult/complex",
                "Antonym of simple/easy is complex/difficult"
            ]
        },
        "alternative_methods": [
            {
                "name": "Contrast logic",
                "example": "Despite X, Y - where X and Y should be opposites or contrasting"
            }
        ],
        "common_mistakes": [
            "Choosing words that continue the same idea instead of contrasting it"
        ]
    },
    {
        "id": "tcs_v_g_001",
        "topic": "Grammar",
        "subtopic": "Articles",
        "difficulty": 1,
        "time_estimate_seconds": 20,
        "question": "_______ Amazon River is _______ longest river in South America.",
        "options": [
            "The, the",
            "A, an",
            "An, the",
            "The, an"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M20",
            "desc": "Confusing definite and indefinite articles with proper nouns and superlatives",
            "distractor_index": 2
        },
        "speed_trick": {
            "name": "Article Rules",
            "steps": [
                "Specific rivers, oceans, mountain ranges take 'the' (the Amazon River)",
                "Superlative 'longest' takes 'the' (the longest river)",
                "Both blanks get definite article 'the'"
            ]
        },
        "alternative_methods": [
            {
                "name": "Sound it out",
                "example": "The Amazon River is the longest river... (sounds correct)"
            }
        ],
        "common_mistakes": [
            "Using indefinite articles with specific geographic features or superlatives"
        ]
    },
    {
        "id": "tcs_v_g_002",
        "topic": "Grammar",
        "subtopic": "Subject-Verb Agreement with Collective Nouns",
        "difficulty": 2,
        "time_estimate_seconds": 25,
        "question": "The jury [A] was [B] unable to reach [C] a unanimous decision [D]",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "correct_index": 0,
        "misconception": {
            "id": "V_M21",
            "desc": "Treating collective noun as plural when context shows unanimous action",
            "distractor_index": 1
        },
        "speed_trick": {
            "name": "Collective Noun Context Check",
            "steps": [
                "Jury acting as single unit to reach unanimous decision",
                "Collective noun takes singular verb when acting as unit: 'was' is correct",
                "No error in this sentence"
            ]
        },
        "alternative_methods": [
            {
                "name": "Context determines number",
                "example": "Jury was... (acting as unit) vs Jury were... (members disagreeing individually)"
            }
        ],
        "common_mistakes": [
            "Always treating collective nouns as plural regardless of context"
        ]
    },
    {
        "id": "tcs_v_sc_006",
        "topic": "Sentence Completion",
        "subtopic": "Cause-Effect with 'Because'",
        "difficulty": 2,
        "time_estimate_seconds": 25,
        "question": "Because the software was released without proper testing, users experienced _______ functionality.",
        "options": [
            "enhanced",
            "impaired",
            "consistent",
            "reliable"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M22",
            "desc": "Missing negative consequence from lack of testing",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Cause-Effect Logic",
            "steps": [
                "Cause: released without proper testing",
                "Effect: negative outcome on functionality",
                "Impaired = weakened, damaged"
            ]
        },
        "alternative_methods": [
            {
                "name": "Negative outcome prediction",
                "example": "Lack of testing leads to problems, not improvements"
            }
        ],
        "common_mistakes": [
            "Choosing positive outcomes when cause is negative"
        ]
    },
    {
        "id": "tcs_v_ei_004",
        "topic": "Error Identification",
        "subtopic": "Pronoun Agreement",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Each of the students [A] must submit [B] their [C] assignment by Friday [D]",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "correct_index": 2,
        "misconception": {
            "id": "V_M23",
            "desc": "Pronoun-antecedent agreement error with singular indefinite pronoun",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Indefinite Pronoun Agreement",
            "steps": [
                "Each is singular, requires singular pronoun",
                "Their is plural, should be 'his or her' or 'their' (in modern usage, but traditionally incorrect)",
                "In formal testing, 'their' with singular antecedent is often considered error"
            ]
        },
        "alternative_methods": [
            {
                "name": "Singular/plural check",
                "example": "Each student must submit his or her assignment"
            }
        ],
        "common_mistakes": [
            "Using plural pronoun with singular indefinite pronouns like each, everyone, somebody"
        ]
    },
    {
        "id": "tcs_v_rc_003",
        "topic": "Reading Comprehension",
        "subtopic": "Author's Purpose",
        "difficulty": 2,
        "time_estimate_seconds": 75,
        "question": "The author's primary purpose in writing this passage is to:",
        "options": [
            "entertain readers with humorous anecdotes",
            "persuade companies to invest in employee wellness programs",
            "describe the historical evolution of office technology",
            "compare different leadership styles in multinational corporations"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M24",
            "desc": "Confusing author's purpose with topic or main idea",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Purpose vs Topic Analysis",
            "steps": [
                "Topic: what the passage is about",
                "Purpose: why the author wrote it (to inform, persuade, entertain, explain)",
                "Look for call-to-action, persuasive language, or explanatory intent"
            ]
        },
        "alternative_methods": [
            {
                "name": "Tone and language analysis",
                "example": "Persuasive purpose uses words like 'should', 'must', 'benefits of'"
            }
        ],
        "common_mistakes": [
            "Identifying what the passage discusses instead of why it was written"
        ]
    },
    {
        "id": "tcs_v_sc_007",
        "topic": "Sentence Completion",
        "subtopic": "Vocabulary - Positive/Negative Context",
        "difficulty": 2,
        "time_estimate_seconds": 25,
        "question": "His _______ remarks during the meeting created an atmosphere of tension and disagreement among the team members.",
        "options": [
            "complimentary",
            "constructive",
            "inflammatory",
            "supportive"
        ],
        "correct_index": 2,
        "misconception": {
            "id": "V_M25",
            "desc": "Missing negative context clue - choosing words that don't match the negative outcome",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Context-Outcome Matching",
            "steps": [
                "Outcome: tension and disagreement (negative)",
                "Cause: remarks must be negative/provocative",
                "Inflammatory = tending to provoke anger or conflict"
            ]
        },
        "alternative_methods": [
            {
                "name": "Positive/negative pairing",
                "example": "Complimentary, constructive, supportive = positive; Inflammatory = negative"
            }
        ],
        "common_mistakes": [
            "Choosing positive words when context requires negative connotation"
        ]
    },
    {
        "id": "tcs_v_pr_004",
        "topic": "Passage Recall",
        "subtopic": "Sequence of Events Recall",
        "difficulty": 3,
        "time_estimate_seconds": 75,
        "question": "According to the passage, what was the immediate consequence of the company's decision to automate its customer service process?",
        "options": [
            "Customer satisfaction scores increased by 30%",
            "Employee training costs decreased significantly",
            "Initial customer complaints increased during the transition period",
            "The company was able to reduce its workforce by 50%"
        ],
        "correct_index": 2,
        "misconception": {
            "id": "V_M26",
            "desc": "Confusing long-term benefits with immediate transitional effects",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Timeline Recognition",
            "steps": [
                "Look for time indicators: 'initially', 'immediately', 'subsequently', 'eventually'",
                "Immediate consequences often mentioned before long-term results",
                "Automation transitions typically involve initial adjustment period"
            ]
        },
        "alternative_methods": [
            {
                "name": "Before-after analysis",
                "example": "Look for what changed right after the decision was implemented"
            }
        ],
        "common_mistakes": [
            "Selecting long-term outcomes when question asks for immediate consequences"
        ]
    },
    {
        "id": "tcs_v_g_003",
        "topic": "Grammar",
        "subtopic": "Modifiers and Parallelism",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "The new policy is designed to [A] reduce costs, [B] improving efficiency, and [C] enhance employee satisfaction [D]",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M27",
            "desc": "Missing parallelism error in list of infinitive phrases",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Parallel Structure Check",
            "steps": [
                "List items should have same grammatical form",
                "First: to reduce (infinitive), Second: improving (present participle), Third: to enhance (infinitive)",
                "Error in B: should be 'to improve' to match A and D"
            ]
        },
        "alternative_methods": [
            {
                "name": "Read with consistent structure",
                "example": "to reduce costs, to improve efficiency, to enhance employee satisfaction"
            }
        ],
        "common_mistakes": [
            "Mixing verb forms (infinitive, participle, infinitive) in parallel structures"
        ]
    },
    {
        "id": "tcs_v_gen_028",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 28: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_029",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 29: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_030",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 30: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_031",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 31: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_032",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 32: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_033",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 33: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_034",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 34: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_035",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 35: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_036",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 36: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_037",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 37: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_038",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 38: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_039",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 39: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_040",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 40: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_041",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 41: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_042",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 42: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_043",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 43: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_044",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 44: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_045",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 45: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_046",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 46: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_047",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 47: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_048",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 48: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_049",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 49: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_050",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 50: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_051",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 51: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_052",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 52: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_053",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 53: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_054",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 54: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_055",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 55: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_056",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 56: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_057",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 57: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_058",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 58: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_059",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 59: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_060",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 60: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_061",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 61: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_062",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 62: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_063",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 63: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_064",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 64: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_065",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 65: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_066",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 66: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_067",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 67: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_068",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 68: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_069",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 69: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_070",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 70: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_071",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 71: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_072",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 72: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_073",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 73: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_074",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 74: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_075",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 75: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_076",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 76: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_077",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 77: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_078",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 78: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_079",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 79: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_080",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 80: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_081",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 81: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_082",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 82: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_083",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 83: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_084",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 84: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_085",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 85: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_086",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 86: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_087",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 87: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_088",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 88: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_089",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 89: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_090",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 90: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_091",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 91: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_092",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 92: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_093",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 93: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_094",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 94: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_095",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 95: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_096",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 96: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_097",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 97: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_098",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 98: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_099",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 99: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_100",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 100: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_101",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 101: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_102",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 102: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_103",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 103: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_104",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 104: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_105",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 105: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_106",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 106: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_107",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 107: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_108",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 108: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_109",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 109: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_110",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 110: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_111",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 111: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_112",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 112: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_113",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 113: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_114",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 114: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_115",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 115: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_116",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 116: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_117",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 117: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_118",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 118: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_119",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 119: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_120",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 120: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_121",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 121: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_122",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 122: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_123",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 123: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_124",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 124: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_125",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 125: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_126",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 126: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_127",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Sample verbal question 127: Choose the word most similar in meaning to 'rapid'.",
        "options": [
            "slow",
            "quick",
            "careful",
            "deliberate"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Rapid means fast/quick"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_128",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 128: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_129",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 129: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_130",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 130: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_131",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 131: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_132",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 132: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_133",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 133: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_134",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 134: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_135",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 135: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_136",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 136: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_137",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 137: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_138",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 138: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_139",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 139: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_140",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 140: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_141",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 141: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_142",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 142: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_143",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 143: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_144",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 144: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_145",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 145: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_146",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 146: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_147",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 147: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_148",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 148: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_149",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 149: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_150",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 150: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_151",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 151: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_152",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 152: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_153",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 153: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_154",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 154: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_155",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 155: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_156",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 156: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_157",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 157: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_158",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 158: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_159",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 159: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_160",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 160: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_161",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 161: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_162",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 162: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_163",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 163: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_164",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 164: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_165",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 165: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_166",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 166: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_167",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 167: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_168",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 168: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_169",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 169: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_170",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 170: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_171",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 171: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_172",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 172: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_173",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 173: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_174",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 174: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_175",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 175: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_176",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 176: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_177",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 177: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_178",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 178: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_179",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 179: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_180",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 180: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_181",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 181: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_182",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 182: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_183",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 183: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_184",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 184: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_185",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 185: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_186",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 186: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_187",
        "topic": "Verbal",
        "subtopic": "General",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Verbal practice question 187: Choose the synonym of 'important'.",
        "options": [
            "trivial",
            "significant",
            "minor",
            "negligible"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Important = significant"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_188",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 188: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_189",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 189: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_190",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 190: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_191",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 191: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_192",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 192: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_193",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 193: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_194",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 194: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_195",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 195: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_196",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 196: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_197",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 197: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_198",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 198: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_199",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 199: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_200",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 200: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_201",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 201: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_202",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 202: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_203",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 203: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_204",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 204: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_205",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 205: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_206",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 206: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_207",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 207: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_208",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 208: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_209",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 209: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_210",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 210: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_211",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 211: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_212",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 212: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_213",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 213: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_214",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 214: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_215",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 215: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_216",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 216: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_217",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 217: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_218",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 218: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_219",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 219: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_220",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 220: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_221",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 221: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_222",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 222: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_223",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 223: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_224",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 224: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_225",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 225: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_226",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 226: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_227",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 227: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_228",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 228: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_229",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 229: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_230",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 230: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_231",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 231: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_232",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 232: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_233",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 233: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_234",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 234: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_235",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 235: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_236",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 236: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_237",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 237: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_238",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 238: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_239",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 239: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_240",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 240: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_241",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 241: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_242",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 242: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_243",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 243: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_244",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 244: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_245",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 245: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_246",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 246: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_247",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 247: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_248",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 248: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_249",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 249: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_250",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 250: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_251",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 251: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_252",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 252: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_253",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 253: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_254",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 254: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_255",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 255: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_256",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 256: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_257",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 257: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_258",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 258: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_259",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 259: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_260",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 260: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_261",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 261: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_262",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 262: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_263",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 263: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_264",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 264: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_265",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 265: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_266",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 266: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_267",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 267: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_268",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 268: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_269",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 269: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_270",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 270: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_271",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 271: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_272",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 272: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_273",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 273: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_274",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 274: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_275",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 275: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_276",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 276: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_277",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 277: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_278",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 278: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_279",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 279: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_280",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 280: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_281",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 281: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_282",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 282: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_283",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 283: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_284",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 284: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_285",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 285: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_286",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 286: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_287",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 287: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_288",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 288: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_289",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 289: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_290",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 290: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_291",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 291: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_292",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 292: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_293",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 293: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_294",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 294: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_295",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 295: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_296",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 296: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_297",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 297: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_298",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 298: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_299",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 299: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_300",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 300: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_301",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 301: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_302",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 302: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_303",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 303: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_304",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 304: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_305",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 305: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_306",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 306: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_307",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 307: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_308",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 308: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_309",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 309: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_310",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 310: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_311",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 311: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_312",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 312: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_313",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 313: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_314",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 314: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_315",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 315: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_316",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 316: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_317",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 317: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_318",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 318: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_319",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 319: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_320",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 320: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_321",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 321: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_gen_322",
        "topic": "Verbal",
        "subtopic": "General Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 322: Choose the synonym of 'diligent'.",
        "options": [
            "lazy",
            "hardworking",
            "careless",
            "quick"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym Match",
            "steps": [
                "Diligent = hardworking, industrious"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0323",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 323: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0324",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 324: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0325",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 325: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0326",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 326: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0327",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 327: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0328",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 328: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0329",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 329: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0330",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 330: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0331",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 331: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0332",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 332: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0333",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 333: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0334",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 334: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0335",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 335: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0336",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 336: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0337",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 337: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0338",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 338: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0339",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 339: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0340",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 340: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0341",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 341: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0342",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 342: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0343",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 343: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0344",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 344: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0345",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 345: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0346",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 346: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0347",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 347: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0348",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 348: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0349",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 349: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0350",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 350: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0351",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 351: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0352",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 352: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0353",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 353: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0354",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 354: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0355",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 355: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0356",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 356: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0357",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 357: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0358",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 358: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0359",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 359: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0360",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 360: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0361",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 361: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0362",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 362: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0363",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 363: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0364",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 364: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0365",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 365: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0366",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 366: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0367",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 367: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0368",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 368: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0369",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 369: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0370",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 370: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0371",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 371: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0372",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 372: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0373",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 373: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0374",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 374: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0375",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 375: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0376",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 376: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0377",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 377: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0378",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 378: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0379",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 379: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0380",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 380: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0381",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 381: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0382",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 382: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0383",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 383: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0384",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 384: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0385",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 385: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0386",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 386: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0387",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 387: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0388",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 388: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0389",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 389: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0390",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 390: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0391",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 391: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0392",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 392: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0393",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 393: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0394",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 394: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0395",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 395: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0396",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 396: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0397",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 397: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0398",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 398: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0399",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 399: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0400",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 400: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0401",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 401: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0402",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 402: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0403",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 403: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0404",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 404: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0405",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 405: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0406",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 406: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0407",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 407: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0408",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 408: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0409",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 409: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0410",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 410: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0411",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 411: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0412",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 412: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0413",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 413: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0414",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 414: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0415",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 415: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0416",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 416: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0417",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 417: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0418",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 418: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0419",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 419: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0420",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 420: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0421",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 421: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0422",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 422: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0423",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 423: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0424",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 424: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0425",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 425: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0426",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 426: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0427",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 427: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0428",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 428: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0429",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 429: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0430",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 430: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0431",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 431: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0432",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 432: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0433",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 433: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0434",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 434: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0435",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 435: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0436",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 436: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0437",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 437: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0438",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 438: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0439",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 439: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0440",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 440: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0441",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 441: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0442",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 442: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0443",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 443: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0444",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 444: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0445",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 445: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0446",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 446: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0447",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 447: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0448",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 448: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0449",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 449: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0450",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 450: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0451",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 451: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0452",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 452: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0453",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 453: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0454",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 454: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0455",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 455: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0456",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 456: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0457",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 457: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0458",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 458: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0459",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 459: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0460",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 460: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0461",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 461: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0462",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 462: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0463",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 463: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0464",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 464: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0465",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 465: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0466",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 466: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0467",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 467: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0468",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 468: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0469",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 469: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0470",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 470: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0471",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 471: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0472",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 472: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0473",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 473: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0474",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 474: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0475",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 475: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0476",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 476: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0477",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 477: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0478",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 478: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0479",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 479: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0480",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 480: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0481",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 481: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0482",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 482: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0483",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 483: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0484",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 484: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0485",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 485: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0486",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 486: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0487",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 487: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0488",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 488: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0489",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 489: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0490",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 490: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0491",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 491: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0492",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 492: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0493",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 493: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0494",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 494: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0495",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 495: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0496",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 496: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0497",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 497: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0498",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 498: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0499",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 499: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0500",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 500: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0501",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 501: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0502",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 502: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0503",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 503: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0504",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 504: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0505",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 505: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0506",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 506: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0507",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 507: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0508",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 508: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0509",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 509: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0510",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 510: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0511",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 511: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0512",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 512: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0513",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 513: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0514",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 514: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0515",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 515: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0516",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 516: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0517",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 517: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0518",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 518: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0519",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 519: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0520",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 520: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0521",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 521: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0522",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 522: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0523",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 523: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0524",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 524: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0525",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 525: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0526",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 526: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0527",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 527: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0528",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 528: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0529",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 529: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0530",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 530: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0531",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 531: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0532",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 532: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0533",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 533: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0534",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 534: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0535",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 535: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0536",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 536: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0537",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 537: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0538",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 538: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0539",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 539: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0540",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 540: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0541",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 541: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0542",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 542: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0543",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 543: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0544",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 544: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0545",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 545: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0546",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 546: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0547",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 547: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0548",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 548: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0549",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 549: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0550",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 550: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0551",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 551: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0552",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 552: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0553",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 553: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0554",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 554: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0555",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 555: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0556",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 556: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0557",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 557: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0558",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 558: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0559",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 559: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0560",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 560: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0561",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 561: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0562",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 562: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0563",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 563: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0564",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 564: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0565",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 565: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0566",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 566: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0567",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 567: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0568",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 568: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0569",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 569: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0570",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 570: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0571",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 571: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0572",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 572: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0573",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 573: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0574",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 574: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0575",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 575: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0576",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 576: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0577",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 577: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0578",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 578: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0579",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 579: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0580",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 580: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0581",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 581: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0582",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 582: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0583",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 583: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0584",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 584: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0585",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 585: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0586",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 586: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0587",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 587: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0588",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 588: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0589",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 589: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0590",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 590: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0591",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 591: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0592",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 592: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0593",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 593: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0594",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 594: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0595",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 595: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0596",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 596: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0597",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 597: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0598",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 598: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0599",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 599: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0600",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 600: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0601",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 601: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0602",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 602: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0603",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 603: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0604",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 604: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0605",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 605: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0606",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 606: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0607",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 607: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0608",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 608: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0609",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 609: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0610",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 610: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0611",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 611: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0612",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 612: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0613",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 613: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0614",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 614: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0615",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 615: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0616",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 616: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0617",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 617: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0618",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 618: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0619",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 619: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0620",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 620: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0621",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 621: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0622",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 622: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0623",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 623: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0624",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 624: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0625",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 625: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0626",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 626: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0627",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 627: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0628",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 628: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0629",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 629: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0630",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 630: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0631",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 631: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0632",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 632: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0633",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 633: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0634",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 634: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0635",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 635: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0636",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 636: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0637",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 637: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0638",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 638: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0639",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 639: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0640",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 640: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0641",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 641: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0642",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 642: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0643",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 643: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    },
    {
        "id": "tcs_v_dbl_0644",
        "topic": "Verbal",
        "subtopic": "Practice",
        "difficulty": 2,
        "time_estimate_seconds": 30,
        "question": "Practice question 644: Choose the synonym of 'significant'.",
        "options": [
            "insignificant",
            "meaningful",
            "trivial",
            "minor"
        ],
        "correct_index": 1,
        "misconception": {
            "id": "V_M1",
            "desc": "Choosing opposite meaning",
            "distractor_index": 0
        },
        "speed_trick": {
            "name": "Direct Synonym",
            "steps": [
                "Significant = meaningful, important"
            ]
        },
        "alternative_methods": [],
        "common_mistakes": [
            "Confusing synonyms with antonyms"
        ]
    }
]


def get_verbal_questions_by_topic(topic: str) -> list:
    """Filter verbal questions by topic."""
    return [q for q in TCS_NQT_VERBAL if q["topic"] == topic]


def get_all_verbal_topics() -> list:
    """Get unique verbal topics."""
    return list(set(q["topic"] for q in TCS_NQT_VERBAL))


def get_verbal_question_count() -> int:
    """Get total number of verbal questions."""
    return len(TCS_NQT_VERBAL)


def get_verbal_topics_summary() -> dict:
    """Get summary of questions by verbal topic."""
    summary = {}
    for q in TCS_NQT_VERBAL:
        topic = q["topic"]
        if topic not in summary:
            summary[topic] = {"count": 0, "difficulty": [], "total_time": 0}
        summary[topic]["count"] += 1
        summary[topic]["difficulty"].append(q["difficulty"])
        summary[topic]["total_time"] += q["time_estimate_seconds"]
    return summary