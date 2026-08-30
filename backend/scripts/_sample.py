import json

d = json.load(open("app/data/questions_bank.json", encoding="utf-8"))
unknown = [q for q in d if not q.get("type")]
coding = [q for q in d if q.get("type") == "coding"]

out = []
out.append("=== 2 unknown-type samples ===")
for q in unknown[:2]:
    out.append(json.dumps(q, indent=1, ensure_ascii=False)[:1200])
    out.append("----")

out.append("=== 2 coding samples (keys) ===")
for q in coding[:2]:
    out.append("KEYS: " + str(list(q.keys())))
out.append("----")

out.append("=== coding sample full ===")
out.append(json.dumps(coding[0], indent=1, ensure_ascii=False)[:1800])
out.append("----")

has_opts = sum(1 for q in unknown if q.get("options") not in (None, []))
has_tc = sum(1 for q in unknown if q.get("testcases") not in (None, []))
out.append("unknown-type: total %d | with options: %d | with testcases: %d" % (len(unknown), has_opts, has_tc))
tc_sample = [q for q in coding if q.get("testcases")]
out.append("coding testcase example shape:")
if tc_sample:
    t = tc_sample[0]["testcases"]
    out.append(json.dumps(t[0] if isinstance(t, list) else t, ensure_ascii=False)[:400])
out.append("coding solution example shape:")
if coding[0].get("solution"):
    out.append(json.dumps(coding[0]["solution"], ensure_ascii=False)[:400])

with open("C:/Users/Admin/AppData/Local/Temp/opencode/_sample_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("done")