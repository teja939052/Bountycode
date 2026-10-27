import sys
sys.path.insert(0, ".")
from app.services.company_atom_map import get_company_atom_path
import re

with open("app/data/companies_2026_2027.py", "r", encoding="utf-8") as f:
    content = f.read()

companies = re.findall(r'"([^"]+)":\s*\{', content)
print(f"Found {len(companies)} companies")

for company in companies[:10]:
    try:
        path = get_company_atom_path(company, "python")
        print(f"{company}: {len(path)} atoms")
    except Exception as e:
        print(f"{company}: ERROR - {e}")
