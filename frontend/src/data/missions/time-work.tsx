// @ts-nocheck
import { useState } from "react";
import { CheckCircle } from "lucide-react";
import { FlagshipMissionProps } from "../../components/missions/FlagshipMissionShell";
import PlacementTimer from "../../components/interactions/PlacementTimer";

function VisualBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Visual Explanation</h2>
      <p className="text-sm text-[#9a9a9a]">Work = Rate × Time. If two people work together, rates add.</p>
      <div className="flex items-center gap-4">
        <div className="flex-1 rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-4 text-center">
          <div className="text-xs text-[#9a9a9a]">Person A</div>
          <div className="mt-1 text-lg font-bold text-[#ffa116]">1/6 job/day</div>
        </div>
        <div className="text-xl font-bold text-[#ffa116]">+</div>
        <div className="flex-1 rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-4 text-center">
          <div className="text-xs text-[#9a9a9a]">Person B</div>
          <div className="mt-1 text-lg font-bold text-[#ffa116]">1/12 job/day</div>
        </div>
      </div>
    </div>
  );
}

function ManipulateBlock() {
  const [a, setA] = useState(6);
  const [b, setB] = useState(12);
  const rateA = 1 / a;
  const rateB = 1 / b;
  const combined = rateA + rateB;
  const days = combined > 0 ? 1 / combined : 0;
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Change how many days each person takes alone.</p>
      <div className="flex items-center gap-4">
        <div>
          <label className="text-xs text-[#9a9a9a]">A takes</label>
          <input type="number" value={a} onChange={(e) => setA(Number(e.target.value))} className="ml-2 w-20 rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] focus:outline-none" />
          <span className="text-xs text-[#9a9a9a]">days</span>
        </div>
        <div>
          <label className="text-xs text-[#9a9a9a]">B takes</label>
          <input type="number" value={b} onChange={(e) => setB(Number(e.target.value))} className="ml-2 w-20 rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] focus:outline-none" />
          <span className="text-xs text-[#9a9a9a]">days</span>
        </div>
      </div>
      <div className="text-lg font-bold text-[#ffa116]">Together: {days.toFixed(2)} days</div>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">If A can finish in 4 days and B in 6 days, how long together?</p>
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">What if a third person joins with the same rate as A?</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Write: combined_rate = 1/A + 1/B</p>
      <input type="text" placeholder="1/A + 1/B" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none font-mono" />
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">What if one worker is slower than the other? Does adding them always help?</p>
    </div>
  );
}

function FixBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Fix</h2>
      <p className="text-sm text-[#9a9a9a]">Adding any worker never hurts: combined rate is always greater than the faster worker's rate alone.</p>
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
From memory: A finishes a job in 6 days. What fraction does A finish in one day?
</p>
      <input
        type="text"
        placeholder="Your answer from memory"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">
One sixth - daily rate equals 1 divided by days.
</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">A tank has two pipes. One fills in 3 hours, the other empties in 6 hours. How long to fill if both are open?</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">A can complete a work in 10 days, B in 15 days. They work together for 4 days, then B leaves. How many more days does A need?</p>
      <input type="number" placeholder="Your answer" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none" />
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
      <p className="text-sm text-[#9a9a9a]">Together they finish 10/15 in 4 days. Remaining = 1/3. A alone needs 10/3 = 3.33 days.</p>
    </div>
  );
}

const mission: FlagshipMissionProps = {
  captainMessage: "Time and work problems are rate problems in disguise. Once rates click, the formula does the work for you.",
  captainMood: "briefing",
  xpReward: 130,
  backTo: "/placement",
  steps: [
    { id: "visual", title: "Visual", description: "See rates in action", render: VisualBlock },
    { id: "manipulate", title: "Manipulate", description: "Change rates", render: ManipulateBlock },
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
    skillId: "aptitude.time_work",
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


