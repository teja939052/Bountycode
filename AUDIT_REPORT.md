# PlacementPro Audit Report — Top 10 Remaining Issues

## 1. FORGOT PASSWORD IS COMPLETELY NON-FUNCTIONAL (CRITICAL)
**Impact:** Students cannot recover accounts. The "forgot password" UI exists but the backend never sends reset emails.

- `backend/app/routes/auth.py:160-176` — `forgot_password()` generates a token, stores it in MongoDB, and logs to console (`logger.info(f"Password reset requested for {req.email}")`). **No email is ever sent.**
- `backend/app/config.py:153-157` — SMTP settings exist but are never imported or used in the auth flow.
- `frontend/src/pages/ForgotPassword.tsx:18` — Shows success message regardless of whether the account exists (standard security practice), but the token is never delivered.
- `frontend/src/pages/ResetPassword.tsx:79-82` — The token input has `onChange={(e) => {}}`, making it read-only with no visual indication.

**Fix:** Wire up SMTP in `auth.py` to send the reset link, or integrate a service like SendGrid/Resend.

---

## 2. NO TOKEN REFRESH MECHANISM — SILENT LOGOUT AFTER 7 DAYS (CRITICAL)
**Impact:** Students doing intensive prep (placement season) are silently logged out mid-session after 7 days. No warning, no graceful redirect.

- `backend/app/config.py:18` — `JWT_EXPIRY_DAYS: int = 7`
- `backend/app/config.py:19` — `JWT_REFRESH_EXPIRY_DAYS: int = 30` — **This setting exists but is never used.**
- `backend/app/middleware/auth.py:72-81` — `create_refresh_token()` is defined but **dead code** — no `/refresh` endpoint, no refresh token cookie.
- `backend/app/routes/auth.py:69` — Login only creates an access token: `token = create_access_token(user_id)`.
- `frontend/src/services/api/request.ts:105-107` — On 401, throws `"Session expired"` with no retry or redirect logic.
- `frontend/src/store/authStore.ts:39-46` — `loadUser()` catches errors and just sets `user: null` — user is dropped to login with no context.

**Fix:** Add a `/api/v1/auth/refresh` endpoint, set a httpOnly refresh token cookie on login, and implement automatic silent refresh in `request.ts` before the access token expires.

---

## 3. `python-multipart` MISSING FROM `requirements.txt` (CRITICAL)
**Impact:** All file upload endpoints return 422 errors. Resume upload, profile picture upload, and any multipart form data is completely broken.

- `backend/requirements.txt` — 18 lines. **`python-multipart` is absent.**
- `backend/app/routes/resume.py:2,47` — Uses `UploadFile` and `File(...)` for resume uploads.
- `backend/app/routes/career_profile.py:2,71` — Uses `UploadFile = File(...)` for profile uploads.
- FastAPI requires `python-multipart` for `UploadFile` parsing. Without it, these endpoints fail at request parsing.

**Fix:** Add `python-multipart>=0.0.9` to `requirements.txt`.

---

## 4. STUDENT DASHBOARD SHOWS HARDCODED FAKE DATA (HIGH)
**Impact:** Students see LeetCode stats (347 solved, 72.4% acceptance, rank 12,453) and GFG stats that are completely fabricated. This destroys trust and makes the dashboard useless as a progress tracker.

- `frontend/src/pages/StudentDashboard.tsx:24-42` — `LEETCODE_STATS` and `GFG_STATS` are hardcoded constants with fake values.
- `frontend/src/pages/StudentDashboard.tsx:162-164` — API calls are made but `.catch(() => null)` and `.catch(() => [])` silently swallow failures.
- `frontend/src/pages/StudentDashboard.tsx:169` — `// Use mock data as fallback` — explicit comment confirming fake data is used when API fails.
- The page is routed as `/dashboard` in `App.tsx:166` — **this is the primary student landing page.**

**Fix:** Replace hardcoded constants with actual API data. If endpoints don't exist, create them. Never fall back to fake data silently.

---

## 5. NO `.dockerignore` FILE (HIGH)
**Impact:** Docker images include `node_modules`, `.git`, `venv`, `__pycache__`, `.env` files. This bloats images by 500MB+, slows builds, and risks leaking secrets.

- No `.dockerignore` found anywhere in the project.
- `backend/Dockerfile:15` — `COPY . .` copies everything including `.env`, `venv/`, `__pycache__/`, `.git/`.
- `docker-compose.yml:65` — `volumes: - ./backend:/app` mounts the entire directory including secrets.
- The frontend Dockerfile (referenced in `docker-compose.yml:72-74`) has the same issue.

**Fix:** Create `.dockerignore` with:
```
node_modules
.git
venv
__pycache__
.env
.env.*
dist
build
coverage
.idea
.vscode
*.pyc
*.pyo
.DS_Store
Thumbs.db
```

---

## 6. FRONTEND MEMORY CACHE GROWS UNBOUNDED (MEDIUM-HIGH)
**Impact:** In a long SPA session with many unique API calls, the `Map` in `request.ts` grows without limit, causing memory leaks.

- `frontend/src/services/api/request.ts:14` — `const memoryCache = new Map<string, { data: unknown; timestamp: number }>();`
- Lines 83-89 — TTL is checked only on **access**. Expired entries are deleted only when the same key is requested again.
- There is **no periodic cleanup**, no max size limit, and no eviction policy.
- With 100+ API modules in `services/api/index.ts`, a student browsing different pages will accumulate hundreds of cache entries.

**Fix:** Add a periodic cleanup interval (e.g., every 5 minutes) that iterates the Map and removes expired entries. Also add a max size with LRU eviction.

---

## 7. `_LazyCollection.__getattr__` MASKS TYPOS (MEDIUM)
**Impact:** Silent runtime bugs in database access. A developer typo like `users_collection.fidn_one()` will raise an AttributeError only at request time, not at import/startup.

- `backend/app/database.py:29-30` — `def __getattr__(self, item): return getattr(self._resolve(), item)`
- `backend/app/database.py:20` — `__slots__ = ("_name",)` — only `_name` is a valid attribute, everything else is proxied.
- 93 collection proxies are defined (lines 100-192). Any typo in method names (e.g., `fidn_one` instead of `find_one`) passes `__getattr__` and fails at runtime.
- This is explicitly called out in `AGENTS.md` P2: `_LazyCollection proxy uses __getattr__ magic which can mask typos`.

**Fix:** Add an explicit whitelist of allowed Motor collection methods in `__getattr__`, or switch to explicit `get_collection(name)` calls.

---

## 8. CSS BLOAT + THEME INCONSISTENCY (MEDIUM)
**Impact:** Slower initial paint, visual confusion for students. The CSS is 1024 lines with ~50 animation keyframes, many unused. The theme mixes dark "space" backgrounds with light cards and cyber colors inconsistently.

- `frontend/src/index.css` — **1024 lines** total.
  - Lines 414-593: Card rarity system (Pokemon/FreeFire style) — ~180 lines of animations (`cardGlowPulse`, `rainbowBorder`, `sparkle`, `holoShimmer`, `cardFloat`, `shineSweep`, etc.)
  - Lines 665-861: Pixel RPG theme — `pixelFloat`, `pixelBounce`, `glitch`, `scanline`, `borderGlow`, `xpBarGlow`
  - Lines 869-941: Juice system animations — `screenShake`, `screenPulse`, `screenSparkle`, `floatUp`, `particleFly`, `bounceIn`, `levelUpPulse`, `starSpin`, `streakBlaze`, `flameFlicker`, `badgeReveal`
- **Dead classes:** No references found for `.pixel-float`, `.pixel-bounce`, `.pixel-glitch`, `.scanline`, `.card-rpg`, `.xp-bar-glow` in JSX/TSX files.
- **Theme inconsistency:**
  - Body background: dark (`#0B1020` space black) with radial gradients — `index.css:25-31`
  - Cards: `bg-white` with `border-gray-100` — `index.css:153-157`
  - `SpaceBackground.tsx:32` uses warm light gradients (`#F9F5EF` → `#EFE8DF`)
  - Components mix `cyber-*` (dark theme: `cyber-blue`, `cyber-red`) with `brand-*` (light theme: `brand-sky`, `brand-coral`) classes
  - `tailwind.config.js:83-90` defines `space` colors as light (`void: "#F5F3EF"`), but `index.css:25` uses `--space-black: #0B1020`

**Fix:** Choose one theme direction (light or dark) and consolidate. Remove dead animation classes. Split `index.css` into feature-specific files.

---

## 9. RESET PASSWORD TOKEN FIELD HAS BROKEN UX (LOW-MEDIUM)
**Impact:** Students trying to reset passwords see a field they can't edit, with no explanation.

- `frontend/src/pages/ResetPassword.tsx:79-82` — Token input has `onChange={(e) => {}}`, making it non-interactive.
- The token comes from URL query params (line 7: `searchParams.get("token")`), but there's no visual indication that it's auto-filled from the email link.
- If the email link is broken or the token is missing, the field appears empty and non-editable, confusing users.

**Fix:** Make the token field explicitly read-only with `readOnly` attribute and a tooltip explaining it comes from the reset link. Better yet, hide it entirely and send it as a header/body param only.

---

## 10. INCONSISTENT LOADING/ERROR STATES ACROSS PAGES (LOW-MEDIUM)
**Impact:** Students experience jarring UI transitions. Some pages show skeletons, others show spinners, and errors are handled inconsistently.

- `frontend/src/pages/Dashboard.tsx:160-189` — Good: shows `Skeleton` components on load, error state with retry button.
- `frontend/src/pages/StudentDashboard.tsx:205-211` — Poor: only shows a centered `<Spinner />` during load.
- `frontend/src/pages/StudentDashboard.tsx:168-169` — Errors are silently swallowed: `catch(() => null)` and `// Use mock data as fallback`.
- `frontend/src/pages/AptitudeTest.tsx:76` — Uses a single `loading` boolean for both starting tests and submitting answers, causing the entire UI to freeze during answer submission.
- `frontend/src/components/ProtectedRoute.tsx:9-14` — Shows a generic `<Spinner />` during auth check, but there's no timeout or fallback if `loadUser()` hangs.

**Fix:** Standardize loading/error patterns. Create reusable `PageSkeleton`, `ErrorState`, and `EmptyState` components. Never silently fall back to mock data.

---

## Summary Table

| # | Issue | Severity | Files Affected | Student Impact |
|---|-------|----------|---------------|----------------|
| 1 | Forgot password never sends emails | CRITICAL | `auth.py`, `ForgotPassword.tsx`, `ResetPassword.tsx` | Cannot recover accounts |
| 2 | No token refresh, silent 7-day logout | CRITICAL | `auth.py`, `request.ts`, `authStore.ts` | Sudden logout mid-prep |
| 3 | `python-multipart` missing | CRITICAL | `requirements.txt`, `resume.py`, `career_profile.py` | Resume upload broken |
| 4 | StudentDashboard hardcoded fake data | HIGH | `StudentDashboard.tsx` | Misleading progress stats |
| 5 | No `.dockerignore` | HIGH | Project root | Bloated images, slow deploys |
| 6 | Memory cache unbounded growth | MEDIUM-HIGH | `request.ts` | Memory leak in SPA |
| 7 | `_LazyCollection.__getattr__` masks typos | MEDIUM | `database.py` | Silent runtime bugs |
| 8 | CSS bloat + theme inconsistency | MEDIUM | `index.css`, `SpaceBackground.tsx` | Slow load, visual confusion |
| 9 | ResetPassword token UX broken | LOW-MEDIUM | `ResetPassword.tsx` | User confusion |
| 10 | Inconsistent loading/error states | LOW-MEDIUM | Multiple pages | Jarring UX |
