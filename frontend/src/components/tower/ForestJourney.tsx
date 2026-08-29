import { motion } from 'framer-motion';

const FOREST_ZONES = [
  { index: 0, name: 'Seedling Grove',  levelMin: 1,  levelMax: 10,  stage: 'seedling',   emoji: '🌱', color: '#a7f3d0', description: 'You sprout. Tiny roots, big potential.' },
  { index: 1, name: 'Sapling Orchard', levelMin: 11, levelMax: 20,  stage: 'sapling',    emoji: '🌿', color: '#86efac', description: 'Flexible, fast-growing, reaching for the light.' },
  { index: 2, name: 'Young Forest',    levelMin: 21, levelMax: 30,  stage: 'young',      emoji: '🌳', color: '#4ade80', description: 'The grove thickens; branches learn to hold weight.' },
  { index: 3, name: 'Canopy Trail',    levelMin: 31, levelMax: 40,  stage: 'canopy',     emoji: '🍃', color: '#22c55e', description: 'You climb above the undergrowth toward the sun.' },
  { index: 4, name: 'Fruiting Tree',   levelMin: 41, levelMax: 50,  stage: 'fruiting',   emoji: '🍎', color: '#16a34a', description: 'Knowledge starts bearing fruit others can share.' },
  { index: 5, name: 'Ancient Woods',   levelMin: 51, levelMax: 60,  stage: 'ancient',    emoji: '🌲', color: '#15803d', description: 'Deep roots, deep rings, quiet resilience.' },
  { index: 6, name: 'Summit Grove',    levelMin: 61, levelMax: 70,  stage: 'summit',     emoji: '⛰️', color: '#166534', description: 'Rare air. Only the tallest trees stand here.' },
  { index: 7, name: 'Crown Canopy',    levelMin: 71, levelMax: 80,  stage: 'crown',      emoji: '👑', color: '#14532d', description: 'You crown the forest — the view is yours.' },
  { index: 8, name: 'Legend Tree',     levelMin: 81, levelMax: 90,  stage: 'legend',     emoji: '🌟', color: '#0f766e', description: 'Stories are told about trees like you.' },
  { index: 9, name: 'World Tree',      levelMin: 91, levelMax: 100, stage: 'world',      emoji: '🌍', color: '#065f46', description: 'Your roots hold up the sky. The forest is you.' },
];

export default function ForestJourney({ forest, level }: { forest: any; level: number }) {
  if (!forest) return null;

  const zoneIndex = Math.min(forest.zone_index ?? 0, FOREST_ZONES.length - 1);
  const zoneProgress = forest.zone_progress ?? 0;
  const currentZone = FOREST_ZONES[zoneIndex];

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
          <h3 className="text-xs font-mono uppercase tracking-widest text-gray-400">🌲 Forest Journey</h3>
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
          <Stat icon="☀️" label="Sunlight" value={forest.sunlight?.toLocaleString() ?? 0} unit="XP" color="#fbbf24" />
          <Stat icon="💧" label="Waterings" value={forest.waterings ?? 0} unit="streak" color="#60a5fa" />
          <Stat icon="🌰" label="Seeds" value={forest.seeds ?? 0} unit="badges" color="#a78bfa" />
          <Stat icon="⛈️" label="Storms Cleared" value={forest.storms_cleared ?? 0} unit="bosses" color="#f87171" />
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
              <div className="text-xs font-bold text-red-300">Storm: {forest.current_storm.name ?? 'Boss Battle'}</div>
              <div className="text-[10px] text-red-400 mt-0.5">Defeat this boss to clear the storm and grow stronger.</div>
            </div>
          </motion.div>
        )}

        {/* Zone map */}
        <div className="mt-5">
          <div className="text-[10px] font-mono text-gray-500 mb-2">All Zones</div>
          <div className="flex items-center gap-1.5 overflow-x-auto pb-2">
            {FOREST_ZONES.map((zone, i) => {
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

function Stat({ icon, label, value, unit, color }: { icon: string; label: string; value: number; unit: string; color: string }) {
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

