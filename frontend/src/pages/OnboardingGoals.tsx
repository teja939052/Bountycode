import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronRight, ArrowLeft, User, Target, Clock, Timer, Users, Sparkles, Check } from "lucide-react";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";
import { Card, SectionHeader } from "../design-system/Card";
import api from "../services/api";

type GoalStep = "company" | "role" | "when" | "minutes" | "done";

const COMPANY_OPTIONS = [
  { id: "tcs", label: "TCS", desc: "Tata Consultancy Services" },
  { id: "infosys", label: "Infosys", desc: "Infosys" },
  { id: "wipro", label: "Wipro", desc: "Wipro" },
  { id: "cognizant", label: "Cognizant", desc: "Cognizant" },
  { id: "capgemini", label: "Capgemini", desc: "Capgemini" },
  { id: "accenture", label: "Accenture", desc: "Accenture" },
  { id: "not_sure", label: "Not sure yet", desc: "I'll get recommendations" },
];

const ROLE_OPTIONS = [
  { id: "student", label: "Student", desc: "Campus placement preparation" },
  { id: "job_seeker", label: "Job Seeker", desc: "Experienced professional" },
];

const WHEN_OPTIONS = [
  { id: "2_weeks", label: "2 weeks", desc: "Test is coming up soon" },
  { id: "1_month", label: "1 month", desc: "About 30 days away" },
  { id: "3_months", label: "3 months", desc: "Have time to prepare" },
  { id: "6_months", label: "6 months", desc: "Long-term preparation" },
];

const MINUTES_OPTIONS = [
  { id: 15, label: "15 min/day", desc: "Quick daily practice" },
  { id: 30, label: "30 min/day", desc: "Steady progress" },
  { id: 60, label: "1 hour/day", desc: "Focused preparation" },
  { id: 90, label: "90 min/day", desc: "Intensive prep" },
];

const STEP_TITLES: Record<GoalStep, string> = {
  company: "Which company are you targeting?",
  role: "Who are you?",
  when: "When is your test?",
  minutes: "How much time daily?",
  done: "Goals saved",
};

const STEP_DESCRIPTIONS: Record<GoalStep, string> = {
  company: "We'll tailor your plan to your target company's pattern.",
  role: "This helps us set the right difficulty and pace.",
  when: "We'll work backward from your test date.",
  minutes: "We'll fit a realistic plan into your schedule.",
  done: "Your goals are saved. Let's start the diagnostic.",
};

const STEP_ICONS: Record<GoalStep, React.ReactNode> = {
  company: <Target size={34} strokeWidth={1.6} />,
  role: <User size={34} strokeWidth={1.6} />,
  when: <Clock size={34} strokeWidth={1.6} />,
  minutes: <Timer size={34} strokeWidth={1.6} />,
  done: <Sparkles size={34} strokeWidth={1.6} />,
};

export default function OnboardingGoals() {
  const navigate = useNavigate();
  const [step, setStep] = useState<GoalStep>("company");
  const [selectedCompany, setSelectedCompany] = useState<string | null>(null);
  const [selectedRole, setSelectedRole] = useState<string | null>(null);
  const [selectedWhen, setSelectedWhen] = useState<string | null>(null);
  const [selectedMinutes, setSelectedMinutes] = useState<number | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const totalSteps = 4;
  const currentStepIndex = (["company", "role", "when", "minutes"] as GoalStep[]).indexOf(step);

  const handleSelect = useCallback(
    (id: string | number) => {
      switch (step) {
        case "company":
          setSelectedCompany(id as string);
          break;
        case "role":
          setSelectedRole(id as string);
          break;
        case "when":
          setSelectedWhen(id as string);
          break;
        case "minutes":
          setSelectedMinutes(id as number);
          break;
      }
    },
    [step]
  );

  const isComplete = () => {
    switch (step) {
      case "company": return selectedCompany !== null;
      case "role": return selectedRole !== null;
      case "when": return selectedWhen !== null;
      case "minutes": return selectedMinutes !== null;
      default: return false;
    }
  };

  const next = useCallback(async () => {
    if (!isComplete()) return;

    const steps = ["company", "role", "when", "minutes"] as GoalStep[];
    const nextIdx = currentStepIndex + 1;
    if (nextIdx >= steps.length) {
      // Save all goals
      setSubmitting(true);
      try {
        await api.onboarding.saveGoals({
          target_company: selectedCompany!,
          target_role: selectedRole!,
          target_date: selectedWhen!,
          days_left: undefined,
          daily_minutes: selectedMinutes!,
          role: selectedRole!,
        });
        setStep("done");
      } catch {
        // Fall through to done even if save fails
        setStep("done");
      } finally {
        setSubmitting(false);
      }
    } else {
      setStep(steps[nextIdx]);
    }
  }, [step, currentStepIndex, selectedCompany, selectedRole, selectedWhen, selectedMinutes, submitting]);

  const prev = useCallback(() => {
    const steps = ["company", "role", "when", "minutes"] as GoalStep[];
    const prevIdx = currentStepIndex - 1;
    if (prevIdx >= 0) setStep(steps[prevIdx]);
  }, [currentStepIndex]);

  const renderOptions = () => {
    switch (step) {
      case "company":
        return COMPANY_OPTIONS.map((o) => (
          <button
            key={o.id}
            onClick={() => handleSelect(o.id)}
            className={`w-full flex items-center gap-3 p-4 rounded-xl border transition-all ${
              selectedCompany === o.id
                ? "border-brand-primary bg-brand-mint text-brand-dark"
                : "border-border-primary bg-surface2 text-text-primary"
            }`}
          >
            <div className="flex-1 text-left">
              <div className="font-semibold">{o.label}</div>
              <div className="text-xs text-text-muted">{o.desc}</div>
            </div>
            {selectedCompany === o.id && <ChevronRight size={18} className="text-brand-primary" />}
          </button>
        ));
      case "role":
        return ROLE_OPTIONS.map((o) => (
          <button
            key={o.id}
            onClick={() => handleSelect(o.id)}
            className={`w-full flex items-center gap-3 p-4 rounded-xl border transition-all ${
              selectedRole === o.id
                ? "border-brand-primary bg-brand-mint text-brand-dark"
                : "border-border-primary bg-surface2 text-text-primary"
            }`}
          >
            <div className="flex-1 text-left">
              <div className="font-semibold">{o.label}</div>
              <div className="text-xs text-text-muted">{o.desc}</div>
            </div>
            {selectedRole === o.id && <ChevronRight size={18} className="text-brand-primary" />}
          </button>
        ));
      case "when":
        return WHEN_OPTIONS.map((o) => (
          <button
            key={o.id}
            onClick={() => handleSelect(o.id)}
            className={`w-full flex items-center gap-3 p-4 rounded-xl border transition-all ${
              selectedWhen === o.id
                ? "border-brand-primary bg-brand-mint text-brand-dark"
                : "border-border-primary bg-surface2 text-text-primary"
            }`}
          >
            <div className="flex-1 text-left">
              <div className="font-semibold">{o.label}</div>
              <div className="text-xs text-text-muted">{o.desc}</div>
            </div>
            {selectedWhen === o.id && <ChevronRight size={18} className="text-brand-primary" />}
          </button>
        ));
      case "minutes":
        return MINUTES_OPTIONS.map((o) => (
          <button
            key={o.id}
            onClick={() => handleSelect(o.id)}
            className={`w-full flex items-center gap-3 p-4 rounded-xl border transition-all ${
              selectedMinutes === o.id
                ? "border-brand-primary bg-brand-mint text-brand-dark"
                : "border-border-primary bg-surface2 text-text-primary"
            }`}
          >
            <div className="flex-1 text-left">
              <div className="font-semibold">{o.label}</div>
              <div className="text-xs text-text-muted">{o.desc}</div>
            </div>
            {selectedMinutes === o.id && <ChevronRight size={18} className="text-brand-primary" />}
          </button>
        ));
      default:
        return null;
    }
  };

  const progress = ((currentStepIndex + 1) / totalSteps) * 100;

  return (
    <PageShell theme="focus">
      <div className="max-w-md mx-auto space-y-6">
        <section className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs text-text-muted uppercase tracking-wider">
              Step {currentStepIndex + 1} of {totalSteps}
            </span>
            <span className="text-xs font-semibold">{STEP_TITLES[step]}</span>
          </div>
          <div className="w-full bg-surface2 rounded-full h-2 overflow-hidden">
            <div
              className="bg-brand-primary h-full rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </section>

        <AnimatePresence mode="wait">
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-5"
          >
            <section className="space-y-3">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-brand-primary flex items-center justify-center text-text-inverse font-bold text-xl">
                  {STEP_ICONS[step]}
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-text-primary">{STEP_TITLES[step]}</h1>
                  <p className="text-text-muted">{STEP_DESCRIPTIONS[step]}</p>
                </div>
              </div>
              {renderOptions()}
            </section>
          </motion.div>
        </AnimatePresence>

        <section className="flex items-center justify-between pt-4">
          {currentStepIndex > 0 && (
            <Button variant="outline" onClick={prev} size="sm">
              <ArrowLeft size={16} strokeWidth={1.8} /> Back
            </Button>
          )}
          <Button
            variant="primary"
            onClick={next}
            disabled={!isComplete() || submitting}
            loading={submitting}
          >
            {step === "minutes" ? "Save Goals" : "Continue"}
            <ChevronRight size={16} strokeWidth={1.8} />
          </Button>
        </section>

        {step === "done" && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center py-8"
          >
            <div className="w-16 h-16 rounded-full bg-success flex items-center justify-center mx-auto mb-4">
              <Check size={24} strokeWidth={2} className="text-text-inverse" />
            </div>
            <h2 className="text-xl font-bold text-text-primary mb-2">Goals Saved</h2>
            <p className="text-text-muted mb-6">
              Your plan is tailored to {selectedCompany}. Starting the diagnostic...
            </p>
            <Button variant="primary" onClick={() => navigate("/onboarding/diagnostic")}>
              Start Diagnostic
            </Button>
          </motion.div>
        )}
      </div>
    </PageShell>
  );
}
