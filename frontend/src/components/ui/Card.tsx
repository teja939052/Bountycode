import { useRef, useCallback, useState, type ReactNode, type MouseEvent } from "react";
import { motion } from "framer-motion";

type Rarity = "common" | "uncommon" | "rare" | "epic" | "legendary" | "mythic";

const rarityConfig: Record<Rarity, any> = {
  common: {
    border: 'border-gray-600/50',
    glow: '',
    bg: 'bg-gray-900/40',
    label: 'Common',
    color: '#9CA3AF',
    borderColor: 'rgba(156,163,175,0.3)',
    glowColor: 'rgba(156,163,175,0.08)',
    particles: 0,
    cssClass: '',
    stars: '★',
  },
  uncommon: {
    border: 'border-green-500/40',
    glow: '',
    bg: 'bg-green-950/30',
    label: 'Uncommon',
    color: '#22C55E',
    borderColor: 'rgba(34,197,94,0.4)',
    glowColor: 'rgba(34,197,94,0.12)',
    particles: 2,
    cssClass: '',
    stars: '★★',
  },
  rare: {
    border: 'border-blue-500/50',
    glow: '',
    bg: 'bg-blue-950/30',
    label: 'Rare',
    color: '#3B82F6',
    borderColor: 'rgba(59,130,246,0.5)',
    glowColor: 'rgba(59,130,246,0.2)',
    particles: 4,
    cssClass: 'card-rare',
    stars: '★★★',
  },
  epic: {
    border: 'border-purple-500/50',
    glow: 'card-glow-pulse',
    bg: 'bg-purple-950/30',
    label: 'Epic',
    color: '#A855F7',
    borderColor: 'rgba(168,85,247,0.5)',
    glowColor: 'rgba(168,85,247,0.25)',
    particles: 6,
    cssClass: 'card-epic',
    stars: '★★★★',
  },
  legendary: {
    border: 'border-yellow-500/60',
    glow: 'card-glow-pulse',
    bg: 'bg-yellow-950/30',
    label: 'Legendary',
    color: '#EAB308',
    borderColor: 'rgba(234,179,8,0.6)',
    glowColor: 'rgba(234,179,8,0.3)',
    particles: 8,
    cssClass: 'card-legendary card-shine',
    stars: '★★★★★',
  },
  mythic: {
    border: 'border-rainbow',
    glow: 'card-glow-pulse card-sparkle',
    bg: 'card-mythic',
    label: 'Mythic',
    color: '#EC4899',
    borderColor: 'rgba(236,72,153,0.6)',
    glowColor: 'rgba(236,72,153,0.35)',
    particles: 12,
    cssClass: 'card-mythic card-shine holo-shimmer',
    stars: '★★★★★★',
  },
};

const rarityEmoji = {
  common: '⬜',
  uncommon: '🟢',
  rare: '🔵',
  epic: '🟣',
  legendary: '🟡',
  mythic: '🩷',
};

const particleColors = {
  common: ['#9CA3AF'],
  uncommon: ['#22C55E', '#4ADE80'],
  rare: ['#3B82F6', '#60A5FA'],
  epic: ['#A855F7', '#C084FC', '#818CF8'],
  legendary: ['#EAB308', '#FACC15', '#F59E0B', '#FBBF24'],
  mythic: ['#EC4899', '#F472B6', '#A855F7', '#3B82F6', '#F59E0B', '#22C55E'],
};

export function getRarityEmoji(rarity: string) {
  return rarityEmoji[rarity as keyof typeof rarityEmoji] || "⬜";
}

export function getRarityStars(rarity: string) {
  return rarityConfig[rarity]?.stars || "★";
}

export function getRarityColor(rarity: string) {
  return rarityConfig[rarity]?.color || "#9CA3AF";
}

function spawnParticles(container: HTMLElement, rarity: string, count: number) {
  const colors = particleColors[rarity] || particleColors.common;
  for (let i = 0; i < count; i++) {
    const p = document.createElement('span');
    p.className = 'particle';
    p.style.background = colors[i % colors.length];
    p.style.left = `${30 + Math.random() * 40}%`;
    p.style.top = `${30 + Math.random() * 40}%`;
    p.style.setProperty('--tx', `${(Math.random() - 0.5) * 80}px`);
    p.style.setProperty('--ty', `${(Math.random() - 0.5) * 80}px`);
    p.style.width = `${3 + Math.random() * 4}px`;
    p.style.height = p.style.width;
    container.appendChild(p);
    setTimeout(() => p.remove(), 900);
  }
}

interface CardProps {
  children?: ReactNode;
  rarity?: string;
  animate?: boolean;
  className?: string;
  onClick?: (e: MouseEvent) => void;
  disabled?: boolean;
  hoverEffect?: boolean;
  tilt?: boolean;
  particles?: boolean;
  compact?: boolean;
}

export function Card({
  children,
  rarity = "common",
  animate = true,
  className = "",
  onClick,
  disabled = false,
  hoverEffect = true,
  tilt = false,
  particles = false,
  compact = false,
}: CardProps) {
  const ref = useRef(null);
  const innerRef = useRef(null);
  const config = rarityConfig[rarity] || rarityConfig.common;
  const [isHovered, setIsHovered] = useState(false);
  const [tiltRotate, setTiltRotate] = useState({ rotateX: 0, rotateY: 0 });
  const [scale, setScale] = useState(1);

  const handleMouseMove = useCallback(
    (e) => {
      if (!tilt || !hoverEffect || disabled || !ref.current) return;
      const rect = ref.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      setTiltRotate({
        rotateX: ((y - centerY) / centerY) * -8,
        rotateY: ((x - centerX) / centerX) * 8,
      });
    },
    [tilt, hoverEffect, disabled]
  );

  const handleMouseLeave = useCallback(() => {
    setIsHovered(false);
    setTiltRotate({ rotateX: 0, rotateY: 0 });
    setScale(1);
    if (particles && ref.current && config.particles > 0) {
      spawnParticles(ref.current, rarity, config.particles);
    }
  }, [particles, rarity, config.particles]);

  const handleMouseEnter = useCallback(() => {
    setIsHovered(true);
    if (hoverEffect) {
      setScale(1.02);
    }
  }, [hoverEffect]);

  const handleMouseUp = useCallback(() => {
    if (hoverEffect) {
      setScale(isHovered ? 1.02 : 1);
    }
  }, [hoverEffect, isHovered]);

  return (
    <motion.div
      ref={ref}
      initial={animate ? { opacity: 0, y: 16, scale: 0.97 } : undefined}
      animate={animate ? { opacity: 1, y: 0, scale: 1 } : undefined}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      onMouseMove={handleMouseMove}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onMouseUp={handleMouseUp}
      onClick={disabled ? undefined : onClick}
      className={`
        relative overflow-hidden rounded-xl border
        ${config.border} ${config.bg} ${config.glow} ${config.cssClass}
        ${compact ? 'p-3' : 'p-5'}
        transition-colors duration-300
        ${disabled ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'}
        ${className}
      `}
      style={{
        transform: `scale(${scale})`,
        transformOrigin: 'center center',
        transition: 'transform 0.2s ease, box-shadow 0.3s ease, border-color 0.3s ease',
        boxShadow: isHovered
          ? `0 8px 30px ${config.glowColor}, 0 0 1px ${config.borderColor}`
          : `0 2px 8px rgba(0,0,0,0.2)`,
        borderColor: isHovered ? config.borderColor : undefined,
      }}
    >
      <div
        ref={innerRef}
        className="relative z-10"
        style={{
          transformStyle: 'preserve-3d',
          transform: `rotateX(${tiltRotate.rotateX}deg) rotateY(${tiltRotate.rotateY}deg)`,
          transition: 'transform 0.15s ease-out',
          willChange: 'transform',
        }}
      >
        {children}
      </div>

      {/* Rarity badge */}
      <div
        className="absolute top-2 right-2 text-[10px] font-mono font-bold uppercase tracking-widest px-2 py-0.5 rounded-full z-20"
        style={{ backgroundColor: `${config.color}20`, color: config.color, border: `1px solid ${config.color}30` }}
      >
        {config.label}
      </div>

      {/* Holo overlay for epic+ */}
      {(rarity === 'epic' || rarity === 'legendary' || rarity === 'mythic') && (
        <div className="absolute inset-0 pointer-events-none z-0 opacity-30">
          <div
            className="absolute inset-0"
            style={{
              background: `radial-gradient(circle at ${isHovered ? '40% 30%' : '50% 50%'}, ${config.glowColor}, transparent 70%)`,
              transition: 'background 0.3s ease',
            }}
          />
        </div>
      )}
    </motion.div>
  );
}

export function CardGrid({ children, className = '' }) {
  const ref = useRef(null);

  return (
    <div
      ref={ref}
      className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 ${className}`}
    >
      {children}
    </div>
  );
}

export function CardSkeleton({ count = 6 }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="rounded-xl border border-gray-700/30 p-5 animate-pulse bg-gray-900/30">
          <div className="h-4 bg-gray-700/50 rounded w-1/3 mb-3" />
          <div className="h-3 bg-gray-700/40 rounded w-2/3 mb-2" />
          <div className="h-3 bg-gray-700/30 rounded w-1/2" />
        </div>
      ))}
    </div>
  );
}

export function StatCard({ icon, label, value, trend, color = 'cyber-blue', className = '' }) {
  return (
    <Card rarity="common" compact hoverEffect className={className}>
      <div className="flex items-center gap-3">
        <div className={`text-xl bg-${color}/15 p-2.5 rounded-lg`}>
          {icon}
        </div>
        <div className="min-w-0">
          <p className="text-[11px] text-gray-500 font-mono uppercase tracking-wider">{label}</p>
          <h3 className="text-lg font-bold font-display">{value}</h3>
          {trend !== undefined && (
            <span className={`text-[10px] font-mono ${trend >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {trend >= 0 ? '↑' : '↓'} {Math.abs(trend)}%
            </span>
          )}
        </div>
      </div>
    </Card>
  );
}

export function ProblemCard({ problem, solved = false, onClick }) {
  const difficultyMap = {
    easy: { color: '#22C55E', bg: 'bg-green-900/30', label: 'Easy' },
    medium: { color: '#EAB308', bg: 'bg-yellow-900/30', label: 'Medium' },
    hard: { color: '#EF4444', bg: 'bg-red-900/30', label: 'Hard' },
    expert: { color: '#A855F7', bg: 'bg-purple-900/30', label: 'Expert' },
  };
  const diff = difficultyMap[problem.difficulty] || difficultyMap.easy;

  return (
    <Card
      rarity={solved ? 'uncommon' : 'common'}
      onClick={onClick}
      tilt
      particles
      compact
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-sm truncate leading-tight">
            {problem.question_title || problem.title}
          </h3>
          <div className="flex items-center gap-2 mt-1.5">
            <span
              className="text-[10px] font-mono font-bold uppercase tracking-wider px-1.5 py-0.5 rounded"
              style={{ backgroundColor: `${diff.color}18`, color: diff.color }}
            >
              {diff.label}
            </span>
            {solved && (
              <span className="text-green-400 text-[10px] font-mono">✓ Solved</span>
            )}
          </div>
        </div>
        <div className="text-lg leading-none mt-0.5">
          {solved ? '✅' : getRarityEmoji(problem.rarity || 'common')}
        </div>
      </div>

      <div className="mt-2.5 flex items-center gap-3 text-[10px] text-gray-500 font-mono">
        <span>{problem.topic}</span>
        {problem.companies?.length > 0 && (
          <span className="text-gray-600">· {problem.companies.length} co.</span>
        )}
      </div>
    </Card>
  );
}

export function WizardCard({ item, selected, onSelect }) {
  return (
    <motion.div
      whileHover={{ scale: 1.04 }}
      whileTap={{ scale: 0.96 }}
      onClick={() => onSelect(item.id)}
      className={`
        glass p-4 rounded-xl cursor-pointer transition-all duration-200 text-center
        ${selected
          ? 'border-2 border-cyber-blue shadow-[0_0_20px_rgba(76,201,240,0.2)]'
          : 'border border-space-border hover:border-cyber-blue/30'
        }
      `}
    >
      <div className="text-3xl mb-2">{item.emoji || item.icon}</div>
      <p className="font-medium text-sm">{item.name}</p>
      {item.locked && (
        <span className="text-[10px] text-gray-500 font-mono">🔒 Lv.{item.unlockLevel}</span>
      )}
      {selected && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="mt-1.5 text-cyber-blue text-xs font-mono"
        >
          ✓ Selected
        </motion.div>
      )}
    </motion.div>
  );
}

export function BattleCard({ opponent, onChallenge, status = 'ready' }) {
  const statusMap = {
    ready: { bg: 'bg-cyber-blue hover:bg-cyber-blue/80', label: '⚔️ Battle' },
    waiting: { bg: 'bg-cyber-amber', label: '⏳ Waiting...' },
    in_progress: { bg: 'bg-cyber-green', label: '⚔️ Fighting' },
  };
  const s = statusMap[status] || statusMap.ready;

  return (
    <Card rarity="rare" compact hoverEffect onClick={status === 'ready' ? onChallenge : undefined}>
      <div className="flex items-center gap-4">
        <div className="w-11 h-11 rounded-full bg-gradient-to-br from-cyber-blue to-cyber-purple flex items-center justify-center text-lg font-bold text-white shrink-0">
          {(opponent.name || 'P')[0]}
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-sm truncate">{opponent.name || 'Player'}</h4>
          <div className="flex items-center gap-3 text-[10px] text-gray-500 font-mono mt-0.5">
            <span>🏆 {opponent.wins || 0}</span>
            <span>📊 {opponent.rating || 1000}</span>
          </div>
        </div>
        <button
          onClick={(e) => { e.stopPropagation(); onChallenge?.(); }}
          disabled={status !== 'ready'}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${s.bg} ${
            status !== 'ready' ? 'opacity-60 cursor-not-allowed' : ''
          }`}
        >
          {s.label}
        </button>
      </div>
    </Card>
  );
}

export function FeatureCard({ icon, title, description, href, color = 'cyber-blue' }) {
  return (
    <Card
      rarity="common"
      onClick={() => href && (window.location.href = href)}
      tilt
      hoverEffect
    >
      <div className="text-center">
        <div
          className={`text-3xl mb-3 bg-${color}/15 w-14 h-14 rounded-xl flex items-center justify-center mx-auto`}
        >
          {icon}
        </div>
        <h3 className="font-semibold mb-1 text-sm">{title}</h3>
        <p className="text-xs text-gray-500 leading-relaxed">{description}</p>
      </div>
    </Card>
  );
}
