from app.main import app
from fastapi.testclient import TestClient

c = TestClient(app)

# Step 1: Register with unique email
print("=== Step 1: Register ===")
resp = c.post("/api/v1/auth/register", json={"email": "newstudent@pro.com", "password": "Pass123!", "name": "New Student"})
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    token = data.get("token", "")
    print(f"Got token: {token[:20]}...")
else:
    print(f"Error: {resp.text[:200]}")
    # Try login instead
    print("\n>>> Trying login directly...")
    resp = c.post("/api/v1/auth/login", json={"email": "newstudent@pro.com", "password": "Pass123!"})
    print(f"Login status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        token = data.get("token", "")
        print(f"Got token: {token[:20]}...")
    else:
        print(f"Login error: {resp.text[:200]}")
        exit(1)

# Step 2: Get me (verify auth)
print("\n=== Step 2: Get Me ===")
resp = c.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
print(f"Status: {resp.status_code}")
me_data = resp.json()
print(f"User: {me_data.get('email', 'N/A')}")

# Step 3: Get aptitude categories
print("\n=== Step 3: Aptitude Categories ===")
resp = c.get("/api/v1/aptitude/categories")
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    cats_data = resp.json()
    cats = cats_data["categories"]
    print(f"Categories: {len(cats)}")
    for c in cats:
        print(f"  - {c['id']}: {c['name']}")

# Step 4: Get quick quantitative questions
print("\n=== Step 4: Quick Quantitative Questions ===")
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
        
        # Step 5: Submit answer
        print(f"\n>>> Submitting answer for question {i+1} (selecting first option)...")
        resp = c.post("/api/v1/aptitude/answer", json={
            "interview_id": "test-session-001",
            "question_id": q["id"],
            "answer": q["options"][0],
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