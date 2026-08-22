"""Async-safe circuit breaker with configurable thresholds.

Implements the circuit breaker pattern to prevent cascading failures in
external service calls. Tracks consecutive failures and opens the circuit
after a threshold is reached, allowing recovery after a cooldown period.
"""
import asyncio
import time
import logging

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """Thread-safe async circuit breaker for protecting external calls.

    Args:
        name: Human-readable identifier for logging and metrics.
        threshold: Number of consecutive failures before opening the circuit.
        recovery_time: Cooldown seconds before allowing a half-open request.
    """

    def __init__(self, name: str, threshold: int = 5, recovery_time: float = 60.0):
        self.name = name
        self._threshold = threshold
        self._recovery_time = recovery_time
        self._failures = 0
        self._last_failure_time = 0.0
        self._is_open = False
        self._lock = asyncio.Lock()

    @property
    def is_open(self) -> bool:
        return self._is_open

    @is_open.setter
    def is_open(self, value: bool) -> None:
        self._is_open = value

    @property
    def failures(self) -> int:
        return self._failures

    @failures.setter
    def failures(self, value: int) -> None:
        self._failures = value

    @property
    def last_failure_time(self) -> float:
        return self._last_failure_time

    @last_failure_time.setter
    def last_failure_time(self, value: float) -> None:
        self._last_failure_time = value

    @property
    def threshold(self) -> int:
        return self._threshold

    @property
    def recovery_time(self) -> float:
        return self._recovery_time

    @property
    def state(self) -> dict:
        return {
            "name": self.name,
            "is_open": self._is_open,
            "failures": self._failures,
            "threshold": self._threshold,
            "recovery_time": self._recovery_time,
        }

    async def allow_request(self) -> bool:
        """Check if a request is allowed.

        Returns True if the circuit is closed, or if enough time has passed
        since the last failure to attempt recovery (half-open state).

        Returns:
            bool: True if the request should proceed, False if the circuit is open.
        """
        async with self._lock:
            if not self._is_open:
                return True
            elapsed = time.time() - self._last_failure_time
            if elapsed > self._recovery_time:
                self._is_open = False
                self._failures = 0
                logger.info(f"Circuit breaker '{self.name}' half-open, allowing request")
                return True
            return False

    async def record_failure(self) -> None:
        """Record a failure.

        Increments the failure counter. Opens the circuit if the threshold is reached.

        Raises:
            None directly, but logs a warning when the circuit opens.
        """
        async with self._lock:
            self._failures += 1
            self._last_failure_time = time.time()
            if self._failures >= self._threshold:
                self._is_open = True
                logger.warning(
                    f"Circuit breaker '{self.name}' opened after {self._failures} failures"
                )

    async def record_success(self) -> None:
        """Record a success.

        Resets the failure counter and closes the circuit.
        """
        async with self._lock:
            self._failures = 0
            self._is_open = False


# Pre-configured breakers
ai_breaker = CircuitBreaker("ai", threshold=5, recovery_time=60)
compiler_breaker = CircuitBreaker("compiler", threshold=5, recovery_time=45)
