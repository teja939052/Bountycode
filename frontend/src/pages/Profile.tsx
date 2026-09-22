import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { User as UserIcon, Flame, Trophy, ArrowRight } from "lucide-react";
import api from "../services/api";
import useAuthStore from "../store/authStore";

// V3 §1 — PROFILE: XP, streak, history, settings, billing. Renders
// backend level/xp (never localStorage curves). Upgrade → single ₹99 tier.
export default function Profile() {
  const { user } = useAuthStore();
  const [gam, setGam] = useState<any>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const p = await (api as any).gamification?.getProfile?.();
        if (alive) setGam(p);
      } catch { /* offline-friendly */ }
    })();
    return () => { alive = false; };
  }, []);

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
        <div className="rounded-2xl border border-border bg-white p-5 shadow-card flex flex-wrap gap-2">
          <Link to="/history" className="btn-secondary text-xs">History</Link>
          <Link to="/settings" className="btn-secondary text-xs">Settings</Link>
          <Link to="/leaderboard" className="btn-secondary text-xs">Leaderboard</Link>
          <Link to="/pricing" className="btn-primary text-xs inline-flex items-center gap-2">
            Upgrade — Job Seeker ₹99/mo <ArrowRight size={12} />
          </Link>
        </div>
      </div>
    </div>
  );
}
