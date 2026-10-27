# BountyCode — Route Consolidation Plan

## Current Route Inventory

### Learning Routes (12+ duplicates)
- `/learn` → UnifiedHub
- `/learning-paths` → LearningPaths
- `/learn/:lessonId` → LessonView
- `/atom/:atomId` → AtomLesson
- `/atoms` → AtomWorlds
- `/concepts` → Concepts
- `/cific` → ConceptGraph
- `/cific/:conceptId` → ConceptFrame
- `/problems` → redirects to question bank
- `/question-bank` → QuestionBank
- `/question-bank/:questionId` → PracticeMode
- `/practice` → Practice
- `/practice-mode` → PracticeMode
- `/problem-of-the-day` → ProblemOfTheDay
- `/daily-drill` → DailyDrill
- `/daily-challenge` → DailyChallenge

### Progression Routes (5+ duplicates)
- `/journey` → JourneyPage
- `/levels` → redirects to /journey
- `/worlds` → redirects to /journey
- `/level-map` → LevelMap
- `/tower` → Tower

### Assessment Routes (7+ duplicates)
- `/mock-oa` → MockOA
- `/tcs-nqt` → TcsNqtSimulation
- `/exam-memory/submit` → ExamMemorySubmission
- `/coding` → CodingChallenge
- `/aptitude` → AptitudeTest
- `/system-design` → SystemDesign
- `/daily-challenge` → DailyChallenge
- `/daily-drill` → DailyDrill

### Career Routes (7+ duplicates)
- `/resume` → ResumeBuilder
- `/resume-studio` → ResumeStudio
- `/ats` → ATSOptimizer
- `/resume-ats` → ResumeATS
- `/career-profile` → CareerProfile
- `/company-tracks` → CompanyTracks
- `/prep-hub` → PrepHub

### Utility Routes (many duplicates)
- `/student-dashboard` → redirect /journey
- `/my-dashboard` → redirect /journey
- `/home` → redirect /journey
- `/hub` → redirect /journey
- `/compete` → redirect /mock-oa
- `/career` → redirect /career-profile
- `/prepare` → redirect /journey
- `/company-mocks` → redirect /mock-oa
- `/analytics` → redirect /skills
- `/learning` → redirect /learn
- `/prep-hub` → redirect /target
- `/atoms/worlds` → redirect /atoms
- `/role-select` → merge into onboarding
- `/find-my-level` → merge into onboarding
- `/diagnostic` → merge into onboarding
- `/onboarding` → merge into register flow

---

## Target Route Map

### WORLD — Learning Journey
```
/world → WorldMap (current JourneyPage simplified)
/world/:worldId → LevelMap (current LevelMap, cleaned)
/world/:worldId/concept/:conceptId → ConceptPlayer (golden flow)
```

**Replaces:** `/journey`, `/levels`, `/level-map`, `/tower`

### LAB — Learning Environment
```
/lab → UnifiedHub (single learning entry point)
/lab/concept/:conceptId → ConceptPlayer
/lab/lesson/:lessonId → LessonPlayer
/lab/project/:projectId → ProjectPlayer (future)
```

**Replaces:** `/learn`, `/learning-paths`, `/learn/:lessonId`, `/atom/:atomId`, `/atoms`, `/concepts`, `/cific`, `/cific/:conceptId`, `/problems`, `/question-bank`, `/question-bank/:questionId`, `/practice`, `/practice-mode`

### ARENA — Assessment & Challenge
```
/arena → ArenaHome (single assessment entry)
/arena/challenge/:challengeId → ChallengePlayer
/arena/boss/:bossId → BossBattle
/arena/mock-oa → MockOA (company filter inside)
/arena/contest/:contestId → ContestPlayer
```

**Replaces:** `/mock-oa`, `/tcs-nqt`, `/exam-memory/submit`, `/coding`, `/aptitude`, `/system-design`, `/daily-challenge`, `/daily-drill`, `/question-bank/:questionId`

### COMMAND CENTER — Readiness & Operations
```
/command → CommandCenter (Today + Readiness + Weaknesses + Applications)
/command/today → TodayPlan
/command/readiness → ReadinessPassport
/command/weaknesses → RepairHub
/command/applications → ApplicationTracker
/command/settings → Settings
```

**Replaces:** `/today`, `/skills`, `/readiness`, `/repair-hub`, `/history`, `/leaderboard`

### CAREER GATE — Resume, Interview, Application
```
/career → CareerGateHome
/career/resume → ResumeBuilder (includes studio, ats, resume-ats)
/career/interview → InterviewPrep
/career/company/:companyId → CompanyPrep
/career/applications → ApplicationTracker
```

**Replaces:** `/resume`, `/resume-studio`, `/ats`, `/resume-ats`, `/career-profile`, `/company-tracks`, `/prep-hub`

### PUBLIC & AUTH (unchanged)
```
/ → Landing
/login → Login
/register → Register
/forgot-password → ForgotPassword
/reset-password → ResetPassword
/onboarding → OnboardingQuest (simplified)
/pricing → Pricing
/free-trial → FreeTrial
/terms → Terms
/privacy → Privacy
/admin → AdminDashboard
```

---

## Navigation Restructure

### Top Nav (desktop)
```
BountyCode    World    Lab    Arena    Command    Career
```

### Bottom Nav (mobile)
```
World    Lab    Arena    Command    Career
```

**Removes:** Current 5-item nav (Journey/Practice/Target/Skills/Profile)
**Removes:** "More" dropdown with 4 groups
**Removes:** Duplicate nav items

---

## Component Consolidation

### Current Duplicates
- `JourneyPage` + `WorldMap` + `LevelMap` → `WorldMap` + `LevelMap` (simplified)
- `UnifiedHub` + `Concepts` + `ConceptGraph` + `ConceptFrame` → `UnifiedHub` + `ConceptPlayer`
- `Practice` + `QuestionBank` + `PracticeMode` → `ArenaHome` + `ChallengePlayer`
- `MockOA` + `TcsNqtSimulation` + `ExamMemorySubmission` → `MockOA` (with company filter)
- `TodayPage` + `Skills` + `ReadinessHeatmap` → `CommandCenter`
- `ResumeBuilder` + `ResumeStudio` + `ATSOptimizer` + `ResumeATS` + `CareerProfile` → `ResumeBuilder` (unified)
- `CompanyTracks` + `PrepHub` → `CompanyPrep` (inside Career)

### Keep As-Is
- `LessonPage` → move to `/lab/lesson/:lessonId`
- `SolveProblem` → integrate into `/arena/challenge/:challengeId`
- `RepairHub` → move to `/command/weaknesses`
- `Interview` + `InterviewSession` + `InterviewBooking` → move to `/career/interview`
- `MockOA` → move to `/arena/mock-oa`
- `Tower` → integrate into `/world` progression

---

## Implementation Order

### Step 1: Backend Canonical State
1. Create `LearnerGraph` service
2. Create unified `/api/v1/learner/state` endpoint
3. Migrate existing systems to read from LearnerGraph

### Step 2: Environment Shells (frontend)
1. Create `/world` shell
2. Create `/lab` shell
3. Create `/arena` shell
4. Create `/command` shell
5. Create `/career` shell

### Step 3: Route Migration
1. Add new routes
2. Update navigation
3. Add redirects from old routes
4. Test all entry points

### Step 4: Deprecation
1. Remove old routes (after redirect period)
2. Remove duplicate components
3. Clean up navigation
4. Remove dead code

### Step 5: Golden Flow Integration
1. Connect golden flow to canonical LearnerState
2. Ensure all 10 golden interactions work in new environment structure
3. Render-verify each environment

---

## Redirect Strategy

Old routes redirect to new routes for 3 months:

```typescript
const REDIRECTS = {
  // Learning
  "/learn": "/lab",
  "/learning-paths": "/lab",
  "/learn/:lessonId": "/lab/lesson/:lessonId",
  "/concepts": "/lab",
  "/cific": "/lab",
  "/cific/:conceptId": "/lab/concept/:conceptId",
  "/problems": "/arena",
  "/question-bank": "/arena",
  "/question-bank/:questionId": "/arena/challenge/:questionId",
  "/practice": "/arena",
  "/practice-mode": "/arena/challenge/:id",
  "/problem-of-the-day": "/command/today",
  "/daily-drill": "/arena",
  "/daily-challenge": "/arena",
  
  // Progression
  "/journey": "/world",
  "/levels": "/world",
  "/level-map": "/world",
  "/tower": "/world",
  
  // Assessment
  "/mock-oa": "/arena/mock-oa",
  "/tcs-nqt": "/arena/mock-oa",
  "/coding": "/arena",
  "/aptitude": "/arena",
  "/system-design": "/arena",
  
  // Career
  "/resume": "/career/resume",
  "/resume-studio": "/career/resume",
  "/ats": "/career/resume",
  "/resume-ats": "/career/resume",
  "/career-profile": "/career",
  "/company-tracks": "/career",
  "/prep-hub": "/career",
  
  // Dashboard
  "/today": "/command/today",
  "/skills": "/command/readiness",
  "/readiness": "/command/readiness",
  "/repair-hub": "/command/weaknesses",
  "/student-dashboard": "/world",
  "/my-dashboard": "/world",
  "/home": "/world",
  "/hub": "/world",
};
```

---

## What This Achieves

1. **One product, not 150 features**
2. **One state, not 15 data sources**
3. **One learner graph, not 5 overlapping systems**
4. **Five environments, not 90 routes**
5. **One motion language, not 20 visual themes**
6. **One teacher presence, not inconsistent guidance**
7. **One value proposition: "Your preparation system"**

The student experience becomes:

```text
Enter at /command
  ↓
See today's plan
  ↓
Enter /lab to learn
  ↓
Enter /arena to prove
  ↓
Enter /world to progress
  ↓
Enter /career to transition
  ↓
All data persists in one LearnerState
  ↓
System adapts everywhere
```

That is a **Personal Placement Operating System**.
