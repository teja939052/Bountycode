import io

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add helper functions after _reward
helpers = '''

def _predict(prompt, answer, explanation=""):
    return Predict(prompt=prompt, answer=answer, explanation=explanation)


def _break_step(prompt, broken_code, expected_failure=""):
    return BreakStep(prompt=prompt, broken_code=broken_code, expected_failure=expected_failure)


def _debug(prompt, buggy_code, fix_steps=None, answer=""):
    return Debug(prompt=prompt, buggy_code=buggy_code, fix_steps=fix_steps or [], answer=answer)


def _retrieval(prompt, answer, explanation=""):
    return Retrieval(prompt=prompt, answer=answer, explanation=explanation)


def _transfer(prompt, answer, context=""):
    return Transfer(prompt=prompt, answer=answer, context=context)
'''

content = content.replace(
    'def _reward(diamonds=0, coins=0, badges=None, unlocks_town=None, unlocks_world=None, title=None):\n    return Reward(diamonds=diamonds, coins=coins, badges=badges or [], unlocks_town=unlocks_town, unlocks_world=unlocks_world, title=title)',
    'def _reward(diamonds=0, coins=0, badges=None, unlocks_town=None, unlocks_world=None, title=None):\n    return Reward(diamonds=diamonds, coins=coins, badges=badges or [], unlocks_town=unlocks_town, unlocks_world=unlocks_world, title=title)' + helpers
)

# Update _level signature
content = content.replace(
    'def _level(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, manipulate, code, checks, hints, success, predict=None, build=None, break_step=None, debug=None, retrieval=None, transfer=None, mastery_threshold=None, estimated_minutes=None, unlocks=None):',
    'def _level(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, manipulate, code, checks, hints, success, predict=None, build=None, break_step=None, debug=None, retrieval=None, transfer=None, mastery_threshold=None, estimated_minutes=None, unlocks=None, role_relevance=None, company_relevance=None):'
)

content = content.replace(
    '    return Level(id=id, title=title, kind="level", icon=icon, order=order, concept=concept, mental_model=mental_model, canonical_skill=canonical_skill, maps_to_competency=maps_to, story=story, tutor=tutor, discover=discover, manipulate=manipulate, predict=predict, build=build, break_step=break_step, debug=debug, code=code, checks=checks, hints=hints, retrieval=retrieval, transfer=transfer, mastery_threshold=mastery_threshold, estimated_minutes=estimated_minutes, success=success, unlocks=unlocks)',
    '    return Level(id=id, title=title, kind="level", icon=icon, order=order, concept=concept, mental_model=mental_model, canonical_skill=canonical_skill, maps_to_competency=maps_to, role_relevance=role_relevance, company_relevance=company_relevance, story=story, tutor=tutor, discover=discover, manipulate=manipulate, predict=predict, build=build, break_step=break_step, debug=debug, code=code, checks=checks, hints=hints, retrieval=retrieval, transfer=transfer, mastery_threshold=mastery_threshold, estimated_minutes=estimated_minutes, success=success, unlocks=unlocks)'
)

# Update _boss signature
content = content.replace(
    'def _boss(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, manipulate, code, checks, hints, success, reward, predict=None, build=None, break_step=None, debug=None, retrieval=None, transfer=None, mastery_threshold=80, estimated_minutes=None, unlocks=None):',
    'def _boss(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, manipulate, code, checks, hints, success, reward, predict=None, build=None, break_step=None, debug=None, retrieval=None, transfer=None, mastery_threshold=80, estimated_minutes=None, unlocks=None, role_relevance=None, company_relevance=None):'
)

content = content.replace(
    '    return Boss(id=id, title=title, kind="boss", icon=icon, order=order, concept=concept, mental_model=mental_model, canonical_skill=canonical_skill, maps_to_competency=maps_to, story=story, tutor=tutor, discover=discover, manipulate=manipulate, predict=predict, build=build, break_step=break_step, debug=debug, code=code, checks=checks, hints=hints, retrieval=retrieval, transfer=transfer, mastery_threshold=mastery_threshold, estimated_minutes=estimated_minutes, success=success, reward=reward, unlocks=unlocks)',
    '    return Boss(id=id, title=title, kind="boss", icon=icon, order=order, concept=concept, mental_model=mental_model, canonical_skill=canonical_skill, maps_to_competency=maps_to, role_relevance=role_relevance, company_relevance=company_relevance, story=story, tutor=tutor, discover=discover, manipulate=manipulate, predict=predict, build=build, break_step=break_step, debug=debug, code=code, checks=checks, hints=hints, retrieval=retrieval, transfer=transfer, mastery_threshold=mastery_threshold, estimated_minutes=estimated_minutes, success=success, reward=reward, unlocks=unlocks)'
)

with io.open('app/data/worlds_data.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Helpers and signatures updated')
