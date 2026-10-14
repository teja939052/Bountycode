// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type ShowModeProps = {
  title: string;
  frames: Array<{ scene: string; duration_ms?: number }>;
  onComplete: () => void;
};

export default function ShowMode({ title, frames, onComplete }: ShowModeProps) {
  const [frameIndex, setFrameIndex] = React.useState(0);

  React.useEffect(() => {
    if (frameIndex < frames.length - 1) {
      const ms = frames[frameIndex].duration_ms || 1200;
      const timer = setTimeout(() => setFrameIndex((i) => i + 1), ms);
      return () => clearTimeout(timer);
    }
  }, [frameIndex, frames]);

  const frame = frames[frameIndex] || {};

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      <div className="bg-gray-900 text-green-400 rounded-xl p-6 font-mono text-sm min-h-[120px] flex items-center">
        <motion.span
          key={frame.scene}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {frame.scene}
        </motion.span>
      </div>
      <div className="flex items-center gap-2">
        {frames.map((_, idx) => (
          <div
            key={idx}
            className={`h-2 rounded-full flex-1 ${
              idx === frameIndex ? "bg-brand-500" : "bg-gray-200"
            }`}
          />
        ))}
      </div>
      {frameIndex >= frames.length - 1 && (
        <motion.button
          className="bg-green-600 text-white px-6 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onComplete}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          Continue
        </motion.button>
      )}
    </div>
  );
}
