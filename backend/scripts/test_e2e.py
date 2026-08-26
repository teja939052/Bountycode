import json
import requests

BASE = "http://127.0.0.1:8000/api"

# Flow 1: Register → Onboarding → Auth me
print("=== Flow 1: Register -> Onboarding -> Auth me ===")

# Register
reg = requests.post(f"{BASE}/auth/register", json={"email": "testrel@example.com", "password": "TestPass123!", "name": "Test User"})
print(f"Register: status={reg.status_code}")
if reg.status_code == 200:
    data = reg.json()
    print(f"  token present: {'token' in data}")
    print(f"  user: {data.get('user', {}).get('email')}")

    # Onboarding complete
    ob = requests.post(f"{BASE}/auth/onboarding-complete", json={"completed": True})
    print(f"Onboarding complete: status={ob.status_code}")
    if ob.status_code == 200:
        print(f"  response: {ob.json()}")

    # GET /auth/me
    me = requests.get(f"{BASE}/auth/me")
    print(f"GET /auth/me: status={me.status_code}")
    if me.status_code == 200:
        mdata = me.json()
        print(f"  user: {mdata.get('email')}")
        print(f"  is_admin: {mdata.get('is_admin')}")
        print(f"  plan: {mdata.get('plan')}")
    else:
        print(f"  error: {me.text}")
else:
    print(f"  error: {reg.text}")

print()

# Flow 2: Login
print("=== Flow 2: Login ===")
login = requests.post(f"{BASE}/auth/login", json={"email": "testrel@example.com", "password": "TestPass123!"})
print(f"Login: status={login.status_code}")
if login.status_code == 200:
    ldata = login.json()
    print(f"  token present: {'token' in ldata}")
    print(f"  user: {ldata.get('user', {}).get('email')}")
    
    # Use the token for subsequent calls
    headers = {"Authorization": f"Bearer {ldata.get('token')}"} if ldata.get('token') else {}
    
    # GET /auth/me with auth header
    me = requests.get(f"{BASE}/auth/me", headers=headers)
    print(f"GET /auth/me: status={me.status_code}")
    if me.status_code == 200:
        mdata = me.json()
        print(f"  user: {mdata.get('email')}")
        print(f"  is_admin: {mdata.get('is_admin')}")
    
    # Test ProtectedRoute behavior - just verify /me works with cookie
    # The app uses httpOnly cookies, so let's test without explicit auth header
    me2 = requests.get(f"{BASE}/auth/me")
    print(f"GET /auth/me (cookies): status={me2.status_code}")
    if me2.status_code == 200:
        mdata2 = me2.json()
        print(f"  user (cookies): {mdata2.get('email')}")
        print(f"  is_admin (cookies): {mdata2.get('is_admin')}")

print()

# Flow 3: Question bank browse
print("=== Flow 3: Question bank browse ===")
browse = requests.get(f"{BASE}/questions/browse?limit=5")
print(f"GET /questions/browse: status={browse.status_code}")
if browse.status_code == 200:
    bdata = browse.json()
    print(f"  questions count: {len(bdata.get('questions', []))}")
    print(f"  total: {bdata.get('total')}")
else:
    print(f"  error: {browse.text}")

print()

# Flow 4: Compiler (check endpoint exists)
print("=== Flow 4: Compiler endpoints ===")
lang = requests.get(f"{BASE}/compiler/languages")
print(f"GET /compiler/languages: status={lang.status_code}")
if lang.status_code == 200:
    print(f"  languages: {lang.json()}")

execute = requests.post(f"{BASE}/compiler/execute", json={"language": "python", "code": "print('hello')", "test_cases": []})
print(f"POST /compiler/execute: status={execute.status_code}")
if execute.status_code == 200:
    print(f"  result: {execute.json()}")
else:
    print(f"  error: {execute.text[:200]}")

print()
print("=== All basic flows completed ===")