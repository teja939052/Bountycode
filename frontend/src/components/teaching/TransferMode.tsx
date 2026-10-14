// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type TransferModeProps = {
  title: string;
  story: string;
  task: string;
  options?: string[];
  correct_order?: number[];
  onComplete: (correct: boolean) => void;
};

export default function TransferMode({ title, story, task, options, correct_order, onComplete }: TransferModeProps) {
  const [selected, setSelected] = React.useState<number[]>([]);
  const [checked, setChecked] = React.useState(false);
  const correct = checked && correct_order ? selected.join(",") === correct_order.join(",") : false;

  const toggle = (idx: number) => {
    setSelected((prev) => (prev.includes(idx) ? prev.filter((i) => i !== idx) : [...prev, idx]));
    setChecked(false);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      <p className="text-sm text-gray-600">{story}</p>
      <p className="text-gray-900">{task}</p>
      <div className="grid gap-2">
        {(options || []).map((opt, idx) => (
          <motion.button
            key={idx}
            className={`px-4 py-3 rounded-xl border-2 text-left text-sm ${
              selected.includes(idx) ? "border-brand-500 bg-brand-50" : "border-gray-200 bg-white"
            }`}
            whileHover={{ scale: 1.01 }}
            onClick={() => toggle(idx)}
          >
            {opt}
          </motion.button>
        ))}
      </div>
      <div className="flex gap-3">
        <motion.button
          className="bg-brand-500 text-white px-6 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setChecked(true)}
        >
          Check order
        </motion.button>
      </div>
      {checked && (
        <div className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}>
          <p className="font-medium">{correct ? "Correct!" : "Not quite — try reordering"}</p>
          {!correct && (
            <motion.button
              className="mt-2 bg-brand-500 text-white px-4 py-2 rounded-full text-sm"
              whileHover={{ scale: 1.05 }}
              onClick={() => { setSelected([]); setChecked(false); onComplete(false); }}
            >
              Try again
            </motion.button>
          )}
          {correct && (
            <motion.button
              className="mt-2 bg-green-600 text-white px-4 py-2 rounded-full text-sm"
              whileHover={{ scale: 1.05 }}
              onClick={() => onComplete(true)}
            >
              Continue
            </motion.button>
          )}
        </div>
      )}
    </div>
  );
}
