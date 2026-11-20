import { useState, useCallback, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ChevronRight, X, Timer, Loader2, CheckCircle, RefreshCw } from "lucide-react";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";
import { Card, SectionHeader } from "../design-system/Card";
import api from "../services/api";

interface DiagnosticQuestion {
  id: string;
  section: string;
  question: string;
  options: string[];
  difficulty: string;
  time_limit: number;
}

type DiagnosticPhase = "intro" | "active" | "result";

const SECTION_LABELS: Record<string, string> = {
  aptitude: "Quantitative Aptitude",
  logical: "Logical Reasoning",
  verbal: "Verbal Ability",
  coding: "Coding / DSA",
  cs_fundamentals: "CS Fundamentals",
};

export default function OnboardingDiagnostic() {
  const navigate = useNavigate();
  const [phase, setPhase] = useState<DiagnosticPhase>("intro");
  const [questions, setQuestions] = useState<DiagnosticQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, { correct: boolean; seconds: number; chosen_option_index: number | null }>>({});
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [startTime, setStartTime] = useState<number>(0);

  const startDiagnostic = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.onboarding.diagnosticStart({
        company: "tcs",
        sections: ["aptitude", "logical", "verbal", "coding", "cs_fundamentals"],
        max_questions: 25,
      });
      setQuestions(data.questions || []);
      setStartTime(Date.now());
      setPhase("active");
    } catch (err: any) {
      setError(err.message || "Failed to start diagnostic");
    } finally {
      setLoading(false);
    }
  }, []);

  const handleAnswer = useCallback(
    (correct: boolean, chosenOptionIndex: number | null) => {
      const q = questions[currentIndex];
      const seconds = Math.round((Date.now() - startTime) / 1000);
      setAnswers((prev) => ({
        ...prev,
        [q.id]: { correct, seconds, chosen_option_index: chosenOptionIndex },
      }));

      if (currentIndex < questions.length - 1) {
        setCurrentIndex((i) => i + 1);
        setStartTime(Date.now());
      } else {
        setPhase("result");
      }
    },
    [questions, currentIndex, startTime]
  );

  const completeDiagnostic = useCallback(async () => {
    setSubmitting(true);
    try {
      const answerList = Object.entries(answers).map(([questionId, ans]) => ({
        question_id: questionId,
        correct: ans.correct,
        seconds: ans.seconds,
        chosen_option_index: ans.chosen_option_index,
        skill_id: "dsa.uncategorized", // Will be mapped server-side
      }));

      // Record each answer
      for (const ans of answerList) {
        await api.onboarding.diagnosticAnswer({
          question_id: ans.question_id,
          skill_id: ans.skill_id,
          correct: ans.correct,
          seconds: ans.seconds,
          chosen_option_index: ans.chosen_option_index,
        });
      }

      const resultData = await api.onboarding.diagnosticComplete({
        company: "tcs",
        days_left: 30,
        slots_per_day: 3,
      });
      setResult(resultData);
      setPhase("result");
    } catch (err: any) {
      setError(err.message || "Failed to complete diagnostic");
    } finally {
      setSubmitting(false);
    }
  }, [answers]);

  const progress = questions.length > 0 ? ((currentIndex + 1) / questions.length) * 100 : 0;
  const currentQ = questions[currentIndex];

  if (phase === "intro") {
    return (
      <PageShell theme="focus">
        <div className="max-w-md mx-auto text-center py-12">
          <div className="w-16 h-16 rounded-full bg-brand-primary flex items-center justify-center mx-auto mb-6">
            <Timer size={32} strokeWidth={2} className="text-text-inverse" />
          </div>
          <h1 className="text-2xl font-bold text-text-primary mb-3">Placement Diagnostic</h1>
          <p className="text-text-muted mb-8">
            Answer up to 25 questions in about 12 minutes. This helps us build
            your personalized learning plan.
          </p>
          <div className="space-y-3 text-left">
            <div className="flex items-start gap-3">
              <CheckCircle size={16} className="text-success" />
              <span className="text-sm text-text-primary">
                <span className="font-semibold">25 questions max</span> — never more
              </span>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle size={16} className="text-success" />
              <span className="text-sm text-text-primary">
                <span className="font-semibold">~12 minutes</span> — timed but not rushed
              </span>
            </div>
            <div className="flex items-start gap-3">
              <CheckCircle size={16} className="text-success" />
              <span className="text-sm text-text-primary">
                <span className="font-semibold">Verified questions only</span> — no low-quality content
              </span>
            </div>
          </div>
          <Button variant="primary" onClick={startDiagnostic} disabled={loading} loading={loading} fullWidth>
            Start Diagnostic
          </Button>
          {error && (
            <div className="mt-4 p-3 rounded-lg bg-semantic-error text-text-inverse text-sm">
              {error}
            </div>
          )}
        </div>
      </PageShell>
    );
  }

  if (phase === "active") {
    return (
      <PageShell theme="focus">
        <div className="max-w-md mx-auto space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-xs text-text-muted uppercase tracking-wider">
              Question {currentIndex + 1} of {questions.length}
            </span>
            <span className="text-xs font-semibold">{SECTION_LABELS[currentQ.section] || currentQ.section}</span>
          </div>
          <div className="w-full bg-surface2 rounded-full h-2 overflow-hidden">
            <div
              className="bg-brand-primary h-full rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>

          <Card padding="p-6">
            <h2 className="text-lg font-bold text-text-primary mb-4">{currentQ.question}</h2>
            <div className="space-y-2">
              {currentQ.options.map((opt, idx) => (
                <button
                  key={idx}
                  onClick={() => handleAnswer(idx === 0, idx)} // option 0 = correct for demo
                  className="w-full text-left p-3 rounded-lg border border-border-primary bg-surface2 hover:bg-brand-mint transition-all text-text-primary"
                >
                  {opt}
                </button>
              ))}
            </div>
          </Card>

          <section className="flex items-center justify-between">
            <Button variant="outline" onClick={() => setPhase("result")} size="sm">
              Skip for now
            </Button>
            <Button
              variant="primary"
              onClick={() => handleAnswer(false, null)}
              disabled={currentQ === undefined}
            >
              Next
              <ChevronRight size={16} strokeWidth={1.8} />
            </Button>
          </section>
        </div>
      </PageShell>
    );
  }

  // phase === "result"
  if (submitting) {
    return (
      <PageShell theme="celebration">
        <div className="max-w-md mx-auto text-center py-12">
          <Loader2 className="animate-spin h-8 w-8 text-brand-primary mx-auto mb-4" />
          <p className="text-text-muted">Computing your results...</p>
        </div>
      </PageShell>
    );
  }

  if (error && !result) {
    return (
      <PageShell theme="celebration">
        <div className="max-w-md mx-auto text-center py-12">
          <X size={32} className="text-semantic-error mx-auto mb-4" />
          <h3 className="font-bold text-text-primary mb-2">{error}</h3>
          <Button variant="outline" onClick={() => setPhase("intro")}>
            Try Again
          </Button>
        </div>
      </PageShell>
    );
  }

  return (
    <PageShell theme="celebration">
      <div className="max-w-md mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-text-primary">Diagnostic Complete</h2>
          <Button variant="outline" size="sm" onClick={() => setPhase("intro")}>
            <RefreshCw size={16} strokeWidth={1.8} /> Retake
          </Button>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-surface2 border border-border-primary">
            <div className="text-xs text-text-muted">Readiness Range</div>
            <div className="text-2xl font-bold text-text-primary">
              {result.readiness_low}% – {result.readiness_high}%
            </div>
          </div>
          <div className="p-4 rounded-xl bg-surface2 border border-border-primary">
            <div className="text-xs text-text-muted">Evidence Label</div>
            <div className="text-sm font-semibold text-brand-primary">
              {result.evidence_label}
            </div>
          </div>
        </div>

        <Card padding="p-5">
          <SectionHeader title="Top Areas to Focus" />
          <div className="space-y-3">
            {result.top_gaps?.map((gap: any, idx: number) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-surface2 border border-border-primary">
                <div>
                  <div className="font-semibold text-text-primary">{gap.skill_name}</div>
                  <div className="text-xs text-text-muted">
                    Mastery: {gap.mastery}% • Weight: {gap.weight}
                  </div>
                </div>
                <div className="text-xs font-semibold text-semantic-error">
                  Gap
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card padding="p-5">
          <SectionHeader title="Today's Plan" />
          <div className="space-y-3">
            {result.todays_plan?.map((action: any, idx: number) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-brand-mint border border-brand-primary/30">
                <div className="flex-1">
                  <div className="font-semibold text-text-primary">
                    {action.type.charAt(0).toUpperCase() + action.type.slice(1)} — {action.skill_id}
                  </div>
                  <div className="text-xs text-text-muted">
                    p={action.factors?.p} • m_eff={action.factors?.m_eff}
                  </div>
                </div>
                {action.exploration && (
                  <span className="text-[10px] font-bold bg-brand-primary/20 text-brand-dark px-2 py-0.5 rounded">
                    Exploration
                  </span>
                )}
              </div>
            ))}
          </div>
        </Card>

        <Button variant="primary" onClick={() => navigate("/dashboard")} fullWidth>
          Go to Dashboard
        </Button>
      </div>
    </PageShell>
  );
}
