import { motion } from "framer-motion";

const CHARACTERS = [
  { minLevel: 1,  emoji: "🧢", label: "Deckhand" },
  { minLevel: 10, emoji: "⚔️", label: "Corsair" },
  { minLevel: 20, emoji: "🦜", label: "Sea Dog" },
  { minLevel: 30, emoji: "🧭", label: "Navigator" },
  { minLevel: 40, emoji: "🏹", label: "Master Gunner" },
  { minLevel: 50, emoji: "🐉", label: "Dragon Captain" },
  { minLevel: 60, emoji: "👑", label: "Commodore" },
  { minLevel: 70, emoji: "🌟", label: "Admiral" },
  { minLevel: 80, emoji: "💎", label: "Privateer" },
  { minLevel: 90, emoji: "🌍", label: "Pirate King" },
];

const VOYAGES = [
  { index: 0, name: 'Shore Camp',      levelMin: 1,  levelMax: 10,  emoji: '⚓', color: '#7dd3fc', bg: "bg-sky-500/10" },
  { index: 1, name: 'Open Deck',       levelMin: 11, levelMax: 20,  emoji: '🧭', color: '#38bdf8', bg: "bg-blue-500/10" },
  { index: 2, name: 'Crow\'s Nest',    levelMin: 21, levelMax: 30,  emoji: '🪶', color: '#0ea5e9', bg: "bg-cyan-500/10" },
  { index: 3, name: 'Quarterdeck',     levelMin: 31, levelMax: 40,  emoji: '🏴‍☠️', color: '#0284c7', bg: "bg-blue-600/10" },
  { index: 4, name: 'Booty Hold',      levelMin: 41, levelMax: 50,  emoji: '💰', color: '#0369a1', bg: "bg-cyan-600/10" },
  { index: 5, name: 'Sterncastle',     levelMin: 51, levelMax: 60,  emoji: '🌊', color: '#075985', bg: "bg-sky-700/10" },
  { index: 6, name: 'Mizzen Mast',     levelMin: 61, levelMax: 70,  emoji: '⛵', color: '#0c4a6e', bg: "bg-blue-800/10" },
  { index: 7, name: 'Fleet Flagship',  levelMin: 71, levelMax: 80,  emoji: '👑', color: '#164e63', bg: "bg-amber-500/10" },
  { index: 8, name: 'Kraken Wake',     levelMin: 81, levelMax: 90,  emoji: '🐙', color: '#155e75', bg: "bg-amber-500/10" },
  { index: 9, name: 'Endless Sea',     levelMin: 91, levelMax: 100, emoji: '🌊', color: '#083344', bg: "bg-cyan-900/10" },
];

export default function CrewShip({ level = 1, forest, compact = false }: { level?: number; forest?: any; compact?: boolean }) {
  const clampedLevel = Math.max(1, Math.min(level || 1, 100));
  const character = CHARACTERS.slice().reverse().find((c) => clampedLevel >= c.minLevel) || CHARACTERS[0];
  const zoneIndex = Math.min(Math.floor((clampedLevel - 1) / 10), VOYAGES.length - 1);
  const currentVoyage = VOYAGES[zoneIndex];
  const zoneProgress = forest?.zone_progress ?? 0;

  return (
    <div className={`rounded-2xl border border-white/10 bg-white/[0.03] overflow-hidden relative ${compact ? "p-4" : "p-5"}`}>
      <div className="absolute inset-0 pointer-events-none opacity-25"
        style={{
          background: `radial-gradient(circle at 70% 20%, ${currentVoyage.color}40 0%, transparent 55%)`,
        }}
      />

      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-xs font-mono uppercase tracking-widest text-gray-400">⛵ Crew & Ship</h3>
            <p className="text-[10px] text-gray-500 mt-0.5">Voyage {zoneIndex + 1} · {currentVoyage.name}</p>
          </div>
          <motion.div
            className="text-4xl"
            animate={{ y: [0, -6, 0], rotate: [0, 3, -3, 0] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          >
            {character.emoji}
          </motion.div>
        </div>

        <div className="flex items-center gap-2 mb-4">
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <span className="text-[10px] font-mono text-gray-400">Voyage Progress</span>
              <span className="text-[10px] font-mono text-gray-400">{Math.round(zoneProgress * 100)}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-black/30 overflow-hidden">
              <motion.div
                className="h-full rounded-full"
                style={{ backgroundColor: currentVoyage.color }}
                initial={{ width: 0 }}
                animate={{ width: `${Math.round(zoneProgress * 100)}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
              />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-2">
          {VOYAGES.map((voyage, i) => {
            const visited = i < zoneIndex;
            const current = i === zoneIndex;
            return (
              <motion.div
                key={voyage.index}
                className={`shrink-0 flex flex-col items-center gap-1 rounded-xl border p-2 transition-all ${
                  current
                    ? "border-white/40 bg-white/10 scale-110 shadow-lg w-16"
                    : visited
                      ? "border-white/10 bg-white/5 opacity-70 w-14"
                      : "border-white/5 bg-white/[0.02] opacity-30 w-14"
                }`}
                title={voyage.name}
                whileHover={visited || current ? { scale: 1.1 } : {}}
              >
                <span className="text-xl">{voyage.emoji}</span>
                <span className="text-[9px] font-mono text-gray-400 truncate w-full text-center">{voyage.name}</span>
                {current && (
                  <motion.div
                    className="text-[10px] font-bold text-center"
                    style={{ color: voyage.color }}
                    animate={{ opacity: [0.6, 1, 0.6] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    {character.emoji}
                  </motion.div>
                )}
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
