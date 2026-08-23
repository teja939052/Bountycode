import { useMemo } from "react";
import useReducedMotion from "../hooks/useReducedMotion";

interface LeafConfig {
  id: number;
  left: string;
  size: number;
  delay: string;
  duration: string;
  drift: string;
  spin: string;
  opacity: number;
  hideOnMobile: boolean;
}

function makeLeaves(count: number): LeafConfig[] {
  return Array.from({ length: count }, (_, i) => {
    const seed = (n: number, salt: number) => ((Math.sin(n * 999 + salt) + 1) / 2);
    const s = i * 7.13;
    return {
      id: i,
      left: `${Math.round(seed(s, 1) * 96)}%`,
      size: Math.round(14 + seed(s, 2) * 16),
      delay: `${(-seed(s, 3) * 18).toFixed(1)}s`,
      duration: `${(11 + seed(s, 4) * 9).toFixed(1)}s`,
      drift: `${Math.round((seed(s, 5) - 0.5) * 160)}px`,
      spin: `${Math.round(180 + seed(s, 6) * 360) * (i % 2 === 0 ? 1 : -1)}deg`,
      opacity: Number((0.25 + seed(s, 7) * 0.3).toFixed(2)),
      hideOnMobile: i >= Math.ceil(count / 2),
    };
  });
}

export default function FallingLeaves({ count = 12 }: { count?: number }) {
  const reducedMotion = useReducedMotion();
  const leaves = useMemo(() => makeLeaves(count), [count]);

  if (reducedMotion) {
    return (
      <div aria-hidden="true" className="pointer-events-none fixed inset-0 overflow-hidden">
        {leaves.slice(0, 6).map((leaf) => (
          <svg
            key={leaf.id}
            viewBox="0 0 24 24"
            width={leaf.size}
            height={leaf.size}
            className="absolute text-brand-primary"
            style={{ top: `${(leaf.id * 17) % 90}%`, left: leaf.left, opacity: leaf.opacity }}
            fill="currentColor"
          >
            <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z" />
          </svg>
        ))}
      </div>
    );
  }

  return (
    <div aria-hidden="true" className="pointer-events-none fixed inset-0 z-0 overflow-hidden">
      {leaves.map((leaf) => (
        <svg
          key={leaf.id}
          viewBox="0 0 24 24"
          width={leaf.size}
          height={leaf.size}
          fill="currentColor"
          className={`absolute top-[-8vh] text-brand-primary leaf-fall ${
            leaf.hideOnMobile ? "hidden md:block" : ""
          }`}
          style={
            {
              left: leaf.left,
              animationDelay: leaf.delay,
              animationDuration: leaf.duration,
              "--leaf-drift": leaf.drift,
              "--leaf-spin": leaf.spin,
              "--leaf-opacity": leaf.opacity,
            } as React.CSSProperties
          }
        >
          <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z" />
        </svg>
      ))}
    </div>
  );
}
