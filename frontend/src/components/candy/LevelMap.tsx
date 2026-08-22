import { useEffect, useRef, useState, useMemo, memo } from "react";
import { Lock, CheckCircle2, Play, Star, Trophy, Zap } from "lucide-react";
import type { ReactNode } from "react";
import { candyGradient, type CandyColor } from "./palette";

export type LevelStatus = "locked" | "available" | "current" | "completed" | "mastered";

export interface LevelNode {
  level: number;
  status: LevelStatus;
  title?: string;
  xp?: number;
  stars?: number;
  color?: CandyColor;
  icon?: ReactNode;
}

interface LevelMapProps {
  levels: LevelNode[];
  onLevelClick?: (level: LevelNode) => void;
  currentLevel?: number;
  className?: string;
}

const STATUS_CONFIG: Record<LevelStatus, { icon: typeof Lock; color: CandyColor; glow: string }> = {
  locked: { icon: Lock, color: "grape", glow: "rgba(132,92,194,0.2)" },
  available: { icon: Play, color: "mint", glow: "rgba(0,201,167,0.3)" },
  current: { icon: Zap, color: "lemon", glow: "rgba(255,199,95,0.4)" },
  completed: { icon: CheckCircle2, color: "blueberry", glow: "rgba(75,123,236,0.3)" },
  mastered: { icon: Trophy, color: "gold", glow: "rgba(255,215,0,0.4)" },
};

const LevelNode = memo(function LevelNode({
  level,
  config,
  isInteractive,
  onClick,
}: {
  level: LevelNode;
  config: { icon: typeof Lock; color: CandyColor; glow: string };
  isInteractive: boolean;
  onClick?: () => void;
}) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setVisible(true), level.level * 8);
    return () => clearTimeout(timer);
  }, [level.level]);

  return (
    <button
      onClick={onClick}
      disabled={!isInteractive}
      className={`
        relative flex flex-col items-center justify-center
        aspect-square rounded-2xl border transition-all duration-300
        ${isInteractive ? "cursor-pointer hover:scale-110 hover:-translate-y-1" : "cursor-not-allowed opacity-50"}
        ${level.status === "current" ? "animate-pulse-glow" : ""}
      `}
      style={{
        background: candyGradient(level.color || config.color),
        borderColor:
          level.status === "mastered"
            ? "rgba(255,215,0,0.7)"
            : level.status === "current"
              ? "rgba(255,255,255,0.6)"
              : level.status === "completed"
                ? "rgba(255,255,255,0.2)"
                : "rgba(255,255,255,0.08)",
        boxShadow:
          level.status === "mastered"
            ? "0 0 20px rgba(255,215,0,0.4)"
            : level.status === "current"
              ? `0 0 25px ${config.glow}`
              : level.status === "completed"
                ? "0 0 12px rgba(75,123,236,0.25)"
                : "none",
        opacity: visible ? 1 : 0,
        transform: visible ? "scale(1)" : "scale(0.5)",
      }}
    >
      <div className="absolute inset-0 rounded-2xl candy-gloss pointer-events-none" />

      {level.status === "locked" && <div className="absolute inset-0 rounded-2xl bg-black/60 backdrop-blur-[1px]" />}

      <div className="relative z-10 flex flex-col items-center gap-0.5">
        <span className="text-white/90" style={{ fontSize: level.status === "locked" ? 12 : 16 }}>
          {level.icon || <config.icon size={level.status === "locked" ? 12 : 16} />}
        </span>
        <span className="text-[8px] font-black text-white/90 leading-none">{level.level}</span>
        {level.stars !== undefined && level.status !== "locked" && (
          <div className="flex gap-0.5">
            {[1, 2, 3].map((star) => (
              <Star
                key={star}
                size={6}
                className={star <= level.stars ? "text-yellow-300 fill-yellow-300" : "text-white/20"}
              />
            ))}
          </div>
        )}
      </div>

      {level.status === "mastered" && (
        <span className="absolute -top-1.5 -right-1.5 z-20 inline-flex h-5 w-5 items-center justify-center rounded-full bg-yellow-400 shadow-lg">
          <Trophy size={10} className="text-yellow-900" />
        </span>
      )}

      {level.title && isInteractive && (
        <span className="absolute -bottom-7 left-1/2 -translate-x-1/2 z-30 whitespace-nowrap text-[9px] font-bold text-white/90 bg-black/70 px-2 py-0.5 rounded-full backdrop-blur-md border border-white/10">
          {level.title}
        </span>
      )}
    </button>
  );
});

const LevelMap = memo(function LevelMap({ levels, onLevelClick, currentLevel, className = "" }: LevelMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isInView, setIsInView] = useState(false);
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReducedMotion(motionQuery.matches);
    const handler = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches);
    motionQuery.addEventListener("change", handler);
    return () => motionQuery.removeEventListener("change", handler);
  }, []);

  useEffect(() => {
    const node = containerRef.current;
    if (!node) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  const cols = 10;
  const rows = Math.ceil(levels.length / cols);

  const pathLines = useMemo(() => {
    if (prefersReducedMotion) return [];
    return levels
      .map((level, i) => {
        if (level.status === "locked") return null;
        const next = levels[i + 1];
        if (!next || next.status === "locked") return null;

        const x1 = ((i % cols) + 0.5) * (100 / cols);
        const y1 = (Math.floor(i / cols) + 0.5) * (100 / rows);
        const x2 = ((i + 1) % cols + 0.5) * (100 / cols);
        const y2 = (Math.floor((i + 1) / cols) + 0.5) * (100 / rows);

        const color =
          level.status === "mastered" ? "#ffd700" : level.status === "completed" ? "#4b7bec" : "rgba(255,255,255,0.15)";

        return (
          <line
            key={`path-${i}`}
            x1={`${x1}%`}
            y1={`${y1}%`}
            x2={`${x2}%`}
            y2={`${y2}%`}
            stroke={color}
            strokeWidth="0.5"
            strokeLinecap="round"
            style={{ opacity: isInView ? 0.5 : 0, transition: `opacity 0.5s ease ${i * 0.02}s` }}
          />
        );
      })
      .filter(Boolean);
  }, [levels, cols, rows, isInView, prefersReducedMotion]);

  if (!isInView) {
    return (
      <div ref={containerRef} className={className}>
        <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}>
          {levels.map((level) => (
            <div key={level.level} className="aspect-square rounded-2xl bg-white/5" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div ref={containerRef} className={`relative ${className}`}>
      {/* Background grid */}
      <div className="absolute inset-0 opacity-10">
        <div
          className="h-full w-full"
          style={{
            backgroundImage: `radial-gradient(circle, rgba(255,255,255,0.12) 1px, transparent 1px)`,
            backgroundSize: "20px 20px",
          }}
        />
      </div>

      {/* Connecting paths */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 0 }}>
        {pathLines}
      </svg>

      {/* Level grid */}
      <div
        className="relative grid gap-2"
        style={{
          gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))`,
          gridTemplateRows: `repeat(${rows}, minmax(0, 1fr))`,
        }}
      >
        {levels.map((level, index) => {
          const config = STATUS_CONFIG[level.status];
          const isInteractive = level.status !== "locked";

          return (
            <LevelNode
              key={level.level}
              level={level}
              config={config}
              isInteractive={isInteractive}
              onClick={() => isInteractive && onLevelClick?.(level)}
            />
          );
        })}
      </div>

      {/* Legend */}
      <div className="mt-10 flex flex-wrap items-center justify-center gap-3 text-xs">
        {Object.entries(STATUS_CONFIG).map(([status, config]) => {
          const Icon = config.icon;
          return (
            <div key={status} className="flex items-center gap-1.5 text-white/50">
              <div
                className="h-2.5 w-2.5 rounded-full"
                style={{ background: candyGradient(config.color), boxShadow: `0 0 6px ${config.glow}` }}
              />
              <Icon size={10} />
              <span className="capitalize font-medium">{status}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
});

export default LevelMap;
