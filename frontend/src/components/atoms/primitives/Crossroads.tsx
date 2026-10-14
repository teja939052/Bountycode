// @ts-nocheck
import { motion } from "framer-motion";

type CrossroadsProps = {
  paths: string[];
  chosen?: string;
};

export default function Crossroads({ paths, chosen }: CrossroadsProps) {
  return (
    <div className="flex flex-col items-center gap-3">
      <div className="flex items-center gap-4">
        {paths.map((path) => (
          <motion.div
            key={path}
            className={`px-4 py-2 rounded-xl text-sm font-medium border-2 ${
              chosen === path
                ? "bg-brand-500 text-white border-brand-500"
                : "bg-white text-gray-700 border-gray-200"
            }`}
            whileHover={{ scale: 1.05 }}
          >
            {path}
          </motion.div>
        ))}
      </div>
      <p className="text-xs text-gray-500">A branch in the road — choose one path</p>
    </div>
  );
}
