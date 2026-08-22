import { useState, useEffect, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import Editor from "@monaco-editor/react";
import {
  ArrowLeft, ArrowRight, CheckCircle2, Play, RotateCcw,
  BookOpen, Code, Trophy, Crown, Zap, Loader2, ChevronRight,
  Terminal, Copy, Check, Star, Sparkles, Eye, AlertTriangle,
  Lightbulb, Brain, Target, ListChecks, Rocket, ShieldCheck, XCircle, Package,
  Hammer, Briefcase, Wrench, Globe
} from "lucide-react";
import api from "../services/api";
import { studyApi } from "../services/api/study.ts";
import Spinner from "../components/ui/Spinner";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";
import AlgorithmVisualizer from "../components/AlgorithmVisualizer";

type AnnotatedCodeBlockProps = {
  code: any;
  languageId: any;
  annotations?: any[];
  runnable?: boolean;
  onRun?: (code: string) => void;
  running?: boolean;
};

function AnnotatedCodeBlock({ code, languageId, annotations, runnable = false, onRun, running = false }: AnnotatedCodeBlockProps) {
  const [copied, setCopied] = useState(false);
  const lang = languageId === "cpp" ? "cpp" : languageId === "java" ? "java" : "c";
  const lines = (code || "").split("\n");

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group rounded-xl overflow-hidden border border-white/5">
      <div className="flex items-center justify-between px-4 py-2 bg-[#0d1117] border-b border-white/5">
        <span className="text-xs font-mono text-brand-muted">{lang}</span>
        <div className="flex items-center gap-2">
          {runnable && (
            <button
              onClick={() => onRun?.(code)}
              disabled={running}
              className="flex items-center gap-1 text-xs px-2.5 py-1 rounded-md bg-cyber-green/15 border border-cyber-green/30 text-cyber-green hover:bg-cyber-green/25 transition-all disabled:opacity-50"
            >
              {running ? <Loader2 size={11} className="animate-spin" /> : <Play size={11} />}
              Try it Yourself
            </button>
          )}
          <button onClick={handleCopy} className="flex items-center gap-1 text-xs text-brand-muted hover:text-brand-secondary transition-colors">
            {copied ? <Check size={12} className="text-green-400" /> : <Copy size={12} />}
            {copied ? "Copied!" : "Copy"}
          </button>
        </div>
      </div>
      <div className="flex">
        <pre className="p-4 overflow-x-auto text-sm font-mono leading-relaxed flex-1" style={{ background: "#0d1117" }}>
          <code className="text-brand-secondary">
            {lines.map((line, i) => {
              const annot = annotations?.find(a => a.line === i + 1);
              return (
                <div key={i} className="flex items-start gap-3 min-h-[1.4em]">
                  <span className="text-brand-secondary text-xs select-none w-6 text-right shrink-0 leading-[1.4em]">{i + 1}</span>
                  <span className="whitespace-pre-wrap leading-[1.4em]">{line || " "}</span>
                  {annot && (
                    <span className="text-xs text-cyber-blue ml-2 shrink-0 leading-[1.4em] opacity-0 group-hover:opacity-100 transition-opacity">
                      ← {annot.text}
                    </span>
                  )}
                </div>
              );
            })}
          </code>
        </pre>
        {annotations && annotations.length > 0 && (
          <div className="hidden md:block w-64 shrink-0 border-l border-white/5 p-4 bg-[#0d1117]">
            <p className="text-xs font-mono text-brand-muted mb-3 uppercase tracking-wider">Annotations</p>
            <div className="space-y-3">
              {annotations.map((a, i) => (
                <div key={i} className="flex gap-2 text-xs">
                  <span className="text-cyber-blue font-mono shrink-0 w-5">L{a.line}</span>
                  <span className="text-brand-muted">{a.text}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function SimpleCodeBlock({ code, languageId }) {
  return (
    <AnnotatedCodeBlock code={code} languageId={languageId} annotations={[]} />
  );
}

function QuizCard({ quiz, onAnswer, answered }) {
  if (!quiz) return null;
  const [selected, setSelected] = useState(null);
  const [showResult, setShowResult] = useState(false);

  const handleSelect = (idx) => {
    if (answered || showResult) return;
    setSelected(idx);
    setShowResult(true);
    onAnswer?.(idx === quiz.correct);
  };

  const isCorrect = selected === quiz.correct;

  return (
    <div className="glass rounded-xl p-6">
      <h3 className="text-md font-display font-bold text-text-primary mb-4 flex items-center gap-2">
        <Brain size={16} className="text-purple-400" /> Quick Quiz
      </h3>
      <p className="text-sm font-mono text-brand-secondary mb-4">{quiz.question}</p>
      <div className="space-y-2">
        {quiz.options.map((opt, i) => {
          let btnStyle = "bg-surface-card/30 border-brand-primary/10 text-brand-secondary hover:bg-white/10";
          if (showResult) {
            if (i === quiz.correct) btnStyle = "bg-green-500/20 border-green-500/30 text-green-400";
            else if (i === selected && !isCorrect) btnStyle = "bg-red-500/20 border-red-500/30 text-red-400";
            else btnStyle = "bg-surface-card/30 border-brand-primary/10 text-brand-muted";
          } else if (selected === i) {
            btnStyle = "bg-cyber-blue/20 border-cyber-blue/30 text-cyber-blue";
          }
          return (
            <button key={i} onClick={() => handleSelect(i)}
              className={`w-full text-left px-4 py-2.5 rounded-lg border text-sm font-mono transition-all ${btnStyle}`}>
              <span className="text-brand-muted mr-2">{String.fromCharCode(65 + i)}.</span> {opt}
            </button>
          );
        })}
      </div>
      {showResult && (
        <motion.div initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }}
          className={`mt-4 p-3 rounded-lg text-sm font-mono ${isCorrect ? "bg-green-500/10 text-green-400 border border-green-500/20" : "bg-red-500/10 text-red-400 border border-red-500/20"}`}>
          {isCorrect ? "Correct!" : "Not quite."} {quiz.explanation}
        </motion.div>
      )}
    </div>
  );
}

export default function LessonView() {
  const { languageId, levelId, lessonId } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [showCelebrate, setShowCelebrate] = useState(false);
  const [xpResult, setXpResult] = useState(null);

  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);
  const [runError, setRunError] = useState("");
  const [checkResult, setCheckResult] = useState(null);

  const [traceData, setTraceData] = useState(null);
  const [tracing, setTracing] = useState(false);
  const [showVisualizer, setShowVisualizer] = useState(false);
  const [relatedArticles, setRelatedArticles] = useState([]);
  const [hintsOpen, setHintsOpen] = useState({});

  const exercises = data?.content?.exercises || [];
  const quizzes = data?.content?.quizzes || [];

  useEffect(() => {
    setLoading(true);
    setHintsOpen({});
    setOutput("");
    setRunError("");
    setTraceData(null);
    setShowVisualizer(false);
    setCheckResult(null);
    api.get(`/api/v1/learning/${languageId}/${levelId}/${lessonId}`)
      .then(d => {
        setData(d);
        setCompleted(d.completed);
        const content = d.content;
        const starterCode = content?.exercise?.starter_code || "";
        if (starterCode) {
          setCode(starterCode);
        } else {
          setCode(content?.code_example?.code || "");
        }
        studyApi
          .getRelatedArticles({ language: languageId, q: d.lesson?.title, limit: 3 })
          .then(rd => setRelatedArticles(rd.articles || []))
          .catch(() => {});
      })
      .catch(err => { console.error(err); })
      .finally(() => setLoading(false));
  }, [languageId, levelId, lessonId]);

  const getLangId = useCallback(() => {
    return languageId === "python" ? "python" : languageId === "cpp" ? "cpp" : languageId === "java" ? "java" : "c";
  }, [languageId]);

  const handleRunCode = useCallback(async (overrideCode?: string) => {
    const runCode = overrideCode ?? code;
    setRunning(true);
    setOutput("");
    setRunError("");
    setCheckResult(null);
    try {
      const result = await api.post("/api/v1/compiler/execute", {
        code: runCode,
        language: getLangId(),
        stdin: "",
        timeout: 10,
      });
      if (result.success) {
        const out = result.stdout || "(no output)";
        setOutput(out);
        return { stdout: out, success: true };
      }
      const msg = result.stderr || result.error || "Execution failed";
      setRunError(msg);
      return { stdout: "", success: false, stderr: msg };
    } catch (err) {
      setRunError(err.message || "Failed to execute");
      return { stdout: "", success: false, stderr: err.message };
    } finally {
      setRunning(false);
    }
  }, [code, getLangId]);

  const tryIt = useCallback((snippet) => {
    setCode(snippet || "");
    setOutput("");
    setRunError("");
    setCheckResult(null);
    handleRunCode(snippet || "");
  }, [handleRunCode]);

  const checkAnswer = useCallback(async (ex) => {
    if (!ex?.expected_output) return;
    setCheckResult(null);
    const result = await handleRunCode();
    const actual = (result?.stdout || "").trim();
    const expected = String(ex.expected_output || "").trim();
    const passed = result?.success === true && actual === expected;
    setCheckResult(passed ? "pass" : "fail");
    if (passed) {
      window.dispatchEvent(new CustomEvent("xp-gained", { detail: { xp: 5 } }));
    }
  }, [handleRunCode]);

  const toggleHints = (idx) => {
    setHintsOpen(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  const loadStarter = (ex) => {
    setCode(ex?.starter_code || "");
    setOutput("");
    setRunError("");
    setTraceData(null);
    setCheckResult(null);
  };

  const handleVisualize = useCallback(async () => {
    setTracing(true);
    setTraceData(null);
    setShowVisualizer(true);
    try {
      const result = await api.post("/api/v1/compiler/trace", { code, language: getLangId(), stdin: "" });
      setTraceData(result);
    } catch (err) {
      console.error(err);
      setTraceData({ steps: [{ line: 1, action: "Error", explanation: err.message || "Failed to generate trace", variables: {}, array_data: [] }], time_complexity: "?", space_complexity: "?" });
    } finally {
      setTracing(false);
    }
  }, [code, getLangId]);

  const handleComplete = useCallback(async () => {
    if (completed) return;
    setCompleting(true);
    try {
      const result = await api.post(`/api/v1/learning/${languageId}/${levelId}/${lessonId}/complete`, {});
      setCompleted(true);
      setXpResult(result);
      setShowCelebrate(true);
      window.dispatchEvent(new CustomEvent("xp-gained", { detail: { xp: result.xp_gained || data?.lesson?.xp || 10 } }));
    } catch (err) {
      console.error(err);
    } finally {
      setCompleting(false);
    }
  }, [languageId, levelId, lessonId, completed, data]);

  const resetPlayground = () => {
    const content = data?.content;
    const starterCode = content?.exercise?.starter_code || "";
    setCode(starterCode || content?.code_example?.code || "");
    setOutput("");
    setRunError("");
    setTraceData(null);
    setShowVisualizer(false);
    setCheckResult(null);
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;
  if (!data) return <div className="min-h-screen flex items-center justify-center text-brand-muted">Lesson not found</div>;

  const { lesson, next_lesson, level, content } = data;
  const isBoss = lesson.type === "boss";
  const isChallenge = lesson.type === "challenge";
  const isQuiz = lesson.type === "quiz";
  const isProject = lesson.type === "project";

  const codeExample = content?.code_example;
  const commonMistakes = content?.common_mistakes || [];
  const sections = content?.sections || [];
  const keyTakeaways = content?.key_takeaways || [];
  const nextSteps = content?.next_steps;
  const analogy = content?.analogy;

  return (
    <div className="relative min-h-screen px-4 py-8">
      <ArcadeBackdrop variant="candy" />
      <div className="relative z-10 mx-auto max-w-7xl">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <Link to={`/learn/${languageId}`} className="inline-flex items-center gap-2 text-brand-muted hover:text-text-primary transition-colors text-sm font-mono">
          <ArrowLeft size={14} /> {level.name}
        </Link>
        <div className="flex items-center gap-2 mt-2 flex-wrap">
          <span className={`text-xs px-2 py-0.5 rounded-full border font-mono ${
            isBoss ? "bg-red-500/10 text-red-400 border-red-500/30" :
            isChallenge ? "bg-orange-500/10 text-orange-400 border-orange-500/30" :
            isProject ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/30" :
            isQuiz ? "bg-purple-500/10 text-purple-400 border-purple-500/30" :
            lesson.type === "practice" ? "bg-green-500/10 text-green-400 border-green-500/30" :
            "bg-blue-500/10 text-blue-400 border-blue-500/30"
          }`}>
            {isBoss ? "BOSS BATTLE" : isChallenge ? "CHALLENGE" : isProject ? "PROJECT" : isQuiz ? "QUIZ" : lesson.type === "practice" ? "PRACTICE" : "LESSON"}
          </span>
          <span className="text-xs font-mono text-yellow-400/80">+{lesson.xp} XP</span>
          <span className="flex gap-0.5">
            {[1, 2, 3].map(d => (
              <Star key={d} size={10} className={d <= (lesson.difficulty || 1) ? "text-yellow-400 fill-yellow-400" : "text-brand-secondary"} />
            ))}
          </span>
        </div>
      </motion.div>

      <motion.h1 initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        className={`text-2xl md:text-3xl font-display font-black mb-6 ${isBoss ? "text-red-300" : "text-text-primary"}`}>
        {isBoss && <Crown className="inline mr-2 text-red-400" size={24} />}
        {lesson.title}
      </motion.h1>

      {/* Candy campaign strip */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.08 }}
        className="relative mb-6 overflow-hidden rounded-2xl p-4"
        style={{
          background: `linear-gradient(120deg, ${level.color && level.color !== "#fff" ? level.color : "#7A3FC4"}, ${level.color && level.color !== "#fff" ? level.color : "#FF5E8A"} 70%, #FFB703)`,
        }}
      >
        <div className="pointer-events-none absolute inset-x-0 top-0 h-1/2 bg-gradient-to-b from-white/25 to-transparent" />
        <div className="relative z-10 flex flex-wrap items-center gap-3">
          <span className="text-2xl">{level.emoji || "🍬"}</span>
          <div className="min-w-0 flex-1">
            <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-white/80">Learning campaign</p>
            <p className="truncate font-display text-sm font-bold text-white">{level.name}</p>
          </div>
          {completed ? (
            <span className="flex items-center gap-1 rounded-full bg-white/25 px-3 py-1 font-mono text-[10px] uppercase tracking-widest text-white">
              <CheckCircle2 size={12} /> Done
            </span>
          ) : (
            <Link to={`/learn/${languageId}`}
              className="flex items-center gap-1 rounded-full bg-black/25 px-3 py-1 font-mono text-[10px] uppercase tracking-widest text-white transition-colors hover:bg-black/40">
              View map <ArrowRight size={11} />
            </Link>
          )}
        </div>
      </motion.div>

      <div className="grid gap-6 lg:grid-cols-[1.05fr_0.9fr] lg:items-start">
        {/* LEFT — Lesson content */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }} className="space-y-6">

          {/* Boss/Challenge intro */}
          {isBoss && (
            <div className="glass rounded-xl p-6 border border-red-500/20 bg-red-500/5">
              <p className="text-sm font-mono text-red-300 flex items-center gap-2">
                <Crown size={16} /> Boss battle! This tests everything you've learned.
              </p>
            </div>
          )}
          {isChallenge && (
            <div className="glass rounded-xl p-6 border border-orange-500/20 bg-orange-500/5">
              <p className="text-sm font-mono text-orange-300 flex items-center gap-2">
                <Target size={16} /> Solve this challenge using what you've learned.
              </p>
            </div>
          )}

          {/* Theory Section */}
          {content?.theory && (
            <div className="glass rounded-xl p-6">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <BookOpen size={18} className="text-cyber-blue" /> Theory
              </h2>
              <div className="text-sm font-mono text-brand-secondary leading-relaxed space-y-4">
                <p>{content.theory}</p>
                {analogy && (
                  <div className="bg-cyber-blue/5 border border-cyber-blue/10 rounded-lg p-4">
                    <p className="text-xs text-cyber-blue/60 font-semibold uppercase tracking-wider mb-1">Real-World Analogy</p>
                    <p className="text-sm text-brand-secondary">{analogy}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Why this matters — world-class depth */}
          {lesson.why && (
            <div className="glass rounded-xl p-6 border border-cyber-blue/20 bg-cyber-blue/5">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Zap size={18} className="text-cyber-blue" /> Why This Matters
              </h2>
              <p className="text-sm font-mono text-brand-secondary leading-relaxed">{lesson.why}</p>
            </div>
          )}

          {/* Real-world use */}
          {lesson.real_world && (
            <div className="glass rounded-xl p-6">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Globe size={18} className="text-cyber-green" /> Real-World Use
              </h2>
              <p className="text-sm font-mono text-brand-secondary leading-relaxed">{lesson.real_world}</p>
            </div>
          )}

          {/* Sections (detailed breakdown with examples) */}
          {sections.length > 0 && sections.map((section, i) => (
            <div key={i} className="glass rounded-xl p-6">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                {i === 0 ? <Lightbulb size={18} className="text-yellow-400" /> : <ChevronRight size={18} className="text-cyber-green" />}
                {section.heading}
              </h2>
              <p className="text-sm font-mono text-brand-secondary leading-relaxed mb-3">{section.body}</p>
              {section.code && (
                <div className="mb-3">
                  <SimpleCodeBlock code={section.code} languageId={languageId} />
                </div>
              )}
              {section.pro_tip && (
                <div className="bg-yellow-500/5 border border-yellow-500/10 rounded-lg p-3 flex items-start gap-2">
                  <Zap size={14} className="text-yellow-400 mt-0.5 shrink-0" />
                  <p className="text-xs font-mono text-yellow-300">{section.pro_tip}</p>
                </div>
              )}
            </div>
          ))}

          {/* Code Example with Annotations + Try it Yourself */}
          {codeExample?.code && (
            <div className="glass rounded-xl p-6">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Code size={18} className="text-cyber-green" /> Code Example
              </h2>
              <AnnotatedCodeBlock
                code={codeExample.code}
                languageId={languageId}
                annotations={codeExample.annotations || []}
                runnable
                onRun={tryIt}
                running={running}
              />
            </div>
          )}

          {/* Common Mistakes */}
          {commonMistakes.length > 0 && (
            <div className="glass rounded-xl p-6">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <AlertTriangle size={18} className="text-red-400" /> Common Mistakes
              </h2>
              <div className="space-y-4">
                {commonMistakes.map((m, i) => (
                  <div key={i} className="border border-white/5 rounded-lg p-4 space-y-2">
                    <p className="text-sm font-mono text-red-300">❌ {m.mistake}</p>
                    <p className="text-sm font-mono text-green-400">✅ {m.fix}</p>
                    {(m.code || m.fixed_code) && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2">
                        {m.code && (
                          <div className="bg-red-500/5 rounded p-2">
                            <p className="text-xs text-red-400 mb-1 font-mono">Wrong</p>
                            <pre className="text-xs font-mono text-red-300 whitespace-pre-wrap">{m.code}</pre>
                          </div>
                        )}
                        {m.fixed_code && (
                          <div className="bg-green-500/5 rounded p-2">
                            <p className="text-xs text-green-400 mb-1 font-mono">Fixed</p>
                            <pre className="text-xs font-mono text-green-300 whitespace-pre-wrap">{m.fixed_code}</pre>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Exercises */}
          {exercises.length > 0 && (
            <div className="space-y-4">
              {exercises.map((exercise, exIdx) => (
                <div key={exIdx} className="glass rounded-xl p-6 border border-cyber-green/20">
                  <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                    <Target size={18} className="text-cyber-green" />
                    {exercises.length > 1 ? `Exercise ${exIdx + 1} of ${exercises.length}` : "Your Task"}
                  </h2>
                  <p className="text-sm font-mono text-brand-secondary leading-relaxed mb-4">{exercise.description}</p>

                  {exercise.expected_output && (
                    <div className="bg-[#0d1117] rounded-lg p-3 mb-4 border border-white/5">
                      <p className="text-xs text-brand-muted font-mono mb-1">Expected Output:</p>
                      <pre className="text-xs font-mono text-brand-secondary whitespace-pre-wrap">{exercise.expected_output}</pre>
                    </div>
                  )}

                  {exercise.hints && exercise.hints.length > 0 && (
                    <div className="mb-4">
                      <button onClick={() => toggleHints(exIdx)}
                        className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-mono hover:bg-purple-500/20 transition-all">
                        <Lightbulb size={12} /> {hintsOpen[exIdx] ? "Hide Hints" : `Show Hints (${exercise.hints.length})`}
                      </button>
                      <AnimatePresence>
                        {hintsOpen[exIdx] && (
                          <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -5 }}
                            className="mt-2 space-y-1">
                            {exercise.hints.map((hint, i) => (
                              <p key={i} className="text-xs font-mono text-purple-300 flex items-start gap-2">
                                <span className="text-purple-500 mt-0.5">💡</span> {hint}
                              </p>
                            ))}
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  )}

                  <div className="flex items-center gap-2 flex-wrap">
                    {exercise.starter_code && (
                      <button onClick={() => loadStarter(exercise)} disabled={running}
                        className="flex items-center gap-2 px-4 py-2 rounded-lg bg-surface-card/30 border border-brand-primary/10 text-brand-secondary text-sm font-mono hover:bg-white/10 transition-all disabled:opacity-50">
                        <Code size={14} /> Load starter code
                      </button>
                    )}
                    <button onClick={() => checkAnswer(exercise)} disabled={running}
                      className="flex items-center gap-2 px-4 py-2 rounded-lg bg-cyber-green/20 border border-cyber-green/30 text-cyber-green text-sm font-mono hover:bg-cyber-green/30 transition-all disabled:opacity-50">
                      {running ? <Loader2 size={14} className="animate-spin" /> : <ShieldCheck size={14} />}
                      Check Answer
                    </button>
                  </div>

                  <AnimatePresence>
                    {checkResult && (
                      <motion.div initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 5 }}
                        className={`mt-3 p-3 rounded-lg text-sm font-mono flex items-center gap-2 ${
                          checkResult === "pass"
                            ? "bg-green-500/10 text-green-400 border border-green-500/20"
                            : "bg-red-500/10 text-red-400 border border-red-500/20"
                        }`}>
                        {checkResult === "pass" ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
                        {checkResult === "pass"
                          ? "Passed! Output matches exactly. +5 XP."
                          : "Not quite — your output doesn't match the expected output. Try again."}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              ))}
            </div>
          )}

          {/* Project Brief */}
          {content?.project && (
            <div className="glass rounded-xl p-6 border border-yellow-500/20 bg-yellow-500/5">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Rocket size={18} className="text-yellow-400" /> Project Build Plan
              </h2>
              <p className="text-sm font-mono text-brand-secondary leading-relaxed mb-4">{content.project.brief}</p>

              <div className="space-y-4">
                {content.project.phases?.map((phase, i) => (
                  <div key={i} className="border border-white/5 rounded-lg p-4 bg-surface-card/10">
                    <h3 className="text-sm font-display font-bold text-yellow-300 mb-2">{phase.title}</h3>
                    <ul className="space-y-1.5">
                      {phase.tasks?.map((task, j) => (
                        <li key={j} className="flex items-start gap-2 text-sm font-mono text-brand-secondary">
                          <span className="text-yellow-500/70 mt-0.5">▸</span> {task}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>

              {content.project.checklist?.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-xs text-yellow-400/70 font-semibold uppercase tracking-wider mb-2">Completion Checklist</h3>
                  <ul className="space-y-1.5">
                    {content.project.checklist.map((item, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm font-mono text-brand-secondary">
                        <CheckCircle2 size={14} className="text-cyber-green mt-0.5 shrink-0" /> {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {content.project.deliverables?.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-xs text-yellow-400/70 font-semibold uppercase tracking-wider mb-2">Deliverables</h3>
                  <ul className="space-y-1.5">
                    {content.project.deliverables.map((item, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm font-mono text-brand-secondary">
                        <Package size={14} className="text-yellow-400 mt-0.5 shrink-0" /> {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Quizzes */}
          {quizzes.length > 0 && (
            <div className="space-y-4">
              {quizzes.map((quiz, i) => (
                <QuizCard key={i} quiz={quiz} answered={false} onAnswer={() => {}} />
              ))}
            </div>
          )}

          {/* Interview Prep — how interviewers ask this */}
          {lesson.interview?.length > 0 && (
            <div className="glass rounded-xl p-6 border border-purple-500/20 bg-purple-500/5">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Brain size={18} className="text-purple-400" /> Interview Prep
              </h2>
              <ul className="space-y-2.5">
                {lesson.interview.map((q: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-sm font-mono text-brand-secondary">
                    <span className="text-purple-400 mt-0.5 shrink-0">Q{i + 1}.</span> {q}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Build Something — every lesson ships an artifact */}
          {lesson.build && (
            <div className="glass rounded-xl p-6 border border-yellow-500/20 bg-yellow-500/5">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Hammer size={18} className="text-yellow-400" /> Build Something
              </h2>
              <p className="text-sm font-mono text-brand-secondary leading-relaxed">{lesson.build}</p>
            </div>
          )}

          {/* Problem Set — CS50-style applied problem */}
          {lesson.problem_set && (
            <div className="glass rounded-xl p-6">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Target size={18} className="text-cyber-green" /> Problem Set
              </h2>
              <p className="text-sm font-mono text-brand-secondary leading-relaxed">{lesson.problem_set}</p>
            </div>
          )}

          {/* Engineering practice */}
          {lesson.engineering && (
            <div className="glass rounded-xl p-6">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Wrench size={18} className="text-cyber-blue" /> Engineering Practice
              </h2>
              <p className="text-sm font-mono text-brand-secondary leading-relaxed">{lesson.engineering}</p>
            </div>
          )}

          {/* Career mapping */}
          {lesson.career && (
            <div className="glass rounded-xl p-6">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Briefcase size={18} className="text-cyber-green" /> Career Impact
              </h2>
              <p className="text-sm font-mono text-brand-secondary leading-relaxed">{lesson.career}</p>
            </div>
          )}

          {/* Level goals — world-class level enrichment */}
          {(level.interview_prep?.length > 0 || level.career_mapping?.length > 0 || level.capstone_challenge) && (
            <div className="glass rounded-xl p-6 border border-cyber-blue/20">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <Trophy size={18} className="text-yellow-400" /> This Level's Goals
              </h2>
              {level.capstone_challenge && (
                <div className="mb-3">
                  <p className="text-xs font-mono text-brand-muted uppercase tracking-wider mb-1">Capstone</p>
                  <p className="text-sm font-mono text-brand-secondary">{level.capstone_challenge}</p>
                </div>
              )}
              {level.interview_prep?.length > 0 && (
                <div className="mb-3">
                  <p className="text-xs font-mono text-brand-muted uppercase tracking-wider mb-1">Interview Drills</p>
                  <ul className="space-y-1.5">
                    {level.interview_prep.map((tip: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm font-mono text-brand-secondary">
                        <span className="text-purple-400 mt-0.5 shrink-0">▸</span> {tip}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {level.career_mapping?.length > 0 && (
                <div>
                  <p className="text-xs font-mono text-brand-muted uppercase tracking-wider mb-1">What This Unlocks</p>
                  <ul className="space-y-1.5">
                    {level.career_mapping.map((c: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm font-mono text-brand-secondary">
                        <span className="text-cyber-green mt-0.5 shrink-0">✓</span> {c}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Key Takeaways */}
          {keyTakeaways.length > 0 && (
            <div className="glass rounded-xl p-6">
              <h2 className="text-lg font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <ListChecks size={18} className="text-cyber-blue" /> Key Takeaways
              </h2>
              <ul className="space-y-2">
                {keyTakeaways.map((t, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm font-mono text-brand-secondary">
                    <Sparkles size={12} className="text-yellow-400 mt-0.5 shrink-0" />
                    {t}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Next Steps */}
          {nextSteps && (
            <div className="glass rounded-xl p-6 border border-cyber-blue/20 bg-cyber-blue/5">
              <p className="text-sm font-mono text-cyber-blue flex items-center gap-2">
                <Zap size={14} /> {nextSteps}
              </p>
            </div>
          )}

          {/* Related Study Articles — connect the dots */}
          {relatedArticles.length > 0 && (
            <div className="glass rounded-xl p-6 border border-purple-500/20 bg-purple-500/5">
              <h2 className="text-lg font-display font-bold text-text-primary mb-4 flex items-center gap-2">
                <BookOpen size={18} className="text-purple-400" /> Go deeper — study articles
              </h2>
              <div className="space-y-3">
                {relatedArticles.map(art => (
                  <Link
                    key={art.id}
                    to={`/study?article=${art.id}`}
                    className="block rounded-lg border border-white/5 bg-surface-card/10 p-4 transition-all hover:border-purple-400/30 hover:bg-purple-500/5"
                  >
                    <div className="flex items-center gap-2">
                      <span className={`rounded-full border px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider ${
                        art.category === "javascript" ? "text-[#F7DF1E] border-[#F7DF1E]/30" :
                        art.category === "react" ? "text-[#61DAFB] border-[#61DAFB]/30" :
                        art.category === "typescript" ? "text-[#3178C6] border-[#3178C6]/30" :
                        art.category === "node" ? "text-[#339933] border-[#339933]/30" :
                        art.category === "sql" ? "text-[#4479A1] border-[#4479A1]/30" :
                        "text-purple-300 border-purple-400/30"
                      }`}>
                        {art.category.replace("-", " & ")}
                      </span>
                      <span className="text-[10px] font-mono text-brand-muted">{art.read_time_min} min · {art.level}</span>
                    </div>
                    <p className="mt-2 text-sm font-medium text-gray-200">{art.title}</p>
                    <p className="mt-1 text-xs font-mono text-brand-muted line-clamp-2">{art.summary}</p>
                  </Link>
                ))}
              </div>
              <Link to="/study" className="mt-3 inline-flex items-center gap-1 text-xs font-mono text-purple-400 hover:text-purple-300 transition-colors">
                Browse full study library <ArrowRight size={12} />
              </Link>
            </div>
          )}

          {/* Complete Button */}
          <div className="flex items-center gap-4 flex-wrap">
            <button onClick={handleComplete} disabled={completed || completing}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-mono text-sm transition-all ${
                completed
                  ? "bg-green-500/20 border border-green-500/30 text-green-400 cursor-default"
                  : "bg-cyber-blue/20 border border-cyber-blue/30 text-cyber-blue hover:bg-cyber-blue/30 hover:shadow-lg hover:shadow-cyber-blue/10"
              }`}>
              {completed ? (
                <><CheckCircle2 size={16} /> Completed! (+{lesson.xp} XP)</>
              ) : completing ? (
                <><Loader2 size={16} className="animate-spin" /> Completing...</>
              ) : (
                <><CheckCircle2 size={16} /> Mark as Complete</>
              )}
            </button>

            {next_lesson && (
              <Link to={`/learn/${languageId}/${levelId}/${next_lesson.id}`}
                className="flex items-center gap-2 px-6 py-3 rounded-xl bg-surface-card/30 border border-brand-primary/10 text-brand-secondary font-mono text-sm hover:bg-surface-card/50 transition-all">
                Next: {next_lesson.title}
                <ArrowRight size={14} />
              </Link>
            )}

            {!next_lesson && completed && (
              <Link to={`/learn/${languageId}`}
                className="flex items-center gap-2 px-6 py-3 rounded-xl bg-yellow-500/20 border border-yellow-500/30 text-yellow-400 font-mono text-sm hover:bg-yellow-500/30 transition-all">
                <Trophy size={16} /> Level Complete!
              </Link>
            )}
          </div>
        </motion.div>

        {/* RIGHT — Sticky practice console */}
        <div className="space-y-6 lg:sticky lg:top-6">
          <div className="glass rounded-xl p-6">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-display font-bold text-text-primary flex items-center gap-2">
                <Terminal size={18} className="text-cyber-purple" /> Code Playground
              </h2>
              <a href="/playground" title="Open full digital playground"
                className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-cyber-purple/15 border border-cyber-purple/30 text-cyber-purple text-xs font-mono hover:bg-cyber-purple/25 transition-all">
                <Rocket size={12} /> Playground
              </a>
            </div>
            <div className="h-72 rounded-lg overflow-hidden border border-brand-primary/10">
              <Editor
                height="100%"
                language={getLangId()}
                theme="vs-dark"
                value={code}
                onChange={val => setCode(val || "")}
                options={{
                  minimap: { enabled: false },
                  fontSize: 13,
                  tabSize: 2,
                  lineNumbers: "on",
                  wordWrap: "on",
                  padding: { top: 8 },
                  bracketPairColorization: { enabled: true },
                  renderLineHighlight: "all",
                  smoothScrolling: true,
                  cursorBlinking: "smooth",
                  cursorSmoothCaretAnimation: "on",
                  scrollBeyondLastLine: false,
                }}
              />
            </div>

            <div className="flex items-center gap-3 mt-3 flex-wrap">
              <button onClick={() => handleRunCode()} disabled={running}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-cyber-green/20 border border-cyber-green/30 text-cyber-green text-sm font-mono hover:bg-cyber-green/30 transition-all disabled:opacity-50">
                {running ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
                {running ? "Running..." : "Run Code"}
              </button>
              {exercises[0]?.expected_output && (
                <button onClick={() => checkAnswer(exercises[0])} disabled={running}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500/20 border border-emerald-500/30 text-emerald-400 text-sm font-mono hover:bg-emerald-500/30 transition-all disabled:opacity-50">
                  <ShieldCheck size={14} /> Check Answer
                </button>
              )}
              <button onClick={handleVisualize} disabled={tracing}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-purple-500/20 border border-purple-500/30 text-purple-400 text-sm font-mono hover:bg-purple-500/30 transition-all disabled:opacity-50">
                {tracing ? <Loader2 size={14} className="animate-spin" /> : <Eye size={14} />}
                {tracing ? "Tracing..." : "Visualize"}
              </button>
              <button onClick={resetPlayground}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-surface-card/30 border border-brand-primary/10 text-brand-muted text-sm font-mono hover:text-text-primary transition-all">
                <RotateCcw size={14} /> Reset
              </button>
            </div>

            {(output || runError) && (
              <div className="mt-4 rounded-lg overflow-hidden border border-white/5">
                <div className="px-3 py-1.5 bg-[#0d1117] border-b border-white/5 text-xs font-mono text-brand-muted">
                  Output
                </div>
                <pre className={`p-4 bg-[#0d1117] text-sm font-mono whitespace-pre-wrap ${
                  runError ? "text-red-400" : "text-green-400"
                }`}>
                  {runError || output}
                </pre>
              </div>
            )}
          </div>

          {/* Algorithm Visualizer */}
          {showVisualizer && (
            <AlgorithmVisualizer
              traceData={traceData}
              code={code}
              language={languageId}
            />
          )}
        </div>
      </div>

      <AnimatePresence>
        {showCelebrate && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 flex items-center justify-center bg-black/70 z-50 p-4"
            onClick={() => setShowCelebrate(false)}>
            <motion.div initial={{ scale: 0.7, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.7, opacity: 0 }} transition={{ type: "spring", damping: 15 }}
              className="glass rounded-2xl p-8 max-w-sm w-full text-center border border-green-500/30"
              onClick={e => e.stopPropagation()}>
              <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2, type: "spring" }}
                className="text-5xl mb-4">
                {isBoss ? "👑" : lesson.type === "project" ? "🔨" : "🎉"}
              </motion.div>
              <h2 className="text-2xl font-display font-black text-white mb-2">
                {isBoss ? "Boss Defeated!" : isProject ? "Project Complete!" : "Lesson Complete!"}
              </h2>
              <p className="text-brand-muted text-sm font-mono mb-4">{lesson.title}</p>
              <div className="flex justify-center gap-6 mb-6">
                <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.3 }}>
                  <p className="text-2xl font-bold text-green-400">+{xpResult?.xp_gained || lesson.xp}</p>
                  <p className="text-xs text-brand-muted font-mono">XP EARNED</p>
                </motion.div>
                {xpResult?.bonus_xp > 0 && (
                  <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.4 }}>
                    <p className="text-2xl font-bold text-yellow-400">+{xpResult.bonus_xp}</p>
                    <p className="text-xs text-brand-muted font-mono">DAILY BONUS</p>
                  </motion.div>
                )}
                {xpResult?.daily_goal_reached && (
                  <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.5 }}>
                    <p className="text-2xl font-bold text-orange-400">🔥</p>
                    <p className="text-xs text-brand-muted font-mono">GOAL DONE</p>
                  </motion.div>
                )}
              </div>
              {next_lesson && (
                <Link to={`/learn/${languageId}/${levelId}/${next_lesson.id}`}
                  onClick={() => setShowCelebrate(false)}
                  className="block w-full py-3 rounded-xl bg-cyber-blue/20 border border-cyber-blue/30 text-cyber-blue font-mono text-sm hover:bg-cyber-blue/30 transition-all">
                  Continue → {next_lesson.title}
                </Link>
              )}
              {!next_lesson && (
                <Link to={`/learn/${languageId}`} onClick={() => setShowCelebrate(false)}
                  className="block w-full py-3 rounded-xl bg-yellow-500/20 border border-yellow-500/30 text-yellow-400 font-mono text-sm hover:bg-yellow-500/30 transition-all">
                  🏆 Level Complete!
                </Link>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
      </div>
    </div>
  );
}
