import bleach

ALLOWED_TAGS = []
ALLOWED_ATTRIBUTES = {}


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
