import { useState } from "react";
import { motion } from "framer-motion";
import useReducedMotion from "../../hooks/useReducedMotion";
import { requestWithRetry as request } from "../../services/api/request";

const SKILL_ID = "dsa.sliding_window";
const VALUES = [2, 1, 5, 1, 3, 2];
const K = 3;

type Step = { left: number; right: number; sum: number; note: string };

function buildSteps(): Step[] {
  const steps: Step[] = [];
  let sum = 0;
  for (let right = 0; right < VALUES.length; right++) {
    sum += VALUES[right];
    const left = right >= K - 1 ? right - K + 1 : 0;
    if (right < K - 1) {
      steps.push({
        left,
        right,
        sum,
        note: `Enter ${VALUES[right]}. Window not full yet (${right + 1}/${K}).`,
      });
    } else {
      const entering = VALUES[right];
      const leaving = right >= K ? VALUES[right - K] : null;
      steps.push({
        left,
        right,
        sum,
        note:
          leaving === null
            ? `Enter ${entering}. Window full [${VALUES.slice(left, right + 1).join(", ")}], sum=${sum}.`
            : `Enter ${entering}, leave ${leaving}. Window [${VALUES.slice(left, right + 1).join(", ")}], sum=${sum}.`,
      });
      sum -= VALUES[left];
    }
  }
  return steps;
}

const STEPS = buildSteps();

export default function PatternTracer() {
  const reduced = useReducedMotion();
  const [idx, setIdx] = useState(0);
  const [done, setDone] = useState(false);
  const step = STEPS[idx];

  const emit = async () => {
    try {
      await request("/api/v1/study/activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "practice",
          skill_id: SKILL_ID,
          passed: true,
          score: 100,
          time_spent: 60,
          diagnosis_codes: [],
          source: "pattern_tracer",
          metadata: { component: "tracer", pattern: "sliding-window", steps_completed: STEPS.length },
        }),
      });
    } catch {
      // fail-open: evidence is best-effort when unauthenticated
    }
  };

  const complete = () => {
    if (!done) {
      setDone(true);
      emit();
    }
  };

  return (
    <div className="rounded-xl border border-border dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900/50">
      <h3 className="font-bold text-sm dark:text-white mb-1">Tracer: fixed window, k={K}</h3>
      <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">
        Step through. Each element enters once and leaves once — that is why the total work stays O(n).
      </p>
      <div className="flex gap-1.5 mb-3 flex-wrap" role="group" aria-label="Array values">
        {VALUES.map((v, i) => {
          const inWindow = i >= step.left && i <= step.right;
          return (
            <motion.div
              key={i}
              initial={reduced ? {} : { scale: 0.9 }}
              animate={{ scale: inWindow ? 1.08 : 1 }}
              className={`w-10 h-10 flex items-center justify-center rounded-lg font-mono text-sm font-bold border-2 ${
                inWindow
                  ? "bg-emerald-100 dark:bg-emerald-900/40 border-emerald-500 text-emerald-700 dark:text-emerald-300"
                  : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-500"
              }`}
            >
              {v}
            </motion.div>
          );
        })}
      </div>
      <p className="text-sm text-gray-600 dark:text-gray-300 mb-1">
        left={step.left}, right={step.right}, sum={step.sum}
      </p>
      <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">{step.note}</p>
      <div className="flex gap-2">
        <button
          onClick={() => setIdx((i) => Math.max(0, i - 1))}
          disabled={idx === 0}
          className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-gray-200 dark:bg-gray-700 disabled:opacity-40"
        >
          Prev
        </button>
        {idx < STEPS.length - 1 ? (
          <button
            onClick={() => setIdx((i) => i + 1)}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-primary-600 text-white"
          >
            Step {idx + 2}/{STEPS.length}
          </button>
        ) : (
          <button
            onClick={complete}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white"
          >
            {done ? "Traced ✓" : "Finish trace"}
          </button>
        )}
      </div>
    </div>
  );
}
