// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type SameConceptNewWorldProps = {
  context: string;
  story: string;
  task: string;
  onComplete: (answer: string) => void;
};

export default function SameConceptNewWorld({ context, story, task, onComplete }: SameConceptNewWorldProps) {
  const [answer, setAnswer] = React.useState("");
  const [submitted, setSubmitted] = React.useState(false);

  return (
    <div className="space-y-4">
      <div className="bg-purple-50 border border-purple-200 rounded-xl p-4">
        <p className="text-xs font-mono text-purple-700 mb-1">NEW CONTEXT: {context}</p>
        <p className="text-sm text-purple-900">{story}</p>
      </div>
      <p className="text-gray-900">{task}</p>
      {!submitted ? (
        <>
          <textarea
            className="w-full border-2 border-gray-200 rounded-xl p-4 focus:outline-none focus:border-brand-500"
            rows={4}
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Write your solution..."
          />
          <motion.button
            className="bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => { setSubmitted(true); onComplete(answer); }}
          >
            Submit
          </motion.button>
        </>
      ) : (
        <div className="bg-green-50 border border-green-200 rounded-xl p-4">
          <p className="font-medium">Solution recorded</p>
          <p className="text-sm text-gray-600 mt-1">{answer}</p>
        </div>
      )}
    </div>
  );
}
