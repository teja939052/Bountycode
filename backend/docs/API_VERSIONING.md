# API Versioning Strategy

## Current State
All routes use the `/api/v1/` prefix, but there is no formal version negotiation or deprecation policy.

## Recommended Approach: URL Path Versioning

### Version Format
```
/api/v1/...
/api/v2/...
```

### Versioning Rules
1. **Breaking changes only** — New versions are created only for breaking changes (removing fields, changing response shapes, removing endpoints)
2. **Non-breaking changes are additive** — New fields, new endpoints, new optional parameters do not require a version bump
3. **Support window** — Each major version is supported for at least 12 months after the next major version is released
4. **Deprecation headers** — Deprecated endpoints return `Sunset` or `Deprecation` headers with the removal date

### Migration Process
1. Announce deprecation in changelog and via API response headers
2. Keep old version running alongside new version for 3 months
3. Update frontend to use new version
4. Remove old version after support window expires

### Current Version: v1
- Stable, production-ready
- All 65+ route files use `/api/v1/` prefix

### Planned v2 Changes (examples)
- Rename `interviews_used` → `usage.interviews` for consistency
- Standardize error response format with `code`, `message`, `details`, `request_id`
- Add pagination cursors for all list endpoints
- Add `fields` query parameter for sparse fieldsets

### Implementation
- Add `API_VERSION` constant in `config.py`
- Add version negotiation middleware (optional, for future-proofing)
- Add version deprecation utilities in `services/versioning.py`
