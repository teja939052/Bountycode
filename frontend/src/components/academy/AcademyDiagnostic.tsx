import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowRight, Brain, Clock3, RefreshCw, Target } from "lucide-react";
import api from "../../services/api";

type DiagnosticQuestion = {
  id: string;
  index: number;
  title: string;
  question: string;
  topic: string;
  domain: string;
  difficulty: string;
  type: string;
  options: string[];
};

export default function AcademyDiagnostic() {
  const client = useQueryClient();
  const [session, setSession] = useState<any>(null);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [answered, setAnswered] = useState<string[]>([]);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const { data: latestData, isLoading } = useQuery({
    queryKey: ["academy", "diagnostic", "latest"],
    queryFn: () => api.academy.getLatestDiagnostic(),
    staleTime: 60_000,
  });
  const latest = (latestData as any)?.result;
  const questions: DiagnosticQuestion[] = session?.questions || [];
  const question = questions[index];
  const start = useMutation({
    mutationFn: () => api.academy.startDiagnostic(4),
    onSuccess: (response: any) => {
      setSession(response.diagnostic);
      setIndex(0);
      setAnswer("");
      setAnswered([]);
      setResult(null);
      setError("");
    },
    onError: (err: any) => setError(err?.message || "Could not start the diagnostic."),
  });
  const progress = questions.length ? Math.round(answered.length / questions.length * 100) : 0;

  const submit = async () => {
    if (!session || !question || !answer || answered.includes(question.id)) return;
    setError("");
    setSubmitting(true);
    try {
      await api.academy.answerDiagnostic(session.diagnostic_id, question.id, answer);
      const next = [...answered, question.id];
      setAnswered(next);
      setAnswer("");
      if (index < questions.length - 1) setIndex(index + 1);
      else {
        const response: any = await api.academy.completeDiagnostic(session.diagnostic_id);
        setResult(response.result);
        setSession(null);
        await Promise.all([
          client.invalidateQueries({ queryKey: ["academy", "diagnostic", "latest"] }),
          client.invalidateQueries({ queryKey: ["academy", "plan"] }),
          client.invalidateQueries({ queryKey: ["adaptive"] }),
        ]);
      }
    } catch (err: any) {
      setError(err?.message || "Your answer could not be saved. Please retry.");
    } finally {
      setSubmitting(false);
    }
  };

  const displayResult = result || latest;
  if (isLoading) return null;

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-indigo-700"><Brain size={14} /> Skill diagnostic</p>
          <h2 className="mt-2 text-xl font-black text-slate-900">Find your real starting point</h2>
          <p className="mt-1 text-sm text-slate-600">A short baseline across coding, DSA, aptitude, reasoning, verbal, CS and SQL. Answers are graded on the server.</p>
        </div>
        <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700"><Target className="mr-1 inline" size={13}/> Evidence-based</span>
      </div>

      {session && question ? (
        <div className="mt-5">
          <div className="mb-3 flex items-center justify-between text-xs font-semibold text-slate-500">
            <span>Question {index + 1} of {questions.length}</span><span>{progress}% completed</span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-indigo-600 transition-all" style={{ width: `${progress}%` }}/></div>
          <div className="mt-5 rounded-2xl bg-slate-50 p-4">
            <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500"><span>{question.topic}</span><span>•</span><span>{question.difficulty}</span></div>
            <h3 className="mt-2 font-bold text-slate-900">{question.question}</h3>
            {question.options?.length ? (
              <div className="mt-4 grid gap-2">
                {question.options.map((option, optionIndex) => (
                  <button key={optionIndex} type="button" onClick={() => setAnswer(String(optionIndex))} className={`rounded-xl border p-3 text-left text-sm transition ${answer === String(optionIndex) ? "border-indigo-600 bg-indigo-50 text-indigo-900" : "border-slate-200 bg-white text-slate-700 hover:border-slate-400"}`}>
                    <span className="mr-2 font-bold">{String.fromCharCode(65 + optionIndex)}.</span>{option}
                  </button>
                ))}
              </div>
            ) : (
              <input value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder="Type your answer" className="mt-4 w-full rounded-xl border border-slate-200 bg-white p-3 text-sm"/>
            )}
          </div>
          {error && <p role="alert" className="mt-3 text-sm text-red-600">{error}</p>}
          <button type="button" disabled={!answer || start.isPending || submitting} onClick={submit} className="mt-4 inline-flex items-center gap-2 rounded-xl bg-indigo-700 px-5 py-3 text-sm font-bold text-white disabled:opacity-50">
            {submitting ? "Saving answer…" : index === questions.length - 1 ? "Finish diagnostic" : "Submit and continue"} <ArrowRight size={15}/>
          </button>
        </div>
      ) : displayResult ? (
        <div className="mt-5">
          <div className="flex flex-wrap items-end gap-3">
            <div><p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Baseline score</p><p className="text-4xl font-black text-slate-900">{displayResult.overall_score}%</p></div>
            <p className="pb-1 text-sm text-slate-600">{displayResult.correct_answers} of {displayResult.total_questions} correct</p>
          </div>
          <div className="mt-4 grid gap-2 sm:grid-cols-2">
            {(displayResult.skills || []).map((skill: any) => (
              <div key={skill.domain} className="rounded-xl border border-slate-200 p-3">
                <div className="flex items-center justify-between gap-2 text-sm"><span className="font-semibold text-slate-800">{skill.label}</span><strong>{skill.score}%</strong></div>
                <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-indigo-500" style={{ width: `${skill.score}%` }}/></div>
                <p className="mt-1 text-xs text-slate-500">{skill.level.replaceAll("_", " ")}</p>
              </div>
            ))}
          </div>
          <button type="button" onClick={() => start.mutate()} className="mt-4 inline-flex items-center gap-2 rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-700"><RefreshCw size={14}/> Retake diagnostic</button>
        </div>
      ) : (
        <div className="mt-5 flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-slate-50 p-4">
          <div><p className="font-semibold text-slate-900">Not assessed yet</p><p className="mt-1 text-sm text-slate-600">Usually 15–25 questions, depending on the available question bank.</p></div>
          <button type="button" disabled={start.isPending} onClick={() => start.mutate()} className="rounded-xl bg-indigo-700 px-5 py-3 text-sm font-bold text-white disabled:opacity-50">{start.isPending ? "Preparing..." : "Start diagnostic"}</button>
        </div>
      )}
      <p className="mt-4 text-xs text-slate-500"><Clock3 className="mr-1 inline" size={12}/> Baseline estimates guide your learning; they are not a hiring prediction.</p>
    </section>
  );
}
