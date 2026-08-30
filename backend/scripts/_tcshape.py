import json

d = json.load(open("app/data/questions_bank.json", encoding="utf-8"))
coding = [q for q in d if q.get("type") == "coding"]

out = []
out.append("=== testcases field type/value samples (coding) ===")
n = 0
for q in coding:
    tcs = q.get("testcases")
    if tcs:
        out.append("id=%s type=%s sample=%s" % (q.get("id"), type(tcs).__name__, json.dumps(tcs[:2], ensure_ascii=False)[:500]))
        n += 1
        if n >= 8:
            break
if n == 0:
    out.append("NO coding questions have testcases")

# problem statement sample lengths
out.append("\n=== coding problem statements (short/long) ===")
for q in coding[:6]:
    qq = (q.get("question") or "")[:120].replace("\n", " ")
    out.append("id=%s len=%d: %s" % (q.get("id"), len(q.get("question") or ""), qq))

with open("C:/Users/Admin/AppData/Local/Temp/opencode/_tcshape.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")