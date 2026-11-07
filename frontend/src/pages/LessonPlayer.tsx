import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import {
  ArrowLeft,
  CheckCircle2,
  Play,
  Trophy,
  ListChecks,
  Loader2,
  Lock,
} from "lucide-react";
import api from "../services/api";
import { Card } from "../design-system/Card";
import { Button } from "../design-system/Button";
import { PageShell } from "../design-system/PageShell";

type StepStatus = "locked" | "current" | "completed";

function StepBadge({ status }: { status: StepStatus }) {
  const variants: Record<StepStatus, string> = {
    locked: "text-brand-muted",
    current: "text-cyber-green",
    completed: "text-brand-primary",
  };
  const icons: Record<StepStatus, JSX.Element> = {
    locked: <Lock size={14} />,
    current: <Play size={14} />,
    completed: <CheckCircle2 size={14} />,
  };
  return (
    <span className={`flex items-center gap-1 text-xs font-medium ${variants[status]}`}>
      {icons[status]}
    </span>
  );
}

function feedbackClass(result: any): string {
  if (result?.is_correct === true) {
    return "bg-[#4ade80]/10 border border-[#4ade80]/30 text-[#4ade80]";
  }
  if (result?.is_correct === false) {
    return "bg-red-500/10 border border-red-500/30 text-red-400";
  }
  return "bg-amber-500/10 border border-amber-500/30 text-amber-300";
}

export default function LessonPlayer() {
  const { lessonId } = useParams<{ lessonId: string }>();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<any>(null);
  const [progress, setProgress] = useState<any>(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);
  const [feedback, setFeedback] = useState<any>(null);
  const [celebrating, setCelebrating] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedOption, setSelectedOption] = useState<number | null>(null);

  useEffect(() => {
    if (!lessonId) return;
    loadLesson();
    loadProgress();
  }, [lessonId]);

  const loadLesson = async () => {
    if (!lessonId) return;
    try {
      const data = await api.lessons.get(lessonId);
      setLesson(data);
      const completedKeys = Object.keys(data?.completed || {});
      const firstIncomplete = data.steps.findIndex(
        (s: any) => !completedKeys.includes(`${lessonId}:${String(s.id)}`)
      );
      setCurrentStepIndex(firstIncomplete === -1 ? data.steps.length - 1 : firstIncomplete);
      if (data.steps[0]?.starterCode) setCode(data.steps[0].starterCode);
    } catch (e: any) {
      setError(e?.detail || "Failed to load lesson");
    } finally {
      setLoading(false);
    }
  };

  const loadProgress = async () => {
    try {
      const data = await api.lessons.progress();
      setProgress(data);
    } catch {}
  };

  const currentStep = lesson?.steps?.[currentStepIndex];
  const stepStatus = (step: any): StepStatus => {
    if (!progress) return "locked";
    const key = `${lessonId}:${step.id}`;
    if (progress.completed?.[key]) return "completed";
    if (step.id === currentStep?.id) return "current";
    return "locked";
  };

  const runCode = async () => {
    if (!currentStep) return;
    setRunning(true);
    setOutput("");
    try {
      const result = await api.compiler.executeCode({
        code,
        language: lesson?.track === "java" || lesson?.track === "cpp" ? lesson.track : "python",
      });
      setOutput(result.output || "");
      if (result.error) setOutput((prev) => prev + "\n" + result.error);
    } catch (e: any) {
      setOutput("Error: " + (e?.detail || e?.message || "Unknown error"));
    } finally {
      setRunning(false);
    }
  };

  const advanceAfter = async (result: any) => {
    const nextIndex = currentStepIndex + 1;
    if (nextIndex < (lesson?.steps.length || 0)) {
      setFeedback(null);
      setCurrentStepIndex(nextIndex);
      setCode(lesson.steps[nextIndex].starterCode || "");
      setOutput("");
      setSelectedOption(null);
      setRunning(false);
      await loadProgress();
    } else if (result.lesson_complete) {
      setCelebrating(true);
      setRunning(false);
      await loadProgress();
    } else {
      setFeedback(null);
      setRunning(false);
    }
  };

  const submitStep = async () => {
    if (!currentStep) return;
    setFeedback(null);
    setError("");
    if (currentStep.type === "quiz" && selectedOption === null) {
      setError("Please select an answer.");
      return;
    }
    setRunning(true);
    try {
      // Correctness is decided by the server; the client only sends the answer.
      const result = await api.lessons.completeStep({
        lesson_id: lessonId || "",
        step_id: currentStep.id,
        code: currentStep.type === "exercise" ? code : "",
        answer:
          currentStep.type === "quiz" && selectedOption !== null
            ? String(selectedOption)
            : undefined,
      });
      setFeedback(result);
      if (result.step_completed) {
        await advanceAfter(result);
      } else {
        setRunning(false);
      }
    } catch (e: any) {
      setError(e?.detail || "Failed to submit");
      setRunning(false);
    }
  };

  const goToNextLesson = async () => {
    try {
      const data = await api.lessons.next();
      if (data.lesson) {
        navigate(`/lessons/${data.lesson.id}`);
      }
    } catch {}
  };

  if (loading || !lesson) {
    return (
      <PageShell theme="focus" className="max-w-4xl mx-auto py-20">
        <div className="flex items-center justify-center gap-2">
          <Loader2 className="w-6 h-6 animate-spin" />
          <span className="text-text-muted">Loading lesson…</span>
        </div>
      </PageShell>
    );
  }

  if (error) {
    return (
      <PageShell theme="focus" className="max-w-4xl mx-auto py-20">
        <Card pad="md" className="text-center">
          <div className="text-red-400 mb-4">{error}</div>
          <Button variant="outline" onClick={() => navigate("/lessons")}>
            Back to lessons
          </Button>
        </Card>
      </PageShell>
    );
  }

  const progressPct = lesson.steps.length
    ? Math.round(
        ((progress?.completed
          ? Object.keys(progress.completed).filter((k) =>
              k.startsWith(`${lessonId}:`)
            ).length : 0) /
          lesson.steps.length) *
          100
        )
    : 0;

  return (
    <PageShell theme="focus" className="max-w-5xl mx-auto">
      <div className="mb-6 flex items-center justify-between gap-4">
        <Link to="/lessons">
          <Button variant="ghost" size="sm">
            <ArrowLeft size={16} className="mr-2" /> Back to lessons
          </Button>
        </Link>
        <div className="flex items-center gap-3 text-sm font-medium text-text-muted">
          <ListChecks className="w-4 h-4" />
          <span>{progressPct}% complete</span>
        </div>
      </div>

      {celebrating && (
        <Card pad="md" className="bg-[#1a1a1a] border-white/5 text-center">
          <Trophy className="w-10 h-10 text-amber-500 mx-auto mb-3" />
          <h3 className="font-bold text-text mb-2">Lesson complete!</h3>
          <p className="text-text-muted mb-4">
            {feedback?.lesson_verified
              ? `Verified completion of ${lesson.title}. Earned ${
                  feedback?.xp_earned || 0
                } XP.`
              : `${lesson.title} is complete, but it has no automatically verified check yet, so no XP or mastery was awarded.`}
          </p>
          <div className="flex gap-3 justify-center">
            <Button variant="primary" onClick={goToNextLesson}>
              Next lesson
            </Button>
            <Button variant="outline" onClick={() => navigate("/lessons")}>
              Back to lessons
            </Button>
          </div>
        </Card>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Lesson content */}
        <div className="lg:col-span-7 space-y-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold text-text text-xl">{lesson.title}</h2>
            <span className="text-xs font-mono text-brand-muted">{lesson.track}</span>
          </div>
          <p className="text-text-muted">{lesson.description}</p>

          <div className="space-y-4">
            {lesson.steps.map((step: any, idx: number) => {
              const status = stepStatus(step);
              const isCurrent = idx === currentStepIndex;
              return (
                <Card
                  key={step.id}
                  pad="md"
                  className={`cursor-pointer transition-all ${
                    isCurrent
                      ? "ring-2 ring-cyber-green bg-[#0d1117]"
                      : "hover:border-white/10"
                  }`}
                  onClick={
                    status === "locked"
                      ? undefined
                      : () => setCurrentStepIndex(idx)
                  }
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <StepBadge status={status} />
                        <span className="font-semibold text-text">
                          {step.title}
                        </span>
                      </div>
                      {status === "completed" && (
                        <p className="text-xs text-[#4ade80]">Completed</p>
                      )}
                      {status === "current" && (
                        <p className="text-xs text-cyber-green">Current step</p>
                      )}
                      {status === "locked" && (
                        <p className="text-xs text-brand-muted">
                          Complete previous steps to unlock
                        </p>
                      )}
                    </div>
                    <div className="text-xs font-mono text-brand-muted">
                      {idx + 1} / {lesson.steps.length}
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>

          {/* Current step content */}
          {currentStep && (
            <Card pad="md" className="bg-[#0d1117] border-white/5">
              {currentStep.type === "explain" && (
                <div className="space-y-4">
                  <h3 className="font-bold text-text">{currentStep.title}</h3>
                  <div className="prose prose-sm text-[#c9d1d9] max-w-none">
                    {currentStep.content || ""}
                  </div>
                  {currentStep.code && (
                    <div className="bg-[#0a0a0a] border border-white/10 rounded-lg p-4 mt-4 overflow-hidden">
                      <div className="flex items-center justify-between px-4 py-2 bg-[#0d1117] border-b border-white/5">
                        <span className="text-xs font-mono text-brand-muted">python</span>
                        <span className="text-xs text-[#c9d1d9]">{currentStep.explanation ? "Example" : "Code"}</span>
                      </div>
                      <pre className="p-4 overflow-x-auto text-sm font-mono text-[#e9e9e9]">{currentStep.code}</pre>
                      {currentStep.output && (
                        <div className="bg-[#000] border border-[#333] rounded-lg p-3 mt-2 text-sm font-mono text-[#4ade80] overflow-x-auto">
                          {currentStep.output}
                        </div>
                      )}
                      {currentStep.explanation && (
                        <p className="text-xs text-[#4ade80] mt-3">{currentStep.explanation}</p>
                      )}
                    </div>
                  )}
                  <Button
                    variant="primary"
                    onClick={() => submitStep()}
                    disabled={running}
                  >
                    {running ? <Loader2 size={14} className="mr-2 animate-spin" /> : null}
                    Mark complete &rarr;
                  </Button>
                </div>
              )}
              {currentStep.type === "exercise" && (
                <div className="space-y-4">
                  <h3 className="font-bold text-text">{currentStep.title}</h3>
                  <p className="text-text-muted text-sm">{currentStep.instruction}</p>
                  <div className="bg-[#0a0a0a] border border-white/10 rounded-lg overflow-hidden">
                    <div className="flex items-center justify-between px-4 py-2 bg-[#0d1117] border-b border-white/5">
                      <span className="text-xs font-mono text-brand-muted">python</span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={runCode}
                        disabled={running}
                        className="text-cyber-green"
                      >
                        {running ? <Loader2 size={12} className="animate-spin mr-2" /> : <Play size={12} />}
                        Run
                      </Button>
                    </div>
                    <pre className="p-4 overflow-x-auto text-sm font-mono text-[#e9e9e9]">
                      {code || currentStep.starterCode || ""}
                    </pre>
                  </div>
                  <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    rows={8}
                    className="w-full rounded-lg border border-[#2a2a2a] bg-[#0a0a0a] px-3 py-2 text-sm text-[#e9e9e9] font-mono focus:border-[#ffa116] outline-none placeholder:text-brand-muted"
                    placeholder="Write your code here..."
                  />
                  {output && (
                    <div className="mt-3">
                      <div className="text-xs text-brand-muted mb-1">Output:</div>
                      <pre className="p-3 rounded bg-[#000] border border-[#333] text-sm text-[#4ade80] font-mono overflow-x-auto">
                        {output}
                      </pre>
                    </div>
                  )}
                  <div className="mt-4 flex gap-3">
                    <Button
                      variant="primary"
                      disabled={running || !code.trim()}
                      onClick={submitStep}
                    >
                      {running ? <Loader2 size={14} className="mr-2 animate-spin" /> : null}
                      Submit answer &rarr;
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => setCode(currentStep.starterCode || "")}
                    >
                      Reset
                    </Button>
                  </div>
                  {feedback && (
                    <div
                      className={`mt-3 p-3 rounded text-sm ${feedbackClass(feedback)}`}
                    >
                      {feedback.feedback}
                    </div>
                  )}
                  {error && (
                    <div className="mt-3 p-3 rounded bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
                      {error}
                    </div>
                  )}
                </div>
              )}
              {currentStep.type === "quiz" && (
                <div className="space-y-4">
                  <h3 className="font-bold text-text">{currentStep.title}</h3>
                  <p className="text-text-muted text-sm">{currentStep.question}</p>
                  <div className="space-y-2">
                    {(currentStep.options || []).map((opt: string, i: number) => {
                      const isSelected = selectedOption === i;
                      const answered = feedback && feedback.graded;
                      const tone = !answered
                        ? "border-[#2a2a2a] bg-[#0a0a0a] text-[#e9e9e9] hover:border-white/30"
                        : isSelected
                        ? feedback.is_correct
                          ? "bg-[#4ade80]/20 border-[#4ade80]/50 text-[#4ade80]"
                          : "bg-red-500/20 border-red-500/50 text-red-400"
                        : "border-[#2a2a2a] bg-[#0a0a0a] text-[#e9e9e9] hover:border-white/30";
                      return (
                        <button
                          key={i}
                          onClick={() => setSelectedOption(i)}
                          className={`w-full text-left px-4 py-3 rounded-lg border text-sm font-mono transition-all ${tone}`}
                        >
                          {i}. {opt}
                        </button>
                      );
                    })}
                  </div>
                  <div className="mt-3 flex gap-3">
                    <Button
                      variant="primary"
                      disabled={selectedOption === null || running}
                      onClick={submitStep}
                    >
                      {running ? <Loader2 size={14} className="mr-2 animate-spin" /> : null}
                      Submit answer &rarr;
                    </Button>
                  </div>
                  {feedback && (
                    <div
                      className={`mt-3 p-3 rounded font-bold ${feedbackClass(feedback)}`}
                    >
                      {feedback.feedback}
                    </div>
                  )}
                  {error && (
                    <div className="mt-3 p-3 rounded bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
                      {error}
                    </div>
                  )}
                </div>
              )}
            </Card>
          )}
        </div>

        {/* Right: Progress sidebar */}
        <div className="lg:col-span-5 space-y-6">
          <Card pad="md">
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-semibold text-text-muted">Progress</span>
              <span className="text-sm font-bold text-text">{progressPct}%</span>
            </div>
            <div className="w-full bg-[#1a1a1a] rounded-full h-2">
              <div
                className="bg-cyber-green h-2 rounded-full transition-all duration-500"
                style={{ width: `${progressPct}%` }}
              ></div>
            </div>
            <div className="mt-3 text-xs text-[#9a9a9a]">
              {progress?.xp_earned || 0} XP earned
            </div>
          </Card>

          <Card pad="md" className="bg-[#1a1a1a] border-white/5">
            <h3 className="font-bold text-text mb-3">Steps</h3>
            <div className="space-y-2">
              {lesson.steps.map((step: any, idx: number) => {
                const status = stepStatus(step);
                return (
                  <div
                    key={step.id}
                    className={`flex items-center gap-3 p-2 rounded ${
                      status === "completed"
                        ? "bg-[#4ade80]/20"
                        : status === "current"
                        ? "bg-cyber-green/20"
                        : "bg-transparent"
                    }`}
                  >
                    <div
                      className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                        status === "completed"
                          ? "bg-[#4ade80] text-[#0a0a0a]"
                          : status === "current"
                          ? "bg-cyber-green text-[#0a0a0a]"
                          : "bg-[#1a1a1a] text-brand-muted border border-[#2a2a2a]"
                      }`}
                    >
                      {idx + 1}
                    </div>
                    <div className="flex-1">
                      <div className="text-sm text-text truncate">{step.title}</div>
                      <div className="text-xs text-brand-muted capitalize">
                        {step.type}
                      </div>
                    </div>
                    <StepBadge status={status} />
                  </div>
                );
              })}
            </div>
          </Card>

          {progress && (
            <Card pad="md" className="bg-[#1a1a1a] border-white/5">
              <h3 className="font-bold text-text mb-3">Your stats</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-brand-muted">XP earned</span>
                  <span className="text-text">{progress.xp_earned}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-brand-muted">Steps done</span>
                  <span className="text-text">
                    {Object.keys(progress.completed || {}).filter((k) =>
                      k.startsWith(`${lessonId}:`)
                    ).length} / {lesson.steps.length}
                  </span>
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </PageShell>
  );
}
