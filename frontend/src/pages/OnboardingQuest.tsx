import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight, ArrowLeft, Check, ChevronRight, Star,
  Crown, Gem,
} from "lucide-react";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import useReducedMotion from "../hooks/useReducedMotion";

const QUEST_STEPS = [
  {
    id: "step-1",
    title: "Choose Your Language",
    description: "Pick the language you want to learn. C, C++, Java, or Python — all paths lead to placement success.",
    type: "navigation",
    action: "Select a language from the learning hub",
    target: "/learn/c",
    icon: "\U0001f3af",
    iconLabel: "🎯",
  },
  {
    id: "step-2",
    title: "Write Your First Code",
    description: "Open the first lesson and run your first program. You will have code running in under 30 seconds.",
    type: "action",
    action: "Open any lesson and click Run",
    target: "/free-trial",
    icon: "\u2328\ufe0f",
    iconLabel: "⌨️",
  },
  {
    id: "step-3",
    title: "Earn Your First XP",
    description: "Complete the lesson and watch your progress climb. Gamification keeps you hooked.",
    type: "action",
    action: "Complete a lesson to earn XP",
    target: "/learn/c",
    icon: "\u2b50",
    iconLabel: "⭐",
  },
  {
    id: "step-4",
    title: "Track Your Streak",
    description: "Keep learning daily to build your streak multiplier. Consistency beats intensity.",
    type: "info",
    action: "Check your streak in the dashboard",
    target: "/dashboard",
    icon: "\U0001f525",
    iconLabel: "🔥",
  },
  {
    id: "step-5",
    title: "Go Pro for Unlimited Access",
    description: "Free users get 3 lessons per month. Pro unlocks everything for $9/mo or lock in lifetime for $39.",
    type: "conversion",
    action: "Upgrade to Pro",
    target: "/pricing",
    icon: "\U0001f680",
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
      <div className="relative min-h-screen flex items-center justify-center">
        <ArcadeBackdrop variant="arcade" />
        <div className="relative z-10 flex flex-col items-center gap-4">
          <div className="w-10 h-10 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-gray-400 font-mono text-sm">Loading your quest...</p>
        </div>
      </div>
    );
  }

  const steps = questData?.steps || QUEST_STEPS;
  const step = steps[currentStep] || steps[0];
  const totalSteps = steps.length;
  const progress = status?.overall_progress || Math.round(((currentStep) / totalSteps) * 100);

  return (
    <div className="relative min-h-screen flex items-center justify-center px-4 py-12">
      <ArcadeBackdrop variant="candy" />

      <div className="relative z-10 w-full max-w-lg">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="glass rounded-2xl border border-white/10 overflow-hidden"
        >
          {/* Progress bar */}
          <div className="px-6 pt-5 pb-3">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-mono text-gray-500">
                Step {currentStep + 1} of {totalSteps}
              </span>
              <span className="text-xs font-mono text-indigo-400">{progress}%</span>
            </div>
            <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"
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
              className="px-6 pb-6 space-y-6"
            >
              {/* Icon */}
              <div className="text-center">
                <motion.div
                  initial={{ scale: 0, rotate: -20 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.1 }}
                  className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-white/10 flex items-center justify-center text-4xl"
                >
                  {step.iconLabel}
                </motion.div>
              </div>

              {/* Title & Description */}
              <div className="text-center">
                <h2 className="text-2xl font-display font-bold text-white mb-2">
                  {step.title}
                </h2>
                <p className="text-sm text-gray-400 leading-relaxed">
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
                          ? "border-indigo-500 bg-indigo-500/10 shadow-lg shadow-indigo-500/20"
                          : "border-white/10 bg-white/5 hover:border-white/20"
                      }`}
                    >
                      <div className={`absolute inset-0 rounded-xl bg-gradient-to-br ${lang.color} opacity-10`} />
                      <p className="relative text-lg font-bold text-white">{lang.label}</p>
                      <p className="relative text-xs text-gray-400 mt-1">{lang.desc}</p>
                      {selectedLanguage === lang.id && (
                        <Check size={16} className="absolute top-2 right-2 text-indigo-400" />
                      )}
                    </button>
                  ))}
                </div>
              )}

              {/* Action hint for non-conversion steps */}
              {step.type !== "conversion" && (
                <div className="flex items-center gap-2 text-xs text-gray-500">
                  <ChevronRight size={14} className="shrink-0" />
                  <span>{step.action}</span>
                </div>
              )}

              {/* XP reward badge */}
              <div className="flex items-center justify-center gap-2 text-sm">
                <Star size={14} className="text-yellow-400" />
                <span className="text-gray-400">+10 XP on completion</span>
              </div>

              {/* Action button */}
              <button
                onClick={() => handleCompleteStep(step)}
                disabled={submitting || (step.id === "step-1" && !selectedLanguage)}
                className="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-bold text-sm transition-all bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-lg shadow-indigo-500/20 disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {submitting ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : step.id === "step-5" ? (
                  <>
                    <Crown size={16} />
                    {step.action}
                  </>
                ) : step.type === "action" ? (
                  <>
                    {step.action}
                    <ArrowRight size={16} />
                  </>
                ) : (
                  <>
                    Let's Go!
                    <ArrowRight size={16} />
                  </>
                )}
              </button>

              {/* Conversion pricing for step 5 */}
              {step.id === "step-5" && (
                <div className="space-y-3 mt-2">
                  <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10">
                    <div>
                      <p className="text-sm font-semibold text-white">Pro Monthly</p>
                      <p className="text-xs text-gray-500">$9/month</p>
                    </div>
                    <span className="text-lg font-bold text-cyan-400">$9</span>
                  </div>
                  <div className="flex items-center justify-between p-4 rounded-xl bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border border-indigo-500/30">
                    <div>
                      <p className="text-sm font-semibold text-white flex items-center gap-2">
                        <Gem size={14} className="text-yellow-400" />
                        Lifetime
                      </p>
                      <p className="text-xs text-gray-500">Lock in forever</p>
                    </div>
                    <span className="text-lg font-bold text-yellow-400">$39</span>
                  </div>
                  <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10">
                    <div>
                      <p className="text-sm font-semibold text-white flex items-center gap-2">
                        <Star size={14} className="text-emerald-400" />
                        Student Discount
                      </p>
                      <p className="text-xs text-gray-500">50% off with .edu</p>
                    </div>
                    <span className="text-sm font-bold text-emerald-400">50% OFF</span>
                  </div>
                </div>
              )}
            </motion.div>
          </AnimatePresence>

          {/* Bottom navigation */}
          <div className="flex items-center justify-between px-6 py-4 border-t border-white/5">
            {currentStep > 0 ? (
              <button
                onClick={() => setCurrentStep((s) => s - 1)}
                className="flex items-center gap-1 text-sm text-gray-400 hover:text-white transition-colors"
              >
                <ArrowLeft size={14} /> Back
              </button>
            ) : (
              <div />
            )}
            <button
              onClick={handleSkip}
              className="text-xs font-mono text-gray-500 hover:text-gray-300 transition-colors"
            >
              Skip onboarding
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}