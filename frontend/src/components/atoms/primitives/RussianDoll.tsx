// @ts-nocheck
import { motion, AnimatePresence } from "framer-motion";

type Doll = { id: string; size: number; color: string };

type RussianDollProps = {
  dolls: Doll[];
  openIndex?: number;
};

export default function RussianDoll({ dolls, openIndex = 0 }: RussianDollProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative w-32 h-40 flex items-center justify-center">
        <AnimatePresence mode="wait">
          {dolls.map((doll, idx) => (
            idx <= openIndex && (
              <motion.div
                key={doll.id}
                className="absolute rounded-full border-4 border-white shadow-md"
                style={{
                  width: doll.size,
                  height: doll.size,
                  backgroundColor: doll.color,
                }}
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0, opacity: 0 }}
                transition={{ type: "spring", stiffness: 200, delay: idx * 0.1 }}
              />
            )
          ))}
        </AnimatePresence>
      </div>
      <p className="text-xs text-gray-500">Open until smallest</p>
    </div>
  );
}
