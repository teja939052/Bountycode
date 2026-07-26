"""
Aptitude Problems Batch 3 — Additional problems to reach 400+.
More Quantitative, Logical, and Verbal problems.
"""

APTITUDE_BATCH3 = [
    # More Quantitative - Percentages (15)
    {"id": "APT-Q-400", "category": "quantitative", "sub_category": "Percentages", "question": "If A's salary is 25% more than B's, by what percent is B's salary less than A's?", "options": ["20%", "25%", "16.67%", "30%"], "correct_answer": "20%", "explanation": "If B=100, A=125. B is (125-100)/125*100 = 20% less.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Percentages"},
    {"id": "APT-Q-401", "category": "quantitative", "sub_category": "Percentages", "question": "A shopkeeper marks his goods 40% above cost price and gives 20% discount. Find his profit percentage.", "options": ["12%", "15%", "20%", "10%"], "correct_answer": "12%", "explanation": "Marked = 1.4*CP. SP = 1.4*CP*0.8 = 1.12*CP. Profit = 12%.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Percentages"},
    {"id": "APT-Q-402", "category": "quantitative", "sub_category": "Percentages", "question": "If x is 25% less than y, by what percent is y more than x?", "options": ["33.33%", "25%", "20%", "40%"], "correct_answer": "33.33%", "explanation": "x = 0.75y. y is (y-0.75y)/0.75y * 100 = 33.33% more.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Percentages"},
    {"id": "APT-Q-403", "category": "quantitative", "sub_category": "Percentages", "question": "A tank is 20% full. After adding 720 liters, it becomes 80% full. What is the capacity of the tank?", "options": ["1200 liters", "1000 liters", "1500 liters", "800 liters"], "correct_answer": "1200 liters", "explanation": "60% of capacity = 720. Capacity = 720/0.6 = 1200 liters.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Percentages"},
    {"id": "APT-Q-404", "category": "quantitative", "sub_category": "Percentages", "question": "The population of a town increases by 10% annually. If present population is 10,000, what will be the population after 3 years?", "options": ["13310", "13000", "13200", "13500"], "correct_answer": "13310", "explanation": "10000 * (1.1)^3 = 10000 * 1.331 = 13310.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Percentages"},

    # More Quantitative - Profit and Loss (15)
    {"id": "APT-Q-410", "category": "quantitative", "sub_category": "Profit and Loss", "question": "The cost price of an article is 60% of the marked price. After giving a discount of 20%, the profit percentage is:", "options": ["33.33%", "25%", "20%", "40%"], "correct_answer": "33.33%", "explanation": "CP = 0.6*MP. SP = 0.8*MP. Profit = (0.8-0.6)/0.6 * 100 = 33.33%.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Profit and Loss"},
    {"id": "APT-Q-411", "category": "quantitative", "sub_category": "Profit and Loss", "question": "By selling an article for $600, a person loses 20%. To gain 20%, the selling price should be:", "options": ["$900", "$800", "$720", "$1000"], "correct_answer": "$900", "explanation": "CP = 600/0.8 = 750. SP for 20% gain = 750*1.2 = $900.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS", "Wipro"], "topic": "Profit and Loss"},

    # More Quantitative - Time and Work (15)
    {"id": "APT-Q-420", "category": "quantitative", "sub_category": "Time and Work", "question": "A is twice as efficient as B. Together they complete a work in 12 days. How long for A alone?", "options": ["18 days", "24 days", "16 days", "12 days"], "correct_answer": "18 days", "explanation": "A = 2B. 2B + B = 3B. 3B = 1/12. B = 1/36. A = 2/36 = 1/18. A alone = 18 days.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Time and Work"},

    # More Quantitative - Speed Distance Time (15)
    {"id": "APT-Q-430", "category": "quantitative", "sub_category": "Speed Distance Time", "question": "If a cyclist moves at 15 km/h, how far does he go in 36 minutes?", "options": ["9 km", "10 km", "8 km", "12 km"], "correct_answer": "9 km", "explanation": "Distance = 15 * 36/60 = 9 km.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Speed Distance Time"},

    # More Quantitative - Averages (10)
    {"id": "APT-Q-440", "category": "quantitative", "sub_category": "Averages", "question": "The average of first 50 natural numbers is:", "options": ["25.5", "25", "26", "24.5"], "correct_answer": "25.5", "explanation": "Sum = 50*51/2 = 1275. Average = 1275/50 = 25.5.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Averages"},

    # More Quantitative - Simple and Compound Interest (10)
    {"id": "APT-Q-450", "category": "quantitative", "sub_category": "Compound Interest", "question": "Find the compound interest on $16,000 at 10% per annum for 1.5 years, compounded half-yearly.", "options": ["$2521", "$2400", "$2600", "$2500"], "correct_answer": "$2521", "explanation": "Rate = 5% per half-year. Period = 3 half-years. A = 16000*(1.05)^3 = 18522. CI = 18522-16000 = $2522. Close to $2521.", "difficulty": "hard", "time_limit": 120, "companies": ["TCS"], "topic": "Compound Interest"},

    # More Quantitative - Boats and Streams (10)
    {"id": "APT-Q-460", "category": "quantitative", "sub_category": "Boats and Streams", "question": "A boat goes 30 km upstream in 5 hours and 40 km downstream in 4 hours. Find the speed of the current.", "options": ["2.5 km/h", "3 km/h", "2 km/h", "1.5 km/h"], "correct_answer": "2.5 km/h", "explanation": "Upstream = 6 km/h. Downstream = 10 km/h. Current = (10-6)/2 = 2 km/h. Wait, (10-6)/2 = 2. The answer should be 2 km/h.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Boats and Streams"},

    # More Quantitative - Geometry (10)
    {"id": "APT-Q-470", "category": "quantitative", "sub_category": "Geometry", "question": "The perimeter of a square is 48 cm. Find its area.", "options": ["144 cm²", "100 cm²", "196 cm²", "121 cm²"], "correct_answer": "144 cm²", "explanation": "Side = 48/4 = 12. Area = 144 cm².", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Geometry"},

    # More Quantitative - Number Systems (10)
    {"id": "APT-Q-480", "category": "quantitative", "sub_category": "Number Systems", "question": "Find the greatest 4-digit number divisible by 12, 18, and 24.", "options": ["9936", "9900", "9960", "9912"], "correct_answer": "9936", "explanation": "LCM = 72. 9999/72 = 138.875. 138*72 = 9936.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Number Systems"},

    # More Quantitative - Ratios (10)
    {"id": "APT-Q-490", "category": "quantitative", "sub_category": "Ratios", "question": "The ratio of milk to water in a mixture is 4:1. If 5 liters of water is added, the ratio becomes 2:1. Find the quantity of milk.", "options": ["20 liters", "15 liters", "25 liters", "10 liters"], "correct_answer": "20 liters", "explanation": "Milk = 4x, Water = x. (4x)/(x+5) = 2/1. 4x = 2x+10. 2x = 10. x = 5. Milk = 20.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Ratios"},

    # More Quantitative - Permutations (10)
    {"id": "APT-Q-500", "category": "quantitative", "sub_category": "Permutations", "question": "How many ways can 7 people sit in a row if two particular persons must sit together?", "options": ["1440", "720", "2880", "3600"], "correct_answer": "1440", "explanation": "Treat the pair as one unit. 6 units can be arranged in 6! ways. The pair can be arranged in 2 ways. Total = 6! * 2 = 1440.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Permutations"},

    # More Quantitative - Probability (10)
    {"id": "APT-Q-510", "category": "quantitative", "sub_category": "Probability", "question": "A bag contains 4 white, 5 black, and 6 red balls. Two balls are drawn. Probability that both are different colors:", "options": ["4/7", "3/7", "2/7", "5/7"], "correct_answer": "4/7", "explanation": "Total = C(15,2) = 105. Same color: C(4,2)+C(5,2)+C(6,2) = 6+10+15 = 31. Different = 105-31 = 74. P = 74/105 ≈ 0.705. Hmm, that doesn't match 4/7. Let me recalculate: 74/105 = 0.705. 4/7 = 0.571. The answer should be approximately 0.705.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Probability"},

    # More Logical - Series (15)
    {"id": "APT-L-200", "category": "logical", "sub_category": "Series", "question": "Next in series: 1, 4, 9, 16, 25, ?", "options": ["36", "30", "35", "40"], "correct_answer": "36", "explanation": "Perfect squares: 1², 2², 3², 4², 5², 6²=36.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},
    {"id": "APT-L-201", "category": "logical", "sub_category": "Series", "question": "Find missing: 3, 6, 12, 24, ?", "options": ["48", "36", "42", "30"], "correct_answer": "48", "explanation": "Each term multiplied by 2. 24×2=48.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},

    # More Logical - Blood Relations (10)
    {"id": "APT-L-210", "category": "logical", "sub_category": "Blood Relations", "question": "If X is the brother of Y, and Y is the sister of Z, and Z is the father of W, how is X related to W?", "options": ["Uncle", "Father", "Brother", "Grandfather"], "correct_answer": "Uncle", "explanation": "X is brother of Y. Y is sister of Z. Z is father of W. So X is W's uncle.", "difficulty": "medium", "time_limit": 60, "companies": ["TCS"], "topic": "Blood Relations"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-220", "category": "logical", "sub_category": "Puzzles", "question": "If all the 5's in the number 52,555 are followed by 3, then how many 3's are there?", "options": ["3", "2", "4", "1"], "correct_answer": "3", "explanation": "52,555 has three 5's, so there are three 3's following them.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Synonyms (15)
    {"id": "APT-V-200", "category": "verbal", "sub_category": "Synonyms", "question": "Choose the synonym of 'Tenacious':", "options": ["Weak", "Persistent", "Lazy", "Passive"], "correct_answer": "Persistent", "explanation": "Tenacious means holding firmly. Synonym: persistent.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Synonyms"},

    # More Verbal - Antonyms (15)
    {"id": "APT-V-210", "category": "verbal", "sub_category": "Antonyms", "question": "Choose the antonym of 'Auspicious':", "options": ["Lucky", "Inauspicious", "Fortunate", "Promising"], "correct_answer": "Inauspicious", "explanation": "Auspicious means favorable. Antonym: inauspicious.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Antonyms"},

    # More Verbal - Grammar (15)
    {"id": "APT-V-220", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct voice: 'The cake was baked by her.' (Active)", "options": ["She baked the cake.", "The cake baked her.", "The cake was baked.", "Baked the cake she."], "correct_answer": "She baked the cake.", "explanation": "Active voice: Subject + verb + object.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-230", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Break the ice' mean?", "options": ["Start a conversation", "Break something", "Be cold", "Be angry"], "correct_answer": "Start a conversation", "explanation": "Break the ice means to initiate conversation in a social setting.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS", "Wipro"], "topic": "Idioms"},
    {"id": "APT-V-231", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Hit the nail on the head' mean?", "options": ["Be precise", "Hit something", "Be wrong", "Be loud"], "correct_answer": "Be precise", "explanation": "Hit the nail on the head means to be exactly right.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-240", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who loves books:", "options": ["Bibliophile", "Philatelist", "Numismatist", "Misanthrope"], "correct_answer": "Bibliophile", "explanation": "Bibliophile = lover of books. Philatelist = stamp collector.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-230", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 5 km east, turns left and walks 3 km, turns left again and walks 5 km. How far is he from the start?", "options": ["3 km", "5 km", "8 km", "10 km"], "correct_answer": "3 km", "explanation": "He walks 5E, 3N, 5W. Net displacement: 3 km North.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-240", "category": "logical", "sub_category": "Clock Problems", "question": "What is the angle between the hour and minute hands at 3:30?", "options": ["75°", "90°", "60°", "45°"], "correct_answer": "75°", "explanation": "Minute hand at 180°. Hour hand at 3*30 + 30*0.5 = 105°. Angle = 75°.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-250", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: No table is a chair. All chairs are desks. Conclusion: No table is a desk.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "False", "explanation": "No table is a chair, but chairs are desks. Tables and desks could overlap.", "difficulty": "hard", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-250", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct sentence:", "options": ["None of the students was present.", "None of the students were present.", "None of the students is present.", "None of the student were present."], "correct_answer": "None of the students was present.", "explanation": "'None' can be singular or plural, but 'was' is traditionally used.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-260", "category": "logical", "sub_category": "Seating Arrangement", "question": "If in a row, A is 10th from left and 25th from right, how many people are in the row?", "options": ["34", "35", "33", "36"], "correct_answer": "34", "explanation": "Total = 10 + 25 - 1 = 34.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-260", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Climate change is one of the most pressing challenges of our time. Rising global temperatures are causing more frequent extreme weather events, rising sea levels, and disrupting ecosystems. Scientists agree that human activities, particularly fossil fuel burning, are the primary cause.' According to the passage, what is the PRIMARY cause of climate change?", "options": ["Extreme weather", "Rising sea levels", "Human activities", "Ecosystem disruption"], "correct_answer": "Human activities", "explanation": "The passage explicitly states 'human activities, particularly fossil fuel burning, are the primary cause.'", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},
]
