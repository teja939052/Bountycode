# BountyCode — Complete A-to-Z Code Explanation

This document explains every piece of code built for the unified Indian prep platform integration, including context, purpose, architecture, routes, and how all components connect. It is designed to be read by another AI model to understand the full system.

---

## 1. Project Context

**BountyCode** is an AI-powered placement preparation platform targeting Indian students and job seekers. The codebase follows a **canonical architecture freeze** where the architecture is frozen and only content excellence work is permitted. The canonical pipeline is:

```
Journey → Study Engine → Lesson Engine → Mastery → SRS → Gamification → Mock OA → Repair → AI Interview → Readiness → Journey
```

The goal of this work was to add **role-based learning paths** and **company-specific tracks** as a discovery layer, then wire enrollment to set the user's goal so the **Journey Engine** becomes the single execution surface.

---

## 2. Architecture Overview

### 2.1 The Unified Architecture

```
                 PREPHUB (discovery only)
             "What can I prepare for?"
                      |
             +--------+--------+
             |                 |
             v                 v
        ROLE PATHS        COMPANY TRACKS
             |                 |
             +--------+--------+
                      |
                  ENROLLMENT
                      |
                      v
                 USER GOAL
        (role_path, company_track, target_company)
                      |
                      v
                  JOURNEY
                      |
                      v
              STUDY ENGINE
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
      LESSON        PRACTICE       SRS
        |             |             |
        +-------------+-------------+
                      v
                   MASTERY
                      |
                 +----+----+
                 v         v
              MOCK OA   AI INTERVIEW
                 |         |
                 +----+----+
                      v
                  READINESS
                      |
                      v
                   JOURNEY (loop)
```

### 2.2 Key Design Principles

1. **No new engines** — We compose existing canonical systems (Study Engine, Journey Engine, Gamification, Readiness).
2. **Enrollment sets the goal** — When a user enrolls, their `role_path` and `company_track` are written to the users collection.
3. **Journey is the single surface** — The student never needs to open `/learning-paths` → `/company-tracks` → `/quiz` → `/mock-oa` → `/interview` separately.
4. **Company influence is content-aware** — When a company track is enrolled, practice questions and role exercises are filtered by company-relevant topics, not just given a scoring bonus.

---

## 3. Backend Files

### 3.1 `backend/app/data/learning_paths.py` — Seed Data

**Purpose**: Defines the role-based learning paths and company-specific tracks catalog.

**Context**: This is the single source of truth for what roles and companies the platform supports. It is imported by services and used to generate API responses.

**Contents**:
- `ROLES` dict — 4 role paths: `sde`, `data_analyst`, `qa_engineer`, `devops`
- `COMPANY_TRACKS` dict — 8 company tracks: `tcs_nqt`, `accenture_amcat`, `infosys_infytq`, `wipro_nlth`, `tech_mahindra_smart`, `cognizant_genc`, `lti_mindtree`, `capgemini_indrive`

**Role structure**:
```python
{
    "id": "sde",
    "name": "Software Development Engineer",
    "short_name": "SDE",
    "icon": "💻",
    "color": "#3B82F6",
    "description": "Master data structures, algorithms...",
    "target_roles": ["SDE", "Backend Engineer", ...],
    "avg_package": "6-25 LPA",
    "duration_weeks": 12,
    "difficulty": "medium",
    "prerequisites": [...],
    "modules": [
        {
            "id": "sde_m1",
            "title": "Programming Fundamentals",
            "description": "...",
            "icon": "🐍",
            "color": "#22C55E",
            "duration_days": 7,
            "xp_reward": 200,
            "topics": ["Python/Java/C++ basics", ...],
            "skills": ["language_proficiency", "problem_solving"],
            "activities": ["coding", "aptitude"],
            "unlocks": ["sde_m2"],
        },
        ...
    ],
    "final_project": {...},
    "certification": "SDE Ready",
}
```

**Company track structure**:
```python
{
    "id": "tcs_nqt",
    "company_id": "tcs",
    "name": "TCS NQT",
    "full_name": "TCS National Qualifier Test",
    "icon": "🏢",
    "color": "#1E3A5F",
    "role": "SDE",
    "package_range": "3.5-11 LPA",
    "duration_minutes": 190,
    "difficulty": "easy",
    "description": "...",
    "sections": [
        {
            "id": "tcs_foundation",
            "title": "Foundation Round",
            "description": "Aptitude, Verbal, Reasoning...",
            "duration_minutes": 75,
            "questions_count": 65,
            "negative_marking": False,
            "topics": [
                {"name": "Quantitative Aptitude", "weight": 20, "sub_topics": [...]},
                ...
            ],
            "modules": [
                {"id": "tcs_f1", "title": "...", "xp": 100, "questions": 20, "topics": [...]},
                ...
            ],
        },
        ...
    ],
    "coding_patterns": ["Find second largest element in array", ...],
    "hr_questions": ["Tell me about yourself", ...],
    "tips": ["TCS NQT has no negative marking...", ...],
    "success_rate": "High (70%+ with preparation)",
}
```

**Why this design**: File-based seed data is simple, version-controllable, and easy to update. No database migration needed for content changes. The structured format with sections → modules → topics mirrors the actual exam pattern of Indian IT companies.

---

### 3.2 `backend/app/models/learning_path.py` — Pydantic Models

**Purpose**: Type-safe request/response models for the learning paths and company tracks API.

**Models**:
- `LearningPathEnroll` — `{ path_id: str, company_track_id?: str }`
- `PathModuleProgress` — tracks per-module progress
- `UserPathProgress` — full user progress in a role path
- `UserTrackProgress` — full user progress in a company track
- `LearningPathSummary` — catalog list item
- `CompanyTrackSummary` — catalog list item
- `PathModuleDetail` — module with status flags
- `TrackModuleDetail` — track module with status flags
- `PathRecommendation` — personalized recommendation

**Why Pydantic**: FastAPI uses Pydantic for automatic validation, serialization, and OpenAPI schema generation. This ensures type safety across the entire API surface.

---

### 3.3 `backend/app/services/learning_paths.py` — Core Service

**Purpose**: Business logic for catalog, enrollment, progress tracking, and recommendations. This is the single most important service for the new feature.

**Key functions**:

1. **`get_all_roles()`** — Returns all role paths with computed `total_modules` and `total_xp`.

2. **`get_role_path(role_id)`** — Returns a single role path from the seed data.

3. **`get_all_company_tracks()`** — Returns all company tracks with computed `total_sections`, `total_modules`, `total_xp`.

4. **`get_company_track(track_id)`** — Returns a single company track.

5. **`enroll_in_path(user_id, path_id)`** — Enrolls user in a role path. **Critical**: Also sets `role_path` and `target_role` in the users collection so Journey Engine can use it.
   ```python
   await users_collection().update_one(
       {"user_id": user_id},
       {"$set": {
           "role_path": path_id,
           "target_role": role.get("short_name", path_id),
           "role_path_enrolled_at": now,
       }},
   )
   ```

6. **`enroll_in_track(user_id, track_id)`** — Enrolls user in a company track. **Critical**: Also sets `company_track` and `target_company` in the users collection.
   ```python
   await users_collection().update_one(
       {"user_id": user_id},
       {"$set": {
           "company_track": track_id,
           "target_company": track.get("company_id", track_id),
           "company_track_enrolled_at": now,
       }},
   )
   ```

7. **`complete_path_module(user_id, path_id, module_id, score)`** — Marks a module complete, awards XP with bonus for high scores, unlocks next module.

8. **`complete_track_module(user_id, track_id, module_id, score)`** — Marks a company track module complete.

9. **`get_user_path_progress(user_id, path_id)`** — Reads progress from `user_learning_paths_collection`.

10. **`get_user_track_progress(user_id, track_id)`** — Reads progress from `user_company_tracks_collection`.

11. **`get_all_user_paths(user_id)`** — Lists all enrolled paths with progress.

12. **`get_all_user_tracks(user_id)`** — Lists all enrolled tracks with progress.

13. **`get_user_goal(user_id)`** — **Key helper**: Reads the user's `role_path`, `company_track`, `target_company`, `target_role` from the users collection. This is what the Journey Engine and Study Engine consume.

14. **`get_recommended_paths(user_id)`** — Returns personalized recommendations based on enrollment history and skill graph.

**Database collections used**:
- `user_learning_paths_collection` — stores `user_id`, `path_id`, `modules` (with completion status), `total_xp_earned`, `completed`
- `user_company_tracks_collection` — stores `user_id`, `track_id`, `sections` (with completion status), `total_xp_earned`
- `users_collection` — stores the goal fields: `role_path`, `company_track`, `target_company`, `target_role`

**Why this design**: The service is the single source of truth for the new feature. It writes the goal to the users collection so other systems (Journey, Study) can read it without coupling to the new feature.

---

### 3.4 `backend/app/routes/learning_paths.py` — Role Path API

**Purpose**: HTTP endpoints for role-based learning paths.

**Routes**:
- `GET /api/v1/learning-paths/roles` — List all role paths with enrollment status
- `GET /api/v1/learning-paths/roles/{role_id}` — Get a single role with module status
- `POST /api/v1/learning-paths/roles/enroll` — Enroll in a role path
- `POST /api/v1/learning-paths/roles/{role_id}/modules/{module_id}/complete` — Complete a module
- `GET /api/v1/learning-paths/my-paths` — List user's enrolled paths
- `GET /api/v1/learning-paths/recommendations` — Get personalized recommendations

**Helper**: `_is_unlocked(module, all_modules, progress)` — Checks if a module should be unlocked based on `depends_on` dependencies.

---

### 3.5 `backend/app/routes/company_tracks.py` — Company Track API

**Purpose**: HTTP endpoints for company-specific tracks.

**Routes**:
- `GET /api/v1/company-tracks/companies` — List all company tracks with enrollment status
- `GET /api/v1/company-tracks/companies/{track_id}` — Get a single track with section/module status
- `POST /api/v1/company-tracks/companies/enroll` — Enroll in a company track
- `POST /api/v1/company-tracks/companies/{track_id}/modules/{module_id}/complete` — Complete a track module
- `GET /api/v1/company-tracks/my-tracks` — List user's enrolled tracks

---

### 3.6 `backend/app/database.py` — Collections and Indexes

**Purpose**: MongoDB collections and index management.

**New collections added**:
```python
user_learning_paths_collection = _LazyCollection("user_learning_paths")
user_company_tracks_collection = _LazyCollection("user_company_tracks")
```

**New indexes added in `init_db()`**:
```python
await _safe_create_index(db["user_learning_paths"], [("user_id", 1), ("path_id", 1)], unique=True)
await _safe_create_index(db["user_company_tracks"], [("user_id", 1), ("track_id", 1)], unique=True)
await _safe_create_index(db["user_learning_paths"], "user_id")
await _safe_create_index(db["user_company_tracks"], "user_id")
await _safe_create_index(db["user_learning_paths"], [("user_id", 1), ("completed", 1)])
await _safe_create_index(db["user_company_tracks"], [("user_id", 1), ("completed", 1)])
```

**Why indexes**: The unique compound index on `(user_id, path_id)` prevents duplicate enrollments. The single-field index on `user_id` speeds up lookups. The `(user_id, completed)` index supports progress queries.

---

### 3.7 `backend/app/services/journey_engine.py` — Journey Engine (Modified)

**Purpose**: The canonical orchestrator that determines the highest-value next action for any student. It composes from Study Engine, Gamification, Mastery, Readiness, and Company context.

**Key modifications for the new feature**:

1. **New helpers**:
   ```python
   def _user_role_path(user: Dict[str, Any]) -> str:
       """Read enrolled role path from user profile."""
       return user.get("role_path", "") or ""

   def _user_company_track(user: Dict[str, Any]) -> str:
       """Read enrolled company track from user profile."""
       return user.get("company_track", "") or ""
   ```

2. **Priority scoring boost** — When a company track is enrolled, `company_track` gets a priority weight of `role_practice + 10`:
   ```python
   if company_track:
       scores["company_track"] = PRIORITY_WEIGHTS["role_practice"] + 10
   ```

3. **Journey state output** — The `company` block now includes `role_path` and `company_track`:
   ```python
   "company": {
       "target": target_company,
       "target_role": target_role,
       "role_path": role_path,
       "company_track": company_track,
   },
   ```

**Priority matrix** (the canonical priority engine):
```python
PRIORITY_WEIGHTS = {
    "srs_overdue": 100,
    "failed_repair": 95,
    "prerequisite": 90,
    "company_critical": 85,
    "current_lesson": 80,
    "role_practice": 70,
    "mock_prep": 60,
    "challenge": 40,
    "exploration": 10,
}
```

**How `_rank_activities()` works**:
1. Reads user profile (`role_path`, `company_track`, `target_company`, `target_role`)
2. Reads Study Engine daily plan
3. Reads mastery/skill assessment
4. Reads readiness scores
5. Reads SRS due cards
6. Computes priority scores for each category
7. Selects the winner (highest score)

**`build_journey_state(user_id)` output**:
```python
{
    "character": { "level", "title", "position", "state" },
    "today": {
        "date": "2026-09-04",
        "next": { "type", "title", "description", ... },
        "reviews": [...],
        "practice": [...],
        "challenge": {...},
    },
    "stats": { "xp", "level", "coins", "streak", "badges_count" },
    "readiness": { "interview_readiness", "oa_readiness", "mastered_count" },
    "company": {
        "target": "tcs",
        "target_role": "SDE",
        "role_path": "sde",
        "company_track": "tcs_nqt",
    },
    "priority": { "winner_category", "scores", "winner_score" },
}
```

**Why this design**: The Journey Engine is the single entry point for the frontend. It answers "What do I do next?" by composing all canonical systems. The new `role_path` and `company_track` fields flow through here so the frontend can display the goal.

---

### 3.8 `backend/app/services/study_engine.py` — Study Engine (Modified)

**Purpose**: Decides what a student does next. Owns the `TODAY` loop: NEXT + REVIEW + PRACTICE + CHALLENGE.

**Key modifications for the new feature**:

1. **New function `_get_company_mission(user_id)`**:
   ```python
   async def _get_company_mission(user_id: str) -> Optional[Dict[str, Any]]:
       """Get the next company-aligned mission for the student."""
       user = await users_collection().find_one({"user_id": user_id})
       company_track = user.get("company_track", "")
       target_company = user.get("target_company", "")
       if not company_track and not target_company:
           return None

       track = COMPANY_TRACKS.get(company_track)
       progress = await user_company_tracks_collection.find_one(
           {"user_id": user_id, "track_id": company_track}
       )
       # Find first incomplete section/module
       for sec_id, sec_data in sections.items():
           if sec_data.get("completed"):
               continue
           for mod_id, mod_data in modules.items():
               if mod_data.get("completed"):
                   continue
               return {
                   "type": "company_mission",
                   "title": f"{track['name']}: {sec_data.get('title', 'Practice')}",
                   "track_id": company_track,
                   "section_id": sec_id,
                   "module_id": mod_id,
                   "estimated_minutes": 30,
                   "xp_reward": 50,
               }
   ```

2. **`_get_practice_tasks()` modified for company-aware filtering**:
   ```python
   # Read company-relevant topics from the enrolled track
   company_relevant_topics = []
   if company_track:
       track = COMPANY_TRACKS.get(company_track)
       for section in track.get("sections", []):
           for topic in section.get("topics", []):
               for sub in topic.get("sub_topics", []):
                   company_relevant_topics.append(sub)

   # Filter question pool by company-relevant topics
   if company_relevant_topics and pool:
       company_pool = [
           q for q in pool
           if any(t in (q.get("topics") or []) for t in company_relevant_topics)
           or any(t in (q.get("tags") or []) for t in company_relevant_topics)
       ]
       if company_pool:
           pool = company_pool
   ```

3. **`get_today()` output now includes `company_mission`**:
   ```python
   plan = {
       "date": today,
       "user_id": user_id,
       "streak": streak,
       "level": level,
       "next": next_mission,
       "reviews": reviews,
       "practice": practice,
       "challenge": challenge,
       "role_activity": role_activity,
       "company_mission": company_mission,  # NEW
   }
   ```

**Why this design**: The Study Engine is the content selection layer. By making `_get_practice_tasks` company-aware, we ensure that when a student is preparing for TCS, they get TCS-relevant practice questions, not random SDE exercises. The `_get_company_mission` function surfaces the next incomplete company track module as a daily mission.

---

### 3.9 `backend/app/services/role_content_service.py` — Role Content (Modified)

**Purpose**: Integrates role content with the existing pipeline. Connects role exercises/challenges → Mastery → SRS → XP → Readiness.

**Key modification**: `get_next_role_activity()` is now company-aware:
```python
async def get_next_role_activity(user_id: str, role_id: str):
    # Read user goal
    company_relevant_topics = []
    if user_doc.get("company_track"):
        track = COMPANY_TRACKS.get(user_doc["company_track"])
        # Collect company topics...

    # Filter exercises by company-relevant topics
    if company_relevant_topics:
        company_exercises = [
            eid for eid in ps.exercise_ids
            if any(t in exercise.topics for t in company_relevant_topics)
        ]
        if company_exercises:
            exercise_id = company_exercises[0]
```

**Why this design**: Role exercises are filtered by company topics, so a student preparing for TCS gets TCS-relevant role exercises, not generic SDE exercises.

---

### 3.10 `backend/app/routes/journey.py` — Journey Route

**Purpose**: Single HTTP endpoint that returns the canonical journey state.

**Route**:
- `GET /api/v1/journey/state` — Returns the full JourneyState from `build_journey_state()`

**Why a single route**: The Journey Engine composes everything into one payload. The frontend calls this one endpoint to render the entire Journey page.

---

## 4. Frontend Files

### 4.1 `frontend/src/services/api/learningPaths.ts` — API Client

**Purpose**: Typed API client for both learning paths and company tracks.

**Exports**:
- `learningPathsApi` — `listRoles()`, `getRole()`, `enroll()`, `completeModule()`, `getMyPaths()`, `getRecommendations()`
- `companyTracksApi` — `listCompanies()`, `getTrack()`, `enroll()`, `completeModule()`, `getMyTracks()`

**Types**:
- `RolePath`, `PathModule`, `CompanyTrack`, `TrackSection`, `TrackModule`, `Recommendation`

**Why this design**: One file for both APIs since they share concepts. Typed interfaces ensure the frontend and backend stay in sync.

---

### 4.2 `frontend/src/pages/LearningPaths.tsx` — Role Paths Page

**Purpose**: Browse and enroll in role-based learning paths.

**Features**:
- Grid of role cards (SDE, Data Analyst, QA, DevOps)
- Each card shows: icon, name, description, duration, difficulty, modules count, XP, avg package
- Progress bar for enrolled paths
- Detail view with module list, completion, and unlock status
- "Complete" button for enrolled modules
- "Enroll Now" button for unenrolled paths

**State management**: React Query (`useQuery`, `useMutation`) for server state.

---

### 4.3 `frontend/src/pages/CompanyTracks.tsx` — Company Tracks Page

**Purpose**: Browse and enroll in company-specific tracks.

**Features**:
- Grid of company track cards (TCS, Accenture, Infosys, etc.)
- Each card shows: icon, name, description, duration, difficulty, modules count, package range
- Detail view with sections, modules, coding patterns, HR questions, and pro tips
- "Complete" button for enrolled modules
- "Enroll Now" button for unenrolled tracks

**Key sections in detail view**:
- **Sections**: The actual exam pattern (e.g., TCS Foundation + Advanced)
- **Topics**: Weighted topic list (e.g., Quantitative Aptitude 20%, Verbal 20%, Reasoning 20%)
- **Modules**: Practice modules within each section
- **Coding Patterns**: 10 common coding problems for that company
- **HR Questions**: 10 common HR questions
- **Pro Tips**: Company-specific preparation advice

---

### 4.4 `frontend/src/pages/PrepHub.tsx` — Unified Discovery

**Purpose**: Single discovery page for both roles and companies.

**Features**:
- Search bar across roles and companies
- Three tabs: "For You" (recommendations), "Learning Paths", "Company Tracks"
- Recommendations based on user profile
- Quick links to all roles and companies

**Why this design**: PrepHub is **discovery only**. It does not duplicate the learning system. It just surfaces what the student can prepare for, and enrollment leads to Journey becoming the single execution surface.

---

### 4.5 `frontend/src/hooks/useJourneyState.ts` — Journey State Hook

**Purpose**: React Query hook that fetches the journey state.

**Modification**: Added `JourneyCompany` and `JourneyReadiness` interfaces to the `JourneyState` type:
```typescript
export interface JourneyCompany {
  target: string;
  target_role: string;
  role_path: string;
  company_track: string;
}

export interface JourneyReadiness {
  interview_readiness: number;
  oa_readiness: number;
  mastered_count: number;
}
```

---

### 4.6 `frontend/src/services/api/index.ts` — API Index

**Modification**: Added `learningPathsApi` and `companyTracksApi` to the aggregated API object:
```typescript
import { learningPathsApi, companyTracksApi } from "./learningPaths.ts";

const api = {
  ...
  learningPaths: learningPathsApi,
  companyTracks: companyTracksApi,
  ...
};
```

---

### 4.7 `frontend/src/pages/lazy.ts` — Lazy Imports

**Modification**: Added lazy imports and exports for new pages:
```typescript
const LearningPaths = lazy(() => import('./LearningPaths'));
const CompanyTracks = lazy(() => import('./CompanyTracks'));
const PrepHub = lazy(() => import('./PrepHub'));
```

---

### 4.8 `frontend/src/App.tsx` — Routing

**Modification**: Added new routes:
```typescript
<Route path="/learning-paths" element={<LearningPaths />} />
<Route path="/company-tracks" element={<CompanyTracks />} />
<Route path="/prep-hub" element={<PrepHub />} />
```

---

### 4.9 `frontend/src/components/Navbar.tsx` — Navigation

**Modification**: 
- Changed "Prepare" link to point to `/prep-hub`
- Added "Learning Paths" and "Company Tracks" in the "Your Journey" group in the More menu

---

## 5. The Complete Flow — End to End

### 5.1 Student Journey

```
1. Student signs up
   ↓
2. Student visits /prep-hub
   - Sees "For You" recommendations
   - Sees "Learning Paths" (SDE, Data Analyst, QA, DevOps)
   - Sees "Company Tracks" (TCS, Accenture, Infosys, etc.)
   ↓
3. Student clicks SDE → enrolls
   - POST /api/v1/learning-paths/roles/enroll { path_id: "sde" }
   - users.role_path = "sde"
   - users.target_role = "SDE"
   ↓
4. Student clicks TCS NQT → enrolls
   - POST /api/v1/company-tracks/companies/enroll { path_id: "tcs_nqt" }
   - users.company_track = "tcs_nqt"
   - users.target_company = "tcs"
   ↓
5. Student lands on Journey
   - GET /api/v1/journey/state
   - state.company.role_path = "sde"
   - state.company.company_track = "tcs_nqt"
   - state.company.target = "tcs"
   - state.company.target_role = "SDE"
   ↓
6. Journey shows today's plan:
   - Today's Mission (company-filtered practice)
   - Company Mission (next TCS module)
   - Role Activity (SDE exercise, company-filtered)
   - SRS Reviews
   - Readiness Score (TCS-specific)
   ↓
7. Student completes activities
   - POST /api/v1/learning-paths/roles/sde/modules/sde_m1/complete
   - POST /api/v1/company-tracks/companies/tcs_nqt/modules/tcs_f1/complete
   - XP awarded, mastery updated, SRS scheduled
   ↓
8. Journey recomputes
   - Readiness increases
   - Next module unlocks
   - Daily queue changes
```

### 5.2 Goal Switching

```
Student changes from SDE + TCS to SDE + Amazon
   ↓
1. Student visits /company-tracks
2. Clicks Amazon → enrolls
   - POST /api/v1/company-tracks/companies/enroll { path_id: "amazon_sde" }
   - users.company_track = "amazon_sde"
   - users.target_company = "amazon"
   ↓
3. Journey recomputes:
   - state.company.company_track = "amazon_sde"
   - state.company.target = "amazon"
   - Practice tasks now filtered by Amazon-relevant topics
   - Readiness computed against Amazon profile
   - Company Mission surfaces next Amazon module
```

---

## 6. Research Purpose & Design Rationale

### 6.1 Why Role-Based Learning Paths?

Indian placement preparation is role-specific:
- **SDE** (Software Development Engineer) needs DSA, system design, coding
- **Data Analyst** needs SQL, Python, statistics, visualization
- **QA Engineer** needs testing fundamentals, Selenium, API testing
- **DevOps Engineer** needs Linux, Docker, Kubernetes, CI/CD

Each role has a different curriculum, different companies, and different interview patterns. By organizing by role, we give students a clear path tailored to their target.

### 6.2 Why Company-Specific Tracks?

Indian IT companies (TCS, Infosys, Wipro, Accenture, etc.) have distinct exam patterns:
- **TCS NQT**: Foundation (Aptitude + Verbal + Reasoning) + Advanced (Coding)
- **Accenture AMCAT**: Numerical + Logical + Verbal + Coding
- **Infosys InfyTQ**: Aptitude + Programming MCQ + Coding + SQL
- **Wipro NLTH**: Aptitude + Coding + English

By organizing by company, we give students company-specific preparation that matches the actual exam pattern.

### 6.3 Why Goal-Aware Content Selection?

The key insight is: **random practice is not effective**. A student preparing for TCS should practice TCS-relevant topics (aptitude, arrays, strings, basic algorithms), not random LeetCode hard problems. By making the Study Engine company-aware, we ensure that practice is relevant to the student's goal.

### 6.4 Why Journey as the Single Surface?

The original platform had 5+ separate pages (`/learning-paths`, `/company-tracks`, `/quiz`, `/mock-oa`, `/interview`). This created a coordination problem: students had to manually decide what to study. By making Journey the single execution surface:
- Students see one clear "next action"
- The system adapts to their goal automatically
- No more manual coordination between subsystems

### 6.5 Why Content-Aware Company Influence (not just +10)?

The initial design had `company_track: role_practice + 10` in the priority scoring. This was too shallow — it just changed the ranking order, not the actual content. The improved design filters practice questions and role exercises by company-relevant topics, so the actual content is company-specific, not just the priority order.

---

## 7. Testing & Verification

### 7.1 Backend Tests
- **221 tests pass** — all existing tests still pass
- Backend compiles clean with `python -m compileall app/ -q`

### 7.2 Frontend Build
- **Build passes** — `npm run build` completes successfully
- TypeScript clean (only pre-existing `MiniProject.tsx` errors, unrelated)

### 7.3 Catalog Verification
- 4 roles: `sde`, `data_analyst`, `qa_engineer`, `devops`
- 8 company tracks: `tcs_nqt`, `accenture_amcat`, `infosys_infytq`, `wipro_nlth`, `tech_mahindra_smart`, `cognizant_genc`, `lti_mindtree`, `capgemini_indrive`

### 7.4 Integration Flow
1. Enroll in SDE → `users.role_path = "sde"` ✓
2. Enroll in TCS → `users.company_track = "tcs_nqt"` ✓
3. Journey state includes goal ✓
4. Study Engine surfaces company mission ✓
5. Practice tasks filtered by company topics ✓
6. Role exercises filtered by company topics ✓
7. Goal switching recomputes everything ✓

---

## 8. File Summary

| File | Purpose | Lines |
|------|---------|-------|
| `backend/app/data/learning_paths.py` | Seed data for roles and companies | ~1100 |
| `backend/app/models/learning_path.py` | Pydantic models | ~80 |
| `backend/app/services/learning_paths.py` | Core service (catalog, enrollment, progress, goal) | ~584 |
| `backend/app/routes/learning_paths.py` | Role path API | ~130 |
| `backend/app/routes/company_tracks.py` | Company track API | ~123 |
| `backend/app/database.py` | Collections and indexes (modified) | +6 lines |
| `backend/app/services/journey_engine.py` | Journey Engine (modified) | +~15 lines |
| `backend/app/services/study_engine.py` | Study Engine (modified) | +~80 lines |
| `backend/app/services/role_content_service.py` | Role content (modified) | +~25 lines |
| `frontend/src/services/api/learningPaths.ts` | API client | ~120 |
| `frontend/src/pages/LearningPaths.tsx` | Role paths page | ~280 |
| `frontend/src/pages/CompanyTracks.tsx` | Company tracks page | ~320 |
| `frontend/src/pages/PrepHub.tsx` | Unified discovery page | ~250 |
| `frontend/src/hooks/useJourneyState.ts` | Journey state hook (modified) | +~15 lines |
| `frontend/src/services/api/index.ts` | API index (modified) | +3 lines |
| `frontend/src/pages/lazy.ts` | Lazy imports (modified) | +3 lines |
| `frontend/src/App.tsx` | Routing (modified) | +3 lines |
| `frontend/src/components/Navbar.tsx` | Navigation (modified) | +5 lines |

---

## 9. Key Takeaways for Another AI Model

1. **Architecture is frozen** — We did NOT create new engines. We composed existing canonical systems.
2. **Enrollment sets the goal** — `role_path` and `company_track` are written to the users collection.
3. **Journey is the single surface** — The frontend calls `GET /api/v1/journey/state` to render the entire Journey page.
4. **Company influence is content-aware** — Practice tasks and role exercises are filtered by company-relevant topics, not just given a scoring bonus.
5. **No new database collections for content** — Roles and companies are in file-based seed data (`backend/app/data/learning_paths.py`). Only user progress is in MongoDB.
6. **Goal switching works** — Re-enrolling overwrites the goal fields, and all downstream systems recompute.
7. **The user never needs to open multiple pages** — Enrollment sets the goal, Journey becomes the single execution surface.

---

## 10. Future Work (Not Implemented)

1. **Dashboard widget for goal display** — Show the enrolled role/company prominently on the dashboard.
2. **Mock OA company-specific content** — When a company track is enrolled, Mock OA should use company-specific questions.
3. **AI Interview company-specific configuration** — When a company track is enrolled, AI Interview should use company-specific behavioral questions.
4. **Readiness breakdown by company requirement** — Show which company requirements are met/unmet.
5. **Goal switching animation** — Smooth transition when switching goals.
6. **Goal history** — Track which goals the student has tried before.
