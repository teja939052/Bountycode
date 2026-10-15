"""Test configuration."""
import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(autouse=True)
def _reset_rate_limiters():
    """Keep the in-process IP/login limiters from leaking across the suite.

    The rate limiter keys on client IP; every test shares one client
    (``testclient``), so the sliding window otherwise accumulates over the
    run and trips a 429 mid-suite. Reset both limiters around every test.
    """
    from app.middleware import rate_limiter

    rate_limiter.request_counts.clear()
    rate_limiter.login_attempts.clear()
    yield
    rate_limiter.request_counts.clear()
    rate_limiter.login_attempts.clear()
