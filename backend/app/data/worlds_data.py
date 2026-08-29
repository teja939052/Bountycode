"""World data for all 12 BountyCode worlds."""

from app.models.world import (
    Boss, BreakStep, Build, Code, Debug, Discover, Level, Manipulate,
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


def _success(world_before, world_after, world_reaction, reward_text, byte_line, xp):
    return Success(world_before=world_before, world_after=world_after, world_reaction=world_reaction, reward_text=reward_text, byte_line=byte_line, xp=xp)


def _boss_success(world_before, world_after, world_reaction, reward_text, byte_line, xp):
    return _success(world_before, world_after, world_reaction, reward_text, byte_line, xp)


def _reward(xp=0, coins=0, badges=None, unlocks_town=None, unlocks_world=None, title=None):
    return Reward(xp=xp, coins=coins, badges=badges or [], unlocks_town=unlocks_town, unlocks_world=unlocks_world, title=title)


def _level(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, manipulate, code, checks, hints, success, predict=None, build=None, break_step=None, debug=None, retrieval=None, transfer=None, mastery_threshold=None, estimated_minutes=None, unlocks=None):
    return Level(id=id, title=title, kind="level", icon=icon, order=order, concept=concept, mental_model=mental_model, canonical_skill=canonical_skill, maps_to_competency=maps_to, story=story, tutor=tutor, discover=discover, manipulate=manipulate, predict=predict, build=build, break_step=break_step, debug=debug, code=code, checks=checks, hints=hints, retrieval=retrieval, transfer=transfer, mastery_threshold=mastery_threshold, estimated_minutes=estimated_minutes, success=success, unlocks=unlocks)


def _boss(id, title, icon, order, concept, mental_model, canonical_skill, maps_to, story, tutor, discover, manipulate, code, checks, hints, success, reward, predict=None, build=None, break_step=None, debug=None, retrieval=None, transfer=None, mastery_threshold=80, estimated_minutes=None, unlocks=None):
    return Boss(id=id, title=title, kind="boss", icon=icon, order=order, concept=concept, mental_model=mental_model, canonical_skill=canonical_skill, maps_to_competency=maps_to, story=story, tutor=tutor, discover=discover, manipulate=manipulate, predict=predict, build=build, break_step=break_step, debug=debug, code=code, checks=checks, hints=hints, retrieval=retrieval, transfer=transfer, mastery_threshold=mastery_threshold, estimated_minutes=estimated_minutes, success=success, reward=reward, unlocks=unlocks)


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
                _manipulate("memory-box","apples = ?","apples = 5",hint="Give the box the name apples and put 5 inside."),
                _code("Label the box: create a variable called apples with the value 5.","# Give the box a name\n","apples = 5"),
                _checks([r"^\s*apples\s*=\s*5\s*(#.*)?$"]),
                ["What information does the robot need to remember here?","Programs can give a name to information so they can use it later — like labeling a box.","Try giving the number 5 the name `apples`.","Reveal: apples = 5 — the box needs this label to be remembered."],
                _success("📦 ??? · 📋 Empty ledger","📦 5 apples · 📋 ✓ Inventory recorded","The crate now glows: 🍎 Apples: 5 — the villagers cheer!","Variable Mastery — you can make programs remember things.","Your program remembered something. That is what variables do.",20)),
            _level("level-2","The Label","🏷️",2,"variables","Naming","coding.variables","coding.variables",
                _story("Village Store","Mira the Keeper","One box is not enough. We also have 3 loaves of bread. Remember both — then show me what is inside!"),
                _tutor("Byte","🧭","Each piece of information gets its own box. And print() lets you look inside.","Two variables, two boxes. print() is how you ask: what is inside this box right now?"),
                _discover("Two crates: 🍎 5 and 🍞 3. Tap each to label.","pair-labels","Label them: apples and bread","apples = 5; bread = 3"),
                _manipulate("memory-boxes","apples = 5 / bread = ?","apples = 5\nbread = 3\nprint(apples)",blocks=["apples","=","5","bread","=","3","print","(",")"]),
                _code("Create apples = 5 and bread = 3, then print the apples.","# Two boxes, then look inside\n","apples = 5\nbread = 3\nprint(apples)"),
                _checks([r"apples\s*=\s*5",r"bread\s*=\s*3",r"print\s*\(\s*apples\s*\)"]),
                ["What second fact does the shop need besides apples? How would you look inside a box?","Each fact gets its own labeled box. print() asks what is inside this one?","Try creating a second variable for bread, then print(apples).","Reveal:\napples = 5\nbread = 3\nprint(apples)"],
                _success("🧺 🍎 ? · 🍞 ? · 📋 1/2 recorded","🧺 🍎 5 · 🍞 3 · 📋 ✓ Both recorded","The store inventory board updates: Apples 5 · Bread 3 — it works!","State Sense — programs hold many facts at once.","Two boxes, two facts. That is state.",25)),
            _level("level-3","The Change","🔄",3,"reassignment","Changing","coding.variables","coding.variables",
                _story("Village Store — Delivery Day","Mira the Keeper","A delivery arrived! The apple crate should now hold the new stock. Can you update what the program remembers?"),
                _tutor("Byte","🧭","Variables can change. Assigning again replaces what is inside the box.","apples = 10 does not mean apples equals 10 — it means now put 10 in the box called apples. The old value is gone."),
                _discover("Crate 🍎 changes from 5 → 10 when you update.","slider","The stock changed from 5 to 10. How does the box update?","apples = 5; apples = 10"),
                _manipulate("slider-box","apples = 5\napples = ?","apples = 10"),
                _code("First set apples = 5, then update it to 10, then print it.","# Start at 5, then update\n","apples = 5\napples = 10\nprint(apples)"),
                _checks([r"apples\s*=\s*5",r"apples\s*=\s*10",r"print\s*\(\s*apples\s*\)"]),
                ["What changed in the stockroom? What should the box hold now?","A variable is a label — you can put a new value in the same box.","Keep the first line apples = 5, then put 10 in the same box on the next line.","Reveal:\napples = 5\napples = 10\nprint(apples)"],
                _success("📦 5 apples · 🧾 Ledger says 5","📦 10 apples · 🧾 Ledger says 10","The crate count ticks 5 → 10. The ledger is correct!","Mutation — you can change what the program remembers.","You did not create a new box — you changed the one you had.",25)),
            _level("level-4","The Many","🧺",4,"multiple-variables","Organizing","coding.variables","coding.variables",
                _story("Village Market","Old Tomas","I track apples, bread, AND coins. Three facts, three boxes. Can you set them all up?"),
                _tutor("Byte","🧭","State is just everything the program remembers right now. More variables = richer state.","Three variables in a row — the program now remembers three things at once."),
                _discover("Three stalls: 🍎 🍞 🪙 — each needs a label.","match","Match: apples→5, bread→3, coins→20","apples = 5; bread = 3; coins = 20"),
                _manipulate("three-boxes",blocks=["apples","bread","coins","=","5","3","20"],answer="apples = 5\nbread = 3\ncoins = 20"),
                _code("Create three variables: apples = 5, bread = 3, coins = 20.","# Three facts\n","apples = 5\nbread = 3\ncoins = 20"),
                _checks([r"apples\s*=\s*5",r"bread\s*=\s*3",r"coins\s*=\s*20"]),
                ["How many different facts does Tomas need to track?","State = everything the program remembers right now. Each fact needs its own name.","Try three labeled boxes: one for apples, one for bread, one for coins.","Reveal:\napples = 5\nbread = 3\ncoins = 20"],
                _success("🏪 3 stalls · 📋 Empty","🏪 🍎 5 · 🍞 3 · 🪙 20 · 📋 ✓ All recorded","Three stalls light up. The market ledger is complete!","State Keeper — you hold a whole world in variables.","That is state: everything remembered, organized.",25)),
            _level("level-5","The Echo","📣",5,"expressions","Using","coding.variables","coding.variables",
                _story("Village Square — Announcement","Mira the Keeper","The elders want the total items! Apples plus bread — make the program figure it out and announce it."),
                _tutor("Byte","🧭","Variables are not just storage — you can compute with them. apples + bread is an expression.","total = apples + bread stores the result of the computation. Then print(total) shows it."),
                _discover("🍎 5 + 🍞 3 = ? — drag + to combine.","expression","Compute: total = apples + bread","total = apples + bread"),
                _manipulate("expression-box","total = apples + bread","total = apples + bread"),
                _code("Set apples = 5, bread = 3, compute total = apples + bread, then print(total).","# Compute the total\n","apples = 5\nbread = 3\ntotal = apples + bread\nprint(total)"),
                _checks([r"apples\s*=\s*5",r"bread\s*=\s*3",r"total\s*=\s*apples\s*\+\s*bread",r"print\s*\(\s*total\s*\)"]),
                ["How would the crier announce the total without counting by hand?","You can compute with names, not just numbers — try combining the two boxes.","Try making a new box that holds the result of apples + bread, then announce it.","Reveal:\napples = 5\nbread = 3\ntotal = apples + bread\nprint(total)"],
                _success("📢 Elders waiting · 🧮 No total yet","📢 Announced: 8 items! · 🧮 total = 8","The town crier announces: 8 items in total! — you computed the answer.","Expression Craft — you make programs calculate.","You used remembered facts to make something new.",30)),
            _boss("boss-1","The Broken Inventory","🐉",6,"boss-variables-state","Transfer","coding.variables","coding.variables",
                _story("Supply Hut — Emergency","Mira the Keeper","The inventory system has stopped remembering its stock. The stockroom has apples, bread and coins — 12, 4 and 30 — but the program remembers nothing. The elders need the total items (apples + bread) announced. Repair it!"),
                _tutor("Byte","🧭","Combine everything: remember, update, compute, announce.","This is transfer: a new situation, same ideas. If you can do this, you truly understand Remembering → Naming → Using."),
                _discover("Scrambled ledger: ??? ??? ??? — rebuild from stockroom count.","boss-fix","Stockroom: 12 apples, 4 bread, 30 coins. Total = apples + bread. Repair the ledger.","apples = 12; bread = 4; coins = 30; total = apples + bread; print(total)"),
                _manipulate("boss-ledger","Remember 3 stocks + announce total","apples = 12; bread = 4; coins = 30; total = apples + bread; print(total)"),
                _code("Repair the inventory: make the program remember the stockroom (12 apples, 4 bread, 30 coins) and announce the total items (apples + bread).","# Repair the scrambled ledger\n# Stockroom: 12 apples, 4 bread, 30 coins\n","apples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)"),
                _checks([r"apples\s*=\s*12",r"bread\s*=\s*4",r"coins\s*=\s*30",r"total\s*=\s*apples\s*\+\s*bread",r"print\s*\(\s*total\s*\)"]),
                ["What facts does the stockroom need the program to hold? What does the elder want announced?","You learned Remembering, Naming, Organizing, Using — which ones does this emergency need?","Try three remembered facts for the stock, then compute the total and announce it.","Reveal:\napples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)"],
                _success("🏚️ Ledger broken · 📦 ??? · 🔇 Silent","🏚️ → 🏘️ Restored · 📦 12/4/30 · 📢 16 announced · 🌿 Path opens","The hut restores! Ledgers glow, crates align. The village is saved — the path to the next town opens. 🌿","🏆 Village Restored — Remembering → Using MASTERED. Next: Kinds of Things!","You did not copy — you transferred. That is mastery.",50),
                _reward(xp=50,coins=25,badges=["variables-master"],unlocks_town="town-2-types")),
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
                _manipulate("check-list","Check position ?","Check each position from 1 to 7 until you find the star.",hint="Start at position 1 and go up."),
                _code("Write code to find the golden star in the list.","cards = [0,0,0,1,0,0,0]\n","target = 1\nfor i in range(len(cards)):\n    if cards[i] == target:\n        print(i)"),
                _checks([r"for\s",r"range\s*\(",r"if\s*cards"]),
                ["Where do you start looking?","You check each one in order. No skipping!","Try a loop that goes from the first to the last."],
                _success("🚪 Gate closed · 🔍 No one checked","🚪 Gate open · ✅ Ticket found","The guard smiles — you found the golden ticket!","Linear Search — you check every item until you find it.","Start at the beginning. That is how search works.",20)),
            _level("s-2","The Counter","🔢",2,"counting","Measuring","searching.linear","searching.linear",
                _story("Searchlands Market","Merchant Mia","How many customers bought apples today? Count them all — one by one."),
                _tutor("Byte","🧭","A counter adds up how many times something happens. It is like tally marks.","Every time you find what you are looking for, you add 1 to your counter."),
                _discover("A receipt with 8 items. Count how many are apples.","tally","How many apples on this receipt?","count = 3"),
                _manipulate("tally-counter","count = 0\nfor item in items:\n    if item == apple: count += 1","count = 3"),
                _code("Count how many apples appear in the list.","items = ['apple','banana','apple','orange','apple']\n","count = 0\nfor item in items:\n    if item == apple:\n        count += 1\nprint(count)"),
                _checks([r"count\s*=\s*0",r"for\s",r"if\s*item\s*=="]),
                ["What do you start the counter at?","Every time you find an apple, add 1.","Try initializing count = 0 first."],
                _success("📝 Empty tally · 📊 0 counted","📝 Tally full · 📊 3 apples","The merchant's ledger is updated!","Counting — tallying how many match.","Every match adds one to the count.",20)),
            _level("s-3","The Worst Case","😰",3,"complexity","Understanding","searching.linear","searching.linear",
                _story("Searchlands Library","Librarian Leo","What if the book you want is the very last one? Or not here at all?"),
                _tutor("Byte","🧭","Linear search takes time proportional to the list size. That is O(n).","If the list has 1000 items, you might check all 1000. That is the worst case."),
                _discover("A shelf of 100 books. The target is book #100.","worst-case","How many checks in the worst case?","100"),
                _manipulate("complexity-box","Worst case for n items = ?","n"),
                _code("Explain: what is the worst case for linear search on n items?","# Write your explanation\n","# Worst case: check all n items\n# Best case: find at index 0\n# So worst case = n checks"),
                _checks([r"n\s*items",r"all\s*n",r"n\s*checks"]),
                ["What if the item is at the very end?","What if it is not in the list at all?","Both cases require checking every single item."],
                _success("📚 Shelf empty · ⏱️ Unknown","📚 Shelf searched · ⏱️ n checks","The library log records: worst case = n.","Complexity — understanding how long search takes.","Time grows with the list. That is O(n).",25)),
            _boss("s-boss","The Lost Scroll","📜",4,"search-master","Applying","searching.linear","searching.linear",
                _story("Searchlands Archive","Archivist Ana","A ancient scroll is hidden in a vault of 500 scrolls. Find it before the temple collapses!"),
                _tutor("Byte","🧭","Linear search is your first tool. Check every scroll, but be smart about it.","Even a slow search beats no search. But can you do better?"),
                _discover("500 scrolls in a vault. One has the ancient symbol. Find it.","vault-search","Find the scroll with the ancient symbol.","index = 247"),
                _manipulate("scroll-find","Search scrolls for the ancient symbol","found at index"),
                _code("Search through the scrolls for the ancient symbol.","scrolls = [0]*500\nscrolls[247] = 1\n","target = 1\nfor i in range(len(scrolls)):\n    if scrolls[i] == target:\n        print(f'Found at {i}')\n        break"),
                _checks([r"for\s",r"range\s*\(",r"break"]),
                ["Start from the first scroll.","You can stop as soon as you find it — no need to check the rest.","Use break to stop early."],
                _success("🏛️ Vault sealed · 📜 Missing","🏛️ Vault open · 📜 Found","The ancient scroll is recovered! The temple is saved.","Search Mastery — you can find anything by looking.","Every search starts with a line.",40),
                _reward(xp=40,coins=20,badges=["search-novice"],unlocks_town="town-2-binary")),
        ]),
        _make_town("binary", "Binary Search Borough", "🏘️", "Divide and conquer. Cut the search space in half each time.", 2, "Divide and Conquer", ["searching.binary"], ["binary-search", "logarithmic", "sorted"], [
            _level("b-1","The Sorted Shelf","📚",1,"binary search","Halving","searching.binary","searching.binary",
                _story("Binary Borough Library","Librarian Zoe","Books are sorted by title. Find Dragon without checking every shelf."),
                _tutor("Byte","🧭","When things are sorted, you can cut the search in half each time.","Open the middle. If your target is smaller, go left. If bigger, go right. Repeat."),
                _discover("A sorted shelf of 8 books. Find Dragon by checking the middle.","binary-flip","Which book do you check first?","middle = 4"),
                _manipulate("mid-point","Check position ?","middle = (low + high) // 2"),
                _code("Find the target using binary search on a sorted list.","books = ['Ant','Bear','Cat','Dragon','Eagle','Fox','Goat','Hawk']\n","target = 'Dragon'\nlo, hi = 0, len(books)-1\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if books[mid] == target: print(mid); break\n    elif books[mid] < target: lo = mid+1\n    else: hi = mid-1"),
                _checks([r"while\s+lo",r"mid\s*=\s*\(lo\s*\+\s*hi\)",r"books\[mid\]"]),
                ["The books are sorted — use that!","Check the middle first.","If target is bigger, discard the left half."],
                _success("📚 Full shelf · 🔍 Slow scan","📚 Sorted shelf · ⚡ Found at mid","The librarian is amazed — you found it in 2 checks!","Binary Search — halve the problem each time.","Sorted data unlocks speed.",25)),
            _level("b-2","The Guess Game","🎯",2,"logarithmic","Estimating","searching.binary","searching.binary",
                _story("Binary Borough Square","Game Master Gus","Guess a number from 1 to 100 in as few tries as possible."),
                _tutor("Byte","🧭","Each guess eliminates half the possibilities. That is O(log n)!","With 100 numbers, you need at most 7 guesses. With 1000, only 10."),
                _discover("A number from 1 to 100 is hidden. Guess with feedback too high or too low.","guess-game","What is the maximum number of guesses needed?","7"),
                _manipulate("guess-range","Guess ? (too high / too low)","narrow the range"),
                _code("Implement a number guessing game with binary search logic.","# Pick a number 1-100\n","import random\ntarget = random.randint(1,100)\nlo, hi = 1, 100\nwhile lo <= hi:\n    guess = (lo+hi)//2\n    # feedback would guide lo/hi"),
                _checks([r"lo\s*=\s*guess\s*\+\s*1",r"hi\s*=\s*guess\s*-\s*1"]),
                ["Each guess cuts possibilities in half.","100 numbers → max 7 guesses.","1000 numbers → max 10 guesses."],
                _success("🎯 Range unknown · 🤔 Blind guessing","🎯 Range narrowed · ✅ Found in log steps","The crowd cheers — binary guessing is lightning fast!","Logarithmic thinking — O(log n) speed.","Half the possibilities each time.",25)),
            _level("b-3","The Edge Cases","⚠️",3,"boundary conditions","Precision","searching.binary","searching.binary",
                _story("Binary Borough Edge","Inspector Ivy","What happens when the list has 1 item? Or the target is not there?"),
                _tutor("Byte","🧭","Edge cases matter. Empty lists, single items, missing targets — handle them all.","The loop condition `lo <= hi` ensures you do not miss anything."),
                _discover("A list of 1 item. Is it the target?","edge-case","What does your code do with 1 item?","yes"),
                _manipulate("edge-check","What if lo > hi?","target not found"),
                _code("Handle edge cases in binary search.","# Empty list, single item, missing\n","def search(nums, target):\n    lo, hi = 0, len(nums)-1\n    while lo <= hi:\n        mid = (lo+hi)//2\n        if nums[mid] == target: return mid\n        elif nums[mid] < target: lo = mid+1\n        else: hi = mid-1\n    return -1"),
                _checks([r"return\s*-1",r"len\(nums\)",r"lo\s*<=\s*hi"]),
                ["What if the list is empty?","What if the target is not in the list?","Return -1 when lo > hi."],
                _success("⚠️ Edge ignored · 💥 Crash","⚠️ Edge handled · ✅ Robust","All edge cases covered. The search is bulletproof.","Edge handling — every case matters.","Robust code handles all inputs.",30)),
            _boss("b-boss","The Missing Page","📖",4,"search-legend","Mastering","searching.binary","searching.binary",
                _story("Binary Borough Archive","Keeper Kai","A critical page is missing from the ancient tome. Find where it should be in the sorted index."),
                _tutor("Byte","🧭","When the target is not there, binary search tells you where it should be. That is insertion position.","This is the foundation of many real-world systems."),
                _discover("A sorted index of 16 pages. Find where page 9 should be inserted.","insert-position","Where does page 9 go?","position = 8"),
                _manipulate("insert-find","Find insertion position for 9","lower_bound"),
                _code("Find the insertion position for a missing target.","pages = list(range(1,17))\n","target = 9\nlo, hi = 0, len(pages)\nwhile lo < hi:\n    mid = (lo+hi)//2\n    if pages[mid] < target: lo = mid+1\n    else: hi = mid\nprint(lo)"),
                _checks([r"lo\s*=\s*lo\s*\+\s*1",r"pages\[mid\]\s*<\s*target"]),
                ["When target is not found, lo is the insertion point.","Use `lo < hi` instead of `lo <= hi`.","This finds the lower bound."],
                _success("📖 Page missing · 🔍 Lost","📖 Position found · ✅ Inserted","The tome is complete! The archive is restored.","Search Legend — you master binary search.","Finding where things belong is as powerful as finding them.",45),
                _reward(xp=45,coins=25,badges=["search-legend"],unlocks_town="town-3-sorting")),
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
                _manipulate("swap-adj","If bar[i] > bar[i+1], swap","pass through the list"),
                _code("Implement bubble sort to arrange bars from shortest to longest.","bars = [5,3,1,4,2]\n","n = len(bars)\nfor i in range(n):\n    for j in range(0, n-i-1):\n        if bars[j] > bars[j+1]:\n            bars[j], bars[j+1] = bars[j+1], bars[j]\nprint(bars)"),
                _checks([r"for\s+in\s*range",r"if\s*bars\[j\]",r"bars\[j\],\s*bars\[j\+1\]"]),
                ["Compare each pair of neighbors.","Swap if the left one is bigger.","Repeat until no swaps needed."],
                _success("🔥 Bars jumbled · ⚒️ Unsorted","🔥 Bars arranged · ✅ Sorted","The forge glows — bars are now in order!","Bubble Sort — swap neighbors until sorted.","Each pass places the largest in place.",20)),
            _level("so-2","The Optimization","⚡",2,"optimized bubble","Early Stop","sorting.bubble","sorting.bubble",
                _story("Sorting Forge — Second Chamber","Forge Master Finn","What if the bars are already sorted? Do not waste passes!"),
                _tutor("Byte","🧭","If no swaps happen in a pass, the list is already sorted. Stop early!","This optimization makes bubble sort O(n) for nearly-sorted data."),
                _discover("Bars are already sorted: [1,2,3,4,5]. Can you stop after the first pass?","early-stop","How do you know to stop?","no swaps"),
                _manipulate("early-exit","If no swaps, break","swapped = False"),
                _code("Add early stopping to bubble sort.","bars = [1,2,3,4,5]\n","swapped = False\nfor i in range(n):\n    if not swapped: break\n    swapped = False\n    for j in range(0, n-i-1):\n        if bars[j] > bars[j+1]:\n            bars[j], bars[j+1] = bars[j+1], bars[j]\n            swapped = True"),
                _checks([r"swapped\s*=\s*False",r"if\s*not\s*swapped",r"break"]),
                ["If no swaps happen, the list is sorted.","Add a flag to track swaps.","Break out of the outer loop."],
                _success("⚡ Unnecessary passes · 🐢 Slow","⚡ Early exit · 🚀 Fast","The forge saves energy — no wasted passes!","Optimized Bubble — stop when sorted.","Early termination saves time.",25)),
            _boss("so-boss","The Great Sort","🏆",3,"sort-master","Forging","sorting.bubble","sorting.bubble",
                _story("Sorting Forge — Final Chamber","Grand Forge Master","Sort 1000 bars for the kingdom's grand archive. Every bar must be in order!"),
                _tutor("Byte","🧭","Bubble sort is simple and reliable. For large data, it is slow but correct.","Sometimes the simplest approach is the most trustworthy."),
                _discover("1000 unsorted bars. Sort them all for the archive.","great-sort","All bars in ascending order.","sorted"),
                _manipulate("great-arrange","Sort all bars","bubble sort with early exit"),
                _code("Sort the full array for the grand archive.","bars = list(range(1000,0,-1))\n","n = len(bars)\nfor i in range(n):\n    swapped = False\n    for j in range(0, n-i-1):\n        if bars[j] > bars[j+1]:\n            bars[j], bars[j+1] = bars[j+1], bars[j]\n            swapped = True\n    if not swapped: break\nprint(bars[:10], '...', bars[-10:])"),
                _checks([r"swapped",r"break",r"bars\[j\]"]),
                ["The simple approach works for any size.","Early exit helps when nearly sorted.","Correctness matters more than speed."],
                _success("🏆 Bars scattered · 🔨 Chaos","🏆 Bars ordered · ✅ Archive complete","The grand archive is sorted! The kingdom celebrates.","Sort Mastery — you can order anything.","Simple, correct, reliable.",40),
                _reward(xp=40,coins=20,badges=["sort-forger"],unlocks_town="town-2-merge")),
        ]),
        _make_town("merge", "Merge Hall", "🔗", "Divide, sort, merge. The elegant recursive approach.", 2, "Divide and Conquer", ["sorting.merge"], ["merge-sort", "recursion", "merging"], [
            _level("m-1","The Split","✂️",1,"merge sort","Dividing","sorting.merge","sorting.merge",
                _story("Merge Hall — Entry","Merge Master Mira","To merge, you must first split. Cut the list in half, then half again."),
                _tutor("Byte","🧭","Merge sort divides the list in half, sorts each half, then merges them back.","Like sorting a deck of cards — split, sort each hand, then merge."),
                _discover("A list of 8 numbers. Split it in half repeatedly until single elements.","split-list","How many splits to get single elements?","3"),
                _manipulate("split-half","Split list at mid","left = arr[:mid]; right = arr[mid:]"),
                _code("Implement the split phase of merge sort.","arr = [8,3,1,7,0,5,2,6]\n","def merge_sort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr)//2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)"),
                _checks([r"len\(arr\)\s*<=\s*1",r"mid\s*=\s*len",r"arr\[:mid\]"]),
                ["Keep splitting until single elements.","A single element is already sorted.","The base case stops the recursion."],
                _success("✂️ List whole · 🔀 Unsplitted","✂️ Fully split · 🔀 Ready to merge","The list is split into single elements.","Split Phase — divide until trivial.","Every sort starts with a split.",25)),
            _level("m-2","The Merge","🤝",2,"merging","Combining","sorting.merge","sorting.merge",
                _story("Merge Hall — Center","Merge Master Mira","Now merge the sorted halves back together. Compare front elements."),
                _tutor("Byte","🧭","Merging two sorted lists is simple: compare the front of each, take the smaller.","Like merging two sorted decks — always pick the smaller top card."),
                _discover("Two sorted lists: [1,3,5] and [2,4,6]. Merge them into one.","merge-lists","Merged result","[1,2,3,4,5,6]"),
                _manipulate("merge-two","Compare fronts, take smaller","result = []"),
                _code("Merge two sorted lists into one sorted list.","left = [1,3,5]\nright = [2,4,6]\n","result = []\ni = j = 0\nwhile i < len(left) and j < len(right):\n    if left[i] <= right[j]:\n        result.append(left[i]); i += 1\n    else:\n        result.append(right[j]); j += 1\nresult.extend(left[i:])\nresult.extend(right[j:])\nprint(result)"),
                _checks([r"while\s+",r"append",r"extend"]),
                ["Compare the front of each list.","Take the smaller one.","Append the rest of the remaining list."],
                _success("🤝 Halves separate · 🔀 Unmerged","🤝 Fully merged · ✅ One sorted list","The two halves are one sorted list!","Merge — combining sorted lists efficiently.","Two sorted inputs → one sorted output.",25)),
            _boss("m-boss","The Grand Merge","👑",3,"merge-legend","Mastering","sorting.merge","sorting.merge",
                _story("Merge Hall — Throne Room","Arch-Merge Master","Sort the entire kingdom's census data using merge sort. Every record must be in order."),
                _tutor("Byte","🧭","Merge sort is O(n log n) — fast and stable. It is the gold standard of sorting.","Divide, sort, merge. Repeat until the whole list is ordered."),
                _discover("Census data of 1000 records. Sort by ID using merge sort.","census-sort","All records sorted by ID.","sorted"),
                _manipulate("grand-merge","Full merge sort implementation","O(n log n)"),
                _code("Implement complete merge sort for the census data.","data = [5,2,8,1,9,3,7,4,6,0]\n","def merge_sort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr)//2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\ndef merge(l,r):\n    res = []\n    i = j = 0\n    while i < len(l) and j < len(r):\n        if l[i] <= r[j]: res.append(l[i]); i += 1\n        else: res.append(r[j]); j += 1\n    res.extend(l[i:]); res.extend(r[j:])\n    return res\nprint(merge_sort(data))"),
                _checks([r"merge_sort",r"merge\s*\(",r"return\s*res"]),
                ["Divide recursively, then merge.","The merge step is the key.","O(n log n) — efficient for any size."],
                _success("👑 Data chaotic · 📊 Unsorted","👑 Data ordered · ✅ Census complete","The kingdom's census is perfectly sorted!","Merge Legend — O(n log n) elegance.","Divide, conquer, merge.",45),
                _reward(xp=45,coins=25,badges=["merge-master"],unlocks_town="town-3-recursion")),
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
                _manipulate("mirror-stop","When does recursion stop?","base case"),
                _code("Write a recursive function with a base case.","# Factorial: n! = n * (n-1)!\n","def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n-1)\nprint(factorial(5))"),
                _checks([r"if\s+n\s*<=\s*1",r"return\s*1",r"return\s+n\s*\*"]),
                ["The smallest case stops the recursion.","5! = 5 × 4!, 4! = 4 × 3!, ..., 1! = 1.","Each call works on a smaller input."],
                _success("🪞 Infinite mirrors · 💥 Stack overflow","🪞 Mirrors resolved · ✅ Base found","The reflection stops at the base case.","Recursion — solving big problems with small versions.","Every recursive journey needs a base case.",20)),
            _level("r-2","The Ladder","🪜",2,"call stack","Understanding","recursion.base","recursion.base",
                _story("Mountain Lodge","Lodge Keeper Leo","Each recursive call waits on a ladder. The last one called returns first."),
                _tutor("Byte","🧭","The call stack is like a ladder — each recursive call adds a rung. The base case is the top.","When the base case is reached, each call returns in reverse order."),
                _discover("A ladder with 5 rungs. Climb up recursively, then come back down.","ladder-climb","What order do you return?","5,4,3,2,1"),
                _manipulate("stack-ladder","Climb to rung ?","push then pop"),
                _code("Trace the call stack for a recursive function.","def countdown(n):\n    if n <= 0: return\n    print(n)\n    countdown(n-1)\n","countdown(5) prints 5,4,3,2,1"),
                _checks([r"countdown\(n-1\)",r"if\s+n\s*<=\s*0"]),
                ["Each call waits for the next one.","The deepest call returns first.","Stack: Last In, First Out."],
                _success("🪜 Ladder infinite · ⏳ Waiting","🪜 Ladder climbed · ✅ Returns in order","The lodge keeper understands the call stack perfectly.","Call Stack — understanding the execution order.","Last call returns first.",25)),
            _boss("r-boss","The Summit","🏔️",3,"recursion-master","Reaching","recursion.base","recursion.base",
                _story("Mountain Summit","Summit Sage","Reach the summit by solving progressively smaller problems. Each step is a recursive call."),
                _tutor("Byte","🧭","The summit is the base case. Every step down is a recursive call.","When you reach the top, you can trace your path back down."),
                _discover("Climb from base camp (0) to summit (10). Each step doubles your progress.","summit-climb","How many steps to reach 10?","4"),
                _manipulate("summit-path","Reach summit with recursive steps","steps = 0"),
                _code("Use recursion to compute a power of 2.","# 2^n using recursion\n","def power_of_2(n):\n    if n == 0: return 1\n    return 2 * power_of_2(n-1)\nprint(power_of_2(10))"),
                _checks([r"if\s+n\s*==\s*0",r"return\s*1",r"return\s*2\s*\*"]),
                ["Each step reduces the problem by 1.","2^10 = 2 × 2^9 = 2 × 2 × 2^8 ...","The base case is 2^0 = 1."],
                _success("🏔️ Base camp only · 🏔️ Not summited","🏔️ Summit reached · ✅ View from top","You see the entire recursive mountain from the top!","Recursion Master — you can climb any recursive problem.","Base case + recursive case = solution.",40),
                _reward(xp=40,coins=20,badges=["recursion-base"],unlocks_town="town-2-divide")),
        ]),
        _make_town("divide", "Divide Peak", "🏔️", "Recursive division. Break problems into independent sub-problems.", 2, "Divide and Conquer", ["recursion.divide"], ["divide-conquer", "recursive-structure", "combine"], [
            _level("d-1","The Split Path","🛤️",1,"divide and conquer","Splitting","recursion.divide","recursion.divide",
                _story("Divide Peak Trail","Trail Guide Dora","At each fork, the path splits into two. Follow both branches."),
                _tutor("Byte","🧭","Divide and conquer: split the problem, solve each part, combine the results.","Merge sort and binary search both use this pattern."),
                _discover("A path splits into two at each junction. How many paths after 3 splits?","path-split","Total paths","8"),
                _manipulate("path-count","Paths after n splits","2^n"),
                _code("Count paths in a divide-and-conquer tree.","# Binary tree of splits\n","def count_paths(depth):\n    if depth == 0: return 1\n    return 2 * count_paths(depth-1)\nprint(count_paths(3))"),
                _checks([r"if\s+depth\s*==\s*0",r"return\s*1",r"return\s*2\s*\*"]),
                ["Each split doubles the paths.","3 splits → 2³ = 8 paths.","The tree of recursive calls."],
                _success("🛤️ Single path · 🔀 No splits","🛤️ All paths explored · ✅ Counted","Every branch of the divide tree is traced.","Divide — splitting into sub-problems.","2^n paths after n splits.",25)),
            _level("d-2","The Combine","🔗",2,"combining results","Merging","recursion.divide","recursion.divide",
                _story("Divide Peak Summit","Summit Architect","The sub-problems are solved. Now combine their results into the final answer."),
                _tutor("Byte","🧭","The combine step is where the magic happens. Sorted halves become a sorted whole.","Without combining, you just have solved pieces, not the solution."),
                _discover("Two sorted results: [1,3,5] and [2,4,6]. Combine into one sorted result.","combine-results","Combined sorted","[1,2,3,4,5,6]"),
                _manipulate("combine-step","Merge two sorted results","two-pointer merge"),
                _code("Combine two sorted arrays into one.","left = [1,3,5]\nright = [2,4,6]\n","result = []\ni = j = 0\nwhile i < len(left) and j < len(right):\n    if left[i] <= right[j]:\n        result.append(left[i]); i += 1\n    else:\n        result.append(right[j]); j += 1\nresult.extend(left[i:])\nresult.extend(right[j:])\nprint(result)"),
                _checks([r"while\s+",r"append",r"extend"]),
                ["Compare elements from each half.","Take the smaller one.","Append remaining elements."],
                _success("🔗 Halves separate · ❌ Not combined","🔗 Fully combined · ✅ One result","The combined result is perfectly sorted!","Combine — merging sub-solutions.","The whole is greater than the sum of parts.",25)),
            _boss("d-boss","The Master Divide","👑",3,"divide-legend","Mastering","recursion.divide","recursion.divide",
                _story("Divide Peak Throne","Master Architect","Solve the master problem: given an array, return the sum of all elements using divide and conquer."),
                _tutor("Byte","🧭","The master divide: split the array in half, sum each half, add the two sums.","This is the essence of recursive problem solving."),
                _discover("Array of 16 numbers. Sum them using divide and conquer.","master-sum","Total sum","136"),
                _manipulate("master-split","Split and sum recursively","sum = left_sum + right_sum"),
                _code("Implement sum using divide and conquer.","arr = list(range(1,17))\n","def dc_sum(arr):\n    if len(arr) <= 1: return arr[0] if arr else 0\n    mid = len(arr)//2\n    return dc_sum(arr[:mid]) + dc_sum(arr[mid:])\nprint(dc_sum(list(range(1,17))))"),
                _checks([r"dc_sum",r"arr\[:mid\]",r"arr\[mid:\]"]),
                ["Base case: single element or empty.","Split and recurse on both halves.","Combine by adding the two sums."],
                _success("👑 Problem whole · ❌ Not divided","👑 Problem solved · ✅ Master of divide","The master problem is solved with pure divide and conquer!","Divide Legend — recursive problem mastery.","Split, solve, combine.",45),
                _reward(xp=45,coins=25,badges=["divide-master"],unlocks_town="town-3-trees")),
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
                _manipulate("link-nodes","Create node with value and next","Node(value, next)"),
                _code("Create a linked list with 3 nodes.","class Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None\n","head = Node('A')\nhead.next = Node('B')\nhead.next.next = Node('C')"),
                _checks([r"class\s+Node",r"self\.val",r"self\.next"]),
                ["Each node has a value and a next pointer.","The head is the first node.","The last node's next is None."],
                _success("⛓️ No chain · 🔗 Loose nodes","⛓️ Chain built · ✅ Linked","The pathway is connected from head to tail!","Linked List — chains of connected nodes.","Each node knows the next one.",20)),
            _level("l-2","The Traversal","🚶",2,"traversal","Following","data-structures.linked-list","data-structures.linked-list",
                _story("Linked Pathway — Middle","Path Walker Willow","Walk the chain from head to tail. Collect all the values along the way."),
                _tutor("Byte","🧭","Traversal follows the chain from head to tail, visiting each node exactly once.","Like reading a chain of clues — start at the beginning and follow each link."),
                _discover("Chain: A → B → C → D. Collect all values in order.","traverse-chain","Collected values","['A','B','C','D']"),
                _manipulate("walk-chain","Start at head, follow next","current = head"),
                _code("Traverse a linked list and collect all values.","head = Node('A')\nhead.next = Node('B')\n","vals = []\ncurrent = head\nwhile current:\n    vals.append(current.val)\n    current = current.next\nprint(vals)"),
                _checks([r"while\s+current",r"current\s*=\s*current\.next",r"vals\.append"]),
                ["Start at the head node.","Follow the next pointer.","Stop when current is None."],
                _success("🚶 Chain broken · ❌ Can't traverse","🚶 Full traversal · ✅ All values collected","Every node in the chain has been visited!","Traversal — following the chain.","O(n) time — visit each node once.",25)),
            _boss("l-boss","The Reversal","🔄",3,"linked-master","Reversing","data-structures.linked-list","data-structures.linked-list",
                _story("Linked Pathway — End","Path Master Piper","Reverse the chain so the tail becomes the head. Every pointer now goes backward."),
                _tutor("Byte","🧭","Reversing a linked list is a classic problem. Change each node's next pointer to point to the previous node.","Three pointers: previous, current, next. Walk through and flip."),
                _discover("Chain: A → B → C → D. Reverse it to D → C → B → A.","reverse-chain","Reversed chain","D → C → B → A"),
                _manipulate("flip-pointers","Reverse the chain","prev, curr, next"),
                _code("Reverse a linked list in-place.","head = Node('A')\nhead.next = Node('B')\n","prev = None\ncurrent = head\nwhile current:\n    next_node = current.next\n    current.next = prev\n    prev = current\n    current = next_node\nhead = prev"),
                _checks([r"prev\s*=\s*None",r"next_node",r"current\.next\s*=\s*prev"]),
                ["Three pointers: prev, current, next.","Flip each pointer to the previous node.","Move all three forward."],
                _success("🔄 Chain forward · ❌ Not reversed","🔄 Chain reversed · ✅ Tail is head","The chain now flows backward! The tail is the new head.","Linked Master — reverse any chain.","Pointer manipulation mastery.",40),
                _reward(xp=40,coins=20,badges=["linked-master"],unlocks_town="town-2-stack")),
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
                _manipulate("push-plate","Push plate ? onto stack","stack.append(plate)"),
                _code("Implement a stack using a list. Push and pop plates.","stack = []\n","stack.append(1)\nstack.append(2)\nstack.append(3)\nprint(stack.pop())  # 3\nprint(stack.pop())  # 2"),
                _checks([r"append",r"pop",r"stack\s*=\s*\[\]"]),
                ["Push adds to the top.","Pop removes from the top.","Last in, first out."],
                _success("🧱 No tower · 📦 Empty","🧱 Tower built · ✅ LIFO working","The tower works perfectly!","Stack — Last In, First Out.","Push and pop from the same end.",20)),
            _level("st-2","The Bracket Match","🔍",2,"matching","Validating","data-structures.stack","data-structures.stack",
                _story("Stack Tower — Middle Floor","Checker Cara","Match opening and closing brackets. Every opening bracket needs a closing one."),
                _tutor("Byte","🧭","Use a stack to check bracket matching. Push opening brackets, pop when you see closing.","If the stack is empty at the end, all brackets are matched."),
                _discover("String: ({[]}). Check if all brackets match.","bracket-check","Valid","True"),
                _manipulate("match-bracket","Push open, pop on close","stack"),
                _code("Check if brackets in a string are balanced.","s = '({[]})'\n","stack = []\nfor c in s:\n    if c in '({[': stack.append(c)\n    elif c in ')}]':\n        if not stack: print(False); break\n        stack.pop()\nprint(len(stack) == 0)"),
                _checks([r"append",r"pop",r"if\s+not\s+stack"]),
                ["Push opening brackets.","Pop when you see a closing bracket.","Stack must be empty at the end."],
                _success("🔍 Brackets unmatched · ❌ Invalid","🔍 Brackets matched · ✅ Valid","All brackets are perfectly matched!","Bracket Matching — stack validation.","Stacks are perfect for matching pairs.",25)),
            _boss("st-boss","The Function Call","📞",3,"stack-master","Calling","data-structures.stack","data-structures.stack",
                _story("Stack Tower — Top Floor","Call Master Carl","Understand how function calls use the call stack. Each call pushes a frame, each return pops it."),
                _tutor("Byte","🧭","The call stack is a stack! Each function call pushes a frame with local variables. Returns pop the frame.","Recursion uses the call stack — each recursive call adds a frame."),
                _discover("Function calls: main() → foo() → bar(). Track the call stack frames.","call-stack","Frame order","main, foo, bar"),
                _manipulate("frame-push","Push frame on call, pop on return","call stack"),
                _code("Trace the call stack for nested function calls.","def bar(): return 'bar'\ndef foo(): return bar()\ndef main(): return foo()\n","# Call stack: main → foo → bar\n# Returns: bar → foo → main\nprint(main())"),
                _checks([r"def\s+",r"return",r"print\(main"]),
                ["Each function call pushes a frame.","The deepest call returns first.","The call stack is LIFO."],
                _success("📞 No frames · ❌ Lost","📞 Frames tracked · ✅ Stack understood","The call stack is fully understood!","Stack Master — understand LIFO in practice.","Every function call is a stack operation.",40),
                _reward(xp=40,coins=20,badges=["stack-master"],unlocks_town="town-2-queue")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 7: Queue Plaza (queue)
# ═══════════════════════════════════════════════════════════════
WORLD_QUEUE = World(
    id="queue", name="Queue Plaza", subtitle="First In, First Out",
    description="Stand in line. The first to arrive is the first to be served. Learn queues.",
    icon="🎫", order=7, theme="queue", recommended_roles=["developer"], prerequisites=["stack"],
    towns=[
        _make_town("line", "The Line", "👥", "First come, first served. A fair queue for everyone.", 1, "FIFO", ["data-structures.queue"], ["queue", "fifo", "deque"], [
            _level("q-1","The Line","🚶",1,"queue","FIFO","data-structures.queue","data-structures.queue",
                _story("Queue Plaza — Entrance","Ticket Tina","People line up at the plaza. The first person in line is the first to get in."),
                _tutor("Byte","🧭","A queue is First In, First Out (FIFO). Like a line at a store.","You enqueue at the back and dequeue from the front."),
                _discover("People arrive: Alice, Bob, Charlie. Who goes in first?","queue-line","First person","Alice"),
                _manipulate("enqueue-person","Add person to back of line","queue.append(person)"),
                _code("Implement a queue. Enqueue and dequeue people.","queue = []\n","queue.append('Alice')\nqueue.append('Bob')\nqueue.append('Charlie')\nprint(queue.pop(0))  # Alice"),
                _checks([r"append",r"pop\(0\)",r"queue\s*=\s*\[\]"]),
                ["Enqueue adds to the back.","Dequeue removes from the front.","First in, first out."],
                _success("👥 No line · 🚪 Empty","👥 Line formed · ✅ FIFO working","The queue works fairly!","Queue — First In, First Out.","Enqueue at back, dequeue at front.",20)),
            _level("q-2","The Priority","⭐",2,"priority","Ordering","data-structures.queue","data-structures.queue",
                _story("Queue Plaza — VIP Section","VIP Manager Vera","Some people have priority. They get served before others in the priority queue."),
                _tutor("Byte","🧭","A priority queue serves the highest priority item first, regardless of arrival order.","Useful for scheduling, Dijkstra's algorithm, and more."),
                _discover("Tasks: A(priority 3), B(priority 1), C(priority 2). Serve highest priority first.","priority-tasks","Serve order","B, C, A"),
                _manipulate("priority-serve","Serve highest priority first","sorted by priority"),
                _code("Implement a priority queue and serve tasks by priority.","tasks = [('A',3),('B',1),('C',2)]\n","tasks.sort(key=lambda x: x[1])\nfor task, pri in tasks:\n    print(f'Serving {task} (priority {pri})')"),
                _checks([r"sort",r"key\s*=",r"lambda"]),
                ["Sort by priority.","Serve in priority order.","Highest priority first."],
                _success("⭐ No priority · ❌ Random","⭐ Priority served · ✅ Fair order","Tasks served by priority!","Priority Queue — ordering by importance.","Priority determines service order.",25)),
            _boss("q-boss","The Printer Queue","🖨️",3,"queue-master","Scheduling","data-structures.queue","data-structures.queue",
                _story("Queue Plaza — Center","Printer Manager Paul","A printer queue handles multiple documents. Each job has a priority and page count."),
                _tutor("Byte","🧭","Real-world queues balance priority and fairness. The printer serves jobs efficiently.","Simulate a printer queue with priority handling."),
                _discover("Print jobs: Doc1(3 pages, pri 2), Doc2(1 page, pri 1), Doc3(2 pages, pri 3). Serve by priority.","printer-queue","Serve order","Doc2, Doc1, Doc3"),
                _manipulate("printer-serve","Sort and serve print jobs","priority queue"),
                _code("Simulate a printer queue with priority.","jobs = [('Doc1',3,2),('Doc2',1,1),('Doc3',2,3)]\n","jobs.sort(key=lambda x: x[2])\nfor name, pages, pri in jobs:\n    print(f'Printing {name}: {pages} pages, priority {pri}')"),
                _checks([r"sort",r"lambda",r"jobs"]),
                ["Sort jobs by priority.","Print each job in order.","Track pages and priority."],
                _success("🖨️ Queue chaotic · ❌ Not scheduled","🖨️ Queue ordered · ✅ All printed","All documents printed in priority order!","Queue Master — real-world scheduling.","Queues power real-world systems.",40),
                _reward(xp=40,coins=20,badges=["queue-master"],unlocks_town="town-2-hash")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 8: Hash Harbor (hashing)
# ═══════════════════════════════════════════════════════════════
WORLD_HASHING = World(
    id="hashing", name="Hash Harbor", subtitle="Instant Lookup",
    description="Find anything instantly with a hash function. Learn hash tables and collision resolution.",
    icon="⚡", order=8, theme="hashing", recommended_roles=["developer"], prerequisites=["queue"],
    towns=[
        _make_town("hash", "Hash Dock", "🏗️", "Hash it, store it, find it instantly.", 1, "Key-Value", ["data-structures.hash"], ["hashing", "hash-table", "collision"], [
            _level("h-1","The Hash Function","🔑",1,"hashing","Mapping","data-structures.hash","data-structures.hash",
                _story("Hash Harbor — Dock","Hash Master Hugo","Convert a key into an index using a hash function. The same key always maps to the same index."),
                _tutor("Byte","🧭","A hash function converts a key into an array index. It should be fast and deterministic.","Like a locker number system — your name maps to a specific locker."),
                _discover("Hash function: index = key % 10. Map keys 15, 25, 37 to indices.","hash-calc","Indices","5, 5, 7"),
                _manipulate("compute-hash","index = key % 10","hash function"),
                _code("Implement a simple hash function and map keys to indices.","keys = [15, 25, 37]\n","hash_table = [None]*10\nfor key in keys:\n    idx = key % 10\n    hash_table[idx] = key\nprint(hash_table)"),
                _checks([r"%",r"hash_table",r"idx"]),
                ["The hash function maps keys to indices.","Same key → same index.","Collisions happen when different keys map to the same index."],
                _success("🔑 No mapping · ❌ Lost","🔑 Hash table built · ✅ Keys mapped","Keys are instantly mappable!","Hash Function — key to index mapping.","Deterministic and fast.",20)),
            _level("h-2","The Collision","💥",2,"collision","Resolving","data-structures.hash","data-structures.hash",
                _story("Hash Harbor — Collision Alley","Collision Handler Cara","Two keys hash to the same index! How do you handle it?"),
                _tutor("Byte","🧭","Collisions are handled by chaining (linked list at each index) or open addressing (find next slot).","Chaining is simpler and more common in practice."),
                _discover("Keys 15 and 25 both hash to index 5. Handle the collision.","collision-handle","Resolution","chain at index 5"),
                _manipulate("chain-handle","Store collided keys in a list","hash_table[idx] = [key1, key2]"),
                _code("Handle collisions using chaining.","hash_table = [[] for _ in range(10)]\n","keys = [15, 25, 35]\nfor key in keys:\n    idx = key % 10\n    hash_table[idx].append(key)\nprint(hash_table)"),
                _checks([r"\[\]\s*for",r"append",r"hash_table"]),
                ["Each index holds a chain (list).","Collided keys go into the same chain.","Search through the chain."],
                _success("💥 Collision ignored · ❌ Data lost","💥 Collision chained · ✅ All stored","Collisions are handled with chaining!","Collision Resolution — chaining method.","Every collision has a home.",25)),
            _boss("h-boss","The Dictionary","📖",3,"hash-master","Looking Up","data-structures.hash","data-structures.hash",
                _story("Hash Harbor — Archive","Dictionary Master Dana","Build a dictionary from scratch using a hash table. Look up, insert, and delete in O(1)."),
                _tutor("Byte","🧭","A dictionary (hash map) is the ultimate hash table application. O(1) average lookup, insert, delete.","Python's dict is a built-in hash table. Understanding it from scratch makes you a better developer."),
                _discover("Build a dictionary: {name: age} for Alice:25, Bob:30, Charlie:35.","build-dict","Dictionary","{'Alice':25,'Bob':30,'Charlie':35}"),
                _manipulate("dict-build","Key-value storage","hash map"),
                _code("Implement a simple dictionary with get, set, and delete.","class Dict:\n    def __init__(self):\n        self.size = 10\n        self.buckets = [[] for _ in range(self.size)]\n","def _hash(self, key): return hash(key) % self.size\n    def set(self, key, val):\n        idx = self._hash(key)\n        for i, (k, v) in enumerate(self.buckets[idx]):\n            if k == key: self.buckets[idx][i] = (k, v); return\n        self.buckets[idx].append((key, val))\n    def get(self, key):\n        idx = self._hash(key)\n        for k, v in self.buckets[idx]:\n            if k == key: return v\n        return None"),
                _checks([r"_hash",r"buckets",r"enumerate"]),
                ["Hash the key to find the bucket.","Search the chain for the key.","Update if found, append if new."],
                _success("📖 No dictionary · ❌ Slow lookup","📖 Dictionary built · ✅ O(1) lookup","The dictionary works at lightning speed!","Hash Master — build a hash map from scratch.","O(1) average case for all operations.",40),
                _reward(xp=40,coins=20,badges=["hash-master"],unlocks_town="town-2-tree")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 9: Tree Grove (trees)
# ═══════════════════════════════════════════════════════════════
WORLD_TREES = World(
    id="trees", name="Tree Grove", subtitle="Hierarchical Data",
    description="Trees branch upward and downward. Learn binary trees, BST, and traversal.",
    icon="🌳", order=9, theme="trees", recommended_roles=["developer", "data-analyst"], prerequisites=["hashing"],
    towns=[
        _make_town("binary", "Binary Grove", "🌲", "Each node branches into at most two children.", 1, "Branching", ["data-structures.tree"], ["binary-tree", "traversal", "BST"], [
            _level("t-1","The Branch","🌿",1,"binary tree","Branching","data-structures.tree","data-structures.tree",
                _story("Tree Grove — Root","Tree Keeper Tara","A tree starts with a root. Each node branches into children. The root has no parent."),
                _tutor("Byte","🧭","A binary tree has at most 2 children per node: left and right.","Like a family tree — each person has at most 2 parents in a binary structure."),
                _discover("Build a binary tree: root(1) → left(2), right(3).","tree-build","Tree structure","root with 2 children"),
                _manipulate("branch-node","Node with left and right","TreeNode(val, left, right)"),
                _code("Create a binary tree with root and two children.","class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n","root = TreeNode(1)\nroot.left = TreeNode(2)\nroot.right = TreeNode(3)"),
                _checks([r"class\s+TreeNode",r"self\.left",r"self\.right"]),
                ["Each node has at most 2 children.","Left child < parent, right child > parent (BST).","The root has no parent."],
                _success("🌿 No tree · 🌳 Just a node","🌿 Tree grown · ✅ Rooted","The tree has a root and branches!","Binary Tree — branching structure.","Each node branches into at most two.",20)),
            _level("t-2","The Traversal","🚶",2,"tree traversal","Visiting","data-structures.tree","data-structures.tree",
                _story("Tree Grove — Path","Path Walker Willow","Visit every node in the tree. In-order: left, root, right."),
                _tutor("Byte","🧭","Tree traversal visits all nodes in a specific order. In-order gives sorted output for BSTs.","Pre-order: root, left, right. Post-order: left, right, root. In-order: left, root, right."),
                _discover("Tree: 2(left), 1(root), 3(right). In-order traversal gives?","tree-traverse","Sorted order","2, 1, 3"),
                _manipulate("in-order","Left → Root → Right","recursive"),
                _code("Implement in-order traversal of a binary tree.","root = TreeNode(1)\nroot.left = TreeNode(2)\nroot.right = TreeNode(3)\n","def inorder(node):\n    if node:\n        inorder(node.left)\n        print(node.val)\n        inorder(node.right)\ninorder(root)"),
                _checks([r"if\s+node",r"inorder\(node\.left\)",r"inorder\(node\.right\]"]),
                ["Visit left subtree first.","Then the root.","Then right subtree."],
                _success("🚶 No traversal · ❌ Missed nodes","🚶 Full traversal · ✅ All visited","Every node is visited in order!","Tree Traversal — in-order, pre-order, post-order.","Recursive visiting of all nodes.",25)),
            _boss("t-boss","The BST","🔍",3,"tree-master","Searching","data-structures.tree","data-structures.tree",
                _story("Tree Grove — Summit","BST Master Boris","A Binary Search Tree keeps data sorted. Search in O(log n) by comparing at each node."),
                _tutor("Byte","🧭","BST: left child < parent < right child. Search by comparing and going left or right.","It is like binary search on a tree structure — O(log n) average case."),
                _discover("BST with values 5,3,7,2,4,6,8. Search for 6.","bst-search","Found at node","6"),
                _manipulate("bst-search","Compare, go left or right","recursive"),
                _code("Implement BST search.","root = TreeNode(5)\nroot.left = TreeNode(3)\nroot.right = TreeNode(7)\n","def search(node, val):\n    if not node: return False\n    if node.val == val: return True\n    if val < node.val: return search(node.left, val)\n    return search(node.right, val)\nprint(search(root, 6))"),
                _checks([r"if\s+not\s+node",r"if\s+val\s*==",r"search\(node\.left"]),
                ["Compare with current node.","Go left if smaller, right if larger.","Return True if found, False if not."],
                _success("🔍 No BST · ❌ Linear search","🔍 BST built · ✅ O(log n) search","The BST enables fast searching!","Tree Master — BST operations.","Logarithmic search on a tree.",40),
                _reward(xp=40,coins=20,badges=["tree-master"],unlocks_town="town-2-graph")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 10: Graph Forest (graphs)
# ═══════════════════════════════════════════════════════════════
WORLD_GRAPHS = World(
    id="graphs", name="Graph Forest", subtitle="Networks of Connection",
    description="Everything connects to everything. Learn graphs, BFS, DFS, and shortest paths.",
    icon="🌐", order=10, theme="graphs", recommended_roles=["developer", "ai-engineer"], prerequisites=["trees"],
    towns=[
        _make_town("bfs", "BFS Meadow", "🌾", "Breadth-first search explores neighbors level by level.", 1, "Level Exploration", ["graphs.bfs"], ["bfs", "queue", "shortest-path"], [
            _level("g-1","The Meadow","🌾",1,"BFS","Level-by-level","graphs.bfs","graphs.bfs",
                _story("Graph Forest — Meadow","Explorer Emma","Explore the meadow level by level. Visit all neighbors before going deeper."),
                _tutor("Byte","🧭","BFS uses a queue to explore nodes level by level. It finds the shortest path in unweighted graphs.","Like ripples in water — each level is one ripple further."),
                _discover("Graph: A connects to B, C. B connects to D. C connects to E. BFS from A.","bfs-meadow","Visit order","A, B, C, D, E"),
                _manipulate("bfs-queue","Queue-based level exploration","queue"),
                _code("Implement BFS on a simple graph.","graph = {'A':['B','C'],'B':['D'],'C':['E']}\n","from collections import deque\nq = deque(['A'])\nvisited = set()\nwhile q:\n    node = q.popleft()\n    if node in visited: continue\n    visited.add(node)\n    print(node)\n    for neighbor in graph[node]:\n        if neighbor not in visited: q.append(neighbor)"),
                _checks([r"deque",r"popleft",r"visited"]),
                ["Use a queue for BFS.","Visit all neighbors before going deeper.","Track visited nodes to avoid cycles."],
                _success("🌾 No exploration · ❌ Lost","🌾 Meadow explored · ✅ BFS done","The meadow is fully explored level by level!","BFS — breadth-first exploration.","Finds shortest path in unweighted graphs.",20)),
            _level("g-2","The Shortest Path","📏",2,"shortest path","Optimal","graphs.bfs","graphs.bfs",
                _story("Graph Forest — Path","Path Finder Felix","Find the shortest path from A to E in the graph. BFS guarantees the shortest path."),
                _tutor("Byte","🧭","BFS finds the shortest path in unweighted graphs because it explores level by level.","The first time you reach a node, that is the shortest path to it."),
                _discover("Graph: A-B, A-C, B-D, C-E, D-E. Shortest path from A to E?","shortest-path","Shortest path","A → C → E"),
                _manipulate("find-path","Track parent pointers","BFS with path reconstruction"),
                _code("Find the shortest path using BFS.","graph = {'A':['B','C'],'B':['D'],'C':['E'],'D':['E']}\n","from collections import deque\nq = deque([[start]])\nvisited = set()\nwhile q:\n    path = q.popleft()\n    node = path[-1]\n    if node == end: print(path); break\n    if node in visited: continue\n    for n in graph[node]:\n        if n not in visited: q.append(path + [n])\n    return None"),
                _checks([r"path\s*\+",r"node\s*==",r"popleft"]),
                ["Track the path as you BFS.","The first arrival is the shortest.","Use parent pointers or path tracking."],
                _success("📏 No path · ❌ Lost","📏 Shortest path found · ✅ Optimal","The shortest path is guaranteed by BFS!","Shortest Path — BFS optimality.","Level-by-level guarantees shortest.",25)),
            _boss("g-boss","The Network","🌐",3,"graph-master","Connecting","graphs.bfs","graphs.bfs",
                _story("Graph Forest — Network","Network Architect Nora","Map a social network of 100 people. Find the shortest connection chain between any two people."),
                _tutor("Byte","🧭","Real-world networks use BFS for friend suggestions, degrees of separation, and more.","Six degrees of separation — BFS proves it."),
                _discover("Social network: 100 people, connections between them. Find shortest chain from person 1 to 100.","social-network","Shortest chain","7 hops"),
                _manipulate("social-bfs","BFS on social graph","queue + visited"),
                _code("Implement BFS on a social network graph.","graph = {i: [] for i in range(1,101)}\n","# Add connections\nfrom collections import deque\nq = deque([(1, [1])])\nvisited = {1}\nwhile q:\n    node, path = q.popleft()\n    if node == 100: print(f'{len(path)-1} hops'); break\n    for n in graph[node]:\n        if n not in visited:\n            visited.add(n)\n            q.append((n, path+[n]))"),
                _checks([r"deque",r"visited",r"path\s*\+"]),
                ["Model the network as a graph.","BFS finds shortest connection chain.","Track visited to avoid infinite loops."],
                _success("🌐 Network unmapped · ❌ Lost","🌐 Network mapped · ✅ Shortest path found","The social network is fully analyzed!","Graph Master — BFS on real networks.","BFS powers social network analysis.",40),
                _reward(xp=40,coins=20,badges=["graph-master"],unlocks_town="town-2-dp")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 11: Dynamic Delta (dynamic programming)
# ═══════════════════════════════════════════════════════════════
WORLD_DYNAMIC = World(
    id="dynamic", name="Dynamic Delta", subtitle="Optimal Substructure",
    description="Break problems into overlapping sub-problems. Store results to avoid redundant work.",
    icon="📐", order=11, theme="dynamic", recommended_roles=["developer", "ai-engineer"], prerequisites=["graphs"],
    towns=[
        _make_town("memo", "Memoization Marsh", "🧠", "Remember results of expensive computations. Reuse them.", 1, "Caching", ["algorithms.dynamic"], ["memoization", "overlapping", "optimal-substructure"], [
            _level("d-1","The Memo","📝",1,"dynamic programming","Caching","algorithms.dynamic","algorithms.dynamic",
                _story("Dynamic Delta — Marsh","DP Master Dora","Computing Fibonacci naively repeats work. Store results and reuse them."),
                _tutor("Byte","🧭","Memoization stores computed results so you do not recalculate them. It turns exponential into linear.","Like keeping a notebook of answers you have already solved."),
                _discover("Fibonacci: fib(5) = fib(4) + fib(3). Without memo, how many calls?","fib-calls","Number of calls","15"),
                _manipulate("memo-fib","Store computed fib values","cache = {}"),
                _code("Implement Fibonacci with memoization.","def fib(n):\n","cache = {}\ndef fib(n):\n    if n <= 1: return n\n    if n in cache: return cache[n]\n    cache[n] = fib(n-1) + fib(n-2)\n    return cache[n]\nprint(fib(10))"),
                _checks([r"cache\s*=\s*\{\}",r"if\s+n\s+in\s+cache",r"cache\[n\]"]),
                ["Store results in a cache.","Check cache before computing.","Reuse stored results."],
                _success("📝 No memo · 💥 Exponential","📝 Memo built · ✅ Linear","Fibonacci is now O(n)!","Memoization — caching computed results.","Avoid redundant computation.",20)),
            _level("d-2","The Table","📊",2,"tabulation","Bottom-up","algorithms.dynamic","algorithms.dynamic",
                _story("Dynamic Delta — Table","Table Master Tom","Build a table from the bottom up. Start with base cases, fill the table iteratively."),
                _tutor("Byte","🧭","Tabulation is the bottom-up approach to DP. Fill a table iteratively instead of recursing.","No recursion overhead, no stack overflow risk."),
                _discover("Climbing stairs: 1 or 2 steps at a time. How many ways to climb 5 stairs?","stairs-table","Number of ways","8"),
                _manipulate("fill-table","Bottom-up table filling","dp[i] = dp[i-1] + dp[i-2]"),
                _code("Implement climbing stairs with tabulation.","n = 5\n","dp = [0]*(n+1)\ndp[0], dp[1] = 1, 1\nfor i in range(2, n+1):\n    dp[i] = dp[i-1] + dp[i-2]\nprint(dp[n])"),
                _checks([r"dp\s*=\s*\[0\]",r"dp\[i\]\s*=\s*dp",r"range"]),
                ["Initialize base cases.","Fill the table iteratively.","Each entry depends on previous entries."],
                _success("📊 No table · ❌ Recursive overflow","📊 Table filled · ✅ Bottom-up","The table is complete — no recursion needed!","Tabulation — bottom-up DP.","Iterative, no stack risk.",25)),
            _boss("d-boss","The Knapsack","🎒",3,"DP-master","Optimizing","algorithms.dynamic","algorithms.dynamic",
                _story("Dynamic Delta — Vault","Optimization Officer Oscar","You have a knapsack with limited capacity. Choose items to maximize total value. Each item can be taken once."),
                _tutor("Byte","🧭","The 0/1 knapsack is the classic DP problem. For each item, decide: take it or leave it.","Build a 2D table: rows are items, columns are capacities."),
                _discover("Capacity 10. Items: (weight=2,value=6), (weight=3,value=7), (weight=5,value=8), (weight=7,value=9). Max value?","knapsack-opt","Max value","19"),
                _manipulate("knapsack-table","2D DP: take or skip","dp[i][w]"),
                _code("Solve the 0/1 knapsack problem.","weights=[2,3,5,7]\nvalues=[6,7,8,9]\ncapacity=10\n","n = len(weights)\ndp = [[0]*(capacity+1) for _ in range(n+1)]\nfor i in range(1, n+1):\n    for w in range(capacity+1):\n        if weights[i-1] <= w:\n            dp[i][w] = max(dp[i-1][w], values[i-1]+dp[i-1][w-weights[i-1]])\n        else:\n            dp[i][w] = dp[i-1][w]\nprint(dp[n][capacity])"),
                _checks([r"dp\s*=\s*\[\[0\]",r"dp\[i\]\[w\]",r"max\("]),
                ["Build a 2D DP table.","For each item and capacity, decide: take or skip.","The optimal value is in dp[n][capacity]."],
                _success("🎒 No optimization · ❌ Greedy fails","🎒 Knapsack solved · ✅ Optimal","The knapsack is optimally filled!","DP Master — knapsack optimization.","Dynamic programming for combinatorial optimization.",40),
                _reward(xp=40,coins=20,badges=["dp-master"],unlocks_town="town-2-alpine")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 12: Alpine Summit (advanced)
# ═══════════════════════════════════════════════════════════════
WORLD_ALPINE = World(
    id="alpine", name="Alpine Summit", subtitle="Mastery of Algorithms",
    description="The peak of algorithmic knowledge. Combine all skills to solve the hardest problems.",
    icon="🏔️", order=12, theme="alpine", recommended_roles=["developer", "ai-engineer"], prerequisites=["dynamic"],
    towns=[
        _make_town("synthesis", "Synthesis Peak", "🎯", "Combine all data structures and algorithms to solve complex problems.", 1, "Synthesis", ["algorithms.synthesis"], ["synthesis", "integration", "advanced"], [
            _level("a-1","The Synthesis","🧩",1,"algorithm synthesis","Combining","algorithms.synthesis","algorithms.synthesis",
                _story("Alpine Summit — Base","Summit Sage Sera","Combine sorting, searching, and graph algorithms to solve a complex problem."),
                _tutor("Byte","🧭","Real problems require combining multiple algorithms and data structures.","The best developers know when to use which tool."),
                _discover("Given a list of words, find the shortest unique prefix for each word using a trie.","unique-prefix","Prefixes","['d','do','dog','cat']"),
                _manipulate("build-trie","Insert words into trie","prefix"),
                _code("Find shortest unique prefixes for all words.","words = ['dog','cat','car','apple']\n","class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.count = 0\ndef insert(root, word):\n    node = root\n    for c in word:\n        if c not in node.children: node.children[c] = TrieNode()\n        node = node.children[c]\n        node.count += 1\ndef prefix(root, word):\n    node = root\n    p = ''\n    for c in word:\n        p += c\n        node = node.children[c]\n        if node.count == 1: return p\n    return p\nroot = TrieNode()\nfor w in words: insert(root, w)\nprint([prefix(root, w) for w in words])"),
                _checks([r"class\s+TrieNode",r"children",r"count"]),
                ["Build a trie from all words.","Count how many words pass through each node.","The first unique prefix is where count = 1."],
                _success("🧩 No synthesis · ❌ Fragmented","🧩 Synthesis complete · ✅ Unified","All algorithms work together!","Synthesis — combining algorithms.","The whole is greater than the sum of parts.",25)),
            _level("a-2","The Optimization","⚡",2,"advanced optimization","Refining","algorithms.synthesis","algorithms.synthesis",
                _story("Alpine Summit — Ridge","Optimization Officer Oscar","Optimize a solution that uses multiple data structures. Reduce time and space complexity."),
                _tutor("Byte","🧭","Optimization is about choosing the right data structure and algorithm for each sub-problem.","Sometimes a hash table replaces a search. Sometimes a heap replaces sorting."),
                _discover("Optimize: find the top K frequent elements. Use hash map + heap.","top-k","Optimized","O(n log k)"),
                _manipulate("top-k","Hash map for counts, heap for top K","heapq"),
                _code("Find the top K frequent elements efficiently.","nums=[1,1,1,2,2,3]\nk=2\n","from collections import Counter\nimport heapq\ncount = Counter(nums)\nprint(heapq.nlargest(k, count.keys(), key=count.get))"),
                _checks([r"Counter",r"heapq",r"nlargest"]),
                ["Count frequencies with a hash map.","Use a heap to get top K.","O(n log k) instead of O(n log n)."],
                _success("⚡ No optimization · ❌ Slow","⚡ Optimized · ✅ Fast","The solution is optimized!", "Advanced Optimization — choosing the right tools.", "Hash map + heap = efficiency.",30)),
            _boss("a-boss","The Grand Challenge","👑",3,"algo-master","Mastering","algorithms.synthesis","algorithms.synthesis",
                _story("Alpine Summit — Peak","Grand Master Gemini","The ultimate challenge: design a system that combines search, sort, graph, DP, and hashing to solve a real-world problem."),
                _tutor("Byte","🧭","The grand challenge tests everything you have learned. Combine all your tools to solve it.","This is what it means to be a Code Wanderer — mastery of all algorithms."),
                _discover("Design a route planner: shortest path (BFS), sorted results (sort), cached lookups (hash), optimal choices (DP).","grand-challenge","Complete system","All components working"),
                _manipulate("build-system","Combine all algorithms","integrated solution"),
                _code("Implement a route planner combining BFS, sorting, and caching.","graph = {'A':['B','C'],'B':['D'],'C':['D'],'D':[]}\n","from collections import deque\ndef bfs(graph, start, end):\n    q = deque([[start]])\n    visited = set()\n    while q:\n        path = q.popleft()\n        node = path[-1]\n        if node == end: return path\n        if node in visited: continue\n        for n in graph.get(node, []):\n            if n not in visited: q.append(path + [n])\n    return None\ndef shortest_paths(graph, start):\n    return sorted(bfs(graph, start, end) or [], key=len)\nprint(shortest_paths(graph, 'A', 'D'))"),
                _checks([r"deque",r"sorted",r"bfs"]),
                ["BFS for shortest path.","Sort paths by length.","Cache results for repeated queries."],
                _success("👑 Challenge incomplete · ❌ Failed","👑 Challenge complete · ✅ Grand Master","You have mastered all algorithms! The Alpine Summit is yours!","Algorithm Master — the peak of coding knowledge.","All skills combined into mastery.",50),
                _reward(xp=50,coins=50,badges=["alpine-master"],title="Grand Master")),
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
    "queue": WORLD_QUEUE,
    "hashing": WORLD_HASHING,
    "trees": WORLD_TREES,
    "graphs": WORLD_GRAPHS,
    "dynamic": WORLD_DYNAMIC,
    "alpine": WORLD_ALPINE,
}
