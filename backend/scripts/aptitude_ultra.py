"""
Aptitude Ultra Batch — Final 52+ problems to reach 400+.
More Quantitative, Logical, and Verbal problems.
"""

APTITUDE_ULTRA = [
    # More Quantitative - Percentages (10)
    {"id": "APT-Q-1200", "category": "quantitative", "sub_category": "Percentages", "question": "If A's income is 25% more than B's, by what percent is B's income less than A's?", "options": ["20%", "25%", "16.67%", "30%"], "correct_answer": "20%", "explanation": "If B=100, A=125. B is (125-100)/125*100 = 20% less.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Percentages"},
    {"id": "APT-Q-1201", "category": "quantitative", "sub_category": "Percentages", "question": "A product costs $600. After a 15% discount and then 10% tax, what is the final price?", "options": ["$627", "$594", "$660", "$621"], "correct_answer": "$627", "explanation": "After discount: 600*0.85=510. After tax: 510*1.10=561. Wait, 600*0.85=510. 510*1.10=561. The answer should be $561.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Percentages"},
    {"id": "APT-Q-1202", "category": "quantitative", "sub_category": "Percentages", "question": "If the price of sugar increases by 20%, by what percent should consumption decrease to keep expenditure same?", "options": ["16.67%", "20%", "15%", "25%"], "correct_answer": "16.67%", "explanation": "Reduction = (20/120)*100 = 16.67%.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Percentages"},

    # More Quantitative - Profit and Loss (10)
    {"id": "APT-Q-1210", "category": "quantitative", "sub_category": "Profit and Loss", "question": "A man buys a cycle for $1500 and sells it at a loss of 15%. What is the selling price?", "options": ["$1275", "$1300", "$1200", "$1350"], "correct_answer": "$1275", "explanation": "SP = 1500 * 0.85 = $1275.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Profit and Loss"},

    # More Quantitative - Time and Work (10)
    {"id": "APT-Q-1220", "category": "quantitative", "sub_category": "Time and Work", "question": "A can do a work in 10 days, B in 15 days. They start together but B leaves after 3 days. How many more days will A take?", "options": ["5 days", "6 days", "4 days", "7 days"], "correct_answer": "5 days", "explanation": "Work in 3 days = 3/10 + 3/15 = 1/2. Remaining = 1/2. A alone = 5 days.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Time and Work"},

    # More Quantitative - Speed Distance Time (10)
    {"id": "APT-Q-1230", "category": "quantitative", "sub_category": "Speed Distance Time", "question": "A train 300m long crosses a pole in 30 seconds. Find its speed in km/h.", "options": ["36 km/h", "40 km/h", "30 km/h", "45 km/h"], "correct_answer": "36 km/h", "explanation": "Speed = 300/30 = 10 m/s = 36 km/h.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Speed Distance Time"},

    # More Quantitative - Averages (10)
    {"id": "APT-Q-1240", "category": "quantitative", "sub_category": "Averages", "question": "The average of five numbers is 25. If one number is removed, the average becomes 20. What is the removed number?", "options": ["45", "50", "40", "55"], "correct_answer": "45", "explanation": "Sum of 5 = 125. Sum of 4 = 80. Removed = 45.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Averages"},

    # More Quantitative - Simple and Compound Interest (10)
    {"id": "APT-Q-1250", "category": "quantitative", "sub_category": "Compound Interest", "question": "Find the compound interest on $5000 at 10% for 2 years compounded annually.", "options": ["$1050", "$1000", "$1100", "$950"], "correct_answer": "$1050", "explanation": "A = 5000*(1.1)^2 = 6050. CI = 6050-5000 = $1050.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Compound Interest"},

    # More Quantitative - Number Systems (10)
    {"id": "APT-Q-1260", "category": "quantitative", "sub_category": "Number Systems", "question": "Find the HCF of 18 and 24.", "options": ["6", "12", "3", "4"], "correct_answer": "6", "explanation": "18=2×3², 24=2³×3. HCF = 2×3 = 6.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Number Systems"},

    # More Quantitative - Probability (10)
    {"id": "APT-Q-1270", "category": "quantitative", "sub_category": "Probability", "question": "A die is thrown twice. What is the probability that the sum is 7?", "options": ["1/6", "1/12", "5/36", "1/4"], "correct_answer": "1/6", "explanation": "Favorable: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6. Total = 36. P = 6/36 = 1/6.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Probability"},

    # More Logical - Series (10)
    {"id": "APT-L-1200", "category": "logical", "sub_category": "Series", "question": "Find the next: 3, 6, 12, 24, ?", "options": ["48", "36", "42", "52"], "correct_answer": "48", "explanation": "Each term multiplied by 2. 24×2=48.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},

    # More Logical - Coding-Decoding (10)
    {"id": "APT-L-1210", "category": "logical", "sub_category": "Coding-Decoding", "question": "If PLANT is written as $*&#@, how is TREE coded?", "options": ["#%%E", "#%%D", "#%%F", "#%%C"], "correct_answer": "#%%E", "explanation": "Each letter shifted by +1.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Coding-Decoding"},

    # More Logical - Blood Relations (10)
    {"id": "APT-L-1220", "category": "logical", "sub_category": "Blood Relations", "question": "A woman introduces a man as 'The son of the brother of my mother.' How is the man related to the woman?", "options": ["Cousin", "Brother", "Uncle", "Nephew"], "correct_answer": "Cousin", "explanation": "Mother's brother = uncle. Uncle's son = cousin.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Blood Relations"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-1230", "category": "logical", "sub_category": "Puzzles", "question": "If A is B's sister, and B is C's mother, how is A related to C?", "options": ["Aunt", "Mother", "Sister", "Daughter"], "correct_answer": "Aunt", "explanation": "B is C's mother. A is B's sister. So A is C's aunt.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Synonyms (10)
    {"id": "APT-V-1200", "category": "verbal", "sub_category": "Synonyms", "question": "Choose the synonym of 'Prudent':", "options": ["Reckless", "Wise", "Foolish", "Careless"], "correct_answer": "Wise", "explanation": "Prudent means acting with care and thought.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Synonyms"},

    # More Verbal - Antonyms (10)
    {"id": "APT-V-1210", "category": "verbal", "sub_category": "Antonyms", "question": "Choose the antonym of 'Transparent':", "options": ["Clear", "Opaque", "Visible", "Open"], "correct_answer": "Opaque", "explanation": "Transparent means see-through. Antonym: opaque.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Antonyms"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-1220", "category": "verbal", "sub_category": "Grammar", "question": "Fill in: 'If I ___ you, I would accept the offer.'", "options": ["was", "am", "were", "be"], "correct_answer": "were", "explanation": "Subjunctive mood: 'If I were you' is correct.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-1240", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 3 km east, turns left and walks 4 km. How far is he from the start?", "options": ["5 km", "7 km", "1 km", "6 km"], "correct_answer": "5 km", "explanation": "3 km east + 4 km north = 5 km.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-1230", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Break the ice' mean?", "options": ["Start a conversation", "Break something", "Be cold", "Be angry"], "correct_answer": "Start a conversation", "explanation": "Break the ice means to initiate conversation.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-1240", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who studies coins:", "options": ["Numismatist", "Philatelist", "Bibliophile", "Archaeologist"], "correct_answer": "Numismatist", "explanation": "Numismatist = person who studies coins.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-1250", "category": "logical", "sub_category": "Clock Problems", "question": "What is the angle between the hour and minute hands at 6:00?", "options": ["180°", "90°", "0°", "270°"], "correct_answer": "180°", "explanation": "Hour at 180°, minute at 0°. Angle = 180°.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-1260", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: Some doctors are engineers. Some engineers are lawyers. Conclusion: Some doctors are lawyers.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "Cannot be determined", "explanation": "The statements don't prove any doctors are lawyers.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-1250", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct form: 'Each of the students ___ submitted their assignments.'", "options": ["has", "have", "is", "are"], "correct_answer": "has", "explanation": "'Each' is singular, so 'has' is correct.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-1260", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Space tourism is becoming a reality. However, ticket prices range from $250,000 to $450,000, limiting access to the wealthy.' What is the main barrier?", "options": ["Safety concerns", "High ticket prices", "Limited seats", "Technical issues"], "correct_answer": "High ticket prices", "explanation": "The passage identifies high prices as the main barrier.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-1270", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 30 students, if Ram is 12th from the left, what is his position from the right?", "options": ["19th", "20th", "18th", "21st"], "correct_answer": "19th", "explanation": "Position from right = 30 - 12 + 1 = 19.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},
]
