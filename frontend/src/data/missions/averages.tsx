// @ts-nocheck
import { ReactNode } from "react";
import { FlagshipMissionProps } from "../../components/missions/FlagshipMissionShell";
import PlacementTimer from "../../components/interactions/PlacementTimer";

function VisualBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Visual Explanation</h2>
      <p className="text-sm text-[#9a9a9a]">Average = Sum of values / Count of values.</p>
      <div className="flex items-end gap-2">
        {[40, 60, 80, 100].map((v, i) => (
          <div key={i} className="flex-1 rounded bg-[#ffa116]" style={{ height: `${v / 2}px` }} />
        ))}
      </div>
      <p className="text-xs text-[#9a9a9a]">Heights represent values: 40, 60, 80, 100</p>
    </div>
  );
}

function ManipulateBlock() {
  const [values, setValues] = useState([40, 60, 80, 100]);
  const avg = values.reduce((a, b) => a + b, 0) / values.length;
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Change values and watch the average update.</p>
      <div className="flex items-end gap-2">
        {values.map((v, i) => (
          <div key={i} className="flex-1 rounded bg-[#ffa116]" style={{ height: `${Math.max(v / 2, 8)}px` }} />
        ))}
      </div>
      <div className="text-lg font-bold text-[#ffa116]">Average: {avg.toFixed(1)}</div>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">If one score increases by 20, how does the average change?</p>
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">What happens if you add an outlier value of 500?</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Write: average = sum / count</p>
      <input
        type="text"
        placeholder="sum / count"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none font-mono"
      />
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">What if count = 0?</p>
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
      <p className="text-sm text-[#9a9a9a]">Add a guard: if count === 0, return 0.</p>
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
No notes: 4 numbers average 50. One number drops by 12. What is the new average?
</p>
      <input
        type="text"
        placeholder="Your answer from memory"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">
47 - the total drops by 12, spread over 4 numbers: 50 minus 3.
</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">A student scored 72, 85, 91, and 88 in 4 subjects. What is the average?</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">The average of 5 numbers is 30. If one number is excluded, the average becomes 28. Find the excluded number.</p>
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
      <p className="text-sm text-[#9a9a9a]">Sum of 5 numbers = 150. Sum of 4 numbers = 112. Excluded = 38.</p>
    </div>
  );
}

import { useState } from "react";
import { CheckCircle } from "lucide-react";

const mission: FlagshipMissionProps = {
  captainMessage:
    "Averages are deceptively simple. Let's build intuition for how one value can shift the whole picture.",
  captainMood: "briefing",
  xpReward: 130,
  backTo: "/placement",
  steps: [
    { id: "visual", title: "Visual", description: "See averages in action", render: VisualBlock },
    { id: "manipulate", title: "Manipulate", description: "Change values and observe", render: ManipulateBlock },
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
    skillId: "aptitude.averages",
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


