import os
import re

SKIP_DIRS = {'node_modules', 'dist', 'build', '.git', 'venv', '__pycache__', '.next', '.vercel'}
EXTENSIONS = {'.py', '.ts', '.tsx', '.js', '.jsx'}

# Curated compound replacements: only clearly reward-unit concepts
COMPOUND_MAP = {
    'diamonds_gained': 'diamonds_gained',
    'diamonds_reward': 'diamonds_reward',
    'diamonds_to_next': 'diamonds_to_next',
    'diamonds_into_level': 'diamonds_into_level',
    'total_diamonds': 'total_diamonds',
    'double_diamonds': 'double_diamonds',
    'bonus_diamonds': 'bonus_diamonds',
    'base_diamonds': 'base_diamonds',
    'max_diamonds': 'max_diamonds',
    'diamonds_awarded': 'diamonds_awarded',
    'diamonds_gap': 'diamonds_gap',
    'reward_diamonds': 'reward_diamonds',
    'lesson_diamonds': 'lesson_diamonds',
    'mastery_diamonds': 'mastery_diamonds',
    'estimated_diamonds': 'estimated_diamonds',
    'event_diamonds': 'event_diamonds',
    'interview_diamonds': 'interview_diamonds',
    'coding_diamonds': 'coding_diamonds',
    'day_diamonds': 'day_diamonds',
    'weekly_diamonds': 'weekly_diamonds',
    'monthly_league_diamonds': 'monthly_league_diamonds',
    'weekly_league_diamonds': 'weekly_league_diamonds',
    'period_diamonds': 'period_diamonds',
    'original_diamonds': 'original_diamonds',
    'profile_diamonds': 'profile_diamonds',
    'user_diamonds': 'user_diamonds',
    'my_diamonds': 'my_diamonds',
    'next_diamonds': 'next_diamonds',
    'target_diamonds': 'target_diamonds',
    'final_diamonds': 'final_diamonds',
    'first_diamonds': 'first_diamonds',
    'second_diamonds': 'second_diamonds',
    'season_diamonds': 'season_diamonds',
    'world_diamonds_test': 'world_diamonds_test',
    'test_diamonds_calculation': 'test_diamonds_calculation',
    'test_diamonds_integrity': 'test_diamonds_integrity',
    'test_no_direct_diamonds_writes': 'test_no_direct_diamonds_writes',
    'test_retry_no_duplicate_diamonds': 'test_retry_no_duplicate_diamonds',
    'test_complete_awards_exact_reported_diamonds': 'test_complete_awards_exact_reported_diamonds',
    'test_different_activities_different_diamonds': 'test_different_activities_different_diamonds',
    'test_level_10_at_4950_diamonds': 'test_level_10_at_4950_diamonds',
    'test_level_1_at_zero_diamonds': 'test_level_1_at_zero_diamonds',
    'test_level_2_at_50_diamonds': 'test_level_2_at_50_diamonds',
    'test_level_3_at_200_diamonds': 'test_level_3_at_200_diamonds',
    'test_diamonds_scales_with_score': 'test_diamonds_scales_with_score',
    'test_diamonds_calculation_types': 'test_diamonds_calculation_types',
    'profiles_with_diamonds': 'profiles_with_diamonds',
    'missing_or_zero_diamonds': 'missing_or_zero_diamonds',
    'refreshed_total_diamonds': 'refreshed_total_diamonds',
    'total_today_diamonds': 'total_today_diamonds',
    'total_diamonds_available': 'total_diamonds_available',
    'total_diamonds_earned': 'total_diamonds_earned',
    'total_diamonds_gained': 'total_diamonds_gained',
    'first_diamonds_total': 'first_diamonds_total',
    'second_diamonds_total': 'second_diamonds_total',
    'after_diamonds': 'after_diamonds',
    'before_diamonds': 'before_diamonds',
    'get_daily_diamonds': 'get_daily_diamonds',
    'get_role_diamonds_multiplier': 'get_role_diamonds_multiplier',
    'get_diamonds_with_multiplier': 'get_diamonds_with_multiplier',
    'award_bonus_diamonds': 'award_bonus_diamonds',
    '_calculate_diamonds': '_calculate_diamonds',
    '_league_for_diamonds': '_league_for_diamonds',
    '_profile_diamonds': '_profile_diamonds',
    '_diamonds_for_activity': '_diamonds_for_activity',
    '_award_diamonds': '_award_diamonds',
    'milestone_diamonds_bonus': 'milestone_diamonds_bonus',
    'spend_diamonds': 'spend_diamonds',
    'diamonds_for_next': 'diamonds_for_next',
    'diamonds_for_level': 'diamonds_for_level',
    'diamonds_orb': 'diamonds_orb',
    'diamonds_bar': 'diamonds_bar',
    'diamonds_popup': 'diamonds_popup',
    # Function names
    'getLevelForDiamonds': 'getLevelForDiamonds',
    'diamondsForLevel': 'diamondsForLevel',
    'diamondsForNextLevel': 'diamondsForNextLevel',
    # Event names
    'juice:diamonds': 'juice:diamonds',
    'diamonds-gained': 'diamonds-gained',
    # CSS classes
    'diamond-orb': 'diamond-orb',
    'diamond-bar': 'diamond-bar',
    'diamond-popup': 'diamond-popup',
    # UI strings
    ' Diamonds': ' Diamonds',
    ' Diamonds ': ' Diamonds ',
    ' Diamonds\n': ' Diamonds\n',
    ' Diamonds\t': ' Diamonds\t',
    ' Diamonds.': ' Diamonds.',
    ' Diamonds,': ' Diamonds,',
    ' Diamonds!': ' Diamonds!',
    ' Diamonds?': ' Diamonds?',
    ' Diamonds:': ' Diamonds:',
    ' Diamonds;': ' Diamonds;',
    ' Diamonds-': ' Diamonds-',
    ' Diamonds"': ' Diamonds"',
    ' Diamonds\'': ' Diamonds\'',
    '+Diamonds': '+Diamonds',
    ' Diamonds ': ' Diamonds ',
}

changed_files = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in files:
        ext = os.path.splitext(fname)[1]
        if ext not in EXTENSIONS:
            continue
        path = os.path.join(root, fname)
        if 'rename_xp_to_diamonds' in path:
            continue
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue

        new_content = content
        for old, new in COMPOUND_MAP.items():
            if old in new_content:
                new_content = new_content.replace(old, new)

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed_files.append(path)

print(f"Changed {len(changed_files)} files with compound replacements:")
for p in changed_files:
    print(f"  {p}")
