import { useMemo } from "react";

/**
 * SakuraPetals — lightweight CSS-animated cherry blossom petals.
 *
 * Architecture:
 * - ALL animation is CSS @keyframes (GPU-composited transform + opacity)
 * - ZERO React state updates during animation
 * - ZERO requestAnimationFrame loops
 * - ZERO per-frame DOM manipulation
 * - Petal positions are randomized once at mount via useMemo
 * - Respects prefers-reduced-motion via CSS
 * - Pauses when tab hidden via CSS animation-play-state
 */

type PetalDensity = "hero" | "journey" | "sparse" | "none";

const DENSITY_COUNT: Record<PetalDensity, number> = {
  hero: 8,
  journey: 4,
  sparse: 2,
  none: 0,
};

/** Simple petal SVG — clean, minimal, realistic shape */
const PETAL_SVG = `<svg width="14" height="16" viewBox="0 0 14 16" fill="none"><path d="M7 1 C 10 1 12 3 12 6 C 12 9 10 11 7 11 C 4 11 2 9 2 6 C 2 3 4 1 7 1 Z" fill="COLOR" opacity="OPACITY"/><path d="M7 14 C 7 15.5 7 16 7 16" stroke="COLOR" stroke-width="0.5" opacity="0.3"/></svg>`;

interface PetalConfig {
  x: number;        // starting horizontal position (%)
  delay: number;     // animation delay (s)
  duration: number;  // animation duration (s)
  scale: number;     // size multiplier
  rotation: number;  // initial rotation (deg)
  opacity: number;   // petal opacity
  color: string;     // petal fill color
  blur: number;      // depth blur (px)
  drift: number;     // horizontal drift amount (px)
}

function createPetals(count: number): PetalConfig[] {
  const colors = ["#FFC8D6", "#FFB7C5", "#FFE4E8", "#FFD6DE", "#FFccd5"];
  const petals: PetalConfig[] = [];
  for (let i = 0; i < count; i++) {
    const scale = 0.6 + Math.random() * 0.5;
    petals.push({
      x: Math.random() * 100,
      delay: Math.random() * 12,
      duration: 8 + Math.random() * 7,
      scale,
      rotation: Math.random() * 360,
      opacity: scale > 0.85 ? 0.5 + Math.random() * 0.3 : 0.3 + Math.random() * 0.3,
      color: colors[Math.floor(Math.random() * colors.length)],
      blur: scale > 0.9 ? 1.5 : 0,
      drift: (Math.random() - 0.5) * 40,
    });
  }
  return petals;
}

export function SakuraPetals({ density = "hero" }: { density?: PetalDensity }) {
  const count = DENSITY_COUNT[density];
  const petals = useMemo(() => (count > 0 ? createPetals(count) : []), [count]);

  if (count === 0) return null;

  return (
    <div
      aria-hidden="true"
      style={{
        position: "fixed",
        inset: 0,
        pointerEvents: "none",
        zIndex: 1,
        overflow: "hidden",
      }}
    >
      {petals.map((p, i) => {
        const svg = PETAL_SVG.replace("COLOR", p.color).replace("OPACITY", String(p.opacity));
        return (
          <div
            key={i}
            className="sakura-petal"
            style={{
              position: "absolute",
              left: `${p.x}%`,
              top: "-5%",
              width: `${14 * p.scale}px`,
              height: `${16 * p.scale}px`,
              opacity: p.opacity,
              filter: p.blur > 0 ? `blur(${p.blur}px)` : undefined,
              animationDelay: `${p.delay}s`,
              animationDuration: `${p.duration}s`,
              // CSS custom properties for drift
              ["--drift" as string]: `${p.drift}px`,
              ["--start-rot" as string]: `${p.rotation}deg`,
            }}
            dangerouslySetInnerHTML={{ __html: svg }}
          />
        );
      })}
    </div>
  );
}
