import re
with open("D:\\Project-Fremen\\backend\\app\\data\\curriculum.py", "r", encoding="utf-8") as f:
    content = f.read()
counts = {"theory": 0, "practice": 0, "challenge": 0, "project": 0, "quiz": 0, "boss": 0}
total_lessons = len(re.findall(r"_L\s*\(", content))
for t in counts:
    counts[t] = len(re.findall('"' + t + '"', content))
print(f"Total _L() calls: {total_lessons}")
for t, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")
