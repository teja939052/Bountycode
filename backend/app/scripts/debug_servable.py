import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()

# Check if there are ANY servable questions for service companies
for company in ['tcs', 'infosys', 'wipro']:
    company_qs = [q for q in qs._questions if company in [c.lower() for c in q.get("companies", [])]]
    servable = [q for q in company_qs if qs._is_servable(q)]
    print(f"{company.upper()}: {len(company_qs)} total, {len(servable)} servable")
    
    if servable:
        sample = servable[0]
        print(f"  Sample: {sample.get('id')}")
        print(f"    trust_status: {sample.get('trust_status')}")
        print(f"    type: {sample.get('type')}")
        print(f"    frequency: {sample.get('frequency')}")
