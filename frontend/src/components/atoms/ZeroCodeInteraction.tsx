// @ts-nocheck
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function ZeroCodeInteraction({
  interaction,
  onComplete,
}: {
  interaction: any;
  onComplete: (correct: boolean) => void;
}) {
  const [selected, setSelected] = useState<string | null>(null);
  const [finished, setFinished] = useState(false);

  const correctAnswer = interaction.correct || interaction.correct_answer || "";
  const options = interaction.options || [];

  const handleSelect = (option: string) => {
    if (finished) return;
    setSelected(option);
    const correct = option === correctAnswer;
    setTimeout(() => {
      setFinished(true);
      onComplete(correct);
    }, 1200);
  };

  return (
    <div className="max-w-md mx-auto text-center">
      <p className="text-lg mb-4">{interaction.prompt || "Choose the right answer"}</p>
      <div className="flex gap-3 justify-center flex-wrap">
        {options.map((opt: string) => (
          <motion.button
            key={opt}
            className={`px-4 py-2 rounded-full border-2 ${
              finished
                ? opt === correctAnswer
                  ? "bg-green-500 text-white border-green-600"
                  : selected === opt
                  ? "bg-red-500 text-white border-red-600"
                  : "bg-white border-gray-300"
                : "bg-white border-gray-300 hover:border-brand-500"
            }`}
            onClick={() => handleSelect(opt)}
            whileHover={{ scale: finished ? 1 : 1.05 }}
            whileTap={{ scale: finished ? 1 : 0.95 }}
          >
            {opt}
          </motion.button>
        ))}
      </div>
      <AnimatePresence>
        {finished && selected && (
          <motion.p
            className="mt-4 text-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            {selected === correctAnswer
              ? interaction.feedback_correct || "Correct!"
              : interaction.feedback_wrong || "Not quite — try again"}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}
