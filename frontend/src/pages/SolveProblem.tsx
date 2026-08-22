import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import ProblemDetail from "../components/ProblemDetail";
import LeetCodeEditorPanel from "../components/leetcode/LeetCodeEditorPanel";
import useReducedMotion from "../hooks/useReducedMotion";
import { ChevronDown, Clock, Code2, FileText, Pause, Play, RotateCcw } from "lucide-react";

const TIMER_PRESETS = [
  { label: "15 min", seconds: 900 },
  { label: "30 min", seconds: 1800 },
  { label: "45 min", seconds: 2700 },
  { label: "60 min", seconds: 3600 },
];

function formatTime(seconds: number) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, "0")}`;
}

export default function SolveProblem() {
  const { id } = useParams();
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const [problem, setProblem] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [mobileTab, setMobileTab] = useState<"problem" | "code">("problem");

  const [timerActive, setTimerActive] = useState(false);
  const [timerSeconds, setTimerSeconds] = useState(1800);
  const [timerInitial, setTimerInitial] = useState(1800);
  const [timerPaused, setTimerPaused] = useState(false);
  const [showTimerMenu, setShowTimerMenu] = useState(false);
  const timerRef = useRef<number | null>(null);
  const pausedRemainingRef = useRef<number | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const data = await api.getQuestionFull(id);
        setProblem(data);
      } catch {
        setProblem(null);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  useEffect(() => {
    return () => {
      if (timerRef.current) window.clearInterval(timerRef.current);
    };
  }, []);

  const startTimer = useCallback((seconds: number) => {
    setTimerSeconds(seconds);
    setTimerInitial(seconds);
    setTimerActive(true);
    setTimerPaused(false);
    setShowTimerMenu(false);
    pausedRemainingRef.current = null;

    if (timerRef.current) window.clearInterval(timerRef.current);
    timerRef.current = window.setInterval(() => {
      setTimerSeconds((prev) => {
        if (prev <= 1) {
          if (timerRef.current) window.clearInterval(timerRef.current);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  }, []);

  const togglePause = useCallback(() => {
    if (timerPaused) {
      const remaining = pausedRemainingRef.current ?? timerSeconds;
      setTimerSeconds(remaining);
      setTimerPaused(false);
      if (timerRef.current) window.clearInterval(timerRef.current);
      timerRef.current = window.setInterval(() => {
        setTimerSeconds((prev) => {
          if (prev <= 1) {
            if (timerRef.current) window.clearInterval(timerRef.current);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return;
    }

    pausedRemainingRef.current = timerSeconds;
    setTimerPaused(true);
    if (timerRef.current) window.clearInterval(timerRef.current);
  }, [timerPaused, timerSeconds]);

  const resetTimer = useCallback(() => {
    if (timerRef.current) window.clearInterval(timerRef.current);
    setTimerActive(false);
    setTimerSeconds(timerInitial);
    setTimerPaused(false);
    pausedRemainingRef.current = null;
  }, [timerInitial]);

  if (loading) {
    return (
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-brand-bg">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-brand-primary/20 border-t-brand-primary" />
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-brand-bg px-4">
        <div className="rounded-3xl border border-brand-primary/10 bg-white px-6 py-8 text-center shadow-soft-lg">
          <p className="text-sm font-semibold text-text-primary">Problem not found</p>
          <button
            onClick={() => navigate("/question-bank")}
            className="mt-3 rounded-full bg-brand-primary px-4 py-2 text-xs font-semibold text-white"
          >
            Back to Question Bank
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[calc(100vh-64px)] bg-[radial-gradient(circle_at_top,rgba(79,143,87,0.06),transparent_34%),linear-gradient(180deg,#FAFAF6_0%,#F4EFE4_100%)]">
      <div className="mx-auto flex min-h-[calc(100vh-64px)] max-w-[1600px] flex-col px-3 py-3 md:px-4 md:py-4">
        <div className="sticky top-0 z-20 mb-3 rounded-2xl border border-brand-primary/10 bg-white/90 px-3 py-2 shadow-soft backdrop-blur md:px-4">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex min-w-0 items-center gap-3">
              <button
                onClick={() => navigate("/question-bank")}
                className="rounded-full border border-brand-primary/10 bg-brand-bg px-3 py-1.5 text-xs font-semibold text-brand-muted transition-colors hover:text-text-primary"
              >
                Back
              </button>
              <div className="min-w-0">
                <div className="text-[10px] font-mono uppercase tracking-[0.24em] text-brand-muted">Problem</div>
                <h1 className="truncate text-sm font-semibold text-text-primary md:text-base">
                  {problem.title || problem.question_title || "Problem"}
                </h1>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              {!timerActive ? (
                <div className="relative">
                  <button
                    onClick={() => setShowTimerMenu((prev) => !prev)}
                    className="inline-flex items-center gap-2 rounded-full border border-brand-primary/10 bg-brand-bg px-3 py-2 text-xs font-semibold text-brand-muted transition-colors hover:text-text-primary"
                  >
                    <Clock size={14} />
                    Start timer
                    <ChevronDown size={12} />
                  </button>
                  <AnimatePresence>
                    {showTimerMenu && (
                      <>
                        <div className="fixed inset-0 z-30" onClick={() => setShowTimerMenu(false)} />
                        <motion.div
                          initial={{ opacity: 0, y: -4 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -4 }}
                          className="absolute right-0 top-full z-40 mt-2 min-w-[160px] rounded-2xl border border-brand-primary/10 bg-white p-1 shadow-soft-lg"
                        >
                          {TIMER_PRESETS.map((preset) => (
                            <button
                              key={preset.seconds}
                              onClick={() => startTimer(preset.seconds)}
                              className="block w-full rounded-xl px-3 py-2 text-left text-xs font-medium text-brand-muted transition-colors hover:bg-brand-bg hover:text-text-primary"
                            >
                              {preset.label}
                            </button>
                          ))}
                        </motion.div>
                      </>
                    )}
                  </AnimatePresence>
                </div>
              ) : (
                <div className="flex items-center gap-2 rounded-full border border-brand-primary/10 bg-brand-bg px-3 py-1.5 text-xs font-semibold">
                  <Clock size={14} className="text-brand-secondary" />
                  <span className="tabular-nums text-brand-secondary">{formatTime(timerSeconds)}</span>
                  <button onClick={togglePause} className="rounded-full bg-white p-1 text-brand-muted transition-colors hover:text-text-primary">
                    {timerPaused ? <Play size={12} /> : <Pause size={12} />}
                  </button>
                  <button onClick={resetTimer} className="rounded-full bg-white p-1 text-brand-muted transition-colors hover:text-text-primary">
                    <RotateCcw size={12} />
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="md:hidden mb-3 flex gap-2 rounded-2xl border border-brand-primary/10 bg-white/90 p-1 shadow-soft">
          <button
            onClick={() => setMobileTab("problem")}
            className={`flex flex-1 items-center justify-center gap-2 rounded-xl px-3 py-2 text-xs font-semibold transition-colors ${
              mobileTab === "problem" ? "bg-brand-primary text-white" : "text-brand-muted"
            }`}
          >
            <FileText size={13} />
            Problem
          </button>
          <button
            onClick={() => setMobileTab("code")}
            className={`flex flex-1 items-center justify-center gap-2 rounded-xl px-3 py-2 text-xs font-semibold transition-colors ${
              mobileTab === "code" ? "bg-brand-primary text-white" : "text-brand-muted"
            }`}
          >
            <Code2 size={13} />
            Code
          </button>
        </div>

        <div className="grid min-h-0 flex-1 gap-3 lg:grid-cols-[1.02fr_0.98fr]">
          <motion.div
            className={`${mobileTab === "code" ? "hidden md:block" : "block"} min-h-0 overflow-hidden rounded-3xl border border-brand-primary/10 bg-white shadow-soft-lg`}
            initial={reduced ? {} : { opacity: 0, x: -12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.25 }}
          >
            <ProblemDetail problemId={id} problem={problem} />
          </motion.div>

          <motion.div
            className={`${mobileTab === "problem" ? "hidden md:block" : "block"} min-h-0 overflow-hidden`}
            initial={reduced ? {} : { opacity: 0, x: 12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.25 }}
          >
            <LeetCodeEditorPanel problemId={id} problem={problem} onSolved={() => setMobileTab("code")} />
          </motion.div>
        </div>
      </div>
    </div>
  );
}
