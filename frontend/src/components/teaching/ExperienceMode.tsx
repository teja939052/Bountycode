// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type ExperienceModeProps = {
  title: string;
  instruction: string;
  manipulatives?: Array<any>;
  onComplete: () => void;
};

export default function ExperienceMode({ title, instruction, manipulatives, onComplete }: ExperienceModeProps) {
  const [done, setDone] = React.useState(false);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      <p className="text-gray-700">{instruction}</p>
      {manipulatives && manipulatives.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-xl p-4">
          <p className="text-xs font-mono text-gray-500 mb-2">Interactive area</p>
          <p className="text-sm text-gray-600">
            {manipulatives.map((m, i) => (
              <span key={i}>{m.type}</span>
            ))}
          </p>
        </div>
      )}
      {!done ? (
        <motion.button
          className="bg-brand-500 text-white px-6 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setDone(true)}
        >
          Done
        </motion.button>
      ) : (
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
