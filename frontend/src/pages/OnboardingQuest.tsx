import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight, ArrowLeft, Check, ChevronRight, Star,
  Crown, Gem, Leaf, Target, Sparkles,
} from "lucide-react";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import useReducedMotion from "../hooks/useReducedMotion";
import { Button } from "../design-system/components";

const QUEST_STEPS = [
  {
    id: "step-1",
    title: "Choose Your Language",
    description: "Pick the language you want to learn. C, C++, Java, or Python — all paths lead to placement success.",
    type: "navigation",
    action: "Select a language from the learning hub",
    target: "/learn/c",
    icon: "🎯",
    iconLabel: "🎯",
  },
  {
    id: "step-2",
    title: "Write Your First Code",
    description: "Open the first lesson and run your first program. You will have code running in under 30 seconds.",
    type: "action",
    action: "Open any lesson and click Run",
    target: "/free-trial",
    icon: "⌨️",
    iconLabel: "⌨️",
  },
  {
    id: "step-3",
    title: "Earn Your First XP",
    description: "Complete the lesson and watch your progress climb. Gamification keeps you hooked.",
    type: "action",
    action: "Complete a lesson to earn XP",
    target: "/learn/c",
    icon: "⭐",
    iconLabel: "⭐",
  },
  {
    id: "step-4",
    title: "Track Your Streak",
    description: "Keep learning daily to build your streak multiplier. Consistency beats intensity.",
    type: "info",
    action: "Check your streak in the dashboard",
    target: "/dashboard",
    icon: "🔥",
    iconLabel: "🔥",
  },
  {
    id: "step-5",
    title: "Go Pro for Unlimited Access",
    description: "Free users get 3 lessons per month. Pro unlocks everything for $9/mo or lock in lifetime for $39.",
    type: "conversion",
    action: "Upgrade to Pro",
    target: "/pricing",
    icon: "🚀",
    iconLabel: "🚀",
  },
];

const LANGUAGE_OPTIONS = [
  { id: "c", label: "C", desc: "Systems programming", color: "from-blue-500 to-cyan-500" },
  { id: "cpp", label: "C++", desc: "Competitive programming", color: "from-emerald-500 to-teal-500" },
  { id: "java", label: "Java", desc: "Enterprise & Android", color: "from-amber-500 to-orange-500" },
  { id: "python", label: "Python", desc: "AI, Data & Automation", color: "from-purple-500 to-pink-500" },
];

export default function OnboardingQuest() {
  const [currentStep, setCurrentStep] = useState(0);
  const [questData, setQuestData] = useState(null);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedLanguage, setSelectedLanguage] = useState(null);
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
        const steps = questRes.quest?.steps || questRes.steps || QUEST_STEPS;
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
  }, []);

  const handleCompleteStep = useCallback(
    async (step) => {
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
      <div className="min-h-screen flex items-center justify-center bg-background-primary">
        <div className="flex flex-col items-center gap-4">
          <div className="w-10 h-10 border-2 border-brand-primary border-t-transparent rounded-full animate-spin" />
          <p className="text-text-secondary font-mono text-sm">Loading your journey...</p>
        </div>
      </div>
    );
  }

  const steps = questData?.steps || QUEST_STEPS;
  const step = steps[currentStep] || steps[0];
  const totalSteps = steps.length;
  const progress = status?.overall_progress || Math.round(((currentStep) / totalSteps) * 100);

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-background-primary">
      {/* Subtle ambient nature */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-20 left-8 w-32 h-32 rounded-full bg-brand-mint/30 blur-3xl" />
        <div className="absolute bottom-20 right-8 w-24 h-24 rounded-full bg-brand-mint/20 blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 rounded-full bg-brand-mint/10 blur-3xl" />
      </div>

      <div className="relative z-10 w-full max-w-lg">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="rounded-2xl border border-border-primary bg-background-surface shadow-soft-lg overflow-hidden"
        >
          {/* Progress bar */}
          <div className="px-6 pt-5 pb-3 border-b border-border-primary">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-mono text-text-secondary uppercase tracking-wider">
                Step {currentStep + 1} of {totalSteps}
              </span>
              <span className="text-xs font-mono text-brand-primary font-semibold">{progress}%</span>
            </div>
            <div className="w-full h-1.5 bg-background-secondary rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-brand-primary to-brand-deep rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.6, ease: "easeOut" }}
              />
            </div>
          </div>

          {/* Step content */}
          <AnimatePresence mode="wait">
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -30 }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
              className="px-6 py-6 space-y-6"
            >
              {/* Icon */}
              <div className="text-center">
                <motion.div
                  initial={{ scale: 0, rotate: -20 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.1 }}
                  className="w-20 h-20 mx-auto rounded-2xl bg-brand-mint border border-brand-primary/20 flex items-center justify-center text-4xl"
                >
                  {step.iconLabel}
                </motion.div>
              </div>

              {/* Title & Description */}
              <div className="text-center">
                <h2 className="text-2xl font-display font-bold text-text-primary mb-2">
                  {step.title}
                </h2>
                <p className="text-sm text-text-secondary leading-relaxed max-w-md mx-auto">
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
                      className={`relative p-4 rounded-xl border-2 text-left transition-all ${
                        selectedLanguage === lang.id
                          ? "border-brand-primary bg-brand-mint/30 shadow-glow"
                          : "border-border-primary bg-background-surface hover:border-brand-primary/30 hover:bg-brand-mint/10"
                      }`}
                    >
                      <div className={`absolute inset-0 rounded-xl bg-gradient-to-br ${lang.color} opacity-10`} />
                      <p className="relative text-lg font-bold text-text-primary">{lang.label}</p>
                      <p className="relative text-xs text-text-secondary mt-1">{lang.desc}</p>
                      {selectedLanguage === lang.id && (
                        <Check size={16} className="absolute top-2 right-2 text-brand-primary" />
                      )}
                    </button>
                  ))}
                </div>
              )}

              {/* Action hint for non-conversion steps */}
              {step.type !== "conversion" && (
                <div className="flex items-center gap-2 text-xs text-text-secondary">
                  <ChevronRight size={14} className="shrink-0" />
                  <span>{step.action}</span>
                </div>
              )}

              {/* XP reward badge */}
              <div className="flex items-center justify-center gap-2 text-sm text-text-secondary">
                <Star size={14} className="text-semantic-xp" />
                <span>+10 XP on completion</span>
              </div>

              {/* Action button */}
              <Button
                onClick={() => handleCompleteStep(step)}
                disabled={submitting || (step.id === "step-1" && !selectedLanguage)}
                size="lg"
                fullWidth
                loading={submitting}
                rightIcon={step.id === "step-5" ? <Crown size={16} /> : step.type === "action" ? <ArrowRight size={16} /> : <ArrowRight size={16} />}
              >
                {step.id === "step-5" ? step.action : step.type === "action" ? step.action : "Let's Go!"}
              </Button>

              {/* Conversion pricing for step 5 */}
              {step.id === "step-5" && (
                <div className="space-y-3 mt-2">
                  <div className="p-4 rounded-xl border border-border-primary bg-background-surfaceSecondary">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-text-primary">Pro Monthly</p>
                        <p className="text-xs text-text-secondary">$9/month</p>
                      </div>
                      <span className="text-lg font-bold text-brand-primary">$9</span>
                    </div>
                  </div>
                  <div className="p-4 rounded-xl border border-brand-primary/30 bg-brand-mint/20">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-text-primary flex items-center gap-2">
                          <Gem size={14} className="text-semantic-achievement" />
                          Lifetime
                        </p>
                        <p className="text-xs text-text-secondary">Lock in forever</p>
                      </div>
                      <span className="text-lg font-bold text-semantic-achievement">$39</span>
                    </div>
                  </div>
                  <div className="p-4 rounded-xl border border-border-primary bg-background-surfaceSecondary">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-text-primary flex items-center gap-2">
                          <Star size={14} className="text-semantic-success" />
                          Student Discount
                        </p>
                        <p className="text-xs text-text-secondary">50% off with .edu</p>
                      </div>
                      <span className="text-sm font-bold text-semantic-success">50% OFF</span>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          </AnimatePresence>

          {/* Bottom navigation */}
          <div className="flex items-center justify-between px-6 py-4 border-t border-border-primary bg-background-surfaceSecondary/50">
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
            <Button
              variant="ghost"
              size="sm"
              onClick={handleSkip}
              className="text-xs font-mono"
            >
              Skip onboarding
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}