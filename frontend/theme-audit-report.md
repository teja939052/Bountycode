# Frontend Dark Theme Audit Report

## Summary
- **Total pages audited:** 95
- **Pages with issues:** 63
- **Clean pages:** 32
- **Total old-color instances found:** ~650+

---

## HIGH Priority — Core Pages (Most Traffic / Critical Flows)

### AdaptivePath.tsx — 60 issues
**File:** `D:\Project-Fremen\frontend\src\pages\AdaptivePath.tsx`
- Line 103: `<h1 className="text-2xl font-bold text-gray-800">`
- Line 110: `className="... bg-white/60 border border-gray-200 text-gray-600 ..."`
- Line 175: `className="... bg-gradient-to-r from-white/70 ... border border-gray-200/60 ..."`
- Line 213: `className="... bg-white/60 border border-gray-200 ... text-gray-700"`
- Line 227: `className="... bg-white/40 border border-gray-200/60 ..."`
- Line 236: `"bg-white shadow-sm text-gray-800 border border-gray-200"`
- Line 255: `className="... bg-white/60 backdrop-blur-sm border border-gray-200/60 ..."`
- Lines 294, 326, 382, 445, 475, 498, 546, 604: Repeated `bg-white/60 border-gray-200/60` card patterns
- Line 368: `bg-white/60 border-gray-200 text-gray-700`
- Line 417: `text-gray-600 bg-gray-50`
- Lines 446, 452, 499, 522: Multiple `text-gray-800` headings
- Lines 563, 566, 621, 624: Repeated body text `text-gray-600`

### ProjectGenerator.tsx — 53 issues
**File:** `D:\Project-Fremen\frontend\src\pages\ProjectGenerator.tsx`
- Line 245: `border-b border-gray-200`
- Line 252: `"bg-white border border-b-white border-gray-200 text-brand-sky"`
- Line 266: `border border-gray-200 bg-white p-6`
- Line 280: `rounded-full border border-gray-200 bg-gray-50 ... text-gray-500`
- Line 322, 358, 364, 449, 484, 490, 599, 657, 663, 691: Repeated `bg-white border-gray-200` card/container patterns
- Line 373, 376: `border-gray-200 text-gray-600 hover:bg-gray-50`
- Line 383: `border-t border-gray-100 bg-gray-50/70`
- Line 394: `border-r border-gray-100 bg-gray-50/50`
- Line 403: `text-gray-600 hover:bg-gray-100`
- Line 413, 434: `border-gray-100 bg-gray-50/30`
- Line 415: `rounded bg-gray-100 ... text-gray-500`
- Line 496: `text-gray-800`
- Line 513, 529, 580: `text-gray-600` body text
- Line 549, 665, 674, 680, 688, 695: Multiple `text-gray-600/700/800` labels and content

### QuestionBank.tsx — 52 issues
**File:** `D:\Project-Fremen\frontend\src\pages\QuestionBank.tsx`
- Line 371: `bg-white/15` (should be `bg-brand-primary/15` or `bg-surface-card`)
- Line 383: `bg-white/15`
- Line 386: `bg-white text-indigo-700` (button — should use brand colors)
- Line 437: `bg-gray-200 dark:bg-gray-700` (skeleton)
- Line 471: `border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800`
- Line 489: Same select pattern as 471
- Line 541: `bg-gray-100 dark:bg-gray-800 text-gray-500`
- Line 558: `border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800`
- Line 565: `bg-gray-100 dark:bg-gray-800 text-gray-600`
- Line 576: `bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700`
- Line 584: `text-gray-600 dark:text-gray-400 hover:bg-gray-50`
- Line 604: `bg-gray-100 dark:bg-gray-800 text-gray-600 hover:bg-gray-200`
- Line 618-653: Six consecutive selects all using `bg-white dark:bg-gray-800 border-gray-300`
- Line 672: `bg-gray-100 dark:bg-gray-800 text-gray-600`
- Line 685-688: Three skeleton divs `bg-gray-200 dark:bg-gray-700`
- Line 712: `border-gray-200 bg-white hover:border-brand-sky/30`
- Line 784, 806, 816: `hover:bg-gray-100 text-gray-500`
- Line 831: `bg-gray-200 dark:bg-gray-700`
- Line 842: `bg-white dark:bg-gray-900`
- Line 851: `bg-gray-100 dark:bg-gray-800 text-gray-600`

### Dashboard.tsx — 12 issues
**File:** `D:\Project-Fremen\frontend\src\pages\Dashboard.tsx`
- Line 167: `bg-white/60 blur-sm` (should use `bg-brand-primary/10` or similar)
- Line 455: `bg-white/0 group-hover:bg-brand-gold/10` (good usage but `bg-white/0` is odd)
- Line 734: `border-white/5 bg-white/5` (acceptable but should migrate to `bg-surface-base`)
- Line 754: `bg-white/5 border-white/5`
- Line 756: `bg-white/5 text-slate-400`
- Lines 829, 856, 1069, 1078, 1087, 1096: Repeated `border-white/5 bg-white/5` card patterns

### InterviewBooking.tsx — 23 issues
**File:** `D:\Project-Fremen\frontend\src\pages\InterviewBooking.tsx`
- Line 55: `cancelled: "bg-gray-500/10 text-gray-400 border-gray-500/30"`
- Lines 277-316, 336, 563, 611, 683: Heavy use of `bg-white/5 border-white/10` (should be `bg-surface-card border-brand-primary/10`)
- Lines 346, 380, 392, 405, 422, 436, 452: Input fields using `bg-white/5 text-text-primary`
- Line 364: `border-white/10 bg-white/5 text-text-secondary`
- Lines 472, 541: `border-white/10 bg-white/5 text-text-secondary`
- Line 686: `bg-white/5 border-white/10`
- Lines 713, 736: `border-white/10 bg-white/5 text-text-secondary`

### ATSOptimizer.tsx — 12 issues
**File:** `D:\Project-Fremen\frontend\src\pages\ATSOptimizer.tsx`
- Line 107: `text-gray-600`
- Line 120: `border-gray-200`
- Line 125: `text-gray-600`
- Line 135, 191, 247, 261, 276, 289: Repeated `bg-gray-50 border-gray-200` cards
- Line 318: `text-gray-700 bg-gray-50 border-gray-200`
- Line 341: `text-gray-600`

### CoverLetter.tsx — 7 issues
**File:** `D:\Project-Fremen\frontend\src\pages\CoverLetter.tsx`
- Line 97: `border-gray-200`
- Line 118, 126: `border-gray-200 text-gray-500`
- Line 136: `bg-gray-50 border-gray-200`
- Lines 184, 240: `text-gray-700 bg-gray-50 border-gray-200`

### DailyChallenge.tsx — 16 issues
**File:** `D:\Project-Fremen\frontend\src\pages\DailyChallenge.tsx`
- Line 288: `border-gray-200 hover:border-gray-300`
- Line 299: `border-gray-200 text-text-light hover:bg-gray-50`
- Line 417: `bg-white border-gray-200 text-text-light`
- Line 622: `border-gray-200 resize-none`
- Line 625: `border-gray-200 text-text-light hover:bg-gray-50`
- Line 726: `bg-gray-50 border-gray-200`

### Landing.tsx — 6 issues
**File:** `D:\Project-Fremen\frontend\src\pages\Landing.tsx`
- Line 112: `border-white/10 bg-white/10 text-white`
- Line 116: `border-white/10 bg-white/10 text-white`
- Line 156: `border-white/20 bg-white/10`
- Line 173: `border-white/10 bg-white/10`
- Line 195: `border-white/20 bg-white/10 text-slate-200`
- Line 202: `border-white/10 bg-white/10`

---

## MEDIUM Priority — Secondary Pages

### Dungeons.tsx — 26 issues
**File:** `D:\Project-Fremen\frontend\src\pages\Dungeons.tsx`
- Heavy use of `bg-emerald-500/10`, `border-emerald-500/30`, `text-emerald-400/300` throughout
- Lines 488, 526, 587, 774, 792, 822: Multiple emerald badge/lock patterns

### TeamCompetitions.tsx — 24 issues
**File:** `D:\Project-Fremen\frontend\src\pages\TeamCompetitions.tsx`
- Lines 141, 166, 219, 248, 279: `bg-white border-gray-200` cards
- Lines 148, 158: `border-gray-300` inputs
- Lines 178, 182, 186: `bg-gray-50`
- Lines 221, 250: `bg-gray-50` table headers
- Lines 223-226, 252-255, 237, 263: `text-gray-600` table headers/cells

### CareerProfile.tsx — 23 issues
**File:** `D:\Project-Fremen\frontend\src\pages\CareerProfile.tsx`
- Line 134: `bg-gray-100 dark:bg-gray-800 rounded-lg`
- Line 190: `text-gray-600 dark:text-gray-400 hover:bg-gray-50`
- Line 315: `border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800`
- Line 402: `bg-gray-50 dark:bg-gray-700/30`
- Line 417: `bg-gray-50 dark:bg-gray-700/30`
- Line 519: `bg-gray-200 dark:bg-gray-700 text-gray-600`

### CompanyMocks.tsx — 17 issues
**File:** `D:\Project-Fremen\frontend\src\pages\CompanyMocks.tsx`
- Line 215: `bg-white dark:bg-gray-800 rounded-lg p-4 border-gray-200`
- Line 296: `border-gray-200 dark:border-gray-700`
- Line 308: `border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800`

### BattleArena.tsx — 17 issues
**File:** `D:\Project-Fremen\frontend\src\pages\BattleArena.tsx`
- Line 546: `bg-gray-100 text-gray-600`

### Analytics.tsx — 16 issues
**File:** `D:\Project-Fremen\frontend\src\pages\Analytics.tsx`
- Line 76: `text-gray-600`
- Line 121, 142: `text-gray-600`
- Lines 168, 172, 176: `text-gray-600`
- Lines 219-221: `text-gray-600`
- Line 247: `text-gray-700`
- Line 253: `text-gray-600`
- Line 206: `border-gray-200`

### GameEvents.tsx — 14 issues
**File:** `D:\Project-Fremen\frontend\src\pages\GameEvents.tsx`
- Lines 206, 224, 249, 365, 417, 433-434, 458, 474, 478, 483, 503, 530, 549: `bg-white/5 border-white/10` patterns

### Showcase.tsx — 13 issues
**File:** `D:\Project-Fremen\frontend\src\pages\Showcase.tsx`
- Line 15: `border-emerald-500/30 bg-emerald-500/10 text-emerald-400` (python)
- Line 19: `border-blue-500/30 bg-blue-500/10 text-blue-400` (cpp)
- Line 21: `border-cyan-500/30 bg-cyan-500/10 text-cyan-400` (go)
- Line 110: `text-emerald-400`
- Line 119: `bg-gradient-to-r from-emerald-500/20 ...`
- Line 140: `border-white/10 bg-white/5`
- Lines 152, 171, 199, 253, 263, 296, 310, 321, 331, 343, 368: Various `bg-white/5`, `text-slate-400/500`, `border-white/10`

### CareerRpg.tsx — 13 issues
**File:** `D:\Project-Fremen\frontend\src\pages\CareerRpg.tsx`
- Line 49: `border-emerald-500/30 bg-emerald-500/10 text-emerald-300`
- Line 175: `text-emerald-400`
- Line 185: `bg-gradient-to-r from-emerald-500/20 to-indigo-500/20 border-emerald-500/40 text-emerald-300`
- Lines 226, 238, 265-266: `text-emerald-400/300`
- Line 321: `bg-emerald-400 text-slate-950`
- Line 338: `text-emerald-400`

### ShowcaseDetail.tsx — 12 issues
**File:** `D:\Project-Fremen\frontend\src\pages\ShowcaseDetail.tsx`
- Line 213: `border-emerald-500/30 bg-emerald-500/10 text-emerald-400`
- Line 228: `border-emerald-500/50 bg-emerald-500/15 text-emerald-300`
- Lines 144, 173, 180, 229, 246, 248, 261, 271, 280, 311: `bg-white/5`, `border-white/10`, `text-slate-300/400`

### LanguageJourney.tsx — 12 issues
**File:** `D:\Project-Fremen\frontend\src\pages\LanguageJourney.tsx`
- Line 17: `text-gray-600`
- Line 168: `bg-white/5 text-gray-600`
- Lines 294, 295, 296, 298, 330: `bg-white/[0.01]`, `text-gray-600`

### PracticeMode.tsx — 12 issues
**File:** `D:\Project-Fremen\frontend\src\pages\PracticeMode.tsx`
- Line 86: `text-gray-300 dark:text-gray-600`
- Line 117: `bg-gray-100 dark:bg-gray-700 text-gray-600`
- Line 155: `text-gray-700 dark:text-gray-300`
- Line 173: `text-gray-700 dark:text-gray-300`
- Line 181: `border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800`
- Lines 239, 246, 260, 272, 279, 283: `text-gray-600`
- Line 302: `bg-gray-100 dark:bg-gray-800 text-gray-600`

### Predictor.tsx — 11 issues
**File:** `D:\Project-Fremen\frontend\src\pages\Predictor.tsx`
- Line 75: `text-gray-600`
- Line 82: `text-gray-700`
- Line 88: `border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800`
- Line 108: Same select pattern
- Line 173: `bg-gray-200 dark:bg-gray-700`
- Line 170: `text-gray-600`
- Line 206: `text-gray-600`
- Line 209: `text-gray-700`
- Line 215: `text-gray-600`
- Line 225: `text-gray-600`

### RankProfile.tsx — 11 issues
**File:** `D:\Project-Fremen\frontend\src\pages\RankProfile.tsx`
- Line 103: `border-white/60 bg-white/80`
- Line 111: `bg-gray-200`
- Line 128: `border-white/60 bg-white/80`
- Line 142: `border-white/60 bg-gray-50/50`
- Line 160: `border-white/60 bg-white/80`
- Line 176: `bg-gray-50 border-gray-200`
- Line 178: `hover:bg-gray-50`
- Line 184: `bg-gray-200 text-gray-700`
- Line 186: `bg-gray-100 text-gray-500`
- Line 229: `border-white/60 bg-white/80`
- Line 245: `border-white/60 bg-white/50`

### SeasonalEvents.tsx — 11 issues
**File:** `D:\Project-Fremen\frontend\src\pages\SeasonalEvents.tsx`
- Line 65: `border-gray-200`
- Line 108: `bg-white border rounded-xl ... border-gray-200`
- Line 157: `bg-white border rounded-xl ... border-gray-200`
- Line 178: `bg-white border-gray-200`
- Line 180: `bg-gray-50`
- Line 190: `hover:bg-gray-50`
- Lines 182-185, 193: `text-gray-600`

### AdminDashboard.tsx — 11 issues
**File:** `D:\Project-Fremen\frontend\src\pages\AdminDashboard.tsx`
- Line 120: `border-emerald-500/30 text-emerald-400 bg-emerald-500/10`
- Line 178: `text-gray-600`
- Line 197: `text-gray-600`
- Line 201: `text-gray-600`
- Line 238: `border-emerald-500/20 bg-emerald-500/10 text-emerald-300`
- Line 256: `border-emerald-500/20 bg-emerald-500/5`

### CollectionEvents.tsx — 11 issues
**File:** `D:\Project-Fremen\frontend\src\pages\CollectionEvents.tsx`
- Lines 190, 257, 265, 337, 522: Heavy use of `border-emerald-500/40 bg-emerald-500/10 text-emerald-300/400`

### PlacementDrives.tsx — 11 issues
**File:** `D:\Project-Fremen\frontend\src\pages\PlacementDrives.tsx`
- Line 57: `text-gray-600`
- Line 65: `text-gray-600`
- Line 89: `bg-gray-100 text-gray-600`
- Line 101-102: `bg-gray-200`
- Line 108: `text-gray-300`
- Line 125: `bg-gray-100 text-gray-600`
- Line 134: `text-gray-600`
- Line 138: `text-gray-700`
- Lines 144, 155: `text-gray-600`

### StudyLibrary.tsx — 11 issues
**File:** `D:\Project-Fremen\frontend\src\pages\StudyLibrary.tsx`
- Line 23: `text-emerald-400 border-emerald-500/30 bg-emerald-500/10`
- Line 121: `border-emerald-400/40 bg-emerald-500/10 text-emerald-300`
- Line 134: `text-emerald-400`
- Line 150: `text-emerald-400` / `text-amber-400`
- Line 174: `border-white/10 bg-black/50 text-emerald-300`
- Line 175: `border-emerald-400/20 bg-black/50 text-emerald-300`
- Line 261: `border-white/10 bg-white/[0.02] text-emerald-300`

### ApplicationTracker.tsx — 11 issues
**File:** `D:\Project-Fremen\frontend\src\pages\ApplicationTracker.tsx`
- Line 12: `bg-gray-100 text-gray-700`
- Line 13: `bg-blue-100 text-blue-700` / `bg-emerald-100 text-emerald-700`
- Line 18: `bg-emerald-100 text-emerald-700`
- Line 109: `text-gray-600`
- Line 122: `text-gray-600`
- Line 150: `text-gray-400 hover:text-gray-600`
- Lines 156-168: `text-gray-700`
- Line 184: `text-gray-300`

### ProblemOfTheDay.tsx — 10 issues
**File:** `D:\Project-Fremen\frontend\src\pages\ProblemOfTheDay.tsx`
- Line 82: `bg-gray-100 dark:bg-slate-800`
- Line 84: `bg-white dark:bg-slate-700 text-gray-900`
- Line 97: `text-gray-900 bg-gray-50 text-gray-500`
- Line 105: `bg-gray-50 border-gray-200 text-gray-700`
- Line 112: `bg-gray-50 text-green-600`
- Line 113: `bg-gray-50 border-gray-200 text-gray-700`
- Line 124: `bg-gray-50`
- Line 125: `bg-gray-100 text-gray-700` / `bg-gray-100 text-gray-500`

### LessonView.tsx — 9 issues
**File:** `D:\Project-Fremen\frontend\src\pages\LessonView.tsx`
- Line 65: `text-gray-600`
- Line 123: `bg-white/5 border-white/10 text-gray-300`
- Line 127: `bg-white/5 border-white/10 text-gray-500`
- Line 347: `text-gray-600`
- Line 513: `bg-white/5 border-white/10 text-gray-300`
- Line 554: `border-white/5 bg-white/[0.02]`
- Line 641: `border-white/5 bg-white/[0.02]`
- Line 686: `bg-white/5 border-white/10 text-gray-300 hover:bg-gray-100`
- Line 755: `bg-white/5 border-white/10 text-gray-400`

### AdminContent.tsx — 9 issues
**File:** `D:\Project-Fremen\frontend\src\pages\AdminContent.tsx`
- Line 22: `bg-emerald-500/10 text-emerald-400 border-emerald-500/30`
- Line 75: `bg-emerald-500/10 text-emerald-400 border-emerald-500/30`
- Line 234: `text-gray-600`
- Lines 334, 441: `bg-emerald-500/10 border-emerald-500/20`
- Line 477: `bg-emerald-500/90 hover:bg-emerald-500 text-white`
- Line 637: `bg-emerald-500/90 hover:bg-emerald-500 text-white`

### WorldMap.tsx — 8 issues
**File:** `D:\Project-Fremen\frontend\src\pages\WorldMap.tsx`
- Line 107: `text-slate-600`
- Lines 218, 222, 226, 231, 272, 310, 341: `text-slate-600` / `text-slate-400`

### DSAVisualizer.tsx — 8 issues
**File:** `D:\Project-Fremen\frontend\src\pages\DSAVisualizer.tsx`
- Line 75: `bg-primary-50 bg-gray-50 border-gray-200 text-gray-600`
- Line 106: `bg-gray-200 hover:bg-gray-300 text-gray-700`
- Line 113: `bg-gray-100 text-gray-600`

### LearningHub.tsx — 8 issues
**File:** `D:\Project-Fremen\frontend\src\pages\LearningHub.tsx`
- Line 104: `bg-gray-100`
- Line 137: `bg-gray-50`
- Lines 143, 146: `bg-gray-200 text-gray-600` / `bg-gray-100 text-gray-500`

### CardCollection.tsx — 8 issues
**File:** `D:\Project-Fremen\frontend\src\pages\CardCollection.tsx`
- Line 16-22: Multiple `hover:bg-gray-50 text-gray-400` patterns across rarity types

### MyProgress.tsx — 7 issues
**File:** `D:\Project-Fremen\frontend\src\pages\MyProgress.tsx`
- Line 63: `text-gray-600`
- Lines 99, 128: `text-gray-700`
- Line 102, 131: `bg-gray-200`
- Line 154: `bg-gray-50`
- Line 205: `text-gray-300`

### CoverLetter.tsx — 7 issues
**File:** `D:\Project-Fremen\frontend\src\pages\CoverLetter.tsx`
- Lines 184, 240: `text-gray-700 bg-gray-50 border-gray-200`
- Line 97: `border-gray-200`
- Lines 118, 126: `border-gray-200 text-gray-500`
- Line 136: `bg-gray-50 border-gray-200`

### Topics.tsx — 7 issues
**File:** `D:\Project-Fremen\frontend\src\pages\Topics.tsx`
- Line 104-105: `bg-gray-200`
- Line 134: `text-gray-600`
- Line 151: `text-gray-600`
- Line 156, 222: `bg-gray-200`
- Line 254: `text-gray-300`

### TopicProblems.tsx — 7 issues
**File:** `D:\Project-Fremen\frontend\src\pages\TopicProblems.tsx`
- Line 59-60: `bg-gray-200`
- Line 90: `text-gray-600`
- Line 104: `bg-gray-200`
- Line 159: `bg-gray-100 text-gray-500`
- Line 210: `text-gray-300`

### AptitudeTest.tsx — 6 issues
**File:** `D:\Project-Fremen\frontend\src\pages\AptitudeTest.tsx`
- Line 186: `hover:border-gray-200`
- Line 210: `bg-gray-100 border-gray-200 text-gray-500`
- Line 243: `bg-gray-100 border-gray-200`
- Line 278: `border-gray-200 hover:border-gray-500 text-gray-400`
- Line 309: `text-gray-600`
- Line 349: `text-gray-600`

### LearningModules.tsx — 6 issues
**File:** `D:\Project-Fremen\frontend\src\pages\LearningModules.tsx`
- Line 84: `border-white/60 bg-white/80`
- Line 113: `bg-gray-100`
- Lines 162-163: `bg-gray-50 border-gray-100 text-text-light`
- Line 189: `[&_code]:bg-gray-100 [&_pre]:bg-gray-900`

### Tournaments.tsx — 6 issues
**File:** `D:\Project-Fremen\frontend\src\pages\Tournaments.tsx`
- Lines 115, 155, 203: `bg-white border-gray-200`
- Lines 122, 127: `border-gray-300`
- Line 144: `border-gray-300`

### Economy.tsx — 6 issues
**File:** `D:\Project-Fremen\frontend\src\pages\Economy.tsx`
- Line 116: `bg-gray-100 text-gray-700`
- Line 122: `bg-gray-100 text-gray-700`
- Line 133: `bg-white border-gray-200`
- Line 139: `bg-gray-100 text-gray-600`
- Line 170: `bg-white border-gray-200`
- Line 182: `bg-gray-50 border-gray-200`

### ResetPassword.tsx — 6 issues
**File:** `D:\Project-Fremen\frontend\src\pages\ResetPassword.tsx`
- Line 46: `bg-gray-50`
- Lines 65, 78, 92, 106: `border-gray-300 text-gray-900`

### ReferralGamification.tsx — 6 issues
**File:** `D:\Project-Fremen\frontend\src\pages\ReferralGamification.tsx`
- Lines 88, 93, 98: `bg-white border-gray-200`
- Line 117: `bg-white border-gray-200`
- Line 75: `bg-white/20`
- Line 80: `bg-white/20`

---

## Lower Priority — Minor Issues (1–5 instances)

| File | Count | Key Issues |
|------|-------|------------|
| FreeTrial.tsx | 5 | `bg-white/5`, `text-gray-500`, `text-cyan-400`, `text-emerald-400` |
| PersonalDashboard.tsx | 5 | `text-gray-600`, `bg-white/20` |
| SkillTrees.tsx | 5 | `bg-white border-gray-200`, `text-gray-600`, `bg-gray-200` |
| RetentionAdmin.tsx | 5 | `bg-white/5`, `text-slate-300`, `border-white/10` |
| AchievementChains.tsx | 5 | `bg-white border-gray-200`, `text-gray-600` |
| Enterprise.tsx | 5 | `text-gray-600`, `text-gray-700`, `bg-gray-300` |
| Leaderboard.tsx | 4 | `text-gray-500`, `text-gray-600` |
| OnboardingQuest.tsx | 4 | `bg-white/5`, `border-white/10` |
| ResumeATS.tsx | 4 | `text-gray-600`, `text-gray-700` |
| CompareVisualizer.tsx | 4 | `text-slate-600`, `text-cyan-400` |
| MonthlyContests.tsx | 3 | `text-gray-600`, `text-gray-500` |
| ForgotPassword.tsx | 3 | `border-gray-300 text-gray-900` |
| DailyDrill.tsx | 3 | `text-gray-600` |
| CodePlayground.tsx | 3 | `bg-slate-100 border-slate-200`, `text-emerald-600` |
| MockOA.tsx | 3 | `text-gray-600`, `bg-space-panel` |
| AIMentor.tsx | 3 | `text-slate-600` |
| InterviewSession.tsx | 2 | `text-gray-600` |
| CodingChallenge.tsx | 2 | `bg-gray-50 border-gray-200` |
| Scrims.tsx | 1 | `text-emerald-500` |
| StudyGroups.tsx | 1 | `text-gray-600` |
| PwaSetup.tsx | 1 | `bg-white shadow` |
| BattlePass.tsx | 1 | `bg-slate-800 text-slate-600` |
| ChallengePacks.tsx | 1 | `text-slate-700` |
| CompanyPrep.tsx | 1 | `bg-blue-500/10 text-blue-400` |
| MyAssignments.tsx | 1 | `text-gray-600` |
| IndianPlacement.tsx | 1 | `text-gray-500 hover:bg-gray-50` |
| HealthDashboard.tsx | 1 | `text-gray-600` |
| LanguageLearning.tsx | 1 | `text-gray-600` |
| Register.tsx | 1 | `text-gray-600` |
| CommandCenter.tsx | 1 | `text-slate-600` |
| InterviewFeedback.tsx | 1 | `text-slate-600` |
| Community.tsx | 1 | `text-gray-600` |
| History.tsx | 1 | `text-gray-600` |

---

## Clean Pages (No Old Theme Colors Found)
32 pages have no instances of the flagged old color classes:
CampusConnect, CampusPulse, CampusWars, Chat, CollegeNetwork, Compiler, DSAFingerprint, GuildCastle, Interview, InterviewReplay, Journey, LearningJourneys, Login, LuckyWheel, Merchant, Newspaper, NotFound, Pricing, Referral, ResumeBuilder, SalaryBenchmark, SalaryNegotiation, Settings, ShareCard, SolveProblem, SRSMastery, SteamProfile, StudentDashboard, SystemDesign, Timeline, TowerDashboard, TrendingChallenges

---

## Migration Notes

1. **bg-white** in dark theme contexts should become `bg-surface-card` or `bg-white/5` (if intentionally translucent)
2. **bg-gray-50/100/200** should become `bg-surface-base`, `bg-surface-card`, or `bg-brand-primary/5` depending on intent
3. **text-gray-600/700/800** should become `text-brand-secondary`, `text-brand-muted`, or `text-white`
4. **border-gray-200/300** should become `border-brand-primary/10` or `border-brand-primary/20`
5. **bg-emerald-500/10**, **bg-blue-500/10** used as primary accents should be evaluated — if they represent status, they can stay; if they represent primary UI chrome, migrate to `bg-brand-primary/10`
6. Auth pages (Login, Register, ForgotPassword, ResetPassword) intentionally use light backgrounds — these may be exempt from dark migration if they serve as light-mode auth flows
