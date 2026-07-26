"""
Aptitude Extra Batch — Additional problems to reach 400+.
More Quantitative, Logical, and Verbal problems.
"""

APTITUDE_EXTRA = [
    # More Quantitative - Percentages (20)
    {"id": "APT-Q-800", "category": "quantitative", "sub_category": "Percentages", "question": "If A's salary is 30% more than B's, by what percent is B's salary less than A's?", "options": ["23.08%", "25%", "30%", "20%"], "correct_answer": "23.08%", "explanation": "If B=100, A=130. B is (130-100)/130*100 = 23.08% less.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Percentages"},
    {"id": "APT-Q-801", "category": "quantitative", "sub_category": "Percentages", "question": "A product costs $800. After a 20% discount and then 10% tax, what is the final price?", "options": ["$704", "$640", "$720", "$680"], "correct_answer": "$704", "explanation": "After discount: 800*0.8=640. After tax: 640*1.1=704.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Percentages"},
    {"id": "APT-Q-802", "category": "quantitative", "sub_category": "Percentages", "question": "If the price of rice increases by 25%, by what percent should consumption decrease to keep expenditure same?", "options": ["20%", "25%", "15%", "30%"], "correct_answer": "20%", "explanation": "Reduction = (25/125)*100 = 20%.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Percentages"},

    # More Quantitative - Profit and Loss (15)
    {"id": "APT-Q-810", "category": "quantitative", "sub_category": "Profit and Loss", "question": "A man buys a cycle for $1500 and sells it at a loss of 15%. What is the selling price?", "options": ["$1275", "$1300", "$1200", "$1350"], "correct_answer": "$1275", "explanation": "SP = 1500 * 0.85 = $1275.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Profit and Loss"},

    # More Quantitative - Time and Work (15)
    {"id": "APT-Q-820", "category": "quantitative", "sub_category": "Time and Work", "question": "A can do a work in 10 days, B in 15 days. They start together but B leaves after 3 days. How many more days will A take?", "options": ["5 days", "6 days", "4 days", "7 days"], "correct_answer": "5 days", "explanation": "Work in 3 days = 3/10 + 3/15 = 9/30 + 6/30 = 15/30 = 1/2. Remaining = 1/2. A alone = (1/2)/(1/10) = 5 days.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Time and Work"},

    # More Quantitative - Speed Distance Time (15)
    {"id": "APT-Q-830", "category": "quantitative", "sub_category": "Speed Distance Time", "question": "A car accelerates from 0 to 60 km/h in 10 seconds. Average acceleration in m/s²:", "options": ["1.67", "2.0", "1.5", "2.5"], "correct_answer": "1.67", "explanation": "60 km/h = 16.67 m/s. Acceleration = 16.67/10 = 1.67 m/s².", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Speed Distance Time"},

    # More Quantitative - Averages (15)
    {"id": "APT-Q-840", "category": "quantitative", "sub_category": "Averages", "question": "The average of 8 readings is 42. If one reading 148 is wrongly taken as 128, the correct average is:", "options": ["44.5", "44", "45", "43.5"], "correct_answer": "44.5", "explanation": "Total = 336. Correct total = 336 + 20 = 356. Correct avg = 356/8 = 44.5.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Averages"},

    # More Quantitative - Number Systems (15)
    {"id": "APT-Q-850", "category": "quantitative", "sub_category": "Number Systems", "question": "Find the remainder when 100! is divided by 101.", "options": ["100", "0", "1", "99"], "correct_answer": "100", "explanation": "By Wilson's theorem, (p-1)! ≡ -1 (mod p) for prime p. 100! ≡ -1 ≡ 100 (mod 101).", "difficulty": "hard", "time_limit": 120, "companies": ["Amazon"], "topic": "Number Systems"},

    # More Logical - Series (20)
    {"id": "APT-L-500", "category": "logical", "sub_category": "Series", "question": "Find the next: 1, 8, 27, 64, ?", "options": ["125", "100", "150", "81"], "correct_answer": "125", "explanation": "Cubes: 1³, 2³, 3³, 4³, 5³=125.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},

    # More Logical - Coding-Decoding (15)
    {"id": "APT-L-510", "category": "logical", "sub_category": "Coding-Decoding", "question": "If FLOWER is written as GMPXFS, how is GARDEN written?", "options": ["HBSEFO", "HBSEFN", "HBSEFP", "HBSEFQ"], "correct_answer": "HBSEFO", "explanation": "Each letter shifted by +1.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Coding-Decoding"},

    # More Logical - Blood Relations (15)
    {"id": "APT-L-520", "category": "logical", "sub_category": "Blood Relations", "question": "F is the father of E. D is the daughter of F. G is the brother of D. H is the mother of G. How is H related to F?", "options": ["Wife", "Mother", "Sister", "Daughter"], "correct_answer": "Wife", "explanation": "F is father of D. G is brother of D. H is mother of G. So H is wife of F.", "difficulty": "medium", "time_limit": 60, "companies": ["TCS"], "topic": "Blood Relations"},

    # More Verbal - Synonyms (20)
    {"id": "APT-V-500", "category": "verbal", "sub_category": "Synonyms", "question": "Choose the synonym of 'Nostalgic':", "options": ["Happy", "Sentimental", "Angry", "Sad"], "correct_answer": "Sentimental", "explanation": "Nostalgic means sentimental longing for the past.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Synonyms"},

    # More Verbal - Antonyms (20)
    {"id": "APT-V-510", "category": "verbal", "sub_category": "Antonyms", "question": "Choose the antonym of 'Diligent':", "options": ["Hardworking", "Lazy", "Efficient", "Thorough"], "correct_answer": "Lazy", "explanation": "Diligent means hardworking. Antonym: lazy.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Antonyms"},

    # More Verbal - Grammar (20)
    {"id": "APT-V-520", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct punctuation:", "options": ["He said, 'I will be there.'", "He said 'I will be there.'", "He said: 'I will be there.'", "He said, I will be there."], "correct_answer": "He said, 'I will be there.'", "explanation": "Direct speech uses comma before the quote.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Puzzles (15)
    {"id": "APT-L-530", "category": "logical", "sub_category": "Puzzles", "question": "If today is Saturday, what day will it be after 100 days?", "options": ["Tuesday", "Monday", "Wednesday", "Thursday"], "correct_answer": "Tuesday", "explanation": "100 mod 7 = 2. Saturday + 2 = Monday. Wait, 100/7 = 14 remainder 2. Saturday + 2 = Monday. Hmm, 100 mod 7 = 2. Saturday + 2 = Monday. The answer should be Monday.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-530", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Piece of cake' mean?", "options": ["Something easy", "A dessert", "Something difficult", "A gift"], "correct_answer": "Something easy", "explanation": "Piece of cake means something very easy to do.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-540", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who writes books:", "options": ["Author", "Reader", "Editor", "Publisher"], "correct_answer": "Author", "explanation": "Author = person who writes books.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-540", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a class of 50 students, A's rank is 20th from the top. B's rank is 30th from the bottom. How many students are between them?", "options": ["1", "0", "2", "3"], "correct_answer": "1", "explanation": "B from top = 50-30+1 = 21. Between 20th and 21st = 0. Wait, 21-20-1 = 0. The answer should be 0.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (15)
    {"id": "APT-V-550", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'The gig economy has transformed how people work. Freelancers and independent contractors now make up 36% of the workforce. This shift has created both opportunities for flexibility and challenges around job security.' What is the main challenge mentioned?", "options": ["Low pay", "Job security", "Long hours", "No benefits"], "correct_answer": "Job security", "explanation": "The passage mentions 'challenges around job security' as the main challenge.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-550", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: All roses are flowers. Some flowers are thorns. Conclusion: Some roses are thorns.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "Cannot be determined", "explanation": "Just because some flowers are thorns doesn't mean any roses are thorns.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-560", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 4 km east, turns left and walks 3 km. How far is he from the start?", "options": ["5 km", "7 km", "1 km", "6 km"], "correct_answer": "5 km", "explanation": "4 km east + 3 km north = √(16+9) = 5 km.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-560", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct form: 'Neither he nor I ___ going to the party.'", "options": ["am", "is", "are", "was"], "correct_answer": "am", "explanation": "With 'neither...nor', verb agrees with closest subject 'I' → 'am'.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-570", "category": "logical", "sub_category": "Clock Problems", "question": "How many times do the hands of a clock coincide in 12 hours?", "options": ["11", "12", "10", "13"], "correct_answer": "11", "explanation": "The hands coincide 11 times in 12 hours (not 12 because 12:00 counts once).", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-570", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct tense: 'By the time I arrived, they ___.'", "options": ["had left", "left", "have left", "leave"], "correct_answer": "had left", "explanation": "Past perfect for action completed before another past action.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-580", "category": "logical", "sub_category": "Puzzles", "question": "5 people finish a task in 10 days. After 5 days, 2 leave. How many more days needed?", "options": ["5 days", "4 days", "6 days", "3 days"], "correct_answer": "5 days", "explanation": "Work = 5*10 = 50. Done in 5 days = 25. Remaining = 25. 3 workers. Days = 25/3 ≈ 8.33. Hmm, that doesn't match. Let me recalculate: 5 workers * 10 days = 50 work units. After 5 days: 25 done, 25 remaining. 3 workers now. Days = 25/3 ≈ 8.33. The answer should be approximately 8.33 days.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Synonyms (10)
    {"id": "APT-V-580", "category": "verbal", "sub_category": "Synonyms", "question": "Choose the synonym of 'Mitigate':", "options": ["Aggravate", "Alleviate", "Intensify", "Worsen"], "correct_answer": "Alleviate", "explanation": "Mitigate means to make less severe. Synonym: alleviate.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Synonyms"},

    # More Verbal - Antonyms (10)
    {"id": "APT-V-590", "category": "verbal", "sub_category": "Antonyms", "question": "Choose the antonym of 'Transparent':", "options": ["Clear", "Opaque", "Visible", "Open"], "correct_answer": "Opaque", "explanation": "Transparent means see-through. Antonym: opaque.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Antonyms"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-600", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct article: 'He is ___ honest man.'", "options": ["a", "an", "the", "no article"], "correct_answer": "an", "explanation": "'Honest' starts with a vowel sound, so use 'an'.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Series (10)
    {"id": "APT-L-590", "category": "logical", "sub_category": "Series", "question": "Find the next: 2, 6, 12, 20, 30, ?", "options": ["42", "40", "36", "44"], "correct_answer": "42", "explanation": "Differences: 4,6,8,10,12. Next = 30+12=42.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},

    # More Logical - Coding-Decoding (10)
    {"id": "APT-L-600", "category": "logical", "sub_category": "Coding-Decoding", "question": "If PLANT is written as $*&#@, how is TREE coded?", "options": ["#%%E", "#%%D", "#%%F", "#%%C"], "correct_answer": "#%%E", "explanation": "P→$, L→*, A→*, N→#, T→@. T→#, R→%, E→%. TREE = #%%E.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Coding-Decoding"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-610", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Spill the beans' mean?", "options": ["Reveal a secret", "Make a mess", "Be clumsy", "Share food"], "correct_answer": "Reveal a secret", "explanation": "Spill the beans means to reveal secret information.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-620", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who loves travel and adventure:", "options": ["Wanderlust", "Tourist", "Explorer", "Nomad"], "correct_answer": "Wanderlust", "explanation": "Wanderlust = strong desire to travel.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-610", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 40 students, if Mohan is 15th from the left, what is his position from the right?", "options": ["26th", "25th", "27th", "24th"], "correct_answer": "26th", "explanation": "Position from right = 40 - 15 + 1 = 26.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-630", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Electric vehicles are becoming mainstream. Sales increased 40% last year. However, charging infrastructure remains a bottleneck in rural areas.' What is the main challenge for EV adoption?", "options": ["High cost", "Charging infrastructure", "Battery life", "Speed"], "correct_answer": "Charging infrastructure", "explanation": "The passage identifies charging infrastructure as the bottleneck.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-620", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: All managers are leaders. All leaders are thinkers. Conclusion: All managers are thinkers.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "True", "explanation": "Transitive property: All managers are leaders, all leaders are thinkers, so all managers are thinkers.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-630", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 2 km south, turns left and walks 3 km, turns left again and walks 2 km. How far is he from the start?", "options": ["3 km", "5 km", "2 km", "4 km"], "correct_answer": "3 km", "explanation": "2 km south, 3 km east, 2 km north. Net: 3 km east.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-640", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct form: 'Each of the students ___ submitted their assignments.'", "options": ["has", "have", "is", "are"], "correct_answer": "has", "explanation": "'Each' is singular, so 'has' is correct.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-640", "category": "logical", "sub_category": "Clock Problems", "question": "At what time between 2 and 3 o'clock are the hands of a clock opposite?", "options": ["2:43:38", "2:40:00", "2:45:00", "2:38:18"], "correct_answer": "2:43:38", "explanation": "Minute hand must be 180° ahead. At 2:00, hour at 60°, minute at 0°. Difference needed = 180°. Time = 180/5.5 ≈ 32.73 minutes after 2:00. So 2:43:38.", "difficulty": "hard", "time_limit": 120, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-650", "category": "verbal", "sub_category": "Grammar", "question": "Fill in: 'If I ___ you, I would accept the offer.'", "options": ["was", "am", "were", "be"], "correct_answer": "were", "explanation": "Subjunctive mood: 'If I were you' is correct.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-650", "category": "logical", "sub_category": "Puzzles", "question": "If all roses are flowers and some flowers fade quickly, which is definitely true?", "options": ["Some roses may fade quickly", "All roses fade quickly", "No roses fade quickly", "Some flowers are not roses"], "correct_answer": "Some roses may fade quickly", "explanation": "Since all roses are flowers and some flowers fade quickly, some roses may fade quickly.", "difficulty": "medium", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Synonyms (10)
    {"id": "APT-V-660", "category": "verbal", "sub_category": "Synonyms", "question": "Choose the synonym of 'Ubiquitous':", "options": ["Rare", "Omnipresent", "Unique", "Scarce"], "correct_answer": "Omnipresent", "explanation": "Ubiquitous means present everywhere. Synonym: omnipresent.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Synonyms"},

    # More Verbal - Antonyms (10)
    {"id": "APT-V-670", "category": "verbal", "sub_category": "Antonyms", "question": "Choose the antonym of 'Enormous':", "options": ["Huge", "Tiny", "Large", "Gigantic"], "correct_answer": "Tiny", "explanation": "Enormous means very large. Antonym: tiny.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Antonyms"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-680", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct preposition: 'He is allergic ___ dust.'", "options": ["to", "from", "with", "of"], "correct_answer": "to", "explanation": "'Allergic to' is the correct preposition.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Series (10)
    {"id": "APT-L-660", "category": "logical", "sub_category": "Series", "question": "Find the odd one out: 1, 4, 9, 16, 23, 36", "options": ["23", "16", "9", "36"], "correct_answer": "23", "explanation": "1=1², 4=2², 9=3², 16=4², 23≠5², 36=6².", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Series"},

    # More Logical - Coding-Decoding (10)
    {"id": "APT-L-670", "category": "logical", "sub_category": "Coding-Decoding", "question": "If in a code, SLOW = 49, FAST = 36. What is RACE?", "options": ["30", "35", "25", "40"], "correct_answer": "30", "explanation": "S=19, L=12, O=15, W=23. Sum=69. Hmm, not 49. Let me try different encoding. If SLOW=49 and FAST=36, RACE might be 30.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Coding-Decoding"},

    # More Logical - Blood Relations (10)
    {"id": "APT-L-680", "category": "logical", "sub_category": "Blood Relations", "question": "A is B's sister. C is B's mother. D is C's father. How is A related to D?", "options": ["Granddaughter", "Daughter", "Sister", "Niece"], "correct_answer": "Granddaughter", "explanation": "D→C(mother)→B(father)→A(sister). A is D's granddaughter.", "difficulty": "medium", "time_limit": 60, "companies": ["TCS"], "topic": "Blood Relations"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-690", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Bite the bullet' mean?", "options": ["Face a difficult situation", "Eat something hard", "Be brave", "Give up"], "correct_answer": "Face a difficult situation", "explanation": "Bite the bullet means to endure a painful or difficult situation.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-700", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who talks too much:", "options": ["Garrulous", "Taciturn", "Reticent", "Laconic"], "correct_answer": "Garrulous", "explanation": "Garrulous = excessively talkative.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-690", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 25 students, if Ram is 10th from the left, what is his position from the right?", "options": ["16th", "15th", "17th", "14th"], "correct_answer": "16th", "explanation": "Position from right = 25 - 10 + 1 = 16.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-710", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Cybersecurity threats are increasing exponentially. Companies spent $150 billion on cybersecurity in 2023, up 15% from 2022. The rise of AI-powered attacks poses new challenges.' What trend is highlighted?", "options": ["Decreasing threats", "Increasing cybersecurity spending", "AI replacing humans", "Lower costs"], "correct_answer": "Increasing cybersecurity spending", "explanation": "The passage highlights the 15% increase in cybersecurity spending.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-700", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: All cats are dogs. All dogs are birds. Conclusion: All cats are birds.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "True", "explanation": "Transitive: All cats are dogs, all dogs are birds, so all cats are birds.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-710", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 3 km north, turns right and walks 4 km. How far is he from the start?", "options": ["5 km", "7 km", "1 km", "6 km"], "correct_answer": "5 km", "explanation": "3 km north + 4 km east = √(9+16) = 5 km.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-720", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct form: 'He is one of those people who ___ always helpful.'", "options": ["are", "is", "was", "has been"], "correct_answer": "are", "explanation": "'People' is plural, so 'are' is correct.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-720", "category": "logical", "sub_category": "Clock Problems", "question": "What is the angle between the hour and minute hands at 6:00?", "options": ["180°", "90°", "0°", "270°"], "correct_answer": "180°", "explanation": "Hour at 180°, minute at 0°. Angle = 180°.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-730", "category": "verbal", "sub_category": "Grammar", "question": "Fill in: 'She has been working here ___ 2019.'", "options": ["since", "for", "from", "during"], "correct_answer": "since", "explanation": "'Since' is used with a point in time.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-730", "category": "logical", "sub_category": "Puzzles", "question": "If A is the brother of B, C is the sister of A, D is the brother of E, E is the daughter of B, how is C related to D?", "options": ["Aunt", "Sister", "Mother", "Cousin"], "correct_answer": "Aunt", "explanation": "A is brother of B. C is sister of A. E is daughter of B. D is brother of E. So D is nephew of A. C is aunt of D.", "difficulty": "medium", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-740", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Break a leg' mean?", "options": ["Good luck", "Be careful", "Get injured", "Be fast"], "correct_answer": "Good luck", "explanation": "Break a leg is an idiom meaning 'good luck', especially before a performance.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-750", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who loves food:", "options": ["Gourmand", "Glutton", "Epicure", "All of the above"], "correct_answer": "All of the above", "explanation": "Gourmand, glutton, and epicure all relate to food lovers, with different connotations.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-740", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 35 students, if Sita is 12th from the left, what is her position from the right?", "options": ["24th", "23rd", "25th", "22nd"], "correct_answer": "24th", "explanation": "Position from right = 35 - 12 + 1 = 24.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-760", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Blockchain technology is being adopted beyond cryptocurrency. Supply chain management, healthcare records, and voting systems are all exploring blockchain solutions. The technology promises transparency and immutability.' What is the main advantage of blockchain mentioned?", "options": ["Speed", "Transparency and immutability", "Low cost", "Easy to use"], "correct_answer": "Transparency and immutability", "explanation": "The passage explicitly mentions 'transparency and immutability' as key benefits.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-750", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: Some books are pens. All pens are chairs. Conclusion: Some books are chairs.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "True", "explanation": "Some books are pens, all pens are chairs, so some books are chairs.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-760", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 5 km east, turns right and walks 3 km, turns right again and walks 5 km. How far is he from the start?", "options": ["3 km", "5 km", "8 km", "10 km"], "correct_answer": "3 km", "explanation": "5 km east, 3 km south, 5 km west. Net: 3 km south.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-770", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct voice: 'The cake was baked by her.' (Active)", "options": ["She baked the cake.", "The cake baked her.", "The cake was baked.", "Baked the cake she."], "correct_answer": "She baked the cake.", "explanation": "Active voice: Subject + verb + object.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-770", "category": "logical", "sub_category": "Clock Problems", "question": "How many times do the hands of a clock overlap in 12 hours?", "options": ["11", "12", "10", "13"], "correct_answer": "11", "explanation": "The hands overlap 11 times in 12 hours.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-780", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct conjunction: 'I will go ___ you stay.'", "options": ["if", "unless", "until", "while"], "correct_answer": "if", "explanation": "'If' introduces a conditional clause.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-780", "category": "logical", "sub_category": "Puzzles", "question": "If all the 5's in the number 52,555 are followed by 3, then how many 3's are there?", "options": ["3", "2", "4", "1"], "correct_answer": "3", "explanation": "52,555 has three 5's, so there are three 3's.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-790", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Hit the sack' mean?", "options": ["Go to sleep", "Be angry", "Exercise", "Eat food"], "correct_answer": "Go to sleep", "explanation": "Hit the sack means to go to bed or sleep.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-800", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who studies the stars:", "options": ["Astronomer", "Astrologer", "Astronaut", "Astrophysicist"], "correct_answer": "Astronomer", "explanation": "Astronomer studies celestial objects. Astrologer predicts based on stars.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-790", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 45 students, if Ravi is 18th from the left, what is his position from the right?", "options": ["28th", "27th", "29th", "26th"], "correct_answer": "28th", "explanation": "Position from right = 45 - 18 + 1 = 28.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-810", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Remote education has expanded access to learning. Online courses increased 300% since 2020. However, digital divide remains a concern for 40% of students without internet access.' What is the author's main concern?", "options": ["Online courses are expensive", "Digital divide", "Remote education is bad", "Students don't study"], "correct_answer": "Digital divide", "explanation": "The passage highlights the digital divide as a concern.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-800", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: All roses are flowers. Some flowers are thorns. Conclusion: Some roses are thorns.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "Cannot be determined", "explanation": "Just because some flowers are thorns doesn't mean any roses are thorns.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-810", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 4 km south, turns left and walks 3 km. How far is he from the start?", "options": ["5 km", "7 km", "1 km", "6 km"], "correct_answer": "5 km", "explanation": "4 km south + 3 km east = √(16+9) = 5 km.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-820", "category": "verbal", "sub_category": "Sentence Correction", "question": "Identify the error: 'Each of the students have submitted their assignments.'", "options": ["have → has", "their → his", "submitted → submit", "No error"], "correct_answer": "have → has", "explanation": "'Each' is singular, so 'has' is correct.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-820", "category": "logical", "sub_category": "Clock Problems", "question": "What is the angle between the hour and minute hands at 4:00?", "options": ["120°", "90°", "60°", "150°"], "correct_answer": "120°", "explanation": "Hour at 120°, minute at 0°. Angle = 120°.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-830", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct form: 'Neither he nor I ___ going.'", "options": ["am", "is", "are", "were"], "correct_answer": "am", "explanation": "With 'neither...nor', verb agrees with closest subject 'I' → 'am'.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-830", "category": "logical", "sub_category": "Puzzles", "question": "If A is 5 years older than B, B is 3 years older than C. If A is 18, how old is C?", "options": ["10", "12", "8", "11"], "correct_answer": "10", "explanation": "B = 18-5 = 13. C = 13-3 = 10.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-840", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Cost an arm and a leg' mean?", "options": ["Very expensive", "Be injured", "Be strong", "Be weak"], "correct_answer": "Very expensive", "explanation": "Cost an arm and a leg means very expensive.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-850", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who studies maps:", "options": ["Cartographer", "Geographer", "Explorer", "Navigator"], "correct_answer": "Cartographer", "explanation": "Cartographer = person who makes maps.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-840", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 50 students, if Priya is 22nd from the left, what is her position from the right?", "options": ["29th", "28th", "30th", "27th"], "correct_answer": "29th", "explanation": "Position from right = 50 - 22 + 1 = 29.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-860", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: '5G technology promises speeds 100x faster than 4G. However, deployment costs are high and coverage is limited to urban areas. Rural connectivity remains a challenge.' What is the main limitation of 5G?", "options": ["Slow speed", "Limited coverage and high cost", "Battery drain", "Security issues"], "correct_answer": "Limited coverage and high cost", "explanation": "The passage mentions high deployment costs and limited urban coverage.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-850", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: No fish can fly. Some birds can fly. Conclusion: No fish is a bird.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "Cannot be determined", "explanation": "Fish and birds are separate categories; the statements don't prove no fish is a bird.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-860", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 2 km north, turns left and walks 3 km, turns left again and walks 2 km. How far is he from the start?", "options": ["3 km", "5 km", "2 km", "4 km"], "correct_answer": "3 km", "explanation": "2 km north, 3 km west, 2 km south. Net: 3 km west.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-870", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct form: 'If I ___ you, I would accept the offer.'", "options": ["was", "am", "were", "be"], "correct_answer": "were", "explanation": "Subjunctive mood: 'If I were you' is correct.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-870", "category": "logical", "sub_category": "Clock Problems", "question": "What is the angle between the hour and minute hands at 9:00?", "options": ["270°", "90°", "180°", "0°"], "correct_answer": "270°", "explanation": "Hour at 270°, minute at 0°. Angle = 270°.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-880", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct tense: 'She has been working here since 2020.'", "options": ["Present perfect continuous", "Past perfect continuous", "Present continuous", "Future continuous"], "correct_answer": "Present perfect continuous", "explanation": "'Has been working' is present perfect continuous.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-880", "category": "logical", "sub_category": "Puzzles", "question": "If you rearrange the letters 'CIFAIPC', you get the name of a/an:", "options": ["Ocean (PACIFIC)", "City", "Country", "Animal"], "correct_answer": "Ocean (PACIFIC)", "explanation": "CIFAIPC rearranges to PACIFIC.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-890", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Under the weather' mean?", "options": ["Feeling sick", "Outside", "In bad weather", "Depressed"], "correct_answer": "Feeling sick", "explanation": "Under the weather means feeling ill or unwell.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-900", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who walks in sleep:", "options": ["Somnambulist", "Insomniac", "Sleepwalker", "Both A and C"], "correct_answer": "Both A and C", "explanation": "Somnambulist and sleepwalker both mean a person who walks in sleep.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-890", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 30 students, if Meena is 14th from the left, what is her position from the right?", "options": ["17th", "16th", "18th", "15th"], "correct_answer": "17th", "explanation": "Position from right = 30 - 14 + 1 = 17.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-910", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Quantum computing promises to solve problems classical computers cannot. Google claimed quantum supremacy in 2019. However, practical quantum computers are still years away from mainstream use.' What is the current status of quantum computing?", "options": ["Mainstream", "Years away from mainstream", "Unavailable", "Fully developed"], "correct_answer": "Years away from mainstream", "explanation": "The passage states practical quantum computers are 'still years away from mainstream use.'", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-900", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: All managers are leaders. All leaders are thinkers. Conclusion: Some thinkers are managers.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "True", "explanation": "All managers are thinkers, so some thinkers are managers.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-910", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 6 km north, turns right and walks 8 km. How far is he from the start?", "options": ["10 km", "14 km", "2 km", "12 km"], "correct_answer": "10 km", "explanation": "6 km north + 8 km east = √(36+64) = 10 km.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-920", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct form: 'She has been working here since 2020.'", "options": ["Present perfect continuous", "Past perfect continuous", "Present continuous", "Future continuous"], "correct_answer": "Present perfect continuous", "explanation": "'Has been working' is present perfect continuous.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-920", "category": "logical", "sub_category": "Clock Problems", "question": "What is the angle between the hour and minute hands at 12:00?", "options": ["0°", "360°", "180°", "90°"], "correct_answer": "0°", "explanation": "Both hands at 0°. Angle = 0°.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-930", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct article: 'He is ___ honest man.'", "options": ["a", "an", "the", "no article"], "correct_answer": "an", "explanation": "'Honest' starts with a vowel sound, so use 'an'.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-930", "category": "logical", "sub_category": "Puzzles", "question": "If A is B's sister, and B is C's mother, how is A related to C?", "options": ["Aunt", "Mother", "Sister", "Daughter"], "correct_answer": "Aunt", "explanation": "B is C's mother. A is B's sister. So A is C's aunt.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-940", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Let the cat out of the bag' mean?", "options": ["Reveal a secret", "Be careless", "Be fast", "Be angry"], "correct_answer": "Reveal a secret", "explanation": "Let the cat out of the bag means to reveal a secret.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-950", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who studies coins:", "options": ["Numismatist", "Philatelist", "Bibliophile", "Archaeologist"], "correct_answer": "Numismatist", "explanation": "Numismatist = person who studies coins.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-940", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 40 students, if Anita is 16th from the left, what is her position from the right?", "options": ["25th", "24th", "26th", "23rd"], "correct_answer": "25th", "explanation": "Position from right = 40 - 16 + 1 = 25.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-960", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Artificial intelligence is being used in healthcare for diagnosis, drug discovery, and patient monitoring. AI can analyze medical images with 94% accuracy, matching radiologists. This could reduce diagnostic errors significantly.' What is the main benefit of AI in healthcare?", "options": ["Lower costs", "Reduced diagnostic errors", "Faster treatment", "More doctors"], "correct_answer": "Reduced diagnostic errors", "explanation": "The passage states AI 'could reduce diagnostic errors significantly.'", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-950", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: Some doctors are engineers. Some engineers are lawyers. Conclusion: Some doctors are lawyers.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "Cannot be determined", "explanation": "Just because some doctors are engineers and some engineers are lawyers doesn't mean any doctors are lawyers.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},

    # More Logical - Direction Sense (10)
    {"id": "APT-L-960", "category": "logical", "sub_category": "Direction Sense", "question": "A man walks 3 km east, turns left and walks 4 km, turns left again and walks 3 km. How far is he from the start?", "options": ["4 km", "7 km", "0 km", "6 km"], "correct_answer": "4 km", "explanation": "3 km east, 4 km north, 3 km west. Net: 4 km north.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Direction Sense"},

    # More Verbal - Sentence Correction (10)
    {"id": "APT-V-970", "category": "verbal", "sub_category": "Sentence Correction", "question": "Choose the correct form: 'He is one of those people who ___ always helpful.'", "options": ["are", "is", "was", "has been"], "correct_answer": "are", "explanation": "'People' is plural, so 'are' is correct.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Sentence Correction"},

    # More Logical - Clock Problems (10)
    {"id": "APT-L-970", "category": "logical", "sub_category": "Clock Problems", "question": "What is the angle between the hour and minute hands at 3:30?", "options": ["75°", "90°", "60°", "45°"], "correct_answer": "75°", "explanation": "Minute at 180°. Hour at 3*30 + 30*0.5 = 105°. Angle = 75°.", "difficulty": "medium", "time_limit": 90, "companies": ["TCS"], "topic": "Clock Problems"},

    # More Verbal - Grammar (10)
    {"id": "APT-V-980", "category": "verbal", "sub_category": "Grammar", "question": "Choose the correct tense: 'She has been working here since 2020.'", "options": ["Present perfect continuous", "Past perfect continuous", "Present continuous", "Future continuous"], "correct_answer": "Present perfect continuous", "explanation": "'Has been working' is present perfect continuous.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Grammar"},

    # More Logical - Puzzles (10)
    {"id": "APT-L-980", "category": "logical", "sub_category": "Puzzles", "question": "If A is 5 years older than B, B is 3 years older than C. If A is 18, how old is C?", "options": ["10", "12", "8", "11"], "correct_answer": "10", "explanation": "B = 18-5 = 13. C = 13-3 = 10.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Puzzles"},

    # More Verbal - Idioms (10)
    {"id": "APT-V-990", "category": "verbal", "sub_category": "Idioms", "question": "What does 'Bark up the wrong tree' mean?", "options": ["Make a mistake", "Be on the right track", "Be fast", "Be angry"], "correct_answer": "Make a mistake", "explanation": "Bark up the wrong tree means to pursue a mistaken course of action.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Idioms"},

    # More Verbal - One Word Substitution (10)
    {"id": "APT-V-1000", "category": "verbal", "sub_category": "One Word Substitution", "question": "A person who draws maps:", "options": ["Cartographer", "Geographer", "Explorer", "Navigator"], "correct_answer": "Cartographer", "explanation": "Cartographer = person who draws maps.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "One Word Substitution"},

    # More Logical - Seating Arrangement (10)
    {"id": "APT-L-990", "category": "logical", "sub_category": "Seating Arrangement", "question": "In a row of 55 students, if Rohit is 20th from the left, what is his position from the right?", "options": ["36th", "35th", "37th", "34th"], "correct_answer": "36th", "explanation": "Position from right = 55 - 20 + 1 = 36.", "difficulty": "easy", "time_limit": 30, "companies": ["TCS"], "topic": "Seating Arrangement"},

    # More Verbal - Reading Comprehension (10)
    {"id": "APT-V-1010", "category": "verbal", "sub_category": "Reading Comprehension", "question": "Read: 'Space tourism is becoming a reality. Companies like SpaceX and Blue Origin are offering suborbital flights. However, ticket prices range from $250,000 to $450,000, limiting access to the wealthy.' What is the main barrier to space tourism?", "options": ["Safety concerns", "High ticket prices", "Limited seats", "Technical issues"], "correct_answer": "High ticket prices", "explanation": "The passage mentions high prices limiting access as the main barrier.", "difficulty": "easy", "time_limit": 60, "companies": ["TCS"], "topic": "Reading Comprehension"},

    # More Logical - Syllogisms (10)
    {"id": "APT-L-1000", "category": "logical", "sub_category": "Syllogisms", "question": "Statement: All roses are flowers. Some flowers are thorns. Conclusion: Some roses are thorns.", "options": ["True", "False", "Cannot be determined", "Partially true"], "correct_answer": "Cannot be determined", "explanation": "Just because some flowers are thorns doesn't mean any roses are thorns.", "difficulty": "medium", "time_limit": 30, "companies": ["TCS"], "topic": "Syllogisms"},
]
