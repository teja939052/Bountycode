import { useRef, useEffect, useMemo } from 'react';
import { motion } from 'framer-motion';
import confetti from 'canvas-confetti';

const TOTAL_DAYS = 30;

interface StreakConstellationProps {
  streak?: number;
  longestStreak?: number;
  className?: string;
  atRisk?: boolean;
}

const STREAK_MILESTONES = [
  { day: 3,  rarity: 'common',    color: '#9CA3AF', label: 'Consistent' },
  { day: 7,  rarity: 'uncommon',  color: '#22C55E', label: 'Dedicated' },
  { day: 14, rarity: 'uncommon',  color: '#3B82F6', label: 'Two Weeks' },
  { day: 30, rarity: 'rare',      color: '#A855F7', label: 'Unstoppable' },
  { day: 60, rarity: 'epic',      color: '#EC4899', label: 'Month Master' },
  { day: 100,rarity: 'legendary', color: '#EAB74D', label: 'Centurion' },
];

function getConstellationPath(days: number) {
  const points = [];
  for (let i = 0; i < days; i++) {
    const angle = (i / days) * Math.PI * 2 - Math.PI / 2;
    const radius = 90 + (i % 3) * 8;
    points.push({
      x: 120 + Math.cos(angle) * radius,
      y: 120 + Math.sin(angle) * radius,
      day: i + 1,
    });
  }
  return points;
}

export default function StreakConstellation({ streak = 0, longestStreak = 0, className = '', atRisk = false }: StreakConstellationProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const displayDays = Math.min(streak, TOTAL_DAYS);
  const points = useMemo(() => getConstellationPath(TOTAL_DAYS), []);

  const nextMilestone = useMemo(() => {
    return STREAK_MILESTONES.find(m => streak < m.day) || null;
  }, [streak]);

  const currentMilestone = useMemo(() => {
    return [...STREAK_MILESTONES].reverse().find(m => streak >= m.day) || null;
  }, [streak]);

  useEffect(() => {
    if (!svgRef.current) return;

    const stars = svgRef.current.querySelectorAll('.constellation-star');
    const lines = svgRef.current.querySelectorAll('.constellation-line');

    lines.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.animation = `fadeLine 0.3s ease-out ${0.2 + i * 0.015}s forwards`;
    });

    stars.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'scale(0)';
      el.style.transformOrigin = 'center';
      el.style.animation = `fadeStar 0.2s cubic-bezier(0.34,1.56,0.64,1) ${0.05 + i * 0.03}s forwards`;
    });
  }, [streak]);

  useEffect(() => {
    const milestone = STREAK_MILESTONES.find(m => streak === m.day);
    if (milestone) {
      confetti({
        particleCount: streak >= 100 ? 150 : 80,
        spread: streak >= 100 ? 120 : 65,
        origin: { y: 0.7 },
        colors: [milestone.color, '#ffffff', '#fbbf24'],
      });
    }
  }, [streak]);

  const streakColor = currentMilestone ? currentMilestone.color : '#6366f1';

  return (
    <motion.div
      className={`gamification-card rounded-3xl p-5 relative overflow-hidden ${className}`}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.01 }}
    >
      {atRisk && (
        <div className="absolute inset-0 bg-red-500/5 animate-pulse rounded-3xl" />
      )}

      {/* Header */}
      <div className="flex items-center justify-between mb-3 px-1 relative">
        <div>
          <h3 className="text-sm font-display font-bold text-text-primary uppercase tracking-wider">
            Streak Constellation
          </h3>
          <p className="text-[10px] font-mono text-gray-500 mt-0.5">
            {displayDays}/{TOTAL_DAYS} days active this month
          </p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-display font-black flex items-center gap-1.5 justify-end" style={{ color: atRisk ? '#EF4444' : streakColor }}>
            {atRisk ? '⚠️' : '🔥'} {streak}
          </div>
          <p className="text-[9px] font-mono text-gray-600">
            best: {longestStreak}
          </p>
        </div>
      </div>

      {/* Constellation SVG */}
      <div className="flex justify-center relative">
        <svg
          ref={svgRef}
          viewBox="0 0 240 240"
          className="w-44 h-44 sm:w-56 sm:h-56"
          fill="none"
        >
          <defs>
            <radialGradient id="bgGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor={atRisk ? 'rgba(239,68,68,0.1)' : `rgba(99,102,241,0.08)`} />
              <stop offset="100%" stopColor="transparent" />
            </radialGradient>
            <filter id="starGlow">
              <feGaussianBlur stdDeviation="2.5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <filter id="milestoneGlow">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <circle cx="120" cy="120" r="110" fill="url(#bgGlow)" />

          {/* Lines */}
          {points.slice(0, TOTAL_DAYS - 1).map((p, i) => {
            if (i >= displayDays) return null;
            const next = points[i + 1];
            if (!next) return null;
            const isActive = i < displayDays - 1;
            const isMilestone = STREAK_MILESTONES.some(m => m.day === i + 1);
            return (
              <line
                key={`line-${i}`}
                className="constellation-line"
                x1={p.x}
                y1={p.y}
                x2={next.x}
                y2={next.y}
                stroke={isMilestone ? `rgba(234,183,77,0.6)` : isActive ? `rgba(99,102,241,0.5)` : 'rgba(100,100,120,0.15)'}
                strokeWidth={isMilestone ? 2.5 : isActive ? 1.8 : 0.5}
                strokeDasharray={isActive ? 'none' : '2 3'}
              />
            );
          })}

          {/* Stars */}
          {points.map((p, i) => {
            const dayNum = i + 1;
            const isActive = i < displayDays;
            const isToday = i === displayDays - 1;
            const isFuture = i >= displayDays;
            const milestone = STREAK_MILESTONES.find(m => m.day === dayNum);
            const isMilestone = !!milestone;

            return (
              <g key={`star-${i}`} className={`constellation-star ${isActive ? 'active' : ''}`} filter={isMilestone && isActive ? 'url(#milestoneGlow)' : isActive ? 'url(#starGlow)' : undefined}>
                {isToday && (
                  <circle
                    cx={p.x}
                    cy={p.y}
                    r={10}
                    fill="none"
                    stroke={streakColor}
                    strokeWidth={1.2}
                  >
                    <animate attributeName="r" values="8;12;8" dur="2s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.6;0.15;0.6" dur="2s" repeatCount="indefinite" />
                  </circle>
                )}

                <circle
                  cx={p.x}
                  cy={p.y}
                  r={isMilestone ? 4.5 : isToday ? 4 : isActive ? 3 : 1.5}
                  fill={
                    isActive
                      ? isMilestone
                        ? milestone.color
                        : i < 7
                          ? '#22C55E'
                          : i < 14
                            ? '#3B82F6'
                            : i < 21
                              ? '#A855F7'
                              : '#EAB308'
                      : 'rgba(100,100,120,0.2)'
                  }
                />

                {isActive && (
                  <text
                    x={p.x}
                    y={p.y + 0.5}
                    textAnchor="middle"
                    dominantBaseline="central"
                    fill={isMilestone ? '#fff' : 'rgba(255,255,255,0.85)'}
                    fontSize={isMilestone ? '5.5' : '5'}
                    fontFamily="JetBrains Mono"
                    fontWeight={isMilestone ? '700' : '600'}
                  >
                    {dayNum}
                  </text>
                )}
              </g>
            );
          })}

          {/* Center label */}
          <text x="120" y="116" textAnchor="middle" fill="rgba(255,255,255,0.6)" fontSize="8" fontFamily="Orbitron" fontWeight="700">
            STREAK
          </text>
          <motion.text
            x="120"
            y="130"
            textAnchor="middle"
            fill={atRisk ? '#EF4444' : streakColor}
            fontSize="14"
            fontFamily="Orbitron"
            fontWeight="900"
            animate={atRisk ? { opacity: [1, 0.5, 1] } : {}}
            transition={{ duration: 1.2, repeat: Infinity }}
          >
            {streak}
          </motion.text>

          {/* Next milestone indicator */}
          {nextMilestone && (
            <g transform={`translate(${points[Math.min(nextMilestone.day - 1, TOTAL_DAYS - 1)]?.x || 120}, ${points[Math.min(nextMilestone.day - 1, TOTAL_DAYS - 1)]?.y || 120})`}>
              <circle r="14" fill="rgba(0,0,0,0.6)" stroke={nextMilestone.color} strokeWidth="1" strokeDasharray="2 2" />
              <text textAnchor="middle" dominantBaseline="central" fill={nextMilestone.color} fontSize="7" fontFamily="Orbitron" fontWeight="700">
                {nextMilestone.day}
              </text>
            </g>
          )}
        </svg>
      </div>

      {/* Milestone badges row */}
      <div className="flex items-center justify-center gap-2 mt-4">
        {STREAK_MILESTONES.map((m) => {
          const achieved = streak >= m.day;
          return (
            <div key={m.day} className="flex flex-col items-center gap-0.5">
              <div
                className="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold transition-all duration-500"
                style={{
                  background: achieved ? m.color : 'rgba(100,100,120,0.1)',
                  color: achieved ? '#fff' : 'rgba(100,100,120,0.4)',
                  boxShadow: achieved ? `0 0 10px ${m.color}40` : 'none',
                }}
              >
                {achieved ? '✓' : m.day}
              </div>
              <span className="text-[8px] font-mono uppercase tracking-wider" style={{ color: achieved ? m.color : 'rgba(100,100,120,0.4)' }}>
                {m.day}d
              </span>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}
