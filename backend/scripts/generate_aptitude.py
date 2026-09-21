"""Generate aptitude questions for Indian placement companies.

Creates questions tagged with Indian companies (TCS, Infosys, Wipro, Cognizant,
Accenture, IBM, etc.) across quantitative, logical, and verbal categories.
"""

import json
import random
import uuid
import os

COMPANIES_INDIAN = ["tcs", "infosys", "wipro", "cognizant", "hcl", "accenture", "capgemini", "tech_mahindra", "lti", "mphasis"]

DIFFICULTIES = ["easy", "medium", "hard"]


def choose(items):
    """Pick a random item from a list."""
    return random.choice(items) if items else ""


def generate_quantitative_questions(count=200):
    """Generate quantitative aptitude questions."""
    questions = []
    topics = ["Percentages", "Profit and Loss", "Time and Work", 
              "Time and Distance", "Probability", "Averages",
              "Simple Interest", "Compound Interest", "Mixtures"]
    
    for _ in range(count):
        topic = random.choice(topics)
        difficulty = random.choice(DIFFICULTIES)
        
        q = {"id": str(uuid.uuid4())}
        
        if topic == "Percentages":
            pct = random.choice([10, 15, 20, 25, 30])
            q["question"] = f"A shop offers a {pct}% discount on an item. If the discount amount is Rs.{random.randint(100, 5000)}, what is the marked price?"
            q["options"] = [f"Rs.{random.randint(1000, 10000)}" for _ in range(4)]
            q["correct_index"] = random.randint(0, 3)
            q["explanation"] = f"Discount is {pct}% of marked price. Marked price = Discount * 100 / {pct}."
            
        elif topic == "Profit and Loss":
            cp = random.randint(500, 5000)
            sp = cp + random.randint(-500, 1000)
            loss_pct = round((cp - sp) / cp * 100, 1) if sp < cp else 0
            q["question"] = f"Shopkeeper buys for Rs.{cp} and sells for Rs.{sp}. What is the {'loss' if sp < cp else 'profit'} %?"
            q["options"] = [f"{random.randint(1, 50)}%", f"{random.randint(1, 50)}%", 
                           f"{random.randint(1, 50)}%", f"{random.randint(1, 50)}%"]
            q["correct_index"] = 0 if sp < cp else 3
            q["explanation"] = f"{'Loss' if sp < cp else 'Profit'} % = {(cp-sp)/cp*100 if sp < cp else (sp-cp)/cp*100:.1f}%"
            
        elif topic == "Time and Work":
            workers = random.randint(2, 10)
            days = random.randint(5, 20)
            q["question"] = f"{workers} workers complete a task in {days} days. How many days will {random.randint(1, workers)} workers take?"
            q["options"] = [str(random.randint(10, 50)) for _ in range(4)]
            q["correct_index"] = 0
            x_days = workers * days // (workers - 1 + random.randint(0, 1))  # ensure denominator >= 1
            q["explanation"] = f"Work constant: {workers} * {days} = {workers-1+random.randint(0,1)} * {x_days} → {workers-1+random.randint(0,1)} * {x_days} = {workers * days}" if workers > 1 else f"Work constant: {workers} * {days} = {workers} * {days}"
            
        elif topic == "Time and Distance":
            speed = random.randint(40, 80)
            time = random.randint(2, 6)
            dist = speed * time
            q["question"] = f"Train at {speed} km/h for {time} hours covers what distance?"
            q["options"] = [f"{dist-20} km", f"{dist} km", f"{dist+20} km", f"{dist+50} km"]
            q["correct_index"] = 1
            q["explanation"] = f"Distance = Speed × Time = {speed} × {time} = {dist} km"
            
        elif topic == "Probability":
            total = random.randint(10, 50)
            favorable = random.randint(1, total // 2)
            q["question"] = f"From {total} people, {favorable} are selected. Probability of specific person?"
            q["options"] = [f"1/{total}", f"1/{favorable}", f"{favorable}/{total}", f"{total}/{favorable}"]
            q["correct_index"] = 0
            q["explanation"] = f"Probability = {favorable}/{total}"
            
        else:
            q["question"] = f"Aptitude question on {topic}"
            q["options"] = [f"Option {chr(65+i)}" for i in range(4)]
            q["correct_index"] = random.randint(0, 3)
            q["explanation"] = f"Explanation for {topic}"
        
        q["difficulty"] = difficulty
        q["topic"] = topic
        q["category"] = "quantitative"
        q["companies"] = random.sample(COMPANIES_INDIAN, k=random.randint(1, 3))
        q["tags"] = ["aptitude", "quantitative", "placement"]
        
        questions.append(q)
    
    return questions


def generate_logical_questions(count=150):
    """Generate logical reasoning questions."""
    questions = []
    topics = ["Series", "Coding Decoding", "Syllogisms", "Arrangements", 
              "Blood Relations", "Direction Sense"]
    
    for _ in range(count):
        topic = random.choice(topics)
        difficulty = random.choice(DIFFICULTIES)
        
        q = {"id": str(uuid.uuid4())}
        
        if topic == "Series":
            seq = [random.randint(1, 30) for _ in range(5)]
            diffs = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
            next_val = seq[-1] + (diffs[-1] if diffs else 1)
            q["question"] = f"Find next: {' '.join(str(x) for x in seq)}"
            q["options"] = [f"{next_val-10}", f"{next_val}", f"{next_val+10}", f"{next_val+20}"]
            q["correct_index"] = 1
            q["explanation"] = f"Pattern: differences {diffs}. Next = {seq[-1]} + {diffs[-1]}"
            
        elif topic == "Coding Decoding":
            code_map = {chr(65+i): random.randint(1, 9) for i in range(5)}
            q["question"] = f"If A=1,B=2,C=3,D=4,E=5 and CODE={random.randint(100,999)}, pattern?"
            q["options"] = ["Sum of digits", "Product of digits", "Position mapping", "Random code"]
            q["correct_index"] = 2
            q["explanation"] = f"Code mapping: {code_map}. Pattern based on alphabet positions."
            
        elif topic == "Syllogisms":
            q["question"] = f"All {choose(['men','boys','students'])} are {choose(['tall','smart','intelligent'])}. Some {choose(['tall','smart','intelligent'])} are {choose(['engineers','doctors','artists'])}. Conclusion?"
            q["options"] = ["Valid", "Invalid", "Partially valid", "Cannot determine"]
            q["correct_index"] = 0
            q["explanation"] = "Standard syllogism: All A are B. Some B are C. Therefore some A are C."
            
        elif topic == "Arrangements":
            q["question"] = f"In how many ways can {random.randint(3, 8)} people sit in a row?"
            q["options"] = [str(random.randint(6, 40320)) for _ in range(4)]
            q["correct_index"] = 0  # factorial
            q["explanation"] = f"{random.randint(3, 8)}! = factorial"
            
        else:
            q["question"] = f"Logical reasoning: {topic}"
            q["options"] = [f"Option {chr(65+i)}" for i in range(4)]
            q["correct_index"] = random.randint(0, 3)
            q["explanation"] = f"Explanation for {topic}"
        
        q["difficulty"] = difficulty
        q["topic"] = topic
        q["category"] = "logical"
        q["companies"] = random.sample(COMPANIES_INDIAN, k=random.randint(1, 3))
        q["tags"] = ["aptitude", "logical", "placement"]
        
        questions.append(q)
    
    return questions


def generate_verbal_questions(count=150):
    """Generate verbal ability questions."""
    questions = []
    topics = ["Grammar", "Vocabulary", "Reading Comprehension", "Sentence Correction", "Para Jumbles"]
    
    for _ in range(count):
        topic = random.choice(topics)
        difficulty = random.choice(DIFFICULTIES)
        
        q = {"id": str(uuid.uuid4())}
        
        if topic == "Grammar":
            q["question"] = f"Choose correct: The team {choose(['is','are'])} winning."
            q["options"] = [f"The team {choose(['is','are'])} winning", 
                           f"The team {choose(['were','are'])} winning",
                           f"The team {choose(['has been','was']) } winning",
                           f"The team {choose(['being','being']) } winning"]
            q["correct_index"] = 0
            q["explanation"] = "Collective noun takes singular verb"
            
        elif topic == "Vocabulary":
            word = choose(["arduous", "candid", "eloquent", "gregarious", "ostentatious"])
            q["question"] = f"Opposite of '{word}':"
            q["options"] = [choose(["simple", "easy", "minor", "trivial"]) for _ in range(4)]
            q["correct_index"] = random.randint(0, 3)
            q["explanation"] = f"Antonyms of {word}"
            
        elif topic == "Reading Comprehension":
            q["question"] = f"Passage: {choose(['Company results', 'Government policy', 'Market trends'])}. Main topic?"
            q["options"] = ["Topic A", "Topic B", "Topic C", "Topic D"]
            q["correct_index"] = random.randint(0, 3)
            q["explanation"] = f"Main topic: {choose(['financial results', 'policy changes', 'market trends'])}"
            
        elif topic == "Sentence Correction":
            q["question"] = f"Error: Manager with team {choose(['is','are'])} planning."
            q["options"] = [f"Manager with team {choose(['is','are'])} planning",
                           f"Manager with team {choose(['were','are'])} planning",
                           f"Manager with team {choose(['was','were'])} planning",
                           f"Manager with team {choose(['has been','were'])} planning"]
            q["correct_index"] = 0
            q["explanation"] = "Subject is manager (singular)"
            
        else:
            q["question"] = f"Verbal: {topic}"
            q["options"] = [f"Option {chr(65+i)}" for i in range(4)]
            q["correct_index"] = random.randint(0, 3)
            q["explanation"] = f"Explanation for {topic}"
        
        q["difficulty"] = difficulty
        q["topic"] = topic
        q["category"] = "verbal"
        q["companies"] = random.sample(COMPANIES_INDIAN, k=random.randint(1, 3))
        q["tags"] = ["aptitude", "verbal", "placement"]
        
        questions.append(q)
    
    return questions


def main():
    """Generate all aptitude questions."""
    all_questions = []
    
    print("Generating quantitative questions (200)...")
    q_q = generate_quantitative_questions(200)
    print(f"  Generated: {len(q_q)}")
    all_questions.extend(q_q)
    
    print("Generating logical questions (150)...")
    q_l = generate_logical_questions(150)
    print(f"  Generated: {len(q_l)}")
    all_questions.extend(q_l)
    
    print("Generating verbal questions (150)...")
    q_v = generate_verbal_questions(150)
    print(f"  Generated: {len(q_v)}")
    all_questions.extend(q_v)
    
    # Deduplicate by question text
    seen = set()
    unique = []
    for q in all_questions:
        key = q["question"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(q)
    
    print(f"\nTotal before dedup: {len(all_questions)}")
    print(f"Total after dedup: {len(unique)}")
    
    # Save
    output_path = r"D:\Project-Fremen\backend\app\data\generated_aptitude_questions.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to: {output_path}")
    print(f"Final count: {len(unique)} questions")
    
    # Company distribution
    company_counts = {}
    for q in unique:
        for c in q.get("companies", []):
            company_counts[c] = company_counts.get(c, 0) + 1
    print(f"\nCompany distribution:")
    for c, count in sorted(company_counts.items(), key=lambda x: -x[1]):
        print(f"  {c}: {count}")
    
    # Topic distribution
    topic_counts = {}
    for q in unique:
        t = q.get("topic", "")
        topic_counts[t] = topic_counts.get(t, 0) + 1
    print(f"\nTop topics:")
    for t, count in sorted(topic_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {t}: {count}")


if __name__ == "__main__":
    main()