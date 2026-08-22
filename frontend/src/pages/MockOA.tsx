import { useState, useEffect, useRef, useCallback, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import CelebrationOverlay from "../components/CelebrationOverlay";
import {
  Clock,
  CheckCircle,
  XCircle,
  ArrowRight,
  ArrowLeft,
  FileText,
  Shield,
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
} from "lucide-react";

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

const DURATION_OPTIONS = [
  { value: 30, label: "30 min" },
  { value: 45, label: "45 min" },
  { value: 60, label: "60 min" },
];

function CountdownTimer({ totalSeconds, onTimeUp, isActive }) {
  const [remaining, setRemaining] = useState(totalSeconds);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (!isActive) return;
    setRemaining(totalSeconds);
  }, [totalSeconds, isActive]);

  useEffect(() => {
    if (!isActive || remaining <= 0) return;
    intervalRef.current = setInterval(() => {
      setRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(intervalRef.current);
          onTimeUp();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(intervalRef.current);
  }, [isActive, onTimeUp, remaining > 0]);

  const minutes = Math.floor(remaining / 60);
  const seconds = remaining % 60;
  const pct = (remaining / totalSeconds) * 100;
  const urgency =
    remaining <= 300 ? "critical" : remaining <= 900 ? "warning" : "normal";

  const colors = {
    normal: { text: "text-text-primary", ring: "#4CC9F0", bg: "rgba(76,201,240,0.1)" },
    warning: { text: "text-cyber-amber", ring: "#F59E0B", bg: "rgba(245,158,11,0.1)" },
    critical: { text: "text-cyber-red", ring: "#EF4444", bg: "rgba(239,68,68,0.1)" },
  };
  const c = colors[urgency];

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative w-32 h-32">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
          <circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke="rgba(255,255,255,0.05)"
            strokeWidth="6"
          />
          <circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke={c.ring}
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={339.292}
            strokeDashoffset={339.292 * (1 - pct / 100)}
            className="transition-all duration-1000"
            style={{
              filter: `drop-shadow(0 0 6px ${c.ring})`,
            }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`font-display font-black text-2xl ${c.text} leading-none`}>
            {String(minutes).padStart(2, "0")}
          </span>
          <span className={`font-mono text-xs ${c.text} opacity-60`}>:</span>
          <span className={`font-display font-black text-2xl ${c.text} leading-none`}>
            {String(seconds).padStart(2, "0")}
          </span>
        </div>
      </div>
      <div className="text-center">
        <p className={`font-mono text-xs uppercase tracking-widest ${
          urgency === "critical"
            ? "text-cyber-red animate-pulse"
            : urgency === "warning"
            ? "text-cyber-amber"
            : "text-gray-500"
        }`}>
          {urgency === "critical" ? "Time Running Out!" : "Time Remaining"}
        </p>
      </div>
    </div>
  );
}

function QuestionPalette({
  total,
  current,
  answers,
  submittedAnswers,
  onNavigate,
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
            btnClass += "bg-cyber-blue text-space-void border-cyber-blue shadow-cyber-blue scale-110";
          } else if (isSubmitted && isCorrect) {
            btnClass += "bg-cyber-green/20 text-cyber-green border-cyber-green/40";
          } else if (isSubmitted && !isCorrect) {
            btnClass += "bg-cyber-red/20 text-cyber-red border-cyber-red/40";
          } else if (isAnswered) {
            btnClass += "bg-cyber-amber/20 text-cyber-amber border-cyber-amber/40";
          } else {
            btnClass += "bg-white text-text-muted border-black/5 hover:border-gray-500 hover:text-text-primary";
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
          <div className="w-3 h-3 rounded bg-cyber-blue" />
          <span className="font-mono text-[10px] text-gray-500">Current</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-cyber-green/40" />
          <span className="font-mono text-[10px] text-gray-500">Correct</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-cyber-red/40" />
          <span className="font-mono text-[10px] text-gray-500">Wrong</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-cyber-amber/40" />
          <span className="font-mono text-[10px] text-gray-500">Answered</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-3 w-3 rounded border border-black/5 bg-black/5" />
          <span className="font-mono text-[10px] text-gray-500">Unattempted</span>
        </div>
      </div>
    </div>
  );
}

function ScoreRing({ percentage, size = 180 }) {
  const r = (size - 16) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - percentage / 100);
  const color =
    percentage >= 80
      ? "#4BB543"
      : percentage >= 50
      ? "#F59E0B"
      : "#EF4444";

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
          {percentage}%
        </span>
        <span className="font-mono text-xs text-gray-500 mt-1">
          {percentage >= 80
            ? "ELITE"
            : percentage >= 60
            ? "GOOD"
            : percentage >= 40
            ? "AVERAGE"
            : "NEEDS WORK"}
        </span>
      </div>
    </div>
  );
}

export default function MockOA() {
  const [step, setStep] = useState("select");
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [customDuration, setCustomDuration] = useState(45);
  const [testId, setTestId] = useState("");
  const [questions, setQuestions] = useState([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submittedAnswers, setSubmittedAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [timeTaken, setTimeTaken] = useState(0);
  const [startTime, setStartTime] = useState(null);
  const [showCelebration, setShowCelebration] = useState(false);
  const [currentSection, setCurrentSection] = useState("");
  const [reviewMode, setReviewMode] = useState(false);
  const [showExplanation, setShowExplanation] = useState({});
  const timerRef = useRef(null);

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
      submitTest();
    }
  }, [step, testId, timeTaken]);

  const startTest = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.startAptitudeTest(
        "mixed",
        company.difficulty,
        company.questionCount
      );
      setTestId(data.test_id);
      setQuestions(data.questions);
      setCurrentQ(0);
      setAnswers({});
      setSubmittedAnswers({});
      setShowExplanation({});
      setStartTime(Date.now());
      setTimeTaken(0);
      setReviewMode(false);
      setResult(null);
      setStep("test");
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const submitAnswer = async (answer) => {
    if (submittedAnswers[currentQ] !== undefined) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.submitAptitudeAnswer(testId, currentQ, answer);
      setAnswers((prev) => ({ ...prev, [currentQ]: answer }));
      setSubmittedAnswers((prev) => ({ ...prev, [currentQ]: data }));
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const submitTest = async () => {
    setLoading(true);
    try {
      const answersArray = questions.map((_, i) => answers[i] ?? null);
      const data = await api.completeAptitudeTest(testId, timeTaken);
      setResult({
        ...data,
        answers: submittedAnswers,
        timeTaken,
      });
      setStep("results");
      if (data.percentage >= 70) {
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 3000);
      }
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const navigateQuestion = (idx) => {
    if (idx >= 0 && idx < questions.length) setCurrentQ(idx);
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
              Company Assessment Simulator
            </span>
            <h1 className="section-header text-3xl mb-2">
              <FileText className="text-cyber-blue inline mr-2" size={28} />
              Mock <span className="text-cyber-blue">Online Assessment</span>
            </h1>
            <p className="text-gray-500 font-mono text-sm max-w-lg mx-auto">
              Simulate real company OAs — timed sections, MCQ aptitude, instant
              results. Train like it's placement day.
            </p>
          </motion.div>

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
                      className="rounded border border-black/5 bg-black/5 px-2 py-0.5 text-[10px] font-mono text-text-muted"
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
    const sectionSize = Math.ceil(questions.length / company.sections.length);
    const sectionIdx = Math.min(
      Math.floor(currentQ / sectionSize),
      company.sections.length - 1
    );
    const sectionStart = sectionIdx * sectionSize;
    const sectionEnd = Math.min(sectionStart + sectionSize, questions.length);

    return (
      <div className="min-h-screen">
        {/* ── Top Section Bar ── */}
        <div className="sticky top-0 z-30 border-b border-black/5 bg-white/95 backdrop-blur">
          <div className="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="font-display font-bold text-text-primary text-sm flex items-center gap-2">
                <span className="text-lg">{company.logo}</span>
                {company.name}
              </span>
              <span className="w-px h-4 bg-space-border" />
              <span className="font-mono text-xs text-cyber-blue">
                {currentSection}
              </span>
              <span className="font-mono text-[10px] text-gray-500">
                Q{currentQ + 1}–{sectionEnd} of {questions.length}
              </span>
            </div>
            <div className="flex items-center gap-3">
              <span className="font-mono text-xs text-gray-500">
                {answeredCount}/{questions.length} answered
              </span>
              <CountdownTimer
                totalSeconds={customDuration * 60}
                onTimeUp={handleTimeUp}
                isActive={step === "test"}
              />
            </div>
          </div>
          {/* Section Progress Bar */}
          <div className="h-1 bg-black/5">
            <div
              className="h-full bg-gradient-to-r from-cyber-blue to-cyber-purple transition-all duration-300"
              style={{
                width: `${((currentQ + 1) / questions.length) * 100}%`,
              }}
            />
          </div>
        </div>

        {/* ── Main Content ── */}
        <div className="max-w-7xl mx-auto px-4 py-6 flex gap-6">
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
                        <span className="ml-2 text-cyber-blue">
                          [{q.category}]
                        </span>
                      )}
                    </span>
                    {submittedAnswers[currentQ] && (
                      <span
                        className={`font-mono text-[10px] px-2 py-0.5 rounded-full ${
                          submittedAnswers[currentQ].is_correct
                            ? "bg-cyber-green/10 text-cyber-green border border-cyber-green/20"
                            : "bg-cyber-red/10 text-cyber-red border border-cyber-red/20"
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
                          "border-black/5 bg-white/70 text-text-muted cursor-not-allowed";
                      }
                    } else if (isSelected) {
                      optClass +=
                        "border-cyber-blue bg-cyber-blue/10 text-text-primary shadow-cyber-blue";
                    } else {
                      optClass +=
                        "border-black/5 hover:border-gray-500 text-text-muted hover:text-text-primary hover:bg-black/5 cursor-pointer";
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
                    onClick={() => navigateQuestion(currentQ - 1)}
                    disabled={currentQ === 0}
                    className="btn-ghost flex items-center gap-1 disabled:opacity-30"
                  >
                    <ArrowLeft size={16} /> Previous
                  </button>
                  <div className="flex items-center gap-3">
                    {currentQ < questions.length - 1 ? (
                      <button
                        onClick={() => navigateQuestion(currentQ + 1)}
                        className="btn-secondary flex items-center gap-1"
                      >
                        Next <ChevronRight size={16} />
                      </button>
                    ) : (
                      <button
                        onClick={submitTest}
                        disabled={loading}
                        className="btn-primary flex items-center gap-2"
                      >
                        {loading ? (
                          <Spinner size="sm" className="text-space-void" />
                        ) : (
                          <>
                            Submit OA <ArrowRight size={16} />
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
                  onClick={submitTest}
                  disabled={loading}
                  className="btn-primary w-full flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <Spinner size="sm" className="text-space-void" />
                  ) : (
                    <>
                      Submit OA <ArrowRight size={16} />
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
                      submitTest();
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
    const pct = result.percentage || 0;

    return (
      <div className="page-surface min-h-screen py-6 px-4">
        <CelebrationOverlay
          show={showCelebration}
          type="perfect"
          message="OA Destroyed!"
        />
        <div className="max-w-5xl mx-auto">
          {/* Header */}
          <motion.div
            className="card mb-8 text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <span className="section-subheader mb-4 block">
              Assessment Complete
            </span>
            <div className="flex justify-center mb-6">
              <ScoreRing percentage={pct} />
            </div>
            <div className="flex items-center justify-center gap-6 mb-4">
              <div className="text-center">
                <p className="font-display font-black text-2xl text-cyber-green">
                  {correctCount}
                </p>
                <p className="font-mono text-[10px] text-gray-500 uppercase">
                  Correct
                </p>
              </div>
              <div className="w-px h-8 bg-space-border" />
              <div className="text-center">
                <p className="font-display font-black text-2xl text-cyber-red">
                  {wrongCount}
                </p>
                <p className="font-mono text-[10px] text-gray-500 uppercase">
                  Wrong
                </p>
              </div>
              <div className="w-px h-8 bg-space-border" />
              <div className="text-center">
                <p className="font-display font-black text-2xl text-gray-400">
                  {unattemptedCount}
                </p>
                <p className="font-mono text-[10px] text-gray-500 uppercase">
                  Unattempted
                </p>
              </div>
              <div className="w-px h-8 bg-space-border" />
              <div className="text-center">
                <p className="font-display font-black text-2xl text-cyber-blue">
                  {formatTime(result.timeTaken)}
                </p>
                <p className="font-mono text-[10px] text-gray-500 uppercase">
                  Time Taken
                </p>
              </div>
            </div>
            <p className="font-mono text-xs text-gray-500">
              {company.name} Mock OA — {total} Questions
            </p>
          </motion.div>

          {/* Section Breakdown */}
          <motion.div
            className="mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h2 className="section-header text-lg mb-4 flex items-center gap-2">
              <BarChart3 size={20} className="text-cyber-purple" />
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
                      <span className="font-mono text-2xl font-black text-cyber-blue">
                        {secPct}%
                      </span>
                      <span className="font-mono text-xs text-gray-500">
                        {stats.correct}/{stats.total}
                      </span>
                    </div>
                    <div className="mb-3 h-1.5 w-full rounded-full border border-black/5 bg-black/5">
                      <div
                        className={`h-1.5 rounded-full transition-all duration-1000 ${
                          secPct >= 70
                            ? "bg-cyber-green"
                            : secPct >= 40
                            ? "bg-cyber-amber"
                            : "bg-cyber-red"
                        }`}
                        style={{ width: `${secPct}%` }}
                      />
                    </div>
                    <div className="flex gap-3 text-[10px] font-mono">
                      <span className="text-cyber-green">
                        ✓ {stats.correct}
                      </span>
                      <span className="text-cyber-red">✗ {stats.wrong}</span>
                      <span className="text-gray-500">
                        — {stats.unattempted}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>

          {/* Question Review Toggle */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="section-header text-lg flex items-center gap-2">
                <Target size={20} className="text-cyber-blue" />
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
                        ? "border-cyber-green/15"
                        : sub
                        ? "border-cyber-red/15"
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
                          <span className="rounded bg-black/5 px-2 py-0.5 font-mono text-[10px] text-text-muted">
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
                                ringClass += "border-cyber-green/40 bg-cyber-green/5 ";
                              if (isUserAnswer && !wasCorrect && !isCorrectAns)
                                ringClass += "border-cyber-red/40 bg-cyber-red/5 ";

                              return (
                                <div
                                  key={oi}
                                  className={`flex items-start gap-2 p-2.5 rounded-lg border text-xs font-mono ${ringClass}`}
                                >
                                  <span className="text-cyber-blue font-bold shrink-0">
                                    {String.fromCharCode(65 + oi)}.
                                  </span>
                                  <span className="text-gray-300 flex-1">
                                    {opt}
                                  </span>
                                  <span className="shrink-0 flex items-center gap-1">
                                    {isCorrectAns && (
                                      <span className="text-cyber-green text-[10px]">
                                        ✓ Correct
                                      </span>
                                    )}
                                    {isUserAnswer && !isCorrectAns && (
                                      <span className="text-cyber-red text-[10px]">
                                        ✗ Your answer
                                      </span>
                                    )}
                                    {isUserAnswer && isCorrectAns && (
                                      <span className="text-cyber-green text-[10px]">
                                        ✓ Your answer
                                      </span>
                                    )}
                                  </span>
                                </div>
                              );
                            })}
                            {sub?.explanation && (
                              <p className="text-[11px] font-mono text-gray-500 mt-2 leading-relaxed">
                                <span className="text-cyber-blue font-bold">
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

          {/* Action Buttons */}
          <motion.div
            className="flex gap-4 mt-10"
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
    <div className="min-h-screen flex items-center justify-center">
      <Spinner size="lg" />
    </div>
  );
}
