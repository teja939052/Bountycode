import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { X, ArrowRight, ArrowLeft, Flame, Trophy, Code, Target, Rocket } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

const STEPS = [
  {
    icon: Rocket,
    title: "Welcome to PlacementPro",
    description: "Your AI-powered placement command center. Let's get you mission-ready in 30 seconds.",
    color: "text-cyber-blue",
    bg: "bg-cyber-blue/10",
    action: null,
  },
  {
    icon: Code,
    title: "584+ Problems Await",
    description: "Coding, aptitude, system design, behavioral — all tagged with 53 companies. Solve, earn XP, level up.",
    color: "text-cyber-green",
    bg: "bg-cyber-green/10",
    action: { label: "Try a Problem", to: "/questions" },
  },
  {
    icon: Flame,
    title: "Build Your Streak",
    description: "Practice daily to maintain your streak. Streak freezes protect your chain when life happens.",
    color: "text-orange-400",
    bg: "bg-orange-400/10",
    action: { label: "Start Daily Drill", to: "/daily-drill" },
  },
  {
    icon: Target,
    title: "Mock Interviews with AI",
    description: "Real-time feedback, score tracking, and company-specific prep. Practice like it's the real thing.",
    color: "text-cyber-purple",
    bg: "bg-cyber-purple/10",
    action: { label: "Try an Interview", to: "/interview" },
  },
  {
    icon: Trophy,
    title: "Climb the Tower",
    description: "100 levels, 10 boss battles, power-ups, and a wizard that evolves with you. Your progress, visualized.",
    color: "text-yellow-400",
    bg: "bg-yellow-400/10",
    action: { label: "Enter the Tower", to: "/tower" },
  },
];

const STORAGE_KEY = "placementpro_onboarded";

export default function Onboarding() {
  const [step, setStep] = useState(0);
  const [show, setShow] = useState(false);
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  useEffect(() => {
    const onboarded = localStorage.getItem(STORAGE_KEY);
    if (!onboarded) {
      const timer = setTimeout(() => setShow(true), 800);
      return () => clearTimeout(timer);
    }
  }, []);

  const dismiss = () => {
    localStorage.setItem(STORAGE_KEY, "true");
    setShow(false);
  };

  const next = () => {
    if (step < STEPS.length - 1) {
      setStep(step + 1);
    } else {
      dismiss();
    }
  };

  const prev = () => {
    if (step > 0) setStep(step - 1);
  };

  const handleAction = (to) => {
    dismiss();
    navigate(to);
  };

  if (!show) return null;

  const current = STEPS[step];
  const Icon = current.icon;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md px-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <motion.div
          className="glass rounded-2xl max-w-md w-full p-8 relative border border-space-border"
          initial={reduced ? {} : { scale: 0.9, y: 20 }}
          animate={{ scale: 1, y: 0 }}
          exit={reduced ? {} : { scale: 0.9, y: 20 }}
          transition={{ type: 'spring', stiffness: 300, damping: 25 }}
        >
          <button
            onClick={dismiss}
            className="absolute top-4 right-4 text-gray-500 hover:text-gray-300 transition-colors"
          >
            <X size={20} />
          </button>

          <div className="text-center mb-6">
            <motion.div
              key={step}
              initial={reduced ? {} : { scale: 0, rotate: -20 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: 'spring', stiffness: 400, damping: 15 }}
              className={`w-16 h-16 ${current.bg} rounded-2xl flex items-center justify-center mx-auto mb-4`}
            >
              <Icon size={32} className={current.color} />
            </motion.div>
            <h2 className="text-xl font-display font-bold text-text-primary mb-2">{current.title}</h2>
            <p className="text-gray-400 font-mono text-sm leading-relaxed">{current.description}</p>
          </div>

          {/* Progress dots */}
          <div className="flex justify-center gap-2 mb-6">
            {STEPS.map((_, i) => (
              <motion.div
                key={i}
                className={`h-1.5 rounded-full transition-all ${
                  i === step ? "w-8 bg-cyber-blue" : i < step ? "w-1.5 bg-cyber-blue/40" : "w-1.5 bg-gray-600"
                }`}
                layout
              />
            ))}
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            {step > 0 && (
              <button
                onClick={prev}
                className="flex items-center gap-1 px-4 py-2.5 text-gray-400 hover:text-gray-200 font-mono text-sm transition-colors"
              >
                <ArrowLeft size={14} /> Back
              </button>
            )}
            <button
              onClick={next}
              className="flex-1 flex items-center justify-center gap-2 btn-primary py-3"
            >
              {step < STEPS.length - 1 ? (
                <>Next <ArrowRight size={16} /></>
              ) : (
                "Launch Mission"
              )}
            </button>
          </div>

          {/* Quick action link */}
          {current.action && (
            <button
              onClick={() => handleAction(current.action.to)}
              className="w-full mt-3 text-xs font-mono text-gray-500 hover:text-cyber-blue transition-colors"
            >
              Skip to {current.action.label} →
            </button>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
