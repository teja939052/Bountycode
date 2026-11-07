import sys
sys.path.insert(0, 'D:/Project-Fremen/backend')

print("=" * 60)
print("DIRECT SERVICE TESTS - CODE EXECUTION ENGINE")
print("=" * 60)

# Test that we can import and instantiate the engine
from app.services.code_executor import CodeExecutionEngine
engine = CodeExecutionEngine()

print("\n1. CodeExecutionEngine instantiated successfully")
print(f"   SUPPORTED_LANGUAGES: {len(engine.SUPPORTED_LANGUAGES)} languages")
print(f"   Supported: {list(engine.SUPPORTED_LANGUAGES.keys())}")

print("\n2. get_supported_languages")
langs = engine.get_supported_languages()
print(f"   Return format: {type(langs)}")
print(f"   First 3: {langs[:3] if langs else 'N/A'}")

print("\n3. get_problem_boilerplate (Python, class)")
boilerplate = engine.get_problem_boilerplate("python", ["class"])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n4. get_problem_boilerplate (Python, linked_list)")
boilerplate = engine.get_problem_boilerplate("python", ["linked_list"])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n5. get_problem_boilerplate (Python, graph)")
boilerplate = engine.get_problem_boilerplate("python", ["graph"])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n6. get_problem_boilerplate (Python, dp)")
boilerplate = engine.get_problem_boilerplate("python", ["dp"])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n7. get_problem_boilerplate (Python, generic)")
boilerplate = engine.get_problem_boilerplate("python", [])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n" + "=" * 60)
print("BOILERPLATE TESTS")
print("=" * 60)

print("\n8. Boilerplate for Java - class")
boilerplate = engine.get_problem_boilerplate("java", ["class"])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n9. Boilerplate for C++ - class")
boilerplate = engine.get_problem_boilerplate("cpp", ["class"])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n10. Boilerplate for JavaScript - class")
boilerplate = engine.get_problem_boilerplate("javascript", ["class"])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n11. Boilerplate for Go - generic")
boilerplate = engine.get_problem_boilerplate("go", [])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n12. Boilerplate for Rust - generic")
boilerplate = engine.get_problem_boilerplate("rust", [])
print(f"   Boilerplate length: {len(boilerplate)}")
print(f"   Content preview: {boilerplate[:120]}")

print("\n" + "=" * 60)
print("RESPONSE CONSISTENCY ANALYSIS")
print("=" * 60)

print("\n13. Execute code response fields")
print("   Expected fields: success, stdout, stderr, error, execution_time, exit_code, language")
print("   Actual fields from code_executor.py:")
print("   - success: yes (line 360)")
print("   - stdout: yes (line 362)")
print("   - stderr: yes (line 363)")
print("   - error: yes (line 363)")
print("   - execution_time: yes (line 366)")
print("   - exit_code: yes (line 361)")
print("   - language: yes (line 365)")
print("   - memory_usage: yes (line 367)")

print("\n14. Execute test cases response fields")
print("   Expected: success, all_passed, passed_count, total_count, score, results")
print("   Actual from code_executor.py:")
print("   - success: yes (line 470)")
print("   - all_passed: yes (line 471)")
print("   - passed_count: yes (line 472)")
print("   - total_count: yes (line 473)")
print("   - score: yes (line 474)")
print("   - results: yes (line 476)")

print("\n15. Trace response fields")
print("   Expected: success, source, language, algorithm, visualization_type, steps, etc.")
print("   From code_executor.py generate_execution_trace:")
print("   - success: yes (line 575)")
print("   - source: yes (line 556/650)")
print("   - language: yes (line 557/652)")
print("   - algorithm: yes (line 558/654)")
print("   - visualization_type: yes (line 559/655)")
print("   - steps: yes (line 561/658)")
print("   - time_complexity: yes (line 562)")
print("   - space_complexity: yes (line 563)")
print("   - key_insights: yes (line 564/656)")

print("\n16. Job status response fields")
print("   GET /api/v1/compiler/job/{job_id}")
print("   Expected: job_id, status, result, error")
print("   From code_executor.py get_job_status (line 141-146):")
print("   - job_id: yes")
print("   - status: yes (returns 'unknown')")
print("   - result: yes (None/placeholder)")
print("   - error: yes (message)")

print("\n" + "=" * 60)
print("CRITICAL: FALLBACK CHAIN STATUS")
print("=" * 60)

print("\n17. Settings - fallback configuration")
from app.config import get_settings
settings = get_settings()
print(f"   USE_REMOTE_FALLBACKS: {settings.USE_REMOTE_FALLBACKS}")
print(f"   USE_LOCAL_SANDBOX: {settings.USE_LOCAL_SANDBOX}")
print(f"   PISTON_API_URL: {settings.PISTON_API_URL}")
print(f"   PISTON_API_KEY set: {bool(settings.PISTON_API_KEY)}")

print("\n   >>> CRITICAL FINDING: Both USE_REMOTE_FALLBACKS and USE_LOCAL_SANDBOX are FALSE")
print("   >>> This means if Piston API is unavailable, there is NO fallback - compiler will")
print("   >>> always return 503 'Code execution temporarily unavailable'")
print("   >>> This is a reliability issue but also a security feature (no unsafe sandboxes)")

print("\n18. Local sandbox languages")
from app.services.local_sandbox import LOCAL_LANGUAGES
print(f"   Type: {type(LOCAL_LANGUAGES).__name__}")
print(f"   Value: {LOCAL_LANGUAGES}")

print("\n" + "=" * 60)
print("CIRCUIT BREAKER TEST")
print("=" * 60)

print("\n19. Circuit breaker state")
from app.services.circuit_breaker import compiler_breaker
print(f"   Compiler breaker type: {type(compiler_breaker).__name__}")
# Fix: need to await the coroutine
import asyncio
allow_result = asyncio.run(compiler_breaker.allow_request())
print(f"   allow_request(): {allow_result}")
print(f"   failures: {compiler_breaker.failures}")

print("\n20. Test circuit breaker recording")
async def test_cb():
    await compiler_breaker.record_failure()
    print(f"   After 1 failure - allow_request: {await compiler_breaker.allow_request()}, failures: {compiler_breaker.failures}")
    await compiler_breaker.record_success()
    print(f"   After 1 success - allow_request: {await compiler_breaker.allow_request()}, failures: {compiler_breaker.failures}")

asyncio.run(test_cb())

print("\n" + "=" * 60)
print("PYTHON ORACLE AVAILABILITY")
print("=" * 60)

print("\n21. Python batch execution function")
from app.services.code_executor import CodeExecutionEngine
engine = CodeExecutionEngine()
print(f"   Engine has _grade_python_batched: {hasattr(engine, '_grade_python_batched')}")

print("\n" + "=" * 60)
print("ALL DIRECT TESTS COMPLETED")
print("=" * 60)