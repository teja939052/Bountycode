import { Flame, Zap, Shield } from "lucide-react";
import { getLevelForXP, getXPForLevel, getLevelColor } from "./XPBar";
import { useGamification } from "../hooks/useGamification";

const LEAGUE_TIERS = [
  { key: "diamond", name: "Diamond", icon: "♦️", color: "text-blue-400" },
  { key: "platinum", name: "Platinum", icon: "💎", color: "text-gray-300" },
  { key: "gold", name: "Gold", icon: "🥇", color: "text-yellow-400" },
  { key: "silver", name: "Silver", icon: "🥈", color: "text-gray-400" },
  { key: "bronze", name: "Bronze", icon: "🥉", color: "text-amber-600" },
];

function leagueBadge(weeklyXp) {
  const xp = weeklyXp || 0;
  const tier = xp >= 10000 ? LEAGUE_TIERS[0]
    : xp >= 4000 ? LEAGUE_TIERS[1]
    : xp >= 1500 ? LEAGUE_TIERS[2]
    : xp >= 500 ? LEAGUE_TIERS[3]
    : LEAGUE_TIERS[4];
  return tier;
}

export default function GamificationStrip({ compact = false }: { compact?: boolean }) {
  const { profile, startup, loading } = useGamification();

  if (loading || !profile) {
    return compact ? null : (
      <div className="h-8 w-40 rounded-full bg-gray-100 animate-pulse" />
    );
  }

  const xp = profile.xp || 0;
  const level = profile.level || getLevelForXP(xp);
  const color = getLevelColor(level);
  const streak = profile.streak || 0;
  const freezes = profile.streak_freezes || startup?.streak_freezes || 0;
  const protectedToday = startup?.streak_protected;
  const tier = startup?.tier || leagueBadge(startup && startup.xp ? startup.xp : 0);

  const curLevelXP = getXPForLevel(level);
  const nextLevelXP = getXPForLevel(level + 1);
  const progress = nextLevelXP > curLevelXP ? ((xp - curLevelXP) / (nextLevelXP - curLevelXP)) * 100 : 100;

  if (compact) {
    return (
      <div className="flex items-center gap-2.5 shrink-0">
        <div
          className="w-6 h-6 rounded-lg flex items-center justify-center font-display font-black text-[10px]"
          style={{
            background: `linear-gradient(135deg, ${color.from}40, ${color.to}30)`,
            border: `1px solid ${color.from}50`,
            color: color.from,
          }}
        >
          {level}
        </div>
        <div className="flex items-center gap-1 text-xs font-mono text-text-light">
          <Zap size={12} className="text-yellow-500" />
          <span className="text-text-primary font-bold">{xp.toLocaleString()}</span>
        </div>
         {streak > 0 && (
           <div className="flex items-center gap-0.5 text-xs font-mono text-orange-500">
             <Flame size={12} />
             <span>{streak}</span>
           </div>
         )}
         {freezes > 0 && (
           <div className="flex items-center gap-0.5 text-xs font-mono text-sky-500" title="streak protection held">
             <Shield size={12} />
             <span>{freezes}</span>
           </div>
         )}
         {protectedToday && (
           <span className="text-[9px] font-mono text-green-500" title="streak protected today">🛡️</span>
         )}
         <span className="text-xs leading-none" title={`League: ${tier.name}`}>
          {tier.icon}
        </span>
       </div>
     );
   }

  return (
    <div className="flex items-center gap-3">
      <div
        className="w-8 h-8 rounded-xl flex items-center justify-center font-display font-black text-sm"
        style={{
          background: `linear-gradient(135deg, ${color.from}30, ${color.to}20)`,
          border: `2px solid ${color.from}50`,
          color: color.from,
        }}
      >
        {level}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[10px] font-mono text-text-light">Level {level}</span>
          <span className="text-[10px] font-mono text-text-light">
            {xp - curLevelXP} / {nextLevelXP - curLevelXP} XP
          </span>
        </div>
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-all"
            style={{
              width: `${progress}%`,
              background: `linear-gradient(90deg, ${color.from}, ${color.to})`,
            }}
          />
        </div>
      </div>
      {streak > 0 && (
        <div className="flex items-center gap-1 text-xs font-mono text-orange-500 shrink-0">
          <Flame size={14} className="text-orange-500" />
          <span className="font-bold">{streak}</span>
        </div>
      )}
    </div>
  );
}
