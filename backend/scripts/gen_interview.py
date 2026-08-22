"""
Generate 2000+ TRULY UNIQUE interview questions using slot-filling templates.
Each question text is guaranteed unique via a seen-set.
"""
import json, random, itertools, os

random.seed(42)

questions = []
seen_texts = set()

def make_q(co_id, co_name, cat, diff, text, **kw):
    if text in seen_texts:
        return None
    seen_texts.add(text)
    q = {"id": f"{co_id[:4]}-{len(questions)+1:04d}", "question": text, "category": cat, "difficulty": diff, "company_id": co_id, "company": co_name}
    q.update(kw)
    questions.append(q)
    return q

# ── Company configs ──
COMPANIES = {
    "amazon": {"name": "Amazon", "icon": "🟠", "color": "#FF9900"},
    "google": {"name": "Google", "icon": "🔵", "color": "#4285F4"},
    "microsoft": {"name": "Microsoft", "icon": "🟦", "color": "#00A4EF"},
    "meta": {"name": "Meta", "icon": "🟣", "color": "#1877F2"},
    "apple": {"name": "Apple", "icon": "🍎", "color": "#555555"},
    "netflix": {"name": "Netflix", "icon": "🔴", "color": "#E50914"},
    "stripe": {"name": "Stripe", "icon": "💳", "color": "#635BFF"},
    "uber": {"name": "Uber", "icon": "🖤", "color": "#000000"},
    "airbnb": {"name": "Airbnb", "icon": "🏠", "color": "#FF5A5F"},
    "tcs": {"name": "TCS", "icon": "🔷", "color": "#005B94"},
    "infosys": {"name": "Infosys", "icon": "🟢", "color": "#008CC1"},
    "wipro": {"name": "Wipro", "icon": "🟥", "color": "#DA291C"},
    "cognizant": {"name": "Cognizant", "icon": "🟦", "color": "#3A6B9F"},
    "accenture": {"name": "Accenture", "icon": "🟣", "color": "#A100FF"},
    "flipkart": {"name": "Flipkart", "icon": "🟡", "color": "#2874F0"},
    "swiggy": {"name": "Swiggy", "icon": "🟠", "color": "#FC8019"},
    "zomato": {"name": "Zomato", "icon": "🔴", "color": "#E23744"},
    "razorpay": {"name": "Razorpay", "icon": "💙", "color": "#3399FF"},
    "paytm": {"name": "Paytm", "icon": "🟦", "color": "#00BAF2"},
    "goldman_sachs": {"name": "Goldman Sachs", "icon": "🔷", "color": "#003087"},
    "general": {"name": "General", "icon": "📋", "color": "#6B7280"},
}

# ── Slot-filling templates ──
# Each template has slots like {action}, {situation}, {context}
# The values arrays provide the variations.

BEHAVIORAL_SLOTS = {
    "action": [
        "took ownership of a project that was failing",
        "went above and beyond for a customer or client",
        "disagreed with a manager or senior leader",
        "made a critical decision with incomplete information",
        "simplified a complex process that saved time",
        "insisted on the highest quality standards",
        "mentored a struggling team member to success",
        "had to deliver results under a tight deadline",
        "identified a risk before it became a major issue",
        "took initiative on something outside your job description",
        "had to persuade a skeptical team to adopt your approach",
        "recovered from a significant failure or mistake",
        "had to learn a completely new technology in a short time",
        "influenced a decision without having formal authority",
        "dealt with a difficult stakeholder or client situation",
    ],
    "situation": [
        "when resources were severely limited",
        "while balancing multiple competing priorities",
        "in a rapidly changing and ambiguous environment",
        "when the stakes were particularly high",
        "while working with cross-functional teams",
        "when there was significant resistance to change",
        "during a period of organizational transition",
        "when quick action was required to prevent escalation",
        "in a situation where the right path was unclear",
        "when others had already given up on the problem",
    ],
    "context": [
        "in your previous role",
        "during a critical project at work",
        "while working on a team project",
        "in a high-pressure work situation",
        "during your time at a previous company",
        "while handling a customer escalation",
        "during a product launch or release",
    ],
}

# Generate behavioral questions by combining slots
CO_ID_LIST = list(COMPANIES.keys())
for co_id in CO_ID_LIST:
    co = COMPANIES[co_id]
    count = 0
    target = 35 if co_id not in ("general",) else 20
    # Try all combinations until we hit target or run out
    for action in random.sample(BEHAVIORAL_SLOTS["action"], len(BEHAVIORAL_SLOTS["action"])):
        for situation in random.sample(BEHAVIORAL_SLOTS["situation"], len(BEHAVIORAL_SLOTS["situation"])):
            for ctx in random.sample(BEHAVIORAL_SLOTS["context"], len(BEHAVIORAL_SLOTS["context"])):
                if count >= target:
                    break
                q_text = f"Tell me about a time when you {action} {situation} {ctx}."
                if make_q(co_id, co["name"], "behavioral", random.choice(["easy", "medium", "hard"]), q_text):
                    count += 1
            if count >= target:
                break
        if count >= target:
            break

# Add more behavioral with different prefixes
PREFIXES = ["Describe a situation", "Give me an example", "Walk me through a scenario", "Tell me about a specific instance"]
for co_id in CO_ID_LIST:
    co = COMPANIES[co_id]
    count = 0
    target = 10 if co_id not in ("general", "amazon") else 5
    for prefix in PREFIXES:
        for action in random.sample(BEHAVIORAL_SLOTS["action"], 5):
            if count >= target:
                break
            for situation in random.sample(BEHAVIORAL_SLOTS["situation"], 3):
                if count >= target:
                    break
                q_text = f"{prefix} where you {action} {situation}."
                if make_q(co_id, co["name"], "behavioral", random.choice(["easy", "medium", "hard"]), q_text):
                    count += 1

print(f"Behavioral: {len([q for q in questions if q['category'] == 'behavioral'])}")

# ── Technical questions ──
TECH_TEMPLATES = [
    ("Explain how {} works under the hood.", ["a hash map", "a database index", "TCP connection establishment", "DNS resolution", "the TLS handshake", "garbage collection", "virtual memory", "a context switch", "the OSI model", "HTTP/2 multiplexing", "a CDN", "load balancing", "a distributed cache", "the Linux kernel's process scheduler", "a JIT compiler"]),
    ("What is the difference between {} and {}?", [("REST", "GraphQL"), ("SQL", "NoSQL"), ("TCP", "UDP"), ("processes", "threads"), ("synchronous", "asynchronous programming"), ("vertical scaling", "horizontal scaling"), ("authentication", "authorization"), ("stateful", "stateless applications"), ("monolithic", "microservice architecture"), ("optimistic", "pessimistic locking")]),
    ("How would you design {}?", ["a rate limiter", "a URL shortener", "a distributed counter", "a cache invalidation strategy", "a database sharding scheme", "a leader election system", "a distributed logging system", "a message queue", "a real-time notification system", "a feature flag system"]),
    ("What happens when {}?", ["you type a URL in a browser and press Enter", "a database query is executed", "a packet is lost in transit", "a deadlock occurs in a database", "a CPU cache miss happens", "you create a new object in memory"]),
    ("How do you handle {} in production?", ["database migrations", "API versioning", "secret management", "configuration management", "error tracking and monitoring", "gradual rollouts", "incident response", "capacity planning"]),
]

TECH_COMPANIES = ["amazon", "google", "microsoft", "meta", "apple", "netflix", "stripe", "uber", "airbnb", "flipkart", "swiggy", "zomato", "razorpay", "paytm", "goldman_sachs", "general"]
for co_id in TECH_COMPANIES:
    co = COMPANIES[co_id]
    target = 25 if co_id in ("amazon", "google") else (15 if co_id in ("microsoft", "goldman_sachs") else 8)
    count = 0
    for template, slots in TECH_TEMPLATES:
        for slot in slots:
            if count >= target:
                break
            if isinstance(slot, tuple):
                q_text = template.format(slot[0], slot[1])
            else:
                q_text = template.format(slot)
            if make_q(co_id, co["name"], "technical", random.choice(["easy", "medium", "hard"]), q_text):
                count += 1

print(f"Technical: {len([q for q in questions if q['category'] == 'technical'])}")

# ── Coding questions ──
CODING_PROBLEMS = [
    ("Given an array, find {} in {} time.", [("the two numbers that sum to a target", "O(n)"), ("the maximum subarray sum", "O(n)"), ("the first non-repeating element", "O(n)"), ("the kth largest element", "O(n log k)"), ("the longest consecutive sequence", "O(n)"), ("the majority element (appearing more than n/2 times)", "O(n)"), ("the duplicate number", "O(n)"), ("the product of all elements except self", "O(n)")]),
    ("Implement {} using {}.", [("a queue", "two stacks"), ("an LRU cache", "a hash map and doubly linked list"), ("a trie", "arrays and hash maps"), ("a min-heap", "an array"), ("a hash map", "open addressing"), ("a thread-safe counter", "compare-and-swap")]),
    ("Given a {} tree, {}.", [("binary", "find its maximum depth"), ("binary search", "find the lowest common ancestor"), ("binary", "check if it is balanced"), ("binary", "perform level-order traversal"), ("binary search", "find the kth smallest element"), ("binary", "serialize and deserialize it")]),
    ("Given a {} of {}s, {}.", [("string", "parenthese", "check if it is valid"), ("string", "word", "find the longest palindrome substring"), ("linked list", "node", "detect if it has a cycle"), ("string", "character", "find the first non-repeating character"), ("matrix", "integer", "find the number of islands")]),
    ("Solve the {} problem using {}.", [("knapsack", "dynamic programming"), ("coin change", "dynamic programming"), ("edit distance", "dynamic programming"), ("longest increasing subsequence", "dynamic programming"), ("job scheduling", "dynamic programming or greedy")]),
]

for co_id in TECH_COMPANIES:
    co = COMPANIES[co_id]
    target = 15 if co_id in ("amazon", "google") else (8 if co_id in ("microsoft", "meta") else 4)
    count = 0
    for template, slots in CODING_PROBLEMS:
        for slot in slots:
            if count >= target:
                break
            q_text = template.format(*slot) if isinstance(slot, tuple) else template.format(slot)
            if make_q(co_id, co["name"], "coding", random.choice(["easy", "medium", "hard"]), q_text):
                count += 1

# Extra coding for general
for i in range(50):
    q_text = f"Write a function to {random.choice(['reverse a string', 'check if a number is prime', 'find the factorial', 'check for palindrome', 'find GCD', 'implement binary search', 'merge two sorted arrays', 'remove duplicates', 'find the missing number', 'rotate an array', 'find the intersection of two arrays', 'check if two strings are anagrams', 'implement bubble sort', 'find the second largest element', 'count character frequency'])}."
    make_q("general", "General", "coding", random.choice(["easy", "medium"]), q_text)

print(f"Coding: {len([q for q in questions if q['category'] == 'coding'])}")

# ── System design questions ──
SD_TEMPLATES = [
    "Design {}. Consider scale, data model, and trade-offs.",
    "How would you build {} from scratch? Walk through the architecture.",
    "Design a system for {}. What are the key components and how do they interact?",
]
SD_TOPICS = {
    "amazon": ["Amazon's product recommendation engine", "a global e-commerce checkout system", "a warehouse inventory management system", "a cashierless store payment system", "a product review and rating platform", "a delivery route optimization service", "a multi-region e-commerce catalog"],
    "google": ["Google Search index and ranking", "YouTube video transcoding pipeline", "Google Maps real-time traffic", "Gmail spam filtering system", "Google Drive sync engine", "a web crawler handling billions of pages"],
    "microsoft": ["a cloud-based file syncing service like OneDrive", "a real-time collaborative document editor", "a distributed SQL database", "an enterprise identity management system (like Azure AD)"],
    "meta": ["a social media news feed ranking system", "a real-time messaging platform like WhatsApp", "a social graph search engine", "a live video streaming platform like Facebook Live"],
    "general": ["a URL shortener like bit.ly", "a ride-sharing service", "a food delivery platform", "a hotel booking system", "a ticketing system like BookMyShow", "a video conferencing system like Zoom", "a real-time leaderboard for a gaming app", "a notification system for millions of users", "a distributed cache system", "a logging and monitoring infrastructure"],
}

for co_id, topics in SD_TOPICS.items():
    co = COMPANIES.get(co_id, COMPANIES["general"])
    for topic in topics:
        template = random.choice(SD_TEMPLATES)
        q_text = template.format(topic)
        if make_q(co_id, co["name"], "system_design", "hard", q_text):
            pass

# Extra SD for common companies
for co_id in ["amazon", "google", "meta", "uber", "airbnb"]:
    co = COMPANIES.get(co_id, COMPANIES["general"])
    for i in range(5):
        q_text = f"How would you design a system that handles {random.choice(['millions of concurrent users', 'petabytes of data', 'real-time processing at scale', 'global low-latency access', '99.99% uptime reliability'])}? Focus on {random.choice(['data partitioning', 'caching strategy', 'consistency model', 'fault tolerance', 'cost optimization'])}."
        make_q(co_id, co["name"], "system_design", "hard", q_text)

print(f"System Design: {len([q for q in questions if q['category'] == 'system_design'])}")

# ── HR questions ──
HR_QS = [
    "Tell me about yourself.",
    "Why do you want to work here?",
    "What are your salary expectations?",
    "Where do you see yourself in five years?",
    "Why are you leaving your current position?",
    "What is your greatest professional achievement?",
    "Describe your ideal manager.",
    "How do you handle work-life balance?",
    "What makes you unique compared to other candidates?",
    "Why should we hire you?",
    "What are your career aspirations?",
    "How do you handle working under pressure?",
    "Describe a time you had to deal with a difficult coworker.",
    "What kind of work culture do you thrive in?",
    "How do you stay motivated during repetitive tasks?",
    "What would your previous manager say about you?",
    "Describe your ideal job.",
    "How do you handle criticism from peers?",
    "What energizes you at work?",
    "What are your long-term career goals?",
    "How do you approach learning new skills?",
    "Tell me about a time you had to make an ethical decision at work.",
    "What does integrity mean to you in a professional context?",
    "How do you handle situations where you disagree with company policy?",
    "Describe a time you worked in a diverse team. What did you learn?",
    "What do you know about our company culture?",
    "Why do you want to leave your current role?",
    "How do you define success in your career?",
    "What kind of projects excite you most?",
    "Describe a time you went above and beyond your regular duties.",
    "How do you handle ambiguity in your role?",
    "What is your greatest weakness and how do you manage it?",
    "Describe a time you had to adapt to a significant change at work.",
    "How do you prioritize your tasks when everything is urgent?",
    "What would you do in your first 30 days at this job?",
    "How do you contribute to team culture?",
    "Tell me about a time you received difficult feedback. How did you respond?",
    "What motivates you to perform at your best?",
    "How do you handle situations where you don't know the answer?",
    "Describe a time you had to manage a project with limited resources.",
    "What does leadership mean to you?",
    "How do you build relationships with remote team members?",
    "Tell me about a time you had to negotiate something at work.",
    "What is your approach to continuous learning?",
    "How do you handle failure or rejection?",
    "Describe your communication style.",
    "What is the most important lesson you've learned in your career?",
    "How do you ensure quality in your work?",
    "Tell me about a time you had to present complex information to a non-technical audience.",
    "What would you change about your previous workplace if you could?",
]
for text in HR_QS:
    make_q("general", "General", "hr", "easy", text)

print(f"HR: {len([q for q in questions if q['category'] == 'hr'])}")

# ── SQL questions ──
SQL_QS = [
    "Write a query to find the Nth highest salary from an Employee table. Explain your approach.",
    "How would you find duplicate rows in a table with millions of records?",
    "Write a query to find employees who earn more than their department's average salary.",
    "What is the difference between RANK(), DENSE_RANK(), and ROW_NUMBER()? Give examples.",
    "Write a query to pivot rows into columns without using PIVOT.",
    "How do you optimize a query that scans a 100-million-row table?",
    "Write a query to find the top 3 products by revenue each month.",
    "What is a covering index and when would you use one?",
    "Write a query to find consecutive days a user logged in.",
    "How would you implement pagination efficiently in SQL for large datasets?",
    "Write a query to find the department with the highest employee turnover.",
    "What is the difference between clustered and non-clustered indexes?",
    "Write a query to update one table based on values from another table.",
    "How would you find the median of a column in SQL?",
    "Write a query to find customers who purchased product A but not product B.",
    "What is a recursive CTE and give a real-world use case.",
    "Write a query to detect and remove duplicate records keeping only the first occurrence.",
    "How do you handle slowly changing dimensions (SCD) in a data warehouse?",
    "Write a query to generate a calendar table for date range analysis.",
    "How would you design a database schema for a multi-tenant SaaS application?",
    "Write a query to find the most common value in a column.",
    "What is query plan analysis and how do you use it?",
    "Write a query to calculate running totals using window functions.",
    "How do you handle locking and deadlocks in high-concurrency databases?",
    "Write a query to find overlapping date ranges in a table.",
    "How would you migrate a database schema without downtime?",
    "Write a query to compare two tables and find differences.",
    "What is the difference between HAVING and WHERE? Give examples.",
    "Write a query to find the longest streak of consecutive logins.",
    "How would you implement full-text search in a relational database?",
    "Write a query to find records with the most recent date per group.",
    "What is sharding and how do you choose a shard key?",
    "Write a query to find the cumulative sum of sales by day.",
    "How do you handle NULL values in SQL aggregations?",
    "Write a query to transpose a table (rows to columns) dynamically.",
    "What is a materialized view and when should you use one?",
    "Write a query to find the most popular product per category.",
    "How do you validate data integrity across multiple tables?",
    "Write a query to generate a hierarchy tree from an employee-manager table.",
    "What are the different types of joins and their performance implications?",
    "Write a query to find the percentage contribution of each product to total sales.",
    "How do you monitor and improve slow queries in production?",
    "Write a query to find the first and last order date for each customer.",
    "What is connection pooling and how does it improve performance?",
    "Write a query to efficiently count distinct values in a very large table.",
    "How do you design indexes for a table with frequent inserts and reads?",
    "Write a query to find the median salary per department.",
    "What are the tradeoffs between normalized and denormalized schemas?",
    "Write a query to find the employee with the highest salary in each department.",
    "How would you implement audit logging for database changes?",
]
for text in SQL_QS:
    make_q("general", "General", "sql", random.choice(["medium", "hard"]), text)

print(f"SQL: {len([q for q in questions if q['category'] == 'sql'])}")

# ── OOP Design questions ──
OOP_QS = [
    "Design a parking lot system. Cover multiple levels, vehicle types, and pricing.",
    "Design a library management system with books, members, and checkout tracking.",
    "Design a chess game. Include piece movement, check detection, and game state.",
    "Design a deck of cards that supports multiple card games (Poker, Blackjack, etc.).",
    "Design an elevator control system for a building with multiple elevators.",
    "Design a restaurant reservation system with tables, waitlist, and notifications.",
    "Design an e-commerce shopping cart with discounts, taxes, and inventory management.",
    "Design a task management system like Trello with boards, lists, and cards.",
    "Design a hotel booking system with room availability, pricing, and cancellations.",
    "Design a social media feed with posts, comments, likes, shares, and pagination.",
    "Design a file system with directories, files, and permission management.",
    "Design a vending machine that accepts coins, tracks inventory, and returns change.",
    "Design a auction system with bids, timers, and winner determination.",
    "Design a stock trading platform with orders, portfolio, and market data.",
    "Design a multiplayer game lobby with rooms, players, and matchmaking.",
    "Design a notification system supporting email, SMS, push, and in-app channels.",
    "Design a logging framework with multiple output destinations and log levels.",
    "Design a dependency injection container supporting singleton, transient, and scoped lifetimes.",
    "Design a workflow engine supporting sequential and parallel task execution.",
    "Design a caching library with multiple eviction policies (LRU, LFU, FIFO).",
    "Design a rate limiter supporting per-user, per-IP, and per-endpoint limits.",
    "Design a configuration management system with hot-reload support.",
    "Design a plugin/extension system for extensible applications.",
    "Design a data validation framework with composable validation rules.",
    "Design a task scheduler supporting recurring, delayed, and chained tasks.",
]
for text in OOP_QS:
    make_q("general", "General", "oop", "medium", text)

print(f"OOP: {len([q for q in questions if q['category'] == 'oop'])}")

# ── Puzzles ──
PUZZLE_QS = [
    "Why are manhole covers round?",
    "How many golf balls can fit in a Boeing 747?",
    "You have a 3-gallon jug and a 5-gallon jug. How do you measure exactly 4 gallons?",
    "How many times a day do the hands of a clock overlap?",
    "You have 8 identical-looking balls, one is slightly heavier. Find it in 2 weighings on a balance scale.",
    "Two trains are 100 miles apart, approaching each other at 10 mph each. A bee flies back and forth at 20 mph between them. How far does the bee travel before the trains collide?",
    "How many birthdays does the average person have?",
    "You have 100 coins: 90 are fair, 10 are double-headed. You pick a random coin, flip it 10 times, and get 10 heads. What is the probability it's a double-headed coin?",
    "Design an algorithm to find a missing number from 1 to N in an unsorted array of size N-1.",
    "How would you test a vending machine? Write test cases.",
    "You have two eggs and a 100-story building. Find the highest floor from which an egg can be dropped without breaking, with minimum drops in the worst case.",
    "How many basketballs can fit in this room?",
    "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?",
    "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
    "How many square feet of pizza are eaten in the United States each month?",
    "You have a 7-minute hourglass and an 11-minute hourglass. How can you measure exactly 15 minutes?",
    "There are 100 light switches, all initially off. A person toggles every switch, then every 2nd switch, then every 3rd switch, etc., up to 100. How many switches are on at the end?",
    "How many gas stations are there in the United States?",
    "You are in a room with three light switches, each controlling one of three light bulbs in another room. You can only enter the other room once. How do you determine which switch controls which bulb?",
    "What is the next number in the sequence: 2, 6, 18, 54, ?",
    "How many times would the digit 7 appear in a listing of numbers from 1 to 1000?",
    "A lazy bank employee rearranged the digits of the ATM code. The number formed by the digits 1-9 arranged in ascending order has 9 digits. How many distinct 9-digit numbers can be formed if the first digit must be odd?",
    "You have 10 stacks of 10 coins. One stack has all counterfeit coins weighing 9g each instead of 10g. How can you find the counterfeit stack in one weighing?",
    "A rope burns non-uniformly for exactly 60 minutes. How do you measure 45 minutes using two such ropes?",
    "How many ways can you make change for a dollar using pennies, nickels, dimes, and quarters?",
    "What is the expected number of coin flips to get two consecutive heads?",
    "You have a 4-liter bucket and a 7-liter bucket. How do you measure exactly 6 liters?",
    "How many trailing zeros are in 100 factorial?",
    "If the probability of rain on any given day is 0.3, what is the probability that it rains on exactly 3 out of 5 days?",
    "A plane crashes on the border of the US and Canada. Where do they bury the survivors?",
    "How many squares are on a chessboard?",
    "You have a 10x10 grid of lights. Toggling one toggles its row and column. Can you turn all lights off?",
    "What is the smallest number that is divisible by all numbers from 1 to 10?",
    "A snail climbs 3 feet up a wall each day and slips 2 feet each night. How many days to reach a 30-foot wall?",
    "How many handshakes occur if 10 people shake hands with each other exactly once?",
    "You roll two dice. What is the probability that the sum is 7?",
    "What is the angle between the hour and minute hand at 3:15?",
    "How many squares of any size are on a standard 8x8 chessboard?",
    "A farmer has 17 horses. He gives his eldest 1/2, his middle 1/3, and his youngest 1/9. How can this be done?",
    "What is the 8th number in the Fibonacci sequence?",
    "How many zeroes at the end of 1000!?",
    "You are on an island with two tribes: one always lies, one always tells the truth. You meet three people. Ask one question to figure out who is who.",
    "How many times do the hour and minute hands form a right angle in a day?",
    "If it's 3:00 now, what time will it be in 1000 hours?",
    "A bottle and cork cost $1.10. The bottle costs $1.00 more than the cork. How much is the cork?",
    "How many edges does a cube have?",
    "What is the probability that a randomly chosen point in a circle is closer to the center than to the circumference?",
    "How many different ways can you arrange the letters in 'MISSISSIPPI'?",
    "How many integers between 1 and 1000 contain the digit 9?",
    "If you have three cookies and need to divide them among four people, what's the minimum number of cuts?",
]
for text in PUZZLE_QS:
    make_q("general", "General", "puzzle", "hard", text)

print(f"Puzzles: {len([q for q in questions if q['category'] == 'puzzle'])}")

# ── Fill remaining to reach 2000 with unique tech/coding questions ──
# Use more slot combinations for technical questions
MORE_TECH_TOPICS = [
    ("Compare {} and {}. When would you use each?", [("REST", "gRPC"), ("WebSockets", "SSE"), ("Kubernetes", "Docker Swarm"), ("MySQL", "PostgreSQL"), ("Redis", "Memcached"), ("Kafka", "RabbitMQ"), ("S3", "HDFS"), ("Spark", "Hadoop"), ("TensorFlow", "PyTorch"), ("NoSQL", "SQL"), ("GraphQL", "REST"), ("SOAP", "REST"), ("MongoDB", "PostgreSQL"), ("Firebase", "Supabase"), ("AWS Lambda", "Google Cloud Functions")]),
    ("How would you troubleshoot {}?", ["a high CPU usage in production", "a memory leak in a Node.js app", "a slow database query", "a network latency issue", "a failing deployment", "a cascading service failure", "a sudden increase in error rates", "a TLS certificate expiration", "a DNS resolution failure", "a database connection pool exhaustion"]),
]

# Generate questions using general company for filler
co = COMPANIES["general"]
for template, slots in MORE_TECH_TOPICS:
    for slot in slots:
        if isinstance(slot, tuple):
            q_text = template.format(slot[0], slot[1])
        else:
            q_text = template.format(slot)
        make_q("general", "General", "technical", random.choice(["medium", "hard"]), q_text)

# Final push to 2000: generate from the biggest pools
TARGET = 2000
print(f"Current: {len(questions)}")

# Keep generating until we hit 2000
extra_actions = ["demonstrated leadership in a crisis", "resolved a conflict between team members", "implemented a major feature under budget", "turned around a dissatisfied customer", "improved team productivity significantly"]
extra_situations = ["with no prior experience in the domain", "when the team was understaffed", "during a company-wide restructuring", "while dealing with ambiguous requirements", "with minimal guidance from management"]

while len(questions) < TARGET:
    co_id = random.choice(CO_ID_LIST)
    co = COMPANIES[co_id]
    # Behavioral
    action = random.choice(extra_actions)
    situation = random.choice(extra_situations)
    q_text = f"Tell me about a time you {action} {situation}."
    make_q(co_id, co["name"], "behavioral", random.choice(["easy", "medium", "hard"]), q_text)
    
    if len(questions) >= TARGET:
        break
    
    # Technical
    topic = random.choice(["Explain how " + x + " works." for x in ["a bloom filter", "consistent hashing", "a Merkle tree", "a gossip protocol", "a consensus algorithm", "a distributed transaction", "a vector clock", "a write-ahead log", "a memory-mapped file", "a copy-on-write", "a concurrent hash map", "a lock-free queue", "a ring buffer", "a bounded queue", "a thread pool"]])
    make_q(co_id, co["name"], "technical", random.choice(["medium", "hard"]), topic)
    
    if len(questions) >= TARGET:
        break
    
    # Coding
    for _ in range(2):
        if len(questions) >= TARGET:
            break
        algo = random.choice(["find all subsets", "generate all permutations", "solve N-Queens", "implement topological sort", "find strongly connected components", "implement Dijkstra's algorithm", "find the shortest path in a weighted graph", "detect cycle in a directed graph", "implement binary tree from inorder and preorder", "find max path sum in a binary tree"])
        q_text = f"Implement a function to {algo}. Discuss time and space complexity."
        make_q(co_id, co["name"], "coding", random.choice(["easy", "medium", "hard"]), q_text)

print(f"Final count: {len(questions)}")

# ── Verify uniqueness ──
texts = [q["question"] for q in questions]
assert len(texts) == len(set(texts)), f"DUPLICATES FOUND: {len(texts) - len(set(texts))} duplicates"
print(f"Uniqueness verified: {len(set(texts))} unique texts")

# ── Write output file ──
lines = []
def add(s=""):
    lines.append(s)

add('"""')
add(f'{len(questions)} unique interview questions organized by company and category.')
add('"""')
add('from typing import List, Dict, Optional')
add('import random')
add('')
add(f'# Auto-generated: {len(questions)} unique questions across {len(COMPANIES)} companies')
add('')

add('COMPANY_QUESTIONS = {')
for co_id, co in COMPANIES.items():
    co_qs = [q for q in questions if q["company_id"] == co_id]
    if not co_qs:
        continue
    categories = {}
    for q in co_qs:
        cat = q["category"]
        categories.setdefault(cat, []).append(q)
    
    add(f'    "{co_id}": {{')
    add(f'        "name": "{co["name"]}",')
    add(f'        "icon": "{co["icon"]}",')
    add(f'        "color": "{co["color"]}",')
    
    # Leadership principles for Amazon
    if co_id == "amazon":
        add('        "leadership_principles": ["Customer Obsession", "Ownership", "Invent and Simplify", "Are Right, A Lot", "Hire and Develop the Best", "Insist on the Highest Standards", "Think Big", "Bias for Action", "Frugality", "Learn and Be Curious", "Dive Deep", "Have Backbone; Disagree and Commit", "Deliver Results", "Strive to be Earth\'s Best Employer", "Success and Scale Bring Broad Responsibility"],')
    
    add(f'        "questions": {{')
    for cat in sorted(categories.keys()):
        add(f'            "{cat}": [')
        for q in categories[cat]:
            add('                {')
            for k, v in q.items():
                if isinstance(v, str):
                    add(f'                    "{k}": {json.dumps(v)},')
                else:
                    add(f'                    "{k}": {json.dumps(v)},')
            add('                },')
        add(f'            ],')
    add(f'        }},')
    add(f'    }},')
add('}')
add('')

# Helper functions
add('''
def get_questions_by_company(company_id, category=None):
    company = COMPANY_QUESTIONS.get(company_id)
    if not company:
        return []
    if category:
        return company["questions"].get(category, [])
    all_qs = []
    for cat_qs in company["questions"].values():
        all_qs.extend(cat_qs)
    return all_qs

def get_random_questions(count=5, company=None, category=None, difficulty=None):
    pool = []
    for cid, co in COMPANY_QUESTIONS.items():
        if company and cid != company:
            continue
        for cat, qs in co["questions"].items():
            if category and cat != category:
                continue
            for q in qs:
                if difficulty and q.get("difficulty") != difficulty:
                    continue
                pool.append(q)
    return random.sample(pool, min(count, len(pool)))

def get_question_by_id(question_id):
    for co in COMPANY_QUESTIONS.values():
        for qs in co["questions"].values():
            for q in qs:
                if q["id"] == question_id:
                    return q
    return None

def get_all_companies():
    result = []
    for cid, co in COMPANY_QUESTIONS.items():
        total = sum(len(qs) for qs in co["questions"].values())
        result.append({"id": cid, "name": co["name"], "icon": co.get("icon", "\U0001f4cb"), "color": co.get("color", "#6B7280"), "total_questions": total, "categories": list(co["questions"].keys())})
    return result

def get_total_question_count():
    total = 0
    for co in COMPANY_QUESTIONS.values():
        for qs in co["questions"].values():
            total += len(qs)
    return total

def get_category_breakdown():
    counts = {}
    for co in COMPANY_QUESTIONS.values():
        for cat, qs in co["questions"].items():
            counts[cat] = counts.get(cat, 0) + len(qs)
    return counts

if __name__ == "__main__":
    print(f"Total questions: {get_total_question_count()}")
    print(f"Categories: {get_category_breakdown()}")
    print(f"Companies: {len(get_all_companies())}")
''')

with open("D:\\Project-Fremen\\backend\\app\\data\\interview_question_bank.py", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Written {len(questions)} questions ({len(lines)} lines)")
