"""CS-core mission template — OOPs, DBMS/SQL, OS, CN for interviews.

CS interviews score mechanisms, not definitions. The student explains
aloud; checks come from bank_refs (verified bank IDs) + rubrics.
"""
from __future__ import annotations

from app.content.mission_definitions import (
    MissionBrief, MissionConsequence, MissionDefinition, MissionReward, MissionStage,
)


def template(topic: str = "<topic>", skill: str = "<canonical_skill>") -> MissionDefinition:
    return MissionDefinition(
        id=f"template.cs_core.{topic}", domain="cs_core", canonical_skill=skill,
        brief=MissionBrief(
            mission_title=f"Master {topic}",
            round_name="Technical interview — explain, don't recite",
            threat="Definitions crack on the first follow-up.",
            goal=f"Explain {topic} by mechanism, then survive follow-ups.",
            reward_diamonds=60,
        ),
        stages=[
            MissionStage(stage="discover", title="See the mechanism", interaction="interactive_diagram",
                         check="read", mentor_moment="intro"),
            MissionStage(stage="manipulate", title="Change conditions", interaction="before_after",
                         moments=["change_one_thing"], check="interaction_event", mentor_moment="intro"),
            MissionStage(stage="predict", title="Commit", interaction="multiple_choice_reasoning",
                         check="mcq:predict", mentor_moment="correct_1"),
            MissionStage(stage="build", title="Explain aloud", interaction="explain_aloud",
                         check="rubric_pass", mentor_moment="correct_1"),
            MissionStage(stage="break", title="Break the definition", interaction="error_hunt",
                         check="names_misconception", mentor_moment="wrong_1"),
            MissionStage(stage="debug", title="Repair the mechanism", interaction="explain_the_bug",
                         check="fix_verified", mentor_moment="wrong_2"),
            MissionStage(stage="retrieve", title="From memory", interaction="recall_check",
                         check="correct_no_notes", mentor_moment="retry_prompt"),
            MissionStage(stage="transfer", title="New scenario", interaction="transfer_problem",
                         check="rubric_pass_out_of_domain", mentor_moment="retry_prompt"),
            MissionStage(stage="mastery", title="Rapid-fire proof", interaction="timed_prove",
                         check="rubric_pass_under_time", mentor_moment="after_mastery",
                         time_limit_seconds=120),
        ],
        mentor_skill=skill,
        reward=MissionReward(diamonds=60, unlocks="next_mission"),
        consequence=MissionConsequence(
            on_mastery="harder transfer in 2 days",
            on_developing="retrieval drill tomorrow",
            on_repair="repair mission before advancing",
        ),
    )
