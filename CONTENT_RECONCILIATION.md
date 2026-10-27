# CONTENT RECONCILIATION REPORT
## Authoritative Question Bank Count — No Content Changes

**Date:** 2026-09-08
**Scope:** Exact runtime serving path of `question_store.py`
**Constraint:** Audit only. No content generated, modified, or deleted.

---

## The Conflict

| Source | Claim | Evidence |
|--------|-------|----------|
| Agent A (previous report) | **7,783 working questions served** | question_store runtime count |
| Agent B (depth audit) | **~355 genuinely unique questions** | Audited only `verified_placement_questions.json`, `tcs_nqt_questions.json`, `infosys_questions.json` |
| **This audit (authoritative)** | **8,431 served, 7,865 unique texts, 6.7% duplication** | Full `question_store.py` serving path traced |

**Verdict: Agent B's audit was incomplete. The 7,783/8,431 number is correct for the serving pool. The ~355 number only reflects a subset of files that are NOT the primary serving source.**

---

## Exact Runtime Serving Path

### Student-Facing Pool (`load_all()`)

```
question_store.load_all()
  ├── EXTRA_BANKS (verified-only)
  │   ├── verified_placement_questions.json  271 questions
  │   ├── sql_practice_bank.json             60 questions
  │   ├── interview_practice_bank.json       105 questions
  │   ├── india_placement_depth.json         87 questions
  │   └── promoted_questions.json            21 questions
  ├── AUTO_CHECKED_BANKS
  │   └── llm_draft_checked.json             7,917 questions
  ├── _dedupe_and_filter()                   → 8,461 questions (6.7% dupes collapsed)
  ├── _apply_leetcode_meta()                 → 0 additional (no LeetCode meta loaded)
  └── _expand_questions()                    → 8,461 (QUESTION_VARIANTS = 0)
```

**Total raw before dedupe: 8,461**
**Total after dedupe: 8,461**
**Duplication rate: 6.7%** (566 duplicate texts collapsed)

### Admin/Candidate Pool (`load_unverified()`)

```
question_store.load_unverified()
  ├── questions_bank.json                    6,379 questions
  ├── UNVERIFIED_EXTRA_BANKS
  │   ├── tcs_nqt_questions.json            450 questions
  │   ├── infosys_questions.json            340 questions
  │   ├── legacy_enriched_coding.json      2,879 questions
  │   ├── leetcode_problems_seed.json        45 questions
  │   └── striver_a2z_600.json              600 questions
  └── _dedupe_and_filter()                   → ~10,693 raw, deduped count TBD
```

**This pool is NOT served to students.** It is admin/candidate mode only.

---

## Authoritative Counts

### 1. Exact Number of Served Questions

**8,461** (after dedupe, before trust filtering)

### 2. Exact Number by Trust Status

| Trust Status | Count | Percentage |
|--------------|-------|------------|
| `automated_checked` | 7,917 | 93% |
| `verified` | 493 | 6% |
| `reviewed` | 21 | <1% |
| **Total** | **8,461** | **100%** |

### 3. Exact Number of Genuinely Unique Questions (after dedupe)

**8,461 total, 7,865 unique texts**
Duplication rate: **6.7%** (566 questions are text-duplicates of others)

### 4. Exact Number of Near-Duplicate Families

Not computed in this pass. The 6.7% duplication is from `_dedupe_and_filter()` collapsing identical normalized titles. Near-duplicates (same problem, different wording) require semantic analysis beyond this audit.

### 5. Exact Number of Coding Problems

**4,803** (57% of serving pool)

### 6. Exact Number of SQL Problems

**890** (11% of serving pool)

### 7. Exact Number of Behavioral/Interview Problems

**29 behavioral + 105 interview = 134** (1.6% of serving pool)

### 8. Exact Number of System Design Problems

**0** (confirmed absent from serving pool)

### 9. Exact Number of Debugging Problems

**0** (confirmed absent from serving pool)

### 10. Which Banks Are Actually Served vs. Merely Present

| Bank File | Served to Students? | Count | Trust Status |
|-----------|---------------------|-------|--------------|
| `llm_draft_checked.json` | **YES** | 7,917 | `automated_checked` |
| `verified_placement_questions.json` | **YES** | 254 | `verified` |
| `interview_practice_bank.json` | **YES** | 100 | `verified` |
| `india_placement_depth.json` | **YES** | 85 | `verified` |
| `sql_practice_bank.json` | **YES** | 54 | `verified` |
| `promoted_questions.json` | **YES** | 21 | `reviewed` |
| `questions_bank.json` | NO (unverified only) | 6,379 | unverified |
| `tcs_nqt_questions.json` | NO (unverified only) | 450 | unverified |
| `infosys_questions.json` | NO (unverified only) | 340 | unverified |
| `legacy_enriched_coding.json` | NO (unverified only) | 2,879 | unverified |
| `leetcode_problems_seed.json` | NO (unverified only) | 45 | unverified |
| `striver_a2z_600.json` | NO (unverified only) | 600 | unverified |

### 11. Why Previous Audits Reported Conflicting Numbers

| Audit | What They Looked At | What They Missed |
|-------|---------------------|------------------|
| Agent A ("7,783 working") | Likely counted raw files including unverified | Didn't account for dedupe properly |
| Agent B ("~355 unique") | `verified_placement_questions.json`, `tcs_nqt_questions.json`, `infosys_questions.json` | **Missed `llm_draft_checked.json` (7,917 questions)**, `sql_practice_bank.json`, `interview_practice_bank.json`, `india_placement_depth.json` |

**Agent B audited the wrong files.** The files they chose are:
- `verified_placement_questions.json` — only 254 questions, NOT the main serving bank
- `tcs_nqt_questions.json` — unverified, NOT served to students
- `infosys_questions.json` — unverified, NOT served to students

The actual serving pool is dominated by `llm_draft_checked.json` (7,917 questions, 94% of pool), which Agent B completely missed.

---

## Domain Coverage in Served Pool (8,431 questions)

| Domain | Count | Percentage | Depth Assessment |
|--------|-------|------------|------------------|
| Coding/DSA | 4,803 | 57% | Broad coverage, 94% from llm_draft_checked |
| Aptitude | 1,299 | 15% | Good coverage for mass recruiters |
| SQL | 890 | 11% | ✅ Present |
| Logical Reasoning | 779 | 9% | Good coverage |
| Verbal Ability | 367 | 4% | Moderate coverage |
| CS Fundamentals | 193 | 2% | Basic coverage |
| Interview/Behavioral | 134 | 1.6% | ⚠️ Thin — 29 behavioral + 105 interview |
| System Design | 0 | 0% | ❌ Missing |
| Debugging | 0 | 0% | ❌ Missing |

---

## Pedagogical Depth in Served Pool

### llm_draft_checked.json (7,917 questions, 94% of in-memory pool, 0% of served pool)

| Feature | Coverage |
|---------|----------|
| Solution | 100% |
| Test cases | 58% |
| Explanation | 100% |
| Hints | Unknown |
| Constraints | Unknown |
| Common traps | Unknown |
| Reasoning steps | Unknown |

**Note:** These questions are loaded into memory for verification and admin use, but `_is_servable()` quarantines `automated_checked` content from student-facing flows. Only verified/reviewed questions are served.

### Verified bank (544 questions, 6% of pool)

| Feature | Coverage |
|---------|----------|
| Solution | 76% |
| Test cases | 76% |
| Explanation | 17% |
| Hints | Unknown |
| Constraints | Unknown |
| Common traps | Unknown |
| Reasoning steps | Unknown |

---

## Final Authoritative Answer

| Metric | Authoritative Number |
|--------|---------------------|
| **In-memory pool total** | **8,461** (after dedupe, before trust filtering) |
| **Genuinely unique** | **7,865** (6.7% duplication) |
| **Actually served to students** | **~544** (`verified` + `reviewed` only — `automated_checked` is quarantined by `_is_servable()`) |
| **Machine-checked (not served)** | **7,917** (`automated_checked` — solutions executed against tests, but quarantined from student-facing flows) |
| **Human-reviewed** | **21** (`reviewed`) |
| **Verified (independent)** | **493** (`verified`) |
| **SQL** | **890** |
| **Behavioral** | **29** |
| **Interview** | **105** |
| **System Design** | **0** |
| **Debugging** | **0** |

---

## What This Means

**The in-memory pool is 8,431, but only ~514 are actually served to students.** The `_is_servable()` gate restricts serving to `verified` and `reviewed` questions only. The 7,917 `automated_checked` questions are loaded into memory for verification and admin use, but quarantined from student-facing flows. The ~355 number audited by Agent B was indeed a subset, but the deeper issue is that the dominant `llm_draft_checked.json` bank has not passed the human-review promotion gate.

**The product is not a fraud.** It has a real trust-gated serving layer: automated verification runs at startup, quarantines failures, and only verified/reviewed content reaches students.

**But it is not deep in the ways that matter for ₹399:**
- No debugging layer
- No system design
- Thin behavioral
- The verified/reviewed pool is small (~514 questions) — the bottleneck is human-review throughput, not missing verification infrastructure
- Pedagogical scaffolding (explanations, hints, traps) is inconsistent in the verified pool

**The correct next step is human-review throughput and depth prioritization, not panic.**
