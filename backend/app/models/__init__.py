"""SQLAlchemy models package — all domain models for PostgreSQL migration."""

from app.models.assessments import (
    AssessmentAttempt,
    AssessmentSection,
    CodingSubmission,
    CompanyAssessmentMetadata,
    ExecutionResult,
    InterviewSession,
    OASession,
    Response,
)
from app.models.base import Base
from app.models.career import CareerProfile, PortfolioProject, ResumeMetadata, UploadedFile
from app.models.content import (
    AssessmentDefinition,
    AssessmentVariant,
    ContentPackage,
    ContentVersion,
    QuestionMetadata,
    TrustRecord,
)
from app.models.gamification import Badge, GamificationProfile, StreakRecord, UserBadge, XPEventLedger
from app.models.identity import RefreshToken, User, UserIdentityMap, UserProfile, UserSession
from app.models.learning import (
    LearnerSkillState,
    LearningAttempt,
    LearningEvidence,
    MasterySnapshot,
    RemediationAttempt,
    RepairMission,
    ReviewCard,
    Skill,
    SkillPrerequisite,
)
from app.models.operations import AnalyticsEvent, AnalyticsRollup, AuditLog, BillingRecord

__all__ = [
    "Base",
    # Identity
    "User",
    "UserProfile",
    "UserSession",
    "RefreshToken",
    "UserIdentityMap",
    # Learning
    "Skill",
    "SkillPrerequisite",
    "LearnerSkillState",
    "LearningAttempt",
    "LearningEvidence",
    "MasterySnapshot",
    "ReviewCard",
    "RepairMission",
    "RemediationAttempt",
    # Content
    "ContentPackage",
    "ContentVersion",
    "QuestionMetadata",
    "TrustRecord",
    "AssessmentDefinition",
    "AssessmentVariant",
    # Assessments
    "AssessmentAttempt",
    "AssessmentSection",
    "Response",
    "CodingSubmission",
    "ExecutionResult",
    "OASession",
    "InterviewSession",
    "CompanyAssessmentMetadata",
    # Gamification
    "GamificationProfile",
    "XPEventLedger",
    "Badge",
    "UserBadge",
    "StreakRecord",
    # Career
    "CareerProfile",
    "PortfolioProject",
    "ResumeMetadata",
    "UploadedFile",
    # Operations
    "AnalyticsEvent",
    "AnalyticsRollup",
    "AuditLog",
    "BillingRecord",
]
