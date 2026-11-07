"""Run content trust fixes and print summary."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.question_store import run_all_content_trust_fixes

result = run_all_content_trust_fixes()
print("Content Trust Fixes Applied:")
print(f"  Stale MCQ stamps fixed: {result['stale_mcq_fixed']}")
print(f"  SQL quarantined: {result['sql_quarantined']}")
print(f"  Verified-not-executable quarantined: {result['verified_not_exec_quarantined']}")
print(f"  Total servable: {result['total_servable']} / {result['total_questions']}")
