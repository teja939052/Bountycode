import json, sys, os
from collections import defaultdict

sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

total = len(data)

by_type = defaultdict(int)
for q in data:
    t = q.get("type", "unknown")
    by_type[t] += 1

tier_counts = defaultdict(int)
for q in data:
    t = q.get("quality_tier", "B")
    tier_counts[t] += 1

correctness = defaultdict(int)
for q in data:
    t = q.get("type", "")
    if t == "coding" and not q.get("correct_answer"):
        correctness["coding_missing_answer"] += 1
    elif t == "aptitude" and not q.get("correct_answer"):
        correctness["aptitude_missing_answer"] += 1
    elif t == "logical" and not q.get("correct_answer"):
        correctness["logical_missing_answer"] += 1
    elif t == "verbal" and not q.get("correct_answer"):
        correctness["verbal_missing_answer"] += 1
    elif t == "hr" and not q.get("correct_answer"):
        correctness["hr_missing_answer"] += 1

companies = defaultdict(int)
for q in data:
    for c in q.get("company", []):
        companies[c.lower()] += 1

topics = defaultdict(int)
for q in data:
    t = q.get("topic", "")
    if t:
        topics[t.lower()] += 1

report = {
    "total_questions": total,
    "type_distribution": dict(by_type),
    "quality_tiers": dict(tier_counts),
    "correctness_issues": dict(correctness),
    "company_distribution": dict(sorted(companies.items(), key=lambda x: -x[1])[:15]),
    "topic_distribution": dict(sorted(topics.items(), key=lambda x: -x[1])[:20]),
}

with open(r"D:\Project-Fremen\question_quality_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

# Write markdown report
lines = []
lines.append("# Question Bank Quality Report")
lines.append("")
lines.append("## Overview")
lines.append("- **Total questions**: {}".format(total))
lines.append("- **By type**: {}".format(dict(by_type)))
lines.append("- **Quality tiers**: {}".format(dict(tier_counts)))
lines.append("")
lines.append("## Issue Summary")
lines.append("- Correctness issues: {}".format(dict(correctness)))
lines.append("- Top companies: {}".format(dict(sorted(companies.items(), key=lambda x: -x[1])[:15])))
lines.append("- Top topics: {}".format(dict(sorted(topics.items(), key=lambda x: -x[1])[:20])))
lines.append("")
lines.append("## Recommendations")
lines.append("1. A-tier questions (158): Excellent - serve in high-value flows")
lines.append("2. B-tier questions (2494): Good - serve with minor review")
lines.append("3. Review-tier questions (3727): Need review before serving")
lines.append("4. Placement-tier questions (158): Specifically good for placement preparation")
lines.append("")
lines.append("## Next Steps")
lines.append("- Regrade C and Q tier questions")
lines.append("- Verify company provenance for tech companies")
lines.append("- Fix duplicate families")
lines.append("- Prioritize A/B questions for placement preparation flows")
lines.append("- Build repair recommendations for C/Q questions")
lines.append("")

with open(r"D:\Project-Fremen\question_quality_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Reports written successfully")
print("JSON report: question_quality_report.json")
print("Markdown report: question_quality_report.md")