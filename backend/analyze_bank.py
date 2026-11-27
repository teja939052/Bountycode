import json, os
bank_path = r"D:\Project-Fremen\backend\app\data\questions_bank.json"
with open(bank_path, encoding='utf-8') as f:
    bank = json.load(f)

# Analyze current structure
types = {}
difficulties = {}
topics = {}
companies_set = set()

for q in bank:
    q_type = q.get('type', 'unknown')
    types[q_type] = types.get(q_type, 0) + 1
    
    diff = q.get('difficulty', 'unknown')
    difficulties[diff] = difficulties.get(diff, 0) + 1
    
    topic = q.get('topic', 'unknown')
    topics[topic] = topics.get(topic, 0) + 1
    
    companies = q.get('companies', [])
    for c in companies:
        companies_set.add(c)

print("=== TYPE DISTRIBUTION ===")
for t, c in sorted(types.items()):
    print(f"  {t}: {c}")

print("\n=== DIFFICULTY DISTRIBUTION ===")
for d, c in sorted(difficulties.items()):
    print(f"  {d}: {c}")

print("\n=== TOPIC DISTRIBUTION (top 20) ===")
for t, c in sorted(topics.items(), key=lambda x: -x[1])[:20]:
    print(f"  {t}: {c}")

print(f"\n=== COMPANIES ===")
for c in sorted(companies_set):
    print(f"  {c}")