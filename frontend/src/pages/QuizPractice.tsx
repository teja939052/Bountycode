import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Clock,
  Lightbulb,
  Play,
  RefreshCw,
  Send,
  Target,
  Trophy,
  XCircle,
  Zap,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

type QuizQuestion = {
  id: string;
  title?: string;
  question: string;
  topic?: string;
  sub_topic?: string;
  difficulty?: string;
  type?: string;
  options?: string[];
  hint_count?: number;
  index: number;
};

type QuizSession = {
  quiz_id: string;
  mode: string;
  total_questions: number;
  time_limit_seconds: number;
  questions: QuizQuestion[];
  filters: { topics?: string[]; difficulty?: string; company?: string };
};

type GradedAnswer = {
  question_id: string;
  is_correct: boolean;
  explanation?: string;
  correct_answer?: string;
  solution?: { code?: string; language?: string; time_complexity?: string; space_complexity?: string };
  xp_earned?: number;
  hints_used?: number;
};

function getErrorMessage(error: any) {
  return error?.response?.data?.detail || error?.data?.detail || error?.message || "Something went wrong. Please try again.";
}

export default function QuizPractice() {
  const queryClient = useQueryClient();
  const { data: statsResult, isLoading: statsLoading } = useQuery({
    queryKey: ["quiz", "stats"],
    queryFn: () => api.quiz.getStats(),
    staleTime: 300_000,
  });
  const { data: trackResult, isLoading: tracksLoading } = useQuery({
    queryKey: ["company-tracks", "list"],
    queryFn: () => api.companyTracks.listCompanies(),
    staleTime: 60_000,
  });

  const stats = (statsResult as any)?.stats || {};
  const topicNames = useMemo(
    () => Object.keys(stats.by_topic || {}).filter(Boolean).sort((a, b) => a.localeCompare(b)),
    [stats.by_topic],
  );
  const tracks = (trackResult as any)?.tracks || [];

  const [topic, setTopic] = useState("");
  const [trackId, setTrackId] = useState("");
  const [difficulty, setDifficulty] = useState("all");
  const [mode, setMode] = useState("practice");
  const [questionCount, setQuestionCount] = useState(10);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [session, setSession] = useState<QuizSession | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answerValue, setAnswerValue] = useState("");
  const [graded, setGraded] = useState<GradedAnswer | null>(null);
  const [hintText, setHintText] = useState("");
  const [hintsUsed, setHintsUsed] = useState(0);
  const [loading, setLoading] = useState(false);
  const [finishing, setFinishing] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);
  const [weakTopics, setWeakTopics] = useState<any[]>([]);
  const startedAt = useRef<number>(0);
  const questionStartedAt = useRef<number>(0);
  const timerExpired = useRef(false);

  const selectedTrack = tracks.find((item: any) => item.id === trackId);
  const questions = session?.questions || [];
  const question = questions[currentIndex];
  const progress = questions.length ? Math.round(((currentIndex + (graded ? 1 : 0)) / questions.length) * 100) : 0;
  const totalQuestions = Number(stats.total || 0);
  const hasOptions = Boolean(question?.options?.length);

  const startQuiz = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    setWeakTopics([]);
    try {
      const response: any = await api.quiz.buildQuiz({
        mode,
        ...(topic ? { topics: [topic] } : {}),
        ...(difficulty !== "all" ? { difficulty } : {}),
        ...(selectedTrack?.company_id ? { company: selectedTrack.company_id } : {}),
        num_questions: questionCount,
        time_limit_seconds: mode === "quiz" ? questionCount * 60 : 0,
      });
      const built = response?.quiz;
      if (!built?.questions?.length) throw new Error("No questions match these filters. Try a broader topic or company selection.");
      setSession(built);
      setCurrentIndex(0);
      setAnswerValue("");
      setGraded(null);
      setHintText("");
      setHintsUsed(0);
      timerExpired.current = false;
      setTimeRemaining(Number(built.time_limit_seconds || 0));
      startedAt.current = Date.now();
      questionStartedAt.current = Date.now();
    } catch (err: any) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const requestHint = async () => {
    if (!session || !question || graded || hintsUsed >= (question.hint_count || 0)) return;
    setLoading(true);
    setError("");
    try {
      const response: any = await api.quiz.getHint(
        question.id,
        hintsUsed + 1,
        hintsUsed,
        session.quiz_id,
      );
      const hint = response?.hint;
      setHintText(hint?.text || hint?.content || String(hint || "Think about the key constraint in the question."));
      setHintsUsed(Number(response?.hints_used ?? hintsUsed + 1));
    } catch (err: any) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!session || !question || graded || !answerValue.trim()) return;
    setLoading(true);
    setError("");
    try {
      const response: any = await api.quiz.submitAnswer({
        quiz_id: session.quiz_id,
        question_id: question.id,
        user_answer: answerValue.trim(),
        time_taken_seconds: Math.max(0, (Date.now() - questionStartedAt.current) / 1000),
        // This is only backward compatibility; the backend uses its own hint ledger.
        hints_used: hintsUsed,
      });
      setGraded({
        question_id: question.id,
        ...response.result,
        hints_used: Number(response.result?.hints_used ?? hintsUsed),
      });
    } catch (err: any) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const finishQuiz = async () => {
    if (!session) return;
    setFinishing(true);
    setError("");
    try {
      const elapsed = Math.max(0, Math.floor((Date.now() - startedAt.current) / 1000));
      const response: any = await api.quiz.calculateResults({
        quiz_id: session.quiz_id,
        total_time_seconds: elapsed,
      });
      setResult(response?.results || null);
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["study", "today"] }),
        queryClient.invalidateQueries({ queryKey: ["journey", "state"] }),
        queryClient.invalidateQueries({ queryKey: ["adaptive"] }),
      ]);
      try {
        const weak: any = await api.quiz.getWeakTopics();
        setWeakTopics(weak?.weak_topics || []);
      } catch {
        setWeakTopics([]);
      }
      setSession(null);
    } catch (err: any) {
      setError(getErrorMessage(err));
    } finally {
      setFinishing(false);
    }
  };

  useEffect(() => {
    if (!session?.time_limit_seconds) return;
    const deadline = startedAt.current + session.time_limit_seconds * 1000;
    const tick = () => {
      const remaining = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
      setTimeRemaining(remaining);
      if (remaining === 0 && !timerExpired.current) {
        timerExpired.current = true;
        void finishQuiz();
      }
    };
    tick();
    const timer = window.setInterval(tick, 1000);
    return () => window.clearInterval(timer);
    // The timer belongs to one immutable quiz session; finishQuiz reads that session.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session?.quiz_id]);

  const goNext = async () => {
    if (!session || !graded) return;
    if (currentIndex >= questions.length - 1) {
      await finishQuiz();
      return;
    }
    setCurrentIndex((value) => value + 1);
    setAnswerValue("");
    setGraded(null);
    setHintText("");
    setHintsUsed(0);
    questionStartedAt.current = Date.now();
  };

  const restart = () => {
    setSession(null);
    setResult(null);
    setWeakTopics([]);
    setError("");
    setCurrentIndex(0);
    setAnswerValue("");
    setGraded(null);
    setHintText("");
  };

  if (result) {
    return (
      <div className="mx-auto max-w-4xl space-y-5 px-4 py-6 pb-20">
        <Link to="/academy" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-600 hover:text-slate-900">
          <ArrowLeft size={15} /> Placement Academy
        </Link>
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-700"><Trophy size={30} /></div>
            <div className="flex-1">
              <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-emerald-700">Practice report</p>
              <h1 className="mt-1 text-2xl font-black text-slate-900">You completed the session</h1>
              <p className="mt-1 text-sm text-slate-500">Use this evidence to decide what to revisit next.</p>
            </div>
            <div className="text-left sm:text-right">
              <p className="text-4xl font-black text-slate-900">{result.score_percentage ?? 0}%</p>
              <p className="text-xs font-semibold text-slate-500">Grade {result.grade || "—"}</p>
            </div>
          </div>
          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <div className="rounded-2xl bg-slate-50 p-3"><p className="text-2xl font-black text-slate-900">{result.correct}/{result.total_questions}</p><p className="text-xs text-slate-500">Correct answers</p></div>
            <div className="rounded-2xl bg-slate-50 p-3"><p className="text-2xl font-black text-slate-900">{result.answered_questions ?? result.total_questions}</p><p className="text-xs text-slate-500">Answered</p></div>
            <div className="rounded-2xl bg-slate-50 p-3"><p className="text-2xl font-black text-slate-900">{result.hints_used ?? 0}</p><p className="text-xs text-slate-500">Hints used</p></div>
            <div className="rounded-2xl bg-slate-50 p-3"><p className="text-2xl font-black text-slate-900">+{result.total_xp ?? 0}</p><p className="text-xs text-slate-500">XP earned</p></div>
          </div>
          <div className="mt-6 flex flex-wrap gap-2">
            <button type="button" onClick={restart} className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-slate-900 px-4 text-sm font-bold text-white"><RefreshCw size={15} /> New practice</button>
            <Link to="/academy" className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-slate-200 px-4 text-sm font-bold text-slate-700">Back to Academy <ArrowRight size={15} /></Link>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-5">
          <h2 className="font-bold text-slate-900">Topic breakdown</h2>
          <div className="mt-4 space-y-3">
            {Object.entries(result.topic_breakdown || {}).map(([name, value]: [string, any]) => {
              const pct = value.total ? Math.round(value.correct / value.total * 100) : 0;
              return <div key={name}>
                <div className="mb-1 flex justify-between gap-3 text-xs"><span className="font-semibold text-slate-700">{name}</span><span className="text-slate-500">{value.correct}/{value.total} · {pct}%</span></div>
                <div className="h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-emerald-600" style={{ width: `${pct}%` }} /></div>
              </div>;
            })}
          </div>
        </section>

        {weakTopics.length > 0 && (
          <section className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
            <h2 className="flex items-center gap-2 font-bold text-amber-950"><Target size={16} /> Recommended review</h2>
            <p className="mt-1 text-sm text-amber-900/80">These topics have low accuracy across your saved practice history.</p>
            <div className="mt-3 flex flex-wrap gap-2">{weakTopics.slice(0, 6).map((item: any) => <span key={item.topic} className="rounded-full bg-white px-3 py-1.5 text-xs font-semibold text-amber-900">{item.topic} · {Math.round(item.success_rate * 100)}%</span>)}</div>
            <p className="mt-3 text-xs text-amber-900/70">Return to the Academy and choose an easier lesson or practice set for these skills.</p>
          </section>
        )}
      </div>
    );
  }

  if (session && question) {
    const answered = Boolean(graded);
    const chosenIndex = hasOptions ? Number(answerValue) : -1;
    return (
      <div className="mx-auto max-w-4xl space-y-5 px-4 py-6 pb-20">
        <div className="flex items-center justify-between gap-3">
          <button type="button" onClick={restart} className="inline-flex items-center gap-2 text-sm font-semibold text-slate-600"><ArrowLeft size={15} /> Exit practice</button>
          <span className="inline-flex items-center gap-1 rounded-full bg-slate-100 px-3 py-1 text-[11px] font-semibold text-slate-600"><Clock size={12} /> Question {currentIndex + 1} of {questions.length}</span>
        </div>
        <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">
          <div className="mb-5 flex items-center justify-between gap-3">
            <div className="flex flex-wrap gap-2">
              <span className="rounded-full bg-emerald-50 px-3 py-1 text-[10px] font-bold text-emerald-800">{question.topic || "General"}</span>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-[10px] font-bold capitalize text-slate-600">{question.difficulty || "medium"}</span>
            </div>
            <span className="text-xs font-bold text-slate-500">{progress}%</span>
          </div>
          <div className="h-1.5 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-emerald-600 transition-all" style={{ width: `${progress}%` }} /></div>
          <p className="mt-6 text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">{question.sub_topic || question.type || "Practice question"}</p>
          <h1 className="mt-2 whitespace-pre-wrap text-xl font-bold leading-8 text-slate-900">{question.title || question.question}</h1>
          {question.title && <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-700">{question.question}</p>}

          {hasOptions ? (
            <div className="mt-6 space-y-2">
              {question.options!.map((option, index) => {
                const isCorrect = graded && (graded.correct_answer === option);
                const isSelected = chosenIndex === index;
                const style = answered
                  ? isCorrect ? "border-emerald-400 bg-emerald-50 text-emerald-950"
                    : isSelected ? "border-rose-300 bg-rose-50 text-rose-950"
                    : "border-slate-100 bg-slate-50 text-slate-500"
                  : isSelected ? "border-emerald-500 bg-emerald-50 text-slate-900"
                    : "border-slate-200 bg-white text-slate-700 hover:border-emerald-400";
                return <button key={index} type="button" disabled={answered || loading} onClick={() => setAnswerValue(String(index))} className={`flex min-h-12 w-full items-center gap-3 rounded-xl border px-4 py-3 text-left text-sm transition ${style}`}>
                  <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-black/5 text-xs font-bold">{String.fromCharCode(65 + index)}</span>
                  <span className="flex-1">{option}</span>
                  {answered && isCorrect && <CheckCircle2 size={17} className="text-emerald-600" />}
                  {answered && isSelected && !isCorrect && <XCircle size={17} className="text-rose-600" />}
                </button>;
              })}
            </div>
          ) : (
            <label className="mt-6 block">
              <span className="mb-2 block text-xs font-semibold text-slate-600">Your answer</span>
              <input value={answerValue} onChange={(event) => setAnswerValue(event.target.value)} disabled={answered || loading} placeholder="Type your answer…" className="min-h-12 w-full rounded-xl border border-slate-200 px-4 text-sm outline-none focus:border-emerald-500" />
            </label>
          )}

          {hintText && <div className="mt-4 rounded-2xl border border-amber-200 bg-amber-50 p-4"><p className="flex items-center gap-2 text-xs font-bold text-amber-900"><Lightbulb size={14} /> Hint {hintsUsed}</p><p className="mt-2 text-sm leading-6 text-amber-950">{hintText}</p></div>}

          {answered && (
            <div className={`mt-5 rounded-2xl border p-4 ${graded!.is_correct ? "border-emerald-200 bg-emerald-50" : "border-rose-200 bg-rose-50"}`}>
              <p className={`flex items-center gap-2 text-sm font-bold ${graded!.is_correct ? "text-emerald-900" : "text-rose-900"}`}>
                {graded!.is_correct ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
                {graded!.is_correct ? "Correct — nice work!" : "Not quite. Let's learn from it."}
              </p>
              {graded!.explanation && <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-700">{graded!.explanation}</p>}
              {graded!.solution?.code && <pre className="mt-3 overflow-x-auto rounded-xl bg-slate-950 p-3 text-xs text-slate-100">{graded!.solution.code}</pre>}
              {graded!.solution?.time_complexity && <p className="mt-2 text-xs text-slate-600">Time: {graded!.solution.time_complexity} · Space: {graded!.solution.space_complexity || "—"}</p>}
              <p className="mt-2 text-xs font-semibold text-slate-600">+{graded!.xp_earned || 0} XP earned · {hintsUsed} hints used</p>
            </div>
          )}

          {error && <p role="alert" className="mt-4 rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-800">{error}</p>}
          <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
            {!answered ? (
              <>
                <button type="button" onClick={requestHint} disabled={loading || hintsUsed >= (question.hint_count || 0)} className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-amber-200 px-4 text-sm font-semibold text-amber-900 disabled:opacity-40"><Lightbulb size={15} /> {loading ? "Loading…" : hintsUsed >= (question.hint_count || 0) ? "No more hints" : "Get a hint"}</button>
                <button type="button" onClick={submitAnswer} disabled={loading || !answerValue.trim()} className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-slate-900 px-5 text-sm font-bold text-white disabled:opacity-40">{loading ? "Checking…" : "Check answer"} <Send size={14} /></button>
              </>
            ) : (
              <button type="button" onClick={goNext} disabled={finishing} className="ml-auto inline-flex min-h-11 items-center gap-2 rounded-xl bg-emerald-700 px-5 text-sm font-bold text-white disabled:opacity-50">{currentIndex === questions.length - 1 ? finishing ? "Finishing…" : "See results" : "Next question"} <ArrowRight size={14} /></button>
            )}
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl space-y-5 px-4 py-6 pb-20">
      <Link to="/academy" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-600 hover:text-slate-900"><ArrowLeft size={15} /> Placement Academy</Link>
      <header className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-emerald-50 p-6 shadow-sm sm:p-8">
        <p className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.18em] text-emerald-700"><BookOpen size={14} /> Adaptive practice</p>
        <h1 className="mt-2 text-3xl font-black text-slate-900">Practise until you understand</h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">Build a focused quiz from the placement question bank. Hints arrive gradually, answers are graded by the server, and your attempts update your skill evidence.</p>
        <div className="mt-4 flex flex-wrap gap-3 text-xs font-semibold text-slate-600">
          <span className="rounded-full bg-white px-3 py-1">{totalQuestions.toLocaleString()} questions in bank</span>
          <span className="rounded-full bg-white px-3 py-1">{stats.with_hints || 0} with hints</span>
          <span className="rounded-full bg-white px-3 py-1">{stats.with_solutions || 0} with solutions</span>
        </div>
      </header>
      <section className="rounded-2xl border border-slate-200 bg-white p-5 sm:p-6">
        <h2 className="text-lg font-bold text-slate-900">Build your practice session</h2>
        <div className="mt-5 grid gap-4 sm:grid-cols-2">
          <label className="block"><span className="mb-2 block text-xs font-bold text-slate-700">Target company track</span>
            <select value={trackId} onChange={(event) => setTrackId(event.target.value)} disabled={tracksLoading || loading} className="min-h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm">
              <option value="">All companies</option>
              {tracks.map((track: any) => <option key={track.id} value={track.id}>{track.name}</option>)}
            </select>
          </label>
          <label className="block"><span className="mb-2 block text-xs font-bold text-slate-700">Question topic</span>
            <select value={topic} onChange={(event) => setTopic(event.target.value)} disabled={statsLoading || loading} className="min-h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm">
              <option value="">All topics</option>
              {topicNames.map(name => <option key={name} value={name}>{name} ({stats.by_topic[name]})</option>)}
            </select>
          </label>
          <label className="block"><span className="mb-2 block text-xs font-bold text-slate-700">Assessment mode</span>
            <select value={mode} onChange={(event) => setMode(event.target.value)} disabled={loading} className="min-h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm">
              <option value="practice">Guided practice · hints and explanations</option>
              <option value="quiz">Assessment quiz · no time limit</option>
              <option value="mock_interview">Company mock · no hints</option>
              <option value="speed_run">Speed run · bonus XP</option>
              <option value="boss_battle">Boss battle · challenge mode</option>
            </select>
          </label>
          <label className="block"><span className="mb-2 block text-xs font-bold text-slate-700">Difficulty</span>
            <select value={difficulty} onChange={(event) => setDifficulty(event.target.value)} disabled={loading} className="min-h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm">
              <option value="all">Mixed</option><option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option>
            </select>
          </label>
          <label className="block"><span className="mb-2 block text-xs font-bold text-slate-700">Number of questions</span>
            <select value={questionCount} onChange={(event) => setQuestionCount(Number(event.target.value))} disabled={loading} className="min-h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm">
              <option value={5}>5 questions · Quick practice</option><option value={10}>10 questions · Focus session</option><option value={15}>15 questions · Deep practice</option><option value={20}>20 questions · Challenge</option>
            </select>
          </label>
        </div>
        {error && <p role="alert" className="mt-4 rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-800">{error}</p>}
        <button type="button" onClick={startQuiz} disabled={loading || statsLoading} className="mt-5 inline-flex min-h-12 items-center gap-2 rounded-xl bg-emerald-700 px-5 text-sm font-bold text-white disabled:opacity-50">{loading ? <Spinner size={15} /> : <Play size={15} />} {mode === "quiz" ? "Start assessment" : mode === "mock_interview" ? "Start mock interview" : mode === "speed_run" ? "Start speed run" : mode === "boss_battle" ? "Start boss battle" : "Start practice"}</button>
      </section>
      <section className="grid gap-3 sm:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-4"><Lightbulb className="text-amber-600" size={18} /><h3 className="mt-2 font-bold text-slate-900">Progressive hints</h3><p className="mt-1 text-xs leading-5 text-slate-500">Use a small nudge before revealing more. Hint usage is recorded with your attempt.</p></div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4"><Target className="text-emerald-700" size={18} /><h3 className="mt-2 font-bold text-slate-900">Real grading</h3><p className="mt-1 text-xs leading-5 text-slate-500">Answers are checked against the saved key. Unverifiable coding tasks go through the code runner.</p></div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4"><Zap className="text-violet-700" size={18} /><h3 className="mt-2 font-bold text-slate-900">Adaptive evidence</h3><p className="mt-1 text-xs leading-5 text-slate-500">Correct and incorrect attempts update the skills used by your personalized plan.</p></div>
      </section>
    </div>
  );
}
