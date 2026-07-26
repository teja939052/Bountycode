# FUTURE.md — PlacementPro $1M ARR Roadmap

> From $0 to $1M annual recurring revenue as a solo founder, built with MimoCode.

---

## Current State (v1.0 — NOW)

- 3 core features: AI Interview, Resume Builder, ATS Optimizer
- Tech: React + FastAPI + MongoDB + Gemini Flash via OpenRouter
- Payments: PayPal (monthly $9 / lifetime $39)
- Cost: $0/mo infrastructure (all free tiers), ~$0.07/1M tokens for AI
- Security: Rate limiting, account lockout, httpOnly cookies, PDF validation

**Monthly cost estimate at current scale:**
- Infrastructure: $0
- AI: ~$5/mo
- Total: ~$5/mo

---

## Phase 1: Launch & Validate (Month 1-3)

**Goal:** 200 free users, 20 paying customers, $180 MRR

### Features to Build
- [ ] Monthly free tier reset (currently lifetime counters)
- [ ] Password reset flow (email-based)
- [ ] Email verification on signup
- [ ] Onboarding flow (3-step wizard after first login)
- [ ] Interview history with detailed breakdown view
- [ ] Resume versioning (save multiple versions, compare changes)

### Distribution (0 → 200 users)
1. **Reddit** (primary channel)
   - r/jobs (2M members): "I built a free AI interview practice tool — feedback welcome"
   - r/cscareerquestions (1M): "AI interviewer that actually critiques your answers"
   - r/resumes (500K): "Free AI resume analyzer vs Jobscan ($50/mo)"
   - r/interviews (200K): "Mock interview tool with real-time AI feedback"
   - Post 2-3x/week, engage in comments, never spam

2. **LinkedIn** (secondary)
   - Build in public posts: "Day 14 of building PlacementPro..."
   - Share user wins (with permission)
   - Engage with HR/recruiter content to get visibility

3. **Product Hunt** (one-time launch)
   - Prepare launch assets 1 week before
   - Build email list of early users to boost on launch day

### Revenue Model at This Phase
- Free: 3 interviews + 3 resumes/month
- Pro: $9/mo → unlimited everything
- Lifetime: $39 one-time

### Key Metrics
- Signups/week
- Free → paid conversion rate (target: 10%)
- Churn rate (target: <10%/mo)
- Average session duration
- AI cost per user

---

## Phase 2: Growth Engine (Month 3-6)

**Goal:** 1,000 free users, 80 paying customers, $720 MRR

### Features to Build
- [ ] **Cover Letter Generator** — AI writes tailored cover letters from resume + JD
- [ ] **Interview Coach Mode** — Not just mock interviews, but coaching tips before real ones
- [ ] **ATS Keyword Tracker** — Track keyword usage across multiple applications
- [ ] **Progress Dashboard** — Charts showing improvement over time
- [ ] **Export to LinkedIn** — Generate LinkedIn "About" section from resume
- [ ] **Team/Referral Program** — Give 1 month free for each referral

### Distribution (200 → 1,000 users)
1. **SEO + Content Marketing**
   - Blog posts: "How to Ace Your Software Engineer Interview in 2025"
   - Programmatic SEO: "/resume-template-[role]" pages
   - Target long-tail keywords: "free ai interview practice"

2. **YouTube / TikTok**
   - "I Let AI Interview Me — Here's What Happened"
   - Resume before/after transformations
   - "This AI Found 12 Missing Keywords in My Resume"
   - 1-2 videos/week, cross-post to all platforms

3. **Partnerships**
   - University career centers (free tier for students)
   - Bootcamp affiliates (revenue share)
   - Career coaches (white-label opportunity)

### Revenue Expansion
- Introduce Annual plan: $79/year (saves $29 vs monthly)
- Lifetime price increase: $39 → $49 (for new users)
- Referral program: existing user gets 1 month free per referral

### Key Metrics
- Organic traffic (Google)
- Referral conversion rate
- Feature adoption by plan type
- CAC (Customer Acquisition Cost) — target: <$15

---

## Phase 3: Scale & Optimize (Month 6-12)

**Goal:** 3,000 free users, 200 paying customers, $1,800 MRR + $2K lifetime = $3,800/mo

### Features to Build
- [ ] **Multi-Language Support** — Spanish, French, Portuguese (expand TAM)
- [ ] **Industry-Specific Modules** — Tech, Finance, Healthcare, Marketing
- [ ] **Video Interview Practice** — Record yourself, AI analyzes body language cues
- [ ] **Company-Specific Prep** — "Amazon Leadership Principles" interview mode
- [ ] **Certification Badges** — "Completed 10 interviews, scored 8+ average"
- [ ] **API Access** — Let career services integrate our AI

### Technical Scaling
- [ ] Move to dedicated MongoDB cluster (when 512MB limit hit)
- [ ] Add Redis caching (for frequently accessed data)
- [ ] CDN for static assets (Vercel handles this)
- [ ] Queue system for AI calls (prevent rate limiting)
- [ ] A/B testing framework (for pricing + features)

### Distribution (1,000 → 3,000 users)
1. **Paid Acquisition Testing**
   - Google Ads: "free ai interview practice" — target $2 CAC
   - Reddit Ads: Target r/jobs, r/cscareerquestions
   - Test $100/week, optimize for ROAS

2. **Community Building**
   - Discord/Slack community for job seekers
   - Weekly "Interview Prep" live sessions
   - User success stories as case studies

3. **Enterprise/B2B Exploration**
   - Reach out to bootcamps (placement assistance)
   - University partnerships (career services)
   - Recruitment agencies (value-add for candidates)

### Revenue Optimization
- Raise Pro to $12/mo for new users (grandfather existing)
- Introduce "Team" plan: $29/mo for 5 seats (for bootcamps)
- Increase Lifetime to $59 (scarcity + value perception)

### Key Metrics
- LTV:CAC ratio (target: 3:1)
- Monthly active users (MAU)
- Feature usage heatmap
- Support ticket volume

---

## Phase 4: $1M ARR (Month 12-18)

**Goal:** 10,000 free users, 500 paying customers, $4,500 MRR + $2K lifetime = $6,500/mo → push to $83K/mo = $1M ARR

### Path to $1M ARR

To hit $1M ARR from here, you need ONE of these levers:

#### Option A: Volume Play (Recommended)
- 10,000 paying users × $9/mo = $1,080K ARR
- Need: 10x user base from Phase 3
- Requires: Strong SEO, content marketing, word of mouth

#### Option B: Price Increase
- 2,000 paying users × $49/mo = $1,176K ARR
- Need: Premium features (video, company-specific, API)
- Requires: Enterprise/b2b sales motion

#### Option C: Hybrid (Best Path)
- 800 Pro users × $12/mo = $115K ARR
- 200 Team users × $29/mo = $70K ARR
- 100 Enterprise users × $99/mo = $120K ARR
- Total: ~$305K ARR from subscriptions
- Plus: $500K from one-time purchases, partnerships, and upsells
- Combined: ~$800K-1M ARR

### Features for $1M Scale
- [ ] **White-label platform** — Bootcamps deploy their own PlacementPro
- [ ] **API product** — Sell AI interview/ATS API to other tools
- [ ] **Mobile app** — React Native (interview practice on commute)
- [ ] **Browser extension** — Real-time ATS scoring while editing resume
- [ ] **Interview recording + playback** — Premium feature for self-review
- [ ] **AI career coach** — Ongoing personalized guidance (subscription)

### Technical Requirements at Scale
- [ ] Move from Render to AWS/GCP (when traffic justifies cost)
- [ ] Dedicated PostgreSQL for billing/analytics (MongoDB for app data)
- [ ] Microservices split (auth, AI, billing, analytics)
- [ ] Load balancing + auto-scaling
- [ ] Observability stack (Datadog/Grafana)
- [ ] SOC 2 compliance (for enterprise sales)

### Team Building
- [ ] Hire 1 part-time support person (at ~$500 MRR)
- [ ] Contract content writer (at ~$1K MRR)
- [ ] First full-time hire: backend engineer (at ~$3K MRR)
- [ ] Sales/BD person for enterprise (at ~$10K MRR)

---

## Revenue Milestones & Decisions

| MRR | Decision |
|-----|----------|
| $0-100 | Keep day job, build nights/weekends |
| $100-500 | Consider going full-time if runway allows |
| $500-1K | Hire first contractor (support/content) |
| $1K-3K | Full-time on PlacementPro, hire part-time help |
| $3K-5K | Hire first full-time employee |
| $5K-10K | Start enterprise/b2b sales motion |
| $10K-25K | Team of 3-5, dedicated sales |
| $25K-50K | VC conversation (optional), scale marketing |
| $50K-83K | **$1M ARR** — you made it |

---

## Cost Structure at Scale

| Scale | Infrastructure | AI | Team | Total |
|-------|---------------|-----|------|-------|
| $0 MRR | $0 | $5 | $0 | $5/mo |
| $180 MRR | $0 | $15 | $0 | $15/mo |
| $720 MRR | $20 | $50 | $0 | $70/mo |
| $1,800 MRR | $50 | $150 | $500 | $700/mo |
| $4,500 MRR | $100 | $400 | $2,000 | $2,500/mo |
| $83K MRR | $500 | $3,000 | $25,000 | $28,500/mo |

**Target gross margin: 65-75%** (after AI + infrastructure costs)

---

## Competitive Moats to Build

1. **AI Prompt Quality** — Best interview questions, most helpful feedback (80% of value)
2. **User Data Network Effect** — More users → better AI training data → better prompts
3. **Brand Trust** — Job seekers trust "PlacementPro" over random tools
4. **Switching Cost** — Resume history, interview progress, certifications
5. **SEO Dominance** — Rank #1 for "ai interview practice", "free resume scanner"
6. **Community** — Discord/forum where users help each other

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| OpenRouter raises prices | Switch to self-hosted LLM (Ollama + Llama) |
| Competitors copy features | Focus on UX + brand + community moat |
| PayPal issues | Add Stripe as secondary payment option |
| Low conversion rates | A/B test pricing, add annual plans, improve onboarding |
| High churn | Build habit loops (weekly email, progress tracking) |
| Solo founder burnout | Hire early, automate everything, take breaks |

---

## Weekly Habits for Growth

1. **Monday:** Review metrics (signups, conversions, churn, AI costs)
2. **Tuesday-Thursday:** Build features + fix bugs
3. **Friday:** Content creation (1 blog post or Reddit post)
4. **Saturday:** Engage with community (Reddit, Discord, LinkedIn)
5. **Sunday:** Plan next week, review competitor moves

---

## The One-Thing Focus

At each stage, focus on ONE growth lever:

- **Month 1-3:** Reddit + organic content (get first 200 users)
- **Month 3-6:** SEO + YouTube (get to 1,000 users)
- **Month 6-12:** Referrals + partnerships (get to 3,000 users)
- **Month 12-18:** Enterprise + API sales (get to $1M ARR)

Don't try to do everything at once. Master one channel before adding the next.

---

*Last updated: July 2026*
*Built with MimoCode*
