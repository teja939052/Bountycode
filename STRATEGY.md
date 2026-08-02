# PlacementPro — Codedex-Style Gamification Strategy

## Core Philosophy
Transform placement preparation into an addictive RPG experience, optimized for both **Indian campus hiring** (mass recruiters, aptitude tests) and **US tech hiring** (FAANG, behavioral, system design).

---

## 1. Platform Core Architecture

### Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite 5 + Tailwind 3 + Framer Motion |
| Code Editor | Monaco Editor |
| Backend | FastAPI (Python 3.11+) |
| Database | MongoDB Atlas (Motor async) |
| AI | OpenRouter → Gemini 2.0 Flash |
| Sandbox | Piston API (Dockerized code execution) |
| Payments | PayPal REST API |
| Auth | JWT (httpOnly cookie) |
| Resume | PyMuPDF + python-docx |
| Real-time | WebSockets (future) |

### Key Differentiators
- **Codedex-style RPG gamification** (pixel art, trading cards, learning journeys, XP/levels/streaks/badges)
- **Dual market** (India + US) with localized content
- **Adaptive learning** powered by DSA Fingerprint skill graph
- **5,950+ lessons** across 7 languages × 50 levels

---

## 2. The Student Journey (RPG Progression)

```
Level 1: "The Rookie Sandbox"   → Daily Quests (DSA)
Level 10: "The Core Realm"      → Unlock Guilds (College Cohorts)
Level 30: "The Placement Gate"  → Boss Fights (Mock Interviews)
```

### Roadmap as Fantasy Map
- Syllabus mapped as chronological regions
  - Array Archipelago
  - The Recursion Valley
  - Dynamic Programming Dungeon
  - System Design Citadel
- Players clear Quests to reveal fog-of-war

### XP & Levels
- Every passed test case awards XP
- Streaks (5+ days) multiply XP
- Level-up triggers screen-wide celebration effects

### Inventory & Shop
- Virtual currency: "Bits" or "Tokens" earned from assignments
- Spend to unlock: profile avatars, custom IDE themes, "Hint Scrolls"
- Mystery boxes with random rewards

### Boss Fights (Milestone Assessments)
- Timed, proctored mock tests mimicking real company rounds
- Plagiarism monitoring
- Company-specific (Infosys Digital, TCS NQT, FAANG)

---

## 3. India-Specific Content Framework

### Quest Line A: Technical Mastery (Product-Based/FAANG)
- DSA: Trees, Graphs, Sliding Window, Two-Pointers
- System Design & CS Core: OOPs, DBMS/SQL, Computer Networks

### Quest Line B: Mass Recruiter Aptitude (Service-Based)
- Quantitative: Percentages, Profit/Loss, Time/Work, Speed/Distance
- Logical Reasoning: Series, Coding-Decoding, Blood Relations, Syllogisms
- Verbal: Synonyms, Antonyms, Grammar, Spelling
- Pseudocode & Automata: Dry-run code debugging challenges

### Company Tags
- Tag questions with #TCS-Digital, #Infosys-SP, #Amazon, etc.
- Banner on solve: "You just defeated a challenge used by Accenture!"

---

## 4. B2B College Orchestration

### Guild System (College Classroom)
- Students join official college "Guild"
- TPOs act as Guild Masters
- Assign custom "Raid Bosses" (mandatory college placement exams)

### Predictive Placement Analytics (TPO Dashboard)
- **Green Zone**: Ready for Product-Based (12+ LPA)
- **Amber Zone**: Suited for Service-Based (5-10 LPA)
- **Red Zone**: Needs urgent remedial bootcamps

### Anti-Cheat / Plagiarism Engine
- Copy-paste metrics tracking
- Tab switching detection
- Code structure similarity indices

---

## 5. Question Engine

### Question Format
- **Narrative**: "The King's database has been corrupted..."
- **Technical Core**: Merge Sort / Two-Pointer
- **Company Tags**: #TCS-Digital, #Infosys-SP, #Amazon
- **Reward Schema**: XP + Coins per question

### Progression Database
| Question ID | Concept | Company | Difficulty | XP | Coins |
|-------------|---------|---------|------------|----|-------|
| Q_ARR_01 | Subarray Sum | TCS Digital | Easy-Med | 150 | 15 |
| Q_DP_12 | 0/1 Knapsack | Amazon | Hard | 500 | 50 |

---

## 6. Real-Time Browser Compiler

### Execution Flow
```
Monaco Editor → Submit → Backend API Gateway → Auth + Sanitize
  → Piston API (Docker Sandbox) → Compile + Execute
  → Gamification Middleware → Calculate XP & Multipliers → Update UI
```

### Gamification Hook
```python
def reward_player(user, question, metrics):
    base_xp = question.xp
    streak_mult = 1.5 if user.streak >= 5 else 1.0
    speed_bonus = 50 if metrics.runtime_ms < 50 else 0
    final_xp = (base_xp * streak_mult) + speed_bonus
    # Trigger level-up check, achievements, animations
```

### Live Arcade Feedback
- 8-bit chime on pass
- XP bar fill animation
- Screen explosion on level-up
- Achievement card popup (e.g., "Recursion Rookie!")

---

## 7. US Market Features

### "LeetCode Killer" Speed Run Mode
- 15-min matchmaking queue
- Solve Blind 75 / NeetCode style problems
- "Complexity Shields" — optimal O(N) beats O(N²)

### Open-Source Bounties (World Quests)
- Fetch real "good first issues" from GitHub
- Webhook detects merged PR → legendary loot + profile badge

### FAANG Gauntlet (Boss Rush)
- Targeted corporate dungeon paths (Netflix, Stripe, Quant)
- Company-specific IDE mode (C++ for Quant)
- "Certified [Company] Dungeon Raider" badge for LinkedIn

### Resume Loot Box (ATS Optimizer)
- Dynamic ATS-friendly wording based on solved challenges
- Auto-populate resume from verified game stats

### AI Behavioral Interview RPG
- Voice-activated STAR method practice
- "Charisma Points" for well-structured answers
- AI acts as mock US Tech Manager

### Inter-University Clan System
- .edu email → auto-join university clan
- Weekly XP leaderboard competition
- "Digital Throne" on homepage for top university

### YC Hackathon Speedrun
- 48-hour "Startup Sandbox Sprint"
- Deploy features on half-baked API codebase
- "Unicorn Builder" badge

### Layoff Shields & Severance Shop
- 7-day streak → Layoff Shield
- "Open to Work Mode" → 2x XP, orange theme, emergency hints

### Blind/Reddit Underground Guild
- Anonymous forum for interview Q sharing
- Community bounties for best solutions

### AI Copilot Debuff Mode ("The Pure Canvas")
- No copy-paste, no autocomplete, no hints
- "Verified Independent Engineer" status emblem

### Charisma Tree (Networking RPG)
- Cold-email strategy visual novel
- "Charisma XP" → unlock outreach templates

### WFH Desk Customization
- Pixel-art digital office backdrop
- Earned decor: ultrawide monitor, Herman Miller chair, lava lamp

---

## 8. Implementation Roadmap

### Phase 1 (Month 1-2) ✅ (Completed)
- Monaco Editor integration
- Piston API code execution
- Basic gamification (XP, levels, streaks)
- Auth system
- Landing page + pricing

### Phase 2 (Month 3-4) 🔄 (In Progress)
- Learning Journeys (8 curated paths)
- Challenge Packs (trading card system)
- AI Mentor (Lumi clone)
- Code Playground (Builds clone)
- Command Center dashboard
- Compare Visualizer UI
- Community Feed

### Phase 3 (Month 5-6) 📋 (Planned)
- TPO College Dashboard
- Anti-cheat / Plagiarism Engine
- FAANG Gauntlet dungeon paths
- Open-Source Bounty integration (GitHub webhooks)
- Voice-activated behavioral interview (Web Speech API + AI)
- Inter-University Clan leaderboard

### Phase 4 (Month 7-8) 📋 (Future)
- YC Hackathon speedrun mode
- AI Copilot Debuff Mode
- Cold-Email Charisma Tree
- WFH Desk pixel-art customization
- Marketplace / Shop (avatars, themes, hint scrolls)
- Mobile app (React Native)

---

## 9. Revenue & Monetization

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 3 interviews/mo, 3 resume reviews/mo, 5 aptitude tests/mo, 5 practice Qs/mo |
| Pro | $9/mo | Unlimited everything, priority AI, all badges, leaderboard |
| Lifetime | $39 | One-time, same as Pro, forever |
| College B2B | Custom | TPO dashboard, analytics, custom raid bosses |

### Geo Pricing
- **India**: ₹299/mo Pro (adjusted for purchasing power)
- **US**: $9/mo Pro
- **Other**: $6/mo Pro

---

## 10. Success Metrics

| Metric | Target |
|--------|--------|
| Daily Active Users | 1,000 (Month 6) |
| Monthly Active Users | 10,000 (Month 12) |
| Paid Conversion Rate | 5-8% |
| 7-Day Retention | 40%+ |
| Avg Sessions/User/Day | 3+ |
| Questions Solved/User/Month | 20+ |
| MRR | $4,500 (Month 12) |
| College Partners | 10+ (Month 8) |
