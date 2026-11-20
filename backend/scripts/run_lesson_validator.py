import sys, os, json
sys.path.insert(0, '.')
from app.services.lesson_validator import validate_all_lessons

result = validate_all_lessons()

print(f"Total lessons: {result['total']}")
print(f"Valid: {result['valid']}")
print(f"Invalid: {result['invalid']}")
print()

if result['errors']:
    print("=== Lesson validation errors ===")
    for fname, errors in sorted(result['errors'].items()):
        print(f"\n{fname}:")
        for err in errors:
            print(f"  - {err}")
else:
    print("All lessons passed validation!")
