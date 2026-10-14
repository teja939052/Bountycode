"""Captain Byte speeches for the engineering track.

19 skills across the backend, data, engineering, system-design and creative
levels. These lessons previously shipped the generic placeholder as their
authored speech — see `is_generic_block()`.

Voice: name the contract or the trade-off first. These are subjects where a
half-answer is worse than a short precise one.
"""
from typing import Any, Dict

from ._text import block

ENGINEERING: Dict[str, Dict[str, Any]] = {
    # --------------------------------------------------------------- backend
    "backend.rest": block(
        "“REST is a contract about resources, not about URLs you invent as you go. "
        "Each noun is a thing the client names, each verb is what you’re allowed "
        "to do to it — if you can’t name the resource, the endpoint isn’t designed yet.”",
        [
            "“Nice. The resource named itself, so the route followed.”",
            "“Clean. Nouns and verbs, no action-verbs bolted on.”",
        ],
        [
            "“Stop. That endpoint is describing an action, not a resource.”",
            "“Careful — you invented a new path for something you already had.”",
        ],
        "“Which resource is this? Name it before you design the route.”",
        "“You’ve got it. Any REST question — resource first, route second.”",
        "“Try again. If the noun were plural, what would the five routes be?”",
    ),
    "backend.status_codes": block(
        "“A status code tells the client what changed, not what you were thinking. "
        "200 is success, 201 created with a location, 204 nothing to return, 400 "
        "the client is wrong, 404 it isn’t there, 409 conflict, 500 you broke it.”",
        [
            "“Nice. The code matched the actual outcome.”",
            "“Clean. You picked 201 and set the location header.”",
        ],
        [
            "“Stop. You returned 200 for something that didn’t exist.”",
            "“Careful — that’s a client error wearing a server-error costume.”",
        ],
        "“Whose fault is it, and did the resource change? The code follows.”",
        "“You’ve got it. Any API question — outcome first, code second.”",
        "“Try again. Client mistake, missing resource, or server bug?”",
    ),
    "backend.apis": block(
        "“An API is a promise about the future: the shape you return today is the "
        "shape clients depend on tomorrow. Version deliberately, never silently "
        "remove a field, and make errors structured rather than apologetic.”",
        [
            "“Nice. You treated the contract as something you can’t casually break.”",
            "“Clean. The error told the client what to do next.”",
        ],
        [
            "“Stop. You changed the response shape and called it a fix.”",
            "“Careful — the error body is a string nobody can parse.”",
        ],
        "“What does a client written last month do with this response?”",
        "“You’ve got it. Any API design question — start from the consumer.”",
        "“Try again. What breaks for a client you shipped six months ago?”",
    ),
    "backend.sql": block(
        "“A query is read top to bottom and executed inside out: FROM builds the "
        "rows, WHERE filters them, SELECT names them. Add an index where you "
        "filter and join — and check the plan before you trust the intuition.”",
        [
            "“Nice. You reasoned about the rows the database actually touches.”",
            "“Clean. You matched the index to the predicate.”",
        ],
        [
            "“Stop. You selected before you filtered.”",
            "“Careful — you’re scanning the whole table on a column with no index.”",
        ],
        "“How many rows does this actually read? Rebuild it inside out.”",
        "“You’ve got it. Any query — rows first, columns after.”",
        "“Try again. What index would make this stop scanning?”",
    ),
    "backend.joins": block(
        "“A join pairs rows on a key — INNER keeps only matches, LEFT keeps "
        "everything from the left even when nothing matches. When the count "
        "doubles after a join, you added a one-to-many and didn’t notice.”",
        [
            "“Nice. You knew exactly which side would survive.”",
            "“Clean. The row count after the join was what you predicted.”",
        ],
        [
            "“Stop. You used INNER where you needed to keep the left side.”",
            "“Careful — the join key isn’t unique, so your rows multiplied.”",
        ],
        "“Count the rows on each side. Which key is one-to-many here?”",
        "“You’ve got it. Any join — settle which rows survive first.”",
        "“Try again. What does this return for a row with no match?”",
    ),
    "backend.databases": block(
        "“Choose the database by what you must guarantee: transactions and "
        "consistency point to a relational store, scale and flexible shape point "
        "to a document store, relationships and graph traversal point to a graph "
        "store. The wrong choice is expensive later.”",
        [
            "“Nice. You picked from the guarantee, not from the trend.”",
            "“Clean. You named what you’d give up as well.”",
        ],
        [
            "“Stop. You chose it because it was popular.”",
            "“Careful — you need transactions, and you picked something that doesn’t offer them.”",
        ],
        "“What must this data guarantee? Let that decide the store.”",
        "“You’ve got it. Any data question — guarantees before tooling.”",
        "“Try again. Which requirement kills each of your two options?”",
    ),
    # ------------------------------------------------------------------ data
    "data.aggregation": block(
        "“Aggregation folds many rows into one answer: GROUP BY decides what "
        "counts as a group, the aggregate decides what you measure. Get the "
        "grouping wrong and every number in the answer is confidently wrong.”",
        [
            "“Nice. You set the grouping before you picked the measure.”",
            "“Clean. The total matched the rows you expected.”",
        ],
        [
            "“Stop. You aggregated without saying what a group was.”",
            "“Careful — NULLs formed their own group and skewed the result.”",
        ],
        "“What counts as one group here? Fix the grouping first.”",
        "“You’ve got it. Any aggregation — groups before sums.”",
        "“Try again. Which rows collapse into a single output row?”",
    ),
    "data.window_functions": block(
        "“A window function computes across a set of rows that are related but "
        "not collapsed — it adds a column instead of removing rows. PARTITION BY "
        "sets the group, ORDER BY sets the running order.”",
        [
            "“Nice. You kept the rows and added the answer alongside.”",
            "“Clean. Partition and order both did what you intended.”",
        ],
        [
            "“Stop. You used an aggregate where you needed a window.”",
            "“Careful — the ranking reset because you didn’t partition.”",
        ],
        "“Rows disappear or rows stay? That decides aggregate or window.”",
        "“You’ve got it. Any window function — partition, then order.”",
        "“Try again. What is the frame, and when does it reset?”",
    ),
    "data.analytics": block(
        "“Analytics is deciding what question the number answers before you trust "
        "it. Define the metric, fix the time window, state the cohort — then, and "
        "only then, look at the trend.”",
        [
            "“Nice. You defined the metric before you charted it.”",
            "“Clean. Same cohort on both sides of the comparison.”",
        ],
        [
            "“Stop. You’re comparing two numbers measured on different windows.”",
            "“Careful — the metric changed definition halfway through the series.”",
        ],
        "“What exactly is this number counting, over what period?”",
        "“You’ve got it. Any analytics question — definition first.”",
        "“Try again. Who’s in the cohort, and what starts and stops the clock?”",
    ),
    # ------------------------------------------------------------ engineering
    "engineering.branching": block(
        "“A branch is cheap, a merge is not. Keep branches short-lived, integrate "
        "into main often, and make every merge either revertible or obvious — "
        "because the expensive part of version control is the day you’re stuck.”",
        [
            "“Nice. Small branch, integrated while it’s still fresh.”",
            "“Clean. You could revert that in one step if you had to.”",
        ],
        [
            "“Stop. That branch has three weeks of unrelated work in it.”",
            "“Careful — you merged with conflicts you never actually read.”",
        ],
        "“Can you still revert this cleanly? If not, split it.”",
        "“You’ve got it. Any workflow question — think about the day it breaks.”",
        "“Try again. What’s in this branch besides the thing you set out to do?”",
    ),
    "engineering.git": block(
        "“Git records decisions, not files. Stage what belongs together, commit the "
        "reason in the message, and read the diff before you commit it — the diff "
        "is the only honest description of what you actually changed.”",
        [
            "“Nice. One coherent change, explained in the message.”",
            "“Clean. The diff contained only what the message claimed.”",
        ],
        [
            "“Stop. That commit mixes four unrelated changes.”",
            "“Careful — you committed a secret. Revert it, don’t just delete it.”",
        ],
        "“Read the diff. Does it do exactly one thing the message can name?”",
        "“You’ve got it. Any Git question — think about whoever reads this next.”",
        "“Try again. What story does this diff tell, in one line?”",
    ),
    "engineering.unit_tests": block(
        "“A unit test pins one behaviour, not one implementation. Assert the "
        "outcome the caller cares about — if renaming a private method breaks "
        "your test, the test is testing the wrong thing.”",
        [
            "“Nice. The assertion survived an internal rename.”",
            "“Clean. One behaviour, one test, clear name.”",
        ],
        [
            "“Stop. You’re asserting on private structure, so the test is brittle.”",
            "“Careful — that test passes even when the behaviour is wrong.”",
        ],
        "“What does the caller actually depend on? Assert that.”",
        "“You’ve got it. Any test question — behaviour, not implementation.”",
        "“Try again. Could this test stay green while the feature is broken?”",
    ),
    "engineering.testing": block(
        "“Test the risk, not the coverage number. Cover the paths that fail "
        "expensively — money moves, data deletes, permission checks — and treat "
        "a missing edge case as a bug you’ve already found.”",
        [
            "“Nice. You tested the case that would actually hurt.”",
            "“Clean. The edge case was written before the fix.”",
        ],
        [
            "“Stop. You’re chasing a coverage percentage, not a risk.”",
            "“Careful — the happy path is green and the failure path is untested.”",
        ],
        "“If this breaks in production, what’s the cost? Test that first.”",
        "“You’ve got it. Any testing question — start from the damage.”",
        "“Try again. Which failure here is the most expensive one?”",
    ),
    # --------------------------------------------------------- system design
    "sd.requirements": block(
        "“Design starts with requirements, not with boxes. Write down what must be "
        "true — users, load, latency, consistency, failure modes — because every "
        "architectural choice you make afterwards is only correct relative to them.”",
        [
            "“Nice. You pinned the requirements before drawing anything.”",
            "“Clean. The design followed from a stated constraint.”",
        ],
        [
            "“Stop. You started naming technologies before stating the problem.”",
            "“Careful — you assumed a scale nobody gave you.”",
        ],
        "“What must be true? Write the constraints, then draw.”",
        "“You’ve got it. Any design question — requirements first, boxes after.”",
        "“Try again. Which requirement forces the choice you just made?”",
    ),
    "sd.estimation": block(
        "“Back-of-envelope is a discipline, not a guess. Fix the numbers you can "
        "reason about — bytes per record, records per user, requests per second — "
        "state every assumption out loud, and be visibly wrong in the right order "
        "of magnitude rather than quietly wrong to two digits.”",
        [
            "“Nice. You stated the assumptions and the arithmetic followed.”",
            "“Clean. Order of magnitude right, and you showed the working.”",
        ],
        [
            "“Stop. You produced a precise number from unstated assumptions.”",
            "“Careful — you skipped the step where the estimate meets reality.”",
        ],
        "“Name your assumptions. Which one is the shakiest?”",
        "“You’ve got it. Estimate out loud, then sanity-check the magnitude.”",
        "“Try again. What’s the one number everything else depends on?”",
    ),
    "sd.tradeoffs": block(
        "“There is no design without a trade-off — only designs where the cost is "
        "still hidden. Name what you’re giving up: consistency for availability, "
        "latency for durability, simplicity for flexibility. A design you can’t "
        "criticise is a design you don’t yet understand.”",
        [
            "“Nice. You named the cost as clearly as the benefit.”",
            "“Clean. You’d defend that choice under load and under failure.”",
        ],
        [
            "“Stop. You presented a benefit with no cost attached.”",
            "“Careful — you called it ‘simpler’ without saying what you gave up.”",
        ],
        "“What did that choice cost? Every option has a bill.”",
        "“You’ve got it. Any design question — find the trade-off.”",
        "“Try again. When does this choice become the wrong one?”",
    ),
    # --------------------------------------------------------------- creative
    "creative.problem_definition": block(
        "“A portfolio project is judged on the problem, not the code. Define who "
        "has the problem, how they have it now, and what changes when yours works "
        "— everything technical follows from being able to say that in one sentence.”",
        [
            "“Nice. You could say the problem in one sentence.”",
            "“Clean. The solution followed from who has the pain.”",
        ],
        [
            "“Stop. You built it before you could say who it’s for.”",
            "“Careful — you described the features, not the problem.”",
        ],
        "“Who has this problem today, and what do they do instead?”",
        "“You’ve got it. Problem first — the code is the proof.”",
        "“Try again. Say the problem without mentioning your solution.”",
    ),
    "creative.documentation": block(
        "“Documentation is the part of your work a stranger meets first. A README "
        "that answers ‘what is this, why does it exist, and how do I run it in "
        "one command’ is worth more than another feature nobody can start.”",
        [
            "“Nice. A stranger could run it from the README alone.”",
            "“Clean. What, why, and how — in that order.”",
        ],
        [
            "“Stop. The README is a file list, not an explanation.”",
            "“Careful — the setup steps don’t work on a clean machine.”",
        ],
        "“Follow your own README on a clean clone. Where does it break?”",
        "“You’ve got it. Write for the person who meets this cold.”",
        "“Try again. What’s the first question a stranger asks, and where’s the answer?”",
    ),
    "creative.independent": block(
        "“Shipping something alone is the proof employers look for: you defined "
        "the scope, hit a wall, found your way through, and finished. Make the "
        "hard part visible — that’s the portfolio, not the stack list.”",
        [
            "“Nice. The hard part is documented, not hidden.”",
            "“Clean. You finished it, and you can defend the choices.”",
        ],
        [
            "“Stop. It’s a list of technologies with nothing you actually solved.”",
            "“Careful — it’s unfinished, and you’re hoping nobody asks.”",
        ],
        "“What was genuinely hard here? That’s the part worth showing.”",
        "“You’ve got it. One finished thing beats five started ones.”",
        "“Try again. Where did you get stuck, and how did you get out?”",
    ),
}

#: Shared voice for the engineering track when a skill has no authored entry.
DOMAIN_ENGINEERING: Dict[str, Any] = block(
    "“State the contract or the trade-off before you describe the implementation. "
    "These subjects reward the person who can say what must be true and what it "
    "costs — the code is only the last step.”",
    [
        "“Nice. You named the contract before the mechanics.”",
        "“Clean. You said what it costs as well as what it buys.”",
    ],
    [
        "“Stop. You jumped to implementation without saying what must hold.”",
        "“Careful — the benefit is clear and the cost isn’t.”",
    ],
    "“What has to be true here, and what does that cost you?”",
    "“You’ve got it. Contract first, implementation second.”",
    "“Try again. What does this guarantee — and what does it give up?”",
)
