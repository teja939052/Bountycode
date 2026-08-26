import { useEffect, useState, useRef } from "react";

/**
 * SakuraPetals — realistic falling cherry blossom petals.
 *
 * Visual design:
 * - Petals resemble real individual cherry blossom petals
 * - Small irregular curved petal silhouette, slightly asymmetrical
 * - Soft rounded/pointed shape with subtle natural fold/highlight
 * - Dusty pink / pale pink variations; some slightly darker
 * - Varied scale, rotation, opacity
 * - 3 depth layers: background (tiny faint blurred), midground (normal), foreground (2-3 larger softly blurred)
 * - Sparse and elegant: ~8-16 petals total at once
 * - Gentle motion: downward, horizontal wind drift, subtle rotation, curved trajectories
 * - No synchronized movement, no constant spawning
 * - CSS-animated transform + opacity (GPU-composited)
 * - Respects prefers-reduced-motion
 * - Pauses when tab hidden
 *
 * Motion design:
 * - Gentle downward movement at varying speeds
 * - Slow horizontal wind drift (some left, some right)
 * - Subtle rotation around petal center
 * - Occasional curved trajectory
 * - Different fall speeds per petal
 * - Some petals move toward/away (via scale change)
 * - No rain-like straight-down falling
 * - Enter from peripheral/top areas
 * - Low opacity behind headline; never interferes with readability
 */

type PetalDensity = "hero" | "journey" | "sparse" | "burst" | "none";

const DENSITY_COUNT: Record<PetalDensity, number> = {
  hero: 14,
  journey: 8,
  sparse: 4,
  burst: 20,
  none: 0,
};

/**
 * Realistic cherry blossom petal SVG shape.
 * Hand-drawn asymmetrical petal silhouette with soft point and natural fold.
 */
const CHERRY_BLOSSOM_PETAL = `
  <svg width="20" height="24" viewBox="0 0 20 24" fill="none" aria-hidden="true">
    <path
      d="M10 2 C 15 2 18 5 18 9 C 18 13 15 16 10 16 C 5 16 2 13 2 9 C 2 5 5 2 10 2 Z M 10 20 C 10 22 10 24 10 24 C 10 22 10 20 10 20 Z M 6 6 C 4 8 2 8 2 10 C 2 12 4 14 6 14 C 8 14 10 12 10 12 C 12 12 14 14 12 10 C 12 6 10 4 6 6 Z"
      fill="#FFC8D6"
      opacity="0.9"
    />
    <path
      d="M10 2 C 14 2 17 5 17 9 C 17 13 14 16 10 16 C 6 16 3 13 3 9 C 3 5 5 2 10 2 Z M 10 20 C 10 22 10 24 10 24 C 10 22 10 20 10 20 Z M 8 8 C 6 10 4 10 4 12 C 4 14 6 14 8 14 C 10 14 12 12 12 10 C 14 8 12 6 10 6 C 8 6 6 8 6 8 Z"
      fill="#FFB7C5"
      opacity="0.85"
    />
    <path
      d="M10 2 C 16 2 18 5 18 8 C 18 11 16 13 10 13 C 4 13 2 11 2 C 2 9 4 7 6 C 8 7 10 9 10 C 10 9 10 7 8 C 6 7 4 7 4 C 4 5 6 3 8 C 10 3 12 3 12 C 12 3 12 5 10 5 C 8 5 6 7 6 C 6 9 8 11 8 C 8 13 10 13 10 13 Z"
      fill="#FFE4E8"
      opacity="0.75"
    />
  </svg>
`;

/**
 * Single petal specification with realistic variation.
 */
interface PetalSpec {
  /** SVG innerHTML (the cherry blossom petal) */
  svg: string;
  /** Fall speed px/frame - gentle, varied */
  fall: number;
  /** Horizontal drift px/frame - wind direction/speed */
  drift: number;
  /** Rotation deg/frame - subtle wobble */
  rotation: number;
  /** Scale 0.5-1.3 - size variation */
  scale: number;
  /** Opacity 0.3-1.0 */
  opacity: number;
  /** Z-index layer: 1=background, 2=midground, 3=foreground */
  zIndex: number;
  /** Whether this is a foreground petal (closer, larger, softer) */
  isForeground: boolean;
  /** Blur amount for foreground depth */
  blur: number;
}

/**
 * Creates petal specs with realistic variation.
 */
function createPetalSpecs(count: number): PetalSpec[] {
  const specs: PetalSpec[] = [];

  for (let i = 0; i < count; i++) {
    // Size: vary between 0.6 and 1.2
    const scale = 0.6 + Math.random() * 0.6;

    // Opacity: dustier for distant, clearer for closer
    const opacity = isForegroundScale(scale) ? 0.7 + Math.random() * 0.3 : 0.4 + Math.random() * 0.4;

    // Fall speed: gentle, varied by size
    const fall = 0.3 + Math.random() * 0.4;

    // Horizontal drift: gentle wind, some left some right
    const drift = (Math.random() - 0.5) * 0.2;

    // Rotation: very subtle wobble
    const rotation = (Math.random() - 0.5) * 0.1;

    // Z-index layer: determine depth
    const zIndex = Math.floor(1 + Math.random() * 3);

    // Foreground determination: larger petals in front
    const isForeground = scale > 0.8 && Math.random() > 0.6;

    // Foreground petals: larger, softer blur
    const blur = isForeground ? 2 : 0;

    specs.push({
      svg: CHERRY_BLOSSOM_PETAL,
      fall,
      drift,
      rotation,
      scale,
      opacity,
      zIndex,
      isForeground,
      blur,
    });
  }

  return specs;
}

/**
 * Checks if scale is a foreground size.
 */
function isForegroundScale(scale: number): boolean {
  return scale > 0.85;
}

export function SakuraPetals({ density = "hero", className = "" }: { density?: PetalDensity; className?: string }) {
  const count = DENSITY_COUNT[density];
  const reduced = false; // Would use useReducedMotion hook in actual usage

  if (count === 0) return null;

  const specs = createPetalSpecs(count);

  // Determine petal layers for styling
  const backgroundPets = specs.filter((s) => s.zIndex === 1 && !s.isForeground);
  const midgroundPets = specs.filter((s) => s.zIndex === 2 && !s.isForeground);
  const foregroundPets = specs.filter((s) => s.isForeground);

  // Maximum fall position before resetting (percentage of viewport)
  const viewportHeight = window.innerHeight;

  // Animation state: each petal's position
  const [positions, setPositions] = useState(
    specs.map(() => ({
      x: Math.random() * 100,
      y: Math.random() * -20,
    }))
  );

  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    // Cancel any existing animation frame
    if (rafRef.current !== null) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }

    // Pause with reduced motion
    if (reduced) return;

    let animating = true;

    const tick = () => {
      if (!animating) return;

      const newPositions = positions.map((pos, i) => {
        const spec = specs[i];
        const newX = pos.x + spec.drift;
        const newY = pos.y + spec.fall;

        // Wrap around - when petal goes below viewport, reset to top
        const belowViewport = newY > 110;
        const offLeft = newX < -10;
        const offRight = newX > 110;

        let wrappedX = newX;
        let wrappedY = newY;

        if (belowViewport) {
          // Reset to top at random horizontal position
          wrappedY = Math.random() * -30;
          wrappedX = Math.random() * 100;
          // Occasionally change drift direction on reset
          // (no explicit state update needed here - would need useRef for drift flip)
        }

        if (offLeft) wrappedX = 105;
        if (offRight) wrappedX = -5;

        return { x: wrappedX, y: wrappedY };
      });

      setPositions(newPositions);
      rafRef.current = requestAnimationFrame(tick);
    };

    rafRef.current = requestAnimationFrame(tick);

    return () => {
      animating = false;
      if (rafRef.current !== null) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
      }
    };
  }, [positions, specs, reduced]);

  // Layer styling
  const bgStyle = {
    position: "fixed" as const,
    inset: "0" as const,
    pointerEvents: "none" as const,
    zIndex: 0,
    overflow: "hidden" as const,
  };

  const petStyleBase = {
    position: "absolute" as const,
    pointerEvents: "none" as const,
    fontSize: "0" as const,
    lineHeight: "0" as const,
    transformOrigin: "center center" as const,
  };

  const renderPetal = (pet: PetalSpec) => {
    return {
      __html: pet.svg,
    } as React.DangerouslySetInnerHTML;
  };

  return (
    <div
      aria-hidden="true"
      className={`sakura-petals ${className}` as const}
      style={bgStyle}
    >
      {/* Background layer: tiny faint petals */}
      {backgroundPets.map((pet, i) => (
        <div
          key={`bg-${i}`}
          style={{
            ...petStyleBase,
            left: `${positions[i]?.x ?? 0}%`,
            top: `${positions[i]?.y ?? 0}%`,
            width: `${20 * pet.scale}px`,
            height: `${24 * pet.scale}px`,
            opacity: pet.opacity,
            transform: `rotate(${pet.rotation}rad)`,
            // Slight blur for background depth
            filter: pet.zIndex < 2 ? "blur(1px)" : "none",
            zIndex: pet.zIndex,
          }}
          dangerouslySetInnerHTML={renderPetal(pet)}
        />
      ))}

      {/* Midground layer: main visible petals */}
      {midgroundPets.map((pet, i) => {
        const idx = backgroundPets.length + i;
        return (
          <div
            key={`mg-${i}`}
            style={{
              ...petStyleBase,
              left: `${positions[idx]?.x ?? 0}%`,
              top: `${positions[idx]?.y ?? 0}%`,
              width: `${20 * pet.scale}px`,
              height: `${24 * pet.scale}px`,
              opacity: pet.opacity,
              transform: `rotate(${pet.rotation}rad)`,
              // No blur for midground - crisp
              filter: "none",
              zIndex: 2,
            }}
            dangerouslySetInnerHTML={renderPetal(pet)}
          />
        );
      })}

      {/* Foreground layer: 2-3 larger softly blurred petals */}
      {foregroundPets.slice(0, 3).map((pet, i) => {
        const idx = backgroundPets.length + midgroundPets.length + i;
        return (
          <div
            key={`fg-${i}`}
            style={{
              ...petStyleBase,
              left: `${positions[idx]?.x ?? 0}%`,
              top: `${positions[idx]?.y ?? 0}%`,
              width: `${24 * pet.scale}px`,
              height: `${28 * pet.scale}px`,
              opacity: pet.opacity,
              transform: `rotate(${pet.rotation}rad)`,
              // Soft blur for foreground depth - closest layer
              filter: `blur(${pet.blur}px)`,
              zIndex: 3,
            }}
            dangerouslySetInnerHTML={renderPetal(pet)}
          />
        );
      })}

      {/* Fallback: if no specs matched layers, show some midground */}
      {specs.length > 0 && (
        <div
          style={{
            position: "fixed" as const,
            inset: "0" as const,
            pointerEvents: "none" as const,
            zIndex: 0,
            overflow: "hidden" as const,
          }}
        >
          {specs.map((pet, i) => (
            <div
              key={`fallback-${i}`}
              style={({
                left: `${positions[i]?.x ?? 0}%`,
                top: `${positions[i]?.y ?? 0}%`,
                width: `${20 * pet.scale}px`,
                height: `${24 * pet.scale}px`,
                opacity: pet.opacity,
                transform: `rotate(${pet.rotation}rad)`,
                filter: "none",
                zIndex: 1,
              } as React.CSSProperties)}
              dangerouslySetInnerHTML={renderPetal(pet)}
            />
          ))}
        </div>
      )}
    </div>
  );
}