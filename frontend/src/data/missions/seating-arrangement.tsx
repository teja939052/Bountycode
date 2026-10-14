// @ts-nocheck
import { useState } from "react";
import { CheckCircle } from "lucide-react";
import { FlagshipMissionProps } from "../../components/missions/FlagshipMissionShell";
import PlacementTimer from "../../components/interactions/PlacementTimer";

function VisualBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Visual Explanation</h2>
      <p className="text-sm text-[#9a9a9a]">
        Seating arrangement problems ask you to place people around a table or in a row using given clues. Draw the positions first, then place each person.
      </p>
      <div className="font-mono text-sm bg-[#1c1c1c] p-4 rounded-lg border border-[#2a2a2a]">
        <div>A [ ] B [ ] C</div>
        <div className="text-[#9a9a9a]">Positions: 1, 2, 3</div>
      </div>
    </div>
  );
}

function ManipulateBlock() {
  const [pos, setPos] = useState(2);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Place A at position {pos}. If B is immediately to the right of A, where is B?</p>
      <input type="number" min={1} max={5} value={pos} onChange={(e) => setPos(Number(e.target.value))} className="w-20 rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] focus:outline-none" />
      <div className="font-mono text-sm">B is at position {pos + 1}</div>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">If A is at position 2 and C is at position 4, is B at position 3?</p>
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">Change from a row to a circular table. How does "immediately right" change?</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Place 3 people in a row given: A is left of B, and B is left of C.</p>
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">What if the clue says "A is between B and C" but doesn't specify order? Both arrangements are possible.</p>
    </div>
  );
}

function FixBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Fix</h2>
      <p className="text-sm text-[#9a9a9a]">Use all clues together to eliminate impossible positions before placing anyone.</p>
    </div>
  );
}

function RecallBlock() {
  const [shown, setShown] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Recall</h2>
      <p className="text-sm text-[#9a9a9a]">No notes. In a row of 5, if A is 3rd from left and 3rd from right, how many people are there?</p>
      <input type="text" placeholder="Your answer" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none" />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">5. If someone is 3rd from both ends in a row, total = 3 + 3 - 1 = 5.</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">Apply row logic to a circular table: 4 people around a table. Who sits opposite A if B is to A's left and C is opposite B?</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">A, B, C, D sit in a row. A is left of B. C is between A and D. Who is at the right end?</p>
      <input
        disabled={locked}
        type="text"
        placeholder="Your answer"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
      {locked && (
        <p className="text-xs text-red-400">Time is up - the proof counts only what you solved under time.</p>
      )}
    </div>
  );
}

function ProveBlock() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <CheckCircle className="text-green-400" size={24} />
        <h2 className="text-xl font-bold">Correct!</h2>
      </div>
      <p className="text-sm text-[#9a9a9a]">D is at the right end. Order: A C B D or A C D B depending on interpretation; C between A and D fixes A-C-D with B left of A or between.</p>
    </div>
  );
}

const mission: FlagshipMissionProps = {
  captainMessage: "Seating arrangements turn vague words like 'left' and 'between' into exact positions. Let's practice translating clues into diagrams.",
  captainMood: "briefing",
  xpReward: 110,
  backTo: "/placement",
  steps: [
    { id: "visual", title: "Visual", description: "See the arrangement", render: VisualBlock },
    { id: "manipulate", title: "Manipulate", description: "Move people around", render: ManipulateBlock },
    { id: "predict", title: "Predict", description: "Predict positions", render: PredictBlock },
    { id: "change", title: "Change", description: "Change one thing", render: ChangeBlock },
    { id: "build", title: "Build", description: "Build the arrangement", render: BuildBlock },
    { id: "break", title: "Break", description: "Ambiguous clues", render: BreakBlock },
    { id: "fix", title: "Fix", description: "Use all clues", render: FixBlock },
    { id: "recall", title: "Recall", description: "Answer from memory", render: RecallBlock },
    { id: "transfer", title: "Transfer", description: "Apply to a new problem", render: TransferBlock },
    { id: "placement", title: "Placement", description: "Real placement question", render: PlacementBlock },
    { id: "prove", title: "Prove", description: "Submit your answer", render: ProveBlock },
  ],

  evidence: {
    skillId: "reasoning.seating_arrangement",
    stages: [
      { stageId: "visual" },
      { stageId: "manipulate" },
      { stageId: "predict" },
      { stageId: "change" },
      { stageId: "build" },
      { stageId: "break" },
      { stageId: "fix" },
      { stageId: "recall" },
      { stageId: "transfer" },
      { stageId: "placement" },
      { stageId: "prove" },
    ],
    finalPassed: false,
    timeSpentSeconds: 0,
  },
};

export default mission;


