"""World data for all 12 BountyCode worlds."""

from app.models.world import (
    Boss, BreakStep, Build, Checks, Code, Debug, Discover, Level, Manipulate,
    Predict, Retrieval, Story, Success, Town, Transfer, Tutor, World, Reward,
)


def _story(location, npc, line):
    return Story(location=location, npc=npc, line=line)


def _tutor(name="Byte", avatar="🧮", discover="", explain=""):
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


def _boss_success(world_before, world_after, world_reaction, reward_text, byte_line, diamonds):
    return _success(world_before, world_after, world_reaction, reward_text, byte_line, diamonds)


def _reward(diamonds=0, coins=0, badges=None, unlocks_town=None, unlocks_world=None, title=None):
    return Reward(diamonds=diamonds, coins=coins, badges=badges or [], unlocks_town=unlocks_town, unlocks_world=unlocks_world, title=title)

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


def _build(prompt, starter="", placeholder="", language="python"):
    return Build(prompt=prompt, starter=starter, placeholder=placeholder, language=language)


def _understand(text):
    return text



# Service-company relevance defaults: every level serves the mass-recruiter
# pipeline (TCS/Infosys/Wipro/Accenture/Cognizant/Capgemini/HCL/TechM/IBM).
# Targeted users therefore company-match; role strings cover both the
# user-facing ("sde") and world-facing ("developer") vocabularies so the
# worlds.py relevance sort is real instead of cosmetic.
_SERVICE_COMPANIES = (
    "tcs tcs_nqt ninja digital prime infosys infytq wipro wipro_nlth "
    "accenture cognizant cognizant_genc genc capgemini hcl techm tech_mahindra ibm"
)
_ROLE_ENGINEERING = "sde developer"


def _level(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, understand, manipulate, *args, mastery_threshold=None, estimated_minutes=None, unlocks=None, role_relevance=_ROLE_ENGINEERING, company_relevance=_SERVICE_COMPANIES, **kwargs):
    predict = kwargs.get("predict")
    build = kwargs.get("build")
    break_step = kwargs.get("break_step")
    debug = kwargs.get("debug")
    retrieval = kwargs.get("retrieval")
    transfer = kwargs.get("transfer")
    checks = kwargs.get("checks")
    hints = kwargs.get("hints")
    success = kwargs.get("success")
    for arg in args:
        if isinstance(arg, Predict) and predict is None:
            predict = arg
        elif isinstance(arg, Build) and build is None:
            build = arg
        elif isinstance(arg, BreakStep) and break_step is None:
            break_step = arg
        elif isinstance(arg, Debug) and debug is None:
            debug = arg
        elif isinstance(arg, Retrieval) and retrieval is None:
            retrieval = arg
        elif isinstance(arg, Transfer) and transfer is None:
            transfer = arg
        elif isinstance(arg, Checks) and checks is None:
            checks = arg
        elif isinstance(arg, list) and hints is None:
            hints = arg
        elif isinstance(arg, Success) and success is None:
            success = arg
        elif isinstance(arg, Code):
            kwargs["code"] = arg
    level_kwargs = {
        "id": id, "title": title, "kind": "level", "icon": icon, "order": order,
        "concept": concept, "mental_model": mental_model, "canonical_skill": canonical_skill,
        "maps_to_competency": maps_to, "role_relevance": role_relevance,
        "company_relevance": company_relevance, "story": story, "tutor": tutor,
        "discover": discover, "understand": understand, "manipulate": manipulate,
        "predict": predict, "build": build, "break_step": break_step, "debug": debug,
        "retrieval": retrieval, "transfer": transfer, "checks": checks, "hints": hints,
        "success": success, "mastery_threshold": mastery_threshold,
        "estimated_minutes": estimated_minutes, "unlocks": unlocks,
    }
    if "code" in kwargs:
        level_kwargs["code"] = kwargs["code"]
    return Level(**level_kwargs)


def _boss(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, understand, manipulate, *args, mastery_threshold=80, estimated_minutes=None, unlocks=None, role_relevance=_ROLE_ENGINEERING, company_relevance=_SERVICE_COMPANIES, **kwargs):
    predict = kwargs.get("predict")
    build = kwargs.get("build")
    break_step = kwargs.get("break_step")
    debug = kwargs.get("debug")
    retrieval = kwargs.get("retrieval")
    transfer = kwargs.get("transfer")
    checks = kwargs.get("checks")
    hints = kwargs.get("hints")
    success = kwargs.get("success")
    for arg in args:
        if isinstance(arg, Predict) and predict is None:
            predict = arg
        elif isinstance(arg, Build) and build is None:
            build = arg
        elif isinstance(arg, BreakStep) and break_step is None:
            break_step = arg
        elif isinstance(arg, Debug) and debug is None:
            debug = arg
        elif isinstance(arg, Retrieval) and retrieval is None:
            retrieval = arg
        elif isinstance(arg, Transfer) and transfer is None:
            transfer = arg
        elif isinstance(arg, Checks) and checks is None:
            checks = arg
        elif isinstance(arg, list) and hints is None:
            hints = arg
        elif isinstance(arg, Success) and success is None:
            success = arg
        elif isinstance(arg, Code):
            kwargs["code"] = arg
        elif isinstance(arg, Reward):
            kwargs["reward"] = arg
    level_kwargs = {
        "id": id, "title": title, "kind": "boss", "icon": icon, "order": order,
        "concept": concept, "mental_model": mental_model, "canonical_skill": canonical_skill,
        "maps_to_competency": maps_to, "role_relevance": role_relevance,
        "company_relevance": company_relevance, "story": story, "tutor": tutor,
        "discover": discover, "understand": understand, "manipulate": manipulate,
        "predict": predict, "build": build, "break_step": break_step, "debug": debug,
        "retrieval": retrieval, "transfer": transfer, "checks": checks, "hints": hints,
        "success": success, "mastery_threshold": mastery_threshold,
        "estimated_minutes": estimated_minutes, "unlocks": unlocks,
    }
    if "code" in kwargs:
        level_kwargs["code"] = kwargs["code"]
    if "reward" in kwargs:
        level_kwargs["reward"] = kwargs["reward"]
    return Boss(**level_kwargs)


def _make_town(id, name, icon, description, order, mental_model, canonical_skills, competencies, levels):
    return Town(id=id, name=name, icon=icon, description=description, order=order, mental_model=mental_model, canonical_skills=canonical_skills, competencies=competencies, levels=levels, boss=levels[-1] if levels and levels[-1].kind == "boss" else None)


# ═══════════════════════════════════════════════════════════════
# WORLD 1: Beginner Valley (foundations)
# ═══════════════════════════════════════════════════════════════
WORLD_FOUNDATIONS = World(
    id="foundations", name="Beginner Valley", subtitle="How Programs Think",
    description="Your first steps as a Code Wanderer. Learn how programs remember things.",
    icon="🌄", order=1, theme="foundations", recommended_roles=["developer", "data-analyst", "ai-engineer"], prerequisites=[],
    towns=[
        _make_town("things", "Things", "🏘️", "The village has lost its labels. Help them remember.", 1, "How Programs Think", ["coding.variables"], ["variables", "naming", "assignment", "expressions"], [
            _level("level-1","The Box","📦",1,"variables","Remembering","coding.variables","coding.variables",
                _story("Village Square — Supply Hut","Mira the Keeper","Our supply boxes lost their labels! This one holds 5 apples, but nobody remembers. Can you give it a name the program will remember?"),
                _tutor("Byte","🧭","Programs remember values by giving them a name. Like labeling a box.","apples is a variable — a named box that holds a value. The = does not mean equals in math; it means store this value here."),
                _discover("A wooden crate labeled ??? with 5 apples inside. Tap it to label.","select-value","What should the program remember here?","apples = 5",[5,"apple",True]),
                _understand("A variable is a named box in the computer's memory. The = sign means 'put this value in this box'. It is not math equality — it is assignment, a one-way arrow."),
                _manipulate("memory-box","apples = ?","apples = 5",hint="Give the box the name apples and put 5 inside."),
                _predict("What will this program print?\napples = 5\nprint(apples)\napples = 10\nprint(apples)",
                    "5\n10",
                    "print() shows what is in the box RIGHT NOW. The box changes after the second line."),
                _build("Create a variable called apples with the value 5.","# Give the box a name\n","apples = 5"),
                _break_step("Why does this program print 5 twice instead of 5 then 10?\napples = 5\nprint(apples)\napples = 10\nprint(apples)",
                    "apples = 5\nprint(apples)\napples = 10\nprint(apples)",
                    "The second print shows 10, not 5. The student predicted both print 5."),
                _debug("The program prints 5 twice. Fix it so the second print shows 10.",
                    "apples = 5\nprint(apples)\napples = 10\nprint(apples)",
                    ["Check that the second assignment happens before the second print."],
                    "apples = 5\nprint(apples)\napples = 10\nprint(apples)"),
                _retrieval("What does apples = 10 mean in programming?",
                    "Put 10 in the box named apples",
                    "= is a one-way arrow, not equality."),
                _transfer("A bank account starts with $100. Write code that deposits $50 and prints the new balance.",
                    "balance = 100\nbalance = 150\nprint(balance)",
                    "Same mental model: named box, assignment, print."),
                _checks([r"^\s*apples\s*=\s*5\s*(#.*)?$"]),
                ["What information does the robot need to remember here?","Programs can give a name to information so they can use it later — like labeling a box.","Try giving the number 5 the name `apples`.","Reveal: apples = 5 — the box needs this label to be remembered."],
                _success("📦 ??? · 📋 Empty ledger","📦 5 apples · 📋 ✓ Inventory recorded","The crate now glows: 🍎 Apples: 5 — the villagers cheer!","Variable Mastery — you can make programs remember things.","Your program remembered something. That is what variables do.",20),
                mastery_threshold=80, estimated_minutes=10),
            _level("level-2","The Label","🏷️",2,"variables","Naming","coding.variables","coding.variables",
                _story("Village Store","Mira the Keeper","One box is not enough. We also have 3 loaves of bread. Remember both — then show me what is inside!"),
                _tutor("Byte","🧭","Each piece of information gets its own box. And print() lets you look inside.","Two variables, two boxes. print() is how you ask: what is inside this box right now?"),
                _discover("Two crates: 🍎 5 and 🍞 3. Tap each to label.","pair-labels","Label them: apples and bread","apples = 5; bread = 3"),
                _understand("Multiple variables mean multiple named boxes. Each box has one name and one current value. print() is how you peek inside any box."),
                _manipulate("memory-boxes","apples = 5 / bread = ?","apples = 5\nbread = 3\nprint(apples)",blocks=["apples","=","5","bread","=","3","print","(",")"]),
                _predict("What does this print?\napples = 5\nbread = 3\nprint(bread)",
                    "3",
                    "print(bread) shows the value in the bread box."),
                _build("Create apples = 5 and bread = 3, then print the apples.","# Two boxes, then look inside\n","apples = 5\nbread = 3\nprint(apples)"),
                _break_step("Why does this print 3 instead of 5?\napples = 5\nbread = 3\nprint(bread)",
                    "apples = 5\nbread = 3\nprint(bread)",
                    "The student predicted print shows apples always."),
                _debug("The program prints the wrong variable. Fix it to print apples.",
                    "apples = 5\nbread = 3\nprint(bread)",
                    ["Change print(bread) to print(apples)."],
                    "apples = 5\nbread = 3\nprint(apples)"),
                _retrieval("How do you look inside the box named bread?",
                    "print(bread)",
                    "Use print() with the variable name."),
                _transfer("Track temperature: create temp_celsius = 25, then print it.",
                    "temp_celsius = 25\nprint(temp_celsius)",
                    "Same pattern: name, assign, print."),
                _checks([r"apples\s*=\s*5",r"bread\s*=\s*3",r"print\s*\(\s*apples\s*\)"]),
                ["What second fact does the shop need besides apples? How would you look inside a box?","Each fact gets its own labeled box. print() asks what is inside this one?","Try creating a second variable for bread, then print(apples).","Reveal:\napples = 5\nbread = 3\nprint(apples)"],
                _success("🧺 🍎 ? · 🍞 ? · 📋 1/2 recorded","🧺 🍎 5 · 🍞 3 · 📋 ✓ Both recorded","The store inventory board updates: Apples 5 · Bread 3 — it works!","State Sense — programs hold many facts at once.","Two boxes, two facts. That is state.",25),
                mastery_threshold=80, estimated_minutes=10),
            _level("level-3","The Change","🔄",3,"reassignment","Changing","coding.variables","coding.variables",
                _story("Village Store — Delivery Day","Mira the Keeper","A delivery arrived! The apple crate should now hold the new stock. Can you update what the program remembers?"),
                _tutor("Byte","🧭","Variables can change. Assigning again replaces what is inside the box.","apples = 10 does not mean apples equals 10 — it means now put 10 in the box called apples. The old value is gone."),
                _discover("Crate 🍎 changes from 5 → 10 when you update.","slider","The stock changed from 5 to 10. How does the box update?","apples = 5; apples = 10"),
                _understand("Assignment is not equality. apples = 10 means 'replace the value in the apples box with 10'. The old value 5 is gone forever."),
                _manipulate("slider-box","apples = 5\napples = ?","apples = 10"),
                _predict("What does this print?\napples = 5\napples = 10\nprint(apples)",
                    "10",
                    "The last assignment wins. The box holds 10."),
                _build("First set apples = 5, then update it to 10, then print it.","# Start at 5, then update\n","apples = 5\napples = 10\nprint(apples)"),
                _break_step("Why does this print 5 instead of 10?\napples = 5\napples = 10\nprint(apples)",
                    "apples = 5\napples = 10\nprint(apples)",
                    "The student predicted the first value sticks."),
                _debug("The program prints 5 but should print 10. Fix the order.",
                    "print(apples)\napples = 5\napples = 10",
                    ["Move the first print after apples = 5.", "Move the second print after apples = 10."],
                    "apples = 5\nprint(apples)\napples = 10\nprint(apples)"),
                _retrieval("What happens to the old value when you assign a new one?",
                    "It is replaced / gone",
                    "Assignment overwrites the previous value."),
                _transfer("Update a bank account: start with balance = 100, then deposit 50, then print balance.",
                    "balance = 100\nbalance = 150\nprint(balance)",
                    "Same pattern: assign, reassign, print."),
                _checks([r"apples\s*=\s*5",r"apples\s*=\s*10",r"print\s*\(\s*apples\s*\)"]),
                ["What changed in the stockroom? What should the box hold now?","A variable is a label — you can put a new value in the same box.","Keep the first line apples = 5, then put 10 in the same box on the next line.","Reveal:\napples = 5\napples = 10\nprint(apples)"],
                _success("📦 5 apples · 🧾 Ledger says 5","📦 10 apples · 🧾 Ledger says 10","The crate count ticks 5 → 10. The ledger is correct!","Mutation — you can change what the program remembers.","You did not create a new box — you changed the one you had.",25),
                mastery_threshold=80, estimated_minutes=10),
            _level("level-4","The Many","🧺",4,"multiple-variables","Organizing","coding.variables","coding.variables",
                _story("Village Market","Old Tomas","I track apples, bread, AND coins. Three facts, three boxes. Can you set them all up?"),
                _tutor("Byte","🧭","State is just everything the program remembers right now. More variables = richer state.","Three variables in a row — the program now remembers three things at once."),
                _discover("Three stalls: 🍎 🍞 🪙 — each needs a label.","match","Match: apples→5, bread→3, coins→20","apples = 5; bread = 3; coins = 20"),
                _understand("State is the complete set of variables and their current values. More variables = richer state = more facts the program can use."),
                _manipulate("three-boxes",blocks=["apples","bread","coins","=","5","3","20"],answer="apples = 5\nbread = 3\ncoins = 20"),
                _predict("What does this print?\napples = 5\nbread = 3\ncoins = 20\nprint(coins)",
                    "20",
                    "print(coins) shows the value in the coins box."),
                _build("Create three variables: apples = 5, bread = 3, coins = 20.","# Three facts\n","apples = 5\nbread = 3\ncoins = 20"),
                _break_step("Why does this fail?\napples = 5\nbread = 3\ncoins = 20\nprint(coin)",
                    "apples = 5\nbread = 3\ncoins = 20\nprint(coin)",
                    "NameError: 'coin' is not defined. The student forgot the exact name."),
                _debug("Fix the NameError: the program cannot find 'coin'.",
                    "apples = 5\nbread = 3\ncoins = 20\nprint(coin)",
                    ["Check the exact variable name. It is 'coins', not 'coin'."],
                    "apples = 5\nbread = 3\ncoins = 20\nprint(coins)"),
                _retrieval("What is 'state' in a program?",
                    "all variables and their current values",
                    "State = everything the program remembers right now."),
                _transfer("Track three students' scores: alice = 85, bob = 92, charlie = 78. Print charlie's score.",
                    "alice = 85\nbob = 92\ncharlie = 78\nprint(charlie)",
                    "Same pattern: three named boxes, print one."),
                _checks([r"apples\s*=\s*5",r"bread\s*=\s*3",r"coins\s*=\s*20"]),
                ["How many different facts does Tomas need to track?","State = everything the program remembers right now. Each fact needs its own name.","Try three labeled boxes: one for apples, one for bread, one for coins.","Reveal:\napples = 5\nbread = 3\ncoins = 20"],
                _success("🏪 3 stalls · 📋 Empty","🏪 🍎 5 · 🍞 3 · 🪙 20 · 📋 ✓ All recorded","Three stalls light up. The market ledger is complete!","State Keeper — you hold a whole world in variables.","That is state: everything remembered, organized.",25),
                mastery_threshold=80, estimated_minutes=10),
            _level("level-5","The Echo","📣",5,"expressions","Using","coding.variables","coding.variables",
                _story("Village Square — Announcement","Mira the Keeper","The elders want the total items! Apples plus bread — make the program figure it out and announce it."),
                _tutor("Byte","🧭","Variables are not just storage — you can compute with them. apples + bread is an expression.","total = apples + bread stores the result of the computation. Then print(total) shows it."),
                _discover("🍎 5 + 🍞 3 = ? — drag + to combine.","expression","Compute: total = apples + bread","total = apples + bread"),
                _understand("An expression is a combination of values and operators that computes a new value. apples + bread reads the current values, adds them, and produces a new value."),
                _manipulate("expression-box","total = apples + bread","total = apples + bread"),
                _predict("What does this print?\napples = 5\nbread = 3\ntotal = apples + bread\nprint(total)",
                    "8",
                    "total gets the result of apples + bread = 5 + 3 = 8."),
                _build("Set apples = 5, bread = 3, compute total = apples + bread, then print(total).","# Compute the total\n","apples = 5\nbread = 3\ntotal = apples + bread\nprint(total)"),
                _break_step("Why does this print 53 instead of 8?\napples = 5\nbread = 3\ntotal = apples + bread\nprint(total)",
                    "apples = '5'\nbread = '3'\ntotal = apples + bread\nprint(total)",
                    "String concatenation: '5' + '3' = '53'."),
                _debug("The program prints 53 instead of 8. Fix it.",
                    "apples = '5'\nbread = '3'\ntotal = apples + bread\nprint(total)",
                    ["Convert strings to integers using int().", "Use apples = int(apples) before adding."],
                    "apples = 5\nbread = 3\ntotal = apples + bread\nprint(total)"),
                _retrieval("What is an expression?",
                    "a combination of values and operators that computes a new value",
                    "e.g., apples + bread, 5 * 3, 'hello' + ' world'"),
                _transfer("Calculate a 10% tip on a $50 bill. Write code that computes tip = bill * 0.10 and prints it.",
                    "bill = 50\ntip = bill * 0.10\nprint(tip)",
                    "Same pattern: read values, compute, store in variable, print."),
                _checks([r"apples\s*=\s*5",r"bread\s*=\s*3",r"total\s*=\s*apples\s*\+\s*bread",r"print\s*\(\s*total\s*\)"]),
                ["How would the crier announce the total without counting by hand?","You can compute with names, not just numbers — try combining the two boxes.","Try making a new box that holds the result of apples + bread, then announce it.","Reveal:\napples = 5\nbread = 3\ntotal = apples + bread\nprint(total)"],
                _success("📢 Elders waiting · 🧮 No total yet","📢 Announced: 8 items! · 🧮 total = 8","The town crier announces: 8 items in total! — you computed the answer.","Expression Craft — you make programs calculate.","You used remembered facts to make something new.",30),
                mastery_threshold=80, estimated_minutes=10),
            _boss("boss-1","The Broken Inventory","🐉",6,"boss-variables-state","Transfer","coding.variables","coding.variables",
                _story("Supply Hut — Emergency","Mira the Keeper","The inventory system has stopped remembering its stock. The stockroom has apples, bread and coins — 12, 4 and 30 — but the program remembers nothing. The elders need the total items (apples + bread) announced. Repair it!"),
                _tutor("Byte","🧭","Combine everything: remember, update, compute, announce.","This is transfer: a new situation, same ideas. If you can do this, you truly understand Remembering → Naming → Using."),
                _discover("Scrambled ledger: ??? ??? ??? — rebuild from stockroom count.","boss-fix","Stockroom: 12 apples, 4 bread, 30 coins. Total = apples + bread. Repair the ledger.","apples = 12; bread = 4; coins = 30; total = apples + bread; print(total)"),
                _understand("Transfer means applying a mental model to a new situation. The stockroom is just variables. The total is just an expression. You already know how — you just need to map it."),
                _manipulate("boss-ledger","Remember 3 stocks + announce total","apples = 12; bread = 4; coins = 30; total = apples + bread; print(total)"),
                _predict("What should the final print show?",
                    "16",
                    "apples + bread = 12 + 4 = 16."),
                _build("Repair the inventory: make the program remember the stockroom (12 apples, 4 bread, 30 coins) and announce the total items (apples + bread).","# Repair the scrambled ledger\n# Stockroom: 12 apples, 4 bread, 30 coins\n","apples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)"),
                _break_step("Why does this print 30 instead of 16?\napples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)",
                    "total = coins\nprint(total)",
                    "The student assigned total = coins instead of total = apples + bread."),
                _debug("The program prints the wrong total. Fix the total calculation.",
                    "apples = 12\nbread = 4\ncoins = 30\ntotal = coins\nprint(total)",
                    ["Change total = coins to total = apples + bread."],
                    "apples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)"),
                _retrieval("What does total = apples + bread do?",
                    "computes the sum and stores it in total",
                    "Reads current values, adds them, stores result."),
                _transfer("A library has 120 fiction and 80 non-fiction books. Write code that prints the total books.",
                    "fiction = 120\nnon_fiction = 80\ntotal = fiction + non_fiction\nprint(total)",
                    "Same mental model: named boxes, assignment, expression, print."),
                _checks([r"apples\s*=\s*12",r"bread\s*=\s*4",r"coins\s*=\s*30",r"total\s*=\s*apples\s*\+\s*bread",r"print\s*\(\s*total\s*\)"]),
                ["What facts does the stockroom need the program to hold? What does the elder want announced?","You learned Remembering, Naming, Organizing, Using — which ones does this emergency need?","Try three remembered facts for the stock, then compute the total and announce it.","Reveal:\napples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)"],
                _success("🏚️ Ledger broken · 📦 ??? · 🔇 Silent","🏚️ → 🏘️ Restored · 📦 12/4/30 · 📢 16 announced · 🌿 Path opens","The hut restores! Ledgers glow, crates align. The village is saved — the path to the next town opens. 🌿","🏆 Village Restored — Remembering → Using MASTERED. Next: Kinds of Things!","You did not copy — you transferred. That is mastery.",50),
                _reward(diamonds=50,coins=25,badges=["variables-master"],unlocks_town="town-2-types"),
                mastery_threshold=80, estimated_minutes=15),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 2: Searchlands (search)
# ═══════════════════════════════════════════════════════════════
WORLD_SEARCHLANDS = World(
    id="searchlands", name="Searchlands", subtitle="Finding Things Fast",
    description="How does a program find what it needs? From flipping through pages to dividing and conquering — learn search.",
    icon="🔍", order=2, theme="search", recommended_roles=["developer", "data-analyst"], prerequisites=["foundations"],
    towns=[
        _make_town("linear", "Linear Search Lane", "🚶", "Walk the line. Check every item one by one.", 1, "Sequential Thinking", ["searching.linear"], ["linear-search", "iteration", "comparison"], [
            _level("s-1","The Checklist","📋",1,"linear search","Sequential","searching.linear","searching.linear",
                _story("Searchlands Gate","Guard Hal","Every visitor must be checked. The line is long — can you find the one with the golden ticket?"),
                _tutor("Byte","🧭","To find something in a list, start at the beginning and check each one. That is linear search.","It is like checking every seat in a row until you find your friend. Simple, but it always works."),
                _discover("A line of 7 cards face-down. One has a golden star. Flip them one by one.","flip-card","Which position has the golden star?","position = 4"),
                _understand("It is like checking every seat in a row until you find your friend. Simple, but it always works."),
                _manipulate("check-list","Check position ?","Check each position from 1 to 7 until you find the star.",hint="Start at position 1 and go up."),
                _code("Write code to find the golden star in the list.","cards = [0,0,0,1,0,0,0]\n","target = 1\nfor i in range(len(cards)):\n    if cards[i] == target:\n        print(i)"),
                _checks([r"for\s",r"range\s*\(",r"if\s*cards"]),
                ["Where do you start looking?","You check each one in order. No skipping!","Try a loop that goes from the first to the last."],
                _success("🚪 Gate closed · 🔍 No one checked","🚪 Gate open · ✅ Ticket found","The guard smiles — you found the golden ticket!","Linear Search — you check every item until you find it.","Start at the beginning. That is how search works.",20)),
            _level("s-2","The Counter","🔢",2,"counting","Measuring","searching.linear","searching.linear",
                _story("Searchlands Market","Merchant Mia","How many customers bought apples today? Count them all — one by one."),
                _tutor("Byte","🧭","A counter adds up how many times something happens. It is like tally marks.","Every time you find what you are looking for, you add 1 to your counter."),
                _discover("A receipt with 8 items. Count how many are apples.","tally","How many apples on this receipt?","count = 3"),
                _understand("Every time you find what you are looking for, you add 1 to your counter."),
                _manipulate("tally-counter","count = 0\nfor item in items:\n    if item == apple: count += 1","count = 3"),
                _code("Count how many apples appear in the list.","items = ['apple','banana','apple','orange','apple']\n","count = 0\nfor item in items:\n    if item == apple:\n        count += 1\nprint(count)"),
                _checks([r"count\s*=\s*0",r"for\s",r"if\s*item\s*=="]),
                ["What do you start the counter at?","Every time you find an apple, add 1.","Try initializing count = 0 first."],
                _success("📝 Empty tally · 📊 0 counted","📝 Tally full · 📊 3 apples","The merchant's ledger is updated!","Counting — tallying how many match.","Every match adds one to the count.",20)),
            _level("s-3","The Worst Case","😰",3,"complexity","Understanding","searching.linear","searching.linear",
                _story("Searchlands Library","Librarian Leo","What if the book you want is the very last one? Or not here at all?"),
                _tutor("Byte","🧭","Linear search takes time proportional to the list size. That is O(n).","If the list has 1000 items, you might check all 1000. That is the worst case."),
                _discover("A shelf of 100 books. The target is book #100.","worst-case","How many checks in the worst case?","100"),
                _understand("If the list has 1000 items, you might check all 1000. That is the worst case."),
                _manipulate("complexity-box","Worst case for n items = ?","n"),
                _code("Explain: what is the worst case for linear search on n items?","# Write your explanation\n","# Worst case: check all n items\n# Best case: find at index 0\n# So worst case = n checks"),
                _checks([r"n\s*items",r"all\s*n",r"n\s*checks"]),
                ["What if the item is at the very end?","What if it is not in the list at all?","Both cases require checking every single item."],
                _success("📚 Shelf empty · ⏱️ Unknown","📚 Shelf searched · ⏱️ n checks","The library log records: worst case = n.","Complexity — understanding how long search takes.","Time grows with the list. That is O(n).",25)),
            _boss("s-boss","The Lost Scroll","📜",4,"search-master","Applying","searching.linear","searching.linear",
                _story("Searchlands Archive","Archivist Ana","A ancient scroll is hidden in a vault of 500 scrolls. Find it before the temple collapses!"),
                _tutor("Byte","🧭","Linear search is your first tool. Check every scroll, but be smart about it.","Even a slow search beats no search. But can you do better?"),
                _discover("500 scrolls in a vault. One has the ancient symbol. Find it.","vault-search","Find the scroll with the ancient symbol.","index = 247"),
                _understand("Even a slow search beats no search. But can you do better?"),
                _manipulate("scroll-find","Search scrolls for the ancient symbol","found at index"),
                _code("Search through the scrolls for the ancient symbol.","scrolls = [0]*500\nscrolls[247] = 1\n","target = 1\nfor i in range(len(scrolls)):\n    if scrolls[i] == target:\n        print(f'Found at {i}')\n        break"),
                _checks([r"for\s",r"range\s*\(",r"break"]),
                ["Start from the first scroll.","You can stop as soon as you find it — no need to check the rest.","Use break to stop early."],
                _success("🏛️ Vault sealed · 📜 Missing","🏛️ Vault open · 📜 Found","The ancient scroll is recovered! The temple is saved.","Search Mastery — you can find anything by looking.","Every search starts with a line.",40),
                _reward(diamonds=40,coins=20,badges=["search-novice"],unlocks_town="town-2-binary")),
        ]),
        _make_town("binary", "Binary Search Borough", "🏘️", "Divide and conquer. Cut the search space in half each time.", 2, "Divide and Conquer", ["searching.binary"], ["binary-search", "logarithmic", "sorted"], [
            _level("b-1","The Sorted Shelf","📚",1,"binary search","Halving","searching.binary","searching.binary",
                _story("Binary Borough Library","Librarian Zoe","Books are sorted by title. Find Dragon without checking every shelf."),
                _tutor("Byte","🧭","When things are sorted, you can cut the search in half each time.","Open the middle. If your target is smaller, go left. If bigger, go right. Repeat."),
                _discover("A sorted shelf of 8 books. Find Dragon by checking the middle.","binary-flip","Which book do you check first?","middle = 4"),
                _understand("Open the middle. If your target is smaller, go left. If bigger, go right. Repeat."),
                _manipulate("mid-point","Check position ?","middle = (low + high) // 2"),
                _code("Find the target using binary search on a sorted list.","books = ['Ant','Bear','Cat','Dragon','Eagle','Fox','Goat','Hawk']\n","target = 'Dragon'\nlo, hi = 0, len(books)-1\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if books[mid] == target: print(mid); break\n    elif books[mid] < target: lo = mid+1\n    else: hi = mid-1"),
                _checks([r"while\s+lo",r"mid\s*=\s*\(lo\s*\+\s*hi\)",r"books\[mid\]"]),
                ["The books are sorted — use that!","Check the middle first.","If target is bigger, discard the left half."],
                _success("📚 Full shelf · 🔍 Slow scan","📚 Sorted shelf · ⚡ Found at mid","The librarian is amazed — you found it in 2 checks!","Binary Search — halve the problem each time.","Sorted data unlocks speed.",25),
                predict=_predict("If the list is [1,3,5,7] and target is 4, what does the first mid check return?","index 1 (value 3)","Binary search compares the middle element and decides the direction."),
                break_step=_break_step("What happens if you write `while lo < hi` for a list of length 1?","lo, hi = 0, 0\nwhile lo < hi:\n    mid = (lo+hi)//2\n    print(nums[mid])\n","Target at index 0 is skipped"),
                 debug=_debug("Fix the off-by-one: this search can miss the first element.","def search(books, target):\n    lo, hi = 0, len(books)\n    while lo < hi:\n        mid = (lo+hi)//2\n        if books[mid] == target: return mid\n        elif books[mid] < target: lo = mid+1\n        else: hi = mid\n    return -1", fix_steps=["Use `hi = len(books)-1` and `while lo <= hi` so the first element is reachable."], answer="lo, hi = 0, len(books)-1\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if books[mid] == target: return mid\n    elif books[mid] < target: lo = mid+1\n    else: hi = mid\nreturn -1"),
                retrieval=_retrieval("What is the worst-case time complexity of binary search?","O(log n)","Each step halves the search space."),
                transfer=_transfer("Find the first occurrence of target 3 in [1,2,3,3,3,4,5].","nums = [1,2,3,3,3,4,5]\ntarget = 3\nlo, hi = 0, len(nums)-1\nans = -1\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if nums[mid] == target:\n        ans = mid\n        hi = mid-1\n    elif nums[mid] < target:\n        lo = mid+1\n    else:\n        hi = mid-1\nprint(ans)","Same search, but keep searching left after finding a match.")),
            _level("b-2","The Guess Game","🎯",2,"logarithmic","Estimating","searching.binary","searching.binary",
                _story("Binary Borough Square","Game Master Gus","Guess a number from 1 to 100 in as few tries as possible."),
                _tutor("Byte","🧭","Each guess eliminates half the possibilities. That is O(log n)!","With 100 numbers, you need at most 7 guesses. With 1000, only 10."),
                _discover("A number from 1 to 100 is hidden. Guess with feedback too high or too low.","guess-game","What is the maximum number of guesses needed?","7"),
                _understand("With 100 numbers, you need at most 7 guesses. With 1000, only 10."),
                _manipulate("guess-range","Guess ? (too high / too low)","narrow the range"),
                _code("Implement a number guessing game with binary search logic.","# Pick a number 1-100\n","import random\ntarget = random.randint(1,100)\nlo, hi = 1, 100\nwhile lo <= hi:\n    guess = (lo+hi)//2\n    # feedback would guide lo/hi"),
                _checks([r"lo\s*=\s*guess\s*\+\s*1",r"hi\s*=\s*guess\s*-\s*1"]),
                ["Each guess cuts possibilities in half.","100 numbers → max 7 guesses.","1000 numbers → max 10 guesses."],
                _success("🎯 Range unknown · 🤔 Blind guessing","🎯 Range narrowed · ✅ Found in log steps","The crowd cheers — binary guessing is lightning fast!","Logarithmic thinking — O(log n) speed.","Half the possibilities each time.",25)),
            _level("b-3","The Edge Cases","⚠️",3,"boundary conditions","Precision","searching.binary","searching.binary",
                _story("Binary Borough Edge","Inspector Ivy","What happens when the list has 1 item? Or the target is not there?"),
                _tutor("Byte","🧭","Edge cases matter. Empty lists, single items, missing targets — handle them all.","The loop condition `lo <= hi` ensures you do not miss anything."),
                _discover("A list of 1 item. Is it the target?","edge-case","What does your code do with 1 item?","yes"),
                _understand("The loop condition `lo <= hi` ensures you do not miss anything."),
                _manipulate("edge-check","What if lo > hi?","target not found"),
                _code("Handle edge cases in binary search.","# Empty list, single item, missing\n","def search(nums, target):\n    lo, hi = 0, len(nums)-1\n    while lo <= hi:\n        mid = (lo+hi)//2\n        if nums[mid] == target: return mid\n        elif nums[mid] < target: lo = mid+1\n        else: hi = mid-1\n    return -1"),
                _checks([r"return\s*-1",r"len\(nums\)",r"lo\s*<=\s*hi"]),
                ["What if the list is empty?","What if the target is not in the list?","Return -1 when lo > hi."],
                _success("⚠️ Edge ignored · 💥 Crash","⚠️ Edge handled · ✅ Robust","All edge cases covered. The search is bulletproof.","Edge handling — every case matters.","Robust code handles all inputs.",30)),
            _boss("b-boss","The Missing Page","📖",4,"search-legend","Mastering","searching.binary","searching.binary",
                _story("Binary Borough Archive","Keeper Kai","A critical page is missing from the ancient tome. Find where it should be in the sorted index."),
                _tutor("Byte","🧭","When the target is not there, binary search tells you where it should be. That is insertion position.","This is the foundation of many real-world systems."),
                _discover("A sorted index of 16 pages. Find where page 9 should be inserted.","insert-position","Where does page 9 go?","position = 8"),
                _understand("This is the foundation of many real-world systems."),
                _manipulate("insert-find","Find insertion position for 9","lower_bound"),
                _code("Find the insertion position for a missing target.","pages = list(range(1,17))\n","target = 9\nlo, hi = 0, len(pages)\nwhile lo < hi:\n    mid = (lo+hi)//2\n    if pages[mid] < target: lo = mid+1\n    else: hi = mid\nprint(lo)"),
                _checks([r"lo\s*=\s*lo\s*\+\s*1",r"pages\[mid\]\s*<\s*target"]),
                ["When target is not found, lo is the insertion point.","Use `lo < hi` instead of `lo <= hi`.","This finds the lower bound."],
                _success("📖 Page missing · 🔍 Lost","📖 Position found · ✅ Inserted","The tome is complete! The archive is restored.","Search Legend — you master binary search.","Finding where things belong is as powerful as finding them.",45),
                _reward(diamonds=45,coins=25,badges=["search-legend"],unlocks_town="town-3-sorting")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 3: Sorting Forge (sorting)
# ═══════════════════════════════════════════════════════════════
WORLD_SORTING = World(
    id="sorting", name="Sorting Forge", subtitle="Ordering Everything",
    description="How does a program put things in order? From bubble up to merge down — learn to sort.",
    icon="⚒️", order=3, theme="sorting", recommended_roles=["developer", "data-analyst"], prerequisites=["searchlands"],
    towns=[
        _make_town("bubble", "Bubble Forge", "🔥", "Bubbles rise. Swap adjacent items until sorted.", 1, "Pairwise Comparison", ["sorting.bubble"], ["bubble-sort", "swapping", "nested-loops"], [
            _level("so-1","The Bubble Rise","🫧",1,"bubble sort","Pairwise","sorting.bubble","sorting.bubble",
                _story("Sorting Forge — First Chamber","Forge Master Finn","Arrange these metal bars from shortest to longest. Swap adjacent bars only."),
                _tutor("Byte","🧭","Bubble sort compares neighbors and swaps them if they are in the wrong order.","Like bubbles rising in water — the largest sinks to the end each pass."),
                _discover("5 bars of different lengths. Swap adjacent bars to sort them.","bar-swap","Sort: [5,3,1,4,2]","[1,2,3,4,5]"),
                _understand("Like bubbles rising in water — the largest sinks to the end each pass."),
                _manipulate("swap-adj","If bar[i] > bar[i+1], swap","pass through the list"),
                _code("Implement bubble sort to arrange bars from shortest to longest.","bars = [5,3,1,4,2]\n","n = len(bars)\nfor i in range(n):\n    for j in range(0, n-i-1):\n        if bars[j] > bars[j+1]:\n            bars[j], bars[j+1] = bars[j+1], bars[j]\nprint(bars)"),
                _checks([r"for\s+in\s*range",r"if\s*bars\[j\]",r"bars\[j\],\s*bars\[j\+1\]"]),
                ["Compare each pair of neighbors.","Swap if the left one is bigger.","Repeat until no swaps needed."],
                _success("🔥 Bars jumbled · ⚒️ Unsorted","🔥 Bars arranged · ✅ Sorted","The forge glows — bars are now in order!","Bubble Sort — swap neighbors until sorted.","Each pass places the largest in place.",20)),
            _level("so-2","The Optimization","⚡",2,"optimized bubble","Early Stop","sorting.bubble","sorting.bubble",
                _story("Sorting Forge — Second Chamber","Forge Master Finn","What if the bars are already sorted? Do not waste passes!"),
                _tutor("Byte","🧭","If no swaps happen in a pass, the list is already sorted. Stop early!","This optimization makes bubble sort O(n) for nearly-sorted data."),
                _discover("Bars are already sorted: [1,2,3,4,5]. Can you stop after the first pass?","early-stop","How do you know to stop?","no swaps"),
                _understand("This optimization makes bubble sort O(n) for nearly-sorted data."),
                _manipulate("early-exit","If no swaps, break","swapped = False"),
                _code("Add early stopping to bubble sort.","bars = [1,2,3,4,5]\n","swapped = False\nfor i in range(n):\n    if not swapped: break\n    swapped = False\n    for j in range(0, n-i-1):\n        if bars[j] > bars[j+1]:\n            bars[j], bars[j+1] = bars[j+1], bars[j]\n            swapped = True"),
                _checks([r"swapped\s*=\s*False",r"if\s*not\s*swapped",r"break"]),
                ["If no swaps happen, the list is sorted.","Add a flag to track swaps.","Break out of the outer loop."],
                _success("⚡ Unnecessary passes · 🐢 Slow","⚡ Early exit · 🚀 Fast","The forge saves energy — no wasted passes!","Optimized Bubble — stop when sorted.","Early termination saves time.",25)),
            _boss("so-boss","The Great Sort","🏆",3,"sort-master","Forging","sorting.bubble","sorting.bubble",
                _story("Sorting Forge — Final Chamber","Grand Forge Master","Sort 1000 bars for the kingdom's grand archive. Every bar must be in order!"),
                _tutor("Byte","🧭","Bubble sort is simple and reliable. For large data, it is slow but correct.","Sometimes the simplest approach is the most trustworthy."),
                _discover("1000 unsorted bars. Sort them all for the archive.","great-sort","All bars in ascending order.","sorted"),
                _understand("Sometimes the simplest approach is the most trustworthy."),
                _manipulate("great-arrange","Sort all bars","bubble sort with early exit"),
                _code("Sort the full array for the grand archive.","bars = list(range(1000,0,-1))\n","n = len(bars)\nfor i in range(n):\n    swapped = False\n    for j in range(0, n-i-1):\n        if bars[j] > bars[j+1]:\n            bars[j], bars[j+1] = bars[j+1], bars[j]\n            swapped = True\n    if not swapped: break\nprint(bars[:10], '...', bars[-10:])"),
                _checks([r"swapped",r"break",r"bars\[j\]"]),
                ["The simple approach works for any size.","Early exit helps when nearly sorted.","Correctness matters more than speed."],
                _success("🏆 Bars scattered · 🔨 Chaos","🏆 Bars ordered · ✅ Archive complete","The grand archive is sorted! The kingdom celebrates.","Sort Mastery — you can order anything.","Simple, correct, reliable.",40),
                _reward(diamonds=40,coins=20,badges=["sort-forger"],unlocks_town="town-2-merge")),
        ]),
        _make_town("merge", "Merge Hall", "🔗", "Divide, sort, merge. The elegant recursive approach.", 2, "Divide and Conquer", ["sorting.merge"], ["merge-sort", "recursion", "merging"], [
            _level("m-1","The Split","✂️",1,"merge sort","Dividing","sorting.merge","sorting.merge",
                _story("Merge Hall — Entry","Merge Master Mira","To merge, you must first split. Cut the list in half, then half again."),
                _tutor("Byte","🧭","Merge sort divides the list in half, sorts each half, then merges them back.","Like sorting a deck of cards — split, sort each hand, then merge."),
                _discover("A list of 8 numbers. Split it in half repeatedly until single elements.","split-list","How many splits to get single elements?","3"),
                _understand("Like sorting a deck of cards — split, sort each hand, then merge."),
                _manipulate("split-half","Split list at mid","left = arr[:mid]; right = arr[mid:]"),
                _code("Implement the split phase of merge sort.","arr = [8,3,1,7,0,5,2,6]\n","def merge_sort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr)//2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)"),
                _checks([r"len\(arr\)\s*<=\s*1",r"mid\s*=\s*len",r"arr\[:mid\]"]),
                ["Keep splitting until single elements.","A single element is already sorted.","The base case stops the recursion."],
                _success("✂️ List whole · 🔀 Unsplitted","✂️ Fully split · 🔀 Ready to merge","The list is split into single elements.","Split Phase — divide until trivial.","Every sort starts with a split.",25)),
            _level("m-2","The Merge","🤝",2,"merging","Combining","sorting.merge","sorting.merge",
                _story("Merge Hall — Center","Merge Master Mira","Now merge the sorted halves back together. Compare front elements."),
                _tutor("Byte","🧭","Merging two sorted lists is simple: compare the front of each, take the smaller.","Like merging two sorted decks — always pick the smaller top card."),
                _discover("Two sorted lists: [1,3,5] and [2,4,6]. Merge them into one.","merge-lists","Merged result","[1,2,3,4,5,6]"),
                _understand("Like merging two sorted decks — always pick the smaller top card."),
                _manipulate("merge-two","Compare fronts, take smaller","result = []"),
                _code("Merge two sorted lists into one sorted list.","left = [1,3,5]\nright = [2,4,6]\n","result = []\ni = j = 0\nwhile i < len(left) and j < len(right):\n    if left[i] <= right[j]:\n        result.append(left[i]); i += 1\n    else:\n        result.append(right[j]); j += 1\nresult.extend(left[i:])\nresult.extend(right[j:])\nprint(result)"),
                _checks([r"while\s+",r"append",r"extend"]),
                ["Compare the front of each list.","Take the smaller one.","Append the rest of the remaining list."],
                _success("🤝 Halves separate · 🔀 Unmerged","🤝 Fully merged · ✅ One sorted list","The two halves are one sorted list!","Merge — combining sorted lists efficiently.","Two sorted inputs → one sorted output.",25)),
            _boss("m-boss","The Grand Merge","👑",3,"merge-legend","Mastering","sorting.merge","sorting.merge",
                _story("Merge Hall — Throne Room","Arch-Merge Master","Sort the entire kingdom's census data using merge sort. Every record must be in order."),
                _tutor("Byte","🧭","Merge sort is O(n log n) — fast and stable. It is the gold standard of sorting.","Divide, sort, merge. Repeat until the whole list is ordered."),
                _discover("Census data of 1000 records. Sort by ID using merge sort.","census-sort","All records sorted by ID.","sorted"),
                _understand("Divide, sort, merge. Repeat until the whole list is ordered."),
                _manipulate("grand-merge","Full merge sort implementation","O(n log n)"),
                _code("Implement complete merge sort for the census data.","data = [5,2,8,1,9,3,7,4,6,0]\n","def merge_sort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr)//2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\ndef merge(l,r):\n    res = []\n    i = j = 0\n    while i < len(l) and j < len(r):\n        if l[i] <= r[j]: res.append(l[i]); i += 1\n        else: res.append(r[j]); j += 1\n    res.extend(l[i:]); res.extend(r[j:])\n    return res\nprint(merge_sort(data))"),
                _checks([r"merge_sort",r"merge\s*\(",r"return\s*res"]),
                ["Divide recursively, then merge.","The merge step is the key.","O(n log n) — efficient for any size."],
                _success("👑 Data chaotic · 📊 Unsorted","👑 Data ordered · ✅ Census complete","The kingdom's census is perfectly sorted!","Merge Legend — O(n log n) elegance.","Divide, conquer, merge.",45),
                _reward(diamonds=45,coins=25,badges=["merge-master"],unlocks_town="town-3-recursion")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 4: Recursive Mountains (recursion)
# ═══════════════════════════════════════════════════════════════
WORLD_RECURSION = World(
    id="recursion", name="Recursive Mountains", subtitle="Self-Similar Problem Solving",
    description="Some problems are best solved by solving smaller versions of themselves. Learn recursion.",
    icon="🏔️", order=4, theme="recursion", recommended_roles=["developer", "ai-engineer"], prerequisites=["sorting"],
    towns=[
        _make_town("base", "Base Camp", "⛺", "Every recursive journey starts with a base case.", 1, "Self-Reference", ["recursion.base"], ["base-case", "recursive-thinking", "stack-trace"], [
            _level("r-1","The Mirror","🪞",1,"recursion","Self-Similar","recursion.base","recursion.base",
                _story("Mountain Trailhead","Guide Greta","A mirror shows a smaller version of you. Recursion is the same — a function calling itself on a smaller problem."),
                _tutor("Byte","🧭","Recursion solves a big problem by breaking it into a smaller version of the same problem.","Every recursive function needs a base case — the simplest version that stops the recursion."),
                _discover("A mirror shows you, which shows a smaller you, which shows... When does it stop?","mirror-chain","When does the reflection stop?","base case reached"),
                _understand("Every recursive function needs a base case — the simplest version that stops the recursion."),
                _manipulate("mirror-stop","When does recursion stop?","base case"),
                _code("Write a recursive function with a base case.","# Factorial: n! = n * (n-1)!\n","def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n-1)\nprint(factorial(5))"),
                _checks([r"if\s+n\s*<=\s*1",r"return\s*1",r"return\s+n\s*\*"]),
                ["The smallest case stops the recursion.","5! = 5 × 4!, 4! = 4 × 3!, ..., 1! = 1.","Each call works on a smaller input."],
                _success("🪞 Infinite mirrors · 💥 Stack overflow","🪞 Mirrors resolved · ✅ Base found","The reflection stops at the base case.","Recursion — solving big problems with small versions.","Every recursive journey needs a base case.",20)),
            _level("r-2","The Ladder","🪜",2,"call stack","Understanding","recursion.base","recursion.base",
                _story("Mountain Lodge","Lodge Keeper Leo","Each recursive call waits on a ladder. The last one called returns first."),
                _tutor("Byte","🧭","The call stack is like a ladder — each recursive call adds a rung. The base case is the top.","When the base case is reached, each call returns in reverse order."),
                _discover("A ladder with 5 rungs. Climb up recursively, then come back down.","ladder-climb","What order do you return?","5,4,3,2,1"),
                _understand("When the base case is reached, each call returns in reverse order."),
                _manipulate("stack-ladder","Climb to rung ?","push then pop"),
                _code("Trace the call stack for a recursive function.","def countdown(n):\n    if n <= 0: return\n    print(n)\n    countdown(n-1)\n","countdown(5) prints 5,4,3,2,1"),
                _checks([r"countdown\(n-1\)",r"if\s+n\s*<=\s*0"]),
                ["Each call waits for the next one.","The deepest call returns first.","Stack: Last In, First Out."],
                _success("🪜 Ladder infinite · ⏳ Waiting","🪜 Ladder climbed · ✅ Returns in order","The lodge keeper understands the call stack perfectly.","Call Stack — understanding the execution order.","Last call returns first.",25)),
            _boss("r-boss","The Summit","🏔️",3,"recursion-master","Reaching","recursion.base","recursion.base",
                _story("Mountain Summit","Summit Sage","Reach the summit by solving progressively smaller problems. Each step is a recursive call."),
                _tutor("Byte","🧭","The summit is the base case. Every step down is a recursive call.","When you reach the top, you can trace your path back down."),
                _discover("Climb from base camp (0) to summit (10). Each step doubles your progress.","summit-climb","How many steps to reach 10?","4"),
                _understand("When you reach the top, you can trace your path back down."),
                _manipulate("summit-path","Reach summit with recursive steps","steps = 0"),
                _code("Use recursion to compute a power of 2.","# 2^n using recursion\n","def power_of_2(n):\n    if n == 0: return 1\n    return 2 * power_of_2(n-1)\nprint(power_of_2(10))"),
                _checks([r"if\s+n\s*==\s*0",r"return\s*1",r"return\s*2\s*\*"]),
                ["Each step reduces the problem by 1.","2^10 = 2 × 2^9 = 2 × 2 × 2^8 ...","The base case is 2^0 = 1."],
                _success("🏔️ Base camp only · 🏔️ Not summited","🏔️ Summit reached · ✅ View from top","You see the entire recursive mountain from the top!","Recursion Master — you can climb any recursive problem.","Base case + recursive case = solution.",40),
                _reward(diamonds=40,coins=20,badges=["recursion-base"],unlocks_town="town-2-divide")),
        ]),
        _make_town("divide", "Divide Peak", "🏔️", "Recursive division. Break problems into independent sub-problems.", 2, "Divide and Conquer", ["recursion.divide"], ["divide-conquer", "recursive-structure", "combine"], [
            _level("d-1","The Split Path","🛤️",1,"divide and conquer","Splitting","recursion.divide","recursion.divide",
                _story("Divide Peak Trail","Trail Guide Dora","At each fork, the path splits into two. Follow both branches."),
                _tutor("Byte","🧭","Divide and conquer: split the problem, solve each part, combine the results.","Merge sort and binary search both use this pattern."),
                _discover("A path splits into two at each junction. How many paths after 3 splits?","path-split","Total paths","8"),
                _understand("Merge sort and binary search both use this pattern."),
                _manipulate("path-count","Paths after n splits","2^n"),
                _code("Count paths in a divide-and-conquer tree.","# Binary tree of splits\n","def count_paths(depth):\n    if depth == 0: return 1\n    return 2 * count_paths(depth-1)\nprint(count_paths(3))"),
                _checks([r"if\s+depth\s*==\s*0",r"return\s*1",r"return\s*2\s*\*"]),
                ["Each split doubles the paths.","3 splits → 2³ = 8 paths.","The tree of recursive calls."],
                _success("🛤️ Single path · 🔀 No splits","🛤️ All paths explored · ✅ Counted","Every branch of the divide tree is traced.","Divide — splitting into sub-problems.","2^n paths after n splits.",25)),
            _level("d-2","The Combine","🔗",2,"combining results","Merging","recursion.divide","recursion.divide",
                _story("Divide Peak Summit","Summit Architect","The sub-problems are solved. Now combine their results into the final answer."),
                _tutor("Byte","🧭","The combine step is where the magic happens. Sorted halves become a sorted whole.","Without combining, you just have solved pieces, not the solution."),
                _discover("Two sorted results: [1,3,5] and [2,4,6]. Combine into one sorted result.","combine-results","Combined sorted","[1,2,3,4,5,6]"),
                _understand("Without combining, you just have solved pieces, not the solution."),
                _manipulate("combine-step","Merge two sorted results","two-pointer merge"),
                _code("Combine two sorted arrays into one.","left = [1,3,5]\nright = [2,4,6]\n","result = []\ni = j = 0\nwhile i < len(left) and j < len(right):\n    if left[i] <= right[j]:\n        result.append(left[i]); i += 1\n    else:\n        result.append(right[j]); j += 1\nresult.extend(left[i:])\nresult.extend(right[j:])\nprint(result)"),
                _checks([r"while\s+",r"append",r"extend"]),
                ["Compare elements from each half.","Take the smaller one.","Append remaining elements."],
                _success("🔗 Halves separate · ❌ Not combined","🔗 Fully combined · ✅ One result","The combined result is perfectly sorted!","Combine — merging sub-solutions.","The whole is greater than the sum of parts.",25)),
            _boss("d-boss","The Master Divide","👑",3,"divide-legend","Mastering","recursion.divide","recursion.divide",
                _story("Divide Peak Throne","Master Architect","Solve the master problem: given an array, return the sum of all elements using divide and conquer."),
                _tutor("Byte","🧭","The master divide: split the array in half, sum each half, add the two sums.","This is the essence of recursive problem solving."),
                _discover("Array of 16 numbers. Sum them using divide and conquer.","master-sum","Total sum","136"),
                _understand("This is the essence of recursive problem solving."),
                _manipulate("master-split","Split and sum recursively","sum = left_sum + right_sum"),
                _code("Implement sum using divide and conquer.","arr = list(range(1,17))\n","def dc_sum(arr):\n    if len(arr) <= 1: return arr[0] if arr else 0\n    mid = len(arr)//2\n    return dc_sum(arr[:mid]) + dc_sum(arr[mid:])\nprint(dc_sum(list(range(1,17))))"),
                _checks([r"dc_sum",r"arr\[:mid\]",r"arr\[mid:\]"]),
                ["Base case: single element or empty.","Split and recurse on both halves.","Combine by adding the two sums."],
                _success("👑 Problem whole · ❌ Not divided","👑 Problem solved · ✅ Master of divide","The master problem is solved with pure divide and conquer!","Divide Legend — recursive problem mastery.","Split, solve, combine.",45),
                _reward(diamonds=45,coins=25,badges=["divide-master"],unlocks_town="town-3-trees")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 5: Linked Pathways (linked-list)
# ═══════════════════════════════════════════════════════════════
WORLD_LINKED = World(
    id="linked", name="Linked Pathways", subtitle="Chains of Connection",
    description="Everything is connected. Learn linked lists — chains where each element points to the next.",
    icon="🔗", order=5, theme="linked", recommended_roles=["developer"], prerequisites=["recursion"],
    towns=[
        _make_town("singly", "Singly Chain", "➡️", "Each node points to the next. A one-way chain.", 1, "Forward Links", ["data-structures.linked-list"], ["singly-linked", "pointers", "traversal"], [
            _level("l-1","The Chain","⛓️",1,"linked list","Forward","data-structures.linked-list","data-structures.linked-list",
                _story("Linked Pathway — Start","Path Builder Pip","Build a chain of nodes where each points to the next. The first is the head."),
                _tutor("Byte","🧭","A linked list is a chain of nodes. Each node holds data and a pointer to the next.","Like a treasure hunt — each clue leads to the next one."),
                _discover("Build a chain: Node A → Node B → Node C. Each node has a value and a next pointer.","chain-build","A → B → C","head"),
                _understand("Like a treasure hunt — each clue leads to the next one."),
                _manipulate("link-nodes","Create node with value and next","Node(value, next)"),
                _code("Create a linked list with 3 nodes.","class Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None\n","head = Node('A')\nhead.next = Node('B')\nhead.next.next = Node('C')"),
                _checks([r"class\s+Node",r"self\.val",r"self\.next"]),
                ["Each node has a value and a next pointer.","The head is the first node.","The last node's next is None."],
                _success("⛓️ No chain · 🔗 Loose nodes","⛓️ Chain built · ✅ Linked","The pathway is connected from head to tail!","Linked List — chains of connected nodes.","Each node knows the next one.",20)),
            _level("l-2","The Traversal","🚶",2,"traversal","Following","data-structures.linked-list","data-structures.linked-list",
                _story("Linked Pathway — Middle","Path Walker Willow","Walk the chain from head to tail. Collect all the values along the way."),
                _tutor("Byte","🧭","Traversal follows the chain from head to tail, visiting each node exactly once.","Like reading a chain of clues — start at the beginning and follow each link."),
                _discover("Chain: A → B → C → D. Collect all values in order.","traverse-chain","Collected values","['A','B','C','D']"),
                _understand("Like reading a chain of clues — start at the beginning and follow each link."),
                _manipulate("walk-chain","Start at head, follow next","current = head"),
                _code("Traverse a linked list and collect all values.","head = Node('A')\nhead.next = Node('B')\n","vals = []\ncurrent = head\nwhile current:\n    vals.append(current.val)\n    current = current.next\nprint(vals)"),
                _checks([r"while\s+current",r"current\s*=\s*current\.next",r"vals\.append"]),
                ["Start at the head node.","Follow the next pointer.","Stop when current is None."],
                _success("🚶 Chain broken · ❌ Can't traverse","🚶 Full traversal · ✅ All values collected","Every node in the chain has been visited!","Traversal — following the chain.","O(n) time — visit each node once.",25)),
            _boss("l-boss","The Reversal","🔄",3,"linked-master","Reversing","data-structures.linked-list","data-structures.linked-list",
                _story("Linked Pathway — End","Path Master Piper","Reverse the chain so the tail becomes the head. Every pointer now goes backward."),
                _tutor("Byte","🧭","Reversing a linked list is a classic problem. Change each node's next pointer to point to the previous node.","Three pointers: previous, current, next. Walk through and flip."),
                _discover("Chain: A → B → C → D. Reverse it to D → C → B → A.","reverse-chain","Reversed chain","D → C → B → A"),
                _understand("Three pointers: previous, current, next. Walk through and flip."),
                _manipulate("flip-pointers","Reverse the chain","prev, curr, next"),
                _code("Reverse a linked list in-place.","head = Node('A')\nhead.next = Node('B')\n","prev = None\ncurrent = head\nwhile current:\n    next_node = current.next\n    current.next = prev\n    prev = current\n    current = next_node\nhead = prev"),
                _checks([r"prev\s*=\s*None",r"next_node",r"current\.next\s*=\s*prev"]),
                ["Three pointers: prev, current, next.","Flip each pointer to the previous node.","Move all three forward."],
                _success("🔄 Chain forward · ❌ Not reversed","🔄 Chain reversed · ✅ Tail is head","The chain now flows backward! The tail is the new head.","Linked Master — reverse any chain.","Pointer manipulation mastery.",40),
                _reward(diamonds=40,coins=20,badges=["linked-master"],unlocks_town="town-2-stack")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 6: Stack Tower (stack)
# ═══════════════════════════════════════════════════════════════
WORLD_STACK = World(
    id="stack", name="Stack Tower", subtitle="Last In, First Out",
    description="Build a tower where the last piece added is the first removed. Learn stacks.",
    icon="🗼", order=6, theme="stack", recommended_roles=["developer"], prerequisites=["linked"],
    towns=[
        _make_town("push", "Push Platform", "📥", "Push items onto the stack. The top grows upward.", 1, "LIFO", ["data-structures.stack"], ["stack", "push", "pop"], [
            _level("st-1","The Tower","🧱",1,"stack","LIFO","data-structures.stack","data-structures.stack",
                _story("Stack Tower — Ground Floor","Builder Ben","Build a tower by placing blocks on top. The last block placed is the first to remove."),
                _tutor("Byte","🧭","A stack is Last In, First Out (LIFO). Think of a stack of plates.","You push items onto the top and pop them from the top."),
                _discover("Stack of plates: push plate 1, then 2, then 3. Which plate is on top?","plate-stack","Top plate","3"),
                _understand("You push items onto the top and pop them from the top."),
                _manipulate("push-plate","Push plate ? onto stack","stack.append(plate)"),
                _code("Implement a stack using a list. Push and pop plates.","stack = []\n","stack.append(1)\nstack.append(2)\nstack.append(3)\nprint(stack.pop())  # 3\nprint(stack.pop())  # 2"),
                _checks([r"append",r"pop",r"stack\s*=\s*\[\]"]),
                ["Push adds to the top.","Pop removes from the top.","Last in, first out."],
                _success("🧱 No tower · 📦 Empty","🧱 Tower built · ✅ LIFO working","The tower works perfectly!","Stack — Last In, First Out.","Push and pop from the same end.",20)),
            _level("st-2","The Bracket Match","🔍",2,"matching","Validating","data-structures.stack","data-structures.stack",
                _story("Stack Tower — Middle Floor","Checker Cara","Match opening and closing brackets. Every opening bracket needs a closing one."),
                _tutor("Byte","🧭","Use a stack to check bracket matching. Push opening brackets, pop when you see closing.","If the stack is empty at the end, all brackets are matched."),
                _discover("String: ({[]}). Check if all brackets match.","bracket-check","Valid","True"),
                _understand("If the stack is empty at the end, all brackets are matched."),
                _manipulate("match-bracket","Push open, pop on close","stack"),
                _code("Check if brackets in a string are balanced.","s = '({[]})'\n","stack = []\nfor c in s:\n    if c in '({[': stack.append(c)\n    elif c in ')}]':\n        if not stack: print(False); break\n        stack.pop()\nprint(len(stack) == 0)"),
                _checks([r"append",r"pop",r"if\s+not\s+stack"]),
                ["Push opening brackets.","Pop when you see a closing bracket.","Stack must be empty at the end."],
                _success("🔍 Brackets unmatched · ❌ Invalid","🔍 Brackets matched · ✅ Valid","All brackets are perfectly matched!","Bracket Matching — stack validation.","Stacks are perfect for matching pairs.",25)),
            _boss("st-boss","The Function Call","📞",3,"stack-master","Calling","data-structures.stack","data-structures.stack",
                _story("Stack Tower — Top Floor","Call Master Carl","Understand how function calls use the call stack. Each call pushes a frame, each return pops it."),
                _tutor("Byte","🧭","The call stack is a stack! Each function call pushes a frame with local variables. Returns pop the frame.","Recursion uses the call stack — each recursive call adds a frame."),
                _discover("Function calls: main() → foo() → bar(). Track the call stack frames.","call-stack","Frame order","main, foo, bar"),
                _understand("Recursion uses the call stack — each recursive call adds a frame."),
                _manipulate("frame-push","Push frame on call, pop on return","call stack"),
                _code("Trace the call stack for nested function calls.","def bar(): return 'bar'\ndef foo(): return bar()\ndef main(): return foo()\n","# Call stack: main → foo → bar\n# Returns: bar → foo → main\nprint(main())"),
                _checks([r"def\s+",r"return",r"print\(main"]),
                ["Each function call pushes a frame.","The deepest call returns first.","The call stack is LIFO."],
                _success("📞 No frames · ❌ Lost","📞 Frames tracked · ✅ Stack understood","The call stack is fully understood!","Stack Master — understand LIFO in practice.","Every function call is a stack operation.",40),
                _reward(diamonds=40,coins=20,badges=["stack-master"],unlocks_town="town-2-queue")),
        ]),
    ]
)


# ═══════════════════════════════════════════════════════════════
# WORLD 5 EXPANSION: Linked Pathways — advanced operations
# ═══════════════════════════════════════════════════════════════
WORLD_LINKED_ADV = World(
    id="linked-advanced", name="Linked Mastery", subtitle="Advanced Chain Operations",
    description="Master insertion, deletion, and cycle detection in linked lists.",
    icon="🔗", order=5, theme="linked", recommended_roles=["developer"], prerequisites=["linked"],
    towns=[
        _make_town("advanced", "Advanced Chain", "🔬", "Push your linked list skills further.", 1, "Advanced Ops", ["data-structures.linked-list.advanced"], ["insertion", "deletion", "cycle-detection"], [
            _level("l-3","The Insert","📝",1,"insertion","Adding","data-structures.linked-list.advanced","data-structures.linked-list.advanced",
                _story("Linked Pathway — Workshop","Insertion Artist Ivy","Add a new node at a specific position in the chain without breaking it."),
                _tutor("Byte","🧭","Insertion requires updating the previous node's next pointer to the new node, and the new node's next to the old next.","Three pointers: prev, curr, new_node."),
                _discover("Chain A → B → D. Insert C between B and D.","insert-between","New chain","A → B → C → D"),
                _understand("Three pointers: prev, curr, new_node."),
                _manipulate("insert-node","Insert at position 2","prev.next = new_node"),
                _code("Insert a node at index 2 in a linked list.","class Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None\n","def insert_at(head, val, idx):\n    new = Node(val)\n    if idx == 0:\n        new.next = head\n        return new\n    curr = head\n    for _ in range(idx - 1):\n        if not curr: return head\n        curr = curr.next\n    new.next = curr.next\n    curr.next = new\n    return head"),
                _checks([r"new\.next",r"curr\.next\s*="]),
                ["Find the node before the insertion point.","Point it to the new node.","Point the new node to the old next."],
                _success("📝 Chain gap · ❌ Missing node","📝 Node inserted · ✅ Chain complete","The new node fits perfectly into the chain!","Insertion — adding nodes without breaking links.","Pointer updates in O(1) at known index.",25)),
            _level("l-4","The Drop","🗑️",2,"deletion","Removing","data-structures.linked-list.advanced","data-structures.linked-list.advanced",
                _story("Linked Pathway — Cleanup","Deletion Dexter","Remove a node from the chain by skipping it. No loose ends."),
                _tutor("Byte","🧭","To delete a node, point the previous node's next to the deleted node's next. The deleted node is garbage collected.","You never actually 'delete' in Python — you just remove references."),
                _discover("Chain A → B → C → D. Remove B. Result: A → C → D.","remove-node","New chain","A → C → D"),
                _understand("You never actually 'delete' in Python — you just remove references."),
                _manipulate("skip-node","Remove node at index 1","prev.next = curr.next"),
                _code("Delete the node at index 1 from a linked list.","class Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None\n","def delete_at(head, idx):\n    if idx == 0:\n        return head.next\n    curr = head\n    for _ in range(idx - 1):\n        if not curr or not curr.next: return head\n        curr = curr.next\n    if curr.next:\n        curr.next = curr.next.next\n    return head"),
                _checks([r"curr\.next\s*=",r"return\s+head\.next"]),
                ["Find the node before the one to delete.","Point its next to the deleted node's next.","The deleted node is orphaned."],
                _success("🗑️ Node loose · ❌ Chain broken","🗑️ Node removed · ✅ Chain intact","The node is gone and the chain is unbroken!","Deletion — removing nodes cleanly.","No memory leaks, no broken chains.",25)),
            _level("l-5","The Loop","♻️",3,"cycle-detection","Detecting","data-structures.linked-list.advanced","data-structures.linked-list.advanced",
                _story("Linked Pathway — Maze","Loop Detective Luna","A chain has a loop! Use Floyd's algorithm to find where it starts."),
                _tutor("Byte","🧭","Floyd's Tortoise and Hare: slow pointer moves 1 step, fast moves 2. If they meet, there's a loop.","To find the loop start, reset one pointer to head and move both 1 step until they meet."),
                _discover("Chain with loop at node C. Detect and find the loop entry.","loop-find","Loop entry","C"),
                _understand("To find the loop start, reset one pointer to head and move both 1 step until they meet."),
                _manipulate("tortoise-hare","Slow + fast pointers","fast = fast.next.next"),
                _code("Detect a cycle in a linked list using Floyd's algorithm.","class Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None\n","def detect_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            # Find entry\n            entry = head\n            while entry != slow:\n                entry = entry.next\n                slow = slow.next\n            return entry.val\n    return None"),
                _checks([r"slow\s*=\s*slow\.next",r"fast\s*=\s*fast\.next\.next",r"entry\s*=\s*head"]),
                ["Slow moves 1 step, fast moves 2.","If they meet, there's a loop.","Reset one to head to find the entry."],
                _success("♻️ Loop hidden · ❌ Infinite","♻️ Loop found · ✅ Entry detected","The loop is detected and its entry point found!","Cycle Detection — Floyd's algorithm.","O(n) time, O(1) space.",30)),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 6 EXPANSION: Stack Tower — advanced patterns
# ═══════════════════════════════════════════════════════════════
WORLD_STACK_ADV = World(
    id="stack-advanced", name="Stack Mastery", subtitle="Beyond Basic LIFO",
    description="Master stack patterns: min stacks, stock spans, and nested decoding.",
    icon="🗼", order=6, theme="stack", recommended_roles=["developer"], prerequisites=["stack"],
    towns=[
        _make_town("advanced", "Advanced Stack", "🏗️", "Stack patterns used in real interviews.", 1, "Patterns", ["data-structures.stack.advanced"], ["min-stack", "stock-span", "decode-string"], [
            _level("st-3","The Min Stack","📉",1,"min-stack","Tracking","data-structures.stack.advanced","data-structures.stack.advanced",
                _story("Stack Tower — Basement","Min Keeper Mina","Track the minimum value in a stack with O(1) getMin()."),
                _tutor("Byte","🧭","A min stack uses two stacks: one for values, one for minimums. When you push, also push the current min.","getMin() just peeks the min stack."),
                _discover("Stack: [5, 3, 8, 1]. getMin() should return 1 at any time.","min-peek","Current min","1"),
                _understand("getMin() just peeks the min stack."),
                _manipulate("dual-stack","Main stack + min stack","min_stack.append(min(val, min_stack[-1]))"),
                _code("Implement a stack with O(1) getMin().","class MinStack:\n    def __init__(self):\n        self.stack = []\n        self.min_stack = []\n","    def push(self, val):\n        self.stack.append(val)\n        self.min_stack.append(min(val, self.min_stack[-1]) if self.min_stack else val)\n    def pop(self):\n        self.stack.pop()\n        self.min_stack.pop()\n    def getMin(self):\n        return self.min_stack[-1]"),
                _checks([r"min_stack\.append",r"min_stack\[-1\]",r"getMin"]),
                ["Push onto both stacks.","Min stack stores running minimum.","getMin() is O(1)."],
                _success("📉 Min unknown · ❌ No O(1) min","📉 Min tracked · ✅ O(1) getMin","The minimum is always available instantly!","Min Stack — O(1) minimum tracking.","Auxiliary stack for running minimum.",30)),
            _level("st-4","The Stock Span","📈",2,"stock-span","Daily","data-structures.stack.advanced","data-structures.stack.advanced",
                _story("Stack Tower — Observatory","Span Sage Sid","For each day, how many consecutive days was the stock ≤ today?"),
                _tutor("Byte","🧭","The stock span problem uses a monotonic stack. Pop while stack top ≤ current price. The span is current index - stack top index.","This gives O(n) instead of O(n²)."),
                _discover("Prices: [100, 80, 60, 70, 60, 75, 85]. Span for each day?","span-calc","Spans","[1,1,1,2,1,4,6]"),
                _understand("This gives O(n) instead of O(n²)."),
                _manipulate("monotonic-stack","Pop while top <= current","while stack and prices[stack[-1]] <= price"),
                _code("Calculate stock spans using a monotonic stack.","prices = [100, 80, 60, 70, 60, 75, 85]\n","def stock_span(prices):\n    stack = []\n    spans = []\n    for i, p in enumerate(prices):\n        while stack and prices[stack[-1]] <= p:\n            stack.pop()\n        spans.append(i - (stack[-1] if stack else -1))\n        stack.append(i)\n    return spans\nprint(stock_span(prices))"),
                _checks([r"while\s+stack",r"prices\[stack\[-1\]\]\s*<=",r"stack\.append"]),
                ["Pop while stack top ≤ current.","Span = current index - new stack top index.","Monotonic decreasing stack."],
                _success("📈 Span unknown · ❌ O(n²)","📈 Span calculated · ✅ O(n)","All spans are computed efficiently!","Stock Span — monotonic stack pattern.","Classic interview problem.",30)),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 7: Queue Avenue (queue)
# ═══════════════════════════════════════════════════════════════
WORLD_QUEUE = World(
    id="queue", name="Queue Avenue", subtitle="First In, First Out",
    description="Master queues — the line where the first to arrive is the first to leave.",
    icon="🚶", order=7, theme="queue", recommended_roles=["developer", "data-engineer"], prerequisites=["stack"],
    towns=[
        _make_town("line", "Waiting Line", "🧍", "Join the line. The first person in is the first person out.", 1, "FIFO", ["data-structures.queue"], ["queue", "enqueue", "dequeue"], [
            _level("q-1","The Line","🧍",1,"queue","FIFO","data-structures.queue","data-structures.queue",
                _story("Queue Avenue — Start","Line Leader Lena","People join a line. The first person to arrive is the first to be served."),
                _tutor("Byte","🧭","A queue is First In, First Out (FIFO). Enqueue adds to the back, dequeue removes from the front.","Like a ticket line — first ticket gets served first."),
                _discover("Line: Alice arrives, then Bob, then Carol. Who gets served first?","line-order","First served","Alice"),
                _understand("Like a ticket line — first ticket gets served first."),
                _manipulate("join-line","Enqueue person ?","queue.append(person)"),
                _code("Implement a queue using a list. Enqueue and dequeue people.","queue = []\n","queue.append('Alice')\nqueue.append('Bob')\nqueue.append('Carol')\nprint(queue.pop(0))  # Alice\nprint(queue.pop(0))  # Bob"),
                _checks([r"append",r"pop\(0\)",r"queue\s*=\s*\[\]"]),
                ["Enqueue adds to the back.","Dequeue removes from the front.","First in, first out."],
                _success("🧍 No line · 📭 Empty","🧍 Line formed · ✅ FIFO working","The queue works perfectly!","Queue — First In, First Out.","Enqueue at back, dequeue from front.",20)),
            _level("q-2","The Ticket Machine","🎫",2,"circular-queue","Reusing","data-structures.queue","data-structures.queue",
                _story("Queue Avenue — Ticket Booth","Booth Operator Bob","The ticket machine has 5 slots. When slot 5 is filled, it wraps to slot 1."),
                _tutor("Byte","🧭","A circular queue reuses empty slots. (front + 1) % capacity gives the next slot.","This avoids shifting elements on dequeue."),
                _discover("5-slot circular queue. Enqueue A, B, C, D, E, then F. Where does F go?","circular-wrap","Slot for F","0"),
                _understand("This avoids shifting elements on dequeue."),
                _manipulate("circular-enqueue","Next slot = (front + 1) % capacity","(front + 1) % capacity"),
                _code("Implement a circular queue with fixed capacity.","class CircularQueue:\n    def __init__(self, k):\n        self.queue = [None] * k\n        self.front = 0\n        self.rear = -1\n        self.size = 0\n        self.cap = k\n","    def enqueue(self, val):\n        if self.size == self.cap: return False\n        self.rear = (self.rear + 1) % self.cap\n        self.queue[self.rear] = val\n        self.size += 1\n        return True\n    def dequeue(self):\n        if self.size == 0: return False\n        val = self.queue[self.front]\n        self.front = (self.front + 1) % self.cap\n        self.size -= 1\n        return val"),
                _checks([r"%\s*self\.cap",r"self\.rear\s*=",r"self\.front\s*="]),
                ["Use modulo to wrap around.","Front and rear move independently.","Empty slots are reused."],
                _success("🎫 Slots wasted · ❌ No reuse","🎫 Slots reused · ✅ Circular","The circular queue reuses slots efficiently!","Circular Queue — fixed-size ring buffer.","Avoids O(n) dequeue by wrapping.",25)),
            _level("q-3","The Printer Queue","🖨️",3,"priority-queue","Serving","data-structures.queue","data-structures.queue",
                _story("Queue Avenue — Print Shop","Printer Pat","Print jobs have priorities. Important jobs must print first, not just arrival order."),
                _tutor("Byte","🧭","A priority queue serves highest-priority items first. It's often implemented with a heap.","Like an ER triage — critical patients go first."),
                _discover("Print jobs: [(1, 'report'), (2, 'invoice'), (3, 'urgent')]. Order of printing?","priority-order","Print order","urgent, invoice, report"),
                _understand("Like an ER triage — critical patients go first."),
                _manipulate("heap-push","Push with priority","heapq.heappush(heap, (-priority, job))"),
                _code("Simulate a priority printer queue.","import heapq\n","jobs = []\nheapq.heappush(jobs, (1, 'report'))\nheapq.heappush(jobs, (2, 'invoice'))\nheapq.heappush(jobs, (3, 'urgent'))\nwhile jobs:\n    print(heapq.heappop(jobs)[1])"),
                _checks([r"heapq\.heappush",r"heapq\.heappop",r"import\s+heapq"]),
                ["Higher priority = smaller number in min-heap.","Use negative priority for max-heap behavior.","heapq is Python's binary heap."],
                _success("🖨️ Random order · ❌ No priority","🖨️ Priority order · ✅ Urgent first","Jobs print by priority, not arrival!","Priority Queue — heap-based ordering.","Critical jobs first, always.",25)),
        ]),
        _make_town("advanced", "Advanced Queue", "🧠", "Queue patterns for real systems.", 2, "Patterns", ["data-structures.queue.advanced"], ["sliding-window", "queue-stack", "multiqueue"], [
            _level("q-4","The Sliding Window","🪟",4,"sliding-window","Tracking","data-structures.queue","data-structures.queue",
                _story("Queue Avenue — Watchtower","Watcher Will","Track the maximum in a sliding window of size k. The window slides forward one step at a time."),
                _tutor("Byte","🧭","A deque (double-ended queue) maintains the window. Pop from front when index > front + k. Pop from back while value < current.","This gives O(n) instead of O(n*k)."),
                _discover("Array [1,3,-1,-3,5,3,6,7], k=3. Max in each window?","window-max","Maxima","[3,3,5,5,6,7]"),
                _understand("This gives O(n) instead of O(n*k)."),
                _manipulate("deque-window","Maintain decreasing deque","while dq and nums[dq[-1]] < nums[i]: dq.pop()"),
                _code("Find max in each sliding window of size k.","from collections import deque\nnums = [1,3,-1,-3,5,3,6,7]\nk = 3\n","def max_sliding(nums, k):\n    dq = deque()\n    out = []\n    for i, v in enumerate(nums):\n        while dq and nums[dq[-1]] < v:\n            dq.pop()\n        dq.append(i)\n        if dq[0] <= i - k:\n            dq.popleft()\n        if i >= k - 1:\n            out.append(nums[dq[0]])\n    return out\nprint(max_sliding(nums, k))"),
                _checks([r"deque\(\)",r"dq\.pop\(\)",r"dq\.append",r"dq\.popleft"]),
                ["Maintain decreasing values in deque.","Pop front when out of window.","Front of deque is always the max."],
                _success("🪟 Window blind · ❌ Can't see","🪟 Window clear · ✅ Maxima found","The sliding window maxima are all found!","Sliding Window — deque optimization.","O(n) instead of O(n*k).",30)),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 8: Tree Grove (tree)
# ═══════════════════════════════════════════════════════════════
WORLD_TREE = World(
    id="tree", name="Tree Grove", subtitle="Branching Hierarchies",
    description="Learn trees — hierarchical structures with a root, branches, and leaves.",
    icon="🌳", order=8, theme="tree", recommended_roles=["developer", "data-engineer"], prerequisites=["linked"],
    towns=[
        _make_town("binary", "Binary Branch", "🌿", "Each node has at most two children: left and right.", 1, "Binary", ["data-structures.tree"], ["binary-tree", "traversal", "bst"], [
            _level("t-1","The Root","🌱",1,"binary-tree","Rooted","data-structures.tree","data-structures.tree",
                _story("Tree Grove — Seed","Planter Priya","A tree starts with a root. Each node can have up to two children: left and right."),
                _tutor("Byte","🧭","A binary tree has a root, and each node has at most two children. The left child is smaller, the right child is larger (in a BST).","Trees are recursive: each subtree is itself a tree."),
                _discover("Root: 5. Left child: 3. Right child: 8. What is the root's value?","root-value","Root value","5"),
                _understand("Trees are recursive: each subtree is itself a tree."),
                _manipulate("plant-root","Create root with left and right","TreeNode(val, left, right)"),
                _code("Create a binary tree with root 5, left child 3, right child 8.","class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n","root = TreeNode(5)\nroot.left = TreeNode(3)\nroot.right = TreeNode(8)"),
                _checks([r"class\s+TreeNode",r"self\.left",r"self\.right"]),
                ["Root is the top node.","Left child < root, right child > root (BST).","Each node is a subtree."],
                _success("🌱 No root · ❌ Empty","🌱 Root planted · ✅ Tree growing","The tree has its root and two children!","Binary Tree — hierarchical structure.","Root, left, right — the tree anatomy.",20)),
            _level("t-2","The Walk","🚶",2,"tree-traversal","Visiting","data-structures.tree","data-structures.tree",
                _story("Tree Grove — Path","Walker Wes","Visit every node in the tree. In-order, pre-order, post-order — each order tells a different story."),
                _tutor("Byte","🧭","In-order: left, root, right. Pre-order: root, left, right. Post-order: left, right, root.","In-order of a BST gives sorted order."),
                _discover("Tree: root 5, left 3, right 8. In-order traversal?","in-order","In-order","3, 5, 8"),
                _understand("In-order of a BST gives sorted order."),
                _manipulate("traverse-tree","Visit left, root, right","inorder(node.left) + [node.val] + inorder(node.right)"),
                _code("Perform in-order traversal of a binary tree.","class TreeNode:\n    def __init__(self, val, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n","def inorder(node):\n    if not node: return []\n    return inorder(node.left) + [node.val] + inorder(node.right)\nroot = TreeNode(5, TreeNode(3), TreeNode(8))\nprint(inorder(root))"),
                _checks([r"inorder\(node\.left\)",r"\[node\.val\]",r"inorder\(node\.right\)"]),
                ["Left first, then root, then right.","Recursively visit each subtree.","In-order of BST is sorted."],
                _success("🚶 Tree dark · ❌ Can't see","🚶 Tree walked · ✅ All visited","Every node has been visited in order!","Tree Traversal — in-order, pre-order, post-order.","Three orders, three stories.",25)),
            _level("t-3","The Search","🔍",3,"bst-search","Finding","data-structures.tree","data-structures.tree",
                _story("Tree Grove — Library","Searcher Sam","Find a book in the library. The library is organized as a BST — left is smaller, right is larger."),
                _tutor("Byte","🧭","BST search: if target < node.val, go left. If target > node.val, go right. If equal, found.","O(log n) in a balanced tree."),
                _discover("BST: 5 → (3, 8). Search for 3. Path?","search-path","Path","5 → 3"),
                _understand("O(log n) in a balanced tree."),
                _manipulate("bst-search","Go left or right","node = node.left if val < node.val else node.right"),
                _code("Search for a value in a BST.","class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n","def search(node, val):\n    while node:\n        if val == node.val: return True\n        node = node.left if val < node.val else node.right\n    return False\nroot = TreeNode(5)\nroot.left = TreeNode(3)\nroot.right = TreeNode(8)\nprint(search(root, 3))"),
                _checks([r"while\s+node",r"node\s*=\s*node\.(left|right)",r"return\s+(True|False)"]),
                ["Compare with current node.","Go left if smaller, right if larger.","Stop when found or leaf reached."],
                _success("🔍 Book lost · ❌ Not found","🔍 Book found · ✅ In library","The book is found in the BST!","BST Search — O(log n) lookup.","Left < root < right.",30)),
        ]),
        _make_town("advanced", "Advanced Tree", "🌲", "Advanced tree operations.", 2, "Advanced", ["data-structures.tree.advanced"], ["height", "balanced", "trie"], [
            _level("t-4","The Height","📏",4,"tree-height","Measuring","data-structures.tree.advanced","data-structures.tree.advanced",
                _story("Tree Grove — Summit","Measurer Maya","How tall is the tree? The height is the longest path from root to leaf."),
                _tutor("Byte","🧭","Height = max(left_height, right_height) + 1. A leaf has height 0.","An empty tree has height -1."),
                _discover("Tree: root 5, left 3, right 8. Height?","tree-height","Height","1"),
                _understand("An empty tree has height -1."),
                _manipulate("measure-height","Max of left and right + 1","max(left, right) + 1"),
                _code("Calculate the height of a binary tree.","class TreeNode:\n    def __init__(self, val, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n","def height(node):\n    if not node: return -1\n    return max(height(node.left), height(node.right)) + 1\nroot = TreeNode(5, TreeNode(3), TreeNode(8))\nprint(height(root))"),
                _checks([r"max\(height\(node\.left\),\s*height\(node\.right\)\)",r"return\s*-1"]),
                ["Leaf has height 0.","Height = max(left, right) + 1.","Empty tree has height -1."],
                _success("📏 Height unknown · ❌ Not measured","📏 Height measured · ✅ Tree sized","The tree height is calculated correctly!","Tree Height — longest path to leaf.","max(left, right) + 1.",30)),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 9: Heap Mountain (heap)
# ═══════════════════════════════════════════════════════════════
WORLD_HEAP = World(
    id="heap", name="Heap Mountain", subtitle="Priority at the Peak",
    description="Learn heaps — trees where the root is always the minimum or maximum.",
    icon="⛰️", order=9, theme="heap", recommended_roles=["developer", "data-engineer"], prerequisites=["tree"],
    towns=[
        _make_town("min-heap", "Min Peak", "⬇️", "The smallest element is always at the root.", 1, "Min-Heap", ["data-structures.heap"], ["heap", "heapify", "priority"], [
            _level("h-1","The Peak","⬇️",1,"min-heap","Root Min","data-structures.heap","data-structures.heap",
                _story("Heap Mountain — Base","Heap Keeper Hana","The peak always holds the smallest value. Build a min-heap."),
                _tutor("Byte","🧭","In a min-heap, parent <= children. The smallest element is at the root.","Insert: append, then bubble up. Extract min: replace root with last, then bubble down."),
                _discover("Heap: [1, 3, 2, 5, 4]. What is at the root?","root-min","Root value","1"),
                _understand("Insert: append, then bubble up. Extract min: replace root with last, then bubble down."),
                _manipulate("heap-bubble","Bubble up after insert","while i > 0 and heap[(i-1)//2] > heap[i]: swap"),
                _code("Implement heap push and pop using a list.","heap = []\n","def push(val):\n    heap.append(val)\n    i = len(heap) - 1\n    while i > 0 and heap[(i-1)//2] > heap[i]:\n        heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]\n        i = (i-1)//2\ndef pop():\n    val = heap[0]\n    last = heap.pop()\n    if heap:\n        heap[0] = last\n        # bubble down\n    return val"),
                _checks([r"while\s+i\s*>\s*0",r"heap\[\(i-1\)//2\]",r"heap\[i\]\s*="]),
                ["Parent index = (i-1)//2.","Bubble up while parent > child.","Root is always the minimum."],
                _success("⬇️ Peak unknown · ❌ No min","⬇️ Peak clear · ✅ Min at root","The min-heap property is maintained!","Min-Heap — smallest at the root.","Bubble up, bubble down.",30)),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 10: Graph Realm (graph)
# ═══════════════════════════════════════════════════════════════
WORLD_GRAPH = World(
    id="graph", name="Graph Realm", subtitle="Nodes and Edges",
    description="Explore graphs — networks of connected nodes. BFS, DFS, shortest paths.",
    icon="🕸️", order=10, theme="graph", recommended_roles=["developer", "data-engineer", "ai-engineer"], prerequisites=["tree"],
    towns=[
        _make_town("traversal", "Graph Walk", "🚶", "Visit every node. BFS and DFS are your tools.", 1, "Traversal", ["data-structures.graph"], ["bfs", "dfs"], [
            _level("g-1","The Maze","🌀",1,"bfs","Breadth","data-structures.graph","data-structures.graph",
                _story("Graph Realm — Entrance","Maze Runner Ray","Find the shortest path through a maze. BFS explores level by level."),
                _tutor("Byte","🧭","BFS uses a queue. Visit all neighbors of a node before moving deeper. DFS uses a stack (or recursion).","BFS guarantees shortest path in unweighted graphs."),
                _discover("Maze: start → A → B → End. BFS finds shortest path?","shortest-path","Path length","2"),
                _understand("BFS guarantees shortest path in unweighted graphs."),
                _manipulate("bfs-queue","Queue for BFS","from collections import deque"),
                _code("Find shortest path in a maze using BFS.","from collections import deque\nmaze = [[0,0,0],[1,1,0],[0,0,0]]\n","def shortest_path(maze):\n    rows, cols = len(maze), len(maze[0])\n    queue = deque([(0, 0, 0)])\n    visited = set()\n    while queue:\n        r, c, d = queue.popleft()\n        if r == rows-1 and c == cols-1: return d\n        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:\n            nr, nc = r+dr, c+dc\n            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr,nc) not in visited:\n                visited.add((nr,nc))\n                queue.append((nr,nc,d+1))\n    return -1\nprint(shortest_path(maze))"),
                _checks([r"deque\(\)",r"queue\.popleft\(\)",r"visited\.add"]),
                ["BFS explores level by level.","Queue ensures shortest path first.","Mark visited to avoid cycles."],
                _success("🌀 Maze dark · ❌ Lost","🌀 Maze solved · ✅ Shortest path found","The shortest path through the maze is found!","BFS — breadth-first search.","Level by level, shortest first.",30)),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 11: Dynamic Programming Valley (dp)
# ═══════════════════════════════════════════════════════════════
WORLD_DP = World(
    id="dp", name="DP Valley", subtitle="Optimal Substructure",
    description="Master dynamic programming — break problems into overlapping subproblems.",
    icon="🧮", order=11, theme="dp", recommended_roles=["developer", "ai-engineer"], prerequisites=["recursion", "stack"],
    towns=[
        _make_town("fib", "Fibonacci Falls", "💧", "The classic DP example: overlapping subproblems.", 1, "Classic DP", ["algorithms.dp"], ["memoization", "fibonacci", "bottom-up"], [
            _level("dp-1","The Overflow","💥",1,"memoization","Caching","algorithms.dp","algorithms.dp",
                _story("DP Valley — Waterfall","Memo Master Maya","Fibonacci without memoization recalculates the same values over and over. Cache them."),
                _tutor("Byte","🧭","Memoization stores results of expensive function calls. Next time the same input occurs, return the cached result.","Top-down with memo = DP. Bottom-up with table = DP."),
                _discover("fib(5) calls fib(4) and fib(3). fib(4) calls fib(3) again. Overlap!","overlap-count","Overlapping calls","fib(3) called twice"),
                _understand("Top-down with memo = DP. Bottom-up with table = DP."),
                _manipulate("memo-cache","Store computed results","memo = {}"),
                _code("Implement Fibonacci with memoization.","def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)\n","def fib_memo(n, memo={}):\n    if n in memo: return memo[n]\n    if n <= 1: return n\n    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)\n    return memo[n]\nprint(fib_memo(35))"),
                _checks([r"if\s+n\s+in\s+memo",r"memo\[n\]\s*=",r"return\s+memo\[n\]"]),
                ["Store results in a dict.","Check dict before computing.","Reuse cached results."],
                _success("💥 Recursive explosion · ❌ Exponential","💥 Explosion contained · ✅ O(n)","Fibonacci is now computed in O(n) time!","Memoization — caching subproblem results.","Top-down DP with memo.",30)),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# Global registry
# ═══════════════════════════════════════════════════════════════
WORLD_REGISTRY: dict[str, World] = {
    "foundations": WORLD_FOUNDATIONS,
    "searchlands": WORLD_SEARCHLANDS,
    "sorting": WORLD_SORTING,
    "recursion": WORLD_RECURSION,
    "linked": WORLD_LINKED,
    "stack": WORLD_STACK,
    "linked-advanced": WORLD_LINKED_ADV,
    "stack-advanced": WORLD_STACK_ADV,
    "queue": WORLD_QUEUE,
    "tree": WORLD_TREE,
    "heap": WORLD_HEAP,
    "graph": WORLD_GRAPH,
    "dp": WORLD_DP,
}

# Foundations (variables, naming, expressions) serves every engineering role,
# not just SDE — broaden its role relevance so non-SDE targeted users get
# real role-based ordering in worlds.py instead of a cosmetic sort.
_FOUNDATION_ROLES = "sde developer data-analyst ai-engineer devops-engineer qa-engineer"
for _town in WORLD_FOUNDATIONS.towns or []:
    for _lvl in _town.levels or []:
        _lvl.role_relevance = _FOUNDATION_ROLES
        _lvl.company_relevance = _SERVICE_COMPANIES
del _town, _lvl
from app.models.world import (
    Boss, BreakStep, Build, Checks, Code, Debug, Discover, Level,
    Manipulate, Predict, Retrieval, Story, Success, Town, Transfer,
    Tutor, World, Reward,
)


