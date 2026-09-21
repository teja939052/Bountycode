"""Schemas for blog/article/game content types.

These are intentionally empty/structural — they provide the shape for verified
content only. No LLM-generated content may be promoted into these stores
without passing the trust pipeline: UNVERIFIED → AUTOMATED_CHECKED →
HUMAN_REVIEWED → TRUSTED.
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ContentBlock(BaseModel):
    """A single block within a blog/article/game body."""
    type: str = Field(..., description="text|code|image|quiz|terminal|callout")
    content: str = Field(..., description="Markdown text, code snippet, URL, or structured payload")
    language: Optional[str] = Field(None, description="For code blocks: python|cpp|java|js|...")
    caption: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)


class BlogPost(BaseModel):
    slug: str
    title: str
    excerpt: str
    content_blocks: List[ContentBlock] = Field(default_factory=list)
    world_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    author: str = "content-team"
    verified_status: str = "UNVERIFIED"
    trust_pipeline_version: str = "v1"
    expected_outputs: Optional[Dict[str, Any]] = Field(None, description="Required for code-containing blocks before promotion to TRUSTED")
    provenance: Optional[str] = Field(None, description="Source URL or author credentials for HUMAN_REVIEWED+ content")
    reading_time_minutes: Optional[int] = None


class Article(BlogPost):
    subtype: str = Field("article", description="article|whitepaper|case-study|company-guide")
    company_tags: List[str] = Field(default_factory=list)
    role_tags: List[str] = Field(default_factory=list)


class GameConfig(BaseModel):
    type: str = Field(..., description="pattern-quiz|debug-arena|terminal-challenge|drag-drop|simulation")
    difficulty: str = "easy"
    xp_reward: int = 20
    time_limit_seconds: Optional[int] = None
    attempts_allowed: int = 3
    passing_score: int = 60
    tags: List[str] = Field(default_factory=list)
    world_id: Optional[str] = None
    lesson_id: Optional[str] = None


class Game(BaseModel):
    slug: str
    title: str
    description: str
    config: GameConfig
    content_blocks: List[ContentBlock] = Field(default_factory=list)
    solutions: Optional[Dict[str, Any]] = Field(None, description="Hidden until attempt; required for AUTOMATED_CHECKED")
    verified_status: str = "UNVERIFIED"
    trust_pipeline_version: str = "v1"
    provenance: Optional[str] = None


class TrustGateRecord(BaseModel):
    content_id: str
    content_type: str = Field(..., description="question|lesson|blog|article|game")
    status: str = "UNVERIFIED"
    auto_checks_passed: bool = False
    human_reviewed_by: Optional[str] = None
    promoted_at: Optional[str] = None
    notes: Optional[str] = None
