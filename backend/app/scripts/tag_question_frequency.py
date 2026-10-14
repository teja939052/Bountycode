"""Tag service company questions with frequency based on real drive data."""
import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()

# Frequency patterns based on real company drive data from web search
# Sources: testbook.com, prepinsta.com, papersadda.com, faceprep.in
FREQUENCY_MAP = {
    # TCS NQT most frequent topics (candidate-reported 2024-2026)
    "tcs": {
        "high": [
            "Percentages", "Profit and Loss", "Time and Work", "Time Speed Distance",
            "Number Series", "Data Interpretation", "Seating Arrangement", "Syllogism",
            "Coding Decoding", "Blood Relations", "Averages", "Ratios",
            "Verbal Ability", "Reasoning Ability", "Numerical Ability"
        ],
        "medium": [
            "Permutations and Combinations", "Probability", "Geometry", "Clocks",
            "Direction Sense", "Data Sufficiency", "Compound Interest", "Simple Interest"
        ]
    },
    # Infosys SP/DSE most frequent topics
    "infosys": {
        "high": [
            "Arrays", "Strings", "Dynamic Programming", "Linked Lists", "Trees",
            "Recursion", "Backtracking", "Sorting", "Searching", "Hashing",
            "Graphs", "Stack", "Queue"
        ],
        "medium": [
            "Greedy", "Binary Search", "Two Pointers", "Sliding Window", "Heap"
        ]
    },
    # Wipro NTH most frequent topics
    "wipro": {
        "high": [
            "Time Speed Distance", "Percentages", "Profit and Loss", "Number Series",
            "Seating Arrangement", "Reading Comprehension", "Sentence Correction",
            "Blood Relations", "Arrays", "Strings", "Coding", "Logical Reasoning"
        ],
        "medium": [
            "Clocks", "Calendars", "Data Sufficiency", "Direction Sense", "Syllogism"
        ]
    },
    # Cognizant most frequent topics
    "cognizant": {
        "high": [
            "Quantitative Aptitude", "Logical Reasoning", "Verbal Ability",
            "Arrays", "Strings", "Numbers", "Basic Coding", "Database"
        ],
        "medium": [
            "Time and Work", "Profit and Loss", "Ratios", "Averages"
        ]
    },
    # Capgemini most frequent topics
    "capgemini": {
        "high": [
            "Arrays", "Strings", "Dynamic Programming", "Sorting", "Searching",
            "Quantitative Aptitude", "Logical Reasoning", "Permutations"
        ],
        "medium": [
            "Linked Lists", "Trees", "Graphs", "Hashing"
        ]
    },
    # Accenture most frequent topics
    "accenture": {
        "high": [
            "Quantitative Aptitude", "Logical Reasoning", "Verbal Ability",
            "Arrays", "Strings", "Basic Coding", "Numbers", "Time and Work"
        ],
        "medium": [
            "Profit and Loss", "Percentages", "Ratios", "Averages"
        ]
    }
}

def get_frequency(question):
    """Determine frequency based on topic and company."""
    companies = [c.lower() for c in question.get("companies", [])]
    topic = str(question.get("topic", "")).lower()
    qtype = str(question.get("type", "")).lower()
    
    for company in companies:
        if company not in FREQUENCY_MAP:
            continue
        company_freq = FREQUENCY_MAP[company]
        
        # Check high frequency topics
        for high_topic in company_freq.get("high", []):
            if high_topic.lower() in topic or high_topic.lower() in qtype:
                return "high"
        
        # Check medium frequency topics
        for med_topic in company_freq.get("medium", []):
            if med_topic.lower() in topic or med_topic.lower() in qtype:
                return "medium"
    
    return "low"

# Tag questions with frequency
tagged = 0
for q in qs._questions:
    if q.get("frequency"):
        continue  # Already tagged
    
    companies = [c.lower() for c in q.get("companies", [])]
    # Only tag service company questions
    service_companies = {"tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"}
    if not any(c in service_companies for c in companies):
        continue
    
    freq = get_frequency(q)
    q["frequency"] = freq
    tagged += 1

print(f"Tagged {tagged} questions with frequency")
print("\nBreakdown by company and frequency:")

from collections import Counter
for company in ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]:
    company_qs = [q for q in qs._questions if company in [c.lower() for c in q.get("companies", [])]]
    freq_counts = Counter(q.get("frequency", "untagged") for q in company_qs)
    print(f"\n{company.upper()}:")
    for freq, count in sorted(freq_counts.items(), key=lambda x: str(x[0])):
        print(f"  {freq}: {count}")
