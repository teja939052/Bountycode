import os

content = '''import { useState, useEffect, useRef, useCallback, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { oaApi } from "../services/api/oa";
import Spinner from "../components/ui/Spinner";

const COMPANIES = [
  { id: "tcs", name: "TCS", logo: "\\u2657", duration: 60, questionCount: 20, difficulty: "medium", sections: ["aptitude", "logical", "verbal"], color: "cyber-blue" },
  { id: "infosys", name: "Infosys", logo: "\\u2659", duration: 45, questionCount: 15, difficulty: "medium", sections: ["aptitude", "logical", "verbal"], color: "cyber-purple" },
  { id: "wipro", name: "Wipro", logo: "\\ud83d\\udc8e", duration: 45, questionCount: 20, difficulty: "medium", sections: ["aptitude", "logical", "verbal", "coding"], color: "cyber-green" },
  { id: "cognizant", name: "Cognizant", logo: "\\ud83d\\udc76", duration: 30, questionCount: 15, difficulty: "medium", sections: ["aptitude", "logical", "verbal"], color: "cyber-amber" },
  { id: "google", name: "Google", logo: "\\ud83d\\udc8e", duration: 60, questionCount: 15, difficulty: "hard", sections: ["coding", "dsa", "cs_fundamentals"], color: "cyber-blue" },
];

const DURATION_OPTIONS = [
  { value: 30, label: "30 min" },
  { value: 45, label: "45 min" },
  { value: 60, label: "60 min" },
];

export default function MockOA() {
  const [step, setStep] = useState("select");
  const [selectedCompany, setSelectedCompany] = useState<string | null>(null);
  const [customDuration, setCustomDuration] = useState(45);
  const [testId, setTestId] = useState("");
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [submittedAnswers, setSubmittedAnswers] = useState<Record<number, any>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);
  const [timeTaken, setTimeTaken] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [showCelebration, setShowCelebration] = useState(false);
  const [currentSection, setCurrentSection] = useState("");
  const [reviewMode, setReviewMode] = useState(false);
  const [showExplanation, setShowExplanation] = useState<Record<number, boolean>>({});
  const timerRef = useRef<number | null>(null);

  const company = useMemo(() => COMPANIES.find((c) => c.id === selectedCompany) || COMPANIES[0], [selectedCompany]);

  useEffect(() => {
    let interval: number;
    if (step === "test" && startTime) {
      interval = setInterval(() => setTimeTaken(Math.floor((Date.now() - startTime) / 1000)), 1000);
    }
    return () => clearInterval(interval);
  }, [step, startTime]);

  const startTest = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await oaApi.start({
        company: selectedCompany || "tcs",
        role: "swe",
        total_questions: company.questionCount,
        duration_minutes: customDuration,
        mode: "calm",
        integrity: true,
        verified_only: true,
      });
      setTestId(data.session_id);
      setQuestions(data.questions || []);
      setCurrentQ(0);
      setAnswers({});
      setSubmittedAnswers({});
      setStartTime(Date.now());
      setTimeTaken(0);
      setReviewMode(false);
      setResult(null);
      setStep("test");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start assessment");
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async (answer: string) => {
    if (submittedAnswers[currentQ] !== undefined) return;
    setLoading(true);
    setError("");
    try {
      await oaApi.submitAnswer(testId, [{
        question_uid: questions[currentQ].question_uid || "q_" + currentQ,
        answer,
        time_taken: timeTaken,
      }]);
      setAnswers((prev) => ({ ...prev, [currentQ]: answer }));
      setSubmittedAnswers((prev) => ({ ...prev, [currentQ]: answer }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit answer");
    } finally {
      setLoading(false);
    }
  };

  const submitTest = async () => {
    setLoading(true);
    try {
      const data = await oaApi.complete(testId);
      setResult({ ...data, answers: submittedAnswers, timeTaken });
      setStep("results");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit assessment");
    } finally {
      setLoading(false);
    }
  };

  const navigateQuestion = (idx: number) => {
    if (idx >= 0 && idx < questions.length) setCurrentQ(idx);
  };

  const formatTime = (s: number) => Math.floor(s / 60) + ":" + (s % 60).toString().padStart(2, "0");

  const answeredCount = Object.keys(submittedAnswers).length;
  const correctCount = Object.values(submittedAnswers).filter((a: any) => a.is_correct).length;
  const wrongCount = answeredCount - correctCount;
  const unattemptedCount = questions.length - answeredCount;

  const getSectionStats = (sectionName: string) => {
    const cat: any = SECTION_CATEGORIES[sectionName as keyof typeof SECTION_CATEGORIES];
    if (!cat) return { total: 0, correct: 0, wrong: 0, unattempted: 0 };
    const sectionQs = questions.map((q, i) => ({ q, i })).filter(({ q }) => q.category === cat || q.category === sectionName.toLowerCase());
    const total = sectionQs.length;
    const correct = sectionQs.filter(({ i }) => submittedAnswers[i]?.is_correct).length;
    const answered = sectionQs.filter(({ i }) => submittedAnswers[i] !== undefined).length;
    return { total, correct, wrong: answered - correct, unattempted: total - answered };
  };

  if (step === "select") {
    return (
      <div className="page-surface min-h-screen py-6 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-10">
            <span className="section-subheader mb-3 block">Company Assessment Simulator</span>
            <h1 className="section-header text-3xl mb-2">
              <span className="mr-2">{company.logo}</span>{company.name} — Mock OA
            </h1>
            <p className="text-gray-500 font-mono text-sm max-w-lg mx-auto">Simulate real company OAs — timed sections, MCQ aptitude, instant results. Train like it's placement day.</p>
          </div>
          {error && (
            <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">{error}</div>
          )}
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
            {COMPANIES.map((c, i) => (
              <motion.button
                key={c.id}
                onClick={() => { setSelectedCompany(c.id); setCustomDuration(c.duration); }}
                className={"card text-left transition-all border-2 " + (selectedCompany === c.id ? "border-" + c.color + " bg-" + c.color + "/10" : "border-transparent hover:border-black/5")}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
                style={selectedCompany === c.id ? { borderColor: "var(--tw-" + c.color + "-border, rgba(76,201,240,0.5))", backgroundColor: "rgba(76,201,240,0.06)" } : {}}
              >
                <div className="flex items-center gap-2.5 mb-3">
                  <span className="text-3xl">{c.logo}</span>
                  <div>
                    <h3 className="font-display font-bold text-text-primary text-sm">{c.name}</h3>
                    <p className="text-[10px] font-mono text-gray-500">{c.description}</p>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2 mb-3">
                  {c.sections.map((s) => (
                    <span key={s} className="rounded border border-black/5 bg-surface-2 px-2 py-0.5 text-[10px] font-mono text-text-muted">{s}</span>
                  ))}
                </div>
                <div className="flex items-center justify-between text-[10px] font-mono text-gray-500">
                  <span className="flex items-center gap-1"><Clock size={10} /> {c.duration} min</span>
                  <span>{c.questionCount} Qs</span>
                  <span className="capitalize">{c.difficulty}</span>
                </div>
              </motion.button>
            ))}
          </div>
          {selectedCompany && (
            <motion.div className="card" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                  <h3 className="font-display font-bold text-text-primary text-sm mb-1"><span className="mr-2">{company.logo}</span>{company.name} — Mock OA</h3>
                  <p className="text-xs font-mono text-gray-500">{company.questionCount} questions across {company.sections.length} sections</p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <Clock size={14} className="text-gray-500" />
                    <select value={customDuration} onChange={(e) => setCustomDuration(Number(e.target.value))} className="rounded-lg border border-black/5 bg-white px-3 py-2 font-mono text-xs text-text-secondary focus:border-cyber-blue/50 focus:outline-none">
                      {DURATION_OPTIONS.map((d) => (
                        <option key={d.value} value={d.value}>{d.label}</option>
                      ))}
                    </select>
                  </div>
                  <button onClick={startTest} disabled={loading} className="btn-primary flex items-center gap-2">
                    {loading ? <Spinner size="sm" className="text-space-void" /> : <><span>Start Mock OA</span> <ArrowRight size={16} /></>}
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    );
  }

  if (step === "test" && questions.length > 0) {
    const q = questions[currentQ];
    const sectionSize = Math.ceil(questions.length / company.sections.length);
    const sectionIdx = Math.min(Math.floor(currentQ / sectionSize), company.sections.length - 1);
    const sectionStart = sectionIdx * sectionSize;
    const sectionEnd = Math.min(sectionStart + sectionSize, questions.length);

    return (
      <div className="min-h-screen">
        <div className="sticky top-0 z-30 border-b border-black/5 bg-white border-border/95 backdrop-blur">
          <div className="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="font-display font-bold text-text-primary text-sm flex items-center gap-2"><span className="text-lg">{company.logo}</span>{company.name}</span>
              <span className="w-px h-4 bg-space-border" />
              <span className="font-mono text-xs text-cyber-blue">{currentSection}</span>
              <span className="font-mono text-[10px] text-gray-500">Q{currentQ + 1}–{sectionEnd} of {questions.length}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="font-mono text-xs text-gray-500">{answeredCount}/{questions.length} answered</span>
              <CountdownTimer totalSeconds={customDuration * 60} onTimeUp={handleTimeUp} isActive={step === "test"} />
            </div>
          </div>
          <div className="h-1 bg-surface-2">
            <div className="h-full bg-gradient-to-r from-cyber-blue to-cyber-purple transition-all duration-300" style={{ width: ((currentQ + 1) / questions.length) * 100 + "%" }} />
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-4 py-6 flex gap-6">
          <div className="flex-1 min-w-0">
            <div className="card mb-4">
              <div className="flex items-start justify-between mb-1">
                <span className="font-mono text-[10px] text-gray-600 uppercase tracking-wider">Question {currentQ + 1} of {questions.length}</span>
                {q.category && (
                  <span className="ml-2 text-cyber-blue">[{q.category}]</span>
                )}
              </span>
              <p className="font-display font-bold text-text-primary text-lg leading-relaxed mt-3">{q.question}</p>
            </div>
            <div className="space-y-2.5 mb-6">
              {q.options.map((option: string, oi: number) => {
                const isSelected = answers[currentQ] === oi;
                const isSubmitted = submittedAnswers[currentQ] !== undefined;
                const isCorrectOption = isSubmitted && submittedAnswers[currentQ].correct_answer === oi;
                const isWrongSelected = isSubmitted && isSelected && !submittedAnswers[currentQ].is_correct;

                let optClass =
                  "w-full text-left p-4 rounded-xl border-2 transition-all font-mono text-sm flex items-start gap-3 ";
                if (isSubmitted) {
                  if (isCorrectOption) {
                    optClass += "border-cyber-green bg-cyber-green/5 text-cyber-green";
                  } else if (isWrongSelected) {
                    optClass += "border-cyber-red bg-cyber-red/5 text-cyber-red";
                  } else {
                    optClass += "border-black/5 bg-white border-border/70 text-text-muted cursor-not-allowed";
                  }
                } else if (isSelected) {
                  optClass += "border-cyber-blue bg-cyber-blue/10 text-text-primary shadow-cyber-blue";
                } else {
                  optClass += "border-black/5 hover:border-gray-500 text-text-muted hover:bg-surface-2 cursor-pointer";
                }

                return (
                  <button
                    key={oi}
                    onClick={() => !isSubmitted && submitAnswer(oi)}
                    disabled={isSubmitted || loading}
                    className={optClass}
                  >
                    <span className="font-bold text-cyber-blue shrink-0 w-6 h-6 rounded-full border border-current flex items-center justify-center text-[10px]">
                      {String.fromCharCode(65 + oi)}
                    </span>
                    <span className="leading-relaxed">{option}</span>
                    {isCorrectOption && (
                      <CheckCircle size={18} className="text-cyber-green shrink-0 ml-auto mt-0.5" />
                    )}
                    {isWrongSelected && (
                      <XCircle size={18} className="text-cyber-red shrink-0 ml-auto mt-0.5" />
                    )}
                  </button>
                )}
              </div>
              {submittedAnswers[currentQ] && (
                <motion.div
                  className={submittedAnswers[currentQ].is_correct ? "border-cyber-green/10" : "border-cyber-red/15"} className="card mb-4"
                >
                  <p className="text-[11px] font-mono text-gray-500 mt-2 leading-relaxed">
                    {submittedAnswers[currentQ].explanation}
                  </p>
                </motion.div>
              )}
              <div className="flex items-center justify-between">
                <button
                  onClick={() => navigateQuestion(currentQ - 1)}
                  disabled={currentQ === 0}
                  className="btn-ghost flex items-center gap-2 disabled:opacity-30"
                >
                  <ArrowLeft size={16} /> Previous
                </button>
                <div className="flex items-center gap-3">
                  {currentQ < questions.length - 1 ? (
                    <button
                      onClick={() => navigateQuestion(currentQ + 1)}
                      className="btn-ghost flex items-center gap-2"
                    >
                      Next <ChevronRight size={16} />
                    </button>
                  ) : (
                    <button
                      onClick={submitTest}
                      disabled={loading}
                      className="btn-primary flex items-center gap-2"
                    >
                      {loading ? <Spinner size="sm" className="text-space-void" /> : <><span>Submit OA</span> <ArrowRight size={16} /></>}
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
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
                <p className="font-mono text-[10px] uppercase tracking-widest text-gray-500 mb-3">Progress</p>
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
                    <span className="text-gray-400">{unattemptedCount}</span>
                  </div>
                </div>
              </div>

              <div className="border-t border-black/5 pt-4">
                <button
                  onClick={submitTest}
                  disabled={loading}
                  className="btn-primary w-full flex items-center justify-center gap-2"
                >
                  {loading ? <Spinner size="sm" className="text-space-void" /> : <><span>Submit OA</span> <ArrowRight size={16} /></>}
                </button>
                <button
                  onClick={() => {
                    if (window.confirm("Are you sure? This will submit your OA.")) submitTest();
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

  if (step === "results" && result) {
    const pct = result.percentage || 0;
    return (
      <div className="page-surface min-h-screen py-6 px-4">
        <div className="max-w-5xl mx-auto">
          <motion.div
            className="card mb-8 text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <span className="section-subheader mb-4 block">Assessment Complete</span>
            <div className="flex justify-center mb-6">
              <div className="text-center">
                <p className="font-display font-black text-2xl text-cyber-green">{correctCount}</p>
                <p className="font-mono text-[10px] text-gray-500 uppercase">Correct</p>
              </div>
              <div className="w-px h-8 bg-space-border" />
              <div className="text-center">
                <p className="font-display font-black text-2xl text-cyber-red">{wrongCount}</p>
                <p className="font-mono text-[10px] text-gray-500 uppercase">Wrong</p>
              </div>
              <div className="w-px h-8 bg-space-border" />
              <div className="text-center">
                <p className="font-display font-black text-2xl text-gray-400">{unattemptedCount}</p>
                <p className="font-mono text-[10px] text-gray-500 uppercase">Unattempted</p>
              </div>
              <div className="w-px h-8 bg-space-border" />
              <div className="text-center">
                <p className="font-display font-black text-2xl text-cyber-blue">{formatTime(result.timeTaken)}</p>
                <p className="font-mono text-[10px] text-gray-500 uppercase">Time Taken</p>
              </div>
            </div>
            <p className="font-mono text-xs text-gray-500">{company.name} Mock OA — {total} Questions</p>
          </motion.div>

          <motion.div className="mb-8" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <h2 className="section-header text-lg mb-4 flex items-center gap-2">
              <BarChart3 size={20} className="text-cyber-purple" /> Section Breakdown
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {company.sections.map((sectionName) => {
                const stats = getSectionStats(sectionName);
                const secPct = stats.total > 0 ? Math.round((stats.correct / stats.total) * 100) : 0;
                return (
                  <div key={sectionName} className="card">
                    <h3 className="font-display font-bold text-text-primary text-sm mb-3">{sectionName}</h3>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-mono text-2xl font-black text-cyber-blue">{secPct}%</span>
                      <span className="font-mono text-xs text-gray-500">{stats.correct}/{stats.total}</span>
                    </div>
                    <div className="mb-3 h-1.5 w-full rounded-full border border-black/5 bg-surface-2">
                      <div className={`h-1.5 rounded-full transition-all duration-1000 ${secPct >= 70 ? "bg-cyber-green" : secPct >= 40 ? "bg-cyber-amber" : "bg-cyber-red"}`} style={{ width: secPct + "%" }} />
                    </div>
                    <div className="flex gap-3 text-[10px] font-mono">
                      <span className="text-cyber-green">✓ {stats.correct}</span>
                      <span className="text-cyber-red">✗ {stats.wrong}</span>
                      <span className="text-gray-500">— {stats.unattempted}</span>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>

            <motion.div className="flex gap-4 mt-10">
              <button
                onClick={() => {
                  setStep("select");
                  setResult(null);
                  setQuestions([]);
                  setAnswers({});
                  setSubmittedAnswers({});
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
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Spinner size="lg" />
    </div>
  );
}
'''

with open('D:/Project-Fremen/frontend/src/pages/MockOA.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("MockOA.tsx written successfully")