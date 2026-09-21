import { useState, useEffect, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Play, Pause, SkipBack, SkipForward, RotateCcw,
  ChevronRight, Lightbulb, Eye
} from "lucide-react";

interface TraceStep {
  step: number;
  description: string;
  array: number[];
  pointers: Record<string, number>;
  highlight: number[];
  window?: { start: number; end: number };
  variables: Record<string, string | number>;
  codeLine?: number;
}

interface AlgorithmTracerProps {
  steps: TraceStep[];
  title?: string;
  interactive?: boolean;
  questionMode?: boolean;
  questionStep?: number;
  questionText?: string;
  correctAnswer?: string | number;
  onComplete?: (correct: boolean) => void;
  speed?: number;
}

export default function AlgorithmTracer({
  steps,
  title = "Algorithm Trace",
  interactive = true,
  questionMode = false,
  questionStep = 3,
  questionText = "",
  correctAnswer,
  onComplete,
  speed = 1.0,
}: AlgorithmTracerProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed_, setSpeed] = useState(speed);
  const [showAnswer, setShowAnswer] = useState(false);
  const [userAnswer, setUserAnswer] = useState("");
  const [answered, setAnswered] = useState(false);
  const [pausedForQuestion, setPausedForQuestion] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const step = steps[currentStep];
  const totalSteps = steps.length;
  const progress = totalSteps > 0 ? ((currentStep + 1) / totalSteps) * 100 : 0;

  const nextStep = useCallback(() => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep((s) => s + 1);
    } else {
      setIsPlaying(false);
    }
  }, [currentStep, totalSteps]);

  const prevStep = useCallback(() => {
    if (currentStep > 0) setCurrentStep((s) => s - 1);
  }, [currentStep]);

  const reset = useCallback(() => {
    setCurrentStep(0);
    setIsPlaying(false);
    setPausedForQuestion(false);
    setAnswered(false);
    setShowAnswer(false);
    setUserAnswer("");
  }, []);

  // Auto-play
  useEffect(() => {
    if (isPlaying && !pausedForQuestion) {
      timerRef.current = setTimeout(nextStep, 1200 / speed_);
    }
    return () => { if (timerRef.current) clearTimeout(timerRef.current); };
  }, [isPlaying, currentStep, speed_, pausedForQuestion, nextStep]);

  // Pause at question step
  useEffect(() => {
    if (questionMode && currentStep === questionStep && !answered) {
      setIsPlaying(false);
      setPausedForQuestion(true);
    }
  }, [currentStep, questionMode, questionStep, answered]);

  const handleAnswer = () => {
    if (!userAnswer.trim()) return;
    setAnswered(true);
    setPausedForQuestion(false);
    const correct = userAnswer.trim().toLowerCase() === String(correctAnswer).toLowerCase();
    onComplete?.(correct);
    if (isPlaying) {
      // Resume playing after answer
    }
  };

  const maxVal = step ? Math.max(...step.array.map((v) => Math.abs(v)), 1) : 1;

  return (
    <div className="rounded-2xl border border-border bg-surface overflow-hidden shadow-card">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-surface-elevated">
        <div className="flex items-center gap-2">
          <Eye size={18} className="text-primary" />
          <span className="font-bold text-sm text-text-primary">{title}</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSpeed((s) => (s === 0.5 ? 1 : s === 1 ? 2 : 0.5))}
            className="px-2 py-1 rounded-lg text-xs font-mono bg-surface text-text-muted hover:bg-surface-elevated transition-colors"
          >
            {speed_}x
          </button>
          <span className="text-xs text-text-muted font-mono">
            {currentStep + 1}/{totalSteps}
          </span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="h-1 bg-surface-elevated">
        <motion.div
          className="h-full bg-primary"
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>

      {/* Visualization */}
      <div className="p-6 min-h-[200px] flex flex-col items-center justify-center">
        {step && (
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="w-full"
            >
              {/* Array visualization */}
              <div className="flex items-end justify-center gap-2 mb-6">
                {step.array.map((val, idx) => {
                  const isActive = step.highlight.includes(idx);
                  const pointerEntry = Object.entries(step.pointers).find(
                    ([, v]) => v === idx
                  );
                  const inWindow =
                    step.window &&
                    idx >= step.window.start &&
                    idx <= step.window.end;
                  const height = Math.max(36, (Math.abs(val) / maxVal) * 80);

                  return (
                    <div key={idx} className="flex flex-col items-center gap-1">
                      {pointerEntry && (
                        <span
                          className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                            pointerEntry[0] === "left"
                              ? "bg-emerald-500/30 text-emerald-300 border border-emerald-500/40"
                              : pointerEntry[0] === "right"
                              ? "bg-rose-500/30 text-rose-300 border border-rose-500/40"
                              : "bg-indigo-500/30 text-indigo-300 border border-indigo-500/40"
                          }`}
                        >
                          {pointerEntry[0]}
                        </span>
                      )}
                      <motion.div
                        layout
                        animate={{ scale: isActive ? 1.1 : 1 }}
                        className={`w-11 rounded-lg border flex items-center justify-center font-mono font-bold text-xs shadow-lg transition-colors ${
                          isActive
                            ? "bg-amber-500/25 border-amber-400 text-amber-200"
                            : inWindow
                            ? "bg-primary/10 border-primary/30 text-primary"
                            : "bg-slate-900 border-slate-700 text-slate-200"
                        }`}
                        style={{ height: `${height}px` }}
                      >
                        {val}
                      </motion.div>
                      <span className="text-[10px] text-text-muted font-mono">
                        [{idx}]
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* Variables display */}
              <div className="flex flex-wrap justify-center gap-3 mb-4">
                {Object.entries(step.variables).map(([key, val]) => (
                  <div
                    key={key}
                    className="px-3 py-1.5 rounded-lg bg-surface-elevated border border-border font-mono text-xs"
                  >
                    <span className="text-text-muted">{key} = </span>
                    <span className="text-primary font-bold">{String(val)}</span>
                  </div>
                ))}
              </div>

              {/* Description */}
              <p className="text-center text-sm text-text-secondary mt-2">
                {step.description}
              </p>
            </motion.div>
          </AnimatePresence>
        )}

        {/* Question overlay */}
        {questionMode && pausedForQuestion && !answered && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mt-4 p-4 rounded-xl bg-primary/5 border border-primary/20 w-full max-w-md"
          >
            <div className="flex items-center gap-2 mb-2">
              <Lightbulb size={16} className="text-amber-400" />
              <span className="text-sm font-bold text-text-primary">
                Trace Question
              </span>
            </div>
            <p className="text-sm text-text-secondary mb-3">{questionText}</p>
            <div className="flex gap-2">
              <input
                type="text"
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleAnswer()}
                placeholder="Your answer..."
                className="flex-1 px-3 py-2 rounded-lg bg-surface border border-border text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-primary"
                autoFocus
              />
              <button
                onClick={handleAnswer}
                className="px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                Check
              </button>
            </div>
          </motion.div>
        )}

        {/* Answer reveal */}
        {answered && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-3 text-center"
          >
            <span
              className={`text-sm font-medium ${
                String(userAnswer).toLowerCase() === String(correctAnswer).toLowerCase()
                  ? "text-emerald-400"
                  : "text-rose-400"
              }`}
            >
              {String(userAnswer).toLowerCase() === String(correctAnswer).toLowerCase()
                ? "Correct!"
                : `Answer: ${correctAnswer}`}
            </span>
          </motion.div>
        )}
      </div>

      {/* Controls */}
      {interactive && (
        <div className="flex items-center justify-center gap-2 px-4 py-3 border-t border-border bg-surface-elevated">
          <button
            onClick={reset}
            className="p-2 rounded-lg text-text-muted hover:text-text-primary hover:bg-surface transition-colors"
            title="Reset"
          >
            <RotateCcw size={16} />
          </button>
          <button
            onClick={prevStep}
            disabled={currentStep === 0}
            className="p-2 rounded-lg text-text-muted hover:text-text-primary hover:bg-surface transition-colors disabled:opacity-30"
          >
            <SkipBack size={16} />
          </button>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="p-3 rounded-full bg-primary text-white hover:bg-primary/90 transition-colors shadow-lg"
          >
            {isPlaying ? <Pause size={18} /> : <Play size={18} />}
          </button>
          <button
            onClick={nextStep}
            disabled={currentStep === totalSteps - 1}
            className="p-2 rounded-lg text-text-muted hover:text-text-primary hover:bg-surface transition-colors disabled:opacity-30"
          >
            <SkipForward size={16} />
          </button>
          <button
            onClick={() => setShowAnswer(!showAnswer)}
            className="p-2 rounded-lg text-text-muted hover:text-text-primary hover:bg-surface transition-colors"
            title="Show step details"
          >
            <ChevronRight
              size={16}
              className={`transition-transform ${showAnswer ? "rotate-90" : ""}`}
            />
          </button>
        </div>
      )}

      {/* Step details */}
      <AnimatePresence>
        {showAnswer && step && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden border-t border-border"
          >
            <div className="p-4 text-xs font-mono text-text-secondary space-y-1">
              <p>
                <span className="text-text-muted">Step:</span> {step.step}
              </p>
              <p>
                <span className="text-text-muted">Array:</span> [{step.array.join(", ")}]
              </p>
              <p>
                <span className="text-text-muted">Pointers:</span>{" "}
                {Object.entries(step.pointers)
                  .map(([k, v]) => `${k}=${v}`)
                  .join(", ")}
              </p>
              {step.window && (
                <p>
                  <span className="text-text-muted">Window:</span> [
                  {step.window.start}, {step.window.end}]
                </p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
