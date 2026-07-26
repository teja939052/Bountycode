"""
Comprehensive Indian Company Placement Data.
Real patterns from TCS NQT, Infosys InfyTQ, Wipro NLTH, Cognizant, HCL, Accenture, Capgemini, Tech Mahindra,
and 45+ additional companies covering IT Services, Product, Global MNCs, PSU/Govt, Startups, Banking, and Conglomerates.
"""

INDIAN_COMPANIES = {}

INDIAN_COMPANIES['tcs'] = {'name': 'TCS', 'full_name': 'Tata Consultancy Services', 'icon': '🏢', 'color': '#1E3A5F', 'package': '3.36 LPA (Ninja) / 7 LPA (Digital)', 'eligibility': '60% aggregate, no active backlogs', 'exam_pattern': 'TCS NQT (National Qualifier Test)', 'interview_rounds': ['NQT Online Test (90 min)', 'Technical Interview (1)', 'HR Interview (1)'], 'focus_areas': ['Aptitude', 'Programming Logic', 'English', 'Technical Basics'], 'nqt_pattern': {'total_time_minutes': 90, 'sections': [{'name': 'Aptitude', 'questions': 26, 'time_minutes': 25, 'types': ['Quantitative', 'Logical Reasoning', 'Data Interpretation'], 'difficulty': 'easy-medium', 'topics': ['Time & Work', 'Profit & Loss', 'Probability', 'Permutations', 'Number Series', 'Blood Relations', 'Coding-Decoding', 'Syllogisms', 'Pie Charts', 'Bar Graphs']}, {'name': 'Programming Logic', 'questions': 10, 'time_minutes': 15, 'types': ['MCQ on Programming', 'Basic Coding'], 'difficulty': 'easy', 'topics': ['Variables', 'Loops', 'Functions', 'Arrays', 'Strings', 'OOP Basics', 'Output Prediction', 'Error Finding']}, {'name': 'Coding', 'questions': 2, 'time_minutes': 45, 'types': ['Problem Solving'], 'difficulty': 'easy-medium', 'topics': ['Arrays', 'Strings', 'Pattern Matching', 'Basic Math', 'GCD/LCM', 'Prime Numbers', 'Palindrome', 'Anagram']}, {'name': 'English', 'questions': 24, 'time_minutes': 15, 'types': ['Grammar', 'Vocabulary', 'Reading Comprehension'], 'difficulty': 'easy', 'topics': ['Articles', 'Prepositions', 'Tenses', 'Subject-Verb Agreement', 'Synonyms', 'Antonyms', 'Sentence Correction']}]}, 'coding_patterns': ['Find second largest element in array', 'Count vowels and consonants in string', 'Check if number is prime', 'Reverse a number without converting to string', 'Find GCD of two numbers', 'Print Fibonacci series up to N', 'Check if string is palindrome', 'Find factorials using recursion', 'Matrix addition', 'Sort array without using built-in sort'], 'hr_questions': ['Tell me about yourself', 'Why TCS?', 'Where do you see yourself in 5 years?', 'Are you willing to relocate?', 'Tell me about a time you worked in a team', 'What are your strengths and weaknesses?', 'Why should we hire you?', 'Do you have any questions for us?', 'How do you handle pressure?', 'What motivates you?'], 'tips': ['Focus on speed — TCS NQT is time-pressed', 'Practice basic programming patterns, not advanced DSA', 'TCS values accuracy over complexity', "English section is easy but don't skip preparation", 'Ninja role is easier to crack than Digital', 'Know basic DBMS and OS concepts for technical round']}

INDIAN_COMPANIES['infosys'] = {'name': 'Infosys', 'full_name': 'Infosys Limited', 'icon': '🔷', 'color': '#007CC3', 'package': '3.6 LPA (InfyTQ) / 6.25 LPA (Specialist)', 'eligibility': '65% aggregate, CS/IT branches preferred', 'exam_pattern': 'InfyTQ Certification + Halo Round', 'interview_rounds': ['InfyTQ Online Test (3 hrs)', 'Technical Interview (2 rounds)', 'HR Interview (1)'], 'focus_areas': ['Programming', 'Database', 'Aptitude', 'Java/Python'], 'infytq_pattern': {'total_time_minutes': 180, 'sections': [{'name': 'Aptitude & Logic', 'questions': 30, 'time_minutes': 30, 'types': ['Quantitative', 'Logical', 'Data Interpretation'], 'difficulty': 'easy-medium', 'topics': ['Percentages', 'Mixtures', 'Clocks', 'Calendars', 'Series', 'Puzzles', 'Seating Arrangement', 'Venn Diagrams']}, {'name': 'Programming (MCQ)', 'questions': 20, 'time_minutes': 20, 'types': ['Programming Concepts', 'Output Prediction'], 'difficulty': 'easy-medium', 'topics': ['Java/Python Basics', 'OOP', 'Exception Handling', 'Collections', 'File I/O', 'Recursion', 'Time Complexity']}, {'name': 'Coding', 'questions': 3, 'time_minutes': 90, 'types': ['Problem Solving'], 'difficulty': 'medium', 'topics': ['Arrays', 'Strings', 'Linked Lists', 'Trees', 'Dynamic Programming', 'HashMaps', 'Stacks & Queues']}, {'name': 'SQL', 'questions': 5, 'time_minutes': 20, 'types': ['Query Writing', 'Normalization'], 'difficulty': 'medium', 'topics': ['Joins', 'Subqueries', 'Group By', 'Having', 'Normalization', 'Indexing', 'Triggers']}]}, 'coding_patterns': ['Find the most frequent element in array', 'Implement a simple HashMap', 'Check if two strings are anagrams', 'Find longest substring without repeating characters', 'Binary tree level order traversal', 'Merge two sorted arrays', 'Find the intersection of two arrays', 'Implement stack using queue', 'Detect cycle in linked list', 'Find path sum in binary tree'], 'hr_questions': ['Tell me about yourself', 'Why Infosys?', 'What do you know about Infosys founders?', 'Describe a challenging project you worked on', 'How do you handle conflicts in a team?', 'Where do you see yourself in 5 years?', 'What is your biggest achievement?', 'How do you learn new technologies?', 'Are you comfortable with night shifts?', 'What are your hobbies?'], 'tips': ['InfyTQ is harder than NQT — practice DSA seriously', 'Know Java or Python really well (pick one)', 'SQL section is scoring — practice joins and subqueries', 'Infosys values problem-solving approach over final answer', 'Technical interview goes deep into your project', 'Know basic system design concepts for Specialist role']}

INDIAN_COMPANIES['wipro'] = {'name': 'Wipro', 'full_name': 'Wipro Limited', 'icon': '💡', 'color': '#FF6600', 'package': '3.5 LPA (WILP) / 6 LPA (Turbo)', 'eligibility': '60% aggregate, 10th and 12th cutoffs apply', 'exam_pattern': 'Wipro NLTH (National Level Talent Hunt)', 'interview_rounds': ['NLTH Online Test (96 min)', 'Technical Interview (2 rounds)', 'HR Interview (1)'], 'focus_areas': ['Aptitude', 'Coding', 'Communication', 'Technical'], 'nlth_pattern': {'total_time_minutes': 96, 'sections': [{'name': 'Aptitude', 'questions': 20, 'time_minutes': 20, 'types': ['Quantitative', 'Logical'], 'difficulty': 'easy-medium', 'topics': ['Time & Distance', 'Probability', 'Permutation', 'Ratio & Proportion', 'Blood Relations', 'Direction Sense', 'Odd One Out', 'Number Series']}, {'name': 'Coding', 'questions': 2, 'time_minutes': 60, 'types': ['Problem Solving'], 'difficulty': 'medium', 'topics': ['Arrays', 'Strings', 'Linked Lists', 'Recursion', 'Dynamic Programming Basics', 'Pattern Printing', 'Matrix Operations']}, {'name': 'English', 'questions': 20, 'time_minutes': 16, 'types': ['Grammar', 'Vocabulary', 'Sentence Completion'], 'difficulty': 'easy', 'topics': ['Active/Passive Voice', 'Direct/Indirect Speech', 'Error Spotting', 'Fill in the Blanks', 'Word Analogy', 'One Word Substitution']}]}, 'coding_patterns': ["Find the largest subarray sum (Kadane's Algorithm)", 'Implement string compression', 'Find common elements in three sorted arrays', 'Check if a number is power of 2', 'Rotate array by K positions', 'Find the missing number in 1 to N', 'Implement binary search', 'Count set bits in a number', 'Check for balanced parentheses', 'Find the duplicate number in array'], 'hr_questions': ['Tell me about yourself', 'Why Wipro?', "What do you know about Wipro's CEO?", 'Describe your final year project', 'How do you manage deadlines?', 'What are your career goals?', 'Tell me about a time you failed', 'How do you handle stress?', 'Are you willing to work in any location?', 'What makes you unique?'], 'tips': ['NLTH has strict time limits — practice speed', 'Wipro focuses on communication skills heavily', 'Know basics of at least one programming language deeply', 'Turbo role requires stronger coding skills', 'Technical interview focuses on DBMS and OS', 'Wipro values attitude and willingness to learn']}

INDIAN_COMPANIES['cognizant'] = {'name': 'Cognizant', 'full_name': 'Cognizant Technology Solutions', 'icon': '🟦', 'color': '#0033A0', 'package': '4 LPA (GenC) / 6.75 LPA (GenC Next)', 'eligibility': '60% aggregate, eligible branches', 'exam_pattern': 'Cognizant GenC Assessment', 'interview_rounds': ['Online Assessment (90 min)', 'Technical Interview (1-2 rounds)', 'HR Interview (1)'], 'focus_areas': ['Aptitude', 'Programming', 'English', 'Domain Knowledge'], 'genc_pattern': {'total_time_minutes': 90, 'sections': [{'name': 'Aptitude', 'questions': 25, 'time_minutes': 25, 'types': ['Numerical', 'Logical', 'Verbal'], 'difficulty': 'easy-medium', 'topics': ['Profit & Loss', 'Simple/Compound Interest', 'Time & Work', 'Pipes & Cisterns', 'Coding-Decoding', 'Number Analogies', 'Odd One Out', 'Word Relationships']}, {'name': 'Programming', 'questions': 2, 'time_minutes': 45, 'types': ['Problem Solving'], 'difficulty': 'easy-medium', 'topics': ['Arrays', 'Strings', 'Math', 'Basic Algorithms', 'Sorting', 'Searching', 'Pattern Recognition']}, {'name': 'Essay Writing', 'questions': 1, 'time_minutes': 20, 'types': ['Written Communication'], 'difficulty': 'easy', 'topics': ['Technology Topics', 'Current Affairs', 'Opinion Essays']}]}, 'coding_patterns': ['Find the maximum product subarray', 'Count pairs with given sum', 'Check if string is a valid shuffle of two strings', 'Find the longest palindromic substring', 'Implement atoi() function', 'Find all Pythagorean triplets', 'Rotate matrix by 90 degrees', 'Find the smallest positive missing number', 'Implement strStr() function', 'Find equilibrium index of array'], 'hr_questions': ['Tell me about yourself', 'Why Cognizant?', 'What do you know about digital transformation?', 'Describe a situation where you showed leadership', 'How do you prioritize tasks?', 'What are your short-term and long-term goals?', 'Tell me about your strengths', 'How do you handle criticism?', 'Are you flexible with timings?', 'Do you prefer working alone or in teams?'], 'tips': ['GenC is easier to crack than GenC Next', 'Essay writing is scoring — practice writing essays', 'Cognizant values communication skills highly', 'Know basic OOP concepts and SQL', 'GenC Next requires strong coding (LeetCode Easy-Medium)', 'Be prepared for cross-platform questions']}

INDIAN_COMPANIES['hcl'] = {'name': 'HCL Tech', 'full_name': 'HCL Technologies', 'icon': '🔴', 'color': '#E42527', 'package': '3.5 LPA (HCL TSS) / 5.5 LPA (Regular)', 'eligibility': '60% aggregate, no standing arrears', 'exam_pattern': 'HCL Tech Bee / HCL SAT', 'interview_rounds': ['HCL SAT Online Test (90 min)', 'Technical Interview (1-2 rounds)', 'HR Interview (1)'], 'focus_areas': ['Aptitude', 'Logical', 'Programming', 'English'], 'hcl_pattern': {'total_time_minutes': 90, 'sections': [{'name': 'Quantitative Aptitude', 'questions': 20, 'time_minutes': 20, 'types': ['Numerical', 'Data Interpretation'], 'difficulty': 'easy', 'topics': ['Simplification', 'Percentage', 'Average', 'Ratio', 'Simple Interest', 'Compound Interest', 'Partnership', 'Bar Graphs']}, {'name': 'Logical Reasoning', 'questions': 20, 'time_minutes': 20, 'types': ['Puzzles', 'Patterns'], 'difficulty': 'easy-medium', 'topics': ['Syllogisms', 'Statements & Assumptions', 'Blood Relations', 'Seating Arrangement', 'Patterns', 'Coding-Decoding', 'Venn Diagrams']}, {'name': 'Programming', 'questions': 2, 'time_minutes': 40, 'types': ['Problem Solving'], 'difficulty': 'easy-medium', 'topics': ['Arrays', 'Strings', 'Math', 'Loops', 'Conditions', 'Basic Data Structures']}, {'name': 'English', 'questions': 20, 'time_minutes': 10, 'types': ['Grammar', 'Comprehension'], 'difficulty': 'easy', 'topics': ['Reading Comprehension', 'Error Detection', 'Sentence Formation', 'Synonyms', 'Antonyms']}]}, 'coding_patterns': ['Find the element that appears once in sorted array', 'Check if a number is divisible by all its digits', 'Find the minimum element in a sorted rotated array', 'Implement substring search', 'Find the maximum length of subarray with sum K', 'Check if string has all unique characters', 'Find the sum of digits until single digit', 'Print all divisors of a number', 'Check if two rectangles overlap', 'Find the missing element in arithmetic progression'], 'hr_questions': ['Tell me about yourself', 'Why HCL Technologies?', "What do you know about HCL's founder Shiv Nadar?", 'Describe your teamwork experience', 'How do you handle tight deadlines?', 'What are your career aspirations?', 'Tell me about a challenging situation you faced', 'How do you stay updated with technology?', 'Are you willing to work in shifts?', 'What questions do you have for us?'], 'tips': ['HCL SAT is moderate difficulty — easy to clear with practice', 'HCL values loyalty and long-term commitment', 'Know basics of any one programming language', 'Communication is key — HCL works with global clients', 'HCL TSS program has bond period — be aware before joining', 'Technical interview focuses on fundamentals']}

INDIAN_COMPANIES['accenture'] = {'name': 'Accenture', 'full_name': 'Accenture India', 'icon': '🟪', 'color': '#A100FF', 'package': '4.5 LPA (ASE) / 6.5 LPA (SE)', 'eligibility': '60% aggregate, 10th and 12th cutoffs', 'exam_pattern': 'Accenture AMCAT / Internal Assessment', 'interview_rounds': ['Online Assessment (90 min)', 'Technical Interview (1-2 rounds)', 'HR Interview (1)'], 'focus_areas': ['Aptitude', 'Coding', 'Problem Solving', 'Communication'], 'amcat_pattern': {'total_time_minutes': 90, 'sections': [{'name': 'Numerical Ability', 'questions': 25, 'time_minutes': 20, 'types': ['Quantitative'], 'difficulty': 'easy-medium', 'topics': ['Number System', 'HCF & LCM', 'Percentages', 'Profit & Loss', 'Time & Work', 'Speed, Time & Distance', 'Simple & Compound Interest', 'Mixture & Alligation']}, {'name': 'Logical Reasoning', 'questions': 25, 'time_minutes': 25, 'types': ['Logical', 'Abstract Reasoning'], 'difficulty': 'medium', 'topics': ['Coding-Decoding', 'Syllogisms', 'Blood Relations', 'Direction Sense', 'Series', 'Puzzles', 'Arrangements', 'Odd One Out']}, {'name': 'Verbal Ability', 'questions': 25, 'time_minutes': 20, 'types': ['English', 'Reading'], 'difficulty': 'easy', 'topics': ['Grammar', 'Sentence Correction', 'Cloze Test', 'Synonyms', 'Antonyms', 'Reading Comprehension', 'Para Jumbles']}, {'name': 'Coding', 'questions': 2, 'time_minutes': 25, 'types': ['Problem Solving'], 'difficulty': 'medium', 'topics': ['Arrays', 'Strings', 'Linked Lists', 'Basic Algorithms', 'Mathematical', 'Pattern Matching']}]}, 'coding_patterns': ['Find the contiguous subarray with maximum sum', 'Implement Caesar Cipher encryption', 'Find the second smallest element', 'Check if a linked list is palindrome', 'Count occurrences of a character in string', 'Find the closest pair from two sorted arrays', 'Implement queue using stack', 'Find maximum width of binary tree', 'Check if number is Fibonacci', 'Find the index of 0 to be replaced to get maximum consecutive 1s'], 'hr_questions': ['Tell me about yourself', 'Why Accenture?', "What do you know about Accenture's services?", 'Describe your most impactful project', 'How do you handle multiple deadlines?', 'What does innovation mean to you?', 'Tell me about a time you showed initiative', 'How do you adapt to change?', 'Where do you see yourself in 3 years?', 'What are your salary expectations?'], 'tips': ['Accenture values innovation and creative thinking', 'AMCAT format is similar to other campus placements', 'Coding section is moderate — practice basic patterns', 'Accenture focuses on consulting mindset', 'Know about current technology trends (AI, Cloud, Blockchain)', 'Communication skills are very important for client-facing roles']}

INDIAN_COMPANIES['capgemini'] = {'name': 'Capgemini', 'full_name': 'Capgemini India', 'icon': '🔷', 'color': '#0070AD', 'package': '3.8 LPA (Analyst) / 6 LPA (Senior Analyst)', 'eligibility': '60% aggregate, no live backlogs', 'exam_pattern': 'Capgemini InDrive Assessment', 'interview_rounds': ['Online Aptitude Test (60 min)', 'Coding Test (30 min)', 'Technical Interview (1-2 rounds)', 'HR Interview (1)'], 'focus_areas': ['Aptitude', 'Coding', 'Technical', 'Communication'], 'indrive_pattern': {'total_time_minutes': 90, 'sections': [{'name': 'Aptitude', 'questions': 25, 'time_minutes': 30, 'types': ['Numerical', 'Logical', 'Verbal'], 'difficulty': 'easy-medium', 'topics': ['Arithmetic', 'Algebra', 'Geometry', 'Puzzles', 'Coding-Decoding', 'Critical Reasoning', 'Grammar', 'Vocabulary']}, {'name': 'Coding', 'questions': 2, 'time_minutes': 30, 'types': ['Problem Solving'], 'difficulty': 'easy-medium', 'topics': ['Arrays', 'Strings', 'Math', 'Loops', 'Conditions', 'Basic Pattern Matching']}, {'name': 'Essay Writing', 'questions': 1, 'time_minutes': 15, 'types': ['Written Communication'], 'difficulty': 'easy', 'topics': ['Technology', 'Business', 'Social Issues']}]}, 'coding_patterns': ['Find the maximum sum of non-adjacent elements', 'Check if a string is a valid palindrome ignoring non-alphanumeric chars', 'Find the missing number in a permutation', 'Print all prime numbers up to N', 'Find the length of longest increasing subsequence', 'Check if two strings are one edit away', 'Find the minimum number of coins for change', 'Implement flatten nested array', 'Find majority element in array', 'Check if a number is a happy number'], 'hr_questions': ['Tell me about yourself', 'Why Capgemini?', "What do you know about Capgemini's values?", 'Describe a time you solved a difficult problem', 'How do you manage work-life balance?', 'What role do you usually take in team projects?', 'Tell me about your project experience', 'How do you handle feedback?', 'Are you willing to relocate?', 'Where do you see yourself after 5 years?'], 'tips': ['Capgemini InDrive is slightly easier than other placements', 'Essay writing is scoring — write structured essays', 'Focus on aptitude speed and accuracy', 'Know basics of SQL and one programming language', 'Capgemini values diverse perspectives', 'Technical interview is moderate — focus on fundamentals']}

INDIAN_COMPANIES['tech_mahindra'] = {'name': 'Tech Mahindra', 'full_name': 'Tech Mahindra Limited', 'icon': '🟢', 'color': '#0066B3', 'package': '3.6 LPA (Coder) / 5.5 LPA (Coder Plus)', 'eligibility': '60% aggregate, eligible branches', 'exam_pattern': 'Tech Mahindra SMART Interview Process', 'interview_rounds': ['Online Assessment (75 min)', 'Technical Interview (1-2 rounds)', 'HR/Manger Interview (1)'], 'focus_areas': ['Aptitude', 'Programming', 'English', 'Domain'], 'smart_pattern': {'total_time_minutes': 75, 'sections': [{'name': 'Aptitude', 'questions': 20, 'time_minutes': 20, 'types': ['Numerical', 'Logical'], 'difficulty': 'easy-medium', 'topics': ['Percentages', 'Averages', 'Ratio', 'Time & Work', 'Number Series', 'Coding-Decoding', 'Syllogisms', 'Direction Sense']}, {'name': 'Coding', 'questions': 2, 'time_minutes': 35, 'types': ['Problem Solving'], 'difficulty': 'easy-medium', 'topics': ['Arrays', 'Strings', 'Math', 'Basic DS', 'Recursion', 'Sorting', 'Searching']}, {'name': 'English', 'questions': 20, 'time_minutes': 20, 'types': ['Grammar', 'Comprehension'], 'difficulty': 'easy', 'topics': ['Error Spotting', 'Fill in Blanks', 'Reading Comprehension', 'Sentence Rearrangement', 'One Word Substitution']}]}, 'coding_patterns': ['Find equilibrium index of array', 'Check if a string is valid shuffle of two strings', 'Find the maximum depth of binary tree', 'Count number of inversions in array', 'Implement basic calculator', 'Find the celebrity problem', 'Find longest consecutive sequence', 'Check if binary tree is balanced', 'Find minimum window substring', 'Implement LRU cache'], 'hr_questions': ['Tell me about yourself', 'Why Tech Mahindra?', 'What do you know about 5G technology?', 'Describe your learning experience', 'How do you handle conflicts?', 'What are your technical skills?', 'Tell me about a project you are proud of', 'How do you handle failure?', 'Are you willing to work in telecom domain?', 'What are your hobbies?'], 'tips': ['Tech Mahindra values technical depth', 'Know about telecom and 5G basics', 'Aptitude is moderate — focus on speed', 'Coding requires basic to medium DSA', 'Tech Mahindra has bond period — check before accepting', "English section is scoring — don't neglect it"]}



INDIAN_COMPANIES["lti"] = {
    "name": "LTIMindtree",
    "full_name": "L&T Infotech (LTIMindtree)",
    "icon": "\U0001f3d7\ufe0f",
    "color": "#00529B",
    "package": "4 LPA (Analyst) / 6.25 LPA (Senior Analyst)",
    "eligibility": "60% aggregate, CS/IT/ECE branches",
    "exam_pattern": "LTI Aptitude Test + Coding",
    "interview_rounds": ["Online Aptitude & Coding Test (120 min)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["Aptitude", "Coding", "Technical", "Communication"],
    "lti_aptitude_pattern": {
        "total_time_minutes": 120,
        "sections": [
            {"name": "Aptitude", "questions": 30, "time_minutes": 30, "types": ["Quantitative", "Logical"], "difficulty": "easy-medium", "topics": ["Time & Work", "Profit & Loss", "Percentages", "Probability", "Blood Relations", "Coding-Decoding", "Series", "Direction Sense"]},
            {"name": "Programming", "questions": 20, "time_minutes": 30, "types": ["MCQ on Programming", "Output Prediction"], "difficulty": "easy-medium", "topics": ["C/Java/Python Basics", "OOP", "Loops", "Arrays", "Strings", "Recursion", "Time Complexity"]},
            {"name": "Coding", "questions": 2, "time_minutes": 45, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Linked Lists", "Math", "Sorting", "Searching", "Basic DP"]},
            {"name": "English", "questions": 25, "time_minutes": 15, "types": ["Grammar", "Vocabulary", "Reading"], "difficulty": "easy", "topics": ["Error Spotting", "Synonyms", "Antonyms", "Cloze Test", "Sentence Correction"]}
        ]
    },
    "coding_patterns": ["Find the maximum occurring character in a string", "Reverse a linked list in groups of K", "Check if a number is a power of another number", "Find the shortest path in a maze", "Implement a circular buffer", "Find the first non-repeating character in a stream", "Merge two binary search trees", "Find the largest rectangle in histogram", "Check if two BSTs are identical", "Implement trie for word search"],
    "hr_questions": ["Tell me about yourself", "Why LTIMindtree?", "What do you know about Larsen & Toubro?", "Describe a project where you worked under tight deadlines", "How do you handle multiple priorities?", "Where do you see yourself in 5 years?", "What are your strengths and weaknesses?", "Are you willing to relocate?", "How do you handle stress?", "What motivates you to work in IT services?"],
    "tips": ["LTIMindtree aptitude is moderate \u2014 practice arithmetic and logical reasoning", "Know about L&T group's diverse business portfolio", "Coding section focuses on arrays, strings, and basic DSA", "Communication skills are valued for client-facing roles", "Technical interview may go deep into your project and CS fundamentals", "Know basics of cloud computing and digital transformation trends"]
}

INDIAN_COMPANIES["mphasis"] = {
    "name": "Mphasis",
    "full_name": "Mphasis Limited",
    "icon": "\U0001f52e",
    "color": "#6B2D8B",
    "package": "4 LPA (Analyst) / 6 LPA (Sr. Analyst)",
    "eligibility": "60% aggregate, CS/IT/ECE/EEE branches",
    "exam_pattern": "AMCAT-based Assessment",
    "interview_rounds": ["AMCAT Online Test (90 min)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["Aptitude", "Coding", "English", "Domain Knowledge"],
    "amcat_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Logical Reasoning", "questions": 25, "time_minutes": 20, "types": ["Logical", "Abstract"], "difficulty": "easy-medium", "topics": ["Syllogisms", "Puzzles", "Blood Relations", "Direction Sense", "Coding-Decoding", "Series", "Seating Arrangement", "Venn Diagrams"]},
            {"name": "Quantitative Aptitude", "questions": 25, "time_minutes": 25, "types": ["Numerical", "Data Interpretation"], "difficulty": "easy-medium", "topics": ["Percentages", "Profit & Loss", "Time & Work", "Probability", "Permutations", "Bar Graphs", "Pie Charts", "Simple Interest"]},
            {"name": "Coding", "questions": 2, "time_minutes": 30, "types": ["Problem Solving"], "difficulty": "easy-medium", "topics": ["Arrays", "Strings", "Math", "Loops", "Pattern Printing", "Basic Data Structures"]},
            {"name": "Verbal Ability", "questions": 20, "time_minutes": 15, "types": ["Grammar", "Comprehension"], "difficulty": "easy", "topics": ["Grammar", "Vocabulary", "Reading Comprehension", "Sentence Correction", "Fill in Blanks"]}
        ]
    },
    "coding_patterns": ["Find the kth largest element in array", "Implement string to integer conversion", "Find the level with maximum sum in binary tree", "Check if a linked list has a cycle", "Find the longest common prefix among strings", "Implement a basic LRU cache", "Count the number of islands in a grid", "Find the intersection point of two linked lists", "Implement queue using two stacks", "Find the smallest window containing all characters of another string"],
    "hr_questions": ["Tell me about yourself", "Why Mphasis?", "What do you know about Mphasis's AI-first approach?", "Describe a challenging technical problem you solved", "How do you handle work pressure?", "Where do you see yourself in 5 years?", "What are your career goals?", "Are you flexible with location?", "How do you keep yourself updated with technology?", "What questions do you have for us?"],
    "tips": ["Mphasis uses AMCAT \u2014 familiarize yourself with the format", "Focus on logical reasoning \u2014 it's heavily weighted", "Know about Mphasis's focus on AI and automation", "Practice basic to medium DSA problems", "Communication skills are valued for client projects", "Be prepared to discuss your projects in detail"]
}

INDIAN_COMPANIES["hexaware"] = {
    "name": "Hexaware",
    "full_name": "Hexaware Technologies",
    "icon": "\U0001f537",
    "color": "#E31937",
    "package": "4 LPA (Trainee) / 5.5 LPA (Analyst)",
    "eligibility": "60% aggregate, CS/IT branches preferred",
    "exam_pattern": "Hexaware Assessment Test",
    "interview_rounds": ["Online Aptitude & Coding Test (100 min)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["Aptitude", "Programming", "English", "Problem Solving"],
    "hexaware_assessment_pattern": {
        "total_time_minutes": 100,
        "sections": [
            {"name": "Aptitude", "questions": 25, "time_minutes": 25, "types": ["Numerical", "Logical"], "difficulty": "easy-medium", "topics": ["Number System", "Percentages", "Ratio", "Time & Work", "Blood Relations", "Coding-Decoding", "Syllogisms", "Odd One Out"]},
            {"name": "Coding", "questions": 2, "time_minutes": 40, "types": ["Problem Solving"], "difficulty": "easy-medium", "topics": ["Arrays", "Strings", "Math", "Sorting", "Searching", "Pattern Printing", "Basic Recursion"]},
            {"name": "English", "questions": 20, "time_minutes": 15, "types": ["Grammar", "Vocabulary"], "difficulty": "easy", "topics": ["Error Spotting", "Fill in Blanks", "Synonyms", "Antonyms", "Sentence Completion", "Reading Comprehension"]},
            {"name": "Domain", "questions": 15, "time_minutes": 20, "types": ["MCQ"], "difficulty": "medium", "topics": ["DBMS", "OS", "Computer Networks", "OOP", "Data Structures"]}
        ]
    },
    "coding_patterns": ["Find the maximum subarray sum (Kadane's)", "Check if a number is Armstrong number", "Find the GCD and LCM of two numbers", "Implement bubble sort and count swaps", "Find the second largest element without sorting", "Count the frequency of each element in array", "Check if string is anagram of palindrome", "Find the spiral order traversal of matrix", "Implement binary search on rotated sorted array", "Find the longest palindromic subsequence"],
    "hr_questions": ["Tell me about yourself", "Why Hexaware?", "What do you know about Hexaware's automation focus?", "Describe a project you worked on", "How do you manage your time?", "Where do you see yourself in 5 years?", "What are your hobbies?", "Are you willing to relocate?", "How do you handle failure?", "What is your biggest achievement?"],
    "tips": ["Hexaware assessment is moderate \u2014 focus on speed and accuracy", "Domain section covers CS fundamentals \u2014 review DBMS and OS", "Know about Hexaware's digital transformation services", "Practice basic coding patterns \u2014 arrays and strings", "English section is scoring \u2014 prepare grammar basics", "Technical interview focuses on fundamentals and projects"]
}

INDIAN_COMPANIES["cgi"] = {
    "name": "CGI",
    "full_name": "CGI India",
    "icon": "\U0001f310",
    "color": "#005B82",
    "package": "3.5 LPA (Analyst) / 6 LPA (Sr. Analyst)",
    "eligibility": "60% aggregate, CS/IT/ECE branches",
    "exam_pattern": "CGI Assessment Test",
    "interview_rounds": ["Online Assessment (90 min)", "Technical Interview (2 rounds)", "HR Interview (1)"],
    "focus_areas": ["Aptitude", "Programming", "Database", "Communication"],
    "cgi_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Aptitude", "questions": 25, "time_minutes": 25, "types": ["Quantitative", "Logical"], "difficulty": "easy-medium", "topics": ["Arithmetic", "Algebra", "Time & Work", "Profit & Loss", "Puzzles", "Blood Relations", "Direction Sense", "Series"]},
            {"name": "Coding", "questions": 2, "time_minutes": 40, "types": ["Problem Solving"], "difficulty": "easy-medium", "topics": ["Arrays", "Strings", "Math", "Loops", "Conditions", "Basic DS"]},
            {"name": "SQL", "questions": 10, "time_minutes": 15, "types": ["Query Writing", "MCQ"], "difficulty": "medium", "topics": ["Joins", "Subqueries", "Group By", "Having", "Normalization", "Indexing"]},
            {"name": "English", "questions": 15, "time_minutes": 10, "types": ["Grammar", "Comprehension"], "difficulty": "easy", "topics": ["Grammar", "Vocabulary", "Reading Comprehension", "Error Detection"]}
        ]
    },
    "coding_patterns": ["Find the peak element in array", "Implement myAtoi() function", "Find the maximum length of subarray with equal 0s and 1s", "Check if a binary tree is a BST", "Find the minimum path sum in grid", "Implement a simple text editor using stack", "Find the first repeating element in array", "Check if two strings are isomorphic", "Find the median of two sorted arrays", "Implement next permutation"],
    "hr_questions": ["Tell me about yourself", "Why CGI?", "What do you know about CGI's global presence?", "Describe a team project you led", "How do you handle deadlines?", "Where do you see yourself in 5 years?", "What are your strengths and weaknesses?", "Are you flexible with relocation?", "How do you learn new technologies?", "What motivates you to work in consulting?"],
    "tips": ["CGI values strong technical fundamentals", "SQL section is important \u2014 practice joins and queries", "Know about CGI's consulting and IT services model", "Focus on aptitude and coding basics", "Technical interview goes deep into CS concepts", "Communication skills are valued for client interactions"]
}

INDIAN_COMPANIES["virtusa"] = {
    "name": "Virtusa",
    "full_name": "Virtusa Consulting Services",
    "icon": "\U0001f537",
    "color": "#0066CC",
    "package": "4 LPA (Analyst) / 6 LPA (Senior Analyst)",
    "eligibility": "60% aggregate, CS/IT/ECE branches",
    "exam_pattern": "Virtusa Assessment Test",
    "interview_rounds": ["Online Assessment (105 min)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["Aptitude", "Coding", "Technical", "Communication"],
    "virtusa_assessment_pattern": {
        "total_time_minutes": 105,
        "sections": [
            {"name": "Aptitude", "questions": 25, "time_minutes": 25, "types": ["Quantitative", "Logical"], "difficulty": "easy-medium", "topics": ["Percentages", "Time & Work", "Profit & Loss", "Probability", "Coding-Decoding", "Syllogisms", "Blood Relations", "Number Series"]},
            {"name": "Coding", "questions": 2, "time_minutes": 45, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Linked Lists", "Trees", "Recursion", "Dynamic Programming Basics", "HashMaps"]},
            {"name": "English", "questions": 20, "time_minutes": 15, "types": ["Grammar", "Vocabulary"], "difficulty": "easy", "topics": ["Grammar", "Synonyms", "Antonyms", "Reading Comprehension", "Sentence Correction", "Para Jumbles"]},
            {"name": "Technical MCQ", "questions": 20, "time_minutes": 20, "types": ["MCQ"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Data Structures", "Algorithms"]}
        ]
    },
    "coding_patterns": ["Find the maximum area of rectangle in histogram", "Check if a string can be formed from another", "Find the sum of all subarrays of array", "Implement a priority queue", "Find the level of a given node in binary tree", "Count the number of occurrences in sorted array", "Find the longest mountain in array", "Check if a number can be expressed as sum of two primes", "Find the minimum number of jumps to reach end", "Implement flatten a multilevel linked list"],
    "hr_questions": ["Tell me about yourself", "Why Virtusa?", "What do you know about Virtusa's digital engineering focus?", "Describe a challenging problem you solved", "How do you handle stress?", "Where do you see yourself in 5 years?", "What are your career goals?", "Are you willing to relocate?", "How do you handle feedback?", "What questions do you have for us?"],
    "tips": ["Virtusa has a slightly harder coding section \u2014 practice medium DSA", "Know about Virtusa's digital engineering and consulting services", "Technical MCQ section tests CS fundamentals thoroughly", "Communication skills are valued for global client delivery", "Focus on DSA fundamentals for the coding section", "Be prepared to discuss projects in detail"]
}

INDIAN_COMPANIES["ibm"] = {
    "name": "IBM",
    "full_name": "IBM Global Business Services",
    "icon": "\U0001f4a0",
    "color": "#0530AD",
    "package": "4.5 LPA (GBS) / 7 LPA (Software)",
    "eligibility": "65% aggregate, CS/IT/ECE preferred",
    "exam_pattern": "IBM Cognitive Assessment + Hackathon",
    "interview_rounds": ["IBM Online Cognitive Test (120 min)", "Coding Challenge / Hackathon (120 min)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["Cognitive Ability", "Coding", "Technical", "Problem Solving"],
    "ibm_cognitive_pattern": {
        "total_time_minutes": 120,
        "sections": [
            {"name": "Numerical Reasoning", "questions": 20, "time_minutes": 25, "types": ["Quantitative", "Data Interpretation"], "difficulty": "medium", "topics": ["Data Interpretation", "Percentages", "Ratios", "Time & Work", "Probability", "Statistics", "Graphs", "Tables"]},
            {"name": "Verbal Reasoning", "questions": 20, "time_minutes": 25, "types": ["Reading", "Grammar"], "difficulty": "medium", "topics": ["Reading Comprehension", "Critical Reasoning", "Sentence Correction", "Inference", "Argument Analysis", "Para Jumbles"]},
            {"name": "Abstract Reasoning", "questions": 15, "time_minutes": 20, "types": ["Patterns", "Logical"], "difficulty": "medium", "topics": ["Pattern Recognition", "Series", "Odd One Out", "Analogy", "Spatial Reasoning", "Matrix Reasoning"]},
            {"name": "Coding", "questions": 2, "time_minutes": 50, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Recursion", "HashMaps", "Sorting"]}
        ]
    },
    "coding_patterns": ["Find the shortest path between two nodes in graph", "Implement a JSON parser", "Find the longest increasing subsequence in O(n log n)", "Design and implement an autocomplete system", "Find all valid parentheses combinations", "Implement a thread-safe singleton", "Find the maximum profit from stock transactions", "Check if a string is a valid IPv4 address", "Find the smallest range covering elements from K lists", "Implement a rate limiter"],
    "hr_questions": ["Tell me about yourself", "Why IBM?", "What do you know about IBM's AI and cloud strategy?", "Describe a time you solved a complex problem", "How do you handle ambiguity?", "Where do you see yourself in 5 years?", "What is your biggest achievement?", "How do you handle failure?", "Are you willing to work on legacy systems?", "What questions do you have for us?"],
    "tips": ["IBM cognitive test is analytical \u2014 practice data interpretation", "Hackathon round tests real coding ability under time pressure", "Know about IBM's focus on AI (Watson), Cloud, and Quantum", "Practice medium to hard DSA problems", "IBM values problem-solving methodology over perfect code", "Be prepared for system design questions in technical round"]
}

INDIAN_COMPANIES["dell"] = {
    "name": "Dell",
    "full_name": "Dell Technologies India",
    "icon": "\U0001f4bb",
    "color": "#007DB8",
    "package": "5 LPA (Analyst) / 8 LPA (Sr. Analyst)",
    "eligibility": "65% aggregate, CS/IT/ECE branches",
    "exam_pattern": "Dell Assessment Test",
    "interview_rounds": ["Online Assessment (90 min)", "Technical Interview (2 rounds)", "Manager / HR Interview (1)"],
    "focus_areas": ["Aptitude", "Coding", "Problem Solving", "Technical"],
    "dell_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Logical Reasoning", "questions": 20, "time_minutes": 20, "types": ["Logical", "Abstract"], "difficulty": "medium", "topics": ["Puzzles", "Syllogisms", "Coding-Decoding", "Series", "Blood Relations", "Seating Arrangement", "Direction Sense", "Venn Diagrams"]},
            {"name": "Quantitative Aptitude", "questions": 20, "time_minutes": 20, "types": ["Numerical", "Data Interpretation"], "difficulty": "medium", "topics": ["Percentages", "Profit & Loss", "Time & Work", "Probability", "Permutations", "Graphs", "Tables", "Caselets"]},
            {"name": "Coding", "questions": 2, "time_minutes": 40, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Trees", "Graphs", "DP Basics", "Recursion", "HashMaps", "Sorting"]},
            {"name": "Verbal Ability", "questions": 15, "time_minutes": 10, "types": ["Grammar", "Reading"], "difficulty": "easy", "topics": ["Grammar", "Vocabulary", "Reading Comprehension", "Sentence Correction"]}
        ]
    },
    "coding_patterns": ["Find the longest substring with at most K distinct characters", "Implement a deep copy of a linked list with random pointers", "Find the maximum path sum in binary tree", "Check if a string is a valid shuffle of two strings", "Find the minimum window substring", "Implement a circular deque", "Find the number of provinces in graph", "Check if a binary tree is a mirror of itself", "Find the maximum product of three numbers", "Implement a stack that supports getMin in O(1)"],
    "hr_questions": ["Tell me about yourself", "Why Dell Technologies?", "What do you know about Dell's digital transformation?", "Describe a project where you showed innovation", "How do you handle competing priorities?", "Where do you see yourself in 5 years?", "What is your leadership style?", "How do you handle conflict?", "Are you comfortable with agile methodology?", "What questions do you have for us?"],
    "tips": ["Dell's test is analytical \u2014 focus on logical reasoning and data interpretation", "Know about Dell's cloud and infrastructure solutions", "Practice medium difficulty DSA problems", "Technical interviews focus on CS fundamentals and projects", "Dell values innovation and customer-centric thinking", "Be prepared for system design basics in senior roles"]
}

INDIAN_COMPANIES["coforge"] = {
    "name": "Coforge",
    "full_name": "Coforge (formerly NIIT Technologies)",
    "icon": "\U0001f537",
    "color": "#003087",
    "package": "4 LPA (Analyst) / 6.5 LPA (Sr. Analyst)",
    "eligibility": "60% aggregate, CS/IT/ECE branches",
    "exam_pattern": "Coforge Online Test",
    "interview_rounds": ["Online Aptitude & Coding Test (110 min)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["Aptitude", "Coding", "Technical", "Communication"],
    "coforge_test_pattern": {
        "total_time_minutes": 110,
        "sections": [
            {"name": "Aptitude", "questions": 30, "time_minutes": 30, "types": ["Numerical", "Logical"], "difficulty": "easy-medium", "topics": ["Percentages", "Profit & Loss", "Time & Work", "Probability", "Blood Relations", "Coding-Decoding", "Syllogisms", "Number Series"]},
            {"name": "Programming", "questions": 15, "time_minutes": 20, "types": ["MCQ on Programming"], "difficulty": "easy-medium", "topics": ["C/Java Basics", "OOP", "Loops", "Arrays", "Strings", "Recursion", "Output Prediction"]},
            {"name": "Coding", "questions": 2, "time_minutes": 45, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Linked Lists", "Trees", "DP Basics", "HashMaps", "Sorting", "Searching"]},
            {"name": "English", "questions": 15, "time_minutes": 15, "types": ["Grammar", "Comprehension"], "difficulty": "easy", "topics": ["Error Spotting", "Synonyms", "Antonyms", "Reading Comprehension", "Fill in Blanks"]}
        ]
    },
    "coding_patterns": ["Find the maximum difference between two elements where larger appears after smaller", "Implement a basic expression evaluator", "Find the celebrity in a party using matrix", "Check if a string can be rearranged to form a palindrome", "Find the kth smallest element in BST", "Implement a basic URL shortener logic", "Find the number of ways to climb stairs with variable steps", "Check if two binary trees are mirrors", "Find the longest palindromic substring", "Implement a basic job scheduling algorithm"],
    "hr_questions": ["Tell me about yourself", "Why Coforge?", "What do you know about Coforge's travel and BFSI focus?", "Describe a challenging project you worked on", "How do you manage time effectively?", "Where do you see yourself in 5 years?", "What are your strengths?", "How do you handle stress?", "Are you willing to relocate?", "What motivates you in your career?"],
    "tips": ["Coforge test is moderate \u2014 focus on aptitude and coding", "Know about Coforge's BFSI and travel domain expertise", "Practice basic to medium DSA problems", "Programming MCQ section covers fundamentals thoroughly", "Communication skills are valued for consulting roles", "Be prepared for project-based technical questions"]
}



INDIAN_COMPANIES["flipkart"] = {
    "name": "Flipkart",
    "full_name": "Flipkart (Walmart Group)",
    "icon": "\U0001f6d2",
    "color": "#2874F0",
    "package": "12 LPA (SDE-1) / 20 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Flipkart Online Coding Test + Interviews",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "Hiring Manager Interview (1)", "HR Interview (1)"],
    "focus_areas": ["Data Structures", "Algorithms", "System Design", "Problem Solving"],
    "flipkart_coding_test": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Aptitude & Logic", "questions": 15, "time_minutes": 20, "types": ["Quantitative", "Logical"], "difficulty": "medium", "topics": ["Probability", "Combinatorics", "Puzzles", "Number Theory", "Data Interpretation"]},
            {"name": "Coding", "questions": 3, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Two Pointers"]}
        ]
    },
    "coding_patterns": ["Design and implement an autocomplete system", "Find the maximum sum of a subarray of size K", "Find the median of a stream of integers", "Implement LRU Cache with O(1) operations", "Find the shortest path in a weighted graph (Dijkstra)", "Design a URL shortener with analytics", "Find the maximum width of a binary tree", "Implement a sliding window maximum", "Find all anagrams of a string in another string", "Design a ticket booking system"],
    "hr_questions": ["Tell me about yourself", "Why Flipkart?", "What do you know about Flipkart's tech stack?", "Describe a time you solved a critical bug", "How do you handle high-pressure situations?", "Where do you see yourself in 3 years?", "What is your biggest technical achievement?", "How do you stay updated with technology?", "What do you think about Flipkart's competition with Amazon?", "What questions do you have for us?"],
    "tips": ["Flipkart coding test is challenging \u2014 practice LeetCode Medium-Hard", "Know about Flipkart's tech stack (Microservices, React, Java/Python)", "System design basics are expected for SDE-1", "Focus on DSA fundamentals \u2014 Trees, Graphs, DP", "Know about e-commerce domain (inventory, payments, logistics)", "Flipkart values clean code and optimal solutions"]
}

INDIAN_COMPANIES["razorpay"] = {
    "name": "Razorpay",
    "full_name": "Razorpay Software Private Limited",
    "icon": "\U0001f4b3",
    "color": "#072654",
    "package": "10 LPA (SDE-1) / 18 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Razorpay SWE Assessment + Interviews",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Problem Solving"],
    "razorpay_swe_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Coding", "questions": 3, "time_minutes": 90, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Sliding Window", "Two Pointers", "Recursion"]}
        ]
    },
    "coding_patterns": ["Design a payment gateway system", "Find the maximum profit from at most K transactions", "Implement a rate limiter using sliding window", "Find the shortest path in unweighted graph", "Design a notification system", "Find the number of ways to decode a string", "Implement a basic ledger system", "Find the maximum product subarray", "Design an idempotent API endpoint", "Find the longest increasing subsequence"],
    "hr_questions": ["Tell me about yourself", "Why Razorpay?", "What do you know about Razorpay's payment infrastructure?", "Describe a complex system you designed", "How do you handle production incidents?", "Where do you see yourself in 3 years?", "What is your approach to debugging?", "How do you handle disagreements with teammates?", "What do you know about fintech regulations?", "What questions do you have for us?"],
    "tips": ["Razorpay expects strong DSA \u2014 practice Medium to Hard problems", "Know about payment systems (UPI, cards, net banking)", "System design round is crucial \u2014 study distributed systems", "Razorpay uses Go, Python, Java \u2014 know at least one well", "Understand concepts like idempotency, exactly-once delivery", "Razorpay values engineering excellence and ownership"]
}

INDIAN_COMPANIES["zomato"] = {
    "name": "Zomato",
    "full_name": "Zomato Limited",
    "icon": "\U0001f355",
    "color": "#E23744",
    "package": "10 LPA (SDE-1) / 16 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Zomato Online Coding Test + Interviews",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design / Architecture (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Problem Solving"],
    "zomato_coding_test": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "MCQ", "questions": 15, "time_minutes": 20, "types": ["CS Fundamentals"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Time Complexity", "Data Structures"]},
            {"name": "Coding", "questions": 3, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Stacks", "Queues"]}
        ]
    },
    "coding_patterns": ["Design a restaurant discovery system", "Find the minimum time to reach all restaurants", "Implement a real-time order tracking system", "Find the most popular item across restaurants", "Design a food delivery routing algorithm", "Implement a search autocomplete for restaurants", "Find the maximum number of non-overlapping orders", "Design a review and rating system", "Find the shortest delivery route in a city", "Implement a surge pricing algorithm"],
    "hr_questions": ["Tell me about yourself", "Why Zomato?", "What do you know about Zomato's tech architecture?", "Describe a time you improved a process", "How do you handle ambiguity?", "Where do you see yourself in 3 years?", "What is your approach to code reviews?", "How do you handle on-call incidents?", "What do you think about Zomato's business model?", "What questions do you have for us?"],
    "tips": ["Zomato focuses on problem-solving ability and engineering thinking", "Practice LeetCode Medium problems consistently", "Know about Zomato's microservices architecture", "Understand concepts like caching, message queues, load balancing", "Zomato values ownership and shipping fast", "Be prepared to discuss real-world system design trade-offs"]
}

INDIAN_COMPANIES["phonepe"] = {
    "name": "PhonePe",
    "full_name": "PhonePe Private Limited",
    "icon": "\U0001f4f1",
    "color": "#5F259F",
    "package": "12 LPA (SDE-1) / 20 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "PhonePe Engineering Assessment",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Fintech Domain"],
    "phonepe_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Coding", "questions": 4, "time_minutes": 90, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Two Pointers", "Recursion", "Bit Manipulation"]}
        ]
    },
    "coding_patterns": ["Design a UPI payment system", "Find the maximum cashback amount in range", "Implement a wallet balance management system", "Find the minimum cost to transfer money between accounts", "Design a transaction reconciliation system", "Implement a basic blockchain validation", "Find the maximum number of transactions in time window", "Design a fraud detection system", "Find the shortest path for bill splitting", "Implement a split payment calculator"],
    "hr_questions": ["Tell me about yourself", "Why PhonePe?", "What do you know about PhonePe's UPI infrastructure?", "Describe a system you designed from scratch", "How do you ensure code quality?", "Where do you see yourself in 3 years?", "What is your approach to handling technical debt?", "How do you handle disagreements in code reviews?", "What do you know about fintech security?", "What questions do you have for us?"],
    "tips": ["PhonePe expects strong DSA and system design skills", "Know about UPI, payment systems, and fintech regulations", "Practice hard DSA problems \u2014 graphs, DP, trees", "PhonePe uses Java extensively \u2014 know it well", "Understand distributed systems concepts (consensus, replication)", "PhonePe values engineering rigor and security awareness"]
}

INDIAN_COMPANIES["swiggy"] = {
    "name": "Swiggy",
    "full_name": "Swiggy (Bundl Technologies)",
    "icon": "\U0001f6f5",
    "color": "#FC8019",
    "package": "10 LPA (SDE-1) / 18 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Swiggy Online Coding Test + Interviews",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Problem Solving"],
    "swiggy_coding_test": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Aptitude & CS Fundamentals", "questions": 20, "time_minutes": 20, "types": ["MCQ"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Aptitude", "Probability", "Puzzles"]},
            {"name": "Coding", "questions": 3, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Stacks"]}
        ]
    },
    "coding_patterns": ["Design a real-time delivery tracking system", "Find the optimal route for a delivery partner", "Implement a surge pricing algorithm based on demand", "Find the maximum number of orders deliverable in time T", "Design a restaurant ranking system", "Implement a live order status update system", "Find the minimum delivery time for multiple orders", "Design an ETA prediction system", "Find the closest restaurants using geospatial data", "Implement a queue management system for restaurants"],
    "hr_questions": ["Tell me about yourself", "Why Swiggy?", "What do you know about Swiggy's tech stack?", "Describe a feature you'd add to Swiggy", "How do you handle on-call situations?", "Where do you see yourself in 3 years?", "What is your approach to debugging production issues?", "How do you handle competing priorities?", "What do you think about the food tech industry?", "What questions do you have for us?"],
    "tips": ["Swiggy focuses on practical problem-solving and system design", "Practice LeetCode Medium-Hard problems regularly", "Know about microservices, event-driven architecture", "Understand real-time systems and geospatial data", "Swiggy values speed, ownership, and impact", "Be prepared to design systems with high availability"]
}

INDIAN_COMPANIES["paytm"] = {
    "name": "Paytm",
    "full_name": "Paytm (One97 Communications)",
    "icon": "\U0001f4b3",
    "color": "#002E6D",
    "package": "8 LPA (SDE-1) / 14 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Paytm Engineering Assessment",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Fintech Domain"],
    "paytm_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Aptitude & CS Basics", "questions": 20, "time_minutes": 20, "types": ["MCQ"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Data Structures", "Algorithms"]},
            {"name": "Coding", "questions": 3, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "HashMaps"]}
        ]
    },
    "coding_patterns": ["Design a digital wallet system", "Find the maximum cashback in a transaction range", "Implement a basic payment processing pipeline", "Design a QR code payment system", "Find the optimal cashback distribution", "Implement a bill splitting feature", "Design a recharge and utility payment system", "Find the most used payment method in time window", "Implement a transaction history with search", "Design a merchant settlement system"],
    "hr_questions": ["Tell me about yourself", "Why Paytm?", "What do you know about Paytm's ecosystem?", "Describe a challenging project you worked on", "How do you handle high-traffic situations?", "Where do you see yourself in 3 years?", "What is your approach to secure coding?", "How do you handle technical disagreements?", "What do you know about UPI and digital payments?", "What questions do you have for us?"],
    "tips": ["Paytm focuses on DSA and fintech domain knowledge", "Know about digital payments, UPI, and wallet systems", "Practice medium difficulty DSA problems", "Understand security best practices for financial applications", "Paytm values innovation and scalability", "Be prepared for system design questions on payment systems"]
}

INDIAN_COMPANIES["ola"] = {
    "name": "Ola",
    "full_name": "Ola (ANI Technologies / OLA Electric)",
    "icon": "\U0001f697",
    "color": "#2B61F0",
    "package": "8 LPA (SDE-1) / 15 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Ola Online Coding Test + Interviews",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Problem Solving"],
    "ola_coding_test": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "MCQ", "questions": 15, "time_minutes": 20, "types": ["CS Fundamentals"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Time Complexity", "Data Structures"]},
            {"name": "Coding", "questions": 3, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Two Pointers"]}
        ]
    },
    "coding_patterns": ["Design a ride matching system", "Find the optimal route for a driver", "Implement surge pricing based on demand-supply", "Design a real-time location tracking system", "Find the nearest available cab for a rider", "Implement a fare calculation engine", "Design a driver rating and feedback system", "Find the maximum rides possible in a time window", "Implement a ride pooling/matching algorithm", "Design a fleet management system"],
    "hr_questions": ["Tell me about yourself", "Why Ola?", "What do you know about Ola's mobility platform?", "Describe a system you'd design for ride-sharing", "How do you handle real-time systems?", "Where do you see yourself in 3 years?", "What is your approach to scalability?", "How do you handle failures in distributed systems?", "What do you think about the EV revolution?", "What questions do you have for us?"],
    "tips": ["Ola focuses on system design and DSA", "Know about ride-sharing algorithms and geospatial data", "Practice graph and DP problems extensively", "Understand real-time systems and location services", "Ola values impact and ownership", "Be prepared to design scalable location-based services"]
}

INDIAN_COMPANIES["makemytrip"] = {
    "name": "MakeMyTrip",
    "full_name": "MakeMyTrip (IndiaMART InterMESH)",
    "icon": "\u2708\ufe0f",
    "color": "#E82828",
    "package": "8 LPA (SDE-1) / 14 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "MakeMyTrip Online Coding Test",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Problem Solving"],
    "mmt_coding_test": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Aptitude & CS", "questions": 15, "time_minutes": 15, "types": ["MCQ"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Aptitude", "Puzzles"]},
            {"name": "Coding", "questions": 3, "time_minutes": 75, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing"]}
        ]
    },
    "coding_patterns": ["Design a flight search and booking system", "Find the cheapest flight route between two cities", "Implement a hotel room availability checker", "Design a dynamic pricing engine for flights", "Find the best combination of connecting flights", "Implement a seat selection system", "Design a review and rating system for hotels", "Find the optimal travel itinerary within budget", "Implement a real-time booking confirmation system", "Design a coupon and discount engine"],
    "hr_questions": ["Tell me about yourself", "Why MakeMyTrip?", "What do you know about MakeMyTrip's platform?", "Describe a feature you'd improve on MakeMyTrip", "How do you handle high-traffic booking periods?", "Where do you see yourself in 3 years?", "What is your approach to API design?", "How do you handle payment failures?", "What do you know about the travel tech industry?", "What questions do you have for us?"],
    "tips": ["MakeMyTrip focuses on practical problem-solving", "Know about travel tech (flights, hotels, packages)", "Practice medium difficulty DSA problems", "Understand e-commerce patterns (search, booking, payments)", "MakeMyTrip values user experience and performance", "Be prepared for system design on booking systems"]
}

INDIAN_COMPANIES["freshworks"] = {
    "name": "Freshworks",
    "full_name": "Freshworks Inc.",
    "icon": "\U0001f7e2",
    "color": "#25C656",
    "package": "8 LPA (SDE-1) / 15 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Freshworks Engineering Assessment",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "SaaS Knowledge"],
    "freshworks_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "MCQ", "questions": 15, "time_minutes": 20, "types": ["CS Fundamentals"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Data Structures", "Algorithms"]},
            {"name": "Coding", "questions": 3, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Stacks"]}
        ]
    },
    "coding_patterns": ["Design a ticketing support system", "Implement a real-time chat notification system", "Find the most efficient ticket assignment algorithm", "Design a customer support analytics dashboard", "Implement a SLA tracking system", "Design a multi-tenant SaaS architecture", "Find the peak support hours using data analysis", "Implement a ticket escalation workflow", "Design a knowledge base search system", "Implement a customer satisfaction scoring system"],
    "hr_questions": ["Tell me about yourself", "Why Freshworks?", "What do you know about Freshworks' SaaS products?", "Describe a feature you'd add to Freshdesk", "How do you handle SaaS scalability?", "Where do you see yourself in 3 years?", "What is your approach to API versioning?", "How do you handle multi-tenant data isolation?", "What do you know about SaaS metrics?", "What questions do you have for us?"],
    "tips": ["Freshworks focuses on SaaS product engineering", "Know about Freshdesk, Freshsales, Freshservice products", "Practice medium DSA problems", "Understand SaaS concepts (multi-tenancy, subscriptions, billing)", "Freshworks values product thinking and user empathy", "Be prepared for system design on SaaS-specific challenges"]
}

INDIAN_COMPANIES["zoho"] = {
    "name": "Zoho",
    "full_name": "Zoho Corporation",
    "icon": "\U0001f537",
    "color": "#E42527",
    "package": "5 LPA (Analyst) / 12 LPA (Senior Developer)",
    "eligibility": "60% aggregate, CS/IT/ECE branches",
    "exam_pattern": "Zoho Written Test + Programming",
    "interview_rounds": ["Written Test (90 min)", "Programming Round (90 min)", "Technical Interview (2-3 rounds)", "HR Interview (1)"],
    "focus_areas": ["Aptitude", "Programming", "DSA", "Problem Solving"],
    "zoho_written_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Aptitude", "questions": 25, "time_minutes": 30, "types": ["Numerical", "Logical"], "difficulty": "medium", "topics": ["Number Series", "Coding-Decoding", "Blood Relations", "Direction Sense", "Profit & Loss", "Time & Work", "Probability", "Puzzles"]},
            {"name": "Programming Logic", "questions": 15, "time_minutes": 30, "types": ["MCQ on Programming", "Output Prediction"], "difficulty": "medium", "topics": ["C/Java/Python Basics", "OOP", "Recursion", "Pointers", "File I/O", "Data Structures"]},
            {"name": "Coding", "questions": 2, "time_minutes": 30, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Math", "Recursion", "Sorting", "Searching", "Basic DS"]}
        ]
    },
    "coding_patterns": ["Find the maximum sum of non-adjacent elements", "Print all permutations of a string", "Find the longest consecutive sequence", "Implement power function without using pow()", "Find all subsets of a set", "Check if a string is a valid palindrome II", "Find the minimum number of platforms required", "Implement snake and ladder problem", "Find the number of ways to reach the top of stairs", "Print all combinations of elements that sum to target"],
    "hr_questions": ["Tell me about yourself", "Why Zoho?", "What do you know about Zoho's bootstrapped model?", "Describe a challenging project you worked on", "How do you approach learning new technologies?", "Where do you see yourself in 5 years?", "What are your strengths and weaknesses?", "How do you handle criticism?", "Are you comfortable working in Chennai?", "What motivates you to code?"],
    "tips": ["Zoho's written test focuses on logical reasoning and programming", "Know C, Java, or Python really well", "Practice recursion and backtracking problems", "Zoho values self-learning and problem-solving ability", "Technical interview goes deep into fundamentals", "Zoho has a strong work culture \u2014 be prepared for culture fit"]
}

INDIAN_COMPANIES["byjus"] = {
    "name": "BYJU'S",
    "full_name": "BYJU'S (Think & Learn)",
    "icon": "\U0001f4da",
    "color": "#1B365D",
    "package": "6 LPA (SDE-1) / 12 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "BYJU'S Engineering Assessment",
    "interview_rounds": ["Online Assessment (90 min)", "Technical Interview (2 rounds)", "Hiring Manager Interview (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "Coding", "System Design", "Problem Solving"],
    "byjus_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Aptitude & CS", "questions": 20, "time_minutes": 20, "types": ["MCQ"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Aptitude", "Puzzles", "Data Structures"]},
            {"name": "Coding", "questions": 3, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Recursion"]}
        ]
    },
    "coding_patterns": ["Design a live class streaming system", "Implement a content recommendation engine", "Find the most engaging content using analytics", "Design a student progress tracking system", "Implement a real-time quiz platform", "Design a content delivery network for videos", "Find the optimal learning path for a student", "Implement a doubt resolution system", "Design an adaptive test engine", "Implement a gamification reward system"],
    "hr_questions": ["Tell me about yourself", "Why BYJU'S?", "What do you know about BYJU'S ed-tech platform?", "Describe a feature you'd improve in BYJU'S app", "How do you handle building for millions of users?", "Where do you see yourself in 3 years?", "What is your approach to mobile-first development?", "How do you handle content delivery at scale?", "What do you think about ed-tech in India?", "What questions do you have for us?"],
    "tips": ["BYJU'S focuses on DSA and system design", "Know about streaming, CDN, and mobile app development", "Practice medium difficulty DSA problems", "Understand scalable architecture for millions of users", "BYJU'S values impact-driven engineering", "Be prepared for questions on mobile and web technologies"]
}

INDIAN_COMPANIES["dream11"] = {
    "name": "Dream11",
    "full_name": "Dream11 (Dream Sports)",
    "icon": "\U0001f3cf",
    "color": "#0E4DA4",
    "package": "10 LPA (SDE-1) / 18 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Dream11 Engineering Assessment",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Real-time Systems"],
    "dream11_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "MCQ", "questions": 15, "time_minutes": 15, "types": ["CS Fundamentals"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Time Complexity", "Data Structures"]},
            {"name": "Coding", "questions": 3, "time_minutes": 75, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Two Pointers"]}
        ]
    },
    "coding_patterns": ["Design a fantasy sports team selection algorithm", "Implement real-time score updating system", "Design a contest matchmaking system", "Find the optimal team combination under salary cap", "Implement a live leaderboard with millions of users", "Design a player performance prediction model", "Find the maximum fantasy points combination", "Implement a real-time notification system", "Design a match simulation engine", "Implement a cashout calculation system"],
    "hr_questions": ["Tell me about yourself", "Why Dream11?", "What do you know about fantasy sports technology?", "Describe a system you'd design for real-time scoring", "How do you handle millions of concurrent users?", "Where do you see yourself in 3 years?", "What is your approach to low-latency systems?", "How do you handle data consistency in real-time?", "What do you know about sports analytics?", "What questions do you have for us?"],
    "tips": ["Dream11 focuses on system design and real-time systems", "Know about WebSockets, message queues, and caching", "Practice graph and DP problems", "Understand low-latency and high-concurrency systems", "Dream11 values engineering excellence and innovation", "Be prepared to design real-time leaderboards and scoring systems"]
}



INDIAN_COMPANIES["google_india"] = {
    "name": "Google India",
    "full_name": "Google LLC (India Office)",
    "icon": "\U0001f535",
    "color": "#4285F4",
    "package": "15 LPA (SDE-1) / 30+ LPA (SDE-2)",
    "eligibility": "70% aggregate, CS/IT preferred",
    "exam_pattern": "Google Online Coding Test + Interviews",
    "interview_rounds": ["Online Coding Test (2 rounds, 45 min each)", "Technical Phone Screen (45 min)", "On-site Interview (4-5 rounds)", "Googliness / Googleyness (1)"],
    "focus_areas": ["DSA", "Algorithms", "System Design", "Problem Solving"],
    "google_coding_test": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Coding", "questions": 2, "time_minutes": 45, "types": ["Problem Solving"], "difficulty": "hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Two Pointers", "Recursion", "Bit Manipulation"]},
            {"name": "Coding (Round 2)", "questions": 2, "time_minutes": 45, "types": ["Problem Solving"], "difficulty": "hard", "topics": ["Advanced DP", "Graph Algorithms", "Trees", "Sorting", "Searching", "Math", "Design"]}
        ]
    },
    "coding_patterns": ["Find median from data stream", "Implement LRU Cache with O(1) operations", "Find the longest increasing subsequence", "Serialize and deserialize binary tree", "Find the minimum window substring", "Implement a Trie with autocomplete", "Find the maximum path sum in binary tree", "Find the number of islands in grid", "Implement wildcard pattern matching", "Find the shortest path in a graph with weights"],
    "hr_questions": ["Tell me about yourself", "Why Google?", "Describe a time you showed leadership", "How do you handle ambiguity in projects?", "Tell me about a project you're most proud of", "How do you handle conflict in a team?", "Where do you see yourself in 5 years?", "How do you learn new technologies?", "What does 'Googleyness' mean to you?", "What questions do you have for us?"],
    "tips": ["Practice LeetCode Hard problems \u2014 Google asks medium to hard", "Focus on optimal solutions with best time/space complexity", "System design is crucial for L4+ levels", "Know about Google's products and infrastructure", "Google values problem-solving methodology, not just the answer", "Prepare behavioral answers using STAR format"]
}

INDIAN_COMPANIES["microsoft_india"] = {
    "name": "Microsoft India",
    "full_name": "Microsoft Corporation (India Office)",
    "icon": "\U0001f7e6",
    "color": "#00A4EF",
    "package": "15 LPA (SDE-1) / 30+ LPA (SDE-2)",
    "eligibility": "70% aggregate, CS/IT preferred",
    "exam_pattern": "Microsoft Online Assessment + Interviews",
    "interview_rounds": ["Online Coding Test (2 rounds)", "Technical Phone Screen (45 min)", "On-site Interview (4-5 rounds)", "As Appropriate (AA) Round (1)"],
    "focus_areas": ["DSA", "Algorithms", "System Design", "Problem Solving"],
    "microsoft_aoa_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Coding", "questions": 2, "time_minutes": 45, "types": ["Problem Solving"], "difficulty": "hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Recursion"]},
            {"name": "Coding (Round 2)", "questions": 2, "time_minutes": 45, "types": ["Problem Solving"], "difficulty": "hard", "topics": ["Advanced DP", "Graph Algorithms", "Trees", "Design", "Math", "Bit Manipulation"]}
        ]
    },
    "coding_patterns": ["Find the kth smallest element in sorted matrix", "Implement a task scheduler with cooldown", "Find the alien dictionary order", "Serialize and deserialize a binary tree", "Find the maximum XOR of two numbers in array", "Implement a spell checker", "Find the shortest path visiting all nodes", "Find the number of valid parentheses expressions", "Implement range module (range tracking)", "Find the longest increasing path in matrix"],
    "hr_questions": ["Tell me about yourself", "Why Microsoft?", "Describe a time you influenced without authority", "How do you handle disagreements?", "Tell me about a challenging technical problem you solved", "How do you prioritize tasks?", "Where do you see yourself in 5 years?", "How do you handle ambiguity?", "What does growth mindset mean to you?", "What questions do you have for us?"],
    "tips": ["Microsoft values clean code and optimal solutions", "Practice LeetCode Medium-Hard problems consistently", "Know about Microsoft Azure, VS Code, GitHub products", "System design is important for SDE-2+ roles", "Microsoft values collaboration and growth mindset", "Prepare behavioral questions using STAR format"]
}

INDIAN_COMPANIES["amazon_india"] = {
    "name": "Amazon India",
    "full_name": "Amazon Development Centre (India)",
    "icon": "\U0001f4e6",
    "color": "#FF9900",
    "package": "15 LPA (SDE-1) / 28 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Amazon Online Assessment (OA) + Interviews",
    "interview_rounds": ["Online Assessment (OA1: 90 min + OA2: 90 min)", "Technical Phone Screen (45 min)", "On-site Interview (4-5 rounds)", "Bar Raiser Round (1)"],
    "focus_areas": ["DSA", "Leadership Principles", "System Design", "Problem Solving"],
    "amazon_oa_pattern": {
        "total_time_minutes": 180,
        "sections": [
            {"name": "OA1 - Debugging", "questions": 7, "time_minutes": 20, "types": ["Code Debugging", "Output Prediction"], "difficulty": "medium", "topics": ["Java/Python/C++ Debugging", "OOP", "Exception Handling", "Logic Errors", "Output Tracing"]},
            {"name": "OA1 - Data Structures", "questions": 2, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "HashMaps", "Sorting", "Searching", "Two Pointers"]},
            {"name": "OA2 - Coding", "questions": 2, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "hard", "topics": ["Arrays", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Stacks", "Queues", "Sliding Window"]},
            {"name": "Work Style Assessment", "questions": 25, "time_minutes": 20, "types": ["Behavioral"], "difficulty": "easy", "topics": ["Situational Judgement", "Work Preferences", "Leadership Principles", "Team Collaboration"]}
        ]
    },
    "coding_patterns": ["Find the minimum window substring", "Implement a task scheduler", "Find the number of recent calls", "Implement LFU Cache", "Find the maximum binary tree from preorder traversal", "Design a search autocomplete system", "Find the minimum cost to make array equal", "Implement a stream of integers", "Find the maximum height of binary tree after cutting", "Design a parking lot system"],
    "hr_questions": ["Tell me about yourself", "Why Amazon?", "Describe a time you simplified a process", "Tell me about a time you made a decision with incomplete data", "How do you handle customer obsession?", "Where do you see yourself in 5 years?", "Tell me about a time you disagreed with a decision", "How do you handle multiple priorities?", "Describe a time you delivered results under tight deadlines", "What questions do you have for us?"],
    "tips": ["Know Amazon's 16 Leadership Principles \u2014 critical for behavioral", "Practice LeetCode Medium-Hard \u2014 Amazon OA is challenging", "Amazon values customer obsession \u2014 mention it in behavioral", "System design is important for SDE-2+ roles", "Practice debugging \u2014 OA1 has a debugging section", "Bar Raiser round is a culture fit assessment \u2014 be genuine"]
}

INDIAN_COMPANIES["goldman_sachs"] = {
    "name": "Goldman Sachs",
    "full_name": "Goldman Sachs Services India",
    "icon": "\U0001f3e6",
    "color": "#6BA4C7",
    "package": "12 LPA (Analyst) / 22 LPA (Sr. Analyst)",
    "eligibility": "70% aggregate, CS/IT/ECE preferred",
    "exam_pattern": "Goldman Sachs Online Assessment + Interviews",
    "interview_rounds": ["Online Assessment (120 min)", "Technical Phone Screen (45 min)", "On-site Interview (3-4 rounds)", "HR Interview (1)"],
    "focus_areas": ["DSA", "Algorithms", "Mathematics", "System Design"],
    "gs_assessment_pattern": {
        "total_time_minutes": 120,
        "sections": [
            {"name": "Aptitude & Math", "questions": 20, "time_minutes": 25, "types": ["Quantitative", "Logical"], "difficulty": "medium-hard", "topics": ["Probability", "Combinatorics", "Statistics", "Number Theory", "Puzzles", "Logical Reasoning", "Data Interpretation"]},
            {"name": "Coding", "questions": 2, "time_minutes": 60, "types": ["Problem Solving"], "difficulty": "hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Math", "Sorting", "Searching"]},
            {"name": "Computer Science", "questions": 15, "time_minutes": 35, "types": ["MCQ"], "difficulty": "medium-hard", "topics": ["OS", "Networking", "DBMS", "OOP", "Data Structures", "Algorithms", "Computer Architecture"]}
        ]
    },
    "coding_patterns": ["Find the maximum profit from stock prices with K transactions", "Design a real-time market data feed system", "Find the probability of winning a game", "Implement a portfolio management system", "Find the shortest path in a weighted graph", "Design a risk calculation engine", "Find the number of ways to make change", "Implement a trading order matching engine", "Find the maximum subarray sum with at most K elements", "Design a financial time series analysis system"],
    "hr_questions": ["Tell me about yourself", "Why Goldman Sachs?", "What do you know about Goldman Sachs' tech division?", "Describe a complex algorithm you implemented", "How do you handle working under pressure?", "Where do you see yourself in 5 years?", "What is your understanding of financial markets?", "How do you handle ambiguity in projects?", "Tell me about a time you showed analytical thinking", "What questions do you have for us?"],
    "tips": ["Goldman Sachs values quantitative and mathematical skills", "Practice probability, combinatorics, and math-based problems", "Know about financial markets (stocks, bonds, derivatives)", "DSA problems are typically medium-hard difficulty", "GS values analytical thinking and attention to detail", "Technical interview covers CS fundamentals and system design"]
}

INDIAN_COMPANIES["jp_morgan"] = {
    "name": "JP Morgan",
    "full_name": "JP Morgan Chase & Co. (India Office)",
    "icon": "\U0001f3e6",
    "color": "#003D6B",
    "package": "10 LPA (Analyst) / 20 LPA (Associate)",
    "eligibility": "65% aggregate, CS/IT/ECE preferred",
    "exam_pattern": "JPMC Engineering Assessment + Interviews",
    "interview_rounds": ["Online Assessment (90 min)", "Technical Phone Screen (45 min)", "On-site Interview (3-4 rounds)", "HR Interview (1)"],
    "focus_areas": ["DSA", "Algorithms", "System Design", "Fintech"],
    "jpmc_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Quantitative Aptitude", "questions": 20, "time_minutes": 25, "types": ["Quantitative", "Logical"], "difficulty": "medium-hard", "topics": ["Probability", "Statistics", "Combinatorics", "Number Series", "Data Interpretation", "Puzzles", "Logical Reasoning"]},
            {"name": "Coding", "questions": 2, "time_minutes": 50, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Math", "Bit Manipulation"]},
            {"name": "CS Fundamentals", "questions": 15, "time_minutes": 15, "types": ["MCQ"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Data Structures", "Algorithms"]}
        ]
    },
    "coding_patterns": ["Design a stock trading system", "Find the maximum portfolio return within risk limit", "Implement a real-time transaction processing system", "Find the optimal asset allocation strategy", "Design a fraud detection system", "Implement a basic derivatives pricing model", "Find the maximum profit from multiple buy-sell pairs", "Design a market risk calculation engine", "Find the shortest path for fund transfer between banks", "Implement a compliance checking system"],
    "hr_questions": ["Tell me about yourself", "Why JP Morgan?", "What do you know about JP Morgan's technology division?", "Describe a complex technical problem you solved", "How do you handle high-pressure situations?", "Where do you see yourself in 5 years?", "What do you know about financial technology?", "How do you ensure code quality in financial systems?", "Tell me about a time you showed attention to detail", "What questions do you have for us?"],
    "tips": ["JP Morgan values quantitative skills and analytical thinking", "Practice math-based coding problems", "Know about financial systems (trading, risk, compliance)", "DSA problems are medium to hard difficulty", "JP Morgan values attention to detail and accuracy", "Be prepared for questions on system design for financial systems"]
}



INDIAN_COMPANIES["drdo"] = {
    "name": "DRDO",
    "full_name": "Defence Research and Development Organisation",
    "icon": "\U0001f6e1\ufe0f",
    "color": "#1B365D",
    "package": "5.5 LPA (Scientist B) / 8 LPA (with allowances)",
    "eligibility": "GATE score required, 65% aggregate, CS/IT/ECE",
    "exam_pattern": "GATE + DRDO Scientist B Selection",
    "interview_rounds": ["GATE Score Shortlisting", "Written Test / Interview (if needed)", "Technical Interview (1-2 rounds)", "Personal Interview (1)"],
    "focus_areas": ["GATE Topics", "Core CS", "Technical Knowledge", "Problem Solving"],
    "drdo_gate_pattern": {
        "total_time_minutes": 180,
        "sections": [
            {"name": "General Aptitude", "questions": 10, "time_minutes": 15, "types": ["Verbal", "Numerical"], "difficulty": "easy-medium", "topics": ["Grammar", "Vocabulary", "Numerical Ability", "Data Interpretation", "Logical Reasoning"]},
            {"name": "Core CS (GATE)", "questions": 55, "time_minutes": 165, "types": ["MCQ", "NAT"], "difficulty": "hard", "topics": ["DSA", "OS", "DBMS", "Computer Networks", "Theory of Computation", "Compiler Design", "Digital Logic", "Computer Architecture", "Algorithms", "Operating Systems"]}
        ]
    },
    "coding_patterns": ["Implement BFS and DFS for graph traversal", "Solve GATE-style DSA problems on arrays and strings", "Find shortest path using Dijkstra's algorithm", "Implement a basic compiler parser", "Solve problems on dynamic programming (GATE pattern)", "Find the critical path in a directed graph", "Implement pattern matching algorithms", "Solve problems on trees and binary search trees", "Find the minimum spanning tree using Kruskal's/Prim's", "Implement hash table with collision handling"],
    "hr_questions": ["Tell me about yourself", "Why DRDO?", "What do you know about DRDO's research areas?", "Describe a technical project you worked on", "How do you handle working under security clearance?", "Where do you see yourself in 5 years?", "What is your contribution to defense technology?", "How do you handle working in teams?", "What motivates you to work in defense research?", "What questions do you have for us?"],
    "tips": ["GATE score is the primary selection criterion \u2014 score above 650", "Focus on core CS subjects (DSA, OS, DBMS, Networks)", "DRDO values technical depth and research aptitude", "Prepare for questions on defense technology and current affairs", "Know about DRDO's major projects (missiles, radars, etc.)", "Security clearance is mandatory \u2014 be prepared for thorough background check"]
}

INDIAN_COMPANIES["isro"] = {
    "name": "ISRO",
    "full_name": "Indian Space Research Organisation",
    "icon": "\U0001f680",
    "color": "#0B3D91",
    "package": "5.5 LPA (Scientist/Engineer SC) / 8 LPA (with allowances)",
    "eligibility": "GATE score + ISRO exam, 65% aggregate, CS/IT/ECE",
    "exam_pattern": "GATE + ISRO Scientist/Engineer Written Test",
    "interview_rounds": ["GATE Score Shortlisting", "ISRO Written Test (if applicable)", "Technical Interview (2 rounds)", "Personal Interview (1)"],
    "focus_areas": ["GATE Topics", "Core CS", "Technical Knowledge", "Space Technology"],
    "isro_exam_pattern": {
        "total_time_minutes": 150,
        "sections": [
            {"name": "General Aptitude", "questions": 10, "time_minutes": 15, "types": ["Verbal", "Numerical"], "difficulty": "easy-medium", "topics": ["Grammar", "Vocabulary", "Numerical Ability", "Data Interpretation", "Logical Reasoning"]},
            {"name": "Core CS (GATE-level)", "questions": 80, "time_minutes": 135, "types": ["MCQ", "NAT", "MSQ"], "difficulty": "hard", "topics": ["DSA", "OS", "DBMS", "Computer Networks", "Theory of Computation", "Compiler Design", "Digital Logic", "Computer Architecture", "Algorithms", "Programming"]}
        ]
    },
    "coding_patterns": ["Implement real-time data processing algorithms", "Solve GATE-style algorithm analysis problems", "Find the optimal resource allocation in satellite communication", "Implement error detection and correction codes", "Solve problems on computational geometry", "Find the critical path in mission planning", "Implement image processing algorithms", "Solve problems on signal processing", "Find the minimum spanning tree for network design", "Implement scheduling algorithms for real-time systems"],
    "hr_questions": ["Tell me about yourself", "Why ISRO?", "What do you know about ISRO's recent missions?", "Describe a technical project you worked on", "How do you handle working on critical missions?", "Where do you see yourself in 5 years?", "What is your understanding of space technology?", "How do you handle working under pressure?", "What motivates you to work in space research?", "What questions do you have for us?"],
    "tips": ["GATE score is critical \u2014 aim for AIR under 500", "Focus on core CS subjects at GATE level", "ISRO values technical excellence and dedication", "Know about ISRO's missions (Chandrayaan, Mangalyaan, Gaganyaan)", "Prepare for questions on space technology and applications", "Be prepared for a rigorous technical interview"]
}

INDIAN_COMPANIES["bel"] = {
    "name": "BEL",
    "full_name": "Bharat Electronics Limited",
    "icon": "\U0001f4e1",
    "color": "#006B3F",
    "package": "5 LPA (Engineer) / 7 LPA (Senior Engineer)",
    "eligibility": "GATE score, 60% aggregate, CS/IT/ECE",
    "exam_pattern": "GATE + BEL Selection Process",
    "interview_rounds": ["GATE Score Shortlisting", "Written Test (if needed)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["Electronics", "Communication", "CS Fundamentals", "Defense Tech"],
    "bel_gate_pattern": {
        "total_time_minutes": 150,
        "sections": [
            {"name": "General Aptitude", "questions": 10, "time_minutes": 15, "types": ["Verbal", "Numerical"], "difficulty": "easy-medium", "topics": ["Grammar", "Vocabulary", "Numerical Ability", "Logical Reasoning"]},
            {"name": "Core CS/ECE (GATE)", "questions": 55, "time_minutes": 135, "types": ["MCQ", "NAT"], "difficulty": "hard", "topics": ["DSA", "OS", "DBMS", "Computer Networks", "Digital Logic", "Signals & Systems", "Electronics", "Communication Systems"]}
        ]
    },
    "coding_patterns": ["Implement signal processing algorithms", "Solve GATE-level DSA problems", "Find the optimal communication protocol", "Implement error handling in embedded systems", "Solve problems on digital logic and circuits", "Find the shortest path in radar systems", "Implement encryption/decryption algorithms", "Solve problems on real-time systems", "Find the minimum latency in communication", "Implement data compression algorithms"],
    "hr_questions": ["Tell me about yourself", "Why BEL?", "What do you know about BEL's products?", "Describe a technical project you worked on", "How do you handle working in defense sector?", "Where do you see yourself in 5 years?", "What is your understanding of electronics in defense?", "How do you handle working under deadlines?", "What motivates you to work in defense electronics?", "What questions do you have for us?"],
    "tips": ["GATE score is the primary selection criterion", "Focus on electronics, communication, and CS fundamentals", "Know about BEL's products (radars, communication systems)", "BEL values technical expertise and dedication", "Prepare for questions on defense electronics", "Be thorough with digital logic and embedded systems"]
}

INDIAN_COMPANIES["bhel"] = {
    "name": "BHEL",
    "full_name": "Bharat Heavy Electricals Limited",
    "icon": "\u26a1",
    "color": "#00529B",
    "package": "5 LPA (Engineer Trainee) / 7 LPA (with allowances)",
    "eligibility": "GATE score, 60% aggregate, eligible branches",
    "exam_pattern": "GATE + BHEL Selection Process",
    "interview_rounds": ["GATE Score Shortlisting", "Group Discussion (if needed)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["GATE Topics", "Core Engineering", "Technical Knowledge", "Power Systems"],
    "bhel_gate_pattern": {
        "total_time_minutes": 150,
        "sections": [
            {"name": "General Aptitude", "questions": 10, "time_minutes": 15, "types": ["Verbal", "Numerical"], "difficulty": "easy-medium", "topics": ["Grammar", "Vocabulary", "Numerical Ability", "Logical Reasoning"]},
            {"name": "Core Engineering (GATE)", "questions": 55, "time_minutes": 135, "types": ["MCQ", "NAT"], "difficulty": "hard", "topics": ["Power Systems", "Control Systems", "Electrical Machines", "Power Electronics", "Signals", "Circuits", "EM Theory", "Digital Electronics"]}
        ]
    },
    "coding_patterns": ["Implement power system simulation algorithms", "Solve GATE-level circuit analysis problems", "Find optimal load flow in power systems", "Implement control system transfer functions", "Solve problems on electrical machines", "Find the stability margin of a power system", "Implement SCADA data processing", "Solve problems on power electronics converters", "Find the optimal generator scheduling", "Implement protection relay algorithms"],
    "hr_questions": ["Tell me about yourself", "Why BHEL?", "What do you know about BHEL's products?", "Describe a project you worked on", "How do you handle working in heavy industry?", "Where do you see yourself in 5 years?", "What is your understanding of power systems?", "How do you handle working under pressure?", "What motivates you to work in power equipment?", "What questions do you have for us?"],
    "tips": ["GATE score is the primary criterion \u2014 score well in your branch", "Focus on core electrical/electronics engineering subjects", "Know about BHEL's products (turbines, transformers, motors)", "BHEL values technical knowledge and dedication", "Prepare for questions on power systems and heavy electricals", "Be prepared for group discussion if shortlisted"]
}

INDIAN_COMPANIES["ntpc"] = {
    "name": "NTPC",
    "full_name": "NTPC Limited (National Thermal Power Corporation)",
    "icon": "\u26a1",
    "color": "#00529B",
    "package": "5 LPA (Executive Trainee) / 7 LPA (with allowances)",
    "eligibility": "GATE score, 60% aggregate, eligible branches",
    "exam_pattern": "GATE + NTPC Selection Process",
    "interview_rounds": ["GATE Score Shortlisting", "Group Discussion (if needed)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["GATE Topics", "Power Engineering", "Technical Knowledge", "Energy Systems"],
    "ntpc_gate_pattern": {
        "total_time_minutes": 150,
        "sections": [
            {"name": "General Aptitude", "questions": 10, "time_minutes": 15, "types": ["Verbal", "Numerical"], "difficulty": "easy-medium", "topics": ["Grammar", "Vocabulary", "Numerical Ability", "Logical Reasoning"]},
            {"name": "Core Engineering (GATE)", "questions": 55, "time_minutes": 135, "types": ["MCQ", "NAT"], "difficulty": "hard", "topics": ["Power Systems", "Thermodynamics", "Heat Transfer", "Fluid Mechanics", "Power Plant Engineering", "Renewable Energy", "Control Systems"]}
        ]
    },
    "coding_patterns": ["Implement power generation scheduling algorithms", "Solve GATE-level thermal engineering problems", "Find optimal coal blending strategy", "Implement turbine performance monitoring", "Solve problems on heat exchanger design", "Find the efficiency of combined cycle plants", "Implement emission monitoring systems", "Solve problems on renewable energy integration", "Find the optimal maintenance schedule", "Implement grid stability monitoring"],
    "hr_questions": ["Tell me about yourself", "Why NTPC?", "What do you know about NTPC's power generation capacity?", "Describe a project you worked on", "How do you handle working in power plants?", "Where do you see yourself in 5 years?", "What is your understanding of energy sector?", "How do you handle working in shifts?", "What motivates you to work in power generation?", "What questions do you have for us?"],
    "tips": ["GATE score is the primary selection criterion", "Focus on power systems, thermodynamics, and power plant engineering", "Know about NTPC's capacity and renewable energy plans", "NTPC values technical knowledge and commitment to energy sector", "Prepare for questions on energy policy and sustainability", "Be prepared for group discussion on current energy topics"]
}

INDIAN_COMPANIES["sail"] = {
    "name": "SAIL",
    "full_name": "Steel Authority of India Limited",
    "icon": "\U0001f3ed",
    "color": "#C8102E",
    "package": "5 LPA (Management Trainee) / 7 LPA (with allowances)",
    "eligibility": "GATE score, 60% aggregate, eligible branches",
    "exam_pattern": "GATE + SAIL Selection Process",
    "interview_rounds": ["GATE Score Shortlisting", "Group Discussion (if needed)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["GATE Topics", "Core Engineering", "Technical Knowledge", "Steel Technology"],
    "sail_gate_pattern": {
        "total_time_minutes": 150,
        "sections": [
            {"name": "General Aptitude", "questions": 10, "time_minutes": 15, "types": ["Verbal", "Numerical"], "difficulty": "easy-medium", "topics": ["Grammar", "Vocabulary", "Numerical Ability", "Logical Reasoning"]},
            {"name": "Core Engineering (GATE)", "questions": 55, "time_minutes": 135, "types": ["MCQ", "NAT"], "difficulty": "hard", "topics": ["Thermodynamics", "Fluid Mechanics", "Heat Transfer", "Materials Science", "Manufacturing", "Industrial Engineering"]}
        ]
    },
    "coding_patterns": ["Implement steel production scheduling algorithms", "Solve GATE-level materials science problems", "Find optimal blast furnace operation parameters", "Implement quality control monitoring systems", "Solve problems on heat treatment processes", "Find the optimal rolling schedule", "Implement inventory management for raw materials", "Solve problems on steel making processes", "Find the cost optimization for production", "Implement supply chain optimization"],
    "hr_questions": ["Tell me about yourself", "Why SAIL?", "What do you know about SAIL's steel plants?", "Describe a project you worked on", "How do you handle working in heavy industry?", "Where do you see yourself in 5 years?", "What is your understanding of steel manufacturing?", "How do you handle working under pressure?", "What motivates you to work in steel industry?", "What questions do you have for us?"],
    "tips": ["GATE score is the primary selection criterion", "Focus on core engineering subjects relevant to your branch", "Know about SAIL's steel plants and production capacity", "SAIL values technical knowledge and dedication", "Prepare for questions on steel manufacturing processes", "Be prepared for group discussion on industry topics"]
}

INDIAN_COMPANIES["iocl"] = {
    "name": "IOCL",
    "full_name": "Indian Oil Corporation Limited",
    "icon": "\U0001f6e2\ufe0f",
    "color": "#FF6600",
    "package": "5 LPA (Engineer/Officer) / 7 LPA (with allowances)",
    "eligibility": "GATE score, 60% aggregate, eligible branches",
    "exam_pattern": "GATE + IOCL Selection Process",
    "interview_rounds": ["GATE Score Shortlisting", "Group Discussion (if needed)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["GATE Topics", "Core Engineering", "Petrochemicals", "Technical Knowledge"],
    "iocl_gate_pattern": {
        "total_time_minutes": 150,
        "sections": [
            {"name": "General Aptitude", "questions": 10, "time_minutes": 15, "types": ["Verbal", "Numerical"], "difficulty": "easy-medium", "topics": ["Grammar", "Vocabulary", "Numerical Ability", "Logical Reasoning"]},
            {"name": "Core Engineering (GATE)", "questions": 55, "time_minutes": 135, "types": ["MCQ", "NAT"], "difficulty": "hard", "topics": ["Thermodynamics", "Fluid Mechanics", "Heat Transfer", "Mass Transfer", "Chemical Engineering", "Process Control"]}
        ]
    },
    "coding_patterns": ["Implement refinery scheduling algorithms", "Solve GATE-level process engineering problems", "Find optimal crude oil blending ratios", "Implement pipeline monitoring systems", "Solve problems on distillation column design", "Find the optimal refinery throughput", "Implement quality control for petroleum products", "Solve problems on process optimization", "Find the cost minimization for operations", "Implement inventory management for refineries"],
    "hr_questions": ["Tell me about yourself", "Why IOCL?", "What do you know about IOCL's refineries?", "Describe a project you worked on", "How do you handle working in oil and gas?", "Where do you see yourself in 5 years?", "What is your understanding of petroleum industry?", "How do you handle working under pressure?", "What motivates you to work in energy sector?", "What questions do you have for us?"],
    "tips": ["GATE score is the primary selection criterion", "Focus on chemical/process engineering subjects", "Know about IOCL's refineries and operations", "IOCL values technical knowledge and safety awareness", "Prepare for questions on petroleum industry and regulations", "Be prepared for group discussion on energy sector topics"]
}

INDIAN_COMPANIES["gail"] = {
    "name": "GAIL",
    "full_name": "GAIL (India) Limited",
    "icon": "\U0001f525",
    "color": "#006B3F",
    "package": "5 LPA (Executive Trainee) / 7 LPA (with allowances)",
    "eligibility": "GATE score, 60% aggregate, eligible branches",
    "exam_pattern": "GATE + GAIL Selection Process",
    "interview_rounds": ["GATE Score Shortlisting", "Group Discussion (if needed)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["GATE Topics", "Core Engineering", "Gas Processing", "Technical Knowledge"],
    "gail_gate_pattern": {
        "total_time_minutes": 150,
        "sections": [
            {"name": "General Aptitude", "questions": 10, "time_minutes": 15, "types": ["Verbal", "Numerical"], "difficulty": "easy-medium", "topics": ["Grammar", "Vocabulary", "Numerical Ability", "Logical Reasoning"]},
            {"name": "Core Engineering (GATE)", "questions": 55, "time_minutes": 135, "types": ["MCQ", "NAT"], "difficulty": "hard", "topics": ["Thermodynamics", "Fluid Mechanics", "Heat Transfer", "Mass Transfer", "Chemical Process", "Pipeline Engineering"]}
        ]
    },
    "coding_patterns": ["Implement gas pipeline flow optimization", "Solve GATE-level process engineering problems", "Find optimal gas processing parameters", "Implement pipeline leak detection systems", "Solve problems on gas compression and distribution", "Find the optimal LPG bottling schedule", "Implement quality control for natural gas", "Solve problems on petrochemical processes", "Find the cost minimization for gas distribution", "Implement supply chain management for gas products"],
    "hr_questions": ["Tell me about yourself", "Why GAIL?", "What do you know about GAIL's pipeline network?", "Describe a project you worked on", "How do you handle working in gas industry?", "Where do you see yourself in 5 years?", "What is your understanding of natural gas business?", "How do you handle working under pressure?", "What motivates you to work in energy sector?", "What questions do you have for us?"],
    "tips": ["GATE score is the primary selection criterion", "Focus on chemical/process engineering subjects", "Know about GAIL's pipeline network and operations", "GAIL values technical knowledge and safety", "Prepare for questions on natural gas and petrochemicals", "Be prepared for group discussion on energy sector topics"]
}



INDIAN_COMPANIES["cars24"] = {
    "name": "Cars24",
    "full_name": "Cars24 Services Private Limited",
    "icon": "\U0001f697",
    "color": "#1A1A1A",
    "package": "8 LPA (SDE-1) / 14 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Cars24 Online Coding Test + Interviews",
    "interview_rounds": ["Online Coding Test (60 min)", "Technical Interview (2-3 rounds)", "Hiring Manager Interview (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Problem Solving"],
    "cars24_coding_test": {
        "total_time_minutes": 60,
        "sections": [
            {"name": "Coding", "questions": 3, "time_minutes": 60, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing"]}
        ]
    },
    "coding_patterns": ["Design a used car pricing engine", "Find the best car deal within budget", "Implement a vehicle inspection scoring system", "Design a car marketplace search system", "Find the optimal pricing strategy for cars", "Implement a car condition assessment algorithm", "Design a loan EMI calculator", "Find the best trade-in value for a car", "Implement a car recommendation system", "Design a service history tracking system"],
    "hr_questions": ["Tell me about yourself", "Why Cars24?", "What do you know about Cars24's business model?", "Describe a project you worked on", "How do you handle fast-paced startup environment?", "Where do you see yourself in 3 years?", "What is your approach to building products?", "How do you handle ambiguity?", "What do you know about the used car market?", "What questions do you have for us?"],
    "tips": ["Cars24 focuses on practical problem-solving", "Know about Cars24's business model (used car marketplace)", "Practice medium DSA problems", "Understand e-commerce and marketplace concepts", "Cars24 values speed and impact", "Be prepared to design systems for marketplace and pricing"]
}

INDIAN_COMPANIES["meesho"] = {
    "name": "Meesho",
    "full_name": "Meesho (Meesho Inc.)",
    "icon": "\U0001f6cd\ufe0f",
    "color": "#F43397",
    "package": "10 LPA (SDE-1) / 18 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Meesho Online Coding Test + Interviews",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Problem Solving"],
    "meesho_coding_test": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "MCQ", "questions": 15, "time_minutes": 15, "types": ["CS Fundamentals"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Data Structures", "Algorithms"]},
            {"name": "Coding", "questions": 3, "time_minutes": 75, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Sliding Window"]}
        ]
    },
    "coding_patterns": ["Design a social commerce platform", "Implement a product recommendation engine", "Find the trending products in real-time", "Design a supplier onboarding system", "Implement a real-time inventory tracking system", "Find the optimal product ranking for search", "Design a commission calculation engine", "Implement a live order tracking system", "Find the best deals using price comparison", "Design a micro-influencer recommendation system"],
    "hr_questions": ["Tell me about yourself", "Why Meesho?", "What do you know about Meesho's social commerce model?", "Describe a feature you'd add to Meesho", "How do you handle scaling for millions of users?", "Where do you see yourself in 3 years?", "What is your approach to product development?", "How do you handle ambiguity in a startup?", "What do you think about social commerce in India?", "What questions do you have for us?"],
    "tips": ["Meesho focuses on system design and DSA", "Know about social commerce and marketplace dynamics", "Practice medium-hard DSA problems", "Understand scaling for Tier 2/3 city users", "Meesho values speed and shipping fast", "Be prepared to design systems for high scale"]
}

INDIAN_COMPANIES["groww"] = {
    "name": "Groww",
    "full_name": "Groww (NextBillion Technology)",
    "icon": "\U0001f4c8",
    "color": "#00B386",
    "package": "10 LPA (SDE-1) / 16 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Groww Engineering Assessment + Interviews",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Fintech"],
    "groww_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "MCQ", "questions": 15, "time_minutes": 15, "types": ["CS Fundamentals"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Data Structures", "Algorithms"]},
            {"name": "Coding", "questions": 3, "time_minutes": 75, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing"]}
        ]
    },
    "coding_patterns": ["Design a mutual fund portfolio tracker", "Implement a stock price streaming system", "Find the optimal SIP investment strategy", "Design a real-time market data feed", "Implement a portfolio rebalancing algorithm", "Find the best investment recommendations", "Design a KYC verification system", "Implement a real-time profit/loss calculator", "Find the risk assessment algorithm", "Design a notification system for price alerts"],
    "hr_questions": ["Tell me about yourself", "Why Groww?", "What do you know about Groww's investment platform?", "Describe a system you designed for fintech", "How do you handle financial data security?", "Where do you see yourself in 3 years?", "What is your approach to building financial products?", "How do you handle regulatory compliance?", "What do you know about investment platforms?", "What questions do you have for us?"],
    "tips": ["Groww focuses on system design and fintech domain knowledge", "Know about mutual funds, SIPs, and investment platforms", "Practice medium-hard DSA problems", "Understand financial regulations and compliance", "Groww values engineering excellence and user trust", "Be prepared to design secure and scalable fintech systems"]
}

INDIAN_COMPANIES["cred"] = {
    "name": "CRED",
    "full_name": "CRED (Dreamplug Technologies)",
    "icon": "\U0001f48e",
    "color": "#1B1B1B",
    "package": "12 LPA (SDE-1) / 20 LPA (SDE-2)",
    "eligibility": "70% aggregate, CS/IT preferred",
    "exam_pattern": "CRED Engineering Assessment + Interviews",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Fintech", "UI/UX"],
    "cred_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "MCQ", "questions": 15, "time_minutes": 15, "types": ["CS Fundamentals"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Data Structures", "Algorithms"]},
            {"name": "Coding", "questions": 3, "time_minutes": 75, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Two Pointers"]}
        ]
    },
    "coding_patterns": ["Design a credit score tracking system", "Implement a bill payment processing engine", "Find the optimal reward distribution algorithm", "Design a real-time credit card bill tracker", "Implement a payment gateway with retries", "Find the best credit card recommendation", "Design a membership rewards system", "Implement a real-time notification engine", "Find the optimal cashback distribution", "Design a financial analytics dashboard"],
    "hr_questions": ["Tell me about yourself", "Why CRED?", "What do you know about CRED's premium membership model?", "Describe a system you designed for fintech", "How do you handle high-value transactions?", "Where do you see yourself in 3 years?", "What is your approach to building premium products?", "How do you ensure payment security?", "What do you know about credit card ecosystem?", "What questions do you have for us?"],
    "tips": ["CRED expects high engineering standards and design thinking", "Know about credit cards, payments, and fintech", "Practice medium-hard DSA problems", "CRED values elegant design and user experience", "Understand payment systems and security", "Be prepared to design systems with high reliability"]
}

INDIAN_COMPANIES["urban_company"] = {
    "name": "Urban Company",
    "full_name": "Urban Company (formerly UrbanClap)",
    "icon": "\U0001f527",
    "color": "#0E4DA4",
    "package": "8 LPA (SDE-1) / 14 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "Urban Company Online Coding Test + Interviews",
    "interview_rounds": ["Online Coding Test (60 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Marketplace"],
    "uc_coding_test": {
        "total_time_minutes": 60,
        "sections": [
            {"name": "Coding", "questions": 3, "time_minutes": 60, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing"]}
        ]
    },
    "coding_patterns": ["Design a service matching algorithm", "Implement a real-time booking system", "Find the optimal service provider ranking", "Design a dynamic pricing engine for services", "Implement a live tracking system for service providers", "Find the best service provider for a location", "Design a review and rating system", "Implement a scheduling system for appointments", "Find the optimal route for service providers", "Design a wallet and payment system"],
    "hr_questions": ["Tell me about yourself", "Why Urban Company?", "What do you know about Urban Company's marketplace model?", "Describe a feature you'd add to the app", "How do you handle on-demand services?", "Where do you see yourself in 3 years?", "What is your approach to building two-sided marketplaces?", "How do you handle quality assurance for services?", "What do you know about the home services industry?", "What questions do you have for us?"],
    "tips": ["Urban Company focuses on marketplace dynamics and system design", "Know about two-sided marketplace challenges (supply, demand, quality)", "Practice medium DSA problems", "Understand location-based services and real-time tracking", "Urban Company values customer experience and operations", "Be prepared to design systems for service marketplace"]
}

INDIAN_COMPANIES["sharechat"] = {
    "name": "ShareChat",
    "full_name": "ShareChat/Moj (Mohalla Tech)",
    "icon": "\U0001f3ac",
    "color": "#FF0000",
    "package": "10 LPA (SDE-1) / 18 LPA (SDE-2)",
    "eligibility": "65% aggregate, CS/IT preferred",
    "exam_pattern": "ShareChat Online Coding Test + Interviews",
    "interview_rounds": ["Online Coding Test (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Media/Content"],
    "sharechat_coding_test": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "MCQ", "questions": 15, "time_minutes": 15, "types": ["CS Fundamentals"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Data Structures", "Algorithms"]},
            {"name": "Coding", "questions": 3, "time_minutes": 75, "types": ["Problem Solving"], "difficulty": "medium-hard", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing", "Two Pointers"]}
        ]
    },
    "coding_patterns": ["Design a content feed ranking algorithm", "Implement a video recommendation system", "Find the trending hashtags in real-time", "Design a short video recommendation engine", "Implement a content moderation system", "Find the optimal content distribution strategy", "Design a notification delivery system", "Implement a real-time comment system", "Find the best content creators for a category", "Design a CDN for media content"],
    "hr_questions": ["Tell me about yourself", "Why ShareChat?", "What do you know about ShareChat's content platform?", "Describe a feature you'd add to Moj", "How do you handle content moderation at scale?", "Where do you see yourself in 3 years?", "What is your approach to building social features?", "How do you handle viral content spikes?", "What do you know about regional content platforms?", "What questions do you have for us?"],
    "tips": ["ShareChat focuses on system design for social/content platforms", "Know about content recommendation algorithms", "Practice medium-hard DSA problems", "Understand video processing and CDN concepts", "ShareChat values impact on Indian regional audiences", "Be prepared to design systems for real-time content delivery"]
}

# ============================================================
# BANKING
# ============================================================

INDIAN_COMPANIES["sbi"] = {
    "name": "SBI",
    "full_name": "State Bank of India",
    "icon": "\U0001f3e6",
    "color": "#2196F3",
    "package": "4 LPA (PO) / 8 LPA (with allowances)",
    "eligibility": "Graduate degree, 60% aggregate",
    "exam_pattern": "SBI PO Exam (Prelims + Mains + Interview)",
    "interview_rounds": ["SBI PO Prelims (60 min)", "SBI PO Mains (180 min)", "Group Exercise + Interview"],
    "focus_areas": ["Quantitative Aptitude", "Reasoning", "English", "General Awareness", "Descriptive"],
    "sbi_po_pattern": {
        "total_time_minutes": 180,
        "sections": [
            {"name": "Reasoning & Computer Aptitude", "questions": 45, "time_minutes": 60, "types": ["MCQ", "Puzzles"], "difficulty": "medium-hard", "topics": ["Puzzles", "Syllogisms", "Coding-Decoding", "Seating Arrangement", "Machine Input-Output", "Computer Fundamentals", "Networking", "MS Office"]},
            {"name": "Data Analysis & Interpretation", "questions": 35, "time_minutes": 45, "types": ["MCQ", "DI"], "difficulty": "medium-hard", "topics": ["Pie Charts", "Bar Graphs", "Tables", "Caselets", "Probability", "Statistics", "Ratio", "Percentages"]},
            {"name": "General/Economy/Banking Awareness", "questions": 40, "time_minutes": 35, "types": ["MCQ"], "difficulty": "medium", "topics": ["Current Affairs", "Banking Terms", "Economic Policies", "Financial Markets", "Government Schemes", "Awards & Honors"]},
            {"name": "English Language", "questions": 35, "time_minutes": 40, "types": ["MCQ"], "difficulty": "medium", "topics": ["Reading Comprehension", "Cloze Test", "Error Detection", "Sentence Rearrangement", "Vocabulary", "Grammar"]}
        ]
    },
    "coding_patterns": ["Reasoning puzzles on arrangement and sequencing", "Data interpretation with banking scenarios", "Quantitative problems on interest and profit/loss", "Syllogism and logical reasoning problems", "Coding-decoding patterns for banking exams", "Probability and permutation problems", "Number series and analogy problems", "Time and work problems in banking context", "Blood relations and direction sense puzzles", "Seating arrangement and scheduling problems"],
    "hr_questions": ["Tell me about yourself", "Why SBI?", "What do you know about banking sector in India?", "How do you handle customer service?", "Where do you see yourself in 5 years?", "What is your understanding of NPA?", "How do you handle stressful situations?", "What do you know about digital banking?", "What motivates you to work in banking?", "What questions do you have for us?"],
    "tips": ["SBI PO is highly competitive \u2014 prepare thoroughly for all sections", "Current affairs and banking awareness are crucial", "Practice data interpretation and reasoning puzzles daily", "Time management is key in prelims and mains", "Know about SBI's digital initiatives and recent developments", "Prepare well for the group exercise and interview round"]
}

INDIAN_COMPANIES["hdfc"] = {
    "name": "HDFC Bank",
    "full_name": "HDFC Bank Limited",
    "icon": "\U0001f3e6",
    "color": "#004B87",
    "package": "4 LPA (PO) / 7 LPA (with allowances)",
    "eligibility": "Graduate degree, 60% aggregate",
    "exam_pattern": "HDFC Bank Assessment + Interview",
    "interview_rounds": ["Online Aptitude Test (90 min)", "Group Discussion (1)", "Technical Interview (1)", "HR Interview (1)"],
    "focus_areas": ["Quantitative Aptitude", "Reasoning", "English", "Banking Knowledge"],
    "hdfc_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Quantitative Aptitude", "questions": 25, "time_minutes": 25, "types": ["Numerical"], "difficulty": "medium", "topics": ["Percentages", "Profit & Loss", "Time & Work", "Probability", "Data Interpretation", "Number Series", "Simplification"]},
            {"name": "Reasoning", "questions": 25, "time_minutes": 25, "types": ["Logical"], "difficulty": "medium", "topics": ["Puzzles", "Syllogisms", "Coding-Decoding", "Seating Arrangement", "Blood Relations", "Direction Sense", "Series"]},
            {"name": "English", "questions": 25, "time_minutes": 20, "types": ["Grammar", "Reading"], "difficulty": "medium", "topics": ["Reading Comprehension", "Grammar", "Vocabulary", "Cloze Test", "Error Detection", "Sentence Correction"]},
            {"name": "General Awareness", "questions": 15, "time_minutes": 20, "types": ["MCQ"], "difficulty": "medium", "topics": ["Current Affairs", "Banking Terms", "Economic Policies", "Financial News", "Awards & Honors"]}
        ]
    },
    "coding_patterns": ["Solve banking quantitative problems on interest", "Data interpretation for banking reports", "Reasoning puzzles on bank queue management", "Logical problems on transaction sequencing", "Probability problems in banking scenarios", "Time and work problems for branch operations", "Profit and loss calculations for banking", "Syllogism problems related to banking rules", "Coding-decoding for banking communication", "Seating arrangement for branch staff scheduling"],
    "hr_questions": ["Tell me about yourself", "Why HDFC Bank?", "What do you know about HDFC Bank's services?", "How do you handle customer complaints?", "Where do you see yourself in 5 years?", "What is your understanding of retail banking?", "How do you handle pressure in banking?", "What do you know about KYC and compliance?", "What motivates you to work in banking?", "What questions do you have for us?"],
    "tips": ["HDFC Bank values customer service orientation", "Know about banking products (loans, credit cards, accounts)", "Practice aptitude and reasoning daily", "Know about HDFC Bank's digital banking initiatives", "Prepare for group discussion on banking topics", "Be thorough with banking regulations and compliance"]
}

INDIAN_COMPANIES["icici"] = {
    "name": "ICICI Bank",
    "full_name": "ICICI Bank Limited",
    "icon": "\U0001f3e6",
    "color": "#F37920",
    "package": "4 LPA (PO) / 7 LPA (with allowances)",
    "eligibility": "Graduate degree, 60% aggregate",
    "exam_pattern": "ICICI Bank Assessment + Interview",
    "interview_rounds": ["Online Aptitude Test (90 min)", "Group Discussion (1)", "Technical Interview (1)", "HR Interview (1)"],
    "focus_areas": ["Quantitative Aptitude", "Reasoning", "English", "Banking Knowledge"],
    "icici_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Quantitative Aptitude", "questions": 25, "time_minutes": 25, "types": ["Numerical"], "difficulty": "medium", "topics": ["Percentages", "Profit & Loss", "Time & Work", "Probability", "Data Interpretation", "Number Series", "Simplification"]},
            {"name": "Reasoning", "questions": 25, "time_minutes": 25, "types": ["Logical"], "difficulty": "medium", "topics": ["Puzzles", "Syllogisms", "Coding-Decoding", "Seating Arrangement", "Blood Relations", "Direction Sense", "Series"]},
            {"name": "English", "questions": 25, "time_minutes": 20, "types": ["Grammar", "Reading"], "difficulty": "medium", "topics": ["Reading Comprehension", "Grammar", "Vocabulary", "Cloze Test", "Error Detection", "Sentence Correction"]},
            {"name": "General Awareness", "questions": 15, "time_minutes": 20, "types": ["MCQ"], "difficulty": "medium", "topics": ["Current Affairs", "Banking Terms", "Economic Policies", "Financial News", "Awards & Honors"]}
        ]
    },
    "coding_patterns": ["Solve banking quantitative problems on EMI and loans", "Data interpretation for financial reports", "Reasoning puzzles on bank operations", "Logical problems on transaction verification", "Probability problems in credit risk assessment", "Time and work problems for bank operations", "Profit and loss calculations for loan products", "Syllogism problems for banking policy", "Coding-decoding for secure banking communication", "Seating arrangement for branch management"],
    "hr_questions": ["Tell me about yourself", "Why ICICI Bank?", "What do you know about ICICI Bank's products?", "How do you handle customer service?", "Where do you see yourself in 5 years?", "What is your understanding of corporate banking?", "How do you handle pressure in banking?", "What do you know about digital banking trends?", "What motivates you to work in banking?", "What questions do you have for us?"],
    "tips": ["ICICI Bank values analytical and customer service skills", "Know about ICICI's banking products and digital initiatives", "Practice aptitude and reasoning daily", "Know about corporate banking and financial products", "Prepare for group discussion on economic topics", "Be thorough with banking regulations and compliance"]
}

# ============================================================
# CONGLOMERATES
# ============================================================

INDIAN_COMPANIES["tata_steel"] = {
    "name": "Tata Steel",
    "full_name": "Tata Steel Limited",
    "icon": "\U0001f3ed",
    "color": "#003580",
    "package": "6 LPA (Graduate Trainee) / 10 LPA (with allowances)",
    "eligibility": "GATE score, 60% aggregate, eligible branches",
    "exam_pattern": "Tata Steel Test + GATE + Interview",
    "interview_rounds": ["GATE Score Shortlisting", "Written Test + GD (if needed)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["GATE Topics", "Core Engineering", "Technical Knowledge", "Steel Technology"],
    "tata_steel_pattern": {
        "total_time_minutes": 150,
        "sections": [
            {"name": "General Aptitude", "questions": 10, "time_minutes": 15, "types": ["Verbal", "Numerical"], "difficulty": "easy-medium", "topics": ["Grammar", "Vocabulary", "Numerical Ability", "Logical Reasoning"]},
            {"name": "Core Engineering (GATE)", "questions": 55, "time_minutes": 135, "types": ["MCQ", "NAT"], "difficulty": "hard", "topics": ["Thermodynamics", "Fluid Mechanics", "Heat Transfer", "Materials Science", "Manufacturing", "Industrial Engineering"]}
        ]
    },
    "coding_patterns": ["Implement steel manufacturing process simulation", "Solve GATE-level materials problems", "Find optimal furnace temperature control", "Implement quality inspection algorithms", "Solve problems on metal forming processes", "Find the optimal production scheduling", "Implement supply chain optimization for steel", "Solve problems on structural analysis", "Find the cost minimization for production", "Implement energy management in steel plants"],
    "hr_questions": ["Tell me about yourself", "Why Tata Steel?", "What do you know about Tata Steel's history?", "Describe a project you worked on", "How do you handle working in heavy industry?", "Where do you see yourself in 5 years?", "What is your understanding of steel industry?", "How do you handle working under pressure?", "What motivates you to work in steel manufacturing?", "What questions do you have for us?"],
    "tips": ["GATE score and/or Tata Steel test is the primary criterion", "Know about Tata Steel's history and TATA Group values", "Focus on core engineering subjects", "Tata Steel values safety and sustainability", "Prepare for questions on steel manufacturing processes", "Be prepared for group discussion on industry topics"]
}

INDIAN_COMPANIES["reliance_jio"] = {
    "name": "Reliance Jio",
    "full_name": "Reliance Jio Infocomm Limited",
    "icon": "\U0001f4f6",
    "color": "#0A3A7E",
    "package": "6 LPA (Engineer) / 12 LPA (Senior Engineer)",
    "eligibility": "65% aggregate, CS/IT/ECE preferred",
    "exam_pattern": "Jio Engineering Assessment + Interviews",
    "interview_rounds": ["Online Assessment (90 min)", "Technical Interview (2-3 rounds)", "System Design Round (1)", "HR Interview (1)"],
    "focus_areas": ["DSA", "System Design", "Coding", "Telecom Technology"],
    "jio_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "MCQ", "questions": 20, "time_minutes": 20, "types": ["CS Fundamentals", "Telecom"], "difficulty": "medium", "topics": ["OOP", "DBMS", "OS", "Networking", "Data Structures", "5G Basics", "Telecom Protocols"]},
            {"name": "Coding", "questions": 3, "time_minutes": 70, "types": ["Problem Solving"], "difficulty": "medium", "topics": ["Arrays", "Strings", "Trees", "Graphs", "Dynamic Programming", "Greedy", "Hashing"]}
        ]
    },
    "coding_patterns": ["Design a network traffic optimization system", "Implement a real-time subscriber management system", "Find the optimal tower placement strategy", "Design a bandwidth allocation algorithm", "Implement a service quality monitoring system", "Find the optimal data routing in 5G network", "Design a content delivery network for JioTV", "Implement a billing and recharge system", "Find the network capacity planning algorithm", "Design a customer support ticket routing system"],
    "hr_questions": ["Tell me about yourself", "Why Reliance Jio?", "What do you know about Jio's 5G rollout?", "Describe a project you worked on", "How do you handle telecom infrastructure challenges?", "Where do you see yourself in 5 years?", "What is your understanding of 5G technology?", "How do you handle working under tight deadlines?", "What motivates you to work in telecom?", "What questions do you have for us?"],
    "tips": ["Jio focuses on DSA and telecom domain knowledge", "Know about 5G, telecom protocols, and network architecture", "Practice medium DSA problems", "Understand distributed systems and networking concepts", "Jio values innovation and scale", "Be prepared for questions on telecom industry trends"]
}

INDIAN_COMPANIES["adani"] = {
    "name": "Adani",
    "full_name": "Adani Group",
    "icon": "\u2600\ufe0f",
    "color": "#FF6600",
    "package": "5 LPA (Management Trainee) / 10 LPA (with allowances)",
    "eligibility": "60% aggregate, GATE preferred for engineering roles",
    "exam_pattern": "Adani Group Assessment + Interview",
    "interview_rounds": ["Online Assessment (90 min)", "Group Discussion (1)", "Technical Interview (1-2 rounds)", "HR Interview (1)"],
    "focus_areas": ["Aptitude", "Reasoning", "Technical", "General Awareness"],
    "adani_assessment_pattern": {
        "total_time_minutes": 90,
        "sections": [
            {"name": "Quantitative Aptitude", "questions": 25, "time_minutes": 25, "types": ["Numerical", "Data Interpretation"], "difficulty": "medium", "topics": ["Percentages", "Profit & Loss", "Time & Work", "Probability", "Data Interpretation", "Number Series", "Graphs"]},
            {"name": "Reasoning", "questions": 25, "time_minutes": 25, "types": ["Logical", "Abstract"], "difficulty": "medium", "topics": ["Puzzles", "Syllogisms", "Coding-Decoding", "Seating Arrangement", "Blood Relations", "Direction Sense", "Series"]},
            {"name": "English", "questions": 25, "time_minutes": 20, "types": ["Grammar", "Reading"], "difficulty": "medium", "topics": ["Reading Comprehension", "Grammar", "Vocabulary", "Cloze Test", "Error Detection"]},
            {"name": "General Awareness / Domain", "questions": 15, "time_minutes": 20, "types": ["MCQ"], "difficulty": "medium", "topics": ["Current Affairs", "Infrastructure", "Energy Sector", "Economic Policies", "Domain-Specific Knowledge"]}
        ]
    },
    "coding_patterns": ["Solve aptitude problems on infrastructure projects", "Data interpretation for energy sector reports", "Reasoning puzzles on project management", "Logical problems on resource allocation", "Quantitative problems on energy production", "Time and work problems for project scheduling", "Profit and loss calculations for infrastructure", "Syllogism problems for governance", "Coding-decoding for communication systems", "Seating arrangement for team management"],
    "hr_questions": ["Tell me about yourself", "Why Adani Group?", "What do you know about Adani's business verticals?", "Describe a project you worked on", "How do you handle working in infrastructure?", "Where do you see yourself in 5 years?", "What is your understanding of India's infrastructure growth?", "How do you handle working under pressure?", "What motivates you to work in conglomerates?", "What questions do you have for us?"],
    "tips": ["Adani Group values ambition and execution speed", "Know about Adani's business verticals (ports, energy, airports, cement)", "Practice aptitude and reasoning thoroughly", "Know about India's infrastructure development plans", "Prepare for group discussion on business topics", "Be aware of Adani's sustainability and green energy initiatives"]
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_all_companies():
    """Return simplified company list for API."""
    return [
        {
            "id": key,
            "name": info["name"],
            "full_name": info["full_name"],
            "icon": info["icon"],
            "color": info["color"],
            "package": info["package"],
            "eligibility": info["eligibility"],
            "exam_pattern": info["exam_pattern"],
            "interview_rounds": info["interview_rounds"],
            "focus_areas": info["focus_areas"],
        }
        for key, info in INDIAN_COMPANIES.items()
    ]


def get_company_detail(company_id: str):
    """Return full company detail including patterns and questions."""
    return INDIAN_COMPANIES.get(company_id.lower())


def get_company_mock_sections(company_id: str):
    """Return the mock test sections for a company."""
    company = INDIAN_COMPANIES.get(company_id.lower())
    if not company:
        return None

    pattern_key = {
        "tcs": "nqt_pattern",
        "infosys": "infytq_pattern",
        "wipro": "nlth_pattern",
        "cognizant": "genc_pattern",
        "hcl": "hcl_pattern",
        "accenture": "amcat_pattern",
        "capgemini": "indrive_pattern",
        "tech_mahindra": "smart_pattern",
        "lti": "lti_aptitude_pattern",
        "mphasis": "amcat_assessment_pattern",
        "hexaware": "hexaware_assessment_pattern",
        "cgi": "cgi_assessment_pattern",
        "virtusa": "virtusa_assessment_pattern",
        "ibm": "ibm_cognitive_pattern",
        "dell": "dell_assessment_pattern",
        "coforge": "coforge_test_pattern",
        "flipkart": "flipkart_coding_test",
        "razorpay": "razorpay_swe_pattern",
        "zomato": "zomato_coding_test",
        "phonepe": "phonepe_assessment_pattern",
        "swiggy": "swiggy_coding_test",
        "paytm": "paytm_assessment_pattern",
        "ola": "ola_coding_test",
        "makemytrip": "mmt_coding_test",
        "freshworks": "freshworks_assessment_pattern",
        "zoho": "zoho_written_pattern",
        "byjus": "byjus_assessment_pattern",
        "dream11": "dream11_assessment_pattern",
        "google_india": "google_coding_test",
        "microsoft_india": "microsoft_aoa_pattern",
        "amazon_india": "amazon_oa_pattern",
        "goldman_sachs": "gs_assessment_pattern",
        "jp_morgan": "jpmc_assessment_pattern",
        "drdo": "drdo_gate_pattern",
        "isro": "isro_exam_pattern",
        "bel": "bel_gate_pattern",
        "bhel": "bhel_gate_pattern",
        "ntpc": "ntpc_gate_pattern",
        "sail": "sail_gate_pattern",
        "iocl": "iocl_gate_pattern",
        "gail": "gail_gate_pattern",
        "cars24": "cars24_coding_test",
        "meesho": "meesho_coding_test",
        "groww": "groww_assessment_pattern",
        "cred": "cred_assessment_pattern",
        "urban_company": "uc_coding_test",
        "sharechat": "sharechat_coding_test",
        "sbi": "sbi_po_pattern",
        "hdfc": "hdfc_assessment_pattern",
        "icici": "icici_assessment_pattern",
        "tata_steel": "tata_steel_pattern",
        "reliance_jio": "jio_assessment_pattern",
        "adani": "adani_assessment_pattern",
    }

    key = pattern_key.get(company_id.lower())
    if not key:
        return None

    return company.get(key)
