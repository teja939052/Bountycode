import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import ProblemDetail from "../components/ProblemDetail";
import Compiler from "../pages/Compiler";
import useReducedMotion from "../hooks/useReducedMotion";
import { Clock, Pause, Play, RotateCcw, ChevronDown } from "lucide-react";

const TIMER_PRESETS = [
  { label: "15 min", seconds: 900 },
  { label: "30 min", seconds: 1800 },
  { label: "45 min", seconds: 2700 },
  { label: "60 min", seconds: 3600 },
];

export default function SolveProblem() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  const [timerActive, setTimerActive] = useState(false);
  const [timerSeconds, setTimerSeconds] = useState(1800);
  const [timerInitial, setTimerInitial] = useState(1800);
  const [timerPaused, setTimerPaused] = useState(false);
  const [showTimerMenu, setShowTimerMenu] = useState(false);
  const timerRef = useRef(null);
  const startTimeRef = useRef(null);
  const pausedRemainingRef = useRef(null);

  useEffect(() => {
    const load = async () => {
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
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const startTimer = useCallback((seconds) => {
    setTimerSeconds(seconds);
    setTimerInitial(seconds);
    setTimerActive(true);
    setTimerPaused(false);
    setShowTimerMenu(false);
    startTimeRef.current = Date.now();
    pausedRemainingRef.current = null;

    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setTimerSeconds((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  }, []);

  const togglePause = useCallback(() => {
    if (timerPaused) {
      const remaining = pausedRemainingRef.current || timerSeconds;
      setTimerSeconds(remaining);
      setTimerPaused(false);
      startTimeRef.current = Date.now() - (timerInitial - remaining) * 1000;
      timerRef.current = setInterval(() => {
        setTimerSeconds((prev) => {
          if (prev <= 1) {
            clearInterval(timerRef.current);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else {
      pausedRemainingRef.current = timerSeconds;
      setTimerPaused(true);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  }, [timerPaused, timerSeconds, timerInitial]);

  const resetTimer = useCallback(() => {
    if (timerRef.current) clearInterval(timerRef.current);
    setTimerActive(false);
    setTimerSeconds(timerInitial);
    setTimerPaused(false);
    startTimeRef.current = null;
    pausedRemainingRef.current = null;
  }, [timerInitial]);

  const formatTime = (s) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, "0")}`;
  };

  const pct = timerActive ? ((timerInitial - timerSeconds) / timerInitial) * 100 : 0;
  const isLow = timerSeconds <= 300 && timerActive;
  const isCritical = timerSeconds <= 60 && timerActive;

  if (loading) {
    return (
      <div className="h-[calc(100vh-64px)] flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="h-[calc(100vh-64px)] flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-400 mb-2">Problem not found</p>
          <a href="/question-bank" className="text-cyber-blue hover:underline text-sm">Back to Question Bank</a>
        </div>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col">
      {/* Timer Bar */}
      <div className="shrink-0 border-b border-space-border bg-space-panel/80 backdrop-blur-sm px-4 py-2">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate("/question-bank")}
              className="text-xs font-mono text-gray-500 hover:text-cyber-blue transition-colors"
            >
              ← Back
            </button>
            <span className="text-xs font-mono text-gray-600 truncate max-w-[200px]">
              {problem.title || problem.question_title || "Problem"}
            </span>
          </div>

          <div className="flex items-center gap-2">
            {!timerActive ? (
              <div className="relative">
                <button
                  onClick={() => setShowTimerMenu(!showTimerMenu)}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-space-border hover:border-cyber-blue/40 text-xs font-mono text-gray-400 hover:text-cyber-blue transition-all"
                >
                  <Clock size={14} />
                  <span>Start Timer</span>
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
                        className="absolute right-0 top-full mt-1 z-40 bg-gray-900 border border-gray-700 rounded-lg shadow-xl py-1 min-w-[140px]"
                      >
                        {TIMER_PRESETS.map((p) => (
                          <button
                            key={p.seconds}
                            onClick={() => startTimer(p.seconds)}
                            className="w-full px-3 py-2 text-xs font-mono text-gray-300 hover:bg-gray-800 hover:text-cyber-blue text-left transition-colors"
                          >
                            {p.label}
                          </button>
                        ))}
                      </motion.div>
                    </>
                  )}
                </AnimatePresence>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                {/* Timer display */}
                <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border font-mono text-sm font-bold transition-all ${
                  isCritical
                    ? "border-red-500/50 bg-red-500/10 text-red-400 animate-pulse"
                    : isLow
                    ? "border-yellow-500/50 bg-yellow-500/10 text-yellow-400"
                    : "border-cyber-blue/30 bg-cyber-blue/10 text-cyber-blue"
                }`}>
                  <Clock size={14} className={isCritical ? "animate-spin" : ""} />
                  <span className="tabular-nums">{formatTime(timerSeconds)}</span>
                </div>

                {/* Progress ring */}
                <svg className="w-8 h-8 -rotate-90" viewBox="0 0 36 36">
                  <circle cx="18" cy="18" r="15" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-700" />
                  <circle
                    cx="18" cy="18" r="15" fill="none"
                    stroke={isCritical ? "#ef4444" : isLow ? "#eab308" : "#4CC9F0"}
                    strokeWidth="2"
                    strokeDasharray={`${pct * 0.942} 100`}
                    strokeLinecap="round"
                    className="transition-all duration-1000"
                  />
                </svg>

                <button
                  onClick={togglePause}
                  className="p-1.5 rounded-lg border border-space-border hover:border-gray-500 text-gray-400 hover:text-text-primary transition-all"
                >
                  {timerPaused ? <Play size={14} /> : <Pause size={14} />}
                </button>
                <button
                  onClick={resetTimer}
                  className="p-1.5 rounded-lg border border-space-border hover:border-gray-500 text-gray-400 hover:text-text-primary transition-all"
                >
                  <RotateCcw size={14} />
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-col md:flex-row flex-1 overflow-hidden">
        {/* Left Panel: Problem Description */}
        <motion.div
          className="w-full md:w-1/2 overflow-y-auto border-b md:border-b-0 md:border-r border-space-border"
          initial={reduced ? {} : { opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <ProblemDetail problemId={id} problem={problem} />
        </motion.div>

        {/* Right Panel: Compiler */}
        <motion.div
          className="w-full md:w-1/2 flex flex-col"
          initial={reduced ? {} : { opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <Compiler problemId={id} problem={problem} />
        </motion.div>
      </div>
    </div>
  );
}
