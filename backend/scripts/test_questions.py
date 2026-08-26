from app.data.interview_question_bank import (
    COMPANY_QUESTIONS, get_all_companies, get_question_by_id,
    get_random_questions, get_total_question_count
)

print("Import OK")
print(f"Total companies: {len(get_all_companies())}")
amz = len(COMPANY_QUESTIONS.get("amazon", {}).get("questions", {}))
print(f"Amazon question count: {amz}")
goog = len(COMPANY_QUESTIONS.get("google", {}).get("questions", {}))
print(f"Google question count: {goog}")
tcs = len(COMPANY_QUESTIONS.get("tcs", {}).get("questions", {}))
print(f"TCS question count: {tcs}")

q = get_question_by_id("amaz-beh-0001")
print(f"Sample question: {q['question'][:80]}..." if q else "Sample question: None")

r = get_random_questions(count=3, company_id="google", category="technical")
print(f"Random Google technical: {len(r)} questions")

print(f"TOTAL QUESTIONS: {get_total_question_count()}")
