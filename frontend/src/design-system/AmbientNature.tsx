import { useEffect, useState } from "react";

/**
 * AmbientNature — ambient nostalgia layer for BountyCode.
 *
 * Design rules (DESIGN FREEZE V2):
 * - 3–8 leaves max. Ambient presence, not decoration spam.
 * - CSS-only animation (GPU-composited transform/opacity). No rAF loops.
 * - SVG leaves — never emoji.
 * - Pauses when tab hidden; disabled entirely with prefers-reduced-motion.
 */

const LEAF_COUNT = 6;

/** Deterministic leaf shapes so every render looks identical. */
function Leaf({ variant }: { variant: number }) {
  switch (variant % 3) {
    case 0:
      // Simple pointed leaf
      return (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M12 2C7 7 4 12 4 16c0 3 2 5 5 5h6c3 0 5-2 5-5 0-4-3-9-8-14z"
            fill="currentColor"
            opacity="0.9"
          />
          <path d="M12 5v13" stroke="rgba(255,255,255,0.45)" strokeWidth="1" strokeLinecap="round" />
        </svg>
      );
    case 1:
      // Rounded leaf
      return (
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M20 4c-8 0-15 4-15 11 0 2 1 4 3 5 1-5 5-10 10-13-4 4-8 9-9 13 1 .3 2 .5 3 .5 6 0 9-7 8-16z"
            fill="currentColor"
            opacity="0.85"
          />
        </svg>
      );
    default:
      // Small drifting seed/spore
      return (
        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="12" cy="12" r="5" fill="currentColor" opacity="0.75" />
          <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="1.5" opacity="0.35" fill="none" />
        </svg>
      );
  }
}

export type NatureDensity = "minimal" | "normal";

interface AmbientNatureProps {
  /** minimal = 3 elements (tool pages), normal = 6 (landing/home/map) */
  density?: NatureDensity;
  className?: string;
}

export function AmbientNature({ density = "normal", className = "" }: AmbientNatureProps) {
  const count = density === "minimal" ? 3 : LEAF_COUNT;
  const [paused, setPaused] = useState(false);

  useEffect(() => {
    const onVisibility = () => setPaused(document.hidden);
    document.addEventListener("visibilitychange", onVisibility);
    return () => document.removeEventListener("visibilitychange", onVisibility);
  }, []);

  return (
    <div
      aria-hidden="true"
      className={`ambient-nature pointer-events-none fixed inset-0 overflow-hidden ${className} ${
        paused ? "ambient-paused" : ""
      }`}
      style={{ zIndex: 0 }}
    >
      {Array.from({ length: count }, (_, i) => {
        const variants = ["#86B98A", "#A8C69F", "#7FB89B"];
        return (
          <div
            key={i}
            className="leaf-fall absolute -top-8"
            style={{ color: variants[i % variants.length] }}
          >
            <Leaf variant={i} />
          </div>
        );
      })}
    </div>
  );
}
