// @ts-nocheck
import { motion } from "framer-motion";

type ConveyorBeltProps = {
  items: Array<{ id: string; label: string }>;
  activeIndex?: number;
};

export default function ConveyorBelt({ items, activeIndex = 0 }: ConveyorBeltProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {items.map((item, idx) => (
          <motion.div
            key={item.id}
            className={`px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap ${
              idx === activeIndex ? "bg-brand-500 text-white" : "bg-gray-200 text-gray-700"
            }`}
            animate={{ x: idx === activeIndex ? [0, -5, 0] : 0 }}
            transition={{ duration: 0.3 }}
          >
            {item.label}
          </motion.div>
        ))}
      </div>
      <div className="w-full h-1 bg-gray-200 rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-brand-500"
          animate={{ width: `${((activeIndex + 1) / Math.max(1, items.length)) * 100}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>
      <p className="text-xs text-gray-500">Code runs top to bottom</p>
    </div>
  );
}
