// @ts-nocheck
import { useState } from "react";
import { CheckCircle } from "lucide-react";
import { FlagshipMissionProps } from "../../components/missions/FlagshipMissionShell";
import PlacementTimer from "../../components/interactions/PlacementTimer";

function VisualBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Visual Explanation</h2>
      <p className="text-sm text-[#9a9a9a]">Vocabulary is built through context. The same word can mean different things in different sentences.</p>
      <div className="grid grid-cols-1 gap-3 text-sm">
        <div className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3">
          <div className="font-mono text-[#ffa116]">"Bank"</div>
          <div className="mt-1 text-[#9a9a9a]">1. Financial institution</div>
          <div className="text-[#9a9a9a]">2. River bank</div>
        </div>
      </div>
    </div>
  );
}

function ManipulateBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Use the word in two different sentences.</p>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">What does "bark" mean in: "The dog barked" vs "The tree bark is rough"?</p>
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">Replace "ran quickly" with a single synonym.</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Write a sentence using "meticulous" correctly.</p>
      <input type="text" placeholder="Your sentence" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none" />
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">"He is an notorious criminal." Find the error.</p>
    </div>
  );
}

function FixBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Fix</h2>
      <p className="text-sm text-[#9a9a9a]">Use "a notorious" because "notorious" starts with a consonant sound.</p>
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
From memory: 'The committee ___ divided' - is or are, and what decides it?
</p>
      <input
        type="text"
        placeholder="Your answer from memory"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">
Are - a collective noun takes the plural when its members act as individuals.
</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">Choose the correct word: "The committee ___ divided on the issue." (is / are)</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">Pick the synonym of "ephemeral": permanent / fleeting / solid / eternal</p>
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
      <p className="text-sm text-[#9a9a9a]">"Ephemeral" means fleeting or short-lived.</p>
    </div>
  );
}

const mission: FlagshipMissionProps = {
  captainMessage: "Vocabulary is not memorization. It's about using context clues to guess meaning.",
  captainMood: "briefing",
  xpReward: 110,
  backTo: "/placement",
  steps: [
    { id: "visual", title: "Visual", description: "See word in context", render: VisualBlock },
    { id: "manipulate", title: "Manipulate", description: "Use the word", render: ManipulateBlock },
    { id: "predict", title: "Predict", description: "What happens if...?", render: PredictBlock },
    { id: "change", title: "Change", description: "Change one thing", render: ChangeBlock },
    { id: "build", title: "Build", description: "Write the sentence", render: BuildBlock },
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
};

export default mission;
