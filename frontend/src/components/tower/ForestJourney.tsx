import { memo } from 'react';
import { motion } from 'framer-motion';
import { Sun, Droplets, Sprout, CloudLightning } from 'lucide-react';

interface ForestZone {
  index: number;
  name: string;
  level_min: number;
  level_max: number;
  stage: string;
  emoji: string;
  color: string;
  description: string;
}

interface Storm {
  name: string;
  emoji: string;
  element: string;
}

export interface ForestState {
  current_zone: ForestZone;
  zone_index: number;
  zones_total: number;
  tree_stage: string;
  growth_rings: number;
  sunlight: number;
  waterings: number;
  seeds: number;
  storms_cleared: number;
  current_storm: Storm | null;
  zone_progress: number;
}

// Fallback in case the API shape is missing (defensive only).
const FALLBACK_ZONES: ForestZone[] = Array.from({ length: 10 }, (_, i) => ({
  index: i,
  name: `Zone ${i + 1}`,
  level_min: i * 10 + 1,
  level_max: (i + 1) * 10,
  stage: 'forest',
  emoji: '🌳',
  color: '#16a34a',
  description: '',
}));

function MetricChip({ icon, label, value, tint }: { icon: React.ReactNode; label: string; value: string | number; tint: string }) {
  return (
    <div className="bg-gray-900/60 border border-gray-700/25 rounded-xl p-3 text-center">
      <div className={`flex items-center justify-center gap-1 mb-1 ${tint}`}>{icon}</div>
      <div className="text-sm font-display font-bold text-white">{value}</div>
      <div className="text-[9px] font-mono text-gray-500 uppercase tracking-wider">{label}</div>
    </div>
  );
}

const ForestJourney = memo(function ForestJourney({
  forest,
  level = 1,
}: {
  forest?: ForestState | null;
  level?: number;
}) {
  if (!forest) return null;

  const zone: ForestZone = forest.current_zone || FALLBACK_ZONES[0];
  const track: ForestZone[] = Array.from(
    { length: forest.zones_total || 10 },
    (_, i) => FALLBACK_ZONES[i]
  );
  const zoneProgress = Math.round((forest.zone_progress || 0) * 100);
  const storm = forest.current_storm;

  return (
    <div className="space-y-4">
      {/* Current Zone hero */}
      <motion.div
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden rounded-2xl p-5 sm:p-6 border"
        style={{ backgroundColor: `${zone.color}14`, borderColor: `${zone.color}55` }}
      >
        <div className="flex items-center gap-4">
          <motion.div
            className="text-5xl sm:text-6xl shrink-0"
            animate={{ y: [0, -6, 0] }}
            transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
          >
            {zone.emoji}
          </motion.div>
          <div className="flex-1 min-w-0">
            <p className="text-[9px] font-mono uppercase tracking-widest mb-1" style={{ color: zone.color }}>
              Current Forest Zone
            </p>
            <h2 className="text-lg sm:text-xl font-display font-black text-white leading-tight">
              {zone.name}
            </h2>
            <p className="text-[10px] font-mono text-gray-400 mt-0.5">
              Levels {zone.level_min}–{zone.level_max} · Level {level}
            </p>
            {zone.description && (
              <p className="text-xs text-gray-400 mt-2 hidden sm:block">{zone.description}</p>
            )}
          </div>
        </div>

        {/* Zone progress bar */}
        <div className="mt-4">
          <div className="flex justify-between text-[10px] font-mono text-gray-500 mb-1">
            <span>{zoneProgress}% through this zone</span>
            <span>{zone.level_max - level} levels to next zone</span>
          </div>
          <div className="h-2.5 rounded-full bg-gray-800/60 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${zoneProgress}%` }}
              transition={{ duration: 1, ease: 'easeOut' }}
              className="h-full rounded-full"
              style={{
                background: `linear-gradient(90deg, ${zone.color}66, ${zone.color})`,
              }}
            />
          </div>
        </div>
      </motion.div>

      {/* Zone journey track */}
      <div className="bg-gray-900/60 border border-gray-700/30 rounded-2xl p-4">
        <p className="text-[9px] font-mono uppercase tracking-widest text-gray-500 mb-3">
          The Growing Forest
        </p>
        <div className="flex items-center justify-between gap-1">
          {track.map((z, i) => {
            const isCurrent = i === forest.zone_index;
            const isPast = i < forest.zone_index;
            return (
              <div key={z.index} className="flex-1 flex flex-col items-center gap-1 min-w-0">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm border transition-all ${
                    isCurrent
                      ? 'scale-110'
                      : isPast
                        ? 'opacity-70'
                        : 'opacity-35 grayscale'
                  }`}
                  style={{
                    backgroundColor: isPast || isCurrent ? `${z.color}22` : 'transparent',
                    borderColor: isCurrent ? z.color : 'rgba(255,255,255,0.15)',
                  }}
                >
                  {z.emoji}
                </div>
                <span className="hidden sm:block text-[8px] font-mono text-gray-600 truncate w-full text-center">
                  {z.name}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Seasonal Storm */}
      {storm ? (
        <motion.div
          initial={{ scale: 0.92, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="rounded-2xl p-5 border border-purple-500/40 bg-gradient-to-r from-purple-500/10 to-gray-900/60 text-center"
        >
          <p className="text-[9px] font-mono uppercase tracking-widest text-purple-400 mb-1">
            ⛈ Seasonal Storm Brewing
          </p>
          <div className="text-5xl mb-2">{storm.emoji}</div>
          <h3 className="text-lg font-display font-black text-white">{storm.name}</h3>
          <p className="text-[10px] font-mono text-gray-400 mt-1">
            Clear {zone.name} to face the storm · your roots are tested at level{' '}
            {(forest.zone_index + 1) * 10}
          </p>
        </motion.div>
      ) : (
        <div className="rounded-2xl p-5 border border-gray-700/25 bg-gray-900/40 text-center">
          <p className="text-[10px] font-mono text-gray-500">
            🌈 The skies are clear — no seasonal storm overhead.
          </p>
        </div>
      )}

      {/* Forest metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <MetricChip icon={<Sun size={14} />} label="Sunlight" value={forest.sunlight ?? 0} tint="text-yellow-400" />
        <MetricChip icon={<Droplets size={14} />} label="Waterings" value={forest.waterings ?? 0} tint="text-cyan-400" />
        <MetricChip icon={<Sprout size={14} />} label="Seeds" value={forest.seeds ?? 0} tint="text-green-400" />
        <MetricChip icon={<CloudLightning size={14} />} label="Storms Cleared" value={forest.storms_cleared ?? 0} tint="text-purple-400" />
      </div>
    </div>
  );
});

ForestJourney.displayName = "ForestJourney";

export default ForestJourney;
