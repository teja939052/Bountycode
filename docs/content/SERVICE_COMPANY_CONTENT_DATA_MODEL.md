# Bountycode content and assessment data model

## What is and is not public

The internal schemas used by TCS, Infosys, Wipro, Cognizant, HCLTech, Accenture, Capgemini and other employers for their private question banks and applicant tracking systems are not generally public. Bountycode must not claim it has reconstructed an employer's private data model.

There are public interoperability standards. 1EdTech QTI models assessment items, tests/sections and results so those artifacts can move between item banks, authoring systems, delivery systems and scoring/analytics tools. ADL xAPI defines a consistent learning-experience statement with an actor, verb, object, result and context. These are useful reference standards, not proof that a particular employer uses them internally.

## Mainline curriculum integration

The current canonical product documents are:
- `docs/SERVICE_COMPANY_CURRICULUM.md`: ordered service-company curriculum spine and release priorities.
- `docs/learning/LEARNING_EXPERIENCE_STANDARD.md`: lesson anatomy, interactive exercise patterns, feedback, mastery and quality gates.
- `backend/app/content/world_registry.py` plus `world*.py`: the single student-facing lesson/world registry.
- `backend/app/content/company_journeys.py` and the company blueprint infrastructure: employer overlays.

The 17 learning objects in `backend/app/data/candidates/service_company_patterns_v1.json` are authoring/review artifacts, not LessonDefinitions and not a new student-facing registry. If a candidate is approved, the content team should either adapt it into the existing world/town lesson definition with the required interactive learning sequence, or create a verified question-bank item where a standalone assessment question is appropriate. Do not add the candidate directory to runtime loaders or the World Registry.

## Existing Bountycode sources of truth

Reuse what already exists:

| Need | Existing owner |
|---|---|
| Canonical learning-object shape | backend/app/content/learning_object.py |
| Step-based student lesson delivery and answer sanitization | backend/app/routes/company_lessons.py |
| General lesson runtime and evidence | existing lesson service/runtime |
| Company blueprint and company pattern source metadata | backend/app/data/company_blueprints.json and company track infrastructure |
| Versioned coding/MCQ question data | backend/app/data and backend/app/content |
| In-memory question bank and trust-serving filter | backend/app/services/question_store.py |
| Student attempts, session state and learning evidence | existing Mongo learner-state collections and learning-event service |

Do not create a third playable registry or store question text, answer keys, solutions or test cases in MongoDB. MongoDB is for learner-owned state, attempts, sessions, results and telemetry.

## Logical object model

A single content item is versioned independently from the company blueprint that may select it.

### Content artifact

- item_id: immutable stable ID
- version: integer or content hash
- item_type: mcq, short_response, code, sql, ordering, prediction, debugging, lesson_step
- domain / skill_id / pattern_id: canonical taxonomy identifiers
- difficulty: calibrated label with an explicit rubric
- prompt / stimulus: learner-visible statement, table, passage, code or scenario
- options: structured choices when applicable
- answer_key: server-only, never returned before submission
- explanation: worked reasoning, not just a one-line answer
- distractor_analysis: why each wrong choice is tempting and what misconception it signals
- hints: ordered conceptual → structural → near-solution scaffold
- transfer_task: a new context testing whether the student can apply the pattern
- prerequisites and learning_objectives
- assessment rubric and grading contract
- test_cases: visible and hidden for code; independent input/expected output pairs
- provenance: official / candidate_reported / pattern_relevant / canonical / synthetic
- trust_state: unverified → automated_checked → human_reviewed → trusted
- review/verification evidence: reviewer, timestamp, decision, independent validation method and report reference
- publication_state: draft, in_review, approved, retired

### Company / programme blueprint

- company_id and programme_id: do not conflate one employer with every drive or role
- blueprint_id and version
- role / hiring event / eligible cohort scope
- effective_from and last_verified_at
- source_urls and source checked date
- confidence and provenance classification
- sections: stable section IDs, timing rules, weight, allowed item types and ordering rules
- selection rules: eligible skill/pattern IDs and trust-state minimum
- scoring policy: objective scoring rules, negative marking if known, normalization and omitted-question behavior
- item IDs: references to immutable content versions, not copies of question text
- evidence sufficiency rules and readiness blockers

A pattern label by itself must never imply that an item appeared in a company's actual assessment. Synthetic items can be attached to a company as pattern-relevant practice only when a public source supports the broad skill area.

### Assessment attempt

The attempt references a frozen blueprint version and the exact item versions used:
- attempt_id, user_id, company/programme, role
- blueprint_id/version, start/end timestamps, status
- ordered sections and item IDs/versions
- user responses
- server grading outputs and scoring-policy version
- section and overall result
- time spent, hints, navigation and integrity context
- provenance and trust state for every item at attempt time

Do not update historical attempts when a blueprint or content item is revised.

### Learning evidence event

Keep the existing event service and add only fields it needs. A useful xAPI-aligned mapping is:
- actor: pseudonymous learner identifier
- verb: viewed, attempted, answered, passed, failed, repaired, retained, transferred
- object: content item/lesson ID and version
- result: correctness, score, response duration, hints and rubric dimensions
- context: company/programme blueprint version, role, skill/pattern, section, language and session

This is an interoperability mapping, not a request to build a separate xAPI store or another evidence engine.

## Storage policy

1. Authoring artifacts are version-controlled JSON in the canonical content locations.
2. Runtime loads approved content into the existing in-memory question/lesson stores.
3. Answer keys and hidden tests remain server-side; the learner API gets a sanitized projection.
4. MongoDB stores only learner state and outcomes, never item bodies or grading secrets.
5. Content promotion is a governed operation with evidence; a structural validator or generated answer is not a human review.
6. Company blueprints and content are versioned independently.
7. Item selection for mocks is deterministic/reproducible from blueprint version, candidate pool version and selection seed where required.

## QTI / xAPI interoperability

QTI 3.0 should be considered for importing/exporting supported MCQ, stimulus, section/test and result structures. Bountycode's custom code-lab and mastery evidence may need extensions or a separate companion representation.

xAPI concepts can help standardize learner event vocabularies across lesson, practice, mock, repair and retest. The existing LearningEvent model should remain canonical internally until an interoperability requirement justifies an adapter.

## Release gates

- Do not expose candidate/unverified content to student-facing lesson or mock endpoints.
- Do not display a "company asked this" label without exact public provenance.
- Do not promote a code item because its solution compiles; independently checked test oracles and edge cases are required.
- Do not promote aptitude/reasoning/verbal items without independent answer and reasoning checks plus ambiguity review.
- Do not call a lesson mastery from completion alone; transfer/prove evidence is required.
- Do not calculate readiness from untrusted items or insufficient evidence.
