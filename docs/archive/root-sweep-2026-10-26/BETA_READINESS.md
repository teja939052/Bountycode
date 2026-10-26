# BountyCode Beta Readiness

**Date:** 2026-09-08
**Status:** Engineering complete. Awaiting human actions for live beta.

---

## What’s already working (verified)

| Component | Status | Evidence |
|-----------|--------|----------|
| Company blueprint system | ✅ | `company_blueprints.json` + `oa.py` wiring + 7/7 integration tests |
| TCS/Infosys/Wipro/Accenture blueprints | ✅ | Pattern-relevant with sources, `verification_todo` where needed |
| OA engine (data-driven) | ✅ | Blueprint exact counts, section durations, exam rules |
| Verified question trust pipeline | ✅ | 513 trusted questions, hidden tests, provenance stamps |
| World 1 pedagogy loop | ✅ | Discover → Manipulate → Predict → Build → Break → Debug → Transfer → Prove |
| Mock test content | ✅ | TCS mock has verified aptitude/verbal/logical/coding sections |
| Session persistence | ✅ | `oa_sessions_collection` stores sessions with `session_id` |
| Frontend build | ✅ | `npm run build` passes, 2309 modules |
| Backend compilation | ✅ | `python -m compileall app/` passes |

---

## What this beta measures

The single question that matters:

> **Will students actually use it and pay?**

Everything else is secondary until this is answered.

---

## Human actions required before beta launch

### 1. Infrastructure (1–2 days)

- [ ] **Domain + hosting**: Point a domain at your hosting provider (Vercel frontend, backend on Render/Railway/Fly.io/Docker)
- [ ] **Environment variables**: Fill in `.env` on the backend server:
  - `MONGODB_URI` — production MongoDB (Atlas or self-hosted)
  - `OPENROUTER_API_KEY` — AI provider
  - `PAYPAL_CLIENT_ID` / `PAYPAL_CLIENT_SECRET` — payments
  - `JWT_SECRET` — random 32+ char string
  - `ADMIN_EMAILS` — include your email for admin access
  - `CORS_ORIGINS` — frontend domain
- [ ] **SSL certificates**: Automatic on Vercel/Render; manual if self-hosted

### 2. Payments (1 day)

- [ ] **PayPal Business account**: Create app, get client ID/secret
- [ ] **Webhook endpoint**: Point PayPal webhook to `/api/v1/billing/webhook`
- [ ] **Test transaction**: Complete one ₹99 test payment end-to-end
- [ ] **Pricing**: Confirm ₹99 / ₹399 / ₹2,499 are the live prices

### 3. Ambassador onboarding (1 day)

- [ ] **Share signup link**: Give Ajay + 6 ambassadors a unique signup URL
- [ ] **Brief ambassadors**: 2-minute video or doc explaining:
  - What the platform does
  - Who it’s for (their audience)
  - What you’re testing (the Journey → OA loop)
  - What feedback you need
- [ ] **Set expectations**: “This is a beta. You’ll see bugs. Tell me what breaks.”

### 4. Analytics access (30 min)

- [ ] **MongoDB access**: Ensure you can query `analytics_events` collection
- [ ] **Run beta funnel script**: `python -m app.scripts.beta_funnel`
- [ ] **Bookmark queries**: Save the funnel queries for daily/weekly checks

---

## The activation funnel (what to measure)

```
signup_complete
    ↓
onboarding_complete
    ↓
activation (first /study/today load)
    ↓
first_mission_complete
    ↓
oa_start
    ↓
oa_complete
```

### Key metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Signup → Onboarding | onboarding / signup | >60% |
| Signup → Activation | activation / signup | >50% |
| Signup → First Mission | first_mission / signup | >30% |
| Signup → OA Start | oa_start / signup | >10% |
| OA Start → Complete | oa_complete / oa_start | >70% |
| Day-7 return | users with 2+ events in days 1-7 | >20% |

### Revenue metrics (after payments are live)

| Metric | Target |
|--------|--------|
| Free → ₹99 | >5% |
| Free → ₹399 | >2% |
| ₹399 → retention (month 2) | >40% |
| Lifetime purchases | Track separately |

---

## What NOT to do during beta

**Do NOT:**
- Add new engines, routes, collections, or question systems
- Expand question volume beyond verified 513
- Refactor architecture
- Add gamification mechanics
- Build “nice to have” features

**Do:**
- Fix bugs students report
- Improve UX where students get stuck
- Add questions for topics students explicitly request
- Tune difficulty/pace based on completion rates

---

## Daily beta checklist

1. Run `python -m app.scripts.beta_funnel` — check funnel conversion
2. Check MongoDB `analytics_events` for new event types / errors
3. Read ambassador feedback (Slack/WhatsApp/email)
4. Fix any P0 bugs (broken flows, crashes, payment failures)
5. Note top 3 student requests for next week

---

## If students say…

| Student feedback | Action |
|------------------|--------|
| “I need more SQL” | Add SQL questions to verified bank |
| “TCS prep is great, Amazon is weak” | Expand Amazon blueprint + questions |
| “The Journey is useful but content is basic” | Improve World 1–3 lesson depth |
| “I can get this free on YouTube” | Identify what’s unique (personalization, evidence loop, repair) and make it more visible |
| “I don’t understand what to do first” | Improve onboarding / first-mission guidance |
| “The OA doesn’t match real TCS” | Refine blueprint with student-sourced corrections |

---

## Files to share with ambassadors

1. **Signup URL** — your production `/register` endpoint
2. **2-minute demo video** — screen recording of: signup → onboarding → first mission → OA
3. **Feedback form** — simple Google Form or WhatsApp group
4. **This document** — so they understand what you’re testing

---

## Next review

After **20 signups** or **7 days**, whichever comes first:

1. Review funnel metrics
2. Identify biggest drop-off
3. Decide: iterate on conversion fix, or expand to next 20 users
