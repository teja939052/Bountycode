"""Tag service company questions with numeric frequency and persist to file."""
import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import json
import os
import app.services.question_store as qs

qs.load_all()

FREQUENCY_MAP = {
    "tcs": {
        "high": ["Percentages", "Profit and Loss", "Time and Work", "Time Speed Distance", "Number Series", "Data Interpretation", "Seating Arrangement", "Syllogism", "Coding Decoding", "Blood Relations", "Averages", "Ratios", "Verbal Ability", "Reasoning Ability", "Numerical Ability"],
        "medium": ["Permutations and Combinations", "Probability", "Geometry", "Clocks", "Direction Sense", "Data Sufficiency", "Compound Interest", "Simple Interest"]
    },
    "infosys": {
        "high": ["Arrays", "Strings", "Dynamic Programming", "Linked Lists", "Trees", "Recursion", "Backtracking", "Sorting", "Searching", "Hashing", "Graphs", "Stack", "Queue"],
        "medium": ["Greedy", "Binary Search", "Two Pointers", "Sliding Window", "Heap"]
    },
    "wipro": {
        "high": ["Time Speed Distance", "Percentages", "Profit and Loss", "Number Series", "Seating Arrangement", "Reading Comprehension", "Sentence Correction", "Blood Relations", "Arrays", "Strings", "Coding", "Logical Reasoning"],
        "medium": ["Clocks", "Calendars", "Data Sufficiency", "Direction Sense", "Syllogism"]
    },
    "cognizant": {
        "high": ["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Arrays", "Strings", "Numbers", "Basic Coding", "Database"],
        "medium": ["Time and Work", "Profit and Loss", "Ratios", "Averages"]
    },
    "capgemini": {
        "high": ["Arrays", "Strings", "Dynamic Programming", "Sorting", "Searching", "Quantitative Aptitude", "Logical Reasoning", "Permutations"],
        "medium": ["Linked Lists", "Trees", "Graphs", "Hashing"]
    },
    "accenture": {
        "high": ["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Arrays", "Strings", "Basic Coding", "Numbers", "Time and Work"],
        "medium": ["Profit and Loss", "Percentages", "Ratios", "Averages"]
    }
}

def get_frequency_score(question):
    companies = [c.lower() for c in question.get("companies", [])]
    topic = str(question.get("topic", "")).lower()
    
    for company in companies:
        if company not in FREQUENCY_MAP:
            continue
        company_freq = FREQUENCY_MAP[company]
        
        for high_topic in company_freq.get("high", []):
            if high_topic.lower() in topic:
                return 75 + hash(high_topic.lower()) % 20
        
        for med_topic in company_freq.get("medium", []):
            if med_topic.lower() in topic:
                return 40 + hash(med_topic.lower()) % 20
    
    return 10 + hash(topic) % 20

# Tag and collect frequency overrides
frequency_overrides = {}
tagged = 0
for q in qs._questions:
    qid = str(q.get("id", ""))
    if not qid:
        continue
    
    companies = [c.lower() for c in q.get("companies", [])]
    service_companies = {"tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"}
    
    if not any(c in service_companies for c in companies):
        continue
    
    if q.get("frequency", 0) == 0:
        freq = get_frequency_score(q)
        q["frequency"] = freq
        frequency_overrides[qid] = freq
        tagged += 1

print(f"Tagged {tagged} questions with numeric frequency")

# Persist to file
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
overrides_path = os.path.join(backend_root, "data", "frequency_overrides.json")
with open(overrides_path, "w", encoding="utf-8") as f:
    json.dump(frequency_overrides, f, indent=2)
print(f"Saved {len(frequency_overrides)} frequency overrides to {overrides_path}")

# Show breakdown
from collections import Counter
for company in ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]:
    company_qs = [q for q in qs._questions if company in [c.lower() for c in q.get("companies", [])]]
    freq_counts = Counter(q.get("frequency", 0) for q in company_qs)
    high = sum(1 for f, c in freq_counts.items() if f >= 50)
    medium = sum(1 for f, c in freq_counts.items() if 10 <= f < 50)
    low = sum(1 for f, c in freq_counts.items() if f < 10)
    print(f"{company.upper()}: high={high}, medium={medium}, low={low}")
