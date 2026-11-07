import json, random, uuid, os

COMPANIES_INDIAN = ["tcs", "infosys", "wipro", "cognizant", "hcl", "accenture", "capgemini", "tech_mahindra", "lti", "mphasis"]

questions = []

# Generate 300 HR questions
for i in range(300):
    topic = random.choice(["Hiring", "Teamwork", "Leadership", "Conflict Resolution", "Communication", "Time Management", "Decision Making", "Adaptability", "Problem Solving", "Cultural Fit"])
    diff = random.choice(["easy", "medium", "hard"])
    cid = str(uuid.uuid4())
    q = {"id": cid}
    
    if topic == "Hiring":
        q["question"] = "What approach do you take when recruiting for a technical role where you need to assess both technical skills and cultural fit?"
        q["options"] = ["Focus only on technical skills", "Focus only on cultural fit", "Balance both with structured interviews", "Outsource hiring entirely"]
        q["correct_index"] = 2
        q["explanation"] = "Structured interviews give consistent, comparable data on both dimensions"
    elif topic == "Teamwork":
        q["question"] = "A team member is not contributing. What do you do?"
        q["options"] = ["Ignore it and hope it improves", "Talk to the person privately", "Escalate to manager immediately", "Reassign the person"]
        q["correct_index"] = 1
        q["explanation"] = "Private conversation is the first step in addressing performance issues"
    elif topic == "Leadership":
        q["question"] = "How do you motivate a demotivated team?"
        q["options"] = ["Increase salaries", "Provide clear vision and goals", "Threatened with termination", "Remove all responsibilities"]
        q["correct_index"] = 1
        q["explanation"] = "Clear vision and goals re-engages team purpose"
    elif topic == "Conflict Resolution":
        q["question"] = "Two team members have a constant conflict. How do you resolve it?"
        q["options"] = ["Let them resolve it themselves", "Assign them to separate projects", "Mediate a discussion with both parties", "Fire both employees"]
        q["correct_index"] = 2
        q["explanation"] = "Mediation addresses the root cause"
    elif topic == "Communication":
        q["question"] = "How do you ensure clear communication in a remote team?"
        q["options"] = ["Daily video calls", "Strict email protocols", "Async updates + weekly video", "No formal communication"]
        q["correct_index"] = 2
        q["explanation"] = "Async updates + weekly video balances focus and connection"
    elif topic == "Time Management":
        q["question"] = "You have too many tasks. What do you prioritize?"
        q["options"] = ["Work overtime daily", "Prioritize by deadline and impact", "Delegate everything", "Take no new tasks"]
        q["correct_index"] = 1
        q["explanation"] = "Prioritization by impact and deadline is most effective"
    elif topic == "Decision Making":
        q["question"] = "You must make a decision with incomplete information. How?"
        q["options"] = ["Gather until you have 100% information", "Make the best decision with available data", "Flip a coin", "Avoid deciding"]
        q["correct_index"] = 1
        q["explanation"] "Best decision with available data minimizes regret"
    elif topic == "Adaptability":
        q["question"] = "A project's requirements change suddenly. Your reaction?"
        q["options"] = ["Resist the change", "Complain to management", "Adapt quickly and re-plan", "Wait for things to return to normal"]
        q["correct_index"] = 2
        q["explanation"] = "Quick adaptation keeps projects on track"
    elif topic == "Problem Solving":
        q["question"] = "A customer is angry about a delay. What do you do?"
        q["options"] = ["Blame external factors", "Apologize and offer compensation", "Explain technical reasons", "Ignore the complaint"]
        q["correct_index"] = 1
        q["explanation"] = "Apology + compensation maintains customer goodwill"
    elif topic == "Problem Solving":
        q["question"] = "A project is behind schedule. What is your first step?"
        q["options"] = ["Work overtime every day", "Analyze the bottleneck and re-plan", "Add more people immediately", "Cancel the project"]
        q["correct_index"] = 1
        q["explanation"] = "Analyze bottleneck before acting"
    elif topic == "Cultural Fit":
        q["question"] = "A brilliant candidate doesn't align with company values. What do you do?"
        q["options"] = ["Hire anyway because of skills", "Reject because of values mismatch", "Hire and add values training", "Delay decision indefinitely"]
        q["correct_index"] = 1
        q["explanation"] = "Values mismatch eventually causes team friction"
    else:
        q["question"] = "HR question on {}".format(topic)
        q["options"] = ["Option A", "Option B", "Option C", "Option D"]
        q["correct_index"] = random.randint(0,3)
        q["explanation"] = "Explanation"
    
    q["difficulty"] = diff
    q["topic"] = topic
    q["category"] = "hr"
    q["companies"] = random.sample(COMPANIES_INDIAN, k=random.randint(1,3))
    q["tags"] = ["aptitude","hr","placement"]
    questions.append(q)

# Deduplicate
seen = set()
unique = []
for q in questions:
    key = q["question"].lower().strip()
    if key not in seen:
        seen.add(key)
        unique.append(q)

print("HR - Total generated:", len(questions))
print("HR - Unique questions:", len(unique))

# Save
output_path = r"D:\Project-Fremen\backend\app\data\generated_hr_questions.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(unique, f, indent=2, ensure_ascii=False)

print("Saved to:", output_path)

# Summary
companies = {}
for q in unique:
    for c in q.get("companies", []):
        companies[c] = companies.get(c, 0) + 1
print("\nHR Company distribution:")
for c, count in sorted(companies.items(), key=lambda x: -x[1]):
    print("  {}: {}".format(c, count))
" 2>&1