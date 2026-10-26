# DEPLOY CHECKLIST — Atlas / Render / Cloudflare Pages / GCP compiler
(prepared, not executed)

Nothing here has been run. Work top to bottom when accounts exist; each
step states exactly what to click/set. Prepped 2026-09-18 against
`backend/app/config.py`, `backend/.env.example`, `backend/render.yaml`,
`frontend/public/_redirects`, `frontend/public/_headers`,
`frontend/functions/api/[[path]].js`,
`frontend/src/services/api/request.ts`, `backend/compiler-service/`.

Hosting map (locked): frontend → Cloudflare Pages, API → Render,
compiler microservice → Google Cloud Run free tier, database → Atlas.

## 0. Preconditions (already true in tree)

- [ ] `render.yaml`: plan `starter` (not free — free sleep = OA cold-start
      timeouts), Python 3.12 (matches CI + Dockerfile), health check
      `/api/v1/health/live`, `MONGODB_URL` (the app ignores `MONGODB_URI`),
      `DATABASE_NAME=placementpro`, `USE_LOCAL_SANDBOX=true`.
- [ ] `frontend/vercel.json` rewrite still points at
      `REPLACE-WITH-YOUR-RENDER-URL` — dead file for this hosting map
      (Cloudflare uses `public/_redirects` + Functions instead); update or
      remove only if nothing else references Vercel.
- [ ] Frontend API base is `VITE_API_URL` (`services/api/request.ts`,
      `services/errorTracker.ts`). Empty (default) routes through the
      same-origin Pages Function proxy — preferred. No other base-URL
      wiring to hunt for.

## 1. Atlas (MongoDB)

1. Create cluster (M0 is fine for first deploy; M10+ when 72 users grow).
2. Database Access → user with readWrite on `placementpro` (NOT atlasAdmin).
3. Network Access → allow Render egress (0.0.0.0/0 if no static IPs).
4. Connect → Drivers → Python → copy SRV string. It must land in
   Render as `MONGODB_URL`, with `DATABASE_NAME=placementpro` alongside it.
5. Verify the live data is under `placementpro` (72 users), not the phantom
   `BountyCode` database the old config pointed at. Do NOT rename anything —
   config was matched to reality, not the reverse.
6. Confirm the startup migration creates the sparse `users.uid` index on
   `placementpro` (it previously targeted the phantom DB — fixed in
   `app/services/migrations.py`).

## 2. Render (API)

1. New → Blueprint → point at repo (`backend/render.yaml`).
2. Plan: **starter or higher** (the paid-tier call — free spin-down breaks
   timed OA sections on cold start; no code fix substitutes).
3. Set secret env vars (Dashboard → Environment, all `sync: false`):
   `MONGODB_URL`, `JWT_SECRET` (64-char random, new — never reuse dev),
   `OPENROUTER_API_KEY`, `PAYPAL_CLIENT_ID/SECRET/WEBHOOK_ID` (sandbox ok
   for first deploy), `STRIPE_*` only if billing goes live day one.
4. Set `CORS_ORIGINS=https://<your-vercel-app>.vercel.app` (exact origin,
   no trailing slash) and keep `COOKIE_SAMESITE=none` (cross-origin auth
   cookies will not send without it).
5. Optional but recommended: `GOOGLE_*` (OAuth callback must be the Render
   URL: `https://<api>.onrender.com/api/v1/auth/google/callback`),
   `USE_REMOTE_FALLBACKS=true` (+ `JUDGE0_URL/KEY` if available) for
   compiler resilience beyond the local sandbox.
6. Safe to skip on first deploy (all degrade gracefully, verified in
   `app/main.py` lifespan + `services/email.py`): `REDIS_URL` (falls back
   to in-memory cache/rate-limit; revisit for multi-instance scale),
   `RABBITMQ_URL` (falls back to sync code execution), `SMTP_*` (password
   resets log to outbox file instead of sending — real reset emails need
   SMTP before users depend on them).
7. Frontend: leave `VITE_ASYNC_COMPILER` unset (sync execution path —
   matches the no-RabbitMQ first deploy).
8. Deploy → confirm `/api/v1/health/live` 200 and `/api/v1/health/ready`
   output; note the final `https://<api>.onrender.com` URL for step 3.

## 3. Cloudflare Pages (frontend)

1. Pages → Create → Connect to Git → repo, root directory `frontend`,
   build `npm run build`, output `dist`. SPA routing is already handled by
   `public/_redirects` (`/* /index.html 200`); do NOT add a `404.html`
   (known Pages bug: it breaks SPA fallback). Security/cache headers ship
   via `public/_headers`.
2. Pages → Settings → Environment variables: leave `VITE_API_URL` EMPTY
   (default path — the app calls same-origin `/api/*`, served by
   `functions/api/[[path]].js` proxying to Render). Set `VITE_API_URL`
   only if direct cross-origin mode is wanted instead.
3. Pages → Settings → Environment variables (production): set `API_URL`
   to `https://<api>.onrender.com` (no trailing slash). This is a
   *runtime* secret — never baked into the JS bundle, unlike `VITE_*`.
4. Same-origin proxy means auth cookies stay first-party: no preview-URL
   CORS allowlisting, no `COOKIE_SAMESITE=none` requirement for the web
   flow (keep Render's `none` only if native mobile/direct-API clients
   need cross-origin cookies).
5. Preview deployments work with zero extra config (same proxy, same
   secret) — verify login on a preview URL before promoting to production.

## 4. Google Cloud Run free tier (compiler microservice)

Source: `backend/compiler-service/` (standalone FastAPI, no app imports).

1. `gcloud run deploy compiler --source backend/compiler-service \
   --region us-central1 --allow-unauthenticated --max-instances 4 \
   --concurrency 4 --memory 512Mi --cpu 1 --timeout 60s \
   --set-env-vars COMPILER_KEY=<64-char random, new>`.
   Free tier covers this (2M req/mo, scale-to-zero, us-central1).
2. Harden in console: read-only root filesystem, no VPC egress, min-instances 0.
3. Copy the service URL + key into Render env: `COMPILER_SERVICE_URL`,
   `COMPILER_SERVICE_KEY`. Backend tries it before all third-party
   providers and falls through silently when unset/unreachable.
4. Verify: `GET <url>/health` → `{"status":"ok"}`; then one Render-logged
   `source: gcp_compiler` execution. Languages: python + javascript only —
   everything else falls through to Piston/Judge0 by design.

## 5. First live verification (the actual milestone)

Not "does it build": a real person runs
signup → journey → one lesson → one OA section → one interview turn,
and every number shown (XP, readiness, rank) is real. Any fabricated,
zeroed, or stale value found here is a P0 against the deploy, not the
feature backlog. Confirm one compiler execution with `source:
gcp_compiler` in Render logs during the run.

## 6. Explicitly out of scope for first deploy

- Unifying the two world registries (`TECH_DEBT_TWO_REGISTRIES.md`).
- Company/interview/daily route consolidation (no collisions; frontend
  generated clients are coupled per module — post-deploy work).
- Dead `alembic/` removal. Server-side solve-duration timestamps.
