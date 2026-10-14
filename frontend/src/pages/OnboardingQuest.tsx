// @ts-nocheck
import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, ArrowLeft, Check, Sparkles, Rocket } from "lucide-react";
import { authApi } from "../services/api/auth";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";

type Step = "welcome" | "identity" | "goal" | "experience" | "time" | "done";

type Identity = "student" | "professional" | "switcher" | "beginner";
type Goal = "campus" | "service" | "product" | "freelance" | "exploring";
type Experience = "none" | "basic" | "intermediate" | "advanced";
type Time = "5min" | "15min" | "30min" | "60min";

const IDENTITIES = [
  { id: "student", label: "Student", desc: "College, campus placements, first job hunt", icon: "🎓" },
  { id: "professional", label: "Professional", desc: "Currently working, leveling up", icon: "💼" },
  { id: "switcher", label: "Career Switcher", desc: "Moving into tech from another field", icon: "🔄" },
  { id: "beginner", label: "Total Beginner", desc: "Never coded before, starting fresh", icon: "🌱" },
];

const GOALS = [
  { id: "campus", label: "Campus Placement", desc: "TCS, Infosys, Wipro, campus drives", icon: "🏆" },
  { id: "service", label: "Service Company", desc: "TCS, Infosys, Wipro, Cognizant", icon: "🏢" },
  { id: "product", label: "Product Company", desc: "SDE at Amazon, Google, Microsoft", icon: "💻" },
  { id: "freelance", label: "Freelance / Startup", desc: "Build products or services", icon: "🚀" },
  { id: "exploring", label: "Just Exploring", desc: "Figure out what fits", icon: "🧭" },
];

const EXPERIENCES = [
  { id: "none", label: "Never coded", desc: "Starting from absolute zero", icon: "🌱" },
  { id: "basic", label: "Some basics", desc: "I've written simple programs", icon: "🌿" },
  { id: "intermediate", label: "Comfortable", desc: "I can solve problems independently", icon: "💪" },
  { id: "advanced", label: "Strong coder", desc: "Interviews and advanced topics", icon: "🔥" },
];

const TIME_OPTIONS = [
  { id: "5min", label: "5 min/day", desc: "Micro sessions", icon: "⚡" },
  { id: "15min", label: "15 min/day", desc: "Steady pace", icon: "🔥" },
  { id: "30min", label: "30 min/day", desc: "Focused practice", icon: "🎯" },
  { id: "60min", label: "60 min/day", desc: "Deep work", icon: "🚀" },
];

const STEPS = ["identity", "goal", "experience", "time"];

export default function OnboardingQuest() {
  const [step, setStep] = useState<Step>("welcome");
  const [identity, setIdentity] = useState<Identity | null>(null);
  const [goal, setGoal] = useState<Goal | null>(null);
  const [experience, setExperience] = useState<Experience | null>(null);
  const [time, setTime] = useState<Time | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const progress = step === "welcome" ? 0 : step === "done" ? 100 : STEPS.indexOf(step) + 1;

  const persistAndGo = useCallback(async () => {
    setSubmitting(true);
    try {
      await authApi.onboardingComplete({
        klass: identity,
        target_role: goal,
        daily_minutes: time,
        prep_level: experience,
        skill_self_assessment: { identity, goal, experience, time },
      } as never);
    } catch {
      // never block journey on network
    }
    setSubmitting(false);
    navigate("/placement", { replace: true });
  }, [identity, goal, experience, time, navigate]);

  const canProceed = () => {
    switch (step) {
      case "identity":
        return identity !== null;
      case "goal":
        return goal !== null;
      case "experience":
        return experience !== null;
      case "time":
        return time !== null;
      default:
        return true;
    }
  };

  const handleNext = () => {
    switch (step) {
      case "identity":
        setStep("goal");
        break;
      case "goal":
        setStep("experience");
        break;
      case "experience":
        setStep("time");
        break;
      case "time":
        setStep("done");
        break;
      case "welcome":
        setStep("identity");
        break;
    }
  };

  const handleBack = () => {
    switch (step) {
      case "goal":
        setStep("identity");
        break;
      case "experience":
        setStep("goal");
        break;
      case "time":
        setStep("experience");
        break;
    }
  };

  return (
    <PageShell theme="spring">
      <div className="flex min-h-screen items-center justify-center px-4 py-12">
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-lg"
        >
          {step !== "done" && (
            <div className="mb-8">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono uppercase tracking-widest text-text-muted">
                  {step === "welcome" ? "Start" : `Step ${STEPS.indexOf(step) + 1} of ${STEPS.length}`}
                </span>
                <span className="text-[10px] font-mono text-text-muted">{Math.round((progress / STEPS.length) * 100)}%</span>
              </div>
              <div className="h-1.5 w-full rounded-full bg-black/5 overflow-hidden">
                <motion.div
                  className="h-full rounded-full bg-[#C96F3D]"
                  initial={{ width: 0 }}
                  animate={{ width: `${(progress / STEPS.length) * 100}%` }}
                  transition={{ duration: 0.4, ease: "easeOut" }}
                />
              </div>
            </div>
          )}

          <AnimatePresence mode="wait">
            {step === "welcome" && (
              <motion.div
                key="welcome"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={reduced ? {} : { opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className="text-center"
              >
                <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-[#17263B] to-[#C96F3D] text-white">
                  <Rocket size={28} />
                </div>
                <h2 className="font-display text-3xl font-extrabold text-text mb-3">
                  Welcome to BountyCode
                </h2>
                <p className="text-sm text-text-muted mb-8 max-w-sm mx-auto">
                  Tell us a little about yourself and we'll build your personalized prep plan in 60 seconds.
                </p>
                <Button
                  variant="primary"
                  size="xl"
                  fullWidth
                  onClick={handleNext}
                  rightIcon={<ArrowRight size={18} />}
                >
                  Let's go
                </Button>
              </motion.div>
            )}

            {step === "identity" && (
              <motion.div
                key="identity"
                initial={reduced ? {} : { opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={reduced ? {} : { opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <div className="text-center mb-6">
                  <h2 className="font-display text-2xl font-extrabold text-text">Who are you?</h2>
                  <p className="mt-2 text-sm text-text-muted">Pick the closest fit.</p>
                </div>
                <div className="grid grid-cols-2 gap-3 mb-6">
                  {IDENTITIES.map((item) => (
                    <motion.button
                      key={item.id}
                      initial={reduced ? {} : { opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.03 }}
                      onClick={() => setIdentity(item.id)}
                      className={`rounded-2xl border-2 p-4 text-left transition-all ${
                        identity === item.id ? "border-[#C96F3D] bg-[#C96F3D]/5" : "border-border hover:border-[#C96F3D]/30"
                      }`}
                    >
                      <span className="text-2xl mb-2 block">{item.icon}</span>
                      <p className="font-display font-bold text-text text-sm">{item.label}</p>
                      <p className="text-[11px] text-text-muted mt-1 leading-snug">{item.desc}</p>
                      {identity === item.id && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="mt-3 h-5 w-5 rounded-full bg-[#C96F3D] flex items-center justify-center"
                        >
                          <Check size={12} className="text-white" />
                        </motion.div>
                      )}
                    </motion.button>
                  ))}
                </div>
                <div className="flex justify-between">
                  <Button variant="ghost" onClick={handleBack} disabled={step === "identity"}>
                    <ArrowLeft size={14} /> Back
                  </Button>
                  <Button variant="primary" disabled={!identity} onClick={handleNext} rightIcon={<ArrowRight size={16} />}>
                    Continue
                  </Button>
                </div>
              </motion.div>
            )}

            {step === "goal" && (
              <motion.div
                key="goal"
                initial={reduced ? {} : { opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={reduced ? {} : { opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <div className="text-center mb-6">
                  <h2 className="font-display text-2xl font-extrabold text-text">What's your main goal?</h2>
                  <p className="mt-2 text-sm text-text-muted">We'll tailor your plan around this.</p>
                </div>
                <div className="space-y-3 mb-6">
                  {GOALS.map((item) => (
                    <motion.button
                      key={item.id}
                      initial={reduced ? {} : { opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.03 }}
                      onClick={() => setGoal(item.id)}
                      className={`w-full rounded-2xl border-2 p-4 text-left transition-all ${
                        goal === item.id ? "border-[#C96F3D] bg-[#C96F3D]/5" : "border-border hover:border-[#C96F3D]/30"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{item.icon}</span>
                        <div className="flex-1">
                          <p className="font-display font-bold text-text text-sm">{item.label}</p>
                          <p className="text-[11px] text-text-muted">{item.desc}</p>
                        </div>
                        {goal === item.id && (
                          <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="h-5 w-5 rounded-full bg-[#C96F3D] flex items-center justify-center shrink-0"
                          >
                            <Check size={12} className="text-white" />
                          </motion.div>
                        )}
                      </div>
                    </motion.button>
                  ))}
                </div>
                <div className="flex justify-between">
                  <Button variant="ghost" onClick={handleBack}>
                    <ArrowLeft size={14} /> Back
                  </Button>
                  <Button variant="primary" disabled={!goal} onClick={handleNext} rightIcon={<ArrowRight size={16} />}>
                    Continue
                  </Button>
                </div>
              </motion.div>
            )}

            {step === "experience" && (
              <motion.div
                key="experience"
                initial={reduced ? {} : { opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={reduced ? {} : { opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <div className="text-center mb-6">
                  <h2 className="font-display text-2xl font-extrabold text-text">Coding experience?</h2>
                  <p className="mt-2 text-sm text-text-muted">Be honest — we adapt to your level.</p>
                </div>
                <div className="grid grid-cols-2 gap-3 mb-6">
                  {EXPERIENCES.map((item) => (
                    <motion.button
                      key={item.id}
                      initial={reduced ? {} : { opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.03 }}
                      onClick={() => setExperience(item.id)}
                      className={`rounded-2xl border-2 p-4 text-left transition-all ${
                        experience === item.id ? "border-[#C96F3D] bg-[#C96F3D]/5" : "border-border hover:border-[#C96F3D]/30"
                      }`}
                    >
                      <span className="text-2xl mb-2 block">{item.icon}</span>
                      <p className="font-display font-bold text-text text-sm">{item.label}</p>
                      <p className="text-[11px] text-text-muted mt-1 leading-snug">{item.desc}</p>
                      {experience === item.id && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="mt-3 h-5 w-5 rounded-full bg-[#C96F3D] flex items-center justify-center"
                        >
                          <Check size={12} className="text-white" />
                        </motion.div>
                      )}
                    </motion.button>
                  ))}
                </div>
                <div className="flex justify-between">
                  <Button variant="ghost" onClick={handleBack}>
                    <ArrowLeft size={14} /> Back
                  </Button>
                  <Button variant="primary" disabled={!experience} onClick={handleNext} rightIcon={<ArrowRight size={16} />}>
                    Continue
                  </Button>
                </div>
              </motion.div>
            )}

            {step === "time" && (
              <motion.div
                key="time"
                initial={reduced ? {} : { opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={reduced ? {} : { opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <div className="text-center mb-6">
                  <h2 className="font-display text-2xl font-extrabold text-text">How much time daily?</h2>
                  <p className="mt-2 text-sm text-text-muted">We'll build a plan that fits your schedule.</p>
                </div>
                <div className="grid grid-cols-2 gap-3 mb-6">
                  {TIME_OPTIONS.map((item) => (
                    <motion.button
                      key={item.id}
                      initial={reduced ? {} : { opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.03 }}
                      onClick={() => setTime(item.id)}
                      className={`rounded-2xl border-2 p-4 text-left transition-all ${
                        time === item.id ? "border-[#C96F3D] bg-[#C96F3D]/5" : "border-border hover:border-[#C96F3D]/30"
                      }`}
                    >
                      <span className="text-2xl mb-2 block">{item.icon}</span>
                      <p className="font-display font-bold text-text text-sm">{item.label}</p>
                      <p className="text-[11px] text-text-muted mt-1">{item.desc}</p>
                      {time === item.id && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="mt-3 h-5 w-5 rounded-full bg-[#C96F3D] flex items-center justify-center"
                        >
                          <Check size={12} className="text-white" />
                        </motion.div>
                      )}
                    </motion.button>
                  ))}
                </div>
                <div className="flex justify-between">
                  <Button variant="ghost" onClick={handleBack}>
                    <ArrowLeft size={14} /> Back
                  </Button>
                  <Button
                    variant="primary"
                    size="xl"
                    disabled={!time}
                    onClick={handleNext}
                    rightIcon={<Sparkles size={18} />}
                  >
                    Build My Plan
                  </Button>
                </div>
              </motion.div>
            )}

            {step === "done" && (
              <motion.div
                key="done"
                initial={reduced ? {} : { opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center py-8"
              >
                <motion.div
                  initial={reduced ? {} : { scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 200, damping: 15 }}
                  className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-[#17263B] to-[#C96F3D] text-white"
                >
                  <Sparkles size={28} />
                </motion.div>
                <h2 className="font-display text-2xl font-extrabold text-text mb-2">You're all set</h2>
                <p className="text-sm text-text-muted mb-6 max-w-xs mx-auto">
                  Your personalized prep plan is ready. Redirecting you now...
                </p>
                <Button
                  variant="primary"
                  size="xl"
                  fullWidth
                  onClick={persistAndGo}
                  loading={submitting}
                  rightIcon={<ArrowRight size={18} />}
                >
                  Start Now
                </Button>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </PageShell>
  );
}
