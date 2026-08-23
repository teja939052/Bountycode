import { motion } from "framer-motion";

interface BountyCardProps {
  user: {
    name: string;
    display_title?: string;
    avatar_url?: string;
    bounty: number;
    bounty_formatted: string;
    tier: { title: string; color: string; stars: number; tier: string };
    level: number;
    streak: number;
    readiness?: number;
    categories?: Record<string, number>;
    problems_solved?: number;
    badges_count?: number;
    bosses_defeated?: number;
    status?: string;
  };
  size?: "small" | "medium" | "large";
  showStats?: boolean;
}

const SIZE_MAP = {
  small: { card: "w-56", avatar: "w-14 h-14", name: "text-sm", bounty: "text-lg" },
  medium: { card: "w-72", avatar: "w-20 h-20", name: "text-base", bounty: "text-2xl" },
  large: { card: "w-80", avatar: "w-28 h-28", name: "text-lg", bounty: "text-3xl" },
};

const STATUS_BORDER: Record<string, string> = {
  active: "border-green-500/60",
  inactive: "border-gray-500/40",
  legendary: "border-yellow-400/60",
};

const CATEGORY_ICONS: Record<string, string> = {
  dsa: "⚔️", system_design: "🛡️", behavioral: "🧠",
  resume: "📄", aptitude: "📊", coding: "💻",
};

export default function BountyCard({ user, size = "medium", showStats = true }: BountyCardProps) {
  const s = SIZE_MAP[size];
  const color = user.tier?.color || "#9CA3AF";
  const status = user.status || "active";

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      whileHover={{ scale: 1.03, rotate: -0.5 }}
      className={`relative ${s.card} bg-gradient-to-br from-amber-950/90 to-amber-900/90 border-2 ${STATUS_BORDER[status] || STATUS_BORDER.active} rounded-2xl overflow-hidden shadow-2xl`}
    >
      {/* Aged paper texture overlay */}
      <div className="absolute inset-0 opacity-[0.03] bg-gradient-to-b from-white/20 to-transparent pointer-events-none" />

      {/* Top bar */}
      <div className="relative px-4 pt-3 pb-2 border-b border-amber-700/30">
        <div className="flex items-center justify-between">
          <span className="text-[9px] font-bold tracking-[0.3em] text-amber-400/50 uppercase">WANTED</span>
          <span className="text-xs text-amber-400/70">
            {"★".repeat(user.tier?.stars || 1)}
          </span>
        </div>
        <div className="text-center mt-1">
          <span className={`${s.bounty} font-black text-amber-300 tracking-tight`}>
            {user.bounty_formatted}
          </span>
          <span className="text-[10px] text-amber-400/50 ml-1">BELLI</span>
        </div>
      </div>

      {/* Avatar */}
      <div className="relative px-4 pt-4 pb-3 flex flex-col items-center">
        <div
          className={`${s.avatar} rounded-full border-[3px] overflow-hidden bg-gradient-to-br from-amber-800 to-amber-700 shadow-lg`}
          style={{ borderColor: `${color}88`, boxShadow: `0 0 20px ${color}22` }}
        >
          {user.avatar_url ? (
            <img src={user.avatar_url} alt={user.name} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center font-black text-amber-200"
              style={{ fontSize: size === "small" ? 20 : size === "large" ? 36 : 28 }}>
              {user.name?.charAt(0) || "?"}
            </div>
          )}
        </div>
        <h3 className={`${s.name} font-bold text-text-primary mt-3 tracking-wide text-center`}>{user.name}</h3>
        <p className="text-[10px] font-medium uppercase tracking-wider mt-0.5"
          style={{ color }}>
          &ldquo;{user.display_title || user.tier?.title}&rdquo;
        </p>
      </div>

      {/* Stats */}
      {showStats && (
        <div className="relative px-4 py-3 bg-surface-2 border-t border-amber-700/30">
          <div className="grid grid-cols-2 gap-x-3 gap-y-1.5 text-[11px]">
            <div className="flex justify-between">
              <span className="text-amber-400/50">LVL</span>
              <span className="text-text-primary font-semibold">{user.level}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-amber-400/50">🔥</span>
              <span className="text-text-primary font-semibold">{user.streak}d</span>
            </div>
            {user.categories && Object.entries(user.categories).slice(0, 4).map(([k, v]) => (
              <div key={k} className="flex justify-between">
                <span className="text-amber-400/50">{CATEGORY_ICONS[k] || "•"} {k.slice(0, 4)}</span>
                <span className="text-text-primary font-semibold">{Math.round(v)}%</span>
              </div>
            ))}
          </div>
          <div className="mt-2 pt-2 border-t border-amber-700/20 flex justify-between text-[9px] text-amber-400/40">
            <span>Placement Pro</span>
            <span>
              {user.bosses_defeated ? `💀 ${user.bosses_defeated}` : ""}
              {user.problems_solved ? ` 📋 ${user.problems_solved}` : ""}
            </span>
          </div>
        </div>
      )}

      {/* Corner decorations */}
      <div className="absolute top-1.5 left-1.5 w-3 h-3 border-t-2 border-l-2 border-amber-500/25 rounded-tl" />
      <div className="absolute top-1.5 right-1.5 w-3 h-3 border-t-2 border-r-2 border-amber-500/25 rounded-tr" />
      <div className="absolute bottom-1.5 left-1.5 w-3 h-3 border-b-2 border-l-2 border-amber-500/25 rounded-bl" />
      <div className="absolute bottom-1.5 right-1.5 w-3 h-3 border-b-2 border-r-2 border-amber-500/25 rounded-br" />
    </motion.div>
  );
}
