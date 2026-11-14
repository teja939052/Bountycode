import { useState, useEffect, useCallback, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight,
  ArrowLeft,
  Check,
  CheckCircle2,
  Rocket,
  Code2,
  Laptop,
  Target,
  Code,
  Shield,
  Brain,
  Zap,
  Lock,
  Database,
  Briefcase,
  Sparkles,
  ArrowUpRight,
  User,
  RefreshCw,
} from "lucide-react";
import api from "../services/api";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";

type Step = "welcome" | "goals" | "interests" | "dashboard";

const GOALS = [
  {
    id: "internship",
    label: "Get an Internship",
    desc: "Land your first internship",
    icon: Briefcase,
  },
  {
    id: "placements",
    label: "Prepare for Placements",
    desc: "Campus placement prep",
    icon: Target,
  },
  {
    id: "learning",
    label: "Learn Programming",
    desc: "Build coding fundamentals",
    icon: Code2,
  },
  {
    id: "hackathons",
    label: "Participate in Hackathons",
    desc: "Build and ship projects",
    icon: Zap,
  },
  {
    id: "full_stack",
    label: "Become a Full Stack Developer",
    desc: "Frontend + backend",
    icon: Laptop,
  },
  {
    id: "ai_ml",
    label: "Explore AI and Machine Learning",
    desc: "AI/ML career path",
    icon: Brain,
  },
];

const TECHS = [
  { id: "java", label: "Java", icon: Code },
  { id: "python", label: "Python", icon: Code },
  { id: "javascript", label: "JavaScript", icon: Code },
  { id: "react", label: "React", icon: Code },
  { id: "nodejs", label: "Node.js", icon: Code },
  { id: "spring_boot", label: "Spring Boot", icon: Shield },
  { id: "dsa", label: "Data Structures & Algorithms", icon: Shield },
  { id: "ai", label: "Artificial Intelligence", icon: Brain },
  { id: "ml", label: "Machine Learning", icon: Brain },
  { id: "cybersecurity", label: "Cybersecurity", icon: Lock },
  { id: "data_science", label: "Data Science", icon: Database },
];

const GOAL_ICONS: Record<string, React.ComponentType<any>> = {
  internship: Briefcase,
  placements: Target,
  learning: Code2,
  hackathons: Zap,
  full_stack: Laptop,
  ai_ml: Brain,
};

const TECH_LABELS: Record<string, string> = {
  java: "Java",
  python: "Python",
  javascript: "JavaScript",
  react: "React",
  nodejs: "Node.js",
  spring_boot: "Spring Boot",
  dsa: "Data Structures & Algorithms",
  ai: "Artificial Intelligence",
  ml: "Machine Learning",
  cybersecurity: "Cybersecurity",
  data_science: "Data Science",
};

const LEARNING_PATHS: Record<string, { title: string; desc: string; to: string }> = {
  internship: {
    title: "Internship Ready",
    desc: "Resume + DSA + mock interviews to land your first internship.",
    to: "/internship-prep",
  },
  placements: {
    title: "Placement Prep",
    desc: "Company-wise questions, aptitude, and interview tracks.",
    to: "/placements",
  },
  learning: {
    title: "Learn to Code",
    desc: "Step-by-step lessons across 7 languages.",
    to: "/learn",
  },
  hackathons: {
    title: "Hackathon Builder",
    desc: "Project templates and rapid prototyping tracks.",
    to: "/projects",
  },
  full_stack: {
    title: "Full Stack Track",
    desc: "React, Node.js, and database fundamentals.",
    to: "/fullstack",
  },
  ai_ml: {
    title: "AI & Machine Learning",
    desc: "Python, ML models, and AI engineering fundamentals.",
    to: "/ai-ml",
  },
};

export default function OnboardingFlow({ onComplete, inline }: { onComplete?: () => void; inline?: boolean } = {}) {
  const navigate = useNavigate();
  const reduced = useReducedMotion();
  const [step, setStep] = useState<Step>("welcome");
  const [goals, setGoals] = useState<string[]>([]);
  const [interests, setInterests] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [finished, setFinished] = useState(false);

  // When inline (opened from Profile "Change"), never auto-redirect so the user
  // can actually see and fill out the form. On the standalone /onboarding route,
  // auto-redirect completed users to /dashboard.
  const skipRedirect = !!inline;

  const toggleGoal = useCallback((id: string) => {
    setGoals((prev) => (prev.includes(id) ? prev.filter((g) => g !== id) : [...prev, id]));
  }, []);

  const toggleInterest = useCallback((id: string) => {
    setInterests((prev) => (prev.includes(id) ? prev.filter((t) => t !== id) : [...prev, id]));
  }, []);

  useEffect(() => {
    let mounted = true;
    async function load() {
      try {
        const prefs = await api.onboarding.getPreferences();
        if (mounted) {
          setGoals(prefs.career_goals || []);
          setInterests(prefs.tech_interests || []);
          if (!skipRedirect && prefs.completed) {
            navigate("/dashboard", { replace: true });
          }
        }
      } catch {
        // Preferences may not exist yet — start fresh.
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => {
      mounted = false;
    };
  }, [navigate, skipRedirect]);

  const savePrefs = useCallback(async () => {
    setSaving(true);
    setError(null);
    try {
      await api.onboarding.savePreferences({ career_goals: goals, tech_interests: interests });
    } catch (err) {
      setError("Failed to save preferences. You can continue anyway.");
    } finally {
      setSaving(false);
    }
  }, [goals, interests]);

  const completeOnboarding = useCallback(async () => {
    setSaving(true);
    setError(null);
    try {
      await api.auth.onboardingComplete({
        career_goals: goals,
        tech_interests: interests,
      });
      setFinished(true);
      if (inline && onComplete) {
        onComplete();
      } else {
        navigate("/dashboard", { replace: true });
      }
    } catch (err) {
      setError("Failed to complete onboarding. Please try again.");
    } finally {
      setSaving(false);
    }
  }, [goals, interests, navigate]);

  const skipOnboarding = useCallback(async () => {
    setSaving(true);
    setError(null);
    try {
      await api.auth.onboardingComplete({
        career_goals: [],
        tech_interests: [],
      });
      if (inline && onComplete) {
        onComplete();
      } else {
        navigate("/dashboard", { replace: true });
      }
    } catch {
      if (inline && onComplete) {
        onComplete();
      } else {
        navigate("/dashboard", { replace: true });
      }
    } finally {
      setSaving(false);
    }
  }, [navigate, onComplete, inline]);

  const restartOnboarding = useCallback(async () => {
    setSaving(true);
    try {
      await api.onboarding.restart();
      setGoals([]);
      setInterests([]);
      setStep("welcome");
      setFinished(false);
    } catch {
      setError("Failed to restart onboarding.");
    } finally {
      setSaving(false);
    }
  }, []);

  const progress = step === "welcome" ? 0 : step === "goals" ? 33 : step === "interests" ? 66 : 100;

  const canContinue = step === "goals" ? goals.length > 0 : step === "interests" ? interests.length > 0 : true;

  if (loading) {
    return (
      <PageShell theme="focus">
        <div className="min-h-screen flex items-center justify-center px-4">
          <div className="flex flex-col items-center gap-3">
            <div className="h-10 w-10 animate-spin rounded-full border-2 border-primary border-t-transparent" />
            <p className="text-sm text-text-muted">Preparing your journey…</p>
          </div>
        </div>
      </PageShell>
    );
  }

  const Shell = ({ children }: { children: ReactNode }) => {
    if (inline) {
      return <div className="flex flex-col px-4 pt-6">{children}</div>;
    }
    return (
      <PageShell theme="focus">
        <div className="min-h-screen flex flex-col px-4 pt-6">{children}</div>
      </PageShell>
    );
  };

  return (
    <Shell>
      {/* Header */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 flex items-center justify-between"
        >
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
              <Rocket size={20} />
            </div>
            <div>
              <h2 className="font-display font-bold text-xl text-text-primary">Welcome to BountyCode!</h2>
              <p className="text-sm text-text-muted">Set up your personalized learning path</p>
            </div>
          </div>
          {step !== "welcome" && (
            <Button variant="ghost" size="sm" onClick={skipOnboarding} disabled={saving}>
              Skip
            </Button>
          )}
        </motion.div>

        {/* Progress */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-2 text-xs font-bold text-text-muted uppercase tracking-wider">
            <span>Step {["welcome", "goals", "interests", "dashboard"].indexOf(step) + 1} of 4</span>
            <span>{progress}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-surface-2 border border-border overflow-hidden">
            <div
              className="h-full bg-primary transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        </motion.div>

        {/* Steps content */}
        <AnimatePresence mode="wait">
          {step === "welcome" && (
            <motion.div
              key="welcome"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={reduced ? {} : { opacity: 0, y: -20 }}
              className="flex-1 flex flex-col items-center justify-center text-center space-y-8"
            >
              <div className="relative inline-block">
                <svg
                  className="w-32 h-32 text-primary drop-shadow-sm"
                  viewBox="0 0 200 200"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <rect x="20" y="20" width="140" height="110" rx="16" fill="white" stroke="#DCE8DE" strokeWidth="4" />
                  <rect x="36" y="40" width="110" height="8" rx="4" fill="#F0F7F1" />
                  <rect x="36" y="56" width="70" height="8" rx="4" fill="#F0F7F1" />
                  <rect x="36" y="72" width="110" height="8" rx="4" fill="#EAF7ED" />
                  <rect x="36" y="88" width="50" height="8" rx="4" fill="#EAF7ED" />
                  <rect x="36" y="104" width="110" height="8" rx="4" fill="#F0F7F1" />
                  <rect x="120" y="140" width="28" height="28" rx="8" fill="#EAB74D" />
                  <circle cx="134" cy="154" r="12" fill="#FDF6EB" stroke="#EAB74D" strokeWidth="4" />
                </svg>
              </div>
              <h1 className="font-display text-3xl font-black text-text-primary tracking-tight">
                Welcome to BountyCode!
              </h1>
              <p className="text-lg text-text-muted max-w-md leading-relaxed">
                Your journey towards becoming a skilled developer starts here.
              </p>
              <div className="flex flex-col sm:flex-row gap-3 w-full max-w-sm">
                <Button
                  variant="primary"
                  size="lg"
                  fullWidth
                  onClick={() => setStep("goals")}
                  rightIcon={<ArrowRight size={18} />}
                >
                  Get Started
                </Button>
                <Button variant="ghost" size="lg" fullWidth onClick={skipOnboarding} disabled={saving}>
                  Skip
                </Button>
              </div>
            </motion.div>
          )}

          {step === "goals" && (
            <motion.div
              key="goals"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={reduced ? {} : { opacity: 0, y: -20 }}
              className="flex-1"
            >
              <div className="mb-6">
                <h2 className="font-display font-bold text-2xl text-text-primary mb-1">Choose Your Career Goal</h2>
                <p className="text-text-muted">Select one or more goals that match your ambitions.</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {GOALS.map((g) => {
                  const Icon = GOAL_ICONS[g.id] || Code2;
                  const selected = goals.includes(g.id);
                  return (
                    <motion.button
                      key={g.id}
                      whileHover={reduced ? {} : { scale: 1.02 }}
                      whileTap={reduced ? {} : { scale: 0.98 }}
                      onClick={() => toggleGoal(g.id)}
                      className={`w-full group card p-5 text-left transition-all ${
                        selected
                          ? "border-primary bg-primary/5"
                          : "border hover:border-primary/30"
                      }`}
                    >
                      <div className="flex items-center gap-3 mb-3">
                        <div className="w-10 h-10 rounded-xl flex items-center justify-center">
                          <Icon size={20} className={`text-${selected ? "primary-dark" : "text-muted"}`} />
                        </div>
                        <span className={`font-bold ${selected ? "text-text-primary" : "text-text-muted"}`}>
                          {g.label}
                        </span>
                      </div>
                      <p className="text-sm text-text-muted">{g.desc}</p>
                      {selected && (
                        <div className="mt-3 flex items-center gap-1 text-xs font-bold text-primary">
                          <Check size={14} /> Selected
                        </div>
                      )}
                    </motion.button>
                  );
                })}
              </div>
              <div className="mt-6 flex items-center justify-between">
                <Button variant="ghost" size="sm" onClick={() => setStep("welcome")} leftIcon={<ArrowLeft size={16} />}>
                  Back
                </Button>
                <Button
                  variant="primary"
                  size="lg"
                  fullWidth
                  disabled={!canContinue || saving}
                  onClick={async () => {
                    await savePrefs();
                    setStep("interests");
                  }}
                  rightIcon={<ArrowRight size={18} />}
                  loading={saving}
                >
                  Continue
                </Button>
              </div>
            </motion.div>
          )}

          {step === "interests" && (
            <motion.div
              key="interests"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={reduced ? {} : { opacity: 0, y: -20 }}
              className="flex-1"
            >
              <div className="mb-6">
                <h2 className="font-display font-bold text-2xl text-text-primary mb-1">Select Your Interests</h2>
                <p className="text-text-muted">Pick the technologies you want to learn.</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {TECHS.map((t) => {
                  const Icon = t.icon;
                  const selected = interests.includes(t.id);
                  return (
                    <motion.button
                      key={t.id}
                      whileHover={reduced ? {} : { scale: 1.02 }}
                      whileTap={reduced ? {} : { scale: 0.98 }}
                      onClick={() => toggleInterest(t.id)}
                      className={`w-full group card p-5 text-left transition-all ${
                        selected
                          ? "border-primary bg-primary/5"
                          : "border hover:border-primary/30"
                      }`}
                    >
                      <div className="flex items-center gap-3 mb-3">
                        <div className="w-10 h-10 rounded-xl flex items-center justify-center">
                          <Icon size={20} className={`text-${selected ? "primary-dark" : "text-muted"}`} />
                        </div>
                        <span className={`font-bold ${selected ? "text-text-primary" : "text-text-muted"}`}>
                          {TECH_LABELS[t.id]}
                        </span>
                      </div>
                      {selected && (
                        <div className="mt-3 flex items-center gap-1 text-xs font-bold text-primary">
                          <Check size={14} /> Selected
                        </div>
                      )}
                    </motion.button>
                  );
                })}
              </div>
              <div className="mt-6 flex items-center justify-between">
                <Button variant="ghost" size="sm" onClick={() => setStep("goals")} leftIcon={<ArrowLeft size={16} />}>
                  Back
                </Button>
                <Button
                  variant="primary"
                  size="lg"
                  fullWidth
                  disabled={!canContinue || saving}
                  onClick={async () => {
                    await savePrefs();
                    setStep("dashboard");
                  }}
                  rightIcon={<ArrowRight size={18} />}
                  loading={saving}
                >
                  Continue
                </Button>
              </div>
            </motion.div>
          )}

          {step === "dashboard" && (
            <motion.div
              key="dashboard"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex-1 flex flex-col items-center justify-center text-center space-y-6"
            >
              <div className="flex flex-col items-center gap-3">
                <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary mb-2">
                  <CheckCircle2 size={32} />
                </div>
                <div className="animate-pulse flex items-center gap-1 text-primary font-bold text-sm">
                  <Sparkles size={14} /> Onboarding complete
                </div>
              </div>
              <h2 className="font-display font-bold text-2xl text-text-primary">Welcome aboard!</h2>
              <p className="text-text-muted max-w-md leading-relaxed">
                Your personalized learning path is ready. Here is what you selected:
              </p>

              <div className="w-full max-w-2xl space-y-4">
                <Card pad="md" className="text-left">
                  <div className="flex items-center gap-3 mb-3">
                    <User size={18} className="text-primary" />
                    <h3 className="font-bold text-text-primary">Your Goals</h3>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {goals.length > 0 ? (
                      goals.map((g) => (
                        <span key={g} className="px-3 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-medium">
                          {GOALS.find((x) => x.id === g)?.label || g}
                        </span>
                      ))
                    ) : (
                      <span className="text-text-muted text-sm italic">None selected</span>
                    )}
                  </div>
                </Card>

                <Card pad="md" className="text-left">
                  <div className="flex items-center gap-3 mb-3">
                    <Code size={18} className="text-primary" />
                    <h3 className="font-bold text-text-primary">Your Interests</h3>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {interests.length > 0 ? (
                      interests.map((i) => (
                        <span key={i} className="px-3 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-medium">
                          {TECH_LABELS[i] || i}
                        </span>
                      ))
                    ) : (
                      <span className="text-text-muted text-sm italic">None selected</span>
                    )}
                  </div>
                </Card>

                <Card pad="md" className="text-left border-primary/20 bg-primary/5">
                  <div className="flex items-center gap-3 mb-3">
                    <ArrowUpRight size={18} className="text-[#15803D]" />
                    <h3 className="font-bold text-text-primary">Recommended Paths</h3>
                  </div>
                  <div className="space-y-3">
                    {[
                      ...new Set([
                        ...goals.filter((g) => LEARNING_PATHS[g]),
                        ...interests.filter((i) => i === "python" || i === "ai" || i === "ml" ? "ai_ml" : i === "java" ? "placements" : i === "javascript" || i === "react" || i === "nodejs" ? "full_stack" : null),
                      ]),
                    ].map((g) => {
                      const path = LEARNING_PATHS[g as keyof typeof LEARNING_PATHS];
                      if (!path) return null;
                      return (
                        <div key={g} className="flex items-center justify-between p-3 rounded-xl border border-border bg-surface">
                          <div>
                            <h4 className="font-bold text-text-primary">{path.title}</h4>
                            <p className="text-xs text-text-muted">{path.desc}</p>
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => navigate(path.to)}
                          >
                            Explore <ArrowRight size={14} />
                          </Button>
                        </div>
                      );
                    })}
                  </div>
                </Card>
              </div>

              <div className="mt-8 flex flex-col sm:flex-row gap-3 w-full max-w-sm">
                <Button
                  variant="primary"
                  size="lg"
                  fullWidth
                  onClick={completeOnboarding}
                  loading={saving}
                  disabled={saving}
                >
                  Finish & Explore Dashboard
                </Button>
                <Button variant="ghost" size="lg" fullWidth onClick={restartOnboarding} disabled={saving}>
                  <RefreshCw size={16} className="mr-2" /> Restart
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 rounded-xl border border-red bg-red/10 text-red text-sm"
          >
            {error}
          </motion.div>
        )}
    </Shell>
  );
}
