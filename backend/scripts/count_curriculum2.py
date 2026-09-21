import re

for fname in ["curriculum_50_levels.py", "curriculum_enrichment.py"]:
    path = "D:\\Project-Fremen\\backend\\app\\data\\" + fname
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    total = len(re.findall(r"\_L\s*\(", content))
    quizzes = len(re.findall(r'"quiz"', content))
    print(f"{fname}: total lessons = {total}, quiz type refs = {quizzes}")
