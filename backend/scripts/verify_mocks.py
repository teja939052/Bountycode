import sys
sys.path.insert(0, 'backend')
from app.data.company_mocks import get_all_mocks, get_mock_by_company

mocks = get_all_mocks()
print(f'Total company mocks: {len(mocks)}')
for mock in mocks:
    print(f"  - {mock['company']} {mock['exam']}: {mock['total_questions']} questions, {mock['duration_minutes']} min")

tcs = get_mock_by_company('TCS')
print(f"\nTCS mock found: {tcs['id'] if tcs else 'Not found'}")
