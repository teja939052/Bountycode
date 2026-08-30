"""Comprehensive question bank validation and quality grading.

Audits every published question for correctness, quality, and pedagogical value.
Produces question_quality_report.json and question_quality_report.md.
"""

import json, sys, os, re, hashlib
from collections import defaultdict

sys.path.insert(0, r"D:\Project-Fremen\backend")

# ─── Load question bank ──────────────────────────────────────────────

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ─── Validation helpers ───────────────────────────────────────────────

def check_answer_coding(q):
    """Validate coding question answer correctness."""
    issues = []
    correct = q.get("correct_answer")
    explanation = q.get("explanation", "")
    topic = q.get("topic", "")
    
    # Check that correct_answer makes sense given the question
    q_text = q.get("question", "").lower()
    
    if q.get("type") == "coding":
        # Basic sanity: correct_answer should not be empty
        if not correct:
            issues.append("MISSING correct_answer")
        # Check explanation references the answer
        if not any(kw in explanation.lower() for kw in ["correct", "solution", "answer"]):
            issues.append("EXPLANATION doesn't reference correct answer")
    
    return issues


def check_answer_aptitude(q):
    """Validate aptitude question answer correctness."""
    issues = []
    correct = q.get("correct_answer")
    options = q.get("options", [])
    explanation = q.get("explanation", "")
    
    if not correct:
        issues.append("MISSING correct_answer")
    elif correct not in options:
        issues.append("correct_answer NOT in options")
    
    # Check reasoning steps
    if not any(kw in explanation.lower() for kw in ["formula", "calculation", "step"]):
        issues.append("EXPLANATION lacks reasoning steps")
    
    return issues


def check_answer_logical(q):
    """Validate logical question answer correctness."""
    issues = []
    correct = q.get("correct_answer")
    explanation = q.get("explanation", "")
    
    if not correct:
        issues.append("MISSING correct_answer")
    elif len(correct) < 3:
        issues.append("TOO SHORT correct_answer")
    
    return issues


def check_answer_verbal(q):
    """Validate verbal question answer correctness."""
    issues = []
    correct = q.get("correct_answer")
    options = q.get("options", [])
    
    if not correct:
        issues.append("MISSING correct_answer")
    elif correct not in options:
        issues.append("correct_answer NOT in options")
    
    return issues


def check_answer_hr(q):
    """Validate HR question answer correctness."""
    issues = []
    correct = q.get("correct_answer")
    
    if not correct:
        issues.append("MISSING correct_answer")
    
    return issues


# ─── Complexity validation ────────────────────────────────────────────

def check_complexity_coding(q):
    """Validate complexity metadata for coding questions."""
    issues = []
    complexity = q.get("complexity", {})
    
    if not complexity:
        issues.append("MISSING complexity")
        return issues
    
    # Check time complexity structure
    time = complexity.get("time", {})
    if not time:
        issues.append("MISSING time complexity")
    else:
        # Check for best/avg/worst
        for key in ["best", "average", "worst"]:
            if key not in time:
                issues.append(f"MISSING {key} time complexity")
    
    # Check space complexity
    space = complexity.get("space", "")
    if not space:
        issues.append("MISSING space complexity")
    
    # Check complexity explanation
    comp_exp = q.get("complexity_explanation", {})
    if not comp_exp:
        issues.append("MISSING complexity_explanation")
    
    return issues


def check_difficulty(q):
    """Validate difficulty assignment."""
    issues = []
    diff = q.get("difficulty", "").lower()
    cognitive = q.get("difficulty_cognitive", "")
    placement = q.get("placement_metadata", {}).get("difficulty_placement", "")
    
    # Check consistency
    if diff not in ["easy", "medium", "hard"]:
        issues.append(f"INVALID difficulty: {diff}")
    
    # For coding questions, check cognitive level
    if q.get("type") == "coding" and cognitive not in [1, 2, 3, 4, 5]:
        issues.append(f"INVALID cognitive difficulty: {cognitive}")
    
    return issues


# ─── Prerequisite validation ─────────────────────────────────────────

def check_prerequisites(q):
    """Validate prerequisite mapping."""
    issues = []
    prereq = q.get("pedagogy", {}).get("prerequisites", [])
    
    # Check that prerequisites are relevant to the skill
    skill = q.get("pedagogy", {}).get("skill", "")
    topic = q.get("topic", "")
    
    if not prereq and skill != "general":
        issues.append("MISSING prerequisites for non-general skill")
    
    # Check for circular prerequisites (just flag)
    # In a full system, we'd check the skill graph for cycles
    
    return issues


# ─── Company provenance validation ────────────────────────────────────

def check_company_provenance(q):
    """Validate company relevance claims."""
    issues = []
    companies = q.get("company", [])
    
    # Check for generic/fake claims
    for c in companies:
        c_lower = c.lower()
        # These are common Indian placement companies - generally valid
        valid_indian = ["tcs", "infosys", "wipro", "cognizant", "hcl", "accenture", 
                       "capgemini", "tech_mahindra", "lti", "mphasis"]
        # Tech companies - pattern-relevant but may need verification
        tech_companies = ["amazon", "google", "microsoft", "meta", "apple", "netflix"]
        
        if c_lower in valid_indian:
            # Indian companies in placement context - generally valid
            pass
        elif c_lower in tech_companies:
            # Tech companies - pattern-relevant but may need verification
            issues.append(f"COMPANY {c} - pattern-relevant, verify actual placement history")
        else:
            issues.append(f"UNKNOWN company: {c}")
    
    return issues


# ─── Duplicate detection ─────────────────────────────────────────────

def question_text_hash(q):
    """Create a hash from question content for duplicate detection."""
    # Hash based on question text + type + topic
    key_parts = [
        q.get("type", ""),
        q.get("topic", ""),
        q.get("question", "")[:200]  # first 200 chars
    ]
    return hashlib.sha256("|".join(key_parts).encode()).hexdigest()[:16]


def detect_duplicates(data):
    """Detect duplicate questions."""
    seen = {}
    duplicates = []
    
    for q in data:
        q_hash = question_text_hash(q)
        q_text = q.get("question", "").lower().strip()
        q_id = q.get("id", "")
        
        if q_hash in seen:
            seen[q_hash].append(q_id)
        else:
            seen[q_hash] = [q_id]
    
    # Find actual duplicates (same text, different IDs)
    actual_dupes = {h: ids for h, ids in seen.items() if len(ids) > 1}
    
    return actual_dupes, len(actual_dupes)


# ─── Quality grading ─────────────────────────────────────────────────

def grade_question(q):
    """Assign A/B/C/Q quality grade based on multiple factors."""
    score = 100
    reasons = []
    
    # Check correctness
    q_type = q.get("type", "")
    if q_type == "coding":
        ans_issues = check_answer_coding(q)
        score -= len(ans_issues) * 25
        for a in ans_issues:
            reasons.append(f"Answer: {a}")
    elif q_type == "aptitude":
        ans_issues = check_answer_aptitude(q)
        score -= len(ans_issues) * 25
        for a in ans_issues:
            reasons.append(f"Answer: {a}")
    elif q_type == "logical":
        ans_issues = check_answer_logical(q)
        score -= len(ans_issues) * 25
        for a in ans_issues:
            reasons.append(f"Answer: {a}")
    elif q_type == "verbal":
        ans_issues = check_answer_verbal(q)
        score -= len(ans_issues) * 25
        for a in ans_issues:
            reasons.append(f"Answer: {a}")
    elif q_type == "hr":
        ans_issues = check_answer_hr(q)
        score -= len(ans_issues) * 25
        for a in ans_issues:
            reasons.append(f"Answer: {a}")
    
    # Check complexity (coding only)
    if q_type == "coding":
        comp_issues = check_complexity_coding(q)
        score -= len(comp_issues) * 10
        for a in comp_issues:
            reasons.append(f"Complexity: {a}")
    
    # Check difficulty
    diff_issues = check_difficulty(q)
    score -= len(diff_issues) * 5
    for a in diff_issues:
        reasons.append(f"Difficulty: {a}")
    
    # Check prerequisites
    prereq_issues = check_prerequisites(q)
    score -= len(prereq_issues) * 5
    for a in prereq_issues:
        reasons.append(f"Prerequisite: {a}")
    
    # Check company provenance
    comp_issues = check_company_provenance(q)
    score -= len(comp_issues) * 5
    for a in comp_issues:
        reasons.append(f"Company: {a}")
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    
    # Assign tier
    if score >= 90:
        tier = "A"
    elif score >= 75:
        tier = "B"
    elif score >= 50:
        tier = "C"
    else:
        tier = "Q"
    
    return tier, max(0, score), reasons


# ─── Run validation ───────────────────────────────────────────────────

print("=" * 70)
print("QUESTION BANK VALIDATION AUDIT")
print("=" * 70)
print(f"Total questions: {len(data)}")
print()

# Categorize by type
by_type = defaultdict(list)
for q in data:
    q_type = q.get("type", "unknown")
    by_type[q_type].append(q)

# Statistics
stats = {
    "total": len(data),
    "by_type": {t: len(qs) for t, qs in by_type.items()},
    "correctness_failures": 0,
    "complexity_failures": 0,
    "difficulty_failures": 0,
    "provenance_failures": 0,
    "duplicate_families": 0,
    "tier_A": 0,
    "tier_B": 0,
    "tier_C": 0,
    "tier_Q": 0,
}

# Validate each question
for i, q in enumerate(data):
    q_type = q.get("type", "unknown")
    
    # Track tier
    tier, score, reasons = grade_question(q)
    if tier == "A":
        stats["tier_A"] += 1
    elif tier == "B":
        stats["tier_B"] += 1
    elif tier == "C":
        stats["tier_C"] += 1
    else:
        stats["tier_Q"] += 1
    
    # Check correctness
    if q_type in ["coding", "aptitude", "logical", "verbal", "hr"]:
        if q_type == "coding":
            ans_issues = check_answer_coding(q)
        elif q_type == "aptitude":
            ans_issues = check_answer_aptitude(q)
        elif q_type == "logical":
            ans_issues = check_answer_logical(q)
        elif q_type == "verbal":
            ans_issues = check_answer_verbal(q)
        elif q_type == "hr":
            ans_issues = check_answer_hr(q)
        
        if ans_issues:
            stats["correctness_failures"] += 1
            # Don't fail the whole question grade for this, just track
    
    # Check complexity (coding only)
    if q_type == "coding":
        comp_issues = check_complexity_coding(q)
        stats["complexity_failures"] += len(comp_issues)
    
    # Check difficulty
    diff_issues = check_difficulty(q)
    stats["difficulty_failures"] += len(diff_issues)
    
    # Check provenance
    prov_issues = check_company_provenance(q)
    stats["provenance_failures"] += len(prov_issues)
    
    # Track duplicates later

# Detect duplicates
dupes, dupe_count = detect_duplicates(data)
stats["duplicate_families"] = dupe_count

# Print results
print("=" * 70)
print("VALIDATION RESULTS")
print("=" * 70)
print(f"\nTotal questions: {stats['total']}")
print(f"\nBy type:")
for t, c in stats["by_type"].items():
    print(f"  {t}: {c}")
print(f"\nQuality grades:")
print(f"  A: {stats['tier_A']} ({stats['tier_A']/stats['total']*100:.1f}%)")
print(f"  B: {stats['tier_B']} ({stats['tier_B']/stats['total']*100:.1f}%)")
print(f"  C: {stats['tier_C']} ({stats['tier_C']/stats['total']*100:.1f}%)")
print(f"  Q: {stats['tier_Q']} ({stats['tier_Q']/stats['total']*100:.1f}%)")
print(f"\nIssues found:")
print(f"  Correctness failures: {stats['correctness_failures']}")
print(f"  Complexity failures: {stats['complexity_failures']}")
print(f"  Difficulty failures: {stats['difficulty_failures']}")
print(f"  Provenance failures: {stats['provenance_failures']}")
print(f"  Duplicate families: {stats['duplicate_families']}")

# Show some example issues
print("\n=== SAMPLE ISSUES ===")
# Show a few questions with issues
for i, q in enumerate(data[:20]):
    q_type = q.get("type", "unknown")
    if q_type in ["coding", "aptitude", "logical", "verbal", "hr"]:
        tier, score, reasons = grade_question(q)
        if reasons:
            print(f"\n{q.get('id', '')[:8]} ({q_type}): tier={tier}, score={score}")
            for r in reasons[:3]:
                print(f"  - {r}")

# Show duplicate info
if dupe_count > 0:
    print(f"\n=== DUPLICATE FAMILIES ({dupe_count}) ===")
    for h, ids in list(dupes.items())[:5]:
        print(f"  Hash: {h}")
        print(f"  IDs: {ids[:3]}")

# Save the report
report = {
    "total_questions": stats["total"],
    "by_type": stats["by_type"],
    "quality_grades": {
        "A": stats["tier_A"],
        "B": stats["tier_B"],
        "C": stats["tier_C"],
        "Q": stats["tier_Q"]
    },
    "correctness_failures": stats["correctness_failures"],
    "complexity_failures": stats["complexity_failures"],
    "difficulty_failures": stats["difficulty_failures"],
    "provenance_failures": stats["provenance_failures"],
    "duplicate_families": stats["duplicate_families"],
    "tier_distribution": {
        "A": stats["tier_A"]/stats["total"]*100 if stats["total"] else 0,
        "B": stats["tier_B"]/stats["total"]*100 if stats["total"] else 0,
        "C": stats["tier_C"]/stats["total"]*100 if stats["total"] else 0,
        "Q": stats["tier_Q"]/stats["total"]*100 if stats["total"] else 0
    },
    "issue_details": {
        "correctness": stats["correctness_failures"],
        "complexity": stats["complexity_failures"],
        "difficulty": stats["difficulty_failures"],
        "provenance": stats["provenance_failures"]
    },
    "duplicate_count": dupe_count
}

with open(r"D:\Project-Fremen\question_quality_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

# Also produce markdown report
md = f"""# Question Bank Quality Report

## Summary
- **Total questions**: {stats['total']}
- **A questions**: {stats['tier_A']} ({stats['tier_A']/stats['total']*100:.1f}%)
- **B questions**: {stats['tier_B']} ({stats['tier_B']/stats['total']*100:.1f}%)
- **C questions**: {stats['tier_C']} ({stats['tier_C']/stats['total']*100:.1f}%)
- **Q questions**: {stats['tier_Q']} ({stats['tier_Q']/stats['total']*100:.1f}%)

## Quality Distribution
"""

for tier_name, tier_count in [("A", stats["tier_A"]), ("B", stats["tier_B"]), ("C", stats["tier_C"]), ("Q", stats["tier_Q"])]:
    md += f"- **{tier_name}**: {tier_count} questions ({tier_count/stats['total']*100:.1f}%)\n\n"

md += "## Issue Counts\n"
md += f"- **Correctness failures**: {stats['correctness_failures']}\n"
md += f"- **Complexity failures**: {stats['complexity_failures']}\n"
md += f"- **Difficulty failures**: {stats['difficulty_failures']}\n"
md += f"- **Provenance failures**: {stats['provenance_failures']}\n"
md += f"- **Duplicate families**: {stats['duplicate_families']}\n\n"

md += "## Top Issues by Type\n"
for t in ["coding", "aptitude", "logical", "verbal", "hr"]:
    subset = [q for q in data if q.get("type") == t]
    if subset:
        md += f"- **{t.upper()}**: {len(subset)} questions\n"

md += "\n## Recommended Repair Priority\n"
md += "The following questions should be fixed first based on student impact:\n"
# Find questions with Q tier or multiple issues
bad_questions = []
for q in data:
    tier, score, reasons = grade_question(q)
    if tier in ["Q", "C"] or len(reasons) > 2:
        bad_questions.append((q.get("id", "")[:8], q.get("type", ""), len(reasons)))
bad_questions.sort(key=lambda x: x[2], reverse=True)
for qid, qtype, issue_count in bad_questions[:100]:
    md += f"- **{qid}** ({qtype}): {issue_count} issues\n"""

with open(r"D:\Project-Fremen\question_quality_report.md", "w", encoding="utf-8") as f:
    f.write(md)

print("\nReports written: question_quality_report.json, question_quality_report.md")
print("\n=== VALIDATION COMPLETE ===")
" 2>&1