import { useState } from "react";
import { requestWithRetry as request } from "../../services/api/request";

const SKILL_ID = "dsa.sliding_window";
const OPTIONS = [
  "while right < len(arr):",
  "while left <= right:",
  "while window_sum > target:",
  "while not valid(summary):",
];
const CORRECT = "while not valid(summary):";

export default function CodeFillInTheBlank() {
  const [choice, setChoice] = useState("");
  const [verdict, setVerdict] = useState<"idle" | "correct" | "wrong">("idle");

  const submit = async () => {
    if (!choice) return;
    const ok = choice === CORRECT;
    setVerdict(ok ? "correct" : "wrong");
    try {
      await request("/api/v1/study/activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "practice",
          skill_id: SKILL_ID,
          passed: ok,
          score: ok ? 100 : 0,
          time_spent: 45,
          diagnosis_codes: ok ? [] : ["PATTERN_RECOGNITION"],
          source: "pattern_fillblank",
          metadata: { component: "fillblank", pattern: "sliding-window", chosen: choice },
        }),
      });
    } catch {
      // fail-open
    }
  };

  return (
    <div className="rounded-xl border border-border dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900/50">
      <h3 className="font-bold text-sm dark:text-white mb-1">Predict the next operation</h3>
      <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">
        No answer is revealed until you submit. Choose the line that shrinks a variable window when the constraint breaks.
      </p>
      <pre className="p-3 text-[12px] leading-relaxed font-mono bg-gray-950 text-cyan-300 rounded-lg overflow-x-auto mb-3">
{`left = 0
summary = 0
for right in range(len(arr)):
    summary += arr[right]   # grow
    ?????                   # shrink while invalid
    best = min(best, ...)`}
      </pre>
      <div className="space-y-1.5 mb-3">
        {OPTIONS.map((o) => (
          <label
            key={o}
            className={`flex items-center gap-2 text-xs font-mono px-3 py-2 rounded-lg border cursor-pointer ${
              choice === o
                ? "border-primary-500 bg-primary-50 dark:bg-primary-900/20"
                : "border-gray-200 dark:border-gray-700"
            }`}
          >
            <input
              type="radio"
              name="sw-fillblank"
              checked={choice === o}
              onChange={() => {
                setChoice(o);
                setVerdict("idle");
              }}
              className="accent-indigo-600"
            />
            <span className="dark:text-gray-200">{o}</span>
          </label>
        ))}
      </div>
      <button
        onClick={submit}
        disabled={!choice}
        className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-primary-600 text-white disabled:opacity-40"
      >
        Submit prediction
      </button>
      {verdict === "correct" && (
        <p className="mt-2 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
          Correct — shrink while the window is invalid, then record the best valid window.
        </p>
      )}
      {verdict === "wrong" && (
        <p className="mt-2 text-xs font-semibold text-red-600 dark:text-red-400">
          Not quite — the shrink loop must test validity, not just indices. Re-trace which element leaves and why.
        </p>
      )}
    </div>
  );
}
