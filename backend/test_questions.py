from app.data.interview_questions import (
    COMPANY_QUESTIONS, INTERVIEW_CATEGORIES,
    get_all_companies, get_question_by_id,
    get_random_questions, get_company_question_count
)

print("Import OK")
print(f"Total companies: {len(get_all_companies())}")
amz = get_company_question_count("amazon")
print(f"Amazon question count: {amz}")
goog = get_company_question_count("google")
print(f"Google question count: {goog}")
tcs = get_company_question_count("tcs")
print(f"TCS question count: {tcs}")

q = get_question_by_id("amz-bh-001")
print(f"Sample question: {q['question'][:80]}...")

r = get_random_questions(count=3, company="google", category="technical")
print(f"Random Google technical: {len(r)} questions")

total = 0
for cid in COMPANY_QUESTIONS:
    total += get_company_question_count(cid)["total"]
print(f"TOTAL QUESTIONS: {total}")
