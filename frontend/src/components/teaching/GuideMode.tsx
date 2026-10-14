// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type GuideModeProps = {
  title: string;
  prompt: string;
  starter_code?: string;
  solution?: string;
  _blanks?: string[];
  hints?: string[];
  onComplete: (correct: boolean) => void;
};

export default function GuideMode({ title, prompt, starter_code, solution, hints, onComplete }: GuideModeProps) {
  const [code, setCode] = React.useState(starter_code || "");
  const [showHint, setShowHint] = React.useState(0);
  const [submitted, setSubmitted] = React.useState(false);
  const [correct, setCorrect] = React.useState(false);

  const check = () => {
    const normalized = code.trim().replace(/\s+/g, " ");
    const expected = (solution || "").trim().replace(/\s+/g, " ");
    const isCorrect = normalized === expected;
    setSubmitted(true);
    setCorrect(isCorrect);
    onComplete(isCorrect);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      <p className="text-gray-700">{prompt}</p>
      <textarea
        className="w-full border-2 border-gray-200 rounded-xl p-4 font-mono text-sm focus:outline-none focus:border-brand-500"
        rows={6}
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
      <div className="flex gap-3">
        <motion.button
          className="bg-brand-500 text-white px-6 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={check}
        >
          Check
        </motion.button>
        {hints && hints.length > 0 && showHint < hints.length && (
          <motion.button
            className="bg-gray-200 text-gray-800 px-4 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowHint((h) => h + 1)}
          >
            Hint {showHint + 1}/{hints.length}
          </motion.button>
        )}
      </div>
      {hints && hints.length > 0 && showHint > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-3">
          {hints.slice(0, showHint).map((hint, idx) => (
            <p key={idx} className="text-sm text-yellow-800">{hint}</p>
          ))}
        </div>
      )}
      {submitted && (
        <div className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}>
          <p className="font-medium">{correct ? "Correct!" : "Not quite — try again"}</p>
          {!correct && solution && (
            <pre className="mt-2 bg-gray-900 text-green-400 rounded-lg p-3 text-xs overflow-x-auto">{solution}</pre>
          )}
        </div>
      )}
    </div>
  );
}
