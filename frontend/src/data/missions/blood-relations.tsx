// @ts-nocheck
import { ReactNode } from "react";
import { FlagshipMissionProps } from "../../components/missions/FlagshipMissionShell";
import PlacementTimer from "../../components/interactions/PlacementTimer";

function VisualBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Visual Explanation</h2>
      <p className="text-sm text-[#9a9a9a]">
        Blood relations are best understood as a family tree. Let's map a simple one.
      </p>
      <div className="space-y-2 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-24 rounded border border-[#2a2a2a] bg-[#1c1c1c] px-2 py-1 text-center">You</div>
        </div>
        <div className="ml-8 flex items-center gap-2">
          <div className="w-24 rounded border border-[#2a2a2a] bg-[#1c1c1c] px-2 py-1 text-center">Mother</div>
          <div className="w-24 rounded border border-[#2a2a2a] bg-[#1c1c1c] px-2 py-1 text-center">Father</div>
        </div>
        <div className="ml-16 flex items-center gap-2">
          <div className="w-24 rounded border border-[#2a2a2a] bg-[#1c1c1c] px-2 py-1 text-center">Maternal Grandmother</div>
          <div className="w-24 rounded border border-[#2a2a2a] bg-[#1c1c1c] px-2 py-1 text-center">Maternal Grandfather</div>
        </div>
      </div>
    </div>
  );
}

function ManipulateBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Swap relationships and see how the tree changes.</p>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">If your mother's brother is your uncle, what is your father's sister?</p>
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">What if the relationship is through marriage instead of blood?</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Write the relationship: mother's brother = uncle</p>
      <input
        type="text"
        placeholder="mother's brother = ?"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none font-mono"
      />
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">What if gender is unspecified? Does the answer still hold?</p>
    </div>
  );
}

function FixBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Fix</h2>
      <p className="text-sm text-[#9a9a9a]">Use neutral terms when gender is unknown, or include both possibilities.</p>
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
From memory: your father's brother's daughter is your ___?
</p>
      <input
        type="text"
        placeholder="Your answer from memory"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">
Cousin - children of your parent's siblings are your cousins.
</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">Pointing to a photograph, a man said, "I have no siblings. That man's father is my father's son." How is he related to the person in the photo?</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">If A is the father of B, but B is not A's son, what is B to A?</p>
      <input
        disabled={locked}
        type="text"
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
      <p className="text-sm text-[#9a9a9a]">B must be A's daughter.</p>
    </div>
  );
}

import { useState } from "react";
import { CheckCircle } from "lucide-react";

const mission: FlagshipMissionProps = {
  captainMessage:
    "Blood relations look messy until you draw the tree. Let's make family logic visual and repeatable.",
  captainMood: "briefing",
  xpReward: 120,
  backTo: "/placement",
  steps: [
    { id: "visual", title: "Visual", description: "Map the family tree", render: VisualBlock },
    { id: "manipulate", title: "Manipulate", description: "Swap relationships", render: ManipulateBlock },
    { id: "predict", title: "Predict", description: "What happens if...?", render: PredictBlock },
    { id: "change", title: "Change", description: "Change one thing", render: ChangeBlock },
    { id: "build", title: "Build", description: "Write the relation", render: BuildBlock },
    { id: "break", title: "Break", description: "Introduce ambiguity", render: BreakBlock },
    { id: "fix", title: "Fix", description: "Clarify assumptions", render: FixBlock },
    {
      id: "recall",
      title: "Recall",
      description: "Answer from memory",
      render: RecallBlock,
    },
    { id: "transfer", title: "Transfer", description: "Apply to a new puzzle", render: TransferBlock },
    { id: "placement", title: "Placement", description: "Real placement question", render: PlacementBlock },
    { id: "prove", title: "Prove", description: "Submit your answer", render: ProveBlock },
  ],

  evidence: {
    skillId: "reasoning.blood_relations",
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


