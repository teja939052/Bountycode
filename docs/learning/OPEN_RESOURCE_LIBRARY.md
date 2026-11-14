# Bountycode Open Learning Resource Library

**Status:** First integrated version — API + topic-aware lesson panel  
**Branch:** `feat/open-learning-resource-library`

## What is implemented

- Curated external source catalogue: `backend/app/data/content/resource_catalog.json`
- Read-only API: `GET /api/v1/learning-resources?domain=&topic=&limit=`
- Topic-aware panel in the canonical LessonPlayer: `frontend/src/components/learning/LearningResourcesPanel.tsx`
- The panel appears inside lessons, queries using the lesson's domain, slug, title and concept tags, and links to original publishers.
- The API returns source title, provider, formats, topic tags, access, rights note and recommended use.
- Resource opens do not award XP, create mastery evidence or modify the learner state.
- Automated tests cover catalogue integrity, duplicate IDs, required provenance, DSA/DBMS matching and endpoint response shape.

The catalogue now includes 29 curated sources spanning DSA, algorithms, programming, C++, Python, JavaScript, TypeScript, React, web development, operating systems, networks, DBMS/SQL, computer science foundations, quantitative aptitude, verbal ability, company preparation and Indian undergraduate curriculum reference.

## Resource coverage

| Area | Examples |
|---|---|
| DSA and algorithms | MIT OCW 6.006, NPTEL DAA, Open Data Structures |
| Indian CSE curriculum | AICTE UG CSE model curriculum, NPTEL |
| Operating systems | Operating Systems: Three Easy Pieces |
| Computer networks | Loyola's An Introduction to Computer Networks |
| Programming and Python | OpenStax, Think Python, Python for Everybody, Python docs |
| C++ | cppreference |
| Web development | MDN Learn Web Development, MDN JavaScript, React Learn, TypeScript Handbook, freeCodeCamp |
| DBMS and SQL | Runestone database textbook, PostgreSQL tutorial |
| Aptitude and mathematics | Khan Academy |
| Verbal and communication | British Council LearnEnglish |
| Company preparation | Official TCS Smart Hiring sample paper |
| Broad CS pathway | OSSU, Saylor, OpenStax Computer Science |

## API behavior

- `domain` is matched against the catalogue's domain tags (with a small set of aliases).
- `topic` is matched against resource topic tags and titles.
- Results are ranked and capped; the endpoint never returns local file copies.
- Empty filters return a bounded catalogue listing.
- The catalogue is loaded from versioned JSON and cached in process memory.

## Lesson experience

The panel is supplementary and deliberately does not replace the existing lesson flow:

1. Bountycode lesson content and worked examples.
2. External books, lecture notes, videos, slides or references relevant to the current topic.
3. Bountycode practice, quizzes, code labs and assessment.
4. Existing BALMA / mastery evidence remains the source of learner-state decisions.

## Rights and provenance rules

- Link to the original publisher by default.
- A free-to-view resource is not automatically free to republish.
- Mirror or adapt only when the exact resource license permits it and attribution, non-commercial, share-alike and no-derivatives conditions are respected.
- Some platforms have different licenses across courses, chapters, code samples and slide decks. Check the exact item.
- OpenStax instructor resources such as slide decks and test banks may require an educator account; access does not itself grant redistribution rights.
- Keep official employer sample papers distinct from candidate-reported experiences and original Bountycode practice.
- Do not scrape proprietary question banks or republish copyrighted question text.
- AI-generated summaries, flashcards, shortcut sheets and quizzes are drafts until fact-checked and reviewed. They must not flow into the trusted question bank automatically.

## Next implementation stages

1. Resolve catalogue topics to canonical skill IDs and lesson IDs rather than relying only on text-token matching.
2. Expand resources for every individual skill and audit broken/retired links.
3. Author original Bountycode explanations, diagrams, formula cards, shortcuts and revision sheets for uncovered skills.
4. Add resource ingestion only for files with verified reuse permissions; otherwise keep external links.
5. Add reviewed visual material and accessible transcripts/notes where publishers permit.
6. Measure whether supplementary resources improve unseen transfer performance and delayed recall.

## Known limitations

- This first version is a curated starting catalogue, not a claim that every canonical skill already has a matching external resource.
- Topic matching currently uses domain aliases and text tokens; canonical skill-ID mapping is the next precision improvement.
- The student panel is integrated into LessonPlayer. Other lesson renderers/pages have not yet been migrated.
- Automated tests were authored but have not been executed in this GitHub-only pass.
- No third-party PPT/PDF has been copied into Bountycode. Original publisher links are used to respect rights.
