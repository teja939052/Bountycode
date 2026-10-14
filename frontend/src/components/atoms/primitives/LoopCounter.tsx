// @ts-nocheck
import { motion } from "framer-motion";

type LoopCounterProps = {
  count: number;
  max: number;
  onChange?: (count: number) => void;
};

export default function LoopCounter({ count, max, onChange }: LoopCounterProps) {
  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex items-center gap-3">
        <motion.button
          className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-xl font-bold disabled:opacity-30"
          onClick={() => onChange?.(Math.max(0, count - 1))}
          disabled={count <= 0}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          −
        </motion.button>
        <motion.div
          className="w-16 h-16 rounded-xl bg-brand-500 text-white flex items-center justify-center text-2xl font-bold shadow-lg"
          animate={{ scale: count > 0 ? [1, 1.1, 1] : 1 }}
          transition={{ duration: 0.3 }}
        >
          {count}
        </motion.div>
        <motion.button
          className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-xl font-bold disabled:opacity-30"
          onClick={() => onChange?.(Math.min(max, count + 1))}
          disabled={count >= max}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          +
        </motion.button>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
        <motion.div
          className="h-full bg-brand-500"
          animate={{ width: `${(count / max) * 100}%` }}
          transition={{ duration: 0.2 }}
        />
      </div>
      <p className="text-xs text-gray-500">Loop repeats while count &lt; {max}</p>
    </div>
  );
}
