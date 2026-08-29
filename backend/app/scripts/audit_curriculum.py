"""
Audit learning object coverage — see which topics/difficulties/stages are represented.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

LOS_PATH = Path(__file__).resolve().parents[2] / "app" / "content" / "questions" / "curated" / "learning_objects.json"

with open(LOS_PATH, encoding="utf-8") as f:
    los = json.load(f)

print(f"Total learning objects: {len(los)}\n")

# Topic distribution
topics = Counter(lo.get("topic", "Unknown") for lo in los)
print("=== TOPIC DISTRIBUTION ===")
for t, c in topics.most_common():
    print(f"  {c:3d}  {t}")

# Difficulty distribution
diffs = Counter(lo.get("difficulty", "Unknown") for lo in los)
print(f"\n=== DIFFICULTY DISTRIBUTION ===")
for d, c in diffs.most_common():
    print(f"  {c:3d}  {d}")

# Curriculum skill distribution
skills = Counter(lo["learning_object"]["curriculum_skill"] for lo in los)
print(f"\n=== CURRICULUM SKILL MAPPING ===")
for s, c in sorted(skills.items()):
    print(f"  {c:3d}  {s}")

# Placement stage distribution
stages = Counter()
for lo in los:
    for st in lo.get("placement_stage", []):
        stages[st] += 1
print(f"\n=== PLACEMENT STAGES ===")
for s, c in stages.most_common():
    print(f"  {c:3d}  {s}")

# Company coverage
companies = Counter()
for lo in los:
    for comp in lo.get("company", []):
        companies[comp] += 1
print(f"\n=== COMPANY COVERAGE ===")
for comp, c in companies.most_common():
    print(f"  {c:3d}  {comp}")

# Questions with/without patterns
patterns = Counter(lo.get("pattern", "general-concept") for lo in los)
print(f"\n=== PATTERN DISTRIBUTION ===")
for p, c in patterns.most_common():
    print(f"  {c:3d}  {p}")

# Coverage gaps vs SDE skill tree targets
print(f"\n=== SDE SKILL TREE TARGET GAPS ===")
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "app"))
from content.curriculum.sde_placement_pack import SDE_SKILL_TREE, TOTAL_SDE_QUESTIONS_TARGET
for skill_id, skill_info in SDE_SKILL_TREE.items():
    current = skills.get(skill_id, 0)
    target = skill_info["question_target"]
    gap = target - current
    pct = round(current / target * 100, 1) if target > 0 else 0
    status = "OK" if gap <= 0 else f"-{gap} needed"
    print(f"  {skill_id:30s} target={target:3d}  current={current:3d}  {status}  ({pct}%)")