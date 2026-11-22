# Content and platform gap review

**Branch reviewed:** `integration/bountycode-consolidation-2026-11-18`

**Review basis:** repository inspection on 19 November 2026, catalog measurement, and the focused content-quality test suite.

## Verdict

The current foundation is good enough to continue building on, but it is not yet the finished “best in the world” placement platform. The strongest parts are the trust-preserving content loader, the canonical step-based lesson player, the service-company content audit, deterministic placement-loop checks, and the decision not to serve unverified candidate content.

The main risk is not that the platform lacks more lesson files. The risk is that content volume, employer claims, assessment composition, learner evidence, and readiness can drift apart. More scraped or generated questions would make that worse unless they pass the same governance path as existing content.

The focused gate currently passes **49 tests** across lesson quality, trust loading, curriculum quality, service-company audit, and placement-loop integration. The catalog contains **69 lesson JSON files**. The measured catalog has **68 lessons with both steps and assessments**, **49 with the richer learning metadata bundle**, and **0 with lesson-level source metadata**. These numbers are inventory measurements, not readiness claims.

## What is already correct

The public lesson route sanitizes answer keys before delivery, while completion is server-graded. The content loader no longer upgrades a bare `verified` or `human_reviewed` label into trusted content without supporting evidence. Contradictory or weak legacy items can remain in source files without entering trusted mocks. Company blueprints are documented as versioned, scope-limited preparation overlays rather than claims about private employer question banks. The current tests protect these boundaries.

The 17-object pattern pack remains correctly treated as an editorial review queue. It should not be registered as a new playable world or a third lesson registry. Candidate objects should be promoted one by one only after answer, explanation, edge-case, provenance, and human-review checks.

## Highest-impact gaps

### 1. Content quality is uneven across the legacy catalog

Many older lessons predate the richer lesson contract. A lesson may have steps and an assessment but lack source/provenance, worked examples, misconception feedback, transfer tasks, or spaced-repetition cards. Do not “fix” this by filling fields with generic boilerplate. Use a promotion checklist and improve the highest-traffic or highest-risk lessons first.

**Acceptance evidence:** each promoted lesson has an immutable version, canonical skill ID, learning objectives, worked examples, misconception-specific feedback, a transfer task, deterministic answer keys, prerequisite links, source/provenance classification, and an independent review record.

### 2. The next content should fill capability gaps, not duplicate existing slugs

The most valuable expansion areas are practical HTTP/API reasoning, Git and pull-request workflow, testing and boundary analysis, debugging with real traces, service-desk data interpretation, professional status communication, and role-aware technical fundamentals. These should be authored as small, interactive, low-bandwidth lessons that reuse the existing lesson player and canonical content loader.

Avoid publishing exact employer timings or question counts unless a current primary source supports the specific programme, role, and hiring event. Label broad preparation as `pattern_relevant`, and keep unverified employer overlays out of official-looking mock claims.

### 3. One canonical question-serving boundary must be enforced

The architecture notes correctly identify a potential ownership problem: the quiz service and question store must not independently load and index production question banks. The next architecture tranche should make `question_store.py` the sole production content-serving owner, with quiz composition consuming an interface rather than maintaining another file list or trust policy.

**Acceptance evidence:** an architecture test detects duplicate production question loaders; the composer receives questions through the canonical store; trust filtering, schema validation, and provenance remain in one place; a missing company pool returns an explicit insufficient-content result instead of silently selecting unrelated items.

### 4. Learner evidence needs one complete lifecycle

The desired lifecycle is Company → Blueprint → Skill → Pattern → Lesson → Practice → Assessment → Evidence → Diagnosis → Repair → Retest → Readiness. The platform should prove this with a single integration test that starts from onboarding, creates a deterministic daily plan, completes a lesson stage, submits a quiz answer, records evidence, creates a repair mission, completes a retest, and recomputes readiness.

**Acceptance evidence:** every step has a persisted learner-owned record or event, duplicate submissions are idempotent, historical attempts retain content and blueprint versions, and the dashboard reads projections rather than recomputing authoritative mastery in the browser.

### 5. Readiness must remain evidence-based

Lesson completion alone should not unlock readiness. Readiness should distinguish first-attempt accuracy, transfer performance, retention, difficulty, hint dependence, time efficiency, trusted-content sufficiency, and company-blueprint coverage. AI may explain a mistake or coach an interview response, but it must not decide objective correctness, mastery, rewards, or readiness.

**Acceptance evidence:** readiness tests fail when evidence is insufficient, untrusted, stale, or based only on repeated attempts; the result explains blockers and next actions; the scoring formula is versioned and reproducible.

## Recommended implementation order

1. **Canonical ownership hardening:** audit and remove duplicate question loading from production paths; add import/ownership tests.
2. **Promotion pipeline:** add a machine-readable content manifest with item version, provenance, publication state, reviewer evidence, canonical skill, and quality-gate status.
3. **High-value content tranche:** add HTTP/API, Git, testing/debugging, data interpretation, and professional communication lessons through the existing lesson schema; keep them draft until reviewed.
4. **End-to-end evidence test:** prove onboarding-to-readiness with idempotency and historical-version assertions.
5. **Catalog migration:** upgrade legacy lessons in measured batches, starting with the most-used company-track prerequisites; do not bulk-generate generic metadata.
6. **Blueprint freshness:** verify current employer sources on a schedule and create a new blueprint version when scope or assessment evidence changes.
7. **Accessible delivery:** ensure every new lesson works in text-first, keyboard, screen-reader, printable, and low-bandwidth modes. Visuals may enhance learning but must not be the only carrier of essential information.

## Definition of “best” for this product

Bountycode becomes unusually strong when it is not merely larger than other preparation sites, but more trustworthy and more adaptive: every company claim has scope and freshness; every served item has a review state; every learner recommendation has an explainable reason; every result is reproducible; every mistake creates a targeted repair and retest; every readiness claim is backed by sufficient trusted evidence; and every core flow still works when AI, network quality, or a third-party compiler is unavailable.

The current branch is a solid foundation for that direction. It should not yet be described as complete.
