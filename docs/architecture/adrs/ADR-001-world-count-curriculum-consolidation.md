# ADR-001: World Count and Curriculum Registry Consolidation

## Status
Proposed

## Context

The codebase contains multiple conflicting curriculum/world representations:

| Registry | File | World Count | Purpose |
|----------|------|-------------|---------|
| World Registry | `app/data/worlds_data.py` | 12 worlds | Level-based learning with Discover/Manipulate/Predict/Build/Break/Debug/Retrieve/Transfer/Mastery |
| Curriculum Base | `app/data/curriculum.py` | 7 languages × 50 levels | Language curricula |
| Curriculum 50 Levels | `app/data/curriculum_50_levels.py` | ? levels | 50-level progression |
| Curriculum Web | `app/data/curriculum_web.py` | ? levels | Web development |
| Curriculum Depth | `app/data/curriculum_depth.py` | ? levels | Deep-dive |
| Curriculum Enrichment | `app/data/curriculum_enrichment.py` | patches | Enrichment patches |
| Curriculum World Class | `app/data/curriculum_world_class.py` | ? levels | World-class curriculum |
| Capability Curriculum | `app/data/capability_curriculum.py` | ? levels | Capability-based |
| Lesson Registry | `app/content/curriculum/registry.py` | lesson slugs | Lesson slug → content |

The Vision Lock specifies 12 worlds registered in `ALL_WORLDS`:
1. foundations (World 1 — Variables/State)
2. searchlands (World 2 — Search)
3. sorting (World 3 — Sorting)
4. recursion (World 4 — Recursion)
5. linked (World 5 — Linked Lists)
6-12: hiring arena, company missions, AI engineering, production, projects, creative
Plus service-company placement tracks and foundation worlds.

The frontend App.tsx references `/worlds/:param` redirecting to `/skills`, suggesting worlds were deprioritized in favor of skills.

## Decision

**Canonical world registry**: `app/data/worlds_data.py` is the single source of truth for world/town/level definitions (12 worlds).

**Canonical lesson registry**: `app/content/curriculum/registry.py` (`LESSON_REGISTRY`) is the single source of truth for lesson content lookup by slug.

**Curriculum consolidation**: All other `curriculum_*.py` files in `app/data/` are deprecated. Their lesson content must be migrated into either:
- `worlds_data.py` (for world-based levels), or
- `registry.py` (for standalone lessons), or
- A new canonical curriculum file if neither fits.

**World count**: 12 worlds as defined in `worlds_data.py`. No 6-world or 18-world representation.

## Rationale

- `worlds_data.py` already has the complete World/Town/Level model with the 10-step pedagogical template (Discover → Manipulate → Predict → Build → Break → Debug → Retrieve → Transfer → Mastery)
- `registry.py` already maps lesson slugs to content dicts and is used by `LessonService`
- Having 8+ curriculum files creates maintenance burden and inconsistent lesson data

## Migration Plan

1. Audit each `curriculum_*.py` file for unique lesson content not in `worlds_data.py` or `registry.py`
2. Migrate unique content into the appropriate canonical registry
3. Deprecate `curriculum_*.py` files (keep for reference, mark with deprecation warnings)
4. Update imports to reference canonical registries only
5. Add architecture test that fails if new curriculum files are created outside canonical registries

## Consequences

- Positive: Single source of truth for worlds and lessons, easier maintenance
- Negative: Migration effort required, temporary dual-reading during transition

## References

- `docs/BOUNTYCODE_VISION_LOCK.md` — §82 lesson template, 12 worlds
- `app/data/worlds_data.py` — canonical world data
- `app/content/curriculum/registry.py` — canonical lesson registry
