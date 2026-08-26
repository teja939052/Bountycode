import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import Editor from "@monaco-editor/react";
import {
  Play, Code, BookOpen, ArrowRight, CheckCircle2, Star, Sparkles,
  Trophy, Loader2, Terminal, Rocket, Zap,
} from "lucide-react";
import api from "../services/api";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";

const STORAGE_KEY = "bountycode_free_trial";
const LANGUAGE = "c";

const COMPILER_MAP = {
  c: "c",
  cpp: "cpp",
  java: "java",
  python: "python",
};

function loadProgress() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : { completedLessons: [], currentLesson: 0, finished: false };
  } catch {
    return { completedLessons: [], currentLesson: 0, finished: false };
  }
}

function saveProgress(progress) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

export default function FreeTrial() {
  const navigate = useNavigate();
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(() => loadProgress());
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);
  const [runError, setRunError] = useState("");
  const [celebrating, setCelebrating] = useState(false);
  const [showConversion, setShowConversion] = useState(false);
  const [conversionData, setConversionData] = useState(null);
  const [tracking, setTracking] = useState(false);

  useEffect(() => {
    async function fetchLessons() {
      try {
        const data = await api.freeTrial.getLessons();
        setLessons(data.lessons || []);
        if (data.lessons?.length > 0 && !progress.finished) {
          const starter = data.lessons[progress.currentLesson]?.content?.exercise?.starter_code;
          if (starter && !code) setCode(starter);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchLessons();
  }, []);

  useEffect(() => {
    if (progress.finished) {
      setShowConversion(true);
      api.freeTrial.getConversionPrompt().then(setConversionData).catch(() => {});
    }
  }, [progress.finished]);

  const currentLesson = lessons[progress.currentLesson];
  const isLastLesson = progress.currentLesson >= lessons.length - 1;

  const trackConversion = useCallback(async (signal) => {
    if (tracking) return;
    setTracking(true);
    try {
      await api.freeTrial.trackTrial({
        completedCount: progress.completedLessons.length,
        totalCount: lessons.length,
        conversionSignal: signal,
      });
    } catch {
      // Silently fail — tracking is non-critical
    } finally {
      setTracking(false);
    }
  }, [progress.completedLessons.length, lessons.length, tracking]);

  const handleMarkComplete = useCallback(async () => {
    const newCompleted = [...progress.completedLessons, currentLesson.id];
    setCelebrating(true);
    setTimeout(() => {
      setCelebrating(false);
      if (isLastLesson) {
        const newProgress = { ...progress, completedLessons: newCompleted, finished: true };
        setProgress(newProgress);
        saveProgress(newProgress);
        api.freeTrial.complete().catch(() => {});
        trackConversion(true);
      } else {
        const nextLesson = progress.currentLesson + 1;
        const newProgress = { ...progress, completedLessons: newCompleted, currentLesson: nextLesson };
        setProgress(newProgress);
        saveProgress(newProgress);
        const next = lessons[nextLesson];
        if (next?.content?.exercise?.starter_code) {
          setCode(next.content.exercise.starter_code);
        } else {
          setCode("");
        }
        setOutput("");
        setRunError("");
      }
    }, 1200);
  }, [progress, currentLesson, isLastLesson, lessons, trackConversion]);

  const handleRunCode = useCallback(async () => {
    setRunning(true);
    setOutput("");
    setRunError("");
    try {
      const res = await fetch("/api/v1/compiler/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language: LANGUAGE, stdin: "", timeout: 10 }),
        credentials: "include",
      });
      const result = await res.json();
      if (result.success) {
        setOutput(result.stdout || "(no output)");
      } else {
        setRunError(result.stderr || result.error || "Execution failed");
      }
    } catch (err) {
      setRunError(err.message || "Failed to execute");
    } finally {
      setRunning(false);
    }
  }, [code]);

  const handleResetCode = useCallback(() => {
    const starter = currentLesson?.content?.exercise?.starter_code || "";
    setCode(starter);
    setOutput("");
    setRunError("");
  }, [currentLesson]);

  const handleLessonSelect = useCallback((index) => {
    if (progress.completedLessons.includes(lessons[index]?.id) || index === progress.currentLesson) {
      const newProgress = { ...progress, currentLesson: index };
      setProgress(newProgress);
      saveProgress(newProgress);
      const lesson = lessons[index];
      if (lesson?.content?.exercise?.starter_code) {
        setCode(lesson.content.exercise.starter_code);
      }
      setOutput("");
      setRunError("");
    }
  }, [progress, lessons]);

  const handleResetTrial = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setProgress({ completedLessons: [], currentLesson: 0, finished: false });
    setShowConversion(false);
    setConversionData(null);
    setCode(lessons[0]?.content?.exercise?.starter_code || "");
    setOutput("");
    setRunError("");
  }, [lessons]);

  if (loading) {
    return (
      <div className="relative min-h-screen flex items-center justify-center">
        <ArcadeBackdrop variant="arcade" />
        <div className="relative z-10 flex flex-col items-center gap-4">
          <Loader2 size={40} className="animate-spin text-cyan-400" />
          <p className="text-gray-400 font-mono text-sm">Loading lessons...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="relative min-h-screen flex items-center justify-center">
        <ArcadeBackdrop variant="arcade" />
        <div className="relative z-10 glass rounded-2xl p-8 max-w-md text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <button onClick={() => window.location.reload()} className="btn-primary px-6 py-3">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!currentLesson && !showConversion) {
    return (
      <div className="relative min-h-screen flex items-center justify-center">
        <ArcadeBackdrop variant="arcade" />
        <div className="relative z-10 text-center">
          <p className="text-gray-400 mb-4">No lessons available.</p>
          <button onClick={() => navigate("/register")} className="btn-primary px-6 py-3">
            Sign Up
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen">
      <ArcadeBackdrop variant="arcade" />

      <div className="relative z-10 max-w-6xl mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <div>
            <h1 className="text-2xl font-black text-text-primary flex items-center gap-2">
              <Rocket className="text-cyan-400" size={24} />
              Free Trial
            </h1>
            <p className="text-sm text-gray-400 mt-1">Start coding in seconds — no signup needed</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="glass rounded-xl px-4 py-2 text-sm font-mono text-gray-300">
              {progress.completedLessons.length}/{lessons.length} complete
            </div>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-[280px_1fr] gap-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass rounded-2xl p-4 h-fit"
          >
            <h2 className="text-xs font-mono uppercase tracking-wider text-gray-500 mb-4">Lessons</h2>
            <div className="space-y-2">
              {lessons.map((lesson, idx) => {
                const isCompleted = progress.completedLessons.includes(lesson.id);
                const isActive = idx === progress.currentLesson;
                const isLocked = !isCompleted && idx > progress.currentLesson;
                return (
                  <button
                    key={lesson.id}
                    onClick={() => handleLessonSelect(idx)}
                    disabled={isLocked}
                    className={`w-full text-left rounded-xl p-3 transition-all ${
                      isActive
                        ? "bg-cyan-500/20 border border-cyan-500/30"
                        : isCompleted
                        ? "bg-emerald-500/10 border border-emerald-500/20"
                        : "bg-white border-border shadow-card border border-white/5 opacity-50 cursor-not-allowed"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      {isCompleted ? (
                        <CheckCircle2 size={16} className="text-emerald-400 shrink-0" />
                      ) : isActive ? (
                        <Code size={16} className="text-cyan-400 shrink-0" />
                      ) : (
                        <BookOpen size={16} className="text-gray-600 shrink-0" />
                      )}
                      <div className="min-w-0">
                        <p className={`text-sm font-medium truncate ${isActive ? "text-text-primary" : isCompleted ? "text-emerald-300" : "text-gray-500"}`}>
                          {lesson.title}
                        </p>
                        <p className="text-[10px] font-mono text-gray-600 mt-0.5">{lesson.xp} XP</p>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </motion.div>

          <AnimatePresence mode="wait">
            <motion.div
              key={currentLesson?.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="min-h-0"
            >
              <div className="glass rounded-2xl overflow-hidden">
                <div className="flex items-center justify-between px-6 py-4 border-b border-white/5">
                  <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-cyan-500/20 text-cyan-400">
                      <BookOpen size={16} />
                    </div>
                    <div>
                      <h2 className="text-lg font-bold text-text-primary">{currentLesson?.title}</h2>
                      <p className="text-xs font-mono text-gray-500">
                        Lesson {progress.currentLesson + 1} of {lessons.length}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-gray-500 bg-white border-border shadow-card px-3 py-1 rounded-lg">
                      +{currentLesson?.xp} XP
                    </span>
                  </div>
                </div>

                <div className="p-6 space-y-6">
                  {currentLesson?.content?.theory && (
                    <div>
                      <h3 className="text-sm font-mono uppercase tracking-wider text-cyan-400 mb-3 flex items-center gap-2">
                        <BookOpen size={14} /> Theory
                      </h3>
                      <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-line">
                        {currentLesson.content.theory}
                      </p>
                    </div>
                  )}

                  {currentLesson?.content?.analogy && (
                    <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4">
                      <p className="text-xs font-mono text-indigo-400 mb-1">Analogy</p>
                      <p className="text-sm text-gray-300 italic">{currentLesson.content.analogy}</p>
                    </div>
                  )}

                  {currentLesson?.content?.sections?.map((section, idx) => (
                    <div key={idx}>
                      <h3 className="text-sm font-mono uppercase tracking-wider text-gray-400 mb-2">{section.heading}</h3>
                      <p className="text-sm text-gray-300 leading-relaxed">{section.body}</p>
                      {section.pro_tip && (
                        <div className="mt-2 bg-amber-500/10 border border-amber-500/20 rounded-lg p-3">
                          <p className="text-xs font-mono text-amber-400 mb-1">Pro Tip</p>
                          <p className="text-sm text-gray-300">{section.pro_tip}</p>
                        </div>
                      )}
                      {section.code && (
                        <div className="mt-3 bg-[#0d1117] rounded-xl overflow-hidden border border-white/5">
                          <div className="flex items-center justify-between px-4 py-2 border-b border-white/5">
                            <span className="text-xs font-mono text-gray-500">Example</span>
                            <Code size={12} className="text-gray-500" />
                          </div>
                          <pre className="p-4 text-sm font-mono text-gray-300 overflow-x-auto"><code>{section.code}</code></pre>
                        </div>
                      )}
                    </div>
                  ))}

                  {currentLesson?.content?.code_example && (
                    <div>
                      <h3 className="text-sm font-mono uppercase tracking-wider text-cyan-400 mb-3 flex items-center gap-2">
                        <Code size={14} /> Annotated Example
                      </h3>
                      <div className="bg-[#0d1117] rounded-xl overflow-hidden border border-white/5">
                        <div className="flex items-center justify-between px-4 py-2 border-b border-white/5">
                          <span className="text-xs font-mono text-gray-500">{LANGUAGE}</span>
                        </div>
                        <div className="flex">
                          <pre className="p-4 text-sm font-mono leading-relaxed overflow-x-auto flex-1" style={{ background: "#fafafa" }}>
                            <code className="text-gray-800">
                              {(currentLesson.content.code_example.code || "").split("\n").map((line, i) => {
                                const annot = currentLesson.content.code_example.annotations?.find(a => a.line === i + 1);
                                return (
                                  <div key={i} className="flex items-start gap-3 min-h-[1.4em]">
                                    <span className="text-gray-400 text-xs select-none w-6 text-right shrink-0 leading-[1.4em]">{i + 1}</span>
                                    <span className="whitespace-pre-wrap leading-[1.4em]">{line || " "}</span>
                                    {annot && (
                                      <span className="text-xs text-cyan-600 ml-2 shrink-0 leading-[1.4em] opacity-0 group-hover:opacity-100 transition-opacity">
                                        ← {annot.text}
                                      </span>
                                    )}
                                  </div>
                                );
                              })}
                            </code>
                          </pre>
                          {currentLesson.content.code_example.annotations?.length > 0 && (
                            <div className="hidden md:block w-56 shrink-0 border-l border-white/5 p-4 bg-[#0d1117]">
                              <p className="text-xs font-mono text-gray-500 mb-3 uppercase tracking-wider">Annotations</p>
                              <div className="space-y-3">
                                {currentLesson.content.code_example.annotations.map((a, i) => (
                                  <div key={i} className="flex gap-2 text-xs">
                                    <span className="text-cyan-500 font-mono shrink-0 w-5">L{a.line}</span>
                                    <span className="text-gray-400">{a.text}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  {currentLesson?.content?.exercise && (
                    <div>
                      <h3 className="text-sm font-mono uppercase tracking-wider text-emerald-400 mb-3 flex items-center gap-2">
                        <Terminal size={14} /> Your Turn — Code It
                      </h3>
                      <p className="text-sm text-gray-300 mb-4">{currentLesson.content.exercise.description}</p>

                      <div className="rounded-xl overflow-hidden border border-white/5 mb-4">
                        <div className="flex items-center justify-between px-4 py-2 bg-[#0d1117] border-b border-white/5">
                          <span className="text-xs font-mono text-gray-500">main.c</span>
                          <button
                            onClick={handleResetCode}
                            className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
                          >
                            Reset
                          </button>
                        </div>
                        <Editor
                          height="240px"
                          language={LANGUAGE}
                          theme="vs-dark"
                          value={code}
                          onChange={(val) => setCode(val || "")}
                          options={{
                            minimap: { enabled: false },
                            fontSize: 14,
                            lineNumbers: "on",
                            scrollBeyondLastLine: false,
                            automaticLayout: true,
                            padding: { top: 12 },
                          }}
                        />
                      </div>

                      <div className="flex items-center gap-3 mb-4">
                        <button
                          onClick={handleRunCode}
                          disabled={running}
                          className="inline-flex items-center gap-2 bg-emerald-500 hover:bg-emerald-400 text-gray-900 font-bold px-6 py-3 rounded-xl transition-all disabled:opacity-50"
                        >
                          {running ? (
                            <Loader2 size={16} className="animate-spin" />
                          ) : (
                            <Play size={16} />
                          )}
                          {running ? "Running..." : "Run Code"}
                        </button>
                        {currentLesson.content.exercise.hints?.length > 0 && (
                          <div className="text-xs text-gray-500">
                            <span className="font-mono text-amber-400">Hint: </span>
                            {currentLesson.content.exercise.hints[0]}
                          </div>
                        )}
                      </div>

                      {runError && (
                        <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 mb-4">
                          <p className="text-xs font-mono text-red-400 mb-1">Error</p>
                          <pre className="text-sm text-red-300 font-mono whitespace-pre-wrap">{runError}</pre>
                        </div>
                      )}

                      {output && (
                        <div className="bg-[#0d1117] border border-white/5 rounded-xl overflow-hidden mb-4">
                          <div className="flex items-center justify-between px-4 py-2 border-b border-white/5">
                            <span className="text-xs font-mono text-gray-500">Output</span>
                            <Terminal size={12} className="text-gray-500" />
                          </div>
                          <pre className="p-4 text-sm font-mono text-gray-300 whitespace-pre-wrap">{output}</pre>
                        </div>
                      )}
                    </div>
                  )}

                  {currentLesson?.content?.common_mistakes?.length > 0 && (
                    <div>
                      <h3 className="text-xs font-mono uppercase tracking-wider text-red-400 mb-3">Common Mistakes</h3>
                      <div className="space-y-3">
                        {currentLesson.content.common_mistakes.map((m, idx) => (
                          <div key={idx} className="bg-red-500/5 border border-red-500/10 rounded-xl p-4">
                            <p className="text-sm text-gray-300 mb-2"><span className="text-red-400">✗</span> {m.mistake}</p>
                            <p className="text-sm text-emerald-400"><span className="text-emerald-400">✓</span> {m.fix}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {currentLesson?.content?.key_takeaways?.length > 0 && (
                    <div className="bg-cyan-500/5 border border-cyan-500/10 rounded-xl p-5">
                      <h3 className="text-sm font-mono uppercase tracking-wider text-cyan-400 mb-3 flex items-center gap-2">
                        <Star size={14} /> Key Takeaways
                      </h3>
                      <ul className="space-y-2">
                        {currentLesson.content.key_takeaways.map((takeaway, idx) => (
                          <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                            <CheckCircle2 size={14} className="text-emerald-400 shrink-0 mt-0.5" />
                            {takeaway}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <div className="px-6 py-4 border-t border-white/5 flex items-center justify-between">
                  <span className="text-xs text-gray-500">
                    {progress.completedLessons.includes(currentLesson?.id) ? "✓ Completed" : "Complete to continue"}
                  </span>
                  {!progress.completedLessons.includes(currentLesson?.id) && (
                    <button
                      onClick={handleMarkComplete}
                      className="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-text-primary font-semibold px-6 py-3 rounded-xl hover:from-cyan-400 hover:to-blue-400 transition-all"
                    >
                      <CheckCircle2 size={16} />
                      Mark Complete
                      {!isLastLesson && <ArrowRight size={16} />}
                    </button>
                  )}
                </div>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      <AnimatePresence>
        {celebrating && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className="fixed inset-0 z-50 flex items-center justify-center pointer-events-none"
          >
            <div className="bg-gradient-to-br from-emerald-400/20 to-cyan-400/20 rounded-3xl p-10 text-center border border-white/10">
              <motion.div
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 0.6 }}
              >
                <Trophy size={64} className="text-yellow-400 mx-auto mb-4" />
              </motion.div>
              <p className="text-2xl font-bold text-text-primary mb-2">Lesson Complete!</p>
              <p className="text-sm text-gray-300">+{currentLesson?.xp} XP earned</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {showConversion && conversionData && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-surface-2 backdrop-blur-sm"
          >
            <motion.div
              initial={{ opacity: 0, y: 40, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 40, scale: 0.95 }}
              className="glass rounded-3xl p-8 max-w-lg w-full border border-white/10 max-h-[90vh] overflow-y-auto"
            >
              <div className="text-center mb-2">
                <motion.div
                  animate={{ rotate: [0, 5, -5, 0] }}
                  transition={{ duration: 1, repeat: Infinity }}
                  className="inline-flex"
                >
                  <Sparkles size={48} className="text-yellow-400 mb-4" />
                </motion.div>
                <h2 className="text-2xl font-black text-text-primary mt-2">You completed all 3 free lessons!</h2>
                <p className="text-gray-400 mt-2 text-sm">You just scratched the surface — here's what's next</p>
              </div>

              {conversionData.messages && (
                <div className="space-y-2 mb-6">
                  {conversionData.messages.map((msg, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                      <Star size={14} className="text-cyan-400 shrink-0 mt-0.5" />
                      {msg}
                    </div>
                  ))}
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-xs font-mono uppercase tracking-wider text-cyan-400 mb-3 flex items-center gap-2">
                  <Zap size={14} /> What's Next with Pro
                </h3>
                <div className="space-y-2">
                  {conversionData.features && conversionData.features.map((feature, idx) => (
                    <div key={idx} className="flex items-start gap-3 text-sm text-gray-300">
                      <CheckCircle2 size={16} className="text-emerald-400 shrink-0 mt-0.5" />
                      {feature}
                    </div>
                  ))}
                </div>
              </div>

              {conversionData.pricing && (
                <div className="glass rounded-xl p-4 mb-6 space-y-3">
                  <h3 className="text-xs font-mono uppercase tracking-wider text-gray-500 mb-2">Pricing</h3>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400">Pro Monthly</span>
                    <span className="text-text-primary font-bold">{conversionData.pricing.pro_monthly}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400">Lifetime Access</span>
                    <span className="text-text-primary font-bold">{conversionData.pricing.lifetime}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm bg-amber-500/10 rounded-lg p-2 px-3 border border-amber-500/20">
                    <span className="text-amber-400">Student Discount</span>
                    <span className="text-amber-300 font-bold">{conversionData.pricing.student_discount}</span>
                  </div>
                </div>
              )}

              <p className="text-center text-xs font-mono text-gray-500 mb-6">
                Join 10,000+ learners preparing for placements
              </p>

              <div className="flex flex-col gap-3 mb-4">
                <button
                  onClick={() => navigate("/register")}
                  className="w-full inline-flex items-center justify-center gap-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-text-primary font-bold px-8 py-4 rounded-xl hover:from-cyan-400 hover:to-blue-400 transition-all"
                >
                  <Rocket size={18} />
                  Create Free Account
                </button>
                <button
                  onClick={() => navigate("/pricing")}
                  className="w-full inline-flex items-center justify-center gap-2 border border-cyan-500/30 bg-cyan-500/10 text-cyan-300 font-semibold px-8 py-4 rounded-xl hover:bg-cyan-500/20 transition-all"
                >
                  <Zap size={18} />
                  Go Pro — $9/mo
                </button>
              </div>

              <p className="text-center text-xs text-gray-500 mb-4">
                Start your journey now — free lessons available monthly
              </p>

              <div className="flex flex-col gap-2">
                <button
                  onClick={() => { trackConversion(false); navigate("/register"); }}
                  className="w-full text-center text-sm text-gray-400 hover:text-white transition-colors py-2"
                >
                  Create a free account to continue
                </button>
                <button
                  onClick={handleResetTrial}
                  className="w-full text-center text-xs text-gray-500 hover:text-gray-400 transition-colors py-2"
                >
                  Go back to lessons
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}