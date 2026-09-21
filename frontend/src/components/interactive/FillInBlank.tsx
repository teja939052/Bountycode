import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Code2, CheckCircle, XCircle, Lightbulb, RotateCcw } from "lucide-react";

interface BlankSlot {
  id: string;
  placeholder?: string;
  correctAnswer: string;
  hint?: string;
  width?: number;
}

interface FillInBlankProps {
  codeTemplate: string;
  blanks: BlankSlot[];
  language?: string;
  explanation?: string;
  onComplete?: (correct: boolean, attempts: number) => void;
}

export default function FillInBlank({
  codeTemplate,
  blanks,
  language = "python",
  explanation,
  onComplete,
}: FillInBlankProps) {
  const [answers, setAnswers] = useState<Record<string, string>>(
    Object.fromEntries(blanks.map((b) => [b.id, ""]))
  );
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState<Record<string, boolean>>({});
  const [attempts, setAttempts] = useState(0);
  const [showHint, setShowHint] = useState<string | null>(null);
  const [allCorrect, setAllCorrect] = useState(false);

  const handleSubmit = useCallback(() => {
    const res: Record<string, boolean> = {};
    let correct = true;
    for (const blank of blanks) {
      const userVal = (answers[blank.id] || "").trim().replace(/\s+/g, " ");
      const expected = blank.correctAnswer.trim().replace(/\s+/g, " ");
      res[blank.id] = userVal.toLowerCase() === expected.toLowerCase();
      if (!res[blank.id]) correct = false;
    }
    setResults(res);
    setSubmitted(true);
    setAttempts((a) => a + 1);
    if (correct) onComplete?.(true, attempts + 1);
  }, [answers, blanks, onComplete, attempts]);

  const handleReset = () => {
    setAnswers(Object.fromEntries(blanks.map((b) => [b.id, ""])));
    setSubmitted(false);
    setResults({});
    setShowHint(null);
  };

  // Build rendered code with blanks inline
  const renderCode = () => {
    const parts = codeTemplate.split(/(\{blank:(\w+)\})/);
    return parts.map((part, i) => {
      const match = part.match(/\{blank:(\w+)\}/);
      if (match) {
        const blankId = match[1];
        const blank = blanks.find((b) => b.id === blankId);
        if (!blank) return part;
        const isCorrect = results[blankId];
        const isWrong = submitted && !isCorrect;

        return (
          <span key={blankId} className="inline-flex items-center mx-1">
            <input
              type="text"
              value={answers[blankId] || ""}
              onChange={(e) =>
                setAnswers((a) => ({ ...a, [blankId]: e.target.value }))
              }
              disabled={allCorrect}
              placeholder={blank.placeholder || "..."}
              style={{ width: blank.width || 120 }}
              className={`px-2 py-0.5 rounded-md border text-xs font-mono bg-slate-800 text-white placeholder:text-slate-500 focus:outline-none transition-colors ${
                isCorrect
                  ? "border-emerald-400 bg-emerald-500/10"
                  : isWrong
                  ? "border-rose-400 bg-rose-500/10"
                  : "border-primary/30 focus:border-primary"
              }`}
            />
            {submitted && isCorrect && (
              <CheckCircle size={14} className="ml-1 text-emerald-400" />
            )}
            {isWrong && (
              <XCircle size={14} className="ml-1 text-rose-400" />
            )}
            {blank.hint && submitted && !isCorrect && (
              <button
                onClick={() =>
                  setShowHint(showHint === blankId ? null : blankId)
                }
                className="ml-1 text-amber-400 hover:text-amber-300"
              >
                <Lightbulb size={14} />
              </button>
            )}
          </span>
        );
      }
      return <span key={i}>{part}</span>;
    });
  };

  return (
    <div className="rounded-2xl border border-border bg-surface overflow-hidden shadow-card">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-surface-elevated">
        <div className="flex items-center gap-2">
          <Code2 size={18} className="text-primary" />
          <span className="font-bold text-sm text-text-primary">
            Fill in the Blanks
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs px-2 py-1 rounded-lg bg-surface text-text-muted font-mono">
            {language}
          </span>
          {attempts > 0 && (
            <span className="text-xs text-text-muted">
              Attempts: {attempts}
            </span>
          )}
        </div>
      </div>

      {/* Code area */}
      <div className="p-4 overflow-x-auto">
        <pre className="text-sm font-mono leading-relaxed text-slate-200 whitespace-pre-wrap">
          {renderCode()}
        </pre>
      </div>

      {/* Hint reveal */}
      <AnimatePresence>
        {showHint && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="px-4 py-2 bg-amber-500/5 border-t border-amber-500/20">
              <p className="text-xs text-amber-300">
                💡 {blanks.find((b) => b.id === showHint)?.hint}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Explanation */}
      <AnimatePresence>
        {submitted && allCorrect && explanation && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="px-4 py-3 bg-emerald-500/5 border-t border-emerald-500/20">
              <p className="text-xs text-emerald-300 leading-relaxed">
                {explanation}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Controls */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-border bg-surface-elevated">
        <button
          onClick={handleReset}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs text-text-muted hover:text-text-primary hover:bg-surface transition-colors"
        >
          <RotateCcw size={14} />
          Reset
        </button>
        {!allCorrect && (
          <button
            onClick={() => {
              handleSubmit();
              const allOk = blanks.every(
                (b) =>
                  (answers[b.id] || "").trim().toLowerCase() ===
                  b.correctAnswer.trim().toLowerCase()
              );
              setAllCorrect(allOk);
            }}
            className="px-5 py-2 rounded-xl bg-primary text-white text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            Check Answer
          </button>
        )}
        {allCorrect && (
          <span className="text-sm font-bold text-emerald-400 flex items-center gap-1">
            <CheckCircle size={16} /> All correct!
          </span>
        )}
      </div>
    </div>
  );
}
