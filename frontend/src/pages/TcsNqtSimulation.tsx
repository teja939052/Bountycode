import { useState, useEffect, useCallback, useMemo, useRef } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import TestTakerAttestation from "../components/TestTakerAttestation";
import {
  Clock,
  CheckCircle,
  ArrowRight,
  ArrowLeft,
  FileText,
  ChevronRight,
  AlertTriangle,
  BarChart3,
  Timer,
  Target,
  Layers,
  Lightbulb,
  GraduationCap,
  Database,
  Code2,
  Download,
} from "lucide-react";

// TCS NQT two-stage structure (pattern-relevant — public exam-pattern analysis,
// NOT exact verified per-cycle counts; the real paper varies by hiring cycle).
const STAGES = [
  {
    id: "foundation",
    title: "Foundation",
    subtitle: "Part A — Aptitude",
    accent: "nature-blossom",
    note: "Numerical Ability, Reasoning Ability & Verbal Ability",
    sections: [
      { id: "aptitude", label: "Numerical Ability", icon: "🔢" },
      { id: "logical", label: "Reasoning Ability", icon: "🧩" },
      { id: "verbal", label: "Verbal Ability", icon: "📝" },
    ],
  },
  {
    id: "advanced",
    title: "Advanced",
    subtitle: "Part B — Programming",
    accent: "cyber-blue",
    note: "Programming Logic (MCQ) + 2 coding problems",
    sections: [
      { id: "cs_fundamentals", label: "Programming Logic (MCQ)", icon: "💠" },
      { id: "coding", label: "Coding", icon: "⌨️" },
    ],
  },
];

const SECTION_META: Record<string, { label: string; stage: string }> = {
  aptitude: { label: "Numerical Ability", stage: "foundation" },
  logical: { label: "Reasoning Ability", stage: "foundation" },
  verbal: { label: "Verbal Ability", stage: "foundation" },
  cs_fundamentals: { label: "Programming Logic", stage: "advanced" },
  coding: { label: "Coding", stage: "advanced" },
};

interface OAQuestion {
  question_uid?: string;
  section?: string;
  section_label?: string;
  kind?: string;
  stage?: string;
  question?: string;
  description?: string;
  options?: unknown[];
  time_limit?: number;
  topic?: string;
  starter_code?: Record<string, string>;
  language?: string;
  function_name?: string;
  trust_status?: string;
  verified_by_takers?: number;
}

interface ExamSection {
  id: string;
  title: string;
  type: string;
  question_ids: string[];
  time_limit_s: number;
}

interface SessionResult {
  overall_readiness?: number;
  verdict?: string;
  readiness_message?: string;
  section_scores?: Record<string, number>;
  score_breakdown?: Record<string, { avg: number; correct: number; total: number }>;
  strong_areas?: string[];
  weak_areas?: string[];
  questions_answered?: number;
  total_questions?: number;
  tab_switch_count?: number;
  scorecard?: Array<Record<string, unknown>>;
  next_missions?: Array<{ title: string; to: string; action?: string }>;
}

const STAGE_AXIS_STYLE: Record<string, string> = {
  foundation: "bg-blossom-50 text-nature-blossom border-nature-blossom/30",
  advanced: "bg-cyber-blue/10 text-cyber-blue border-cyber-blue/30",
};

function formatClock(s: number) {
  const m = Math.floor(Math.max(0, s) / 60);
  const sec = Math.max(0, s) % 60;
  return `${m}:${sec.toString().padStart(2, "0")}`;
}

function ScoreRing({ percentage, size = 180 }: { percentage: number; size?: number }) {
  const p = Math.max(0, Math.min(100, percentage || 0));
  const r = (size - 16) / 2;
  const circ = 2 * Math.PI * r;
  const color = p >= 75 ? "#7AAF5B" : p >= 55 ? "#F59E0B" : "#EF4444";
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg className="w-full h-full -rotate-90" viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(0,0,0,0.06)" strokeWidth="8" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={circ * (1 - p / 100)}
          style={{ transition: "stroke-dashoffset 1s ease" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-display font-black text-4xl" style={{ color }}>{p}%</span>
        <span className="font-mono text-[11px] text-text-muted mt-1 uppercase tracking-widest">
          Ready
        </span>
      </div>
    </div>
  );
}

export default function TcsNqtSimulation() {
  const [step, setStep] = useState<"select" | "test" | "results">("select");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [questions, setQuestions] = useState<OAQuestion[]>([]);
  const [sections, setSections] = useState<ExamSection[]>([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<number, unknown>>({});
  const [submitted, setSubmitted] = useState<Record<number, boolean>>({});
  const [sectionIdx, setSectionIdx] = useState(0);
  const [sectionTimeLeft, setSectionTimeLeft] = useState(0);
  const [result, setResult] = useState<SessionResult | null>(null);
  const [codeDraft, setCodeDraft] = useState("");
  const [reportLoading, setReportLoading] = useState(false);
  const [reportError, setReportError] = useState("");
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const submittingRef = useRef(false);
  const secElapsedRef = useRef(0);

  const currentSection = sections[sectionIdx];

  const sectionQuestions = useMemo(() => {
    if (!currentSection?.question_ids?.length) return [];
    const ids = new Set(currentSection.question_ids);
    return questions
      .map((q, i) => ({ q, i }))
      .filter(({ q }) => ids.has(String(q.question_uid)));
  }, [currentSection, questions]);

  const qInSection = currentSection
    ? sectionQuestions.findIndex(({ i }) => i === currentQ)
    : -1;

  const answeredInSection = sectionQuestions.filter(({ i }) => submitted[i]).length;

  useEffect(() => {
    if (step !== "test") return;
    const sec = sections[sectionIdx];
    if (!sec) return;
    timerRef.current = setInterval(() => {
      setSectionTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timerRef.current as ReturnType<typeof setInterval>);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [step, sections, sectionIdx]);

  const submitCurrentAnswer = useCallback(
    async (answer: unknown) => {
      const q = questions[currentQ];
      if (!q?.question_uid) return;
      await api.oa
        .submitAnswer(sessionId, [
          {
            question_uid: String(q.question_uid),
            answer,
            language: typeof q.language === "string" ? q.language : undefined,
            time_taken: Math.round((secElapsedRef.current)),
          },
        ])
        .catch(() => {});
      setAnswers((prev) => ({ ...prev, [currentQ]: answer }));
      setSubmitted((prev) => ({ ...prev, [currentQ]: true }));
    },
    [sessionId, currentQ, questions]
  );

  useEffect(() => {
    const sec = sections[sectionIdx];
    if (step === "test" && sec) {
      secElapsedRef.current = Math.round(sec.time_limit_s - sectionTimeLeft);
    }
  }, [sectionIdx, sectionTimeLeft, sections, step]);

  const completeSession = useCallback(async () => {
    if (submittingRef.current) return;
    submittingRef.current = true;
    try {
      const res = (await api.oa.complete(sessionId)) as SessionResult;
      setResult(res);
      setStep("results");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to complete assessment");
    } finally {
      submittingRef.current = false;
    }
  }, [sessionId]);

  const downloadReport = useCallback(async () => {
    if (!sessionId) return;
    setReportLoading(true);
    setReportError("");
    try {
      const blob = await api.oa.downloadReadinessReport(sessionId);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `readiness-report-${result?.company || "tcs_nqt"}-${sessionId}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e) {
      setReportError(e instanceof Error ? e.message : "Failed to download report");
    } finally {
      setReportLoading(false);
    }
  }, [sessionId, result?.company]);

  const advanceSection = useCallback(async () => {
    if (submittingRef.current) return;
    if (sectionIdx + 1 >= sections.length) {
      await completeSession();
      return;
    }
    setSectionIdx(sectionIdx + 1);
    setCurrentQ(sections[sectionIdx + 1]?.question_ids?.length
      ? questions.findIndex((q) => q.question_uid === sections[sectionIdx + 1].question_ids[0])
      : 0);
    setSectionTimeLeft(sections[sectionIdx + 1]?.time_limit_s || 0);
  }, [sectionIdx, sections, questions, completeSession]);

  const handleTimeout = useCallback(async () => {
    if (step !== "test") return;
    // Auto-advance on section time expiry (real NQT behavior).
    await advanceSection();
  }, [step, advanceSection]);

  useEffect(() => {
    if (step === "test" && sectionTimeLeft === 0 && sections.length > 0) {
      handleTimeout();
    }
  }, [sectionTimeLeft, step, sections.length, handleTimeout]);

  const startTest = async () => {
    setLoading(true);
    setError("");
    try {
      const data = (await api.oa.start({
        company: "tcs_nqt",
        role: "swe",
        total_questions: 50,
        duration_minutes: 190,
        mode: "calm",
        integrity: false,
        verified_only: true,
      })) as {
        session_id: string;
        questions?: OAQuestion[];
        sections?: ExamSection[];
      };
      const loadedQuestions = Array.isArray(data.questions) ? data.questions : [];
      const builtSections: ExamSection[] = (data.sections || []).map((s) => ({
        id: String(s.id),
        title: String(s.title),
        type: String(s.type),
        question_ids: Array.isArray(s.question_ids) ? s.question_ids.map(String) : [],
        time_limit_s: Number(s.time_limit_s) || 0,
      }));
      if (!loadedQuestions.length || !builtSections.length) {
        throw new Error(
          "Not enough independently-verified TCS NQT content in this section yet. Check back after the exam-memory bank grows."
        );
      }
      setSessionId(String(data.session_id));
      setQuestions(loadedQuestions);
      setSections(builtSections);
      setSectionIdx(0);
      const firstSectionIds = new Set(builtSections[0]?.question_ids || []);
      const firstIdx = loadedQuestions.findIndex((q) => firstSectionIds.has(String(q.question_uid)));
      setCurrentQ(firstIdx >= 0 ? firstIdx : 0);
      setAnswers({});
      setSubmitted({});
      setSectionTimeLeft(builtSections[0]?.time_limit_s || 0);
      setResult(null);
      setStep("test");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start simulation");
    } finally {
      setLoading(false);
    }
  };

  const navigateQuestion = (idx: number) => {
    if (idx < 0 || idx >= questions.length) return;
    const q = questions[idx];
    if (!q) return;
    if (q.section !== currentSection?.id) return; // locked to current section (real NQT)
    setCurrentQ(idx);
  };

  // ─────────────────────────── SELECT ───────────────────────────
  if (step === "select") {
    return (
      <div className="page-surface min-h-screen py-10 px-4">
        <div className="max-w-5xl mx-auto">
          <motion.div className="text-center mb-10" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <span className="section-subheader mb-3 block">TCS National Qualifier Test</span>
            <h1 className="section-header text-3xl mb-3 flex items-center justify-center gap-2">
              <GraduationCap className="text-nature-blossom" size={30} />
              TCS NQT <span className="text-nature-blossom">Simulation</span>
            </h1>
            <p className="text-text-muted font-mono text-sm max-w-2xl mx-auto">
              Two-stage simulation mirroring the real NQT format — timed Foundation
              aptitude plus an Advanced programming round. Questions are
              independently verified; the structure is{" "}
              <span className="text-nature-blossom font-medium">pattern-relevant</span>{" "}
              (public exam-pattern analysis, not exact per-cycle counts).
            </p>
          </motion.div>

          {error && (
            <div className="mx-auto max-w-xl mb-8 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-center font-mono text-sm text-red-600">
              {error}
            </div>
          )}

          <div className="grid gap-5 md:grid-cols-2 mb-8">
            {STAGES.map((stage, si) => (
              <motion.div
                key={stage.id}
                className={`card rounded-3xl border p-6 ${
                  stage.id === "foundation" ? "border-nature-blossom/40 bg-blossom-50/30" : "border-cyber-blue/40 bg-cyber-blue/5"
                }`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: si * 0.08 }}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className={`rounded-full border px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-widest ${STAGE_AXIS_STYLE[stage.id]}`}>
                    Part {si === 0 ? "A" : "B"}
                  </span>
                  <span className="font-mono text-[10px] text-text-muted">pattern-relevant</span>
                </div>
                <h2 className="font-display text-lg font-bold text-text-primary mt-2">{stage.title}</h2>
                <p className="font-mono text-xs text-text-muted mb-3">{stage.note}</p>
                <div className="space-y-2">
                  {stage.sections.map((s) => (
                    <div key={s.id} className="flex items-center gap-3 rounded-xl border border-black/5 bg-white px-3 py-2">
                      <span className="text-lg">{s.icon}</span>
                      <span className="text-sm text-text-secondary">{s.label}</span>
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>

          <motion.div className="card rounded-3xl mx-auto max-w-2xl" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <h3 className="font-display font-bold text-text-primary text-sm mb-1 flex items-center gap-2">
                  <Layers size={16} className="text-nature-blossom" /> Take the simulation
                </h3>
                <p className="font-mono text-xs text-text-muted">~50 questions · timed sections · no negative marking</p>
              </div>
              <button onClick={startTest} disabled={loading} className="btn-primary flex items-center gap-2">
                {loading ? <Spinner size="sm" className="text-space-void" /> : <>Start NQT <ArrowRight size={16} /></>}
              </button>
            </div>
          </motion.div>

          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            {[
              { icon: <Database size={16} />, t: "Verified content only", d: "Every served question is independently checked — no legacy unverified filler." },
              { icon: <Timer size={16} />, t: "Real section pacing", d: "Foundation and Advanced are time-boxed like the real paper; sections lock." },
              { icon: <Lightbulb size={16} />, t: "Exam-memory bank", d: "Did you just take NQT? Contribute what you remember — it grows this simulator." },
            ].map((f) => (
              <motion.div key={f.t} className="card rounded-2xl" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}>
                <div className="text-nature-blossom mb-2">{f.icon}</div>
                <h4 className="text-sm font-semibold text-text-primary mb-1">{f.t}</h4>
                <p className="font-mono text-[11px] leading-relaxed text-text-muted">{f.d}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // ─────────────────────────── TEST ───────────────────────────
  if (step === "test" && questions.length > 0) {
    const q = questions[currentQ];
    const secMeta = SECTION_META[q?.section || ""] || { label: q?.section_label || "Section", stage: "foundation" };
    const stageAxis = STAGE_AXIS_STYLE[secMeta.stage] || STAGE_AXIS_STYLE.foundation;
    const isMcq = q?.kind === "mcq";
    const sectionProgress = sections.length
      ? ((sectionIdx + (answeredInSection > 0 ? 1 : 0)) / sections.length) * 100
      : 0;
    const totalAnswered = Object.keys(submitted).length;

    return (
      <div className="min-h-screen">
        <div className="sticky top-0 z-30 border-b border-black/5 bg-white/95 backdrop-blur">
          <div className="max-w-7xl mx-auto px-4 py-2.5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3 min-w-0">
                <GraduationCap size={18} className="text-nature-blossom shrink-0" />
                <span className="font-display font-bold text-text-primary text-sm hidden sm:inline">TCS NQT</span>
                <span className={`rounded-full border px-2 py-0.5 font-mono text-[10px] uppercase tracking-widest ${stageAxis}`}>
                  {secMeta.stage} · {currentSection?.title || secMeta.label}
                </span>
                <span className="font-mono text-[11px] text-text-muted hidden sm:inline">
                  Q{currentQ + 1} of {questions.length}
                </span>
              </div>
              <div className="flex items-center gap-4">
                <span className="font-mono text-[11px] text-text-muted">
                  {totalAnswered}/{questions.length} answered
                </span>
                <div className="flex items-center gap-2">
                  <Clock size={14} className="text-text-muted" />
                  <span
                    className={`font-display font-black text-lg leading-none ${
                      sectionTimeLeft <= 60 ? "text-red-500" : "text-text-primary"
                    }`}
                  >
                    {formatClock(sectionTimeLeft)}
                  </span>
                </div>
              </div>
            </div>
            <div className="h-1 mt-2 rounded-full bg-surface-2 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-nature-blossom to-cyber-blue transition-all duration-300"
                style={{ width: `${sectionProgress}%` }}
              />
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 py-6 flex gap-6">
          <div className="flex-1 min-w-0">
            <AnimatePresence mode="wait">
              <motion.div key={currentQ} initial={{ opacity: 0, x: -14 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 18 }} transition={{ duration: 0.18 }}>
                <div className="card mb-4 rounded-2xl">
                  <div className="flex items-start justify-between mb-1 gap-3">
                    <span className="font-mono text-[10px] uppercase tracking-wider text-text-muted">
                      Question {currentQ + 1} of {questions.length}
                      {
                        q.topic && <span className="ml-2 normal-case text-nature-blossom">{q.topic}</span>
                      }
                      <TestTakerAttestation count={q.verified_by_takers} />
                    </span>
                    {submitted[currentQ] && (
                      <span className="rounded-full bg-emerald-100 px-2 py-0.5 font-mono text-[10px] text-emerald-700">
                        Answered
                      </span>
                    )}
                  </div>
                  <p className="font-display font-medium text-text-primary leading-relaxed text-[15px] mt-2">
                    {q.question || q.description}
                  </p>
                </div>

                {isMcq ? (
                  <div className="space-y-2.5 mb-6">
                    {(q.options || []).map((opt, idx) => {
                      const isSelected = answers[currentQ] === idx;
                      const answered = submitted[currentQ];
                      return (
                        <button
                          key={idx}
                          onClick={() => !answered && submitCurrentAnswer(idx)}
                          disabled={answered || loading}
                          className={`w-full text-left p-3.5 rounded-xl border-2 transition-all text-sm flex items-start gap-3 ${
                            answered
                              ? "border-black/5 bg-white text-text-muted pointer-events-none"
                              : isSelected
                              ? "border-nature-blossom bg-blossom-50 text-text-primary"
                              : "border-black/5 bg-white text-text-secondary hover:border-nature-blossom/60"
                          }`}
                        >
                          <span className={`font-bold shrink-0 w-6 h-6 rounded-full border border-current flex items-center justify-center text-[10px] ${isSelected ? "text-nature-blossom" : "text-text-muted"}`}>
                            {String.fromCharCode(65 + idx)}
                          </span>
                          <span className="leading-relaxed">{String(opt)}</span>
                        </button>
                      );
                    })}
                  </div>
                ) : (
                  <div className="mb-6">
                    <div className="mb-2 flex items-center gap-2 text-xs font-mono text-text-muted">
                      <Code2 size={14} className="text-cyber-blue" /> Provide your {q.language || "python"} solution
                    </div>
                    <textarea
                      value={typeof answers[currentQ] === "string" ? (answers[currentQ] as string) : codeDraft}
                      onChange={(e) => setCodeDraft(e.target.value)}
                      rows={12}
                      placeholder={Object.keys(q.starter_code || {}).length
                        ? (q.starter_code || {}).python
                        : "# def solve(...):\n#   ..."}
                      className="w-full rounded-xl border border-black/10 bg-[#0d1117] p-4 font-mono text-xs text-emerald-300 focus:border-cyber-blue/60 focus:outline-none"
                    />
                    <button
                      onClick={() => submitCurrentAnswer(typeof answers[currentQ] === "string" ? answers[currentQ] : codeDraft)}
                      disabled={submitted[currentQ] || loading}
                      className="btn-primary mt-2 flex items-center gap-2 text-sm disabled:opacity-50"
                    >
                      <CheckCircle size={15} /> {submitted[currentQ] ? "Submitted" : "Submit solution"}
                    </button>
                  </div>
                )}

                <div className="flex items-center justify-between">
                  <button
                    onClick={() => {
                      const prev = sectionQuestions.filter(({ i }) => i < currentQ);
                      navigateQuestion(prev.length ? prev[prev.length - 1].i : currentQ);
                    }}
                    disabled={qInSection < 0}
                    className="btn-ghost flex items-center gap-1 disabled:opacity-30"
                  >
                    <ArrowLeft size={16} /> Previous
                  </button>
                  {qInSection < sectionQuestions.length - 1 ? (
                    <button onClick={() => navigateQuestion(sectionQuestions[qInSection + 1]?.i ?? currentQ)} className="btn-secondary flex items-center gap-1">
                      Next <ChevronRight size={16} />
                    </button>
                  ) : (
                    <button onClick={advanceSection} disabled={loading} className="btn-primary flex items-center gap-2">
                      {sectionIdx + 1 >= sections.length ? "Submit NQT" : "Submit Section"} <ArrowRight size={16} />
                    </button>
                  )}
                </div>
              </motion.div>
            </AnimatePresence>
          </div>

          <div className="w-64 shrink-0 hidden lg:block">
            <div className="sticky top-28 space-y-5">
              <div>
                <p className="font-mono text-[10px] uppercase tracking-widest text-text-muted mb-3 flex items-center gap-1">
                  <Target size={11} /> Section Palette
                </p>
                <div className="grid grid-cols-6 gap-1.5">
                  {sectionQuestions.map(({ i }, k) => {
                    const isCurrent = i === currentQ;
                    const isAnswered = submitted[i];
                    return (
                      <button
                        key={i}
                        onClick={() => navigateQuestion(i)}
                        className={`h-8 rounded-lg font-mono text-[11px] font-bold border transition-all ${
                          isCurrent
                            ? "bg-nature-blossom text-white border-nature-blossom scale-110"
                            : isAnswered
                            ? "bg-emerald-100 text-emerald-700 border-emerald-200"
                            : "bg-white text-text-muted border-black/5 hover:border-nature-blossom/50"
                        }`}
                      >
                        {k + 1}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="border-t border-black/5 pt-4 space-y-2 text-xs font-mono">
                <div className="flex justify-between">
                  <span className="text-text-muted">Section answered</span>
                  <span className="text-nature-blossom">{answeredInSection}/{sectionQuestions.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Overall</span>
                  <span className="text-cyber-blue">{totalAnswered}/{questions.length}</span>
                </div>
              </div>

              <button onClick={advanceSection} disabled={loading} className="btn-primary w-full flex items-center justify-center gap-2">
                {sectionIdx + 1 >= sections.length ? <>Submit NQT <ArrowRight size={15} /></> : <>Next Section <ArrowRight size={15} /></>}
              </button>
              <button
                onClick={() => {
                  if (window.confirm("Submit the whole assessment now? Unanswered questions count as skipped.")) advanceSection();
                }}
                disabled={loading}
                className="btn-ghost w-full text-red-500 hover:text-red-600 text-xs"
              >
                <AlertTriangle size={12} className="inline mr-1" /> Early Submit
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ─────────────────────────── RESULTS ───────────────────────────
  if (step === "results" && result) {
    const pct = typeof result.overall_readiness === "number" ? result.overall_readiness : 0;
    const breakdown = Object.entries(result.score_breakdown || {});
    return (
      <div className="page-surface min-h-screen py-10 px-4">
        <div className="max-w-5xl mx-auto">
          <motion.div className="card mb-8 text-center rounded-3xl" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <span className="section-subheader mb-4 block">Simulation Complete</span>
            <div className="flex justify-center mb-3">
              <ScoreRing percentage={pct} />
            </div>
            <p className="font-display text-lg font-bold text-text-primary">{result.verdict}</p>
            <p className="font-mono text-xs text-text-muted mt-1">{result.readiness_message}</p>
            <p className="font-mono text-[11px] text-text-muted mt-2">
              {result.questions_answered}/{result.total_questions} answered ·{" "}
              {result.tab_switch_count || 0} tab switches
            </p>
            <div className="mt-4 flex flex-wrap justify-center gap-2">
              {(result.strong_areas || []).map((s) => (
                <span key={s} className="rounded-full bg-emerald-100 px-3 py-1 font-mono text-[11px] text-emerald-700">
                  ✓ {s}
                </span>
              ))}
              {(result.weak_areas || []).map((s) => (
                <span key={s} className="rounded-full bg-amber-100 px-3 py-1 font-mono text-[11px] text-amber-700">
                  needs work · {s}
                </span>
              ))}
            </div>
          </motion.div>

          <motion.div className="mb-8" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <h2 className="section-header text-lg mb-4 flex items-center gap-2">
              <BarChart3 size={20} className="text-nature-blossom" /> Section Breakdown
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {breakdown.map(([sec, stats]) => {
                const meta = SECTION_META[sec] || { label: sec, stage: "foundation" };
                const se = stats as { avg: number; correct: number; total: number };
                return (
                  <div key={sec} className="card rounded-2xl">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-display font-bold text-text-primary text-sm">{meta.label}</h3>
                      <span className={`rounded-full border px-2 py-0.5 font-mono text-[9px] uppercase tracking-widest ${STAGE_AXIS_STYLE[meta.stage]}`}>
                        {meta.stage}
                      </span>
                    </div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-mono text-2xl font-black text-nature-blossom">{Math.round(se.avg)}%</span>
                      <span className="font-mono text-xs text-text-muted">{se.correct}/{se.total}</span>
                    </div>
                    <div className="h-1.5 rounded-full bg-surface-2 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${se.avg >= 70 ? "bg-emerald-500" : se.avg >= 40 ? "bg-amber-500" : "bg-red-500"}`}
                        style={{ width: `${Math.max(2, se.avg)}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>

          <motion.div className="card rounded-3xl mb-8" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <h3 className="font-display font-bold text-text-primary text-sm mb-3 flex items-center gap-2">
              <Lightbulb size={16} className="text-amber-500" /> Repair path
            </h3>
            <div className="grid gap-2 sm:grid-cols-2">
              {(result.next_missions || []).length > 0 ? (
                (result.next_missions as Array<{ title: string; to: string }>).map((m, i) => (
                  <Link
                    key={i}
                    to={m.to}
                    className="flex items-center gap-2 rounded-xl border border-black/5 bg-white px-3 py-2.5 text-xs font-mono text-text-secondary transition-all hover:border-nature-blossom/40 hover:text-nature-blossom"
                  >
                    <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-amber-100 text-[10px] font-bold text-amber-700">{i + 1}</span>
                    {m.title}
                    <ArrowRight size={12} className="ml-auto shrink-0 opacity-60" />
                  </Link>
                ))
              ) : (
                <p className="text-xs text-text-muted font-mono">No critical weaknesses detected — keep leveling with the verified bank.</p>
              )}
            </div>
          </motion.div>

          <Link
            to={{ pathname: "/exam-memory/submit", search: "?exam=tcs_nqt" }}
            className="block rounded-3xl px-6 py-5 mb-6 text-center font-display font-black text-base sm:text-lg text-space-void transition-all duration-200 hover:scale-[1.015] hover:shadow-lg"
            style={{ backgroundColor: "#D4A843", color: "#0a0a0a" }}
          >
            <span className="flex items-center justify-center gap-3">
              <Database size={20} /> I just took the real NQT — submit what I remember
            </span>
            <span className="block font-mono text-[10px] font-normal mt-1 opacity-70 tracking-wide">
              Your recollections help build the verified question bank for future test-takers
            </span>
          </Link>

          {reportError && (
            <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-center font-mono text-sm text-red-600">
              {reportError}
            </div>
          )}

          <div className="grid gap-4 sm:grid-cols-2 mb-4">
            <button onClick={downloadReport} disabled={reportLoading} className="btn-secondary text-center flex items-center justify-center gap-2">
              {reportLoading ? <Spinner size="sm" /> : <><Download size={16} /> Download Readiness Report</>}
            </button>
            <Link to="/mock-oa" className="btn-secondary text-center flex items-center justify-center gap-2">
              <FileText size={16} /> Try another OA
            </Link>
            <Link to="/question-bank" className="btn-ghost text-center flex items-center justify-center gap-2">
              Practice the verified question bank
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Spinner size="lg" />
    </div>
  );
}