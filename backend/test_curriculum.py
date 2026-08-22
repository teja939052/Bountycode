from app.data.master_coding_curriculum import FULL_CURRICULUM, EXERCISE_INDEX, TOPIC_INDEX, DIFFICULTY_DISTRIBUTION, PREMIUM_MAP, TOTAL_EXERCISES, CURRICULUM_STATS

print('import OK')
print('modules:', len(FULL_CURRICULUM))
print('total exercises:', TOTAL_EXERCISES)
print('difficulty dist:', DIFFICULTY_DISTRIBUTION)
print('premium modules:', sum(1 for v in PREMIUM_MAP.values() if v))
print('free modules:', sum(1 for v in PREMIUM_MAP.values() if not v))
# Check a sample module
mod = FULL_CURRICULUM['module_foundations']
print('foundations topics:', len(mod['topics']))
t = mod['topics'][0]
print(f'  {t["id"]}: {t["title"]} ({len(t["exercises"])} exercises)')
print('Curriculum stats:', CURRICULUM_STATS)