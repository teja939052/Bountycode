import re
import os

def get_prefix_and_routes(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    prefixes = re.findall(r'APIRouter\(prefix="([^"]+)"', content)
    routes = re.findall(r'@router\.(get|post|put|delete|patch)\("([^"]+)"', content)
    skill_routes = re.findall(r'@skill_router\.(get|post|put|delete|patch)\("([^"]+)"', content)
    return prefixes, routes, skill_routes

dir_path = r"D:\Project-Fremen\backend\app\routes"
files = [
    "referral.py", "referrals.py", "referral_system.py",
    "analytics.py", "analytics_admin.py",
    "campus.py", "campus_wars.py", "campus_connect.py", "campus_pulse.py"
]

for f in files:
    path = os.path.join(dir_path, f)
    if not os.path.exists(path):
        print(f"\n=== {f} === NOT FOUND")
        continue
    p, r, sr = get_prefix_and_routes(path)
    print(f"\n=== {f} ===")
    print(f"Prefixes: {p}")
    print(f"Routes ({len(r)}): {r[:8]}")
    if sr: print(f"Skill routes: {sr[:5]}")
