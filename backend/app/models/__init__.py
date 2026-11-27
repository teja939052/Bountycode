"""SQLAlchemy models package — all domain models for PostgreSQL migration."""

from app.models.assessments import (
    AssessmentAttempt,
    AssessmentSection,
    CodingSubmission,
    CompanyAssessmentMetadata,
    ExecutionResult,
    InterviewBooking,
    InterviewSession,
    OASession,
    QuestionAnswer,
    Response,
    SolvedProblem,
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
from app.models.enterprise import Cohort, SkillGraph, Gamification
from app.models.identity import RefreshToken, User, UserIdentityMap, UserProfile, UserSession
from app.models.learning import (
    DailyChallengeUser,
    LearnerSkillState,
    LearningAttempt,
    LearningEvidence,
    LearningModule,
    MasterySnapshot,
    RemediationAttempt,
    RepairMission,
    ReviewCard,
    Skill,
    SkillPrerequisite,
    UserLearningProgress,
)
from app.models.operations import AnalyticsEvent, AnalyticsRollup, AuditLog, BillingRecord, RevenueEvent

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
    "DailyChallengeUser",
    "LearningAttempt",
    "LearningEvidence",
    "LearningModule",
    "MasterySnapshot",
    "RemediationAttempt",
    "ReviewCard",
    "UserLearningProgress",
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
    "InterviewBooking",
    "InterviewSession",
    "QuestionAnswer",
    "SolvedProblem",
    "CompanyAssessmentMetadata",
    # Gamification
    "GamificationProfile",
    "XPEventLedger",
    "Badge",
    "UserBadge",
    "StreakRecord",
    "Cohort",
    "SkillGraph",
    "Gamification",
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
    "RevenueEvent",
]
