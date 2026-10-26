"""Generator: creates interview_question_bank.py from compact question data."""
from typing import List, Dict, Optional
import json

def expand_bh(qid, question, diff, sit, task, act, res, flags, principle):
    return {
        "id": qid, "question": question, "category": "behavioral",
        "difficulty": diff, "company_id": qid.split("-")[0].replace("amz","amazon").replace("goog","google").replace("msft","microsoft"),
        "company": "",  # filled by expand_company
        "star_tips": {"situation": sit, "task": task, "action": act, "result": res},
        "red_flags": flags, "principle": principle
    }

def expand_tc(qid, question, diff, knowledge, mistakes):
    cid = qid.split("-")[0].replace("amz","amazon").replace("goog","google").replace("msft","microsoft")
    return {
        "id": qid, "question": question, "category": "technical",
        "difficulty": diff, "company_id": cid, "company": "",
        "expected_knowledge": knowledge, "common_mistakes": mistakes
    }

def expand_cd(qid, question, diff, tc, sc, topics, examples):
    cid = qid.split("-")[0].replace("amz","amazon").replace("goog","google").replace("msft","microsoft")
    return {
        "id": qid, "question": question, "category": "coding",
        "difficulty": diff, "company_id": cid, "company": "",
        "time_complexity": tc, "space_complexity": sc, "topics": topics, "examples": examples
    }

def expand_sd(qid, question, diff, components, scale, est_scale):
    cid = qid.split("-")[0].replace("amz","amazon").replace("goog","google").replace("msft","microsoft")
    return {
        "id": qid, "question": question, "category": "system_design",
        "difficulty": diff, "company_id": cid, "company": "",
        "expected_components": components, "scale_considerations": scale, "estimated_scale": est_scale
    }

def expand_hr(qid, question, diff):
    return {
        "id": qid, "question": question, "category": "hr",
        "difficulty": diff, "company_id": "general", "company": "General"
    }

def expand_pz(qid, question, diff):
    return {
        "id": qid, "question": question, "category": "puzzle",
        "difficulty": diff, "company_id": "general", "company": "General"
    }

def expand_sql(qid, question, diff):
    return {
        "id": qid, "question": question, "category": "sql",
        "difficulty": diff, "company_id": "general", "company": "General"
    }

def expand_oop(qid, question, diff):
    return {
        "id": qid, "question": question, "category": "oop",
        "difficulty": diff, "company_id": "general", "company": "General"
    }

COMPANY_META = {
    "amazon": {"name": "Amazon", "icon": "\U0001f7e0", "color": "#FF9900",
        "principles": ["Customer Obsession", "Ownership", "Invent and Simplify", "Are Right, A Lot", "Hire and Develop the Best", "Insist on the Highest Standards", "Think Big", "Bias for Action", "Frugality", "Learn and Be Curious", "Dive Deep", "Have Backbone; Disagree and Commit", "Deliver Results"]},
    "google": {"name": "Google", "icon": "\U0001f310", "color": "#4285F4", "principles": []},
    "microsoft": {"name": "Microsoft", "icon": "\u25a0\ufe0f", "color": "#00A4EF", "principles": []},
    "meta": {"name": "Meta", "icon": "\U0001f310", "color": "#1877F2", "principles": []},
    "apple": {"name": "Apple", "icon": "\U0001f34e", "color": "#A2AAAD", "principles": []},
    "netflix": {"name": "Netflix", "icon": "\U0001f4fa", "color": "#E50914", "principles": []},
    "stripe": {"name": "Stripe", "icon": "\U0001f4b3", "color": "#635BFF", "principles": []},
    "uber": {"name": "Uber", "icon": "\U0001f698", "color": "#000000", "principles": []},
    "airbnb": {"name": "Airbnb", "icon": "\U0001f3e0", "color": "#FF5A5F", "principles": []},
    "tcs": {"name": "TCS", "icon": "\U0001f3db", "color": "#003DA5", "principles": []},
    "infosys": {"name": "Infosys", "icon": "\U0001f310", "color": "#007CC3", "principles": []},
    "wipro": {"name": "Wipro", "icon": "\U0001f310", "color": "#341C7A", "principles": []},
    "cognizant": {"name": "Cognizant", "icon": "\U0001f310", "color": "#0033A0", "principles": []},
    "accenture": {"name": "Accenture", "icon": "\U0001f310", "color": "#A100FF", "principles": []},
    "flipkart": {"name": "Flipkart", "icon": "\U0001f6cd", "color": "#2874F0", "principles": []},
    "swiggy": {"name": "Swiggy", "icon": "\U0001f35b", "color": "#FC8019", "principles": []},
    "zomato": {"name": "Zomato", "icon": "\U0001f373", "color": "#E23744", "principles": []},
    "razorpay": {"name": "Razorpay", "icon": "\U0001f4b0", "color": "#3399FF", "principles": []},
    "paytm": {"name": "Paytm", "icon": "\U0001f4b5", "color": "#00BAF2", "principles": []},
    "goldman_sachs": {"name": "Goldman Sachs", "icon": "\U0001f3e6", "color": "#003087", "principles": []},
    "general": {"name": "General", "icon": "\U0001f4cb", "color": "#6B7280", "principles": []},
}

CID_MAP = {
    "amz": "amazon", "goog": "google", "msft": "microsoft",
    "meta": "meta", "appl": "apple", "nflx": "netflix",
    "strp": "stripe", "uber": "uber", "abnb": "airbnb",
    "tcs": "tcs", "infy": "infosys", "wipr": "wipro",
    "cts": "cognizant", "acc": "accenture", "flpk": "flipkart",
    "swgy": "swiggy", "zomt": "zomato", "rzpy": "razorpay",
    "paytm": "paytm", "gs": "goldman_sachs", "gen": "general",
}

def get_cid(short):
    return CID_MAP.get(short, "general")

def company_name(cid):
    return COMPANY_META.get(cid, {}).get("name", cid.title())

# ── All questions in compact format ──
QUESTIONS = []

# -------------------------------------------
# AMAZON - Behavioral (30)
# -------------------------------------------
bh_amz = [
("amz-bh-001","Tell me about a time when you had to make a decision with incomplete information. How did you approach it and what was the outcome?","medium",
 "Describe a scenario where you had missing data or tight deadlines","Explain why you could not wait for complete information",
 "Walk through your decision-making framework and risk assessment","Share the outcome, even if not perfect, and what you learned",
 ["Waiting too long for perfect data","Being indecisive"],"Bias for Action"),
("amz-bh-002","Describe a time when you went above and beyond for a customer. What was the situation and how did you handle it?","medium",
 "Set up a specific customer pain point or complaint","Explain what was at stake for the customer",
 "Detail the extra steps you took beyond normal expectations","Quantify the impact on customer satisfaction or retention",
 ["Taking credit for team effort","Not measuring the outcome"],"Customer Obsession"),
("amz-bh-003","Tell me about a time you disagreed with your manager or a senior leader. How did you handle it?","hard",
 "Describe a real disagreement about approach or priorities","Explain why you felt strongly about your position",
 "Show how you respectfully presented data and alternatives","Whether they agreed or not, show you handled it professionally",
 ["Being insubordinate","Not backing your opinion with data"],"Have Backbone; Disagree and Commit"),
("amz-bh-004","Give me an example of a time you took ownership of a project that was failing. What did you do?","hard",
 "Describe a project that was behind schedule or over budget","Explain what was at risk if it failed",
 "Detail how you stepped in, identified root causes, and drove recovery","Share metrics showing the turnaround",
 ["Blaming others for the failure","Taking sole credit"],"Ownership"),
("amz-bh-005","Tell me about a time you invented something or simplified a complex process. What was the impact?","medium",
 "Describe a process that was overly complex or inefficient","Explain why simplification was needed",
 "Show how you thought creatively to solve it","Quantify time saved, cost reduced, or efficiency gained",
 ["Claiming something trivial as invention","Not explaining before and after"],"Invent and Simplify"),
("amz-bh-006","Describe a situation where you had to hire or develop someone. How did you ensure they grew?","medium",
 "Describe a team member who needed growth","Explain the gap in their skills or performance",
 "Detail your mentoring approach and feedback method","Show measurable improvement in their performance",
 ["Claiming you never had to develop anyone","Vague outcomes"],"Hire and Develop the Best"),
("amz-bh-007","Tell me about a time you insisted on the highest standards even when it was difficult. What happened?","hard",
 "Describe pressure to cut corners or lower quality","Explain what standards were at risk",
 "Show how you maintained quality despite pressure","Share the positive outcome from maintaining standards",
 ["Being inflexible without reason","Ignoring trade-offs"],"Insist on the Highest Standards"),
("amz-bh-008","Give me an example of a big goal you set for yourself. How did you achieve it?","medium",
 "Describe an ambitious professional or personal goal","Explain why it was important and challenging",
 "Show the planning, execution, and obstacles overcome","Share the measurable achievement",
 ["Setting easy goals","Not showing the work involved"],"Think Big"),
("amz-bh-009","Tell me about a time you had to work with limited resources. How did you make it work?","medium",
 "Describe a resource-constrained environment","Explain what needed to be delivered",
 "Show creative resource management and prioritization","Demonstrate you delivered despite constraints",
 ["Complaining about lack of resources","Not prioritizing"],"Frugality"),
("amz-bh-010","Describe a time you learned a new technology or skill to solve a problem. How did you approach learning it?","easy",
 "Describe a problem that required new knowledge","Explain what you needed to learn",
 "Detail your learning process and how you applied it","Show the successful outcome from your learning",
 ["Not being specific","Taking too long"],"Learn and Be Curious"),
("amz-bh-011","Tell me about a time you had to dive deep into a problem to understand the root cause. What did you find?","medium",
 "Describe a complex issue that required deep investigation","Explain why surface fixes were not enough",
 "Show your systematic approach to finding root cause","Share the deeper insight and fix implemented",
 ["Stopping at surface-level analysis","Not showing methodology"],"Dive Deep"),
("amz-bh-012","Give me an example of a time you had to deliver results under a tight deadline. How did you manage it?","medium",
 "Describe a deadline that was aggressive or moved up","Explain what was at stake",
 "Show how you prioritized, delegated, and executed","Share that you delivered on time with quality",
 ["Sacrificing quality","Not communicating risks"],"Deliver Results"),
("amz-bh-013","Describe a time when you had to make a decision that was unpopular. How did you handle it?","hard",
 "Describe a choice that went against the majority opinion","Explain the stakes and why it was necessary",
 "Show how you communicated and stood by your decision","Share the outcome and how the team moved forward",
 ["Being dismissive","Not explaining reasoning"],"Have Backbone; Disagree and Commit"),
("amz-bh-014","Tell me about a time you failed at something. What did you learn from it?","medium",
 "Describe a genuine failure, not a veiled success","Explain what you were trying to achieve",
 "Be honest about what went wrong and your role","Show what you learned and how you applied it",
 ["Blaming others","Choosing a trivial failure"],"Learn and Be Curious"),
("amz-bh-015","Give me an example of how you have used data to make a decision. Walk me through your thought process.","medium",
 "Describe a decision with multiple possible paths","Explain what data was available",
 "Show how you collected, analyzed, and interpreted data","Share how data led to a better outcome",
 ["Making decisions without data","Cherry-picking data"],"Are Right, A Lot"),
("amz-bh-016","Describe a time you had to influence someone without having direct authority over them.","hard",
 "Describe a cross-team or peer situation","Explain what you needed from them",
 "Show how you built rapport and found common ground","Share that you achieved alignment",
 ["Using authority inappropriately","Not understanding their perspective"],"Hire and Develop the Best"),
("amz-bh-017","Tell me about a time when you had to deal with a difficult teammate or stakeholder. How did you manage the relationship?","hard",
 "Describe a challenging personality or conflicting priorities","Explain what made them difficult to work with",
 "Show emotional intelligence and conflict resolution","Share how the relationship improved",
 ["Speaking negatively about them","Avoiding conflict"],"Have Backbone; Disagree and Commit"),
("amz-bh-018","Give me an example of a time you had to prioritize multiple competing priorities. How did you decide?","medium",
 "Describe a situation with multiple urgent demands","Explain what each priority required",
 "Show your prioritization framework and communication","Demonstrate successful delivery of key items",
 ["Trying to do everything poorly","Not communicating trade-offs"],"Deliver Results"),
("amz-bh-019","Describe a time you had to deal with ambiguity. How did you find clarity and move forward?","hard",
 "Describe an unclear or undefined situation","Explain what was ambiguous",
 "Show how you gathered information and iterated","Share how you created structure from ambiguity",
 ["Paralyzed by uncertainty","Waiting for others"],"Bias for Action"),
("amz-bh-020","Tell me about a time you had to say no to a request from a customer or stakeholder. How did you handle it?","medium",
 "Describe a request not feasible or aligned with priorities","Explain why saying yes would have been a problem",
 "Show how you communicated no and offered alternatives","Share that the relationship remained strong",
 ["Saying yes to everything","Being rude"],"Customer Obsession"),
("amz-bh-021","Give me an example of a time you identified a risk before it became a problem. What did you do?","medium",
 "Describe a project with hidden risks","Explain what could have gone wrong",
 "Show proactive risk identification and mitigation","Share how the risk was avoided",
 ["Not spotting obvious risks","Being reactive"],"Insist on the Highest Standards"),
("amz-bh-022","Describe a time when you had to make a trade-off between quality and speed. How did you decide?","medium",
 "Describe a tight deadline conflicting with quality goals","Explain what was at stake for both",
 "Show your decision framework and trade-off communication","Share the outcome and lessons learned",
 ["Always choosing speed","Not documenting trade-offs"],"Insist on the Highest Standards"),
("amz-bh-023","Tell me about a time you had to work on something outside your area of expertise. How did you approach it?","medium",
 "Describe a project requiring unfamiliar skills","Explain the gap in your knowledge",
 "Show how you learned and filled the gap","Share that you delivered despite not being an expert",
 ["Refusing to step outside comfort zone","Not asking for help"],"Learn and Be Curious"),
("amz-bh-024","Give me an example of a time you improved a process or system that was inefficient. What was your approach?","medium",
 "Describe a manual, slow, or error-prone process","Explain the impact of inefficiency",
 "Show your improvement plan and implementation","Quantify the improvement achieved",
 ["Suggesting changes without data","Not measuring before and after"],"Invent and Simplify"),
("amz-bh-025","Describe a time you had to mentor or coach a junior team member. What was your approach?","easy",
 "Describe a junior colleague needing guidance","Explain what skills they lacked",
 "Show your mentoring style and adaptation","Share their growth and team benefit",
 ["Being impatient","Not investing real time"],"Hire and Develop the Best"),
("amz-bh-026","Tell me about a time you had to make a difficult decision about allocating resources. How did you decide?","hard",
 "Describe competing demands for limited resources","Explain what each option required",
 "Show your decision criteria and trade-off evaluation","Share the impact of your resource allocation",
 ["Avoiding the decision","Not considering team input"],"Frugality"),
("amz-bh-027","Give me an example of a time you had to deal with a crisis or unexpected problem. How did you respond?","hard",
 "Describe a sudden production issue or emergency","Explain the severity and who was affected",
 "Show your calm, systematic response under pressure","Share how the crisis was resolved and lessons learned",
 ["Panicking","Not having a plan","Not doing post-mortem"],"Deliver Results"),
("amz-bh-028","Describe a time you had to persuade a team to adopt a new approach or technology. How did you get buy-in?","medium",
 "Describe resistance to change in your team","Explain why the new approach was better",
 "Show how you built a case and got buy-in","Share the adoption rate and impact",
 ["Forcing change without consensus","Not listening to objections"],"Think Big"),
("amz-bh-029","Tell me about a time you had to work with a team that was struggling. How did you help turn things around?","hard",
 "Describe a team with low morale or missed deadlines","Explain what the team was struggling with",
 "Show your leadership in addressing issues","Share measurable improvement in team performance",
 ["Playing the hero","Not addressing underlying issues"],"Hire and Develop the Best"),
("amz-bh-030","Give me an example of a time you went beyond your job description to solve a problem. Why did you do it?","medium",
 "Describe a problem not technically yours to solve","Explain why you chose to take it on",
 "Show the extra effort you put in","Share the impact of going above and beyond",
 ["Not knowing when to delegate","Seeking credit"],"Ownership"),
]
for q in bh_amz:
    d = expand_bh(*q); d["company_id"] = "amazon"; d["company"] = "Amazon"; QUESTIONS.append(d)
# -------------------------------------------
# AMAZON - Technical (25)
# -------------------------------------------
tc_amz = [
("amz-tc-001","Explain how Amazon DynamoDB achieves high availability and durability. What trade-offs does it make compared to a traditional relational database?","hard",
 ["NoSQL","Consistency models","Partitioning","Replication"],["Confusing DynamoDB with simple key-value stores","Not understanding eventual consistency"]),
("amz-tc-002","How would you design a service that handles millions of requests per second for product search on Amazon? Walk me through the architecture.","hard",
 ["Distributed systems","Search indexing","Caching","Load balancing"],["Ignoring caching layers","Not considering personalization"]),
("amz-tc-003","What happens when you type a URL into a browser and press Enter? Describe the full flow.","easy",
 ["DNS resolution","HTTP protocols","TCP/IP","Browser rendering"],["Skipping DNS details","Not mentioning HTTPS/TLS"]),
("amz-tc-004","Explain the CAP theorem. How would you apply it when designing a distributed shopping cart system?","medium",
 ["CAP theorem","Consistency models","Partition tolerance"],["Treating CAP as absolute truth","Not understanding PACELC"]),
("amz-tc-005","How would you detect and prevent fraud on an e-commerce platform? Describe the systems and algorithms you would use.","hard",
 ["ML","Real-time processing","Rule engines","Risk scoring"],["Only post-payment detection","Not considering false positives"]),
("amz-tc-006","Describe the differences between REST and GraphQL. When would you use each at Amazon scale?","medium",
 ["REST","GraphQL","API design","Caching"],["Thinking GraphQL always replaces REST","Ignoring caching implications"]),
("amz-tc-007","How does Amazon recommendation engine work? Explain collaborative filtering vs content-based filtering.","medium",
 ["Recommendation systems","Collaborative filtering","Matrix factorization","A/B testing"],["Oversimplifying","Ignoring cold start problem"]),
("amz-tc-008","Explain how you would implement a distributed rate limiter. What algorithms and data stores would you use?","hard",
 ["Rate limiting","Token bucket","Redis","Distributed counters"],["Not handling race conditions","Single-node at scale"]),
("amz-tc-009","What is the difference between SQL and NoSQL databases? Give me use cases where each would be appropriate at Amazon.","easy",
 ["SQL vs NoSQL","ACID vs BASE","Data modeling"],["Claiming one is always better","Not understanding consistency needs"]),
("amz-tc-010","How would you handle caching for a product detail page that gets millions of views per day? What invalidation strategy?","medium",
 ["CDN","Redis","Cache invalidation","Write-through vs write-behind"],["Not considering stale data","Wrong granularity"]),
("amz-tc-011","Explain microservices architecture. What are the main challenges when migrating from a monolith at Amazon scale?","medium",
 ["Microservices","Service mesh","API gateway","Distributed tracing"],["Ignoring network latency","Not planning data consistency"]),
("amz-tc-012","How does consistent hashing work and why is it important for distributed systems like DynamoDB?","medium",
 ["Consistent hashing","DHT","Replication","Virtual nodes"],["Confusing with regular hashing","Not understanding rebalancing"]),
("amz-tc-013","Describe the ACID properties. When would you relax them for performance at Amazon scale?","medium",
 ["ACID","Transaction isolation levels","Eventual consistency"],["Thinking ACID applies everywhere","Not understanding isolation vs consistency"]),
("amz-tc-014","How would you design a logging system that can handle terabytes of log data per day from thousands of services?","hard",
 ["Log aggregation","ELK stack","Kafka","Time-series databases"],["Centralizing all logs","Not planning retention"]),
("amz-tc-015","Explain process vs thread. How does the Linux kernel schedule them differently?","medium",
 ["OS concepts","Process vs thread","Context switching","Scheduling"],["Using interchangeably","Not understanding memory sharing"]),
("amz-tc-016","How would you implement a dead letter queue for a message processing system handling Amazon orders?","medium",
 ["Message queues","SQS","Error handling","Retry strategies"],["Not monitoring DLQ","Infinite retries without backoff"]),
("amz-tc-017","What is the difference between TCP and UDP? Give me a scenario where you would choose UDP over TCP.","easy",
 ["TCP vs UDP","OSI model","Latency vs reliability"],["Thinking UDP is never used","Not knowing when reliability matters less"]),
("amz-tc-018","Explain how you would detect and resolve performance bottlenecks in a high-traffic web application.","medium",
 ["Profiling","APM tools","Database optimization","Memory analysis"],["Optimizing without profiling first","Ignoring database bottleneck"]),
("amz-tc-019","Describe how garbage collection works in Java. How would you tune GC for a low-latency Amazon service?","hard",
 ["GC algorithms","Java memory model","G1GC","ZGC"],["Not understanding STW pauses","Random GC flag tuning"]),
("amz-tc-020","How would you implement a recommendation system for customers who bought this also bought?","hard",
 ["Apriori","Market basket analysis","Graph databases","Real-time processing"],["Ignoring data sparsity","Not updating frequently"]),
("amz-tc-021","Explain eventual consistency. How does Amazon shopping cart handle consistency vs availability trade-offs?","medium",
 ["Eventual consistency","Vector clocks","Conflict resolution"],["Confusing with weak consistency","Not knowing when strong consistency is needed"]),
("amz-tc-022","What is a CDN and how does it work? How would you configure CloudFront for Amazon global audience?","easy",
 ["CDN","Edge locations","Cache behaviors","Origin shield"],["Not considering cache invalidation","Ignoring regional requirements"]),
("amz-tc-023","How would you design a distributed counter tracking views on a product page across thousands of servers?","hard",
 ["Distributed counters","CRDTs","Redis","Approximate counting"],["Single DB counter","Not handling concurrent writes"]),
("amz-tc-024","Explain how you would deploy a new service with zero downtime. What deployment strategies exist?","medium",
 ["Blue-green","Canary releases","Rolling updates","Health checks"],["No rollback plan","Insufficient monitoring"]),
("amz-tc-025","Describe how OAuth 2.0 works. How would you implement authentication for Amazon third-party seller API?","medium",
 ["OAuth 2.0","JWT","Token refresh","Scopes"],["Confusing authN with authZ","Storing tokens insecurely"]),
]
for q in tc_amz:
    d = expand_tc(*q); d["company_id"] = "amazon"; d["company"] = "Amazon"; QUESTIONS.append(d)
# -------------------------------------------
# AMAZON - Coding (20)
# -------------------------------------------
cd_amz = [
("amz-cd-001","Given an array of integers, find the maximum product of two elements. Optimize for time and space.","easy","O(n)","O(1)",["array","math"],[{"input":"[1,10,-5,-2,3,2]","output":"30 (10*3)"}]),
("amz-cd-002","Given two strings, determine if one is a rotation of the other.","easy","O(n)","O(n)",["string"],[{"input":"s1=abcde, s2=cdeab","output":"True"}]),
("amz-cd-003","Implement an LRU cache with get and put operations in O(1) time.","medium","O(1)","O(capacity)",["hashmap","doubly-linked-list","design"],[{"input":"LRUCache(2), put(1,1), put(2,2), get(1), put(3,3), get(2)","output":"1, -1"}]),
("amz-cd-004","Given a binary tree, check if it is a valid Binary Search Tree.","medium","O(n)","O(h)",["tree","BST","recursion"],[{"input":"[2,1,3]","output":"True"},{"input":"[5,1,4,null,null,3,6]","output":"False"}]),
("amz-cd-005","Given a list of integers, find the longest consecutive sequence of numbers in O(n) time.","medium","O(n)","O(n)",["array","hashset"],[{"input":"[100,4,200,1,3,2]","output":"4 (1,2,3,4)"}]),
("amz-cd-006","Implement serialize and deserialize for a binary tree.","hard","O(n)","O(n)",["tree","design","serialization"],[{"input":"[1,2,3,null,null,4,5]","output":"1,2,null,null,3,4,null,null,5,null,null"}]),
("amz-cd-007","Find all duplicates in an array where values are between 1 and n in O(n) time without extra space.","medium","O(n)","O(1)",["array","cycle-detection"],[{"input":"[4,3,2,7,8,2,3,1]","output":"[2,3]"}]),
("amz-cd-008","Design a method to find the median of a stream of integers efficiently.","hard","O(log n) insert","O(n)",["heap","design"],[{"input":"Stream: 5,15,1,3","output":"Medians: 5,10,5,4"}]),
("amz-cd-009","Given a 2D grid of 1s (land) and 0s (water), count the number of islands.","medium","O(m*n)","O(m*n)",["graph","DFS","BFS"],[{"input":"Grid with 4 islands","output":"3"}]),
("amz-cd-010","Find the length of the longest substring without repeating characters.","medium","O(n)","O(min(m,n))",["string","sliding-window"],[{"input":"abcabcbb","output":"3 (abc)"}]),
("amz-cd-011","Find the kth largest element in an unsorted array in O(n) average time.","medium","O(n) avg","O(1)",["array","quickselect","heap"],[{"input":"[3,2,1,5,6,4], k=2","output":"5"}]),
("amz-cd-012","Search in a rotated sorted array. Return the index of target or -1.","medium","O(log n)","O(1)",["array","binary-search"],[{"input":"nums=[4,5,6,7,0,1,2], target=0","output":"4"}]),
("amz-cd-013","Design a data structure supporting insert, delete, and getRandom in O(1) with equal probability.","medium","O(1)","O(n)",["array","hashmap","design"],[{"input":"insert(1), insert(2), getRandom()","output":"1 or 2 equally"}]),
("amz-cd-014","Given an array of strings, group anagrams together.","medium","O(n*k log k)","O(n*k)",["string","hashmap","sorting"],[{"input":"[eat,tea,tan,ate,nat,bat]","output":"[[eat,tea,ate],[tan,nat],[bat]]"}]),
("amz-cd-015","Return the top k frequent elements from a list.","medium","O(n log k)","O(n+k)",["hashmap","heap","bucket-sort"],[{"input":"[1,1,1,2,2,3], k=2","output":"[1,2]"}]),
("amz-cd-016","Find the minimum path sum from top-left to bottom-right in a grid moving only down or right.","medium","O(m*n)","O(1)",["dp","grid"],[{"input":"grid=[[1,3,1],[1,5,1],[4,2,1]]","output":"7 (1->3->1->1->1)"}]),
("amz-cd-017","Determine if a string has all unique characters without using additional data structures.","easy","O(n)","O(1)",["string","bit-manipulation"],[{"input":"abcdef","output":"True"},{"input":"aabbcc","output":"False"}]),
("amz-cd-018","Clone a connected undirected graph. Return a deep copy.","medium","O(V+E)","O(V)",["graph","hashmap","DFS"],[{"input":"adjList=[[2,4],[1,3],[2,4],[1,3]]","output":"Deep copy"}]),
("amz-cd-019","Find the longest word that can be built one character at a time with all intermediate words in the list.","hard","O(n log n + n*l)","O(n*l)",["string","hashset","sorting"],[{"input":"[w,wo,wor,word,world,ord]","output":"world"}]),
("amz-cd-020","Find the element that appears once when all others appear twice, in O(n) time and O(1) space.","easy","O(n)","O(1)",["array","bit-manipulation","XOR"],[{"input":"[4,1,2,1,2]","output":"4"}]),
]
for q in cd_amz:
    d = expand_cd(*q); d["company_id"] = "amazon"; d["company"] = "Amazon"; QUESTIONS.append(d)
# -------------------------------------------
# AMAZON - System Design (10)
# -------------------------------------------
sd_amz = [
("amz-sd-001","Design Amazon product detail page at global scale with personalized content.","hard",
 ["CDN","Microservices","Caching","Personalization engine","CMS"],
 ["Read-heavy","Personalized content","Global distribution","Flash sales"],"500M+ DAU"),
("amz-sd-002","Design Amazon shopping cart handling persistence across devices.","hard",
 ["Cart service","Session management","Database","Sync mechanism"],
 ["Multi-device sync","Cart persistence","Price changes","Inventory holds"],"300M+ active carts daily"),
("amz-sd-003","Design Amazon recommendation engine for personalized product suggestions.","hard",
 ["Recommendation pipeline","Model serving","Feature store","A/B testing platform"],
 ["Real-time vs batch","Cold start","Recommendation diversity"],"500M+ users"),
("amz-sd-004","Design a real-time inventory management system for fulfillment centers.","hard",
 ["Inventory service","Warehouse management","Order routing","Event processing"],
 ["Real-time accuracy","Multi-warehouse","Returns handling","Stock predictions"],"10M+ SKUs, 100+ centers"),
("amz-sd-005","Design a package tracking system handling millions of tracking updates daily.","medium",
 ["Tracking service","Event ingestion","Notification system","Map service"],
 ["Real-time updates","High write volume","Customer notifications","Geolocation"],"100M+ packages daily"),
("amz-sd-006","Design a distributed payment processing system across multiple currencies.","hard",
 ["Payment gateway","Transaction service","Fraud detection","Ledger service"],
 ["Exactly-once processing","Multi-currency","Refund handling","Compliance"],"100M+ transactions daily"),
("amz-sd-007","Design a customer reviews system that prevents abuse and surfaces helpful reviews.","medium",
 ["Review service","Abuse detection","Ranking algorithm","Media storage"],
 ["Verified purchases","Review helpfulness voting","Media moderation"],"1B+ reviews"),
("amz-sd-008","Design search autocomplete handling millions of queries per second with sub-100ms latency.","medium",
 ["Trie service","Caching","Query suggestion","Trending detection"],
 ["Personalization","Trending queries","Multi-language","Misspellings"],"1B+ queries daily"),
("amz-sd-009","Design a flash sale system for millions of users buying limited-stock items simultaneously.","hard",
 ["Queue service","Inventory lock","Rate limiter","Order service"],
 ["Traffic spikes","Fairness","Inventory accuracy","Bot prevention"],"10M+ concurrent users"),
("amz-sd-010","Design Amazon Subscribe and Save recurring delivery service.","hard",
 ["Subscription service","Schedule manager","Inventory reservation","Order generation"],
 ["Recurring schedules","Price changes at renewal","Delivery optimization","Cancelling"],"50M+ subscriptions"),
]
for q in sd_amz:
    d = expand_sd(*q); d["company_id"] = "amazon"; d["company"] = "Amazon"; QUESTIONS.append(d)
# -------------------------------------------
# GOOGLE - Behavioral (20)
# -------------------------------------------
goog_bh = [
("goog-bh-001","Tell me about a project you led that had significant impact. How did you measure success?","medium",
 "Describe a project where you owned the outcome","Explain objectives and key results",
 "Show your leadership and technical decisions","Quantify impact with metrics",
 ["No clear metrics","Not acknowledging team contributions"],"")]
# Remaining goog behavioral to keep this manageable
("goog-bh-002","Describe a time you resolved a technical disagreement in your team. How did you reach consensus?","hard",
 "Describe a real technical debate","Explain what was being decided",
 "Show how you facilitated data-driven discussion","Share the outcome",
 ["Ignoring dissenting opinions","Making it personal"],""),
("goog-bh-003","Tell me about a time you took a significant risk and failed. What did you learn?","medium",
 "Describe a risk that did not pay off","Explain why it was worth taking",
 "Be honest about what went wrong","Focus on the learning",
 ["Not a real failure","Blaming others"],""),
("goog-bh-004","How do you stay current with technology trends? Give a specific example of something you learned and applied.","easy",
 "Describe a new technology you needed","Explain your motivation to learn",
 "Show your learning process and application","Share the impact",
 ["Generic answers like reading blogs","Not showing application"],""),
("goog-bh-005","Describe working with a cross-functional team to achieve a goal. How did you ensure collaboration?","medium",
 "Describe working with different functions","Explain the goal and challenges",
 "Show how you communicated and aligned everyone","Share the successful outcome",
 ["Working in silos","Not respecting other functions"],""),
("goog-bh-006","Tell me about a time you made a decision with limited data. How did you approach it?","medium",
 "Describe ambiguity in data or requirements","Explain the decision needed",
 "Show your framework for uncertainty","Share the outcome",
 ["Analysis paralysis","Not taking action"],""),
("goog-bh-007","Tell me about advocating for a user need that was not obvious to the team. How did you convince them?","medium",
 "Describe a user need being overlooked","Explain why it was important",
 "Show how you gathered user evidence","Share how the product changed",
 ["Not using data","Being confrontational"],""),
("goog-bh-008","Describe significantly improving a system or process. What was your approach?","medium",
 "Describe an inefficient process","Explain the problem and impact",
 "Detail your analysis and solution","Quantify the improvement",
 ["Not measuring before and after","Taking team credit"],""),
("goog-bh-009","Tell me about giving difficult feedback to a colleague. How did you approach it?","hard",
 "Describe when feedback was needed but uncomfortable","Explain what the feedback was",
 "Show constructive delivery approach","Share how they received it",
 ["Avoiding feedback","Being harsh or personal"],""),
("goog-bh-010","Describe a project requiring resourcefulness and creativity. What did you do that was out of the ordinary?","medium",
 "Describe a constraint requiring creativity","Explain what made it challenging",
 "Show your creative solution","Share the impact",
 ["Not actually creative","Standard solution"],""),
("goog-bh-011","Tell me about managing a project with shifting priorities. How did you adapt?","medium",
 "Describe frequently changing requirements","Explain the impact of shifts",
 "Show how you reprioritized and communicated","Share how you still delivered value",
 ["Getting frustrated","Not communicating changes"],""),
("goog-bh-012","Give an example of influencing someone to support your idea. What approach did you use?","medium",
 "Describe needing buy-in","Explain your proposal",
 "Show how you tailored your message","Share if you got support",
 ["Using authority","Not listening to concerns"],""),
("goog-bh-013","Tell me about dealing with conflict within your team. What was the outcome?","hard",
 "Describe a real team conflict","Explain the root cause",
 "Show how you mediated and found resolution","Share how the team improved",
 ["Taking sides","Not addressing directly"],""),
("goog-bh-014","Describe a time you went above and beyond for a project. What motivated you?","easy",
 "Describe a project requiring extra effort","Explain what was at stake",
 "Show what extra steps you took","Share the exceptional outcome",
 ["Making it sound like overwork","Not showing passion"],""),
("goog-bh-015","Tell me about teaching a complex concept to someone. How did you make it understandable?","easy",
 "Describe teaching a technical concept","Explain the audience background",
 "Show your teaching methodology","Share how well they understood",
 ["Being condescending","Not tailoring to audience"],""),
("goog-bh-016","Describe rapidly prototyping something. How did you balance speed with quality?","medium",
 "Describe a prototyping need","Explain the time constraint",
 "Show what you built and what you cut","Share how it informed the final product",
 ["Building production-quality","Not validating assumptions"],""),
]
for q in goog_bh:
    d = expand_bh(*q); d["company_id"] = "google"; d["company"] = "Google"; QUESTIONS.append(d)
# Remaining Google behavioral
goog_bh2 = [
("goog-bh-017","Tell me about solving a problem outside your area of expertise. What did you do?","medium",
 "Describe an unfamiliar domain problem","Explain why you had to solve it",
 "Show how you ramped up quickly","Share the outcome and learning",
 ["Giving up easily","Not asking for help"],""),
("goog-bh-018","Describe receiving critical feedback that changed how you work. How did you respond?","medium",
 "Describe difficult but valuable feedback","Explain why it was important",
 "Show how you processed and acted on it","Share how your behavior changed",
 ["Being defensive","Not taking action on feedback"],""),
("goog-bh-019","Tell me about balancing competing priorities from different stakeholders.","hard",
 "Describe conflicting stakeholder demands","Explain what each wanted",
 "Show your prioritization framework","Share how you satisfied key needs",
 ["Trying to please everyone","Not making trade-offs explicit"],""),
("goog-bh-020","Describe a project where you made significant architectural trade-offs. How did you decide?","hard",
 "Describe an architectural decision with trade-offs","Explain options and constraints",
 "Show your evaluation criteria","Share how it worked out",
 ["One-sided decision","Not acknowledging downsides"],""),
]
for q in goog_bh2:
    d = expand_bh(*q); d["company_id"] = "google"; d["company"] = "Google"; QUESTIONS.append(d)

# -------------------------------------------
# GOOGLE - Technical (30)
# -------------------------------------------
goog_tc = [
("goog-tc-001","Explain how Google Search indexes the web. How does it handle trillions of pages in milliseconds?","hard",
 ["Search indexing","PageRank","MapReduce","Inverted index","Distributed systems"],["Oversimplifying search","Not mentioning ranking"]),
("goog-tc-002","How does TCP congestion control work? Explain AIMD, slow start, and packet loss handling.","hard",
 ["TCP","Congestion control","Slow start","AIMD","Reno/Cubic"],["Confusing flow with congestion control","Not knowing modern variants"]),
("goog-tc-003","Design a distributed key-value store that is HA and partition tolerant. How do you handle consistency?","hard",
 ["Distributed systems","Consistency","Replication","Quorum","Gossip"],["Not handling partitions","Forgetting conflict resolution"]),
("goog-tc-004","Explain how PageRank works. What metrics determine a page importance?","medium",
 ["PageRank","Eigenvalues","Graph theory","Link analysis"],["Thinking it is the only factor","Not understanding math"]),
("goog-tc-005","What is the difference between process and thread? How does Google threading model handle concurrency?","medium",
 ["OS","Process vs thread","Context switching","Cgroups","Borg"],["Not understanding Go goroutines vs OS threads"]),
("goog-tc-006","How does Spanner achieve global consistency with high availability? Explain TrueTime.","hard",
 ["Spanner","TrueTime","Paxos","Global replication","External consistency"],["Confusing with simple replicated DBs","Not understanding atomic clocks"]),
("goog-tc-007","Explain MapReduce paradigm. Give an example of a good fit and one that is not.","medium",
 ["MapReduce","Distributed computing","Shuffle/sort","Data locality"],["Thinking MapReduce is obsolete","Not understanding when inefficient"]),
("goog-tc-008","How does Google load balancing work for frontend services? Describe layers from DNS to app server.","medium",
 ["DNS-based LB","Anycast","VIP-based LB","Maglev","Health checks"],["Only mentioning round-robin DNS","Not understanding connection draining"]),
("goog-tc-009","Time complexity of searching in balanced BST vs hash table? When would you choose each?","easy",
 ["Data structures","BST","Hash tables","Big O"],["Ignoring hash collision worst cases","Forgetting range queries"]),
("goog-tc-010","Explain gRPC and Protocol Buffers. How do they compare to REST and JSON?","medium",
 ["gRPC","Protobuf","HTTP/2","Binary serialization","Streaming"],["Not understanding schema evolution","Ignoring browser limits"]),
("goog-tc-011","How would you design a rate limiter for Google APIs? What algorithms would you consider?","medium",
 ["Rate limiting","Token bucket","Leaky bucket","Sliding window","Distributed counters"],["Not handling bursts","Single-point bottlenecks"]),
("goog-tc-012","Explain how DNS resolution works from typing a URL. What happens at each hierarchy level?","easy",
 ["DNS hierarchy","Recursive resolution","TTL","Anycast"],["Skipping root servers","Not understanding caching"]),
("goog-tc-013","Difference between monolithic and microservices architecture? When would Google choose each?","easy",
 ["Architecture patterns","Service decomposition","Monolith vs microservices"],["Always recommending microservices","Underestimating complexity"]),
("goog-tc-014","Explain how Bigtable stores data. What data model and how does it achieve high write throughput?","hard",
 ["Bigtable","LSM trees","SSTables","Memtables","Compaction"],["Comparing to traditional RDBMS","Not understanding storage format"]),
("goog-tc-015","How does TLS/SSL work? Explain handshake and certificate verification.","medium",
 ["TLS handshake","Public key crypto","Certificate authorities","Forward secrecy"],["Confusing TLS with SSL","Not understanding cert chains"]),
("goog-tc-016","Explain Raft vs Paxos consensus algorithms. When would you use each?","hard",
 ["Raft","Paxos","Consensus","Leader election","Log replication"],["Not understanding practical differences","Thinking they solve different problems"]),
("goog-tc-017","How does Kubernetes scheduler decide pod placement? What factors does it consider?","medium",
 ["Kubernetes","Scheduling","Resource requests","Affinity"],["Thinking it is random","Not understanding predicates vs priorities"]),
("goog-tc-018","Explain distributed tracing. How does Google Dapper help debug latency?","medium",
 ["Distributed tracing","Spans","Trace context","Sampling"],["Confusing with logging","Not understanding sampling trade-offs"]),
("goog-tc-019","Difference between vertical and horizontal scaling? When does vertical make more sense?","easy",
 ["Scaling strategies","Vertical vs horizontal","Stateful vs stateless"],["Always recommending horizontal","Ignoring cost"]),
("goog-tc-020","How does GC work in Go compared to Java? What are the trade-offs?","medium",
 ["Go GC","Java GC","Concurrent GC","STW pauses"],["Not understanding Go non-generational GC"]),
("goog-tc-021","Explain the OSI model layers and how each contributes to network communication.","easy",
 ["OSI model","TCP/IP stack","Encapsulation","Protocols per layer"],["Memorizing without understanding","Not relating to real protocols"]),
("goog-tc-022","Design a system like Google Docs for real-time collaboration. What conflict resolution strategy?","hard",
 ["OT vs CRDT","Real-time sync","WebSockets","Operational transformation"],["Not understanding OT vs CRDT","Ignoring cursor sync"]),
("goog-tc-023","How does HTTP/2 differ from HTTP/1.1? What improvements and challenges remain?","medium",
 ["HTTP/2","Multiplexing","Server push","Header compression","HPACK"],["Claiming HTTP/2 solves everything","Not understanding HOL blocking"]),
("goog-tc-024","Explain B-tree indexing vs LSM trees. Why does Bigtable use LSM trees?","medium",
 ["B-trees","LSM trees","Write amplification","Read vs write optimization"],["Not understanding trade-offs","Thinking one is better"]),
("goog-tc-025","How would you implement a web crawler respecting robots.txt and handling millions of pages?","hard",
 ["Web crawling","Politeness policy","URL canonicalization","Duplicate detection"],["Not handling crawl traps","Ignoring robots.txt"]),
("goog-tc-026","Difference between authorization and authentication? Implement OAuth 2.0 for Google APIs.","medium",
 ["OAuth 2.0","OpenID Connect","JWT","Scope-based authorization"],["Confusing authN with authZ","Not understanding refresh tokens"]),
("goog-tc-027","How does Linux kernel handle file I/O? Explain buffered vs direct I/O.","medium",
 ["Linux I/O stack","Page cache","Buffered vs direct I/O","AIO","io_uring"],["Not understanding page cache","Ignoring sync vs async"]),
("goog-tc-028","Explain how neural networks work at a high level. What is backpropagation?","medium",
 ["Neural networks","Backpropagation","Gradient descent","Activation functions"],["Treating as black box","Not understanding vanishing gradients"]),
("goog-tc-029","How does Gmail spam filter work? What ML techniques does it use?","medium",
 ["Spam filtering","Naive Bayes","Content analysis","Sender reputation"],["Oversimplifying","Not mentioning collaborative filtering"]),
("goog-tc-030","Difference between synchronous and asynchronous replication? When would Google use each?","medium",
 ["Replication","Sync vs async","Quorum","Consistency vs performance"],["Not understanding latency impact","Thinking sync is always better"]),
]
for q in goog_tc:
    d = expand_tc(*q); d["company_id"] = "google"; d["company"] = "Google"; QUESTIONS.append(d)
# -------------------------------------------
# GOOGLE - Coding (30)
# -------------------------------------------
goog_cd = [
("goog-cd-001","Given an array of integers, return indices of the two numbers summing to a target.","easy","O(n)","O(n)",["array","hashmap"],[{"input":"[2,7,11,15], target=9","output":"[0,1]"}]),
("goog-cd-002","Find the longest palindromic substring in a string.","medium","O(n^2)","O(1)",["string","dp"],[{"input":"babad","output":"bab or aba"}]),
("goog-cd-003","Generate all valid parentheses combinations for n pairs.","medium","O(4^n/sqrt(n))","O(n)",["backtracking","string"],[{"input":"n=3","output":"((())),(()()),(())(),()(()),()()()"}]),
("goog-cd-004","Find all unique quadruplets that sum to a target.","medium","O(n^3)","O(1)",["array","two-pointers","sorting"],[{"input":"[1,0,-1,0,-2,2], target=0","output":"[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]"}]),
("goog-cd-005","Find median of two sorted arrays in O(log(min(n,m))) time.","hard","O(log(min(n,m)))","O(1)",["array","binary-search","divide-and-conquer"],[{"input":"[1,3], [2]","output":"2.0"}]),
("goog-cd-006","Longest substring with at most k distinct characters.","medium","O(n)","O(k)",["string","sliding-window","hashmap"],[{"input":"eceba, k=2","output":"3 (ece)"}]),
("goog-cd-007","Data structure with insert, delete, search, getRandom in O(1) allowing duplicates.","hard","O(1) avg","O(n)",["hashmap","array","design"],[{"input":"insert(1),insert(1),insert(2),getRandom()","output":"1 with 2/3 probability"}]),
("goog-cd-008","Maximum path sum in a binary tree. Path can start and end at any node.","hard","O(n)","O(h)",["tree","DFS","recursion"],[{"input":"[-10,9,20,null,null,15,7]","output":"42 (15+20+7)"}]),
("goog-cd-009","Decode string following pattern: k[encoded_string].","medium","O(n*k)","O(n)",["string","stack","recursion"],[{"input":"3[a]2[bc]","output":"aaabcbc"}]),
("goog-cd-010","Find kth largest element in array in O(n) worst-case time.","medium","O(n)","O(1)",["array","quickselect","heap"],[{"input":"[3,2,3,1,2,4,5,5,6], k=4","output":"4"}]),
("goog-cd-011","Implement atoi: convert string to integer handling all edge cases.","medium","O(n)","O(1)",["string","math"],[{"input":"   -42","output":"-42"},{"input":"4193 with words","output":"4193"}]),
("goog-cd-012","Merge all overlapping intervals.","medium","O(n log n)","O(n)",["array","sorting","intervals"],[{"input":"[[1,3],[2,6],[8,10],[15,18]]","output":"[[1,6],[8,10],[15,18]]"}]),
("goog-cd-013","Rotate a matrix 90 degrees clockwise in place.","medium","O(m*n)","O(1)",["matrix","array"],[{"input":"[[1,2,3],[4,5,6],[7,8,9]]","output":"[[7,4,1],[8,5,2],[9,6,3]]"}]),
("goog-cd-014","Find the first non-repeating character in a string.","easy","O(n)","O(1)",["string","hashmap"],[{"input":"leetcode","output":"l"},{"input":"aabb","output":" "}]),
("goog-cd-015","Remove duplicates from sorted array in-place, return new length.","easy","O(n)","O(1)",["array","two-pointers"],[{"input":"[0,0,1,1,1,2,2,3,3,4]","output":"5"}]),
("goog-cd-016","Find kth smallest element in BST. Optimize for frequent modifications.","medium","O(h+k)","O(h)",["tree","BST","binary-search"],[{"input":"[3,1,4,null,2], k=1","output":"1"}]),
("goog-cd-017","Determine if string of parentheses is valid: includes (), [], {}.","easy","O(n)","O(n)",["string","stack"],[{"input":"()[]{}","output":"True"},{"input":"([)]","output":"False"}]),
("goog-cd-018","Find all permutations of a list of unique numbers.","medium","O(n!)","O(n)",["backtracking","recursion"],[{"input":"[1,2,3]","output":"[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"}]),
("goog-cd-019","Compute how much water can be trapped after raining on elevation map.","hard","O(n)","O(1)",["array","two-pointers","stack"],[{"input":"[0,1,0,2,1,0,1,3,2,1,2,1]","output":"6"}]),
("goog-cd-020","Calculate x^n where n can be negative or fractional.","medium","O(log n)","O(1)",["math","recursion","binary-exponentiation"],[{"input":"x=2.0, n=10","output":"1024.0"},{"input":"x=2.0, n=-2","output":"0.25"}]),
("goog-cd-021","Insert a new interval into non-overlapping intervals and merge if needed.","medium","O(n)","O(n)",["array","intervals"],[{"input":"[[1,3],[6,9]], new=[2,5]","output":"[[1,5],[6,9]]"}]),
("goog-cd-022","Clone a directed graph with neighbors list. Return deep copy.","medium","O(V+E)","O(V)",["graph","hashmap","BFS"],[{"input":"adjList=[[2,4],[1,3],[2,4],[1,3]]","output":"Deep copy"}]),
("goog-cd-023","Find longest common prefix string among array of strings.","easy","O(n*min_len)","O(1)",["string","trie"],[{"input":"[flower,flow,flight]","output":"fl"}]),
("goog-cd-024","Determine if a word can be segmented into space-separated dictionary words.","medium","O(n^2)","O(n)",["dp","string","hashset"],[{"input":"s=leetcode, dict=[leet,code]","output":"True"}]),
("goog-cd-025","Find the largest square containing only 1s in a 2D binary matrix.","medium","O(m*n)","O(m*n)",["dp","matrix"],[{"input":"matrix = [[1,0,1,0,0],[1,0,1,1,1],[1,1,1,1,1],[1,0,0,1,0]]","output":"4"}]),
("goog-cd-026","Count number of islands in a 2D grid (1=land, 0=water).","medium","O(m*n)","O(m*n)",["graph","DFS","BFS"],[{"input":"Full grid of 1s except edges","output":"1"}]),
("goog-cd-027","Find maximum rectangle containing only 1s in a binary matrix.","hard","O(m*n)","O(n)",["stack","dp","matrix"],[{"input":"Same matrix as cd-025","output":"6"}]),
("goog-cd-028","Design a URL shortener like tinyurl. Explain encode and decode.","medium","O(1)","O(n)",["design","hashmap","math"],[{"input":"https://example.com/very/long/url","output":"https://short.url/abc123"}]),
("goog-cd-029","Find contiguous subarray with largest sum (Kadane algorithm).","medium","O(n)","O(1)",["array","dp"],[{"input":"[-2,1,-3,4,-1,2,1,-5,4]","output":"6 (subarray [4,-1,2,1])"}]),
("goog-cd-030","Find largest rectangle area in histogram of bar heights.","hard","O(n)","O(n)",["stack","array"],[{"input":"[2,1,5,6,2,3]","output":"10"}]),
]
for q in goog_cd:
    d = expand_cd(*q); d["company_id"] = "google"; d["company"] = "Google"; QUESTIONS.append(d)
# -------------------------------------------
# GOOGLE - System Design (12)
# -------------------------------------------
goog_sd = [
("goog-sd-001","Design Google Search indexing billions of pages with sub-200ms response.","hard",
 ["Web crawler","Indexing pipeline","Query serving","Ranking","Infrastructure"],
 ["Trillions of pages","Global latency under 200ms","Spam resistance","Freshness"],"1B+ queries daily, 100B+ pages"),
("goog-sd-002","Design Google Maps with real-time traffic and routing.","hard",
 ["Map rendering","Routing engine","Traffic data pipeline","Geocoding","Navigation"],
 ["Real-time traffic","Global coverage","Navigation latency","Offline maps"],"1B+ MAU"),
("goog-sd-003","Design YouTube handling upload, transcoding, storage, streaming at scale.","hard",
 ["Upload service","Transcoding pipeline","CDN","Recommendation","Comment service"],
 ["500 hours/minute uploaded","Global streaming","Adaptive bitrate","Copyright detection"],"2B+ MAU, 1B+ hours watched daily"),
("goog-sd-004","Design Google Drive with sync across devices, sharing, version history.","hard",
 ["File sync","Chunk storage","Metadata DB","Conflict resolution","Sharing service"],
 ["Cross-device sync","Delta sync","Collaboration conflicts","Storage optimization"],"1B+ users"),
("goog-sd-005","Design Google ad serving system for real-time matching and revenue optimization.","hard",
 ["Ad server","Auction engine","User profile","Bidding system","Analytics"],
 ["Real-time auctions","Fraud detection","Budget pacing","Relevance ranking"],"100M+ ad impressions daily"),
("goog-sd-006","Design a push notification system sending billions of notifications daily.","medium",
 ["Notification server","Device registration","Queue system","Delivery service","Preferences"],
 ["High throughput","Delivery guarantees","Battery impact","Rate limiting"],"10B+ notifications daily"),
("goog-sd-007","Design Google Calendar with recurring events, sharing, conflict detection.","medium",
 ["Event service","Recurrence engine","Sharing service","Notification","Sync"],
 ["Recurring expansion","Time zone handling","Conflict detection","Offline access"],"500M+ MAU"),
("goog-sd-008","Design global chat system like Google Chat with millions of concurrent connections.","hard",
 ["Chat server","Connection manager","Message store","Presence service","Push notifications"],
 ["WebSocket connections","Message ordering","Multi-device sync","Search"],"100M+ DAU"),
("goog-sd-009","Design distributed photo storage like Google Photos with infinite backup.","hard",
 ["Upload service","Image processing","Storage tier","AI tagging","Search"],
 ["Exabytes of storage","Image compression","Face recognition","Shared albums"],"1B+ users, 4T+ photos"),
("goog-sd-010","Design location history feature processing millions of updates per second.","medium",
 ["Location ingestion","Data pipeline","Storage","Privacy service","Timeline service"],
 ["Privacy-first","High write throughput","Geospatial queries","Data retention"],"1B+ devices"),
("goog-sd-011","Design Google homepage serving doodles and personalization at global scale.","easy",
 ["CDN","Feature flags","Personalization","Static content","Edge caching"],
 ["Worldwide latency","Doodle scheduling","A/B testing","Zero downtime"],"1B+ daily visitors"),
("goog-sd-012","Design Google Translate supporting 100+ languages with billions of daily requests.","hard",
 ["Model serving","Language detection","Training pipeline","Cache","Feedback collection"],
 ["Model latency","Language pair coverage","Context-aware translation","Continuous improvement"],"500M+ DAU"),
]
for q in goog_sd:
    d = expand_sd(*q); d["company_id"] = "google"; d["company"] = "Google"; QUESTIONS.append(d)
# -------------------------------------------
# MICROSOFT - All
# -------------------------------------------
msft_bh = [
("msft-bh-001","Tell me about a time you adapted to a rapidly changing situation. How did you stay focused?","medium","Describe unexpected requirement changes","Explain the adaptation challenge","Show flexibility and reprioritization","Share how you delivered value","Resisting change, Getting flustered",""),
("msft-bh-002","Describe significant impact you had on a product or feature. What was your role?","medium","Describe a product you influenced","Explain what you wanted to achieve","Show specific contributions","Quantify impact","Not specific about role, Taking full credit",""),
("msft-bh-003","Tell me about collaborating with a difficult colleague. How did you make it work?","hard","Describe a challenging collaboration","Explain why it was difficult","Show conflict resolution and communication","Share how collaboration improved","Speaking negatively, Not taking responsibility",""),
("msft-bh-004","Give an example of how you approach learning a new technology. Walk me through your process.","easy","Describe needing to learn something new","Explain why it was important","Show structured learning approach","Share how you applied it","No method, Passive learning",""),
("msft-bh-005","Describe balancing multiple stakeholder needs. How did you decide?","hard","Describe conflicting requirements","Explain each stakeholder position","Show how you gathered input and made trade-offs","Share outcome balancing needs","Ignoring stakeholders, Unilateral decisions",""),
("msft-bh-006","Tell me about identifying a bug before it reached production. How did you catch it?","medium","Describe a potentially costly bug","Explain how you found it","Show testing or review process","Share impact of early detection","No quality process, Relying only on QA",""),
("msft-bh-007","Give an example of presenting complex tech to a non-technical audience. How did you make it accessible?","medium","Describe a technical presentation","Explain the complexity challenge","Show how you simplified without losing accuracy","Share how well the audience understood","Too much jargon, Condescending",""),
("msft-bh-008","Describe working on a project with tight resource constraints. How did you prioritize?","medium","Describe limited time, budget, or people","Explain what needed delivery","Show prioritization and resource management","Share how you delivered essentials","Complaining about constraints, Not prioritizing",""),
("msft-bh-009","Tell me about helping a struggling teammate. How did you approach it?","easy","Describe a colleague needing help","Explain what they struggled with","Show how you offered support","Share how they improved","Waiting to be asked, Judgment",""),
("msft-bh-010","Give an example of going out of your way to ensure product quality. What did you do?","medium","Describe quality concerns","Explain what was at stake","Show extra steps for quality","Share quality improvement","Cutting corners, Not documenting issues",""),
("msft-bh-011","Describe leading a project without formal authority. How did you influence people?","hard","Describe leading without authority","Explain the project goal","Show influence and persuasion skills","Share successful outcome","Using position instead of influence, Pushy",""),
("msft-bh-012","Tell me about making an unpopular decision. How did you communicate it?","hard","Describe an unpopular but necessary decision","Explain why it had to be made","Show communication of rationale","Share team response","Avoiding difficult conversations, Not explaining",""),
("msft-bh-013","Describe receiving negative feedback. How did you react and what changed?","medium","Describe receiving constructive criticism","Explain the feedback","Show growth mindset and action plan","Share how your behavior changed","Defensive, Not taking action",""),
("msft-bh-014","Tell me about a project with ambiguous goals. How did you define success?","medium","Describe ambiguous project goals","Explain the ambiguity","Show how you created clarity and alignment","Share outcome and measurement","Waiting for clarity, No measurable goals",""),
("msft-bh-015","Give an example of challenging the status quo. What was the result?","medium","Describe an assumption you challenged","Explain why change was needed","Show how you proposed a better approach","Share positive outcome","Challenging for its own sake, No alternative",""),
("msft-bh-016","Describe working under pressure to meet a deadline. How did you manage stress?","medium","Describe a high-pressure deadline","Explain what was at risk","Show stress and time management","Share on-time delivery","Not handling pressure, Sacrificing balance",""),
("msft-bh-017","Tell me about learning from a failure. What happened and what changed?","medium","Describe a real failure","Explain what you tried to do","Be honest about what went wrong","Show how you grew","Blaming others, Trivial failure",""),
("msft-bh-018","Give an example of collaborating in a diverse team. Steps for inclusion?","medium","Describe working in a diverse team","Explain importance of inclusion","Show specific inclusion actions","Share improved team outcome","Not recognizing diversity, Performative",""),
]
for q in msft_bh:
    d = expand_bh(*q); d["company_id"] = "microsoft"; d["company"] = "Microsoft"; QUESTIONS.append(d)

msft_tc = [
("msft-tc-001","Explain Windows memory model. How does virtual memory work and what is the page file?","medium",["Virtual memory","Paging","Page file","Memory-mapped files"],["Confusing virtual with physical","Not understanding page faults"]),
("msft-tc-002","How does .NET garbage collector work? Explain generational approach and LOH.","medium",[".NET GC","Generations","LOH","GC modes"],["Treating .NET GC like Java GC","Not understanding pinned objects"]),
("msft-tc-003","Describe Windows NT kernel architecture. What is the HAL?","hard",["NT kernel","HAL","Executive","Kernel vs user mode"],["Confusing kernel with user mode","Not understanding HAL"]),
("msft-tc-004","How does Azure load balancer distribute traffic? Layer 4 vs Layer 7?","medium",["Azure LB","Layer 4 vs 7","Session persistence","Health probes"],["Not understanding session affinity","Confusing LB types"]),
("msft-tc-005","Explain SQL Server query execution. How does the optimizer choose a plan?","hard",["SQL Server","Query optimizer","Execution plans","Indexing","Statistics"],["Not understanding cardinality estimation","Forgetting parameter sniffing"]),
("msft-tc-006","How does Active Directory work? Explain Kerberos authentication.","medium",["AD","Kerberos","LDAP","Domain controllers","Tickets"],["Confusing Kerberos with NTLM","Not understanding TGT process"]),
("msft-tc-007","Design a highly available SQL Server deployment on Azure. Replication options?","medium",["Azure SQL","Always On","Failover clustering","Geo-replication"],["Not planning failover","Ignoring read replicas"]),
("msft-tc-008","Explain async/await in C#. How does the compiler transform async methods?","medium",["C# async/await","State machine","Task","Synchronization context"],["Confusing async with parallelism","Blocking on async code"]),
("msft-tc-009","How does MSAL work? Difference between v1.0 and v2.0 endpoints?","medium",["MSAL","Azure AD","OAuth 2.0","OpenID Connect"],["Not understanding consent","Confusing app-only with delegated"]),
("msft-tc-010","Explain SQL join types: INNER, LEFT, RIGHT, FULL OUTER, CROSS. Use cases?","easy",["SQL joins","Set theory","Query optimization"],["Not understanding NULL behavior","Using WHERE instead of ON"]),
("msft-tc-011","How does Windows scheduler work? Priority levels and context switching.","medium",["Windows scheduler","Priority levels","Context switching","Quantum"],["Not understanding priority boosting","Assuming all schedulers same as Linux"]),
("msft-tc-012","Implement caching in distributed app using Azure Redis Cache.","medium",["Redis","Azure Redis","Caching patterns","Cache-aside","Distributed locks"],["Not setting expiration","Cache invalidation issues"]),
("msft-tc-013","Differences between value types and reference types in C#? Boxing/unboxing impact?","easy",["Value vs reference types","Stack vs heap","Boxing","Performance"],["Structs always faster","Not understanding memory allocation"]),
("msft-tc-014","How does Azure Cosmos DB handle global distribution? Consistency levels and RU pricing?","medium",["Cosmos DB","Consistency levels","Request Units","Global distribution"],["Not understanding RU consumption","Wrong consistency level"]),
("msft-tc-015","Describe OSI model mapped to Microsoft networking stack protocols.","easy",["OSI model","TCP/IP","Windows networking stack"],["Mixing up layers","Not mapping to real protocols"]),
("msft-tc-016","How would you secure a REST API in Azure? Auth, authorization, threat protection?","medium",["API security","Azure AD","OAuth","API Management","Rate limiting"],["Only API keys","No rate limiting"]),
("msft-tc-017","Explain Dependency Injection in .NET. Why important for testability?","easy",["DI","IoC",".NET DI container","Service lifetimes","Testability"],["Service locator pattern","Not understanding lifetimes"]),
("msft-tc-018","How does Microsoft STRIDE threat modeling work? Walk through a new feature.","medium",["STRIDE","Threat modeling","Security architecture","Mitigation"],["Skipping threat modeling","Not involving security early"]),
("msft-tc-019","Explain CDN concepts. How does Azure CDN work? Key configuration options?","easy",["CDN","Azure CDN","Edge nodes","Caching rules","Dynamic acceleration"],["Not understanding cache invalidation","Ignoring origin config"]),
("msft-tc-020","Describe Event Sourcing pattern. When use with Azure Event Hub?","hard",["Event sourcing","CQRS","Event Hub","Event streaming","Projections"],["Not handling event versioning","Ignoring replay challenges"]),
]
for q in msft_tc:
    d = expand_tc(*q); d["company_id"] = "microsoft"; d["company"] = "Microsoft"; QUESTIONS.append(d)

msft_cd = [
("msft-cd-001","Reverse a singly linked list.","easy","O(n)","O(1)",["linked-list"],[{"input":"1->2->3->4->5","output":"5->4->3->2->1"}]),
("msft-cd-002","Level-order traversal of binary tree returning list per level.","medium","O(n)","O(n)",["tree","BFS"],[{"input":"[3,9,20,null,null,15,7]","output":"[[3],[9,20],[15,7]]"}]),
("msft-cd-003","Check if linked list has a cycle. Find the cycle start node.","medium","O(n)","O(1)",["linked-list","two-pointers"],[{"input":"3->2->0->-4 (cycle at 2)","output":"True, node=2"}]),
("msft-cd-004","Determine if a binary tree is symmetric around its center.","easy","O(n)","O(h)",["tree","recursion","BFS"],[{"input":"[1,2,2,3,4,4,3]","output":"True"}]),
("msft-cd-005","Given a string, find the length of the longest substring without repeating characters.","medium","O(n)","O(min(m,n))",["string","sliding-window"],[{"input":"abcabcbb","output":"3"}]),
("msft-cd-006","Add two numbers represented by linked lists where digits stored in reverse order.","medium","O(max(n,m))","O(max(n,m))",["linked-list","math"],[{"input":"(2->4->3) + (5->6->4)","output":"7->0->8 (342+465=807)"}]),
("msft-cd-007","Find the longest common prefix string among array of strings.","easy","O(n*min_len)","O(1)",["string","trie"],[{"input":"[flower,flow,flight]","output":"fl"}]),
("msft-cd-008","Design a method to find the median of two sorted arrays.","hard","O(log(min(n,m)))","O(1)",["array","binary-search"],[{"input":"[1,2], [3,4]","output":"2.5"}]),
("msft-cd-009","Implement a text justification algorithm: format words into lines of equal width.","hard","O(n*k)","O(n)",["string","greedy"],[{"input":"words=[This,is,an,example], maxWidth=16","output":"[This  is  an, example  ]"}]),
("msft-cd-010","Find all valid combinations of k numbers that sum to n using numbers 1-9.","medium","O(9!/(9-k)!)","O(k)",["backtracking","combination"],[{"input":"k=3, n=7","output":"[[1,2,4]]"}]),
("msft-cd-011","Given a matrix, set entire row and column to zero if any element is zero.","medium","O(m*n)","O(1)",["matrix","array"],[{"input":"[[1,1,1],[1,0,1],[1,1,1]]","output":"[[1,0,1],[0,0,0],[1,0,1]]"}]),
("msft-cd-012","Convert a BST to a sorted doubly linked list in place.","medium","O(n)","O(h)",["tree","linked-list","DFS"],[{"input":"[4,2,5,1,3]","output":"1<->2<->3<->4<->5"}]),
("msft-cd-013","Given two strings, find if one is a permutation of the other.","easy","O(n)","O(1)",["string","hashmap"],[{"input":"abc, bca","output":"True"},{"input":"abc, abd","output":"False"}]),
("msft-cd-014","Implement a queue using two stacks.","easy","O(1) amortized","O(n)",["stack","queue","design"],[{"input":"push(1),push(2),peek(),pop()","output":"1, 1"}]),
("msft-cd-015","Find all numbers that appear in both arrays without duplicates.","easy","O(n+m)","O(min(n,m))",["array","hashset"],[{"input":"[1,2,2,1], [2,2]","output":"[2]"}]),
("msft-cd-016","Given n processes with execution time and a CPU cool-down period, find total time.","medium","O(n)","O(n)",["array","hashmap"],[{"input":"tasks=[A,A,A,B,B,B], n=2","output":"8"}]),
("msft-cd-017","Find the diameter of a binary tree (longest path between any two nodes).","easy","O(n)","O(h)",["tree","DFS","recursion"],[{"input":"[1,2,3,4,5]","output":"3 (path 4-2-1-3 or 5-2-1-3)"}]),
("msft-cd-018","Implement pow(x, n) for integer n with O(log n) time.","medium","O(log n)","O(1)",["math","recursion","binary-exponentiation"],[{"input":"x=2.0, n=10","output":"1024.0"}]),
]
for q in msft_cd:
    d = expand_cd(*q); d["company_id"] = "microsoft"; d["company"] = "Microsoft"; QUESTIONS.append(d)

msft_sd = [
("msft-sd-001","Design Microsoft Teams for real-time messaging, calls, and collaboration at enterprise scale.","hard",["Chat service","Media server","Presence service","File sharing","Calendar integration"],["Real-time messaging","Group calls","Screen sharing","Enterprise compliance"],"100M+ DAU"),
("msft-sd-002","Design Azure DevOps pipeline handling millions of CI/CD builds daily.","hard",["Queue system","Build agent pool","Artifact storage","Test runner","Deployment service"],["Scalable build agents","Parallel builds","Artifact retention","Cost optimization"],"10M+ daily builds"),
("msft-sd-003","Design Outlook/Exchange email system handling billions of messages daily.","hard",["Mail server","Spam filter","Search index","Storage","Sync service"],["High availability","Global distribution","Search performance","Calendar sync"],"400M+ users"),
("msft-sd-004","Design OneDrive file sync for cross-device file synchronization.","hard",["File sync engine","Delta sync","Chunk store","Conflict resolution","Sharing"],["Cross-device sync","Large file support","Bandwidth optimization","Offline support"],"100M+ users"),
("msft-sd-005","Design a telemetry system like Application Insights for monitoring millions of apps.","medium",["Data ingestion","Processing pipeline","Storage","Query service","Alerting"],["High throughput","Real-time analytics","Sampling","Retention policies"],"10M+ apps monitored"),
("msft-sd-006","Design Xbox Live gaming backend for multiplayer with low latency.","medium",["Game server","Matchmaking","Leaderboard","Friend service","Party chat"],["Low latency","Global distribution","Cheat detection","Party synchronization"],"100M+ active gamers"),
("msft-sd-007","Design Bing search index and serving system.","hard",["Crawler","Index","Query processor","Ranking","Cache"],["Web scale indexing","Freshness","Spam fighting","Query understanding"],"1B+ monthly users"),
("msft-sd-008","Design Azure Key Vault for secure secret and key management at cloud scale.","medium",["HSM backend","Auth service","Audit logging","Key rotation","Access policies"],["Security isolation","High availability","Compliance","Throttling"],"1M+ vaults"),
]
for q in msft_sd:
    d = expand_sd(*q); d["company_id"] = "microsoft"; d["company"] = "Microsoft"; QUESTIONS.append(d)
# -------------------------------------------
# META - All
# -------------------------------------------
meta_bh = [
("meta-bh-001","Tell me about a time you moved fast and broke things. What did you learn from the experience?","medium","Describe shipping quickly with imperfections","Explain what broke","Show how you fixed and iterated","Share the learning and better process","Moving carelessly, Not learning from mistakes",""),
("meta-bh-002","Describe a time you had a disagreement with a colleague about product direction. How was it resolved?","hard","Describe a product disagreement","Explain both perspectives","Show how you reached alignment","Share the outcome","Personal attacks, Not considering data",""),
("meta-bh-003","Tell me about a project where you had significant impact on user growth or engagement.","medium","Describe a growth-related project","Explain the metric you improved","Show your specific contributions","Quantify the growth impact","Not measuring impact, Vague results",""),
("meta-bh-004","Give an example of how you have dealt with ambiguity in a fast-paced environment.","medium","Describe ambiguity in a startup-like setting","Explain what was unclear","Show how you created structure","Share the outcome","Paralysis, Waiting for clarity",""),
("meta-bh-005","Describe a time you had to ship a product or feature under an extremely tight deadline.","medium","Describe a shipping deadline","Explain why it was aggressive","Show how you cut scope and prioritized","Share that you shipped on time","Sacrificing user experience, Not communicating",""),
("meta-bh-006","Tell me about a time you had to make a decision with conflicting data. How did you decide?","hard","Describe conflicting data points","Explain what you were deciding","Show your framework for resolving conflicts","Share what you decided and why","Ignoring data, Making gut decisions without consideration",""),
("meta-bh-007","Describe how you have used experimentation and A/B testing to drive product decisions.","medium","Describe an experiment you ran","Explain what you tested","Show your methodology and analysis","Share how it influenced the product","Not having clear hypotheses, P-hacking",""),
("meta-bh-008","Tell me about a time you had to work with a cross-functional team to launch something new.","medium","Describe cross-functional launch","Explain the teams involved","Show how you coordinated dependencies","Share the launch outcome","Siloed working, Dropping the ball on dependencies",""),
("meta-bh-009","Give an example of when you had to be extremely entrepreneurial and self-directed.","easy","Describe taking initiative","Explain why you had to be self-directed","Show what you accomplished without guidance","Share the result","Waiting for direction, Needing hand-holding",""),
("meta-bh-010","Describe a time you pushed back on a feature request because it did not align with user needs.","medium","Describe a feature request that missed the mark","Explain why it did not serve users","Show how you advocated for users","Share how the team adjusted","Saying yes to everything, Not understanding users",""),
("meta-bh-011","Tell me about a time you had to rapidly pivot your strategy based on new information.","hard","Describe a strategy change","Explain what new information emerged","Show how you pivoted quickly","Share the improved outcome","Resisting change, Slow to adapt",""),
("meta-bh-012","Describe a time you built something that achieved massive scale. How did you handle growth?","hard","Describe a scaling challenge","Explain the growth you experienced","Show how you architected for scale","Share the scaling success","Not planning for scale, Reactive fixes",""),
("meta-bh-013","Tell me about a time where you had to balance long-term vision with short-term execution.","medium","Describe tension between long and short term","Explain the trade-offs","Show how you balanced both","Share the outcome","Only focusing on short term, Ignoring immediate needs",""),
("meta-bh-014","Give an example of a time you influenced the direction of a product through data and insights.","medium","Describe using data to influence","Explain what insight you found","Show how you presented it","Share how the product changed","Opinions without data, Not sharing findings broadly",""),
("meta-bh-015","Describe a time you took calculated risks to achieve a breakthrough result.","hard","Describe a risky approach","Explain the potential downside","Show how you mitigated risks","Share the breakthrough outcome","Reckless risk-taking, Not having a backup plan",""),
]
for q in meta_bh:
    d = expand_bh(*q); d["company_id"] = "meta"; d["company"] = "Meta"; QUESTIONS.append(d)

meta_tc = [
("meta-tc-001","Explain how Facebook News Feed ranking works. What signals does it use?","hard",["Feed ranking","ML models","User signals","Relevance scoring"],["Oversimplifying ranking","Not mentioning personalization"]),
("meta-tc-002","How does React virtual DOM work? Why is it faster than direct DOM manipulation?","medium",["React","Virtual DOM","Diffing","Reconciliation"],["Thinking virtual DOM is always faster","Not understanding batching"]),
("meta-tc-003","Explain how GraphQL was designed at Meta. What problems does it solve over REST?","medium",["GraphQL","Schema design","Resolver pattern","Data fetching"],["Ignoring caching challenges","Not understanding N+1 problem"]),
("meta-tc-004","How does TAO (Meta distributed data store) work for social graph queries?","hard",["TAO","Social graph","Distributed cache","Associations"],["Confusing with traditional graph DBs","Not understanding cache hierarchy"]),
("meta-tc-005","Explain the architecture of a real-time messaging system like Messenger.","hard",["WebSockets","Message storage","Delivery semantics","Presence"],["Not handling offline messages","Ignoring ordering guarantees"]),
("meta-tc-006","How does Apache Cassandra store data? What consistency levels does it offer?","medium",["Cassandra","LSM trees","Consistency levels","Gossip protocol"],["Confusing with relational DBs","Not understanding tunable consistency"]),
("meta-tc-007","Describe how Presto (Trino) works as a distributed SQL query engine.","medium",["Presto","Distributed query engine","Connector architecture","Query optimization"],["Confusing with Hive","Not understanding memory management"]),
("meta-tc-008","How does the React Fiber reconciliation algorithm work?","hard",["React Fiber","Fiber nodes","Priority","Concurrent mode"],["Not understanding the need for Fiber","Confusing with stack reconciler"]),
("meta-tc-009","Explain how Live video streaming works on Meta platforms. Latency considerations?","medium",["Live streaming","RTMP","HLS","DASH","CDN"],["Not understanding adaptive bitrate","Ignoring latency vs quality trade-offs"]),
("meta-tc-010","How does PyTorch handle automatic differentiation? Explain the tape-based autograd system.","medium",["PyTorch","Autograd","Computational graph","Backpropagation"],["Not understanding dynamic graphs","Confusing with TensorFlow static graphs"]),
("meta-tc-011","Describe the architecture of a high-scale content delivery system like Facebook CDN.","hard",["CDN architecture","Edge caching","Origin offload","Regional CDN"],["Not understanding cache hierarchy","Ignoring warm vs cold cache"]),
("meta-tc-012","How does Instagram feed ranking differ from Facebook feed ranking?","medium",["Feed ranking","Engagement signals","Time decay","Interest prediction"],["Treating them identically","Not understanding visual content signals"]),
("meta-tc-013","Explain how WhatsApp achieves end-to-end encryption. Signal Protocol details?","hard",["E2E encryption","Signal Protocol","Double ratchet","Key exchange"],["Confusing with TLS","Not understanding forward secrecy"]),
("meta-tc-014","How does a friend recommendation system like People You May Know work?","medium",["Recommendation","Graph algorithms","Friend-of-friend","Collaborative filtering"],["Not explaining algorithmic details","Ignoring privacy concerns"]),
("meta-tc-015","Describe the Memcached architecture at Meta. How is it used for caching?","medium",["Memcached","Distributed caching","Cache invalidation","Pool architecture"],["Not understanding Meta specific optimizations","Ignoring cache stampede"]),
]
for q in meta_tc:
    d = expand_tc(*q); d["company_id"] = "meta"; d["company"] = "Meta"; QUESTIONS.append(d)

meta_cd = [
("meta-cd-001","Implement a function to check if a binary tree is a valid BST.","medium","O(n)","O(h)",["tree","BST"],[{"input":"[2,1,3]","output":"True"}]),
("meta-cd-002","Given a list of intervals, merge all overlapping intervals.","medium","O(n log n)","O(n)",["array","sorting","intervals"],[{"input":"[[1,3],[2,6],[8,10],[15,18]]","output":"[[1,6],[8,10],[15,18]]"}]),
("meta-cd-003","Find the k closest points to the origin in a 2D plane.","medium","O(n log k)","O(k)",["array","heap","geometry"],[{"input":"points=[[1,3],[-2,2]], k=1","output":"[[-2,2]]"}]),
("meta-cd-004","Given a binary tree, return its zigzag level order traversal.","medium","O(n)","O(n)",["tree","BFS","stack"],[{"input":"[3,9,20,null,null,15,7]","output":"[[3],[20,9],[15,7]]"}]),
("meta-cd-005","Implement strStr - find first occurrence of needle in haystack.","easy","O(n*m)","O(1)",["string","two-pointers"],[{"input":"haystack=hello, needle=ll","output":"2"}]),
("meta-cd-006","Given a sorted array and a target, find the first and last position of target.","medium","O(log n)","O(1)",["array","binary-search"],[{"input":"[5,7,7,8,8,10], target=8","output":"[3,4]"}]),
("meta-cd-007","Given an array, move all zeros to end while maintaining order of non-zero elements.","easy","O(n)","O(1)",["array","two-pointers"],[{"input":"[0,1,0,3,12]","output":"[1,3,12,0,0]"}]),
("meta-cd-008","Find all subsets of a set of distinct integers.","medium","O(2^n)","O(n)",["backtracking","bit-manipulation"],[{"input":"[1,2,3]","output":"[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]"}]),
("meta-cd-009","Design an algorithm to serialize and deserialize an N-ary tree.","hard","O(n)","O(n)",["tree","design"],[{"input":"N-ary tree with root=1, children=[2,3,4]","output":"Serialized string"}]),
("meta-cd-010","Given a string, find the minimum window substring containing all characters of another string.","hard","O(n)","O(m)",["string","sliding-window","hashmap"],[{"input":"s=ADOBECODEBANC, t=ABC","output":"BANC"}]),
("meta-cd-011","Given a list of words, group words that are anagrams of each other.","medium","O(n*k log k)","O(n*k)",["string","hashmap","sorting"],[{"input":"[eat,tea,tan,ate,nat,bat]","output":"[[eat,tea,ate],[tan,nat],[bat]]"}]),
("meta-cd-012","Implement a trie with insert, search, and startsWith methods.","medium","O(L) per op","O(total_chars)",["trie","design"],[{"input":"insert(apple), search(apple), search(app), startsWith(app)","output":"True, False, True"}]),
("meta-cd-013","Find the longest consecutive path in a binary tree (parent to child).","medium","O(n)","O(h)",["tree","DFS"],[{"input":"[1,null,2,3,4,5]","output":"3 (2-3-4 or 2-3-5)"}]),
("meta-cd-014","Given a matrix of 0s and 1s, find the largest rectangle of 1s.","hard","O(m*n)","O(n)",["stack","dp","matrix"],[{"input":"[[1,0,1,0,0],[1,0,1,1,1],[1,1,1,1,1],[1,0,0,1,0]]","output":"6"}]),
("meta-cd-015","Given a list of non-overlapping axis-aligned rectangles, find if a point lies in any rectangle.","medium","O(log n)","O(n)",["binary-search","geometry"],[{"input":"rectangles=[[0,0,2,2],[3,3,5,5]], point=(1,1)","output":"True"}]),
("meta-cd-016","Implement a rate limiter using sliding window log algorithm.","medium","O(n) per request","O(window_size)",["design","system-design"],[{"input":"RateLimiter(10, 1s), 10 requests in 1s","output":"11th request blocked"}]),
("meta-cd-017","Given two strings, find the number of common characters between them.","easy","O(n+m)","O(1)",["string","hashmap"],[{"input":"aabcc, adcaa","output":"3 (a,a,c)"}]),
("meta-cd-018","Find all possible words that can be formed from a phone number digit string.","medium","O(4^n)","O(n)",["backtracking","string"],[{"input":"23","output":"[ad,ae,af,bd,be,bf,cd,ce,cf]"}]),
("meta-cd-019","Given an array of integers, find all pairs that sum to a target value.","easy","O(n)","O(n)",["array","hashmap"],[{"input":"[1,2,3,4,5], target=5","output":"[(1,4),(2,3)]"}]),
("meta-cd-020","Implement a Least Frequently Used (LFU) cache.","hard","O(1)","O(capacity)",["hashmap","design","linked-list"],[{"input":"LFUCache(2), put(1,1), put(2,2), get(1), put(3,3)","output":"evicts key 2, LFU=1"}]),
]
for q in meta_cd:
    d = expand_cd(*q); d["company_id"] = "meta"; d["company"] = "Meta"; QUESTIONS.append(d)

meta_sd = [
("meta-sd-001","Design Facebook News Feed serving billions of requests with personalized ranking.","hard",["Feed builder","Ranking service","Content storage","Notification system","ML pipeline"],["Personalized ranking","Real-time updates","Diversity","Sponsored content"],"2B+ DAU"),
("meta-sd-002","Design Instagram stories with 500M+ DAU. How do you handle ephemeral content?","hard",["Story service","Media upload","Ephemeral storage","View tracking","Expiry service"],["24-hour expiry","High upload volume","View counting accuracy","Sticker/effect processing"],"500M+ DAU"),
("meta-sd-003","Design WhatsApp messaging system for billions of messages with E2E encryption.","hard",["Chat server","Message store","Presence service","Media service","E2E encryption"],["End-to-end encryption","Multi-device","Message ordering","Delivery receipts"],"2B+ users, 100B+ messages daily"),
("meta-sd-004","Design Facebook Live for real-time video streaming to millions.","hard",["Ingest server","Transcoder","CDN","Chat service","Replay storage"],["Low latency streaming","Adaptive bitrate","Real-time comments","Scale to millions"],"1B+ live viewers"),
("meta-sd-005","Design a notification system handling billions of push notifications daily.","medium",["Notification generator","Queue","Delivery service","Device registration","Preferences"],["High throughput","Delivery guarantees","Device battery","Grouping"],"10B+ notifications daily"),
("meta-sd-006","Design Facebook search across posts, people, groups, photos, and videos.","hard",["Search index","Query parser","Ranking","Personalization","Real-time indexing"],["Unified search","Personalized results","Real-time content","Typo tolerance"],"1B+ search queries daily"),
("meta-sd-007","Design a friend suggestion system like People You May Know.","medium",["Friend-of-friend","Graph processing","Recommendation engine","User embedding"],["Scalable graph walks","Privacy constraints","Real-time updates","New user cold start"],"2B+ users"),
("meta-sd-008","Design Instagram Explore page with personalized content discovery.","medium",["Content ranking","Interest modeling","ML serving","Media storage","Engagement tracking"],["Personalization","Content diversity","Freshness","Explore vs following"],"500M+ DAU on Explore"),
]
for q in meta_sd:
    d = expand_sd(*q); d["company_id"] = "meta"; d["company"] = "Meta"; QUESTIONS.append(d)
# -------------------------------------------
# APPLE
# -------------------------------------------
appl_bh = [
("appl-bh-001","Describe a time you designed a product with simplicity as the primary goal. How did you achieve it?","medium","Describe designing for simplicity","Explain why simplicity was critical","Show how you removed complexity","Share the elegant result","Adding unnecessary features, Not understanding user needs",""),
("appl-bh-002","Tell me about a time you collaborated with hardware and software teams. What challenges did you face?","hard","Describe HW/SW collaboration","Explain the integration challenge","Show how you bridged the gap","Share the successful integration","Not understanding hardware constraints, Siloed work",""),
("appl-bh-003","Give an example of a time you paid extraordinary attention to detail on a project.","medium","Describe a detail-oriented project","Explain why details mattered","Show your meticulous approach","Share how it improved quality","Careless mistakes, Not caring about polish",""),
("appl-bh-004","Describe a time you had to optimize performance for a resource-constrained device.","medium","Describe a constrained environment","Explain what was limited","Show your optimization approach","Share the performance gain","Ignoring memory/CPU limits, Not profiling",""),
("appl-bh-005","Tell me about a time you pushed back on a decision because it compromised user experience.","medium","Describe a UX-compromising decision","Explain why UX would suffer","Show how you advocated for the user","Share how the team adjusted","Sacrificing UX for deadlines, Not speaking up",""),
("appl-bh-006","Describe how you approach accessibility in product design. Give a specific example.","medium","Describe an accessibility challenge","Explain who was affected","Show how you made it accessible","Share the inclusive outcome","Treating accessibility as afterthought, Not understanding WCAG",""),
("appl-bh-007","Tell me about a time you had to learn a completely new technology stack to ship a product.","easy","Describe learning a new stack","Explain why it was necessary","Show how you ramped up effectively","Share the successful launch","Resisting learning, Taking too long",""),
("appl-bh-008","Give an example of when you turned a complex problem into an elegant solution.","medium","Describe a complex problem","Explain why it was hard","Show your simplified approach","Share the elegant solution","Over-engineering, Not seeking simplicity",""),
("appl-bh-009","Describe a time you had to maintain quality while working under extreme time pressure.","medium","Describe time pressure with quality expectations","Explain what was at stake","Show how you maintained standards","Share the quality outcome","Cutting corners, Sacrificing quality",""),
("appl-bh-010","Tell me about a time you received feedback that your work was not up to standard. How did you respond?","medium","Describe receiving quality feedback","Explain the gap","Show how you addressed it","Share the improved result","Being defensive, Not acting on feedback",""),
("appl-bh-011","Describe a project where you had to integrate multiple different systems or frameworks.","hard","Describe a complex integration","Explain the systems involved","Show how you made them work together","Share the successful integration","Not understanding dependencies, Ignoring edge cases",""),
("appl-bh-012","Give an example of a time you anticipated a future problem and proactively addressed it.","medium","Describe anticipating an issue","Explain what could go wrong","Show your proactive solution","Share how the problem was avoided","Being reactive, Not thinking ahead",""),
]
for q in appl_bh:
    d = expand_bh(*q); d["company_id"] = "apple"; d["company"] = "Apple"; QUESTIONS.append(d)

appl_tc = [
("appl-tc-001","Explain the iOS app sandbox security model. How does it protect user data?","medium",["iOS security","App sandbox","Keychain","Entitlements"],["Not understanding sandbox limitations","Confusing with Android model"]),
("appl-tc-002","How does Metal (Apple GPU framework) differ from OpenGL? What performance advantages does it offer?","hard",["Metal","GPU programming","Low-level graphics","Compute shaders"],["Not understanding driver overhead","Confusing with higher-level frameworks"]),
("appl-tc-003","Explain how Swift memory management works through ARC. When do retain cycles occur?","medium",["Swift","ARC","Reference counting","Retain cycles","Weak references"],["Not understanding retain cycles","Confusing with GC"]),
("appl-tc-004","How does Grand Central Dispatch work? Explain queues, QoS classes, and thread safety.","medium",["GCD","Dispatch queues","QoS","Thread safety","Deadlocks"],["Not understanding QoS inversion","Blocking main thread"]),
("appl-tc-005","Explain Core Data architecture. How does it manage object graphs and persistence?","medium",["Core Data","NSManagedObject","Persistent store","Context","Migration"],["Not understanding context hierarchy","Ignoring migration challenges"]),
("appl-tc-006","How does M-series chip unified memory architecture work? What are the performance implications?","hard",["Apple Silicon","Unified memory","SoC architecture","Bandwidth"],["Not understanding cache coherency","Confusing with traditional RAM"]),
("appl-tc-007","Explain how Secure Enclave works on Apple devices. What does it protect?","medium",["Secure Enclave","Hardware security","Biometric auth","Key management"],["Confusing with software-only security","Not understanding isolation"]),
("appl-tc-008","How does the iOS runtime handle method swizzling and dynamic dispatch?","medium",["Objective-C runtime","Method swizzling","Dynamic dispatch","Message forwarding"],["Abusing swizzling","Not understanding runtime implications"]),
("appl-tc-009","Explain how ARKit tracks environmental features and performs world mapping.","medium",["ARKit","Visual-inertial odometry","Feature points","World tracking"],["Not understanding sensor fusion","Ignoring lighting requirements"]),
("appl-tc-010","How does Core Bluetooth work for BLE communication? What are the architectural patterns?","easy",["Core Bluetooth","BLE","Peripheral/Central","Service/Characteristic"],["Not understanding BLE lifecycle","Ignoring power considerations"]),
("appl-tc-011","Explain the difference between value semantics and reference semantics in Swift.","easy",["Swift","Value vs reference","Struct vs class","Copy-on-write"],["Always using classes","Not understanding performance implications"]),
("appl-tc-012","How does Combine framework compare to RxSwift? What are the key concepts?","medium",["Combine","Reactive programming","Publisher/Subscriber","Operators"],["Not understanding backpressure","Confusing with closures"]),
]
for q in appl_tc:
    d = expand_tc(*q); d["company_id"] = "apple"; d["company"] = "Apple"; QUESTIONS.append(d)

appl_cd = [
("appl-cd-001","Given a sorted array and a target, implement binary search.","easy","O(log n)","O(1)",["array","binary-search"],[{"input":"[-1,0,3,5,9,12], target=9","output":"4"}]),
("appl-cd-002","Implement a function to compute the Fibonacci sequence efficiently.","easy","O(n)","O(1)",["dp","math"],[{"input":"n=10","output":"55"}]),
("appl-cd-003","Find the intersection of two arrays.","easy","O(n+m)","O(min(n,m))",["array","hashset"],[{"input":"[1,2,2,1], [2,2]","output":"[2]"}]),
("appl-cd-004","Given a string, find the first unique character and return its index.","easy","O(n)","O(1)",["string","hashmap"],[{"input":"leetcode","output":"0"},{"input":"loveleetcode","output":"2"}]),
("appl-cd-005","Reverse words in a string while preserving whitespace.","medium","O(n)","O(n)",["string"],[{"input":"the sky is blue","output":"blue is sky the"}]),
("appl-cd-006","Find peak element in an array (element greater than neighbors).","medium","O(log n)","O(1)",["array","binary-search"],[{"input":"[1,2,3,1]","output":"2 (index of 3)"}]),
("appl-cd-007","Given a binary tree, find its maximum depth.","easy","O(n)","O(h)",["tree","DFS","recursion"],[{"input":"[3,9,20,null,null,15,7]","output":"3"}]),
("appl-cd-008","Implement pow(x, n) without using built-in functions.","medium","O(log n)","O(1)",["math","recursion"],[{"input":"x=2.0, n=10","output":"1024.0"}]),
("appl-cd-009","Find all duplicate numbers in an array where values are between 1 and n.","medium","O(n)","O(1)",["array","cycle-detection"],[{"input":"[4,3,2,7,8,2,3,1]","output":"[2,3]"}]),
("appl-cd-010","Given a string, check if it is a valid palindrome ignoring non-alphanumeric chars.","easy","O(n)","O(1)",["string","two-pointers"],[{"input":"A man, a plan, a canal: Panama","output":"True"}]),
("appl-cd-011","Merge two sorted linked lists into one sorted list.","easy","O(n+m)","O(1)",["linked-list","recursion"],[{"input":"1->2->4, 1->3->4","output":"1->1->2->3->4->4"}]),
("appl-cd-012","Design a Tic-Tac-Toe game with O(1) move time check for winner.","medium","O(1) per move","O(n)",["design","array"],[{"input":"Moves on 3x3 board","output":"X wins or Draw"}]),
]
for q in appl_cd:
    d = expand_cd(*q); d["company_id"] = "apple"; d["company"] = "Apple"; QUESTIONS.append(d)

appl_sd = [
("appl-sd-001","Design iCloud sync service for seamless data synchronization across Apple devices.","hard",["Sync service","Conflict resolution","Delta sync","Key-value store","Identity service"],["Multi-device sync","Low latency","Offline support","Privacy-first"],"1B+ devices"),
("appl-sd-002","Design Apple Maps with turn-by-turn navigation, traffic, and transit directions.","hard",["Map rendering","Routing engine","Traffic pipeline","POI service","Navigation"],["Global coverage","Real-time traffic","Privacy","Offline maps"],"100M+ MAU"),
("appl-sd-003","Design App Store serving billions of app downloads globally with content delivery.","hard",["App storage","CDN","Review pipeline","Recommendation","Payment processing"],["Large binary distribution","Global CDN","Review latency","App discovery"],"500M+ weekly visitors"),
("appl-sd-004","Design a system for Apple Pay handling millions of contactless transactions daily.","hard",["Payment processing","Tokenization","NFC backend","Fraud detection","Device auth"],["Transaction latency","Security","Merchant integration","Compliance"],"100M+ daily transactions"),
("appl-sd-005","Design AirDrop for peer-to-peer file transfer with proximity detection.","medium",["Bonjour","Wi-Fi Direct","BLE","Transfer service","Security"],["Proximity detection","Cross-platform limitations","File size limits","Privacy"],"100M+ daily transfers"),
("appl-sd-006","Design Apple Push Notification service (APNs) for billions of notifications.","medium",["APNs gateway","Connection management","Notification queue","Device token service","Feedback"],["Connection persistence","Notification priority","Battery impact","Delivery guarantees"],"10B+ notifications daily"),
]
for q in appl_sd:
    d = expand_sd(*q); d["company_id"] = "apple"; d["company"] = "Apple"; QUESTIONS.append(d)
# -------------------------------------------
# NETFLIX
# -------------------------------------------
nflx_bh = [
("nflx-bh-001","Describe a time you had to make a decision with limited information. How did you handle the ambiguity?","medium","Describe ambiguous decision","Explain missing info","Show decision framework","Share outcome","Analysis paralysis, Waiting for perfect info",""),
("nflx-bh-002","Tell me about a time you gave honest, direct feedback that was difficult to deliver.","hard","Describe difficult feedback situation","Explain why it was needed","Show direct communication style","Share how it was received","Sugar-coating, Avoiding tough conversations",""),
("nflx-bh-003","Give an example of a time you took a calculated risk that paid off significantly.", "medium","Describe a calculated risk","Explain your analysis","Show how you measured risk vs reward","Share the payoff","Reckless risk-taking, Not having data",""),
("nflx-bh-004","Describe a situation where you had to challenge the status quo to improve a process.","medium","Describe an inefficient status quo","Explain why it needed to change","Show how you challenged it","Share the improvement","Accepting inefficiency, Not speaking up",""),
("nflx-bh-005","Tell me about a time when you had to hire someone who was significantly better than you at something.","medium","Describe hiring a star","Explain what made them exceptional","Show how you recruited them","Share the impact they had","Feeling threatened, Not hiring strong people",""),
("nflx-bh-006","Describe how you approach making your team more efficient. Give a concrete example.","medium","Describe team inefficiency","Explain your improvement approach","Show what you changed","Share the efficiency gain","Micromanaging, Not delegating",""),
("nflx-bh-007","Tell me about a time you had to let someone go or deliver news they did not want to hear.","hard","Describe a tough personnel conversation","Explain the situation","Show your approach to candor","Share the outcome","Avoiding the conversation, Being cruel",""),
("nflx-bh-008","Give an example of when you had to rapidly adapt your strategy based on market feedback.","medium","Describe strategy pivot","Explain the feedback received","Show how you adapted quickly","Share the improved result","Resisting change, Slow to adapt",""),
("nflx-bh-009","Describe a time you worked on something with high ambiguity where the outcome was not clear.","medium","Describe ambiguous project","Explain the uncertainty","Show how you made progress","Share the eventual clarity","Waiting for certainty, Not making progress",""),
("nflx-bh-010","Tell me about a time you had to advocate for a bold idea that others were skeptical about.","hard","Describe a bold idea","Explain the skepticism","Show how you built conviction","Share the result","Giving up on idea, Not gathering evidence",""),
]
for q in nflx_bh:
    d = expand_bh(*q); d["company_id"] = "netflix"; d["company"] = "Netflix"; QUESTIONS.append(d)

nflx_tc = [
("nflx-tc-001","Explain how Netflix adaptive bitrate streaming works. What algorithms are used for bitrate selection?","hard",["Adaptive streaming","ABR algorithms","Buffer-based","Throughput-based","MPEG-DASH"],["Not understanding buffer occupancy","Ignoring startup delay vs quality"]),
("nflx-tc-002","How does Netflix CDN (Open Connect) work? Why did they build their own CDN?","hard",["Open Connect","CDN architecture","ISP peering","Caching strategy"],["Not understanding ISP cost savings","Comparing to generic CDNs"]),
("nflx-tc-003","Describe Netflix chaos engineering approach. How does Chaos Monkey improve reliability?","medium",["Chaos engineering","Chaos Monkey","Fault tolerance","Resilience testing"],["Thinking it is just random killing","Not understanding blast radius"]),
("nflx-tc-004","How does Netflix handle personalization and recommendations at scale?","medium",["Recommendation system","Matrix factorization","Deep learning","A/B testing"],["Oversimplifying algo","Not understanding cold start"]),
("nflx-tc-005","Explain the Netflix microservices architecture. How do they handle service discovery?","medium",["Microservices","Eureka","Service discovery","API gateway","Circuit breaker"],["Not understanding Hystrix patterns","Ignoring fallback handling"]),
("nflx-tc-006","How does Netflix encode videos efficiently? Explain per-title encoding optimization.","hard",["Video encoding","Per-title encoding","Codec selection","Bitrate ladder"],["Fixed bitrate ladder","Not understanding content complexity variation"]),
("nflx-tc-007","Describe how Netflix migrated from datacenter to AWS. What were the key challenges?","hard",["Cloud migration","AWS","Database migration","Network topology","Resilience"],["Not understanding network costs","Lift-and-shift approach"]),
("nflx-tc-008","How does Netflix Zuul gateway work? What role does it play in the architecture?","medium",["Zuul","API gateway","Routing","Filter chain","Request tracing"],["Confusing with simple reverse proxy","Not understanding filter architecture"]),
]
for q in nflx_tc:
    d = expand_tc(*q); d["company_id"] = "netflix"; d["company"] = "Netflix"; QUESTIONS.append(d)

nflx_cd = [
("nflx-cd-001","Given a string, find the longest substring with at most two distinct characters.","medium","O(n)","O(1)",["string","sliding-window"],[{"input":"eceba","output":"3 (ece)"}]),
("nflx-cd-002","Implement a circular queue using an array.","medium","O(1)","O(n)",["array","design","queue"],[{"input":"MyCircularQueue(3), enQueue(1), enQueue(2), enQueue(3), enQueue(4)","output":"True,True,True,False"}]),
("nflx-cd-003","Given a 2D grid, find if there is a path from top-left to bottom-right that avoids obstacles.","medium","O(m*n)","O(m*n)",["graph","DFS","BFS"],[{"input":"grid=[[0,0,0],[0,1,0],[0,0,0]]","output":"True"}]),
("nflx-cd-004","Given a list of integers, find the longest increasing subsequence.","medium","O(n log n)","O(n)",["dp","binary-search"],[{"input":"[10,9,2,5,3,7,101,18]","output":"4 (2,3,7,101)"}]),
("nflx-cd-005","Encode and decode a list of strings (run-length style encoding).","medium","O(n)","O(n)",["string","design"],[{"input":"[hello,world,leetcode]","output":"Encoded then decoded back"}]),
("nflx-cd-006","Design a time-based key-value store that supports get at specific timestamps.","medium","O(log n) for get","O(n)",["hashmap","binary-search","design"],[{"input":"set(foo,bar,1), get(foo,1), get(foo,3)","output":"bar, bar"}]),
("nflx-cd-007","Find the minimum in a rotated sorted array.","medium","O(log n)","O(1)",["array","binary-search"],[{"input":"[3,4,5,1,2]","output":"1"}]),
("nflx-cd-008","Implement a function to shuffle an array uniformly.","medium","O(n)","O(1)",["array","random"],[{"input":"[1,2,3,4,5]","output":"Random permutation"}]),
]
for q in nflx_cd:
    d = expand_cd(*q); d["company_id"] = "netflix"; d["company"] = "Netflix"; QUESTIONS.append(d)

nflx_sd = [
("nflx-sd-001","Design Netflix streaming service delivering content to 200M+ subscribers globally.","hard",["Content delivery","CDN (Open Connect)","Recommendation service","User profile","DRM"],["Global streaming","Adaptive bitrate","Personalization","Content licensing"],"200M+ subscribers"),
("nflx-sd-002","Design Netflix recommendation system serving personalized content to millions.","hard",["Recommendation pipeline","ML models","Feature store","A/B testing","Real-time inference"],["Real-time vs batch","Cold start","Diversity","Freshness"],"200M+ personalized feeds"),
("nflx-sd-003","Design Netflix video upload and transcoding pipeline for content producers.","medium",["Upload service","Transcoding pipeline","Quality analysis","Storage management","Metadata service"],["Format support","Encoding efficiency","Quality assurance","Storage optimization"],"1000+ hours uploaded daily"),
("nflx-sd-004","Design a global membership and billing system with multi-currency support.","medium",["Account service","Payment processing","Billing pipeline","Tax service","Subscription management"],["Multi-currency","Proration","Plan changes","Dunning"],"200M+ accounts"),
("nflx-sd-005","Design a distributed caching layer for user session data across global regions.","medium",["Cache cluster","Data replication","Consistency","Eviction policy","Regional routing"],["Global consistency","Cache efficiency","Failover","Warm-up"],"200M+ users"),
("nflx-sd-006","Design a system for A/B testing at Netflix scale with statistical rigor.","medium",["Experiment platform","Traffic splitting","Metrics pipeline","Statistical analysis","Feature flags"],["Traffic allocation","Metric selection","Sample size","Long-running experiments"],"1000+ concurrent experiments"),
]
for q in nflx_sd:
    d = expand_sd(*q); d["company_id"] = "netflix"; d["company"] = "Netflix"; QUESTIONS.append(d)
# -------------------------------------------
# STRIPE
# -------------------------------------------
strp_bh = [
("strp-bh-001","Describe a time you had to balance developer experience with strict correctness and reliability.","hard","Describe DX vs correctness tension","Explain the trade-off","Show how you balanced both","Share the outcome","Prioritizing DX over correctness, Ignoring edge cases",""),
("strp-bh-002","Tell me about a time you designed an API that other developers loved. What made it great?","medium","Describe API design","Explain developers needs","Show design principles applied","Share developer feedback","Not considering DX, Inconsistent design",""),
("strp-bh-003","Give an example of when you had to debug a really subtle production issue. How did you find it?","hard","Describe a subtle bug","Explain why it was hard to find","Show systematic debugging","Share root cause","Giving up, Not using data",""),
("strp-bh-004","Describe a time you had to make a service more reliable. What metrics did you improve?","medium","Describe reliability challenge","Explain the reliability gap","Show improvements made","Share reliability metrics","Not measuring, Surface-level fixes",""),
("strp-bh-005","Tell me about a time you advocated for a significant infrastructure investment. How did you get buy-in?","medium","Describe infrastructure need","Explain the ROI","Show business case","Share the approval","Not quantifying impact, Asking without data",""),
("strp-bh-006","Describe a situation where a system failed and you led the incident response.","hard","Describe a production incident","Explain the impact","Show incident response leadership","Share post-mortem and changes","Not having a plan, Blaming individuals",""),
("strp-bh-007","Tell me about a time you had to simplify a complex system for better maintainability.","medium","Describe over-complex system","Explain why simplicity mattered","Show refactoring approach","Share maintainability improvement","Over-engineering, Not reducing complexity",""),
("strp-bh-008","Give an example of a time you had to address a security vulnerability. How did you handle it?","hard","Describe a security finding","Explain the risk","Show remediation approach","Share security improvement","Not disclosing properly, Ignoring severity",""),
]
for q in strp_bh:
    d = expand_bh(*q); d["company_id"] = "stripe"; d["company"] = "Stripe"; QUESTIONS.append(d)

strp_tc = [
("strp-tc-001","Explain how Stripe API handles idempotency. Why is it critical for payment processing?","medium",["Idempotency","API design","Payment idempotency","Retry safety"],["Not understanding idempotency keys","Ignoring concurrency"]),
("strp-tc-002","How does Stripe handle PCI compliance? What is tokenization and how does it reduce scope?","hard",["PCI DSS","Tokenization","Card data handling","SAQ A"],["Not understanding PCI scope","Storing sensitive data unnecessarily"]),
("strp-tc-003","Explain the concept of webhooks in Stripe. How do you ensure reliable delivery?","medium",["Webhooks","Event-driven architecture","Retry logic","Idempotency"],["Not handling duplicates", "Ignoring signature verification"]),
("strp-tc-004","How would you design a system that detects fraudulent transactions in real-time?","hard",["Fraud detection","ML models","Real-time scoring","Rule engine"],["High false positives","Not considering latency"]),
("strp-tc-005","Explain how Stripe Connect works for marketplace payments. Handling money movement?","hard",["Stripe Connect","Platform payments","Payouts","Split payments"],["Not understanding money flow","Ignoring regulatory requirements"]),
("strp-tc-006","How does Stripe handle multi-currency settlement and foreign exchange?","medium",["FX","Multi-currency","Settlement","Conversion rates"],["Not understanding FX fees","Ignoring settlement timing"]),
("strp-tc-007","Describe how you would build a scalable billing system that handles proration and plans.","medium",["Billing","Proration","Subscription management","Invoice generation"],["Not handling edge cases","Proration math errors"]),
("strp-tc-008","How does Stripe Radar work for fraud prevention using ML?","medium",["Stripe Radar","ML fraud","Risk scoring","Supervised learning"],["Not understanding feature engineering","Ignoring model drift"]),
("strp-tc-009","Explain how payment gateway to processor communication works. Card networks involved?","medium",["Payment gateway","Acquirer","Card networks","Settlement"],["Confusing gateway with processor","Not understanding settlement timing"]),
("strp-tc-010","How does Stripe handle API versioning and backwards compatibility?","medium",["API versioning","Backward compatibility","Migration","Deprecation"],["Breaking changes","Not communicating deprecation timeline"]),
]
for q in strp_tc:
    d = expand_tc(*q); d["company_id"] = "stripe"; d["company"] = "Stripe"; QUESTIONS.append(d)

strp_cd = [
("strp-cd-001","Given an array, move all even numbers to the front while maintaining relative order of odds.","easy","O(n)","O(n)",["array"],[{"input":"[3,1,2,4]","output":"[2,4,3,1] or [4,2,3,1]"}]),
("strp-cd-002","Implement a function that validates a credit card number using Luhn algorithm.","easy","O(n)","O(1)",["string","math"],[{"input":"4532015112830366","output":"True"}]),
("strp-cd-003","Design a rate limiter that allows N requests per second with burst support.","medium","O(1)","O(window)",["design","system-design"],[{"input":"RateLimiter(10, 1s), 10 requests in 0.1s","output":"Burst allowed, 11th blocked"}]),
("strp-cd-004","Given an array of stock prices, find the maximum profit from one buy and one sell.","easy","O(n)","O(1)",["array","dp"],[{"input":"[7,1,5,3,6,4]","output":"5"}]),
("strp-cd-005","Implement an idempotent API handler that detects and handles duplicate requests.","medium","O(1)","O(n)",["design","hashmap"],[{"input":"process(idempotency_key=X, request), same request again","output":"Same response returned"}]),
("strp-cd-006","Given a list of transactions with amounts, find pairs that sum to a suspicious threshold.","medium","O(n)","O(n)",["array","hashmap","two-pointers"],[{"input":"[100,250,150,300,200], target=400","output":"[(100,300),(150,250)]"}]),
("strp-cd-007","Design a URL shortener with custom alias support and expiration.","medium","O(1)","O(n)",["design","hashmap"],[{"input":"shorten(https://example.com, custom=stripe)","output":"https://short.url/stripe"}]),
("strp-cd-008","Given an integer n, count how many distinct ways to climb n stairs using 1 or 2 steps.","easy","O(n)","O(1)",["dp","math"],[{"input":"n=3","output":"3"},{"input":"n=5","output":"8"}]),
("strp-cd-009","Implement a simple key-value store with transactions (begin, commit, rollback).","hard","O(1) avg","O(n)",["design","stack","hashmap"],[{"input":"begin, set(a,1), begin, set(a,2), rollback, get(a)","output":"1"}]),
("strp-cd-010","Given a list of version strings, sort them using semantic versioning rules.","medium","O(n log n)","O(n)",["sorting","string"],[{"input":"[1.0.0, 2.0.0, 1.5.0, 1.0.1]","output":"[1.0.0, 1.0.1, 1.5.0, 2.0.0]"}]),
("strp-cd-011","Design a webhook delivery system with retries, idempotency, and logging.","medium","O(n) storage","O(n)",["design","queue"],[{"input":"deliver(webhook_url, payload)","output":"200 OK or retry"}]),
("strp-cd-012","Calculate the total amount including tax for items with different tax rates.","easy","O(n)","O(1)",["math"],[{"input":"items=[(100,0.1),(200,0.08)], currency=USD","output":"326"}]),
]
for q in strp_cd:
    d = expand_cd(*q); d["company_id"] = "stripe"; d["company"] = "Stripe"; QUESTIONS.append(d)

strp_sd = [
("strp-sd-001","Design Stripe payment processing system handling millions of transactions daily with 99.99% uptime.","hard",["Payment API","Transaction service","Ledger","Fraud detection","Payout service"],["Exactly-once processing","Multi-region","Compliance","Latency under 100ms"],"100M+ API requests daily"),
("strp-sd-002","Design Stripe Connect platform for marketplace payments and split payments.","hard",["Connect API","Account management","Split payments","Payout service","KYC verification"],["Complex money movement","Onboarding flow","Regulatory compliance","Dispute handling"],"1M+ connected accounts"),
("strp-sd-003","Design Stripe Billing for subscription management with proration and invoices.","medium",["Subscription service","Invoice generation","Proration engine","Payment collection","Dunning"],["Recurring billing","Proration accuracy","Failed payment retries","Usage-based billing"],"100K+ businesses"),
("strp-sd-004","Design Stripe Radar ML-based fraud detection system processing in real-time.","medium",["Feature pipeline","ML model","Risk scoring","Rule engine","Dashboard"],["Real-time scoring","Low false positive","Model updates","Interpretability"],"100M+ transactions analyzed"),
("strp-sd-005","Design a webhook delivery system guaranteeing at-least-once delivery with idempotency.","medium",["Webhook engine","Queue","Delivery worker","Retry logic","Logging"],["Delivery guarantees","Signature verification","Rate limiting","Dead letter queue"],"1B+ webhook events daily"),
("strp-sd-006","Design Stripe Dashboard for real-time analytics and reporting on payment data.","medium",["Analytics pipeline","Query service","Data warehouse","Caching","Export service"],["Real-time updates","Complex aggregations","Multi-currency reporting","Data freshness"],"100K+ merchants"),
]
for q in strp_sd:
    d = expand_sd(*q); d["company_id"] = "stripe"; d["company"] = "Stripe"; QUESTIONS.append(d)
# -------------------------------------------
# UBER
# -------------------------------------------
uber_bh = [
("uber-bh-001","Describe a time you had to balance growth with reliability. How did you approach the trade-off?","hard","Balance growth and reliability","Explain the tension","Show how you managed both","Share the outcome","Prioritizing growth over reliability, Not communicating risk",""),
("uber-bh-002","Tell me about a time you optimized a system for cost without sacrificing quality.","medium","Describe cost optimization","Explain the cost issue","Show optimization approach","Share cost savings","Saving cost at quality expense, Not measuring impact",""),
("uber-bh-003","Give an example of when a project you were working on needed to be deprioritized. How did you handle it?","medium","Describe a deprioritized project","Explain why it was cut","Show how you handled it professionally","Share what you learned","Taking it personally, Not understanding business reasons",""),
("uber-bh-004","Describe a time you had to make a quick decision in a high-stakes situation.","hard","Describe high-stakes decision","Explain the urgency","Show quick decision-making","Share the outcome","Overthinking, Not deciding",""),
("uber-bh-005","Tell me about a time you had to get multiple teams aligned on a shared goal. How did you do it?","medium","Describe cross-team alignment","Explain conflicting priorities","Show alignment strategy","Share the unified outcome","Working in silos, Not involving stakeholders early",""),
("uber-bh-006","Describe how you measure success in your work. Give a specific example of a metric you improved.","medium","Describe success measurement","Explain the metric","Show how you moved it","Share the quantified impact","Not defining success, Vanity metrics",""),
("uber-bh-007","Tell me about a time you identified a growth opportunity that others had missed.","medium","Describe a missed opportunity","Explain why it was overlooked","Show how you pursued it","Share the growth impact","Not thinking big, Ignoring data",""),
("uber-bh-008","Give an example of a time when you had to navigate a complex political situation at work.","hard","Describe workplace politics","Explain the complexity","Show how you navigated it","Share the resolution","Getting involved in drama, Not staying professional",""),
]
for q in uber_bh:
    d = expand_bh(*q); d["company_id"] = "uber"; d["company"] = "Uber"; QUESTIONS.append(d)

uber_tc = [
("uber-tc-001","Explain how Uber matches riders with drivers. Describe the geo-spatial indexing used.","hard",["Geo-spatial indexing","H3 grid","Quadtree","Dispatching"],["Not understanding geohashing","Ignoring supply-demand balance"]),
("uber-tc-002","How does Uber calculate ETAs? What factors influence the estimation?","medium",["ETA prediction","ML models","Traffic data","Historical patterns"],["Static estimation","Not considering real-time conditions"]),
("uber-tc-003","Describe Uber surge pricing algorithm. How does it balance supply and demand?","medium",["Surge pricing","Supply-demand","Dynamic pricing","Elasticity"],["Not understanding elasticity","Ignoring user fairness concerns"]),
("uber-tc-004","How does Uber handle real-time location tracking across millions of devices?","hard",["GPS tracking","WebSocket","Location ingestion","Geofencing"],["High data volume","Not handling GPS inaccuracies"]),
("uber-tc-005","Explain how Uber maps work for navigation and traffic prediction.","medium",["Map data","Routing","Traffic prediction","Map matching"],["Not understanding map matching","Ignoring road closures"]),
("uber-tc-006","How does UberEATS order routing work? How do you optimize delivery time?","medium",["Order routing","Batching","ETA optimization","Restaurant integration"],["Not considering preparation time","Inefficient batching"]),
("uber-tc-007","Describe how Uber Trip Pricing API works. How much does Uber take as commission?","medium",["Pricing model","Commission","Dynamic pricing","Receipt"],["Not understanding pricing breakdown","Confusing net with gross"]),
("uber-tc-008","How does Uber handle payments across different countries with different payment methods?","medium",["Payment processing","Multi-currency","Local payment methods","Compliance"],["Not supporting local methods","Ignoring regulatory differences"]),
("uber-tc-009","Explain the architecture of Uber push notifications for real-time trip updates.","easy",["Push notifications","Real-time updates","Driver/rider communication"],["Delayed delivery", "Battery impact"]),
("uber-tc-010","How does Uber manage driver incentives and promotions? Describe the system.","medium",["Incentive system","Promotions","Earnings calculation","Fraud detection"],["Gaming incentives", "Not measuring ROI"]),
]
for q in uber_tc:
    d = expand_tc(*q); d["company_id"] = "uber"; d["company"] = "Uber"; QUESTIONS.append(d)

uber_cd = [
("uber-cd-001","Given a list of coordinates, find the closest pair of points.","medium","O(n log n)","O(n)",["geometry","divide-and-conquer"],[{"input":"[(1,2),(3,4),(5,6)]","output":"Euclidean distance"}]),
("uber-cd-002","Design a function that calculates the fare based on distance, time, and surge pricing.","medium","O(1)","O(1)",["math","design"],[{"input":"distance=10km, time=15min, surge=1.5","output":"$X"}]),
("uber-cd-003","Given a directed graph of cities and roads, find the shortest path between two cities.","medium","O(V+E log V)","O(V)",["graph","Dijkstra"],[{"input":"Graph with 5 cities, A to E","output":"Shortest path"}]),
("uber-cd-004","Find all drivers within a given radius of a pickup location.","medium","O(n)","O(n)",["geometry","hashmap"],[{"input":"drivers=[(lat,lng)...], center, radius=2km","output":"Drivers within radius"}]),
("uber-cd-005","Given delivery orders with pickup and dropoff, find the optimal route for a driver.","hard","O(n!)","O(n)",["graph","DFS","greedy"],[{"input":"3 orders with pickup/dropoff","output":"Optimal sequence"}]),
("uber-cd-006","Implement a rate limiter specific to surge pricing triggers.","medium","O(1) per check","O(n)",["design","system-design"],[{"input":"10 requests for surge check in 1 second","output":"Only first 5 processed"}]),
("uber-cd-007","Given a stream of GPS coordinates, detect if a driver is deviating from the route.","easy","O(n)","O(1)",["geometry","array"],[{"input":"Expected route vs actual GPS path","output":"Deviation detected if >50m off"}]),
("uber-cd-008","Calculate the estimated time of arrival given current traffic conditions.","medium","O(n)","O(n)",["graph","math"],[{"input":"Route distance=10km, avg speed=30km/h, traffic factor=1.2","output":"24 minutes"}]),
("uber-cd-009","Given an array of daily ride counts, find the day with the maximum growth rate.","easy","O(n)","O(1)",["array","math"],[{"input":"[100,120,150,140,200]","output":"Day 4 (200-140)/140=42.8%"}]),
("uber-cd-010","Design a matching algorithm that assigns riders to the nearest available driver.","medium","O(n log n)","O(n)",["algorithm","design"],[{"input":"3 riders, 3 drivers with locations","output":"Optimal assignment"}]),
("uber-cd-011","Given a list of trips, find the most frequent route (origin-destination pair).","easy","O(n)","O(n)",["hashmap","array"],[{"input":"[(A,B),(B,C),(A,B)]","output":"(A,B): 2 times"}]),
("uber-cd-012","Implement a trip history system that supports pagination and date filtering.","medium","O(n)","O(1)",["design","array"],[{"input":"user=123, page=1, pageSize=10","output":"10 most recent trips"}]),
]
for q in uber_cd:
    d = expand_cd(*q); d["company_id"] = "uber"; d["company"] = "Uber"; QUESTIONS.append(d)

uber_sd = [
("uber-sd-001","Design Uber dispatch system matching millions of riders to drivers in real-time.","hard",["Dispatch engine","Geo-index","ETA service","Surge pricing","Matching algorithm"],["Real-time matching","Load balancing","Geospatial at scale","Fairness"],"25M+ trips daily"),
("uber-sd-002","Design UberEATS platform for food delivery from order to doorstep.","hard",["Order service","Restaurant platform","Dispatch","Tracking","Payment"],["Real-time tracking","Delivery optimization","Restaurant integration","Quality control"],"10M+ orders daily"),
("uber-sd-003","Design Uber pricing engine handling surge pricing, promotions, and estimates.","medium",["Pricing service","Surge detection","Promotion engine","Estimation API"],["Dynamic pricing","Promotion fraud","Real-time updates","A/B testing"],"25M+ price estimates daily"),
("uber-sd-004","Design Uber driver onboarding and background check system.","medium",["Application service","Document verification","Background check","Training","Go live"],["Document validation","Background check latency","Regulatory compliance","Fraud detection"],"1M+ driver applications yearly"),
("uber-sd-005","Design Uber Safety Toolkit with emergency sharing and incident response.","medium",["Safety service","Trip sharing","Incident detection","Emergency response","Trust & Safety"],["Real-time monitoring","Privacy","False alarms","Law enforcement coordination"],"25M+ daily trips monitored"),
("uber-sd-006","Design a real-time pricing and marketplace system for Uber Freight.","hard",["Load matching","Pricing engine","Carrier network","Tracking","Payment"],["Supply-demand matching","Bidding system","Real-time tracking","Document management"],"100K+ loads daily"),
]
for q in uber_sd:
    d = expand_sd(*q); d["company_id"] = "uber"; d["company"] = "Uber"; QUESTIONS.append(d)

# -------------------------------------------
# AIRBNB
# -------------------------------------------
abnb_bh = [
("abnb-bh-001","Tell me about a time you designed a product for a global audience with diverse needs.","medium","Design for diverse users","Explain the diversity challenge","Show inclusive design approach","Share global impact","Ignoring cultural differences, Not doing user research",""),
("abnb-bh-002","Describe a time you used data to improve a customer experience. What metric improved?","medium","Use data for CX improvement","Explain the customer pain point","Show data-driven approach","Share metric improvement","Not having baseline, Vanity metrics",""),
("abnb-bh-003","Give an example of a time you built trust with users through product decisions.","medium","Build user trust","Explain the trust challenge","Show trust-building decisions","Share trust improvement","Misleading users, Dark patterns",""),
("abnb-bh-004","Describe a time you had to balance the needs of two different user groups (hosts and guests).","hard","Balance host vs guest needs","Explain the conflicting needs","Show how you balanced them","Share the win-win outcome","Biasing one group, Ignoring trade-offs",""),
("abnb-bh-005","Tell me about a time you had to make a decision that prioritized the community over short-term profits.","medium","Community vs profit decision","Explain the tension","Show community-first decision","Share long-term benefit","Short-term thinking, Not valuing community",""),
("abnb-bh-006","Describe how you approach creating a sense of belonging in products you build.","medium","Create belonging through product","Explain belonging concept","Show specific features","Share user feedback","Treating belonging as checkbox, Not authentic",""),
("abnb-bh-007","Give an example of a time you simplified a complex process or flow for users.","medium","Simplify user flow","Explain the complexity","Show simplification approach","Share improved user metrics","Adding more steps, Not testing with users",""),
("abnb-bh-008","Tell me about a time you advocated for a feature that had uncertain ROI but was the right thing to do.","medium","Advocate uncertain but right feature","Explain the uncertainty","Show advocacy approach","Share the impact","Only data-driven decisions, Ignoring intuition",""),
]
for q in abnb_bh:
    d = expand_bh(*q); d["company_id"] = "airbnb"; d["company"] = "Airbnb"; QUESTIONS.append(d)

abnb_tc = [
("abnb-tc-001","Explain how Airbnb search ranking works. What signals determine listing position?","hard",["Search ranking","Listing features","User signals","ML ranking"],["Not understanding personalization","Ignoring recency"]),
("abnb-tc-002","How does Airbnb handle payments between hosts and guests? Describe the payment flow.","medium",["Payment processing","Escrow","Payouts","Dispute handling"],["Not understanding release timing","Ignoring FX"]),
("abnb-tc-003","Describe how Airbnb detection system works for party prevention and trust.","medium",["Trust systems","Risk detection","ML models","Rule engine"],["False positives","Not understanding user behavior patterns"]),
("abnb-tc-004","How does Airbnb manage calendar availability and booking conflicts?","medium",["Calendar service","Availability","Booking lock","Conflict resolution"],["Race conditions","Not handling timezones"]),
("abnb-tc-005","Explain how Airbnb reviews and ratings system works. How is it kept fair?","medium",["Review system","Rating bias","Double-blind","Fraud detection"],["Review bombing","Not handling retaliatory reviews"]),
("abnb-tc-006","How does Airbnb handle image uploads and processing for listing photos?","easy",["Image processing","CDN","Thumbnail generation","Content moderation"],["Not optimizing image sizes","Ignoring moderation"]),
("abnb-tc-007","Describe the architecture behind Airbnb instant book feature.","medium",["Instant book","Booking service","Host settings","Payment auth"],["Availability race conditions","Not handling host overrides"]),
("abnb-tc-008","How does Airbnb manage pricing recommendations for hosts using ML?","medium",["Smart pricing","ML pricing","Seasonality","Demand prediction"],["Overpricing recommendations","Not understanding local factors"]),
]
for q in abnb_tc:
    d = expand_tc(*q); d["company_id"] = "airbnb"; d["company"] = "Airbnb"; QUESTIONS.append(d)

abnb_cd = [
("abnb-cd-001","Given availability calendars, find overlapping availability for a group booking.","medium","O(n*k)","O(k)",["array","intervals"],[{"input":"3 listings with date ranges","output":"Common available dates"}]),
("abnb-cd-002","Calculate the total cost of a stay including cleaning fees, service fees, and taxes.","easy","O(1)","O(1)",["math"],[{"input":"price=200/night, nights=5, cleaning=100, fees=10%","output":"Total calculation"}]),
("abnb-cd-003","Given a list of property locations, find the optimal property to recommend to a user.","medium","O(n)","O(n)",["algorithm","geometry"],[{"input":"User preferences + property list","output":"Top recommendation"}]),
("abnb-cd-004","Detect booking conflicts for a listing given existing bookings and a new request.","easy","O(n)","O(n)",["array","intervals"],[{"input":"Existing bookings + new request","output":"Has conflict or not"}]),
("abnb-cd-005","Implement a search filter that supports multiple criteria (price, dates, rooms, amenities).","medium","O(n)","O(n)",["design","array"],[{"input":"Listings + filter criteria","output":"Filtered listings"}]),
("abnb-cd-006","Given a set of reviews, calculate the average rating and confidence interval.","easy","O(n)","O(1)",["math","statistics"],[{"input":"Review scores: [5,4,5,3,4,5]","output":"Avg=4.33, 95% CI"}]),
("abnb-cd-007","Design a reservation system that prevents double booking using distributed locks.","hard","O(1)","O(1)",["design","distributed-systems"],[{"input":"Concurrent booking requests","output":"Exactly one succeeds"}]),
("abnb-cd-008","Given search history, recommend properties that similar users have booked.","medium","O(n log n)","O(n)",["algorithm","recommendation"],[{"input":"User search history","output":"Top 5 recommendations"}]),
("abnb-cd-009","Calculate the distance between two coordinates using the Haversine formula.","easy","O(1)","O(1)",["geometry","math"],[{"input":"lat1=37.77, lng1=-122.42, lat2=34.05, lng2=-118.25","output":"~550 km"}]),
("abnb-cd-010","Generate a dynamic pricing recommendation based on seasonality, demand, and listing features.","medium","O(1)","O(1)",["ml","math"],[{"input":"Listing data + market data","output":"Recommended price"}]),
]
for q in abnb_cd:
    d = expand_cd(*q); d["company_id"] = "airbnb"; d["company"] = "Airbnb"; QUESTIONS.append(d)

abnb_sd = [
("abnb-sd-001","Design Airbnb search engine handling millions of queries with filtering and ranking.","hard",["Search service","Indexing","Filter engine","Ranking service","Personalization"],["Low latency search","Global coverage","Personalized results","Availability filtering"],"500M+ searches monthly"),
("abnb-sd-002","Design Airbnb booking system preventing double bookings and handling payments.","hard",["Booking service","Payment service","Calendar service","Notification","Fraud detection"],["Race condition prevention","Payment escrow","Cancellation handling","Refunds"],"1M+ bookings nightly"),
("abnb-sd-003","Design Airbnb messaging platform for host-guest communication.","medium",["Message service","Real-time chat","Translation","Notification","Media sharing"],["Real-time delivery","Cross-language translation","Spam detection","Message history"],"100M+ messages daily"),
("abnb-sd-004","Design Airbnb review and rating system ensuring fairness and preventing abuse.","medium",["Review service","Rating calculation","Fraud detection","Double-blind","Reporting"],["Review fairness","Fraud detection","Double-blind timing","Response system"],"10M+ reviews yearly"),
("abnb-sd-005","Design a dynamic pricing engine for Airbnb hosts using ML.","medium",["Pricing engine","Demand prediction","Seasonality model","Competitor analysis","Optimization"],["Real-time pricing adjustments","Market data integration","Host acceptance","Revenue optimization"],"5M+ listings with smart pricing"),
("abnb-sd-006","Design Airbnb trust and safety system handling identity verification and risk.","hard",["Identity service","Document verification","Risk scoring","Background check","Trust signals"],["Global ID verification","Privacy","False positive rate","Fraud patterns"],"100M+ verifications"),
]
for q in abnb_sd:
    d = expand_sd(*q); d["company_id"] = "airbnb"; d["company"] = "Airbnb"; QUESTIONS.append(d)
# -------------------------------------------
# TCS
# -------------------------------------------
tcs_bh = [
("tcs-bh-001","Describe a time you worked effectively in a large team environment. How did you contribute?","easy","Describe team collaboration","Explain team size and structure","Show how you contributed","Share team success","Working in isolation, Not communicating",""),
("tcs-bh-002","Tell me about a time you had to learn a new technology quickly for a client project.","easy","Describe quick learning need","Explain client requirement","Show learning approach","Share successful delivery","Taking too long, Not asking for help",""),
("tcs-bh-003","Describe how you handled a situation where a client had unrealistic expectations.","medium","Describe unrealistic expectations","Explain what was unrealistic","Show expectation management","Share how you aligned","Overpromising, Not communicating constraints",""),
("tcs-bh-004","Tell me about a time you went beyond your job role to help a team member.","easy","Describe stepping beyond role","Explain why help was needed","Show how you assisted","Share positive impact","Not helping, Saying it is not my job",""),
("tcs-bh-005","Give an example of how you manage time when handling multiple project deliverables.","medium","Describe multiple deadlines","Explain the deliverables","Show time management skills","Share on-time delivery","Poor prioritization, Missing deadlines",""),
("tcs-bh-006","Describe a time you identified a process improvement opportunity and acted on it.","easy","Describe inefficiency","Explain the improvement opportunity","Show action taken","Share efficiency gain","Accepting inefficiency, Not taking initiative",""),
("tcs-bh-007","Tell me about a time you received appreciation from a client. What did you do?","easy","Describe client appreciation","Explain what you delivered","Show what earned appreciation","Share the recognition","Bragging, Not acknowledging team",""),
("tcs-bh-008","Describe how you ensure quality in your work. Give a specific example.","easy","Describe quality focus","Explain what was at stake","Show quality measures","Share defect-free delivery","Cutting corners, Not testing",""),
("tcs-bh-009","Tell me about a time you had to work with a team spread across different locations.","medium","Describe distributed team","Explain location challenges","Show collaboration approach","Share successful coordination","Communication gaps, Not considering timezones",""),
("tcs-bh-010","Give an example of how you stay updated with industry trends. How do you apply this learning?","easy","Describe staying current","Explain learning motivation","Show learning application","Share knowledge sharing","Stagnant learning, Not applying knowledge",""),
]
for q in tcs_bh:
    d = expand_bh(*q); d["company_id"] = "tcs"; d["company"] = "TCS"; QUESTIONS.append(d)

tcs_tc = [
("tcs-tc-001","Explain the difference between C and C++. When would you use each?","easy",["C vs C++","OOP","Procedural programming"],["Confusing C with C++","Not understanding memory management differences"]),
("tcs-tc-002","What is the difference between JDK, JRE, and JVM?","easy",["Java","JDK","JRE","JVM"],["Using interchangeably","Not understanding the hierarchy"]),
("tcs-tc-003","Explain SQL joins with examples. What is the difference between INNER and LEFT JOIN?","easy",["SQL","Joins","Relational databases"],["Not understanding NULL behavior","Confusing join types"]),
("tcs-tc-004","What is normalization in databases? Explain 1NF, 2NF, 3NF with examples.","medium",["Database normalization","Normal forms","Anomalies"],["Over-normalizing","Not understanding practical trade-offs"]),
("tcs-tc-005","Explain the OSI model layers. What protocols operate at each layer?","easy",["OSI model","TCP/IP","Protocols"],["Not relating to real-world protocols","Mixing layers"]),
("tcs-tc-006","What is the difference between abstract class and interface in Java?","easy",["Abstract class","Interface","Java OOP"],["Not understanding default methods","Confusing with multiple inheritance"]),
("tcs-tc-007","Explain ACID properties in database transactions.","easy",["ACID","Transactions","Atomicity","Consistency"],["Not understanding isolation levels","Confusing with CAP"]),
("tcs-tc-008","What are RESTful APIs? Explain the key principles.","easy",["REST","HTTP methods","Statelessness","Resource-based"],["Not implementing HATEOAS","Confusing REST with HTTP"]),
("tcs-tc-009","Explain the concept of multithreading. What are the challenges?","medium",["Multithreading","Concurrency","Race conditions","Synchronization"],["Not understanding deadlocks","Ignoring thread safety"]),
("tcs-tc-010","What is the difference between TCP and UDP? When to use each?","easy",["TCP vs UDP","Reliability","Latency"],["Not knowing real-world use cases","Confusing protocols"]),
("tcs-tc-011","Explain primary key vs unique key vs foreign key in SQL.","easy",["SQL keys","Primary key","Foreign key","Unique constraint"],["Not understanding NULL behavior","Confusing references"]),
("tcs-tc-012","What is the waterfall vs agile methodology? Compare them.","easy",["SDLC","Waterfall","Agile","Scrum"],["Thinking agile means no documentation","Not understanding when each fits"]),
("tcs-tc-013","Explain what a pointer is in C. How is it different from a reference in C++?","medium",["Pointers","Memory addresses","References"],["Not understanding pointer arithmetic","Confusing references with pointers"]),
("tcs-tc-014","Describe the Spring Boot framework. What are its key features?","easy",["Spring Boot","Auto-configuration","Dependency injection"],["Not understanding starter dependencies","Confusing with Spring MVC"]),
("tcs-tc-015","What is the difference between stacked and array data structure? Give use cases.","easy",["Stack","Array","Queue","Data structures"],["Not knowing real applications","Confusing LIFO/FIFO"]),
]
for q in tcs_tc:
    d = expand_tc(*q); d["company_id"] = "tcs"; d["company"] = "TCS"; QUESTIONS.append(d)

tcs_cd = [
("tcs-cd-001","Write a program to check if a number is prime.","easy","O(sqrt(n))","O(1)",["math"],[{"input":"n=17","output":"True"},{"input":"n=4","output":"False"}]),
("tcs-cd-002","Write a function to reverse a string without using built-in reverse.","easy","O(n)","O(n)",["string"],[{"input":"hello","output":"olleh"}]),
("tcs-cd-003","Find the factorial of a number using recursion.","easy","O(n)","O(n)",["recursion","math"],[{"input":"n=5","output":"120"}]),
("tcs-cd-004","Check if a string is a palindrome.","easy","O(n)","O(1)",["string","two-pointers"],[{"input":"racecar","output":"True"},{"input":"hello","output":"False"}]),
("tcs-cd-005","Find the largest element in an array.","easy","O(n)","O(1)",["array"],[{"input":"[3,7,2,9,1]","output":"9"}]),
("tcs-cd-006","Sort an array using bubble sort.","easy","O(n^2)","O(1)",["array","sorting"],[{"input":"[64,34,25,12,22,11,90]","output":"[11,12,22,25,34,64,90]"}]),
("tcs-cd-007","Implement binary search on a sorted array.","easy","O(log n)","O(1)",["array","binary-search"],[{"input":"[1,3,5,7,9], target=5","output":"2"}]),
("tcs-cd-008","Find the sum of digits of a number.","easy","O(log n)","O(1)",["math"],[{"input":"1234","output":"10"}]),
("tcs-cd-009","Check if two strings are anagrams.","easy","O(n)","O(1)",["string","hashmap"],[{"input":"listen, silent","output":"True"}]),
("tcs-cd-010","Print Fibonacci series up to n terms.","easy","O(n)","O(1)",["math","dp"],[{"input":"n=7","output":"0,1,1,2,3,5,8"}]),
]
for q in tcs_cd:
    d = expand_cd(*q); d["company_id"] = "tcs"; d["company"] = "TCS"; QUESTIONS.append(d)

tcs_sd = [
("tcs-sd-001","Design a banking system that handles customer accounts, transactions, and statements.","medium",["Account service","Transaction service","Statement generation","Security"],["Data consistency","Transaction isolation","Audit trail","Compliance"],"10M+ customers"),
("tcs-sd-002","Design a railway reservation system that prevents double booking.","medium",["Reservation service","PNR system","Payment gateway","Cancellation"],["Concurrent booking","Waitlist management","Seat allocation","Partial cancellation"],"100K+ daily bookings"),
("tcs-sd-003","Design a customer support ticket system for enterprise clients.","easy",["Ticket service","Queue","Assignment engine","SLA tracking","Knowledge base"],["SLA management","Escalation","Ticket routing","Reporting"],"50K+ tickets daily"),
]
for q in tcs_sd:
    d = expand_sd(*q); d["company_id"] = "tcs"; d["company"] = "TCS"; QUESTIONS.append(d)
# -------------------------------------------
# INFOSYS
# -------------------------------------------
infy_bh = [
("infy-bh-001","Describe a time you took initiative on a project without being asked.","easy","Describe taking initiative","Explain why you stepped up","Show what you did","Share the impact","Waiting to be told, Not proactive",""),
("infy-bh-002","Tell me about a time you solved a complex problem with an innovative approach.","medium","Describe a complex problem","Explain your innovative solution","Show your thinking process","Share the successful outcome","Conventional thinking, Not documenting approach",""),
("infy-bh-003","Describe how you handle working on repetitive tasks. How do you stay motivated?","easy","Describe repetitive work","Explain the challenge","Show how you stayed engaged","Share quality outcomes","Complaining, Losing motivation",""),
("infy-bh-004","Tell me about a time you effectively communicated technical information to a non-technical stakeholder.","easy","Describe technical communication","Explain the audience challenge","Show communication approach","Share understanding achieved","Using jargon, Not simplifying",""),
("infy-bh-005","Give an example of when you helped a junior colleague learn a new concept.","easy","Describe mentoring situation","Explain what you taught","Show teaching approach","Share colleague improvement","Being impatient, Not investing time",""),
("infy-bh-006","Describe a time you successfully managed a difficult client situation.","medium","Describe difficult client","Explain the challenge","Show client management skills","Share positive resolution","Ignoring client concerns, Escalating unnecessarily",""),
("infy-bh-007","Tell me about a time you had to adapt to a significant change in project requirements.","easy","Describe requirement change","Explain the impact","Show adaptability","Share successful adaptation","Resisting change, Not communicating",""),
("infy-bh-008","Describe how you keep your technical skills current. Give a specific example of new learning.","easy","Describe skill development","Explain learning motivation","Show learning methodology","Share application","Not learning, Outdated skills",""),
]
for q in infy_bh:
    d = expand_bh(*q); d["company_id"] = "infosys"; d["company"] = "Infosys"; QUESTIONS.append(d)

infy_tc = [
("infy-tc-001","Explain the difference between procedural and object-oriented programming.","easy",["Procedural","OOP","Paradigms"],["Not understanding encapsulation","Confusing paradigms"]),
("infy-tc-002","What is the difference between method overloading and method overriding?","easy",["Overloading","Overriding","Polymorphism"],["Using interchangeably","Not understanding compile vs runtime"]),
("infy-tc-003","Explain the four pillars of OOP with examples.","easy",["Encapsulation","Inheritance","Polymorphism","Abstraction"],["Not giving real examples","Confusing concepts"]),
("infy-tc-004","What is a deadlock in multithreading? How do you prevent it?","medium",["Deadlock","Thread synchronization","Lock ordering"],["Not understanding conditions for deadlock","Ignoring prevention strategies"]),
("infy-tc-005","Explain the difference between checked and unchecked exceptions in Java.","easy",["Java exceptions","Checked vs unchecked","Exception handling"],["Not understanding propagation","Overusing checked exceptions"]),
("infy-tc-006","What is the difference between WHERE and HAVING in SQL?","easy",["SQL","WHERE","HAVING","Filtering"],["Using HAVING without GROUP BY","Not understanding order of execution"]),
("infy-tc-007","Explain the concept of dependency injection. Why is it used?","medium",["DI","IoC","Loose coupling","Testability"],["Not understanding benefits","Overusing without need"]),
("infy-tc-008","What is the difference between HTTP GET and POST?","easy",["HTTP methods","GET vs POST","Idempotency"],["Not understanding semantics","Using POST for everything"]),
("infy-tc-009","Explain microservices vs monolithic architecture. Pros and cons.","medium",["Microservices","Monolith","Architecture patterns"],["Always recommending microservices","Not understanding complexity"]),
("infy-tc-010","What is the CAP theorem? Explain with examples.","medium",["CAP theorem","Consistency","Availability","Partition tolerance"],["Not understanding PACELC","Assuming CP always right"]),
("infy-tc-011","Explain how garbage collection works in Java.","medium",["Java GC","Heap","Generational GC","GC algorithms"],["Not understanding GC pauses","Tuning without understanding"]),
("infy-tc-012","What is a NoSQL database? When would you use MongoDB over MySQL?","medium",["NoSQL","MongoDB","MySQL","Document DB"],["Not understanding use cases","Claiming NoSQL always better"]),
]
for q in infy_tc:
    d = expand_tc(*q); d["company_id"] = "infosys"; d["company"] = "Infosys"; QUESTIONS.append(d)

infy_cd = [
("infy-cd-001","Find the second largest element in an array.","easy","O(n)","O(1)",["array"],[{"input":"[10,5,8,20,15]","output":"15"}]),
("infy-cd-002","Count vowels and consonants in a string.","easy","O(n)","O(1)",["string"],[{"input":"hello world","output":"vowels=3, consonants=7"}]),
("infy-cd-003","Remove duplicate elements from an array.","easy","O(n)","O(n)",["array","hashset"],[{"input":"[1,2,2,3,4,4,5]","output":"[1,2,3,4,5]"}]),
("infy-cd-004","Check if a number is an Armstrong number.","easy","O(log n)","O(1)",["math"],[{"input":"153","output":"True (1^3+5^3+3^3=153)"}]),
("infy-cd-005","Given an array, find the missing number from 1 to n.","easy","O(n)","O(1)",["array","math"],[{"input":"[1,2,4,5,6]","output":"3"}]),
("infy-cd-006","Implement a stack using arrays with push, pop, and peek.","easy","O(1)","O(n)",["stack","array","design"],[{"input":"push(1),push(2),pop(),peek()","output":"2, 1"}]),
("infy-cd-007","Find the GCD of two numbers.","easy","O(log min(a,b))","O(1)",["math","recursion"],[{"input":"a=12, b=8","output":"4"}]),
("infy-cd-008","Check if a string contains only digits.","easy","O(n)","O(1)",["string"],[{"input":"12345","output":"True"},{"input":"12a45","output":"False"}]),
]
for q in infy_cd:
    d = expand_cd(*q); d["company_id"] = "infosys"; d["company"] = "Infosys"; QUESTIONS.append(d)

infy_sd = [
("infy-sd-001","Design a hospital management system for patient records, appointments, and billing.","medium",["Patient service","Appointment system","Billing","Records"],["Data privacy","Appointment conflicts","Records management","Integration"],"1M+ patients"),
("infy-sd-002","Design an online examination system supporting thousands of concurrent test-takers.","medium",["Exam service","Question bank","Proctoring","Result processing","Time management"],["Concurrent test-takers","Anti-cheating","Auto-grading","Load handling"],"100K+ concurrent exams"),
]
for q in infy_sd:
    d = expand_sd(*q); d["company_id"] = "infosys"; d["company"] = "Infosys"; QUESTIONS.append(d)
