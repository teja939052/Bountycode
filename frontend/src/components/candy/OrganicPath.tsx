import { motion } from "framer-motion";

interface OrganicPathProps {
  points: { x: number; y: number; status: string }[];
  className?: string;
}

export default function OrganicPath({ points, className = "" }: OrganicPathProps) {
  if (points.length < 2) return null;

  const width = 100;
  const height = 100;

  const pathD = points.reduce((d, point, i) => {
    const x = (point.x / width) * 100;
    const y = (point.y / height) * 100;
    if (i === 0) return `M ${x} ${y}`;
    const prev = points[i - 1];
    const px = (prev.x / width) * 100;
    const py = (prev.y / height) * 100;
    const cp1x = px + (x - px) * 0.4;
    const cp1y = py + (y - py) * 0.1;
    const cp2x = px + (x - px) * 0.6;
    const cp2y = py + (y - py) * 0.9;
    return `${d} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${x} ${y}`;
  }, "");

  return (
    <svg
      className={`absolute inset-0 w-full h-full pointer-events-none ${className}`}
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
    >
      <defs>
        <linearGradient id="pathGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="rgba(255,255,255,0.05)" />
          <stop offset="50%" stopColor="rgba(255,255,255,0.15)" />
          <stop offset="100%" stopColor="rgba(255,255,255,0.05)" />
        </linearGradient>
        <filter id="pathGlow">
          <feGaussianBlur stdDeviation="0.5" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <motion.path
        d={pathD}
        fill="none"
        stroke="url(#pathGradient)"
        strokeWidth="0.8"
        strokeLinecap="round"
        filter="url(#pathGlow)"
        initial={{ pathLength: 0, opacity: 0 }}
        animate={{ pathLength: 1, opacity: 1 }}
        transition={{ duration: 2.5, ease: "easeInOut" }}
      />
      {/* Animated flowing particles along the path */}
      <circle r="0.5" fill="rgba(255,255,255,0.6)">
        <animateMotion dur="4s" repeatCount="indefinite" path={pathD} />
      </circle>
      <circle r="0.3" fill="rgba(255,255,255,0.4)">
        <animateMotion dur="5s" repeatCount="indefinite" path={pathD} begin="1s" />
      </circle>
    </svg>
  );
}
