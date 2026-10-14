// @ts-nocheck
import { useState } from "react";
import { motion } from "framer-motion";

export default function MisconceptionRepair({
  misconception,
  repair,
  onRepaired,
}: {
  misconception: any;
  repair: any;
  onRepaired: () => void;
}) {
  const [showFix, setShowFix] = useState(false);

  return (
    <motion.div
      className="max-w-md mx-auto bg-red-50 border border-red-200 rounded-2xl p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <h3 className="text-lg font-bold text-red-800 mb-2">Not quite — let&apos;s repair that.</h3>
      <p className="text-red-700 mb-2">{misconception.break_scene || misconception.mental_model || "That answer suggests a common misconception."}</p>
      {!showFix ? (
        <motion.button
          className="bg-red-600 text-white px-4 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowFix(true)}
        >
          Show me the fix
        </motion.button>
      ) : (
        <div>
          <p className="text-green-800 font-medium mb-4">{misconception.fix || repair.correct_mental_model || ""}</p>
          <motion.button
            className="bg-green-600 text-white px-4 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onRepaired}
          >
            Got it
          </motion.button>
        </div>
      )}
    </motion.div>
  );
}
