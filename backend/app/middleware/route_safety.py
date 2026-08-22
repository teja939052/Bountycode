"""
Middleware and utilities to prevent route crashes and provide graceful error recovery.
Handles validation errors, database errors, timeout issues, and more.
"""

import logging
from typing import Optional, Callable, Any
from functools import wraps
import asyncio
import traceback

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RouteErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to catch all route errors and convert to proper HTTP responses.
    Prevents 500 crashes from becoming unhandled exceptions.
    """
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await asyncio.wait_for(call_next(request), timeout=60.0)
            return response
            
        except asyncio.TimeoutError:
            logger.error(f"Route timeout: {request.method} {request.url.path}")
            return JSONResponse(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                content={
                    "success": False,
                    "error": {
                        "code": 504,
                        "message": "Request timeout",
                        "retriable": True,
                    }
                }
            )
        
        except HTTPException:
            raise  # Let FastAPI handle HTTPExceptions
        
        except Exception as e:
            logger.error(
                f"Unhandled route error: {request.method} {request.url.path}\n{traceback.format_exc()}"
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": {
                        "code": 500,
                        "message": "An unexpected error occurred",
                        "details": str(e) if __debug__ else "Internal server error",
                        "retriable": False,
                    }
                }
            )


def safe_route(timeout: int = 30):
    """
    Decorator for route handlers to add timeout, validation, and error handling.
    
    Usage:
        @router.post("/interview/start")
        @safe_route(timeout=30)
        async def start_interview(data: StartInterviewRequest):
            # Your code
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Execute with timeout
                result = await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=timeout
                )
                return result
                
            except asyncio.TimeoutError:
                logger.error(f"Route timeout: {func.__name__}")
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail="Request took too long to process"
                )
            
            except ValueError as e:
                # Validation errors
                logger.warning(f"Validation error in {func.__name__}: {e}")
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=str(e)
                )
            
            except KeyError as e:
                # Missing required field
                logger.warning(f"Missing field in {func.__name__}: {e}")
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Missing required field: {e.args[0]}"
                )
            
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {traceback.format_exc()}")
                # Re-raise if HTTPException, otherwise convert to 500
                if isinstance(e, HTTPException):
                    raise
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error"
                )
        
        return wrapper
    return decorator


class SafeDatabase:
    """
    Wrapper for database operations to handle common errors gracefully.
    """
    
    def __init__(self, db):
        self.db = db
    
    async def find_one(self, collection: str, query: dict, timeout: int = 10):
        """Find single document with error handling."""
        try:
            collection_obj = self.db[collection]
            result = await asyncio.wait_for(
                collection_obj.find_one(query),
                timeout=timeout
            )
            return result
        except asyncio.TimeoutError:
            logger.error(f"Database timeout on find_one({collection})")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is slow, please try again"
            )
        except Exception as e:
            logger.error(f"Database error on find_one({collection}): {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database error"
            )
    
    async def insert_one(self, collection: str, doc: dict, timeout: int = 10):
        """Insert document with error handling."""
        try:
            collection_obj = self.db[collection]
            result = await asyncio.wait_for(
                collection_obj.insert_one(doc),
                timeout=timeout
            )
            return result.inserted_id
        except asyncio.TimeoutError:
            logger.error(f"Database timeout on insert_one({collection})")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is slow, please try again"
            )
        except Exception as e:
            logger.error(f"Database error on insert_one({collection}): {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to save data"
            )
    
    async def update_one(self, collection: str, query: dict, update: dict, timeout: int = 10):
        """Update document with error handling."""
        try:
            collection_obj = self.db[collection]
            result = await asyncio.wait_for(
                collection_obj.update_one(query, update),
                timeout=timeout
            )
            return result.modified_count
        except asyncio.TimeoutError:
            logger.error(f"Database timeout on update_one({collection})")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is slow, please try again"
            )
        except Exception as e:
            logger.error(f"Database error on update_one({collection}): {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to update data"
            )
    
    async def find(self, collection: str, query: dict, limit: int = None, timeout: int = 10):
        """Find multiple documents with error handling."""
        try:
            collection_obj = self.db[collection]
            cursor = collection_obj.find(query)
            if limit:
                cursor = cursor.limit(limit)
            
            result = await asyncio.wait_for(
                cursor.to_list(length=limit or None),
                timeout=timeout
            )
            return result
        except asyncio.TimeoutError:
            logger.error(f"Database timeout on find({collection})")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database query timeout"
            )
        except Exception as e:
            logger.error(f"Database error on find({collection}): {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database error"
            )


def validate_request(required_fields: list[str]):
    """
    Decorator to validate required fields in request.
    
    Usage:
        @router.post("/interview/answer")
        @validate_request(["interview_id", "answer"])
        async def submit_answer(data: dict):
            # Fields guaranteed to exist
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, request: Request = None, **kwargs):
            if request and hasattr(request, 'json'):
                try:
                    body = await request.json()
                    missing = [f for f in required_fields if f not in body]
                    if missing:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Missing required fields: {', '.join(missing)}"
                        )
                except ValueError as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid JSON in request body"
                    )
            
            return await func(*args, request=request, **kwargs)
        
        return wrapper
    return decorator


class ResilientCallable:
    """
    Make external API calls resilient to failures.
    """
    
    @staticmethod
    async def call_with_retry(
        func: Callable,
        max_retries: int = 3,
        backoff_ms: int = 500,
        timeout: int = 30
    ) -> Any:
        """
        Call function with automatic retry and timeout.
        """
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                return await asyncio.wait_for(func(), timeout=timeout)
            
            except asyncio.TimeoutError as e:
                last_error = e
                if attempt < max_retries:
                    wait_time = (backoff_ms * (2 ** attempt)) / 1000
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after timeout")
                    await asyncio.sleep(wait_time)
                continue
            
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    wait_time = (backoff_ms * (2 ** attempt)) / 1000
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after error: {e}")
                    await asyncio.sleep(wait_time)
                continue
        
        raise last_error or Exception("Max retries exceeded")


def ensure_user_exists(func: Callable) -> Callable:
    """Decorator to ensure user exists before processing."""
    @wraps(func)
    async def wrapper(user=None, *args, **kwargs):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated"
            )
        
        if not user.get("_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        
        return await func(user=user, *args, **kwargs)
    
    return wrapper


def ensure_valid_input(schema_class):
    """Decorator to validate input against Pydantic schema."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(data=None, *args, **kwargs):
            try:
                if isinstance(data, dict):
                    validated = schema_class(**data)
                else:
                    validated = data
                
                return await func(data=validated, *args, **kwargs)
            
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid input: {str(e)}"
                )
        
        return wrapper
    return decorator
