// @ts-nocheck
import React from "react";
import { motion, AnimatePresence } from "framer-motion";

type TeachBackProps = {
  say: string;
  cards: string[];
  correct_order: number[];
  onComplete: (order: number[]) => void;
};

export default function TeachBack({ say, cards, correct_order, onComplete }: TeachBackProps) {
  const [order, setOrder] = React.useState<number[]>(() => [...correct_order]);
  const [checked, setChecked] = React.useState(false);
  const correct = checked ? order.every((val, idx) => val === correct_order[idx]) : false;

  const move = (from: number, to: number) => {
    setOrder((prev) => {
      const next = [...prev];
      const [item] = next.splice(from, 1);
      next.splice(to, 0, item);
      return next;
    });
    setChecked(false);
  };

  return (
    <div className="space-y-4">
      <p className="text-lg font-medium text-gray-800">{say}</p>
      <div className="space-y-2">
        {order.map((cardIndex, displayIdx) => (
          <motion.button
            key={`${cardIndex}-${displayIdx}`}
            className={`w-full text-left px-4 py-3 border-2 rounded-xl flex items-center gap-3 ${
              checked
                ? correct
                  ? "bg-green-50 border-green-300"
                  : "bg-red-50 border-red-300"
                : "bg-white border-gray-200"
            }`}
            whileHover={{ scale: checked ? 1 : 1.01 }}
            onClick={() => {
              if (!checked && displayIdx > 0) move(displayIdx, displayIdx - 1);
            }}
          >
            <span className="text-xs font-mono text-gray-400">#{displayIdx + 1}</span>
            <span className="text-sm text-gray-800">{cards[cardIndex]}</span>
          </motion.button>
        ))}
      </div>
      <div className="flex gap-3">
        <motion.button
          className="bg-brand-500 text-white px-4 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setOrder((prev) => {
            const next = [...prev];
            const last = next.pop();
            if (last !== undefined) next.unshift(last);
            setChecked(false);
            return next;
          })}
        >
          Rotate down
        </motion.button>
        <motion.button
          className="bg-green-600 text-white px-4 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => {
            setChecked(true);
            onComplete(order);
          }}
        >
          Check order
        </motion.button>
      </div>
      <AnimatePresence>
        {checked && (
          <motion.div
            className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <p className="font-medium">{correct ? "Correct order!" : "Not quite — try rearranging"}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
