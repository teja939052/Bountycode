import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Terminal, CheckCircle, XCircle, ArrowRight } from "lucide-react";

interface PredictQuestion {
  id: string;
  code: string;
  input?: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  language?: string;
}

interface PredictOutputProps {
  questions: PredictQuestion[];
  onComplete?: (score: number, total: number) => void;
}

export default function PredictOutput({
  questions,
  onComplete,
}: PredictOutputProps) {
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [answered, setAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [finished, setFinished] = useState(false);

  const q = questions[current];

  const handleSelect = useCallback(
    (idx: number) => {
      if (answered) return;
      setSelected(idx);
      setAnswered(true);
      if (idx === q.correctIndex) setScore((s) => s + 1);
    },
    [answered, q]
  );

  const handleNext = useCallback(() => {
    if (current < questions.length - 1) {
      setCurrent((c) => c + 1);
      setSelected(null);
      setAnswered(false);
    } else {
      setFinished(true);
      onComplete?.(score, questions.length);
    }
  }, [current, questions.length, onComplete, score]);

  if (finished) {
    const pct = Math.round((score / questions.length) * 100);
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="rounded-2xl border border-border bg-surface p-8 text-center shadow-card"
      >
        <div className="text-5xl mb-4">{pct >= 80 ? "🧠" : pct >= 50 ? "🤔" : "📖"}</div>
        <h3 className="text-xl font-black text-text-primary mb-2">
          Predict Output: {score}/{questions.length}
        </h3>
        <p className="text-sm text-text-secondary mb-4">
          {pct >= 80
            ? "Excellent! You can trace code mentally."
            : "Keep practicing. Mental tracing improves with experience."}
        </p>
        <div className="text-3xl font-black text-primary">{pct}%</div>
      </motion.div>
    );
  }

  if (!q) return null;

  return (
    <div className="rounded-2xl border border-border bg-surface overflow-hidden shadow-card">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-surface-elevated">
        <div className="flex items-center gap-2">
          <Terminal size={18} className="text-emerald-400" />
          <span className="font-bold text-sm text-text-primary">
            Predict the Output
          </span>
        </div>
        <span className="text-xs text-text-muted font-mono">
          {current + 1}/{questions.length}
        </span>
      </div>

      <div className="p-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={current}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
          >
            {/* Code block */}
            <div className="rounded-xl bg-slate-900 border border-slate-700 p-4 mb-5 overflow-x-auto">
              <pre className="text-xs font-mono text-slate-200 leading-relaxed whitespace-pre">
                {q.code}
              </pre>
            </div>

            {q.input && (
              <p className="text-xs text-text-muted mb-3 font-mono">
                Input: <span className="text-primary">{q.input}</span>
              </p>
            )}

            <p className="text-sm text-text-secondary mb-4 font-medium">
              What does this print?
            </p>

            {/* Options */}
            <div className="grid grid-cols-2 gap-2">
              {q.options.map((opt, idx) => {
                const isCorrect = idx === q.correctIndex;
                const isSelected = idx === selected;
                let style = "border-border hover:border-primary/50 hover:bg-primary/5";
                if (answered) {
                  if (isCorrect) style = "border-emerald-400 bg-emerald-500/10";
                  else if (isSelected && !isCorrect)
                    style = "border-rose-400 bg-rose-500/10";
                  else style = "border-border opacity-50";
                }

                return (
                  <button
                    key={idx}
                    onClick={() => handleSelect(idx)}
                    disabled={answered}
                    className={`text-left px-4 py-3 rounded-xl border text-sm font-mono transition-all ${style}`}
                  >
                    <span className="text-text-primary">{opt}</span>
                    {answered && isCorrect && (
                      <CheckCircle
                        size={14}
                        className="inline ml-2 text-emerald-400"
                      />
                    )}
                    {answered && isSelected && !isCorrect && (
                      <XCircle
                        size={14}
                        className="inline ml-2 text-rose-400"
                      />
                    )}
                  </button>
                );
              })}
            </div>

            {/* Explanation */}
            <AnimatePresence>
              {answered && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden"
                >
                  <div className="mt-4 p-3 rounded-xl bg-surface-elevated border border-border">
                    <p className="text-xs text-text-secondary leading-relaxed">
                      {q.explanation}
                    </p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </AnimatePresence>
      </div>

      {answered && (
        <div className="flex justify-end px-6 pb-4">
          <button
            onClick={handleNext}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary text-white text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            {current < questions.length - 1 ? "Next" : "See Results"}
            <ArrowRight size={16} />
          </button>
        </div>
      )}
    </div>
  );
}
