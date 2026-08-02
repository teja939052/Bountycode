import { motion } from 'framer-motion';
import { getOutfitForLevel } from './towerData';

// Wizard avatar that evolves with level — shows outfit progression
export default function WizardProgression({ level = 1, size = 96, className = '' }) {
  const outfit = getOutfitForLevel(level);
  const px = typeof size === 'number' ? size : 96;

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`} style={{ width: px, height: px }}>
      <svg viewBox="0 0 100 100" width={px} height={px}>
        {/* Background aura based on outfit effect */}
        {outfit.effect === 'glow' && (
          <circle cx="50" cy="50" r="45" fill={outfit.color} opacity="0.05" />
        )}
        {outfit.effect === 'sparkle' && (
          <>
            <circle cx="50" cy="50" r="45" fill={outfit.color} opacity="0.05" />
            {[0, 60, 120, 180, 240, 300].map((a, i) => {
              const r = (a * Math.PI) / 180;
              return <circle key={i} cx={50 + Math.cos(r) * 40} cy={50 + Math.sin(r) * 40} r="1.5" fill={outfit.color} opacity="0.3" />;
            })}
          </>
        )}
        {outfit.effect === 'fire_aura' && (
          <circle cx="50" cy="50" r="45" fill="url(#fireGrad)" opacity="0.15" />
        )}
        {outfit.effect === 'lightning' && (
          <>
            <circle cx="50" cy="50" r="45" fill={outfit.color} opacity="0.06" />
            <line x1="30" y1="20" x2="35" y2="35" stroke={outfit.color} strokeWidth="0.5" opacity="0.3" />
            <line x1="70" y1="25" x2="65" y2="40" stroke={outfit.color} strokeWidth="0.5" opacity="0.3" />
          </>
        )}
        {outfit.effect === 'rainbow_wings' && (
          <>
            <defs>
              <linearGradient id="rainbowGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#ef4444" />
                <stop offset="25%" stopColor="#f59e0b" />
                <stop offset="50%" stopColor="#22c55e" />
                <stop offset="75%" stopColor="#3b82f6" />
                <stop offset="100%" stopColor="#a855f7" />
              </linearGradient>
            </defs>
            <circle cx="50" cy="50" r="46" fill="none" stroke="url(#rainbowGrad)" strokeWidth="1.5" opacity="0.4" />
            <polygon points="25,50 15,35 20,50 15,65" fill="url(#rainbowGrad)" opacity="0.2" />
            <polygon points="75,50 85,35 80,50 85,65" fill="url(#rainbowGrad)" opacity="0.2" />
          </>
        )}

        {/* Fire gradient for archmage */}
        {outfit.effect === 'fire_aura' && (
          <defs>
            <radialGradient id="fireGrad">
              <stop offset="0%" stopColor="#f59e0b" />
              <stop offset="100%" stopColor="#ef4444" />
            </radialGradient>
          </defs>
        )}

        {/* Body (robe) */}
        <path d="M 35,45 Q 35,80 50,85 Q 65,80 65,45" fill={outfit.color} opacity="0.3" />
        <path d="M 35,45 Q 35,80 50,85 Q 65,80 65,45" fill="none" stroke={outfit.color} strokeWidth="1" opacity="0.5" />

        {/* Head */}
        <circle cx="50" cy="35" r="12" fill="#1a1d26" stroke={outfit.color} strokeWidth="1" opacity="0.8" />

        {/* Hat (triangle) */}
        <polygon points="50,12 38,32 62,32" fill={outfit.color} opacity="0.2" />
        <polygon points="50,12 38,32 62,32" fill="none" stroke={outfit.color} strokeWidth="0.8" opacity="0.5" />

        {/* Eyes */}
        <circle cx="45" cy="34" r="1.5" fill={outfit.color} opacity="0.8" />
        <circle cx="55" cy="34" r="1.5" fill={outfit.color} opacity="0.8" />

        {/* Level badge */}
        <circle cx="50" cy="60" r="8" fill="#111318" stroke={outfit.color} strokeWidth="1" opacity="0.9" />
        <text x="50" y="63" textAnchor="middle" fill={outfit.color}
          fontSize="8" fontFamily="Orbitron" fontWeight="bold">
          {level}
        </text>
      </svg>
    </div>
  );
}
