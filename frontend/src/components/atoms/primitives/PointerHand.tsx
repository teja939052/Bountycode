// @ts-nocheck
import { motion } from "framer-motion";

type PointerHandProps = {
  target: { label: string; color?: string };
  pointingAt?: string;
};

export default function PointerHand({ target, pointingAt }: PointerHandProps) {
  return (
    <div className="relative inline-flex items-center justify-center p-6">
      <motion.div
        className="text-6xl"
        animate={{
          x: pointingAt === "left" ? -20 : pointingAt === "right" ? 20 : 0,
          y: pointingAt === "up" ? -20 : pointingAt === "down" ? 20 : 0,
        }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
      >
        👆
      </motion.div>
      <motion.div
        className="ml-4 px-4 py-2 rounded-lg text-white font-medium shadow-md"
        style={{ backgroundColor: target.color || "#4B5563" }}
        animate={{ scale: [1, 1.05, 1] }}
        transition={{ repeat: Infinity, duration: 2 }}
      >
        {target.label}
      </motion.div>
    </div>
  );
}
