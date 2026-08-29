"""World / Town / Level / Boss schemas for the BountyCode learning game.

A World is a capability transformation containing Towns. Each Town contains
Levels and a Boss. Levels expose the learning loop: discover → understand →
manipulate → predict → build → break → debug → retrieve → transfer.

The same schema is shared by:
- backend route handlers (routes/worlds.py)
- frontend type definitions (pages/WorldJourney.tsx)
- capability curriculum mapping (data/capability_curriculum.py)
"""

from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


class Tutor(BaseModel):
    name: str = "Byte"
    avatar: str = "🧭"
    discover: str = ""
    explain: str = ""


class Story(BaseModel):
    location: str = ""
    npc: str = ""
    line: str = ""


class Discover(BaseModel):
    visual: str = ""
    interaction: str = ""
    prompt: str = ""
    answer: str = ""
    values: Optional[list[Any]] = None


class Manipulate(BaseModel):
    type: str = ""
    template: Optional[str] = None
    answer: str | list[str] = ""
    blocks: Optional[list[str]] = None
    hint: Optional[str] = None


class Predict(BaseModel):
    prompt: str = ""
    answer: str = ""
    explanation: str = ""


class Build(BaseModel):
    prompt: str = ""
    starter: str = ""
    placeholder: str = ""
    language: str = "python"


class BreakStep(BaseModel):
    prompt: str = ""
    broken_code: str = ""
    expected_failure: str = ""


class Debug(BaseModel):
    prompt: str = ""
    buggy_code: str = ""
    fix_steps: list[str] = []
    answer: str = ""


class Retrieval(BaseModel):
    prompt: str = ""
    answer: str = ""
    explanation: str = ""


class Transfer(BaseModel):
    prompt: str = ""
    answer: str = ""
    context: str = ""


class Code(BaseModel):
    prompt: str = ""
    starter: str = ""
    placeholder: str = ""
    language: str = "python"


class Checks(BaseModel):
    required_patterns: list[str] = []
    forbidden: list[str] = []
    hint_triggers: list[str] = []


class Success(BaseModel):
    world_before: Optional[str] = None
    world_after: Optional[str] = None
    world_reaction: str = ""
    reward_text: str = ""
    byte_line: Optional[str] = None
    xp: int = 0


class Reward(BaseModel):
    xp: int = 0
    coins: int = 0
    badges: list[str] = []
    unlocks_town: Optional[str] = None
    unlocks_world: Optional[str] = None
    title: Optional[str] = None


class BossSuccess(BaseModel):
    world_before: Optional[str] = None
    world_after: Optional[str] = None
    world_reaction: str = ""
    reward_text: str = ""
    byte_line: Optional[str] = None
    reward: Reward = Field(default_factory=Reward)


class LevelBase(BaseModel):
    model_config = {"populate_by_name": True}

    id: str
    title: str
    kind: str = "level"
    icon: str = ""
    order: int = 0
    concept: str = ""
    mental_model: str = ""
    canonical_skill: str = ""
    maps_to_competency: Optional[str] = None
    story: Story = Field(default_factory=Story)
    tutor: Tutor = Field(default_factory=Tutor)
    discover: Discover = Field(default_factory=Discover)
    understand: Optional[str] = None
    manipulate: Manipulate = Field(default_factory=Manipulate)
    predict: Optional[Predict] = None
    build: Optional[Build] = None
    break_step: Optional[BreakStep] = Field(default=None, alias="break")
    debug: Optional[Debug] = None
    code: Code = Field(default_factory=Code)
    checks: Checks = Field(default_factory=Checks)
    hints: list[str] = []
    retrieval: Optional[Retrieval] = None
    transfer: Optional[Transfer] = None
    mastery_threshold: Optional[int] = None
    estimated_minutes: Optional[int] = None
    reward: Optional[Reward] = None
    success: Success = Field(default_factory=Success)
    unlocks: Optional[str] = None


class Level(LevelBase):
    pass


class Boss(LevelBase):
    kind: str = "boss"
    mastery_threshold: Optional[int] = 80
    reward: Reward = Field(default_factory=Reward)


class Town(BaseModel):
    id: str
    name: str
    icon: str = ""
    description: str = ""
    order: int = 0
    mental_model: str = ""
    canonical_skills: list[str] = []
    competencies: list[str] = []
    levels: list[Level | Boss] = []
    boss: Optional[Boss] = None


class World(BaseModel):
    id: str
    name: str
    subtitle: str = ""
    description: str = ""
    icon: str = ""
    order: int = 0
    theme: str = ""
    recommended_roles: list[str] = []
    prerequisites: list[str] = []
    towns: list[Town] = []
    completion_reward: Optional[Reward] = None
