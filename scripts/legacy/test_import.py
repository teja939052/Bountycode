import sys
sys.path.insert(0, r"D:\Project-Fremen\backend")
from app.services import readiness_engine
print([x for x in dir(readiness_engine) if not x.startswith('_')])