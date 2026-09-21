import { motion } from 'framer-motion';

const VOYAGE_ZONES = [
  { index: 0, name: 'Shore Camp',      levelMin: 1,  levelMax: 10,  stage: 'shore',     emoji: '⚓', color: '#7dd3fc', description: 'You drop anchor. The hull is thin, the sea is wide.' },
  { index: 1, name: 'Open Deck',       levelMin: 11, levelMax: 20,  stage: 'deck',      emoji: '🧭', color: '#38bdf8', description: 'Winds pick up. You learn to read the currents.' },
  { index: 2, name: 'Crow\'s Nest',    levelMin: 21, levelMax: 30,  stage: 'nest',      emoji: '🪶', color: '#0ea5e9', description: 'Higher ground. The horizon shows more routes.' },
  { index: 3, name: 'Quarterdeck',     levelMin: 31, levelMax: 40,  stage: 'quarter',   emoji: '🏴‍☠️', color: '#0284c7', description: 'You steer. The crew follows your heading.' },
  { index: 4, name: 'Booty Hold',      levelMin: 41, levelMax: 50,  stage: 'hold',      emoji: '💰', color: '#0369a1', description: 'Prizes stack up. The ship gets heavier and faster.' },
  { index: 5, name: 'Sterncastle',     levelMin: 51, levelMax: 60,  stage: 'stern',     emoji: '🌊', color: '#075985', description: 'Deep waters. Only seasoned captains sail here.' },
  { index: 6, name: 'Mizzen Mast',     levelMin: 61, levelMax: 70,  stage: 'mizzen',    emoji: '⛵', color: '#0c4a6e', description: 'Rare air. The rigging strains, but holds.' },
  { index: 7, name: 'Fleet Flagship',  levelMin: 71, levelMax: 80,  stage: 'flagship',  emoji: '👑', color: '#164e63', description: 'You command the fleet. The horizon obeys.' },
  { index: 8, name: 'Kraken Wake',     levelMin: 81, levelMax: 90,  stage: 'kraken',    emoji: '🐙', color: '#155e75', description: 'Stories are told about sailors like you.' },
  { index: 9, name: 'Endless Sea',     levelMin: 91, levelMax: 100, stage: 'endless',   emoji: '🌊', color: '#083344', description: 'Your keel cuts the world. The sea is yours.' },
];

export default function ShipJourney({ forest, level }: { forest: any; level: number }) {
  if (!forest) return null;

  const zoneIndex = Math.min(forest.zone_index ?? 0, VOYAGE_ZONES.length - 1);
  const zoneProgress = forest.zone_progress ?? 0;
  const currentZone = VOYAGE_ZONES[zoneIndex];

  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 mt-6 overflow-hidden relative">
      {/* Background ambient glow */}
      <div className="absolute inset-0 pointer-events-none opacity-30"
        style={{
          background: `radial-gradient(circle at 70% 20%, ${currentZone.color}40 0%, transparent 60%)`,
        }}
      />

      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xs font-mono uppercase tracking-widest text-gray-400">⛵ Ship’s Journey</h3>
          <span className="text-[10px] font-mono text-gray-500">Level {level}</span>
        </div>

        {/* Current zone highlight */}
        <motion.div
          className="rounded-xl p-4 mb-4 border relative overflow-hidden"
          style={{
            backgroundColor: `${currentZone.color}15`,
            borderColor: `${currentZone.color}40`,
          }}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          {/* Animated shimmer */}
          <motion.div
            className="absolute inset-0 opacity-20"
            style={{
              background: `linear-gradient(90deg, transparent, ${currentZone.color}60, transparent)`,
            }}
            animate={{ x: ['-100%', '200%'] }}
            transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
          />

          <div className="relative flex items-center gap-4">
            <motion.div
              className="text-5xl"
              animate={{ scale: [1, 1.1, 1], rotate: [0, 5, -5, 0] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              {currentZone.emoji}
            </motion.div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-bold text-gray-200">{currentZone.name}</div>
              <div className="text-xs text-gray-400 mt-0.5">{currentZone.description}</div>
              <div className="mt-2.5 h-2 w-full rounded-full bg-black/30 overflow-hidden">
                <motion.div
                  className="h-full rounded-full relative"
                  style={{ backgroundColor: currentZone.color }}
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.round(zoneProgress * 100)}%` }}
                  transition={{ duration: 0.8, ease: 'easeOut' }}
                >
                  <div className="absolute inset-0 overflow-hidden rounded-full">
                    <div
                      className="absolute inset-0"
                      style={{
                        background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent)',
                        animation: 'shimmer 2s infinite',
                      }}
                    />
                  </div>
                </motion.div>
              </div>
              <div className="mt-1.5 text-[10px] font-mono text-gray-500">
                {Math.round(zoneProgress * 100)}% through this zone
              </div>
            </div>
          </div>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <Stat icon="☀️" label="Gold" value={forest.sunlight?.toLocaleString() ?? 0} unit="Diamonds" color="#fbbf24" />
          <Stat icon="🍺" label="Rum" value={forest.waterings ?? 0} unit="streak" color="#60a5fa" />
          <Stat icon="💎" label="Treasures" value={forest.seeds ?? 0} unit="badges" color="#a78bfa" />
          <Stat icon="⛈️" label="Sea Battles" value={forest.storms_cleared ?? 0} unit="bosses" color="#f87171" />
        </div>

        {/* Current storm */}
        {forest.current_storm && (
          <motion.div
            className="mt-4 rounded-xl bg-red-950/30 border border-red-500/20 p-3 flex items-center gap-3"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
          >
            <motion.span
              className="text-3xl"
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {forest.current_storm.emoji ?? '⛈️'}
            </motion.span>
            <div>
              <div className="text-xs font-bold text-red-300">Sea Battle: {forest.current_storm.name ?? 'Boss Battle'}</div>
              <div className="text-[10px] text-red-400 mt-0.5">Defeat this boss to clear the storm and grow stronger.</div>
            </div>
          </motion.div>
        )}

        {/* Zone map */}
        <div className="mt-5">
          <div className="text-[10px] font-mono text-gray-500 mb-2">All Zones</div>
          <div className="flex items-center gap-1.5 overflow-x-auto pb-2">
            {VOYAGE_ZONES.map((zone, i) => {
              const visited = i < zoneIndex;
              const current = i === zoneIndex;
              return (
                <motion.div
                  key={zone.index}
                  className={`shrink-0 w-11 h-11 rounded-xl flex items-center justify-center text-xl border transition-all ${
                    current
                      ? 'border-white/40 bg-white/10 scale-110 shadow-lg'
                      : visited
                        ? 'border-white/10 bg-white/5 opacity-60'
                        : 'border-white/5 bg-white/[0.02] opacity-25'
                  }`}
                  title={zone.name}
                  whileHover={visited || current ? { scale: 1.15 } : {}}
                >
                  {zone.emoji}
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

function Stat({ icon, label, value, unit }: { icon: string; label: string; value: number; unit: string; color: string }) {
  return (
    <motion.div
      className="rounded-xl bg-white/[0.03] border border-white/5 p-3"
      whileHover={{ scale: 1.05 }}
    >
      <div className="text-lg">{icon}</div>
      <div className="text-[10px] font-mono text-gray-500 mt-1">{label}</div>
      <div className="text-sm font-bold text-gray-200">
        {value.toLocaleString()} <span className="text-[10px] font-mono text-gray-500">{unit}</span>
      </div>
    </motion.div>
  );
}


