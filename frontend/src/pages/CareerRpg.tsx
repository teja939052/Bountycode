import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  RefreshCw, Lock, CheckCircle2, Crown, Sparkles, Loader2,
  Map, Globe, Store, Sword, Swords, Users, Archive, Coins,
  Trophy, GraduationCap, Building2, Mic2, Palette, Zap,
} from "lucide-react";
import { careerApi } from "../services/api/career.ts";
import Skeleton from "../components/ui/Skeleton";

const FEATURE_META = {
  journey: { icon: Map, label: "Journey" },
  world: { icon: Globe, label: "World" },
  merchant: { icon: Store, label: "Merchant" },
  dungeons: { icon: Sword, label: "Dungeons" },
  guilds: { icon: Users, label: "Guilds" },
  collection: { icon: Archive, label: "Collection" },
  economy: { icon: Coins, label: "Economy" },
  showcase: { icon: Sparkles, label: "Showcase" },
  battles: { icon: Swords, label: "Battles" },
  prestige: { icon: Trophy, label: "Prestige" },
  campus: { icon: GraduationCap, label: "Campus" },
};

const STYLE_LABELS = {
  technical: "Technical",
  behavioral: "Behavioral",
  system_design: "System Design",
  coding: "Coding",
  aptitude: "Aptitude",
};

function formatXp(xp) {
  return Number(xp || 0).toLocaleString();
}

function FeatureChips({ features, muted = false }: any) {
  return (
    <div className="flex flex-wrap gap-2">
      {features.map((key) => {
        const meta = FEATURE_META[key] || { icon: Zap, label: key };
        const Icon = meta.icon;
        return (
          <span
            key={key}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-mono font-medium border transition-all ${
              muted
                ? "border-white/10 bg-white/5 text-slate-500"
                : "border-emerald-500/30 bg-emerald-500/10 text-emerald-300"
            }`}
          >
            <Icon className="w-3.5 h-3.5" />
            {meta.label}
          </span>
        );
      })}
    </div>
  );
}

function StyleChips({ styles }) {
  return (
    <div className="flex flex-wrap gap-2">
      {styles.map((s) => (
        <span
          key={s}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-mono font-medium border border-indigo-500/30 bg-indigo-500/10 text-indigo-300"
        >
          <Mic2 className="w-3.5 h-3.5" />
          {STYLE_LABELS[s] || s}
        </span>
      ))}
    </div>
  );
}

function CompanyChips({ companies }) {
  return (
    <div className="flex flex-wrap gap-2">
      {companies.map((c) => (
        <span
          key={c}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-mono font-medium border border-white/10 bg-white/5 text-slate-300 capitalize"
        >
          <Building2 className="w-3.5 h-3.5 text-slate-500" />
          {c}
        </span>
      ))}
    </div>
  );
}

export default function CareerRpg() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const d = await careerApi.get();
      setData(d);
      setSelectedIndex(d.role_index);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      const d = await careerApi.refresh();
      setData(d);
      setSelectedIndex(d.role_index);
    } catch (e) {
      setError(e.message);
    } finally {
      setRefreshing(false);
    }
  };

  if (loading && !data) {
    return (
      <div className="min-h-screen bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
          <Skeleton className="h-10 w-64 mb-3" />
          <Skeleton className="h-5 w-96 mb-8" />
          <div className="rounded-3xl border border-white/10 bg-white/5 p-8 mb-8">
            <Skeleton className="h-6 w-1/3 mb-4" />
            <Skeleton className="h-4 w-full mb-3" />
            <Skeleton className="h-4 w-2/3 mb-5" />
            <Skeleton className="h-3 w-full rounded-full" />
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {Array.from({ length: 6 }).map((_, i) => (
              <Skeleton key={i} className="h-16 w-full rounded-2xl" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="rounded-2xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
            {error || "Could not load career progression."}
          </div>
        </div>
      </div>
    );
  }

  const current = data.role;
  const next = data.next_role;
  const pct = data.progress_pct_to_next;
  const isMax = data.role_index >= data.all_roles.length;
  const justGained = current.unlocks || [];
  const selected = data.all_roles.find((r) => r.index === selectedIndex) || current;

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-display font-bold text-white flex items-center gap-3">
              <Crown className="w-8 h-8 text-emerald-400" />
              Career RPG
            </h1>
            <p className="text-slate-400 mt-1">
              Level up through career roles — every role unlocks new features, companies, and interview styles.
            </p>
          </div>
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500/20 to-indigo-500/20 border border-emerald-500/40 text-emerald-300 text-sm font-medium hover:border-emerald-400/70 hover:bg-emerald-500/10 transition-all disabled:opacity-50"
          >
            {refreshing ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
            Refresh
          </button>
        </div>

        {error && (
          <div className="mb-6 rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
            {error}
          </div>
        )}

        <motion.div
          key={current.index}
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative mb-8 rounded-3xl border border-white/10 bg-white/[0.04] p-6 sm:p-8 overflow-hidden"
          style={{ boxShadow: `0 0 60px ${current.cosmetic}26` }}
        >
          <div className="absolute inset-x-0 top-0 h-1" style={{ background: current.cosmetic }} />

          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-5 mb-6">
            <div
              className="flex items-center justify-center w-20 h-20 rounded-2xl text-4xl border"
              style={{ borderColor: `${current.cosmetic}66`, background: `${current.cosmetic}14` }}
            >
              {current.emoji}
            </div>
            <div className="flex-1">
              <div className="flex flex-wrap items-center gap-3">
                <h2 className="text-2xl sm:text-3xl font-display font-bold text-white">
                  {current.title}
                </h2>
                <span
                  className="px-3 py-1 rounded-full text-xs font-mono font-bold border"
                  style={{ borderColor: `${current.cosmetic}66`, color: current.cosmetic, background: `${current.cosmetic}14` }}
                >
                  LEVEL {current.level}
                </span>
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-medium border border-white/10 bg-white/5 text-slate-300">
                  <Zap className="w-3.5 h-3.5 text-emerald-400" />
                  {formatXp(data.current_xp)} XP
                </span>
              </div>
              <p className="text-slate-300 mt-2 text-sm">{current.title_perk}</p>
            </div>
          </div>

          <div className="mb-2 flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400">
              {isMax ? "Maxed out" : `Next: ${next.emoji} ${next.title}`}
            </span>
            <span className="text-emerald-300">{pct}%</span>
          </div>
          <div className="h-3 rounded-full bg-white/5 border border-white/10 overflow-hidden">
            <motion.div
              className="h-full rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${pct}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              style={{ background: `linear-gradient(90deg, ${current.cosmetic}, #818cf8)` }}
            />
          </div>
          {!isMax && (
            <p className="mt-2 text-xs text-slate-500 font-mono">
              {formatXp(Math.max(0, next.xp_required - data.current_xp))} XP to {next.title}
            </p>
          )}
        </motion.div>

        <AnimatePresence mode="wait">
          <motion.div
            key={current.index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mb-10 rounded-2xl border border-emerald-500/25 bg-gradient-to-r from-emerald-500/10 to-indigo-500/10 p-5"
          >
            <div className="flex flex-col sm:flex-row sm:items-center gap-3 mb-3">
              <Sparkles className="w-5 h-5 text-emerald-300" />
              <h3 className="text-sm font-semibold text-emerald-200">
                {data.role_index === 1 ? "Starting unlocks" : "Unlocks now"}
              </h3>
            </div>
            <FeatureChips features={justGained} />
          </motion.div>
        </AnimatePresence>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          <div className="lg:col-span-2">
            <h3 className="text-sm font-mono uppercase tracking-wider text-slate-500 mb-4">Role Ladder</h3>
            <div className="relative">
              <div className="absolute left-[23px] top-3 bottom-3 w-px bg-white/10" />
              <div className="space-y-3">
                {data.all_roles.map((r) => {
                  const isCurrent = r.index === data.role_index;
                  const isUnlocked = r.index <= data.role_index;
                  const isSelected = r.index === selectedIndex;
                  return (
                    <motion.button
                      key={r.index}
                      onClick={() => setSelectedIndex(r.index)}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      className={`relative flex items-center gap-4 w-full text-left rounded-2xl border p-3 pr-4 transition-all ${
                        isSelected
                          ? "border-emerald-500/50 bg-white/[0.07]"
                          : "border-white/10 bg-white/[0.03] hover:border-white/25"
                      } ${isCurrent ? "shadow-lg" : ""}`}
                      style={isCurrent ? { boxShadow: `0 0 30px ${r.cosmetic}40` } : undefined}
                    >
                      <div
                        className={`relative z-10 flex items-center justify-center w-11 h-11 rounded-xl text-2xl border shrink-0 ${
                          isUnlocked ? "bg-white/10 border-white/20" : "bg-black/30 border-white/10 grayscale opacity-50"
                        }`}
                        style={isCurrent ? { borderColor: `${r.cosmetic}88` } : undefined}
                      >
                        {isCurrent ? (
                          <motion.span
                            animate={{ scale: [1, 1.15, 1] }}
                            transition={{ repeat: Infinity, duration: 1.6 }}
                            className="inline-block"
                          >
                            {r.emoji}
                          </motion.span>
                        ) : (
                          r.emoji
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <p className={`text-sm font-semibold truncate ${isUnlocked ? "text-slate-100" : "text-slate-500"}`}>
                            {r.title}
                          </p>
                          {isCurrent && (
                            <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold text-slate-950 bg-emerald-400">
                              YOU
                            </span>
                          )}
                        </div>
                        <p className="text-xs font-mono text-slate-500">
                          {isUnlocked ? "Unlocked" : `${formatXp(r.xp_required)} XP`}
                        </p>
                      </div>
                      {isCurrent ? (
                        <motion.span
                          animate={{ opacity: [1, 0.4, 1] }}
                          transition={{ repeat: Infinity, duration: 1.8 }}
                          className="w-2.5 h-2.5 rounded-full shrink-0"
                          style={{ background: r.cosmetic }}
                        />
                      ) : isUnlocked ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                      ) : (
                        <Lock className="w-4 h-4 text-slate-600 shrink-0" />
                      )}
                    </motion.button>
                  );
                })}
              </div>
            </div>
          </div>

          <div className="lg:col-span-3">
            <motion.div
              key={selected.index}
              initial={{ opacity: 0, x: 12 }}
              animate={{ opacity: 1, x: 0 }}
              className="rounded-3xl border border-white/10 bg-white/[0.04] p-6 sm:p-8"
            >
              <div className="flex flex-wrap items-center gap-4 mb-6">
                <div
                  className="flex items-center justify-center w-14 h-14 rounded-2xl text-3xl border"
                  style={{ borderColor: `${selected.cosmetic}66`, background: `${selected.cosmetic}14` }}
                >
                  {selected.emoji}
                </div>
                <div>
                  <h3 className="text-xl font-display font-bold text-white flex items-center gap-2">
                    {selected.title}
                    <span
                      className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold border"
                      style={{ borderColor: `${selected.cosmetic}66`, color: selected.cosmetic }}
                    >
                      LVL {selected.level}
                    </span>
                  </h3>
                  <p className="text-xs text-slate-500 font-mono mt-1">{formatXp(selected.xp_required)} XP required</p>
                </div>
                <span
                  className="ml-auto inline-flex items-center gap-2 px-3 py-2 rounded-xl border border-white/10 bg-white/5"
                  title="Cosmetic profile border"
                >
                  <Palette className="w-4 h-4 text-slate-400" />
                  <span
                    className="w-6 h-6 rounded-full border-2 border-white/20"
                    style={{ backgroundColor: selected.cosmetic }}
                  />
                </span>
              </div>

              <div className="space-y-6">
                <div>
                  <h4 className="text-xs font-mono uppercase tracking-wider text-slate-500 mb-2.5">
                    Perk
                  </h4>
                  <p className="text-sm text-slate-300 leading-relaxed">{selected.title_perk}</p>
                </div>

                <div>
                  <h4 className="text-xs font-mono uppercase tracking-wider text-slate-500 mb-2.5">
                    Unlocks
                  </h4>
                  <FeatureChips features={selected.unlocks} muted={selected.index > data.role_index} />
                </div>

                <div>
                  <h4 className="text-xs font-mono uppercase tracking-wider text-slate-500 mb-2.5">
                    Companies Unlocked
                  </h4>
                  <CompanyChips companies={selected.companies} />
                </div>

                <div>
                  <h4 className="text-xs font-mono uppercase tracking-wider text-slate-500 mb-2.5">
                    Interview Styles
                  </h4>
                  <StyleChips styles={selected.interview_styles} />
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
