// @ts-nocheck
import { useState } from "react";
import { requestWithRetry as request } from "../../services/api/request";

export interface ExplainAloudProps {
  skillId?: string;
  keywords?: string[];
  title?: string;
  prompt?: string;
  pattern?: string;
  minHits?: number;
}

const DEFAULT_SKILL = "dsa.sliding_window";
const DEFAULT_KEYWORDS = ["o(n)", "linear", "once", "expand", "shrink", "window"];
const DEFAULT_TITLE = "Explain: why does the window stay O(n)?";

export default function ExplainAloud({
  skillId = DEFAULT_SKILL,
  keywords = DEFAULT_KEYWORDS,
  title = DEFAULT_TITLE,
  prompt = "Type your explanation. This is a keyword match for study evidence — not an objective grade of your speech.",
  pattern = "sliding-window",
  minHits = 3,
}: ExplainAloudProps) {
  const [text, setText] = useState("");
  const [result, setResult] = useState<null | { hits: string[]; missing: string[] }>(null);

  const submit = async () => {
    if (!text.trim()) return;
    const lower = text.toLowerCase();
    const hits = keywords.filter((k) => lower.includes(k));
    const missing = keywords.filter((k) => !lower.includes(k));
    setResult({ hits, missing });
    const passed = hits.length >= minHits;
    try {
      await request("/api/v1/unified/activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lesson_id: skillId,
          activity_type: "practice",
          score: Math.round((hits.length / keywords.length) * 100),
          passed,
          time_spent_seconds: 90,
          diagnosis_codes: passed ? [] : ["CONCEPT_GAP"],
          metadata: {
            source: "pattern_explain",
            component: "explain",
            pattern,
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
      <h3 className="font-bold text-sm dark:text-white mb-1">{title}</h3>
      <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">{prompt}</p>
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
            Matched {result.hits.length}/{keywords.length}: {result.hits.join(", ") || "none yet"}
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
