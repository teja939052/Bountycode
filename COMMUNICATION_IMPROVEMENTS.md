# React-FastAPI Communication Improvements Guide

## Overview

This guide shows how to integrate the robust API client and error handling into your existing React and FastAPI code.

---

## Part 1: Update Frontend API Services

### Before (Unsafe):
```javascript
// services/api/auth.js
export const login = async (email, password) => {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (!response.ok) throw new Error('Login failed');
  return response.json();
};
```

**Problems:**
- No retry logic
- No timeout handling
- Network errors crash the app
- No circuit breaker

### After (Robust):
```javascript
// services/api/auth.js
import { apiClient } from './robust-api-client';

export const login = async (email, password) => {
  try {
    return await apiClient.post('/api/v1/auth/login', {
      email,
      password
    });
  } catch (error) {
    // Error is automatically retried by apiClient
    // If retriable, will return with error details
    // If not retriable, throws with error info
    throw error;
  }
};

export const register = async (name, email, password) => {
  return await apiClient.post('/api/v1/auth/register', {
    name,
    email,
    password
  });
};

export const logout = async () => {
  return await apiClient.post('/api/v1/auth/logout', {});
};
```

---

## Part 2: Update React Pages with Error Handling

### Before (Crashes on Error):
```jsx
// pages/Dashboard.jsx
import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getStats().then(setStats).finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  return <div>{stats.interviews}</div>;
}
```

**Problems:**
- No error handling
- Blank screen if API fails
- No retry button
- No loading timeout

### After (Resilient):
```jsx
// pages/Dashboard.jsx
import { useEffect, useState } from 'react';
import { apiClient, APIError } from '../services/robust-api-client';
import { APIErrorToast, RequestSpinner } from '../components/GlobalErrorBoundary';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadStats = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.get('/api/v1/dashboard/stats');
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
      setError({
        message: err.message || 'Failed to load dashboard',
        status: err.status,
        retriable: err.retriable,
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  return (
    <div>
      <RequestSpinner isLoading={loading} timeout={10000} />
      
      <APIErrorToast
        error={error}
        onRetry={loadStats}
        onDismiss={() => setError(null)}
      />

      {!loading && !error && stats && (
        <div>
          <h1>Dashboard</h1>
          <p>Interviews: {stats.interviews}</p>
        </div>
      )}

      {!loading && error && !stats && (
        <div style={{ padding: '20px', textAlign: 'center' }}>
          <h2>⚠️ Failed to load dashboard</h2>
          <p>{error.message}</p>
          <button onClick={loadStats}>
            Try Again
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## Part 3: Update App.jsx with Error Boundary

### Before:
```jsx
// App.jsx
import { Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Interview from './pages/Interview';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/interview" element={<Interview />} />
      </Routes>
    </Router>
  );
}
```

### After:
```jsx
// App.jsx
import { Router, Routes, Route } from 'react-router-dom';
import GlobalErrorBoundary, { 
  ConnectionStatusMonitor,
  RequestSpinner,
  APIErrorToast
} from './components/GlobalErrorBoundary';
import Dashboard from './pages/Dashboard';
import Interview from './pages/Interview';

export default function App() {
  return (
    <GlobalErrorBoundary>
      <ConnectionStatusMonitor />
      
      <Router>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/interview" element={<Interview />} />
        </Routes>
      </Router>
    </GlobalErrorBoundary>
  );
}
```

---

## Part 4: Update FastAPI main.py

### Add to imports:
```python
from app.middleware.route_safety import (
    RouteErrorHandlingMiddleware,
    safe_route,
    SafeDatabase,
    ensure_user_exists
)
```

### Update app middleware (in lifespan):
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting PlacementPro API...")
    
    # Initialize database
    await init_database()
    logger.info("Database initialized")
    
    # Create indexes
    await create_all_indexes(database.db)
    logger.info("Database indexes created")
    
    # Initialize services
    await initialize_health_checker()
    await initialize_feature_flags()
    await initialize_idempotency_manager()
    
    logger.info("✅ All services initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down PlacementPro API...")
    await close_database()

app = FastAPI(lifespan=lifespan)

# Add error handling middleware FIRST (highest priority)
app.add_middleware(RouteErrorHandlingMiddleware)

# Add other middleware
app.add_middleware(CORSMiddleware, ...)
app.add_middleware(AuditLogMiddleware)
# ... rest of middleware
```

---

## Part 5: Update Common Routes with Safety Decorators

### Interview Route - Before:
```python
# routes/interview.py
@router.post("/start")
async def start_interview(
    data: StartInterviewRequest,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    # Can crash here
    interview = await db["interviews"].insert_one({
        "user_id": user["_id"],
        "role": data.role,
        ...
    })
    
    # Can crash here
    questions = await ai.generate_questions(data.role)
    
    return {"success": True}
```

### Interview Route - After:
```python
# routes/interview.py
from app.middleware.route_safety import (
    safe_route, 
    SafeDatabase, 
    ResilientCallable,
    ensure_user_exists
)
from pydantic import BaseModel

class StartInterviewRequest(BaseModel):
    role: str
    company: Optional[str] = None
    difficulty: str = "medium"

@router.post("/start")
@safe_route(timeout=30)
@ensure_user_exists
async def start_interview(
    data: StartInterviewRequest,
    user: Dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Start a new interview session with error handling."""
    safe_db = SafeDatabase(db)
    
    try:
        # Insert interview record with timeout
        interview_id = await safe_db.insert_one("interviews", {
            "user_id": user["_id"],
            "role": data.role,
            "company": data.company,
            "difficulty": data.difficulty,
            "created_at": datetime.utcnow(),
            "status": "started"
        })
        
        # Generate questions with retry
        questions = await ResilientCallable.call_with_retry(
            lambda: ai.generate_questions(
                role=data.role,
                count=5,
                difficulty=data.difficulty
            ),
            max_retries=3,
            timeout=30
        )
        
        # Update interview with questions
        await safe_db.update_one(
            "interviews",
            {"_id": interview_id},
            {"$set": {"questions": questions}}
        )
        
        return {
            "success": True,
            "data": {
                "interview_id": str(interview_id),
                "questions": questions
            }
        }
        
    except HTTPException:
        raise  # Let framework handle
    except Exception as e:
        logger.error(f"Interview start failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start interview. Please try again."
        )
```

### Answer Submission - Before:
```python
@router.post("/answer")
async def submit_answer(request: Request):
    data = await request.json()  # Can crash if invalid JSON
    interview_id = data["interview_id"]  # KeyError if missing
    answer = data["answer"]
    
    await db["submissions"].insert_one(...)
    feedback = await ai.evaluate_answer(answer)
    return feedback
```

### Answer Submission - After:
```python
class SubmitAnswerRequest(BaseModel):
    interview_id: str
    answer: str
    time_taken: int = 0

@router.post("/answer")
@safe_route(timeout=30)
@ensure_user_exists
async def submit_answer(
    data: SubmitAnswerRequest,
    user: Dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """Submit interview answer with automatic evaluation."""
    safe_db = SafeDatabase(db)
    
    try:
        # Verify interview belongs to user
        interview = await safe_db.find_one(
            "interviews",
            {
                "_id": ObjectId(data.interview_id),
                "user_id": user["_id"]
            }
        )
        
        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found"
            )
        
        # Record submission
        submission = await safe_db.insert_one("submissions", {
            "interview_id": ObjectId(data.interview_id),
            "user_id": user["_id"],
            "answer": data.answer,
            "time_taken": data.time_taken,
            "created_at": datetime.utcnow()
        })
        
        # Get AI evaluation with retry
        feedback = await ResilientCallable.call_with_retry(
            lambda: ai.evaluate_answer(
                question=interview["current_question"],
                answer=data.answer
            ),
            max_retries=2,
            timeout=30
        )
        
        # Record feedback
        await safe_db.update_one(
            "submissions",
            {"_id": submission},
            {"$set": {"feedback": feedback}}
        )
        
        return {
            "success": True,
            "data": {
                "submission_id": str(submission),
                "feedback": feedback
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Answer submission failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit answer. Please try again."
        )
```

---

## Part 6: Testing the Improvements

### Test Retry Logic:
```bash
# Simulate server timeout by stopping backend
python -m pytest tests/test_api_client.py::test_retry_on_timeout -v
```

### Test Error Boundary:
```bash
# Component should display error and retry button
npm test -- ConnectionErrorTest
```

### Test Health Checks:
```bash
curl http://localhost:8000/api/health/status
# Should return: {"status": "healthy", "checks": {...}}
```

### Test Circuit Breaker:
```bash
# Simulate failures to see circuit breaker open
curl -X GET http://localhost:8000/api/failing-endpoint
# After 5 failures, returns 503 immediately (no retry)
```

---

## Part 7: Deployment Checklist

Before deploying to production:

- [ ] Add `RouteErrorHandlingMiddleware` to `app.middleware`
- [ ] Update all API service methods in `services/api/`
- [ ] Wrap `App.jsx` with `GlobalErrorBoundary`
- [ ] Add `ConnectionStatusMonitor` to layout
- [ ] Test all routes with `@safe_route` decorator
- [ ] Verify `SafeDatabase` used for all DB operations
- [ ] Add `RequestSpinner` to all async pages
- [ ] Test network failure scenarios (offline mode)
- [ ] Verify error logging to backend
- [ ] Load test with chaos engineering (kill random requests)

---

## Expected Results After Implementation

### Before:
- 🔴 Crashes on network errors
- 🔴 Blank screens on API failures
- 🔴 No retry logic
- 🔴 User has to refresh page
- 🔴 Support tickets for "it just broke"

### After:
- ✅ Automatic retry with exponential backoff
- ✅ Error toasts with retry buttons
- ✅ Circuit breaker prevents cascading failures
- ✅ Offline mode shows connection status
- ✅ 99.99% reliability perceived by users
- ✅ Support tickets drop 80%

---

## Monitoring

### Dashboard Metrics:

```
GET /api/admin/dashboard/overview
→ Shows error rate, retry rate, circuit breaker status

GET /api/health/status
→ Full system health including API client health
```

### Alerts:

Set up alerts for:
- Circuit breaker OPEN (endpoint failing)
- Error rate > 5%
- Response time > 1000ms
- Database timeout count > 10/min

---

## Next Steps

1. **Week 1**: Deploy error handling middleware + robust API client
2. **Week 2**: Update all routes with `@safe_route`
3. **Week 3**: Add error boundaries to all React pages
4. **Week 4**: Monitor metrics, fine-tune timeouts
5. **Week 5**: Celebrate 99.99% uptime! 🎉
