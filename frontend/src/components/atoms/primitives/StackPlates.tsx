// @ts-nocheck
import { motion } from "framer-motion";

type Plate = { id: string; label: string; color: string };

type StackPlatesProps = {
  plates: Plate[];
  onPop?: () => void;
  onPush?: (plate: Plate) => void;
};

export default function StackPlates({ plates, onPop, onPush }: StackPlatesProps) {
  return (
    <div className="flex flex-col items-center gap-3">
      <p className="text-xs font-mono text-gray-500">Stack (last in, first out)</p>
      <div className="relative w-40 h-48 bg-gray-100 rounded-xl border-2 border-dashed border-gray-300 flex flex-col-reverse items-center gap-1 p-2 overflow-hidden">
        {plates.map((plate) => (
          <motion.div
            key={plate.id}
            className="w-full rounded-lg px-3 py-1 text-white text-sm font-medium shadow-sm text-center"
            style={{ backgroundColor: plate.color }}
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -20, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 20 }}
          >
            {plate.label}
          </motion.div>
        ))}
        {plates.length === 0 && (
          <p className="text-xs text-gray-400 mt-auto">Empty stack</p>
        )}
      </div>
      <div className="flex gap-2">
        <motion.button
          className="px-3 py-1 bg-brand-500 text-white rounded-lg text-sm disabled:opacity-30"
          onClick={onPop}
          disabled={plates.length === 0}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Pop
        </motion.button>
        <motion.button
          className="px-3 py-1 bg-gray-200 rounded-lg text-sm"
          onClick={() => onPush?.({ id: Date.now().toString(), label: `Plate ${plates.length + 1}`, color: "#6366F1" })}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Push
        </motion.button>
      </div>
    </div>
  );
}
