# Content Trust v1 — Honest Quality Assessment
**Date:** 2026-08-30

## Executive Summary

**The question bank is 2.7% trustworthy.** Metadata completeness does NOT equal content correctness.

| Metric | Value |
|--------|-------|
| Total questions | 6,389 |
| Safely servable today | **~173 (2.7%)** |
| Verified end-to-end | 32 coding |
| Manual q_ questions (sensible, unverifiable) | 131 |
| HR standalone | 10 |
| Untrustworthy | 6,216 (97.3%) |

---

## Trusted Questions (~173)

| Category | Count | Notes |
|----------|-------|-------|
| Coding — verified (code runs & matches test case) | 32 | Truly portable to students |
| Coding — original manual q_ | 131 | Sensible answers, **no test cases** (unverifiable) |
| HR — standalone | 10 | Reasonable, needs rubric/evidence review |

---

## Untrustworthy Questions (6,216)

| Category | Count | Issue |
|----------|-------|-------|
| Coding — no answer / template | 3,217 | Never authored. Templates only. |
| Coding — real code, unverified/broken | 2,899 | Answer doesn't match test cases students see |
| Aptitude | 50 | **ALL duplicates** of one discount question |
| Logical | 30 | **ALL duplicates** of one series question |
| Verbal | 20 | **ALL duplicates** of one synonym question |

---

## Critical Findings

### 1. Solutions don't match their own test cases
Only **~13%** of coding test-case expected outputs match what the stored solution actually produces. If a student runs the code, they get one answer; the test case says another. **This is broken by construction.**

### 2. Auto-extracted answers are internally consistent but wrong for students
Stored answers match code output 68% of the time, but that's circular — they were extracted from code. They do NOT match the test cases students interact with.

### 3. Aptitude/Logical/Verbal are fake "distinct" questions
All 50 aptitude = same "20% + 10% discount → 28%" prompt. All 30 logical = same "1,3,6,10,? → 15". All 20 verbal = same "Synonym of Ubiquitous → Present everywhere". Only the topic **label** differs — the content doesn't match the topic. Severe duplicate + provenance failure.

### 4. 3,217 questions were never authored
Template-only solutions with `# Implement optimal solution here`. Purely empty shells.

### 5. Original 131 q_ questions can't be verified
Sensible answers but zero test cases. Cannot programmatically confirm correctness.

---

## Repair Plan (priority order)

- **P0 — Gate:** Block all Q-tier questions from student flows. Serve only the ~173 trusted now.
- **P0 — Dedupe:** Remove the 100 duplicate aptitude/logical/verbal; keep 1 each; author 28 genuine replacements.
- **P1 — High-value placement:** Repair questions tagged TCS/Infosys/Wipro/Cognizant/Accenture/Amazon/Google/Microsoft first — author correct solutions + test cases + verified answers.
- **P1 — Regenerate test cases:** For coding where code runs, execute the (corrected) solution to produce verified expected outputs, replacing unreliable stored ones.
- **P2 — Foundational:** Repair arrays/strings/hashing/linked-lists/trees/graphs/heap/greedy/backtracking/DP/SQL/OOP/DBMS/OS/Networking.
- **P2 — Author missing:** Write real solutions for the 3,217 template questions.
- **P3 — Depth:** Build Concept→Guided→Practice→Pattern→Timed→Placement→OA→Interview progressions per skill.
- **P3 — Provenance:** Only claim company relevance where verified; otherwise "pattern-relevant to X".

Every repaired question must pass: code executes, all test cases match, explanation agrees, stated complexity matches actual, title matches problem.

---

## Definition of Done (Content Trust v1)

- [ ] 100% of published questions have verified correct answers
- [ ] Q-tier questions cannot enter student flows
- [ ] B/A questions pass automated validation
- [ ] Coding questions execute successfully
- [ ] No meaningful duplicates remain
- [ ] Company claims have provenance
- [ ] Difficulty validated
- [ ] Every question maps to a skill
- [ ] Every skill has a learning progression
- [ ] Every failure generates a repair
- [ ] Repair is re-testable
- [ ] Mock OA consumes the same question evidence
- [ ] AI Interview consumes the same student evidence
- [ ] Readiness reflects demonstrated improvement

**Current completion: ~2.7%**
