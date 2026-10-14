// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type FadeModeProps = {
  title: string;
  stages: Array<any>;
  onComplete: (stageIndex: number) => void;
};

export default function FadeMode({ title, stages, onComplete }: FadeModeProps) {
  const [stageIndex, setStageIndex] = React.useState(0);
  const stage = stages[stageIndex] || {};

  const advance = () => {
    if (stageIndex < stages.length - 1) {
      setStageIndex((i) => i + 1);
    } else {
      onComplete(stageIndex);
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      <p className="text-xs font-mono text-gray-500 bg-gray-100 inline-block px-2 py-1 rounded-full">
        Stage: {stage.stage || stageIndex + 1}
      </p>
      {stage.show_code && stage.prompt && (
        <p className="text-sm text-gray-700">{stage.prompt}</p>
      )}
      {!stage.show_code && stage.starter_code && (
        <textarea
          className="w-full border-2 border-gray-200 rounded-xl p-4 font-mono text-sm focus:outline-none focus:border-brand-500"
          rows={6}
          defaultValue={stage.starter_code}
        />
      )}
      <div className="flex gap-2">
        {stages.map((_, idx) => (
          <div
            key={idx}
            className={`h-2 rounded-full flex-1 ${
              idx <= stageIndex ? "bg-brand-500" : "bg-gray-200"
            }`}
          />
        ))}
      </div>
      <motion.button
        className="bg-brand-500 text-white px-6 py-2 rounded-full"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={advance}
      >
        {stageIndex < stages.length - 1 ? "Next stage" : "Finish"}
      </motion.button>
    </div>
  );
}
