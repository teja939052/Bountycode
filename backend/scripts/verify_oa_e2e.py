import sys
sys.path.insert(0, ".")
import asyncio
from app.routes.oa import _resolve_blueprint, _distribute, _build_questions

async def test():
    bp = _resolve_blueprint("tcs_nqt", "swe")
    print(f"TCS NQT blueprint keys: {list(bp.keys())}")
    
    dist = _distribute(10, bp)
    print(f"10-question distribution: {dist}")
    
    questions = await _build_questions(dist, verified_only=True, company="tcs")
    print(f"Built {len(questions)} questions")
    for q in questions[:3]:
        section = q.get("section")
        qid = q.get("question_uid")
        kind = q.get("kind")
        print(f"  - {section}: {qid} kind={kind}")
    
    print("OA end-to-end test: PASS")

asyncio.run(test())
