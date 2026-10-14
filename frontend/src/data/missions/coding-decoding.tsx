// @ts-nocheck
import { useState } from "react";
import { CheckCircle } from "lucide-react";
import { FlagshipMissionProps } from "../../components/missions/FlagshipMissionShell";
import PlacementTimer from "../../components/interactions/PlacementTimer";

function VisualBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Visual Explanation</h2>
      <p className="text-sm text-[#9a9a9a]">Coding-decoding maps letters to other letters using a fixed pattern.</p>
      <div className="flex flex-wrap gap-2 text-sm">
        {["A", "B", "C", "D", "E"].map((ch, i) => (
          <div key={ch} className="rounded border border-[#2a2a2a] bg-[#1c1c1c] px-2 py-1 text-center">
            <div>{ch}</div>
            <div className="text-[#ffa116]">{String.fromCharCode(65 + (i + 2) % 26)}</div>
          </div>
        ))}
      </div>
      <p className="text-xs text-[#9a9a9a]">Pattern: +2 shift</p>
    </div>
  );
}

function ManipulateBlock() {
  const [shift, setShift] = useState(2);
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Change the shift value.</p>
      <input type="number" value={shift} onChange={(e) => setShift(Number(e.target.value))} className="w-20 rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] focus:outline-none" />
      <div className="flex flex-wrap gap-2 text-sm">
        {["A", "B", "C", "D", "E"].map((ch, i) => (
          <div key={ch} className="rounded border border-[#2a2a2a] bg-[#1c1c1c] px-2 py-1 text-center">
            <div>{ch}</div>
            <div className="text-[#ffa116]">{String.fromCharCode(65 + (i + shift) % 26)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">If A becomes C, what does M become?</p>
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">What if the pattern is reverse order instead of shift?</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Write: coded = (letterIndex + shift) % 26</p>
      <input type="text" placeholder="(index + shift) % 26" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none font-mono" />
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">What if the pattern changes after the midpoint of the alphabet?</p>
    </div>
  );
}

function FixBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Fix</h2>
      <p className="text-sm text-[#9a9a9a]">Use modulo 26 for wrap-around, or switch to a keyword cipher table.</p>
    </div>
  );
}

function RecallBlock() {
  const [shown, setShown] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Recall</h2>
      <p className="text-sm text-[#9a9a9a]">No notes. No scrolling back. Answer from memory, then check yourself.</p>
      <p className="text-sm text-[#e9e9e9]">
From memory: in a +2 shift, what does Z become?
</p>
      <input
        type="text"
        placeholder="Your answer from memory"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">
B - the alphabet wraps around, like modulo 26.
</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">Decode: "DWWDFN" using a +3 Caesar shift.</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">If "PEN" is coded as "QFO", how is "PAPER" coded?</p>
      <input type="text" placeholder="Your answer" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none" />
      {locked && (
        <p className="text-xs text-red-400">Time is up - the proof counts only what you solved under time. Review the steps above, then retry the mission.</p>
      )}
        disabled={locked}
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
      <p className="text-sm text-[#9a9a9a]">P→Q, A→B, P→Q, E→F, R→S. Answer: QBQFBS.</p>
    </div>
  );
}

const mission: FlagshipMissionProps = {
  captainMessage: "Coding-decoding is pattern recognition with letters. Let's make letter-shift logic automatic.",
  captainMood: "briefing",
  xpReward: 120,
  backTo: "/placement",
  steps: [
    { id: "visual", title: "Visual", description: "See the cipher", render: VisualBlock },
    { id: "manipulate", title: "Manipulate", description: "Change shift", render: ManipulateBlock },
    { id: "predict", title: "Predict", description: "What happens if...?", render: PredictBlock },
    { id: "change", title: "Change", description: "Change one thing", render: ChangeBlock },
    { id: "build", title: "Build", description: "Write the formula", render: BuildBlock },
    { id: "break", title: "Break", description: "Introduce a bug", render: BreakBlock },
    { id: "fix", title: "Fix", description: "Debug and repair", render: FixBlock },
    {
      id: "recall",
      title: "Recall",
      description: "Answer from memory",
      render: RecallBlock,
    },
    { id: "transfer", title: "Transfer", description: "Apply to a new problem", render: TransferBlock },
    { id: "placement", title: "Placement", description: "Real placement question", render: PlacementBlock },
    { id: "prove", title: "Prove", description: "Submit your answer", render: ProveBlock },
  ],

  evidence: {
    skillId: "reasoning.coding_decoding",
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


