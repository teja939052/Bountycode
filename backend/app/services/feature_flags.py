"""Feature flags for managing 50+ features with gradual rollout support."""

from __future__ import annotations

from typing import Literal

Plan = Literal["free", "pro", "lifetime"]

from enum import Enum


class FeatureStatus(str, Enum):
    """Status of a feature flag."""
    DISABLED = "disabled"
    INTERNAL = "internal"
    BETA = "beta"
    GRADUAL = "gradual"
    ENABLED = "enabled"


class FeatureManager:
    """Simple feature flag manager for admin operations."""

    def __init__(self, flags: dict | None = None) -> None:
        self.flags = flags or FEATURE_FLAGS

    def get_all_flags(self) -> dict:
        """Return all feature flags."""
        return self.flags

    def update_flag(
        self,
        key: str,
        enabled: bool | None = None,
        status: FeatureStatus | None = None,
        rollout_percentage: int | None = None,
    ) -> None:
        """Update a feature flag."""
        if key not in self.flags:
            return
        flag = self.flags[key]
        if enabled is not None:
            flag["enabled"] = enabled
        if status is not None:
            flag["status"] = status.value
        if rollout_percentage is not None:
            flag["rollout_percentage"] = rollout_percentage

FEATURE_FLAGS: dict[str, dict] = {
    "interviews": {"enabled": True, "description": "AI mock interviews"},
    "resume": {"enabled": True, "description": "Resume builder and analyzer"},
    "aptitude": {"enabled": True, "description": "Aptitude test practice"},
    "coding": {"enabled": True, "description": "Coding challenges"},
    "compiler": {"enabled": True, "description": "LeetCode-style compiler"},
    "questions": {"enabled": True, "description": "Question bank"},
    "ai_mentor": {"enabled": True, "description": "AI mentor chat"},
    "project_generator": {"enabled": True, "description": "AI project generator"},
    "cover_letter": {"enabled": True, "description": "Cover letter generator"},
    "salary_negotiation": {"enabled": True, "description": "Salary negotiation coach"},
    "system_design": {"enabled": True, "description": "System design practice"},
    "company_prep": {"enabled": True, "description": "Company-specific prep"},
    "ai_debugger": {"enabled": True, "description": "AI-powered debugger"},
    "ai_feedback": {"enabled": True, "description": "Real-time AI feedback"},
    "gamification": {"enabled": True, "description": "XP, levels, streaks, badges"},
    "tower": {"enabled": True, "description": "Placement tower progression"},
    "daily_challenges": {"enabled": True, "description": "Daily adaptive challenges"},
    "leaderboard": {"enabled": True, "description": "Global leaderboard"},
    "rank": {"enabled": True, "description": "Honor/Kyu-Dan rank system"},
    "community": {"enabled": True, "description": "Community discussions"},
    "learning_hub": {"enabled": True, "description": "Learning hub"},
    "language_paths": {"enabled": True, "description": "7 language learning paths"},
    "learning_modules": {"enabled": True, "description": "Duolingo-style lessons"},
    "adaptive_path": {"enabled": True, "description": "AI-driven adaptive learning"},
    "dsa_fingerprint": {"enabled": True, "description": "DSA skill assessment"},
    "dsa_visualizer": {"enabled": True, "description": "Algorithm visualizations"},
    "concepts": {"enabled": True, "description": "Concept explanations"},
    "spaced_repetition": {"enabled": True, "description": "SRS mastery system"},
    "ats_optimizer": {"enabled": True, "description": "ATS score optimizer"},
    "salary_benchmark": {"enabled": True, "description": "Salary benchmark data"},
    "application_tracker": {"enabled": True, "description": "Job application tracker"},
    "career_profile": {"enabled": True, "description": "Career profile"},
    "interview_booking": {"enabled": True, "description": "Interview booking system"},
    "mock_oa": {"enabled": True, "description": "Mock online assessments"},
    "predictor": {"enabled": True, "description": "Placement prediction engine"},
    "readiness": {"enabled": True, "description": "Interview readiness scoring"},
    "indian_placement": {"enabled": True, "description": "Indian placement prep"},
    "campus_connect": {"enabled": True, "description": "Campus connect"},
    "campus_wars": {"enabled": True, "description": "Campus wars leaderboard"},
    "placement_drives": {"enabled": True, "description": "Placement drives"},
    "alumni_experiences": {"enabled": True, "description": "Alumni experiences"},

    "admin_dashboard": {"enabled": True, "description": "Admin analytics dashboard", "allowed_plans": ["pro", "lifetime"]},
    "admin_content": {"enabled": True, "description": "Admin content management", "allowed_plans": ["pro", "lifetime"]},
    "enterprise": {"enabled": True, "description": "Enterprise plan features", "allowed_plans": ["pro", "lifetime"]},
    "billing": {"enabled": True, "description": "PayPal/Stripe billing"},
    "pwa": {"enabled": True, "description": "Progressive Web App"},
    "push_notifications": {"enabled": True, "description": "Push notifications"},
    "offline_mode": {"enabled": True, "description": "Offline mode"},

    "retention_admin": {"enabled": True, "description": "Retention analytics admin", "allowed_plans": ["pro", "lifetime"]},
}


def is_feature_enabled(flag_key: str, plan: Plan = "free") -> bool:
    """Check if a feature is enabled for the given plan."""
    flag = FEATURE_FLAGS.get(flag_key)
    if not flag or not flag.get("enabled", False):
        return False

    allowed_plans = flag.get("allowed_plans")
    if allowed_plans and plan not in allowed_plans:
        return False

    return True


def get_enabled_features(plan: Plan = "free") -> list[str]:
    """Get all feature keys enabled for the given plan."""
    return [key for key, flag in FEATURE_FLAGS.items() if is_feature_enabled(key, plan)]


def set_feature_enabled(key: str, enabled: bool) -> None:
    """Enable or disable a feature flag."""
    if key in FEATURE_FLAGS:
        FEATURE_FLAGS[key]["enabled"] = enabled


async def init_feature_flags(db) -> None:
    """Initialize the feature-flag system.

    Flags are stored in-memory in ``FEATURE_FLAGS`` (see module docstring).
    This initializer is intentionally a no-op so the service can be dropped in
    as a startup hook without a DB dependency; future DB-backed rollout will go here.
    """
    return None


def get_feature_manager() -> FeatureManager:
    """Get a feature flag manager instance."""
    return FeatureManager()
