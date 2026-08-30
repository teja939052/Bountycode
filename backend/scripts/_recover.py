import json
from collections import Counter

d = json.load(open("app/data/questions_bank.json", encoding="utf-8"))

def code_of(q):
    s = q.get("solution")
    return s.get("code") if isinstance(s, dict) else s if isinstance(s, str) else ""

coding = [q for q in d if q.get("type") == "coding"]
shells = [q for q in d if not q.get("type")]
others = [q for q in d if q.get("type") not in ("coding", None)]

print("shell-family (no type):", len(shells))
print("  with title+{variant}:", sum(1 for q in shells if "{" in (q.get("title") or "")))
print("  testcases present:", sum(1 for q in shells if q.get("testcases")))
print("  correct_answer present:", sum(1 for q in shells if q.get("correct_answer") not in (None, "")))
print("  solution.code present:", sum(1 for q in shells if code_of(q)))
print()
print("coding-family:", len(coding))
print("  solution.code present:", sum(1 for q in coding if code_of(q)))
print("  correct_answer present:", sum(1 for q in coding if q.get("correct_answer") not in (None, "")))
print("  testcases present:", sum(1 for q in coding if q.get("testcases")))
print("  question text length>=40:", sum(1 for q in coding if len(q.get("question") or "") >= 40))
print("  has explanation:", sum(1 for q in coding if q.get("explanation")))
print("  has hints:", sum(1 for q in coding if q.get("hints")))
print()
print("other typed (aptitude/logical/verbal):", len(others))
print("  type dist:", dict(Counter(q.get("type") for q in others)))
print("  with options:", sum(1 for q in others if q.get("options")))
print("  with correct_answer:", sum(1 for q in others if q.get("correct_answer") not in (None, "")))

fnames = []
import re
for q in coding:
    m = re.search(r"^def\s+(\w+)\s*\(", code_of(q).strip(), re.M)
    if m:
        fnames.append(m.group(1))
from collections import Counter as C
print()
print("coding with def-signature:", len(fnames))
print("sample function names:", list(C(fnames).most_common(15)))