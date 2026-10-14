// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type TimeTravelProps = {
  steps: number;
  question: string;
  memoryStates: any[];
  onInspect: (step: number) => void;
};

export default function TimeTravel({ steps, question, memoryStates, onInspect }: TimeTravelProps) {
  const [step, setStep] = React.useState(0);

  React.useEffect(() => {
    onInspect(step);
  }, [step, onInspect]);

  return (
    <div className="space-y-4">
      <p className="text-sm font-medium text-gray-700">{question}</p>
      <div className="flex items-center gap-2">
        {Array.from({ length: steps }).map((_, idx) => (
          <motion.button
            key={idx}
            className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium ${
              idx === step ? "bg-brand-500 text-white" : "bg-gray-200 text-gray-700"
            }`}
            whileHover={{ scale: 1.1 }}
            onClick={() => setStep(idx)}
          >
            {idx}
          </motion.button>
        ))}
      </div>
      <div className="bg-gray-900 text-green-400 rounded-xl p-4 font-mono text-sm">
        {JSON.stringify(memoryStates[step] || {}, null, 2)}
      </div>
    </div>
  );
}
