// @ts-nocheck
import { motion } from "framer-motion";

type FunctionMachineProps = {
  input?: string;
  output?: string;
  processing?: boolean;
};

export default function FunctionMachine({ input, output, processing }: FunctionMachineProps) {
  return (
    <div className="inline-flex items-center gap-3">
      <motion.div
        className="px-4 py-2 bg-gray-100 border-2 border-dashed border-gray-300 rounded-xl text-sm font-mono"
        animate={{ scale: processing ? [1, 1.05, 1] : 1 }}
        transition={{ duration: 0.4 }}
      >
        {input || "input"}
      </motion.div>
      <motion.div
        className="text-2xl"
        animate={{ x: processing ? [0, 5, 0] : 0 }}
        transition={{ repeat: Infinity, duration: 0.8 }}
      >
        ⚙️
      </motion.div>
      <motion.div
        className="px-4 py-2 bg-brand-500 text-white rounded-xl text-sm font-mono shadow-md"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        {output || "output"}
      </motion.div>
    </div>
  );
}
