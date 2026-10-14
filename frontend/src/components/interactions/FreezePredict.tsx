// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type FreezePredictProps = {
  after_line: number;
  question: string;
  answer: string;
  onPredict: (answer: string) => void;
};

export default function FreezePredict({ after_line, question, answer, onPredict }: FreezePredictProps) {
  const [userAnswer, setUserAnswer] = React.useState("");
  const [revealed, setRevealed] = React.useState(false);
  const correct = userAnswer.trim().toLowerCase() === answer.trim().toLowerCase();

  return (
    <div className="space-y-4">
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
        <p className="text-sm font-medium text-yellow-900 mb-1">⏸ Execution paused after line {after_line}</p>
        <p className="text-yellow-800">{question}</p>
      </div>
      {!revealed ? (
        <>
          <input
            className="w-full border-2 border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-500"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            placeholder="Your prediction..."
            onKeyDown={(e) => e.key === "Enter" && setRevealed(true)}
          />
          <motion.button
            className="bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => { setRevealed(true); onPredict(userAnswer); }}
          >
            Commit prediction
          </motion.button>
        </>
      ) : (
        <div className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}>
          <p className="font-medium">{correct ? "Correct!" : "Not quite"}</p>
          <p className="text-sm text-gray-600 mt-1">Answer: {answer}</p>
        </div>
      )}
    </div>
  );
}
