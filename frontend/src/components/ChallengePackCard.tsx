import { motion } from "framer-motion";
import { Sparkles, Lock, Star, CheckCircle2, Zap, Clock, Code2 } from "lucide-react";

const RARITY_STYLES = {
  common: {
    border: "border-slate-600/50",
    glow: "shadow-slate-600/20",
    bg: "from-slate-900 to-slate-800",
    accent: "text-slate-400",
    label: "COMMON",
    labelColor: "bg-slate-700 text-slate-300",
  },
  uncommon: {
    border: "border-emerald-600/50",
    glow: "shadow-emerald-600/20",
    bg: "from-slate-900 to-emerald-950/30",
    accent: "text-emerald-400",
    label: "UNCOMMON",
    labelColor: "bg-emerald-700/50 text-emerald-300",
  },
  rare: {
    border: "border-blue-600/50",
    glow: "shadow-blue-600/20",
    bg: "from-slate-900 to-blue-950/30",
    accent: "text-blue-400",
    label: "RARE",
    labelColor: "bg-blue-700/50 text-blue-300",
  },
  epic: {
    border: "border-purple-600/50",
    glow: "shadow-purple-600/30",
    bg: "from-slate-900 to-purple-950/30",
    accent: "text-purple-400",
    label: "EPIC",
    labelColor: "bg-purple-700/50 text-purple-300",
  },
  legendary: {
    border: "border-amber-500/50",
    glow: "shadow-amber-500/30",
    bg: "from-slate-900 to-amber-950/20",
    accent: "text-amber-400",
    label: "LEGENDARY",
    labelColor: "bg-amber-700/50 text-amber-300",
  },
};

const DIFFICULTY_STARS = {
  easy: 1, medium: 2, hard: 3,
};

export default function ChallengePackCard({
  challenge,
  onOpen,
  onSelect,
  selected = false,
  compact = false,
  index = 0,
}: any) {
  const rarity = challenge.rarity || "common";
  const style = RARITY_STYLES[rarity] || RARITY_STYLES.common;
  const stars = DIFFICULTY_STARS[challenge.difficulty] || 1;
  const solved = challenge.solved || false;
  const locked = challenge.locked || false;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, rotateX: -5 }}
      animate={{ opacity: 1, y: 0, rotateX: 0 }}
      transition={{ delay: index * 0.05, duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      whileHover={!locked ? { scale: 1.02, y: -4, transition: { duration: 0.2 } } : {}}
      onClick={() => { if (!locked) onSelect?.(challenge); onOpen?.(challenge); }}
      className={`group relative cursor-pointer ${compact ? "w-48" : "w-full"}`}
    >
      <div
        className={`
          relative rounded-xl border overflow-hidden transition-all duration-300
          ${locked ? "opacity-60 grayscale" : ""}
          ${style.border}
          ${selected ? `ring-2 ring-indigo-500 shadow-lg shadow-indigo-500/20` : `hover:${style.glow} hover:shadow-lg`}
          bg-gradient-to-br ${style.bg}
        `}
      >
        {/* Rarity stripe */}
        <div className={`h-1 w-full bg-gradient-to-r ${style.border.replace("border-", "from-").replace("/50", "/70").replace(" to-", " via-")} to-transparent`} />

        <div className="p-4 space-y-3">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div className={`px-2 py-0.5 rounded text-[9px] font-bold tracking-wider uppercase ${style.labelColor}`}>
              {style.label}
            </div>
            {solved && (
              <div className="flex items-center gap-1 text-[10px] text-emerald-400 font-medium">
                <CheckCircle2 className="w-3 h-3" /> Solved
              </div>
            )}
            {locked && <Lock className="w-4 h-4 text-slate-600" />}
          </div>

          {/* Icon / Emoji */}
          <div className="flex justify-center py-1">
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${rarity === "legendary" ? "from-amber-500/20 to-yellow-500/20" : rarity === "epic" ? "from-purple-500/20 to-pink-500/20" : rarity === "rare" ? "from-blue-500/20 to-cyan-500/20" : "from-slate-700/30 to-slate-600/30"} flex items-center justify-center text-2xl`}>
              {challenge.icon || "⚔️"}
            </div>
          </div>

          {/* Title */}
          <div className="text-center">
            <h3 className={`font-bold text-sm text-text-primary leading-tight ${compact ? "truncate" : ""}`}>
              {challenge.title || challenge.question_title || "Challenge"}
            </h3>
            <p className={`text-[10px] text-slate-500 mt-0.5 ${compact ? "truncate" : "line-clamp-2"}`}>
              {challenge.description || challenge.topic || challenge.category || ""}
            </p>
          </div>

          {/* Stats row */}
          <div className="flex items-center justify-center gap-2 text-[10px] text-slate-500">
            <span className="flex items-center gap-1">
              {Array.from({ length: 3 }).map((_, i) => (
                <Star key={i} className={`w-2.5 h-2.5 ${i < stars ? "text-amber-400 fill-amber-400" : "text-slate-700"}`} />
              ))}
            </span>
            {challenge.xp_reward && (
              <span className="flex items-center gap-1 text-indigo-400">
                <Zap className="w-3 h-3" /> +{challenge.xp_reward}
              </span>
            )}
          </div>

          {/* Tags */}
          {challenge.tags && challenge.tags.length > 0 && (
            <div className="flex flex-wrap gap-1 justify-center">
              {challenge.tags.slice(0, 2).map((tag) => (
                <span key={tag} className="px-1.5 py-0.5 rounded bg-slate-800 text-[8px] text-slate-400 font-mono">
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Action button */}
          {!locked && (
            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={(e) => { e.stopPropagation(); onOpen?.(challenge); }}
              className={`
                w-full py-2 rounded-lg text-xs font-bold tracking-wider uppercase transition-all duration-200
                ${solved
                  ? "bg-emerald-600/20 text-emerald-400 border border-emerald-600/30"
                  : "bg-indigo-600 hover:bg-indigo-500 text-text-primary shadow-lg shadow-indigo-600/20"
                }
              `}
            >
              {solved ? "Practice Again" : "Open Challenge"}
            </motion.button>
          )}
        </div>

        {/* Solved overlay */}
        {solved && (
          <div className="absolute top-2 right-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 drop-shadow-lg" />
          </div>
        )}
      </div>
    </motion.div>
  );
}
