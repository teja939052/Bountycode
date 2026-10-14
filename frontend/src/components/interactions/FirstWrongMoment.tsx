// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type FirstWrongMomentProps = {
  steps: string[];
  wrongStep: number;
  onSelect: (step: number) => void;
};

export default function FirstWrongMoment({ steps, wrongStep, onSelect }: FirstWrongMomentProps) {
  const [selected, setSelected] = React.useState<number | null>(null);
  const correct = selected === wrongStep;

  return (
    <div className="space-y-4">
      <p className="text-sm font-medium text-gray-700">At which step did the program stop doing what we intended?</p>
      <div className="space-y-2">
        {steps.map((step, idx) => (
          <motion.button
            key={idx}
            className={`w-full text-left px-4 py-3 rounded-xl border-2 ${
              selected === idx
                ? correct
                  ? "bg-green-50 border-green-300"
                  : "bg-red-50 border-red-300"
                : "bg-white border-gray-200"
            }`}
            whileHover={{ scale: 1.01 }}
            onClick={() => { setSelected(idx); onSelect(idx); }}
          >
            <span className="text-xs font-mono text-gray-400 mr-2">Step {idx + 1}</span>
            <span className="text-sm text-gray-800">{step}</span>
          </motion.button>
        ))}
      </div>
      {selected !== null && (
        <div className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}>
          <p className="font-medium">{correct ? "Correct!" : "Not quite — try again"}</p>
        </div>
      )}
    </div>
  );
}
