import { motion } from 'framer-motion';

// Escalating emblem tiers based on streak length
// Each tier has a unique shape, color, and animation

const STREAK_TIERS = [
  { min: 0, max: 2, name: 'Dormant', color: '#6b7280', glow: 'rgba(107,114,128,0.2)', shape: 'circle', icon: '○' },
  { min: 3, max: 6, name: 'Spark', color: '#f97316', glow: 'rgba(249,115,22,0.3)', shape: 'flame', icon: '◈' },
  { min: 7, max: 13, name: 'Blaze', color: '#ef4444', glow: 'rgba(239,68,68,0.4)', shape: 'star4', icon: '✦' },
  { min: 14, max: 29, name: 'Inferno', color: '#f59e0b', glow: 'rgba(245,158,11,0.5)', shape: 'star6', icon: '⬡' },
  { min: 30, max: 59, name: 'Phoenix', color: '#a855f7', glow: 'rgba(168,85,247,0.5)', shape: 'phoenix', icon: '❖' },
  { min: 60, max: Infinity, name: 'Eternal', color: '#4CC9F0', glow: 'rgba(76,201,240,0.6)', shape: 'eternal', icon: '⊕' },
];

function getTier(streak) {
  return STREAK_TIERS.find(t => streak >= t.min && streak <= t.max) || STREAK_TIERS[0];
}

export default function StreakEmblem({ streak = 0, size = 48, animated = true, className = '' }) {
  const tier = getTier(streak);
  const px = typeof size === 'number' ? size : 48;

  return (
    <motion.div
      className={`relative inline-flex items-center justify-center ${className}`}
      style={{ width: px, height: px }}
      animate={animated ? {
        filter: [
          `drop-shadow(0 0 3px ${tier.glow})`,
          `drop-shadow(0 0 10px ${tier.glow})`,
          `drop-shadow(0 0 3px ${tier.glow})`,
        ],
      } : undefined}
      transition={animated ? { duration: 2.5, repeat: Infinity, ease: 'easeInOut' } : undefined}
    >
      <svg viewBox="0 0 100 100" width={px} height={px}>
        <StreakShape shape={tier.shape} color={tier.color} streak={streak} />
      </svg>
    </motion.div>
  );
}

function StreakShape({ shape, color, streak }) {
  switch (shape) {
    case 'flame':
      return (
        <g transform="translate(50,50)">
          <path d="M 0,-30 Q 15,-15 10,5 Q 20,-5 15,20 Q 10,35 0,40 Q -10,35 -15,20 Q -20,-5 -10,5 Q -15,-15 0,-30"
            fill="none" stroke={color} strokeWidth="2" opacity="0.8" />
          <path d="M 0,-18 Q 8,-8 5,5 Q 10,0 8,15 Q 5,25 0,28 Q -5,25 -8,15 Q -10,0 -5,5 Q -8,-8 0,-18"
            fill={color} opacity="0.15" />
          <circle cx="0" cy="0" r="3" fill={color} opacity="0.6" />
        </g>
      );

    case 'star4':
      return (
        <g transform="translate(50,50)">
          <polygon points="0,-35 8,-8 35,0 8,8 0,35 -8,8 -35,0 -8,-8"
            fill="none" stroke={color} strokeWidth="1.5" opacity="0.7" />
          <polygon points="0,-20 5,-5 20,0 5,5 0,20 -5,5 -20,0 -5,-5"
            fill={color} opacity="0.1" />
          <circle cx="0" cy="0" r="4" fill={color} opacity="0.5" />
        </g>
      );

    case 'star6':
      return (
        <g transform="translate(50,50)">
          {[0, 60, 120].map((angle, i) => (
            <g key={i} transform={`rotate(${angle})`}>
              <polygon points="0,-32 8,0 -8,0" fill="none" stroke={color} strokeWidth="1" opacity="0.6" />
            </g>
          ))}
          <circle cx="0" cy="0" r="25" fill="none" stroke={color} strokeWidth="0.5" opacity="0.3" />
          <circle cx="0" cy="0" r="5" fill={color} opacity="0.3" />
          <circle cx="0" cy="0" r="2.5" fill={color} opacity="0.6" />
          <text x="0" y="3" textAnchor="middle" fill={color} fontSize="7"
            fontFamily="Orbitron" fontWeight="bold" opacity="0.9">
            {streak}
          </text>
        </g>
      );

    case 'phoenix':
      return (
        <g transform="translate(50,50)">
          {[0, 72, 144, 216, 288].map((angle, i) => (
            <g key={i} transform={`rotate(${angle})`}>
              <path d="M 0,-12 Q 8,-28 0,-38 Q -8,-28 0,-12" fill="none"
                stroke={color} strokeWidth="1" opacity="0.6" />
            </g>
          ))}
          <circle cx="0" cy="0" r="12" fill="none" stroke={color} strokeWidth="1.5" opacity="0.5" />
          <circle cx="0" cy="0" r="6" fill={color} opacity="0.15" />
          <circle cx="0" cy="0" r="3" fill={color} opacity="0.5" />
        </g>
      );

    case 'eternal':
      return (
        <g transform="translate(50,50)">
          <circle cx="0" cy="0" r="38" fill="none" stroke={color} strokeWidth="0.5" opacity="0.2" />
          <circle cx="0" cy="0" r="30" fill="none" stroke={color} strokeWidth="1" opacity="0.4" />
          {[0, 60, 120, 180, 240, 300].map((angle, i) => {
            const rad = (angle * Math.PI) / 180;
            return (
              <line key={i} x1={Math.cos(rad) * 12} y1={Math.sin(rad) * 12}
                x2={Math.cos(rad) * 30} y2={Math.sin(rad) * 30}
                stroke={color} strokeWidth="0.8" opacity="0.4" />
            );
          })}
          <circle cx="0" cy="0" r="12" fill="none" stroke={color} strokeWidth="1.5" opacity="0.6" />
          <circle cx="0" cy="0" r="5" fill={color} opacity="0.2" />
          <text x="0" y="3" textAnchor="middle" fill={color} fontSize="8"
            fontFamily="Orbitron" fontWeight="bold" opacity="0.9">
            {streak}
          </text>
        </g>
      );

    default: // circle (dormant)
      return (
        <g transform="translate(50,50)">
          <circle cx="0" cy="0" r="30" fill="none" stroke={color} strokeWidth="1" opacity="0.3" />
          <circle cx="0" cy="0" r="4" fill={color} opacity="0.3" />
        </g>
      );
  }
}

export { STREAK_TIERS, getTier };
