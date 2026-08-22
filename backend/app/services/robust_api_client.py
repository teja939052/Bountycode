"""
Robust API client for React-FastAPI communication.
Features: Retry logic, connection pooling, timeout management, circuit breaker.
"""

import asyncio
import time
from typing import Optional, Dict, Any, Callable
from enum import Enum
import logging
from datetime import datetime, timedelta

from app.utils.timeutil import utcnow

logger = logging.getLogger(__name__)


class RetryStrategy(Enum):
    """Retry strategy types."""
    EXPONENTIAL = "exponential"  # 1s, 2s, 4s, 8s...
    LINEAR = "linear"  # 1s, 2s, 3s, 4s...
    FIXED = "fixed"  # 1s, 1s, 1s, 1s...
    NONE = "none"


class APIClientConfig:
    """Configuration for robust API client."""
    
    # Connection settings
    TIMEOUT_SECONDS = 30
    CONNECT_TIMEOUT_SECONDS = 10
    
    # Retry settings
    MAX_RETRIES = 3
    RETRY_STRATEGY = RetryStrategy.EXPONENTIAL
    RETRY_BACKOFF_MS = 500  # Initial backoff
    RETRY_MAX_BACKOFF_MS = 10000  # Max backoff
    
    # Circuit breaker
    CIRCUIT_BREAKER_FAILURE_THRESHOLD = 5
    CIRCUIT_BREAKER_RECOVERY_TIMEOUT = 60  # seconds
    
    # Request/Response
    POOL_CONNECTIONS = 10
    POOL_MAXSIZE = 20
    MAX_REQUEST_SIZE_MB = 50
    
    # Retriable status codes
    RETRIABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}
    
    # Non-retriable status codes
    NON_RETRIABLE_STATUS_CODES = {400, 401, 403, 404, 422}


class CircuitBreakerState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


class RequestCircuitBreaker:
    """Circuit breaker for API requests."""
    
    def __init__(self, endpoint: str, config: APIClientConfig):
        self.endpoint = endpoint
        self.config = config
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.last_recovery_attempt = None
    
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitBreakerState.OPEN:
            # Check if recovery timeout has passed
            if self._should_attempt_recovery():
                self.state = CircuitBreakerState.HALF_OPEN
            else:
                raise Exception(f"Circuit breaker OPEN for {self.endpoint}")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_recovery(self) -> bool:
        """Check if enough time has passed to attempt recovery."""
        if not self.last_failure_time:
            return True
        
        elapsed = (utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.config.CIRCUIT_BREAKER_RECOVERY_TIMEOUT
    
    def _on_success(self):
        """Handle successful request."""
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
    
    def _on_failure(self):
        """Handle failed request."""
        self.failure_count += 1
        self.last_failure_time = utcnow()
        
        if self.failure_count >= self.config.CIRCUIT_BREAKER_FAILURE_THRESHOLD:
            self.state = CircuitBreakerState.OPEN
            logger.warning(f"Circuit breaker OPEN for {self.endpoint}")


class RobustAPIClient:
    """
    Robust API client with:
    - Automatic retry logic
    - Connection pooling
    - Timeout management
    - Circuit breaker
    - Request validation
    - Error recovery
    """
    
    def __init__(self, base_url: str, config: Optional[APIClientConfig] = None):
        self.base_url = base_url
        self.config = config or APIClientConfig()
        self.circuit_breakers: Dict[str, RequestCircuitBreaker] = {}
        self.session = None
        self.request_timeout = (
            self.config.CONNECT_TIMEOUT_SECONDS,
            self.config.TIMEOUT_SECONDS
        )
    
    def _get_circuit_breaker(self, endpoint: str) -> RequestCircuitBreaker:
        """Get or create circuit breaker for endpoint."""
        if endpoint not in self.circuit_breakers:
            self.circuit_breakers[endpoint] = RequestCircuitBreaker(endpoint, self.config)
        return self.circuit_breakers[endpoint]
    
    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate backoff time in milliseconds."""
        if self.config.RETRY_STRATEGY == RetryStrategy.FIXED:
            backoff = self.config.RETRY_BACKOFF_MS
        elif self.config.RETRY_STRATEGY == RetryStrategy.LINEAR:
            backoff = self.config.RETRY_BACKOFF_MS * (attempt + 1)
        else:  # EXPONENTIAL
            backoff = self.config.RETRY_BACKOFF_MS * (2 ** attempt)
        
        # Cap at max backoff
        backoff = min(backoff, self.config.RETRY_MAX_BACKOFF_MS)
        
        # Add jitter (±10%)
        jitter = backoff * 0.1 * (2 * (time.time() % 1) - 1)
        return (backoff + jitter) / 1000  # Convert to seconds
    
    def _should_retry(self, status_code: int, attempt: int) -> bool:
        """Determine if request should be retried."""
        # Max retries reached
        if attempt >= self.config.MAX_RETRIES:
            return False
        
        # Non-retriable status codes
        if status_code in self.config.NON_RETRIABLE_STATUS_CODES:
            return False
        
        # Retriable status codes
        if status_code in self.config.RETRIABLE_STATUS_CODES:
            return True
        
        # All 5xx errors are retriable
        if status_code >= 500:
            return True
        
        return False
    
    async def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        retries: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with automatic retry, circuit breaker, and error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/api/auth/login")
            data: Request body
            headers: Custom headers
            retries: Override max retries
        
        Returns:
            Response JSON
        
        Raises:
            APIError: On failure after all retries
        """
        import httpx
        
        max_retries = retries if retries is not None else self.config.MAX_RETRIES
        url = f"{self.base_url}{endpoint}"
        
        # Get circuit breaker for this endpoint
        cb = self._get_circuit_breaker(endpoint)
        
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                # Circuit breaker check
                if cb.state == CircuitBreakerState.OPEN:
                    if not cb._should_attempt_recovery():
                        raise APIError(
                            status_code=503,
                            message=f"Service temporarily unavailable ({endpoint})",
                            retriable=True
                        )
                
                # Make request
                async with httpx.AsyncClient(
                    timeout=self.request_timeout,
                    limits=httpx.Limits(
                        max_connections=self.config.POOL_CONNECTIONS,
                        max_keepalive_connections=self.config.POOL_MAXSIZE
                    )
                ) as client:
                    response = await client.request(
                        method,
                        url,
                        json=data,
                        headers=headers or {}
                    )
                
                # Handle response
                if response.status_code < 400:
                    # Success
                    cb._on_success()
                    return response.json() if response.text else {}
                
                elif self._should_retry(response.status_code, attempt):
                    # Retriable error - retry
                    cb._on_failure()
                    backoff = self._calculate_backoff(attempt)
                    logger.warning(
                        f"Retry {attempt + 1}/{max_retries} for {method} {endpoint} "
                        f"(status {response.status_code}), backoff {backoff:.1f}s"
                    )
                    await asyncio.sleep(backoff)
                    continue
                
                else:
                    # Non-retriable error
                    cb._on_failure()
                    try:
                        error_data = response.json()
                    except:
                        error_data = {"message": response.text}
                    
                    raise APIError(
                        status_code=response.status_code,
                        message=error_data.get("message", "Unknown error"),
                        details=error_data,
                        retriable=False
                    )
            
            except (TimeoutError, ConnectionError) as e:
                # Connection errors are retriable
                cb._on_failure()
                last_exception = e
                
                if attempt < max_retries:
                    backoff = self._calculate_backoff(attempt)
                    logger.warning(
                        f"Connection error on {method} {endpoint}: {e}. "
                        f"Retry {attempt + 1}/{max_retries}, backoff {backoff:.1f}s"
                    )
                    await asyncio.sleep(backoff)
                    continue
                else:
                    raise APIError(
                        status_code=504,
                        message="Connection timeout",
                        details={"error": str(e)},
                        retriable=True
                    )
            
            except APIError:
                raise
            
            except Exception as e:
                # Unexpected error
                cb._on_failure()
                logger.error(f"Unexpected error on {method} {endpoint}: {e}")
                raise APIError(
                    status_code=500,
                    message="Internal server error",
                    details={"error": str(e)},
                    retriable=False
                )
        
        # All retries exhausted
        if last_exception:
            raise APIError(
                status_code=504,
                message="Request failed after all retries",
                details={"error": str(last_exception)},
                retriable=True
            )


class APIError(Exception):
    """API error with retriability information."""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        details: Optional[Dict] = None,
        retriable: bool = False
    ):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        self.retriable = retriable
        super().__init__(message)
    
    def to_dict(self):
        """Convert to dictionary for logging/response."""
        return {
            "status_code": self.status_code,
            "message": self.message,
            "details": self.details,
            "retriable": self.retriable,
        }
