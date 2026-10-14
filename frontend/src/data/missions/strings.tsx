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
        A string is a sequence of characters. In code, "hello" is a string. You can access individual characters using indices: h=0, e=1, l=2, l=3, o=4.
      </p>
      <div className="font-mono text-sm bg-[#1c1c1c] p-4 rounded-lg border border-[#2a2a2a]">
        <div>"hello"</div>
        <div className="text-[#9a9a9a]">Index: 0=h, 1=e, 2=l, 3=l, 4=o</div>
        <div className="text-[#ffa116]">length = 5</div>
      </div>
    </div>
  );
}

function ManipulateBlock() {
  const [text, setText] = useState("hello");
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Type a string and see its characters and length.</p>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] focus:outline-none"
      />
      <div className="font-mono text-sm bg-[#1c1c1c] p-4 rounded-lg border border-[#2a2a2a]">
        <div>"{text}"</div>
        <div className="text-[#9a9a9a]">Characters: {text.split("").join(", ")}</div>
        <div className="text-[#ffa116]">length = {text.length}</div>
      </div>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">What is the output? "hello".substring(1, 4)</p>
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">Change substring(1, 4) to substring(1, 5). What changes?</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Extract the first 3 characters from "bounty".</p>
      <input type="text" placeholder='str.substring(0, 3)' className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none font-mono" />
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">What if start &gt; end in substring? Try substring(4, 1).</p>
      <div className="rounded-lg bg-[#0f0f0f] border border-red-500/30 p-4">
        <code className="text-sm text-red-400">Result: empty string</code>
      </div>
    </div>
  );
}

function FixBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Fix</h2>
      <p className="text-sm text-[#9a9a9a]">Validate indices before calling substring: ensure start &lt;= end and both are within bounds.</p>
    </div>
  );
}

function RecallBlock() {
  const [shown, setShown] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Recall</h2>
      <p className="text-sm text-[#9a9a9a]">No notes. What does "hello".indexOf("l") return?</p>
      <input type="text" placeholder="Your answer" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none" />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">2. indexOf returns the first occurrence index.</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">Check if a string is a palindrome using substring and length.</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">What is the output? "bountycode".substring(0, 6)</p>
      <input type="text" placeholder="Your answer" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none" />
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
      <p className="text-sm text-[#9a9a9a]">Output is "bounty". substring(0, 6) extracts characters 0 through 5.</p>
    </div>
  );
}

const mission: FlagshipMissionProps = {
  captainMessage: "Strings are how programs talk to people. Let's learn to slice, measure, and check them precisely.",
  captainMood: "briefing",
  xpReward: 120,
  backTo: "/placement",
  steps: [
    { id: "visual", title: "Visual", description: "See strings as sequences", render: VisualBlock },
    { id: "manipulate", title: "Manipulate", description: "Change the string", render: ManipulateBlock },
    { id: "predict", title: "Predict", description: "What does substring return?", render: PredictBlock },
    { id: "change", title: "Change", description: "Change one thing", render: ChangeBlock },
    { id: "build", title: "Build", description: "Extract characters", render: BuildBlock },
    { id: "break", title: "Break", description: "Invalid indices", render: BreakBlock },
    { id: "fix", title: "Fix", description: "Guard against bad input", render: FixBlock },
    { id: "recall", title: "Recall", description: "Answer from memory", render: RecallBlock },
    { id: "transfer", title: "Transfer", description: "Apply to a new problem", render: TransferBlock },
    { id: "placement", title: "Placement", description: "Real placement question", render: PlacementBlock },
    { id: "prove", title: "Prove", description: "Submit your answer", render: ProveBlock },
  ],

  evidence: {
    skillId: "coding.strings",
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


