import json
from collections import Counter

VERIFIED = r"D:\Project-Fremen\backend\app\data\verified_placement_questions.json"
PACKS = r"D:\Project-Fremen\backend\app\data\trusted_packs.json"
OUT = r"D:\Project-Fremen\backend\app\data\pack_validity_report.json"

verified = json.load(open(VERIFIED, encoding="utf-8"))
packs = json.load(open(PACKS, encoding="utf-8"))["packs"]

# Index verified by type and difficulty
by_type = Counter(q["type"] for q in verified)
by_diff = Counter(q["difficulty"] for q in verified)
by_topic = Counter(q.get("topic","") for q in verified)

# Check for duplicates (normalized title)
seen={}
dups=[]
for q in verified:
    norm = (q.get("title") or q.get("question",""))[:60].strip().lower()
    if norm in seen:
        dups.append((q["id"], seen[norm]))
    else:
        seen[norm]=q["id"]

report=[]
for p in packs:
    secs = p["sections"]
    total = p["total_questions"]
    # check sufficient per section
    section_ok={}
    all_ok=True
    for sec, need in secs.items():
        have = by_type.get(sec, 0)
        # mapping: coding->coding, aptitude->aptitude, etc. cs_fundamentals maps to cs_fundamentals
        # verified uses type names directly
        ok = have >= need
        section_ok[sec] = {"need": need, "have": have, "ok": ok}
        if not ok: all_ok=False
    # also check total
    total_ok = sum(secs.values()) == total
    # difficulty balance: check verified has mix
    diff_ok = by_diff["easy"]>=5 and by_diff["medium"]>=5 and by_diff["hard"]>=2
    # duration realistic: 60-120
    dur_ok = 60 <= p["duration_minutes"] <= 120
    # provenance
    prov_ok = p.get("provenance")=="pattern_relevant"
    # duplicate check global
    dup_ok = len(dups)==0
    # scoring (all packs have scoring via OA)
    validity = all([all_ok, total_ok, diff_ok, dur_ok, prov_ok, dup_ok])
    report.append({
        "id": p["id"],
        "company": p["company"],
        "stage": p["stage"],
        "total": total,
        "sections": secs,
        "section_availability": section_ok,
        "total_matches_sections": total_ok,
        "difficulty_balance": dict(by_diff),
        "difficulty_ok": diff_ok,
        "duration": p["duration_minutes"],
        "duration_ok": dur_ok,
        "provenance": p.get("provenance"),
        "provenance_ok": prov_ok,
        "duplicates": len(dups),
        "duplicates_ok": dup_ok,
        "valid": validity,
        "verdict": "READY" if validity else "NEEDS_CONTENT"
    })

json.dump({"verified_pool": {"total": len(verified), "by_type": dict(by_type), "by_difficulty": dict(by_diff), "by_topic": dict(by_topic), "duplicates": len(dups)}, "packs": report}, open(OUT,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"Verified pool: {len(verified)} by_type={dict(by_type)} by_diff={dict(by_diff)} dups={len(dups)}")
for r in report:
    print(f"  {r['id']:22s} valid={r['valid']} total={r['total']} {r['verdict']}")
print(f"Wrote {OUT}")
