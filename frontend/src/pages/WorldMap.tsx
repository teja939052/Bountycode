import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { worldsApi } from "../services/api/worlds.ts";

type WorldMeta = {
  id: string;
  name: string;
  subtitle: string;
  description: string;
  icon: string;
  order: number;
  theme: string;
  recommended_roles: string[];
  prerequisites: string[];
  towns_count: number;
  levels_count: number;
  completed_count: number;
  progress_pct: number;
  unlocked: boolean;
};

const WORLD_THEME: Record<string, { gradient: string; border: string; glow: string; bg: string }> = {
  foundations: { gradient: "from-emerald-400 to-cyan-400", border: "border-emerald-400/30", glow: "rgba(52,211,153,0.25)", bg: "from-emerald-50 to-cyan-50 dark:from-emerald-950/40 dark:to-cyan-950/30" },
  searchlands: { gradient: "from-blue-400 to-indigo-400", border: "border-blue-400/30", glow: "rgba(96,165,250,0.25)", bg: "from-blue-50 to-indigo-50 dark:from-blue-950/40 dark:to-indigo-950/30" },
  sorting: { gradient: "from-amber-400 to-orange-400", border: "border-amber-400/30", glow: "rgba(251,191,36,0.25)", bg: "from-amber-50 to-orange-50 dark:from-amber-950/40 dark:to-orange-950/30" },
  recursion: { gradient: "from-purple-400 to-pink-400", border: "border-purple-400/30", glow: "rgba(192,132,252,0.25)", bg: "from-purple-50 to-pink-50 dark:from-purple-950/40 dark:to-pink-950/30" },
  linked: { gradient: "from-teal-400 to-emerald-400", border: "border-teal-400/30", glow: "rgba(45,212,191,0.25)", bg: "from-teal-50 to-emerald-50 dark:from-teal-950/40 dark:to-emerald-950/30" },
  stack: { gradient: "from-sky-400 to-blue-400", border: "border-sky-400/30", glow: "rgba(125,211,252,0.25)", bg: "from-sky-50 to-blue-50 dark:from-sky-950/40 dark:to-blue-950/30" },
  queue: { gradient: "from-violet-400 to-purple-400", border: "border-violet-400/30", glow: "rgba(167,139,250,0.25)", bg: "from-violet-50 to-purple-50 dark:from-violet-950/40 dark:to-purple-950/30" },
  hashing: { gradient: "from-rose-400 to-pink-400", border: "border-rose-400/30", glow: "rgba(251,113,133,0.25)", bg: "from-rose-50 to-pink-50 dark:from-rose-950/40 dark:to-pink-950/30" },
  trees: { gradient: "from-green-400 to-lime-400", border: "border-green-400/30", glow: "rgba(74,222,128,0.25)", bg: "from-green-50 to-lime-50 dark:from-green-950/40 dark:to-lime-950/30" },
  graphs: { gradient: "from-cyan-400 to-teal-400", border: "border-cyan-400/30", glow: "rgba(34,211,238,0.25)", bg: "from-cyan-50 to-teal-50 dark:from-cyan-950/40 dark:to-teal-950/30" },
  dynamic: { gradient: "from-fuchsia-400 to-purple-400", border: "border-fuchsia-400/30", glow: "rgba(232,121,249,0.25)", bg: "from-fuchsia-50 to-purple-50 dark:from-fuchsia-950/40 dark:to-purple-950/30" },
  alpine: { gradient: "from-indigo-400 to-violet-400", border: "border-indigo-400/30", glow: "rgba(129,140,248,0.25)", bg: "from-indigo-50 to-violet-50 dark:from-indigo-950/40 dark:to-violet-950/30" },
};

export default function WorldMap() {
  const [loading, setLoading] = useState(true);
  const [worlds, setWorlds] = useState<WorldMeta[]>([]);
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [charPos, setCharPos] = useState({ x: 0, y: 0 });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res: any = await worldsApi.listWorlds();
      setWorlds(res.worlds || []);
    } catch (e) {
      console.error("Failed to load worlds", e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  useEffect(() => {
    const handleMouse = (e: MouseEvent) => {
      setCharPos({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", handleMouse, { passive: true });
    return () => window.removeEventListener("mousemove", handleMouse);
  }, []);

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center gap-4 bg-gradient-to-b from-zinc-50 to-zinc-100 dark:from-zinc-950 dark:to-zinc-900 px-6">
        <motion.div
          className="h-16 w-16 rounded-2xl bg-gradient-to-br from-brand-primary/20 to-brand-primary/5 flex items-center justify-center text-3xl shadow-lg"
          animate={{ rotate: [0, 10, -10, 0], scale: [1, 1.05, 1] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          🗺️
        </motion.div>
        <motion.p
          className="text-sm font-medium text-text-muted"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          Mapping the worlds…
        </motion.p>
      </div>
    );
  }

  const unlocked = worlds.filter((w) => w.unlocked);
  const locked = worlds.filter((w) => !w.unlocked);

  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-50 via-white to-zinc-50 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950 text-zinc-900 dark:text-zinc-100 relative overflow-hidden">
      {/* Ambient background blobs */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <motion.div
          className="absolute -top-32 -left-32 h-96 w-96 rounded-full bg-brand-primary/5 blur-3xl"
          animate={{ x: [0, 40, 0], y: [0, 30, 0] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        />
        <motion.div
          className="absolute top-1/3 -right-32 h-[500px] w-[500px] rounded-full bg-amber-400/5 blur-3xl"
          animate={{ x: [0, -30, 0], y: [0, 40, 0] }}
          transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
        />
        <motion.div
          className="absolute -bottom-32 left-1/3 h-80 w-80 rounded-full bg-purple-400/5 blur-3xl"
          animate={{ x: [0, 50, 0], y: [0, -30, 0] }}
          transition={{ duration: 18, repeat: Infinity, ease: "linear" }}
        />
      </div>

      <div className="relative mx-auto max-w-[1200px] px-4 py-8">
        {/* Header */}
        <motion.div
          className="mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-display font-extrabold tracking-tight">
                <span className="bg-gradient-to-r from-brand-primary via-emerald-600 to-amber-600 bg-clip-text text-transparent">
                  BountyCode Worlds
                </span>
              </h1>
              <p className="text-sm text-text-muted mt-1.5 max-w-lg">
                Each world is a realm of knowledge. Master them all to become a complete engineer.
              </p>
            </div>
            <Link
              to="/dashboard"
              className="hidden sm:flex items-center gap-2 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 px-4 py-2 text-sm font-medium shadow-sm hover:shadow-md transition-all"
            >
              ← Dashboard
            </Link>
          </div>

          {/* Progress summary */}
          <div className="mt-4 flex items-center gap-3">
            <div className="flex-1 h-2 rounded-full bg-zinc-200 dark:bg-zinc-800 overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-brand-primary to-emerald-500"
                initial={{ width: 0 }}
                animate={{ width: `${Math.round(worlds.reduce((a, w) => a + w.progress_pct, 0) / (worlds.length || 1))}%` }}
                transition={{ duration: 1.2, ease: "easeOut" }}
              />
            </div>
            <span className="text-xs font-mono text-text-muted">
              {worlds.reduce((a, w) => a + w.completed_count, 0)} / {worlds.reduce((a, w) => a + w.levels_count, 0)} levels
            </span>
          </div>
        </motion.div>

        {/* World grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <AnimatePresence>
            {worlds.map((w, idx) => {
              const theme = WORLD_THEME[w.id] || WORLD_THEME.foundations;
              const isHovered = hoveredId === w.id;
              const canEnter = w.unlocked;

              return (
                <motion.div
                  key={w.id}
                  initial={{ opacity: 0, y: 30, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ duration: 0.5, delay: idx * 0.05 }}
                  onMouseEnter={() => setHoveredId(w.id)}
                  onMouseLeave={() => setHoveredId(null)}
                  onClick={() => canEnter && setHoveredId(w.id)}
                  className={`relative group rounded-3xl border-2 p-5 cursor-pointer transition-all duration-300 ${
                    isHovered && canEnter
                      ? `border-transparent bg-gradient-to-br ${theme.bg} shadow-2xl scale-[1.03]`
                      : canEnter
                        ? "border-zinc-200/80 dark:border-zinc-700/80 bg-white dark:bg-zinc-900 hover:border-zinc-300 dark:hover:border-zinc-600 shadow-md hover:shadow-xl"
                        : "border-zinc-200/60 dark:border-zinc-800/60 bg-zinc-50/80 dark:bg-zinc-800/40 opacity-55 cursor-not-allowed"
                  }`}
                  style={
                    isHovered && canEnter
                      ? { boxShadow: `0 20px 60px -15px ${theme.glow}` }
                      : undefined
                  }
                >
                  {/* Locked overlay */}
                  {!canEnter && (
                    <div className="absolute inset-0 rounded-3xl bg-zinc-100/40 dark:bg-zinc-900/40 backdrop-blur-[1px] z-10 flex items-center justify-center">
                      <div className="flex flex-col items-center gap-2">
                        <span className="text-2xl grayscale opacity-60">🔒</span>
                        <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                          Locked — complete prerequisites first
                        </span>
                      </div>
                    </div>
                  )}

                  {/* Card content */}
                  <div className="relative z-0 flex items-start gap-4">
                    {/* Icon with glow */}
                    <div className="relative shrink-0">
                      <motion.div
                        className={`text-4xl p-3 rounded-2xl bg-gradient-to-br ${theme.gradient} bg-opacity-10`}
                        animate={isHovered && canEnter ? { scale: [1, 1.15, 1], rotate: [0, 5, -5, 0] } : {}}
                        transition={{ duration: 0.6 }}
                      >
                        {w.icon}
                      </motion.div>
                      {isHovered && canEnter && (
                        <motion.div
                          className="absolute inset-0 rounded-2xl blur-xl opacity-50"
                          style={{ backgroundColor: theme.glow }}
                          initial={{ scale: 0.8, opacity: 0 }}
                          animate={{ scale: 1.5, opacity: 0.4 }}
                          transition={{ duration: 0.8 }}
                        />
                      )}
                    </div>

                    {/* Text content */}
                    <div className="flex-1 min-w-0">
                      <h3 className="text-base font-bold leading-tight text-zinc-900 dark:text-zinc-100">
                        {w.name}
                      </h3>
                      <p className={`text-[11px] font-mono mt-0.5 bg-gradient-to-r ${theme.gradient} bg-clip-text text-transparent font-semibold`}>
                        {w.subtitle}
                      </p>
                      <p className="text-xs text-text-muted mt-1.5 line-clamp-2 leading-relaxed">
                        {w.description}
                      </p>

                      {/* Meta row */}
                      <div className="mt-3 flex items-center gap-2 text-[11px] font-mono text-text-muted">
                        <span className="flex items-center gap-1">
                          <span className="inline-block h-1.5 w-1.5 rounded-full bg-zinc-400" />
                          {w.towns_count} {w.towns_count === 1 ? 'town' : 'towns'}
                        </span>
                        <span className="text-zinc-300 dark:text-zinc-700">·</span>
                        <span className="flex items-center gap-1">
                          <span className="inline-block h-1.5 w-1.5 rounded-full bg-zinc-400" />
                          {w.levels_count} levels
                        </span>
                        <span className="text-zinc-300 dark:text-zinc-700">·</span>
                        <span className="flex items-center gap-1">
                          <span className="inline-block h-1.5 w-1.5 rounded-full bg-zinc-400" />
                          {w.progress_pct}%
                        </span>
                      </div>

                      {/* Progress bar */}
                      <div className="mt-2.5 h-1.5 w-full rounded-full bg-zinc-200/80 dark:bg-zinc-800 overflow-hidden">
                        <motion.div
                          className={`h-full rounded-full bg-gradient-to-r ${theme.gradient}`}
                          initial={{ width: 0 }}
                          animate={{ width: `${w.progress_pct}%` }}
                          transition={{ duration: 0.8, delay: idx * 0.05, ease: "easeOut" }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* CTA button */}
                  {canEnter && (
                    <motion.div
                      className="relative z-0 mt-4"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: isHovered ? 1 : 0.7, y: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Link
                        to={`/worlds/${w.id}`}
                        className={`flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r ${theme.gradient} px-5 py-2.5 text-sm font-bold text-white shadow-lg hover:shadow-xl transition-all`}
                        onClick={(e) => e.stopPropagation()}
                      >
                        <span>Enter World</span>
                        <motion.span
                          animate={{ x: [0, 4, 0] }}
                          transition={{ duration: 1.5, repeat: Infinity }}
                        >
                          →
                        </motion.span>
                      </Link>
                    </motion.div>
                  )}

                  {/* Prerequisites */}
                  {w.prerequisites.length > 0 && canEnter && (
                    <div className="mt-2.5 flex items-center gap-1.5 text-[10px] font-mono text-text-muted">
                      <span>Prerequisites:</span>
                      {w.prerequisites.map((pre) => (
                        <span key={pre} className="rounded-full bg-zinc-100 dark:bg-zinc-800 px-2 py-0.5 text-zinc-600 dark:text-zinc-400">
                          {pre}
                        </span>
                      ))}
                    </div>
                  )}
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>

        {/* Empty state */}
        {unlocked.length === 0 && (
          <motion.div
            className="mt-12 rounded-3xl border-2 border-dashed border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900 p-10 text-center"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <div className="text-5xl mb-4">🗺️</div>
            <p className="text-sm font-medium text-text-muted mb-4">
              No worlds unlocked yet. Complete the onboarding to begin your journey.
            </p>
            <Link
              to="/onboarding"
              className="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-brand-primary to-emerald-600 px-6 py-3 text-sm font-bold text-white shadow-lg hover:shadow-xl transition-all"
            >
              Start Onboarding →
            </Link>
          </motion.div>
        )}

        {/* Legend */}
        <motion.div
          className="mt-10 flex flex-wrap items-center justify-center gap-4 text-[11px] font-mono text-text-muted"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400" />
            {unlocked.length} unlocked
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-zinc-300 dark:bg-zinc-700" />
            {locked.length} locked
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-gradient-to-r from-brand-primary to-emerald-500" />
            {worlds.reduce((a, w) => a + w.completed_count, 0)} completed
          </span>
        </motion.div>
      </div>
    </div>
  );
}
