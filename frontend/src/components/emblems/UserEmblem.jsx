import { useMemo } from 'react';
import { motion } from 'framer-motion';

// Generates a unique emblem from a user's skill profile
// The emblem is a combination of shape layers based on top skills

const SKILL_TO_SHAPE = {
  dsa: 'circles',
  system_design: 'triangles',
  behavioral: 'petals',
  aptitude: 'dots',
  resume: 'lines',
};

const LAYER_COLORS = [
  ['#4CC9F0', 'rgba(76,201,240,0.3)'],
  ['#7209B7', 'rgba(114,9,183,0.3)'],
  ['#4BB543', 'rgba(75,181,67,0.3)'],
  ['#F59E0B', 'rgba(245,158,11,0.3)'],
  ['#ec4899', 'rgba(236,72,153,0.3)'],
];

export default function UserEmblem({
  skills = {},
  level = 1,
  xp = 0,
  size = 96,
  className = '',
  animated = true,
}) {
  const layers = useMemo(() => {
    // Sort skills by score, take top 3
    const sorted = Object.entries(skills)
      .sort(([, a], [, b]) => (b.score || 0) - (a.score || 0))
      .slice(0, 3);

    if (sorted.length === 0) {
      sorted.push(['aptitude', { score: 10, solved: 0 }]);
    }

    return sorted.map(([skill, data], i) => ({
      shape: SKILL_TO_SHAPE[skill] || 'circles',
      score: data.score || 0,
      color: LAYER_COLORS[i][0],
      glow: LAYER_COLORS[i][1],
      opacity: 0.3 + (data.score / 100) * 0.5,
      size: 0.5 + (data.score / 100) * 0.5,
    }));
  }, [skills]);

  // Hash level + xp to create unique rotation offset
  const hash = (level * 31 + xp * 17) % 360;

  return (
    <div className={`relative ${className}`} style={{ width: size, height: size }}>
      <motion.div
        className="w-full h-full"
        animate={animated ? {
          filter: [
            `drop-shadow(0 0 4px ${LAYER_COLORS[0][1]})`,
            `drop-shadow(0 0 12px ${LAYER_COLORS[0][1]})`,
            `drop-shadow(0 0 4px ${LAYER_COLORS[0][1]})`,
          ],
        } : undefined}
        transition={animated ? { duration: 4, repeat: Infinity, ease: 'easeInOut' } : undefined}
      >
        <svg viewBox="0 0 100 100" width={size} height={size}>
          {/* Background ring */}
          <circle cx="50" cy="50" r="46" fill="none" stroke="#1a1d26" strokeWidth="1" opacity={0.5} />

          {/* Skill layers */}
          {layers.map((layer, i) => (
            <g key={i} transform={`translate(50,50) rotate(${hash + i * 30})`}>
              <SkillShape {...layer} index={i} />
            </g>
          ))}

          {/* Center: Level badge */}
          <circle cx="50" cy="50" r="12" fill="#111318" stroke={LAYER_COLORS[0][0]} strokeWidth="1.5" opacity={0.9} />
          <text x="50" y="54" textAnchor="middle" fill={LAYER_COLORS[0][0]}
            fontSize="10" fontFamily="Orbitron" fontWeight="bold">
            {level}
          </text>

          {/* Outer glow ring */}
          <circle cx="50" cy="50" r="46" fill="none" stroke={LAYER_COLORS[0][0]}
            strokeWidth="0.5" opacity={0.3} />
          <circle cx="50" cy="50" r="48" fill="none" stroke={LAYER_COLORS[0][0]}
            strokeWidth="0.3" opacity={0.15} strokeDasharray="3 5" />
        </svg>
      </motion.div>
    </div>
  );
}

function SkillShape({ shape, score, color, glow, opacity, size: sz, index }) {
  const r = 36 * sz;

  switch (shape) {
    case 'circles':
      return (
        <>
          <circle cx="0" cy="0" r={r} fill="none" stroke={color}
            strokeWidth={1.2} opacity={opacity} />
          <circle cx="0" cy="0" r={r * 0.7} fill="none" stroke={color}
            strokeWidth={0.6} opacity={opacity * 0.6} />
          {/* Nodes on the ring */}
          {[0, 72, 144, 216, 288].map((angle, i) => {
            const rad = (angle * Math.PI) / 180;
            return (
              <circle key={i} cx={Math.cos(rad) * r} cy={Math.sin(rad) * r}
                r={1.5} fill={color} opacity={opacity * 0.8} />
            );
          })}
        </>
      );

    case 'triangles':
      const h = r * 0.866;
      return (
        <>
          <polygon points={`0,${-r} ${-r},${h} ${r},${h}`}
            fill="none" stroke={color} strokeWidth={1.2} opacity={opacity} />
          {score > 50 && (
            <polygon points={`0,${-r * 0.6} ${-r * 0.6},${h * 0.6} ${r * 0.6},${h * 0.6}`}
              fill="none" stroke={color} strokeWidth={0.6} opacity={opacity * 0.5} />
          )}
        </>
      );

    case 'petals':
      const count = Math.max(4, Math.floor(score / 15) + 2);
      return (
        <>
          {Array.from({ length: count }).map((_, i) => {
            const angle = (360 / count) * i;
            return (
              <g key={i} transform={`rotate(${angle})`}>
                <ellipse cx="0" cy={-r * 0.6} rx={r * 0.15} ry={r * 0.35}
                  fill="none" stroke={color} strokeWidth={1} opacity={opacity} />
              </g>
            );
          })}
        </>
      );

    case 'dots':
      return (
        <>
          {Array.from({ length: Math.min(12, Math.floor(score / 8) + 3) }).map((_, i) => {
            const angle = (360 / Math.min(12, Math.floor(score / 8) + 3)) * i;
            const rad = (angle * Math.PI) / 180;
            const ring = i % 2 === 0 ? r : r * 0.6;
            return (
              <circle key={i} cx={Math.cos(rad) * ring} cy={Math.sin(rad) * ring}
                r={i % 3 === 0 ? 2.5 : 1.5} fill={color} opacity={opacity} />
            );
          })}
        </>
      );

    case 'lines':
      return (
        <>
          {[0, 30, 60, 90, 120, 150].map((angle, i) => {
            const rad = (angle * Math.PI) / 180;
            return (
              <line key={i} x1={Math.cos(rad) * r * 0.3} y1={Math.sin(rad) * r * 0.3}
                x2={Math.cos(rad) * r} y2={Math.sin(rad) * r}
                stroke={color} strokeWidth={i % 2 === 0 ? 1.2 : 0.6} opacity={opacity} />
            );
          })}
        </>
      );

    default:
      return <circle cx="0" cy="0" r={r} fill="none" stroke={color} strokeWidth={1} opacity={opacity} />;
  }
}
