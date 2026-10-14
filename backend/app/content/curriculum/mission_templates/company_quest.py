"""Company-quest template — one company track, one funnel, one mock.

Same engine as every mission; the company overlay supplies pattern
weights, filters, and the mock blueprint. Provenance stays honest:
pattern-relevant unless bank refs carry verified company tags.
"""
from __future__ import annotations

from app.content.mission_definitions import (
    MissionBrief, MissionConsequence, MissionDefinition, MissionReward, MissionStage,
)


def template(company: str = "<company>", topic: str = "<topic>",
             skill: str = "<canonical_skill>") -> MissionDefinition:
    return MissionDefinition(
        id=f"template.company_quest.{company}.{topic}", domain="company_quest",
        canonical_skill=skill, track_id=f"{company}_track",
        brief=MissionBrief(
            mission_title=f"Clear {topic} for {company}",
            round_name=f"{company} pattern — same engine, their weightage",
            threat="The interface and the clock cause failures, not just knowledge.",
            goal=f"Solve {topic} the way {company} asks it.",
            reward_diamonds=60,
        ),
        stages=[
            MissionStage(stage="discover", title="The pattern", interaction="before_after",
                         check="read", mentor_moment="intro"),
            MissionStage(stage="manipulate", title="Feel the weightage", interaction="parameter_slider",
                         moments=["change_one_thing"], check="interaction_event", mentor_moment="intro"),
            MissionStage(stage="predict", title="Commit", interaction="multiple_choice_reasoning",
                         check="mcq:predict", mentor_moment="correct_1"),
            MissionStage(stage="build", title="Solve their way", interaction="tiny_build",
                         check="tests_or_rubric_pass", mentor_moment="correct_1"),
            MissionStage(stage="break", title="Their favorite trap", interaction="error_hunt",
                         check="names_misconception", mentor_moment="wrong_1"),
            MissionStage(stage="debug", title="Fix + why", interaction="explain_the_bug",
                         check="fix_verified", mentor_moment="wrong_2"),
            MissionStage(stage="retrieve", title="From memory", interaction="recall_check",
                         check="correct_no_notes", mentor_moment="retry_prompt"),
            MissionStage(stage="transfer", title="Twisted variant", interaction="transfer_problem",
                         check="correct_out_of_domain", mentor_moment="retry_prompt"),
            MissionStage(stage="mastery", title="Mock section", interaction="timed_prove",
                         check="mock_section_pass", mentor_moment="after_mastery",
                         time_limit_seconds=600),
        ],
        mentor_skill=skill,
        company_overlay_id=company,
        reward=MissionReward(diamonds=60, unlocks="next_mission"),
        consequence=MissionConsequence(
            on_mastery="full mock unlocked",
            on_developing="pattern drill tomorrow",
            on_repair="repair mission before advancing",
        ),
    )
