import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { X, ArrowRight, ArrowLeft, Sparkles, Target, BarChart3 } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

const STEPS = [
  {
    icon: Sparkles,
    title: "Welcome to PlacementPro",
    description: "Your AI-powered placement preparation platform. Let's get you started in 30 seconds.",
    color: "text-purple-600",
    bg: "bg-purple-100 dark:bg-purple-900/30",
  },
  {
    icon: Target,
    title: "Practice Like the Real Thing",
    description: "AI interviews, coding challenges, aptitude tests, and company-specific prep — all tailored to your target role.",
    color: "text-emerald-600",
    bg: "bg-emerald-100 dark:bg-emerald-900/30",
  },
  {
    icon: BarChart3,
    title: "Track Your Progress",
    description: "See your skill radar, weak areas, and placement readiness score. Improve daily with streaks and XP.",
    color: "text-blue-600",
    bg: "bg-blue-100 dark:bg-blue-900/30",
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
      const timer = setTimeout(() => setShow(true), 1000);
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
      navigate("/dashboard");
    }
  };

  const prev = () => {
    if (step > 0) setStep(step - 1);
  };

  if (!show) return null;

  const current = STEPS[step];

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm px-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <motion.div
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-md w-full p-8 relative"
          initial={reduced ? {} : { scale: 0.9, y: 20 }}
          animate={{ scale: 1, y: 0 }}
          exit={reduced ? {} : { scale: 0.9, y: 20 }}
        >
          <button
            onClick={dismiss}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <X size={20} />
          </button>

          <div className="text-center mb-6">
            <div className={`w-16 h-16 ${current.bg} rounded-2xl flex items-center justify-center mx-auto mb-4`}>
              <current.icon size={32} className={current.color} />
            </div>
            <h2 className="text-2xl font-bold dark:text-white mb-2">{current.title}</h2>
            <p className="text-gray-600 dark:text-gray-400">{current.description}</p>
          </div>

          <div className="flex justify-center gap-2 mb-6">
            {STEPS.map((_, i) => (
              <div
                key={i}
                className={`h-2 rounded-full transition-all ${
                  i === step ? "w-8 bg-primary-600" : "w-2 bg-gray-300 dark:bg-gray-600"
                }`}
              />
            ))}
          </div>

          <div className="flex gap-3">
            {step > 0 && (
              <button
                onClick={prev}
                className="flex items-center gap-1 px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
              >
                <ArrowLeft size={16} /> Back
              </button>
            )}
            <button
              onClick={next}
              className="flex-1 flex items-center justify-center gap-2 bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
            >
              {step < STEPS.length - 1 ? (
                <>Next <ArrowRight size={16} /></>
              ) : (
                "Get Started"
              )}
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
