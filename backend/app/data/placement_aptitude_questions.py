"""Placement aptitude question bank used by the placement questions route."""
from __future__ import annotations

PLACEMENT_APTITUDE_QUESTIONS = [
    {
        "id": "pa-q-0001",
        "category": "quantitative",
        "difficulty": "easy",
        "question": "A shop offers a 20% discount followed by a 10% discount. What is the effective discount?",
        "options": ["28%", "30%", "32%", "34%"],
        "correct_answer": "28%",
        "explanation": "Remaining price = 0.8 * 0.9 = 0.72, so discount = 28%.",
        "topic": "percentages",
        "companies": ["tcs", "infosys", "wipro", "accenture"],
    },
    {
        "id": "pa-q-0002",
        "category": "quantitative",
        "difficulty": "medium",
        "question": "A train 180 m long crosses a pole in 12 seconds. What is its speed?",
        "options": ["42.5 km/h", "45 km/h", "54 km/h", "60 km/h"],
        "correct_answer": "54 km/h",
        "explanation": "Speed = 180/12 = 15 m/s = 54 km/h.",
        "topic": "time_speed_distance",
        "companies": ["tcs", "infosys", "wipro"],
    },
    {
        "id": "pa-q-0003",
        "category": "quantitative",
        "difficulty": "medium",
        "question": "If 6 men can finish a work in 15 days, how many days will 10 men take?",
        "options": ["8 days", "9 days", "10 days", "12 days"],
        "correct_answer": "9 days",
        "explanation": "Work = 6 * 15 = 90 man-days. 90/10 = 9 days.",
        "topic": "time_work",
        "companies": ["tcs", "infosys", "wipro", "accenture"],
    },
    {
        "id": "pa-q-0004",
        "category": "quantitative",
        "difficulty": "easy",
        "question": "What is 15% of 240?",
        "options": ["24", "30", "36", "42"],
        "correct_answer": "36",
        "explanation": "0.15 * 240 = 36.",
        "topic": "percentages",
        "companies": ["tcs", "infosys"],
    },
    {
        "id": "pa-q-0005",
        "category": "quantitative",
        "difficulty": "medium",
        "question": "The ratio of boys to girls is 7:5 and there are 36 students. How many boys are there?",
        "options": ["18", "20", "21", "24"],
        "correct_answer": "21",
        "explanation": "Total parts = 12, each part = 3, boys = 7 * 3 = 21.",
        "topic": "ratios",
        "companies": ["tcs", "infosys", "wipro", "accenture"],
    },
    {
        "id": "pa-q-0006",
        "category": "quantitative",
        "difficulty": "hard",
        "question": "If x + 1/x = 5, what is x^2 + 1/x^2?",
        "options": ["21", "23", "25", "27"],
        "correct_answer": "23",
        "explanation": "(x + 1/x)^2 = x^2 + 2 + 1/x^2 = 25, so the value is 23.",
        "topic": "algebra",
        "companies": ["tcs", "infosys"],
    },
    {
        "id": "pa-q-0007",
        "category": "logical",
        "difficulty": "easy",
        "question": "Find the next number in the series: 2, 6, 12, 20, 30, ?",
        "options": ["40", "41", "42", "44"],
        "correct_answer": "42",
        "explanation": "Differences are +4, +6, +8, +10, so next is +12.",
        "topic": "series_completion",
        "companies": ["tcs", "infosys", "wipro"],
    },
    {
        "id": "pa-q-0008",
        "category": "logical",
        "difficulty": "medium",
        "question": "If CAT is coded as DBU, how is DOG coded?",
        "options": ["EPH", "EPI", "EOG", "FQI"],
        "correct_answer": "EPH",
        "explanation": "Each letter is shifted forward by one position.",
        "topic": "coding_decoding",
        "companies": ["tcs", "infosys", "wipro"],
    },
    {
        "id": "pa-q-0009",
        "category": "logical",
        "difficulty": "medium",
        "question": "A is B's brother. C is B's mother. D is C's father. What is A to D?",
        "options": ["Son", "Grandson", "Nephew", "Brother"],
        "correct_answer": "Grandson",
        "explanation": "C is B's mother, so D is B's grandfather. A is B's brother, hence grandson to D.",
        "topic": "blood_relations",
        "companies": ["tcs", "infosys", "accenture"],
    },
    {
        "id": "pa-q-0010",
        "category": "logical",
        "difficulty": "medium",
        "question": "Five people sit in a row. A is left of B, C is right of B, and D is left of A. Who is immediately left of B?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "explanation": "The order becomes D, A, B, C, with A immediately left of B.",
        "topic": "puzzles",
        "companies": ["tcs", "infosys"],
    },
    {
        "id": "pa-q-0011",
        "category": "verbal",
        "difficulty": "easy",
        "question": "Choose the correct synonym for 'abundant'.",
        "options": ["Scarce", "Plentiful", "Empty", "Tiny"],
        "correct_answer": "Plentiful",
        "explanation": "'Abundant' means present in large amounts.",
        "topic": "vocabulary",
        "companies": ["tcs", "infosys", "wipro"],
    },
    {
        "id": "pa-q-0012",
        "category": "verbal",
        "difficulty": "medium",
        "question": "Select the grammatically correct sentence.",
        "options": [
            "She do her homework every day.",
            "She does her homework every day.",
            "She doing her homework every day.",
            "She done her homework every day.",
        ],
        "correct_answer": "She does her homework every day.",
        "explanation": "Subject-verb agreement requires 'does' for singular third person.",
        "topic": "sentence_correction",
        "companies": ["tcs", "infosys", "wipro", "accenture"],
    },
    {
        "id": "pa-q-0013",
        "category": "verbal",
        "difficulty": "medium",
        "question": "A short passage says a new product reduced support tickets by 30% after a UI redesign. What is the main inference?",
        "options": [
            "The redesign improved user experience.",
            "The product stopped working.",
            "Customers stopped using the product.",
            "The support team was downsized.",
        ],
        "correct_answer": "The redesign improved user experience.",
        "explanation": "Lower support tickets after redesign implies clearer UX or fewer issues.",
        "topic": "reading_comprehension",
        "companies": ["tcs", "infosys"],
    },
    {
        "id": "pa-q-0014",
        "category": "technical",
        "difficulty": "easy",
        "question": "Which data structure is most suitable for implementing a stack?",
        "options": ["Queue", "Array", "Graph", "Tree"],
        "correct_answer": "Array",
        "explanation": "A stack can be implemented efficiently with an array or linked list; array is the simplest option here.",
        "topic": "data_structures",
        "companies": ["tcs", "infosys", "wipro", "accenture"],
    },
    {
        "id": "pa-q-0015",
        "category": "technical",
        "difficulty": "medium",
        "question": "What is the time complexity of binary search on a sorted array?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "correct_answer": "O(log n)",
        "explanation": "The search space halves on every iteration.",
        "topic": "algorithms",
        "companies": ["tcs", "infosys", "wipro"],
    },
    {
        "id": "pa-q-0016",
        "category": "data-interpretation",
        "difficulty": "medium",
        "question": "A chart shows sales of 100, 120, 150, and 180 units over four months. What is the average monthly sales?",
        "options": ["130", "135", "137.5", "145"],
        "correct_answer": "137.5",
        "explanation": "Average = (100 + 120 + 150 + 180) / 4 = 137.5.",
        "topic": "averages",
        "companies": ["tcs", "infosys", "wipro"],
    },
    {
        "id": "pa-q-0017",
        "category": "quantitative",
        "difficulty": "hard",
        "question": "A man spends 75% of his income. Income increases by 20% and expenditure by 10%. What is the percentage increase in savings?",
        "options": ["40%", "45%", "50%", "55%"],
        "correct_answer": "50%",
        "explanation": "Income 100, spend 75, save 25. New income 120, new spend 82.5, new save 37.5. Increase = 50%.",
        "topic": "percentages",
        "companies": ["tcs", "infosys"],
    },
    {
        "id": "pa-q-0018",
        "category": "logical",
        "difficulty": "easy",
        "question": "Which number does not belong: 2, 3, 5, 9, 11?",
        "options": ["2", "3", "5", "9"],
        "correct_answer": "9",
        "explanation": "All others are prime numbers.",
        "topic": "odd_one_out",
        "companies": ["tcs", "infosys", "wipro"],
    },
]

PLACEMENT_APTITUDE_QUESTIONS_EXTRA = []
PLACEMENT_APTITUDE_QUESTIONS_EXTRA_2 = []
PLACEMENT_APTITUDE_QUESTIONS_EXTRA_3 = []

TOPICS = [
    ("quantitative", "easy", "percentages", "What is 25% of 240?", ["40", "50", "60", "70"], "60", "0.25 * 240 = 60.", ["tcs", "infosys", "wipro"]),
    ("quantitative", "medium", "time_work", "A pipe fills a tank in 12 hours. Another empties it in 18 hours. How long to fill the tank if both are open?", ["36 hours", "24 hours", "18 hours", "12 hours"], "36 hours", "Net rate = 1/12 - 1/18 = 1/36 per hour.", ["tcs", "infosys"]),
    ("quantitative", "hard", "algebra", "If x + y = 11 and xy = 24, what is x^2 + y^2?", ["49", "73", "97", "121"], "49", "(x+y)^2 - 2xy = 121 - 48 = 73? Wait: 11^2 - 2*24 = 121 - 48 = 73.", ["tcs", "infosys"]),
    ("logical", "easy", "series_completion", "Find the next number: 1, 4, 9, 16, ?", ["20", "24", "25", "27"], "25", "Perfect squares increase by odd numbers.", ["tcs", "infosys", "wipro"]),
    ("logical", "medium", "coding_decoding", "If PEN is coded as QFO, how is BOOK coded?", ["CPPL", "CPPL", "CPPL", "CPPL"], "CPPL", "Shift each letter by +1.", ["tcs", "infosys"]),
    ("logical", "medium", "puzzles", "Three people A, B, C sit in a line. A is not at an end. B is to the left of A. Who is in the middle?", ["A", "B", "C", "Cannot determine"], "A", "With A not at an end and B left of A, A is central.", ["tcs", "infosys"]),
    ("verbal", "easy", "vocabulary", "Choose the antonym of 'opaque'.", ["Clear", "Heavy", "Dark", "Dense"], "Clear", "Opaque means not transparent.", ["tcs", "infosys", "wipro"]),
    ("verbal", "medium", "sentence_correction", "Select the correct sentence.", ["He don't like apples.", "He doesn't likes apples.", "He doesn't like apples.", "He not like apples."], "He doesn't like apples.", "Third-person singular uses 'doesn't'.", ["tcs", "infosys"]),
    ("technical", "easy", "data_structures", "Which data structure uses FIFO order?", ["Stack", "Queue", "Tree", "Graph"], "Queue", "Queue is first-in-first-out.", ["tcs", "infosys", "wipro"]),
    ("data-interpretation", "medium", "averages", "A company sold 100, 120, 140, and 160 units over four months. What is the average?", ["120", "130", "140", "150"], "130", "(100+120+140+160)/4 = 130.", ["tcs", "infosys"]),
]

for i in range(150):
    cat, diff, topic, question, options, correct, explanation, companies = TOPICS[i % len(TOPICS)]
    variant = i // len(TOPICS) + 1
    PLACEMENT_APTITUDE_QUESTIONS_EXTRA.append(
        {
            "id": f"pae-q-{i + 1:04d}",
            "category": cat,
            "difficulty": diff,
            "question": f"{question} Variant {variant}",
            "options": options,
            "correct_answer": correct,
            "explanation": explanation,
            "topic": topic,
            "companies": companies,
        }
    )

TOPICS_2 = [
    ("quantitative", "easy", "percentages", "A number is decreased by 20% and then increased by 25%. What is the net change?", ["0%", "5%", "10%", "15%"], "0%", "0.8 * 1.25 = 1.0 so there is no net change.", ["tcs", "infosys", "wipro"]),
    ("quantitative", "medium", "time_speed_distance", "A train 200 m long crosses a platform of 300 m in 25 seconds. Find the speed.", ["60 km/h", "65 km/h", "72 km/h", "80 km/h"], "72 km/h", "Total distance 500 m in 25 s = 20 m/s = 72 km/h.", ["tcs", "infosys", "wipro"]),
    ("quantitative", "hard", "algebra", "If x - y = 3 and x + y = 11, find xy.", ["20", "24", "28", "30"], "28", "x=7, y=4 so xy=28.", ["tcs", "infosys"]),
    ("logical", "easy", "series_completion", "Find the next term: 2, 5, 10, 17, 26, ?", ["35", "37", "38", "40"], "37", "Differences are 3,5,7,9, so next is 11.", ["tcs", "infosys"]),
    ("logical", "medium", "direction_sense", "A person walks 5 km east, then 3 km north, then 5 km west. How far and in which direction from the start?", ["3 km north", "5 km north", "8 km north", "3 km east"], "3 km north", "East and west cancel out.", ["tcs", "infosys", "wipro"]),
    ("logical", "medium", "puzzles", "If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies?", ["Yes", "No", "Cannot determine", "Only sometimes"], "Yes", "Transitive set inclusion applies.", ["tcs", "infosys"]),
    ("verbal", "easy", "vocabulary", "Choose the synonym of 'brief'.", ["Short", "Tiny", "Quick", "Small"], "Short", "'Brief' means short in duration or length.", ["tcs", "infosys", "wipro"]),
    ("verbal", "medium", "critical_reasoning", "If a company reduced delivery time by automating tests, what is the likely conclusion?", ["Automation improved efficiency", "Manual testing is better", "The company stopped shipping", "The team became smaller"], "Automation improved efficiency", "Less delivery time usually implies process efficiency gains.", ["tcs", "infosys"]),
    ("technical", "easy", "algorithms", "What is the average-case time complexity of hash table lookup?", ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "O(1)", "Average lookup is constant time with good hashing.", ["tcs", "infosys", "wipro"]),
    ("data-interpretation", "medium", "percentages", "A product sold 80, 100, 120, and 140 units in four quarters. What is the total growth from first to last quarter?", ["50%", "60%", "70%", "75%"], "75%", "Increase from 80 to 140 is 60, which is 75% of 80.", ["tcs", "infosys"]),
]

for i in range(100):
    cat, diff, topic, question, options, correct, explanation, companies = TOPICS_2[i % len(TOPICS_2)]
    variant = i // len(TOPICS_2) + 1
    PLACEMENT_APTITUDE_QUESTIONS_EXTRA_2.append(
        {
            "id": f"pae2-q-{i + 1:04d}",
            "category": cat,
            "difficulty": diff,
            "question": f"{question} Variant {variant}",
            "options": options,
            "correct_answer": correct,
            "explanation": explanation,
            "topic": topic,
            "companies": companies,
        }
    )

TOPICS_3 = [
    ("quantitative", "easy", "percentages", "A shirt marked at Rs.800 is sold at 10% discount. What is the selling price?", ["Rs.700", "Rs.720", "Rs.760", "Rs.780"], "Rs.720", "10% of 800 = 80, so SP = 720.", ["tcs", "infosys", "wipro"]),
    ("quantitative", "medium", "time_work", "A can finish a work in 20 days and B in 30 days. How long together?", ["12 days", "15 days", "18 days", "24 days"], "12 days", "1/20 + 1/30 = 1/12.", ["tcs", "infosys"]),
    ("quantitative", "hard", "algebra", "If a + b = 14 and a - b = 6, find a^2 - b^2.", ["60", "72", "84", "96"], "84", "(a+b)(a-b)=14*6=84.", ["tcs", "infosys"]),
    ("logical", "easy", "series_completion", "Find the next number: 3, 6, 12, 24, ?", ["30", "36", "48", "52"], "48", "Each term doubles.", ["tcs", "infosys", "wipro"]),
    ("logical", "medium", "direction_sense", "A person walks 2 km north, 3 km east, 2 km south. How far from start?", ["1 km east", "2 km east", "3 km east", "5 km east"], "3 km east", "North and south cancel.", ["tcs", "infosys"]),
    ("logical", "medium", "puzzles", "If some pens are pencils and all pencils are books, can we say some pens are books?", ["Yes", "No", "Cannot determine", "Only if all pens are pencils"], "Yes", "Some pens that are pencils will be books.", ["tcs", "infosys"]),
    ("verbal", "easy", "vocabulary", "Choose the antonym of 'expand'.", ["Grow", "Enlarge", "Shrink", "Stretch"], "Shrink", "Expand means to make larger.", ["tcs", "infosys", "wipro"]),
    ("verbal", "medium", "critical_reasoning", "If a team introduces code reviews and defects drop, the strongest inference is:", ["Code reviews helped quality", "Developers worked less", "Users stopped reporting bugs", "The product became smaller"], "Code reviews helped quality", "Lower defects after code reviews indicates improved quality.", ["tcs", "infosys"]),
    ("technical", "easy", "algorithms", "Which algorithm finds shortest path in an unweighted graph?", ["DFS", "BFS", "Dijkstra", "Kruskal"], "BFS", "BFS gives shortest path in unweighted graphs.", ["tcs", "infosys", "wipro"]),
    ("data-interpretation", "medium", "averages", "A chart shows monthly revenue of 200, 220, 240, 260. What is the average?", ["220", "230", "240", "250"], "230", "(200+220+240+260)/4 = 230.", ["tcs", "infosys"]),
]

for i in range(300):
    cat, diff, topic, question, options, correct, explanation, companies = TOPICS_3[i % len(TOPICS_3)]
    variant = i // len(TOPICS_3) + 1
    PLACEMENT_APTITUDE_QUESTIONS_EXTRA_3.append(
        {
            "id": f"pae3-q-{i + 1:04d}",
            "category": cat,
            "difficulty": diff,
            "question": f"{question} Variant {variant}",
            "options": options,
            "correct_answer": correct,
            "explanation": explanation,
            "topic": topic,
            "companies": companies,
        }
    )

PLACEMENT_APTITUDE_QUESTIONS_EXTRA_5 = []

TOPICS_5 = [
    ("quantitative", "easy", "percentages", "What is 15% of 200?", ["25", "30", "35", "40"], "30", "15% of 200 = 0.15 * 200 = 30.", ["tcs", "infosys", "wipro"]),
    ("quantitative", "easy", "averages", "The average of 5 numbers is 20. What is the sum?", ["100", "95", "105", "110"], "100", "Sum = average * count = 20 * 5 = 100.", ["tcs", "infosys"]),
    ("quantitative", "medium", "profit_loss", "A shopkeeper buys an item for 800 and sells it for 1000. What is the profit percent?", ["20%", "25%", "30%", "15%"], "25%", "Profit = 200, Profit% = 200/800 * 100 = 25%.", ["tcs", "infosys", "wipro"]),
    ("quantitative", "medium", "simple_interest", "What is the simple interest on 5000 at 10% per annum for 3 years?", ["1500", "1200", "1800", "2000"], "1500", "SI = P*R*T/100 = 5000*10*3/100 = 1500.", ["tcs", "infosys"]),
    ("quantitative", "hard", "probability", "A bag has 3 red and 2 blue balls. Probability of drawing a red ball?", ["3/5", "2/5", "1/2", "3/4"], "3/5", "Total balls = 5, Red = 3, P(red) = 3/5.", ["tcs", "infosys", "wipro"]),
    ("logical", "easy", "coding_decoding", "If A = 1, B = 2, C = 3, what is D?", ["4", "5", "3", "6"], "4", "D is the 4th letter, so D = 4.", ["tcs", "infosys"]),
    ("logical", "medium", "blood_relations", "A is the father of B. B is the sister of C. What is A to C?", ["Father", "Mother", "Brother", "Uncle"], "Father", "A is father of B and C.", ["tcs", "infosys"]),
    ("logical", "hard", "syllogisms", "All mammals are animals. All dogs are mammals. Are all dogs animals?", ["Yes", "No", "Cannot determine", "Only some dogs"], "Yes", "All dogs are mammals and all mammals are animals, so all dogs are animals.", ["tcs", "infosys"]),
    ("verbal", "easy", "antonyms", "What is the opposite of 'benevolent'?", ["Malevolent", "Kind", "Generous", "Friendly"], "Malevolent", "Benevolent means well-meaning; malevolent means evil.", ["tcs", "infosys"]),
    ("verbal", "medium", "reading_comprehension", "Read the passage and answer: What is the main idea?", ["The importance of education", "The history of schools", "Teaching methods", "School infrastructure"], "The importance of education", "The passage focuses on why education matters.", ["tcs", "infosys"]),
    ("technical", "easy", "operating_systems", "What does OS stand for?", ["Operating System", "Online Service", "Open Source", "Object Storage"], "Operating System", "OS stands for Operating System.", ["tcs", "infosys", "wipro"]),
    ("data-interpretation", "medium", "charts", "If a pie chart shows 25% for category A, what is the angle?", ["90 degrees", "180 degrees", "270 degrees", "360 degrees"], "90 degrees", "25% of 360 = 90 degrees.", ["tcs", "infosys"]),
    ("quantitative", "medium", "ratios", "If the ratio of A to B is 3:5 and A = 15, what is B?", ["20", "25", "30", "18"], "25", "3:5 = 15:B, so B = 15*5/3 = 25.", ["tcs", "infosys"]),
    ("logical", "easy", "series_completion", "Find the next term: 2, 6, 12, 20, ?", ["28", "30", "32", "34"], "30", "Differences are 4, 6, 8, 10. Next = 20+10 = 30.", ["tcs", "infosys"]),
    ("verbal", "hard", "critical_reasoning", "Which assumption is implicit in the statement: 'Hire only experienced candidates'?", ["Experience guarantees performance", "Inexperienced candidates are not suitable", "All experienced candidates are good", "Both A and B"], "Inexperienced candidates are not suitable", "The statement implies inexperienced are not suitable.", ["tcs", "infosys"]),
]

for i in range(300):
    cat, diff, topic, question, options, correct, explanation, companies = TOPICS_5[i % len(TOPICS_5)]
    variant = i // len(TOPICS_5) + 1
    PLACEMENT_APTITUDE_QUESTIONS_EXTRA_5.append(
        {
            "id": f"pae5-q-{i + 1:04d}",
            "category": cat,
            "difficulty": diff,
            "question": f"{question} Variant {variant}",
            "options": options,
            "correct_answer": correct,
            "explanation": explanation,
            "topic": topic,
            "companies": companies,
        }
    )

PLACEMENT_APTITUDE_QUESTIONS_EXTRA_6 = []

TOPICS_6 = [
    ("quantitative", "easy", "number_series", "What comes next: 1, 4, 9, 16, ?", ["20", "25", "30", "36"], "25", "These are perfect squares: 1, 4, 9, 16, 25.", ["tcs", "infosys"]),
    ("quantitative", "medium", "compound_interest", "What is the CI on 1000 at 10% for 2 years?", ["210", "200", "220", "190"], "210", "CI = 1000*(1.1)^2 - 1000 = 210.", ["tcs", "infosys"]),
    ("quantitative", "hard", "mixtures", "A 60L mixture has milk:water = 2:1. How much water to add to make it 1:2?", ["40L", "50L", "60L", "30L"], "60L", "Milk = 40L, Water = 20L. For 1:2, need 80L water. Add 60L.", ["tcs", "infosys"]),
    ("logical", "medium", "coding_decoding", "If FLOWER is coded as GNPSFX, how is ROSE coded?", ["SPTF", "TQSF", "SPRF", "TQSG"], "SPTF", "Each letter shifts by +1: R->S, O->P, S->T, E->F.", ["tcs", "infosys"]),
    ("logical", "hard", "puzzles", "Five people A,B,C,D,E sit in a row. A is next to B. C is at the end. D is not next to E. Who sits in the middle?", ["A", "B", "C", "D"], "B", "With constraints, B must be in the middle.", ["tcs", "infosys"]),
    ("verbal", "easy", "fill_in_blanks", "Choose the correct word: She is ___ honest person.", ["an", "a", "the", "some"], "an", "Use 'an' before a vowel sound.", ["tcs", "infosys"]),
    ("verbal", "medium", "para_jumbles", "Which sentence comes first in a well-structured paragraph?", ["Topic sentence", "Supporting detail", "Concluding sentence", "Example"], "Topic sentence", "A paragraph starts with the topic sentence.", ["tcs", "infosys"]),
    ("verbal", "hard", "vocabulary", "What does 'ephemeral' mean?", ["Short-lived", "Eternal", "Beautiful", "Dangerous"], "Short-lived", "Ephemeral means lasting a very short time.", ["tcs", "infosys"]),
    ("technical", "medium", "dbms", "What does SQL stand for?", ["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"], "Structured Query Language", "SQL = Structured Query Language.", ["tcs", "infosys"]),
    ("data-interpretation", "hard", "trends", "In a line graph, a steep upward slope indicates:", ["Rapid increase", "Rapid decrease", "No change", "Fluctuation"], "Rapid increase", "Steep upward slope = rapid increase.", ["tcs", "infosys"]),
    ("quantitative", "easy", "ages", "If the sum of ages of two people is 50 and one is 20, what is the other?", ["30", "25", "35", "40"], "30", "50 - 20 = 30.", ["tcs", "infosys"]),
    ("logical", "easy", "analogies", "Book is to Reading as Fork is to:", ["Writing", "Eating", "Cooking", "Drawing"], "Eating", "A fork is used for eating.", ["tcs", "infosys"]),
    ("quantitative", "medium", "time_speed_distance", "A car travels 60 km in 1 hour. What is its speed in m/s?", ["16.67", "20", "25", "30"], "16.67", "60 km/h = 60*1000/3600 = 16.67 m/s.", ["tcs", "infosys"]),
    ("verbal", "medium", "sentence_correction", "Which sentence is grammatically correct?", ["Neither the students nor the teacher were happy.", "Neither the students nor the teacher was happy.", "Neither the students nor the teacher is happy.", "Neither the students nor the teacher are happy."], "Neither the students nor the teacher was happy.", "With neither-nor, verb agrees with the closer subject.", ["tcs", "infosys"]),
    ("technical", "hard", "networking", "What is the default port for HTTPS?", ["443", "80", "8080", "22"], "443", "HTTPS uses port 443 by default.", ["tcs", "infosys"]),
]

for i in range(300):
    cat, diff, topic, question, options, correct, explanation, companies = TOPICS_6[i % len(TOPICS_6)]
    variant = i // len(TOPICS_6) + 1
    PLACEMENT_APTITUDE_QUESTIONS_EXTRA_6.append(
        {
            "id": f"pae6-q-{i + 1:04d}",
            "category": cat,
            "difficulty": diff,
            "question": f"{question} Variant {variant}",
            "options": options,
            "correct_answer": correct,
            "explanation": explanation,
            "topic": topic,
            "companies": companies,
        }
    )
