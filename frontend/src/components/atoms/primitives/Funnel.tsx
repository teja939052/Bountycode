// @ts-nocheck
import { motion } from "framer-motion";

type FunnelProps = {
  stages: string[];
  activeStage?: number;
};

export default function Funnel({ stages, activeStage = 0 }: FunnelProps) {
  const widths = ["w-3/4", "w-2/3", "w-1/2", "w-1/3"];
  return (
    <div className="flex flex-col items-center gap-1">
      {stages.map((stage, idx) => (
        <motion.div
          key={idx}
          className={`${widths[idx % widths.length]} bg-brand-500 text-white text-center py-2 rounded-lg text-sm font-medium shadow-sm`}
          animate={{ scale: idx === activeStage ? [1, 1.05, 1] : 1 }}
          transition={{ duration: 0.4 }}
        >
          {stage}
        </motion.div>
      ))}
      <p className="text-xs text-gray-500 mt-2">Input → Process → Output</p>
    </div>
  );
}
