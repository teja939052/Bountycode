import { useState } from "react";

export default function TargetPage() {
  const [target, setTarget] = useState<string>("");
  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Choose Your Target</h1>
      <p className="text-text-muted">Set the company, role and timeline you are preparing for.</p>
      <div className="space-y-3">
        <input value={target} onChange={(e) => setTarget(e.target.value)}
          placeholder="e.g. Microsoft — Software Engineer"
          className="w-full rounded-lg border border-gray-700 bg-gray-900 px-3 py-2 text-sm" />
        <button className="btn-primary" disabled={!target.trim()}>
          Set Target & Get Path
        </button>
      </div>
      {target.trim() && <p className="text-green-400">Target saved: {target}</p>}
    </div>
  );
}
