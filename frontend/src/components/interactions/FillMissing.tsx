// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type FillMissingProps = {
  code: string;
  blanks: string[];
  onComplete: (filled: string[]) => void;
};

export default function FillMissing({ code, blanks, onComplete }: FillMissingProps) {
  const [answers, setAnswers] = React.useState<string[]>(() => Array(blanks.length).fill(""));
  const [checked, setChecked] = React.useState(false);
  const correct = checked && answers.every((a, i) => a.trim() === blanks[i].trim());

  const submit = () => {
    setChecked(true);
    onComplete(answers);
  };

  return (
    <div className="space-y-4">
      <pre className="bg-gray-900 text-green-400 rounded-xl p-4 text-sm font-mono overflow-x-auto whitespace-pre-wrap">
        {code.split("___").map((part, idx) => (
          <span key={idx}>
            {part}
            {idx < blanks.length && (
              <input
                className="inline-block w-32 bg-gray-800 text-white border-b-2 border-brand-500 px-1 text-center mx-1"
                value={answers[idx]}
                onChange={(e) => {
                  const next = [...answers];
                  next[idx] = e.target.value;
                  setAnswers(next);
                  setChecked(false);
                }}
                onKeyDown={(e) => e.key === "Enter" && submit()}
              />
            )}
          </span>
        ))}
      </pre>
      <motion.button
        className="bg-brand-500 text-white px-6 py-2 rounded-full"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={submit}
      >
        Check
      </motion.button>
      {checked && (
        <div className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}>
          <p className="font-medium">{correct ? "Correct!" : "Not quite"}</p>
          {!correct && (
            <p className="text-sm text-gray-600 mt-1">Expected: {blanks.join(", ")}</p>
          )}
        </div>
      )}
    </div>
  );
}
