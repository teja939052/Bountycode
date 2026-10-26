# Route Crash Fixes - Common Issues & Solutions

## Issue #1: Unhandled Exceptions in Route Handlers

### Problem:
```python
@router.post("/interview/start")
async def start_interview(user=Depends(get_current_user)):
    # If this fails, route crashes with 500
    result = await ai.generate_questions(user_id=user["_id"])
    return result
```

### Solution:
```python
from app.middleware.route_safety import safe_route, ResilientCallable

@router.post("/interview/start")
@safe_route(timeout=30)
async def start_interview(user=Depends(get_current_user)):
    try:
        # Wrap external calls with retry
        result = await ResilientCallable.call_with_retry(
            lambda: ai.generate_questions(user_id=user["_id"]),
            max_retries=3,
            timeout=30
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Interview start failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to start interview. Please try again."
        )
```

---

## Issue #2: Database Connection Timeout

### Problem:
```python
@router.get("/user/profile")
async def get_profile(user=Depends(get_current_user), db=Depends(get_db)):
    # If DB is slow, hangs forever
    user_data = await db["users"].find_one({"_id": user["_id"]})
    return user_data
```

### Solution:
```python
from app.middleware.route_safety import SafeDatabase

@router.get("/user/profile")
@safe_route(timeout=10)
async def get_profile(user=Depends(get_current_user), db=Depends(get_db)):
    safe_db = SafeDatabase(db)
    
    # Automatically handles timeout + error
    user_data = await safe_db.find_one("users", {"_id": user["_id"]})
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "data": user_data}
```

---

## Issue #3: Missing Required Fields

### Problem:
```python
@router.post("/interview/answer")
async def submit_answer(request: Request):
    data = await request.json()
    # Crashes if "interview_id" missing
    interview_id = data["interview_id"]
    answer = data["answer"]
    return {"success": True}
```

### Solution:
```python
from pydantic import BaseModel

class SubmitAnswerRequest(BaseModel):
    interview_id: str
    answer: str
    
    class Config:
        validate_assignment = True

@router.post("/interview/answer")
async def submit_answer(data: SubmitAnswerRequest, user=Depends(get_current_user)):
    # Fields validated by Pydantic before route code runs
    return {"success": True}
```

---

## Issue #4: JSON Parsing Errors

### Problem:
```python
@router.post("/resume/analyze")
async def analyze_resume(request: Request):
    # Crashes on invalid JSON
    data = await request.json()
    return process_resume(data)
```

### Solution:
```python
@router.post("/resume/analyze")
async def analyze_resume(request: Request):
    try:
        data = await request.json()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON in request body"
        )
    
    try:
        return await process_resume(data)
    except Exception as e:
        logger.error(f"Resume analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze resume"
        )
```

---

## Issue #5: Unauthenticated Access

### Problem:
```python
@router.get("/dashboard")
async def get_dashboard(user=Depends(get_current_user)):
    # Crashes if user is None (not logged in)
    user_id = user["_id"]
    return get_user_stats(user_id)
```

### Solution:
```python
from app.middleware.route_safety import ensure_user_exists

@router.get("/dashboard")
@ensure_user_exists
async def get_dashboard(user=Depends(get_current_user)):
    # User guaranteed to exist and have _id
    stats = await get_user_stats(user["_id"])
    return {"success": True, "data": stats}
```

---

## Issue #6: WebSocket Connection Drops

### Problem:
```python
@router.websocket("/ws/interview/{interview_id}")
async def websocket_interview(websocket: WebSocket, interview_id: str):
    await websocket.accept()
    while True:
        # If connection drops, crashes
        data = await websocket.receive_text()
        await send_response(data)
```

### Solution:
```python
@router.websocket("/ws/interview/{interview_id}")
async def websocket_interview(websocket: WebSocket, interview_id: str):
    try:
        await websocket.accept()
        
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=300  # 5 min timeout
                )
                
                try:
                    response = await send_response(data)
                    await websocket.send_json(response)
                except Exception as e:
                    logger.error(f"Send failed: {e}")
                    await websocket.send_json({"error": "Failed to process request"})
                    
            except asyncio.TimeoutError:
                logger.warning(f"WebSocket {interview_id} timeout")
                await websocket.close(code=1000, reason="Timeout")
                break
            
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break
    
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        try:
            await websocket.close()
        except:
            pass
```

---

## Issue #7: API Response Not JSON

### Problem:
```python
@router.get("/download/pdf")
async def download_pdf():
    # Returns file instead of JSON
    return FileResponse("resume.pdf")
```

### Solution:
```python
from fastapi import FileResponse
from fastapi.responses import StreamingResponse

@router.get("/download/pdf")
async def download_pdf(user=Depends(get_current_user)):
    try:
        pdf_content = await generate_pdf(user["_id"])
        
        return StreamingResponse(
            iter([pdf_content]),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=resume.pdf"}
        )
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate PDF"
        )
```

---

## Issue #8: Memory Leak / OOM

### Problem:
```python
# Global state accumulates without cleanup
interview_sessions = {}

@router.post("/interview/start")
async def start_interview(user=Depends(get_current_user)):
    # Sessions never cleaned up
    interview_sessions[user["_id"]] = {...}
    return {"success": True}
```

### Solution:
```python
import weakref
from typing import WeakKeyDictionary

# Use weak references + cleanup
interview_sessions: WeakKeyDictionary = WeakKeyDictionary()

@router.post("/interview/start")
async def start_interview(user=Depends(get_current_user)):
    user_id = user["_id"]
    
    # Auto-cleanup with context manager
    session = InterviewSession(user_id)
    interview_sessions[user] = session
    
    try:
        return await session.start()
    finally:
        # Cleanup
        if user in interview_sessions:
            del interview_sessions[user]

@router.post("/interview/cleanup/{interview_id}")
async def cleanup_interview(interview_id: str, user=Depends(get_current_user)):
    # Explicit cleanup after interview ends
    if user in interview_sessions:
        del interview_sessions[user]
    return {"success": True}
```

---

## Issue #9: Concurrent Request Conflicts

### Problem:
```python
@router.post("/billing/upgrade")
async def upgrade_to_pro(user=Depends(get_current_user)):
    # If user clicks twice, gets charged twice
    result = await paypal.charge(user["_id"], 9.99)
    await update_user_tier(user["_id"], "pro")
    return result
```

### Solution (Use Idempotency Keys):
```python
@router.post("/billing/upgrade")
async def upgrade_to_pro(
    user=Depends(get_current_user),
    idempotency_key: str = Header(...)
):
    from app.services.idempotency import get_idempotency_manager
    
    manager = get_idempotency_manager()
    
    # Check if already processed
    existing = await manager.get_operation_result(idempotency_key)
    if existing:
        return existing["result"]
    
    try:
        # Process payment
        result = await paypal.charge(user["_id"], 9.99)
        await update_user_tier(user["_id"], "pro")
        
        # Record success
        await manager.record_operation(
            idempotency_key,
            user["_id"],
            "upgrade_to_pro",
            "success",
            result=result
        )
        
        return result
    except Exception as e:
        # Record failure
        await manager.record_operation(
            idempotency_key,
            user["_id"],
            "upgrade_to_pro",
            "failed",
            error=str(e)
        )
        raise
```

---

## Issue #10: Rate Limit Not Enforced

### Problem:
```python
@router.post("/ai/generate")
async def generate_content(user=Depends(get_current_user)):
    # No limit - user can spam requests, expensive API calls
    return await ai.generate(user["_id"])
```

### Solution:
```python
from app.services.usage import check_usage_limit, record_usage

@router.post("/ai/generate")
async def generate_content(user=Depends(get_current_user), db=Depends(get_db)):
    # Check limit
    usage = await check_usage_limit(
        user["_id"],
        feature="ai_generate",
        limit_per_day=10,
        tier=user.get("tier", "free")
    )
    
    if usage["exceeded"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Limit reached. {usage['reset_in']}s until reset"
        )
    
    # Process
    result = await ai.generate(user["_id"])
    
    # Record usage
    await record_usage(user["_id"], "ai_generate")
    
    return {"success": True, "data": result}
```

---

## Quick Checklist for New Routes

Before deploying a new route, verify:

- [ ] All dependencies are explicitly declared (no implicit globals)
- [ ] External API calls wrapped with `ResilientCallable.call_with_retry()`
- [ ] Database operations wrapped with `SafeDatabase` or have try/catch
- [ ] All HTTP routes have status code (200, 201, 400, 401, 403, 404, 500, etc.)
- [ ] Request validation with Pydantic models
- [ ] Proper error responses (not raw exceptions)
- [ ] Logging for debugging
- [ ] Timeouts on all I/O operations
- [ ] User authentication check (if needed)
- [ ] Rate limiting (if expensive operation)
- [ ] No global state mutations
- [ ] Proper resource cleanup (files, connections, etc.)

---

## Integration into main.py

Add this to your `main.py` lifespan:

```python
from app.middleware.route_safety import RouteErrorHandlingMiddleware

# Add BEFORE other middleware
app.add_middleware(RouteErrorHandlingMiddleware)

# ... rest of middleware
```

This ensures all unhandled route errors are caught and converted to proper JSON responses.
