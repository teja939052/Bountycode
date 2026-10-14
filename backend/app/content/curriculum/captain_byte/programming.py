"""Captain Byte speeches for Coding Foundations (World 3) and DSA.

22 skills across 29 levels. The existing wrappers already covered these by
theme keyword; keying on the canonical skill id is stricter and stops the
title-scan from mis-firing (e.g. a lesson called "Sorting It Out" inside a
reasoning world).

Voice: trace before you predict, name the invariant before you code it.
"""
from typing import Any, Dict

from ._text import block

PROGRAMMING: Dict[str, Dict[str, Any]] = {
    # ------------------------------------------------------------- code basics
    "code.pseudocode": block(
        "“Pseudocode is thinking made checkable. Write it in plain steps a person "
        "could follow, then read it back and look for the step that’s missing — "
        "almost every logic bug is a line you never wrote down.”",
        [
            "“Nice. You wrote the missing line before the code existed.”",
            "“Clean. A person could have followed that.”",
        ],
        [
            "“Stop. Step four appears from nowhere — where did that value come from?”",
            "“Careful — you skipped the decision entirely. Where’s the branch?”",
        ],
        "“A step is missing. What has to happen before that line?”",
        "“You’ve got it. Any program — write the steps, then defend them.”",
        "“Try again. Walk it out loud as if you were the machine.”",
    ),
    "code.prediction": block(
        "“Predict output by running the code on paper, line by line, updating each "
        "variable exactly as written. Never guess from the shape of the program — "
        "the answer is almost always in the line you skimmed past.”",
        [
            "“Nice. You traced it line by line instead of recognising it.”",
            "“Clean. Every variable updated exactly as written.”",
        ],
        [
            "“Stop. You predicted what the code *meant*, not what it *does*.”",
            "“Careful — that loop runs one more time than you counted.”",
        ],
        "“Re-trace it. Where does the counter actually stop?”",
        "“You’ve got it. Trace it and the output is inevitable.”",
        "“Try again. Run it in your head, one line at a time.”",
    ),
    "code.variables": block(
        "“A variable is a labelled box holding one value at a time. After every "
        "assignment, ask what’s inside now — most ‘wrong output’ bugs are someone "
        "remembering what used to be in the box.”",
        [
            "“Nice. You updated the box after every assignment.”",
            "“Clean. Type and value both accounted for.”",
        ],
        [
            "“Stop. That name still points at the old value.”",
            "“Careful — you read the box before you wrote to it.”",
        ],
        "“The box is stale. Re-run the assignments in order.”",
        "“You’ve got it. Any variable problem — check the box first.”",
        "“Try again. What’s in it right now, line by line?”",
    ),
    "code.operators": block(
        "“Operator precedence decides what binds first — parentheses make that "
        "explicit and cost nothing. Watch integer division and the difference "
        "between `=` and `==`; they cause more broken programs than anything else.”",
        [
            "“Nice. You parenthesised instead of trusting your memory of precedence.”",
            "“Clean. Assignment and comparison kept apart.”",
        ],
        [
            "“Stop. You used `=` where you meant `==`.”",
            "“Careful — the precedence made that expression bind differently.”",
        ],
        "“The expression parsed differently than you read it. Add parentheses.”",
        "“You’ve got it. Any expression — make the binding explicit.”",
        "“Try again. What does this evaluate to, innermost group first?”",
    ),
    "code.conditions": block(
        "“A condition is a claim that’s true or false — nothing in between. Work out "
        "the truth of each part before combining them with AND and OR, and never "
        "chain comparisons the way you’d read them in English.”",
        [
            "“Nice. You evaluated each part before combining.”",
            "“Clean. Short-circuiting did what you expected.”",
        ],
        [
            "“Stop. You chained a comparison the way English reads it.”",
            "“Careful — operator precedence split your AND and OR.”",
        ],
        "“The condition isn’t saying what you think. Break it into parts.”",
        "“You’ve got it. Any branch — get the truth table right first.”",
        "“Try again. What does each part evaluate to on its own?”",
    ),
    "code.loops": block(
        "“A loop is a start, a condition, and a step — in that order, every time. "
        "Write down the counter’s value on entry, on each pass, and on exit; the "
        "off-by-one is always visible when you do.”",
        [
            "“Nice. You tracked the counter through every pass.”",
            "“Clean. The exit condition landed where you expected.”",
        ],
        [
            "“Stop. You used `<` where the bound needs `<=`.”",
            "“Careful — the loop body changed the thing the condition depends on.”",
        ],
        "“The bound is off. Write the counter at entry and at exit.”",
        "“You’ve got it. Any loop — trace the counter, don’t trust the feel.”",
        "“Try again. What’s the value of the counter on the last pass?”",
    ),
    "code.functions": block(
        "“A function is a contract: these inputs in, this result out, no surprises "
        "from the outside. Test it on the edge — empty, zero, one element — because "
        "that’s where a contract quietly breaks.”",
        [
            "“Nice. You tested the edge, not just the happy path.”",
            "“Clean. Inputs in, result out, nothing leaked out.”",
        ],
        [
            "“Stop. The function is reading a variable from outside its contract.”",
            "“Careful — it works for the example and fails on empty input.”",
        ],
        "“The contract breaks at the edge. What happens with nothing given?”",
        "“You’ve got it. Any function — state the contract, then break it.”",
        "“Try again. Run it on the smallest possible input.”",
    ),
    "code.arrays": block(
        "“An array gives you constant-time access and nothing else — searching it "
        "costs linear time. Know the index arithmetic cold: `len - 1` for the last "
        "element, and a loop that stops one before the end.”",
        [
            "“Nice. The index arithmetic was exact.”",
            "“Clean. You picked access over scan without hesitating.”",
        ],
        [
            "“Stop. You read one past the end.”",
            "“Careful — you searched an array you could have indexed.”",
        ],
        "“The bound is wrong. What is the last valid index?”",
        "“You’ve got it. Any array problem — settle the bounds first.”",
        "“Try again. How many elements, and what’s the last index?”",
    ),
    "code.strings": block(
        "“Strings are just arrays with rules about mutation. Count carefully — "
        "empty string, one character, and repeated characters are the three cases "
        "that break a first solution.”",
        [
            "“Nice. You handled the empty case before it bit you.”",
            "“Clean. Index and character kept separate.”",
        ],
        [
            "“Stop. You assumed the string is non-empty.”",
            "“Careful — you treated it as mutable when it isn’t.”",
        ],
        "“A case is missing. What happens with an empty input?”",
        "“You’ve got it. Any string problem — list the three cases first.”",
        "“Try again. What does it do with zero characters?”",
    ),
    "code.dicts": block(
        "“A dict trades storage for constant-time lookup — that’s the whole deal. "
        "Always ask what happens on a key that isn’t there; the missing-key path "
        "is where most crashes live.”",
        [
            "“Nice. You handled the key that isn’t there.”",
            "“Clean. You used the lookup instead of scanning.”",
        ],
        [
            "“Stop. You read a key that may not exist.”",
            "“Careful — you scanned the whole dict when the lookup was O(1).”",
        ],
        "“The missing-key path isn’t handled. What happens then?”",
        "“You’ve got it. Any dict problem — settle the absent case first.”",
        "“Try again. Is that key guaranteed to be present?”",
    ),
    "code.debugging": block(
        "“Debug by hypothesis, not by poking. Read the first place the output "
        "diverges from expectation, form one guess, print the state there, and let "
        "the evidence decide — changing three things at once tells you nothing.”",
        [
            "“Nice. One hypothesis, one probe, evidence.”",
            "“Clean. You found the first divergence, not the last symptom.”",
        ],
        [
            "“Stop. You changed three lines at once and can’t tell which fixed it.”",
            "“Careful — you’re debugging the symptom, not the first wrong value.”",
        ],
        "“Too many changes. Revert, then probe the first divergence.”",
        "“You’ve got it. That’s debugging as a method, not a mood.”",
        "“Try again. Where is the output first wrong — not merely late?”",
    ),
    "code.sorting": block(
        "“Sorting is about picking the right cost: stable when order matters, "
        "in-place when memory matters, O(n log n) when time matters. Understand "
        "what the algorithm does to equal elements before you reach for it.”",
        [
            "“Nice. You chose the sort for the constraint you had.”",
            "“Clean. Stability was considered, not assumed.”",
        ],
        [
            "“Stop. You sorted when the order of equals would break the answer.”",
            "“Careful — you accepted the complexity without checking the constraint.”",
        ],
        "“This sort changes something you needed preserved. Which?”",
        "“You’ve got it. Any sorting problem — name the constraint first.”",
        "“Try again. Does the order of equal elements matter here?”",
    ),
    "code.complexity": block(
        "“Complexity is a question about growth, not about a stopwatch. Ask how the "
        "work doubles when the input doubles — one loop grows linearly, a nested "
        "loop grows quadratically, halving grows logarithmically.”",
        [
            "“Nice. You counted the growth instead of guessing the constant.”",
            "“Clean. Nested loops, and you called it O(n²) without hesitating.”",
        ],
        [
            "“Stop. You timed it instead of analysing how it scales.”",
            "“Careful — you counted the loop but ignored the work inside it.”",
        ],
        "“What happens when the input doubles? Count the growth again.”",
        "“You’ve got it. I’m removing the training wheels. Any complexity question.”",
        "“Try again. How does the work grow — linearly, quadratically, or by halves?”",
    ),
    "code.input_output": block(
        "“Read the input format before you read anything else — how many values, in "
        "what order, separated by what. Most wrong answers here come from parsing a "
        "shape the problem never promised.”",
        [
            "“Nice. You matched the parser to the stated format.”",
            "“Clean. Exactly the values the input actually contains.”",
        ],
        [
            "“Stop. You assumed one value where the format gives several.”",
            "“Careful — you printed the working, not the answer that was asked for.”",
        ],
        "“The shape doesn’t match the format. Re-read what it promises.”",
        "“You’ve got it. Any I/O problem — read the format first.”",
        "“Try again. How many values, in what order, and what must you print?”",
    ),
    "code.marathon": block(
        "“A marathon is a pacing problem. Solve the ones you convert in ninety "
        "seconds, then spend real time on the ones that need it — the mistake that "
        "sinks people is spending the whole session on one problem that won’t fall.”",
        [
            "“Nice. You banked the converts before chasing the hard one.”",
            "“Clean. Pacing held to the end.”",
        ],
        [
            "“Stop. You spent twenty minutes on one problem and left three untouched.”",
            "“Careful — you rushed the easy ones to reach the hard one.”",
        ],
        "“The pacing is off. What converts fastest right now?”",
        "“You’ve got it. Bank first, chase second.”",
        "“Try again. What’s the next problem that converts in under two minutes?”",
    ),
    "code.mastery": block(
        "“You’ve covered the fundamentals — now prove they hold together: read a "
        "program you haven’t seen, predict it, break it deliberately, and fix it "
        "without me. That’s the actual standard.”",
        [
            "“Nice. You predicted and then defended it.”",
            "“Clean. You broke it on purpose and repaired it on purpose.”",
        ],
        [
            "“Stop. You got the right answer without being able to explain it.”",
            "“Careful — it held on the familiar case and fell on a new one.”",
        ],
        "“It has to survive an unfamiliar case. Where would it break?”",
        "“You’ve got it. Foundations that hold without supervision.”",
        "“Try again. Explain it cold, then break it on purpose.”",
    ),
    # --------------------------------------------------------------------- dsa
    "dsa.two_pointers": block(
        "“Two pointers walk a structure from two ends, or in tandem — and the "
        "answer usually appears when they meet. The real work is naming the "
        "invariant: what must stay true after every single move.”",
        [
            "“Nice. You moved both pointers with a stated invariant.”",
            "“Clean. O(n) instead of the O(n²) you were one step from.”",
        ],
        [
            "“Stop. You fell back to checking every pair.”",
            "“Careful — one pointer moved without the other, and the invariant broke.”",
        ],
        "“The invariant broke. What must be true after every move?”",
        "“You’ve got it. I’m removing the training wheels. Any two-pointer problem.”",
        "“Try again. What does each pointer guarantee — and what does the move preserve?”",
    ),
    "dsa.sliding_window": block(
        "“A sliding window is a moving frame: expand right until the condition "
        "breaks, then shrink from the left. The frame slides — it never restarts "
        "— and that’s exactly why it stays linear.”",
        [
            "“Nice. Expand, then shrink — the window did the work.”",
            "“Clean. The invariant held through the shrink.”",
        ],
        [
            "“Stop. You restarted the window at every right index.”",
            "“Careful — you shrank past the condition instead of to it.”",
        ],
        "“You threw the state away. What can be carried forward instead?”",
        "“You’ve got it. I’m removing the training wheels. Any subarray problem.”",
        "“Try again. Expand until it breaks, then shrink only while it’s broken.”",
    ),
    "dsa.binary_search": block(
        "“Binary search only opens for sorted data. Ask the middle guard which side "
        "the target lives on, discard half, repeat — and keep the loop invariant "
        "explicit or the boundary will eat you.”",
        [
            "“Nice. You halved the space again and again.”",
            "“Clean. O(log n) beats O(n) every time.”",
        ],
        [
            "“Stop. You scanned linearly through sorted data.”",
            "“Careful — you discarded the middle before checking it.”",
        ],
        "“The invariant broke at the boundary. Which half survives, and why?”",
        "“You’ve got it. I’m removing the training wheels. Any sorted-search problem.”",
        "“Try again. Write the invariant, then move exactly one bound.”",
    ),
    "dsa.linked_list": block(
        "“A linked list is a chain — you cannot jump to index i, you walk it. "
        "Save `next` before you overwrite a link, keep `prev` in your hand, and "
        "the reversal becomes a three-step dance you can do by memory.”",
        [
            "“Nice. You saved the next node before breaking the link.”",
            "“Clean. prev, curr, nxt — all three accounted for.”",
        ],
        [
            "“Stop. You lost the rest of the list when you rewired the node.”",
            "“Careful — you treated it like an array and indexed it.”",
        ],
        "“The chain is severed. What did you need before you overwrote it?”",
        "“You’ve got it. I’m removing the training wheels. Any linked-list problem.”",
        "“Try again. Track prev, current, next — in that order.”",
    ),
    "dsa.stack_queue": block(
        "“A stack is last in first out, a queue is first in first out — choosing "
        "the wrong one makes a simple problem unreadable. If you need to undo or "
        "match nesting, reach for a stack; if you need arrival order, a queue.”",
        [
            "“Nice. The structure matched the order the problem needed.”",
            "“Clean. Push and pop from the same end, as designed.”",
        ],
        [
            "“Stop. You’re using a list for everything regardless of order.”",
            "“Careful — you popped from the end while the problem wanted the front.”",
        ],
        "“The order doesn’t fit. Which end does this problem need?”",
        "“You’ve got it. I’m removing the training wheels. Any stack or queue problem.”",
        "“Try again. What order does the problem actually demand?”",
    ),
    "dsa.trees": block(
        "“Tree problems almost always reduce to knowing what each subtree returns. "
        "Pick DFS or BFS from the question — depth questions are DFS, level "
        "questions are BFS — then let the recursion or the queue carry the rest.”",
        [
            "“Nice. You chose traversal from what the question asked.”",
            "“Clean. Each subtree returned exactly what the parent needed.”",
        ],
        [
            "“Stop. You walked level by level when the question wanted depth.”",
            "“Careful — you lost track of what the recursive call gives back.”",
        ],
        "“Wrong traversal for the question. What does it actually need?”",
        "“You’ve got it. I’m removing the training wheels. Any tree problem.”",
        "“Try again. What does one subtree return to its parent?”",
    ),
    "dsa.graphs": block(
        "“Graphs are adjacency and visited. Mark visited the moment you enqueue "
        "or push — not after you pop it — or you’ll process the same node twice "
        "and the queue will never drain.”",
        [
            "“Nice. You marked visited at enqueue, not at pop.”",
            "“Clean. Frontier, visited set, parent map — all held.”",
        ],
        [
            "“Stop. You marked visited too late and enqueued the node twice.”",
            "“Careful — you lost the parent map, so you can’t reconstruct the path.”",
        ],
        "“The frontier isn’t guarded. When does a node count as seen?”",
        "“You’ve got it. I’m removing the training wheels. Any graph problem.”",
        "“Try again. What exactly goes in the visited set, and when?”",
    ),
    "dsa.dp": block(
        "“Dynamic programming is two questions in order: what does the state "
        "represent, and what is it computed from. Write the recurrence and the "
        "base case before a single loop — the code is the easy part afterwards.”",
        [
            "“Nice. Recurrence and base case first, then code.”",
            "“Clean. The state meant something you could defend.”",
        ],
        [
            "“Stop. You started coding before you could say what dp[i] means.”",
            "“Careful — the base case is missing, so the recursion never lands.”",
        ],
        "“The recurrence doesn’t close. What is dp[i] built from, and where does it stop?”",
        "“You’ve got it. I’m removing the training wheels. Any DP problem.”",
        "“Try again. Say what the state means, then write the recurrence.”",
    ),
}

#: Shared voice for any `code.*` or `dsa.*` skill without its own entry.
DOMAIN_PROGRAMMING: Dict[str, Any] = block(
    "“Trace before you predict, and name the invariant before you code it. If you "
    "can’t say what must stay true after each step, you don’t yet have an "
    "algorithm — you have a guess.”",
    [
        "“Nice. The invariant held, step after step.”",
        "“Clean. You defended it instead of hoping.”",
    ],
    [
        "“Stop. You guessed the state instead of tracking it.”",
        "“Careful — the invariant broke and you kept going anyway.”",
    ],
    "“The invariant broke. Which step violated it?”",
    "“You’ve got it. Trace it, name the invariant, then code it.”",
    "“Try again. What must remain true after every single step?”",
)
