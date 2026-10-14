// @ts-nocheck
import { motion } from "framer-motion";

export default function AnalogyCard({
  physical,
  action,
  example,
  mentalModel,
  onComplete,
}: {
  physical: string;
  action: string;
  example: string;
  mentalModel?: string;
  onComplete: () => void;
}) {
  return (
    <motion.div
      className="max-w-md mx-auto bg-white rounded-2xl shadow-xl p-6 text-center"
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ type: "spring", stiffness: 200 }}
    >
      <motion.div
        className="text-6xl mb-4"
        animate={{ rotate: [0, 10, -10, 0] }}
        transition={{ repeat: Infinity, duration: 3 }}
      >
        📦
      </motion.div>
      <h3 className="text-xl font-bold mb-2">Think of it like this:</h3>
      <p className="text-lg mb-4">{physical}</p>
      <p className="text-sm text-gray-600 mb-2">Action: {action}</p>
      {example ? (
        <code className="bg-gray-100 rounded px-3 py-1 text-sm">{example}</code>
      ) : null}
      {mentalModel ? (
        <p className="text-xs text-gray-500 mt-3 italic">{mentalModel}</p>
      ) : null}
      <motion.button
        className="mt-6 bg-brand-500 text-white px-6 py-2 rounded-full"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onComplete}
      >
        I get it — let&apos;s try it
      </motion.button>
    </motion.div>
  );
}
