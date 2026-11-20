# 03_ROUTE_API_CONTRACT.md — Route-to-API-to-Engine Mapping

> Every frontend route maps to backend APIs, application use cases, domain engines, and data sources. No orphan pages, dead buttons, or undocumented shortcuts.

---

## Six Primary Navigation Hubs

| Hub | Frontend Route | Backend API | Use Case | Engine | Data Source |
|-----|---------------|-------------|----------|--------|-------------|
| Dashboard | `/dashboard` | `GET /api/v1/dashboard` | GetLearnerDashboard | Dashboard projections | gamification, skill_graph |
| Journey | `/journey/:worldId` | `GET /api/v1/worlds/{id}` | GetLesson | Curriculum registry | worlds_data, registry |
| Practice | `/practice` | `GET /api/v1/questions/browse` | BrowseQuestions | Question store | question_store |
| Mock OA | `/mock-oa` | `POST /api/v1/oa/start` | StartMockAssessment | Company blueprint + quiz | company_blueprints.json |
| AI Interview | `/ai-interview` | `POST /api/v1/interview/start` | StartInterview | AI Gateway + interview engine | ai_core, COMPANY_PROFILES |
| Company Tracks | `/company-tracks` | `GET /api/v1/company-tracks` | GetCompanyTracks | Blueprint overlay | company_blueprints.json |
| Profile | `/profile` | `GET /api/v1/profile/stats` | GetProfile | Profile service | users, gamification |

---

## Complete Route-to-Engine Mapping

### Authentication

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/login` | `POST /api/v1/auth/login` | Authenticate | Auth middleware | users |
| `/register` | `POST /api/v1/auth/register` | Register | Auth middleware | users |
| `/forgot-password` | `POST /api/v1/auth/forgot-password` | Reset request | Email service | - |
| `/reset-password` | `POST /api/v1/auth/reset-password` | Reset password | Auth middleware | users |
| `/logout` | `POST /api/v1/auth/logout` | Clear cookie | Auth middleware | - |

### Onboarding

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/onboarding` | `GET /api/v1/auth/onboarding-status` | Check status | Onboarding service | academy_learner_profiles |
| `/onboarding` | `POST /api/v1/auth/onboarding-complete` | CompleteOnboarding | Profile + blueprint | academy_learner_profiles |

### Dashboard (Daily Starting Point)

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/dashboard` | `GET /api/v1/dashboard` | GetLearnerDashboard | Dashboard projections | gamification, skill_graph, readiness |
| `/dashboard` | `GET /api/v1/gamification/profile` | GetRewardProjection | Gamification read model | gamification_collection |

### Journey (Worlds & Lessons)

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/journey/:worldId` | `GET /api/v1/worlds/{id}` | GetLesson | Curriculum registry | worlds_data |
| `/journey/:worldId/progress` | `GET /api/v1/worlds/{id}/progress` | GetProgress | Progress tracker | gamification_collection |
| `/journey/:worldId/levels/{id}/attempt` | `POST /api/v1/worlds/{id}/levels/{id}/attempt` | AttemptLevel | Deterministic judge | worlds_data checks |
| `/journey/:worldId/levels/{id}/complete` | `POST /api/v1/worlds/{id}/levels/{id}/complete` | CompleteLesson | Mastery engine + rewards | gamification, skill_graph |
| `/journey/:worldId/levels/{id}/hint` | `POST /api/v1/worlds/{id}/levels/{id}/hint` | RecordHint | Hint tracker | gamification_collection |

### Practice (Question Bank)

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/question-bank` | `GET /api/v1/questions/browse` | BrowseQuestions | Question store | question_store |
| `/question-bank/:questionId` | `GET /api/v1/questions/{id}` | GetQuestion | Question store | question_store |
| `/question-bank/:questionId/solve` | `POST /api/v1/questions/{id}/submit` | SubmitQuizAttempt | Deterministic grader | question_answers |
| `/problems` | `GET /api/v1/problems` | ListProblems | Question store | question_store |
| `/problems/:topic` | `GET /api/v1/problems/{topic}` | FilterByTopic | Question store | question_store |
| `/solve/:id` | `POST /api/v1/questions/{id}/answer` | SubmitAnswer | AI feedback + grader | question_answers |

### Mock OA

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/mock-oa` | `GET /api/v1/oa/companies` | ListCompanies | Company blueprint | company_blueprints.json |
| `/mock-oa/:company` | `POST /api/v1/oa/start` | StartMockAssessment | Blueprint + quiz + timer | company_blueprints.json |
| `/mock-oa/sessions/:id` | `POST /api/v1/oa/{id}/answer` | SubmitOAAnswer | Server timer + grader | oa_sessions |
| `/mock-oa/sessions/:id/result` | `GET /api/v1/oa/{id}/result` | FinalizeMock | Evidence + readiness | oa_results, readiness_engine |

### AI Interview

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/ai-interview/sessions` | `POST /api/v1/interview/start` | StartInterview | AI Gateway + COMPANY_PROFILES | interview_sessions |
| `/ai-interview/sessions/:id` | `POST /api/v1/interview/answer` | SubmitAnswer | AI Gateway + rubric | interview_answers |
| `/ai-interview/sessions/:id/result` | `GET /api/v1/interview/{id}/result` | GetResult | Interview evaluation | interview_results |

### Company Tracks

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/company-tracks` | `GET /api/v1/company-tracks` | GetTracks | Blueprint overlay | company_blueprints.json |
| `/company-tracks/:slug` | `GET /api/v1/company/{slug}/guide` | GetCompanyGuide | Blueprint | company_blueprints.json |
| `/company-tracks/:slug/readiness` | `GET /api/v1/readiness` | CalculateReadiness | Readiness engine | readiness_engine |

### Profile

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/profile/overview` | `GET /api/v1/profile/stats` | GetProfile | Profile service | users, gamification |
| `/profile/evidence` | `GET /api/v1/evidence` | GetEvidence | Evidence aggregator | telemetry_events |
| `/profile/achievements` | `GET /api/v1/gamification/badges` | GetBadges | Badge engine | gamification_collection |
| `/profile/resume` | `GET /api/v1/resume/history` | GetResumeHistory | Resume service | resumes |

### Admin

| Frontend Route | API | Use Case | Engine | Data |
|---------------|-----|----------|--------|------|
| `/admin` | `GET /api/v1/analytics/admin` | GetAdminMetrics | Analytics service | telemetry_events |
| `/admin/content` | `GET /api/v1/admin/content` | GetContent | Content admin | question_store (read-only) |
| `/admin/trust-review` | `POST /api/v1/questions/review` | ReviewQuestion | Trust gate | question_store |

---

## Redirected / Legacy Routes

| Old Route | Redirect Target | Reason |
|-----------|----------------|--------|
| `/academy` | `/question-bank` | Removed feature (August 2026 cleanup) |
| `/journey` | `/learn` | Replaced by skill map |
| `/profile` | `/dashboard` | Consolidated into dashboard |
| `/rank` | `/leaderboard` | Renamed |
| `/company-prep` | `/skills` | Replaced by company-tracks |
| `/company-tracks` | `/skills` | Replaced by skills |
| `/quiz` | `/question-bank` | Consolidated |
| `/levels` | `/tower` | Renamed |
| `/modules` | `/learn/modules` | Consolidated |

---

## API Domains

```
/api/v1/auth           — Registration, login, logout, onboarding
/api/v1/onboarding     — Onboarding quest and first-run
/api/v1/dashboard      — Learner dashboard (today's hunt)
/api/v1/worlds         — World/town/level progression
/api/v1/lesson         — Lesson content and step completion
/api/v1/questions      — Question bank (browse, solve, submit)
/api/v1/quiz           — Quiz sessions (practice, timed, boss)
/api/v1/oa             — Mock online assessment
/api/v1/interview      — AI mock interviews
/api/v1/company        — Company-specific preparation
/api/v1/readiness      — Interview readiness scoring
/api/v1/repair         — Repair missions and retest
/api/v1/srs            — Spaced repetition
/api/v1/gamification   — XP, streaks, badges, tower
/api/v1/evidence       — Learning event telemetry
/api/v1/observability  — Funnel + algorithm health metrics
/api/v1/admin          — Admin content and analytics
```

---

## Route Safety Rules

1. Every route has a Pydantic request model and response model
2. No answer keys in client payloads
3. All write endpoints are idempotent
4. Authenticated routes require valid JWT (httpOnly cookie)
5. Admin routes require `role=admin` or `is_admin=true`
6. Browser refresh on dynamic routes restores state
7. No duplicate (method, path) combinations
