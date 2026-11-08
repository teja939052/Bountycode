# Bountycode Learning Intelligence Architecture

**Status:** Proposed architecture / implementation contract  
**Scope:** BALMA (Bountycode Adaptive Learning & Mastery Algorithm), powered by BLPA (Bountycode Learning Path Algorithm)  
**Branch:** `fix/adaptive-quiz-skill-graph-snapshot-20261107`

## 1. Product principle

Bountycode is not a collection of lessons, quizzes, dashboards and gamification features. It is a learning intelligence system that uses a learner's evidence to decide what to teach or assess next, then measures whether that intervention worked.

The central decision question is:

> Given the evidence available about this learner, their goal and their time budget, what is the most valuable next learning action, and what evidence will demonstrate that it worked?

The system must remain useful without an external LLM or paid AI API. Core estimation, planning, scheduling, mastery and readiness calculations are deterministic, testable and explainable. Optional AI services may assist with content authoring or explanations, but must not be a dependency of the decision engine.

## 2. Naming and relationship

- **BALMA — Bountycode Adaptive Learning & Mastery Algorithm:** the overall learning-intelligence architecture and feedback loop.
- **BLPA — Bountycode Learning Path Algorithm:** the planning and scheduling policy inside BALMA.
- **Learner State Engine:** estimates knowledge and uncertainty for each learner-skill pair.
- **Knowledge Graph Engine:** represents concepts, prerequisite dependencies and goal relevance.
- **Readiness Engine:** estimates performance against a defined assessment blueprint, with uncertainty and calibration status.

BALMA is the umbrella system. BLPA is not a competing second engine; it is the part that selects and orders learning actions.

## 3. PageRank analogy — and its limits

The useful analogy is structural:

| Search ranking | Bountycode |
|---|---|
| Pages and links | Skills, patterns and prerequisite edges |
| Ranking computation | Learner-state estimation and constrained action scheduling |
| Ranking output | A learner-specific plan and assessment forecast |
| Feedback | Observed learning and assessment outcomes |

The analogy is not a claim that the algorithms are mathematically identical. PageRank uses graph-based importance propagation; Bountycode combines knowledge tracing, dependency reasoning, scheduling and predictive calibration. The algorithms themselves are reproducible. Defensibility must come from the quality of the curated graph, validated content, consent-based longitudinal evidence, calibration and demonstrated outcomes—not secrecy or a claim that competitors cannot copy the mathematics.

## 4. Core data model

Every assessment event used for mastery must have a server-verifiable provenance and a stable identity.

### 4.1 Learner-skill state

Maintain state per `user_id + canonical_skill_id`, including:

- estimated probability of mastery;
- uncertainty / evidence strength;
- BKT parameter-set version;
- distinct question count and recent outcomes;
- last demonstrated date;
- estimated retention / next review date;
- evidence provenance and assessment type;
- observed difficulty, hints and timing where reliably available.

Do not equate lesson opens, lesson completion, XP, streaks, clicks or client-supplied correctness claims with demonstrated mastery.

### 4.2 Question and skill metadata

Every question should map to one or more canonical skills with explicit mapping confidence, difficulty, format, answer provenance, grading mode, and (where possible) misconception tags. Ambiguous mapping must not silently become evidence for a specific skill.

### 4.3 Goal blueprint

A target such as a role, company assessment or general placement goal has a versioned blueprint:

- skill/pattern weights and their source;
- required domains and assessment formats;
- difficulty distribution;
- time constraints;
- last verified date and confidence level.

Company weights are estimates based on documented evidence, not guaranteed or definitive employer exam patterns. If no reliable blueprint exists, show a generic pathway and label the limitation.

## 5. Component A — Bayesian Knowledge Tracing

### 5.1 Purpose

Estimate (P(L)): the probability that the learner has acquired a skill, given a sequence of observations. This is more informative than raw correct-answer percentage because the model explicitly accounts for guessing, slips and learning transitions.

For a binary question, standard BKT uses:

- (P(L_0)): prior probability the learner already knows the skill;
- (P(T)): probability of learning the skill between opportunities;
- (P(G)): probability of a correct guess when the skill is not known;
- (P(S)): probability of an incorrect response despite knowing the skill.

These parameters are initial model assumptions, not universal constants. Version them, test sensitivity and calibrate them against suitable learner evidence. Different item formats may require different guessing assumptions; do not apply the four-option MCQ guess rate to coding or free-response tasks.

### 5.2 Observation update

Let (p) be the prior mastery probability.

For a correct response:

[
p_{obs} = \frac{p(1-S)}{p(1-S)+(1-p)G}
]

For an incorrect response:

[
p_{obs} = \frac{pS}{pS+(1-p)(1-G)}
]

Then apply the learning transition:

[
p_{next} = p_{obs} + (1-p_{obs})T
]

The implementation must handle zero denominators safely, clamp probabilities to ([0,1]), validate parameters, and have deterministic unit tests for boundary cases.

### 5.3 Evidence safeguards

- Use server-graded outcomes and distinct question identities.
- Repeated retries of the same item must not masquerade as independent evidence.
- Preserve the latest outcome per question for evidence summaries; keep the full event history for audit and model fitting.
- Treat hints, repeated exposure, leaked answer keys and non-independent attempts as evidence-quality modifiers.
- Do not infer a stable misconception from one wrong answer.
- Maintain uncertainty separately from mastery. A high estimate based on two observations is not equivalent to a high estimate supported by broad independent evidence.
- BKT is a model of skill acquisition, not a complete model of every aspect of competence. Supplement it with transfer tasks, coding performance, retention checks and timed assessments.

## 6. Component B — Prerequisite and pattern graph

Represent canonical skills and problem-solving patterns as a directed acyclic graph where an edge (a 	o b) means skill (a) is a prerequisite for skill (b).

The graph must support:

- prerequisite ordering and cycle validation;
- multiple prerequisites;
- goal-specific relevance weights;
- identification of bottleneck prerequisites;
- alternative paths where a concept can be learned through different routes;
- versioning and reviewed ownership of graph edges.

Examples of pathways:

- Arrays → Two Pointers → Sliding Window
- Arrays → Hashing → Frequency Counting
- Functions → Recursion → Backtracking
- Recursion + Arrays → Dynamic Programming
- Graphs → BFS / DFS

A prerequisite is not considered met merely because it was visited. It requires sufficient, independent evidence under a versioned mastery policy. If evidence is absent, schedule diagnosis; if evidence indicates a gap, schedule teaching and reassessment.

## 7. Component C — Marginal-value scheduling (BLPA)

### 7.1 Objective

Select the next learning actions that maximize expected progress toward the learner's chosen goal, subject to their time budget, prerequisites, review obligations and content availability.

For skill (s), define an estimated benefit:

[
\Delta_s = (\mathbb{E}[M_s\mid a, t] - M_s) \times W_s
]

where:

- (M_s) is current estimated mastery;
- (a) is a candidate learning action (lesson, practice, review, diagnostic or project);
- (t) is the estimated time cost;
- (W_s) is the versioned goal-blueprint importance weight.

A simple baseline ranks candidates by expected weighted gain per minute:

[
V(a) = \frac{\Delta_s}{t}
]

The production scheduler should also account for prerequisite readiness, uncertainty reduction, retention urgency, learner preferences/accessibility, action diversity, fatigue and content quality. The formula is a decision aid; it is not a claim that learning gain is known exactly.

### 7.2 Candidate actions

The planner may choose:

- diagnostic assessment when state uncertainty is high;
- prerequisite lesson when a blocker is unassessed;
- reteaching and targeted practice when a blocker is weak;
- new learning when prerequisites are sufficiently demonstrated;
- spaced review when retention risk is high;
- transfer challenge when basic accuracy is high but application evidence is weak;
- timed mock or interview simulation when the target blueprint calls for it.

### 7.3 Time-budget planning

Start with a transparent deterministic greedy scheduler for a bounded daily plan. Reserve time for due reviews, then choose eligible actions by expected value per minute. Do not overrun the user's budget or emit actions whose required content does not exist.

As the system matures, compare greedy selection with a constrained knapsack / planning approach and evaluate both against measured outcomes. Add diversity constraints so the plan does not repeatedly select only one high-weight skill.

Every recommendation must carry an explanation record: selected skill, evidence snapshot, prerequisite status, goal weight, estimated duration, reason for selection, alternatives considered and planner version.

## 8. Component D — Retention and spaced repetition

Track demonstrated knowledge over time and schedule retrieval practice before likely forgetting. A simple exponential retention curve can be an initial baseline:

[
R(t)=e^{-t/\tau}
]

where (t) is elapsed time and (	au) is a skill- or learner-specific stability estimate.

This is only an initial approximation. Calibrate stability from actual delayed-recall outcomes. A review should update the learner state using the new observation; merely opening a review card is not evidence of retention.

## 9. Component E — Readiness prediction

Readiness must be tied to a specific target, blueprint, assessment format and forecast date. The primary output is an expected score distribution, not an unexplained percentage badge.

A first transparent baseline can aggregate predicted skill performance using blueprint weights:

[
\widehat{Score}=\sum_s W_s\,\widehat{P}(s\text{ demonstrated at assessment time})
]

However, the implementation must not assume skills are independent or that BKT mastery probability equals exam accuracy. The production model should incorporate question difficulty, blueprint coverage, assessment format, timing and observed mock-test performance.

Report:
- expected score or score range;
- prediction interval and its method;
- probability of meeting a stated threshold only when calibrated data supports it;
- blueprint coverage and evidence sample size;
- top actions expected to improve the forecast;
- model version, data freshness and calibration status.

If the data is insufficient, say **insufficient evidence for a calibrated prediction**. Do not fabricate a 95% confidence interval or pass probability. A simple retention factor may be used as a baseline projection, but it must not be represented as a validated exam forecast.

## 10. Component F — Misconception diagnosis and remediation

Use structured error patterns and question metadata to generate hypotheses about why an answer failed. Examples include off-by-one errors, incorrect loop bounds, condition confusion, wrong invariant, incorrect SQL join logic or misunderstanding of recursion state.

A diagnosis is a hypothesis until confirmed. The system should select a discriminating follow-up question or short diagnostic, then choose a targeted explanation and reassessment based on the result. Remediation assessments must use fresh or appropriately varied items rather than simply repeating the failed question.

## 11. Feedback and calibration loop

For each planned intervention, record:

1. learner-state snapshot and model version;
2. action selected and its reason;
3. expected benefit and time;
4. learner completion and engagement (kept separate from mastery);
5. immediate assessment result;
6. delayed retention / transfer result where available;
7. actual mock or placement outcome where voluntarily supplied and verifiable.

Compare predictions with outcomes using suitable metrics: calibration curves, Brier score for probability forecasts, MAE/RMSE for score forecasts, interval coverage, and subgroup checks. Use temporal and learner-level holdouts to avoid leakage. Do not claim that a particular sample size guarantees accuracy; sample needs depend on outcome variance, blueprint quality and subgroup coverage.

Use privacy-by-design: collect only necessary data, obtain clear consent for outcome use, support deletion/retention policies, avoid exposing one learner's data to another, and report aggregate statistics only when cohort sizes protect privacy.

## 12. System boundaries and architecture

Separate the system into four contracts:

1. **Content infrastructure:** curriculum, lessons, question bank, projects, answer keys, rubrics and company blueprints.
2. **Learner model:** canonical skills, evidence events, mastery estimates, uncertainty and retention state.
3. **Decision engine:** prerequisite resolution, candidate generation, marginal-value scoring, time-budget scheduling and readiness forecasting.
4. **Evidence infrastructure:** immutable/append-only assessment events, provenance, model versions, prediction logs and outcome feedback.

Frontend pages should consume these services rather than independently implementing learning logic. XP, streaks, achievements and other engagement features remain downstream experiences and must never certify mastery.

The core engine should be deterministic and operable without third-party AI APIs. External AI may be an optional adapter for authored explanations or content assistance; it must not own the learner state or silently decide mastery.

## 13. Evaluation and release gates

Before exposing a model output as a trusted learner-facing prediction, require:

- unit tests for BKT updates, parameter validation and edge cases;
- graph reference and cycle validation;
- deterministic scheduler tests for prerequisites, time budgets, missing content and due reviews;
- tests proving client telemetry and engagement signals cannot alter mastery;
- question-to-skill mapping coverage and audit;
- offline replay against historical event sequences;
- synthetic simulations for sanity checks, explicitly separated from real-world validation;
- calibration evaluation on held-out learner and time periods;
- clear fallback behavior when evidence or blueprint coverage is insufficient;
- explanation records that allow every recommendation to be reproduced.

Do not claim readiness prediction superiority, a fixed accuracy target, or a defensible data moat before representative empirical validation.

## 14. Phased implementation

| Phase | Deliverable | Acceptance evidence |
|---|---|---|
| 0 | Data contracts, canonical skill IDs, event provenance and graph audit | Schemas, migration plan, coverage report |
| 1 | BKT learner-state service | Pure Python implementation, versioned parameters, unit tests and offline replay |
| 2 | Graph-aware BLPA scheduler | Reproducible daily plans with explanations and strict time budgets |
| 3 | Retention and review scheduling | Delayed-recall tests and review-state persistence |
| 4 | Misconception diagnosis and repair | Confirmatory diagnostics and fresh-item reassessment |
| 5 | Readiness baseline | Blueprint coverage, score estimates and honest uncertainty |
| 6 | Calibration pipeline | Held-out evaluation, calibration metrics and subgroup checks |
| 7 | Learner-facing integration | Daily path, mastery evidence and readiness views powered by shared services |

Build in this order. Do not expand the feature surface while the core state, evidence and decision contracts remain unreliable.

## 15. Immediate implementation sequence

1. Inspect and validate the existing prerequisite graph and canonical skill mapping.
2. Audit the current LearningEvent schema and question-grading flow; ensure the event stream has stable question IDs, server provenance and correct timestamps.
3. Implement BKT as a pure, isolated service with versioned parameters and tests; do not wire it into production mastery until event semantics are verified.
4. Build an offline replay/simulation harness and compare BKT estimates with simple accuracy baselines.
5. Implement BLPA scheduling against the existing graph and actual content availability.
6. Add prediction logging before showing readiness forecasts.
7. Integrate into the UI only after backend decisions are reproducible and tests pass.

## 16. Existing repository work to reuse

The current PR branch already contains an initial canonical prerequisite graph, evidence aggregation, prerequisite planning and authenticated diagnostic/reassessment route work. Reuse and audit those components rather than creating parallel systems. In particular, verify the newly added assessment routes against the actual quiz-service/session APIs and event persistence contracts before extending them. The graph and planner are a foundation, not proof that BKT, marginal-value scheduling or calibrated readiness prediction are already implemented.

---

**North star:** Bountycode should not merely tell a learner what content exists. It should infer what they know, identify what is blocking them, choose the next most valuable action, and verify whether that action improved durable, transferable ability.
