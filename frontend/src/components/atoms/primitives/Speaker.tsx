// @ts-nocheck
import { motion } from "framer-motion";

type SpeakerProps = {
  text: string;
  volume?: number;
};

export default function Speaker({ text, volume = 1 }: SpeakerProps) {
  return (
    <div className="inline-flex items-center gap-3 bg-gray-50 border rounded-xl px-4 py-3 shadow-sm">
      <motion.div
        className="text-3xl"
        animate={{ scale: [1, 1.2, 1] }}
        transition={{ repeat: Infinity, duration: 1.5 / (volume || 1) }}
      >
        🔊
      </motion.div>
      <motion.p
        className="text-lg font-medium text-gray-800"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        key={text}
      >
        {text}
      </motion.p>
    </div>
  );
}
