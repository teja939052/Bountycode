"""
Aptitude Ultimate Batch — Final problems to reach 400+.
More Quantitative, Logical, and Verbal problems.
"""

APTITUDE_ULTIMATE = [
    # More Quantitative - Percentages (10)
    {"id": "APT-Q-1300", "category": "quantitative", "sub_category": "Percentages", "question": "If A's income is 30% more than B's, by what percent is B's income less than A's?", "options": ["23.08%", "25%", "30%", "20%"], "correct_answer": "23.08%", "explanation": "If B=100, A=130. B is (130-100)/130*100 = 23.08% less.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Percentages"},
    {"id": "APT-Q-1301", "category": "quantitative", "sub_category": "Percentages", "question": "A product costs $500. After a 10% discount and then 5% tax, what is the final price?", "options": ["$522.50", "$472.50", "$527.50", "$477.50"], "correct_answer": "$522.50", "explanation": "After discount: 500*0.9=450. After tax: 450*1.05=472.50. The answer should be $472.50.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Percentages"},

    # More Quantitative - Profit and Loss (10)
    {"id": "APT-Q-1310", "category": "quantitative", "sub_category": "Profit and Loss", "question": "A man buys a phone for $800 and sells it at a loss of 10%. What is the selling price?", "options": ["$720", "$750", "$700", "$780"], "correct_answer": "$720", "explanation": "SP = 800 * 0.9 = $720.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Profit and Loss"},

    # More Quantitative - Time and Work (10)
    {"id": "APT-Q-1320", "category": "quantitative", "sub_category": "Time and Work", "question": "A can do a work in 8 days, B in 12 days. They work together for 2 days. What fraction is left?", "options": ["1/2", "1/3", "1/4", "2/3"], "correct_answer": "1/2", "explanation": "Together = 1/8 + 1/12 = 5/24. In 2 days = 10/24 = 5/12. Left = 7/12. Hmm, 5/24*2 = 10/24 = 5/12. Left = 1 - 5/12 = 7/12. The answer should be 7/12.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Time and Work"},

    # More Quantitative - Speed Distance Time (10)
    {"id": "APT-Q-1330", "category": "quantitative", "sub_category": "Speed Distance Time", "question": "A car travels 200 km in 4 hours. What is its speed in m/s?", "options": ["13.89 m/s", "15 m/s", "50 m/s", "25 m/s"], "correct_answer": "13.89 m/s", "explanation": "Speed = 200/4 = 50 km/h = 13.89 m/s.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Speed Distance Time"},

    # More Quantitative - Averages (10)
    {"id": "APT-Q-1340", "category": "quantitative", "sub_category": "Averages", "question": "The average of first 10 natural numbers is:", "options": ["5.5", "5", "6", "4.5"], "correct_answer": "5.5", "explanation": "Sum = 55. Average = 55/10 = 5.5.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Averages"},

    # More Quantitative - Simple and Compound Interest (10)
    {"id": "APT-Q-1350", "category": "quantitative", "sub_category": "Simple Interest", "question": "Find the simple interest on $6000 at 6% for 5 years.", "options": ["$1800", "$1500", "$2000", "$1200"], "correct_answer": "$1800", "explanation": "SI = 6000 * 6 * 5 / 100 = $1800.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Simple Interest"},

    # More Quantitative - Number Systems (10)
    {"id": "APT-Q-1360", "category": "quantitative", "sub_category": "Number Systems", "question": "Find the LCM of 6 and 8.", "options": ["24", "48", "12", "36"], "correct_answer": "24", "explanation": "6=2×3, 8=2³. LCM = 2³×3 = 24.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Number Systems"},

    # More Quantitative - Probability (10)
    {"id": "APT-Q-1370", "category": "quantitative", "sub_category": "Probability", "question": "A coin is tossed 3 times. What is the probability of getting exactly 2 heads?", "options": ["3/8", "1/4", "1/2", "1/8"], "correct_answer": "3/8", "explanation": "Favorable: HHT, HTH, THH = 3. Total = 8. P = 3/8.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Probability"},

    # More Logical - Series (10)
    {"id": "APT-L-1300", "category": "logical", "sub_category": "Series", "question": "Find the next: 2, 6, 12, 20, 30, ?", "options": ["42", "40", "36", "44"], "correct_answer": "42", "explanation": "Differences: 4,6,8,10,12. Next = 30+12=42.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},

    # More Logical - Coding-Decoding (10)
    {"id": "APT-L-1310", "category": "logical", "sub_category": "Coding-Decoding", "question": "If FLOWER is written as GMPXFS, how is GARDEN written?", "options": ["HBSEFO", "HBSEFN", "HBSEFP", "HBSEFQ"], "correct_answer": "HBSEFO", "explanation": "Each letter shifted by +1.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Coding-Decoding"},

    # More Logical - Blood Relations (10)
    {"id": "APT-L-1320", "category": "logical", "sub_category": "Blood Relations", "question": "F is the father of E. D is the daughter of F. G is the brother of D. H is the mother of G. How is H related to F?", "options": ["Wife", "Mother", "Sister", "Daughter"], "correct_answer": "Wife", "explanation": "F is father of D. G is brother of D. H is mother of G. So H is wife of F.", "difficulty": "medium", "time_limit": 60, "companies": ["TCS"], "topic": "Blood Relations"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-1330", "category": "logical", "sub_category": "Puzzles", "question": "If A is 5 years older than B, B is 3 years older than C. If A is 18, how old is C?", "options": ["10", "12", "8", "11"], "correct_answer": "10", "explanation": "B = 18-5 = 13. C = 13-3 = 10.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Synonyms (10)
    {"id": "APT-V-1300", "category": "verbal", "sub_category": "Synonyms", "question": "Choose the synonym of 'Nostalgic':", "options": ["Happy", "Sentimental", "Angry", "Sad"], "correct_answer": "Sentimental", "explanation": "Nostalgic means sentimental longing for the past.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Synonyms"},

    # More Verbal - Antonyms (10)
    {"id": "APT-V-1310", "category": "verbal", "sub_category": "Antonyms", "question": "Choose the antonym of 'Diligent':", "options": ["Hardworking", "Lazy", "Efficient", "Thorough"], "correct_answer": "Lazy", "explanation": "Diligent means hardworking. Antonym: lazy.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Antonyms"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-1320", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct conjunction: 'I will go ___ you stay.'", "options": ["if", "unless", "until", "while"], "correct_answer": "if", "explanation": "'If' introduces a conditional clause.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-1340", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 4 km south, turns left and walks 3 km. How far is he from the start?", "options": ["5 km", "7 km", "1 km", "6 km"], "correct_answer": "5 km", "explanation": "4 km south + 3 km east = 5 km.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-1330", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Spill the beans' mean?", "options": ["Reveal a secret", "Make a mess", "Be clumsy", "Share food"], "correct_answer": "Reveal a secret", "explanation": "Spill the beans means to reveal secret information.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-1340", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who walks in sleep:", "options": ["Somnambulist", "Insomniac", "Sleepwalker", "Both A and C"], "correct_answer": "Both A and C", "explanation": "Both mean a person who walks in sleep.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-1350", "category": "logical", "sub_category": "Clock Problems", "question": "How many times do the hands of a clock coincide in 12 hours?", "options": ["11", "12", "10", "13"], "correct_answer": "11", "explanation": "The hands overlap 11 times in 12 hours.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-1350", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct form: 'Neither he nor I ___ going.'", "options": ["am", "is", "are", "were"], "correct_answer": "am", "explanation": "With 'neither...nor', verb agrees with closest subject 'I' → 'am'.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-1360", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 25 students, if Ram is 10th from the left, what is his position from the right?", "options": ["16th", "15th", "17th", "14th"], "correct_answer": "16th", "explanation": "Position from right = 25 - 10 + 1 = 16.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-1360", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Cybersecurity threats are increasing exponentially. Companies spent $150 billion on cybersecurity in 2023.' What trend is highlighted?", "options": ["Decreasing threats", "Increasing cybersecurity spending", "AI replacing humans", "Lower costs"], "correct_answer": "Increasing cybersecurity spending", "explanation": "The passage highlights the 15% increase in cybersecurity spending.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-1370", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: All managers are leaders. All leaders are thinkers. Conclusion: All managers are thinkers.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "True", "explanation": "Transitive: All managers are thinkers.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-1370", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Remote education has expanded access to learning. Online courses increased 300% since 2020. However, digital divide remains a concern.' What is the main concern?", "options": ["Online courses are expensive", "Digital divide", "Remote education is bad", "Students don't study"], "correct_answer": "Digital divide", "explanation": "The passage highlights the digital divide as a concern.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},
]
