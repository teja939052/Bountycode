// @ts-nocheck
import { motion, Reorder } from "framer-motion";

type Item = { id: string; label: string };

type QueueLineProps = {
  items: Item[];
  onReorder?: (items: Item[]) => void;
};

export default function QueueLine({ items, onReorder }: QueueLineProps) {
  return (
    <div className="flex flex-col gap-2">
      <p className="text-xs font-mono text-gray-500 mb-1">Queue (first in, first out)</p>
      <Reorder.Group axis="y" values={items} onReorder={onReorder || (() => {})} className="flex flex-col gap-2">
        {items.map((item) => (
          <Reorder.Item key={item.id} value={item} className="cursor-grab active:cursor-grabbing">
            <motion.div
              className="flex items-center gap-2 bg-white border rounded-lg px-4 py-2 shadow-sm"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <span className="text-lg">🧍</span>
              <span className="font-medium">{item.label}</span>
            </motion.div>
          </Reorder.Item>
        ))}
      </Reorder.Group>
      <p className="text-xs text-gray-500 mt-1">Drag to reorder. First item leaves first.</p>
    </div>
  );
}
