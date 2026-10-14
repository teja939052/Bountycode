// @ts-nocheck
import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { GripVertical, CheckCircle2, XCircle, Lightbulb, ArrowRight } from "lucide-react";
import { curriculumApi } from "../../services/api/curriculum";

interface ParsonsProblemProps {
  parsons: {
    id: string;
    title: string;
    language: string;
    lines: string[];
    correct_order: number[];
    distractors: string[];
    hints: string[];
  };
  conceptId: string;
  onComplete: (correct: boolean, attempts: number, timeTaken: number) => void;
}

export default function ParsonsProblem({ parsons, conceptId, onComplete }: ParsonsProblemProps) {
  const [available, setAvailable] = useState<string[]>([...parsons.lines, ...parsons.distractors]);
  const [ordered, setOrdered] = useState<string[]>([]);
  const [feedback, setFeedback] = useState<{ correct: boolean; message: string } | null>(null);
  const [hintIndex, setHintIndex] = useState(0);
  const [attempts, setAttempts] = useState(0);
  const [startTime] = useState(Date.now());

  const moveToOrdered = (idx: number) => {
    setAvailable((prev) => prev.filter((_, i) => i !== idx));
    setOrdered((prev) => [...prev, available[idx]]);
    setFeedback(null);
  };

  const moveToAvailable = (idx: number) => {
    const [item] = ordered.splice(idx, 1);
    setAvailable((prev) => [...prev, item]);
    setOrdered([...ordered]);
    setFeedback(null);
  };

  const check = useCallback(async () => {
    const selectedOrder = ordered.map((line) => {
      const idx = [...parsons.lines, ...parsons.distractors].indexOf(line);
      return idx;
    });

    const result = await curriculumApi.validateParsons(conceptId, parsons.id, selectedOrder);
    const timeTaken = (Date.now() - startTime) / 1000;
    setAttempts((a) => a + 1);

    if (result.correct) {
      setFeedback({ correct: true, message: "Correct order! Well done." });
      await curriculumApi.recordParsonsAttempt(conceptId, parsons.id, true, attempts + 1, timeTaken);
      setTimeout(() => onComplete(true, attempts + 1, timeTaken), 1200);
    } else {
      setFeedback({ correct: false, message: result.explanation });
      setHintIndex((h) => Math.min(h + 1, parsons.hints.length));
    }
  }, [ordered, parsons, conceptId, startTime, attempts, onComplete]);

  const shuffle = () => {
    const shuffled = [...available].sort(() => Math.random() - 0.5);
    setAvailable(shuffled);
    setFeedback(null);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl font-extrabold text-text-primary">Parson's: {parsons.title}</h2>
        <p className="mt-1 text-sm text-text-secondary">
          Drag or click the lines below to arrange them in the correct order. Extra lines are distractors.
        </p>
      </div>

      {/* Available lines */}
      <div className="rounded-2xl border border-dashed border-black/15 bg-slate-50/60 p-4">
        <p className="mb-3 text-xs font-mono uppercase tracking-widest text-text-muted">Available Lines</p>
        <div className="flex flex-wrap gap-2">
          <AnimatePresence>
            {available.map((line, idx) => (
              <motion.button
                key={`avail-${idx}-${line}`}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                onClick={() => moveToOrdered(idx)}
                className="group flex items-center gap-2 rounded-xl border border-black/10 bg-white px-3 py-2 text-left font-mono text-xs shadow-sm transition hover:border-emerald-300 hover:shadow-md"
              >
                <GripVertical className="h-3.5 w-3.5 text-text-muted" />
                {line}
              </motion.button>
            ))}
          </AnimatePresence>
        </div>
      </div>

      {/* Ordered lines */}
      <div className="rounded-2xl border border-black/10 bg-white p-4">
        <p className="mb-3 text-xs font-mono uppercase tracking-widest text-text-muted">Your Order</p>
        <div className="flex flex-col gap-2">
          <AnimatePresence>
            {ordered.map((line, idx) => (
              <motion.div
                key={`ord-${idx}-${line}`}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50/60 px-3 py-2 font-mono text-xs"
              >
                <span className="flex h-5 w-5 items-center justify-center rounded-full bg-emerald-500 text-[10px] font-black text-white">{idx + 1}</span>
                {line}
                <button onClick={() => moveToAvailable(idx)} className="ml-auto text-text-muted hover:text-red-500">
                  <XCircle className="h-4 w-4" />
                </button>
              </motion.div>
            ))}
          </AnimatePresence>
          {ordered.length === 0 && (
            <p className="py-4 text-center text-xs text-text-muted">Click lines above to add them here</p>
          )}
        </div>
      </div>

      {/* Feedback */}
      <AnimatePresence>
        {feedback && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`rounded-2xl p-4 ${feedback.correct ? "border border-emerald-200 bg-emerald-50/60" : "border border-red-200 bg-red-50/60"}`}
          >
            <div className="flex items-center gap-2">
              {feedback.correct ? <CheckCircle2 className="h-5 w-5 text-emerald-600" /> : <XCircle className="h-5 w-5 text-red-600" />}
              <p className={`text-sm font-bold ${feedback.correct ? "text-emerald-800" : "text-red-800"}`}>{feedback.message}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Hint */}
      {hintIndex > 0 && !feedback?.correct && (
        <div className="rounded-2xl border border-amber-200 bg-amber-50/60 p-4">
          <div className="flex items-center gap-2">
            <Lightbulb className="h-4 w-4 text-amber-600" />
            <p className="text-sm font-bold text-amber-800">Hint {hintIndex}</p>
          </div>
          <p className="mt-1 text-sm text-amber-900">{parsons.hints[hintIndex - 1]}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex justify-between">
        <button onClick={shuffle} className="rounded-xl border border-black/10 px-4 py-2 text-xs font-bold text-text-muted hover:bg-black/5">
          Shuffle
        </button>
        <button onClick={check} disabled={ordered.length === 0} className="rounded-xl bg-emerald-600 px-6 py-3 text-sm font-bold text-white hover:bg-emerald-700 disabled:opacity-40">
          Check Order
        </button>
      </div>
    </div>
  );
}
