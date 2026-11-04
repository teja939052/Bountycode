import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import {
  ArrowRight,
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
import Markdown from "../components/learning/Markdown";

type StepStatus = "locked" | "current" | "completed";

function StepBadge({ status }: { status: StepStatus }) {
  const variants: Record<string, string> = {
    locked: "text-brand-muted",
    current: "text-cyber-green",
    completed: "text-brand-primary",
  };
  const icons: Record<string, JSX.Element> = {
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
  const stepStatus = (step: any): string => {
    if (!progress) return "locked";
    const key = `${lessonId}:${step.id}`;
    if (progress.completed?.[key]) return "completed";
    if (step.id === currentStep?.id) return "current";
    return "locked";
  };

  const isLastStep = currentStepIndex >= (lesson?.steps.length || 0) - 1;

  const runCode = async () => {
    if (!currentStep) return;
    setRunning(true);
    setOutput("");
    try {
      const result = await api.compiler.executeCode({
        code,
        language: "python",
      });
      setOutput(result.output || "");
      if (result.error) setOutput((prev) => prev + "\n" + result.error);
    } catch (e: any) {
      setOutput("Error: " + (e?.detail || e?.message || "Unknown error"));
    } finally {
      setRunning(false);
    }
  };

  const submitStep = async () => {
    if (!currentStep) return;
    setFeedback(null);
    setError("");
    try {
      if (currentStep.type === "quiz") {
        if (selectedOption === null) {
          setError("Please select an answer.");
          return;
        }
        const correct = selectedOption === (currentStep.correctIndex ?? -1);
        setFeedback(result);
        if (correct) {
          await markStepComplete(currentStep.id, code);
        }
        return;
      }
      const result = await api.lessons.completeStep({
        lesson_id: lessonId || "",
        step_id: currentStep.id,
        code,
      });
      setFeedback(result);
      if (result.is_correct) {
        const nextIndex = currentStepIndex + 1;
        if (nextIndex < (lesson?.steps.length || 0)) {
          setCurrentStepIndex(nextIndex);
          setCode(lesson.steps[nextIndex].starterCode || "");
          setOutput("");
          setSelectedOption(null);
        } else if (result.lesson_complete) {
          setCelebrating(true);
          try {
            const prog = await api.lessons.progress();
            setProgress(prog);
          } catch {}
        }
      }
    } catch (e: any) {
      setError(e?.detail || "Failed to submit");
    }
  };

  const markStepComplete = async (stepId: string, code: string) => {
    try {
      await api.lessons.completeStep({
        lesson_id: lessonId || "",
        step_id: stepId,
        code,
      });
      const nextIndex = currentStepIndex + 1;
      if (nextIndex < (lesson?.steps.length || 0)) {
        setCurrentStepIndex(nextIndex);
        setCode(lesson.steps[nextIndex].starterCode || "");
        setOutput("");
        setSelectedOption(null);
      } else {
        setCelebrating(true);
        try {
          const prog = await api.lessons.progress();
          setProgress(prog);
        } catch {}
      }
    } catch {}
  };

  const [selectedOption, setSelectedOption] = useState<number | null>(null);

  const goToNextLesson = async () => {
    try {
      const data = await api.lessons.next();
      if (data.lesson) {
        navigate(`/coding-academy/${data.lesson.id}`);
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
              k.startsWith(`${lessonId}:`),
            ).length : 0) /
            lesson.steps.length) *
            100,
        )
      : 0;

  return (
    <PageShell theme="focus" className="max-w-5xl mx-auto">
      <div className="mb-6 flex items-center justify-between gap-4">
        <Link to="/lessons">
          <Button variant="ghost" size="sm">
            <ArrowRight size={16} className="mr-2 rotate-180" /> Back to lessons
          </Button>
        </Link>
        <div className="flex items-center gap-3 text-sm font-medium text-text-muted">
          <ListChecks className="w-4 h-4" />
          <span>{progressPct}% complete</span>
        </div>
      </div>

      {celebrating && (
        <Card pad="md" className="text-center">
          <Trophy className="w-12 h-12 text-green-500 mx-auto mb-4" />
          <h3 className="font-bold text-text mb-2">Lesson complete!</h3>
          <p className="text-text-muted mb-4">
            You mastered {lesson.title}. Earned {lesson.xpReward} XP.
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
        <div className="lg:col-span-7 space-y-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold text-text text-xl">{lesson.title}</h2>
            <span className="text-xs font-mono text-brand-500">{lesson.track}</span>
          </div>
          <p className="text-text-muted">{lesson.description}</p>

          <div className="space-y-4">
            {lesson.steps.map((step: any, idx: number) => {
              const status = stepStatus(step);
              const isCurrent = idx === currentStepIndex;
              return (
                <Card pad="md" className={`cursor-pointer transition-all ${isCurrent ? "ring-2 ring-cyber-green bg-[#0f0f0f]" : "hover:border-white/10"}`} key={step.id} pad="md" interactive={status !== "completed"} onClick={() => setCurrentStepIndex(idx)}>
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <StepBadge status={status} />
                        <span className="font-bold text-text">{step.title}</span>
                      </div>
                      {status === "completed" && (
                        <p className="text-xs text-[#4ade80]">Completed</p>
                      )}
                      {status === "current" && (
                        <p className="text-xs text-cyber-green">Current step</p>
                      )}
                      {status === "locked" && (
                        <p className="text-xs text-[#9a9a9a]">Complete previous steps to unlock</p>
                      )}
                    </div>
                    <div className="text-xs font-mono text-slate-500">{idx + 1} / {lesson.steps.length}</div>
                  </div>
                </Card>
              </div>
            )}
          </div>

          {currentStep && (
            <Card pad="md" className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-4">
              {currentStep.type === "explain" && (
                <div className="space-y-4">
                  <div className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-4 font-mono text-sm text-[#e9e9e9] mb-4">
                    {currentStep.question || currentStep.code || ""}
                  </div>
                  {currentStep.code && (
                    <div className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg p-4 mt-4">
                      <div className="font-mono text-sm text-[#e9e9e9]">{currentStep.code}</div>
                    </div>
                    {currentStep.explanation && (
                      <p className="text-xs text-[#4ade80] mt-2">{currentStep.explanation}</p>
                    )}
                  </div>
                  <Button variant="primary" disabled={running} onClick={() => submitStep()}>
                    {running ? <Loader2 size={14} className="mr-2 animate-spin" /> : null} Mark complete &rarr;
                  </Button>
                </div>
              )}
              {currentStep.type === "predict" && (
                <div className="space-y-4">
                  <div className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-4 mb-4">
                    <div className="font-mono text-sm text-[#e9e9e9]">{currentStep.question}</div>
                    <input type="text" value={code} onChange={(e) => setCode(e.target.value)} placeholder="Predict the output..." className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] outline-none" />
                    <div className="mt-3 flex gap-3">
                      <Button variant="outline" disabled={!answer.trim()} onClick={() => setPhase("practice")}>
                        Back
                      </Button>
                      <Button variant="primary" onClick={() => setPhase("test")}>
                        Clock icon
                        Lock prediction
                      </Button>
                    </div>
                  </div>
                  {feedback && (
                    <div className={`mt-3 p-3 rounded bg-[#16161a] border border-green-500/20 text-green-400 text-sm`}>
                      {feedback.message}
                    </div>
                  )}
                </Card>
              )}

              {/* PHASE: TEST */}
              {phase === "test" && (
                <Card pad="md">
                  <SectionHeader eyebrow="Test" title="Timed topic test" description="5 questions, 10 minutes. Independent assessment." />
                  {loading && <div className="text-center py-8 text-text-muted">Loading questions…</div>}
                  {error && <div className="p-3 rounded bg-red-500/10 border border-red-500/30 text-red-400 text-sm">{error}</div>}
                  {!loading && currentQuestion && attemptId && (
                    <div className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-4 mb-4">
                      <div className="font-mono text-sm text-[#e9e9e9] mb-2">{currentQuestion.question}</div>
                      {currentQuestion.options && (
                        <div className="space-y-2">
                          {currentQuestion.options.map((opt: string, i: number) => (
                            <button
                              key={i}
                              onClick={() => setAnswer(opt)}
                              className={`w-full text-left px-3 py-2 rounded border text-sm ${answer === opt ? "border-[#ffa116] bg-[#16161a]" : "border-[#2a2a2a] bg-[#0f0f0f]"} text-[#e9e9e9]`}
                            >
                              {opt}
                            </button>
                          ))}
                        </div>
                        {!currentQuestion.options && (
                          <input
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            placeholder="Your answer"
                            className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] outline-none"
                          />
                        )}
                        <div className="mt-4 flex justify-between">
                          <Button variant="outline" onClick={() => setPhase("practice")}>Back</Button>
                          <Button variant="primary" disabled={!answer.trim() || loading} onClick={submitAnswer}>
                            {loading ? "Saving…" : "Next question &rarr;"}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </Card>
                )}
              }

              {/* PHASE: DIAGNOSE */}
              {phase === "diagnose" && (
                <Card pad="md">
                  <SectionHeader eyebrow="Diagnose" title="Where did the model break?" description="Evidence-based misconception diagnosis." />
                  {diagnostics.length === 0 && <div className="text-center py-8 text-text-muted">No diagnostics yet.</div>}
                  <div className="space-y-3">
                    {diagnostics.map((d) => (
                      <Card key={d.pattern} pad="sm" tone="sand">
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-bold text-text">{d.pattern}</span>
                          <span className={`text-xs font-bold px-2 py-1 rounded ${d.weakness_tier === "critical" ? "bg-red-500/20 text-red-400" : d.weakness_tier === "weak" ? "bg-amber-50 text-amber-400" : "bg-green-500/20 text-green-400"}`}>{d.weakness_tier}</span>
                        </div>
                        <div className="text-sm text-text-muted mb-3">Score: {(d.exam_score ?? 0) * 100}% ({d.questions_correct}/{d.questions_seen})</div>
                        <div className="flex gap-3">
                          <Button variant="outline" size="sm" onClick={() => goToRepair(d.pattern)}>
                            Targeted repair
                          </Button>
                          <Button variant="primary" size="sm" onClick={() => goToReassess(d.pattern)}>
                            Reassess
                          </Button>
                        </div>
                        <div className="mt-2 text-xs text-[#ffa116]">
                          Next action: {d.next_action?.action} — {d.next_action?.reason}
                        </div>
                      </Card>
                    ))}
                  </div>
                  <div className="mt-6 flex gap-3">
                    <Button variant="outline" onClick={() => setPhase("test")}>Retake test</Button>
                    {!xpClaimed && (
                      <Button variant="gold" onClick={claimXp} disabled={loading}>
                        Claim {selectedTopic.key} XP
                      </Button>
                    )}
                  </div>
                </Card>
              )}
            </Card>
          </div>

          {/* PHASE: REPAIR */}
          {phase === "repair" && (
            <Card pad="md">
              <SectionHeader eyebrow="Repair" title="Targeted drill" description="Practice the diagnosed misconception." />
              <div className="space-y-4">
                {repairQuestions.map((q, i) => (
                  <div key={i} className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-4 mb-3">
                    <div className="font-mono text-sm text-[#e9e9e9] mb-2">{q.question}</div>
                    <input
                      placeholder="Answer"
                      className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] outline-none"
                    />
                  </div>
                ))}
              </div>
              <div className="mt-6 flex gap-3">
                <Button variant="outline" onClick={() => setPhase("diagnose")}>Back to diagnosis</Button>
                <Button variant="primary" onClick={() => goToReassess(selectedTopic.key)}>
                  <Clock className="w-4 h-4 mr-2" /> Reassess with new questions
                </Button>
              </div>
            </Card>
          )}

          {/* PHASE: REASSESS */}
          {phase === "reassess" && (
            <Card pad="md">
              <SectionHeader eyebrow="Reassess" title="Unseen questions" description="Prove improvement with different questions." />
              <div className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-4 mb-4">
                <div className="font-mono text-sm text-[#e9e9e9] mb-2">{reassessQuestions[reassessIndex]?.question}</div>
                <input
                  value={reassessAnswers[reassessQuestions[reassessIndex]?.id] || ""}
                  onChange={(e) => setReassessAnswers({ ...reassessAnswers, [reassessQuestions[reassessIndex]?.id]: e.target.value })}
                  placeholder="Your answer"
                  className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] focus:border-[#ffa116] outline-none"
                />
              </div>
              <div className="flex gap-3">
                <Button variant="outline" onClick={() => setPhase("diagnose")}>Back</Button>
                <Button variant="primary" disabled={reassessIndex >= reassessQuestions.length - 1} onClick={() => setReassessIndex((i) => i + 1)}>
                  Next &rarr;
                </Button>
                {reassessIndex >= reassessQuestions.length - 1 && (
                  <Button variant="gold" onClick={() => setPhase("done")}>
                    Finish &rarr;
                  </Button>
                )}
              </div>
            </Card>
          )}

          {/* PHASE: DONE */}
          {phase === "done" && (
            <Card pad="md" className="text-center py-12">
              <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
              <h3 className="font-bold text-text mb-2">Topic mastered</h3>
              <p className="text-text-muted mb-6">You traced, predicted, practiced, tested, diagnosed, repaired, and reassessed.</p>
              {!xpClaimed && (
                <Button variant="gold" onClick={claimXp} disabled={loading}>
                  Claim {selectedTopic.key} mastery XP
                </Button>
              )}
              <div className="mt-6 flex gap-3 justify-center">
                <Button variant="outline" onClick={() => setSelectedTopic(null)}>Back to topics</Button>
                <Button variant="primary" onClick={() => navigate("/coding-academy")}>Start another topic</Button>
              </div>
            </Card>
          )}
        </Card>
      </div>
    </PageShell>
  );
}