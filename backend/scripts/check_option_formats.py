import json

with open("app/data/india_placement_depth.json", "r", encoding="utf-8") as f:
    data = json.load(f)

standard_mcqs = 0
non_standard = 0
for q in data:
    t = str(q.get("type", "")).lower()
    if t not in ("aptitude", "logical", "verbal", "hr", "cs_fundamentals"):
        continue
    
    opts = q.get("options", [])
    if not opts:
        continue
    
    # Check if options are simple values (numbers) rather than strings
    all_numbers = all(isinstance(o, (int, float)) for o in opts)
    all_strings = all(isinstance(o, str) for o in opts)
    
    if all_numbers and len(opts) == 4:
        non_standard += 1
    elif all_strings and len(opts) == 4:
        standard_mcqs += 1
    else:
        print(f"Other format: {q.get('id')} opts={opts}")

print(f"Standard MCQs (string options): {standard_mcqs}")
print(f"Non-standard (numeric options): {non_standard}")
print(f"Total MCQ-type: {standard_mcqs + non_standard}")
