from pathlib import Path
import sys
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0,str(BACKEND_ROOT))
from scripts.validate_intake_v2 import validate_all  # noqa: E402

def test_intake_v2_contracts():
    assert validate_all() == {
        "mcq_candidates":430,
        "essay_prompts":28,
        "spoken_tasks":30,
        "company_blueprint_drafts":4,
    }
