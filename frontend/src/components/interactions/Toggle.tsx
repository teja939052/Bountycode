// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type ToggleProps = {
  condition: string;
  values: any[];
  onToggle: (value: any) => void;
};

export default function Toggle({ condition, values, onToggle }: ToggleProps) {
  const [index, setIndex] = React.useState(0);

  React.useEffect(() => {
    onToggle(values[index]);
  }, [index, onToggle]);

  const cycle = () => {
    setIndex((i) => (i + 1) % values.length);
  };

  return (
    <div className="space-y-3">
      <label className="text-sm font-medium text-gray-700">{condition}</label>
      <motion.button
        className="px-4 py-2 bg-brand-500 text-white rounded-xl text-sm"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={cycle}
      >
        Value: {String(values[index])}
      </motion.button>
    </div>
  );
}
