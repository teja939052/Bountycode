"""Learning path and company track models."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class LearningPathEnroll(BaseModel):
    path_id: str = Field(min_length=1)
    company_track_id: Optional[str] = None


class PathModuleProgress(BaseModel):
    module_id: str
    completed: bool = False
    completed_at: Optional[str] = None
    xp_earned: int = 0
    score: Optional[float] = None
    attempts: int = 0
    activities_completed: List[str] = []


class UserPathProgress(BaseModel):
    user_id: str
    path_id: str
    enrolled_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    current_module_id: Optional[str] = None
    modules: Dict[str, PathModuleProgress] = {}
    total_xp_earned: int = 0
    completed: bool = False
    completed_at: Optional[str] = None
    last_activity_at: Optional[str] = None


class UserTrackProgress(BaseModel):
    user_id: str
    track_id: str
    enrolled_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    current_section_id: Optional[str] = None
    sections: Dict[str, Dict[str, Any]] = {}
    total_xp_earned: int = 0
    completed: bool = False
    completed_at: Optional[str] = None
    mock_score: Optional[float] = None
    last_activity_at: Optional[str] = None


class LearningPathSummary(BaseModel):
    id: str
    name: str
    short_name: str
    icon: str
    color: str
    description: str
    target_roles: List[str]
    avg_package: str
    duration_weeks: int
    difficulty: str
    total_modules: int
    total_xp: int
    enrolled: bool = False
    progress_pct: float = 0.0
    completed: bool = False


class CompanyTrackSummary(BaseModel):
    id: str
    company_id: str
    name: str
    full_name: str
    icon: str
    color: str
    role: str
    package_range: str
    duration_minutes: int
    difficulty: str
    description: str
    total_sections: int
    total_modules: int
    total_xp: int
    enrolled: bool = False
    progress_pct: float = 0.0
    completed: bool = False


class PathModuleDetail(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    color: str
    duration_days: int
    xp_reward: int
    topics: List[str]
    skills: List[str]
    activities: List[str]
    unlocks: List[str]
    depends_on: List[str] = []
    completed: bool = False
    locked: bool = True
    score: Optional[float] = None


class TrackModuleDetail(BaseModel):
    id: str
    title: str
    description: str
    duration_minutes: int
    questions_count: int
    xp_reward: int
    topics: List[str]
    completed: bool = False
    locked: bool = True
    score: Optional[float] = None


class PathRecommendation(BaseModel):
    path_id: str
    reason: str
    match_score: float
    based_on: List[str]
