"""
Explicit router registry for BountyCode backend.

Replaces dynamic pkgutil router discovery in main.py with an explicit,
versioned, auditable registry. Every route module is listed here with its
module path, router attribute name, URL prefix, and tags.

Startup validation:
- Every required router must register successfully
- No duplicate (method, path) combinations
- Critical route prefixes must be correct
- No router may fail to import

This registry is the single source of truth for backend route ownership.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from typing import Any


@dataclass(frozen=True)
class RouteEntry:
    """A single route module registration entry."""
    module: str  # e.g. "app.routes.auth"
    router_attr: str = "router"  # attribute name on the module holding the APIRouter
    prefix: str = ""  # URL prefix for the router
    tags: list[str] = field(default_factory=list)
    required: bool = True  # if import fails, app refuses to start


# ── Route registry ─────────────────────────────────────────────────────────
# Order matters: more specific prefixes should register before less specific
# ones to avoid FastAPI route shadowing.
ROUTE_REGISTRY: list[RouteEntry] = [
    # Auth (foundational — must register first)
    RouteEntry("app.routes.auth", "router", "/api/v1/auth", ["auth"], True),

    # Onboarding
    RouteEntry("app.routes.onboarding", "router", "/api/v1/onboarding", ["onboarding"], True),
    RouteEntry("app.routes.onboarding_launch", "router", "/api/v1/onboarding", ["onboarding-launch"], True),
    RouteEntry("app.routes.onboarding_diagnostic", "router", "/api/v1/onboarding/diagnostic", ["onboarding-diagnostic"], True),
    RouteEntry("app.routes.onboarding_doors", "router", "/api/v1/onboarding/doors", ["onboarding-doors"], True),

    # Academy
    RouteEntry("app.routes.academy_diagnostic", "router", "/api/v1/academy/diagnostic", ["academy-diagnostic"], True),
    RouteEntry("app.routes.academy_plan", "router", "/api/v1/academy/plan", ["academy-plan"], True),
    RouteEntry("app.routes.academy_profile", "router", "/api/v1/academy/profile", ["academy-profile"], True),

    # Adaptive learning
    RouteEntry("app.routes.adaptive_learning", "router", "/api/v1/adaptive", ["adaptive"], True),

    # AI
    RouteEntry("app.routes.ai_debugger", "router", "/api/v1/ai-debugger", ["ai-debugger"], True),
    RouteEntry("app.routes.ai_feedback", "router", "/api/v1/feedback", ["ai-feedback"], True),

    # Analytics
    RouteEntry("app.routes.analytics", "router", "/api/v1/analytics", ["analytics"], True),
    RouteEntry("app.routes.analytics_admin", "router", "/api/v1/analytics", ["analytics"], True),

    # Aptitude
    RouteEntry("app.routes.aptitude", "router", "/api/v1/aptitude", ["aptitude"], True),
    RouteEntry("app.routes.aptitude_tests", "router", "/api/v1/aptitude-tests", ["aptitude-tests"], True),

    # Assessments
    RouteEntry("app.routes.assessments", "router", "/api/v1/assessments", ["assessments"], True),

    # Admin
    RouteEntry("app.routes.admin_monitoring", "router", "/api/v1/admin", ["admin"], True),
    RouteEntry("app.routes.admin_content", "router", "/api/v1/admin/content", ["admin-content"], True),

    # Billing
    RouteEntry("app.routes.billing", "router", "/api/v1/billing", ["billing"], True),

    # Blog
    RouteEntry("app.routes.blog", "router", "/api/v1/blog", ["blog"], True),

    # Career profile
    RouteEntry("app.routes.career_profile", "router", "/api/v1/profile", ["career-profile"], True),

    # Behavioral
    RouteEntry("app.routes.behavioral", "router", "/api/v1/behavioral", ["behavioral"], True),

    # Companies
    RouteEntry("app.routes.companies", "router", "/api/v1/companies", ["companies"], True),
    RouteEntry("app.routes.company_directory", "router", "/api/v1/company-directory", ["Company Directory"], True),
    RouteEntry("app.routes.company_lessons", "router", "/api/v1/company-lessons", ["company-lessons"], True),
    RouteEntry("app.routes.company_mocks", "router", "/api/v1/company-mocks", ["company-mocks"], True),
    RouteEntry("app.routes.company_prep", "router", "/api/v1/company-prep", ["company-prep"], True),
    RouteEntry("app.routes.company_tracks", "router", "/api/v1/company-tracks", ["company-tracks"], True),

    # Compiler
    RouteEntry("app.routes.compiler", "router", "/api/v1/compiler", ["compiler"], True),

    # Concepts
    RouteEntry("app.routes.concepts", "router", "/api/v1/concepts", ["concepts"], True),

    # Content
    RouteEntry("app.routes.content", "router", "/api/v1/content", ["content"], True),
    RouteEntry("app.routes.content_factory", "router", "/api/v1/admin/content", ["content-factory"], True),

    # Coupon
    RouteEntry("app.routes.coupon", "router", "/api/v1/coupon", ["coupon"], True),

    # Cover letter
    RouteEntry("app.routes.cover_letter", "router", "/api/v1/tools", ["tools"], True),

    # Curriculum
    RouteEntry("app.routes.curriculum", "router", "/api/v1/curriculum", ["Curriculum"], True),

    # Daily
    RouteEntry("app.routes.daily_challenge", "router", "/api/v1/daily", ["daily-challenge"], True),
    RouteEntry("app.routes.daily_challenge", "challenge_router", "/api/v1/daily-challenge", ["30-day-challenge"], True),
    RouteEntry("app.routes.daily_problem", "router", "/api/v1/daily-problem", ["daily-problem"], True),

    # Discussions
    RouteEntry("app.routes.discussions", "router", "/api/v1/discussions", ["discussions"], True),

    # Distributions
    RouteEntry("app.routes.distributions", "router", "/api/v1/distributions", ["distributions"], True),

    # DSA fingerprint
    RouteEntry("app.routes.dsa_fingerprint", "router", "/api/v1/fingerprint", ["dsa-fingerprint"], True),

    # Enhanced
    RouteEntry("app.routes.enhanced", "router", "/api/v1/enhanced", ["enhanced"], True),

    # Enterprise
    RouteEntry("app.routes.enterprise", "router", "/api/v1/enterprise", ["enterprise"], True),

    # Exam
    RouteEntry("app.routes.exam", "router", "/api/v1/exam", ["exam"], True),
    RouteEntry("app.routes.exam_memories", "router", "/api/v1/exam-memories", ["exam-memories"], True),

    # Evidence
    RouteEntry("app.routes.evidence", "router", "/api/v1/evidence", ["evidence"], True),

    # Features
    RouteEntry("app.routes.features", "router", "/api/v1/features", ["features"], True),

    # Free
    RouteEntry("app.routes.free_practice", "router", "/api/v1/free", ["free-practice"], True),
    RouteEntry("app.routes.free_trial", "router", "/api/v1/free-trial", ["free-trial"], True),

    # Gamification
    RouteEntry("app.routes.gamification", "router", "/api/v1/gamification", ["gamification"], True),

    # Health
    RouteEntry("app.routes.health", "router", "/api/v1/health", ["health"], True),

    # HR
    RouteEntry("app.routes.hr", "router", "/api/v1/hr", ["hr"], True),

    # Indian placement
    RouteEntry("app.routes.indian_placement", "router", "/api/v1/indian-placement", ["indian-placement"], True),

    # Interview
    RouteEntry("app.routes.interview", "router", "/api/v1/interview", ["interview"], True),
    RouteEntry("app.routes.interview_replay", "router", "/api/v1/interview", ["interview-replay"], True),
    RouteEntry("app.routes.mock_interview", "router", "/api/v1/interview", ["mock-interview"], True),
    RouteEntry("app.routes.interview_chat", "router", "/api/v1/interview-chat", ["interview-chat"], True),

    # Interview booking
    RouteEntry("app.routes.interview_booking", "router", "/api/v1/interview-booking", ["interview-booking"], True),

    # Invoices
    RouteEntry("app.routes.invoices", "router", "/api/v1/invoices", ["invoices"], True),

    # Journey
    RouteEntry("app.routes.journey", "router", "/api/v1/journey", ["journey"], True),

    # Language paths
    RouteEntry("app.routes.language_paths", "router", "/api/v1/languages", ["languages"], True),

    # Learning
    RouteEntry("app.routes.learning", "router", "/api/v1/learning", ["learning"], True),
    RouteEntry("app.routes.learning_modules", "router", "/api/v1/learning-modules", ["Learning Modules"], True),
    RouteEntry("app.routes.learning_paths", "router", "/api/v1/learning-paths", ["learning-paths"], True),

    # Lesson
    RouteEntry("app.routes.lesson", "router", "/api/v1/lesson", ["lesson"], True),
    RouteEntry("app.routes.lessons", "router", "/api/v1/lessons", ["lessons"], True),

    # Map
    RouteEntry("app.routes.map", "router", "/api/v1/map", ["map", "adventure"], True),

    # Metrics
    RouteEntry("app.routes.metrics", "router", "/api/v1/metrics", ["metrics"], True),

    # Mock interview
    RouteEntry("app.routes.mock_interview", "router", "/api/v1/interview", ["mock-interview"], True),

    # OA
    RouteEntry("app.routes.oa", "router", "/api/v1/oa", ["oa"], True),
    RouteEntry("app.routes.oa_engine", "router", "/api/v1/oa", ["oa-engine"], True),

    # Observability
    RouteEntry("app.routes.observability", "router", "/observability", ["observability"], True),

    # Placement
    RouteEntry("app.routes.placement", "router", "/api/v1/placement", ["placement"], True),
    RouteEntry("app.routes.placement_calendar", "router", "/api/v1/placement-calendar", ["Placement Calendar"], True),
    RouteEntry("app.routes.placement_packs", "router", "/api/v1/placement-packs", ["placement-packs"], True),
    RouteEntry("app.routes.placement_questions", "router", "/api/v1/placement-questions", ["placement-questions"], True),

    # Personal dashboard
    RouteEntry("app.routes.personal_dashboard", "router", "/api/v1/dashboard", ["personal-dashboard"], True),

    # Playlists
    RouteEntry("app.routes.playlists", "router", "/api/v1/playlists", ["playlists"], True),

    # Practice
    RouteEntry("app.routes.practice", "router", "/api/v1/practice", ["practice"], True),

    # Problems
    RouteEntry("app.routes.problems", "router", "/api/v1/problems", ["problems"], True),

    # Predictor
    RouteEntry("app.routes.predictor", "router", "/api/v1/predictor", ["predictor"], True),

    # Progress
    RouteEntry("app.routes.progress", "router", "/api/v1/progress", ["progress"], True),

    # Profile stats
    RouteEntry("app.routes.profile_stats", "router", "/api/v1/profile", ["profile"], True),

    # Public
    RouteEntry("app.routes.public", "router", "/api/v1/public", ["public"], True),

    # Questions
    RouteEntry("app.routes.questions", "router", "/api/v1/questions", ["question-bank"], True),
    RouteEntry("app.routes.questions_solve", "router", "/api/v1/questions", ["question-solve"], True),

    # Quiz
    RouteEntry("app.routes.quiz", "router", "/api/v1/quiz", ["Quiz & Mock Interview"], True),

    # Readiness
    RouteEntry("app.routes.readiness", "router", "/api/v1/readiness", ["readiness"], True),

    # Repair
    RouteEntry("app.routes.repair", "router", "/api/v1/repair", ["repair"], True),

    # Resume
    RouteEntry("app.routes.resume", "router", "/api/v1/resume", ["resume"], True),

    # Revenue
    RouteEntry("app.routes.revenue", "router", "/api/v1/revenue", ["Revenue"], True),

    # Roles
    RouteEntry("app.routes.roles", "router", "/api/v1/roles", ["roles"], True),

    # Runtime
    RouteEntry("app.routes.runtime", "router", "/api/v1/runtime", ["local-runtime"], True),

    # SDE diagnostic
    RouteEntry("app.routes.sde_diagnostic", "router", "/api/v1/sde", ["sde-diagnostic"], True),

    # Service sprint
    RouteEntry("app.routes.service_sprint", "router", "/api/v1/sprint", ["service-sprint"], True),

    # SRS
    RouteEntry("app.routes.srs", "router", "/api/v1/srs", ["spaced-repetition-problems"], True),

    # Student discount
    RouteEntry("app.routes.student_discount", "router", "/api/v1/discount", ["discount"], True),

    # Student features
    RouteEntry("app.routes.student_features", "router", "/api/v1/student", ["student-features"], True),

    # Study
    RouteEntry("app.routes.study", "router", "/api/v1/study", ["study-engine"], True),
    RouteEntry("app.routes.study_library", "router", "/api/v1/study", ["study"], True),

    # Study extended
    RouteEntry("app.routes.study_extended", "router", "/api/v1/study-extended", ["study-extended"], True),

    # Study timer
    RouteEntry("app.routes.study_timer", "router", "/api/v1/study-timer", ["study-timer"], True),

    # Submissions
    RouteEntry("app.routes.submissions", "router", "/api/v1/submissions", ["submissions"], True),

    # System design
    RouteEntry("app.routes.system_design", "router", "/api/v1/system-design", ["system-design"], True),
    RouteEntry("app.routes.system_design_tests", "router", "/api/v1/system-design-tests", ["system-design-tests"], True),

    # Target
    RouteEntry("app.routes.target", "router", "/api/v1/target", ["target"], True),

    # TCS NQT
    RouteEntry("app.routes.tcs_nqt", "router", "/api/v1/tcs-nqt", ["tcs-nqt"], True),

    # Tiers
    RouteEntry("app.routes.tiers", "router", "/api/v1/tiers", ["tiers"], True),

    # Trace
    RouteEntry("app.routes.trace", "router", "/api/v1/trace", ["trace"], True),

    # Tracks
    RouteEntry("app.routes.tracks", "router", "/api/v1/tracks", ["tracks"], True),

    # Trial
    RouteEntry("app.routes.trial", "router", "/api/v1/trial", ["trial"], True),

    # Visualizations
    RouteEntry("app.routes.visualizations", "router", "/api/v1/visualizations", ["visualizations"], True),

    # Worlds
    RouteEntry("app.routes.worlds", "router", "/api/v1/worlds", ["worlds"], True),
]


def load_router(entry: RouteEntry) -> Any:
    """Import a route module and return its router attribute.

    Raises ImportError if the module or router attribute is missing.
    """
    module = import_module(entry.module)
    router = getattr(module, entry.router_attr, None)
    if router is None:
        raise ImportError(
            f"Module {entry.module} has no attribute '{entry.router_attr}'"
        )
    return router


def collect_all_routers() -> list[tuple[str, Any, str, list[str]]]:
    """Load all registered routers.

    Returns a list of (module_name, router, prefix, tags) tuples.

    Raises ImportError if any required router fails to load.
    """
    routers = []
    for entry in ROUTE_REGISTRY:
        router = load_router(entry)
        routers.append((entry.module, router, entry.prefix, entry.tags))
    return routers


def get_duplicate_prefixes() -> dict[str, list[str]]:
    """Find modules that share the same URL prefix (potential conflicts)."""
    from collections import defaultdict

    prefix_map: dict[str, list[str]] = defaultdict(list)
    for entry in ROUTE_REGISTRY:
        prefix_map[entry.prefix].append(entry.module)
    return {p: mods for p, mods in prefix_map.items() if len(mods) > 1}


def validate_no_duplicate_paths() -> list[str]:
    """Validate that no two routers register the same (method, path).

    Each router manages its own prefix internally (via APIRouter(prefix=...)).
    We do not add the registry prefix again, so the actual path is just
    route.path as defined in the router.

    Returns a list of error messages.
    """
    errors = []
    seen: dict[str, str] = {}  # "METHOD path" -> module

    for module_name, router, _prefix, _tags in collect_all_routers():
        for route in router.routes:
            path = getattr(route, "path", "") or ""
            methods = getattr(route, "methods", None) or set()
            for method in methods:
                key = f"{method} {path}"
                if key in seen:
                    errors.append(
                        f"Duplicate route {key}: defined in {seen[key]} "
                        f"and {module_name}"
                    )
                else:
                    seen[key] = module_name

    return errors
