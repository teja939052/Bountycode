# This file is imported by gen_questions.py
# It defines the 'data' variable with all interview questions

data = {}

# ── AMAZON ──
data["amazon"] = {
    "name": "Amazon",
    "icon": "\U0001f7e0",
    "leadership_principles": [
        "Customer Obsession", "Ownership", "Invent and Simplify",
        "Are Right, A Lot", "Hire and Develop the Best",
        "Insist on the Highest Standards", "Think Big",
        "Bias for Action", "Frugality", "Learn and Be Curious",
        "Dive Deep", "Have Backbone; Disagree and Commit",
        "Deliver Results", "Strive to be Earth's Best Employer",
        "Success and Scale Bring Broad Responsibility",
    ],
    "questions": {
        "behavioral": [
            {
                "id": "amz-bh-001",
                "question": "Tell me about a time when you had to make a decision with incomplete information. How did you handle it, and what was the outcome?",
                "principle": "Bias for Action",
                "difficulty": "medium",
                "context": "Amazon values speed in decision-making. They want to see you can act decisively even without perfect data.",
                "star_tips": {"situation": "Describe a scenario with a real deadline or time pressure", "task": "Explain what decision needed to be made and why it was urgent", "action": "Show how you gathered what data you could in the limited time, consulted the right people, and made a call", "result": "Highlight the outcome, even if it wasnt perfect, show what you learned"},
                "red_flags": ["Saying you waited until you had 100% of the information", "Blaming others for not having enough data", "Making a decision without any analysis or input", "Not taking ownership of the outcome"]
            },
            {
                "id": "amz-bh-002",
                "question": "Describe a time when you went above and beyond for a customer. What was the situation and what did you do?",
                "principle": "Customer Obsession",
                "difficulty": "medium",
                "context": "Amazon's #1 principle. They want to see you genuinely care about customer experience, not just satisfy requirements.",
                "star_tips": {"situation": "Describe a customer who was frustrated or had an unusual request", "task": "Explain why the standard solution wouldn't work", "action": "Show the extra steps you took (staying late, building a workaround, personally following up)", "result": "Quantify the impact (satisfaction score, repeat business, or a testimonial)"},
                "red_flags": ["Only doing what was minimally required", "Not being able to name a specific customer", "Taking credit for a team effort without acknowledging others", "Focusing on how difficult the customer was rather than solving their problem"]
            },
            {
                "id": "amz-bh-003",
                "question": "Tell me about a time you disagreed with your manager or a peer. How did you handle it?",
                "principle": "Have Backbone; Disagree and Commit",
                "difficulty": "hard",
                "context": "Amazon wants people who can challenge ideas respectfully but also commit once a decision is made.",
                "star_tips": {"situation": "Set up the disagreement, what was the decision at stake?", "task": "Explain why you disagreed and what you believed was the better approach", "action": "Show how you presented your case with data, not just opinions. Then explain how you committed once the decision was made", "result": "The final outcome and how the relationship remained strong"},
                "red_flags": ["Saying you never disagree with your manager", "Being defiant or insubordinate after the decision", "Not being able to articulate the other person's perspective", "Making it personal rather than professional"]
            },
            {
                "id": "amz-bh-004",
                "question": "Give me an example of a time you took ownership of a project that was failing or off-track. What did you do?",
                "principle": "Ownership",
                "difficulty": "hard",
                "context": "Amazon expects owners, not just participants. They want to see you take full responsibility.",
                "star_tips": {"situation": "Describe a project that was behind schedule, over budget, or had quality issues", "task": "What was at stake if it failed?", "action": "Show how you stepped up, identified root causes, made tough calls, and rallied the team", "result": "Quantify how you turned it around (new timeline, saved revenue, improved quality)"},
                "red_flags": ["Blaming the team or external factors", "Only taking credit for successes, not responsibility for failures", "Not having a clear picture of what went wrong", "Waiting for someone else to fix it"]
            },
            {
                "id": "amz-bh-005",
                "question": "Tell me about a time when you invented a simple solution to a complex problem.",
                "principle": "Invent and Simplify",
                "difficulty": "medium",
                "context": "Amazon values simplicity. They want to see you can cut through complexity.",
                "star_tips": {"situation": "Describe a complex problem that others were overcomplicating", "task": "What needed to be achieved?", "action": "Explain how you broke it down and found an elegant, simple solution", "result": "How much simpler/faster/cheaper was your approach?"},
                "red_flags": ["Proposing a complex solution instead of a simple one", "Not being able to explain why your solution was innovative", "Claiming you did it alone when it was a team effort", "Not measuring the impact of simplification"]
            },
            {
                "id": "amz-bh-006",
                "question": "Describe a situation where you had to learn a new technology or skill quickly to get the job done.",
                "principle": "Learn and Be Curious",
                "difficulty": "medium",
                "context": "Amazon moves fast and tech stacks change. They want lifelong learners.",
                "star_tips": {"situation": "What was the project and what skill were you missing?", "task": "What was the deadline and why couldn't someone else do it?", "action": "How did you learn it? Courses, docs, pair programming? How did you apply it?", "result": "What did you build and how did the learning pay off?"},
                "red_flags": ["Saying you already knew everything you needed", "Not being specific about how you learned", "Learning something but never applying it successfully", "Taking too long to learn something simple"]
            },
            {
                "id": "amz-bh-007",
                "question": "Tell me about a time when you insisted on the highest standards even when it was easier to lower them.",
                "principle": "Insist on the Highest Standards",
                "difficulty": "hard",
                "context": "Amazon will not compromise on quality. They want to see you have a backbone about standards.",
                "star_tips": {"situation": "Describe pressure to cut corners (tight deadline, budget constraints)", "task": "What standard was at risk?", "action": "How did you advocate for quality? Did you find a creative way to maintain standards?", "result": "Was the outcome better because you insisted? Did it save rework later?"},
                "red_flags": ["Lowering standards without a fight", "Being perfectionistic to the point of missing deadlines", "Not understanding the difference between high standards and perfectionism", "Making others feel bad for not meeting your standards"]
            },
            {
                "id": "amz-bh-008",
                "question": "Give me an example of a goal you set that was very ambitious. How did you achieve it?",
                "principle": "Think Big",
                "difficulty": "medium",
                "context": "Amazon wants bold thinkers who set ambitious goals and find ways to reach them.",
                "star_tips": {"situation": "What was the ambitious goal and why was it a stretch?", "task": "What made it hard? What was the gap between where you were and where you needed to be?", "action": "How did you break it down? What resources did you marshal? Who did you convince?", "result": "Did you achieve it? What was the impact?"},
                "red_flags": ["Setting easily achievable goals", "Not having a clear plan to reach the goal", "Giving up when faced with obstacles", "Not measuring success"]
            },
            {
                "id": "amz-bh-009",
                "question": "Tell me about a time you had to dive deep into a problem to find the root cause. What did you discover?",
                "principle": "Dive Deep",
                "difficulty": "medium",
                "context": "Amazon expects people to operate at all levels. They don't want surface-level analysis.",
                "star_tips": {"situation": "What was the symptom that something was wrong?", "task": "Why couldn't you accept the surface-level explanation?", "action": "Walk through your analysis (what data did you look at? What did you find 3-4 levels down?)", "result": "What was the real root cause? What fix did you implement?"},
                "red_flags": ["Accepting the first explanation you heard", "Not being technical enough to dive deep", "Delegating the investigation without understanding it yourself", "Fixing symptoms instead of root causes"]
            },
            {
                "id": "amz-bh-010",
                "question": "Describe a time when you had to deliver results under a tight deadline with limited resources.",
                "principle": "Deliver Results",
                "difficulty": "hard",
                "context": "Amazon is results-oriented. They care about what you actually accomplished, not how hard you tried.",
                "star_tips": {"situation": "What was the deadline and why was it tight?", "task": "What resources were limited? (team size, budget, time)", "action": "How did you prioritize? What tradeoffs did you make? How did you keep the team motivated?", "result": "What did you deliver? On time? Under budget? What were the metrics?"},
                "red_flags": ["Making excuses for missed deadlines", "Not being able to articulate tradeoffs", "Delivering poor quality to meet the deadline", "Not communicating timeline risks early"]
            },
            {
                "id": "amz-bh-011",
                "question": "Tell me about a time you had to make a tough tradeoff between speed and quality.",
                "principle": "Deliver Results",
                "difficulty": "hard",
                "context": "Amazon wants to see you can make smart tradeoffs without compromising core quality.",
                "star_tips": {"situation": "What was the feature or project and why was speed critical?", "task": "What would quality look like in an ideal world?", "action": "How did you decide what to cut and what to keep? Did you create a plan to revisit quality later?", "result": "What shipped and what was the customer impact? Did you follow up on the quality debt?"},
                "red_flags": ["Always choosing speed over quality", "Always choosing quality and missing every deadline", "Not communicating tradeoffs to stakeholders", "Not having a plan to address what was cut"]
            },
            {
                "id": "amz-bh-012",
                "question": "Give me an example of how you have hired or developed someone. What did you see in them and how did you help them grow?",
                "principle": "Hire and Develop the Best",
                "difficulty": "medium",
                "context": "Amazon expects every employee to be a talent scout and mentor.",
                "star_tips": {"situation": "Who was the person and what role were you hiring for or developing?", "task": "What potential did you see that others might have missed?", "action": "How did you assess them? What coaching or opportunities did you provide?", "result": "How did they perform? Did they get promoted or take on more responsibility?"},
                "red_flags": ["Not having mentored anyone", "Taking credit for someone else's growth", "Only hiring people like yourself", "Not being able to articulate what makes someone high-potential"]
            },
            {
                "id": "amz-bh-013",
                "question": "Tell me about a time you were frugal and it led to a better outcome.",
                "principle": "Frugality",
                "difficulty": "medium",
                "context": "Amazon is famously frugal. They want to see resourcefulness, not just cost-cutting.",
                "star_tips": {"situation": "What resources were constrained or what was the budget?", "task": "What needed to be accomplished?", "action": "How did you find a cheaper, faster, or simpler way? Did you reuse something?", "result": "How much did you save? Did the frugal approach actually work better?"},
                "red_flags": ["Confusing frugality with being cheap", "Spending money wastefully in other examples", "Not understanding that frugality is about resourcefulness", "Frugality that led to poor quality or rework"]
            },
            {
                "id": "amz-bh-014",
                "question": "Describe a situation where you had to persuade a team to adopt a different approach. How did you build consensus?",
                "principle": "Have Backbone; Disagree and Commit",
                "difficulty": "medium",
                "context": "Amazon wants leaders who can influence without authority.",
                "star_tips": {"situation": "What was the existing approach and why did you think it should change?", "task": "Who needed to be convinced? What was their resistance?", "action": "How did you build your case? Data? Prototypes? Small experiments?", "result": "Did the team adopt your approach? What was the outcome?"},
                "red_flags": ["Using authority or position to force change", "Not listening to counterarguments", "Building a straw man instead of understanding the real concern", "Giving up after the first objection"]
            },
            {
                "id": "amz-bh-015",
                "question": "Tell me about a time you failed. What happened and what did you learn?",
                "principle": "Learn and Be Curious",
                "difficulty": "hard",
                "context": "Amazon wants self-aware candidates who can learn from failure. Dont pick a trivial example.",
                "star_tips": {"situation": "Describe a real failure that had consequences", "task": "What were you trying to accomplish?", "action": "What did you do (or not do) that led to the failure?", "result": "What was the impact? Most importantly, what did you change afterward?"},
                "red_flags": ["Picking a fake failure that's actually a success", "Blaming others or circumstances", "Not showing what you learned", "Making the same mistake again"]
            },
            {
                "id": "amz-bh-016",
                "question": "Describe a time when you had to deal with a difficult stakeholder or customer. How did you manage the relationship?",
                "principle": "Customer Obsession",
                "difficulty": "medium",
                "context": "Amazon deals with demanding customers. They want to see you can handle difficult personalities professionally.",
                "star_tips": {"situation": "Who was the stakeholder and why were they difficult?", "task": "What was the conflict or tension?", "action": "How did you listen, empathize, and find common ground? Did you have to say no firmly?", "result": "How did the relationship improve? Did you deliver what they needed?"},
                "red_flags": ["Labeling the stakeholder as unreasonable without self-reflection", "Avoiding the stakeholder entirely", "Escalating without trying to resolve first", "Sacrificing your team or principles just to please them"]
            },
            {
                "id": "amz-bh-017",
                "question": "Tell me about a time when you had to work on a project that was ambiguous, with no clear owner or path forward. How did you handle it?",
                "principle": "Ownership",
                "difficulty": "hard",
                "context": "Amazon has a lot of ambiguity. They want people who create clarity, not wait for it.",
                "star_tips": {"situation": "What was the ambiguous situation? No clear requirements? Unclear ownership?", "task": "What needed to happen?", "action": "How did you define the problem, get alignment, and create structure?", "result": "What did you deliver and how did it reduce ambiguity for others?"},
                "red_flags": ["Waiting for someone to assign you", "Getting stuck in analysis paralysis", "Not communicating with stakeholders", "Building something nobody asked for"]
            },
            {
                "id": "amz-bh-018",
                "question": "Give me an example of a time when you used data to make a difficult decision.",
                "principle": "Dive Deep",
                "difficulty": "medium",
                "context": "Amazon is obsessed with data-driven decisions. They want to see you use metrics, not gut feelings.",
                "star_tips": {"situation": "What was the decision that needed to be made?", "task": "What was at stake? Who disagreed?", "action": "What data did you gather? How did you analyze it? What metrics mattered?", "result": "What decision did you make and what was the outcome?"},
                "red_flags": ["Using data to confirm a bias rather than find the truth", "Not being able to explain your analysis methodology", "Cherry-picking data points", "Ignoring data that contradicted your position"]
            },
            {
                "id": "amz-bh-019",
                "question": "Tell me about a time when you had to prioritize multiple competing priorities. How did you decide what to work on first?",
                "principle": "Deliver Results",
                "difficulty": "medium",
                "context": "Amazon moves fast and priorities shift. They want to see good judgment.",
                "star_tips": {"situation": "What were the competing priorities? Who was pushing for each?", "task": "What criteria did you use to evaluate importance?", "action": "How did you communicate priorities to stakeholders? What did you deprioritize?", "result": "What got delivered and what was the impact?"},
                "red_flags": ["Trying to do everything at once", "Not being able to say no", "Prioritizing based on whoever shouted loudest", "Not communicating tradeoffs"]
            },
            {
                "id": "amz-bh-020",
                "question": "Describe a time when you had a bold or unconventional idea. How did you sell it to the team or leadership?",
                "principle": "Think Big",
                "difficulty": "medium",
                "context": "Amazon wants big thinkers who can also execute. They want ideas backed by reasoning.",
                "star_tips": {"situation": "What was the conventional wisdom you were challenging?", "task": "What opportunity did you see that others didn't?", "action": "How did you build your pitch? Data? A prototype? A written narrative?", "result": "Did it get adopted? What was the impact?"},
                "red_flags": ["An idea that was bold but not practical", "Not doing the homework to support the idea", "Getting defensive when challenged", "Claiming credit for an idea that was already being pursued"]
            },
        ],
        "technical": [
            {
                "id": "amz-tc-001",
                "question": "How would you design a highly available and scalable system for Amazon's product catalog that serves millions of read requests per second with low latency?",
                "difficulty": "hard",
                "expected_knowledge": ["Distributed caching strategies (CDN, Redis, Memcached)", "Database sharding and replication", "Eventual consistency vs strong consistency", "Read-heavy architecture patterns", "Content delivery networks"],
                "common_mistakes": ["Not considering cache invalidation strategies", "Assuming a single database can handle the load", "Ignoring the cost implications of caching at scale", "Not discussing how to handle product updates with caching"]
            },
            {
                "id": "amz-tc-002",
                "question": "Explain how you would detect and prevent fraud in a real-time payment processing system handling millions of transactions per day.",
                "difficulty": "hard",
                "expected_knowledge": ["Real-time stream processing (Kafka, Flink)", "Machine learning models for fraud detection", "Rule-based vs ML-based approaches", "Latency requirements for payment processing", "Distributed transaction monitoring"],
                "common_mistakes": ["Not considering false positive rates and impact on customers", "Assuming batch processing is acceptable for real-time fraud", "Not discussing data privacy and compliance (PCI-DSS)", "Overlooking the cold-start problem for ML models"]
            },
            {
                "id": "amz-tc-003",
                "question": "Describe how you would implement a recommendation system for Amazon's 'Customers who bought this also bought' feature.",
                "difficulty": "hard",
                "expected_knowledge": ["Collaborative filtering (user-based vs item-based)", "Matrix factorization techniques", "Real-time vs batch recommendation generation", "A/B testing frameworks", "Handling cold-start problems for new items"],
                "common_mistakes": ["Only describing one approach without tradeoffs", "Not addressing how to handle the scale of Amazon's catalog", "Ignoring the exploration vs exploitation tradeoff", "Not considering real-time user behavior signals"]
            },
            {
                "id": "amz-tc-004",
                "question": "How would you optimize the performance of a website that serves dynamic content to users across the globe? Walk me through your approach.",
                "difficulty": "medium",
                "expected_knowledge": ["CDN architecture and edge caching", "Lazy loading and code splitting", "SSR vs CSR", "Database query optimization and indexing", "HTTP/2, HTTP/3, connection pooling", "Resource minification and compression"],
                "common_mistakes": ["Focusing only on frontend optimizations", "Not considering geographic distribution of users", "Proposing solutions without measuring first", "Ignoring the mobile experience"]
            },
            {
                "id": "amz-tc-005",
                "question": "Explain the differences between NoSQL databases like DynamoDB and traditional relational databases. When would you choose one over the other?",
                "difficulty": "medium",
                "expected_knowledge": ["ACID vs BASE properties", "DynamoDB partition key and sort key design", "When to use RDS vs DynamoDB", "Indexing strategies for both", "Consistency models", "Cost implications at scale"],
                "common_mistakes": ["Claiming NoSQL is always faster", "Not understanding DynamoDB query patterns and limitations", "Ignoring the complexity of joins in NoSQL", "Choosing based on hype rather than requirements"]
            },
            {
                "id": "amz-tc-006",
                "question": "How would you design a distributed job scheduling system that can handle millions of tasks per day with different priorities and dependencies?",
                "difficulty": "hard",
                "expected_knowledge": ["Message queues (SQS, RabbitMQ) for task distribution", "Priority queues and scheduling algorithms", "Dependency resolution (DAG-based scheduling)", "Worker pool management and auto-scaling", "Dead letter queues and retry mechanisms", "Monitoring and alerting for job failures"],
                "common_mistakes": ["Not handling task idempotency", "Assuming all tasks have the same priority", "Not considering what happens when a worker crashes mid-task", "Forgetting about task timeouts and staleness"]
            },
            {
                "id": "amz-tc-007",
                "question": "Describe your experience with microservices architecture. What are the tradeoffs compared to a monolithic architecture?",
                "difficulty": "medium",
                "expected_knowledge": ["Service decomposition strategies", "Inter-service communication (REST, gRPC, message queues)", "Data consistency across services (Saga pattern)", "Service discovery and API gateways", "Observability: logging, metrics, tracing", "Deployment complexity and CI/CD implications"],
                "common_mistakes": ["Suggesting microservices for every project", "Not understanding the operational overhead", "Ignoring network latency between services", "Not discussing distributed transactions"]
            },
            {
                "id": "amz-tc-008",
                "question": "How would you handle a scenario where your database is experiencing a high number of deadlocks? Walk through your debugging and resolution process.",
                "difficulty": "medium",
                "expected_knowledge": ["Transaction isolation levels", "Analyzing slow query logs and deadlock graphs", "Index optimization to reduce lock contention", "Application-level retry logic for deadlocks", "Database partitioning and sharding strategies"],
                "common_mistakes": ["Only suggesting to increase database resources", "Not understanding deadlocks vs lock waits", "Applying fixes without understanding root cause", "Not considering application-level changes"]
            },
            {
                "id": "amz-tc-009",
                "question": "Explain how you would implement a rate-limiting system for a public API that serves thousands of clients. Consider different tiers of access.",
                "difficulty": "medium",
                "expected_knowledge": ["Token bucket vs leaky bucket algorithms", "Sliding window vs fixed window counters", "Distributed rate limiting with Redis", "Rate limit headers in API responses", "Graceful degradation when limits are exceeded"],
                "common_mistakes": ["Implementing rate limiting on a single server only", "Not considering race conditions in counter updates", "Hard-coding rate limits without configuration", "Not differentiating between client tiers"]
            },
            {
                "id": "amz-tc-010",
                "question": "Walk me through how you would debug a production issue where a service is intermittently returning 5xx errors with no obvious pattern.",
                "difficulty": "medium",
                "expected_knowledge": ["Systematic debugging methodology", "Log aggregation and analysis tools", "Distributed tracing to identify bottleneck services", "Memory and CPU profiling", "Gradual rollback and canary deployments", "Correlating errors with deployments or traffic spikes"],
                "common_mistakes": ["Restarting servers without finding root cause", "Only looking at application logs, ignoring system metrics", "Making changes without a hypothesis", "Not communicating with stakeholders during the incident"]
            },
            {
                "id": "amz-tc-011",
                "question": "Describe the CAP theorem and how it applies to distributed database design. Give real-world examples of tradeoffs.",
                "difficulty": "hard",
                "expected_knowledge": ["Consistency, Availability, Partition Tolerance definitions", "CP vs AP vs CA tradeoffs", "Real-world examples (DynamoDB, Cassandra, MongoDB, Spanner)", "PACELC extension to CAP", "How Amazon DynamoDB handles these tradeoffs"],
                "common_mistakes": ["Misunderstanding what network partition means", "Claiming a system can be both CP and AP", "Not being able to give concrete examples", "Confusing CAP with ACID"]
            },
            {
                "id": "amz-tc-012",
                "question": "How would you ensure security in a cloud-based application handling sensitive user data? Walk through your security architecture.",
                "difficulty": "medium",
                "expected_knowledge": ["Encryption at rest and in transit", "IAM roles and least privilege access", "AWS security best practices (Security Groups, VPC, KMS)", "Authentication and authorization (OAuth2, JWT)", "Security monitoring and incident response", "Compliance requirements (GDPR, SOC2, PCI-DSS)"],
                "common_mistakes": ["Treating security as an afterthought", "Storing secrets in code or config files", "Overly permissive IAM policies", "Not having an incident response plan"]
            },
        ],
        "coding": [
            {
                "id": "amz-cd-001",
                "question": "Given a list of product IDs and their prices, implement a function that returns the top k most expensive products. If there are ties, return them in lexicographical order of product ID. Optimize for large lists.",
                "difficulty": "medium",
                "time_complexity": "O(n log k) using min-heap",
                "space_complexity": "O(k) for heap",
                "topics": ["Heap", "Sorting", "Top K elements"]
            },
            {
                "id": "amz-cd-002",
                "question": "Implement an LRU (Least Recently Used) cache with O(1) time complexity for both get and put operations. The cache should evict the least recently used item when it reaches capacity.",
                "difficulty": "medium",
                "time_complexity": "O(1) for both operations",
                "space_complexity": "O(capacity)",
                "topics": ["Hash Map", "Doubly Linked List", "Cache Design"]
            },
            {
                "id": "amz-cd-003",
                "question": "Given two strings representing order and product IDs, determine if the products can be shipped in the given order sequence. Each order contains multiple products and each product appears at most once per order.",
                "difficulty": "medium",
                "time_complexity": "O(n + m) where n and m are string lengths",
                "space_complexity": "O(1)",
                "topics": ["Two Pointers", "String Matching", "Greedy"]
            },
            {
                "id": "amz-cd-004",
                "question": "Implement a function to find the median of two sorted arrays of different sizes. Optimize for O(log(min(n,m))) time complexity.",
                "difficulty": "hard",
                "time_complexity": "O(log(min(n,m)))",
                "space_complexity": "O(1)",
                "topics": ["Binary Search", "Divide and Conquer", "Arrays"]
            },
            {
                "id": "amz-cd-005",
                "question": "Given a list of intervals representing meeting times, determine the minimum number of conference rooms required to host all meetings.",
                "difficulty": "medium",
                "time_complexity": "O(n log n) due to sorting",
                "space_complexity": "O(n) for the heap",
                "topics": ["Intervals", "Heap", "Greedy", "Sorting"]
            },
            {
                "id": "amz-cd-006",
                "question": "Design and implement a text justification algorithm. Given an array of words and a max width per line, format the text such that each line has exactly max width characters, fully justified (left and right).",
                "difficulty": "hard",
                "time_complexity": "O(n * L) where n is words and L is max line length",
                "space_complexity": "O(n) for the output",
                "topics": ["String Manipulation", "Greedy", "Simulation"]
            },
            {
                "id": "amz-cd-007",
                "question": "Implement a function that serializes and deserializes a binary tree. The tree can have up to 10^5 nodes and values can be any integer.",
                "difficulty": "hard",
                "time_complexity": "O(n) for both operations",
                "space_complexity": "O(n) for the serialized string",
                "topics": ["Binary Tree", "DFS", "String Serialization"]
            },
            {
                "id": "amz-cd-008",
                "question": "Given a matrix of 0s and 1s where 1 represents land and 0 represents water, find the number of distinct islands. Two islands are the same if one can be translated (but not rotated or reflected) to match the other.",
                "difficulty": "medium",
                "time_complexity": "O(m * n) where m and n are matrix dimensions",
                "space_complexity": "O(m * n) for visited set and recursion stack",
                "topics": ["DFS/BFS", "Hash Set", "Matrix Traversal", "Island Pattern"]
            },
        ],
        "system_design": [
            {
                "id": "amz-sd-001",
                "question": "Design Amazon's shopping cart service. It should handle adding/removing items, applying promotions, calculating taxes, and persisting across sessions. Scale to 500 million active users.",
                "difficulty": "hard",
                "expected_components": ["Cart service with REST API", "Redis for session-level cart caching", "DynamoDB for persistent cart storage", "Promotion/discount service", "Pricing and tax calculation service", "Event-driven architecture for cart updates"],
                "scale_considerations": ["Cart merge logic when anonymous users log in", "Handling concurrent cart modifications", "Price changes between adding and checkout", "Global latency for multi-region access", "Data consistency vs availability for cart operations"]
            },
            {
                "id": "amz-sd-002",
                "question": "Design a real-time inventory management system for Amazon's fulfillment centers. Must handle millions of SKUs across hundreds of warehouses worldwide.",
                "difficulty": "hard",
                "expected_components": ["Inventory service with distributed state", "Event sourcing for inventory changes", "CDC (Change Data Capture) for real-time updates", "Warehouse management system integration", "Reservation system for active carts", "Reconciliation service for drift detection"],
                "scale_considerations": ["Race conditions during flash sales", "Compensating transactions for failed orders", "Multi-region inventory replication", "Handling inventory holds vs actual decrements", "Detection and resolution of inventory drift"]
            },
            {
                "id": "amz-sd-003",
                "question": "Design a package tracking system similar to Amazon's delivery tracking. Users should get real-time updates on their package location and estimated delivery time.",
                "difficulty": "hard",
                "expected_components": ["GPS ingestion service for delivery vehicles", "Real-time tracking data pipeline (Kafka/Flink)", "Geospatial database for location data", "ETA calculation service with ML", "Push notification service for status updates", "Customer-facing tracking dashboard"],
                "scale_considerations": ["Handling location updates from millions of packages simultaneously", "ETA accuracy in different traffic conditions", "Data retention policies for historical tracking data", "Graceful degradation when real-time data is delayed", "Privacy considerations for delivery location data"]
            },
            {
                "id": "amz-sd-004",
                "question": "Design a product review and rating system like Amazon's. Users should be able to write reviews, rate products, upvote helpful reviews, and sort/filter reviews.",
                "difficulty": "medium",
                "expected_components": ["Review service for CRUD operations", "Voting/helpfulness service", "Review ranking algorithm", "Media storage for review images/videos", "Moderation service for spam and abuse detection", "Analytics service for aggregate ratings"],
                "scale_considerations": ["Preventing fake reviews and vote manipulation", "Handling high write volume during product launches", "Real-time aggregation of ratings", "Caching strategies for top reviews", "Handling verified purchase vs unverified reviews"]
            },
        ],
    },
}
