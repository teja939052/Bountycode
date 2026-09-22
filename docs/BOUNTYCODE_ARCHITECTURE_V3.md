# BOUNTYCODE_ARCHITECTURE_V3.md
**Version:** 3.0 (Launch Spec)  
**Effective Date:** October 16, 2026  
**Governed By:** `/docs/BOUNTYCODE_VISION_LOCK.md`  

## Decision Log (binding resolutions, 2026-09-21)
- **Nav IA:** PRD §3 6-hub IA governs (Journey / Practice / Mock OA / AI Interview / Company Tracks / Profile). V3 §1's Target/Skills ship as views inside Journey/Company Tracks, not top-level nav.
- **Billing:** V3 §7 governs — switch to Razorpay single ₹99/month tier + STUDENT50 discount (₹49/month, `.edu.in`/`.ac.in` verification). Replaces PayPal Free/Pro/Lifetime.
- **Launch date:** October 18, 2026 (Vision Lock + PRD win over §0 header).
- **Product name:** BountyCode (Vision Lock wins over "PLACEMENTPRO" diagram label).  

***

## 0. Core Philosophy

**ONE product, not 100+ routes.**

**Old architecture:**
```
Home
 ├── C++
 ├── TCS
 ├── Aptitude
 ├── DSA
 ├── Interview
 ├── System Design
 ├── SQL
 ├── CS Fundamentals
 ├── Behavioral
 └── ... (100+ routes)
```

**New architecture:**
```
PLACEMENTPRO
     │
     ├────────────────────┐
     │                    │
  LEARN               GET HIRED
     │                    │
     └────────┬───────────┘
              │
       PERSONAL JOURNEY
              │
        TARGET ENGINE
              │
     ┌────────┴────────┐
     │                 │
   ROLE            COMPANY
     │                 │
     └────────┬────────┘
              │
       CAPABILITY GRAPH
              │
     ┌────────┼────────┐
     │        │        │
  Coding   Aptitude  Interview
     │        │        │
     └────────┼────────┘
              │
        STUDY ENGINE
              │
     Learn → Practice → Mastery → SRS → Assessment → Diagnosis → Repair → Retest → AI Interview → Readiness → 🎯 TARGET
```

**Key insight:** C++ / TCS / Aptitude / DSA / Interview are **inputs, capabilities, targets, and stages inside ONE product**, not separate products.

***

## 1. Student Navigation (5 Items Max)

**Primary nav (top/bottom bar):**
```
┌──────────────────────────┐
│                          │
│  🗺 JOURNEY              │
│  ⚔ PRACTICE             │
│  🎯 TARGET              │
│  📊 SKILLS              │
│  👤 PROFILE              │
│                          │
└──────────────────────────┘
```

**What each means:**

**🗺 JOURNEY (`/journey`):**
- Your personalized path (based on target + capability graph)
- Shows: "Next mission: Repair Sliding Window Edge Cases"
- Why: "Your last assessment showed: Concept 86%, Implementation 81%, Edge Cases 43%"
- Estimated time: 18 minutes
- [START MISSION] button

**⚔ PRACTICE (`/practice`):**
- "I want to choose what I practice"
- Categories: Coding / SQL / Aptitude / Reasoning / Verbal / CS / Interview / System Design / Debugging
- Unordered (student picks any pattern, not locked to Journey order)

**🎯 TARGET (`/target`):**
- Current target: Software Engineer @ TCS Digital
- [Change Target] button
- [Explore Companies] button
- [Explore Roles] button

**📊 SKILLS (`/skills`):**
- Your Skill Graph / readiness
- Coding: 82%
- Aptitude: 88%
- SQL: 68%
- CS Fundamentals: 51%
- DBMS: 63%
- Communication: 71%
- [View Details] button

**👤 PROFILE (`/profile`):**
- XP, achievements, streak, history
- Settings, billing, subscription
- [Upgrade to Job Seeker (₹99/month)] button

**Internal routes (implementation details, not nav concepts):**
- `/oa` (Online Assessment engine)
- `/repair` (Repair loop engine)
- `/interview` (AI interviewer engine)
- `/srs` (Spaced Repetition engine)
- `/gamification` (XP/Proof/Bounty engine)
- `/trace` (Code tracing engine)
- `/questions` (Question bank)
- `/quiz` (Quiz engine)
- `/lesson` (Lesson player)
- `/mock` (Mock OA engine)
- `/readiness` (Readiness score engine)
- `/company/{company}` (Company target page)
- `/role/{role}` (Role target page)

**Why this wins:**
- ✅ **5 nav items** (not 100+)
- ✅ **Clear mental model** (Journey/Practice/Target/Skills/Profile)
- ✅ **Internal routes are implementation details** (student doesn't need to understand your architecture)

***

## 2. Onboarding Flow (2 Screens Max)

**Screen 1: Sign Up**
```
┌─────────────────────────────────────────┐
│  SIGN UP                                │
│                                         │
│  Continue with Google                   │
│  Continue with GitHub                   │
│  Sign up with Email                     │
│                                         │
│  [Sign Up →]                            │
└─────────────────────────────────────────┘
```

**Screen 2: ONE Question**
```
┌─────────────────────────────────────────┐
│  What are you here to accomplish?       │
│                                         │
│  [ ] 🎓 BUILD MY CODING SKILLS          │
│      Prepare from the fundamentals.     │
│                                         │
│  [ ] 🎯 PREPARE FOR PLACEMENTS          │
│      Build skills + aptitude + interviews.
│                                         │
│  [ ] 💼 PREPARE FOR A JOB               │
│      Target a role/company and prove readiness.
│                                         │
│  [Next →]                               │
└─────────────────────────────────────────┘
```

**If "🎓 Build my coding skills":**
```
┌─────────────────────────────────────────┐
│  What do you want to learn?             │
│                                         │
│  [ ] C++                                │
│  [ ] Python                             │
│  [ ] Java                               │
│  [ ] JavaScript                         │
│  [ ] SQL                                │
│  [ ] Not sure yet (show me basics)      │
│                                         │
│  [Start Journey →]                      │
└─────────────────────────────────────────┘
```

**If "🎯 Prepare for placements" or "💼 Prepare for a job":**
```
┌─────────────────────────────────────────┐
│  What role are you targeting?           │
│                                         │
│  [ ] Software Engineer                  │
│  [ ] Frontend Developer                 │
│  [ ] Backend Developer                  │
│  [ ] Full Stack Developer               │
│  [ ] Data Analyst                       │
│  [ ] QA Engineer                        │
│  [ ] DevOps Engineer                    │
│  [ ] Not sure yet                       │
│                                         │
│  [Next →]                               │
└─────────────────────────────────────────┘
```

**Then (optional):**
```
┌─────────────────────────────────────────┐
│  Where are you applying? (optional)     │
│                                         │
│  [ ] TCS NQT                            │
│  [ ] Infosys Elevate                    │
│  [ ] Wipro NLTH                         │
│  [ ] Cognizant GenC                     │
│  [ ] Capgemini                          │
│  [ ] Amazon                             │
│  [ ] Google                             │
│  [ ] Not sure yet (generic prep)        │
│                                         │
│  [Start Journey →]                      │
└─────────────────────────────────────────┘
```

**After choosing:**
```
┌─────────────────────────────────────────┐
│  🎉 Welcome to BountyCode!              │
│                                         │
│  Your Journey starts now:               │
│                                         │
│  If "Learn C++":                        │
│  🗺️ C++ Mastery Journey                 │
│  - Level 1: Syntax                      │
│  - Level 2: Variables                   │
│  - Level 3: Conditions                  │
│  - Level 4: Loops                       │
│  - Level 5: Functions                   │
│  - Level 6: Arrays                      │
│  - Level 7: Strings                     │
│  ...                                    │
│                                         │
│  If "Software Engineer @ TCS Digital":  │
│  🗺️ TCS Digital Prep Journey            │
│  - Coding: 72%                          │
│  - Aptitude: 91%                        │
│  - Reasoning: 83%                       │
│  - CS Fundamentals: 54% ← REPAIR        │
│  - SQL: 64%                             │
│  - Interview: 43% ← REPAIR              │
│                                         │
│  First Mission:                         │
│  [Start →]                              │
│                                         │
│  Your streak starts now! 🔥             │
│  Complete today's mission to keep it going.
└─────────────────────────────────────────┘
```

**Why this wins:**
- ✅ **2 screens max** (sign up → ONE question → Journey)
- ✅ **Same destination** (Journey map, just different content ordering)
- ✅ **Gamification from lesson 1** (streak/Proof/Bounty, no matter the path)
- ✅ **Company optional** (student can start with "generic prep" and add company later)

***

## 3. Journey Page (Home After Login)

**URL:** `/journey` (canonical route, replaces `/dashboard`)  
**Purpose:** Show personalized path based on target + capability graph

**Layout:**
```
┌─────────────────────────────────────────┐
│  GOOD MORNING, TEJA                     │
│                                         │
│  🎯 Target: Software Engineer @ TCS Digital
│  ████████████░░░░ 68% Ready             │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │ ⚡ TODAY'S MISSION                 │ │
│  │                                    │ │
│  │ Repair: Sliding Window Edge Cases  │ │
│  │                                    │ │
│  │ Why? Your last assessment showed:  │ │
│  │ - Concept: 86%                     │ │
│  │ - Implementation: 81%              │ │
│  │ - Edge Cases: 43% ← WEAK           │ │
│  │                                    │ │
│  │ Estimated time: 18 minutes         │ │
│  │                                    │ │
│  │ [ START MISSION → ]                │ │
│  └────────────────────────────────────┘ │
│                                         │
│  YOUR JOURNEY                           │
│                                         │
│  🟢 C++ Foundations                     │
│  🟢 Arrays                              │
│  🟢 Strings                             │
│  🔵 Sliding Window  ← YOU ARE HERE      │
│  🔒 Two Pointers                        │
│  🔒 Binary Search                       │
│  🔒 Hashing                             │
│  🔒 Trees                               │
│  🔒 Graphs                              │
│  🔒 DP                                  │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  Weakness detected                      │
│  ⚠ Edge-case reasoning                  │
│  [ REPAIR → ]                           │
└─────────────────────────────────────────┘
```

**Why this wins:**
- ✅ **ONE question answered:** "What should I do next?"
- ✅ **Not:** "What feature do you want?"
- ✅ **Personalized mission** (based on target + capability graph + last assessment)
- ✅ **Repair loop** (weakness detected → [REPAIR] button)
- ✅ **Same Journey map** (just different content ordering based on target)

***

## 4. Capability Graph (Central Object)

**Central object:**
```
User
  ↓
Journey
  ↓
Target
  ↓
Capability
  ↓
Mission
  ↓
Evidence
  ↓
Mastery
```

**Not:**
```
User
  ↓
Question
  ↓
XP
```

**Capability Graph:**
```
┌─────────────────────────────────────────┐
│  YOUR CAPABILITIES                      │
│                                         │
│  C++              ████████████░░ 82%    │
│  Arrays           ██████████░░░░ 74%    │
│  Graphs           ██████░░░░░░░░ 41%    │
│  SQL              ██████████░░░░ 68%    │
│  OS               ████████░░░░░░ 51%    │
│  DBMS             ██████████░░░░ 63%    │
│  Aptitude         █████████████░ 88%    │
│  Communication    ███████████░░░ 71%    │
│                                         │
│  [View Details →]                       │
└─────────────────────────────────────────┘
```

**Multiple targets, one capability profile:**
```
┌─────────────────────────────────────────┐
│  YOUR TARGETS                           │
│                                         │
│  TCS Digital                            │
│  Readiness: 72%                         │
│  ████████████████████░░░░ 72%          │
│                                         │
│  Infosys                                │
│  Readiness: 78%                         │
│  ██████████████████████░░░░ 78%        │
│                                         │
│  Amazon                                 │
│  Readiness: 46%                         │
│  ██████████████░░░░░░░░░░ 46%          │
│                                         │
│  [Add Target →]                         │
└─────────────────────────────────────────┘
```

**Why this wins:**
- ✅ **ONE capability profile** (not 4 separate profiles)
- ✅ **Multiple targets** (TCS Digital 72%, Infosys 78%, Amazon 46%)
- ✅ **Each target weights capabilities differently** (TCS weights Aptitude higher, Amazon weights DSA higher)

***

## 5. Company Pages (Target Packs, Not Mini-LMS)

**URL:** `/companies/tcs`  
**Purpose:** Choose target pack (TCS NQT / TCS Digital / TCS Prime)

**Layout:**
```
┌─────────────────────────────────────────┐
│  TCS                                    │
│                                         │
│  Choose your target:                    │
│                                         │
│  ┌─────────────────────┐                │
│  │ TCS NQT             │                │
│  │ General preparation │                │
│  │                     │                │
│  │ [ START → ]         │                │
│  └─────────────────────┘                │
│                                         │
│  ┌─────────────────────┐                │
│  │ TCS Digital         │                │
│  │ Advanced preparation│                │
│  │                     │                │
│  │ [ START → ]         │                │
│  └─────────────────────┘                │
│                                         │
│  ┌─────────────────────┐                │
│  │ TCS Prime           │                │
│  │ Elite preparation   │                │
│  │                     │                │
│  └─────────────────────┘                │
└─────────────────────────────────────────┘
```

**After selecting TCS Digital:**
```
┌─────────────────────────────────────────┐
│  TCS DIGITAL                            │
│                                         │
│  Your readiness: 62%                    │
│  ██████████████████░░░░░░ 62%          │
│                                         │
│  Coding             ███████░░ 72%       │
│  Aptitude           █████████ 91%       │
│  Reasoning          ████████░ 83%       │
│  CS Fundamentals    █████░░░░ 54% ← REPAIR
│  SQL                ██████░░░ 64%       │
│  Interview          ████░░░░░ 43% ← REPAIR
│                                         │
│  NEXT:                                  │
│                                         │
│  ⚔ Repair CS Fundamentals               │
│  [ ENTER JOURNEY → ]                    │
└─────────────────────────────────────────┘
```

**Why this wins:**
- ✅ **Target packs** (TCS NQT / Digital / Prime), not mini-LMS
- ✅ **Readiness score** (62% for TCS Digital)
- ✅ **Capability breakdown** (Coding 72%, Aptitude 91%, CS Fundamentals 54%)
- ✅ **Repair loop** (CS Fundamentals 54% → [ENTER JOURNEY] button)
- ✅ **Same Journey** (just reordered based on TCS Digital requirements)

***

## 6. Practice Mode (Unordered, Always Accessible)

**URL:** `/practice`  
**Purpose:** Browse pattern categories without Journey ordering

**Layout:**
```
┌─────────────────────────────────────────┐
│  PRACTICE BY CATEGORY                   │
│                                         │
│  💻 Coding (40 patterns)                │
│  - Two Pointers                         │
│  - Sliding Window                       │
│  - Hash Lookup                          │
│  - Binary Search                        │
│  - Prefix Sum                           │
│  ...                                    │
│                                         │
│  📊 Aptitude (20 patterns)              │
│  - Successive Percentage Change         │
│  - Ratio Scaling                        │
│  - Profit/Loss Transformation           │
│  - Work-Rate Composition                │
│  - Relative Speed                       │
│  ...                                    │
│                                         │
│  🧠 Reasoning (20 patterns)             │
│  - Syllogism Set Logic                  │
│  - Blood-Relation Graph                 │
│  - Coding-Decoding Transformation       │
│  - Direction Graph                      │
│  - Sequence Detection                   │
│  ...                                    │
│                                         │
│  📚 Verbal (15 patterns)                │
│  - Subject-Verb Agreement               │
│  - Reading Comprehension (Main Idea)    │
│  - Para Jumbles (Chronological Order)   │
│  - Sentence Correction                  │
│  ...                                    │
│                                         │
│  🗄 SQL (10 patterns)                   │
│  - SELECT + WHERE                       │
│  - JOINs                                │
│  - GROUP BY + HAVING                    │
│  - Subqueries                           │
│  - Indexes                              │
│  ...                                    │
│                                         │
│  🖥 CS Fundamentals (15 patterns)        │
│  - OS (Processes, Threads, Deadlocks)   │
│  - DBMS (Normalization, Transactions)   │
│  - Networks (OSI Model, TCP/IP)         │
│  - OOP (Inheritance, Polymorphism)      │
│  ...                                    │
│                                         │
│  🎤 Interview (10 patterns)             │
│  - Technical (DSA, System Design)       │
│  - Behavioral (STAR method)             │
│  - HR (Salary negotiation, Notice period)
│  ...                                    │
│                                         │
│  [Start Practice →]                     │
└─────────────────────────────────────────┘
```

**Why this wins:**
- ✅ **Always accessible** (from Journey map, top nav)
- ✅ **Unordered** (student can pick any pattern, not locked to Journey order)
- ✅ **Same patterns** (Coding/Aptitude/Reasoning/Verbal/SQL/CS/Interview)

***

## 7. Pricing (Simple, Not Confusing)

**ONE pricing tier** (₹99/month), with **student discount code** (₹50 off → ₹49/month).

**Implementation:**
```python
# backend/app/routes/billing.py
@router.post("/create-checkout-session")
async def create_checkout_session(user_id: str, discount_code: str = None):
    # Base price: ₹99/month
    base_price = 9900  # paise
    
    # Apply student discount if valid
    if discount_code == "STUDENT50":
        # Verify student status (college email, .edu.in domain)
        user = await db.users.find_one({"_id": user_id})
        if user["email"].endswith(".edu.in") or user["email"].endswith(".ac.in"):
            base_price = 4900  # ₹49/month
    
    # Create Razorpay checkout session
    session = razorpay.order.create({
        "amount": base_price,
        "currency": "INR",
        "receipt": f"order_{user_id}_{int(time.time())}",
    })
    
    return session
```

**Why this wins:**
- ✅ **ONE pricing tier** (₹99/month, not separate student/job seeker tiers)
- ✅ **Student discount** (₹50 off with valid .edu.in/.ac.in email)
- ✅ **No price-tier wall** (student can switch to job seeker without confusion)
- ✅ **Simple to implement** (discount code, not separate tiers)

***

## 8. The Bottom Line

**Your unified architecture:**
```
Sign Up → ONE Question (build skills / prepare for placements / prepare for job) → Journey Map (same for all, different content weighting) → Practice (always accessible, unordered) → Profile (switch goal later, no re-onboarding)
```

**Not:**
```
Student: Sign up → Choose C++ → C++ dashboard → C++ Journey → C++ gamification
Job Seeker: Sign up → Choose TCS → TCS dashboard → TCS Journey → TCS gamification
Casual Coder: Sign up → Choose DSA → DSA dashboard → DSA Journey → DSA gamification
```

**Give this to your agent** and say:

> "Build unified architecture: Sign Up → ONE Question (build skills / prepare for placements / prepare for job) → Journey Map (same for all, different content weighting) → Practice (always accessible, unordered) → Profile (switch goal later, no re-onboarding). ONE pricing tier (₹99/month), student discount code (₹50 off with .edu.in email). No separate platforms for students/job seekers/casual coders."

**This is how you unify placement prep + coding learning into ONE coherent platform.** 🚀
