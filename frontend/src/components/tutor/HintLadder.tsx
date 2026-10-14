// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type HintLadderProps = {
  say: string;
  hints: string[];
  onComplete: () => void;
};

export default function HintLadder({ say, hints, onComplete }: HintLadderProps) {
  const [step, setStep] = React.useState(0);
  const visible = hints.slice(0, step + 1);

  return (
    <div className="space-y-4">
      <p className="text-lg font-medium text-gray-800">{say}</p>
      <div className="space-y-2">
        {visible.map((hint, idx) => (
          <motion.div
            key={idx}
            className="px-4 py-2 bg-brand-50 border border-brand-200 rounded-xl text-sm text-gray-700"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {hint}
          </motion.div>
        ))}
      </div>
      <div className="flex gap-3">
        {step < hints.length - 1 && (
          <motion.button
            className="bg-brand-500 text-white px-4 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setStep((s) => s + 1)}
          >
            Next hint
          </motion.button>
        )}
        {step === hints.length - 1 && (
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
    </div>
  );
}
