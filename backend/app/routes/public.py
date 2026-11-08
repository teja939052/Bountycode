"""Public API endpoints for landing page and marketing pages.

No authentication required. Serves pricing, features, testimonials,
company directory, and FAQ data for the marketing site.
"""
from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/v1/public", tags=["public"])

# ─── Pricing plans ──────────────────────────────────────────────────────

PRICING_PLANS = [
    {
        "id": "free",
        "name": "Free",
        "description": "Get started with placement prep",
        "price": {"USD": 0, "INR": 0},
        "billing_cycle": "forever",
        "features": [
            "3 mock interviews per month",
            "3 resume reviews per month",
            "5 aptitude tests per month",
            "3 cover letters per month",
            "1 company mock per month",
            "5 AI questions per day",
            "20 compiler runs per day",
            "Access to question bank (5 problems/month)",
        ],
        "limits": {
            "interviews_per_month": 3,
            "resumes_per_month": 3,
            "aptitude_tests_per_month": 5,
            "cover_letters_per_month": 3,
            "company_mocks_per_month": 1,
            "ai_questions_per_day": 5,
            "compiler_runs_per_day": 20,
            "problems_per_month": 5,
        },
        "popular": False,
        "cta": "Start for free",
    },
    {
        "id": "pro",
        "name": "Pro",
        "description": "Unlimited placement prep for serious candidates",
        "price": {"USD": 9, "INR": 799},
        "billing_cycle": "month",
        "features": [
            "Unlimited mock interviews",
            "Unlimited resume reviews",
            "Unlimited aptitude tests",
            "Unlimited cover letters",
            "Unlimited company mocks",
            "Unlimited AI questions",
            "Unlimited compiler runs",
            "Full question bank access",
            "AI Interviewer with company-specific questions",
            "ATS Resume Optimizer",
            "Priority support",
        ],
        "limits": {
            "interviews_per_month": -1,
            "resumes_per_month": -1,
            "aptitude_tests_per_month": -1,
            "cover_letters_per_month": -1,
            "company_mocks_per_month": -1,
            "ai_questions_per_day": -1,
            "compiler_runs_per_day": -1,
            "problems_per_month": -1,
        },
        "popular": True,
        "cta": "Get Pro — $9/month",
    },
    {
        "id": "lifetime",
        "name": "Lifetime",
        "description": "One-time payment, lifetime access",
        "price": {"USD": 149, "INR": 3999},
        "billing_cycle": "forever",
        "features": [
            "Everything in Pro, forever",
            "No monthly payments",
            "Lifetime question bank access",
            "Lifetime interview recordings",
            "Early access to new features",
            "Priority support",
        ],
        "limits": {
            "interviews_per_month": -1,
            "resumes_per_month": -1,
            "aptitude_tests_per_month": -1,
            "cover_letters_per_month": -1,
            "company_mocks_per_month": -1,
            "ai_questions_per_day": -1,
            "compiler_runs_per_day": -1,
            "problems_per_month": -1,
        },
        "popular": False,
        "cta": "Lifetime Access — $149",
    },
]


@router.get("/pricing")
async def get_pricing():
    """Get all pricing plans."""
    return {"plans": PRICING_PLANS}


# ─── Features ───────────────────────────────────────────────────────────

FEATURES = [
    {
        "id": "ai-interviewer",
        "title": "AI Interviewer",
        "description": "Mock interviews with AI that asks questions, evaluates answers, and gives detailed feedback with competency-level diagnosis.",
        "icon": "users",
        "category": "interview",
    },
    {
        "id": "resume-builder",
        "title": "Resume Builder & ATS Optimizer",
        "description": "Generate ATS-friendly resumes, optimize against job descriptions, and get semantic scoring to pass ATS filters.",
        "icon": "file-text",
        "category": "resume",
    },
    {
        "id": "coding-challenges",
        "title": "Coding Challenges",
        "description": "Timed coding problems with hidden test cases, company-specific patterns, and progressive hints.",
        "icon": "code",
        "category": "coding",
    },
    {
        "id": "company-prep",
        "title": "Company-Specific Prep",
        "description": "53+ company profiles with FAANG leadership principles, behavioral questions, and role-specific preparation paths.",
        "icon": "building",
        "category": "company",
    },
    {
        "id": "aptitude-test",
        "title": "Aptitude Test Practice",
        "description": "Quantitative, logical, verbal, and technical MCQs for campus placements with timed test sessions.",
        "icon": "bar-chart",
        "category": "aptitude",
    },
    {
        "id": "learning-modules",
        "title": "Learning Modules",
        "description": "Duolingo-style step-by-step coding lessons across 7 languages with Discover → Manipulate → Predict → Build → Debug loop.",
        "icon": "book-open",
        "category": "learning",
    },
    {
        "id": "gamification",
        "title": "Gamification System",
        "description": "XP, levels (1-100), streaks, badges, tower progression, and boss battles to keep you motivated.",
        "icon": "zap",
        "category": "gamification",
    },
    {
        "id": "mock-oa",
        "title": "Mock Online Assessments",
        "description": "Realistic company-style online assessments with diagnostic reports and weakness repair paths.",
        "icon": "clipboard",
        "category": "assessment",
    },
]


@router.get("/features")
async def get_features():
    """Get all platform features for the marketing page."""
    return {"features": FEATURES}


# ─── Testimonials ───────────────────────────────────────────────────────

TESTIMONIALS = [
    {
        "id": "t1",
        "name": "Rahul Sharma",
        "role": "SDE",
        "company": "Google",
        "package": "45 LPA",
        "avatar": "R",
        "testimonial": "The mock interviews on BountyCode were spot-on for Google rounds. The competency-level diagnosis helped me fix my weaknesses before the real interview.",
        "placed": True,
    },
    {
        "id": "t2",
        "name": "Priya Patel",
        "role": "SDE",
        "company": "Amazon",
        "package": "38 LPA",
        "avatar": "P",
        "testimonial": "Company-specific prep made all the difference. The Amazon Leadership Principles practice was exactly what I needed.",
        "placed": True,
    },
    {
        "id": "t3",
        "name": "Arjun Reddy",
        "role": "SDE",
        "company": "Microsoft",
        "package": "42 LPA",
        "avatar": "A",
        "testimonial": "The ATS optimizer helped my resume pass automated filters. Got interview calls from 5 product companies within 2 weeks.",
        "placed": True,
    },
    {
        "id": "t4",
        "name": "Sneha Gupta",
        "role": "SDE",
        "company": "TCS",
        "package": "7 LPA",
        "avatar": "S",
        "testimonial": "Great for TCS NQT and services companies. The aptitude practice and company mocks were very accurate.",
        "placed": True,
    },
    {
        "id": "t5",
        "name": "Vikram Singh",
        "role": "SDE",
        "company": "Flipkart",
        "package": "32 LPA",
        "avatar": "V",
        "testimonial": "Flipkart rounds were exactly as practiced on BountyCode. The system design questions were particularly helpful.",
        "placed": True,
    },
]


@router.get("/testimonials")
async def get_testimonials():
    """Get student testimonials and placement outcomes."""
    return {"testimonials": TESTIMONIALS}


# ─── Companies ──────────────────────────────────────────────────────────

COMPANIES_DIRECTORY = [
    {"id": "google", "name": "Google", "tier": "FAANG", "color": "#4285F4", "focus": ["DSA", "System Design", "Behavioral"]},
    {"id": "amazon", "name": "Amazon", "tier": "FAANG", "color": "#FF9900", "focus": ["DSA", "Leadership Principles", "System Design"]},
    {"id": "meta", "name": "Meta", "tier": "FAANG", "color": "#1877F2", "focus": ["DSA", "System Design", "Behavioral"]},
    {"id": "microsoft", "name": "Microsoft", "tier": "FAANG", "color": "#00A4EF", "focus": ["DSA", "Clean Code", "System Design"]},
    {"id": "apple", "name": "Apple", "tier": "FAANG", "color": "#A2AAAD", "focus": ["DSA", "System Design", "Behavioral"]},
    {"id": "netflix", "name": "Netflix", "tier": "FAANG", "color": "#E50914", "focus": ["DSA", "System Design", "Behavioral"]},
    {"id": "flipkart", "name": "Flipkart", "tier": "Product", "color": "#2874F0", "focus": ["DSA", "System Design", "Behavioral"]},
    {"id": "razorpay", "name": "Razorpay", "tier": "Product", "color": "#072654", "focus": ["DSA", "System Design", "Backend"]},
    {"id": "swiggy", "name": "Swiggy", "tier": "Product", "color": "#FC8019", "focus": ["DSA", "System Design", "Backend"]},
    {"id": "zomato", "name": "Zomato", "tier": "Product", "color": "#E23744", "focus": ["DSA", "System Design", "Backend"]},
    {"id": "phonepe", "name": "PhonePe", "tier": "Product", "color": "#5F259F", "focus": ["DSA", "System Design", "Backend"]},
    {"id": "uber", "name": "Uber", "tier": "Product", "color": "#000000", "focus": ["DSA", "System Design", "Backend"]},
    {"id": "tcs", "name": "TCS", "tier": "Services", "color": "#0072C6", "focus": ["Aptitude", "DSA", "HR"]},
    {"id": "infosys", "name": "Infosys", "tier": "Services", "color": "#007CC3", "focus": ["Aptitude", "DSA", "HR"]},
    {"id": "wipro", "name": "Wipro", "tier": "Services", "color": "#005B9E", "focus": ["Aptitude", "DSA", "HR"]},
    {"id": "hcl", "name": "HCL", "tier": "Services", "color": "#003366", "focus": ["Aptitude", "DSA", "HR"]},
    {"id": "cognizant", "name": "Cognizant", "tier": "Services", "color": "#0033A0", "focus": ["Aptitude", "DSA", "HR"]},
    {"id": "accenture", "name": "Accenture", "tier": "Services", "color": "#A100FF", "focus": ["Aptitude", "DSA", "HR"]},
    {"id": "paytm", "name": "Paytm", "tier": "Startup", "color": "#00BAF2", "focus": ["DSA", "System Design", "Backend"]},
    {"id": "ola", "name": "Ola", "tier": "Startup", "color": "#2A6DFF", "focus": ["DSA", "System Design", "Backend"]},
    {"id": "cred", "name": "CRED", "tier": "Startup", "color": "#1A1A1A", "focus": ["DSA", "System Design", "Backend"]},
    {"id": "meesho", "name": "Meesho", "tier": "Startup", "color": "#F43397", "focus": ["DSA", "System Design", "Backend"]},
]


@router.get("/companies")
async def get_companies_directory(tier: Optional[str] = Query(None, description="Filter by tier")):
    """Get company directory with optional tier filter."""
    companies = COMPANIES_DIRECTORY
    if tier:
        companies = [c for c in companies if c["tier"].lower() == tier.lower()]
    return {
        "companies": companies,
        "total": len(companies),
        "tiers": ["FAANG", "Product", "Services", "Startup"],
    }


# ─── FAQ ────────────────────────────────────────────────────────────────

FAQS = [
    {
        "id": "faq1",
        "question": "Is there a free trial?",
        "answer": "Yes! The free tier includes 3 mock interviews, 3 resume reviews, 5 aptitude tests, and access to 5 question bank problems per month. No credit card required.",
    },
    {
        "id": "faq2",
        "question": "Can I upgrade or downgrade anytime?",
        "answer": "Yes. You can upgrade to Pro or Lifetime anytime. Downgrades take effect at the end of your current billing cycle.",
    },
    {
        "id": "faq3",
        "question": "Do you offer student discounts?",
        "answer": "Yes! We offer student discount codes for verified students. Contact support with your student ID.",
    },
    {
        "id": "faq4",
        "question": "What companies do you cover?",
        "answer": "We cover 25+ companies including FAANG (Google, Amazon, Meta, Microsoft, Apple, Netflix), product companies (Flipkart, Razorpay, Swiggy, Zomato), services (TCS, Infosys, Wipro, HCL, Cognizant, Accenture), and startups (Paytm, Ola, CRED, Meesho).",
    },
    {
        "id": "faq5",
        "question": "How does the AI Interviewer work?",
        "answer": "The AI Interviewer asks role-specific questions, evaluates your answers using rubric-based scoring, provides follow-up questions, and generates a competency-level diagnosis with repair paths.",
    },
]


@router.get("/faq")
async def get_faq():
    """Get frequently asked questions."""
    return {"faqs": FAQS}
