"""Aptitude mission template — quant / logic / verbal under time.

Teaching comes from lesson_slug (backend lesson cards); checks come from
bank_refs (verified bank IDs). Fill those two, keep the skeleton.
"""
from __future__ import annotations

from app.content.mission_definitions import (
    MissionBrief, MissionConsequence, MissionDefinition, MissionReward, MissionStage,
)


def template(topic: str = "<topic>", skill: str = "<canonical_skill>") -> MissionDefinition:
    return MissionDefinition(
        id=f"template.aptitude.{topic}", domain="aptitude", canonical_skill=skill,
        brief=MissionBrief(
            mission_title=f"Master {topic}",
            round_name="Aptitude round — eliminates most candidates",
            threat="Speed kills: 60-90 seconds per question.",
            goal=f"Identify {topic} patterns without falling for traps.",
            reward_diamonds=40,
        ),
        stages=[
            MissionStage(stage="discover", title="See it", interaction="visual_hook",
                         check="read", mentor_moment="intro"),
            MissionStage(stage="manipulate", title="Touch it", interaction="parameter_slider",
                         moments=["change_one_thing"], check="interaction_event", mentor_moment="intro"),
            MissionStage(stage="predict", title="Commit", interaction="multiple_choice_reasoning",
                         check="mcq:predict", mentor_moment="correct_1"),
            MissionStage(stage="build", title="Show working", interaction="tiny_build",
                         check="constructed_calculation", mentor_moment="correct_1"),
            MissionStage(stage="break", title="Spot the trap", interaction="error_hunt",
                         check="names_misconception", mentor_moment="wrong_1"),
            MissionStage(stage="debug", title="Fix + why", interaction="explain_the_bug",
                         check="fix_verified", mentor_moment="wrong_2"),
            MissionStage(stage="retrieve", title="From memory", interaction="recall_check",
                         check="correct_no_notes", mentor_moment="retry_prompt"),
            MissionStage(stage="transfer", title="New skin", interaction="transfer_problem",
                         check="correct_out_of_domain", mentor_moment="retry_prompt"),
            MissionStage(stage="mastery", title="Prove it", interaction="timed_prove",
                         check="score>=threshold_under_time", mentor_moment="after_mastery",
                         time_limit_seconds=90),
        ],
        mentor_skill=skill,
        reward=MissionReward(diamonds=40, unlocks="next_mission"),
        consequence=MissionConsequence(
            on_mastery="harder transfer in 2 days",
            on_developing="retrieval drill tomorrow",
            on_repair="repair mission before advancing",
        ),
    )
