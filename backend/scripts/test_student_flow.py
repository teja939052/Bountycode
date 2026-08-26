from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("=" * 60)
print("STEP 1: Register a new user")
print("=" * 60)
resp = client.post("/api/auth/register", json={
    "email": "test.student@placementpro.com",
    "password": "TestPass123!",
    "name": "Test Student"
})
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"Token: {data.get('token', 'N/A')[:20]}...")
    print(f"User: {data.get('user', {}).get('email', 'N/A')}")
else:
    print(f"Error: {resp.json()}")

print("\n" + "=" * 60)
print("STEP 2: Login")
print("=" * 60)
resp = client.post("/api/auth/login", json={
    "email": "test.student@placementpro.com",
    "password": "TestPass123!"
})
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    token = data.get('token', '')
    print(f"Got token, now testing with cookies...")
else:
    print(f"Error: {resp.json()}")

print("\n" + "=" * 60)
print("STEP 3: Get Aptitude Categories (with auth)")
print("=" * 60)
resp = client.get("/api/v1/aptitude/categories")
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    cats = data['categories']
    print(f"Categories: {len(cats)} found")
    for c in cats:
        print(f"  - {c['id']}: {c['name']} ({len(c.get('questions', 0))} questions)")
else:
    print(f"Error: {resp.json()}")

print("\n" + "=" * 60)
print("STEP 4: Get Quick Aptitude Questions (with auth)")
print("=" * 60)
resp = client.get("/api/v1/aptitude/quick-quantitative")
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    questions = data['questions']
    print(f"Got {len(questions)} questions")
    for i, q in enumerate(questions[:1]):
        print(f"\nQuestion {i+1}: {q['question'][:50]}...")
        print(f"  Options: {q['options']}")
        print(f"  Correct answer index: {q['correct_answer']}")
        print(f"  Explanation: {q['explanation'][:80]}...")
        print(f"  Difficulty: {q['difficulty']}")
        print(f"  Topic: {q['topic']}")
        print(f"  Companies: {q.get('companies', [])}")
else:
    print(f"Error: {resp.json()}")

print("\n" + "=" * 60)
print("STEP 5: Submit Answer & Get Feedback")
print("=" * 60)
if resp.status_code == 200:
    questions = resp.json()['questions']
    if questions:
        q = questions[0]
        question_id = q.get('id', 'unknown')
        print(f"Submitting answer for question ID: {question_id}")
        print(f"Selected answer: {q['options'][0]}")
        
        resp = client.post("/api/v1/aptitude/answer", json={
            "interview_id": "test-session-001",
            "question_id": question_id,
            "answer": q['options'][0],
            "time_taken": 30,
            "is_follow_up": False
        })
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Feedback: {data.get('feedback', 'N/A')[:100]}...")
            print(f"Score: {data.get('score', 'N/A')}")
            print(f"Explanation: {data.get('explanation', 'N/A')[:100]}...")
            print(f"Correct: {data.get('correct', False)}")
        else:
            print(f"Error: {resp.json()}")

print("\n" + "=" * 60)
print("FLOW TEST COMPLETE")
print("=" * 60)