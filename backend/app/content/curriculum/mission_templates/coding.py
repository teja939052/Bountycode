"""Coding mission template — trace, build, debug, prove under time.

Service-based coding is output prediction + easy programs + pseudo-code.
Checks come from bank_refs (verified bank IDs with executable tests).
"""
from __future__ import annotations

from app.content.mission_definitions import (
    MissionBrief, MissionConsequence, MissionDefinition, MissionReward, MissionStage,
)


def template(topic: str = "<topic>", skill: str = "<canonical_skill>") -> MissionDefinition:
    return MissionDefinition(
        id=f"template.coding.{topic}", domain="coding", canonical_skill=skill,
        brief=MissionBrief(
            mission_title=f"Master {topic}",
            round_name="Coding round — 1-2 easy problems, sometimes pseudo-code",
            threat="No output check means no marks.",
            goal=f"Write {topic} that passes hidden tests first try.",
            reward_diamonds=60,
        ),
        stages=[
            MissionStage(stage="discover", title="See execution", interaction="state_trace",
                         check="read", mentor_moment="intro"),
            MissionStage(stage="manipulate", title="Change inputs", interaction="drag_or_manipulate",
                         moments=["change_one_thing"], check="interaction_event", mentor_moment="intro"),
            MissionStage(stage="predict", title="Predict output", interaction="predict_output",
                         check="mcq:predict", mentor_moment="correct_1"),
            MissionStage(stage="build", title="Write it", interaction="tiny_build",
                         check="tests_pass", mentor_moment="correct_1"),
            MissionStage(stage="break", title="Break it", interaction="break_and_debug",
                         check="names_misconception", mentor_moment="wrong_1"),
            MissionStage(stage="debug", title="Fix it", interaction="error_hunt",
                         check="fix_verified", mentor_moment="wrong_2"),
            MissionStage(stage="retrieve", title="From memory", interaction="recall_check",
                         check="correct_no_notes", mentor_moment="retry_prompt"),
            MissionStage(stage="transfer", title="New shape", interaction="transfer_problem",
                         check="tests_pass_out_of_domain", mentor_moment="retry_prompt"),
            MissionStage(stage="mastery", title="Prove it", interaction="timed_prove",
                         check="tests_pass_under_time", mentor_moment="after_mastery",
                         time_limit_seconds=300),
        ],
        mentor_skill=skill,
        reward=MissionReward(diamonds=60, unlocks="next_mission"),
        consequence=MissionConsequence(
            on_mastery="harder transfer in 2 days",
            on_developing="retrieval drill tomorrow",
            on_repair="repair mission before advancing",
        ),
    )
