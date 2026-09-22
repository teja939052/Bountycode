# BountyCode — Product Requirements Document (PRD)
## A to Z. Governed by `/docs/BOUNTYCODE_VISION_LOCK.md` — if anything here conflicts
## with that document, the Vision Lock wins and the conflict must be surfaced, not resolved silently.

---

## 0. How to use this PRD

This document is the operational source of truth for implementation. Agents may propose implementation changes, but they must not silently change product strategy, launch date, product name, or scope. The canonical launch date is 18 October 2026.

Agent rules:

Read this PRD before product or architecture changes.

Preserve working infrastructure unless a verified defect requires a change.

No destructive migration, bulk delete, mass rewrite, or registry consolidation without a written migration map and tests.

No third playable registry.

Build evidence from runtime behavior, not compile/build success alone.

If implementation reality conflicts with this PRD, report the conflict before changing strategy.

---

## 1. Product summary

Interactive placement-prep platform for Indian engineering students targeting
service-based and mass-recruiting companies (TCS, Infosys, Wipro, Cognizant, Capgemini,
Accenture). Visually-taught patterns, personalized by role/company/language, wrapped in a
habit-forming game layer. Launch: October 18, 2026.

**Core loop (the actual product):**
```
Company → Blueprint → Skill → Pattern → Interactive Lesson → Practice →
Assessment → Evidence → Diagnosis → Repair → Retest → Readiness
```

---

## 2. Users

- **Primary:** B.Tech students, 1st-4th year, all branches, tier-2/3 colleges weighted
  higher than tier-1, preparing for service-based-company campus placement.
- **Secondary:** Same students post-placement or later-stage, extending toward
  product-company prep via the same engine with a different role/company adapter.
- **Not the target:** FAANG-only aspirants as a primary segment (real, served, but not
  who the product is built for first).

---

## 3. Information architecture (6 hubs, nothing else top-level)

| Hub | Owns |
|---|---|
| Journey | Voyage map, worlds, lessons, repair branches, SRS |
| Practice | Question bank, patterns/topics, compiler/playground |
| Mock OA | Timed company-templated assessments |
| AI Interview | Behavioral/HR/Technical/System Design/GD sessions |
| Company Tracks | Per-company blueprints, verified prep paths |
| Profile | Rank, badge, readiness score, streak, settings, career tools |

Resume/ATS/Applications live under Profile, not top-level. Admin/auth/legal are unrouted
utility pages.

---

## 4. Feature specification, by hub

### 4.1 Journey

**What it is:** The guided path through content, presented as the voyage map (ship, fog
of war, boss islands — already built and audited). The map is presentation only; the real
work is the lesson engine underneath it.

**Interactive Lesson Engine — the single most important build item in this PRD.**
Every lesson composes from this stage set (use an appropriate subset per content type —
don't force DSA mechanics onto an aptitude question):

```
Explain → See → Interact → Predict → Solve → Break → Debug → Recall → Transfer → Prove
```

| Stage | What it does | Reuses |
|---|---|---|
| Explain | Concept introduction, plain text/narration | New content authoring |
| See | Visual/animated demonstration of the concept | **New — the actual content-depth investment** |
| Interact | Student manipulates a variable/parameter and observes the effect | New interactive component |
| Predict | Student answers "what happens if..." before being shown | Graded deterministically against stored answer |
| Solve | Real problem, real input | Compiler/judge (reuse — don't build a second grading path) |
| Break | Broken code/statement presented for the student to identify what's wrong | Judge, with `step_type=break` flag |
| Debug | Student fixes the broken version | Judge, `step_type=debug` |
| Recall | Spaced-repetition retrieval question | **Wire to existing SRS (`spaced_repetition.py`) — do not build a second SRS** |
| Transfer | Apply the concept in a new, slightly different context | Solve-pattern reuse |
| Prove | Final check that mastery is real, not just completion | Feeds evidence/readiness |

**Completion path:** every stage's success → `POST /lesson/{slug}/complete` →
`study/activity` → `gamification/record` — one path, already built and idempotency-hardened.
Do not create a second completion path for new interactive stages.

**Content priority order (build these five patterns to the full standard first):**
1. Aptitude — percentages, ratios, profit/loss, time/speed/distance, time & work
2. Reasoning — blood relations, syllogism, coding-decoding
3. Verbal — grammar, reading comprehension, para jumble, email format
4. Pseudocode/programming logic — line-by-line execution tracing animations
   (**the actual differentiator — build this well**)
5. Easy service-level DSA — arrays, strings, hashing, two pointers, sliding window

Five excellent patterns beat 2,000 shallow ones. Do not spread thin across more patterns
before these five are genuinely excellent.

**Role/company personalization must be real, not cosmetic.** Tag every level with
`role_relevance` and `company_relevance` metadata so `GET /api/v1/worlds/{worldId}`
actually reorders/filters content per student profile — not just labels the page
differently while serving identical content. Confirmed not yet real as of last audit;
this is P1 work.

### 4.2 Practice

- Question bank browse/filter/solve — existing (`questions.py`, `questions_solve.py`,
  `problems.py`). No new serving path.
- Run vs. Submit split (already confirmed live) — keep.
- Similar-questions via deterministic tag matching (already confirmed live) — keep.
- Hints ladder — currently basic (static array, not the `hint_level` API ladder). Upgrade
  to use the real progressive-hint system.
- Editorials — currently the raw reference solution. Upgrade to a real written walkthrough
  for high-traffic questions, human-authored or human-reviewed, never raw LLM output
  dropped onto a trust-gated page.
- Compiler/Playground — standalone execution tool, kept separate from graded practice.

### 4.3 Mock OA

Full spec: see `bountycode-agent-spec.md` §3. Summary:
- Server-authoritative section timers (`started_at`/`ends_at`, 410 on late submit) —
  already built.
- **Must be wired to the real frontend flow** — confirmed as of last audit that `MockOA.tsx`
  was still driving a separate aptitude flow instead of `/api/v1/oa/*`. This wiring is a
  launch blocker; verify it's actually connected before anything else here.
- Deterministic grading only — MCQ exact-match, coding via judge, SQL excluded from v1.
- Company blueprints: TCS + Accenture built to full fidelity first, others follow.
- Anti-cheat: tab-switch/fullscreen tracking, informational not punitive.

### 4.4 AI Interview

Full spec: see `bountycode-agent-spec.md` §4. Summary:
- Modes: Behavioral (STAR), HR, Technical, System Design, GD — one session model, mode as
  a field, not a collection per mode.
- Rubric-based scoring with quote-or-zero guardrail (built, tested, structural — not
  prompt-hoped).
- Degraded-mode fallback on evaluator failure must be honestly labeled to the student
  (`degraded: true`), never presented as full-quality feedback.
- GD content: 0 authored as of last audit. Target ~150-200 human-reviewed topics before
  GD mode goes live in any visible nav.

### 4.5 Company Tracks

- Canonical file: `company_tracks.py`. Consolidate `companies.py`,
  `company_directory.py`, `company_conversion.py`(service module only, route removed),
  `company_practice.py` — several already removed as dead code; confirm the rest are
  genuinely merged or justified as separate.
- Blueprint → priority skills/patterns → recommended lessons → company-style practice →
  mock → weakness diagnosis → repair. This routing must be real per-company, not a shared
  template with a different logo.
- `last_verified_at` required and visible on every blueprint.
- No claim of "official format" or a percentile ranking without real, current source
  data and a real comparable student population behind it.

### 4.6 Profile

- Rank ladder (Deckhand → Lookout → Navigator → First Mate → Captain → Fleet Admiral) —
  built, tested, tier boundaries verified. Live in profile, both leaderboard payloads.
- Portable badge SVG endpoint — built, PII-safe, tested against profile-minting risk.
- Readiness score — composite of world completion, OA percentile, interview rubric
  average, repair recovery rate, SRS retention. Confirmed partially wired (OA feeding it
  as of last audit); confirm interview and repair-recovery inputs are live before treating
  this as the full v2 formula.
- Career tools (resume, ATS, applications tracker) — real but secondary, nested here, not
  top-level nav.
- Settings, history, streak display.

---

## 5. Evidence/analytics layer (already built, zero AI in the truth path)

Real, deterministic, aggregation-only features — no LLM calls, all computed from existing
logs:
1. Weakness heatmap by pattern (accuracy per Striver pattern)
2. Failure-reason breakdown (timeout vs. wrong-answer vs. runtime error, per pattern)
3. Forgetting-curve visualization off the real SRS schedule
4. Complexity/efficiency scoring (runtime scaling across input sizes)
5. Time-to-solve trend per pattern
6. Pacing calculator against a real placement-drive deadline
7. Company-readiness gap report (per-section performance vs. blueprint weighting)
8. Hints-hidden re-attempt scheduling
9. Portable, verifiable prep report ("not an employer certification" label required)
10. Personal records (fastest solve, streak, first-attempt success rate)

All confirmed built with 67/67 tests green as of last audit — this section is largely
complete; verify it stays reconciled with the single readiness engine (no parallel
readiness truth path — already checked once, re-check after any future readiness edit).

---

## 6. Gamification (retention layer — not the pitch)

Full quality bar: see `bountycode-gamification-brief.md`. Summary rules:
- Every reward traces to a real, verified skill signal — never usage/time-on-app.
- Sequenced juice, under ~900ms, full `prefers-reduced-motion` fallback, one consistent
  state-color vocabulary (gold=done, green=current, muted=locked, sky-dash=recovered).
- No streak-guilt, no fake scarcity, no paywall on correctness or core feedback.
- **Do not build:** guilds, cards, seasons, new currencies, more worlds, new achievement
  systems. Explicitly out of scope until content depth (§4.1) is real.
- 12 worlds / 50 levels is the canonical count — do not reference 16 worlds or 72 levels
  anywhere; both were confirmed stale/incorrect and fixed.

---

## 7. Content trust pipeline (applies to lessons AND questions)

```
Author/source → intake_lint (reject stubs/formatters/malformed) →
Deterministic verification (internal consistency only) →
Independent ground-truth check (a second, separately-derived source — NOT proof
  of correctness from execution alone, per the 26-stub incident) →
Tranche staging → Human review (~11 min/tranche) → Promotion to verified/reviewed
```

Full sourcing rules: see `bountycode-question-sourcing-spec.md`. Applies identically to
new lesson content (§4.1) — lesson authoring is not a side door around this pipeline.

---

## 8. Non-functional requirements

- **Mobile-first.** Most users are on phones, often inconsistent connections. Every UI
  decision defaults to lean and fast over decorative.
- **Server-authoritative timing** on anything graded/timed (OA sections especially) — a
  client-side timer is a suggestion, never the source of truth.
- **Idempotency mandatory** on every write endpoint — proven with a concurrent test, not
  a sequential one. This bug family has recurred four times in this project; treat every
  new write endpoint as guilty until proven otherwise.
- **Residency rule:** question/lesson content lives in versioned files, loaded at startup.
  Student state lives in Mongo. Don't blur this.
- **No LLM in any grading verdict** — generation and conversational feedback only.

---

## 9. Verification standard (non-negotiable)

Compile/build success is never sufficient on its own. Every critical loop requires runtime
evidence: student action → database state → returned API state → UI result → next state.
Paste real output. "Same code path, should work" is not evidence — this project has
been wrong about that specific claim multiple times already.

---

## 10. Priorities (mirrors Vision Lock — repeated here for the PRD's own completeness)

**P0 (fix before anything else):**
- `repair_service.py:103,114` phantom import
- Registry B → A dead link (stop emitting Registry-B missions until adapter-unified)
- `/lesson/complete` orphan keys
- `POST /study/activity` not writing `completed_competencies`
- Confirm MockOA is actually wired to `/api/v1/oa/*`, not the legacy aptitude flow

**P1 (must be genuinely great by Oct 18):**
- Interactive lesson engine, five flagship patterns, real role/company routing,
  lesson-completion → evidence wiring, 2-3 excellent company blueprints (TCS + Accenture
  first)

**P2 (after P1 is solid):**
- Company-style timed mocks fully wired, mock→repair loop proven end-to-end with a real
  run, mobile polish, analytics/error monitoring

**Explicitly not this cycle:** guilds/cards/seasons, more worlds, new role-track systems,
mass content generation, destructive registry cleanup, any large rewrite.

---

## 11. Definition of done (launch gate)

A real student, on a real phone, can: choose a company → follow the recommended path →
complete a real interactive lesson → practice → take a mock → receive a real weakness
diagnosis → complete repair → retest → see readiness/evidence actually change — without
breaking state, rewards, progress, or navigation. Proven with a real run, not a code-path
description.

---

## 12. Readiness engine

### 12.1 Readiness purpose

Readiness is a decision aid answering:

"Given my target company and the evidence collected so far, what do I need to do next?"

### 12.2 Readiness guardrails

- Minimum evidence threshold before displaying a numeric readiness percentage.
- "Insufficient evidence" is a valid first-class state.
- Unknown is not the same as weak.
- Company-specific readiness uses blueprint weights and trusted evidence.
- Automated/untrusted evidence must not silently become high-stakes evidence.
- Repair/retest evidence must update the score when it meets trust requirements.

### 12.3 Next-action taxonomy

Use deterministic actions such as:

| Action | Meaning |
|---|---|
| PROVE | Not enough evidence yet; perform an assessment. |
| REPAIR | A demonstrated weakness needs targeted work. |
| RETAIN | Skill is adequate but retention is deteriorating. |
| ADVANCE | Skill evidence is sufficient; advance to the next priority. |

### 12.4 Readiness UI

Show:

- target company/assessment
- evidence sufficiency state
- readiness when sufficient
- section/skill breakdown
- blockers
- strongest skills
- weakest skills
- trend
- last mock
- next action
- repair CTA
- retest status

Do not manufacture precision from thin data.

---

## 13. Personalization

### 13.1 Inputs

- target company
- target assessment
- optional role
- optional language preference
- evidence history
- skill graph/mastery
- failure history
- retention history

### 13.2 Required behavior

Personalization must change actual recommended content when blueprint/evidence differences justify it. Changing only the page label is not personalization.

Example:

- TCS target → Quant priority → specific patterns → company-style mock
- Wipro target → different weighted skills/pattern order → different practice emphasis → corresponding mock

### 13.3 Authoring rule

Add supported company/role relevance metadata during authoring rather than retrofitting thousands of records later.

---

## 14. Gamification specification

### 14.1 Purpose

Gamification increases consistency and return behavior while preserving learning integrity.

### 14.2 Systems to preserve

- XP/reward ledger
- streaks
- combo/multipliers where already implemented
- badges/achievements
- ranks/levels
- linear unlock progression where canonical
- leaderboards/leagues where stable
- mission/map progression
- victory/result feedback

### 14.3 Reward integrity

All meaningful rewards must route through server-truth reward functions/ledger.

Required invariants:

- reward is idempotent
- duplicate completion cannot double-award
- client cannot choose reward amount
- displayed reward equals authoritative reward returned by backend
- XP/points cannot be farmed by refreshing or replaying a completion endpoint
- cosmetic rewards cannot substitute for mastery evidence

### 14.4 Reward philosophy

Prefer:

```
Demonstrated mastery → unlock/progression → reward → cosmetic expression
```

not:

```
clicks/grinding → currency → unlock
```

### 14.5 Product naming note

The backend uses diamonds as the canonical reward unit. Do not retain a parallel XP naming path in user-facing code.

### 14.6 Gamification screens

Mission success should show:

- what was demonstrated
- reward earned
- progress change
- next unlock
- next action

Avoid excessive particles, animation or sound that slows the learning loop.

### 14.7 Accessibility

- respect `prefers-reduced-motion`
- never use animation as the only information channel
- sound is optional/mutable
- screen-reader labels for reward states
- no flashing effects

---

## 15. Onboarding

Onboarding must collect only information that meaningfully changes the journey.

Minimum:

- year/experience band
- target company or "not sure yet"
- preferred language if supported
- current preparation level / baseline

After onboarding:

```
Target → Blueprint → First mission
```

The student should reach a useful activity quickly.

---

## 16. Profile and progression

Profile should show:

- target company
- current progression/rank
- streak
- badges
- skill/evidence summary
- recent activity
- saved/bookmarked items if supported
- settings

Avoid turning profile into a second dashboard that duplicates readiness.

---

## 17. Community, social, and secondary features

Existing features may remain in the repository but should not compete with the launch loop.

Examples of non-core/secondary systems:

- guilds/study groups
- campus wars
- showcase/peer review
- social feed/community
- cards/collections
- seasons/festivals
- marketplace/crafting/economy

These are post-launch backlog unless an existing feature is already stable and adds clear retention value without scope expansion.

### 17.1 Existing feature inventory and disposition

| Area | Existing capabilities in repository | Launch disposition |
|---|---|---|
| Learning | Journey/world map, learning hub/paths/modules, lessons, concepts, DSA visualizer, language loop, daily challenge, drill/problem-of-day | Core only where connected to target-company preparation; competing navigation should be minimized |
| Practice | Question bank, pattern problems, aptitude, SQL, debugging, compiler/playground, challenge packs, assignments, scrims | Curate and route through blueprint/pattern relevance; keep verified serving paths |
| Assessments | Mock OA, company/role mocks, contests, interview, behavioral/HR, system design, interview replay/feedback | Launch core for supported company simulations; advanced interview/system-design breadth can remain secondary |
| Evidence & career | Skill graph, readiness, evidence dashboard, company gap, failure history, repair/retest, placement calendar/drives/packs | Core; this is the measurable outcome layer |
| AI | AI mentor, debugger, interviewer, adaptive explanations, resume/ATS tools | Assistive; never replace deterministic grading/readiness/trust gates |
| Gamification | XP ledger, streaks, ranks/levels, badges, map progression, unlocks, leaderboards/leagues, boss/missions, cosmetics and existing economy systems | Preserve stable systems; no new mechanics before launch |
| Social / community | Guilds, study groups, showcase/peer review, Campus Wars and community features | Frozen/secondary unless stability fix or proven retention need |
| Admin / operations | Content admin, assignments, corpus tooling, analytics/retention pages, content governance | Operate and review; expand only where necessary for launch quality |
| Platform | Auth, billing, PWA/offline, analytics instrumentation, API/backend, storage/deployment | Required production infrastructure |

---

## 18. AI features

AI is an assistive layer, not the source of truth for readiness.

**Good AI uses:**

- explain a concept in simpler language
- give a contextual hint
- explain code/debugging reasoning
- personalize tone/language
- summarize performance

**Bad uses:**

- inventing company questions
- inventing official company formats
- making high-stakes readiness claims from thin evidence
- silently replacing deterministic grading
- auto-promoting unverified content into high-stakes banks

Deterministic systems must own:

- scoring
- unlocks
- rewards
- evidence state transitions
- readiness calculation
- verification gates

---

## 19. Admin and content operations

Admin capabilities required for sustainable content:

- content review status
- provenance/status editing
- lesson/pattern metadata
- question review
- quarantine visibility
- blueprint versioning
- runtime verification results
- content defect queue
- analytics dashboard

Admin/corpus systems that are not part of the launch loop stay frozen rather than expanded.

---

## 20. Architecture requirements

### 20.1 Canonical playable identity

`app.data.worlds_data.WORLD_REGISTRY` is the canonical playable identity during migration.

### 20.2 Adapter

A single adapter can translate legacy lesson IDs to canonical playable IDs.

Required operations:

- `resolve_level_id(raw_id)`
- validate mapped A IDs exist
- reverse mapping where needed
- reject/flag unresolved IDs

The adapter is a migration bridge, not a new registry.

### 20.3 Layer boundaries

```
Company / Blueprint
        ↓
Skill / Pattern metadata
        ↓
Lesson runtime
        ↓
Practice / Assessment
        ↓
Evidence
        ↓
Diagnosis / Repair
        ↓
Readiness
```

Game layer wraps the above.

### 20.4 Preserved infrastructure

Do not rewrite without verified need:

- readiness engine
- evidence collection
- repair/retest
- SRS
- gamification ledger
- compiler/judge
- SQL execution
- question governance
- company blueprint infrastructure
- mock infrastructure

---

## 21. Initial codebase cleanup priorities

### P0 — deploy blockers

| Item | Requirement |
|---|---|
| repair_service phantom imports | Fix live repair crash path; runtime prove. |
| Registry-B → Registry-A dead link | Stop emitting unresolved B missions or route through adapter. |
| `/lesson/complete` orphan keys | Resolve to canonical playable IDs. |
| `/study/activity` progress write | Update canonical progress expected by Journey/map. |

### P1 — correctness

| Item | Requirement |
|---|---|
| Assessment grading divergence | One canonical judge for attempt + completion. |
| next_level_id off-by-one | Resolve from canonical ordered registry. |
| Reward display mismatch | Display authoritative server reward. |
| Repair completion accounting | Count repair completion in evidence/metrics. |
| Dead unlock fields | Read intentionally or remove later after migration proof. |

### P2 — post-stabilization debt

- consolidate legacy registry consumers through measured migration
- retire unused shadow world definitions
- retire dead curriculum generator side effects
- converge role/company metadata sources

**Migration rule:** No deletion of Registry B, shadow world definitions, or legacy generators until usage is measured at zero and a rollback/migration plan exists.

---

## 22. Data model requirements

Core entities:

- User
- Company
- Blueprint
- SkillDomain
- Pattern
- Lesson
- LessonStep
- PracticeItem
- Assessment
- AssessmentAttempt
- EvidenceEvent
- FailureDiagnosis
- RepairMission
- Retest
- ReadinessSnapshot
- GamificationLedgerEntry
- Badge/Achievement
- SRSCard
- ProgressState

Every entity must have stable IDs and explicit ownership of truth. Identity resolution is a first-class concern during migration.

---

## 23. API principles

APIs should be:

- idempotent for completion/reward operations
- explicit about trust/provenance
- consistent in naming IDs
- deterministic where high-stakes
- backward compatible during migration
- tested at integration level, not only unit level

Critical response examples should expose the authoritative server result used by the UI.

---

## 24. Analytics

Track the product loop, not vanity feature counts.

**Launch metrics:**

- onboarding completion
- first mission start
- first mission completion
- lesson completion rate
- pattern mastery rate
- mock participation
- mock → repair conversion
- repair → retest completion
- readiness evidence sufficiency
- readiness improvement after repair/retest
- Day-7 retention
- Day-30 retention

**Critical funnel:**

```
Signup → Target chosen → First mission → Lesson complete → Practice → Mock →
Diagnosis → Repair → Retest → Readiness update → Return
```

Metric discipline: Do not invent industry baselines or guarantee placement outcomes. Establish baselines from actual BountyCode users.

---

## 25. Non-functional requirements

### Performance

- fast first meaningful render on mobile
- avoid huge DOM animation trees
- lazy-load heavy visualizations
- compiler calls must have timeouts
- long-running assessment timers must be server-truth

### Reliability

- no reward duplication
- no progress loss on refresh
- safe retry semantics
- graceful infrastructure failures

### Security

- authorization on all user-owned resources
- secrets server-side only
- isolated code execution
- input/output limits
- rate limiting on sensitive endpoints
- audit logging for administrative changes

### Accessibility

- keyboard navigable core flow
- reduced motion
- sufficient contrast
- descriptive labels
- non-color-only state communication

---

## 26. Mobile UX specification

### Required devices/layouts for QA

| Viewport | Use |
|---|---|
| 320px | sanity check / no catastrophic overflow |
| 390px | primary launch QA |
| 430px | primary launch QA |
| Desktop | regression |

### Critical screens

- onboarding
- company blueprint
- Journey
- interactive lesson
- code editor
- mock
- result/diagnosis
- repair
- readiness dashboard

### Mobile rules

- no essential content hidden behind horizontal scroll
- code editors have responsive height
- primary action remains reachable
- timers are visible without blocking content
- result state is obvious
- animation never blocks navigation

---

## 27. Verification and QA

### 27.1 Evidence hierarchy

Build/compile success is not proof of product correctness.

Required for critical flows:

```
student action → database state → API response → UI result → next state
```

### 27.2 Runtime QA matrix

| Flow | Required evidence |
|---|---|
| Onboarding | target persisted + first mission generated |
| Lesson | steps transition + completion persisted |
| Practice | correctness + evidence event |
| Mock | score + section outcomes persisted |
| Diagnosis | weakness persisted |
| Repair | repair completion persisted |
| Retest | new evidence + readiness change when threshold met |
| Reward | ledger delta exactly once |
| Unlock | next canonical level accessible |
| Mobile | 390px/430px interaction and visual pass |

### 27.3 Destructive change gate

Before deleting, bulk rewriting, deduplicating, regenerating or migrating:

1. produce an impact report
2. list exact records/files affected
3. show backup/rollback plan
4. provide migration mapping
5. add tests
6. obtain explicit approval

---

## 28. Agentic development protocol

Every agent task must state:

- branch name
- objective
- allowed files/directories
- forbidden scope
- expected tests
- acceptance criteria
- evidence required

### Agent commit protocol

Agents should:

- work on isolated branches/worktrees
- keep commits small and atomic
- inspect git diff before committing
- report files changed
- report tests run
- never silently resolve large architectural conflicts

### Recommended branch model

```
main
 └── release/2026-10-18
      ├── feature/...
      ├── fix/...
      └── experiment/...
```

Use Git worktrees when multiple agents operate concurrently.

---

## 29. Launch scope — 18 October 2026

### Must be excellent

- target company selection
- company blueprint view
- focused Journey
- interactive pattern lessons
- curated practice
- company-style mock for a small well-supported set
- diagnosis → repair → retest
- evidence/readiness
- mobile critical path
- reward/progression integrity
- analytics and production monitoring

### Can remain basic

- broad library browsing
- social/community
- advanced profile customization
- large role track catalog
- advanced AI mentor features

### Explicitly deferred

- new gamification mechanics
- more fantasy worlds
- mass AI content generation
- destructive registry cleanup
- feature-parity marketing
- FAANG-first positioning
- unverified company claims

---

## 30. Launch release checklist

### Product

- [ ] target company can be selected
- [ ] blueprint is visible and understandable
- [ ] recommended path is not generic
- [ ] at least one flagship lesson is genuinely excellent
- [ ] practice is reachable from the lesson
- [ ] mock is reachable from the prep path
- [ ] diagnosis is visible after failure
- [ ] repair is actionable
- [ ] retest uses new context where possible
- [ ] readiness/evidence changes when expected

### Engineering

- [ ] P0 defects closed
- [ ] critical APIs idempotent
- [ ] no duplicate reward path
- [ ] no unresolved canonical IDs
- [ ] compiler execution sandbox verified
- [ ] production error monitoring active
- [ ] backup/rollback plan tested

### Content

- [ ] launch patterns have provenance
- [ ] company claims are honest
- [ ] no unverified high-stakes content leaks into mocks
- [ ] lesson runtime verified
- [ ] explanations reviewed

### UX

- [ ] 390px pass
- [ ] 430px pass
- [ ] desktop regression pass
- [ ] reduced-motion pass
- [ ] loading/error states present

---

## 31. Definition of Done — flagship lesson

A flagship lesson is done only when all of these are true:

- [ ] content exists and is reviewed
- [ ] pattern metadata exists
- [ ] company relevance metadata exists where justified
- [ ] interactive components render
- [ ] wrong answers give useful feedback
- [ ] retries behave correctly
- [ ] code/test execution is correct where used
- [ ] break/debug behavior is real where used
- [ ] retrieval/SRS enrollment works
- [ ] transfer tests a different context
- [ ] completion is persisted
- [ ] reward is authoritative and idempotent
- [ ] evidence is recorded
- [ ] mobile passes
- [ ] runtime QA captures the result

---

## 32. Definition of Done — company readiness

Company readiness is launch-ready only when:

- [ ] blueprint is versioned
- [ ] evidence thresholds are explicit
- [ ] insufficient-evidence state exists
- [ ] target-specific recommendations actually differ when expected
- [ ] mock results feed diagnosis
- [ ] diagnosis feeds repair
- [ ] repair feeds retest
- [ ] retest feeds evidence/readiness
- [ ] UI explains what to do next
- [ ] company claims have provenance

---

## 33. Post-launch roadmap

After October 18, prioritize the hard, compounding work:

1. **Content depth.** Build visually taught, genuinely interactive lessons for the highest-demand service-company patterns. Start with a small number and make them exceptional.

2. **Personalization depth.** Increase real company/role/language differentiation through better metadata and blueprint routing.

3. **Assessment fidelity.** Deepen company simulations using verified and current information.

4. **Scale content.** Expand the pattern library only after the content template and quality bar are proven.

5. **Retention systems.** Revisit community/guild/cards/seasons and other existing systems based on observed retention needs rather than adding them speculatively.

---

## 34. Strategic decision filter

Before building anything, ask:

> Does this make a service-company engineering student better prepared, more consistent, or more certain about what to do next?

- If **no**: backlog.
- If **yes**: define the user outcome, evidence, acceptance criteria, and minimal implementation before coding.

---

## 35. Final product statement

BountyCode is not a question bank with a game attached.

It is a placement preparation engine where the game helps students persist through a structured, company-aware learning and evidence loop.

The product must make this sentence true in the hands of a real student:

> "I know what this company needs, I know what I am weak at, I know what to practice next, and I can see evidence that I am getting closer to being ready."

---

*Canonical execution document — strategy is locked; implementation may evolve without changing the north star.*
