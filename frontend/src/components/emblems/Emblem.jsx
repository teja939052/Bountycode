import { useMemo } from 'react';
import { motion } from 'framer-motion';
import {
  EMBLEM_COLORS, DIFFICULTY_STYLES, EMBLEM_SIZES,
  getEmblemForTopic, getEmblemForQuestion,
} from './emblemData';

export default function Emblem({
  type,
  question,
  topic,
  difficulty = 'medium',
  size = 'md',
  animated = true,
  className = '',
  glow = true,
  label = false,
}) {
  const emblemType = type || (question ? getEmblemForQuestion(question) : getEmblemForTopic(topic));
  const colors = EMBLEM_COLORS[emblemType] || EMBLEM_COLORS.eye;
  const diffStyle = DIFFICULTY_STYLES[difficulty] || DIFFICULTY_STYLES.medium;
  const px = typeof size === 'number' ? size : (EMBLEM_SIZES[size] || 48);

  return (
    <div className={`emblem-container ${className}`} style={{ width: px, height: px }}>
      <motion.div
        className="relative w-full h-full"
        animate={animated ? {
          filter: [
            `drop-shadow(0 0 ${2 * diffStyle.glowIntensity}px ${colors.glow})`,
            `drop-shadow(0 0 ${6 * diffStyle.glowIntensity}px ${colors.glow})`,
            `drop-shadow(0 0 ${2 * diffStyle.glowIntensity}px ${colors.glow})`,
          ],
        } : undefined}
        transition={animated ? { duration: 3, repeat: Infinity, ease: 'easeInOut' } : undefined}
      >
        <svg
          viewBox="0 0 100 100"
          width={px}
          height={px}
          className="emblem-svg"
          style={{ opacity: diffStyle.opacity }}
        >
          <EmblemShape
            type={emblemType}
            colors={colors}
            rings={diffStyle.rings}
            animated={animated}
          />
        </svg>
      </motion.div>
      {label && (
        <div className="text-center mt-1">
          <span className="text-[8px] font-mono uppercase tracking-widest" style={{ color: colors.primary }}>
            {emblemType.replace(/([A-Z])/g, ' $1').trim()}
          </span>
        </div>
      )}
    </div>
  );
}

// ─── Individual Emblem SVG Shapes ───

function EmblemShape({ type, colors, rings, animated }) {
  const p = colors.primary;
  const s = colors.secondary;

  switch (type) {
    case 'triquetra':
      return <Triquetra p={p} s={s} rings={rings} animated={animated} />;
    case 'mandala':
      return <Mandala p={p} s={s} rings={rings} animated={animated} />;
    case 'dharma':
      return <DharmaWheel p={p} s={s} rings={rings} animated={animated} />;
    case 'sriYantra':
      return <SriYantra p={p} s={s} rings={rings} animated={animated} />;
    case 'celticKnot':
      return <CelticKnot p={p} s={s} rings={rings} animated={animated} />;
    case 'flowerOfLife':
      return <FlowerOfLife p={p} s={s} rings={rings} animated={animated} />;
    case 'hexagram':
      return <Hexagram p={p} s={s} rings={rings} animated={animated} />;
    case 'spiral':
      return <GoldenSpiral p={p} s={s} rings={rings} animated={animated} />;
    case 'yinYang':
      return <YinYang p={p} s={s} rings={rings} animated={animated} />;
    case 'eye':
      return <AllSeeingEye p={p} s={s} rings={rings} animated={animated} />;
    case 'shield':
      return <Shield p={p} s={s} rings={rings} animated={animated} />;
    case 'compass':
      return <Compass p={p} s={s} rings={rings} animated={animated} />;
    default:
      return <AllSeeingEye p={p} s={s} rings={rings} animated={animated} />;
  }
}

// ─── Triquetra (3 interlocking vesica piscis) ───
function Triquetra({ p, s, rings }) {
  return (
    <g transform="translate(50,50)">
      {[0, 120, 240].map((angle, i) => (
        <g key={i} transform={`rotate(${angle})`}>
          <ellipse cx="0" cy="-14" rx="16" ry="22" fill="none" stroke={p}
            strokeWidth={1.5} opacity={0.8} />
          {rings > 1 && (
            <ellipse cx="0" cy="-14" rx="12" ry="18" fill="none" stroke={s}
              strokeWidth={0.8} opacity={0.5} />
          )}
        </g>
      ))}
      <circle cx="0" cy="0" r="4" fill={p} opacity={0.6} />
      <circle cx="0" cy="0" r="2" fill={s} />
      {rings > 2 && (
        <circle cx="0" cy="0" r="38" fill="none" stroke={p}
          strokeWidth={0.5} opacity={0.3} strokeDasharray="3 3" />
      )}
    </g>
  );
}

// ─── Mandala (concentric circles + petals) ───
function Mandala({ p, s, rings }) {
  const petals = 8;
  return (
    <g transform="translate(50,50)">
      <circle cx="0" cy="0" r="40" fill="none" stroke={p} strokeWidth={0.5} opacity={0.2} />
      {rings >= 1 && <circle cx="0" cy="0" r="30" fill="none" stroke={p} strokeWidth={0.8} opacity={0.4} />}
      {rings >= 2 && <circle cx="0" cy="0" r="20" fill="none" stroke={s} strokeWidth={0.8} opacity={0.5} />}
      {Array.from({ length: petals }).map((_, i) => {
        const angle = (360 / petals) * i;
        return (
          <g key={i} transform={`rotate(${angle})`}>
            <ellipse cx="0" cy="-25" rx="5" ry="12" fill="none" stroke={p}
              strokeWidth={1} opacity={0.6} />
            <line x1="0" y1="-13" x2="0" y2="-37" stroke={p} strokeWidth={0.3} opacity={0.3} />
          </g>
        );
      })}
      <circle cx="0" cy="0" r="5" fill={p} opacity={0.3} />
      <circle cx="0" cy="0" r="2.5" fill={s} />
    </g>
  );
}

// ─── Dharma Wheel (8-spoke chakra) ───
function DharmaWheel({ p, s, rings }) {
  return (
    <g transform="translate(50,50)">
      <circle cx="0" cy="0" r="38" fill="none" stroke={p} strokeWidth={1.5} opacity={0.5} />
      {rings > 1 && <circle cx="0" cy="0" r="33" fill="none" stroke={s} strokeWidth={0.5} opacity={0.3} />}
      <circle cx="0" cy="0" r="8" fill="none" stroke={p} strokeWidth={1.5} opacity={0.7} />
      {Array.from({ length: 8 }).map((_, i) => {
        const angle = (360 / 8) * i;
        const rad = (angle * Math.PI) / 180;
        return (
          <g key={i}>
            <line x1={Math.cos(rad) * 8} y1={Math.sin(rad) * 8}
              x2={Math.cos(rad) * 38} y2={Math.sin(rad) * 38}
              stroke={p} strokeWidth={1} opacity={0.5} />
            <circle cx={Math.cos(rad) * 38} cy={Math.sin(rad) * 38} r="2.5"
              fill={p} opacity={0.6} />
          </g>
        );
      })}
      <circle cx="0" cy="0" r="3" fill={s} />
    </g>
  );
}

// ─── Sri Yantra (nested triangles) ───
function SriYantra({ p, s, rings }) {
  const tri = (y, size, invert) => {
    const h = size * 0.866;
    const pts = invert
      ? `0,${-y - h} ${-size},${-y + h / 2} ${size},${-y + h / 2}`
      : `0,${y + h} ${-size},${y - h / 2} ${size},${y - h / 2}`;
    return pts;
  };
  return (
    <g transform="translate(50,52)">
      <circle cx="0" cy="0" r="40" fill="none" stroke={p} strokeWidth={0.5} opacity={0.2} />
      {[[-12, 20, true], [-6, 26, false], [0, 32, true], [6, 38, false]].map(([y, sz, inv], i) => (
        <polygon key={i} points={tri(y, sz, inv)} fill="none"
          stroke={i % 2 === 0 ? p : s} strokeWidth={1} opacity={0.5 + i * 0.1} />
      ))}
      {rings > 1 && (
        <circle cx="0" cy="0" r="10" fill="none" stroke={s} strokeWidth={0.8} opacity={0.4} />
      )}
      <circle cx="0" cy="0" r="3" fill={p} opacity={0.5} />
      <circle cx="0" cy="0" r="1.5" fill={s} />
    </g>
  );
}

// ─── Celtic Knot (interlocking loops) ───
function CelticKnot({ p, s, rings }) {
  return (
    <g transform="translate(50,50)">
      {[0, 60, 120].map((angle, i) => (
        <g key={i} transform={`rotate(${angle})`}>
          <rect x="-18" y="-18" width="36" height="36" rx="10" fill="none"
            stroke={p} strokeWidth={1.5} opacity={0.6} />
          {rings > 1 && (
            <rect x="-13" y="-13" width="26" height="26" rx="7" fill="none"
              stroke={s} strokeWidth={0.8} opacity={0.4} />
          )}
        </g>
      ))}
      <circle cx="0" cy="0" r="6" fill="none" stroke={p} strokeWidth={1.5} opacity={0.7} />
      <circle cx="0" cy="0" r="2.5" fill={s} />
      {rings > 2 && (
        <circle cx="0" cy="0" r="42" fill="none" stroke={p}
          strokeWidth={0.4} opacity={0.2} strokeDasharray="4 4" />
      )}
    </g>
  );
}

// ─── Flower of Life (overlapping circles) ───
function FlowerOfLife({ p, s, rings }) {
  const r = 14;
  const centers = [[0, 0]];
  const offsets = [[0, -r], [r * 0.866, r * 0.5], [r * 0.866, -r * 0.5],
    [0, r], [-r * 0.866, r * 0.5], [-r * 0.866, -r * 0.5]];
  offsets.forEach(o => centers.push(o));

  return (
    <g transform="translate(50,50)">
      {rings > 2 && <circle cx="0" cy="0" r="40" fill="none" stroke={p} strokeWidth={0.3} opacity={0.2} />}
      {centers.map((c, i) => (
        <circle key={i} cx={c[0]} cy={c[1]} r={r} fill="none"
          stroke={i === 0 ? p : s} strokeWidth={i === 0 ? 1.2 : 0.7} opacity={0.5 + (i === 0 ? 0.2 : 0)} />
      ))}
      {rings > 1 && (
        <circle cx="0" cy="0" r={r * 0.5} fill={p} opacity={0.15} />
      )}
      <circle cx="0" cy="0" r="3" fill={s} />
    </g>
  );
}

// ─── Hexagram (two overlapping triangles) ───
function Hexagram({ p, s, rings }) {
  return (
    <g transform="translate(50,50)">
      <polygon points="0,-32 28,16 -28,16" fill="none" stroke={p} strokeWidth={1.5} opacity={0.7} />
      <polygon points="0,32 28,-16 -28,-16" fill="none" stroke={s} strokeWidth={1.5} opacity={0.7} />
      {rings > 1 && (
        <>
          <polygon points="0,-20 17,10 -17,10" fill="none" stroke={p} strokeWidth={0.8} opacity={0.4} />
          <polygon points="0,20 17,-10 -17,-10" fill="none" stroke={s} strokeWidth={0.8} opacity={0.4} />
        </>
      )}
      <circle cx="0" cy="0" r="8" fill="none" stroke={p} strokeWidth={0.8} opacity={0.5} />
      <circle cx="0" cy="0" r="2.5" fill={s} />
      {rings > 2 && (
        <circle cx="0" cy="0" r="42" fill="none" stroke={p}
          strokeWidth={0.4} opacity={0.2} strokeDasharray="2 4" />
      )}
    </g>
  );
}

// ─── Golden Spiral (Fibonacci) ───
function GoldenSpiral({ p, s, rings }) {
  return (
    <g transform="translate(50,50)">
      <rect x="-40" y="-40" width="80" height="80" fill="none" stroke={p} strokeWidth={0.4} opacity={0.15} />
      <path d="M 24,24 Q 24,-16 -16,-16 Q -16,24 24,24 Q 64,24 64,-16 Q -16,-16 -16,64"
        fill="none" stroke={p} strokeWidth={1.5} opacity={0.6} strokeLinecap="round" />
      {rings > 1 && (
        <path d="M 16,16 Q 16,-10 -10,-10 Q -10,16 16,16 Q 40,16 40,-10 Q -10,-10 -10,40"
          fill="none" stroke={s} strokeWidth={0.8} opacity={0.4} strokeLinecap="round" />
      )}
      <circle cx="24" cy="24" r="2" fill={p} opacity={0.8} />
      <circle cx="0" cy="0" r="3" fill={s} />
      {rings > 2 && (
        <rect x="-42" y="-42" width="84" height="84" fill="none" stroke={p}
          strokeWidth={0.3} opacity={0.15} rx="2" />
      )}
    </g>
  );
}

// ─── Yin-Yang ───
function YinYang({ p, s, rings }) {
  return (
    <g transform="translate(50,50)">
      <circle cx="0" cy="0" r="38" fill="none" stroke={p} strokeWidth={0.5} opacity={0.2} />
      <path d="M 0,-35 A 35,35 0 0,1 0,35 A 17.5,17.5 0 0,0 0,0 A 17.5,17.5 0 0,1 0,-35"
        fill={p} opacity={0.25} />
      <path d="M 0,35 A 35,35 0 0,1 0,-35 A 17.5,17.5 0 0,0 0,0 A 17.5,17.5 0 0,1 0,35"
        fill={s} opacity={0.25} />
      <circle cx="0" cy="-17.5" r="4" fill={s} opacity={0.6} />
      <circle cx="0" cy="17.5" r="4" fill={p} opacity={0.6} />
      {rings > 1 && (
        <circle cx="0" cy="0" r="25" fill="none" stroke={p} strokeWidth={0.6} opacity={0.3} />
      )}
      <circle cx="0" cy="0" r="38" fill="none" stroke={p} strokeWidth={1.5} opacity={0.5} />
      {rings > 2 && (
        <circle cx="0" cy="0" r="42" fill="none" stroke={s} strokeWidth={0.3} opacity={0.2} />
      )}
    </g>
  );
}

// ─── All-Seeing Eye ───
function AllSeeingEye({ p, s, rings }) {
  return (
    <g transform="translate(50,50)">
      <polygon points="0,-38 33,20 -33,20" fill="none" stroke={p} strokeWidth={1.5} opacity={0.5} />
      {rings > 1 && (
        <polygon points="0,-28 24,14 -24,14" fill="none" stroke={s} strokeWidth={0.8} opacity={0.4} />
      )}
      <ellipse cx="0" cy="2" rx="14" ry="9" fill="none" stroke={p} strokeWidth={1.2} opacity={0.7} />
      <circle cx="0" cy="2" r="5" fill={p} opacity={0.3} />
      <circle cx="0" cy="2" r="2.5" fill={s} opacity={0.8} />
      {rings > 2 && (
        <>
          <line x1="0" y1="-38" x2="0" y2="-44" stroke={p} strokeWidth={0.8} opacity={0.4} />
          <circle cx="0" cy="-46" r="2" fill={p} opacity={0.4} />
        </>
      )}
    </g>
  );
}

// ─── Shield ───
function Shield({ p, s, rings }) {
  return (
    <g transform="translate(50,50)">
      <path d="M 0,-36 L 30,-20 L 30,8 Q 30,30 0,40 Q -30,30 -30,8 L -30,-20 Z"
        fill="none" stroke={p} strokeWidth={1.5} opacity={0.6} />
      {rings > 1 && (
        <path d="M 0,-26 L 22,-14 L 22,5 Q 22,22 0,30 Q -22,22 -22,5 L -22,-14 Z"
          fill="none" stroke={s} strokeWidth={0.8} opacity={0.4} />
      )}
      {rings > 2 && (
        <path d="M 0,-16 L 14,-8 L 14,3 Q 14,14 0,20 Q -14,14 -14,3 L -14,-8 Z"
          fill="none" stroke={p} strokeWidth={0.6} opacity={0.3} />
      )}
      <line x1="0" y1="-36" x2="0" y2="40" stroke={p} strokeWidth={0.5} opacity={0.3} />
      <line x1="-30" y1="0" x2="30" y2="0" stroke={p} strokeWidth={0.5} opacity={0.3} />
      <circle cx="0" cy="2" r="4" fill={p} opacity={0.3} />
      <circle cx="0" cy="2" r="2" fill={s} />
    </g>
  );
}

// ─── Compass ───
function Compass({ p, s, rings }) {
  return (
    <g transform="translate(50,50)">
      <circle cx="0" cy="0" r="38" fill="none" stroke={p} strokeWidth={0.8} opacity={0.3} />
      {rings > 1 && <circle cx="0" cy="0" r="30" fill="none" stroke={s} strokeWidth={0.5} opacity={0.2} />}
      {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => {
        const rad = (angle * Math.PI) / 180;
        const inner = i % 2 === 0 ? 28 : 32;
        return (
          <line key={i} x1={Math.cos(rad) * 8} y1={Math.sin(rad) * 8}
            x2={Math.cos(rad) * inner} y2={Math.sin(rad) * inner}
            stroke={i % 2 === 0 ? p : s} strokeWidth={i % 2 === 0 ? 1.2 : 0.6}
            opacity={i % 2 === 0 ? 0.7 : 0.4} />
        );
      })}
      <polygon points="0,-26 4,-4 -4,-4" fill={p} opacity={0.7} />
      <polygon points="0,26 4,4 -4,4" fill={s} opacity={0.5} />
      <circle cx="0" cy="0" r="4" fill="none" stroke={p} strokeWidth={1} opacity={0.6} />
      <circle cx="0" cy="0" r="1.5" fill={s} />
    </g>
  );
}
