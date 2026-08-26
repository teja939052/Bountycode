from app.main import app
from fastapi.testclient import TestClient

c = TestClient(app)

# Step 1: Register
print("=== Step 1: Register ===")
resp = c.post("/api/v1/auth/register", json={"email": "student@pro.com", "password": "Pass123!", "name": "Test Student"})
print(f"Status: {resp.status_code}")
data = resp.json()
token = data["token"]

# Step 2: Login (could also use registered token)
print("\n=== Step 2: Login ===")
resp = c.post("/api/v1/auth/login", json={"email": "student@pro.com", "password": "Pass123!"})
print(f"Status: {resp.status_code}")
login_data = resp.json()

# Step 3: Get me (verify auth works)
print("\n=== Step 3: Get Me ===")
resp = c.get("/api/v1/auth/me")
print(f"Status: {resp.status_code}")
me_data = resp.json()

# Step 4: Get aptitude categories
print("\n=== Step 4: Aptitude Categories ===")
resp = c.get("/api/v1/aptitude/categories")
print(f"Status: {resp.status_code}")
cats_data = resp.json()
cats = cats_data["categories"]
print(f"Categories: {len(cats)}")
for c in cats:
    print(f"  - {c['id']}: {c['name']}")

# Step 5: Get quick quantitative questions
print("\n=== Step 5: Quick Quantitative Questions ===")
resp = c.get("/api/v1/aptitude/quick-quantitative")
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    q_data = resp.json()
    questions = q_data["questions"]
    print(f"Got {len(questions)} questions")
    for i, q in enumerate(questions[:2]):
        print(f"\n--- Question {i+1} ---")
        print(f"Question: {q['question'][:60]}...")
        print(f"Options: {q['options']}")
        print(f"Correct answer: {q['correct_answer']}")
        print(f"Explanation: {q['explanation'][:80]}...")
        print(f"Difficulty: {q['difficulty']}")
        print(f"Topic: {q['topic']}")
        print(f"Companies: {q.get('companies', [])}")
        
        # Step 6: Submit answer
        print(f"\n>>> Submitting answer for question {i+1}...")
        resp = c.post("/api/v1/aptitude/answer", json={
            "interview_id": "test-session-001",
            "question_id": q["id"],
            "answer": q["options"][0],  # Student selects first option
            "time_taken": 30,
            "is_follow_up": False
        })
        print(f"Submit status: {resp.status_code}")
        if resp.status_code == 200:
            ans_data = resp.json()
            print(f"Correct: {ans_data.get('correct')}")
            print(f"Score: {ans_data.get('score')}")
            print(f"Feedback: {ans_data.get('feedback', '')[:80]}...")
            print(f"Explanation: {ans_data.get('explanation', '')[:80]}...")
        else:
            print(f"Submit error: {resp.text[:200]}")