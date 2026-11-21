import sys

with open('backend/app/services/study_engine.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''            "skill": domain_id,
<<<<<<< HEAD
            "reason": decision.reason,
            "reason_codes": decision.reason_codes,
            "action": decision.action,
            "retest_after_days": decision.retest_after_days,
            "estimated_minutes": decision.estimated_minutes,
            "mastery": decision.mastery,
            "score": skill_score,
=======
            "reason": area.get("reason"),
            "selection_reason": "stable_daily_rotation",
>>>>>>> 2513abbf5afd49040fd2f2c6b74d8f92c90e1901
            "estimated_minutes": pick.get("estimated_minutes", 10),
            "xp_reward": 25,'''

new_block = '''            "skill": domain_id,
            "reason": decision.reason,
            "reason_codes": decision.reason_codes,
            "action": decision.action,
            "retest_after_days": decision.retest_after_days,
            "estimated_minutes": decision.estimated_minutes,
            "mastery": decision.mastery,
            "score": skill_score,
            "estimated_minutes": pick.get("estimated_minutes", 10),
            "xp_reward": 25,'''

if old_block in content:
    content = content.replace(old_block, new_block, 1)
    with open('backend/app/services/study_engine.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: study_engine.py resolved')
else:
    print('FAILED: Could not find exact old_block')
    # Debug
    lines = content.split('\n')
    for i, line in enumerate(lines[404:420], start=405):
        print(f'{i}: {repr(line)}')