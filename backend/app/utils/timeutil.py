"""Shared datetime helpers.

All application timestamps are stored as *naive* UTC datetimes (matching
pymongo's default ``tz_aware=False`` behaviour). This helper produces the
same values as the deprecated ``datetime.utcnow()`` without triggering the
deprecation warning.
"""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return the current UTC time as a naive datetime (no tzinfo)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
