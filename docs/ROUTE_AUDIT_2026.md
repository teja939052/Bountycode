# Route Audit — Backend Route Consolidation

## Current State
- **96 route files** in `backend/app/routes/`
- Auto-discovered by `main.py` via `pkgutil.iter_modules`
- Many features are split across multiple files with overlapping prefixes or duplicated functionality
- FastAPI does **not** allow two routes on the same `method + path`; duplicate prefixes in different files are fine, but duplicated functionality causes maintenance burden, inconsistent auth/limits, and frontend confusion

## Critical Duplicate Prefix Conflicts
These share the exact same `prefix` and can collide on overlapping paths:

| Prefix | Files | Risk |
|---|---|---|
| `/api/v1/interview` | `interview.py`, `interview_replay.py`, `mock_interview.py` | HIGH — 3 files, overlapping interview semantics |
| `/api/v1/onboarding` | `onboarding.py`, `onboarding_doors.py`, `onboarding_launch.py` | HIGH — 3 files, same prefix |
| `/api/v1/analytics` | `analytics.py`, `analytics_admin.py` | MEDIUM — admin vs user analytics |
| `/api/v1/profile` | `career_profile.py`, `profile_stats.py` | MEDIUM — same prefix, split concerns |
| `/api/v1/oa` | `oa.py`, `oa_engine.py` | MEDIUM — same prefix |
| `/api/v1/questions` | `questions.py`, `questions_solve.py` | MEDIUM — same prefix, split solve/browse |
| `/api/v1/lesson` | `lesson.py`, `lesson_planner.py` | MEDIUM — same prefix |

## Feature-Level Duplicates (different prefixes, same domain)

### Resume — 5 files
| File | Prefix | Routes |
|---|---|---|
| `resume.py` | `/api/v1/resume` | upload, generate, optimize, export/docx, export/pdf, history, semantic-score, analyze-rulebased |
| `enhanced.py` | `/api/v1/enhanced` | resume/tailor, resume/improve-bullet, resume/improve-bullets, resume/ats-checklist, resume/missing-bullet, resume/semantic-score |
| `career_profile.py` | `/api/v1/profile` | from-resume, upload-resume |
| `cover_letter.py` | `/api/v1/tools` | linkedin-about (reads resumes_collection) |
| `student_features.py` | `/api/v1/student` | humanize/resume |

### Interview — 4+ files
| File | Prefix | Routes |
|---|---|---|
| `interview.py` | `/api/v1/interview` | start, answer, result, history, company questions, readiness |
| `mock_interview.py` | `/api/v1/interview` | start, answer, result, available-roles, sample questions |
| `interview_replay.py` | `/api/v1/interview` | {id}/replay, {id}/replay/stats |
| `interview_booking.py` | `/api/v1/interview-booking` | booking-specific |
| `interview_chat.py` | `/api/v1/interview-chat` | chat-specific |

### Company — 7+ files
| File | Prefix | Routes |
|---|---|---|
| `companies.py` | `/api/v1/companies` | list, role companies, journey, evaluate, roadmap |
| `company_prep.py` | `/api/v1/company-prep` | blueprints, questions, readiness, start-assessment |
| `company_mocks.py` | `/api/v1/company-mocks` | companies, config, start, answer, complete, status, results |
| `company_lessons.py` | `/api/v1/company-lessons` | list, get, complete |
| `company_tracks.py` | `/api/v1/company-tracks` | companies, enroll, complete module, my-tracks |
| `placement_packs.py` | `/api/v1/placement-packs` | sde, companies, learning-objects, mock-tests, roles |
| `tracks.py` | `/api/v1/tracks` | {company}/overview |

### Learning — 8+ files
| File | Prefix | Routes |
|---|---|---|
| `learning.py` | `/api/v1/learning` | modules, progress, concept engine |
| `learning_modules.py` | `/api/v1/learning-modules` | module-specific |
| `learning_paths.py` | `/api/v1/learning-paths` | path-specific |
| `unified_learning.py` | `/api/v1/unified-learning` | lessons, activity, progress, catalog |
| `lesson.py` | `/api/v1/lesson` | {slug}, {slug}/step, run, build, transfer, predict, explain, break, assess, complete |
| `lesson_planner.py` | `/api/v1/lesson` | plan/{concept_id}, next-action |
| `company_lessons.py` | `/api/v1/company-lessons` | list, get, complete |
| `free_trial.py` | `/api/v1/free-trial` | lessons, complete, conversion-prompt |

### Problems/Questions — 5 files
| File | Prefix | Routes |
|---|---|---|
| `questions.py` | `/api/v1/questions` | browse, company, filters, patterns, topics, stats, submit, upvote, pattern-readiness, pattern-checklist |
| `questions_solve.py` | `/api/v1/questions` | answer, explanation, solved, submit, recent, random, {id}, solution, quality-stats |
| `problems.py` | `/api/v1/problems` | create, list, {id}, visible, lock-state, reset-locks, check-lock, run, static-analysis, srs/due, srs/mastery |
| `features.py` | `/api/v1/features` | random, bookmarks, notes, company problems, enhanced problem, similar, acceptance |
| `submissions.py` | `/api/v1/submissions` | {id}/submit, history, problem/{id}, status/{id}, solved, stats |

### Placement — 4 files
| File | Prefix | Routes |
|---|---|---|
| `placement.py` | `/api/v1/placement` | alumni |
| `placement_calendar.py` | `/api/v1/placement-calendar` | companies, calendar, countdown, company timeline, boss-battles |
| `placement_packs.py` | `/api/v1/placement-packs` | sde, companies, learning-objects, mock-tests, roles |
| `placement_questions.py` | `/api/v1/placement-questions` | random, by-company, stats |

### Study — 2 files
| File | Prefix | Routes |
|---|---|---|
| `study.py` | `/api/v1/study` | today, activity |
| `adaptive_learning.py` | `/api/v1/adaptive` | skills, weak-areas, daily-plan, recommendations, learning-path, readiness, activity, domains |

### Gamification/Progress — 2 files
| File | Prefix | Routes |
|---|---|---|
| `gamification.py` | `/api/v1/gamification` | profile, readiness, tower, streak, badges, leaderboard, skills, combo, daily-login |
| `progress.py` | `/api/v1/progress` | heatmap, streak, topic-progress, weekly-goal, daily-goal, overview |

## Proposed Canonical Route Map

### Resume
```
/api/v1/resume/* → resume.py (canonical)
```
- Move `enhanced.py` resume endpoints into `resume.py` as `/api/v1/resume/tailor`, `/api/v1/resume/improve-bullet`, etc.
- Move `career_profile.py` resume upload/from-resume into `resume.py` or keep as profile-specific
- Add redirects from `/api/v1/enhanced/resume/*` → `/api/v1/resume/*`
- Add redirects from `/api/v1/profile/from-resume` → `/api/v1/resume/from-text`

### Interview
```
/api/v1/interview/* → interview.py (canonical)
```
- Merge `mock_interview.py` endpoints into `interview.py`
- Merge `interview_replay.py` endpoints into `interview.py`
- Keep `interview_booking.py` and `interview_chat.py` separate if they are truly distinct features

### Onboarding
```
/api/v1/onboarding/* → onboarding.py (canonical)
```
- Merge `onboarding_doors.py` into `onboarding.py`
- Merge `onboarding_launch.py` into `onboarding.py`
- Merge `onboarding_diagnostic.py` into `onboarding.py`

### Analytics
```
/api/v1/analytics/* → analytics.py (user) + analytics_admin.py (admin)
```
- Keep separate but ensure no overlapping paths

### Profile
```
/api/v1/profile/* → career_profile.py (canonical)
```
- Merge `profile_stats.py` endpoints into `career_profile.py`

### OA
```
/api/v1/oa/* → oa.py (canonical)
```
- Merge `oa_engine.py` into `oa.py`

### Questions
```
/api/v1/questions/* → questions.py (canonical)
```
- Merge `questions_solve.py` into `questions.py`
- Keep `features.py` separate for feature-specific routes (bookmarks, notes)
- Keep `problems.py` separate if it's a distinct admin/problem-management feature
- Keep `submissions.py` separate for submission history

### Lesson
```
/api/v1/lesson/* → lesson.py (canonical)
```
- Merge `lesson_planner.py` into `lesson.py`

### Company
```
/api/v1/company-prep/* → company_prep.py (canonical)
```
- Merge `companies.py` into `company_prep.py`
- Merge `company_mocks.py` into `company_prep.py`
- Merge `company_lessons.py` into `company_prep.py`
- Merge `company_tracks.py` into `company_prep.py`
- Keep `placement_packs.py` separate for placement-specific routes
- Keep `tracks.py` separate if it's a distinct feature

### Learning
```
/api/v1/learning/* → learning.py (canonical)
```
- Merge `learning_modules.py` into `learning.py`
- Merge `learning_paths.py` into `learning.py`
- Merge `unified_learning.py` into `learning.py`
- Keep `lesson.py` separate for lesson-specific routes
- Keep `company_lessons.py` separate for company-specific lessons
- Keep `free_trial.py` separate for trial routes

### Problems
```
/api/v1/problems/* → problems.py (canonical)
```
- Keep `features.py` separate for feature-specific routes
- Keep `submissions.py` separate for submission history

### Placement
```
/api/v1/placement/* → placement.py (canonical)
```
- Merge `placement_calendar.py` into `placement.py`
- Merge `placement_packs.py` into `placement.py`
- Merge `placement_questions.py` into `placement.py`

### Study
```
/api/v1/study/* → study.py (canonical)
```
- Merge `adaptive_learning.py` into `study.py`

### Gamification
```
/api/v1/gamification/* → gamification.py (canonical)
```
- Merge `progress.py` into `gamification.py`

## Files to Remove After Consolidation
These will become empty or redundant after merging:
- `interview_replay.py`
- `mock_interview.py`
- `onboarding_doors.py`
- `onboarding_launch.py`
- `onboarding_diagnostic.py`
- `lesson_planner.py`
- `questions_solve.py`
- `oa_engine.py`
- `profile_stats.py`
- `aptitude_tests.py` (merge into `aptitude.py`)
- `daily_problem.py` (merge into `daily_challenge.py`)

## Redirect Strategy
For backward compatibility, add redirect endpoints in the canonical files:

```python
# In interview.py
@router.get("/{interview_id}/replay")
async def get_interview_replay_redirect(interview_id: str, user=Depends(get_current_user)):
    return await get_interview_replay(interview_id, user)
```

Or use FastAPI's `include_router` with `prefix` remapping.

## Frontend Impact
- Update `frontend/src/services/api/*.ts` to use canonical endpoints
- Update `frontend/src/pages/lazy.ts` if any imports change
- Update `frontend/src/hooks/*.ts` if any API calls change
- Test all pages that call the affected endpoints

## Backend Impact
- `main.py` auto-discovers routes via `pkgutil.iter_modules` — removing files is safe
- No need to update `main.py` unless we want to explicitly exclude files
- Run `python -m compileall app/ -q` after changes to verify no import errors
- Run `python -m py_compile` on all modified files

## Testing Plan
1. Backend compile check
2. Start backend and check `/docs` for duplicate paths
3. Run existing tests
4. Update frontend API modules
5. Run frontend build
6. Test critical flows: resume upload → optimize → export, interview start → answer → result, onboarding flow
