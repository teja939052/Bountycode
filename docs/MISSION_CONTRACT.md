# Mission Contract — the learning unit of PlacementPro

One mission is one fight, not one chapter. Every concept a student meets —
aptitude, reasoning, verbal, coding, CS core, company prep — is learned
through the same grammar. This document is the contract; the validators
enforce it.

## 1. The grammar (ADR: BOUNTYCODE_CURRICULUM_STRUCTURE)

Backend source of truth: `backend/app/content/lesson_definitions.py::STEP_TYPES`.
Frontend mirrors: `frontend/src/data/missions/patterns.ts::CanonicalStageType`,
`frontend/src/engine/missionTypes.ts::MissionStepType`.

**Nine canonical teaching stages, in order, all required:**

| # | Stage | Student does | Evidence |
|---|-------|--------------|----------|
| 1 | `discover` | Sees the idea (visual, ≤150 words) | — |
| 2 | `manipulate` | Changes something, watches it move | interaction event |
| 3 | `predict` | Commits to an answer before seeing it | correct / wrong |
| 4 | `build` | Produces (code, calculation, sentence) | tests / rubric pass |
| 5 | `break` | Diagnoses a plausible wrong solution | names the misconception |
| 6 | `debug` | Repairs it (fix + why) | fix verified |
| 7 | `retrieve` | Recalls with no notes, no scrolling back | correct from memory |
| 8 | `transfer` | Applies in an unfamiliar context | correct out-of-domain |
| 9 | `mastery` | Timed proof, no scaffolding | score ≥ threshold under time |

**Composition chrome (framing, never a substitute for a stage):**
`intro` (mission brief) · `practice` · `recognize` (= predict with options shown) ·
`prove` (= mastery) · `reward` (capability-attached payout, never click-XP).

**Interaction subtypes** (`stage.interaction.kind`, never a top-level stage):
`visual_hook, micro_animation, state_trace, drag_or_manipulate, tap_to_reveal,
predict_output, multiple_choice_reasoning, change_one_thing, fill_in_blank,
code_reorder, tiny_build, interactive_diagram, match_relationships, sort_steps,
parameter_slider, before_after, break_and_debug, error_hunt, explain_the_bug,
recall_check, srs_card, transfer_problem, timed_prove`.

Two are load-bearing evidence, not decoration: every mission MUST contain a
`change_one_thing` moment (reuse the idea with one value changed) and a real
`timed_prove` (clock on, hints off, input locks at zero).

## 2. The mission model

Code: `backend/app/content/mission_definitions.py`. A mission binds:

- **brief** — threat + goal + reward, ≤3 lines. Names the round it prepares.
- **stages[9]** — each canonical stage with its interaction and its check.
- **bank_refs** — question IDs from the file banks, NEVER inline content.
  Every ref must resolve in `question_store` with servable `trust_status`
  (`verified` / `reviewed` / `automated_checked` per the serving gate).
  Unresolvable or unservable refs fail validation.
- **company_overlay_id** — e.g. `tcs_nqt`, `infosys_sp`. Overlays carry
  pattern weights, never claims.
- **mentor_skill** — canonical skill id driving Captain Byte moments.
- **reward** — Diamonds + unlock, attached to the mastery verdict.
- **consequence** — the forward commitment: harder transfer tomorrow on
  mastery, repair mission before advancing otherwise. Stored as data the
  journey engine reads; never prose that evaporates.

Verdict per mission: `mastered | developing | repair_needed` — persisted to
the mastery graph, read by the journey planner. Completion is not mastery;
transfer evidence is required.

## 3. Captain Byte in missions

Single resolver: `backend/app/services/mentor_service.py::resolve_captain_byte`.
Moments: `intro, correct_1, correct_2, wrong_1, wrong_2, after_break,
after_mastery, retry_prompt`. Moods from the real `MentorMood` union only.
Fallback order: skill → SRS tag → slug → authored world fallback → silence.
Generic copy is a bug. No LLM, no new collections, no per-page resolvers.

Placement: brief, lesson intro, correct, wrong, debug, repair, result, mock OA
(before/after only). Never in tables, profile, billing, settings.
Length: tight mentor prose, 2–4 lines.

## 4. Trust pipeline (binding)

```
UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED
```

- Mission *structure* (stages, refs, overlays) is code-reviewed like code.
- Mission *question content* lives only in file banks under
  `backend/app/data/`; missions reference IDs. No question text in missions.
- LLM-drafted candidates enter the isolated unverified pool only, pass
  `intake_lint`, and are NEVER served until the pipeline promotes them.
- No LLM in authoring, tagging, grading keys, company attribution.
- Coding: solution executes, visible + hidden tests pass, edge cases covered.
- Aptitude/logic/verbal: independently computed answers + reasoning check +
  ambiguity review.
- Company claims: verified `provenance` + explicit `companies` tags, or the
  mission labels the pattern `pattern-relevant`. "Asked at X" without
  provenance is fabrication — validator rejects it.

## 5. Company overlays (service-based)

Code: `backend/app/content/service_tracks.py` (data over the existing
`CompanyOverlay` / `CompanyJourney` models — no new system).
Tracks: `tcs_nqt, infosys_sp, wipro_nlth, cognizant_genc, accenture, capgemini`.
Each overlay: funnel stages, pattern weights (honest levels), question
filters onto the verified company banks, mock blueprint, interview focus,
version + provenance + confidence. Overlays configure; they contain zero
question content.

## 6. Journey wiring

`mission_index`: `mission_id → { lesson_slug, bank_refs, company_overlay_id,
mentor_skill, frontend_slug }`. The journey planner's `next_action` carries
`mission_id`; the mentor resolver frames *why this mission now*. Frontend
`MissionPlayer` slugs map 1:1 (`frontend_slug`). Reward/consequence lines
are rendered from mission data, not invented by the client.

## 7. Authoring checklist (for agents and humans)

1. Target the canonical 9 — no invented stage names, no skipped stages.
2. Every bank_ref resolves AND is servable today (`validate_mission` checks).
3. `change_one_thing` and a clocked `timed_prove` are present and real.
4. Every wrong path names its misconception; every fix states its why.
5. Company language is `pattern-relevant` unless provenance is attached.
6. Mentor moments resolve to authored speech (run the mentor contract test).
7. New questions enter UNVERIFIED with lint + automated evidence; never served.
8. Run: `validate_mission()` (schema) · `validate.py --strict` (frontend
   grammar) · `pytest tests/test_mentor_contract.py` · bank trust tests.

## 8. File map

```
docs/MISSION_CONTRACT.md                        this contract
backend/app/content/mission_definitions.py      Mission models + validate_mission()
backend/app/content/service_tracks.py           6 service-company overlays + journeys
backend/app/content/curriculum/mission_templates/  6 domain skeletons
backend/app/content/curriculum/missions/        exemplar missions (trust-marked)
backend/app/data/mission_candidates_*.json      generated candidates (UNVERIFIED only)
backend/app/content/curriculum/captain_byte/    authored mentor speech (narration)
backend/scripts/generate_mission_candidates.py  deterministic generators + verifier
```

Bulk volume comes from deterministic generators with machine-checked answers
through the trust pipeline — never from LLM-drafted banks served directly.
