# Curriculum gap audit and first content expansion

**Date:** 2026-11-07  
**Branch:** `curriculum/fill-core-learning-gaps`

## Audit basis

The repository contains several curriculum systems. The interactive placement lesson API is backed by `backend/app/services/lessons/__init__.py` and `lesson_service.py`; lesson modules must be registered there to appear in `GET /api/v1/lessons`. Other content banks and routes exist, but their existence alone does not make them part of this learner-facing lesson catalog.

The existing `CONTENT_RECONCILIATION.md` is dated 2026-09-08. It reported 0 system-design and 0 debugging questions in the question-store student-serving pool, 29 behavioral questions, and uneven explanation coverage in verified question content. These are historical audit findings, not a claim that the current runtime has been re-counted.

## Confirmed repository gaps addressed in this change

| Area | Existing foundation | Gap addressed |
|---|---|---|
| Debugging | AI debugger endpoints and a debugging question bank | No dedicated debugging track in the interactive lesson catalog |
| System design | System-design question bank and interview routes | No dedicated system-design track in the interactive lesson catalog |
| Behavioral interviews | Existing company preparation and behavioral question data | No dedicated, sequenced behavioral communication lesson track |

## New learner-facing lessons

### Debugging
- A Reliable Debugging Workflow
- Trace Logic and Test Edge Cases

Covers reproducible failures, error classification, variable tracing, boundary tests, and regression verification.

### System design
- System Design: Requirements and Constraints
- System Design: Traffic, Caching, and Trade-offs

Covers functional/non-functional requirements, measurable constraints, rough capacity estimates, cache-aside, and freshness trade-offs.

### Behavioral interviews
- Answer Behavioral Questions with STAR
- Teamwork and Handling Disagreement

Covers truthful STAR answers, personal contribution, respectful disagreement, and reflective learning.

## Integration

- Registered all three tracks in the lesson catalog.
- Added skill-graph mappings for debugging, system design, and behavioral communication.
- Added a regression test that checks track registration and valid skill mappings.
- Lessons use the existing server-side quiz grading and answer-key sanitization path.

## Still outstanding

This is the first focused expansion, not a claim that the full A–Z blueprint is complete. Remaining work includes a full topic-by-topic inventory against the ten curriculum pillars, deeper programming-language and DSA lesson coverage, SQL labs and CS fundamentals, aptitude/reasoning/verbal depth, project-based milestones, company syllabus verification, and quality review of the existing large question bank.

## Validation status

Source files and imports were inspected after the changes. Automated backend tests and a full application run have **not** been executed in this GitHub-only editing pass. Run the backend lesson test suite and API smoke tests before merging.
