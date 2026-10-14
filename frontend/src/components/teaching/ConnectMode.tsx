// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type ConnectModeProps = {
  title: string;
  teacher_say: string;
  problem: string;
  _interaction_type?: string;
  _correct_answer?: string[];
  success_feedback?: string;
  _failure_feedback?: string;
  onComplete: () => void;
};

export default function ConnectMode({
  title,
  teacher_say,
  problem,
  success_feedback,
  onComplete,
}: ConnectModeProps) {
  const [done, setDone] = React.useState(false);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      <p className="text-lg text-gray-700">{teacher_say}</p>
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
        <p className="text-sm font-medium text-blue-900 mb-1">Your challenge</p>
        <p className="text-sm text-blue-800">{problem}</p>
      </div>
      {!done ? (
        <motion.button
          className="bg-brand-500 text-white px-6 py-2 rounded-full"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setDone(true)}
        >
          I tried it
        </motion.button>
      ) : (
        <motion.div
          className="bg-green-50 border border-green-200 rounded-xl p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <p className="text-sm text-green-800">{success_feedback || "Great."}</p>
          <motion.button
            className="mt-3 bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onComplete}
          >
            Continue
          </motion.button>
        </motion.div>
      )}
    </div>
  );
}
