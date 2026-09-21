#!/usr/bin/env python3
"""Generate complete worlds_data.py with all 12 BountyCode worlds."""

HEADER = '''"""World data for all 12 BountyCode worlds."""

from app.models.world import (
    Boss, BreakStep, Build, Code, Debug, Discover, Level, Manipulate,
    Predict, Retrieval, Story, Success, Town, Transfer, Tutor, World, Reward,
)


def _story(location, npc, line):
    return Story(location=location, npc=npc, line=line)


def _tutor(name="Byte", avatar="\U0001f9ee", discover="", explain=""):
    return Tutor(name=name, avatar=avatar, discover=discover, explain=explain)


def _discover(visual, interaction, prompt, answer, values=None):
    return Discover(visual=visual, interaction=interaction, prompt=prompt, answer=answer, values=values)


def _manipulate(type, template="", answer="", blocks=None, hint=None):
    return Manipulate(type=type, template=template, answer=answer, blocks=blocks, hint=hint)


def _code(prompt, starter="", placeholder="", language="python"):
    return Code(prompt=prompt, starter=starter, placeholder=placeholder, language=language)


def _checks(required, forbidden=None, hint_triggers=None):
    from app.models.world import Checks
    return Checks(required_patterns=required, forbidden=forbidden or [], hint_triggers=hint_triggers or [])


def _success(world_before, world_after, world_reaction, reward_text, byte_line, diamonds):
    return Success(world_before=world_before, world_after=world_after, world_reaction=world_reaction, reward_text=reward_text, byte_line=byte_line, diamonds=diamonds)


def _boss_success(world_before, world_after, world_reaction, reward_text, byte_line, diamonds, unlocks=""):
    return _success(world_before, world_after, world_reaction, reward_text, byte_line, diamonds)


def _reward(diamonds=0, coins=0, badges=None, unlocks_town=None, unlocks_world=None, title=None):
    return Reward(diamonds=diamonds, coins=coins, badges=badges or [], unlocks_town=unlocks_town, unlocks_world=unlocks_world, title=title)


def _level(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, manipulate, code, checks, hints, success, predict=None, build=None, break_step=None, debug=None, retrieval=None, transfer=None, mastery_threshold=None, estimated_minutes=None, unlocks=None):
    return Level(id=id, title=title, kind="level", icon=icon, order=order, concept=concept, mental_model=mental_model, canonical_skill=canonical_skill, maps_to_competency=maps_to, story=story, tutor=tutor, discover=discover, manipulate=manipulate, predict=predict, build=build, break_step=break_step, debug=debug, code=code, checks=checks, hints=hints, retrieval=retrieval, transfer=transfer, mastery_threshold=mastery_threshold, estimated_minutes=estimated_minutes, success=success, unlocks=unlocks)


def _boss(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, manipulate, code, checks, hints, success, reward, predict=None, build=None, break_step=None, debug=None, retrieval=None, transfer=None, mastery_threshold=80, estimated_minutes=None, unlocks=None):
    return Boss(id=id, title=title, kind="boss", icon=icon, order=order, concept=concept, mental_model=mental_model, canonical_skill=canonical_skill, maps_to_competency=maps_to, story=story, tutor=tutor, discover=discover, manipulate=manipulate, predict=predict, build=build, break_step=break_step, debug=debug, code=code, checks=checks, hints=hints, retrieval=retrieval, transfer=transfer, mastery_threshold=mastery_threshold, estimated_minutes=estimated_minutes, success=success, reward=reward, unlocks=unlocks)


def _make_town(id, name, icon, description, order, mental_model, canonical_skills, competencies, levels):
    return Town(id=id, name=name, icon=icon, description=description, order=order, mental_model=mental_model, canonical_skills=canonical_skills, competencies=competencies, levels=levels, boss=levels[-1] if levels and levels[-1].kind == "boss" else None)
'''


def main():
    """Write the header to worlds_data.py."""
    with open("backend/app/data/worlds_data.py", "w", encoding="utf-8") as f:
        f.write(HEADER)


if __name__ == "__main__":
    main()