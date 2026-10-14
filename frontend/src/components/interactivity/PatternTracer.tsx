// @ts-nocheck
import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import useReducedMotion from "../../hooks/useReducedMotion";
import { requestWithRetry as request } from "../../services/api/request";

export interface PatternTracerProps {
  skillId?: string;
  values?: number[];
  k?: number;
  title?: string;
  description?: string;
  pattern?: string;
}

const DEFAULT_SKILL = "dsa.sliding_window";
const DEFAULT_VALUES = [2, 1, 5, 1, 3, 2];
const DEFAULT_K = 3;

type Step = { left: number; right: number; sum: number; note: string };

function buildSteps(values: number[], k: number): Step[] {
  const steps: Step[] = [];
  let sum = 0;
  for (let right = 0; right < values.length; right++) {
    sum += values[right];
    const left = right >= k - 1 ? right - k + 1 : 0;
    if (right < k - 1) {
      steps.push({
        left,
        right,
        sum,
        note: `Enter ${values[right]}. Window not full yet (${right + 1}/${k}).`,
      });
    } else {
      const entering = values[right];
      const leaving = right >= k ? values[right - k] : null;
      steps.push({
        left,
        right,
        sum,
        note:
          leaving === null
            ? `Enter ${entering}. Window full [${values.slice(left, right + 1).join(", ")}], sum=${sum}.`
            : `Enter ${entering}, leave ${leaving}. Window [${values.slice(left, right + 1).join(", ")}], sum=${sum}.`,
      });
      sum -= values[left];
    }
  }
  return steps;
}

export default function PatternTracer({
  skillId = DEFAULT_SKILL,
  values = DEFAULT_VALUES,
  k = DEFAULT_K,
  title,
  description = "Step through. Each element enters once and leaves once — that is why the total work stays O(n).",
  pattern = "sliding-window",
}: PatternTracerProps) {
  const reduced = useReducedMotion();
  const steps = useMemo(() => buildSteps(values, k), [values, k]);
  const [idx, setIdx] = useState(0);
  const [done, setDone] = useState(false);
  const step = steps[Math.min(idx, steps.length - 1)];
  const heading = title ?? `Tracer: fixed window, k=${k}`;

  const emit = async () => {
    try {
      await request("/api/v1/unified/activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lesson_id: skillId,
          activity_type: "practice",
          score: 100,
          passed: true,
          time_spent_seconds: 60,
          diagnosis_codes: [],
          metadata: { source: "pattern_tracer", component: "tracer", pattern, steps_completed: steps.length },
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

  if (!step) return null;

  return (
    <div className="rounded-xl border border-border dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900/50">
      <h3 className="font-bold text-sm dark:text-white mb-1">{heading}</h3>
      <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">{description}</p>
      <div className="flex gap-1.5 mb-3 flex-wrap" role="group" aria-label="Array values">
        {values.map((v, i) => {
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
        {idx < steps.length - 1 ? (
          <button
            onClick={() => setIdx((i) => i + 1)}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-primary-600 text-white"
          >
            Step {idx + 2}/{steps.length}
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
