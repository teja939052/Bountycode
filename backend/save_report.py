import json
from app.services.scrimba_verification import verify_scrimba_lessons

report = verify_scrimba_lessons()
with open('app/content/scrimba_verification_report.json', 'w') as f:
    json.dump(report, f, indent=2, default=str)
print('Report saved:', report['total_lessons'], 'lessons,', report['passed_all_checks'], 'passed')
