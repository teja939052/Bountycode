// @ts-nocheck
import { motion, AnimatePresence } from "framer-motion";
import React from "react";

export default function VisualMachineModel({
  steps,
  onComplete,
}: {
  steps: Array<{ scene: string; duration_ms: number }>;
  onComplete: () => void;
}) {
  const [index, setIndex] = React.useState(0);

  React.useEffect(() => {
    if (index >= steps.length) {
      onComplete();
      return;
    }
    const timer = setTimeout(() => setIndex((i) => i + 1), steps[index].duration_ms);
    return () => clearTimeout(timer);
  }, [index, steps, onComplete]);

  return (
    <div className="max-w-lg mx-auto text-center">
      <AnimatePresence mode="wait">
        <motion.p
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="text-xl"
        >
          {steps[index]?.scene}
        </motion.p>
      </AnimatePresence>
      <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-brand-500"
          animate={{ width: `${((index + 1) / steps.length) * 100}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>
    </div>
  );
}
