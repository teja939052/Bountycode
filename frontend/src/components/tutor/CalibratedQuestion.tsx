// @ts-nocheck
import { motion } from "framer-motion";

type CalibratedQuestionProps = {
  say: string;
  opts: Array<{ t: string; to: string; code?: string }>;
  onChoose: (index: number) => void;
};

export default function CalibratedQuestion({ say, opts, onChoose }: CalibratedQuestionProps) {
  return (
    <div className="space-y-4">
      <p className="text-lg font-medium text-gray-800">{say}</p>
      <div className="grid gap-3">
        {opts.map((opt, idx) => (
          <motion.button
            key={idx}
            className="w-full text-left px-4 py-3 bg-white border-2 border-gray-200 rounded-xl hover:border-brand-500 hover:shadow-md transition"
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            onClick={() => onChoose(idx)}
          >
            <span className="text-sm font-medium text-gray-800">{opt.t}</span>
          </motion.button>
        ))}
      </div>
    </div>
  );
}
