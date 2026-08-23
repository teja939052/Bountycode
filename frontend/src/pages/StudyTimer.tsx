import { useState, useEffect, useRef, useCallback } from "react";
import { Timer, Play, Pause, RotateCcw, Coins, Flame, Crown } from "lucide-react";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import { useToast } from "../components/Toast";
import { Link } from "react-router-dom";

const PRESETS = [
  { id: "pomodoro", label: "Pomodoro (25/5)", work: 25, break: 5 },
  { id: "quick", label: "5-Minute Sprint", work: 5, break: 1 },
  { id: "focus", label: "10-Minute Focus", work: 10, break: 2 },
  { id: "deep", label: "25-Minute Deep", work: 25, break: 5 },
];

export default function StudyTimer() {
  const { user } = useAuthStore();
  const toast = useToast();
  const [mode, setMode] = useState("pomodoro");
  const [custom, setCustom] = useState(25);
  const [isRunning, setIsRunning] = useState(false);
  const [isBreak, setIsBreak] = useState(false);
  const [secondsLeft, setSecondsLeft] = useState(25 * 60);
  const [activeSession, setActiveSession] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const isPro = (user?.plan || "") === "pro" || (user?.plan as string) === "lifetime";

  const preset = PRESETS.find((p) => p.id === mode);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = useCallback(async () => {
    try {
      const data = await api.studyTimer.getStats();
      setStats(data);
    } catch {
      setStats({ total_sessions: 0, total_minutes: 0, streak_days: 0, focus_rank: "Novice" });
    } finally {
      setLoading(false);
    }
  }, []);

  const workSeconds = () => (mode === "custom" ? custom * 60 : preset!.work * 60);
  const breakSeconds = () => (mode === "custom" ? Math.max(60, Math.floor(custom * 0.2 * 60)) : preset!.break * 60);

  const startSession = async () => {
    const minutes = workSeconds() / 60;
    try {
      const res = await api.studyTimer.createSession(workSeconds(), `${minutes} min focus`, mode);
      setActiveSession(res);
      setIsRunning(true);
      setIsBreak(false);
      setSecondsLeft(workSeconds());
    } catch (e: any) {
      toast.error(e.message || "Could not start session");
    }
  };

  const togglePause = () => setIsRunning((r) => !r);

  const reset = () => {
    setIsRunning(false);
    setIsBreak(false);
    setSecondsLeft(workSeconds());
    setActiveSession(null);
  };

  const completeSession = async () => {
    if (!activeSession) return;
    const completed = workSeconds() - secondsLeft;
    const minutes = Math.max(1, Math.ceil(completed / 60));
    try {
      const res = await api.studyTimer.completeSession(activeSession.session_id, minutes);
      window.dispatchEvent(new CustomEvent("xp-gained", { detail: { xp: res.score } }));
      toast.success(`+${res.score} XP • ${minutes} min focused`);
      loadStats();
    } catch {
      toast.error("Failed to save session");
    }
  };

  // Countdown tick
  useEffect(() => {
    if (!isRunning) {
      if (intervalRef.current) clearInterval(intervalRef.current);
      return;
    }
    intervalRef.current = setInterval(() => {
      setSecondsLeft((s) => {
        if (s <= 1) {
          if (intervalRef.current) clearInterval(intervalRef.current);
          if (isBreak) {
            // Break over → reset to work
            setIsBreak(false);
            setSecondsLeft(workSeconds());
            setActiveSession(null);
            setIsRunning(false);
            return workSeconds();
          } else {
            // Work done → save + flip to break
            completeSession();
            setIsBreak(true);
            setSecondsLeft(breakSeconds());
            return breakSeconds();
          }
        }
        return s - 1;
      });
    }, 1000);
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isRunning, isBreak]);

  const fmt = (s: number) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;

  if (loading) {
    return (
      <div className="min-h-screen py-8 px-4 flex items-center justify-center">
        <div className="animate-pulse text-brand-sky">Loading Study Timer…</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-6 sm:py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center justify-center gap-3">
            <Timer className="text-brand-sky" size={28} />
            Study Timer
          </h1>
          <p className="text-text-secondary mt-1">Pomodoro & custom focus sessions. Earn XP for every minute studied.</p>
          {!isPro && (
            <Link to="/pricing" className="inline-block mt-2 text-xs font-mono text-brand-sky hover:underline">
              Upgrade to Pro for custom durations
            </Link>
          )}
        </header>

        {/* Presets */}
        <div className="mb-6 flex flex-wrap gap-2">
          {PRESETS.map((p) => (
            <button
              key={p.id}
              onClick={() => !isRunning && setMode(p.id)}
              disabled={isRunning}
              className={`px-4 py-2 rounded-xl text-sm font-medium border transition-all ${
                mode === p.id
                  ? "bg-brand-sky/15 border-brand-sky text-brand-sky"
                  : "border-black/5 hover:border-brand-sky/30 text-text-secondary"
              } ${isRunning ? "opacity-50 cursor-not-allowed" : ""}`}
            >
              {p.label}
            </button>
          ))}
          {isPro && (
            <button
              onClick={() => !isRunning && setMode("custom")}
              disabled={isRunning}
              className={`px-4 py-2 rounded-xl text-sm font-medium border transition-all ${
                mode === "custom"
                  ? "bg-brand-sky/15 border-brand-sky text-brand-sky"
                  : "border-black/5 hover:border-brand-sky/30 text-text-secondary"
              } ${isRunning ? "opacity-50 cursor-not-allowed" : ""}`}
            >
              {`Custom: ${custom}m`}
            </button>
          )}
          {!isPro && mode === "custom" && (
            <span className="self-center text-xs text-text-light">Pro only</span>
          )}
        </div>

        {/* Custom duration (Pro only) */}
        {mode === "custom" && isPro && (
          <div className="mb-4 flex items-center gap-3">
            <label className="text-xs font-mono text-text-light">Duration (minutes):</label>
            <input
              type="number"
              min={1}
              max={480}
              value={custom}
              onChange={(e) => setCustom(Math.max(1, Math.min(480, Number(e.target.value))))}
              disabled={isRunning}
              className="w-20 rounded-xl border border-black/5 bg-white border-border shadow-card px-2 py-1 text-sm font-mono"
            />
          </div>
        )}

        {/* Timer display */}
        <div className="rounded-3xl border border-black/5 bg-gradient-to-br from-brand-sky/5 to-brand-lavender/5 p-8 text-center mb-6">
          <div className="text-6xl font-mono font-bold text-text-primary mb-2">{fmt(secondsLeft)}</div>
          <div className="text-sm text-text-light font-mono uppercase tracking-wider mb-4">
            {isBreak ? "Break" : "Focus"} · {isBreak ? breakSeconds() / 60 : workSeconds() / 60} min
          </div>
          <div className="flex justify-center gap-3">
            {!activeSession ? (
              <button
                onClick={startSession}
                className="px-8 py-3 rounded-xl bg-brand-sky text-text-primary font-bold flex items-center gap-2 hover:bg-brand-sky/90 transition"
              >
                <Play size={18} /> Start Session
              </button>
            ) : (
              <>
                <button
                  onClick={togglePause}
                  className="px-6 py-3 rounded-xl bg-brand-sky/10 border border-brand-sky text-brand-sky font-bold flex items-center gap-2 hover:bg-brand-sky/20 transition"
                >
                  {isRunning ? <Pause size={18} /> : <Play size={18} />}
                  {isRunning ? "Pause" : "Resume"}
                </button>
                <button
                  onClick={reset}
                  className="px-6 py-3 rounded-xl border border-black/5 text-text-secondary font-bold flex items-center gap-2 hover:bg-surface-2 transition"
                >
                  <RotateCcw size={18} /> Reset
                </button>
              </>
            )}
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
          <Stat icon={<Timer size={16} />} label="Total (min)" value={stats?.total_minutes ?? 0} color="text-brand-sky" />
          <Stat icon={<Flame size={16} />} label="Streak" value={`${stats?.streak_days ?? 0}d`} color="text-orange-400" />
          <Stat icon={<Coins size={16} />} label="Sessions" value={stats?.total_sessions ?? 0} color="text-yellow-400" />
          <Stat icon={<Crown size={16} />} label="Rank" value={stats?.focus_rank ?? "Novice"} color="text-purple-400" />
        </div>

        <div className="text-center">
          <Link to="/tower" className="text-xs font-mono text-text-light hover:text-brand-sky transition">
            ← Back to Tower Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}

function Stat({ icon, label, value, color }: { icon: any; label: string; value: any; color: string }) {
  return (
    <div className="bg-gray-900/40 border border-gray-700/20 rounded-xl p-3 text-center">
      <div className={`flex items-center justify-center gap-1 mb-1 ${color}`}>{icon}</div>
      <div className="text-xl font-display font-bold text-text-primary">{value}</div>
      <div className="text-[9px] font-mono text-gray-500">{label}</div>
    </div>
  );
}
