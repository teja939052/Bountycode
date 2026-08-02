#!/usr/bin/env python3
"""Generate interview_questions.py with 250+ real-world interview questions."""
import json, os

output_path = os.path.join(os.path.dirname(__file__), "app", "data", "interview_questions.py")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Build the data structure
data = {}

# Import the real data
exec(open(os.path.join(os.path.dirname(__file__), "_questions_data.py"), encoding="utf-8").read())

with open(output_path, "w", encoding="utf-8") as f:
    f.write('# ── Interview Question Bank (250+ real-world questions) ──\n')
    f.write('# Organized by company and category\n')
    f.write('# Auto-generated. Do not edit directly.\n\n')
    f.write('from typing import List, Dict, Optional\nimport random\n\n')
    f.write('INTERVIEW_CATEGORIES = {\n')
    f.write('    "behavioral": "Behavioral & Leadership",\n')
    f.write('    "technical": "Technical CS Fundamentals",\n')
    f.write('    "coding": "Coding & Algorithms",\n')
    f.write('    "system_design": "System Design & Architecture",\n')
    f.write('    "hr": "HR & Fitment",\n')
    f.write('    "puzzle": "Brain Teasers & Puzzles",\n')
    f.write('    "oop": "OOP Design",\n')
    f.write('    "sql": "SQL & Database Design",\n')
    f.write('}\n\n')
    f.write('COMPANY_QUESTIONS = ')
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n\n')
    # Write helper functions
    f.write('''
def get_questions_by_company(company_id: str, category: str = None) -> List[Dict]:
    company = COMPANY_QUESTIONS.get(company_id)
    if not company:
        return []
    questions = company.get("questions", {})
    if category:
        return questions.get(category, [])
    result = []
    for cat_qs in questions.values():
        result.extend(cat_qs)
    return result

def get_random_questions(count: int = 5, company: str = None, category: str = None, difficulty: str = None) -> List[Dict]:
    if company:
        pool = get_questions_by_company(company, category)
    else:
        pool = []
        for cid in COMPANY_QUESTIONS:
            pool.extend(get_questions_by_company(cid, category))
    if difficulty:
        pool = [q for q in pool if q.get("difficulty") == difficulty]
    return random.sample(pool, min(count, len(pool)))

def get_question_by_id(question_id: str) -> Dict:
    for cid in COMPANY_QUESTIONS:
        for cat_qs in COMPANY_QUESTIONS[cid].get("questions", {}).values():
            for q in cat_qs:
                if q["id"] == question_id:
                    return q
    return None

def get_all_companies() -> List[Dict]:
    result = []
    for cid, cdata in COMPANY_QUESTIONS.items():
        total = 0
        for cat_qs in cdata.get("questions", {}).values():
            total += len(cat_qs)
        result.append({
            "id": cid,
            "name": cdata["name"],
            "icon": cdata.get("icon", ""),
            "total_questions": total,
            "leadership_principles": cdata.get("leadership_principles", []),
        })
    return result

def get_company_question_count(company_id: str) -> Dict:
    company = COMPANY_QUESTIONS.get(company_id)
    if not company:
        return {"total": 0, "categories": {}}
    counts = {}
    total = 0
    for cat, qs in company.get("questions", {}).items():
        counts[cat] = len(qs)
        total += len(qs)
    return {"total": total, "categories": counts}
''')

print(f"Written {sum(1 for c in data.values() for ql in c.get('questions', {}).values() for _ in ql)} questions")
