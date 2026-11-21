export function TowerProgress({ level, diamonds, xpForNext }: { level: number; diamonds: number; xpForNext: number }) {
  const pct = xpForNext > 0 ? Math.min(100, Math.round((diamonds / xpForNext) * 100)) : 0;
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
      <div className="flex justify-between text-xs font-mono text-gray-500 mb-1">
        <span>Level {level}</span>
        <span>{pct}%</span>
      </div>
      <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
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
          <h3 className="text-sm font-bold text-red-600">Boss Battle — Level {level}</h3>
          <p className="text-xs text-gray-500">{boss?.name || "Unknown Boss"}</p>
        </div>
        <div className="flex gap-2">
          {canSkip && <button onClick={onSkip} className="px-3 py-1.5 text-xs rounded-lg bg-slate-100 text-gray-600 hover:bg-slate-100">Skip</button>}
          <button onClick={onFight} className="px-3 py-1.5 text-xs rounded-lg bg-red-500 text-white hover:bg-red-600">Fight!</button>
        </div>
      </div>
    </div>
  );
}

export function StarsDisplay({ stars }: { stars: number }) {
  return (
    <div className="flex items-center gap-1 text-yellow-600 text-xs font-mono">
      <span>⭐</span>
      <span>{stars}</span>
    </div>
  );
}

export function PowerUpShop({ coins, owned, onBuy, onUse }: { coins: number; owned: any; onBuy: (id: string) => void; onUse: (id: string) => void }) {
  const powerUps = [
    { id: "skip_boss", name: "Skip Boss", cost: 50, emoji: "⏭️" },
    { id: "double_xp", name: "2x Diamonds", cost: 30, emoji: "⚡" },
    { id: "hint_reveal", name: "Hint", cost: 20, emoji: "💡" },
  ];
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <h3 className="text-xs font-mono uppercase tracking-widest text-gray-500 mb-3">Power-Up Shop</h3>
      <div className="flex items-center gap-1 text-xs text-yellow-600 mb-3">🪙 {coins} coins</div>
      <div className="grid grid-cols-3 gap-2">
        {powerUps.map((p) => (
          <div key={p.id} className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-center">
            <span className="text-xl">{p.emoji}</span>
            <p className="text-[10px] text-gray-500 mt-1">{p.name}</p>
            <p className="text-[10px] text-yellow-600">{p.cost}🪙</p>
            <button onClick={() => onBuy(p.id)} className="mt-2 w-full text-[10px] py-1 rounded bg-emerald-600 text-white hover:bg-emerald-500">Buy</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export function StreakFreeze({ streakFreezes, coins }: { streakFreezes: number; coins: number }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <h3 className="text-xs font-mono uppercase tracking-widest text-gray-500 mb-2">Streak Freeze</h3>
      <div className="flex items-center gap-2 text-sm">
        <span className="text-blue-600">❄️</span>
        <span className="text-gray-600">{streakFreezes} freezes remaining</span>
      </div>
      <p className="text-[10px] text-gray-500 mt-1">Protects your streak from missed days</p>
    </div>
  );
}

export function DailyGoal() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <h3 className="text-xs font-mono uppercase tracking-widest text-gray-500 mb-2">Daily Goal</h3>
      <p className="text-xs text-gray-500">Complete daily practice to maintain your streak</p>
    </div>
  );
}

export function getTitleForLevel(level: number): [string, string] {
  const zones = [
    { maxLevel: 10, title: "Seedling Grove", emoji: "\u{1F331}" },
    { maxLevel: 20, title: "Sapling Orchard", emoji: "\u{1F33F}" },
    { maxLevel: 30, title: "Young Forest", emoji: "\u{1F333}" },
    { maxLevel: 40, title: "Canopy Trail", emoji: "\u{1F343}" },
    { maxLevel: 50, title: "Fruiting Tree", emoji: "\u{1F34E}" },
    { maxLevel: 60, title: "Ancient Woods", emoji: "\u{1F332}" },
    { maxLevel: 70, title: "Summit Grove", emoji: "\u{26F0}\u{FE0F}" },
    { maxLevel: 80, title: "Crown Canopy", emoji: "\u{1F451}" },
    { maxLevel: 90, title: "Legend Tree", emoji: "\u{1F31F}" },
    { maxLevel: 100, title: "World Tree", emoji: "\u{1F30D}" },
  ];

  const safeLevel = Number.isFinite(level)
    ? Math.min(100, Math.max(1, Math.floor(level)))
    : 1;

  const zone = zones.find((item) => safeLevel <= item.maxLevel) ?? zones[9];

  return [zone.title, zone.emoji];
}