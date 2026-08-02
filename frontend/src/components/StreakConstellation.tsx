import { useRef, useEffect } from 'react';
import gsap from 'gsap';

const TOTAL_DAYS = 30;

function getConstellationPath(days) {
  const points = [];
  for (let i = 0; i < days; i++) {
    const angle = (i / days) * Math.PI * 2 - Math.PI / 2;
    const radius = 90 + (i % 3) * 8;
    points.push({
      x: 120 + Math.cos(angle) * radius,
      y: 120 + Math.sin(angle) * radius,
    });
  }
  return points;
}

export default function StreakConstellation({ streak = 0, longestStreak = 0, className = '' }) {
  const svgRef = useRef(null);
  const displayDays = Math.min(streak, TOTAL_DAYS);
  const points = getConstellationPath(TOTAL_DAYS);

  useEffect(() => {
    if (!svgRef.current) return;

    const stars = svgRef.current.querySelectorAll('.constellation-star');
    const lines = svgRef.current.querySelectorAll('.constellation-line');

    gsap.set(stars, { opacity: 0, scale: 0 });
    gsap.set(lines, { opacity: 0 });

    const tl = gsap.timeline({ delay: 0.2 });
    tl.to(lines, { opacity: 1, duration: 0.3, stagger: 0.015, ease: 'power2.out' })
      .to(stars, { opacity: 1, scale: 1, duration: 0.2, stagger: 0.03, ease: 'back.out(2)' }, '-=0.15');

    return () => {
      tl.kill();
    };
  }, [streak]);

  return (
    <div className={`relative ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-3 px-1">
        <div>
          <h3 className="text-sm font-display font-bold text-white uppercase tracking-wider">
            Streak Constellation
          </h3>
          <p className="text-[10px] font-mono text-gray-500 mt-0.5">
            {displayDays}/30 days active this month
          </p>
        </div>
        <div className="text-right">
          <div className="text-lg font-display font-bold text-cyber-blue flex items-center gap-1">
            <span className="streak-fire">🔥</span>
            {streak}
          </div>
          <p className="text-[9px] font-mono text-gray-600">
            best: {longestStreak}
          </p>
        </div>
      </div>

      {/* Constellation SVG */}
      <div className="flex justify-center">
        <svg
          ref={svgRef}
          viewBox="0 0 240 240"
          className="w-40 h-40 sm:w-56 sm:h-56"
          fill="none"
        >
          {/* Background glow */}
          <defs>
            <radialGradient id="bgGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="rgba(76,201,240,0.05)" />
              <stop offset="100%" stopColor="transparent" />
            </radialGradient>
            <filter id="starGlow">
              <feGaussianBlur stdDeviation="2" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <circle cx="120" cy="120" r="110" fill="url(#bgGlow)" />

          {/* Connection lines */}
          {points.slice(0, TOTAL_DAYS - 1).map((p, i) => {
            if (i >= displayDays) return null;
            const next = points[i + 1];
            if (!next) return null;
            const isActive = i < displayDays - 1;
            return (
              <line
                key={`line-${i}`}
                className="constellation-line"
                x1={p.x}
                y1={p.y}
                x2={next.x}
                y2={next.y}
                stroke={isActive ? 'rgba(76,201,240,0.4)' : 'rgba(100,100,120,0.15)'}
                strokeWidth={isActive ? 1.5 : 0.5}
                strokeDasharray={isActive ? 'none' : '2 3'}
              />
            );
          })}

          {/* Stars */}
          {points.map((p, i) => {
            const isActive = i < displayDays;
            const isToday = i === displayDays - 1;
            const isFuture = i >= displayDays;

            return (
              <g key={`star-${i}`} className={`constellation-star ${isActive ? 'active' : ''}`} filter={isActive ? 'url(#starGlow)' : undefined}>
                {/* Outer ring for today */}
                {isToday && (
                  <circle
                    cx={p.x}
                    cy={p.y}
                    r={8}
                    fill="none"
                    stroke="rgba(76,201,240,0.3)"
                    strokeWidth={1}
                  >
                    <animate
                      attributeName="r"
                      values="6;10;6"
                      dur="2s"
                      repeatCount="indefinite"
                    />
                    <animate
                      attributeName="opacity"
                      values="0.5;0.1;0.5"
                      dur="2s"
                      repeatCount="indefinite"
                    />
                  </circle>
                )}

                {/* Star dot */}
                <circle
                  cx={p.x}
                  cy={p.y}
                  r={isToday ? 4 : isActive ? 3 : 1.5}
                  fill={
                    isActive
                      ? i < 7
                        ? '#22C55E'
                        : i < 14
                        ? '#3B82F6'
                        : i < 21
                        ? '#A855F7'
                        : '#EAB308'
                      : 'rgba(100,100,120,0.2)'
                  }
                />

                {/* Day number for active */}
                {isActive && (
                  <text
                    x={p.x}
                    y={p.y + 0.5}
                    textAnchor="middle"
                    dominantBaseline="central"
                    fill="white"
                    fontSize="5"
                    fontFamily="JetBrains Mono"
                    fontWeight="600"
                  >
                    {i + 1}
                  </text>
                )}
              </g>
            );
          })}

          {/* Center label */}
          <text
            x="120"
            y="118"
            textAnchor="middle"
            fill="rgba(255,255,255,0.6)"
            fontSize="8"
            fontFamily="Orbitron"
            fontWeight="700"
          >
            STREAK
          </text>
          <text
            x="120"
            y="130"
            textAnchor="middle"
            fill="rgba(76,201,240,0.8)"
            fontSize="14"
            fontFamily="Orbitron"
            fontWeight="900"
          >
            {streak}
          </text>
        </svg>
      </div>
    </div>
  );
}
