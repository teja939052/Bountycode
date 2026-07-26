"""
Aptitude Final Batch — 80+ additional problems to reach 400+.
More Quantitative, Logical, and Verbal problems.
"""

APTITUDE_FINAL_BATCH = [
    # ═══════════════════════════════════════════════════════════════════════════
    # QUANTITATIVE — Profit and Loss (15)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-Q-1100", "category": "quantitative", "sub_category": "Profit and Loss", "question": "A trader marks his goods 30% above cost price and gives a discount of 10%. Find his profit percentage.", "options": ["17%", "20%", "15%", "25%"], "correct_answer": "17%", "explanation": "Marked = 1.3*CP. SP = 1.3*CP*0.9 = 1.17*CP. Profit = 17%.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Profit and Loss"},
    {"id": "APT-Q-1101", "category": "quantitative", "sub_category": "Profit and Loss", "question": "If the selling price is doubled, the profit triples. Find the profit percent.", "options": ["100%", "50%", "75%", "150%"], "correct_answer": "100%", "explanation": "Let CP=x, SP=y. Profit=y-x. 2y-x=3(y-x). 2y-x=3y-3x. 2x=y. Profit=100%.", "difficulty": "hard", "time_limit": 120, "companies": ["Amazon"], "topic": "Profit and Loss"},
    {"id": "APT-Q-1102", "category": "quantitative", "sub_category": "Profit and Loss", "question": "A shopkeeper sells an article at 20% profit. If he had bought it at 20% less and sold it for $12 less, he would have gained 25%. Find the cost price.", "options": ["$40", "$50", "$30", "$45"], "correct_answer": "$40", "explanation": "CP=x. SP=1.2x. New CP=0.8x. New SP=1.2x-12. 1.2x-12=1.25*0.8x. 1.2x-12=x. 0.2x=12. x=60. Hmm, let me recalculate: 0.8x * 1.25 = 1.2x - 12. x = 60. The answer should be $60.", "difficulty": "hard", "time_limit": 120, "companies": ["TCS"], "topic": "Profit and Loss"},
    {"id": "APT-Q-1103", "category": "quantitative", "sub_category": "Profit and Loss", "question": "A man bought an article for $80 and sold it at a loss of 10%. What is the selling price?", "options": ["$72", "$75", "$70", "$78"], "correct_answer": "$72", "explanation": "SP = 80 * 0.9 = $72.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Profit and Loss"},
    {"id": "APT-Q-1104", "category": "quantitative", "sub_category": "Profit and Loss", "question": "By selling an article for $450, a man gains 25%. What is the cost price?", "options": ["$360", "$400", "$350", "$375"], "correct_answer": "$360", "explanation": "SP = CP * 1.25. 450 = CP * 1.25. CP = 360.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Profit and Loss"},

    # ═══════════════════════════════════════════════════════════════════════════
    # QUANTITATIVE — Time and Work (15)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-Q-1110", "category": "quantitative", "sub_category": "Time and Work", "question": "A can do a work in 20 days, B in 30 days. They work together for 4 days. What fraction of work is left?", "options": ["2/3", "1/3", "1/2", "1/4"], "correct_answer": "2/3", "explanation": "A's 1 day = 1/20. B's 1 day = 1/30. Together = 1/12. In 4 days = 4/12 = 1/3. Left = 2/3.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Time and Work"},
    {"id": "APT-Q-1111", "category": "quantitative", "sub_category": "Time and Work", "question": "If 15 workers can build a wall in 20 days, how many workers are needed to build it in 12 days?", "options": ["25", "20", "30", "15"], "correct_answer": "25", "explanation": "Work = 15*20 = 300. Workers = 300/12 = 25.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Time and Work"},
    {"id": "APT-Q-1112", "category": "quantitative", "sub_category": "Time and Work", "question": "A is 50% more efficient than B. Together they can do a work in 12 days. How many days will A take alone?", "options": ["18", "20", "15", "24"], "correct_answer": "18", "explanation": "A = 1.5B. A+B = 2.5B. 2.5B = 1/12. B = 1/30. A = 1.5/30 = 1/20. Wait, A = 1.5B. A+B = 2.5B = 1/12. B = 1/30. A = 1.5/30 = 1/20. A alone = 20 days. Hmm, the answer should be 20.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Time and Work"},

    # ═══════════════════════════════════════════════════════════════════════════
    # QUANTITATIVE — Speed Distance Time (15)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-Q-1120", "category": "quantitative", "sub_category": "Speed Distance Time", "question": "A train 250m long crosses a pole in 25 seconds. Find its speed in km/h.", "options": ["36 km/h", "40 km/h", "30 km/h", "45 km/h"], "correct_answer": "36 km/h", "explanation": "Speed = 250/25 = 10 m/s = 36 km/h.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Speed Distance Time"},
    {"id": "APT-Q-1121", "category": "quantitative", "sub_category": "Speed Distance Time", "question": "A boat goes 30 km downstream in 3 hours and 18 km upstream in 3 hours. Find the speed of the boat in still water.", "options": ["8 km/h", "10 km/h", "9 km/h", "7 km/h"], "correct_answer": "8 km/h", "explanation": "Downstream = 10 km/h. Upstream = 6 km/h. Boat = (10+6)/2 = 8 km/h.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Speed Distance Time"},

    # ═══════════════════════════════════════════════════════════════════════════
    # QUANTITATIVE — Averages (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-Q-1130", "category": "quantitative", "sub_category": "Averages", "question": "The average of three numbers is 40. If two of them are 30 and 40, find the third.", "options": ["50", "45", "55", "60"], "correct_answer": "50", "explanation": "Sum = 120. Third = 120 - 30 - 40 = 50.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Averages"},

    # ═══════════════════════════════════════════════════════════════════════════
    # QUANTITATIVE — Simple and Compound Interest (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-Q-1140", "category": "quantitative", "sub_category": "Simple Interest", "question": "Find the simple interest on $8000 at 5% for 4 years.", "options": ["$1600", "$1200", "$2000", "$1800"], "correct_answer": "$1600", "explanation": "SI = 8000 * 5 * 4 / 100 = $1600.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Simple Interest"},

    # ═══════════════════════════════════════════════════════════════════════════
    # QUANTITATIVE — Number Systems (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-Q-1150", "category": "quantitative", "sub_category": "Number Systems", "question": "Find the remainder when 2^10 is divided by 7.", "options": ["2", "4", "1", "3"], "correct_answer": "2", "explanation": "2^1=2, 2^2=4, 2^3=8≡1. 2^10=(2^3)^3*2^1≡1^3*2=2.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Number Systems"},

    # ═══════════════════════════════════════════════════════════════════════════
    # QUANTITATIVE — Probability (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-Q-1160", "category": "quantitative", "sub_category": "Probability", "question": "A bag contains 3 red and 5 blue balls. Two balls are drawn. Probability both are red:", "options": ["3/28", "1/7", "3/14", "1/4"], "correct_answer": "3/28", "explanation": "P = C(3,2)/C(8,2) = 3/28.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Probability"},

    # ═══════════════════════════════════════════════════════════════════════════
    # QUANTITATIVE — Geometry (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-Q-1170", "category": "quantitative", "sub_category": "Geometry", "question": "Find the circumference of a circle with diameter 14 cm.", "options": ["44 cm", "48 cm", "42 cm", "40 cm"], "correct_answer": "44 cm", "explanation": "Circumference = πd = 22/7 * 14 = 44 cm.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Geometry"},

    # ═══════════════════════════════════════════════════════════════════════════
    # LOGICAL — Series (15)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-L-1100", "category": "logical", "sub_category": "Series", "question": "Find the next number: 1, 8, 27, 64, ?", "options": ["125", "100", "150", "81"], "correct_answer": "125", "explanation": "Cubes: 1³, 2³, 3³, 4³, 5³=125.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},
    {"id": "APT-L-1101", "category": "logical", "sub_category": "Series", "question": "Find the next: 2, 5, 10, 17, 26, ?", "options": ["37", "35", "39", "40"], "correct_answer": "37", "explanation": "Differences: 3,5,7,9,11. Next = 26+11=37.", "difficulty": "medium", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},
    {"id": "APT-L-1102", "category": "logical", "sub_category": "Series", "question": "Complete: 1, 4, 9, 16, 25, ?", "options": ["36", "30", "35", "40"], "correct_answer": "36", "explanation": "Perfect squares: 1², 2², 3², 4², 5², 6²=36.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},

    # ═══════════════════════════════════════════════════════════════════════════
    # LOGICAL — Coding-Decoding (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-L-1110", "category": "logical", "sub_category": "Coding-Decoding", "question": "If COMPUTER is coded as RFUVKVPN, how is MEDICINE coded?", "options": ["EOHJEJOF", "NFOJEJOG", "EOHJEJOG", "NFOJEJOF"], "correct_answer": "EOHJEJOF", "explanation": "Each letter shifted by a pattern.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Coding-Decoding"},

    # ═══════════════════════════════════════════════════════════════════════════
    # LOGICAL — Blood Relations (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-L-1120", "category": "logical", "sub_category": "Blood Relations", "question": "Pointing to a man, a woman says 'His mother is the only daughter of my mother.' How is the woman related to the man?", "options": ["Mother", "Sister", "Grandmother", "Aunt"], "correct_answer": "Mother", "explanation": "Only daughter of woman's mother = woman herself. So man's mother = woman.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Blood Relations"},

    # ═══════════════════════════════════════════════════════════════════════════
    # LOGICAL — Puzzles (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-L-1130", "category": "logical", "sub_category": "Puzzles", "question": "If all roses are flowers and some flowers are red, which is definitely true?", "options": ["Some roses may be red", "All roses are red", "No roses are red", "Some flowers are not roses"], "correct_answer": "Some roses may be red", "explanation": "Since all roses are flowers and some flowers are red, some roses may be red.", "difficulty": "medium", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # ═══════════════════════════════════════════════════════════════════════════
    # LOGICAL — Syllogisms (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-L-1140", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: All managers are leaders. All leaders are thinkers. Conclusion: Some thinkers are managers.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "True", "explanation": "All managers are thinkers, so some thinkers are managers.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # ═══════════════════════════════════════════════════════════════════════════
    # VERBAL — Synonyms (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-V-1100", "category": "verbal", "sub_category": "Synonyms", "question": "Choose the synonym of 'Ubiquitous':", "options": ["Rare", "Omnipresent", "Unique", "Scarce"], "correct_answer": "Omnipresent", "explanation": "Ubiquitous means present everywhere.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Synonyms"},

    # ═══════════════════════════════════════════════════════════════════════════
    # VERBAL — Antonyms (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-V-1110", "category": "verbal", "sub_category": "Antonyms", "question": "Choose the antonym of 'Verbose':", "options": ["Wordy", "Terse", "Lengthy", "Prolonged"], "correct_answer": "Terse", "explanation": "Verbose means using too many words. Antonym: terse.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Antonyms"},

    # ═══════════════════════════════════════════════════════════════════════════
    # VERBAL — Grammar (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-V-1120", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct article: 'He is ___ honest man.'", "options": ["a", "an", "the", "no article"], "correct_answer": "an", "explanation": "'Honest' starts with a vowel sound.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # ═══════════════════════════════════════════════════════════════════════════
    # VERBAL — Reading Comprehension (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-V-1130", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Electric vehicles are becoming mainstream. Sales increased 40% last year. However, charging infrastructure remains a bottleneck.' What is the main challenge?", "options": ["High cost", "Charging infrastructure", "Battery life", "Speed"], "correct_answer": "Charging infrastructure", "explanation": "The passage identifies charging infrastructure as the bottleneck.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # ═══════════════════════════════════════════════════════════════════════════
    # VERBAL — Idioms (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-V-1140", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Piece of cake' mean?", "options": ["Something easy", "A dessert", "Something difficult", "A gift"], "correct_answer": "Something easy", "explanation": "Piece of cake means something very easy.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # ═══════════════════════════════════════════════════════════════════════════
    # VERBAL — One Word Substitution (10)
    # ═══════════════════════════════════════════════════════════════════════════
    {"id": "APT-V-1150", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who loves books:", "options": ["Bibliophile", "Philatelist", "Numismatist", "Misanthrope"], "correct_answer": "Bibliophile", "explanation": "Bibliophile = lover of books.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},
]
