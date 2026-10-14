// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type ProveModeProps = {
  title: string;
  tasks: Array<any>;
  passing_score: number;
  onComplete: (passed: boolean) => void;
};

export default function ProveMode({ title, tasks, passing_score, onComplete }: ProveModeProps) {
  const [taskIndex, setTaskIndex] = React.useState(0);
  const [score, setScore] = React.useState(0);
  const [_answers, setAnswers] = React.useState<Record<number, any>>({});

  const task = tasks[taskIndex] || {};
  const last = taskIndex >= tasks.length - 1;

  const handleTaskComplete = (correct: boolean) => {
    setAnswers((prev) => ({ ...prev, [taskIndex]: correct }));
    if (correct) setScore((s) => s + 1);
    if (!last) {
      setTaskIndex((i) => i + 1);
    } else {
      const passed = ((score + (correct ? 1 : 0)) / tasks.length) * 100 >= passing_score;
      onComplete(passed);
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      <p className="text-xs text-gray-500">
        Task {taskIndex + 1} of {tasks.length} · Score: {score}/{tasks.length}
      </p>
      {task.type === "predict" && (
        <PredictTask task={task} onComplete={handleTaskComplete} />
      )}
      {task.type === "code" && (
        <CodeTask task={task} onComplete={handleTaskComplete} />
      )}
      {task.type === "debug" && (
        <DebugTask task={task} onComplete={handleTaskComplete} />
      )}
    </div>
  );
}

function PredictTask({ task, onComplete }: { task: any; onComplete: (c: boolean) => void }) {
  const [answer, setAnswer] = React.useState("");
  const [checked, setChecked] = React.useState(false);
  const expected = (task.answer || "").toLowerCase();
  const normalized = answer.trim().toLowerCase();
  const correct = checked && expected && (normalized.includes(expected) || expected.includes(normalized));

  return (
    <div className="space-y-3">
      <p className="text-gray-800">{task.prompt}</p>
      {!checked ? (
        <>
          <input
            className="w-full border-2 border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-500"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your prediction..."
          />
          <motion.button
            className="bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setChecked(true)}
          >
            Check
          </motion.button>
        </>
      ) : (
        <div className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}>
          <p className="font-medium">{correct ? "Correct!" : "Not quite"}</p>
          <p className="text-sm text-gray-600 mt-1">{task.answer}</p>
          <motion.button
            className="mt-3 bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onComplete(correct)}
          >
            Continue
          </motion.button>
        </div>
      )}
    </div>
  );
}

function CodeTask({ task, onComplete }: { task: any; onComplete: (c: boolean) => void }) {
  const [code, setCode] = React.useState(task.starter_code || "");
  const [submitted, setSubmitted] = React.useState(false);
  const [correct, setCorrect] = React.useState(false);

  const check = () => {
    const normalized = code.trim().replace(/\s+/g, " ");
    const expected = (task.solution || "").trim().replace(/\s+/g, " ");
    const isCorrect = normalized === expected;
    setSubmitted(true);
    setCorrect(isCorrect);
    onComplete(isCorrect);
  };

  return (
    <div className="space-y-3">
      <p className="text-gray-800">{task.prompt}</p>
      <textarea
        className="w-full border-2 border-gray-200 rounded-xl p-4 font-mono text-sm focus:outline-none focus:border-brand-500"
        rows={6}
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
      <motion.button
        className="bg-brand-500 text-white px-6 py-2 rounded-full"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={check}
      >
        Run
      </motion.button>
      {submitted && (
        <div className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}>
          <p className="font-medium">{correct ? "Correct!" : "Not quite"}</p>
          {!correct && (
            <pre className="mt-2 bg-gray-900 text-green-400 rounded-lg p-3 text-xs overflow-x-auto">{task.solution}</pre>
          )}
        </div>
      )}
    </div>
  );
}

function DebugTask({ task, onComplete }: { task: any; onComplete: (c: boolean) => void }) {
  const [answer, setAnswer] = React.useState("");
  const [submitted, setSubmitted] = React.useState(false);
  const expected = (task.answer || "").toLowerCase();
  const normalized = answer.trim().toLowerCase();
  const correct = submitted && expected && (normalized.includes(expected) || expected.includes(normalized));

  return (
    <div className="space-y-3">
      <p className="text-gray-800">{task.question}</p>
      <pre className="bg-gray-900 text-red-400 rounded-xl p-4 text-sm overflow-x-auto">{task.buggy_code}</pre>
      {!submitted ? (
        <>
          <input
            className="w-full border-2 border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-500"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="What is wrong?"
          />
          <motion.button
            className="bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setSubmitted(true)}
          >
            Check
          </motion.button>
        </>
      ) : (
        <div className={`p-4 rounded-xl ${correct ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}>
          <p className="font-medium">{correct ? "Correct!" : "Not quite"}</p>
          <p className="text-sm text-gray-600 mt-1">{task.answer}</p>
          <motion.button
            className="mt-3 bg-brand-500 text-white px-6 py-2 rounded-full"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onComplete(correct)}
          >
            Continue
          </motion.button>
        </div>
      )}
    </div>
  );
}
