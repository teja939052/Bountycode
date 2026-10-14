// @ts-nocheck
import { motion } from "framer-motion";

type CameraProps = {
  snapshots: string[];
  activeSnapshot?: number;
};

export default function Camera({ snapshots, activeSnapshot = 0 }: CameraProps) {
  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex items-center gap-2">
        <motion.div
          className="text-4xl"
          animate={{ rotate: [0, -10, 10, 0] }}
          transition={{ repeat: Infinity, duration: 2 }}
        >
          📷
        </motion.div>
        <motion.div
          className="px-4 py-2 bg-gray-900 text-white rounded-lg font-mono text-sm"
          animate={{ opacity: [0.7, 1, 0.7] }}
          transition={{ repeat: Infinity, duration: 1.5 }}
        >
          {snapshots[activeSnapshot] || "Ready..."}
        </motion.div>
      </div>
      <div className="flex gap-2">
        {snapshots.map((_, idx) => (
          <div
            key={idx}
            className={`w-2 h-2 rounded-full ${idx === activeSnapshot ? "bg-brand-500" : "bg-gray-300"}`}
          />
        ))}
      </div>
    </div>
  );
}
