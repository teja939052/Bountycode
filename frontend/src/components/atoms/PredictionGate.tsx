// @ts-nocheck
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function PredictionGate({
  prompt,
  answer,
  explanation,
  onComplete,
}: {
  prompt: string;
  answer: string;
  explanation?: string;
  onComplete: (correct: boolean) => void;
}) {
  const [userAnswer, setUserAnswer] = useState("");
  const [checked, setChecked] = useState(false);

  const normalized = userAnswer.trim().toLowerCase();
  const expected = String(answer).trim().toLowerCase();
  const isCorrect = normalized === expected || expected.includes(normalized) || normalized.includes(expected);

  const handleCheck = () => {
    setChecked(true);
  };

  return (
    <div className="max-w-md mx-auto text-center">
      <h3 className="text-xl font-bold mb-4">Predict before you run</h3>
      <p className="text-lg mb-6">{prompt}</p>
      {!checked ? (
        <div className="space-y-3">
          <input
            type="text"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            placeholder="Type your prediction..."
            className="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-center text-lg focus:outline-none focus:border-brand-500"
            onKeyDown={(e) => e.key === "Enter" && handleCheck()}
          />
          <motion.button
            className="bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleCheck}
          >
            Check prediction
          </motion.button>
        </div>
      ) : (
        <AnimatePresence>
          {isCorrect ? (
            <motion.div
              className="bg-green-50 border border-green-200 rounded-2xl p-6"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <p className="text-green-800 font-medium mb-2">Correct!</p>
              {explanation && <p className="text-green-700 text-sm mb-4">{explanation}</p>}
              <motion.button
                className="bg-green-600 text-white px-6 py-2 rounded-full"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => onComplete(true)}
              >
                Continue
              </motion.button>
            </motion.div>
          ) : (
            <motion.div
              className="bg-red-50 border border-red-200 rounded-2xl p-6"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <p className="text-red-800 font-medium mb-2">Not quite — that&apos;s okay.</p>
              <p className="text-red-700 text-sm mb-1">The expected behavior was:</p>
              <code className="bg-white rounded px-3 py-1 text-sm">{answer}</code>
              {explanation && <p className="text-red-700 text-sm mt-3">{explanation}</p>}
              <motion.button
                className="mt-4 bg-red-600 text-white px-6 py-2 rounded-full"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => onComplete(false)}
              >
                Try again
              </motion.button>
            </motion.div>
          )}
        </AnimatePresence>
      )}
    </div>
  );
}
