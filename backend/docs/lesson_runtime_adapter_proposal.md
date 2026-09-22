# Architectural Proposal: LessonDefinition → Canonical Runtime Adapter

## Problem

Two parallel lesson systems exist:

| System | Model | Route | Player |
|--------|-------|-------|--------|
| LessonPage | `LessonDefinition` / `LessonStep` | `/lesson/{slug}` | `LessonPage.tsx` |
| LevelPlayer | `LevelBase` / `BreakStep` / `Debug` | `/api/v1/worlds/{world_id}/levels/{id}` | `LevelPlayer.tsx` |

World 2 content lives in `LessonDefinition` format and is adapted via `world2_bridge.py` for `LessonPage`. If we ever want `LevelPlayer` to serve World 2, we would need to duplicate all 13 lessons into `LevelBase` format.

This is unsustainable. Adding World 3 would require a third copy.

## Desired End State

```text
LessonDefinition (canonical content)
        |
        v
  Runtime Adapter
        |
        v
  Normalized Lesson Steps
        |
        +---> LessonPage renderer
        |
        +---> LevelPlayer renderer
```

One content source. Two (or more) renderers. No duplication.

## Proposal

### 1. Define a canonical intermediate representation

Create `app/content/lesson_runtime.py`:

```python
class RuntimeLessonStep(BaseModel):
    step_type: str  # discover, manipulate, predict, build, break, debug, retrieve, transfer, mastery
    title: str
    content: str = ""
    # Interaction
    interaction_type: str = ""  # select-value, reveal, code, text
    choices: list[dict] = []   # {text, correct, explanation}
    answer: str = ""
    # Code
    function_name: str = ""
    signature: str = ""
    starter_code: str = ""
    language: str = "python"
    test_cases: list[dict] = []
    hidden_tests: int = 0
    # Break/Debug
    buggy_code: str = ""
    expected_failure: str = ""
    fix_steps: list[str] = []
    # Hints/Repair
    hints: list[dict] = []
    repair_steps: list[dict] = []
    passing_score: int = 70
    max_attempts: int = 3
    # Metadata
    xp: int = 0
    canonical_skill: str = ""

class RuntimeLesson(BaseModel):
    lesson_id: str
    title: str
    description: str
    xp_reward: int
    steps: list[RuntimeLessonStep]
    srs_concept_tag: str = ""
    world_progression: dict = {}
```

### 2. Write adapters FROM existing formats TO RuntimeLesson

```python
# From LessonDefinition (World 1, World 2, Worlds 3-12)
def from_lesson_definition(lesson: LessonDefinition) -> RuntimeLesson:
    steps = []
    for s in lesson.steps:
        steps.append(RuntimeLessonStep(
            step_type=s.step_type,
            title=s.title,
            content=s.content,
            interaction_type=s.interaction or "",
            choices=s.options or [],
            answer=s.answer or "",
            function_name=s.function_name or "",
            signature=s.signature or "",
            starter_code=s.starter_code.get("python", "") if s.starter_code else s.starter or "",
            language=s.language or "python",
            test_cases=s.test_cases or [],
            hidden_tests=s.hidden_tests or 0,
            buggy_code=s.buggy_code or "",
            expected_failure="",  # not in LessonStep yet
            fix_steps=s.fix_steps or [],
            hints=[{"text": h} for h in s.hints] if s.hints else [],
            repair_steps=s.repair_steps or [],
            passing_score=s.passing_score or 70,
            max_attempts=s.max_attempts or 3,
            xp=lesson.xp or 0,
            canonical_skill=s.canonical_skill or lesson.concept or "",
        ))
    return RuntimeLesson(...)

# From LevelBase (existing worlds_data.py worlds)
def from_level_base(level: LevelBase) -> RuntimeLesson:
    # Convert LevelBase fields to RuntimeLessonStep
    ...
```

### 3. Update renderers to consume RuntimeLesson

**LessonPage.tsx**:
- Import `RuntimeLesson`
- Call `from_lesson_definition(lesson)` before rendering
- Render `RuntimeLessonStep` objects in sequence

**LevelPlayer.tsx**:
- Import `RuntimeLesson`
- Call `from_level_base(level)` before rendering
- Render `RuntimeLessonStep` objects in sequence

### 4. Migration path

1. Create `lesson_runtime.py` with `RuntimeLesson` / `RuntimeLessonStep`
2. Write `from_lesson_definition()` adapter
3. Write `from_level_base()` adapter
4. Update `LessonPage.tsx` to consume `RuntimeLesson`
5. Update `LevelPlayer.tsx` to consume `RuntimeLesson`
6. Verify World 1 and World 2 still render correctly
7. Deprecate `world2_bridge.py` (its logic moves into `from_lesson_definition()`)
8. Future worlds only need to author `LessonDefinition`; both players work automatically

## Benefits

- **One content source**: World 3+ authors write `LessonDefinition` once
- **Two renderers**: LessonPage and LevelPlayer both work from the same runtime model
- **No duplication**: No need to convert World 2 into `LevelBase`
- **Extensible**: Add a third renderer (e.g., mobile-native) without touching content
- **Testable**: Test the adapter once, both renderers benefit

## Risks

- Refactoring LessonPage.tsx is risky; it's 1200 lines
- Must not break existing World 1 flow during migration
- LevelPlayer.tsx is already working for its current worlds; changes must be additive

## Recommendation

Implement this **after** World 2 browser QA passes. The current World 2 flow works through `LessonPage` + `world2_bridge.py`. Don't touch it until the runtime QA proves it's solid. Then refactor both players onto the canonical runtime model.
