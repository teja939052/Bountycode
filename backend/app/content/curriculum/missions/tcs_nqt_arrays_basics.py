"""Exemplar mission: array basics (TCS NQT coding).

Status: UNVERIFIED mission structure (new, awaiting human review).
All bank_refs are servable TODAY (verified + provenance + companies).
Service-based coding is easy programs with hidden tests: find, count,
then two-pointers under time.
"""
from __future__ import annotations

from app.content.mission_definitions import (
    MissionBrief, MissionConsequence, MissionDefinition, MissionReward, MissionStage,
)

MISSION = MissionDefinition(
    id="tcs_nqt.arrays_basics",
    track_id="tcs_nqt",
    domain="coding",
    canonical_skill="code.arrays",
    brief=MissionBrief(
        mission_title="Own the Array",
        round_name="TCS NQT coding — easy programs, hidden tests",
        threat="Untested edge cases fail silently.",
        goal="Find, count, then reverse — all green first try.",
        reward_diamonds=60,
    ),
    stages=[
        MissionStage(stage="discover", title="See the layout",
                     interaction="state_trace", check="read",
                     mentor_moment="intro"),
        MissionStage(stage="manipulate", title="Change the input",
                     interaction="drag_or_manipulate", moments=["change_one_thing"],
                     check="interaction_event",
                     mentor_moment="intro"),
        MissionStage(stage="predict", title="Predict the result",
                     interaction="predict_output", check="mcq:predict",
                     mentor_moment="correct_1"),
        MissionStage(stage="build", title="Find the duplicate",
                     interaction="tiny_build", check="tests_pass",
                     bank_refs=["b1d9624d-b974-496b-8043-2a4dd86837a2"],
                     mentor_moment="correct_1"),
        MissionStage(stage="break", title="Empty-array hunt",
                     interaction="break_and_debug", check="names_misconception",
                     mentor_moment="wrong_1"),
        MissionStage(stage="debug", title="Guard the edge",
                     interaction="error_hunt", check="fix_verified",
                     mentor_moment="wrong_2"),
        MissionStage(stage="retrieve", title="Min cold",
                     interaction="recall_check", check="tests_pass_no_notes",
                     bank_refs=["0a5a37a2-0c77-4dce-9ece-5353a4d2988d"],
                     mentor_moment="retry_prompt"),
        MissionStage(stage="transfer", title="Pair sum, not min",
                     interaction="transfer_problem",
                     check="tests_pass_out_of_domain",
                     bank_refs=["tcs_coding_016"],
                     mentor_moment="retry_prompt"),
        MissionStage(stage="mastery", title="5-minute proof",
                     interaction="timed_prove",
                     check="tests_pass_under_time",
                     bank_refs=["tcs_coding_001"],
                     mentor_moment="after_mastery", time_limit_seconds=300),
    ],
    mentor_skill="code.arrays",
    company_overlay_id="tcs",
    provenance="pattern-relevant",
    reward=MissionReward(diamonds=60, unlocks="tcs_nqt.strings_basics"),
    consequence=MissionConsequence(
        on_mastery="harder transfer in 2 days",
        on_developing="retrieval drill tomorrow",
        on_repair="repair mission before advancing",
    ),
    frontend_slug="arrays",
    lesson_slug="arrays",
    trust_floor="reviewed",
    status="unverified",
)
