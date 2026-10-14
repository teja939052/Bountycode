// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type ExplainToUnlockProps = {
  questions: string[];
  onAnswer: (questionIndex: number, answer: string) => void;
};

export default function ExplainToUnlock({ questions, onAnswer }: ExplainToUnlockProps) {
  const [current, setCurrent] = React.useState(0);
  const [answers, setAnswers] = React.useState<Record<number, string>>({});

  const submit = () => {
    onAnswer(current, answers[current] || "");
    if (current < questions.length - 1) {
      setCurrent((c) => c + 1);
    }
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-500">Question {current + 1} of {questions.length}</p>
      <p className="text-lg font-medium text-gray-900">{questions[current]}</p>
      <textarea
        className="w-full border-2 border-gray-200 rounded-xl p-4 focus:outline-none focus:border-brand-500"
        rows={3}
        value={answers[current] || ""}
        onChange={(e) => setAnswers((prev) => ({ ...prev, [current]: e.target.value }))}
        placeholder="Explain in your own words..."
      />
      <motion.button
        className="bg-brand-500 text-white px-6 py-2 rounded-full"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={submit}
      >
        {current < questions.length - 1 ? "Next question" : "Finish"}
      </motion.button>
    </div>
  );
}
