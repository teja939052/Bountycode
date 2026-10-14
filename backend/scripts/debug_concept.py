from unittest.mock import MagicMock, patch
from app.services import concept_engine
import json

frame = MagicMock()
frame.manipulate.target_variable = "score"
frame.manipulate.hint = "good hint"

fake_result = {
    "success": True,
    "stdout": '{"target": 10}\n',
    "stderr": "",
    "exit_code": 0,
}

with patch("app.services.concept_engine.execute_local_sync", return_value=fake_result) as mock_exec:
    # Manually trace through the function logic
    code = "score = 10"
    target = "score"
    wrapper = code + f"\nimport json\nprint(json.dumps({{'target': {target}}}))"
    print("wrapper:", repr(wrapper))
    
    run_result = fake_result
    stdout = run_result.get("stdout", "")
    print("stdout:", repr(stdout))
    
    marker = stdout.rfind("{")
    print("marker:", marker)
    
    if marker >= 0:
        try:
            data = json.loads(stdout[marker:])
            print("parsed data:", data)
            print("data.get('target'):", data.get("target"))
            print("data.get('target') is not None:", data.get("target") is not None)
        except Exception as e:
            print("json parse error:", e)
    
    # Now call the actual function
    correct, explanation = concept_engine._grade_manipulate_frame(frame, code)
    print("correct:", correct)
    print("explanation:", explanation)
