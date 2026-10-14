"""Captain Byte speeches for CS Core (World 4).

7 skills across 23 levels: OOP, DBMS, SQL, OS, CN, plus the mock and capstone.
These are the subjects service-company written rounds actually ask — the voice
is about explaining precisely, because that's what interviews demand.
"""
from typing import Any, Dict

from ._text import block

CS_CORE: Dict[str, Dict[str, Any]] = {
    "cs_fundamentals.oops": block(
        "“OOP is four ideas doing real work: encapsulation hides state, inheritance "
        "reuses behaviour, polymorphism lets one call do different things, and "
        "abstraction hides the how. Name which one a design uses, and why.”",
        [
            "“Nice. You named the principle, not just the keyword.”",
            "“Clean. That distinction would land in an interview.”",
        ],
        [
            "“Stop. You called everything ‘inheritance’.”",
            "“Careful — you described the syntax, not what problem it solves.”",
        ],
        "“Which of the four principles is actually at work here?”",
        "“You’ve got it. Any OOP question — name the principle first.”",
        "“Try again. What does this design buy you, and what does it cost?”",
    ),
    "cs_fundamentals.sql": block(
        "“SQL reads as a sequence of operations: FROM and JOIN build the rows, "
        "WHERE filters them, GROUP BY folds them, HAVING filters the groups, and "
        "SELECT names what survives. Order matters more than keywords.”",
        [
            "“Nice. You walked the clauses in execution order.”",
            "“Clean. HAVING after GROUP BY, exactly right.”",
        ],
        [
            "“Stop. You filtered an aggregate in WHERE — it doesn’t exist yet.”",
            "“Careful — you grouped once and expected two different totals.”",
        ],
        "“The clause is in the wrong stage. Rebuild the execution order.”",
        "“You’ve got it. Any SQL question — walk the clauses in order.”",
        "“Try again. Which rows exist when this condition runs?”",
    ),
    "cs_fundamentals.dbms": block(
        "“DBMS questions are about guarantees: transactions give you ACID, "
        "normalisation removes redundancy without losing facts, and indexes trade "
        "write cost for read speed. Always answer in terms of what is guaranteed.”",
        [
            "“Nice. You answered with the guarantee, not the acronym.”",
            "“Clean. You named the trade-off as well as the benefit.”",
        ],
        [
            "“Stop. You listed ACID without saying what any of it prevents.”",
            "“Careful — you recommended an index on a write-heavy table with no downside noted.”",
        ],
        "“What exactly is guaranteed here, and at what cost?”",
        "“You’ve got it. Any DBMS question — state the guarantee first.”",
        "“Try again. What breaks if this property doesn’t hold?”",
    ),
    "cs_fundamentals.os": block(
        "“The OS is a set of scheduling and isolation decisions: processes versus "
        "threads, how the CPU context-switches, how memory is virtualised, and how "
        "two things avoid deadlocking. Explain the mechanism, not the definition.”",
        [
            "“Nice. You explained the mechanism end to end.”",
            "“Clean. You named the condition that makes it fail.”",
        ],
        [
            "“Stop. You gave the textbook definition with no mechanism behind it.”",
            "“Careful — you listed the deadlock conditions but not why they must all hold.”",
        ],
        "“Definitions don’t score. Walk me through what actually happens.”",
        "“You’ve got it. Any OS question — describe the mechanism.”",
        "“Try again. Step through it: what happens next, and who decides?”",
    ),
    "cs_fundamentals.cn": block(
        "“Networking answers are about layers and delivery: which layer does what, "
        "what happens when a packet is lost, and how two machines agree on anything "
        "at all. Name the layer, then name the guarantee.”",
        [
            "“Nice. You put the responsibility on the right layer.”",
            "“Clean. You explained the handshake, not just the acronym.”",
        ],
        [
            "“Stop. You’re blaming the wrong layer for this failure.”",
            "“Careful — you said ‘it retries’ without saying who retries and when.”",
        ],
        "“Wrong layer, or no mechanism. Which one is it?”",
        "“You’ve got it. Any CN question — layer first, guarantee second.”",
        "“Try again. Who detects the loss, and who recovers from it?”",
    ),
    "cs_fundamentals.mock": block(
        "“A CS mock mixes subjects deliberately, so you have to switch context under "
        "time — exactly like the real paper. Score it by subject afterwards; that "
        "breakdown is the only useful output.”",
        [
            "“Nice. You switched subjects without losing the thread.”",
            "“Clean. The per-subject breakdown tells you where to go next.”",
        ],
        [
            "“Stop. You took one subject’s notes into the mock.”",
            "“Careful — you read the total score and ignored which subject sank it.”",
        ],
        "“That score isn’t usable. Break it down by subject and find the sink.”",
        "“You’ve got it. Mixed under time, and it held.”",
        "“Try again. Which subject cost you the most marks?”",
    ),
    "cs_fundamentals.mastery": block(
        "“You’ve covered the subjects — now prove they survive out of order, with "
        "no notes and a follow-up question. Interviewers push until the definition "
        "cracks; make sure the mechanism underneath it doesn’t.”",
        [
            "“Nice. That held under the follow-up.”",
            "“Clean. You explained it, not just recited it.”",
        ],
        [
            "“Stop. It worked until I asked why.”",
            "“Careful — the definition is memorised, the mechanism isn’t.”",
        ],
        "“It cracked on the follow-up. Rebuild the mechanism underneath.”",
        "“You’ve got it. CS core, interview-proofed.”",
        "“Try again. Now tell me why — and what happens when it fails.”",
    ),
}

#: Shared voice for any `cs_fundamentals.*` skill without its own entry.
DOMAIN_CS: Dict[str, Any] = block(
    "“Explain the mechanism, not the definition. Every CS question scores on "
    "what actually happens and what breaks when it doesn’t — so name the "
    "guarantee, then name the cost.”",
    [
        "“Nice. You explained what happens, not just what it’s called.”",
        "“Clean. The guarantee and the trade-off, both named.”",
    ],
    [
        "“Stop. That’s the textbook line with nothing underneath it.”",
        "“Careful — you named the feature but not what it prevents.”",
    ],
    "“Definitions don’t score. Walk me through the mechanism.”",
    "“You’ve got it. Any CS question — mechanism first.”",
    "“Try again. What actually happens, and what breaks if it doesn’t?”",
)
