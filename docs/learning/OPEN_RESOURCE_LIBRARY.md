# Bountycode Open Learning Resource Library

**Status:** First curated source catalogue; not yet connected to the student UI  
**Branch:** `feat/open-learning-resource-library`

## Purpose

Give each canonical Bountycode skill a useful mix of teaching, reference, visual, practice and revision material. Prefer high-quality public sources and link to their original pages. Do not treat free-to-view as permission to copy, mirror or commercially redistribute.

The machine-readable first-wave catalogue is:

- `backend/app/data/content/resource_catalog.json`

## First-wave source coverage

| Bountycode area | Starting resource | Formats |
|---|---|---|
| DSA and algorithms | MIT OCW 6.006; NPTEL Design and Analysis of Algorithms | Lecture videos, notes, problem sets, exams |
| Operating systems | Operating Systems: Three Easy Pieces; NPTEL OS courses | Textbook chapters, diagrams, simulator exercises, lectures |
| Computer networks | Loyola Chicago, An Introduction to Computer Networks | Open textbook, diagrams, exercises |
| Programming foundations | OpenStax Introduction to Python Programming; OpenStax Introduction to CS | Textbooks, PDF, interactive code activities |
| DBMS and SQL | A Practical Introduction to Databases; PostgreSQL Tutorial | Interactive textbook, SQL exercises, official docs |
| Quantitative aptitude | Khan Academy Mathematics | Worked examples, videos, interactive practice |
| Verbal and communication | British Council LearnEnglish | Grammar, reading, listening, vocabulary and speaking |
| Company preparation | Official TCS Smart Hiring sample paper | Official sample PDF |

## How it should appear in a lesson

Attach resources to existing canonical skill/concept IDs and registered lesson IDs. Do not create a second curriculum or a parallel mastery engine.

A topic resource panel should group material into:

1. **Learn deeply** — textbook chapters, lecture notes and videos.
2. **See it** — slide decks, diagrams, animations and worked examples.
3. **Practise** — exercises, labs, sample papers and problem sets.
4. **Revise quickly** — Bountycode-authored formula cards, patterns, shortcuts and common mistakes.
5. **Check mastery** — Bountycode's existing assessment and evidence flow.

A resource is supplementary; opening or completing it does not grant mastery, XP or readiness evidence. The learner must still complete Bountycode assessments.

## Rights and provenance rules

- Store title, provider, original URL, format, mapped topic IDs, access terms, license note, last-checked date and source type.
- Link-only is the default.
- Mirror or adapt only when the exact resource license permits it and attribution, non-commercial, share-alike and no-derivatives conditions are respected.
- A platform being free to access does not mean its content is open-licensed.
- Keep official employer sample papers distinct from candidate-reported experiences and original Bountycode practice.
- Do not scrape proprietary question banks or republish copyrighted question text.
- AI-generated summaries, flashcards, shortcut sheets and quizzes are draft learning aids. They require factual review. They must not flow into the trusted question bank automatically.

## Implementation sequence

1. **Resource discovery:** Expand this catalogue across every canonical skill, not just the first-wave areas.
2. **Topic mapping:** Resolve every resource to existing skill and lesson IDs; reject orphan mappings.
3. **Resource ingestion:** Where reuse is permitted, extract text, page/slide references, tables and diagrams while preserving provenance. Otherwise retain a link and metadata only.
4. **Learning transformations:** Create Bountycode-original explanations, worked examples, visual guides, formula cards and shortcuts. Label AI-assisted drafts and review them.
5. **Student UI:** Add a resource panel to the existing lesson/topic experience, not a separate disconnected resource hub.
6. **Quality gates:** Check links, rights, mapping, accessibility, factual accuracy and duplication before publishing.
7. **Outcome review:** Measure whether resources improve unseen transfer performance and delayed recall.

## Known limitations of this first wave

This commit adds the curated catalogue only. It does not yet connect the catalogue to the student API or frontend, and it does not claim complete topic coverage. The next engineering step is to inspect the existing lesson/resource response schema and integrate these entries through the canonical content service.
