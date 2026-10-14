// @ts-nocheck
import { ReactNode } from "react";
import { FlagshipMissionProps } from "../../components/missions/FlagshipMissionShell";
import PlacementTimer from "../../components/interactions/PlacementTimer";

function VisualBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Visual Explanation</h2>
      <p className="text-sm text-[#9a9a9a]">
        A percentage is a fraction out of 100. If you have 25 out of 100, that's 25%.
      </p>
      <div className="grid grid-cols-10 gap-1">
        {Array.from({ length: 100 }).map((_, i) => (
          <div key={i} className={`h-8 rounded ${i < 25 ? "bg-[#ffa116]" : "bg-[#2a2a2a]"}`} />
        ))}
      </div>
      <p className="text-xs text-[#9a9a9a]">Orange = 25 items out of 100 total = 25%</p>
    </div>
  );
}

function ManipulateBlock() {
  const [percent, setPercent] = useState(25);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Change the percentage and see what happens.</p>
      <input
        type="range"
        min="0"
        max="100"
        value={percent}
        onChange={(e) => setPercent(Number(e.target.value))}
        className="w-full"
      />
      <div className="text-center">
        <span className="text-3xl font-bold text-[#ffa116]">{percent}%</span>
      </div>
      <div className="grid grid-cols-10 gap-1">
        {Array.from({ length: 100 }).map((_, i) => (
          <div key={i} className={`h-6 rounded ${i < percent ? "bg-[#ffa116]" : "bg-[#2a2a2a]"}`} />
        ))}
      </div>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">If you increase 25% by 20%, what's the new percentage?</p>
      <input
        type="number"
        placeholder="Your answer"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">Change the base from 100 to 200. What happens to the percentage?</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Write the formula: percentage = (part / total) × 100</p>
      <input
        type="text"
        placeholder="(part / total) * 100"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none font-mono"
      />
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">What if total = 0? Try it.</p>
      <div className="rounded-lg bg-[#0f0f0f] border border-red-500/30 p-4">
        <code className="text-sm text-red-400">Error: Division by zero</code>
      </div>
    </div>
  );
}

function FixBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Fix</h2>
      <p className="text-sm text-[#9a9a9a]">Add a guard: if total === 0, return 0.</p>
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
From memory: a price rises 10%, then falls 10%. Back to the start?
</p>
      <input
        type="text"
        placeholder="Your answer from memory"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">
No - 99. The second change applies to the new base, not the original.
</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">A shirt costs ₹800. After a 15% discount, what's the final price?</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">If 40% of a number is 80, what is 60% of the same number?</p>
      <input
        disabled={locked}
        type="number"
        placeholder="Your answer"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
      {locked && (
        <p className="text-xs text-red-400">Time is up - the proof counts only what you solved under time. Review the steps above, then retry the mission.</p>
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
      <p className="text-sm text-[#9a9a9a]">If 40% = 80, then 1% = 2, so 60% = 120.</p>
    </div>
  );
}

import { useState } from "react";
import { CheckCircle } from "lucide-react";

const mission: FlagshipMissionProps = {
  captainMessage:
    "Today we're mastering percentages. This is one of the most common topics in placement tests. Let's build real understanding, not just memorization.",
  captainMood: "briefing",
  xpReward: 150,
  backTo: "/placement",
  steps: [
    {
      id: "visual",
      title: "Visual",
      description: "See percentages in action",
      render: VisualBlock,
    },
    {
      id: "manipulate",
      title: "Manipulate",
      description: "Change values and observe",
      render: ManipulateBlock,
    },
    {
      id: "predict",
      title: "Predict",
      description: "What happens if...?",
      render: PredictBlock,
    },
    {
      id: "change",
      title: "Change",
      description: "Change one thing",
      render: ChangeBlock,
    },
    {
      id: "build",
      title: "Build",
      description: "Write the formula",
      render: BuildBlock,
    },
    {
      id: "break",
      title: "Break",
      description: "Introduce a bug",
      render: BreakBlock,
    },
    {
      id: "fix",
      title: "Fix",
      description: "Debug and repair",
      render: FixBlock,
    },
    {
      id: "recall",
      title: "Recall",
      description: "Answer from memory",
      render: RecallBlock,
    },
    {
      id: "transfer",
      title: "Transfer",
      description: "Apply to a new problem",
      render: TransferBlock,
    },
    {
      id: "placement",
      title: "Placement",
      description: "Real placement question",
      render: PlacementBlock,
    },
    {
      id: "prove",
      title: "Prove",
      description: "Submit your answer",
      render: ProveBlock,
    },
  ],

  evidence: {
    skillId: "aptitude.percentages",
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


