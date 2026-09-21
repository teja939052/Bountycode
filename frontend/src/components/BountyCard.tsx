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
      initial={{ scale: 0.9, opacity: 0, rotateX: 10 }}
      animate={{ scale: 1, opacity: 1, rotateX: 0 }}
      whileHover={{ scale: 1.03, rotateY: -2 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className={`relative ${s.card} gamification-card rounded-2xl overflow-hidden`}
    >
      {/* Animated gradient border glow */}
      <div className="absolute inset-0 rounded-2xl opacity-60 pointer-events-none" style={{ background: `linear-gradient(135deg, ${color}33, transparent, ${color}33)` }} />

      {/* Top bar */}
      <div className="relative px-4 pt-4 pb-2 border-b border-white/10">
        <div className="flex items-center justify-between">
          <span className="text-[9px] font-bold tracking-[0.3em] text-gray-500 uppercase">WANTED</span>
          <span className="text-xs text-gray-400">
            {"★".repeat(user.tier?.stars || 1)}
          </span>
        </div>
        <div className="text-center mt-2">
          <span className={`${s.bounty} font-black bg-gradient-to-r from-amber-300 via-yellow-200 to-amber-300 bg-clip-text text-transparent tracking-tight`}>
            {user.bounty_formatted}
          </span>
          <span className="text-[10px] text-gray-500 ml-1 font-medium">BELLI</span>
        </div>
      </div>

      {/* Avatar */}
      <div className="relative px-4 pt-5 pb-3 flex flex-col items-center">
        <div
          className={`${s.avatar} rounded-full border-[3px] overflow-hidden bg-gradient-to-br from-gray-800 to-gray-700 shadow-lg`}
          style={{ borderColor: `${color}88`, boxShadow: `0 0 24px ${color}33, inset 0 0 12px ${color}22` }}
        >
          {user.avatar_url ? (
            <img src={user.avatar_url} alt={user.name} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center font-black text-gray-200"
              style={{ fontSize: size === "small" ? 20 : size === "large" ? 36 : 28 }}>
              {user.name?.charAt(0) || "?"}
            </div>
          )}
        </div>
        <h3 className={`${s.name} font-bold text-white mt-3 tracking-wide text-center`}>{user.name}</h3>
        <p className="text-[10px] font-medium uppercase tracking-wider mt-0.5"
          style={{ color }}>
          &ldquo;{user.display_title || user.tier?.title}&rdquo;
        </p>
      </div>

      {/* Stats */}
      {showStats && (
        <div className="relative px-4 py-3 bg-black/20 border-t border-white/10">
          <div className="grid grid-cols-2 gap-x-3 gap-y-1.5 text-[11px]">
            <div className="flex justify-between">
              <span className="text-gray-500">LVL</span>
              <span className="text-white font-semibold">{user.level}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">🔥</span>
              <span className="text-white font-semibold">{user.streak}d</span>
            </div>
            {user.categories && Object.entries(user.categories).slice(0, 4).map(([k, v]) => (
              <div key={k} className="flex justify-between">
                <span className="text-gray-500">{CATEGORY_ICONS[k] || "•"} {k.slice(0, 4)}</span>
                <span className="text-white font-semibold">{Math.round(v)}%</span>
              </div>
            ))}
          </div>
          <div className="mt-2 pt-2 border-t border-white/10 flex justify-between text-[9px] text-gray-500">
            <span>Placement Pro</span>
            <span>
              {user.bosses_defeated ? `💀 ${user.bosses_defeated}` : ""}
              {user.problems_solved ? ` 📋 ${user.problems_solved}` : ""}
            </span>
          </div>
        </div>
      )}

      {/* Corner decorations */}
      <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 rounded-tl-lg pointer-events-none" style={{ borderColor: `${color}44` }} />
      <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 rounded-tr-lg pointer-events-none" style={{ borderColor: `${color}44` }} />
      <div className="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 rounded-bl-lg pointer-events-none" style={{ borderColor: `${color}44` }} />
      <div className="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 rounded-br-lg pointer-events-none" style={{ borderColor: `${color}44` }} />
    </motion.div>
  );
}
