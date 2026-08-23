import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Play, Pause, SkipForward, SkipBack, BarChart3, Code, CheckCircle, AlertCircle } from "lucide-react";
import { interviewReplayApi } from "../services/api/interviewReplay.ts";
import useAuthStore from "../store/authStore";

export default function InterviewReplay({ interviewId }: any = {}) {
  const user = useAuthStore((s) => s.user);
  const [replay, setReplay] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentStep, setCurrentStep] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [error, setError] = useState("");
  const [showStats, setShowStats] = useState(false);
  const playInterval = useRef(null);
  const editorRef = useRef(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [r, s] = await Promise.all([
          interviewReplayApi.getReplay(interviewId),
          interviewReplayApi.getStats(interviewId),
        ]);
        setReplay(r);
        setStats(s);
      } catch (e) {
        setError(e.message || "Could not load replay");
      } finally {
        setLoading(false);
      }
    };
    if (interviewId) load();
  }, [interviewId]);

  useEffect(() => {
    return () => {
      if (playInterval.current) clearInterval(playInterval.current);
    };
  }, []);

  const handlePlay = () => {
    if (!replay?.trace?.length) return;
    setPlaying(true);
    playInterval.current = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev >= replay.trace.length - 1) {
          clearInterval(playInterval.current);
          setPlaying(false);
          return prev;
        }
        return prev + 1;
      });
    }, 2000);
  };

  const handlePause = () => {
    setPlaying(false);
    if (playInterval.current) clearInterval(playInterval.current);
  };

  const handleStep = (dir) => {
    if (!replay?.trace) return;
    setCurrentStep((prev) => {
      if (dir === "next") return Math.min(prev + 1, replay.trace.length - 1);
      return Math.max(prev - 1, 0);
    });
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-300">
        Loading replay data...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-xl">
        {error}
      </div>
    );
  }

  const currentCode = replay?.trace?.[currentStep]?.code || replay?.final_code || "";
  const problem = replay?.problem || {};

  return (
    <div className="font-mono text-sm">
      {/* Problem header */}
      {problem.title && (
        <div className="mb-4 rounded-xl bg-slate-900/40 border border-slate-800 p-4">
          <h3 className="font-bold text-slate-200">{problem.title}</h3>
          <p className="text-sm text-slate-400 mt-1">{problem.description}</p>
        </div>
      )}

      {/* Controls */}
      <div className="mb-4 flex items-center justify-between rounded-xl bg-slate-900/40 border border-slate-800 px-4 py-3">
        <div className="flex items-center gap-3">
          {!playing ? (
            <button
              onClick={handlePlay}
              disabled={!replay?.trace?.length}
              className="rounded-lg bg-indigo-600 px-3 py-1 text-sm font-medium text-text-primary hover:bg-indigo-500 disabled:opacity-50"
            >
              <Play className="h-4 w-4 inline mr-1" />
              Play
            </button>
          ) : (
            <button
              onClick={handlePause}
              className="rounded-lg bg-slate-700 px-3 py-1 text-sm font-medium text-slate-200 hover:bg-slate-600"
            >
              <Pause className="h-4 w-4 inline mr-1" />
              Pause
            </button>
          )}
          <button
            onClick={() => handleStep("prev")}
            disabled={currentStep === 0}
            className="rounded-lg border border-slate-700 px-2 py-1 text-slate-300 hover:bg-slate-800 disabled:opacity-50"
          >
            <SkipBack className="h-4 w-4" />
          </button>
          <button
            onClick={() => handleStep("next")}
            disabled={!replay?.trace || currentStep >= replay.trace.length - 1}
            className="rounded-lg border border-slate-700 px-2 py-1 text-slate-300 hover:bg-slate-800 disabled:opacity-50"
          >
            <SkipForward className="h-4 w-4" />
          </button>
          <span className="text-xs text-slate-500">
            Step {currentStep + 1}/{replay?.trace?.length || 1}
          </span>
        </div>

        <button
          onClick={() => setShowStats(true)}
          className="rounded-lg border border-slate-700 px-3 py-1 text-sm text-slate-300 hover:bg-slate-800"
        >
          <BarChart3 className="h-4 w-4 inline mr-1" />
          View Stats
        </button>
      </div>

      {/* Code viewer */}
      <div className="mb-4">
        <pre className="overflow-x-auto rounded-xl bg-slate-900/60 border border-slate-800 p-4 text-sm leading-relaxed whitespace-pre-wrap">
          <code className="text-slate-300">{currentCode}</code>
        </pre>
      </div>

      {/* Run result of current step */}
      {replay?.trace?.[currentStep]?.run_result && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className={`mb-4 rounded-xl border p-3 text-sm ${
            replay.trace[currentStep].run_result.status === "passed"
              ? "border-green-500/30 bg-green-500/10 text-green-300"
              : "border-rose-500/30 bg-rose-500/10 text-rose-300"
          }`}
        >
          <div className="flex items-center gap-2">
            {replay.trace[currentStep].run_result.status === "passed" ? (
              <CheckCircle className="h-4 w-4 text-green-400" />
            ) : (
              <AlertCircle className="h-4 w-4 text-rose-400" />
            )}
            Result: {replay.trace[currentStep].run_result.status}
          </div>
          {replay.trace[currentStep].run_result.error && (
            <pre className="mt-2 text-xs text-rose-400 whitespace-pre-wrap">
              {replay.trace[currentStep].run_result.error.slice(0, 200)}
            </pre>
          )}
        </motion.div>
      )}

      {/* Stats modal */}
      <AnimatePresence>
        {showStats && stats && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-surface-2 backdrop-blur-sm"
            onClick={() => setShowStats(false)}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-800 p-6"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-xl font-bold text-slate-200 mb-4">Coding Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-slate-400">Submissions</span>
                  <span className="font-bold text-text-primary">{stats.total_submissions}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Compile Errors</span>
                  <span className="font-bold text-amber-400">{stats.compile_errors}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Estimated WPM</span>
                  <span className="font-bold text-indigo-300">{stats.estimated_wpm}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Code Length</span>
                  <span className="font-bold text-slate-300">{stats.code_length} chars</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Accepted</span>
                  <span className={stats.accepted ? "font-bold text-green-400" : "font-bold text-rose-400"}>
                    {stats.accepted ? "Yes" : "No"}
                  </span>
                </div>
              </div>
              <button
                onClick={() => setShowStats(false)}
                className="mt-6 w-full rounded-lg bg-indigo-600 py-2 font-semibold text-text-primary hover:bg-indigo-500"
              >
                Close
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
