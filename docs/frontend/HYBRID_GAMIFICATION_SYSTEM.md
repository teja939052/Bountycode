# Hybrid Gamification System — BountyCode

## Source Platforms
- **Mimo**: streak challenges, free weekend tickets, certificates, project milestones, daily goals
- **Brilliant**: mastery-streak leagues, daily problem XP, adaptive practice rewards, tutor-linked progress
- **Boot.dev**: guild squads, embers/streak-savers, spellbooks/notes, boss-fight lore, custom paths
- **Codecademy**: skill-XP buckets, weekly target badges, community events/cups, certificate pathways

## Design Principles
1. **Learning first**: every mechanic must reinforce real practice, not replace it.
2. **One progress engine**: all sources feed the same Diamonds/level/streak/ledger.
3. **Deterministic rewards**: no RNG loot boxes; every bonus tells a clear story.
4. **Optional social**: competition is opt-in; solo progression is always available.
5. **Captain Byte consistent**: mentor mood derives from the same state that drives rewards.

## Hybrid Model
### Core Loop
```
Learn → Practice → Review → Mock/Apply → Repair → Mastery
   ↓        ↓        ↓         ↓          ↓         ↓
  XP      XP+R      XP       XP+R       XP+R     Boss Unlock
   ↓        ↓        ↓         ↓          ↓         ↓
Streak → Combo → Daily Goal → Mastery Streak → League → Certificate
```

### Reward Taxonomy
| Reward | Source | Spend/Display | Notes |
|--------|--------|---------------|-------|
| Diamonds (XP) | All activities | Level progress | Server-calculated only |
| Coins | Activities, milestones | Shop, streak repair | Deterministic |
| Stars | Performance | Profile only | No economy |
| Proof | Mastery evidence | Badges/titles | Non-spendable |
| Bounty | Challenge completions | Cosmetics | Non-spendable |
| Streak | Daily login | Multipliers | With freeze/embers |
| Mastery Streak | ≥8/10 daily | Milestone chests | Mimo-inspired |
| Combo | Rapid practice | XP multiplier | Time-windowed |
| League XP | Weekly activity | Seasonal rank | Brilliant-inspired |
| Guild XP | Squad goals | Shared rewards | Boot.dev-inspired |
| Certificates | Path completion | LinkedIn/PDF | Codecademy-inspired |

### New Hybrid Features
1. **Embers** — Boot.dev-style streak buffer earned on extra-hard days; 1 ember protects 1 missed day.
2. **Spellbook** — Auto-notes per concept; review = XP; searchable; tied to SRS.
3. **Guild/Squad** — Optional 3–10 person cohort; shared weekly quest; top contributors unlock group power-ups.
4. **Daily Problem** — Brilliant-style single problem worth bonus XP; resets daily; streaks multiply reward.
5. **Skill Branches** — Mimo/Codecademy-style per-skill XP trees; separate level per skill with local badges.
6. **Certificate Pathways** — Role + company track → auto-issued certificate on mastery + mock pass.
7. **Community Cup** — Weekly themed event with custom rules; top 10% get unique Proof/Bounty.
8. **Captain Byte Quests** — Narrative wrapper around daily/weekly goals; character mood maps to reward tier.

## Integration Points
- `journey_engine.py` → mentor state already drives Captain Byte moods
- `gamification.py` / `gamification_core.py` → single writer for all counters
- `adaptive_lesson_planner.py` → daily problem selection
- `curriculum.py` → certificate pathway triggers
- `routes/gamification.py` → new endpoints for guild/spellbook/embers
- Frontend: `components/golden/MentorCallout.tsx` + `hooks/useMentor.ts` already wired

## Acceptance Criteria
- Every new reward flows through `record_practice()` or a declared bonus pipeline.
- No RNG; all values are deterministic from state + activity.
- Frontend build passes; backend compiles.
- Captain Byte copy reflects hybrid state (ember count, guild rank, skill branch).
