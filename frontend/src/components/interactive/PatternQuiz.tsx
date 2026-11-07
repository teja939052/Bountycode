import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle, XCircle, ArrowRight, Zap } from "lucide-react";

interface QuizQuestion {
  id: string;
  problemStatement: string;
  options: string[];
  correctIndex: number;
  explanation: string;
  pattern: string;
}

interface PatternQuizProps {
  questions: QuizQuestion[];
  onComplete?: (score: number, total: number) => void;
  timePerQuestion?: number;
}

export default function PatternQuiz({
  questions,
  onComplete,
  timePerQuestion = 15,
}: PatternQuizProps) {
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [answered, setAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [timeLeft, setTimeLeft] = useState(timePerQuestion);
  const [finished, setFinished] = useState(false);

  const q = questions[current];
  const total = questions.length;

  const handleSelect = useCallback(
    (idx: number) => {
      if (answered) return;
      setSelected(idx);
      setAnswered(true);
      const correct = idx === q.correctIndex;
      if (correct) {
        setScore((s) => s + 1);
        setStreak((s) => s + 1);
      } else {
        setStreak(0);
      }
    },
    [answered, q]
  );

  const handleNext = useCallback(() => {
    if (current < total - 1) {
      setCurrent((c) => c + 1);
      setSelected(null);
      setAnswered(false);
      setTimeLeft(timePerQuestion);
    } else {
      setFinished(true);
      onComplete?.(score + (selected === q.correctIndex ? 0 : 0), total);
    }
  }, [current, total, onComplete, score, selected, q, timePerQuestion]);

  // Timer
  useState(() => {
    const interval = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1 && !answered) {
          setAnswered(true);
          setStreak(0);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  });

  if (finished) {
    const pct = Math.round((score / total) * 100);
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="rounded-2xl border border-border bg-surface p-8 text-center shadow-card"
      >
        <div className="text-5xl mb-4">{pct >= 80 ? "🎯" : pct >= 50 ? "💪" : "📚"}</div>
        <h3 className="text-xl font-black text-text-primary mb-2">
          Pattern Recognition: {score}/{total}
        </h3>
        <p className="text-sm text-text-secondary mb-4">
          {pct >= 80
            ? "Excellent! You can identify patterns quickly."
            : pct >= 50
            ? "Good progress. Practice will sharpen your recognition."
            : "Keep studying the patterns. Recognition improves with exposure."}
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
          <Zap size={18} className="text-amber-400" />
          <span className="font-bold text-sm text-text-primary">
            Pattern Recognition
          </span>
        </div>
        <div className="flex items-center gap-3">
          {streak >= 2 && (
            <span className="text-xs font-bold text-amber-400">
              🔥 {streak} streak
            </span>
          )}
          <span className="text-xs text-text-muted font-mono">
            {current + 1}/{total}
          </span>
          <div
            className={`w-8 h-8 rounded-full border-2 flex items-center justify-center text-xs font-bold ${
              timeLeft > 5
                ? "border-emerald-400 text-emerald-400"
                : timeLeft > 0
                ? "border-amber-400 text-amber-400"
                : "border-rose-400 text-rose-400"
            }`}
          >
            {timeLeft}
          </div>
        </div>
      </div>

      {/* Progress */}
      <div className="h-1 bg-surface-elevated">
        <motion.div
          className="h-full bg-primary"
          animate={{ width: `${((current + 1) / total) * 100}%` }}
        />
      </div>

      {/* Question */}
      <div className="p-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={current}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
          >
            <p className="text-sm text-text-secondary mb-1 font-mono">
              Which pattern applies?
            </p>
            <h4 className="text-base font-bold text-text-primary mb-5 leading-relaxed">
              {q.problemStatement}
            </h4>

            {/* Options */}
            <div className="space-y-2">
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
                    className={`w-full text-left px-4 py-3 rounded-xl border text-sm transition-all ${style}`}
                  >
                    <span className="font-medium text-text-primary">{opt}</span>
                    {answered && isCorrect && (
                      <CheckCircle
                        size={16}
                        className="inline ml-2 text-emerald-400"
                      />
                    )}
                    {answered && isSelected && !isCorrect && (
                      <XCircle size={16} className="inline ml-2 text-rose-400" />
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
                    <p className="text-xs text-primary mt-2 font-medium">
                      Pattern: {q.pattern}
                    </p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Footer */}
      {answered && (
        <div className="flex justify-end px-6 pb-4">
          <button
            onClick={handleNext}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary text-white text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            {current < total - 1 ? "Next" : "See Results"}
            <ArrowRight size={16} />
          </button>
        </div>
      )}
    </div>
  );
}
