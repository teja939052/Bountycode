import { useState, useCallback } from "react";
import { motion, AnimatePresence, Reorder } from "framer-motion";
import { GripVertical, CheckCircle, XCircle, ArrowRight, RotateCcw } from "lucide-react";

interface Step {
  id: string;
  text: string;
  order: number;
}

interface OrderStepsProps {
  steps: Step[];
  title?: string;
  explanation?: string;
  onComplete?: (correct: boolean, attempts: number) => void;
}

export default function OrderSteps({
  steps: initialSteps,
  title = "Order the Steps",
  explanation,
  onComplete,
}: OrderStepsProps) {
  const [items, setItems] = useState<Step[]>(() =>
    [...initialSteps].sort(() => Math.random() - 0.5)
  );
  const [submitted, setSubmitted] = useState(false);
  const [correct, setCorrect] = useState(false);
  const [attempts, setAttempts] = useState(0);

  const handleSubmit = useCallback(() => {
    const isCorrect = items.every((item, idx) => item.order === idx + 1);
    setCorrect(isCorrect);
    setSubmitted(true);
    setAttempts((a) => a + 1);
    if (isCorrect) onComplete?.(true, attempts + 1);
  }, [items, onComplete, attempts]);

  const handleReset = () => {
    setItems([...initialSteps].sort(() => Math.random() - 0.5));
    setSubmitted(false);
    setCorrect(false);
  };

  return (
    <div className="rounded-2xl border border-border bg-surface overflow-hidden shadow-card">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-surface-elevated">
        <div className="flex items-center gap-2">
          <GripVertical size={18} className="text-primary" />
          <span className="font-bold text-sm text-text-primary">{title}</span>
        </div>
        {attempts > 0 && (
          <span className="text-xs text-text-muted">Attempts: {attempts}</span>
        )}
      </div>

      <div className="p-6">
        <p className="text-sm text-text-secondary mb-4">
          Drag to arrange the steps in the correct order:
        </p>

        <Reorder.Group
          axis="y"
          values={items}
          onReorder={setItems}
          className="space-y-2"
        >
          {items.map((item, idx) => {
            const isCorrectPosition = submitted && item.order === idx + 1;
            const isWrongPosition = submitted && item.order !== idx + 1;

            return (
              <Reorder.Item
                key={item.id}
                value={item}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl border cursor-grab active:cursor-grabbing transition-colors ${
                  isCorrectPosition
                    ? "border-emerald-400 bg-emerald-500/10"
                    : isWrongPosition
                    ? "border-rose-400 bg-rose-500/10"
                    : "border-border bg-surface-elevated hover:border-primary/30"
                }`}
              >
                <GripVertical size={16} className="text-text-muted flex-shrink-0" />
                <span className="w-6 h-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center flex-shrink-0">
                  {idx + 1}
                </span>
                <span className="text-sm text-text-primary flex-1">
                  {item.text}
                </span>
                {isCorrectPosition && (
                  <CheckCircle size={16} className="text-emerald-400 flex-shrink-0" />
                )}
                {isWrongPosition && (
                  <XCircle size={16} className="text-rose-400 flex-shrink-0" />
                )}
              </Reorder.Item>
            );
          })}
        </Reorder.Group>

        {/* Explanation */}
        <AnimatePresence>
          {submitted && correct && explanation && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden"
            >
              <div className="mt-4 p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
                <p className="text-xs text-emerald-300 leading-relaxed">
                  {explanation}
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-border bg-surface-elevated">
        <button
          onClick={handleReset}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs text-text-muted hover:text-text-primary hover:bg-surface transition-colors"
        >
          <RotateCcw size={14} />
          Shuffle
        </button>
        {!correct && (
          <button
            onClick={handleSubmit}
            className="px-5 py-2 rounded-xl bg-primary text-white text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            Check Order
          </button>
        )}
        {correct && (
          <span className="text-sm font-bold text-emerald-400 flex items-center gap-1">
            <CheckCircle size={16} /> Correct order!
          </span>
        )}
      </div>
    </div>
  );
}
