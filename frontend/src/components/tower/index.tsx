export function getTitleForLevel(level: number): [string, string] {
  if (level >= 90) return ["World Tree", "🌍"];
  if (level >= 80) return ["Legend", "🌟"];
  if (level >= 70) return ["Crown", "👑"];
  if (level >= 60) return ["Summit", "⛰️"];
  if (level >= 50) return ["Ancient", "🌲"];
  if (level >= 40) return ["Canopy", "🍃"];
  if (level >= 30) return ["Young", "🌳"];
  if (level >= 20) return ["Sapling", "🌿"];
  if (level >= 10) return ["Sprout", "🌱"];
  return ["Seedling", "🌱"];
}

export function TowerProgress({ level, xp, xpForNext }: { level: number; xp: number; xpForNext: number }) {
  const pct = xpForNext > 0 ? Math.min(100, Math.round((xp / xpForNext) * 100)) : 0;
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
      <div className="flex justify-between text-xs font-mono text-gray-400 mb-1">
        <span>Level {level}</span>
        <span>{pct}%</span>
      </div>
      <div className="h-2 rounded-full bg-gray-800 overflow-hidden">
        <div className="h-full rounded-full bg-emerald-500 transition-all" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export function BossBattle({ boss, level, onFight, canSkip, onSkip }: { boss: any; level: number; onFight: () => void; canSkip: boolean; onSkip: () => void }) {
  return (
    <div className="rounded-2xl border border-red-500/30 bg-red-500/5 p-4 mb-4">
      <div className="flex items-center gap-3">
        <span className="text-3xl">{boss?.emoji || "👹"}</span>
        <div className="flex-1">
          <h3 className="text-sm font-bold text-red-400">Boss Battle — Level {level}</h3>
          <p className="text-xs text-gray-400">{boss?.name || "Unknown Boss"}</p>
        </div>
        <div className="flex gap-2">
          {canSkip && <button onClick={onSkip} className="px-3 py-1.5 text-xs rounded-lg bg-gray-700 text-gray-300 hover:bg-gray-600">Skip</button>}
          <button onClick={onFight} className="px-3 py-1.5 text-xs rounded-lg bg-red-500 text-white hover:bg-red-600">Fight!</button>
        </div>
      </div>
    </div>
  );
}

export function StarsDisplay({ stars }: { stars: number }) {
  return (
    <div className="flex items-center gap-1 text-yellow-400 text-xs font-mono">
      <span>⭐</span>
      <span>{stars}</span>
    </div>
  );
}

export function PowerUpShop({ coins, owned, onBuy, onUse }: { coins: number; owned: any; onBuy: (id: string) => void; onUse: (id: string) => void }) {
  const powerUps = [
    { id: "skip_boss", name: "Skip Boss", cost: 50, emoji: "⏭️" },
    { id: "double_xp", name: "2x XP", cost: 30, emoji: "⚡" },
    { id: "hint_reveal", name: "Hint", cost: 20, emoji: "💡" },
  ];
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
      <h3 className="text-xs font-mono uppercase tracking-widest text-gray-500 mb-3">Power-Up Shop</h3>
      <div className="flex items-center gap-1 text-xs text-yellow-400 mb-3">🪙 {coins} coins</div>
      <div className="grid grid-cols-3 gap-2">
        {powerUps.map((p) => (
          <div key={p.id} className="rounded-xl border border-white/10 bg-white/[0.02] p-3 text-center">
            <span className="text-xl">{p.emoji}</span>
            <p className="text-[10px] text-gray-400 mt-1">{p.name}</p>
            <p className="text-[10px] text-yellow-400">{p.cost}🪙</p>
            <button onClick={() => onBuy(p.id)} className="mt-2 w-full text-[10px] py-1 rounded bg-emerald-600 text-white hover:bg-emerald-500">Buy</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export function StreakFreeze({ streakFreezes, coins }: { streakFreezes: number; coins: number }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
      <h3 className="text-xs font-mono uppercase tracking-widest text-gray-500 mb-2">Streak Freeze</h3>
      <div className="flex items-center gap-2 text-sm">
        <span className="text-blue-400">❄️</span>
        <span className="text-gray-300">{streakFreezes} freezes remaining</span>
      </div>
      <p className="text-[10px] text-gray-500 mt-1">Protects your streak from missed days</p>
    </div>
  );
}

export function DailyGoal() {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
      <h3 className="text-xs font-mono uppercase tracking-widest text-gray-500 mb-2">Daily Goal</h3>
      <p className="text-xs text-gray-400">Complete daily practice to maintain your streak</p>
    </div>
  );
}
