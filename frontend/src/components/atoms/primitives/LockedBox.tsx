// @ts-nocheck
import { motion } from "framer-motion";

type LockedBoxProps = {
  note?: string;
  locked?: boolean;
};

export default function LockedBox({ note = "Secret note", locked = true }: LockedBoxProps) {
  return (
    <div className="flex flex-col items-center gap-3">
      <motion.div
        className="relative w-24 h-24 bg-gray-800 rounded-xl flex items-center justify-center shadow-lg"
        animate={{ rotateY: locked ? 0 : 180 }}
        transition={{ duration: 0.6 }}
      >
        {locked ? (
          <motion.span className="text-4xl" animate={{ scale: [1, 1.1, 1] }} transition={{ repeat: Infinity, duration: 2 }}>
            🔒
          </motion.span>
        ) : (
          <motion.span className="text-4xl" initial={{ rotateY: 180 }} animate={{ rotateY: 0 }}>
            📝
          </motion.span>
        )}
      </motion.div>
      <motion.p
        className={`text-sm font-medium ${locked ? "text-gray-500" : "text-gray-900"}`}
        animate={{ opacity: locked ? 0.5 : 1 }}
      >
        {locked ? "Locked — only keyholder can read" : note}
      </motion.p>
    </div>
  );
}
