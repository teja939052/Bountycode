import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import useAuthStore from "../store/authStore";
import { requestWithRetry as request } from "../services/api/request.ts";
import {
  Target,
  Flame,
  ArrowRight,
  Trophy,
  Code2,
  Briefcase,
  Zap,
  Star,
  FileText,
} from "lucide-react";
import { PageShell } from "../design-system/PageShell";
import { Card } from "../design-system/Card";
import { Button } from "../design-system/Button";
import { ReadinessRing, MasteryBar } from "../design-system/Progress";
import { BountyCard } from "../design-system/JourneyMap";
import DailyOrdersCard from "../components/dailyOrders/DailyOrdersCard";

interface StudentState {
  readiness: number | null;
  categories: Record<string, number>;
  level: number;
  streak: number;
  xp: number;
  name: string;
  next_mission?: { label: string; to: string; minutes: number; xp?: number } | null;
}

const RING_DEFS: { key: string; label: string; icon: React.ReactNode; tone: "primary" | "tech" | "rare" | "gold"; color: string }[] = [
  { key: "dsa", label: "DSA", icon: <Code2 size={18} />, tone: "primary", color: "#22C55E" },
  { key: "cs_fundamentals", label: "CS Fundamentals", icon: <Trophy size={18} />, tone: "tech", color: "#4A90E2" },
  { key: "interview", label: "Interview", icon: <Briefcase size={18} />, tone: "rare", color: "#8B6BD9" },
  { key: "resume", label: "Resume", icon: <FileText size={18} />, tone: "gold", color: "#EAB74D" },
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
    return () => {
      active = false;
    };
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
    <PageShell theme="adventure">
      <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="space-y-8"
        >
          {/* Header + readiness */}
          <div className="flex flex-col-reverse items-start gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="adventure-label">{greeting}, {firstName}</p>
              <h1 className="font-display mt-2 text-3xl font-extrabold tracking-tight text-text sm:text-4xl">
                {readiness === null
                  ? "Let's chart your course."
                  : `You're ${readiness}% voyage ready.`}
              </h1>
            </div>
            {readiness !== null && (
              <div className="shrink-0 rounded-2xl border border-border bg-surface p-3 shadow-card">
                <ReadinessRing value={readiness} size={92} />
              </div>
            )}
          </div>

          {/* Next Bounty */}
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1, duration: 0.4 }}
          >
            <BountyCard
              title={mission.label}
              subtitle={`~${mission.minutes} minutes · today's bounty`}
              difficulty="Medium"
              reward={mission.xp}
              topics={["Daily"]}
              actionLabel="Accept Bounty"
            >
              <Link to={mission.to} className="btn btn-primary w-full justify-center py-2.5 text-sm font-bold">
                <span className="flex items-center gap-1.5">
                  Accept Bounty <ArrowRight size={15} />
                </span>
              </Link>
            </BountyCard>
          </motion.div>

          {/* First Mate Orders — deadline-driven daily checklist */}
          <DailyOrdersCard />

          {/* Skill mastery */}
          <div>
            <div className="mb-3 flex items-center gap-2">
              <Target size={15} className="text-ocean" />
              <p className="text-xs font-bold uppercase tracking-wider text-text-muted">Your journey</p>
            </div>
            {loading ? (
              <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="surface-border flex animate-pulse flex-col items-center rounded-2xl border bg-surface py-5"
                  >
                    <div className="mb-3 h-10 w-10 rounded-full bg-mint" />
                    <div className="h-2 w-3/4 rounded-full bg-mint" />
                  </div>
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                {RING_DEFS.map((ring) => (
                  <Card key={ring.key} pad="sm" interactive className="flex flex-col items-center text-center">
                    <div
                      className="mb-3 flex h-11 w-11 items-center justify-center rounded-xl"
                      style={{ backgroundColor: `${ring.color}18`, color: ring.color }}
                    >
                      {ring.icon}
                    </div>
                    <MasteryBar value={s.categories[ring.key] ?? 0} showValue={false} size="sm" tone={ring.tone} className="w-full" />
                    <p className="mt-2 text-xs font-bold text-text">{ring.label}</p>
                    <p className="text-[11px] font-semibold text-ocean">{Math.round(s.categories[ring.key] ?? 0)}%</p>
                  </Card>
                ))}
              </div>
            )}
          </div>

          {/* Stats Bar */}
          <Card className="flex flex-col items-center justify-center gap-6 sm:flex-row">
            <div className="flex items-center gap-3 text-center sm:text-left">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-coral-soft">
                <Flame size={20} className="text-coral" />
              </div>
              <div>
                <p className="font-display text-2xl font-extrabold text-text">{s.streak}</p>
                <p className="text-xs font-medium text-text-muted">Day Streak</p>
              </div>
            </div>
            <div className="surface-border h-px w-8 sm:h-8 sm:w-px" />
            <div className="flex items-center gap-3 text-center sm:text-left">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-soft">
                <Trophy size={20} className="text-primary-dark" />
              </div>
              <div>
                <p className="font-display text-2xl font-extrabold text-text">Lv. {s.level}</p>
                <p className="text-xs font-medium text-text-muted">Level</p>
              </div>
            </div>
            <div className="surface-border h-px w-8 sm:h-8 sm:w-px" />
            <div className="flex items-center gap-3 text-center sm:text-left">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-reward-soft">
                <Star size={20} className="text-reward" fill="#EAB74D" />
              </div>
              <div>
                <p className="font-display text-2xl font-extrabold text-text">{s.xp.toLocaleString()}</p>
                <p className="text-xs font-medium text-text-muted">Total XP</p>
              </div>
            </div>
          </Card>

          {/* Quick Actions */}
          <div>
            <h3 className="adventure-label mb-3">Quick actions</h3>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <Link to="/practice">
                <Button variant="outline" fullWidth leftIcon={<Code2 size={16} />}>
                  Practice
                </Button>
              </Link>
              <Link to="/interview">
                <Button variant="outline" fullWidth leftIcon={<Zap size={16} />}>
                  Interview Prep
                </Button>
              </Link>
              <Link to="/learn/c">
                <Button variant="outline" fullWidth leftIcon={<Star size={16} />}>
                  Learn
                </Button>
              </Link>
              <Link to="/career">
                <Button variant="outline" fullWidth leftIcon={<Briefcase size={16} />}>
                  Career
                </Button>
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </PageShell>
  );
}
