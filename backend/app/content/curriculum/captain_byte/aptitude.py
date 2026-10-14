"""Captain Byte speeches for the Aptitude Gauntlet.

Covers `quant.*`, `reason.*`, `verbal.*` and `aptitude.*` — the 32 levels of
World 2 (Aptitude Gauntlet). None of these had authored speech before; they
all fell through to the generic fallback.

Every line names the actual technique or the actual mistake. No filler.
"""
from typing import Any, Dict

from ._text import block

APTITUDE: Dict[str, Dict[str, Any]] = {
    # ------------------------------------------------------------------ quant
    "quant.percentages": block(
        "“A percentage is just a fraction with the denominator forced to 100. "
        "Convert the statement into a fraction first, then scale — never reach "
        "for a calculator before the arithmetic is clean.”",
        [
            "“Nice. You built the fraction before you did the maths.”",
            "“Clean. That’s a percentage you could have done in your head.”",
        ],
        [
            "“Stop. You added two percentages that don’t share a base.”",
            "“Careful — successive changes don’t add up. Each one applies to the new number.”",
        ],
        "“You found the wrong base. Recompute against the original number.”",
        "“You’ve got it. I’m removing the training wheels. Any percentage problem.”",
        "“Try again. Write the fraction first, then cancel.”",
    ),
    "quant.percentage_change": block(
        "“Change is always measured against where you started, never against where "
        "you ended up. Increase to X, then decrease by the same percent, and you do "
        "not come back — you come back short.”",
        [
            "“Nice. You anchored the change to the original value.”",
            "“Clean. That’s the net change done properly.”",
        ],
        [
            "“Stop. You measured the change against the final number.”",
            "“No — a 20% cut and a 20% rise don’t cancel. The base moved.”",
        ],
        "“You anchored to the wrong number. Go back to the original.”",
        "“You’ve got it. I’m removing the training wheels. Any change problem.”",
        "“Try again. Which value was the base when the change happened?”",
    ),
    "quant.profit_loss": block(
        "“Profit and loss are percentages of the cost price, not of the selling "
        "price. Fix the cost at 100 in your head, then every percentage becomes a "
        "plain number.”",
        [
            "“Nice. Cost at 100, and the rest fell out.”",
            "“Clean. You kept cost and selling price in their own lanes.”",
        ],
        [
            "“Stop. You took the margin on the wrong quantity.”",
            "“Careful — marked price is not cost price. Discount applies to the marked price.”",
        ],
        "“You mixed up cost and marked price. Rebuild the chain.”",
        "“You’ve got it. I’m removing the training wheels. Any profit problem.”",
        "“Try again. Set cost = 100 and label every number after it.”",
    ),
    "quant.ratios": block(
        "“A ratio is a comparison with units already stripped out. Turn the ratio "
        "into parts, add the parts, and divide the total by that count — every "
        "ratio question becomes one division.”",
        [
            "“Nice. You worked in parts, not in raw numbers.”",
            "“Clean. One division and the whole thing collapsed.”",
        ],
        [
            "“Stop. You added the ratio terms instead of the parts.”",
            "“Careful — ratios with different units can’t be compared directly.”",
        ],
        "“The parts don’t line up. Find the common unit first.”",
        "“You’ve got it. I’m removing the training wheels. Any ratio problem.”",
        "“Try again. Add the parts, then divide.”",
    ),
    "quant.averages": block(
        "“An average is a balance point, not a typical value. Multiply the average "
        "by the count to get the total — totals are what you actually manipulate, "
        "then divide back down.”",
        [
            "“Nice. You went through the total, as always.”",
            "“Clean. Balance point found without touching every entry.”",
        ],
        [
            "“Stop. You averaged the averages.”",
            "“No — you need the count. An average without a count is unfinished.”",
        ],
        "“You skipped the count. Multiply up before you divide down.”",
        "“You’ve got it. I’m removing the training wheels. Any average problem.”",
        "“Try again. Work with totals, not with averages.”",
    ),
    "quant.time_work": block(
        "“Make one person’s rate the unit — 1 worker does 1 job in the total days. "
        "Then combine rates, and when people leave, subtract. Work problems are "
        "rate problems wearing a different hat.”",
        [
            "“Nice. You added rates, not days.”",
            "“Clean. One unit rate and the whole team resolved.”",
        ],
        [
            "“Stop. You added the days instead of the rates.”",
            "“Careful — efficiency multiplies with people, days don’t.”",
        ],
        "“Days don’t combine. Convert to a per-day rate first.”",
        "“You’ve got it. I’m removing the training wheels. Any work problem.”",
        "“Try again. Give me the rate for one worker.”",
    ),
    "quant.tsd": block(
        "“Distance equals rate times time, and it never changes while you rearrange "
        "it. Write that one equation, then ask what stays constant on both legs of "
        "the journey — usually distance or total time.”",
        [
            "“Nice. You used the constant and let the equation do the work.”",
            "“Clean. One equation, both legs handled.”",
        ],
        [
            "“Stop. You averaged the two speeds. Average speed needs total distance.”",
            "“Careful — the legs look symmetric but the times aren’t.”",
        ],
        "“Something changed between the legs. Which quantity stayed fixed?”",
        "“You’ve got it. I’m removing the training wheels. Any speed problem.”",
        "“Try again. Write distance = speed × time for each leg.”",
    ),
    "quant.interest": block(
        "“Simple interest grows on the principal alone; compound interest grows on "
        "whatever the balance already became. For short horizons the gap is small "
        "— for long ones it’s the whole question.”",
        [
            "“Nice. You let the balance carry the previous years.”",
            "“Clean. You matched the formula to the horizon.”",
        ],
        [
            "“Stop. You applied simple interest to a compounding statement.”",
            "“Careful — the compounding period is what the rate is actually per.”",
        ],
        "“You used the wrong growth base. Check the period.”",
        "“You’ve got it. I’m removing the training wheels. Any interest problem.”",
        "“Try again. Is the principal standing still or growing?”",
    ),
    "quant.di": block(
        "“Data Interpretation rewards reading, not arithmetic. Read the question "
        "first, then go to the chart with a target — you usually need one or two "
        "numbers, never the whole table.”",
        [
            "“Nice. You read the question before the chart.”",
            "“Clean. You took only the numbers that mattered.”",
        ],
        [
            "“Stop. You’re computing numbers the question never asked for.”",
            "“Careful — check the units. Percentages and absolute values look alike.”",
        ],
        "“You pulled the wrong figure. Re-read what was actually asked.”",
        "“You’ve got it. I’m removing the training wheels. Any DI set.”",
        "“Try again. Read the question, then hunt for the two numbers.”",
    ),
    "quant.numbers": block(
        "“Number systems are about place value and divisibility rules, not about "
        "big multiplication. Learn the tests for 3, 4, 8, 9 and 11, and most "
        "questions stop being arithmetic.”",
        [
            "“Nice. You used the divisibility rule instead of dividing.”",
            "“Clean. Place value did the heavy lifting.”",
        ],
        [
            "“Stop. You multiplied out numbers you could have factored.”",
            "“Careful — you lost the sign. Odd, even, negative are not the same question.”",
        ],
        "“The factorisation is wrong. Break it down again.”",
        "“You’ve got it. I’m removing the training wheels. Any number problem.”",
        "“Try again. Which divisibility rule applies here?”",
    ),
    "quant.pnc": block(
        "“Permutations care about order, combinations do not. Decide that first — "
        "it decides the formula. Then apply the constraint: if items must be "
        "together, glue them into one and count the glued set.”",
        [
            "“Nice. You settled order first, then chose the formula.”",
            "“Clean. The constraint went in before the count.”",
        ],
        [
            "“Stop. You used nPr where order doesn’t matter.”",
            "“Careful — you counted arrangements that differ only by order twice.”",
        ],
        "“Order was handled twice or not at all. Reset the count.”",
        "“You’ve got it. I’m removing the training wheels. Any counting problem.”",
        "“Try again. Does order change the outcome here?”",
    ),
    "quant.probability": block(
        "“Probability is favourable over total, with the total fixed once you pick "
        "your sample space. For ‘at least one’ questions, don’t add — subtract the "
        "chance that it never happens.”",
        [
            "“Nice. You complemented instead of enumerating.”",
            "“Clean. Your sample space was complete and equally likely.”",
        ],
        [
            "“Stop. You added outcomes that can happen together.”",
            "“Careful — your denominator counts outcomes that aren’t possible.”",
        ],
        "“Your sample space is wrong. List what’s actually possible.”",
        "“You’ve got it. I’m removing the training wheels. Any probability problem.”",
        "“Try again. Is it easier to count the event or its opposite?”",
    ),
    "quant.logarithms": block(
        "“A logarithm asks ‘this base to what power gives me that’. Collapse the "
        "terms with the log laws first, then solve — never evaluate the log by "
        "guessing.”",
        [
            "“Nice. You collapsed the log before you solved.”",
            "“Clean. The base made the power obvious.”",
        ],
        [
            "“Stop. You multiplied logs that should have been added.”",
            "“Careful — the base has to match before the logs combine.”",
        ],
        "“The bases don’t match. Rewrite one of them first.”",
        "“You’ve got it. I’m removing the training wheels. Any log problem.”",
        "“Try again. Which log law applies to these terms?”",
    ),
    "quant.progressions": block(
        "“An arithmetic progression moves by a fixed difference, a geometric one by "
        "a fixed ratio. Identify which, then use the formula for the sum rather "
        "than adding the terms yourself.”",
        [
            "“Nice. You spotted the fixed difference.”",
            "“Clean. The sum formula handled all n terms at once.”",
        ],
        [
            "“Stop. You treated a ratio-driven sequence as arithmetic.”",
            "“Careful — you used n terms when the list starts at a different index.”",
        ],
        "“You mixed up difference and ratio. Re-identify the progression.”",
        "“You’ve got it. I’m removing the training wheels. Any progression problem.”",
        "“Try again. Is the step constant or the ratio constant?”",
    ),
    "quant.geometry": block(
        "“Geometry is diagram discipline. Label every given length, mark the right "
        "angles, and look for the one triangle or circle property that connects "
        "them — the answer is usually one property away.”",
        [
            "“Nice. You labelled the diagram and the path appeared.”",
            "“Clean. One property linked the two lengths.”",
        ],
        [
            "“Stop. You assumed the diagram was to scale.”",
            "“Careful — you used a theorem that needs a right angle you never proved.”",
        ],
        "“The assumption isn’t in the statement. Prove it or drop it.”",
        "“You’ve got it. I’m removing the training wheels. Any geometry problem.”",
        "“Try again. What does the diagram actually guarantee?”",
    ),
    # ----------------------------------------------------------------- reason
    "reason.relations": block(
        "“Draw the family tree before you answer anything. Nodes for people, arrows "
        "for the relationship, generations on separate rows — once the diagram is "
        "down, the question usually answers itself.”",
        [
            "“Nice. The tree did the reasoning for you.”",
            "“Clean. You placed the generation before the person.”",
        ],
        [
            "“Stop. You inferred gender from a word that doesn’t imply it.”",
            "“Careful — you followed one branch and stopped. Check the other side.”",
        ],
        "“The link you assumed isn’t stated. Draw only what’s given.”",
        "“You’ve got it. I’m removing the training wheels. Any relation puzzle.”",
        "“Try again. Draw it, then point at the node in question.”",
    ),
    "reason.coding": block(
        "“Coding–decoding is substitution with a rule you must first reverse-engineer "
        "from a known pair. Find how one word becomes another, write the rule down, "
        "then apply it — never guess letter by letter.”",
        [
            "“Nice. You derived the rule from a worked pair.”",
            "“Clean. One rule, applied consistently.”",
        ],
        [
            "“Stop. You’re shifting letters in two directions at once.”",
            "“Careful — the direction of the shift changes between examples.”",
        ],
        "“The rule you’re using contradicts the example. Re-derive it.”",
        "“You’ve got it. I’m removing the training wheels. Any coding puzzle.”",
        "“Try again. Compare the first pair and write the shift down.”",
    ),
    "reason.seating": block(
        "“Seating puzzles are solved with a fixed anchor. Place the one person whose "
        "position is fully determined, then hang everyone else off that anchor — "
        "and keep circular and linear arrangements on separate diagrams.”",
        [
            "“Nice. You anchored, then hung the rest.”",
            "“Clean. Left and right stayed consistent.”",
        ],
        [
            "“Stop. You mixed left/right of the table with facing it.”",
            "“Careful — you moved the anchor after placing people against it.”",
        ],
        "“Your anchor shifted. Place it once and never move it.”",
        "“You’ve got it. I’m removing the training wheels. Any seating puzzle.”",
        "“Try again. Who is fully determined? Start there.”",
    ),
    "reason.puzzles": block(
        "“A puzzle is a set of constraints, not a story. Convert each sentence into "
        "a constraint, then eliminate until one arrangement survives — speed comes "
        "from discarding options, not from guessing.”",
        [
            "“Nice. You turned the story into constraints.”",
            "“Clean. Elimination did the work, not a lucky guess.”",
        ],
        [
            "“Stop. You kept a possibility the text already ruled out.”",
            "“Careful — you read a clue as optional when it was definite.”",
        ],
        "“One constraint was ignored. Re-read the sentence you skipped.”",
        "“You’ve got it. I’m removing the training wheels. Any puzzle.”",
        "“Try again. List the constraints before you arrange anything.”",
    ),
    "reason.syllogisms": block(
        "“Draw the circles. If a statement says all A are B, draw A fully inside B. "
        "Then check whether your conclusion is forced by the diagram — if it might "
        "be true but isn’t guaranteed, it does not follow.”",
        [
            "“Nice. The diagram made the conclusion obvious.”",
            "“Clean. You separated ‘might follow’ from ‘must follow’.”",
        ],
        [
            "“Stop. You assumed the two sets are the same size.”",
            "“Careful — ‘some’ doesn’t guarantee which members are included.”",
        ],
        "“You drew more than the statement allows. Shrink it back.”",
        "“You’ve got it. I’m removing the training wheels. Any syllogism.”",
        "“Try again. Draw it, then ask if it’s forced.”",
    ),
    "reason.direction": block(
        "“Turn every sentence into one arrow on a single consistent compass, and "
        "treat a turn as relative to where you were facing — not to the page. Once "
        "the path is drawn, the distance is just Pythagoras.”",
        [
            "“Nice. You kept the compass relative to your heading.”",
            "“Clean. The path resolved without a second diagram.”",
        ],
        [
            "“Stop. You applied ‘left’ to the page instead of to the heading.”",
            "“Careful — you dropped a segment before measuring the net distance.”",
        ],
        "“One leg of the path is missing. Redraw from the start.”",
        "“You’ve got it. I’m removing the training wheels. Any direction problem.”",
        "“Try again. Face the way you came from, then turn.”",
    ),
    # ------------------------------------------------------------------ verbal
    "verbal.grammar": block(
        "“Grammar questions are decided by structure, not by how the sentence sounds. "
        "Find the subject and its verb first, agree them, then check the modifier "
        "is pointing at what you think it is.”",
        [
            "“Nice. You found the subject before anything else.”",
            "“Clean. The modifier landed on the right noun.”",
        ],
        [
            "“Stop. You trusted the ear — a long noun phrase hid the real subject.”",
            "“Careful — the participle is dangling. It can’t modify a subject it isn’t attached to.”",
        ],
        "“The subject and verb still disagree. Isolate them and re-check.”",
        "“You’ve got it. I’m removing the training wheels. Any grammar question.”",
        "“Try again. Strip it to the subject and verb.”",
    ),
    "verbal.reading": block(
        "“Read the questions first, then the passage — you read with a target. The "
        "correct answer must be supported by a line you can point at; anything the "
        "passage merely permits is a trap.”",
        [
            "“Nice. You pointed at the supporting line.”",
            "“Clean. You rejected the answer the passage only allows.”",
        ],
        [
            "“Stop. That’s true in general, but the passage doesn’t say it.”",
            "“Careful — you picked the extreme word. Extreme rarely survives the text.”",
        ],
        "“No line supports that. Find the sentence that does — if you can’t, it’s out.”",
        "“You’ve got it. I’m removing the training wheels. Any reading question.”",
        "“Try again. Which line in the passage proves it?”",
    ),
    "verbal.vocabulary": block(
        "“Build meaning from the roots and the surrounding words, not from a word you "
        "almost recognise. When you’re stuck, use the blank as a filter — read the "
        "sentence, predict the meaning, then match.”",
        [
            "“Nice. You predicted the meaning before looking at the options.”",
            "“Clean. The root carried the answer.”",
        ],
        [
            "“Stop. You picked the word that sounded most familiar.”",
            "“Careful — those two are near-synonyms; the sentence tone separates them.”",
        ],
        "“The fit is wrong for the sentence. Predict the meaning again.”",
        "“You’ve got it. I’m removing the training wheels. Any vocabulary question.”",
        "“Try again. What does the sentence need the word to mean?”",
    ),
    # ----------------------------------------------------------------- mocks
    "aptitude.mock": block(
        "“A mock is a timing rehearsal, not a knowledge test. Skip anything that "
        "costs more than a minute, come back with fresh eyes, and protect the "
        "questions you know you can convert.”",
        [
            "“Nice. You banked the easy marks before chasing the hard ones.”",
            "“Clean. That was a decision, not a guess.”",
        ],
        [
            "“Stop. You spent three minutes on one question while easy marks sat untouched.”",
            "“Careful — you answered from memory instead of from the data given.”",
        ],
        "“That one isn’t converting. Park it and come back.”",
        "“You’ve got it. I’m removing the training wheels. Any timed set.”",
        "“Try again. Convert what you can, then return to this.”",
    ),
    "aptitude.mastery": block(
        "“You’ve covered the syllabus — this is where it has to hold under time "
        "pressure, without notes and without me. Prove you can produce the method "
        "on demand, not just recognise it.”",
        [
            "“Nice. The method came out without prompting.”",
            "“Clean. Under time, and it still held.”",
        ],
        [
            "“Stop. You recognised the technique but didn’t apply it fully.”",
            "“Careful — accuracy slipped when the clock came on. Slow the first step.”",
        ],
        "“It broke under pressure. Identify which step you dropped.”",
        "“You’ve got it. This is the standard. Hold it.”",
        "“Try again. Rebuild the method from the top, out loud.”",
    ),
}

#: Shared voice for any `quant|reason|verbal|aptitude` skill without its own entry.
DOMAIN_APTITUDE: Dict[str, Any] = block(
    "“Work the statement, not the arithmetic. Write what you know in one line, "
    "identify what stays fixed, and let that constraint choose your method.”",
    [
        "“Nice. You used the constraint instead of force.”",
        "“Clean. That method will hold on a harder version.”",
    ],
    [
        "“Stop. You reached for a formula before identifying what’s constant.”",
        "“Careful — you’re solving a similar question, not this one.”",
    ],
    "“The setup is off. Re-read the statement and rebuild the line.”",
    "“You’ve got it. I’m removing the training wheels. Any aptitude question.”",
    "“Try again. What does the statement actually fix?”",
)
