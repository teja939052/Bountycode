// @ts-nocheck
import React from "react";
import { motion, Reorder } from "framer-motion";

type CodeBlocksProps = {
  blocks: string[];
  correctOrder: number[];
  onComplete: (order: number[]) => void;
};

export default function CodeBlocks({ blocks, correctOrder, onComplete }: CodeBlocksProps) {
  const [order, setOrder] = React.useState(() => [...correctOrder]);
  const [checked, setChecked] = React.useState(false);
  const correct = checked && order.every((val, idx) => val === correctOrder[idx]);

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-600">Arrange the blocks into the correct program order</p>
      <Reorder.Group axis="y" values={order} onReorder={setOrder} className="space-y-2">
        {order.map((blockIdx, displayIdx) => (
          <Reorder.Item
            key={`${blockIdx}-${displayIdx}`}
            value={blockIdx}
            className={`px-4 py-3 rounded-xl border-2 cursor-move ${
              checked
                ? correct
                  ? "bg-green-50 border-green-300"
                  : "bg-red-50 border-red-300"
                : "bg-white border-gray-200"
            }`}
          >
            <span className="text-sm font-mono text-gray-800">{blocks[blockIdx]}</span>
          </Reorder.Item>
        ))}
      </Reorder.Group>
      <motion.button
        className="bg-green-600 text-white px-6 py-2 rounded-full"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => { setChecked(true); onComplete(order); }}
      >
        Check order
      </motion.button>
      {checked && (
        <p className={`text-sm ${correct ? "text-green-600" : "text-red-600"}`}>
          {correct ? "Correct order!" : "Not quite — try rearranging"}
        </p>
      )}
    </div>
  );
}
