# PR #3 Architecture Presentation Script

## Title

**Bountycode: An Evidence-Led Placement Preparation Platform for Service-Based Companies**

**Length:** 8–10 minutes

---

## 1. Opening — the problem we are solving

**Speaker notes:**

Most placement-preparation products give every learner the same long list of topics and the same generic mock test. That creates three problems: students do not know where to start, they prepare for the wrong assessment pattern, and progress is measured by activity rather than demonstrated skill.

PR #3 changes that model. Bountycode now connects onboarding, diagnostics, personalized learning, company-specific online assessments, and readiness evidence into one explainable loop. The first target is service-based company preparation in India—especially TCS, Wipro, Accenture, Infosys, and Cognizant—while keeping the architecture extensible for additional employers and roles.

The key product principle is simple: gamification motivates practice, but evidence decides what comes next.

---

## 2. Architecture at a glance

**Speaker notes:**

The platform has five connected layers.

First is the **learner profile layer**, which records the student’s target company, role, assessment track, experience level, language, available study time, device, accessibility needs, and target dates.

Second is the **assessment layer**, which contains a server-graded diagnostic engine and versioned company OA simulations.

Third is the **evidence layer**, which stores accuracy, response time, confidence, weak areas, section scores, integrity signals, and completion metadata.

Fourth is the **personalization layer**, which converts evidence into curriculum levels, daily priorities, repair missions, and reassessment recommendations.

Fifth is the **experience layer**, which presents the journey as a campaign map with levels, unlocks, current missions, mock practice, and transparent explanations.

The important architectural decision is that these layers communicate through structured evidence rather than opaque recommendations.

---

## 3. Onboarding — start with the learner’s real goal

**Speaker notes:**

The onboarding flow is a three-step guided setup.

Step one asks the learner to choose a target role, target companies, assessment track, and—when known—the assessment or placement date. Supported preparation tracks include service-company core, TCS Foundation, TCS Advanced, Infosys InfyTQ, HackWithInfy, Wipro, Accenture, and Cognizant.

Step two captures the learner’s current level, preferred language, daily study time, weekly study days, device, and whether a local coding runtime is available.

Step three captures learning preference and accessibility needs.

This is not treated as a permanent label. The profile is a starting hypothesis. The diagnostic can override the learner’s self-assessment, and later performance evidence can move the learner to a different level.

The onboarding contract is persisted through the Academy profile API and is consumed by both plan generation and mock OA selection.

---

## 4. Personalized diagnostic — measure more than correctness

**Speaker notes:**

The diagnostic selects deterministic, server-gradable questions across programming fundamentals, DSA, quantitative aptitude, logical reasoning, verbal ability, computer science, and SQL where verified content is available.

Each answer now records four types of evidence:

1. Whether the answer is correct.
2. The learner’s response time.
3. The learner’s confidence on a one-to-five scale.
4. The skill domain and difficulty associated with the item.

This enables useful distinctions. A learner who is incorrect and unsure needs foundational teaching. A learner who is incorrect but highly confident needs misconception repair. A learner who is accurate but slow needs timed transfer practice.

At completion, the diagnostic returns per-domain scores, average time, confidence estimate, calibration gap, weakest skill, and a recommended next action. These results are written into the learning event stream and invalidate the personalized plan so the next roadmap reflects the new evidence.

The engine is deliberately explainable: every weak-area recommendation can be traced back to answer accuracy, volume of evidence, timing, and confidence.

---

## 5. Company-wise OA engine — one engine, versioned blueprints

**Speaker notes:**

The OA engine uses one shared session lifecycle but different company and track blueprints.

A session is created with a company, role, optional track, question count, duration, mode, integrity setting, and verified-content setting. The backend resolves the company blueprint, distributes questions by section, builds section timers, strips answer keys from the client response, and stores the complete answer-bearing session server-side for scoring.

The current PR adds visible presets for three requested service-company targets.

For **TCS**, the UI exposes a full Foundation plus Advanced practice, a 75-minute Foundation track, and a 115-minute Advanced track. The backend’s track-scoping helper ensures that Foundation sessions use aptitude, logical, and verbal sections while Advanced sessions use the advanced technical and coding sections supported by the trusted bank.

For **Wipro**, the preset represents WILP/NTH-style verbal, analytical, quantitative, technical, and writing-oriented preparation, with a visible warning that the current cohort invitation is authoritative.

For **Accenture**, the preset emphasizes cognitive, technical, coding, and communication practice, again with an invitation-dependent notice rather than a false universal pattern claim.

Every preset carries provenance text and, where available, a source link. This makes the difference between an official fact, a pattern-relevant simulation, and a product recommendation visible to the learner.

---

## 6. OA runtime — reliable under real learner behavior

**Speaker notes:**

The assessment runtime is designed for the conditions students actually face.

Answers are submitted to the server as the learner progresses. The browser also persists the active session envelope and local session state when storage is available. That state includes the active session, questions, section position, answers, timing state, and review flags.

Learners can flag questions for review. The question palette shows current, answered, correct, incorrect, and flagged states. An autosave indicator communicates that the attempt is being preserved.

Every attempt is versioned with an engine version and blueprint version. When the learner completes the OA, the server stores review metadata, resume metadata, scorecard evidence, section scores, weak sections, time intelligence, and readiness guidance.

This means the platform can improve an individual’s preparation without losing the context of how the evidence was produced.

---

## 7. Personalization without requiring expensive AI infrastructure

**Speaker notes:**

The personalization engine is deterministic and low-cost by design.

It combines evidence from diagnostics, lessons, quiz activities, coding submissions, question answers, and completed OAs. Each skill receives an explainable score based on accuracy, evidence coverage, recent performance, and existing mastery state.

Weak-area detection prioritizes skills that are untouched, foundational, low-accuracy, or repeatedly attempted without improvement. The daily plan then chooses repair lessons, practice tasks, spaced review, or timed challenges.

The company track changes emphasis, but does not erase the shared foundation. For example, a learner preparing for TCS Advanced may need both programming fundamentals and coding endurance; a Wipro learner may need a stronger blend of aptitude, verbal, analytical, and communication preparation.

A hosted compiler or generative AI is not required for the core path. The platform can use authored questions, fixed answer keys, output tracing, pseudocode, debugging, SQL validation, test-case reasoning, and optional local execution.

---

## 8. Gamified progression — levels as a transparent campaign

**Speaker notes:**

The learner sees the plan as a campaign map rather than a flat checklist.

The six-stage path is Orientation, Foundations, Core Skills, Applied Readiness, Timed Performance, and Interview Ready.

The interface shows the current mission, campaign progress, evidence status, readiness mode, and what unlocks the next level. Completed levels show evidence earned. Future levels are locked. The current level exposes the next actionable mission.

The progression design intentionally separates engagement from competence. XP, streaks, and visual rewards can make practice motivating, but a learner advances because of repeated success across varied items, delayed review, and timed evidence—not because they clicked through lessons.

At the Timed Performance stage, the main CTA changes from continuing a lesson to running an employer-style mock. This connects the level system to actual placement behavior.

---

## 9. End-to-end learner journey

**Speaker notes:**

The complete learner journey is now:

1. Select a target company and role.
2. Choose an assessment track and practical study constraints.
3. Take a server-graded diagnostic.
4. Receive a level path and first weak-area mission.
5. Practice through lessons, retrieval, and targeted tasks.
6. Reassess with confidence and timing evidence.
7. Enter the matching company OA simulation when the readiness signal supports it.
8. Review section scores, weak areas, timing, flags, and next missions.
9. Repeat the loop until the evidence supports timed performance and interview readiness.

This loop is personalized, inspectable, and resilient. It does not promise a job; it helps the learner understand the specific work required to become more ready.

---

## 10. Engineering quality and next steps

**Speaker notes:**

PR #3 includes backend regression coverage for diagnostic evidence and TCS track distribution, frontend coverage for company preset metadata and confidence submission, server-side answer persistence, versioned attempt records, and a documented architecture blueprint.

The next engineering priorities are to complete browser-level visual regression coverage, add more employer blueprint editions without hardcoding assumptions, connect richer OA scorecards to the campaign unlock rules, and expose the evidence timeline to learners and mentors.

The core architecture is ready for those additions because company patterns, learner evidence, and learning progression are represented as structured contracts rather than one-off UI behavior.

**Closing line:**

Bountycode is not trying to make placement preparation louder. It is trying to make the next best action clearer—and prove why that action was selected.
