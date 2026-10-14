"""Captain Byte speeches for Placement Readiness (World 1).

17 skills across 32 levels: diagnostic → plan → practice → repair → ready.
This world runs before any subject matter, so the voice is about operating the
campaign itself, not about a topic.
"""
from typing import Any, Dict

from ._text import block

PLACEMENT: Dict[str, Dict[str, Any]] = {
    "placement.basics": block(
        "“Placement isn’t a test of who knows the most — it’s a test of who can "
        "produce it on a clock, in a room, after a night of bad sleep. We’re going "
        "to build that deliberately.”",
        [
            "“Nice. You know what you’re actually preparing for.”",
            "“Clean. Target set. Everything else hangs off this.”",
        ],
        [
            "“Stop. Vague goals produce vague preparation.”",
            "“Careful — you’re preparing for ‘a job’, not for a specific round.”",
        ],
        "“The target isn’t defined yet. Name the company and the round.”",
        "“You’ve got it. The goal is set. Now we build towards it.”",
        "“Try again. Who are you preparing for, and what do they test?”",
    ),
    "placement.company": block(
        "“Every company has a shape — a pattern of rounds, a favourite set of "
        "topics, a time limit. Learn the shape first and you stop preparing for "
        "an imaginary exam.”",
        [
            "“Nice. You chose a company whose pattern you can actually target.”",
            "“Clean. That choice changes what you practise from now on.”",
        ],
        [
            "“Stop. You picked a company without checking what it tests.”",
            "“Careful — you’re comparing salary, not rounds.”",
        ],
        "“Pick again. What does this company actually put in front of you?”",
        "“You’ve got it. Target locked. That filters everything downstream.”",
        "“Try again. Which rounds come first for this company?”",
    ),
    "placement.date": block(
        "“A date turns a wish into a schedule. Work backwards from it — the number "
        "of weeks decides how deep you go, and which weaknesses you must fix first "
        "versus which you can afford to leave.”",
        [
            "“Nice. The date now decides your priorities.”",
            "“Clean. Enough runway to fix what matters.”",
        ],
        [
            "“Stop. That date leaves no room for repair cycles.”",
            "“Careful — you counted weeks, not usable study hours.”",
        ],
        "“The timeline doesn’t work. Either move the date or cut the scope.”",
        "“You’ve got it. The clock is running in your favour now.”",
        "“Try again. How many usable hours does that leave per topic?”",
    ),
    "placement.diagnostic": block(
        "“A diagnostic is not there to embarrass you. It exists so we stop guessing "
        "and find out which topics are actually missing versus which ones you just "
        "haven’t practised under time.”",
        [
            "“Nice. You took it honestly instead of coached.”",
            "“Clean. Now we have real numbers to work from.”",
        ],
        [
            "“Stop. You’re guessing answers instead of attempting them.”",
            "“Careful — you skipped questions you knew, to protect the score.”",
        ],
        "“The result isn’t usable. Attempt honestly — a low real score beats a fake one.”",
        "“You’ve got it. That’s a baseline I can plan against.”",
        "“Try again. Attempt what you can and show me the pattern.”",
    ),
    "placement.baseline": block(
        "“This number is not your worth — it’s your starting position. Baselines "
        "are only useful when they’re honest, because every plan built on an "
        "inflated one fails in week two.”",
        [
            "“Nice. You accepted the number instead of arguing with it.”",
            "“Clean. That’s a baseline you can measure progress against.”",
        ],
        [
            "“Stop. You’re reading this as a verdict, not a position.”",
            "“Careful — you want to re-take it until it looks better.”",
        ],
        "“Don’t re-test to feel better. The first honest attempt is the usable one.”",
        "“You’ve got it. Position known. Now the movement matters.”",
        "“Try again. What does this number say you should fix first?”",
    ),
    "placement.weakness": block(
        "“Weaknesses are only useful once they’re named precisely. ‘I’m bad at "
        "quant’ is useless; ‘I lose four minutes on every DI set because I don’t "
        "read the question first’ is a fix. Get specific.”",
        [
            "“Nice. That’s specific enough to act on.”",
            "“Clean. You named the behaviour, not the feeling.”",
        ],
        [
            "“Stop. That’s a topic label, not a diagnosis.”",
            "“Careful — you blamed the subject instead of the step you skip.”",
        ],
        "“Too vague. What exactly goes wrong, and when?”",
        "“You’ve got it. A named weakness is already half fixed.”",
        "“Try again. Describe the actual failure, not the category.”",
    ),
    "placement.planning": block(
        "“A plan is a priority order with hours attached, not a wish list. Put "
        "weakness repair first, keep fresh skills warm second, and leave slack — "
        "because something always takes longer than planned.”",
        [
            "“Nice. Repair sits at the top, where it belongs.”",
            "“Clean. There’s slack in there for the week that goes badly.”",
        ],
        [
            "“Stop. You planned by interest, not by impact.”",
            "“Careful — that’s every hour of every day. It won’t survive contact.”",
        ],
        "“This plan will collapse. Cut it to what you’ll actually sustain.”",
        "“You’ve got it. That’s a plan you can run and adjust.”",
        "“Try again. What gets dropped when the week goes wrong?”",
    ),
    "placement.daily": block(
        "“A day only needs three things: repair one weakness, keep one strength "
        "warm, and log what actually happened. Consistency beats intensity — the "
        "person who shows up daily beats the one who studies nine hours on Sunday.”",
        [
            "“Nice. Small, done, logged.”",
            "“Clean. You protected the streak instead of chasing the hours.”",
        ],
        [
            "“Stop. You skipped logging, so tomorrow’s plan is guesswork.”",
            "“Careful — you did only the comfortable part of the day.”",
        ],
        "“The day didn’t land. Name the one thing you’ll still do today.”",
        "“You’ve got it. Daily beats dramatic.”",
        "“Try again. What’s the smallest version of today you can still finish?”",
    ),
    "placement.phases": block(
        "“Campaigns run in phases for a reason: foundations first so nothing "
        "crumbles under time, then simulation so the method holds under pressure, "
        "then taper so you arrive sharp instead of exhausted.”",
        [
            "“Nice. You’re in the right phase for your timeline.”",
            "“Clean. You finished foundations instead of skipping to mocks.”",
        ],
        [
            "“Stop. You’re running mocks before the basics exist.”",
            "“Careful — you’re treating this phase like it lasts forever.”",
        ],
        "“The phase doesn’t match your state. Step back one and shore it up.”",
        "“You’ve got it. Phase complete. The next one raises the pressure.”",
        "“Try again. What is this phase supposed to produce?”",
    ),
    "placement.progress": block(
        "“Progress is a trend, not a single score. One mock tells you almost "
        "nothing; four in a row tell you whether the plan works. Track the line, "
        "not the point.”",
        [
            "“Nice. You’re reading the trend instead of the last number.”",
            "“Clean. Four points and the direction is clear.”",
        ],
        [
            "“Stop. You’re over-reading a single result.”",
            "“Careful — you changed the plan after one bad day.”",
        ],
        "“One point isn’t a trend. Get more data before you change anything.”",
        "“You’ve got it. You can see the curve now — keep feeding it.”",
        "“Try again. Which way has this moved over the last three attempts?”",
    ),
    "placement.adaptation": block(
        "“Plans change when evidence changes, not when you get bored. Change one "
        "variable at a time, or you’ll never know which change caused the result.”",
        [
            "“Nice. You adjusted from evidence, not from frustration.”",
            "“Clean. One change, so the cause stays legible.”",
        ],
        [
            "“Stop. You rewrote the whole plan after one data point.”",
            "“Careful — you changed everything, so nothing is measurable.”",
        ],
        "“Too many changes at once. Roll back to one variable.”",
        "“You’ve got it. The plan is alive and still honest.”",
        "“Try again. What evidence would justify this change?”",
    ),
    "placement.mock": block(
        "“A mock is a rehearsal under the real constraints: the same clock, the "
        "same room rules, no pausing. Score it, then spend longer reviewing it "
        "than you spent taking it — that’s where the marks come from.”",
        [
            "“Nice. You reviewed it properly instead of just checking the score.”",
            "“Clean. That review just paid for itself next week.”",
        ],
        [
            "“Stop. You looked at the total and moved on.”",
            "“Careful — you took it without the clock. That isn’t a mock.”",
        ],
        "“That attempt isn’t valid. Run it under real conditions next time.”",
        "“You’ve got it. That’s the standard to hold on test day.”",
        "“Try again. Which errors were careless, and which were gaps?”",
    ),
    "placement.repair": block(
        "“Repair is the whole game. Find the exact step that fails, fix that step, "
        "then re-test the same topic — until a fresh question of that type no "
        "longer catches you.”",
        [
            "“Nice. You fixed the step, not the symptom.”",
            "“Clean. That retest is the proof.”",
        ],
        [
            "“Stop. You re-studied the topic but never re-tested it.”",
            "“Careful — you fixed an example, not the pattern behind it.”",
        ],
        "“The repair didn’t hold. Which step is still breaking?”",
        "“You’ve got it. That weakness is closed until it reappears.”",
        "“Try again. Re-test it — has the same error actually gone?”",
    ),
    "placement.speed": block(
        "“Speed is method familiarity, not rushing. You go faster by recognising "
        "the problem type instantly and reaching for the right approach without "
        "deliberation — never by reading less carefully.”",
        [
            "“Nice. That was faster because the method was familiar.”",
            "“Clean. Time dropped, accuracy didn’t.”",
        ],
        [
            "“Stop. You went fast and lost marks you already had.”",
            "“Careful — you skimmed the question and solved a different one.”",
        ],
        "“Speed without accuracy is a net loss. Slow the read, speed the method.”",
        "“You’ve got it. Faster because you knew, not because you rushed.”",
        "“Try again. Which part is slow — reading, choosing, or computing?”",
    ),
    "placement.accuracy": block(
        "“Accuracy is a habit built on one rule: commit only after you can name "
        "the step that produces the answer. Every careless mark came from skipping "
        "that check, not from not knowing the topic.”",
        [
            "“Nice. You checked before you committed.”",
            "“Clean. Nothing careless slipped through.”",
        ],
        [
            "“Stop. You knew this and still marked it wrong.”",
            "“Careful — you moved on before confirming the unit or the sign.”",
        ],
        "“That mark was avoidable. Name the step you skipped.”",
        "“You’ve got it. Accuracy under time is the actual skill.”",
        "“Try again. Say out loud why the answer is this.”",
    ),
    "placement.interview": block(
        "“Readiness isn’t a feeling — it’s evidence. You can answer consistently, "
        "under time, out of order, on an ordinary day. This check exists to see "
        "whether that’s true yet, or whether it’s still hope.”",
        [
            "“Nice. That held without prompting.”",
            "“Clean. Same result on the second attempt — it’s real.”",
        ],
        [
            "“Stop. You can do this with notes. Take them away.”",
            "“Careful — it only worked when I asked it the way you practised.”",
        ],
        "“It isn’t holding yet. Which part collapses under pressure?”",
        "“You’ve got it. That’s ready, not hopeful.”",
        "“Try again. Same question, cold, no prompting.”",
    ),
    "placement.mastery": block(
        "“This is the end of the runway. Everything you’ve built — diagnosis, "
        "repair, speed, composure — now has to run without me standing next to "
        "you. Prove it once more, alone.”",
        [
            "“Nice. That’s the whole loop, unassisted.”",
            "“Clean. You produced it under the same conditions as the real one.”",
        ],
        [
            "“Stop. You’re coasting on earlier work. This attempt has to stand alone.”",
            "“Careful — the standard slipped now that you felt finished.”",
        ],
        "“Not yet. It has to hold again, without the safety net.”",
        "“You’ve got it. Placement ready — go and take it.”",
        "“Try again. One clean, unassisted run.”",
    ),
}

#: Shared voice for any `placement.*` skill without its own entry.
DOMAIN_PLACEMENT: Dict[str, Any] = block(
    "“Run the campaign, not the mood. Diagnose honestly, fix the sharpest "
    "weakness first, re-test to prove it held, and log what actually happened so "
    "tomorrow’s plan isn’t a guess.”",
    [
        "“Nice. That’s the loop working as designed.”",
        "“Clean. Diagnose, fix, re-test — done properly.”",
    ],
    [
        "“Stop. You skipped the re-test, so you don’t know if this held.”",
        "“Careful — you’re planning the campaign instead of running it.”",
    ],
    "“The loop is broken at some step. Which one did you skip?”",
    "“You’ve got it. That’s how the campaign compounds.”",
    "“Try again. What’s the next weakness, and how will you prove it’s gone?”",
)
