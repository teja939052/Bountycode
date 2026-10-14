"""Captain Byte speeches for Interview Arena (World 6).

14 skills across 44 levels — the largest world. Technical, HR, behavioural,
stress, mock, and the readiness capstone.

The voice here is deliberately about *delivery under pressure*, not about
subject knowledge: an interviewer rewards a structured answer spoken calmly
far more than a correct answer delivered as a wall of words.
"""
from typing import Any, Dict

from ._text import block

INTERVIEW: Dict[str, Dict[str, Any]] = {
    "interview.intro": block(
        "“‘Tell me about yourself’ is a ninety-second structured pitch, not a "
        "biography. Present → past → future: what you do now, what you did that "
        "relevantly proves it, and why you’re sitting here. End pointed at the role.”",
        [
            "“Nice. Present, past, future — and it landed on the role.”",
            "“Clean. Ninety seconds, and every sentence earned its place.”",
        ],
        [
            "“Stop. You narrated your whole history from school onward.”",
            "“Careful — you finished on your past instead of on why you want this.”",
        ],
        "“Rebuild it: where you are now, the proof, then why here.”",
        "“You’ve got it. That pitch works cold, in any room.”",
        "“Try again. Cut it to ninety seconds and point it at the role.”",
    ),
    "interview.self": block(
        "“Strengths need evidence; weaknesses need a repair already underway. "
        "Never pick a humble-brag for either — an interviewer has heard ‘I’m a "
        "perfectionist’ a thousand times and discounts everything after it.”",
        [
            "“Nice. Real strength, real evidence behind it.”",
            "“Clean. A weakness you’re actually doing something about.”",
        ],
        [
            "“Stop. That strength has no example attached to it.”",
            "“Careful — that’s a humble-brag, and it reads as evasive.”",
        ],
        "“Swap it for something true and bring the example with it.”",
        "“You’ve got it. Honest, evidenced, and not rehearsed-sounding.”",
        "“Try again. Where’s the proof — and what changed because of it?”",
    ),
    "interview.motivation": block(
        "“‘Why this role’ is answered with the work itself — what you’d actually "
        "spend your days doing and why that appeals — not with salary or brand. "
        "Tie it to something you’ve already done that predicts you’ll enjoy it.”",
        [
            "“Nice. You talked about the work, not the perks.”",
            "“Clean. Your past behaviour predicted this interest.”",
        ],
        [
            "“Stop. You described the title, not the day-to-day.”",
            "“Careful — the answer was about status, not about the work.”",
        ],
        "“What would you actually be doing all day, and why do you want that?”",
        "“You’ve got it. That answer sounds like conviction, not preparation.”",
        "“Try again. Anchor it to something you’ve already chosen to do.”",
    ),
    "interview.company": block(
        "“‘Why this company’ needs a specific, checkable reason — a product, a "
        "decision they made, a problem in their domain you find interesting. "
        "Generic praise tells the interviewer you sent the same answer everywhere.”",
        [
            "“Nice. Specific enough that I know you looked.”",
            "“Clean. That reason only fits this company.”",
        ],
        [
            "“Stop. That answer would fit any company on earth.”",
            "“Careful — you praised the brand, not anything they actually do.”",
        ],
        "“Too generic. Find one thing only this company would make you say.”",
        "“You’ve got it. That answer couldn’t belong to another applicant.”",
        "“Try again. What did they do that made you look them up?”",
    ),
    "interview.hr": block(
        "“HR scenarios are testing judgement and self-awareness, not the ‘right’ "
        "answer. State the situation, the constraint you were under, the choice "
        "you made, and what you’d refine — the reasoning is the answer.”",
        [
            "“Nice. You showed the judgement behind the choice.”",
            "“Clean. You admitted the refinement without undermining yourself.”",
        ],
        [
            "“Stop. You gave the textbook answer with no trade-off in it.”",
            "“Careful — you claimed you’d do it all perfectly. Nobody believes that.”",
        ],
        "“Where’s the tension? Real answers have one.”",
        "“You’ve got it. Considered, honest, and defensible.”",
        "“Try again. What was the constraint, and what did it cost you?”",
    ),
    "interview.behavioral": block(
        "“STAR, held to time: Situation one sentence, Task one sentence, Action the "
        "bulk, Result with a number. Interviewers stop listening after thirty "
        "seconds of scene-setting — spend them on what you did.”",
        [
            "“Nice. Short setup, long action, number at the end.”",
            "“Clean. That’s a STAR that actually holds its shape.”",
        ],
        [
            "“Stop. Forty seconds of context and I still don’t know what you did.”",
            "“Careful — you used ‘we’ throughout. Where were *you* in it?”",
        ],
        "“Rebalance it: cut the setup, expand the action, add the result.”",
        "“You’ve got it. Structured, specific, and yours.”",
        "“Try again. One sentence each for situation and task, then action.”",
    ),
    "interview.stress": block(
        "“A stress interview is testing composure, not correctness. Slow down, "
        "answer the actual question asked rather than the one you feared, and "
        "treat disagreement as a discussion — silence is a tool you’re allowed "
        "to use.”",
        [
            "“Nice. You stayed deliberate when the pressure rose.”",
            "“Clean. You answered the question that was asked, not the one you expected.”",
        ],
        [
            "“Stop. You started defending instead of answering.”",
            "“Careful — you filled the silence because it felt awkward.”",
        ],
        "“Reset. What was the question actually asking you?”",
        "“You’ve got it. Calm under pressure reads as experience.”",
        "“Try again. Take a beat before you answer — it costs nothing.”",
    ),
    "interview.project": block(
        "“Explain your project like a system, not a tutorial: the problem it "
        "solves, the one decision that was hard, what you’d rebuild with more "
        "time, and the number that proves it worked. Know your own code cold.”",
        [
            "“Nice. You led with the problem, not the tech stack.”",
            "“Clean. You knew exactly where your own code was weakest.”",
        ],
        [
            "“Stop. You listed frameworks instead of explaining decisions.”",
            "“Careful — you couldn’t say what you’d do differently.”",
        ],
        "“Name the hard decision and what you’d change now.”",
        "“You’ve got it. That explanation holds up under follow-ups.”",
        "“Try again. What breaks first if this gets a thousand users?”",
    ),
    "interview.technical": block(
        "“Technical questions are scored on reasoning out loud. State your "
        "assumptions, choose an approach and say why, then implement. A partially "
        "correct answer with clear thinking beats a silent correct one every time.”",
        [
            "“Nice. You narrated the reasoning, not just the code.”",
            "“Clean. You stated the assumption before you used it.”",
        ],
        [
            "“Stop. You jumped to implementation before choosing an approach.”",
            "“Careful — you solved it, but I can’t tell why you chose that.”",
        ],
        "“Say the approach and the reason before you write anything.”",
        "“You’ve got it. Any technical question — reason out loud.”",
        "“Try again. What are you assuming, and what happens if it’s false?”",
    ),
    "interview.mock": block(
        "“A mock technical round exists to find the failure while it’s cheap. Run "
        "it cold, keep the clock honest, and afterwards spend longer on where you "
        "hesitated than on where you were right.”",
        [
            "“Nice. You found a real failure in a cheap setting.”",
            "“Clean. The review focused on hesitation, not on the score.”",
        ],
        [
            "“Stop. You looked up the answer mid-round.”",
            "“Careful — you rehearsed it warm, so it told you nothing.”",
        ],
        "“Run it cold next time, or the mock can’t find anything real.”",
        "“You’ve got it. That hesitation is now something you can fix.”",
        "“Try again. Where did you stall — and what would unstick it?”",
    ),
    "interview.full": block(
        "“A full mock is the whole arc under real conditions: introduction, "
        "technical, behavioural, and the questions you ask them at the end. "
        "Score the transitions too — most people lose the room between sections.”",
        [
            "“Nice. You carried the thread across all the sections.”",
            "“Clean. And your closing questions were genuinely good.”",
        ],
        [
            "“Stop. You reset to zero at every section boundary.”",
            "“Careful — you had no questions for them, and it showed.”",
        ],
        "“The transitions dropped. Connect the sections instead of restarting.”",
        "“You’ve got it. The whole arc, held together.”",
        "“Try again. End with a question that proves you were listening.”",
    ),
    "interview.communication": block(
        "“Communication is structure made audible: signpost what you’re about to "
        "say, say it, then summarise. Speak in two or three sentence units, land "
        "your point, and stop talking — the pause is where they ask the next one.”",
        [
            "“Nice. Signpost, point, stop. Easy to follow.”",
            "“Clean. You finished the answer instead of trailing off.”",
        ],
        [
            "“Stop. Three ideas in one breath with no signposts.”",
            "“Careful — you kept going after the answer was already given.”",
        ],
        "“Restructure it: say what you’ll say, say it, then stop.”",
        "“You’ve got it. That reads as someone who thinks in order.”",
        "“Try again. Land the point in two sentences, then stop.”",
    ),
    "interview.readiness": block(
        "“Readiness is behavioural evidence: you answer the same question cold on "
        "a bad day with the same structure, and you recover from a follow-up "
        "without flinching. This check asks whether that’s true yet.”",
        [
            "“Nice. Same structure, cold, second attempt.”",
            "“Clean. The follow-up didn’t knock it over.”",
        ],
        [
            "“Stop. It only held while you were still warm from practising.”",
            "“Careful — you recovered by guessing instead of by reasoning.”",
        ],
        "“It isn’t holding cold. Which part collapses first?”",
        "“You’ve got it. That’s readiness, not hope.”",
        "“Try again. Cold, no notes, and take the follow-up head-on.”",
    ),
    "interview.mastery": block(
        "“This is the last rehearsal. Everything now runs without scaffolding: the "
        "pitch, the technical reasoning, the STAR, the composure. Deliver one full "
        "pass alone, then you’re done rehearsing.”",
        [
            "“Nice. The whole pass, unassisted and intact.”",
            "“Clean. Held together when the questions changed on you.”",
        ],
        [
            "“Stop. You coasted on the earlier reps.”",
            "“Careful — the standard slipped exactly when you felt finished.”",
        ],
        "“Not yet. It has to hold once more without the safety net.”",
        "“You’ve got it. Interview ready — go take the room.”",
        "“Try again. One complete, unassisted pass.”",
    ),
    # ------------------------------------------- OA / coding-round behaviours
    "interview.pattern_recognition": block(
        "“Before you solve, classify. Naming the pattern — sliding window, "
        "two-pointer, BFS, backtracking — decides which tool you pick; solving "
        "first and naming afterwards is how you end up with a brute force you "
        "can’t improve.”",
        [
            "“Nice. You named the pattern, then reached for the right tool.”",
            "“Clean. Classification first, and the solution followed.”",
        ],
        [
            "“Stop. You started coding before you knew what kind of problem it was.”",
            "“Careful — you saw a familiar shape and assumed the rest matched.”",
        ],
        "“What pattern is this? Say it before you write anything.”",
        "“You’ve got it. Any problem — classify, then solve.”",
        "“Try again. If you had to teach this shape to someone, what would you call it?”",
    ),
    "interview.optimization": block(
        "“Optimize from a measurement, not a feeling. Establish the baseline, find "
        "where the time actually goes, change one thing, then measure again — "
        "otherwise you’ve traded one unknown cost for another.”",
        [
            "“Nice. You measured before you changed anything.”",
            "“Clean. One change, then the number told you if it worked.”",
        ],
        [
            "“Stop. You rewrote it and hoped it got faster.”",
            "“Careful — you optimized the part that wasn’t the bottleneck.”",
        ],
        "“Where is the time actually going? Find the bottleneck first.”",
        "“You’ve got it. Measure, change one thing, measure again.”",
        "“Try again. What’s your baseline, and which step dominates it?”",
    ),
    "interview.oa": block(
        "“An online assessment is triage under a clock: read every question, bank "
        "the ones you convert fast, and return to the hard one with time still on "
        "the board. The candidate who solves three of four beats the one who "
        "perfects one.”",
        [
            "“Nice. You banked the converts before chasing the last one.”",
            "“Clean. Time left on the board at the end.”",
        ],
        [
            "“Stop. You spent half the paper on the first question.”",
            "“Careful — you left two convertible questions untouched.”",
        ],
        "“What still converts quickly? Take those before this one.”",
        "“You’ve got it. Triage first, then depth.”",
        "“Try again. Which question gives the most marks in the next five minutes?”",
    ),
    "interview.clarification": block(
        "“Asking one clarifying question costs ten seconds and saves twenty "
        "minutes. State your assumptions out loud, confirm the edge cases, and "
        "the interviewer will steer you before you build the wrong thing.”",
        [
            "“Nice. You confirmed the contract before you designed it.”",
            "“Clean. One question and the ambiguity was gone.”",
        ],
        [
            "“Stop. You assumed the constraints and built on them silently.”",
            "“Careful — you asked a question the prompt had already answered.”",
        ],
        "“What’s still ambiguous? Ask before you commit to an approach.”",
        "“You’ve got it. Clarify first — it reads as rigour, not hesitation.”",
        "“Try again. What must be true for your approach to work?”",
    ),
    "interview.thinking_aloud": block(
        "“Narrate your reasoning so the interviewer can follow it. Silence looks "
        "like being stuck; a spoken trail of partial ideas looks like someone "
        "working — and lets them rescue you long before you go down the wrong path.”",
        [
            "“Nice. I could follow every step you took.”",
            "“Clean. You said the trade-off out loud before choosing.”",
        ],
        [
            "“Stop. You went quiet and I had no way to know if you were lost.”",
            "“Careful — you solved it privately, then announced the answer.”",
        ],
        "“Say it out loud. What are you considering, and why this one?”",
        "“You’ve got it. Reasoning shown beats a correct answer delivered silently.”",
        "“Try again. Talk me through it from the very first thought.”",
    ),
    "interview.testing": block(
        "“Test on paper before you run it: normal case, empty case, one element, "
        "huge input, duplicate values. Pick your examples deliberately — they "
        "should be chosen to break your approach, not to confirm it.”",
        [
            "“Nice. Your examples were chosen to break it, and they did.”",
            "“Clean. Empty case caught it before the interviewer did.”",
        ],
        [
            "“Stop. You ran only the example the prompt handed you.”",
            "“Careful — you tested the happy path and called it verified.”",
        ],
        "“Give me an input designed to break this.”",
        "“You’ve got it. Any solution — try to disprove it first.”",
        "“Try again. What’s the smallest input, and the nastiest one?”",
    ),
    "interview.coding": block(
        "“Out loud, in this order: restate the problem, name the approach and why, "
        "write it, then test it on an edge case. A clean run through that sequence "
        "scores higher than a silent correct answer written at speed.”",
        [
            "“Nice. Approach stated, code written, edge case tested.”",
            "“Clean. The whole sequence, in order, without prompting.”",
        ],
        [
            "“Stop. You started typing before you’d chosen an approach.”",
            "“Careful — you finished but never tested it yourself.”",
        ],
        "“Stop. Restate it, choose an approach, then code.”",
        "“You’ve got it. The full sequence, unassisted.”",
        "“Try again. What’s the approach, and why this one over the obvious one?”",
    ),
}

#: Shared voice for any `interview.*` skill without its own entry.
DOMAIN_INTERVIEW: Dict[str, Any] = block(
    "“Interviewers reward structure spoken calmly. State your approach in one "
    "line, give the reasoning in two or three sentences, then stop and let them "
    "come to you — clarity reads as competence.”",
    [
        "“Nice. Structured, spoken plainly, and it landed.”",
        "“Clean. You stopped at the right moment instead of over-explaining.”",
    ],
    [
        "“Stop. You gave the answer with no structure around it.”",
        "“Careful — you kept talking after the point was made.”",
    ],
    "“Restructure it: approach first, reasoning second, then stop.”",
    "“You’ve got it. That’s how a strong answer sounds.”",
    "“Try again. Signpost it, land it, and stop.”",
)
