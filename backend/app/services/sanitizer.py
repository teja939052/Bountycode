import bleach
import re

ALLOWED_TAGS = []
ALLOWED_ATTRIBUTES = {}

# Patterns that suggest prompt injection attempts.
_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+DAN", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?prior\s+(instructions|rules)", re.IGNORECASE),
    re.compile(r"act\s+as\s+(if\s+you\s+are|an?)\s+", re.IGNORECASE),
    re.compile(r"pretend\s+(to\s+be|you\s+are)", re.IGNORECASE),
    re.compile(r"return\s+(the\s+)?(system|prompt|instructions)", re.IGNORECASE),
    re.compile(r"reveal\s+(your\s+)?(system|prompt|instructions)", re.IGNORECASE),
    re.compile(r"output\s+(your|the)\s+(system|prompt|instructions)", re.IGNORECASE),
]


def sanitize_text(value: str, max_length: int = 10000) -> str:
    if value is None:
        return ""
    text = str(value)[:max_length]
    stripped = bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )
    return stripped


def contains_prompt_injection(text: str) -> bool:
    if not text:
        return False
    lowered = str(text).lower()
    return any(pattern.search(lowered) for pattern in _INJECTION_PATTERNS)


def sanitize_prompt_input(value: str, max_length: int = 2000) -> str:
    """Sanitize user-controlled input before interpolating into AI prompts.

    Applies length capping, HTML/script stripping, and blocks known prompt
    injection phrases. Returns the cleaned string, or an empty string when the
    input is unsafe.
    """
    if value is None:
        return ""
    text = sanitize_text(value, max_length=max_length)
    if contains_prompt_injection(text):
        return ""
    return text
