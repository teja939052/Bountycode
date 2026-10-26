import os
import re

SKIP_DIRS = {'node_modules', 'dist', 'build', '.git', 'venv', '__pycache__', '.next', '.vercel'}
EXTENSIONS = {'.py', '.ts', '.tsx', '.js', '.jsx'}

# Reverse of the compound map
REVERSE_MAP = {
    'xp_gained': 'xp_gained',
    'xp_reward': 'xp_reward',
    'xp_to_next': 'xp_to_next',
    'xp_into_level': 'xp_into_level',
    'total_xp': 'total_xp',
    'double_xp': 'double_xp',
    'bonus_xp': 'bonus_xp',
    'base_xp': 'base_xp',
    'max_xp': 'max_xp',
    'xp_awarded': 'xp_awarded',
    'xp_gap': 'xp_gap',
    'reward_xp': 'reward_xp',
    'lesson_xp': 'lesson_xp',
    'mastery_xp': 'mastery_xp',
    'estimated_xp': 'estimated_xp',
    'event_xp': 'event_xp',
    'interview_xp': 'interview_xp',
    'coding_xp': 'coding_xp',
    'day_xp': 'day_xp',
    'weekly_xp': 'weekly_xp',
    'monthly_league_xp': 'monthly_league_xp',
    'weekly_league_xp': 'weekly_league_xp',
    'period_xp': 'period_xp',
    'original_xp': 'original_xp',
    'profile_xp': 'profile_xp',
    'user_xp': 'user_xp',
    'my_xp': 'my_xp',
    'next_xp': 'next_xp',
    'target_xp': 'target_xp',
    'final_xp': 'final_xp',
    'first_xp': 'first_xp',
    'second_xp': 'second_xp',
    'season_xp': 'season_xp',
    'world_xp_test': 'world_xp_test',
    'test_xp_calculation': 'test_xp_calculation',
    'test_xp_integrity': 'test_xp_integrity',
    'test_no_direct_xp_writes': 'test_no_direct_xp_writes',
    'test_retry_no_duplicate_xp': 'test_retry_no_duplicate_xp',
    'test_complete_awards_exact_reported_xp': 'test_complete_awards_exact_reported_xp',
    'test_different_activities_different_xp': 'test_different_activities_different_xp',
    'test_level_10_at_4950_xp': 'test_level_10_at_4950_xp',
    'test_level_1_at_zero_xp': 'test_level_1_at_zero_xp',
    'test_level_2_at_50_xp': 'test_level_2_at_50_xp',
    'test_level_3_at_200_xp': 'test_level_3_at_200_xp',
    'test_xp_scales_with_score': 'test_xp_scales_with_score',
    'test_xp_calculation_types': 'test_xp_calculation_types',
    'profiles_with_xp': 'profiles_with_xp',
    'missing_or_zero_xp': 'missing_or_zero_xp',
    'refreshed_total_xp': 'refreshed_total_xp',
    'total_today_xp': 'total_today_xp',
    'total_xp_available': 'total_xp_available',
    'total_xp_earned': 'total_xp_earned',
    'total_xp_gained': 'total_xp_gained',
    'first_xp_total': 'first_xp_total',
    'second_xp_total': 'second_xp_total',
    'after_xp': 'after_xp',
    'before_xp': 'before_xp',
    'get_daily_xp': 'get_daily_xp',
    'get_role_xp_multiplier': 'get_role_xp_multiplier',
    'get_xp_with_multiplier': 'get_xp_with_multiplier',
    'award_bonus_xp': 'award_bonus_xp',
    '_calculate_xp': '_calculate_xp',
    '_league_for_xp': '_league_for_xp',
    '_profile_xp': '_profile_xp',
    '_xp_for_activity': '_xp_for_activity',
    '_award_xp': '_award_xp',
    'milestone_xp_bonus': 'milestone_xp_bonus',
    'spend_xp': 'spend_xp',
    'xp_for_next': 'xp_for_next',
    'xp_for_level': 'xp_for_level',
    'xp_orb': 'xp_orb',
    'xp_bar': 'xp_bar',
    'xp_popup': 'xp_popup',
    'getLevelForXP': 'getLevelForXP',
    'xpForLevel': 'xpForLevel',
    'xpForNextLevel': 'xpForNextLevel',
    'juice:xp': 'juice:xp',
    'xp-gained': 'xp-gained',
    'xp-orb': 'xp-orb',
    'xp-bar': 'xp-bar',
    'xp-popup': 'xp-popup',
}

changed_files = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in files:
        ext = os.path.splitext(fname)[1]
        if ext not in EXTENSIONS:
            continue
        path = os.path.join(root, fname)
        if 'rename_xp_to_diamonds' in path or 'rename_compound_xp' in path:
            continue
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue

        new_content = content
        for old, new in REVERSE_MAP.items():
            if old in new_content:
                new_content = new_content.replace(old, new)

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed_files.append(path)

print(f"Reverted compound replacements in {len(changed_files)} files:")
for p in changed_files:
    print(f"  {p}")
