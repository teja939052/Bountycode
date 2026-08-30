import json
from collections import Counter

d = json.load(open("app/data/questions_bank.json", encoding="utf-8"))
print("total:", len(d))

fields = {}
for q in d:
    for k in (
        "id", "title", "question", "description", "topic", "difficulty",
        "companies", "testcases", "hidden_testcases", "expected",
        "correct_answer", "solution", "constraints", "function_name",
    ):
        fields.setdefault(k, [0, 0])
        if q.get(k) not in (None, "", [], {}):
            fields[k][0] += 1
        else:
            fields[k][1] += 1
for k, (yes, no) in fields.items():
    print(f"{k:20s} has={yes:5d} missing={no:5d}")

print()
print("types:", dict(Counter(q.get("type", "?") for q in d)))
print("difficulty:", dict(Counter(q.get("difficulty", "?") for q in d)))
print("has both title and question:", sum(1 for q in d if q.get("title") and q.get("question")))