// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type CompareWorldsProps = {
  left_code: string;
  right_code: string;
  left_output: string;
  right_output: string;
  question: string;
  onAnswer: (answer: string) => void;
};

export default function CompareWorlds({ left_code, right_code, left_output, right_output, question, onAnswer }: CompareWorldsProps) {
  const [submitted, setSubmitted] = React.useState(false);

  return (
    <div className="space-y-4">
      <p className="text-gray-800">{question}</p>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs font-mono text-gray-500 mb-2">PROGRAM A</p>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-xs font-mono">{left_code}</pre>
          <p className="text-xs text-gray-600 mt-2">Output: {left_output}</p>
        </div>
        <div>
          <p className="text-xs font-mono text-gray-500 mb-2">PROGRAM B</p>
          <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-xs font-mono">{right_code}</pre>
          <p className="text-xs text-gray-600 mt-2">Output: {right_output}</p>
        </div>
      </div>
      {!submitted ? (
        <motion.button
          className="bg-brand-500 text-white px-6 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => { setSubmitted(true); onAnswer(""); }}
        >
          Explain the difference
        </motion.button>
      ) : (
        <motion.div className="bg-blue-50 border border-blue-200 rounded-xl p-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <p className="text-sm text-blue-800">Look at the operator difference carefully.</p>
        </motion.div>
      )}
    </div>
  );
}
