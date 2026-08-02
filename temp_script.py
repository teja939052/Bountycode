import sys, os, re

with open(r'D:\Project-Fremen\backend\app\data\interview_question_bank.py', 'r', encoding='utf-8') as f:
    content = f.read()

ids = re.findall(r"'id':\s*'([^']+)'", content)
print('Total question entries (by id field):', len(ids))
print('Unique question IDs:', len(set(ids)))

# Count by category
categories = {}
for id_val in ids:
    idx = content.find("'id': '" + id_val + "'")
    if idx > 0:
        pre = content[:idx]
        cat_match = re.search(r"'category':\s*'([^']+)'", pre)
        if cat_match:
            cat = cat_match.group(1)
            categories[cat] = categories.get(cat, 0) + 1

print()
print('Questions BY CATEGORY:')
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    print('  {}: {}'.format(cat, count))
print('  TOTAL (categorized):', sum(categories.values()))

# Count by company
companies = {}
for id_val in ids:
    idx = content.find("'id': '" + id_val + "'")
    if idx > 0:
        pre = content[:idx]
        comp_match = re.search(r"'company_id':\s*'([^']+)'", pre)
        if comp_match:
            comp = comp_match.group(1)
            companies[comp] = companies.get(comp, 0) + 1

print()
print('Questions BY COMPANY:')
for comp, count in sorted(companies.items(), key=lambda x: -x[1]):
    print('  {}: {}'.format(comp, count))
print('  TOTAL (by company):', sum(companies.values()))

# Unique question texts
questions = re.findall(r"'question':\s*'([^']+)'", content)
print()
print('Total question text entries:', len(questions))
print('Unique question texts:', len(set(questions)))
print('Duplicate question texts count:', len(questions) - len(set(questions)))

# Unique (id, question) pairs
pairs = set(zip(ids, questions))
print('Unique (id, question) pairs:', len(pairs))

# Find all companies defined in the structure
companies_list = re.findall(r"INDIAN_COMPANIES\[['""]([^'""]+)['""]", content)
print()
print('All companies in question bank:')
company_names = re.findall(r"COMPANY_QUESTIONS\[['""]([^'""]+)['""]", content)
print('  Company entries:', company_names)
