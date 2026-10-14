"""Exemplar mission: successive percentage change (TCS NQT aptitude).

Status: UNVERIFIED mission structure (new, awaiting human review).
All bank_refs are servable TODAY (automated_checked + provenance + companies).
Provenance is pattern-relevant: the mission teaches the TCS NQT pattern;
it does not claim verified placement history.
"""
from __future__ import annotations

from app.content.mission_definitions import (
    MissionBrief, MissionConsequence, MissionDefinition, MissionReward, MissionStage,
)

MISSION = MissionDefinition(
    id="tcs_nqt.percentages_change",
    track_id="tcs_nqt",
    domain="aptitude",
    canonical_skill="quant.percentages",
    brief=MissionBrief(
        mission_title="The Eliminator: Percentage Change",
        round_name="TCS NQT Round 1 — aptitude",
        threat="Round 1 ends most runs. Successive-change traps decide it.",
        goal="Price up, then down: know exactly where it lands.",
        reward_diamonds=40,
    ),
    stages=[
        MissionStage(stage="discover", title="See the change",
                     interaction="visual_hook", check="read",
                     mentor_moment="intro"),
        MissionStage(stage="manipulate", title="Move the slider",
                     interaction="parameter_slider", moments=["change_one_thing"],
                     check="interaction_event",
                     mentor_moment="intro"),
        MissionStage(stage="predict", title="Commit before computing",
                     interaction="multiple_choice_reasoning", check="mcq:predict",
                     bank_refs=["tcs_aptitude_000"],
                     mentor_moment="correct_1"),
        MissionStage(stage="build", title="Show the working",
                     interaction="tiny_build", check="constructed_calculation",
                     mentor_moment="correct_1"),
        MissionStage(stage="break", title="The 'back to start' trap",
                     interaction="error_hunt", check="names_misconception",
                     mentor_moment="wrong_1"),
        MissionStage(stage="debug", title="Fix the base",
                     interaction="explain_the_bug", check="fix_verified",
                     mentor_moment="wrong_2"),
        MissionStage(stage="retrieve", title="Reverse it cold",
                     interaction="recall_check", check="correct_no_notes",
                     bank_refs=["apt-v2-00003"],
                     mentor_moment="retry_prompt"),
        MissionStage(stage="transfer", title="Mixture skin",
                     interaction="transfer_problem", check="correct_out_of_domain",
                     bank_refs=["apt-v2-00401"],
                     mentor_moment="retry_prompt"),
        MissionStage(stage="mastery", title="90-second proof",
                     interaction="timed_prove",
                     check="score>=threshold_under_time",
                     bank_refs=["apt-v2-00402"],
                     mentor_moment="after_mastery", time_limit_seconds=90),
    ],
    mentor_skill="quant.percentages",
    company_overlay_id="tcs",
    provenance="pattern-relevant",
    reward=MissionReward(diamonds=40, unlocks="tcs_nqt.ratio_proportion"),
    consequence=MissionConsequence(
        on_mastery="harder transfer in 2 days",
        on_developing="retrieval drill tomorrow",
        on_repair="repair mission before advancing",
    ),
    frontend_slug="percentages",
    lesson_slug="percentages",
    trust_floor="reviewed",
    status="unverified",
)
