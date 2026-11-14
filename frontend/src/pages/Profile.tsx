import { useEffect, useState } from "react";
import { User as UserIcon, Flame, Trophy, RefreshCw, Target, Code } from "lucide-react";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import { motion } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import OnboardingFlow from "./OnboardingFlow";

const GOALS = [
  { id: "internship", label: "Get an Internship", icon: Target },
  { id: "placements", label: "Prepare for Placements", icon: Target },
  { id: "learning", label: "Learn Programming", icon: Code },
  { id: "hackathons", label: "Participate in Hackathons", icon: Target },
  { id: "full_stack", label: "Become a Full Stack Developer", icon: Code },
  { id: "ai_ml", label: "Explore AI and Machine Learning", icon: Target },
];

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

// V3 §1 — PROFILE: XP, streak, history, settings, billing. Renders
// backend level/xp (never localStorage curves). Upgrade → single ₹99 tier.
export default function Profile() {
  const { user } = useAuthStore();
  const [gam, setGam] = useState<any>(null);
  const [goals, setGoals] = useState<string[]>([]);
  const [interests, setInterests] = useState<string[]>([]);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [message, setMessage] = useState("");
  const reduced = useReducedMotion();

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const p = await (api as any).gamification?.getProfile?.();
        if (alive) setGam(p);
      } catch { /* offline-friendly */ }
      try {
        const prefs = await (api as any).onboarding?.getPreferences?.();
        if (alive) {
          setGoals(prefs.career_goals || []);
          setInterests(prefs.tech_interests || []);
        }
      } catch { /* offline-friendly */ }
    })();
    return () => { alive = false; };
  }, []);

  const fetchPrefs = async () => {
    try {
      const prefs = await (api as any).onboarding?.getPreferences?.();
      setGoals(prefs.career_goals || []);
      setInterests(prefs.tech_interests || []);
    } catch { /* offline-friendly */ }
  };

  const handleChangePreferences = () => {
    setMessage("");
    setShowOnboarding(true);
  };

  const goalLabel = (id: string) => GOALS.find((g) => g.id === id)?.label || id;
  const techLabel = (id: string) => TECH_LABELS[id] || id;

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 pb-24 md:pb-8">
      <div className="mx-auto max-w-3xl space-y-6">
        <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <p className="text-[10px] font-mono uppercase tracking-widest text-primary mb-1 flex items-center gap-2">
            <UserIcon size={12} /> Profile
          </p>
          <h1 className="font-display text-2xl font-black text-text-primary">{user?.name ?? "Cadet"}</h1>
          <p className="text-xs text-text-muted font-mono">{user?.email} · plan: {user?.plan ?? "free"}</p>
          <div className="mt-4 grid grid-cols-3 gap-3">
            <div className="rounded-xl bg-surface-2 p-3 border border-black/5">
              <p className="text-[10px] font-mono uppercase text-text-muted">Level</p>
              <p className="font-display text-lg font-black">{gam?.level ?? "—"}</p>
            </div>
            <div className="rounded-xl bg-surface-2 p-3 border border-black/5">
              <p className="text-[10px] font-mono uppercase text-text-muted flex items-center gap-1"><Flame size={10} /> Streak</p>
              <p className="font-display text-lg font-black">{gam?.streak ?? 0}</p>
            </div>
            <div className="rounded-xl bg-surface-2 p-3 border border-black/5">
              <p className="text-[10px] font-mono uppercase text-text-muted flex items-center gap-1"><Trophy size={10} /> XP</p>
              <p className="font-display text-lg font-black">{gam?.xp ?? gam?.diamonds ?? "—"}</p>
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <h2 className="text-xl font-display font-bold text-text-primary mb-2">Your Onboarding Choices</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl border border-border bg-surface">
              <h3 className="font-bold text-text-primary mb-3 flex items-center gap-2">
                <Target size={14} /> Career Goals
              </h3>
              <div className="flex flex-wrap gap-2">
                {goals.length > 0 ? (
                  goals.map((g) => (
                    <span key={g} className="px-3 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-medium">
                      {goalLabel(g)}
                    </span>
                  ))
                ) : (
                  <span className="text-text-muted text-sm italic">None selected</span>
                )}
              </div>
            </div>
            <div className="p-4 rounded-xl border border-border bg-surface">
              <h3 className="font-bold text-text-primary mb-3 flex items-center gap-2">
                <Code size={14} /> Tech Interests
              </h3>
              <div className="flex flex-wrap gap-2">
                {interests.length > 0 ? (
                  interests.map((i) => (
                    <span key={i} className="px-3 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-medium">
                      {techLabel(i)}
                    </span>
                  ))
                ) : (
                  <span className="text-text-muted text-sm italic">None selected</span>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <h2 className="text-xl font-display font-bold text-text-primary mb-2">Account</h2>
          <div className="p-4 rounded-xl border border-border bg-surface">
            <h3 className="font-bold text-text-primary mb-2">Update Preferences</h3>
            <p className="text-sm text-text-muted mb-4">
              Change your career goals and technology interests. Your choices
              will update here once you finish.
            </p>
            <motion.button
              onClick={handleChangePreferences}
              className="flex items-center gap-2 w-full btn-primary px-6 py-3"
              whileHover={reduced ? {} : { scale: 1.02 }}
              whileTap={reduced ? {} : { scale: 0.98 }}
            >
              <RefreshCw size={18} />
              Change
            </motion.button>
          </div>
        </div>

        {showOnboarding && (
          <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
            <OnboardingFlow inline onComplete={() => {
              setShowOnboarding(false);
              fetchPrefs();
            }} />
          </div>
        )}

        {message && (
          <motion.div
            className={`p-4 rounded-lg mb-6 border ${message.includes("success") ? "bg-cyber-green/10 border-cyber-green/20 text-cyber-green" : "bg-cyber-red/10 border-cyber-red/20 text-cyber-red"}`}
            initial={reduced ? {} : { opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {message}
          </motion.div>
        )}
      </div>
    </div>
  );
}
