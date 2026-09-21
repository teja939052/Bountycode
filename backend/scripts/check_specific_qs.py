import json

with open("app/data/india_placement_depth.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for qid in ["ind-apt-age-1", "ind-apt-profit-1", "ind-apt-mixture-1"]:
    for q in data:
        if q.get("id") == qid:
            print(f"{qid}:")
            print(f"  correct_answer={q.get('correct_answer')!r}")
            print(f"  correct_index={q.get('correct_index')!r}")
            print(f"  options={q.get('options')}")
            print(f"  testcases={q.get('testcases')}")
            print()
