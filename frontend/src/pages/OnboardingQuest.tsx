import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight,
  ArrowLeft,
  Check,
  ChevronRight,
  Star,
  Crown,
  Gem,
  Target,
  Keyboard,
  Flame,
} from "lucide-react";
import api from "../services/api";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";
import { MentorAvatar } from "../design-system/Mentor";
import { MasteryBar } from "../design-system/Progress";

const QUEST_STEPS = [
  {
    id: "step-1",
    title: "Choose Your Language",
    description:
      "Pick the language you want to learn. C, C++, Java, or Python — all paths lead to placement success.",
    type: "navigation",
    action: "Select a language from the learning hub",
    target: "/learn/c",
  },
  {
    id: "step-2",
    title: "Write Your First Code",
    description:
      "Open the first lesson and run your first program. You will have code running in under 30 seconds.",
    type: "action",
    action: "Open any lesson and click Run",
    target: "/free-trial",
  },
  {
    id: "step-3",
    title: "Earn Your First XP",
    description:
      "Complete the lesson and watch your progress climb. Gamification keeps you hooked.",
    type: "action",
    action: "Complete a lesson to earn XP",
    target: "/learn/c",
  },
  {
    id: "step-4",
    title: "Track Your Streak",
    description:
      "Keep learning daily to build your streak multiplier. Consistency beats intensity.",
    type: "info",
    action: "Check your streak in the dashboard",
    target: "/dashboard",
  },
  {
    id: "step-5",
    title: "Go Pro for Unlimited Access",
    description:
      "Free users get 3 lessons per month. Pro unlocks everything for $9/mo or lock in lifetime for $39.",
    type: "conversion",
    action: "Upgrade to Pro",
    target: "/pricing",
  },
];

/** Deterministic SVG glyph per step id — never trust remote emoji fields. */
const STEP_GLYPHS: Record<string, React.ReactNode> = {
  "step-1": <Target size={34} strokeWidth={1.6} className="text-ocean" />,
  "step-2": <Keyboard size={34} strokeWidth={1.6} className="text-tech" />,
  "step-3": <Star size={34} strokeWidth={1.6} className="text-reward" fill="#EAB74D" />,
  "step-4": <Flame size={34} strokeWidth={1.6} className="text-coral" />,
  "step-5": <Crown size={34} strokeWidth={1.6} className="text-wood" />,
};

/** Deterministic mentor line per step — dialogue from state, not random. */
const MENTOR_LINES: Record<string, string> = {
  "step-1": "First, pick your weapon. Every voyage starts with the tool you'll carry.",
  "step-2": "Code before you feel ready. The fastest way to learn is to run something real.",
  "step-3": "XP is your compass. It always points toward the next island.",
  "step-4": "Steady sailors outpace sprinters. Show up tomorrow — that's the whole trick.",
  "step-5": "Free waters only go so far. Pro charts the entire sea.",
};

const LANGUAGE_OPTIONS = [
  { id: "c", label: "C", desc: "Systems programming" },
  { id: "cpp", label: "C++", desc: "Competitive programming" },
  { id: "java", label: "Java", desc: "Enterprise & Android" },
  { id: "python", label: "Python", desc: "AI, Data & Automation" },
];

interface QuestStep {
  id: string;
  title: string;
  description: string;
  type?: string;
  action?: string;
  target?: string;
  icon?: string;
  iconLabel?: string;
}

interface QuestStatus {
  completed_steps?: string[];
  overall_progress?: number;
  is_complete?: boolean;
}

export default function OnboardingQuest() {
  const [currentStep, setCurrentStep] = useState(0);
  const [questData, setQuestData] = useState<{ steps: QuestStep[] } | null>(null);
  const [status, setStatus] = useState<QuestStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  useEffect(() => {
    async function load() {
      try {
        const [questRes, statusRes] = await Promise.all([
          api.onboarding.getQuest(),
          api.onboarding.getStatus(),
        ]);
        setQuestData(questRes.quest || questRes);
        setStatus(statusRes);
        const steps: QuestStep[] = questRes.quest?.steps || questRes.steps || QUEST_STEPS;
        const firstIncomplete = steps.findIndex(
          (s) => !statusRes.completed_steps?.includes(s.id)
        );
        if (firstIncomplete >= 0) {
          setCurrentStep(firstIncomplete);
        } else if (statusRes.is_complete) {
          navigate("/learn/c");
        }
      } catch {
        setQuestData({ steps: QUEST_STEPS });
        setCurrentStep(0);
      } finally {
        setLoading(false);
      }
    }
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleCompleteStep = useCallback(
    async (step: QuestStep) => {
      setSubmitting(true);
      try {
        await api.onboarding.completeStep({
          step_id: step.id,
          completed: true,
          xp_earned: 10,
        });
        const newCompleted = status
          ? [...(status.completed_steps || []), step.id]
          : [step.id];
        const steps = questData?.steps || QUEST_STEPS;
        const total = steps.length;
        const progress = Math.round((newCompleted.length / total) * 100);
        setStatus({
          completed_steps: newCompleted,
          overall_progress: progress,
          is_complete: newCompleted.length >= total,
        });
        if (step.id === "step-5") {
          navigate("/pricing");
          return;
        }
        if (step.target) {
          navigate(step.target);
          return;
        }
        const next = currentStep + 1;
        if (next < total) {
          setCurrentStep(next);
        } else {
          navigate("/learn/c");
        }
      } catch {
      } finally {
        setSubmitting(false);
      }
    },
    [currentStep, questData, status, navigate]
  );

  const handleSkip = useCallback(() => {
    navigate("/learn/c");
  }, [navigate]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-canvas px-4">
        <div className="flex flex-col items-center gap-4">
          <div className="h-10 w-10 animate-spin rounded-full border-2 border-primary border-t-transparent" />
          <p className="font-mono text-sm text-text-muted">Charting your journey...</p>
        </div>
      </div>
    );
  }

  const steps = questData?.steps || QUEST_STEPS;
  const step = steps[currentStep] || steps[0];
  const totalSteps = steps.length;
  const progress =
    status?.overall_progress || Math.round((currentStep / totalSteps) * 100);

  return (
    <PageShell theme="nature">
      <div className="flex min-h-screen items-center justify-center px-4 py-12">
        <div className="w-full max-w-lg">
          {/* Mentor greeting above card */}
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45 }}
            className="mb-5 flex items-center gap-3"
          >
            <MentorAvatar size={52} mood="briefing" />
            <p className="rounded-xl border border-border bg-surface px-4 py-2.5 text-sm leading-snug text-text-muted shadow-card">
              <span className="font-bold text-text">Captain Byte:</span>{" "}
              {MENTOR_LINES[step.id] || MENTOR_LINES["step-1"]}
            </p>
          </motion.div>

          <motion.div
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="overflow-hidden rounded-2xl border border-border bg-surface shadow-soft-lg"
          >
            {/* Progress */}
            <div className="surface-border border-b px-6 pb-4 pt-5">
              <div className="mb-3 flex items-center justify-between">
                <span className="adventure-label">
                  Leg {currentStep + 1} of {totalSteps}
                </span>
                <span className="text-xs font-bold text-primary-dark">{progress}%</span>
              </div>
              <MasteryBar value={progress} showValue={false} />
            </div>

            {/* Step content */}
            <AnimatePresence mode="wait">
              <motion.div
                key={step.id}
                initial={reduced ? {} : { opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                exit={reduced ? {} : { opacity: 0, x: -30 }}
                transition={{ duration: 0.35, ease: "easeInOut" }}
                className="space-y-6 px-6 py-6"
              >
                {/* Glyph */}
                <div className="flex justify-center">
                  <motion.div
                    initial={reduced ? {} : { scale: 0, rotate: -20 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.1 }}
                    className="surface-border flex h-20 w-20 items-center justify-center rounded-2xl border bg-mint"
                  >
                    {STEP_GLYPHS[step.id] ?? <Target size={34} className="text-ocean" />}
                  </motion.div>
                </div>

                {/* Title & Description */}
                <div className="text-center">
                  <h2 className="font-display mb-2 text-2xl font-extrabold text-text">{step.title}</h2>
                  <p className="mx-auto max-w-md text-sm leading-relaxed text-text-muted">
                    {step.description}
                  </p>
                </div>

                {/* Language selection for step 1 */}
                {step.id === "step-1" && (
                  <div className="grid grid-cols-2 gap-3">
                    {LANGUAGE_OPTIONS.map((lang) => (
                      <button
                        key={lang.id}
                        onClick={() => setSelectedLanguage(lang.id)}
                        className={`relative rounded-xl border-2 p-4 text-left transition-all ${
                          selectedLanguage === lang.id
                            ? "border-primary bg-mint"
                            : "border-border bg-surface hover:border-primary/40 hover:bg-surface-2"
                        }`}
                      >
                        <p className="font-display text-lg font-extrabold text-text">{lang.label}</p>
                        <p className="mt-1 text-xs text-text-muted">{lang.desc}</p>
                        {selectedLanguage === lang.id && (
                          <Check size={16} className="absolute right-2 top-2 text-primary-dark" />
                        )}
                      </button>
                    ))}
                  </div>
                )}

                {/* Action hint for non-conversion steps */}
                {step.type !== "conversion" && (
                  <div className="flex items-center gap-2 text-xs text-text-muted">
                    <ChevronRight size={14} className="shrink-0" />
                    <span>{step.action}</span>
                  </div>
                )}

                {/* XP reward badge */}
                <div className="flex items-center justify-center gap-2 text-sm font-semibold text-wood">
                  <Star size={14} className="text-reward" />
                  <span>+10 XP on completion</span>
                </div>

                {/* Action button */}
                <Button
                  variant={step.type === "conversion" ? "gold" : "primary"}
                  onClick={() => handleCompleteStep(step)}
                  disabled={submitting || (step.id === "step-1" && !selectedLanguage)}
                  size="lg"
                  fullWidth
                  loading={submitting}
                  rightIcon={<ArrowRight size={16} />}
                >
                  {step.id === "step-5" ? step.action : step.type === "action" ? step.action : "Let's Go!"}
                </Button>

                {/* Conversion pricing for step 5 */}
                {step.id === "step-5" && (
                  <div className="mt-2 space-y-3">
                    <div className="surface-border rounded-xl border p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-bold text-text">Pro Monthly</p>
                          <p className="text-xs text-text-muted">$9/month</p>
                        </div>
                        <span className="font-display text-lg font-extrabold text-primary-dark">$9</span>
                      </div>
                    </div>
                    <div className="rounded-xl border border-reward/50 bg-reward-soft/50 p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="flex items-center gap-2 text-sm font-bold text-text">
                            <Gem size={14} className="text-reward" />
                            Lifetime
                          </p>
                          <p className="text-xs text-text-muted">Lock in forever</p>
                        </div>
                        <span className="font-display text-lg font-extrabold text-wood">$39</span>
                      </div>
                    </div>
                    <div className="surface-border rounded-xl border p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="flex items-center gap-2 text-sm font-bold text-text">
                            <Star size={14} className="text-primary-dark" />
                            Student Discount
                          </p>
                          <p className="text-xs text-text-muted">50% off with .edu</p>
                        </div>
                        <span className="text-sm font-bold text-primary-dark">50% OFF</span>
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>
            </AnimatePresence>

            {/* Bottom navigation */}
            <div className="surface-border flex items-center justify-between border-t bg-surface-2 px-6 py-4">
              {currentStep > 0 ? (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setCurrentStep((s) => s - 1)}
                  leftIcon={<ArrowLeft size={14} />}
                >
                  Back
                </Button>
              ) : (
                <div className="w-20" />
              )}
              <Button variant="ghost" size="sm" onClick={handleSkip}>
                Skip onboarding
              </Button>
            </div>
          </motion.div>
        </div>
      </div>
    </PageShell>
  );
}
