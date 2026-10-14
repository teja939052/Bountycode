"""Captain Byte speeches for Company Quests (World 5).

14 skills across 32 levels: company shape → pattern drills → mocks → readiness.
Company-specific lines name the actual paper pattern rather than generic advice.
"""
from typing import Any, Dict

from ._text import block

COMPANY: Dict[str, Dict[str, Any]] = {
    "company.tcs": block(
        "“The TCS NQT is a shape you can learn: quantitative aptitude, verbal, "
        "reasoning, and a coding round that rewards clean basics over clever tricks. "
        "Learn the paper’s order and the time each section actually costs you.”",
        [
            "“Nice. You’re preparing for the paper, not for the brand.”",
            "“Clean. You know which section eats the clock.”",
        ],
        [
            "“Stop. You’re drilling random quant when this paper weights sections differently.”",
            "“Careful — you haven’t checked the current pattern before practising it.”",
        ],
        "“Re-check the pattern. Which section is actually scored how?”",
        "“You’ve got it. That’s the paper in your hands now.”",
        "“Try again. What comes first, and how long do you give it?”",
    ),
    "company.infosys": block(
        "“Infosys InfyTQ leans on fundamentals — clean code, clear reasoning, and "
        "speed on straightforward problems. It punishes over-thinking more than it "
        "rewards sophistication.”",
        [
            "“Nice. You kept it simple and correct.”",
            "“Clean. Fundamentals done fast is exactly this paper.”",
        ],
        [
            "“Stop. You reached for an advanced approach on a fundamentals question.”",
            "“Careful — you over-complicated it and ran out of time.”",
        ],
        "“That was over-engineered. Strip it back to the basics.”",
        "“You’ve got it. Simple, correct, quick — that’s the whole paper.”",
        "“Try again. What’s the plainest version that works?”",
    ),
    "company.wipro": block(
        "“Wipro NLTH tests whether your fundamentals survive under time. The "
        "questions are usually not hard — there are just a lot of them, and the "
        "clock is the real examiner.”",
        [
            "“Nice. You converted the easy marks first.”",
            "“Clean. Pacing, not panic.”",
        ],
        [
            "“Stop. You spent four minutes on a question worth one mark.”",
            "“Careful — you didn’t triage. Skip, mark, return.”",
        ],
        "“Park it and move. Bank what converts, then come back.”",
        "“You’ve got it. You beat the clock by triaging, not by rushing.”",
        "“Try again. Which questions do you take first?”",
    ),
    "company.accenture": block(
        "“Accenture’s AMCAT-style round is broad and unspectacular — aptitude, "
        "logical, verbal, and a coding round. Breadth beats depth here: nothing "
        "can be left cold.”",
        [
            "“Nice. You kept every section warm, not just your favourite.”",
            "“Clean. Breadth covered, no cold section.”",
        ],
        [
            "“Stop. You only prepared the section you already liked.”",
            "“Careful — one cold section can sink an otherwise fine score.”",
        ],
        "“That section has gone cold. Rebuild the basics before the mock.”",
        "“You’ve got it. Broad, even, and ready.”",
        "“Try again. Which section is weakest when you test it cold?”",
    ),
    "company.cognizant": block(
        "“Cognizant’s round rewards people who can read a problem, pick a method, "
        "and finish it — under a clock that doesn’t care how close you were.”",
        [
            "“Nice. You chose a method and finished it.”",
            "“Clean. Decided quickly, executed fully.”",
        ],
        [
            "“Stop. You changed method halfway and lost the thread.”",
            "“Careful — you left a started question unfinished and gained nothing.”",
        ],
        "“Half-finished gains nothing. Either complete it or move on sooner.”",
        "“You’ve got it. Decide, then finish.”",
        "“Try again. Commit to the method in the first ten seconds.”",
    ),
    "company.capgemini": block(
        "“Capgemini leans on logical reasoning and game-based aptitude — pattern "
        "recognition under time, not lengthy calculation. Train recognition speed, "
        "not arithmetic depth.”",
        [
            "“Nice. You recognised the pattern instead of computing it.”",
            "“Clean. Fast read, right call.”",
        ],
        [
            "“Stop. You’re calculating something you should have recognised.”",
            "“Careful — you treated a recognition task as a maths task.”",
        ],
        "“Slow down the recognition step. What’s the pattern underneath?”",
        "“You’ve got it. Recognise first, compute last.”",
        "“Try again. Name the pattern before you touch the numbers.”",
    ),
    "company.patterns": block(
        "“A pattern drill is not a quiz — it’s a rehearsal of a repeated shape. "
        "Run it until the shape is recognised on sight, then verify it still holds "
        "when the numbers change.”",
        [
            "“Nice. The shape registered before the maths.”",
            "“Clean. Same pattern, different numbers, same result.”",
        ],
        [
            "“Stop. You learned the answer, not the pattern.”",
            "“Careful — change the numbers and it fell apart.”",
        ],
        "“It only works on that exact instance. Extract the pattern.”",
        "“You’ve got it. The shape is yours now.”",
        "“Try again. What stays the same when the numbers change?”",
    ),
    "company.mock": block(
        "“A company mock is a full dress rehearsal: the real section order, the "
        "real time limits, no pauses. Take it cold, then spend twice as long on "
        "the review as on the paper.”",
        [
            "“Nice. You ran it cold and reviewed it properly.”",
            "“Clean. The review found more than the paper did.”",
        ],
        [
            "“Stop. You paused the clock to finish a question.”",
            "“Careful — you checked the score but never the errors.”",
        ],
        "“That run isn’t representative. Re-run it unpaused, then review.”",
        "“You’ve got it. That’s the company paper, respected.”",
        "“Try again. Which errors repeat across the last two mocks?”",
    ),
    "company.topics": block(
        "“‘Most asked’ is a prioritisation tool, not a syllabus. Cover the high "
        "frequency topics first because they buy the most marks per hour — but a "
        "pattern you can’t yet recognise is still a gap.”",
        [
            "“Nice. You prioritised by marks per hour.”",
            "“Clean. High-frequency topics, then the rest.”",
        ],
        [
            "“Stop. You’re treating ‘most asked’ as the entire syllabus.”",
            "“Careful — you skipped the low-frequency topic that keeps appearing.”",
        ],
        "“The priority list isn’t the whole map. What did you rule out?”",
        "“You’ve got it. Efficient coverage, not lucky coverage.”",
        "“Try again. Which topic gives the most marks for the next hour?”",
    ),
    "company.speed": block(
        "“Company rounds are won in the seconds you don’t waste — recognising the "
        "question type, rejecting two options immediately, and only then doing "
        "arithmetic.”",
        [
            "“Nice. Two options gone before you computed.”",
            "“Clean. The seconds came back at the end.”",
        ],
        [
            "“Stop. You computed in full before eliminating anything.”",
            "“Careful — fast clicks, slow thinking. Reverse that.”",
        ],
        "“Eliminate first, compute second. Reset your order.”",
        "“You’ve got it. Speed from method, not from nerves.”",
        "“Try again. Which option can you rule out immediately?”",
    ),
    "company.repair": block(
        "“Company weakness repair means fixing the exact pattern this company "
        "keeps testing — not doing more of everything. Find the recurring miss, "
        "repair it, then re-run that company’s paper.”",
        [
            "“Nice. You repaired the recurring miss specifically.”",
            "“Clean. The re-run proved it actually closed.”",
        ],
        [
            "“Stop. You did a general revision instead of fixing this pattern.”",
            "“Careful — you moved to a new topic before closing this one.”",
        ],
        "“The gap is still open. Which pattern keeps breaking?”",
        "“You’ve got it. That pattern is closed until the next mock says otherwise.”",
        "“Try again. Re-run the company paper and check the same error.”",
    ),
    "company.prep": block(
        "“Company-specific prep is about fit: their format, their favourite topics, "
        "their time budget. General preparation gets you competent; fit gets you "
        "through.”",
        [
            "“Nice. Your prep matches their format now.”",
            "“Clean. You practised the way they actually test.”",
        ],
        [
            "“Stop. You’re practising in a format this company doesn’t use.”",
            "“Careful — good prep, wrong paper.”",
        ],
        "“Mismatch. Rebuild the practice around their real format.”",
        "“You’ve got it. Fit is what converts preparation into an offer.”",
        "“Try again. What does this company actually put in front of you?”",
    ),
    "company.readiness": block(
        "“Readiness for a specific company is evidence, not confidence: you’ve "
        "passed their paper shape under their clock, twice, with the same result. "
        "Anything less is optimism.”",
        [
            "“Nice. Two clean runs under their conditions.”",
            "“Clean. Same outcome twice — that’s evidence.”",
        ],
        [
            "“Stop. You’re calling one lucky run readiness.”",
            "“Careful — it worked with their clock paused.”",
        ],
        "“One run isn’t evidence. Repeat it under their conditions.”",
        "“You’ve got it. Ready for this company specifically.”",
        "“Try again. Cold, their clock, their paper — hold the result.”",
    ),
    "company.mastery": block(
        "“This company’s shape is yours now. The pattern reads instantly, the time "
        "budget holds, and the review finds little left. Prove it once more with "
        "nothing to lean on.”",
        [
            "“Nice. The shape is recognised before the question finishes loading.”",
            "“Clean. Held under their clock with room to spare.”",
        ],
        [
            "“Stop. The standard slipped now that you feel finished.”",
            "“Careful — you coasted on the previous run.”",
        ],
        "“Not done yet. Run it once more, unassisted.”",
        "“You’ve got it. Company ready — go take the paper.”",
        "“Try again. One clean run on their format, their clock.”",
    ),
    "company.customer_obsession": block(
        "“Customer obsession means starting from the customer’s problem and working "
        "backwards — not from the feature you wanted to build. When two options "
        "are close, the one that removes more of the customer’s friction wins.”",
        [
            "“Nice. You started from their problem, not from your idea.”",
            "“Clean. The decision was justified by the customer, not the roadmap.”",
        ],
        [
            "“Stop. That argues from what’s interesting to build.”",
            "“Careful — you named the customer but never said what they were stuck on.”",
        ],
        "“What is the customer actually blocked on? Start there.”",
        "“You’ve got it. Backwards from the customer, every time.”",
        "“Try again. What does the customer gain, and how would you know?”",
    ),
    "company.star_method": block(
        "“STAR is a spine, not a script: Situation and Task in one sentence each, "
        "Action taking the bulk with *you* as the subject, and a Result that "
        "carries a number. Interviewers decide within thirty seconds whether "
        "your example is real.”",
        [
            "“Nice. Short setup, your action, a number at the end.”",
            "“Clean. That example could only have happened to you.”",
        ],
        [
            "“Stop. The action was entirely ‘we’, so your contribution vanished.”",
            "“Careful — you finished the story with no measurable result.”",
        ],
        "“Rebalance it: cut the setup, put yourself in the action, add the result.”",
        "“You’ve got it. A STAR that actually holds under follow-up.”",
        "“Try again. What was your part, and what changed because of it?”",
    ),
    "company.amazon": block(
        "“Leadership principles are decision tools, not vocabulary to sprinkle on "
        "answers. Pick the principle that actually forced a hard choice, describe "
        "what it cost you, and say what you’d do differently — that’s the shape "
        "they’re listening for.”",
        [
            "“Nice. The principle genuinely decided something hard.”",
            "“Clean. You admitted the cost instead of only the win.”",
        ],
        [
            "“Stop. You dropped the vocabulary in without a decision behind it.”",
            "“Careful — every answer claimed success with no trade-off anywhere.”",
        ],
        "“Which principle forced the trade-off, and what did it cost?”",
        "“You’ve got it. Principle, decision, cost, result.”",
        "“Try again. Where did applying it actually hurt?”",
    ),
}

#: Shared voice for any `company.*` skill without its own entry.
DOMAIN_COMPANY: Dict[str, Any] = block(
    "“Learn the paper before you practise it. Every company has a format, a set "
    "of high-frequency topics, and a time budget — match all three and ordinary "
    "preparation starts converting.”",
    [
        "“Nice. Your practice now matches their format.”",
        "“Clean. You prepared for the paper that actually exists.”",
    ],
    [
        "“Stop. You’re drilling a format this company doesn’t use.”",
        "“Careful — strong effort, aimed at the wrong exam.”",
    ],
    "“The format doesn’t match. Rebuild the practice around their real paper.”",
    "“You’ve got it. Fit is what turns effort into an offer.”",
    "“Try again. What does this company actually put in front of you?”",
)
