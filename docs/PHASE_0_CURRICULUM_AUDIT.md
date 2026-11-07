# Phase 0 — Curriculum & Learning-System Audit

**Date:** 2026-11-07  
**Repo state audited:** `main` @ current HEAD  
**Sources used:**
- `docs/learning/LESSON_INVENTORY_summary.json`
- `docs/learning/BOUNTYCODE_LESSON_AUDIT.md` (2026-11-06)
- `docs/learning/LEARNING_EXPERIENCE_STANDARD.md`
- `backend/app/data/question_content_trust_report.json`
- `backend/app/content/world_registry.py` + World 1 / World 2 content files
- `docs/BOUNTYCODE_VISION_LOCK.md` + `docs/CURRICULUM_A_TO_Z_ROADMAP.md`

**Purpose of this document**  
Produce an honest, repository-grounded picture of what exists versus the A–Z roadmap, so we stop guessing and start fixing only what is actually broken or missing.

---

## 1. Executive summary

| Dimension | Reality |
|-----------|---------|
| **Lesson catalog size** | 1,112 unique lesson IDs |
| **Real hand-authored lessons** | ~89 (python 17, java 12, cpp 13, aptitude 7, logical 5, verbal 4, dbms 5, os 3, networks 3, oop 4, company_prep 8, ~28 real DSA) |
| **Template-filler lessons** | **1,023 (92%)** |
| **Broken prerequisite links** | **1,013** |
| **Silent ID overwrites** | 60 |
| **Question bank size** | ~6,379 |
| **Verified / TRUSTED questions** | **104** |
| **Template-shell or unverified expected-output questions** | Majority of the bank |
| **World system** | 12 worlds registered; World 1 (Foundations) and World 2 (Problem Solver) contain high-quality interactive lessons that already implement the full teaching loop |
| **Learning standard** | Excellent written standard exists (`LEARNING_EXPERIENCE_STANDARD.md`) |
| **Vision lock** | Service-company focused (TCS/Infosys/etc.), 6-world launch target |
| **A–Z roadmap** | Long-term target; far broader than current locked product |

**Bottom line:**  
The platform has a strong interactive lesson *shape* (especially in Worlds 1 & 2) and a clear learning standard, but the bulk of the catalog is filler, most questions are unverified, and the two lesson systems that previously existed created duplication and breakage.  
**Do not author large volumes of new content until the filler is purged, prerequisites are repaired, and the single source of truth is locked.**

---

## 2. Lesson inventory (ground truth)

From `LESSON_INVENTORY_summary.json`:

```json
{
  "total_lesson_rows": 1112,
  "unique_ids": 1112,
  "silently_overwritten_ids": 60,
  "template_filler_lessons": 1023,
  "broken_prerequisite_links": 1013,
  "track_counts": {
    "python": 17,
    "java": 12,
    "cpp": 13,
    "dsa": 1031,
    "aptitude": 7,
    "logical": 5,
    "verbal": 4,
    "dbms": 5,
    "os": 3,
    "networks": 3,
    "oop": 4,
    "company_prep": 8
  }
}
```

### Interpretation

- **DSA track is almost entirely generated filler.** Only a small number of real lessons (arrays, trees, etc.) are substantive.
- All other tracks are tiny. They do not constitute a complete curriculum for any of the 10 pillars.
- 1,013 broken prerequisite links mean the dependency graph is currently unusable for adaptive sequencing.
- Previous audit already recommended **purging** the template `EXTRA_DSA_LESSONS` rather than trying to salvage them.

### High-quality existing content (preserve)

- **World 1 — Foundations** (`world1_foundations.py`): real interactive lessons with discover → manipulate → predict → build → break → debug → retrieve → transfer steps, mental models, engineering context, and mastery evidence.
- **World 2 — Problem Solver** (`world2_problem_solver.py`): same high bar for core patterns (Two Pointers, Sliding Window, etc.).
- Hand-authored language tracks (python/java/cpp) and the small aptitude/logical/verbal/DBMS/OS/networks/OOP sets.

These should be the seed of the real curriculum, not discarded.

---

## 3. Question bank (ground truth)

From `question_content_trust_report.json`:

| Metric | Value |
|--------|-------|
| Bank total | 6,379 |
| Verified | **104** |
| Unverified / pending | ~6,279 |
| Repair reasons | TEMPLATE_SHELL 3,128 · UNVERIFIED_EXPECTED_OUTPUT 2,821 · TEST_CASE_MISSING 430 |
| Type distribution | coding 2,879 · aptitude 50 · logical 30 · verbal 20 · unknown 3,400 |

**Trust pipeline is not being enforced at scale.** Only 104 questions are in a verified state. The rest must not be treated as placement-ready content.

Company tagging exists at scale (Google, Microsoft, Amazon, etc. appear frequently) but without verified provenance these tags are marketing, not evidence.

---

## 4. Coverage matrix vs A–Z pillars

Status key:  
`complete` = production-ready depth + mastery evidence  
`partial` = some real content exists  
`thin` = only a handful of real lessons / questions  
`missing` = effectively absent  
`needs verification` = content present but trust/quality unknown

| Pillar | Status | Evidence |
|--------|--------|----------|
| **1. Programming foundations** | **partial** | World 1 Foundations is the strongest existing material. Language tracks exist but are small. Full beginner	o advanced path across 4 languages is incomplete. |
| **2. Data structures & algorithms** | **partial (real) + massive filler** | World 2 + ~28 real DSA lessons are good. 1,000+ template fillers must be removed. Complexity, trees, graphs, DP, advanced topics are incomplete. |
| **3. SQL & databases** | **thin** | ~5 DBMS lessons + some questions. No structured beginner	o advanced SQL curriculum with exercises, schema design, or timed assessments. |
| **4. DBMS / OS / CN / Architecture** | **thin** | OS 3, networks 3, DBMS 5. Far below placement syllabus depth. |
| **5. Quantitative aptitude** | **thin** | 7 lessons + ~50 verified aptitude questions. Not a full service-company aptitude curriculum. |
| **6. Logical reasoning & verbal** | **thin** | 5 logical + 4 verbal lessons. Insufficient for company OAs. |
| **7. Web development & practical engineering** | **missing / very thin** | No coherent HTML/CSS/JS/React/backend/deployment curriculum visible in the lesson inventory. |
| **8. System design & software engineering** | **thin** | ~20 system-design problems mentioned in earlier inventory; LLD/HLD curriculum and guided projects largely absent. |
| **9. Company-specific pathways** | **partial (service companies)** | Company journeys and blueprints exist for the locked vision (TCS, Infosys, etc.). Product-company pathways and full 4-stage pathways are incomplete. Provenance/confidence levels need enforcement. |
| **10. Resume, interview & career** | **partial** | AI interview, resume, behavioral features exist as product features. Structured curriculum + mastery model for them is incomplete. |

### Learning-system capabilities

| Capability | Status | Notes |
|------------|--------|-------|
| Learner profile + diagnostic | partial | Adaptive / readiness paths exist; full diagnostic → personalized path needs end-to-end verification |
| Skill graph + prerequisites | broken | 1,013 broken links; must be repaired before adaptive sequencing works |
| Adaptive sequencing & difficulty | partial | |
| AI tutor modes | partial | Multiple AI interview / feedback features exist |
| Misconception + repair engine | partial / needs verification | Repair is a first-class concept in the vision; implementation completeness varies |
| Mastery engine (independent evidence) | needs verification | Must not treat completion or XP as mastery |
| Spaced repetition | partial | |
| Readiness engine | partial | Company-weighted readiness exists for service companies |
| Content trust pipeline | **enforced only for 104 questions** | Must become the gate for all served content |
| Gamification tied to learning | partial | XP/tower systems exist; must continue to reward verified learning only |

---

## 5. Architectural risks (already documented, still relevant)

1. **Two divergent lesson systems** historically existed (Academy-style JSON lessons vs `services/lessons`). One source of truth must be enforced. The interactive World system (World 1 & 2 style) is the higher-quality direction.
2. **Client-side answer keys** and exact-string exercise grading were present in the older system and must not return.
3. **Filler content awards XP for low-value activity** — this violates the Gamification Law and Content Trust rules in `AGENTS.md`.
4. Backend import / route discovery has previously been broken by deleted lesson package files. Any hygiene work must keep `app.main` importable.

---

## 6. Ordered next actions (Phase 0 → Phase 1)

### Immediate (this week) — Hygiene & truthfulness

1. **Purge or quarantine the 1,023 template-filler lessons.**  
   Recommendation: remove them from the live catalog. Keep only the ~89 real lessons + World 1/2 content.  
   Update inventory and registry accordingly.

2. **Repair or remove the 1,013 broken prerequisite links.**  
   A learner must not be able to skip foundations.

3. **Confirm single lesson/world source of truth.**  
   Prefer the interactive World registry + high-quality lesson definitions. Deprecate or migrate any remaining parallel systems.

4. **Enforce the trust pipeline on the question bank.**  
   Only the 104 verified questions (or a newly verified subset) may be served as placement-quality. Everything else stays UNVERIFIED or in a repair queue.

5. **Smoke-test the full student loop** defined in `AGENTS.md`:  
   signup → onboarding → Journey → first lesson → fail → hint → repair → mastery → unlock → SRS → practice → Mock OA → weakness → repair → retest → AI Interview → readiness.

### Next (Phase 1) — Learning engine completion

- Diagnostic assessment that actually drives the next recommended lesson.
- Prerequisite checks that block navigation.
- Mastery based on independent evidence, not completion percentage or XP.
- Repair path that produces a fresh retest.
- Integration tests for the critical loop.

### Only after the above

Begin content work on the highest-leverage gaps in this order:

1. Complete Programming Foundations (Pillar 1) using World 1 as the model.
2. Expand real DSA coverage (Pillar 2) — patterns, visualizers, unseen assessments — without reintroducing filler.
3. Aptitude + Logical + Verbal to service-company depth (Pillars 5 & 6).
4. SQL / DBMS / OS / CN (Pillars 3 & 4).
5. Company pathways with explicit provenance (Pillar 9).
6. Everything else in the A–Z roadmap.

---

## 7. What we will *not* do

- Claim A–Z coverage because a large number of lesson titles or questions exist.
- Generate bulk content while 92% of the catalog is filler and 98% of questions are unverified.
- Create a second parallel curriculum or mastery system.
- Treat XP, lesson clicks, or a single lucky answer as mastery.
- Present unverified company tagging as official hiring patterns.

---

## 8. Success criteria for closing Phase 0

- [ ] Live lesson catalog contains only real content (filler purged or quarantined).
- [ ] Prerequisite graph has zero (or near-zero) broken links for the remaining lessons.
- [ ] Question bank serves only TRUSTED / verified items for placement-facing surfaces.
- [ ] Single source of truth for lessons/worlds is documented and enforced.
- [ ] Full student simulation loop can be executed without broken state.
- [ ] Coverage matrix above is updated with concrete file paths for every remaining real lesson and every verified question set.

Once the above are true, content authoring against the A–Z roadmap becomes safe and measurable.

---

*This audit is the binding starting point for the A–Z execution plan. All subsequent work should reference it.*
