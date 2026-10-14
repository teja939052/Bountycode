// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type BugSurgeryProps = {
  buggy_code: string;
  question: string;
  answer: string;
  onFix: (correct: boolean) => void;
};

export default function BugSurgery({ buggy_code, question, answer, onFix }: BugSurgeryProps) {
  const [userFix, setUserFix] = React.useState("");
  const [submitted, setSubmitted] = React.useState(false);
  const expected = answer.toLowerCase();
  const normalized = userFix.trim().toLowerCase();
  const correct = submitted && expected && (normalized.includes(expected) || expected.includes(normalized));

  return (
    <div className="space-y-4">
      <p className="text-gray-800">{question}</p>
      <pre className="bg-gray-900 text-red-400 rounded-xl p-4 text-sm overflow-x-auto">{buggy_code}</pre>
      {!submitted ? (
        <>
          <input
            className="w-full border-2 border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-500"
            value={userFix}
            onChange={(e) => setUserFix(e.target.value)}
            placeholder="Describe the fix or paste corrected code..."
            onKeyDown={(e) => e.key === "Enter" && setSubmitted(true)}
          />
          <motion.button
            className="bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setSubmitted(true)}
          >
            Apply fix
          </motion.button>
        </>
      ) : (
        <div className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}>
          <p className="font-medium">{correct ? "Fixed!" : "Not quite"}</p>
          <p className="text-sm text-gray-600 mt-1">{answer}</p>
          <motion.button
            className="mt-3 bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onFix(Boolean(correct))}
          >
            Continue
          </motion.button>
        </div>
      )}
    </div>
  );
}
