import sys
import asyncio
sys.path.insert(0, r"D:\Project-Fremen\backend")

async def test():
    from app.services.journey_engine import build_journey_state
    from app.middleware.auth import get_current_user
    
    # Mock a user
    class MockUser:
        id = "test_user_123"
        email = "test@example.com"
        name = "Test User"
        plan = "free"
    
    # We need to test with actual DB, but let's just verify the function signature works
    # by checking it's callable
    print(f"build_journey_state is callable: {callable(build_journey_state)}")
    print("Import and basic check OK")

asyncio.run(test())