# BountyCode — Product Map

## Primary Learner Journey

```
ENTRY
  ↓
ONBOARDING
  ↓
TARGET
  ↓
TODAY
  ↓
LEARN
  ↓
PRACTICE
  ↓
REPAIR
  ↓
MASTER
  ↓
ASSESS
  ↓
PREPARE
  ↓
INTERVIEW
  ↓
CAREER
```

Every feature has one place in this system.

---

## Navigation Architecture

### Primary Entry Points
- `/` — Landing (public)
- `/register` — Account creation
- `/onboarding` — Goal and target setting
- `/today` — Daily mission center
- `/journey` — Core progression map

### Learning Surfaces
- `/journey` — Primary learning progression (replaces `/levels`, `/worlds`, `/world-map`)
- `/lesson/:slug` — Individual lesson experience
- `/learn` — Learning hub (consolidated)

### Practice Surfaces
- `/practice` — Practice mode entry
- `/solve/:id` — Problem solver (LeetCode-style)
- `/compiler` — Standalone code execution

### Assessment Surfaces
- `/mock-oa` — Mock online assessment
- `/mission/:id` — Universal mission shell (bosses, challenges)
- `/mission/:id/result` — Mission results

### Repair Surfaces
- `/repair-hub` — Repair mission dashboard
- `/mistakes` — Mistake book

### Interview Surfaces
- `/interview` — Interview simulator selection
- `/interview/:id` — Live interview session
- `/interview-booking` — Mock interview scheduling

### Company Surfaces
- `/company-tracks` — Company preparation hub
- `/tracks/:company` — Single company track

### Career Surfaces
- `/resume` — Resume builder/analyzer
- `/cover-letter` — Cover letter generator
- `/salary` — Salary benchmark/negotiation

### Gamification Surfaces
- `/tower` — Tower dashboard (consolidated gamification view)

### Analytics Surfaces
- `/readiness` — Readiness heatmap (primary)
- `/evidence` — Evidence dashboard (detailed)
- `/skills` — Skills overview

### Admin Surfaces
- `/admin` — Admin dashboard

---

## Feature Consolidation Plan

### Learning Surfaces — MERGE INTO `/journey`
| Current | Action | Reason |
|---------|--------|--------|
| `/levels` | Remove | Redundant with `/journey` map |
| `/world-map` | Remove | Redundant with `/journey` world view |
| `/worlds` | Remove | Redundant with `/journey` world progression |
| `/curriculum-hub` | Remove | Redundant with `/journey` |
| `/atom-worlds` | Remove | Experimental, not canonical |
| `/learning-modules` | Keep as `/learn` | Module listing has value |
| `/lesson-player` | Keep as `/lesson/:slug` | Canonical lesson experience |

### Gamification Surfaces — CONSOLIDATE INTO `/tower`
| Current | Action | Reason |
|---------|--------|--------|
| `/forest-journey` | Merge into `/tower` | Redundant progression view |
| `/voyage-path` | Merge into `/tower` | Redundant with journey map |
| `/world-summary` | Merge into `/tower` | World completion belongs in tower |
| `/streak-constellation` | Merge into `/tower` | Streak display belongs in tower |
| `/anime-cards` | Remove | Experimental, not canonical |
| `/reward-showcase` | Merge into `/tower` | Rewards belong in tower |
| `/badge-ceremony` | Merge into `/tower` | Badge display belongs in tower |

### Career Surfaces — CONSOLIDATE INTO CAREER HUB
| Current | Action | Reason |
|---------|--------|--------|
| `/resume-builder` | Merge into `/resume` | Single resume surface |
| `/resume-studio` | Merge into `/resume` | Redundant |
| `/resume-ats` | Merge into `/resume` | ATS is a mode, not a page |
| `/ats-optimizer` | Merge into `/resume` | Part of resume flow |
| `/career-profile` | Merge into `/resume` | Career data belongs in profile |
| `/application-tracker` | Keep separate | Distinct workflow |
| `/placement-calendar` | Evaluate | May merge into company tracks |

### Interview Surfaces — CONSOLIDATE
| Current | Action | Reason |
|---------|--------|--------|
| `/interview-terminal` | Remove | Legacy, replaced by `/interview` |
| `/interview-replay` | Merge into `/interview/:id` | Replay is a mode |
| `/mentor` | Merge into `/interview` | AI mentor is part of interview prep |
| `/predictor` | Merge into `/readiness` | Prediction belongs in readiness |
| `/readiness-heatmap` | Keep as `/readiness` | Primary readiness view |
| `/evidence-dashboard` | Keep as `/evidence` | Detailed view |

---

## Feature Survival Test Results

### KEEP (Core Loop)
- `/today` — Daily mission center
- `/journey` — Core progression
- `/lesson/:slug` — Lesson experience
- `/solve/:id` — Problem solving
- `/mock-oa` — Assessment
- `/mission/:id` — Universal mission shell
- `/repair-hub` — Repair loop
- `/mistakes` — Mistake book
- `/tower` — Gamification hub
- `/interview` — Interview prep
- `/company-tracks` — Company prep
- `/resume` — Career tools
- `/readiness` — Readiness view

### MERGE (Consolidate)
- All duplicate learning surfaces → `/journey`
- All duplicate gamification surfaces → `/tower`
- All duplicate resume surfaces → `/resume`
- Interview surfaces → `/interview`
- Readiness surfaces → `/readiness`

### REWORK (Needs Redesign)
- `/onboarding` — Needs stronger goal commitment
- `/world-map` — Needs spatial meaning, not just cards
- `/lesson/:slug` — Needs teaching presence, not phase checklist
- `/solve/:id` — Needs unified interaction language
- `/repair-hub` — Needs failure-to-mastery loop
- `/tower` — Needs meaningful progression, not just stats
- `/mock-oa` — Needs boss battle feel, not just exam
- `/company-tracks` — Needs destination meaning, not directory
- `/readiness` — Needs evidence narrative, not just heatmap

### HIDE (Not Primary)
- `/admin` — Admin only
- `/community` — Evaluate after core loop is solid
- `/contests` — Evaluate after core loop is solid

### REMOVE (Dead Weight)
- Legacy dashboards (`/dashboard`, `/home`, `/student-dashboard`)
- Experimental pages (`/atom-worlds`, `/anime-cards`)
- Duplicate learning surfaces
- Duplicate gamification surfaces

---

## Navigation Hierarchy

### Primary (Bottom Nav)
1. Today — Daily mission center
2. Journey — Core progression
3. Practice — Problem solving
4. Tower — Gamification
5. Profile — Settings and career

### Secondary (In-Context)
- Lesson phases (within `/journey` or `/lesson/:slug`)
- Mission steps (within `/mission/:id`)
- Interview flow (within `/interview`)
- Company tracks (within `/company-tracks`)

### Tertiary (Settings/Admin)
- Profile settings
- Admin dashboard
- Help/support

---

## Information Architecture Principles

1. **One destination per learner goal**
   - "What should I do today?" → `/today`
   - "Where am I going?" → `/journey`
   - "How do I practice?" → `/practice`
   - "How am I doing?" → `/tower`

2. **Progressive disclosure**
   - Show minimum required NOW
   - Reveal complexity as competence increases

3. **Spatial over list**
   - Worlds feel like places, not curriculum units
   - Progression feels like movement, not checklist

4. **Single source of truth**
   - One learning surface
   - One gamification surface
   - One career surface
   - One interview surface
