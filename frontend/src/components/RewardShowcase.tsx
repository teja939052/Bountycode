import { motion } from "framer-motion";
import { Zap, Flame, Star, ArrowUp, Snowflake, Trophy, Skull } from "lucide-react";

type RewardBreakdown = {
  baseXP: number;
  multipliers: {
    streak: number;
    combo: number;
    first_of_day: boolean;
    critical: number;
    double_xp: boolean;
  };
  totalXP: number;
  coins: number;
  stars: number;
  streak: number;
  leveledUp: boolean;
  newLevel?: number;
  newBadges?: unknown[];
  milestone?: Record<string, unknown>;
  bossLevel?: number | null;
  streakFrozen?: boolean;
};

type RewardShowcaseProps = {
  visible: boolean;
  breakdown: RewardBreakdown | null;
  onContinue?: () => void;
};

export default function RewardShowcase({ visible, breakdown, onContinue }: RewardShowcaseProps) {
  if (!visible || !breakdown) return null;

  const m = breakdown.multipliers;
  const chips: { label: string; value: string; icon: typeof Zap; highlight?: boolean }[] = [];
  if (m.streak > 1) chips.push({ label: "Streak", value: `${m.streak.toFixed(2)}×`, icon: Flame, highlight: m.streak >= 2 });
  if (m.combo > 1) chips.push({ label: "Combo", value: `${m.combo.toFixed(2)}×`, icon: Zap, highlight: m.combo >= 2 });
  if (m.critical > 1) chips.push({ label: "Crit", value: `${m.critical.toFixed(2)}×`, icon: Star, highlight: true });
  if (m.double_xp) chips.push({ label: "Double Diamonds", value: "2×", icon: Star, highlight: true });
  if (m.first_of_day) chips.push({ label: "First solve", value: "2×", icon: Star, highlight: false });

  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={onContinue} />
      <motion.div
        className="relative w-full max-w-md rounded-3xl border border-white/10 bg-gray-950/90 p-6 shadow-2xl"
        initial={{ opacity: 0, y: 30, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ type: "spring", stiffness: 180, damping: 16 }}
      >
        <div className="flex items-center justify-between mb-5">
          <div>
            <p className="text-xs font-mono uppercase tracking-widest text-gray-500">Session reward</p>
            <h2 className="text-2xl font-black text-white">+{breakdown.totalXP} Diamonds</h2>
          </div>
          <button onClick={onContinue} className="rounded-full bg-white/10 px-3 py-1 text-xs font-mono text-gray-300 hover:bg-white/20">
            Continue
          </button>
        </div>

        <div className="rounded-2xl bg-white/5 p-4 mb-4">
          <p className="text-[10px] font-mono uppercase tracking-widest text-gray-500 mb-2">How you earned it</p>
          <div className="flex flex-wrap items-center gap-2 text-sm font-mono">
            <span className="text-gray-300">Base {breakdown.baseXP}</span>
            {chips.map((chip) => (
              <span key={chip.label} className="flex items-center gap-1">
                <span className="text-gray-500">×</span>
                <span className={`flex items-center gap-1 ${chip.highlight ? "text-amber-300" : "text-gray-200"}`}>
                  <chip.icon size={14} /> {chip.value}
                </span>
              </span>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-3 gap-2 mb-5">
          <div className="rounded-xl bg-white/5 p-3 text-center">
            <p className="text-[10px] font-mono uppercase tracking-widest text-gray-500 mb-1">Stars</p>
            <p className="text-lg font-black text-amber-300">+{breakdown.stars}</p>
          </div>
          <div className="rounded-xl bg-white/5 p-3 text-center">
            <p className="text-[10px] font-mono uppercase tracking-widest text-gray-500 mb-1">Coins</p>
            <p className="text-lg font-black text-yellow-300">+{breakdown.coins}</p>
          </div>
          <div className="rounded-xl bg-white/5 p-3 text-center">
            <p className="text-[10px] font-mono uppercase tracking-widest text-gray-500 mb-1">Streak</p>
            <p className="text-lg font-black text-orange-400">{breakdown.streak}d</p>
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {breakdown.leveledUp && (
            <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/15 px-2.5 py-1 text-xs font-mono text-emerald-300 border border-emerald-500/25">
              <ArrowUp size={14} /> Level {breakdown.newLevel}
            </span>
          )}
          {breakdown.newBadges && breakdown.newBadges.length > 0 && (
            <span className="inline-flex items-center gap-1 rounded-full bg-yellow-500/15 px-2.5 py-1 text-xs font-mono text-yellow-300 border border-yellow-500/25">
              <Trophy size={14} /> {breakdown.newBadges.length} badge{breakdown.newBadges.length > 1 ? "s" : ""}
            </span>
          )}
          {breakdown.milestone && Object.keys(breakdown.milestone).length > 0 && (
            <span className="inline-flex items-center gap-1 rounded-full bg-orange-500/15 px-2.5 py-1 text-xs font-mono text-orange-300 border border-orange-500/25">
              🎁 Milestone
            </span>
          )}
          {breakdown.bossLevel && (
            <span className="inline-flex items-center gap-1 rounded-full bg-red-500/15 px-2.5 py-1 text-xs font-mono text-red-300 border border-red-500/25">
              <Skull size={14} /> Boss {breakdown.bossLevel}
            </span>
          )}
          {breakdown.streakFrozen && (
            <span className="inline-flex items-center gap-1 rounded-full bg-sky-500/10 px-2.5 py-1 text-xs font-mono text-sky-300 border border-sky-500/20">
              <Snowflake size={14} /> Freeze saved streak
            </span>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}
