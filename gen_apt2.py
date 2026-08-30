import json, random, uuid, os

COMPANIES_INDIAN = ["tcs", "infosys", "wipro", "cognizant", "hcl", "accenture", "capgemini", "tech_mahindra", "lti", "mphasis"]

questions = []

# Generate 500 quantitative
for i in range(500):
    topic = random.choice(["Percentages", "Profit and Loss", "Time and Work", "Time and Distance", "Probability"])
    diff = random.choice(["easy", "medium", "hard"])
    cid = str(uuid.uuid4())
    q = {"id": cid}
    
    if topic == "Percentages":
        pct = random.choice([10, 15, 20, 25, 30])
        q["question"] = "Shop % discount. Discount Rs. Marked price?".format(pct)
        q["options"] = ["Rs. {}".format(random.randint(1000,10000)) for _ in range(4)]
        q["correct_index"] = random.randint(0,3)
        q["explanation"] = "Discount is % of marked price"
    elif topic == "Profit and Loss":
        cp = random.randint(500,5000)
        sp = cp + random.randint(-500,1000)
        gain = sp - cp
        q["question"] = "Buys Rs {} sells Rs {}. Profit/Loss %?".format(cp, sp)
        q["options"] = ["{}%".format(random.randint(1,50)) for _ in range(4)]
        q["correct_index"] = 0 if gain > 0 else 3
        q["explanation"] = "{:.1f}%".format(abs(gain)/cp*100)
    elif topic == "Time and Work":
        workers = random.randint(2, 8)
        days = random.randint(5, 15)
        q["question"] = "{} workers in {} days. {} workers?".format(workers, days, random.randint(1,workers))
        q["options"] = ["{}".format(random.randint(10,50)) for _ in range(4)]
        q["correct_index"] = 0
        q["explanation"] = "Work constant"
    elif topic == "Time and Distance":
        speed = random.randint(40,80)
        time = random.randint(2,6)
        dist = speed * time
        q["question"] = "Speed {} km/h for {} h. Distance?".format(speed, time)
        q["options"] = ["{} km".format(dist-20), "{} km".format(dist), "{} km".format(dist+20), "{} km".format(dist+50)]
        q["correct_index"] = 1
        q["explanation"] = "Distance = Speed x Time"
    elif topic == "Probability":
        total = random.randint(10,50)
        fav = random.randint(1, total//2)
        q["question"] = "From {} people select {}. Probability?".format(total, fav)
        q["options"] = ["1/{}".format(total), "1/{}".format(fav), "{}/{}".format(fav, total), "{}/{}".format(total, fav)]
        q["correct_index"] = 0
        q["explanation"] = "Probability = fav/total"
    else:
        q["question"] = "Quant question"
        q["options"] = ["Option A", "Option B", "Option C", "Option D"]
        q["correct_index"] = random.randint(0,3)
        q["explanation"] = "Explanation"
    
    q["difficulty"] = diff
    q["topic"] = topic
    q["category"] = "quantitative"
    q["companies"] = random.sample(COMPANIES_INDIAN, k=random.randint(1,3))
    q["tags"] = ["aptitude","quantitative","placement"]
    questions.append(q)

# Generate 200 logical
for i in range(200):
    topic = random.choice(["Series", "Coding Decoding", "Syllogisms", "Arrangements"])
    diff = random.choice(["easy","medium","hard"])
    cid = str(uuid.uuid4())
    q = {"id": cid}
    
    if topic == "Series":
        seq = [random.randint(1,20) for _ in range(5)]
        diffs = [seq[i+1]-seq[i] for i in range(len(seq)-1)]
        nxt = seq[-1] + (diffs[-1] if diffs else 1)
        q["question"] = "Series: {}".format(" ".join(str(x) for x in seq))
        q["options"] = ["{}".format(nxt-10), "{}".format(nxt), "{}".format(nxt+10), "{}".format(nxt+20)]
        q["correct_index"] = 1
        q["explanation"] = "Differences: {}".format(diffs)
    elif topic == "Coding Decoding":
        q["question"] = "A=1,B=2 CODE={}".format(random.randint(100,999))
        q["options"] = ["Sum digits","Product digits","Position mapping","Random code"]
        q["correct_index"] = 2
        q["explanation"] = "Position mapping"
    elif topic == "Syllogisms":
        q["question"] = "All A are B. Some B are C. Some A are C?"
        q["options"] = ["Valid","Invalid","Partial valid","Cannot determine"]
        q["correct_index"] = 0
        q["explanation"] = "Standard syllogism"
    elif topic == "Arrangements":
        n = random.randint(3,6)
        q["question"] = "{} people sit in a row. Ways?".format(n)
        q["options"] = ["{}".format(random.randint(6,720)) for _ in range(4)]
        q["correct_index"] = 0
        q["explanation"] = "{}! permutations".format(n)
    
    q["difficulty"] = diff
    q["topic"] = topic
    q["category"] = "logical"
    q["companies"] = random.sample(COMPANIES_INDIAN, k=random.randint(1,3))
    q["tags"] = ["aptitude","logical","placement"]
    questions.append(q)

# Generate 200 verbal
for i in range(200):
    topic = random.choice(["Grammar", "Vocabulary", "Reading Comprehension", "Sentence Correction"])
    diff = random.choice(["easy","medium","hard"])
    cid = str(uuid.uuid4())
    q = {"id": cid}
    
    if topic == "Grammar":
        q["question"] = "The team {} winning.".format(random.choice(["is","are"]))
        q["options"] = ["The team {} winning".format(random.choice(["is","are"])),
                       "The team {} winning".format(random.choice(["were","are"])),
                       "The team {} winning".format(random.choice(["was","were"])),
                       "The team {} winning".format(random.choice(["has been"]))]
        q["correct_index"] = 0
        q["explanation"] = "Collective noun singular"
    elif topic == "Vocabulary":
        word = random.choice(["arduous","candid","eloquent"])
        q["question"] = "Opposite of '{}':".format(word)
        q["options"] = [random.choice(["simple","easy","minor","trivial"]) for _ in range(4)]
        q["correct_index"] = random.randint(0,3)
        q["explanation"] = "Antonyms of {}".format(word)
    elif topic == "Reading Comprehension":
        q["question"] = "Passage: Company results. Main topic?"
        q["options"] = ["Topic A","Topic B","Topic C","Topic D"]
        q["correct_index"] = random.randint(0,3)
        q["explanation"] = "Main topic: financial results"
    elif topic == "Sentence Correction":
        q["question"] = "Error: Manager with team {} planning.".format(random.choice(["is","are"]))
        q["options"] = [f"Manager with team {random.choice(['is','are'])} planning",
                       f"Manager with team {random.choice(['were','are'])} planning",
                       f"Manager with team {random.choice(['was','were'])} planning",
                       f"Manager with team {random.choice(['has been'])} planning"]
        q["correct_index"] = 0
        q["explanation"] = "Subject is manager"
    
    q["difficulty"] = diff
    q["topic"] = topic
    q["category"] = "verbal"
    q["companies"] = random.sample(COMPANIES_INDIAN, k=random.randint(1,3))
    q["tags"] = ["aptitude","verbal","placement"]
    questions.append(q)

# Deduplicate
seen = set()
unique = []
for q in questions:
    key = q["question"].lower().strip()
    if key not in seen:
        seen.add(key)
        unique.append(q)

print("Total generated:", len(questions))
print("Unique questions:", len(unique))
print("Quantitative:", sum(1 for q in unique if q["category"]=="quantitative"))
print("Logical:", sum(1 for q in unique if q["category"]=="logical"))
print("Verbal:", sum(1 for q in unique if q["category"]=="verbal"))

# Save
output_path = r"D:\Project-Fremen\backend\app\data\generated_aptitude_questions.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(unique, f, indent=2, ensure_ascii=False)

print("Saved to:", output_path)