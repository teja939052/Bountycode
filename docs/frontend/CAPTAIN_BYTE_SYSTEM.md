# Captain Byte — Character System

Captain Byte is BountyCode’s persistent guide. He is not decoration. He appears when his presence changes what the learner does, understands, or feels.

## Personality

- Warm, wry, encouraging.
- Never sarcastic at the learner’s expense.
- Teaches through questions and hints, not answers.
- Treats mistakes as data, not failure.

## Character Backstory

Captain Byte is a weathered but upbeat coding captain who sailed from foundational syntax into the open sea of real systems. He has seen enough bugs to know that every mistake is a clue, not a defeat. He carries learners from their first line of code through production-grade projects, company assessments, and career milestones.

## Visual Rules

- SVG only. No raster, no emoji in the avatar component.
- One coherent geometry: head, bandana, collar, earring, scar.
- Mood changes color and expression only.
- Appears in two sizes: compact (inline) and full (card).
- Dialogue is never random. It comes from page state via `useMentor`.

## Moods

| Mood | When | Expression |
|------|------|-----------|
| welcome | First meeting, landing, onboarding | Neutral smile, green accent |
| briefing | Mission start, level start, daily briefing | Neutral smile, green accent |
| explaining | Concept introduction, step hint | Neutral smile, teal accent |
| correcting | Gentle mistake feedback | Straight mouth, teal accent |
| encouraging | After failure, repair mode | Small smile, teal accent |
| proud | Success, mastery, reward reveal | Big smile, gold accent |
| celebrating | Big win, boss defeated, streak milestone | Big smile, gold accent |
| serious | Boss intro, high-stakes assessment | Determined lines, red accent |
| thinking | Loading, executing, tracing | Neutral smile, green accent |
| stuck | Learner idle too long, repeated failure | Neutral smile, amber accent |
| handoff | Completion handoff to next step | Proud smile, green accent |

## Placement Rules

1. **Onboarding** — welcome/handoff only.
2. **Lesson start** — briefing.
3. **Concept explanation** — explaining.
4. **Mistake** — correcting or encouraging, never punitive.
5. **Success** — proud or celebrating, tied to mastery events.
6. **Boss** — serious at intro, celebrating on defeat.
7. **Assessment** — briefing at start, encouraging mid-way if struggling.
8. **Repair** — encouraging at start, proud when repaired.
9. **Idle/loading** — thinking only.
10. **No decorative repeats** — one callout per state change.

## Dialogue Rules

- One sentence preferred. Two maximum.
- Always actionable or reassuring.
- Never generic praise. Reference the current concept, error, or progress.
- Never reveal the answer directly. Hint toward the missing piece.

## File Map

- `frontend/src/design-system/Mentor.tsx` — avatar + mentor component
- `frontend/src/hooks/useMentor.ts` — state-driven dialogue
- `frontend/src/components/golden/MentorCallout.tsx` — inline callout
- `docs/frontend/CAPTAIN_BYTE_SYSTEM.md` — this file
