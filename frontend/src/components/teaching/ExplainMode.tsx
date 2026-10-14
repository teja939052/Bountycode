// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type ExplainModeProps = {
  title: string;
  steps: Array<{ say: string; visual?: string; content?: string }>;
  teacher_summary: string;
  onComplete: () => void;
};

export default function ExplainMode({ title, steps, teacher_summary, onComplete }: ExplainModeProps) {
  const [stepIndex, setStepIndex] = React.useState(0);
  const visible = steps.slice(0, stepIndex + 1);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      <div className="space-y-3">
        {visible.map((step, idx) => (
          <motion.div
            key={idx}
            className="bg-white border border-gray-200 rounded-xl p-4"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <p className="text-sm text-gray-600 mb-1">Step {idx + 1}</p>
            <p className="text-gray-900">{step.say}</p>
            {step.visual === "text" && step.content && (
              <p className="mt-2 text-sm font-mono text-brand-700 bg-brand-50 rounded-lg px-3 py-2">
                {step.content}
              </p>
            )}
          </motion.div>
        ))}
      </div>
      <div className="flex gap-3">
        {stepIndex < steps.length - 1 && (
          <motion.button
            className="bg-brand-500 text-white px-4 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setStepIndex((i) => i + 1)}
          >
            Next
          </motion.button>
        )}
        {stepIndex === steps.length - 1 && (
          <motion.button
            className="bg-green-600 text-white px-4 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onComplete}
          >
            Got it
          </motion.button>
        )}
      </div>
      <p className="text-xs text-gray-500">{teacher_summary}</p>
    </div>
  );
}
