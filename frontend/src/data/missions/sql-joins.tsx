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
        A JOIN combines rows from two tables based on a related column. INNER JOIN keeps only matching rows. LEFT JOIN keeps all rows from the left table.
      </p>
      <div className="font-mono text-sm bg-[#1c1c1c] p-4 rounded-lg border border-[#2a2a2a]">
        <div>Users: 1=Alice, 2=Bob, 3=Charlie</div>
        <div>Orders: (1, order1), (2, order2)</div>
        <div className="text-[#ffa116]">INNER JOIN = Alice + Bob (Charlie has no order)</div>
      </div>
    </div>
  );
}

function ManipulateBlock() {
  const [join, setJoin] = useState("INNER");
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Manipulate</h2>
      <p className="text-sm text-[#9a9a9a]">Choose a join type and see which users appear.</p>
      <select value={join} onChange={(e) => setJoin(e.target.value)} className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] focus:outline-none">
        <option>INNER JOIN</option>
        <option>LEFT JOIN</option>
        <option>RIGHT JOIN</option>
      </select>
      <div className="font-mono text-sm">
        {join === "INNER JOIN" && "Result: Alice, Bob"}
        {join === "LEFT JOIN" && "Result: Alice, Bob, Charlie"}
        {join === "RIGHT JOIN" && "Result: Alice, Bob"}
      </div>
    </div>
  );
}

function PredictBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Predict</h2>
      <p className="text-sm text-[#9a9a9a]">If you LEFT JOIN Users to Orders, does Charlie appear?</p>
    </div>
  );
}

function ChangeBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Change One Thing</h2>
      <p className="text-sm text-[#9a9a9a]">Change LEFT JOIN to INNER JOIN. What happens to Charlie?</p>
    </div>
  );
}

function BuildBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Tiny Build</h2>
      <p className="text-sm text-[#9a9a9a]">Write the query: list all users and their order IDs, including users with no orders.</p>
      <input type="text" placeholder='SELECT u.name, o.id FROM users u LEFT JOIN orders o ON u.id = o.user_id' className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none font-mono" />
    </div>
  );
}

function BreakBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Break It</h2>
      <p className="text-sm text-[#9a9a9a]">What if you join on the wrong column? Joining users.name to orders.user_id will return nothing because types don't match.</p>
    </div>
  );
}

function FixBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Fix</h2>
      <p className="text-sm text-[#9a9a9a]">Always join on the foreign key relationship: users.id = orders.user_id.</p>
    </div>
  );
}

function RecallBlock() {
  const [shown, setShown] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Recall</h2>
      <p className="text-sm text-[#9a9a9a]">No notes. Which join keeps all rows from both tables?</p>
      <input type="text" placeholder="Your answer" className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none" />
      <button onClick={() => setShown(!shown)} className="text-xs text-[#ffa116] underline">Check the answer</button>
      {shown && (
        <p className="text-sm text-[#9a9a9a]">FULL OUTER JOIN. INNER keeps matches only. LEFT/RIGHT keep one side fully.</p>
      )}
    </div>
  );
}

function TransferBlock() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Transfer</h2>
      <p className="text-sm text-[#9a9a9a]">You have Products and Categories. Show all products and their category names, including products with no category.</p>
    </div>
  );
}

function PlacementBlock() {
  const [locked, setLocked] = useState(false);
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Placement Question</h2>
      <PlacementTimer seconds={90} onExpire={() => setLocked(true)} />
      <p className="text-sm text-[#9a9a9a]">Which join returns all users and matching orders, plus users with no orders?</p>
      <div className="space-y-2">
        {["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"].map((opt) => (
          <label key={opt} className="flex items-center gap-2 text-sm">
            <input type="radio" name="join" value={opt} disabled={locked} /> {opt}
          </label>
        ))}
      </div>
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
      <p className="text-sm text-[#9a9a9a]">LEFT JOIN keeps all left-table rows and matches from the right table.</p>
    </div>
  );
}

const mission: FlagshipMissionProps = {
  captainMessage: "SQL JOINs are the backbone of relational queries. Let's make sure you never lose a row you actually needed.",
  captainMood: "briefing",
  xpReward: 130,
  backTo: "/placement",
  steps: [
    { id: "visual", title: "Visual", description: "See the tables", render: VisualBlock },
    { id: "manipulate", title: "Manipulate", description: "Choose a join type", render: ManipulateBlock },
    { id: "predict", title: "Predict", description: "Predict the result", render: PredictBlock },
    { id: "change", title: "Change", description: "Change one thing", render: ChangeBlock },
    { id: "build", title: "Build", description: "Write the query", render: BuildBlock },
    { id: "break", title: "Break", description: "Wrong join column", render: BreakBlock },
    { id: "fix", title: "Fix", description: "Fix the join", render: FixBlock },
    { id: "recall", title: "Recall", description: "Answer from memory", render: RecallBlock },
    { id: "transfer", title: "Transfer", description: "Apply to a new problem", render: TransferBlock },
    { id: "placement", title: "Placement", description: "Real placement question", render: PlacementBlock },
    { id: "prove", title: "Prove", description: "Submit your answer", render: ProveBlock },
  ],

  evidence: {
    skillId: "cs_core.sql_joins",
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


