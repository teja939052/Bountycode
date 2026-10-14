// @ts-nocheck
import { motion } from "framer-motion";

type BlueprintProps = {
  rooms: Array<{ id: string; label: string }>;
  builtInstance?: { label: string };
};

export default function Blueprint({ rooms, builtInstance }: BlueprintProps) {
  return (
    <div className="flex flex-col items-center gap-3">
      <div className="grid grid-cols-3 gap-2">
        {rooms.map((room) => (
          <motion.div
            key={room.id}
            className="w-16 h-16 bg-blue-50 border-2 border-dashed border-blue-200 rounded-lg flex items-center justify-center text-xs text-blue-600 font-medium"
            whileHover={{ scale: 1.05, borderColor: "#3B82F6" }}
          >
            {room.label}
          </motion.div>
        ))}
      </div>
      {builtInstance && (
        <motion.div
          className="mt-2 px-4 py-2 bg-brand-500 text-white rounded-lg text-sm font-medium shadow-md"
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: "spring", stiffness: 200 }}
        >
          🏠 {builtInstance.label}
        </motion.div>
      )}
      <p className="text-xs text-gray-500">Blueprint → Instance</p>
    </div>
  );
}
