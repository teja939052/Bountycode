import { motion } from 'framer-motion';

// Animated complexity badges with concentric ring visualization
// Shows time and space complexity after problem submission

const COMPLEXITY_COLORS = {
  'O(1)': { color: '#22c55e', label: 'Constant', tier: 1 },
  'O(log n)': { color: '#06b6d4', label: 'Logarithmic', tier: 2 },
  'O(n)': { color: '#3b82f6', label: 'Linear', tier: 3 },
  'O(n log n)': { color: '#8b5cf6', label: 'Linearithmic', tier: 4 },
  'O(n^2)': { color: '#f59e0b', label: 'Quadratic', tier: 5 },
  'O(n^3)': { color: '#f97316', label: 'Cubic', tier: 6 },
  'O(2^n)': { color: '#ef4444', label: 'Exponential', tier: 7 },
  'O(n!)': { color: '#dc2626', label: 'Factorial', tier: 8 },
};

function getComplexityInfo(c) {
  if (!c) return { color: '#6b7280', label: 'Unknown', tier: 0 };
  const normalized = c.replace(/\s/g, '');
  for (const [key, val] of Object.entries(COMPLEXITY_COLORS)) {
    if (key.replace(/\s/g, '') === normalized) return val;
  }
  return { color: '#6b7280', label: c, tier: 0 };
}

export default function ComplexityDisplay({ timeComplexity, spaceComplexity, algorithm, animated = true }) {
  const time = getComplexityInfo(timeComplexity);
  const space = getComplexityInfo(spaceComplexity);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="bg-gray-900/60 border border-gray-700/40 rounded-xl p-4"
    >
      <div className="text-center mb-3">
        <span className="text-[10px] font-mono uppercase tracking-widest text-gray-500">
          Complexity Analysis
        </span>
      </div>

      <div className="flex items-center justify-center gap-6">
        <ComplexityBadge label="Time" complexity={timeComplexity} info={time} animated={animated} delay={0.3} />
        <div className="w-px h-12 bg-gray-700/30" />
        <ComplexityBadge label="Space" complexity={spaceComplexity} info={space} animated={animated} delay={0.5} />
      </div>

      {algorithm && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="text-center mt-3"
        >
          <span className="text-[10px] font-mono text-gray-500">Algorithm: </span>
          <span className="text-xs font-mono font-bold text-cyber-blue">{algorithm}</span>
        </motion.div>
      )}
    </motion.div>
  );
}

function ComplexityBadge({ label, complexity, info, animated, delay }) {
  const ringCount = Math.min(4, Math.max(1, info.tier));

  return (
    <div className="text-center">
      <div className="relative w-16 h-16 mx-auto mb-2">
        <svg viewBox="0 0 80 80" width="64" height="64">
          {/* Concentric rings — more rings = higher complexity */}
          {Array.from({ length: ringCount }).map((_, i) => (
            <motion.circle
              key={i}
              cx="40" cy="40"
              r={12 + i * 7}
              fill="none"
              stroke={info.color}
              strokeWidth={i === ringCount - 1 ? 2 : 0.8}
              opacity={0.2 + (i / ringCount) * 0.5}
              initial={animated ? { pathLength: 0, opacity: 0 } : undefined}
              animate={animated ? { pathLength: 1, opacity: 0.2 + (i / ringCount) * 0.5 } : undefined}
              transition={{ duration: 0.8, delay: delay + i * 0.15, ease: 'easeOut' }}
            />
          ))}

          {/* Center dot */}
          <motion.circle
            cx="40" cy="40" r="4"
            fill={info.color}
            initial={animated ? { scale: 0 } : undefined}
            animate={animated ? { scale: 1 } : undefined}
            transition={{ delay: delay + 0.3, type: 'spring', stiffness: 300 }}
          />
        </svg>
      </div>

      <div className="font-mono text-xs font-bold" style={{ color: info.color }}>
        {complexity || '?'}
      </div>
      <div className="text-[9px] font-mono text-gray-500 mt-0.5">{label}</div>
      <div className="text-[8px] font-mono mt-0.5" style={{ color: `${info.color}99` }}>
        {info.label}
      </div>
    </div>
  );
}

export { COMPLEXITY_COLORS, getComplexityInfo };
