// @ts-nocheck
import { useState } from "react";
import { CheckCircle } from "lucide-react";
import { FlagshipMissionProps } from "../../components/missions/FlagshipMissionShell";
import PlacementTimer from "../../components/interactions/PlacementTimer";

function VisualBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Visual Explanation</h2>
      <p className="text-sm text-[#9a9a9a]">Profit/Loss is about comparing selling price to cost price.</p>
      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-4">
          <div className="text-xs font-mono text-green-400">PROFIT</div>
          <div className="mt-1 text-sm text-[#e9e9e9]">SP &gt; CP</div>
          <div className="mt-1 text-xs text-[#9a9a9a]">Profit = SP - CP</div>
        </div>
        <div className="rounded-lg border border-red-500/30 bg-red-500/5 p-4">
          <div className="text-xs font-mono text-red-400">LOSS</div>
          <div className="mt-1 text-sm text-[#e9e9e9]">SP &lt; CP</div>
          <div className="mt-1 text-xs text-[#9a9a9a]">Loss = CP - SP</div>
        </div>
      </div>
    </div>
  );
}

function ManipulateBlock() {
  const [cp, setCp] = useState(100);
  const [sp, setSp] = useState(120);
  const profit = sp - cp;
  const percent = cp > 0 ? ((sp - cp) / cp) * 100 : 0;
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Change cost price and selling price.</p>
      <div className="flex items-center gap-4">
        <div>
          <label className="text-xs text-[#9a9a9a]">Cost Price</label>
          <input type="number" value={cp} onChange={(e) => setCp(Number(e.target.value))} className="ml-2 w-24 rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] focus:outline-none" />
        </div>
        <div>
          <label className="text-xs text-[#9a9a9a]">Selling Price</label>
          <input type="number" value={sp} onChange={(e) => setSp(Number(e.target.value))} className="ml-2 w-24 rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] focus:outline-none" />
        </div>
      </div>
      <div className={`text-lg font-bold ${profit >= 0 ? "text-green-400" : "text-red-400"}`}>
        {profit >= 0 ? `Profit: ₹${profit}` : `Loss: ₹${Math.abs(profit)}`} ({percent.toFixed(1)}%)
      </div>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">If CP = ₹200 and profit is 25%, what is the selling price?</p>
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">What if the same item is sold at a 10% loss instead?</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Write: SP = CP + (CP * profit%)</p>
      <input type="text" placeholder="SP = CP + CP * profit%" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none font-mono" />
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">A shopkeeper gives 20% discount but still makes 25% profit. Is the discount calculated on CP or SP?</p>
    </div>
  );
}

function FixBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Fix</h2>
      <p className="text-sm text-[#9a9a9a]">Discount is on the marked price, not CP. Use: MP * (1 - discount%) = SP.</p>
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
From memory: is discount calculated on cost price or marked price?
</p>
      <input
        type="text"
        placeholder="Your answer from memory"
        className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
      />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">
Marked price - never cost price.
</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">A man buys an article for ₹100 and sells it at 20% profit. Then he buys it back and sells again at 20% profit. What is his total profit percent?</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">By selling an article for ₹120, a man loses 20%. At what price must he sell it to gain 20%?</p>
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
      <p className="text-sm text-[#9a9a9a]">CP = ₹150. To gain 20%, SP = ₹180.</p>
    </div>
  );
}

const mission: FlagshipMissionProps = {
  captainMessage: "Profit and loss are everywhere in business math. Let's make the formula feel obvious.",
  captainMood: "briefing",
  xpReward: 130,
  backTo: "/placement",
  steps: [
    { id: "visual", title: "Visual", description: "See profit/loss", render: VisualBlock },
    { id: "manipulate", title: "Manipulate", description: "Change CP and SP", render: ManipulateBlock },
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
    skillId: "aptitude.profit_loss",
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


