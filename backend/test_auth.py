from app.main import app
from fastapi.testclient import TestClient

c = TestClient(app)

print("=== Register ===")
resp = c.post("/api/v1/auth/register", json={"email": "student@pro.com", "password": "Pass123!", "name": "Test Student"})
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"Token present: {'token' in data}")
    print(f"User: {data.get('user', {}).get('email', 'N/A')}")

print("\n=== Login ===")
resp = c.post("/api/v1/auth/login", json={"email": "student@pro.com", "password": "Pass123!"})
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"Token present: {'token' in data}")
    print(f"User: {data.get('user', {}).get('email', 'N/A')}")
    token = data.get("token", "")

    print("\n=== Me (with token) ===")
    resp = c.get("/api/v1/auth/me")
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"User: {data.get('email', 'N/A')}")
        print(f"Is admin: {data.get('is_admin', False)}")
        print(f"Plan: {data.get('plan', 'N/A')}")