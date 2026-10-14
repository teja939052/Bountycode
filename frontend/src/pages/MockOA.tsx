// @ts-nocheck
import { useState, useEffect, useRef, useCallback, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import CelebrationOverlay from "../components/CelebrationOverlay";
import RepairPanel from "../components/RepairPanel";
import TestTakerAttestation from "../components/TestTakerAttestation";
import { useMockSession, type Section } from "../hooks/useMockSession";
import type { OASession, SubmitOAItem } from "../services/api/oa";
import {
  Clock,
  CheckCircle,
  XCircle,
  ArrowRight,
  ArrowLeft,
  FileText,
  Zap,
  ChevronRight,
  AlertTriangle,
  Trophy,
  BarChart3,
  Timer,
  Brain,
  Target,
  Eye,
  EyeOff,
  Database,
} from "lucide-react";
import { MentorCallout } from "../components/golden/MentorCallout";
import CampaignBanner from "../components/CampaignBanner";

const COMPANIES = [
  {
    id: "general",
    name: "General OA",
    logo: "📋",
    duration: 45,
    questionCount: 20,
    difficulty: "medium",
    sections: ["Quant", "Logical", "Verbal", "Technical"],
    description: "Mixed placement OA covering all sections",
    color: "cyber-blue",
  },
  {
    id: "tcs",
    name: "TCS",
    logo: "🔷",
    duration: 60,
    questionCount: 20,
    difficulty: "medium",
    sections: ["Quant", "Logical", "Verbal"],
    description: "TCS National Qualifier Test pattern",
    color: "cyber-blue",
  },
  {
    id: "infosys",
    name: "Infosys",
    logo: "🔹",
    duration: 45,
    questionCount: 15,
    difficulty: "medium",
    sections: ["Quant", "Logical", "Verbal"],
    description: "Infosys SPRT / Mysore training pattern",
    color: "cyber-purple",
  },
  {
    id: "wipro",
    name: "Wipro",
    logo: "💎",
    duration: 45,
    questionCount: 20,
    difficulty: "medium",
    sections: ["Quant", "Logical", "Verbal", "Technical"],
    description: "Wipro TopGear assessment pattern",
    color: "cyber-green",
  },
  {
    id: "cognizant",
    name: "Cognizant",
    logo: "🔶",
    duration: 30,
    questionCount: 15,
    difficulty: "medium",
    sections: ["Quant", "Logical", "Verbal"],
    description: "Cognizant GenC Next assessment",
    color: "cyber-amber",
  },
  {
    id: "capgemini",
    name: "Capgemini",
    logo: "🔆",
    duration: 45,
    questionCount: 20,
    difficulty: "medium",
    sections: ["Quant", "Logical", "Verbal", "Technical"],
    description: "Capgemini online assessment pattern",
    color: "cyber-amber",
  },
  {
    id: "ibm",
    name: "IBM",
    logo: "🔷",
    duration: 45,
    questionCount: 20,
    difficulty: "medium",
    sections: ["Quant", "Logical", "Verbal", "Technical"],
    description: "IBM entry-level Cognitive Ability round",
    color: "cyber-blue",
  },
  {
    id: "hcl",
    name: "HCL Tech",
    logo: "🟢",
    duration: 30,
    questionCount: 15,
    difficulty: "easy",
    sections: ["Quant", "Logical", "Verbal"],
    description: "HCL TalentConnect pattern",
    color: "cyber-green",
  },
  {
    id: "tech_mahindra",
    name: "Tech Mahindra",
    logo: "⚡",
    duration: 45,
    questionCount: 20,
    difficulty: "medium",
    sections: ["Quant", "Logical", "Verbal", "Technical"],
    description: "Tech Mahindra SMART assessment",
    color: "cyber-purple",
  },
];

const SECTION_CATEGORIES = {
  Quant: "quantitative",
  Logical: "logical",
  Verbal: "verbal",
  Technical: "technical",
};

const OA_TO_MEMORY_EXAM: Record<string, string> = {
  tcs: "tcs_nqt",
  infosys: "infytq",
  wipro: "wipro_nlth",
  cognizant: "cognizant_genc",
  accenture: "accenture",
  capgemini: "capgemini_amcat",
  ibm: "ibm_entry",
  hcl: "other",
  tech_mahindra: "other",
  general: "other",
};

const DURATION_OPTIONS = [
  { value: 30, label: "30 min" },
  { value: 45, label: "45 min" },
  { value: 60, label: "60 min" },
];

function QuestionPalette({
  total,
  current,
  answers,
  submittedAnswers,
  onNavigate,
}: {
  total: number;
  current: number;
  answers: Record<number, unknown>;
  submittedAnswers: Record<number, { is_correct?: boolean }>;
  onNavigate: (idx: number) => void;
}) {
  return (
    <div>
      <p className="font-mono text-[10px] uppercase tracking-widest text-gray-500 mb-3">
        Question Palette
      </p>
      <div className="grid grid-cols-5 gap-1.5">
        {Array.from({ length: total }, (_, i) => {
          const isCurrent = i === current;
          const isAnswered = answers[i] !== undefined;
          const isSubmitted = submittedAnswers[i] !== undefined;
          const isCorrect = submittedAnswers[i]?.is_correct;

          let btnClass =
            "w-9 h-9 rounded-lg font-mono text-xs font-bold transition-all duration-200 border ";
          if (isCurrent) {
            btnClass += "bg-brand-sky text-white border-brand-sky shadow-sm scale-110";
          } else if (isSubmitted && isCorrect) {
            btnClass += "bg-emerald-50 text-emerald-600 border-emerald-200";
          } else if (isSubmitted && !isCorrect) {
            btnClass += "bg-red-50 text-red-500 border-red-200";
          } else if (isAnswered) {
            btnClass += "bg-amber-50 text-amber-600 border-amber-200";
          } else {
            btnClass += "bg-white text-text-secondary border-black/5 hover:border-brand-primary/20 hover:text-text-primary";
          }

          return (
            <button
              key={i}
              onClick={() => onNavigate(i)}
              className={btnClass}
            >
              {i + 1}
            </button>
          );
        })}
      </div>
        <div className="mt-4 space-y-1.5">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-brand-sky" />
            <span className="font-mono text-[10px] text-text-secondary">Current</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-emerald-200" />
            <span className="font-mono text-[10px] text-text-secondary">Correct</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-red-200" />
            <span className="font-mono text-[10px] text-text-secondary">Wrong</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-amber-200" />
            <span className="font-mono text-[10px] text-text-secondary">Answered</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 rounded border border-black/5 bg-surface-2" />
            <span className="font-mono text-[10px] text-text-secondary">Unattempted</span>
          </div>
        </div>
    </div>
  );
}

function ScoreRing({
  percentage,
  size = 180,
  tone,
}: {
  percentage: number;
  size?: number;
  tone?: "neutral";
}) {
  const r = (size - 16) / 2;
  const circ = 2 * Math.PI * r;
  const offset =
    tone === "neutral" ? circ : circ * (1 - percentage / 100);
  const color =
    tone === "neutral"
      ? "#9CA3AF"
      : percentage >= 80
      ? "#22c55e"
      : percentage >= 60
      ? "#D4A843"
      : percentage >= 40
      ? "#f59e0b"
      : "#ef4444";

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg className="w-full h-full -rotate-90" viewBox={`0 0 ${size} ${size}`}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          strokeWidth="8"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          style={{
            filter: `drop-shadow(0 0 10px ${color})`,
            animation: "scoreRing 1.5s ease-out forwards",
          }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span
          className="font-display font-black text-4xl"
          style={{ color }}
        >
          {tone === "neutral" ? "—" : `${percentage}%`}
        </span>
        <span className="font-mono text-xs text-gray-500 mt-1">
          {tone === "neutral"
            ? "Awaiting result"
            : percentage >= 80
            ? "Competence verified"
            : percentage >= 60
            ? "Competent with gaps"
            : percentage >= 40
            ? "Fragile — repair needed"
            : "Not yet competent"}
        </span>
      </div>
    </div>
  );
}

interface OAQuestion extends Record<string, unknown> {
  question_uid?: string;
  id?: string;
  section?: string;
  kind?: string;
  language?: string;
  options?: Record<string, unknown>[];
  question?: string;
  verified_by_takers?: number;
}

interface AnswerResult {
  is_correct?: boolean;
  answer?: unknown;
}

export default function MockOA() {
  const [step, setStep] = useState<"select" | "test" | "results">("select");
  const [selectedCompany, setSelectedCompany] = useState<string | null>(null);
  const [customDuration, setCustomDuration] = useState(45);
  const [sessionId, setSessionId] = useState<string>("");
  const [questions, setQuestions] = useState<OAQuestion[]>([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<number, unknown>>({});
  const [submittedAnswers, setSubmittedAnswers] = useState<Record<number, AnswerResult>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [timeTaken, setTimeTaken] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [showCelebration, setShowCelebration] = useState(false);
  const [currentSection, setCurrentSection] = useState("");
  const [reviewMode, setReviewMode] = useState(false);
  const [showExplanation, setShowExplanation] = useState<Record<number, boolean>>({});
  const [sections, setSections] = useState<Section[]>([]);
  const [resultLoading, setResultLoading] = useState(false);
  const timerRef = useRef(null);

  const mockSession = useMockSession({
    mockId: sessionId,
    sections,
    onExamComplete: (sessionState) => {
      // Finalize on the BACKEND `/complete` endpoint. This is the only path
      // that grades answers, runs competence diagnosis, and persists repair
      // missions (fail → diagnose → repair → retest). Building the result
      // client-side skips all of it — so we always POST complete first and
      // only fall back to a placeholder on transport failure.
      setStep("results");
      setResultLoading(true);
      const fallback = () =>
        setResult({
          percentage: 0,
          correct: 0,
          wrong: 0,
          unattempted: questions.length,
          timeTaken: timeTaken,
          answers: sessionState.answers,
          tabViolations: sessionState.tabViolationsCount,
          isExamComplete: true,
          unreachable: true,
        });
      api
        .oa.complete(sessionId)
        .then((data: any) => {
          // Reconcile real per-question correctness from the server scorecard
          // so section breakdown + review rings reflect actual grading.
          const scorecard: any[] = Array.isArray(data?.scorecard)
            ? data.scorecard
            : [];
          if (scorecard.length) {
            setSubmittedAnswers((prev) => {
              const next: Record<number, AnswerResult> = { ...prev };
              scorecard.forEach((pq: any) => {
                const idx = questions.findIndex((q) => {
                  const uid = (q as any)?.question_uid;
                  return String(uid) === String(pq?.question_uid);
                });
                if (idx >= 0) {
                  next[idx] = {
                    ...(next[idx] ?? {}),
                    is_correct: Number(pq?.score) >= 100,
                  };
                }
              });
              return next;
            });
          }
          const readiness = Number(data?.overall_readiness);
          setResult({
            ...data,
            percentage: Number.isFinite(readiness)
              ? Math.max(0, Math.min(100, Math.round(readiness)))
              : Math.round(
                  ((Number(data?.correct_count) || 0) /
                    (Number(data?.total_questions) ||
                      questions.length ||
                      1)) *
                    100
                ),
            timeTaken: Number(data?.time_taken) || timeTaken,
            tabViolations: sessionState.tabViolationsCount,
            answers: sessionState.answers,
            isExamComplete: true,
          });
        })
        .catch(fallback)
        .finally(() => setResultLoading(false));
    },
  });

  const company = useMemo(
    () => COMPANIES.find((c) => c.id === selectedCompany) || COMPANIES[0],
    [selectedCompany]
  );

  useEffect(() => {
    let interval;
    if (step === "test" && startTime) {
      interval = setInterval(
        () => setTimeTaken(Math.floor((Date.now() - startTime) / 1000)),
        1000
      );
    }
    return () => clearInterval(interval);
  }, [step, startTime]);

  useEffect(() => {
    if (step === "test" && questions.length > 0) {
      const sectionSize = Math.ceil(questions.length / company.sections.length);
      const sectionIdx = Math.min(
        Math.floor(currentQ / sectionSize),
        company.sections.length - 1
      );
      setCurrentSection(company.sections[sectionIdx]);
    }
  }, [currentQ, questions.length, step, company.sections]);

  const handleTimeUp = useCallback(() => {
    if (step === "test") {
      mockSession.advanceSection();
    }
  }, [step, mockSession]);

  const navigateQuestion = (idx: number) => {
    if (idx >= 0 && idx < questions.length) {
      const sectionSize = Math.ceil(questions.length / company.sections.length);
      const targetSectionIdx = Math.min(
        Math.floor(idx / sectionSize),
        company.sections.length - 1
      );
      const currentSectionIdx = mockSession.state.currentSectionIndex;
      const completedSections = mockSession.state.completedSectionIds;
      const currentSectionId = mockSession.currentSection?.id;

      const isCurrentOrCompleted =
        targetSectionIdx <= currentSectionIdx &&
        (targetSectionIdx < currentSectionIdx ||
          (typeof currentSectionId === "string" && completedSections.includes(currentSectionId)));

      if (!isCurrentOrCompleted && targetSectionIdx > currentSectionIdx) {
        return;
      }
      setCurrentQ(idx);
    }
  };

  const startTest = async () => {
    setLoading(true);
    setError("");
    try {
      const companyId = (selectedCompany === "general" ? "swe" : selectedCompany) as string;
      const data = (await api.oa.start({
        company: companyId,
        role: "swe",
        total_questions: company.questionCount,
        duration_minutes: customDuration || company.duration,
        mode: "calm",
        integrity: false,
        verified_only: true,
      })) as OASession;
      const loadedQuestions: OAQuestion[] = Array.isArray(data.questions) ? data.questions : [];
      const builtSections: Section[] = (data.sections || []).map((section) => ({
        id: String(section.id),
        title: typeof section.title === "string" ? section.title : String(section.id),
        duration_minutes: Math.round((Number(section.time_limit_s) || 0) / 60) || Math.round((customDuration || company.duration) / (company.sections?.length || 1)),
        question_ids: Array.isArray(section.question_ids) ? section.question_ids.map(String) : [],
      }));

      setSessionId(String(data.session_id));
      setQuestions(loadedQuestions);
      setSections(builtSections);
      setCurrentQ(0);
      setAnswers({});
      setSubmittedAnswers({});
      setShowExplanation({});
      setStartTime(Date.now());
      setTimeTaken(0);
      setReviewMode(false);
      setResult(null);
      setResultLoading(false);
      setStep("test");
      mockSession.triggerFullscreen().catch(() => {});
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start test");
    }
    setLoading(false);
  };

  const submitAnswer = async (answer: unknown) => {
    if (submittedAnswers[currentQ] !== undefined) return;
    setLoading(true);
    setError("");
    try {
      const question = questions[currentQ];
      const item: SubmitOAItem = {
        question_uid: String(question?.question_uid || question?.id || currentQ),
        answer,
        language: typeof question?.language === "string" ? question.language : undefined,
        time_taken: Math.round(((Date.now() - (startTime || Date.now())) / 1000)),
      };
      await api.oa.submitAnswer(sessionId, [item]);
      setAnswers((prev) => ({ ...prev, [currentQ]: answer }));
      setSubmittedAnswers((prev) => ({ ...prev, [currentQ]: { is_correct: null, answer } as unknown as AnswerResult }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit answer");
    }
    setLoading(false);
  };

  const formatTime = (s) =>
    `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

  const answeredCount = Object.keys(submittedAnswers).length;
  const correctCount = Object.values(submittedAnswers).filter(
    (a: any) => a.is_correct
  ).length;
  const wrongCount = answeredCount - correctCount;
  const unattemptedCount = questions.length - answeredCount;

  const getSectionStats = (sectionName) => {
    const cat = SECTION_CATEGORIES[sectionName];
    if (!cat) return { total: 0, correct: 0, wrong: 0, unattempted: 0 };
    const sectionQs = questions.map((q, i) => ({ q, i })).filter(({ q }) => q.category === cat || q.category === sectionName.toLowerCase());
    const total = sectionQs.length;
    const correct = sectionQs.filter(({ i }) => submittedAnswers[i]?.is_correct).length;
    const answered = sectionQs.filter(({ i }) => submittedAnswers[i] !== undefined).length;
    return { total, correct, wrong: answered - correct, unattempted: total - answered };
  };

  // ═══════════════ SELECT SCREEN ═══════════════
  if (step === "select") {
    return (
      <div className="page-surface min-h-screen py-6 px-4">
        <CelebrationOverlay
          show={showCelebration}
          type="perfect"
          message="OA Destroyed!"
        />
        <div className="max-w-5xl mx-auto">
          <motion.div
            className="text-center mb-10"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <span className="section-subheader mb-3 block">
              Boss Assessment
            </span>
            <h1 className="section-header text-3xl mb-2">
              <Target className="text-brand-sky inline mr-2" size={28} />
              Mock <span className="text-brand-sky">Online Assessment</span>
            </h1>
            <p className="text-text-secondary text-sm max-w-lg mx-auto">
              This is a competence test, not a practice drill. Treat it like the real assessment: timed, focused, and diagnostic.
            </p>
            <MentorCallout phase="boss" message="Pick the company pattern closest to your target. The timer is real — pace yourself, don't rush the first section." size="compact" className="mt-4 max-w-lg mx-auto" />
          </motion.div>

          <CampaignBanner world="mock-oa" />

          {error && (
            <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">
              {error}
            </div>
          )}

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
            {COMPANIES.map((c, i) => (
              <motion.button
                key={c.id}
                onClick={() => {
                  setSelectedCompany(c.id);
                  setCustomDuration(c.duration);
                }}
                className={`card text-left transition-all border-2 ${
                  selectedCompany === c.id
                    ? `border-${c.color} bg-${c.color}/10`
                    : "border-transparent hover:border-black/5"
                }`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
                style={
                  selectedCompany === c.id
                    ? {
                        borderColor: `var(--tw-${c.color}-border, rgba(76,201,240,0.5))`,
                        backgroundColor: `rgba(76,201,240,0.06)`,
                      }
                    : {}
                }
              >
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-3xl">{c.logo}</span>
                  <div>
                    <h3 className="font-display font-bold text-text-primary text-sm">
                      {c.name}
                    </h3>
                    <p className="text-[10px] font-mono text-gray-500">
                      {c.description}
                    </p>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2 mb-3">
                  {c.sections.map((s) => (
                    <span
                      key={s}
                      className="rounded border border-black/5 bg-surface-2 px-2 py-0.5 text-[10px] font-mono text-text-muted"
                    >
                      {s}
                    </span>
                  ))}
                </div>
                <div className="flex items-center justify-between text-[10px] font-mono text-gray-500">
                  <span className="flex items-center gap-1">
                    <Clock size={10} /> {c.duration} min
                  </span>
                  <span>{c.questionCount} Qs</span>
                  <span className="capitalize">{c.difficulty}</span>
                </div>
              </motion.button>
            ))}
          </div>

          {selectedCompany && (
            <motion.div
              className="card"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                  <h3 className="font-display font-bold text-text-primary text-sm mb-1">
                    <span className="mr-2">{company.logo}</span>
                    {company.name} — Mock OA
                  </h3>
                  <p className="text-xs font-mono text-gray-500">
                    {company.questionCount} questions across{" "}
                    {company.sections.length} sections
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <Timer size={14} className="text-gray-500" />
                    <select
                      value={customDuration}
                      onChange={(e) => setCustomDuration(Number(e.target.value))}
                      className="rounded-lg border border-black/5 bg-white px-3 py-2 font-mono text-xs text-text-secondary focus:border-cyber-blue/50 focus:outline-none"
                    >
                      {DURATION_OPTIONS.map((d) => (
                        <option key={d.value} value={d.value}>
                          {d.label}
                        </option>
                      ))}
                    </select>
                  </div>
                  <button
                    onClick={startTest}
                    disabled={loading}
                    className="btn-primary flex items-center gap-2"
                  >
                    {loading ? (
                      <Spinner size="sm" className="text-space-void" />
                    ) : (
                      <>
                        Start Mock OA
                        <ArrowRight size={16} />
                      </>
                    )}
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    );
  }

  // ═══════════════ TEST SCREEN ═══════════════
  if (step === "test" && questions.length > 0) {
    const q = questions[currentQ];
    const sessionSection = mockSession.currentSection;
    const sectionTitle = sessionSection?.title || currentSection;
    const sectionSize = Math.ceil(questions.length / company.sections.length);
    const sectionIdx = mockSession.state.currentSectionIndex;
    const sectionStart = sectionIdx * sectionSize;
    const sectionEnd = Math.min(sectionStart + sectionSize, questions.length);
    const remainingSeconds = mockSession.state.timeRemainingSeconds;
    const tabWarnings = mockSession.state.tabViolationsCount;

    const formatTime = (s) =>
      `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

    return (
      <div className="min-h-screen">
        {/* ── Top Section Bar ── */}
        <div className="sticky top-0 z-30 border-b border-black/5 bg-white border-border/95 backdrop-blur">
          <div className="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="font-display font-bold text-text-primary text-sm flex items-center gap-2">
                <span className="text-lg">{company.logo}</span>
                {company.name}
              </span>
              <span className="w-px h-4 bg-space-border" />
              <span className="font-mono text-xs text-brand-sky">
                {sectionTitle}
              </span>
              <span className="font-mono text-[10px] text-gray-500">
                Q{currentQ + 1}–{sectionEnd} of {questions.length}
              </span>
            </div>
            <div className="flex items-center gap-3">
              {tabWarnings > 0 && (
                <span className="font-mono text-[10px] text-brand-amber">
                  ⚠ Tab switches: {tabWarnings}/3
                </span>
              )}
              <span className="font-mono text-xs text-gray-500">
                {answeredCount}/{questions.length} answered
              </span>
              <div className="flex flex-col items-center">
                <span className="font-display font-black text-lg text-text-primary leading-none">
                  {formatTime(remainingSeconds)}
                </span>
                <span className="font-mono text-[10px] text-gray-500">
                  Section Timer
                </span>
              </div>
            </div>
          </div>
          {/* Section Progress Bar */}
          <div className="h-1 bg-surface-2">
            <div
              className="h-full bg-gradient-to-r from-brand-sky to-brand-primary transition-all duration-300"
              style={{
                width: `${((currentQ + 1) / questions.length) * 100}%`,
              }}
            />
          </div>
        </div>

        {/* ── Main Content ── */}
        <div className="max-w-7xl mx-auto px-4 py-6 flex gap-6">
          <MentorCallout phase="active" message="Read each question twice. The first read is for meaning; the second is for traps." size="compact" className="w-full" />
          {/* Left: Question Panel */}
          <div className="flex-1 min-w-0">
            <AnimatePresence mode="wait">
              <motion.div
                key={currentQ}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.2 }}
              >
                <div className="card mb-4">
                  <div className="flex items-start justify-between mb-1">
                    <span className="font-mono text-[10px] text-gray-600 uppercase tracking-wider">
                      Question {currentQ + 1} of {questions.length}
                      {q.category && (
                        <span className="ml-2 text-brand-sky">
                          [{q.category}]
                        </span>
                      )}
                    </span>
                    {submittedAnswers[currentQ] && (
                      <span
                        className={`font-mono text-[10px] px-2 py-0.5 rounded-full ${
                          submittedAnswers[currentQ].is_correct
                            ? "bg-emerald-50 text-emerald-600 border border-emerald-200"
                            : "bg-red-50 text-red-500 border border-red-200"
                        }`}
                      >
                        {submittedAnswers[currentQ].is_correct
                          ? "Correct"
                          : "Wrong"}
                      </span>
                    )}
                  </div>
                  <p className="font-display font-bold text-text-primary text-lg leading-relaxed mt-3">
                    {q.question}
                  </p>
                  <TestTakerAttestation count={q.verified_by_takers} />
                </div>

                <div className="space-y-2.5 mb-6">
                  {q.options.map((option, idx) => {
                    const isSelected = answers[currentQ] === idx;
                    const isSubmitted = submittedAnswers[currentQ] !== undefined;
                    const isCorrectOption =
                      isSubmitted &&
                      submittedAnswers[currentQ].correct_answer === idx;
                    const isWrongSelected =
                      isSubmitted &&
                      isSelected &&
                      !submittedAnswers[currentQ].is_correct;

                    let optClass =
                      "w-full text-left p-4 rounded-xl border-2 transition-all font-mono text-sm flex items-start gap-3 ";

                    if (isSubmitted) {
                      if (isCorrectOption) {
                        optClass +=
                          "border-cyber-green bg-cyber-green/5 text-cyber-green";
                      } else if (isWrongSelected) {
                        optClass +=
                          "border-cyber-red bg-cyber-red/5 text-cyber-red";
                      } else {
                        optClass +=
                          "border-black/5 bg-white border-border/70 text-text-muted cursor-not-allowed";
                      }
                    } else if (isSelected) {
                      optClass +=
                        "border-cyber-blue bg-cyber-blue/10 text-text-primary shadow-cyber-blue";
                    } else {
                      optClass +=
                        "border-black/5 hover:border-gray-500 text-text-muted hover:text-text-primary hover:bg-surface-2 cursor-pointer";
                    }

                    return (
                      <button
                        key={idx}
                        onClick={() => !isSubmitted && submitAnswer(idx)}
                        disabled={isSubmitted || loading}
                        className={optClass}
                      >
                        <span className="font-bold text-cyber-blue shrink-0 w-6 h-6 rounded-full border border-current flex items-center justify-center text-[10px]">
                          {String.fromCharCode(65 + idx)}
                        </span>
                        <span className="leading-relaxed">{option}</span>
                        {isCorrectOption && (
                          <CheckCircle
                            size={18}
                            className="text-cyber-green shrink-0 ml-auto mt-0.5"
                          />
                        )}
                        {isWrongSelected && (
                          <XCircle
                            size={18}
                            className="text-cyber-red shrink-0 ml-auto mt-0.5"
                          />
                        )}
                      </button>
                    );
                  })}
                </div>

                {/* Explanation */}
                {submittedAnswers[currentQ] && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`card mb-4 ${
                      submittedAnswers[currentQ].is_correct
                        ? "border-cyber-green/20"
                        : "border-cyber-red/20"
                    }`}
                  >
                    <button
                      onClick={() =>
                        setShowExplanation((prev) => ({
                          ...prev,
                          [currentQ]: !prev[currentQ],
                        }))
                      }
                      className="flex items-center gap-2 text-xs font-mono text-gray-400 hover:text-text-primary transition-colors w-full"
                    >
                      {showExplanation[currentQ] ? (
                        <EyeOff size={14} />
                      ) : (
                        <Eye size={14} />
                      )}
                      {showExplanation[currentQ] ? "Hide" : "Show"} Explanation
                    </button>
                    {showExplanation[currentQ] && (
                      <p className="text-xs font-mono text-gray-400 mt-3 leading-relaxed">
                        {submittedAnswers[currentQ].explanation}
                      </p>
                    )}
                  </motion.div>
                )}

                {/* Navigation */}
                <div className="flex items-center justify-between">
                  <button
                    onClick={() => mockSession.canGoBack && navigateQuestion(currentQ - 1)}
                    disabled={!mockSession.canGoBack || currentQ === 0}
                    className="btn-ghost flex items-center gap-1 disabled:opacity-30"
                  >
                    <ArrowLeft size={16} /> Previous
                  </button>
                  <div className="flex items-center gap-3">
                    {currentQ < questions.length - 1 ? (
                      <button
                        onClick={() => navigateQuestion(currentQ + 1)}
                        disabled={mockSession.isLocked}
                        className="btn-secondary flex items-center gap-1"
                      >
                        Next <ChevronRight size={16} />
                      </button>
                    ) : (
                      <button
                        onClick={mockSession.advanceSection}
                        disabled={loading || mockSession.isLocked}
                        className="btn-primary flex items-center gap-2"
                      >
                        {loading ? (
                          <Spinner size="sm" className="text-space-void" />
                        ) : (
                          <>
                            Submit Section <ArrowRight size={16} />
                          </>
                        )}
                      </button>
                    )}
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Right Sidebar */}
          <div className="w-64 shrink-0 hidden lg:block">
            <div className="sticky top-28 space-y-6">
              <QuestionPalette
                total={questions.length}
                current={currentQ}
                answers={answers}
                submittedAnswers={submittedAnswers}
                onNavigate={navigateQuestion}
              />

              <div className="border-t border-black/5 pt-4">
                <p className="font-mono text-[10px] uppercase tracking-widest text-gray-500 mb-3">
                  Progress
                </p>
                <div className="space-y-2 text-xs font-mono">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Answered</span>
                    <span className="text-cyber-blue">{answeredCount}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Correct</span>
                    <span className="text-cyber-green">{correctCount}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Wrong</span>
                    <span className="text-cyber-red">{wrongCount}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Unattempted</span>
                    <span className="text-gray-400">
                      {unattemptedCount}
                    </span>
                  </div>
                </div>
              </div>

              <div className="border-t border-black/5 pt-4">
                <button
                  onClick={mockSession.advanceSection}
                  disabled={loading || mockSession.isLocked}
                  className="btn-primary w-full flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <Spinner size="sm" className="text-space-void" />
                  ) : (
                    <>
                      Submit Section <ArrowRight size={16} />
                    </>
                  )}
                </button>
                <button
                  onClick={() => {
                    if (
                      window.confirm(
                        "Are you sure? This will submit your OA."
                      )
                    ) {
                      mockSession.advanceSection();
                    }
                  }}
                  className="btn-ghost w-full mt-2 text-cyber-red hover:text-cyber-red text-xs"
                >
                  <AlertTriangle size={12} className="inline mr-1" />
                  Early Submit
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ═══════════════ RESULTS SCREEN ═══════════════
  if (step === "results" && result) {
    const total = questions.length;
    const pct = typeof result.percentage === "number" ? result.percentage : 0;
    const diag: any = result?.diagnosis ?? null;
    const skills: any[] = Array.isArray(diag?.skill_weaknesses)
      ? diag.skill_weaknesses.slice(0, 3)
      : [];
    const primary =
      typeof diag?.primary_weakness === "string"
        ? diag.primary_weakness
        : skills[0]?.skill ?? null;
    const chain: string[] = Array.isArray(diag?.repair_chain)
      ? diag.repair_chain
      : [];
    const retestCond =
      typeof diag?.retest_condition === "string"
        ? diag.retest_condition
        : "";
    const unreachable = result?.unreachable === true;

    return (
      <div className="page-surface min-h-screen py-6 px-4">
        <CelebrationOverlay
          show={showCelebration && !unreachable}
          type="perfect"
          message="OA Destroyed!"
        />
        <div className="max-w-5xl mx-auto">
          {unreachable && (
            <div className="mb-6 border-2 border-dashed border-brand-amber/60 bg-brand-amber/10 rounded-xl p-4 text-center">
              <p className="font-display font-bold text-brand-amber mb-1">
                Couldn't reach the server
              </p>
              <p className="font-mono text-xs text-text-secondary">
                Your answers could not be submitted for grading. The scores
                shown here are placeholders — no OA result was recorded and no
                repair mission was started. Please check your connection and
                retry the attempt.
              </p>
            </div>
          )}
          {/* Header */}
          <motion.div
            className="card mb-8 text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <span className="section-subheader mb-4 block">
              {unreachable
                ? "Submission Interrupted"
                : "Assessment Complete"}
            </span>
            <div className="flex justify-center mb-6">
              <ScoreRing
                percentage={pct}
                tone={unreachable ? "neutral" : undefined}
              />
            </div>
              <div className="flex items-center justify-center gap-6 mb-4">
              <div className="text-center">
                <p className="font-display font-black text-2xl text-emerald-600">
                  {correctCount}
                </p>
                <p className="font-mono text-[10px] text-text-secondary uppercase">
                  Correct
                </p>
              </div>
              <div className="w-px h-8 bg-brand-primary/10" />
              <div className="text-center">
                <p className="font-display font-black text-2xl text-brand-coral">
                  {wrongCount}
                </p>
                <p className="font-mono text-[10px] text-text-secondary uppercase">
                  Wrong
                </p>
              </div>
              <div className="w-px h-8 bg-brand-primary/10" />
              <div className="text-center">
                <p className="font-display font-black text-2xl text-text-muted">
                  {unattemptedCount}
                </p>
                <p className="font-mono text-[10px] text-text-secondary uppercase">
                  Unattempted
                </p>
              </div>
              <div className="w-px h-8 bg-brand-primary/10" />
              <div className="text-center">
                <p className="font-display font-black text-2xl text-brand-sky">
                  {formatTime(result.timeTaken)}
                </p>
                <p className="font-mono text-[10px] text-text-secondary uppercase">
                  Time Taken
                </p>
              </div>
              {result.tabViolations > 0 && (
                <>
                  <div className="w-px h-8 bg-brand-primary/10" />
                  <div className="text-center">
                    <p className="font-display font-black text-2xl text-brand-amber">
                      {result.tabViolations}
                    </p>
                    <p className="font-mono text-[10px] text-text-secondary uppercase">
                      Tab Violations
                    </p>
                  </div>
                </>
              )}
            </div>
            <p className="font-mono text-xs text-text-secondary">
              {company.name} Mock OA — {total} Questions
            </p>

            {!unreachable && pct >= 80 && (
              <motion.p
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 text-sm text-emerald-700"
              >
                You demonstrated competence across the full assessment. Use the weakness diagnosis only to refine edges, not to rebuild fundamentals.
              </motion.p>
            )}
            {!unreachable && pct >= 60 && pct < 80 && (
              <motion.p
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 text-sm text-amber-700"
              >
                Your baseline is solid. The gaps above are specific, fixable weaknesses — not a signal to start over.
              </motion.p>
            )}
            {!unreachable && pct < 60 && (
              <motion.p
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 text-sm text-brand-coral"
              >
                This assessment exposed structural gaps. Follow the repair path in order; each step targets one misconception.
              </motion.p>
            )}
          </motion.div>

          {/* Section Breakdown — hidden on transport-failure fallback: 0%
              is meaningless when answers never reached the server. */}
          {!unreachable && (
          <motion.div
            className="mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h2 className="section-header text-lg mb-4 flex items-center gap-2">
              <BarChart3 size={20} className="text-brand-primary" />
              Section Breakdown
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {company.sections.map((sectionName) => {
                const stats = getSectionStats(sectionName);
                const secPct =
                  stats.total > 0
                    ? Math.round((stats.correct / stats.total) * 100)
                    : 0;
                return (
                  <div key={sectionName} className="card">
                    <h3 className="font-display font-bold text-text-primary text-sm mb-3">
                      {sectionName}
                    </h3>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-mono text-2xl font-black text-brand-sky">
                        {secPct}%
                      </span>
                      <span className="font-mono text-xs text-text-secondary">
                        {stats.correct}/{stats.total}
                      </span>
                    </div>
                    <div className="mb-3 h-1.5 w-full rounded-full border border-black/5 bg-surface-2">
                      <div
                        className={`h-1.5 rounded-full transition-all duration-1000 ${
                          secPct >= 70
                            ? "bg-emerald-500"
                            : secPct >= 40
                            ? "bg-amber-500"
                            : "bg-red-500"
                        }`}
                        style={{ width: `${secPct}%` }}
                      />
                    </div>
                    <div className="flex gap-3 text-[10px] font-mono">
                      <span className="text-emerald-600">
                        ✓ {stats.correct}
                      </span>
                      <span className="text-red-500">✗ {stats.wrong}</span>
                      <span className="text-text-muted">
                        — {stats.unattempted}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
          )}

          {/* Weakness Diagnosis — the actionable repair path produced by the
              backend competence diagnosis. Hidden when no weak skill exists. */}
          {skills.length > 0 && (
            <motion.div
              className="mb-8"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.13 }}
            >
              <h2 className="section-header text-lg mb-4 flex items-center gap-2">
                <Target size={20} className="text-brand-coral" />
                Weakness Diagnosis
              </h2>
              <div className="card p-5">
                {primary && (
                  <p className="mb-4 flex items-center gap-2 font-display font-bold text-sm">
                    <AlertTriangle
                      size={16}
                      className="text-brand-amber shrink-0"
                    />
                    Primary weakness:
                    <span className="text-brand-coral capitalize">
                      {primary}
                    </span>
                  </p>
                )}
                <p className="text-xs text-text-secondary mb-4">
                  These gaps are specific to this assessment. Repair them with targeted practice, not broad review.
                </p>
                <div className="grid sm:grid-cols-3 gap-4 mb-4">
                  {skills.map((w) => (
                    <div
                      key={w.skill}
                      className="rounded-xl border border-black/5 bg-surface-2 p-3"
                    >
                      <p className="font-display font-bold text-text-primary text-sm mb-1 capitalize">
                        {w.skill}
                      </p>
                      <div className="flex items-center justify-between">
                        <span
                           className={`font-mono text-xl font-black ${
                             w.pct < 40
                               ? "text-brand-coral"
                               : "text-brand-amber"
                           }`}
                        >
                          {Math.round(w.pct)}%
                        </span>
                        <span className="font-mono text-xs text-gray-500">
                          {w.correct}/{w.total} correct
                        </span>
                      </div>
                      <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-[10px]">
                           {Number(w.slow_count) > 0 && (
                           <span className="rounded bg-amber-50 px-1.5 py-0.5 text-amber-600">
                             {w.slow_count} slow
                           </span>
                         )}
                        <span className="rounded bg-black/10 px-1.5 py-0.5 text-text-muted">
                          ~{Math.round(Number(w.avg_time_s))}s avg
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
                {(chain.length > 0 || retestCond) && (
                  <div className="space-y-3 border-t border-black/5 pt-4">
                    {chain.length > 0 && (
                      <div>
                        <p className="mb-2 font-mono text-[10px] text-text-muted uppercase tracking-wide">
                          Repair Path
                        </p>
                        <ol className="space-y-1">
                          {chain.map((step, i) => (
                            <li
                              key={i}
                              className="flex items-center gap-2 font-mono text-xs text-gray-300"
                            >
                               <span className="flex h-4 w-4 shrink-0 items-center justify-center rounded bg-brand-primary/10 text-[10px] font-bold text-brand-sky">
                                 {i + 1}
                               </span>
                              {step}
                            </li>
                          ))}
                        </ol>
                      </div>
                    )}
                    {retestCond && (
                      <p className="font-mono text-[10px] text-gray-500">
                         Retest condition:{" "}
                         <span className="text-emerald-600">
                           {retestCond}
                         </span>
                      </p>
                    )}
                    <div className="pt-1">
                      <button
                        onClick={() =>
                          document
                            .getElementById("repair-missions")
                            ?.scrollIntoView({
                              behavior: "smooth",
                              block: "start",
                            })
                        }
                        className="inline-flex items-center gap-2 rounded-full bg-brand-sky px-4 py-2 text-xs font-bold text-white shadow-sm hover:bg-brand-sky/90 transition-colors"
                      >
                        Focus &amp; Retest <ArrowRight size={14} />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {/* Repair Missions — closed-loop return path. Never shown on a
              transport-failure fallback: no grade was recorded, so there is
              nothing to repair. */}
          {!unreachable && (
            <div id="repair-missions">
              <RepairPanel />
            </div>
          )}

          {/* Question Review Toggle — hidden on transport-failure fallback;
              per-question correctness is unknown because no scorecard exists. */}
          {!unreachable && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="section-header text-lg flex items-center gap-2">
                <Target size={20} className="text-brand-sky" />
                Question Review
              </h2>
              <button
                onClick={() => setReviewMode(!reviewMode)}
                className="btn-ghost text-xs"
              >
                {reviewMode ? "Hide Details" : "Show All Details"}
              </button>
            </div>

            <div className="space-y-3">
              {questions.map((q, i) => {
                const sub = submittedAnswers[i];
                const wasCorrect = sub?.is_correct;
                const userAns = answers[i];
                const isExpanded = reviewMode || showExplanation[i];

                return (
                  <motion.div
                    key={i}
                    className={`card ${
                      wasCorrect
                        ? "border-emerald-200"
                        : sub
                        ? "border-red-200"
                        : "border-black/5"
                    }`}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: Math.min(i * 0.02, 0.5) }}
                  >
                    <div
                      className="flex items-start justify-between cursor-pointer"
                      onClick={() =>
                        setShowExplanation((prev) => ({
                          ...prev,
                          [i]: !prev[i],
                        }))
                      }
                    >
                      <div className="flex items-start gap-3 flex-1 min-w-0">
                        <span className="font-mono text-xs text-gray-500 shrink-0 mt-0.5">
                          Q{i + 1}.
                        </span>
                        <p className="font-display text-text-primary text-sm leading-relaxed line-clamp-2">
                          {q.question}
                        </p>
                      </div>
                      <div className="flex items-center gap-2 shrink-0 ml-3">
                        {sub ? (
                          wasCorrect ? (
                            <CheckCircle
                              size={18}
                              className="text-cyber-green"
                            />
                          ) : (
                            <XCircle size={18} className="text-cyber-red" />
                          )
                        ) : (
                          <span className="rounded bg-surface-2 px-2 py-0.5 font-mono text-[10px] text-text-muted">
                            Skipped
                          </span>
                        )}
                        <ChevronRight
                          size={14}
                          className={`text-gray-600 transition-transform ${
                            isExpanded ? "rotate-90" : ""
                          }`}
                        />
                      </div>
                    </div>

                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="overflow-hidden"
                        >
                          <div className="mt-4 space-y-2 border-t border-black/5 pt-4">
                            {q.options.map((opt, oi) => {
                              const isUserAnswer = userAns === oi;
                              const isCorrectAns =
                                sub?.correct_answer === oi;
                               let ringClass = "border-black/5 ";
                               if (isCorrectAns)
                                 ringClass += "border-emerald-200 bg-emerald-50 ";
                               if (isUserAnswer && !wasCorrect && !isCorrectAns)
                                 ringClass += "border-red-200 bg-red-50 ";

                               return (
                                 <div
                                   key={oi}
                                   className={`flex items-start gap-2 p-2.5 rounded-lg border text-xs font-mono ${ringClass}`}
                                 >
                                   <span className="text-brand-sky font-bold shrink-0">
                                     {String.fromCharCode(65 + oi)}.
                                   </span>
                                   <span className="text-text-secondary flex-1">
                                     {opt}
                                   </span>
                                   <span className="shrink-0 flex items-center gap-1">
                                     {isCorrectAns && (
                                       <span className="text-emerald-600 text-[10px]">
                                         ✓ Correct
                                       </span>
                                     )}
                                     {isUserAnswer && !isCorrectAns && (
                                       <span className="text-red-500 text-[10px]">
                                           ✗ Your answer
                                         </span>
                                     )}
                                     {isUserAnswer && isCorrectAns && (
                                       <span className="text-emerald-600 text-[10px]">
                                         ✓ Your answer
                                       </span>
                                     )}
                                   </span>
                                 </div>
                               );
                            })}
                             {sub?.explanation && (
                               <p className="text-[11px] font-mono text-text-secondary mt-2 leading-relaxed">
                                 <span className="text-brand-sky font-bold">
                                   Explanation:
                                 </span>{" "}
                                 {sub.explanation}
                               </p>
                             )}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
          )}

          <Link
            to={{ pathname: "/exam-memory/submit", search: `?exam=${OA_TO_MEMORY_EXAM[company.id] || "other"}` }}
            className="block rounded-3xl px-6 py-5 mt-10 text-center font-display font-black text-base sm:text-lg text-space-void transition-all duration-200 hover:scale-[1.015] hover:shadow-lg"
            style={{ backgroundColor: "#D4A843", color: "#0a0a0a" }}
          >
            <span className="flex items-center justify-center gap-3">
              <Database size={20} /> Just took the real {company.name}? Report what you remember
            </span>
            <span className="block font-mono text-[10px] font-normal mt-1 opacity-70 tracking-wide">
              Your recollections help build the verified question bank for future test-takers
            </span>
          </Link>

          {/* Action Buttons */}
          <motion.div
            className="flex gap-4 mt-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <button
              onClick={() => {
                setStep("select");
                setResult(null);
                setQuestions([]);
                setAnswers({});
                setSubmittedAnswers({});
                setShowExplanation({});
              }}
              className="flex-1 btn-primary text-center flex items-center justify-center gap-2"
            >
              <Zap size={16} /> Try Again
            </button>
            <Link
              to="/aptitude"
              className="flex-1 btn-secondary text-center flex items-center justify-center gap-2"
            >
              <Brain size={16} /> Aptitude Test
            </Link>
            <Link
              to="/dashboard"
              className="flex-1 btn-secondary text-center flex items-center justify-center gap-2"
            >
              <Trophy size={16} /> Dashboard
            </Link>
          </motion.div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-3">
      <Spinner size="lg" />
      {resultLoading && (
        <p className="font-mono text-xs text-text-muted">
          Finalizing assessment — grading answers &amp; diagnosing weaknesses…
        </p>
      )}
    </div>
  );
}
