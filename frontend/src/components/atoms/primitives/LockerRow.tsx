// @ts-nocheck
import { motion } from "framer-motion";

type LockerRowProps = {
  items: Array<{ id: string; label: string; color?: string }>;
  activeIndex?: number;
};

export default function LockerRow({ items, activeIndex = 0 }: LockerRowProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="flex gap-2">
        {items.map((item, idx) => (
          <motion.div
            key={item.id}
            className={`w-16 h-20 rounded-lg border-2 flex flex-col items-center justify-center gap-1 ${
              idx === activeIndex ? "border-brand-500 bg-brand-50" : "border-gray-200 bg-white"
            }`}
            whileHover={{ scale: 1.05 }}
          >
            <span className="text-xs font-mono text-gray-400">#{idx}</span>
            <span className="text-sm font-medium text-gray-700">{item.label}</span>
          </motion.div>
        ))}
      </div>
      <p className="text-xs text-gray-500">Lockers numbered 0, 1, 2...</p>
    </div>
  );
}
