"""World 1 Pedagogy Audit — canonical 9-step loop audit.

Canonical loop:
  Discover → Manipulate → Predict → Build → Break → Debug → Retrieve → Transfer → Prove

For each lesson, record which steps are present and which are genuinely needed.
Missing steps are documented with a rationale for inclusion/exclusion.
"""

from app.data.worlds_data import WORLD_FOUNDATIONS

LESSON_AUDIT = []

for town in WORLD_FOUNDATIONS.towns:
    for level in town.levels:
        steps_present = []
        steps_missing = []
        steps_needed = []

        # Check what's present
        if level.discover:
            steps_present.append("Discover")
        if level.manipulate:
            steps_present.append("Manipulate")
        if level.predict:
            steps_present.append("Predict")
        if level.code:
            steps_present.append("Build")
        if level.break_step:
            steps_present.append("Break")
        if level.debug:
            steps_present.append("Debug")
        if level.retrieval:
            steps_present.append("Retrieve")
        if level.transfer:
            steps_present.append("Transfer")
        if level.success:
            steps_present.append("Prove")

        # Determine what's needed based on lesson concept
        concept = level.concept or ""
        canonical_skill = level.canonical_skill or ""

        # Predict is needed when there's a misconception to address
        if "Predict" not in steps_present:
            if concept in ["variables", "reassignment", "multiple-variables", "expressions"]:
                steps_needed.append("Predict (what happens when you combine variables?)")
            else:
                steps_missing.append("Predict (not critical for this concept)")

        # Break is needed for state-changing or input-handling concepts
        if "Break" not in steps_present:
            if concept in ["variables", "reassignment", "multiple-variables", "expressions"]:
                steps_needed.append("Break (what happens with wrong types / missing values?)")
            else:
                steps_missing.append("Break (low value for pure syntax lessons)")

        # Debug is needed when students will encounter common errors
        if "Debug" not in steps_present:
            if concept in ["variables", "reassignment", "multiple-variables", "expressions"]:
                steps_needed.append("Debug (NameError, TypeError are common)")
            else:
                steps_missing.append("Debug (not needed if Build step has good error messages)")

        # Retrieve is always useful but the current hints serve this purpose
        if "Retrieve" not in steps_present:
            steps_missing.append("Retrieve (served by hint ladder in Build step)")

        LESSON_AUDIT.append({
            "level_id": level.id,
            "title": level.title,
            "concept": concept,
            "steps_present": steps_present,
            "steps_missing": steps_missing,
            "steps_needed": steps_needed,
        })

# Print summary
print("=== World 1 Pedagogy Audit ===\n")
for audit in LESSON_AUDIT:
    print(f"Level: {audit['level_id']} — {audit['title']}")
    print(f"  Concept: {audit['concept']}")
    print(f"  Present: {', '.join(audit['steps_present'])}")
    print(f"  Missing (not critical): {', '.join(audit['steps_missing']) if audit['steps_missing'] else 'none'}")
    print(f"  Needed (genuinely improves learning): {', '.join(audit['steps_needed']) if audit['steps_needed'] else 'none'}")
    print()

# Summary stats
total = len(LESSON_AUDIT)
has_transfer = sum(1 for a in LESSON_AUDIT if "Transfer" in a["steps_present"])
has_predict = sum(1 for a in LESSON_AUDIT if "Predict" in a["steps_present"])
has_break = sum(1 for a in LESSON_AUDIT if "Break" in a["steps_present"])
has_debug = sum(1 for a in LESSON_AUDIT if "Debug" in a["steps_present"])

print(f"Summary: {total} lessons")
print(f"  Transfer: {has_transfer}/{total}")
print(f"  Predict: {has_predict}/{total}")
print(f"  Break: {has_break}/{total}")
print(f"  Debug: {has_debug}/{total}")
