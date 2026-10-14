"""Mission definitions — the student-facing learning unit.

A mission binds one teaching loop (backend STEP_TYPES, nine canonical stages)
to trust-filtered question-bank IDs, one company overlay, one mentor skill,
and a capability-attached reward + forward consequence.

Binding rules (see docs/MISSION_CONTRACT.md):
- Stages use canonical names only. No invented stages, none skipped.
- Question content is NEVER inline: missions carry bank_refs (IDs). Every
  ref must resolve through question_store's serving gate TODAY.
- Company language is pattern-relevant unless the bank ref carries verified
  provenance + explicit companies tags.
- New content enters UNVERIFIED and is never served until the trust pipeline
  promotes it. validate_mission() enforces the servable-refs rule.
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.content.lesson_definitions import STEP_TYPES

Verdict = Literal["mastered", "developing", "repair_needed"]
#: Floor for bank refs. The serving gate itself admits verified/reviewed
#: only; the floor is defense in depth on top of find_one().
TrustFloor = Literal["reviewed", "verified"]

#: Chrome allowed around (never instead of) the nine canonical stages.
CHROME_STAGES = ("intro", "practice", "recognize", "prove", "reward")

#: Canonical order. validate_mission() requires this exact sequence.
CANONICAL_ORDER = list(STEP_TYPES)

_TRUST_ORDER = {"unverified": 0, "automated_checked": 1, "reviewed": 2, "verified": 3}


class MissionBrief(BaseModel):
    """The 10-second threat + goal + reward. Names the round it prepares."""
    mission_title: str
    round_name: str = ""  # e.g. "TCS NQT Round 1 — aptitude"
    threat: str = ""  # what eliminates candidates here
    goal: str = ""
    reward_diamonds: int = 0


class MissionStage(BaseModel):
    """One canonical stage. Either inline teaching OR bank refs — the check
    that proves the stage must always be explicit.

    ``moments`` hosts additional interaction moments inside the stage
    (e.g. manipulate stages host the change_one_thing moment: controlled
    variation is what manipulation is). The contract gate reads
    interactions ∪ moments.
    """
    stage: str
    title: str = ""
    interaction: str = ""  # one of the contract's interaction subtypes
    moments: List[str] = Field(default_factory=list)  # more subtypes, same vocab
    check: str = ""  # how this stage is evidenced, e.g. "mcq:predict"
    bank_refs: List[str] = Field(default_factory=list)
    mentor_moment: str = "intro"  # one of mentor_service.MOMENTS
    time_limit_seconds: int = 0  # >0 required on mastery (timed_prove)

    @field_validator("stage")
    @classmethod
    def _canonical_stage(cls, v: str) -> str:
        if v not in STEP_TYPES:
            raise ValueError(f"non-canonical stage {v!r}; see STEP_TYPES")
        return v


class MissionReward(BaseModel):
    diamonds: int = 0
    unlocks: str = ""


class MissionConsequence(BaseModel):
    """The forward commitment the journey engine reads."""
    on_mastery: str = ""  # e.g. "harder transfer in 2 days"
    on_developing: str = ""  # e.g. "retrieval drill tomorrow"
    on_repair: str = ""  # e.g. "repair mission before advancing"


class MissionDefinition(BaseModel):
    id: str  # e.g. "tcs_nqt.percentages_change"
    track_id: str = ""  # company track, e.g. "tcs_nqt"
    domain: str = ""  # aptitude | reasoning | verbal | coding | cs_core | company_quest
    canonical_skill: str = ""
    brief: MissionBrief
    stages: List[MissionStage] = Field(default_factory=list)
    mentor_skill: str = ""
    company_overlay_id: str = ""
    provenance: str = "pattern-relevant"  # or "verified"
    reward: MissionReward = Field(default_factory=MissionReward)
    consequence: MissionConsequence = Field(default_factory=MissionConsequence)
    frontend_slug: str = ""  # MissionPlayer slug, 1:1
    lesson_slug: str = ""  # backend lesson, when one exists
    trust_floor: TrustFloor = "automated_checked"
    status: str = "unverified"  # trust pipeline status of THIS mission


def validate_mission(m: MissionDefinition) -> List[str]:
    """Machine gate. Returns error strings (empty = conformant).

    Checks structure synchronously; bank refs resolve against the live
    question_store serving gate (no unverified content behind a mission).
    """
    from app.services import question_store as qs

    errors: List[str] = []

    got = [s.stage for s in m.stages]
    if got != CANONICAL_ORDER:
        errors.append(
            "stages must be the nine canonical stages in order; got %s" % (got,)
        )

    moments = {
        "intro", "correct_1", "correct_2", "wrong_1", "wrong_2",
        "after_break", "after_mastery", "retry_prompt",
    }
    interactions = {
        "visual_hook", "micro_animation", "state_trace", "drag_or_manipulate",
        "tap_to_reveal", "predict_output", "multiple_choice_reasoning",
        "change_one_thing", "fill_in_blank", "code_reorder", "tiny_build",
        "interactive_diagram", "match_relationships", "sort_steps",
        "parameter_slider", "before_after", "break_and_debug", "error_hunt",
        "explain_the_bug", "recall_check", "srs_card", "transfer_problem",
        "timed_prove",
    }
    floor = _TRUST_ORDER[m.trust_floor]
    for s in m.stages:
        for token in [s.interaction] + list(s.moments):
            if token and token not in interactions:
                errors.append(f"stage {s.stage}: unknown interaction {token!r}")
        if s.mentor_moment not in moments:
            errors.append(f"stage {s.stage}: unknown mentor moment {s.mentor_moment!r}")
        if s.stage == "mastery" and s.time_limit_seconds <= 0:
            errors.append("mastery stage requires time_limit_seconds > 0 (timed_prove)")
        for ref in s.bank_refs:
            q = qs.find_one({"id": ref})
            if q is None:
                errors.append(f"stage {s.stage}: bank ref {ref!r} not servable")
                continue
            rank = _TRUST_ORDER.get(str(q.get("trust_status", "unverified")).lower(), 0)
            if rank < floor:
                errors.append(
                    f"stage {s.stage}: bank ref {ref!r} trust "
                    f"{q.get('trust_status')} below floor {m.trust_floor}"
                )

    ix = {s.interaction for s in m.stages}
    ix |= {mm for s in m.stages for mm in s.moments}
    ix.discard("")
    if "change_one_thing" not in ix:
        errors.append("mission requires a change_one_thing moment")
    if "timed_prove" not in ix and not any(
        s.stage == "mastery" and s.time_limit_seconds > 0 for s in m.stages
    ):
        errors.append("mission requires a real timed_prove")

    if m.provenance == "verified":
        for s in m.stages:
            for ref in s.bank_refs:
                q = qs.find_one({"id": ref}) or {}
                if not q.get("provenance") or not q.get("companies"):
                    errors.append(
                        f"verified provenance requires bank provenance+companies on {ref!r}"
                    )
                    break

    if not m.mentor_skill:
        errors.append("mentor_skill is required (drives Captain Byte moments)")
    if not (m.consequence.on_mastery and m.consequence.on_repair):
        errors.append("consequence.on_mastery and consequence.on_repair are required")
    return errors


def mission_index(missions: List[MissionDefinition]) -> Dict[str, Dict[str, Any]]:
    """Journey planner view: mission_id -> routing refs (no content)."""
    return {
        m.id: {
            "lesson_slug": m.lesson_slug,
            "frontend_slug": m.frontend_slug,
            "mentor_skill": m.mentor_skill,
            "company_overlay_id": m.company_overlay_id,
            "track_id": m.track_id,
        }
        for m in missions
    }
