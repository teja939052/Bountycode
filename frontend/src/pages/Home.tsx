import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import useAuthStore from "../store/authStore";
import { requestWithRetry as request } from "../services/api/request.ts";
import { Target, Flame, ArrowRight, Leaf, Trophy, Code2, Briefcase, Zap, Star } from "lucide-react";
import { Button, Card, ProgressBar } from "../design-system/components";

interface StudentState {
  readiness: number | null;
  categories: Record<string, number>;
  level: number;
  streak: number;
  xp: number;
  name: string;
  next_mission?: { label: string; to: string; minutes: number; xp?: number } | null;
}

const RING_DEFS: { key: string; label: string; icon: React.ReactNode; color: string }[] = [
  { key: "dsa", label: "DSA", icon: <Code2 size={20} />, color: "#16A34A" },
  { key: "cs_fundamentals", label: "CS Fundamentals", icon: <Trophy size={20} />, color: "#3B82F6" },
  { key: "interview", label: "Interview", icon: <Briefcase size={20} />, color: "#8B5CF6" },
  { key: "resume", label: "Resume", icon: <Zap size={20} />, color: "#F59E0B" },
];

const DEFAULT_MISSION = { label: "Start Today's Practice", to: "/practice", minutes: 15, xp: 50 };

export default function Home() {
  const storeUser = useAuthStore((s) => s.user);
  const [state, setState] = useState<StudentState | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const res = await request<StudentState>("/api/v1/auth/state");
        if (!active) return;
        setState({
          readiness: res?.readiness ?? null,
          categories: res?.categories || {},
          level: res?.level ?? storeUser?.level ?? 1,
          streak: res?.streak ?? storeUser?.streak ?? 0,
          xp: res?.xp ?? storeUser?.xp ?? 0,
          name: res?.name || storeUser?.name || "",
          next_mission: res?.next_mission,
        });
      } catch {
        setState({
          readiness: null,
          categories: {},
          level: storeUser?.level ?? 1,
          streak: storeUser?.streak ?? 0,
          xp: storeUser?.xp ?? 0,
          name: storeUser?.name || "",
          next_mission: null,
        });
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, [storeUser?.name, storeUser?.level, storeUser?.streak, storeUser?.xp]);

  const s = state ?? {
    readiness: null,
    categories: {},
    level: storeUser?.level ?? 1,
    streak: storeUser?.streak ?? 0,
    xp: storeUser?.xp ?? 0,
    name: storeUser?.name || "",
    next_mission: null,
  };
  const firstName = s.name?.split(" ")[0] || "there";
  const readiness = s.readiness;
  const mission = s.next_mission || DEFAULT_MISSION;

  const greeting = (() => {
    const h = new Date().getHours();
    if (h < 12) return "Good morning";
    if (h < 18) return "Good afternoon";
    return "Good evening";
  })();

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="space-y-8"
      >
        {/* Header */}
        <div>
          <p className="text-sm font-medium text-text-secondary">
            {greeting}, {firstName} 👋
          </p>
          <h1 className="mt-1 font-display text-3xl font-extrabold tracking-tight text-text-primary sm:text-4xl">
            {readiness === null ? "Let's keep building." : `You're ${readiness}% placement ready.`}
          </h1>
        </div>

        {/* Next Mission Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1, duration: 0.4 }}
          className="relative overflow-hidden rounded-2xl border border-brand-primary/20 bg-gradient-to-br from-brand-mint/30 via-background-surface to-brand-mint/30 p-6 shadow-soft-lg sm:p-8"
        >
          <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-brand-primary/60 to-transparent" aria-hidden="true" />
          <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-brand-primary">
            <Target size={14} /> Your next mission
          </div>
          <p className="mt-3 text-xl font-bold text-text-primary sm:text-2xl">{mission.label}</p>
          <div className="mt-1 flex items-center gap-4 text-sm text-text-secondary">
            <span>~{mission.minutes} minutes</span>
            {mission.xp && <span className="flex items-center gap-1 text-xp font-mono">+{mission.xp} XP</span>}
          </div>
          <Button
            asChild
            size="lg"
            className="mt-5"
            rightIcon={<ArrowRight size={16} />}
          >
            <Link to={mission.to}>Start</Link>
          </Button>
        </motion.div>

        {/* Skill Mastery Rings */}
        <div className="space-y-6">
          <div className="mb-3 px-1 text-xs font-mono uppercase tracking-wider text-text-secondary">Your journey</div>
          {loading ? (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              {[1,2,3,4].map((i) => (
                <div key={i} className="flex flex-col items-center rounded-2xl border border-border-primary bg-background-surfaceSecondary py-5 animate-pulse">
                  <div className="w-24 h-24 rounded-full bg-background-secondary" />
                  <span className="mt-2 text-sm font-medium text-text-secondary">Loading</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              {RING_DEFS.map((ring) => (
                <Card variant="outlined" padding="md" className="flex flex-col items-center text-center hover:border-brand-primary/50 transition-colors" key={ring.key}>
                  <div className="w-24 h-24 rounded-full flex items-center justify-center mb-3" style={{ background: `${ring.color}15` }}>
                    <span style={{ color: ring.color }}>{ring.icon}</span>
                  </div>
                  <ProgressBar
                    value={s.categories[ring.key] ?? 0}
                    size="xl"
                    color="primary"
                    showLabel
                    className="w-full mb-2"
                  />
                  <p className="font-semibold text-text-primary">{ring.label}</p>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Stats Bar */}
        <Card variant="outlined" padding="md" className="flex flex-col sm:flex-row items-center justify-center gap-6">
          <div className="flex items-center gap-3 text-center sm:text-left">
            <div className="w-10 h-10 rounded-full bg-xp/15 flex items-center justify-center">
              <Flame size={20} className="text-xp" />
            </div>
            <div>
              <p className="text-2xl font-display font-bold text-text-primary">{s.streak}</p>
              <p className="text-xs font-mono text-text-secondary">Day Streak</p>
            </div>
          </div>
          <div className="w-px h-8 bg-border-primary sm:hidden" />
          <div className="flex items-center gap-3 text-center sm:text-left">
            <div className="w-10 h-10 rounded-full bg-brand-mint/30 flex items-center justify-center">
              <Trophy size={20} className="text-brand-primary" />
            </div>
            <div>
              <p className="text-2xl font-display font-bold text-text-primary">Lv. {s.level}</p>
              <p className="text-xs font-mono text-text-secondary">Level</p>
            </div>
          </div>
          <div className="w-px h-8 bg-border-primary sm:hidden" />
          <div className="flex items-center gap-3 text-center sm:text-left">
            <div className="w-10 h-10 rounded-full bg-brand-mint/30 flex items-center justify-center">
              <Star size={20} className="text-xp" />
            </div>
            <div>
              <p className="text-2xl font-display font-bold text-text-primary">{s.xp.toLocaleString()}</p>
              <p className="text-xs font-mono text-text-secondary">Total XP</p>
            </div>
          </div>
        </Card>

        {/* Quick Actions */}
        <div className="space-y-4">
          <h3 className="text-sm font-mono uppercase tracking-wider text-text-secondary">Quick actions</h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <Button variant="outline" size="md" fullWidth asChild leftIcon={<Code2 size={16} />}>
              <Link to="/practice">Practice</Link>
            </Button>
            <Button variant="outline" size="md" fullWidth asChild leftIcon={<Zap size={16} />}>
              <Link to="/interview">Interview Prep</Link>
            </Button>
            <Button variant="outline" size="md" fullWidth asChild leftIcon={<Leaf size={16} />}>
              <Link to="/learn/c">Learn</Link>
            </Button>
            <Button variant="outline" size="md" fullWidth asChild leftIcon={<Briefcase size={16} />}>
              <Link to="/career">Career</Link>
            </Button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}