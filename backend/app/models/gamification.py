"""Pydantic schemas for gamification profiles, badges, power-ups, and leaderboard entries."""

from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


class PowerUpEntry(BaseModel):
    extra_time: int = 0
    hint_reveal: int = 0
    retry: int = 0
    double_xp: int = 0
    skip_boss: int = 0
    show_answer: int = 0
    speed_boost: int = 0
    shield: int = 0
    x2_coins: int = 0
    auto_save: int = 0
    night_mode: int = 0
    focus_mode: int = 0


class GamificationProfile(BaseModel):
    user_id: str
    diamonds: int = 0
    level: int = 1
    streak: int = 0
    longest_streak: int = 0
    last_practice_date: Optional[str] = None
    badges: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    total_interviews: int = 0
    total_resumes: int = 0
    total_aptitude: int = 0
    total_coding: int = 0
    total_system_design: int = 0
    total_powerups_used: int = 0
    total_perfect_scores: int = 0
    stars_total: int = 0
    stars_per_problem: dict[str, int] = Field(default_factory=dict)
    coins: int = 0
    power_ups: PowerUpEntry = Field(default_factory=PowerUpEntry)
    bosses_defeated: list[int] = Field(default_factory=list)
    first_solve_today: Optional[str] = None
    weekly_challenges: list[dict[str, Any]] = Field(default_factory=list)
    monthly_challenges: list[dict[str, Any]] = Field(default_factory=list)
    weekly_league_xp: int = 0
    weekly_league_week: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class Badge(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    category: str
    rarity: str = "common"
    requirement: Optional[int] = None


class LeaderboardEntry(BaseModel):
    user_id: str
    name: str
    diamonds: int
    level: int
    rank: Optional[int] = None


class StreakStatus(BaseModel):
    streak: int
    longest_streak: int
    multiplier: float
    freezes: int
    protected: bool = False
    message: str = ""


class DailyChallengeData(BaseModel):
    id: str
    title: str
    description: str
    xp_reward: int
    coin_reward: int
    completed: bool
    claimed: bool
    progress: float = 0.0
    target: float = 1.0


class WeeklyChallengeData(BaseModel):
    id: str
    title: str
    description: str
    xp_reward: int
    progress: float = 0.0
    target: float = 1.0
    completed: bool = False
    claimed: bool = False


class SkillNode(BaseModel):
    id: str
    name: str
    category: str
    score: float = 0.0
    max_score: float = 10.0
    level: str = "beginner"


class TowerData(BaseModel):
    level: int
    diamonds: int
    xp_to_next: int
    xp_for_current_level: int
    title: str
    title_emoji: str
    streak: int
    streak_multiplier: float
    coins: int
    stars_total: int
    power_ups: dict[str, int] = Field(default_factory=dict)
    double_xp_expires: Optional[str] = None
    current_boss: Optional[dict[str, Any]] = None
    boss_level: Optional[int] = None
    bosses_defeated: list[int] = Field(default_factory=list)
    streak_freezes: int = 0
    daily_goal_count: int = 0
    daily_goal_target: int = 5
    daily_goal_completed: bool = False
