# Academy-unification branch recovery — candidate assets

**Source branch:** `bountycode/academy-unification-and-resume`
**Source PR:** #3 was merged into main at an earlier revision; this candidate set preserves additional branch-only assets found during the 2026-11-19 consolidation audit.
**Disposition:** CANDIDATE / NOT STUDENT-SERVING.

These files are deliberately placed under `app/data/candidates/`. They must not be imported by the runtime lesson loader, question store, quiz composer, skill taxonomy, or company mock routes.

## Why these assets are isolated

The source branch is substantially behind current mainline and contains alternate implementations of question governance, skill graphs, SRS, company mock routes, service-company sprints, and frontend routing. Those competing engines and routes are not copied into the active architecture.

Content assets are retained for provenance-preserving review. Before promotion, each lesson/question must pass:
- schema and content-quality validation;
- canonical skill mapping;
- duplicate detection against active and candidate inventories;
- answer/solution validation;
- source/provenance review;
- trust lifecycle transitions through the canonical governance service;
- serving-gate and regression tests.

## Contents

- `lessons/`: recovered step-based lesson drafts.
- `banks/`: recovered question-bank snapshots and coding items.
- `metadata/`: company exam ontology, legacy skill-graph proposal, and scrim catalog.

Nothing in this directory is automatically served. Do not add this directory to production loader globs.
