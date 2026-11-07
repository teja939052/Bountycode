# BountyCode — A–Z Implementation Backlog (Initial)

**Generated:** 2026-11-07  
**Source of truth for current product:** `docs/BOUNTYCODE_VISION_LOCK.md` + `AGENTS.md`  
**Long-term target:** `docs/CURRICULUM_A_TO_Z_ROADMAP.md`

This is the **starting** backlog after a first-pass inspection of the repository.  
It is deliberately high-level. Phase 0 (full file-level audit) must still be executed before large content authoring begins.

---

## Current architecture anchors (do not duplicate)

| System | Location / notes |
|--------|------------------|
| World registry | `backend/app/content/world_registry.py` — 12 worlds currently registered |
| Lesson definitions | `backend/app/content/lesson_definitions.py` + per-world files |
| Lesson registry (older) | `backend/app/content/curriculum/registry.py` |
| Curriculum data | `backend/app/content/curriculum/*.json` + role curricula |
| Question bank | `backend/app/content/questions/` (curated / raw / rejected) — file-based, never Mongo |
| Company journeys | `backend/app/content/company_journeys.py` |
| Learning objects / runtime | `backend/app/content/learning_object.py`, `lesson_runtime.py` |
| Vision lock | `docs/BOUNTYCODE_VISION_LOCK.md` (service-company focus, 6-world launch target) |
| Learning standard | `docs/learning/LEARNING_EXPERIENCE_STANDARD.md` |
| Lesson inventory | `docs/learning/LESSON_INVENTORY.csv` + summary |

**Rule (from AGENTS.md):** Prefer reusing existing systems. Search routes, services, frontend pages, and collections before creating new abstractions.

---

## Phase 0 — Repository & curriculum audit (do this first)

- [ ] Inventory every existing lesson and question file  
- [ ] Map every item to a canonical skill ID (create the taxonomy if missing)  
- [ ] Identify incomplete, duplicated, and placeholder content  
- [ ] Test all existing learner flows end-to-end (signup → diagnostic → lesson → fail → repair → mastery → mock → readiness)  
- [ ] Produce an honest curriculum coverage report (pillar × status)  
- [ ] Cross-check against `docs/learning/LESSON_INVENTORY.csv`

**Output of Phase 0:** a machine-readable coverage matrix + ordered backlog of only the gaps that matter for the next phase.

---

## Phase 1 — Learning engine completion (P0)

| Item | Status guess | Notes |
|------|--------------|-------|
| Diagnostic assessment delivery | partial | Exists in adaptive / readiness paths; needs full end-to-end verification |
| Prerequisite checks → lesson navigation | partial | Prerequisite DAG mentioned; confirm it blocks navigation |
| Assessment grading + retesting | partial | |
| Automatic prerequisite unlocks | partial | |
| Mastery engine (independent evidence) | needs verification | Must not treat XP / completion % as mastery |
| Spaced repetition (SRS) | partial | |
| Readiness engine | partial | Company-weighted readiness already present for service companies |
| Route + integration tests for the full loop | missing / weak | |

---

## Phase 2 — Programming foundations + DSA (P0)

| Area | Status guess | Notes |
|------|--------------|-------|
| Python / C / C++ / Java tracks | partial | Lesson profiles exist; depth and language-specific differences need audit |
| Programming foundations modules 1–4 | partial / missing | World 1 foundations + vertical slices exist; full beginner path incomplete |
| Full DSA pattern coverage | partial | Worlds + question bank cover many patterns; mastery gates and visualizers incomplete |
| Visualizers & execution traces | partial | SPEC_DSA_VISUALIZER.md exists |
| Unseen problem assessments | needs verification | |

---

## Phase 3 — Placement core subjects (P0)

SQL / DBMS / OS / CN / Architecture — groundwork exists in curriculum files and aptitude/tech sections. Full structured lessons + timed topic tests + mixed exams are still required.

---

## Phase 4 — Aptitude & verbal (P0)

Quantitative + logical + verbal banks exist at small scale. Expand to full coverage, add timed company-style assessments, and enforce the lesson standard.

---

## Phase 5 — Company preparation (P1)

Service-company blueprints and journeys already exist for the locked vision.  
Expand to the full list (including product companies) only after the core loops are solid.  
Every pathway must carry source, last-verified date, and confidence level.

---

## Phase 6 — Engineering, system design, projects (P1)

Web curriculum, Git/Linux/Docker/cloud, LLD/HLD, and guided projects are largely missing or thin. Build after the placement core is reliable.

---

## Phase 7 — Career preparation (P1)

Resume/ATS, LinkedIn, behavioral, communication, AI mock interview evaluation — several AI features already exist; tighten into a coherent career track with the same mastery rules.

---

## Phase 8 — Quality, analytics, expanded-product readiness

- Audit every lesson and question against the lesson blueprint and trust pipeline  
- Validate answer keys and grading  
- End-to-end personalization tests  
- Security & assessment integrity  
- Learner outcome & retention metrics  
- Performance and accessibility

---

## Immediate next actions (this week)

1. Complete Phase 0 audit (file-level mapping + coverage matrix).  
2. Fix any broken critical loops discovered in the student simulation test defined in AGENTS.md.  
3. Publish the coverage matrix so content authoring can begin only on verified gaps.  
4. Keep all new work behind the existing trust pipeline and single world/lesson registry.

---

## How to use this backlog

- Do **not** start bulk lesson generation until Phase 0 is finished.  
- Every new lesson or question must pass the Content Trust Pipeline (UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED).  
- Prefer extending existing worlds, registries, and engines over creating parallel systems.  
- When a conflict with the locked vision appears, surface it explicitly before changing product direction.
