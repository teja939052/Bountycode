import { useState } from "react";
import { requestWithRetry as request } from "../../services/api/request";

const SKILL_ID = "dsa.sliding_window";
const EXPECTED = ["o(n)", "linear", "once", "expand", "shrink", "window"];

export default function ExplainAloud() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<null | { hits: string[]; missing: string[] }>(null);

  const submit = async () => {
    if (!text.trim()) return;
    const lower = text.toLowerCase();
    const hits = EXPECTED.filter((k) => lower.includes(k));
    const missing = EXPECTED.filter((k) => !lower.includes(k));
    setResult({ hits, missing });
    const passed = hits.length >= 3;
    try {
      await request("/api/v1/study/activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "practice",
          skill_id: SKILL_ID,
          passed,
          score: Math.round((hits.length / EXPECTED.length) * 100),
          time_spent: 90,
          diagnosis_codes: passed ? [] : ["CONCEPT_GAP"],
          source: "pattern_explain",
          metadata: {
            component: "explain",
            pattern: "sliding-window",
            keyword_hits: hits,
            char_count: text.length,
          },
        }),
      });
    } catch {
      // fail-open
    }
  };

  return (
    <div className="rounded-xl border border-border dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900/50">
      <h3 className="font-bold text-sm dark:text-white mb-1">Explain: why does the window stay O(n)?</h3>
      <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">
        Type your explanation. This is a keyword match for study evidence — not an objective grade of your speech.
      </p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={3}
        placeholder="e.g. Each index expands once and shrinks once, so the window work is linear O(N)..."
        className="w-full text-sm p-3 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 dark:text-gray-100 mb-2"
      />
      <button
        onClick={submit}
        disabled={!text.trim()}
        className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-primary-600 text-white disabled:opacity-40"
      >
        Submit explanation
      </button>
      {result && (
        <div className="mt-2 text-xs">
          <p className="text-gray-600 dark:text-gray-300">
            Matched {result.hits.length}/{EXPECTED.length}: {result.hits.join(", ") || "none yet"}
          </p>
          {result.missing.length > 0 && (
            <p className="text-gray-500 dark:text-gray-400">
              Consider: {result.missing.join(", ")}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
