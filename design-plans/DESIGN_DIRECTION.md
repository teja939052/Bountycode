# BountyCode — Design Direction (Wave 0)

Source skills (fetched, not installed): `design-taste-frontend` v2 (taste-skill),
`redesign-existing-projects` (leonxlnx redesign-skill), `baseline-ui`,
plus installed `react-expert` / `test-master` for implementation discipline.
UI-Skills MCP is configured globally; this session used the catalog over HTTPS.

## Design read

**Reading this as:** redesign-preserve of an educational practice product for
placement-aspirant students (2G-market, mobile-heavy), with a calm focused
language, leaning toward the existing Tailwind token system + restrained motion.

**Dials:** VARIANCE match-existing · MOTION match+1 · DENSITY match.
(No overhaul: students must recognize the product on return. Sessions/week is
the metric; novelty that costs familiarity is a bug.)

## Product personality

Intelligent, playful, ambitious, alive, approachable, rewarding, credible,
premium, distinctly educational. NOT: childish, corporate-training, generic
SaaS, cheap gamification, noisy mobile game, AI dashboard, visual chaos.

North-star screen test (from the brief, kept verbatim — it is the whole job):
learner immediately understands **where I am, what I'm learning, what I need
to do, what changed because of my action, and why I should continue.**

## Token decisions (evidence, not taste)

1. **Surfaces:** `.page-surface` (page), `.card` / `Card` primitive (panels),
   `bg-surface-card`, `border-brand-primary/20` (selectable rows). Raw
   `bg-white` / `border-gray-200` / `text-gray-900` are banned on new work —
   they ignore the theme vars (`--pp-canvas/surface/border`) and break dark mode.
2. **Text:** inherit or `text-text` (headings), `text-text-muted` (secondary).
   `text-balance` on headings, `text-pretty` on body, `tabular-nums` on data.
3. **Accent (locked):** existing tree is split — `bg-primary-600` ×30
   (PracticeMode, DailyDrill, `.btn-primary` green system) vs `bg-blue-600` ×22
   (MistakeBook-era). Direction: **all new/edited surfaces use the primary
   system** (`.btn-primary`, `primary-*`); legacy blue migrates opportunistically
   wave by wave. No third hue is introduced, ever. Green/rose reserved for
   correct/wrong verdicts only.
4. **Type:** keep Baloo 2 (display) / Inter (body) / Manrope / JetBrains Mono.
  Already configured; a new webfont family costs 2G users real seconds for zero
   learning gain. (Taste skill's anti-Inter rule explicitly permits Inter for
   neutral/standard products.)
5. **Cards:** elevation must signal hierarchy. Static rows → single container
   with `divide-[var(--pp-border)]`. `Card` reserved for focal panels
   (quiz card, flashcard, scenario, verdict).
6. **Icons:** lucide stays (already depended on; skill prefers Phosphor but
   forbids mixing families mid-tree — consistency wins).

## Motion language

- Learning: calm, focused (opacity/transform only, ≤200ms feedback, ease-out).
- Interaction: tactile (active:scale, hover states on all CTAs).
- Success: brief. Mastery/boss: the only allowed intensity step-up.
- Failure: clear, recoverable, never humiliating.
- Navigation: quiet. No perpetual loops except streak/progress indicators.
- Reduced-motion: verified present — 4 CSS blocks in `index.css`, plus
  `useReducedMotion` hook, `useGSAP` guards, and per-component `matchMedia`
  checks (framer-motion handles its own). No work needed.

## Gamification language (spine, not decor)

Capability verbs, in order, as the visible reward spine:
`Discovered → Understood → Practiced → Mastered → Transferred`.
XP/diamonds/streaks are secondary signals. Never reward opening over
understanding. Boss = proof ceremony with countdown, recoverable failure,
explicit repair path (feeds the mistake notebook).

## Illustration language

One direction only (to be fixed in Wave 1 from existing assets — no new
imagery generated; no image-gen tool is available in this environment, so
references are written specs verified in the real build, never mockups):
no mixed emojis/stock/3D/cartoon. Lucide glyphs + existing primitives only
until Wave 1 locks an illustration vote.

## Screen priority map

Golden screens (benchmark quality first): Dashboard, Journey, one concept
lesson, one interactive coding lesson, Arena, MistakeBook, Boss Battle,
Company prep, Readiness, Interview.
Waves: 1 identity/system/nav/dashboard/Journey → 2 learning → 3 practice
(Deck/Arena/TeachWall/MistakeBook/QuestionBank/PracticeMode/DailyDrill) →
4 gamification → 5 placement → 6 marketing.

## Verification protocol (adapted — stated openly)

No browser/screenshot tooling exists in this environment, so "render and
inspect" becomes: `vite build` (CI frontend gate) + chunk check +
`pytest` (12 independent-learning + 82 bank + regression) + `tsc` on touched
files + class-level inspection against this document. Pre-existing tree dirt
(typecheck noise, dirty working tree) is reported, never silently absorbed.

## Non-goals for the redesign

No framework migration, no API/behavior changes, no new webfont families,
no blue→green mass rewrite outside wave scope, no image assets invented,
no peer/social features, no free-text grading UI.
