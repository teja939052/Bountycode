from app.services.mastery_engine import record_solve, calculate_mastery_level

# Simulate answering the same question 5 times (all correct)
stats = None
for i in range(5):
    stats = record_solve('q-001', 'dsa.arrays', True, time_seconds=30, existing_stats=stats)

print('After 5 correct answers to same question:')
print('  problems_attempted:', stats['problems_attempted'], '(should be 1)')
print('  problems_solved:', stats['problems_solved'], '(should be 1)')
print('  questions_seen:', stats.get('questions_seen', []))
print()

# Now answer a different question correctly
stats = record_solve('q-002', 'dsa.arrays', True, time_seconds=30, existing_stats=stats)
print('After answering a second unique question correctly:')
print('  problems_attempted:', stats['problems_attempted'], '(should be 2)')
print('  problems_solved:', stats['problems_solved'], '(should be 2)')
print('  questions_seen:', stats.get('questions_seen', []))
print()

# Now answer the first question again (should NOT increment attempted)
stats = record_solve('q-001', 'dsa.arrays', True, time_seconds=30, existing_stats=stats)
print('After answering q-001 again (already seen):')
print('  problems_attempted:', stats['problems_attempted'], '(should still be 2)')
print('  problems_solved:', stats['problems_solved'], '(should still be 2)')
print('  questions_seen:', stats.get('questions_seen', []))