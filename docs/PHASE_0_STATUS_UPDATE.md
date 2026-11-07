# Phase 0 Status Update — 2026-11-07

## Current accurate inventory (live main)

### World system (canonical interactive teaching)
- `world_registry.py` registers 12 worlds.
- **World 1 (Foundations)** and **World 2 (Problem Solver)** contain high-quality multi-step interactive lessons (discover → manipulate → predict → build → break → debug → retrieve → transfer → mastery).
- Worlds 3–12 exist but many lessons are thinner (fewer steps). They must be raised to World-1 quality or marked incomplete.

### services/lessons system (legacy track catalog)
- `__init__.py` now imports only real modules (python, python_content, java, cpp, dsa, aptitude, logical, verbal, dbms, os, networks, oop, company_prep).
- `dsa.py` currently holds a small set of real lessons (arrays, strings, linked list, stack, queue, binary search, sorting, BST) — not the 1,000+ filler previously reported on an older branch.
- `python_content.py` contains solid topic-level Python content.
- Generated `gen_*.py` and `*_extra.py` files still exist on disk but are **not imported**. They should be removed or quarantined to avoid future accidents.

### Question bank
- Trust report still shows only ~104 verified questions out of ~6,379.
- TEMPLATE_SHELL and UNVERIFIED_EXPECTED_OUTPUT remain the dominant states.
- Only TRUSTED questions may be served on placement-facing surfaces.

### Previous audit numbers (2026-11-06)
The 1,023 template-filler / 1,013 broken-prereq numbers came from a different branch state. Live main is cleaner on the lesson-catalog side but still requires:
1. Removal of unused gen_* / extra files.
2. Raising thin World 3+ lessons to full standard.
3. Strict trust enforcement on the question bank.
4. Full end-to-end student-loop verification.

## Decision locked today

- **Primary teaching surface** = World system (`world_registry` + world content files).
- **Curriculum direction** = `docs/SERVICE_COMPANY_CURRICULUM.md` (service-company focus).
- **Quality bar** = World-1 interactive standard + LEARNING_EXPERIENCE_STANDARD.md.
- No bulk generation of low-quality lessons. Every new lesson ships complete.

## Next concrete engineering/content steps

1. Delete or move unused `gen_*.py` and `*_extra.py` under services/lessons to a quarantine folder.
2. Expand Phase A (Programming Foundations) and Phase D/E/F (Aptitude/Reasoning/Verbal) using the World-1 lesson template.
3. Wire company readiness scores to the verified skill graph only.
4. Keep question bank gated behind TRUSTED status.
