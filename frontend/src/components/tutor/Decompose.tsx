// @ts-nocheck
import { motion } from "framer-motion";

type DecomposeProps = {
  say: string;
  steps: string[];
  onComplete: () => void;
};

export default function Decompose({ say, steps, onComplete }: DecomposeProps) {
  return (
    <div className="space-y-4">
      <p className="text-lg font-medium text-gray-800">{say}</p>
      <div className="space-y-2">
        {steps.map((step, idx) => (
          <motion.div
            key={idx}
            className="flex items-center gap-3 px-4 py-3 bg-white border border-gray-200 rounded-xl"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <span className="w-6 h-6 rounded-full bg-brand-500 text-white flex items-center justify-center text-xs font-bold">
              {idx + 1}
            </span>
            <span className="text-sm text-gray-700">{step}</span>
          </motion.div>
        ))}
      </div>
      <motion.button
        className="bg-green-600 text-white px-4 py-2 rounded-full"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onComplete}
      >
        Continue
      </motion.button>
    </div>
  );
}
