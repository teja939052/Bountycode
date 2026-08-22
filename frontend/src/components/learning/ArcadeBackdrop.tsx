import { motion } from "framer-motion";
import useReducedMotion from "../../hooks/useReducedMotion";

const THEMES = {
  arcade: {
    base: "from-[#070B18] via-[#0B1632] to-[#120B23]",
    glowA: "bg-brand-sky/25",
    glowB: "bg-brand-lavender/20",
    glowC: "bg-brand-gold/20",
    grid: "opacity-[0.14]",
  },
  dojo: {
    base: "from-[#05060C] via-[#0C1120] to-[#1A0C12]",
    glowA: "bg-red-500/18",
    glowB: "bg-brand-gold/12",
    glowC: "bg-brand-sky/12",
    grid: "opacity-[0.12]",
  },
  candy: {
    base: "from-[#1A1033] via-[#1B204A] to-[#2B0F25]",
    glowA: "bg-fuchsia-400/20",
    glowB: "bg-cyan-300/18",
    glowC: "bg-lime-300/16",
    grid: "opacity-[0.10]",
  },
};

const SHAPES = [
  {
    className: "left-[5%] top-[12%] h-40 w-40 rounded-[2rem] rotate-12",
    color: "bg-white/6 border-white/10",
    motion: { y: [0, -14, 0], x: [0, 8, 0], rotate: [12, 18, 12] },
  },
  {
    className: "right-[8%] top-[18%] h-28 w-28 rounded-3xl -rotate-12",
    color: "bg-brand-sky/10 border-brand-sky/15",
    motion: { y: [0, 10, 0], x: [0, -10, 0], rotate: [-12, -20, -12] },
  },
  {
    className: "left-[18%] bottom-[16%] h-24 w-24 rounded-[1.75rem] rotate-45",
    color: "bg-brand-gold/10 border-brand-gold/15",
    motion: { y: [0, -8, 0], x: [0, 6, 0], rotate: [45, 36, 45] },
  },
  {
    className: "right-[18%] bottom-[20%] h-32 w-32 rounded-[2rem] -rotate-6",
    color: "bg-brand-lavender/10 border-brand-lavender/15",
    motion: { y: [0, -12, 0], x: [0, 10, 0], rotate: [-6, 4, -6] },
  },
];

export type ArcadeVariant = "arcade" | "dojo" | "candy";

export default function ArcadeBackdrop({ variant = "arcade", className = "" }: { variant?: ArcadeVariant; className?: string }) {
  const reduced = useReducedMotion();
  const theme = THEMES[variant] || THEMES.arcade;

  return (
    <div className={`absolute inset-0 overflow-hidden pointer-events-none ${className}`}>
      <div className={`absolute inset-0 bg-gradient-to-br ${theme.base}`} />
      <div
        className={`absolute inset-0 bg-[radial-gradient(circle_at_20%_18%,rgba(72,149,239,0.22),transparent_24%),radial-gradient(circle_at_82%_14%,rgba(124,109,175,0.18),transparent_22%),radial-gradient(circle_at_28%_82%,rgba(233,196,106,0.12),transparent_22%)]`}
      />
      <div
        className={`absolute inset-0 ${theme.grid} bg-[linear-gradient(rgba(255,255,255,0.08)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.08)_1px,transparent_1px)] bg-[size:48px_48px]`}
      />
      <div className="absolute inset-0 bg-[linear-gradient(135deg,transparent_44%,rgba(255,255,255,0.06)_45%,transparent_46%)] opacity-20" />

      <div className="absolute inset-0">
        <div className={`absolute -left-24 top-12 h-64 w-64 rounded-full ${theme.glowA} blur-3xl`} />
        <div className={`absolute -right-24 top-20 h-72 w-72 rounded-full ${theme.glowB} blur-3xl`} />
        <div className={`absolute left-1/2 bottom-0 h-64 w-64 -translate-x-1/2 rounded-full ${theme.glowC} blur-3xl`} />
      </div>

      {!reduced && (
        <div className="absolute inset-0">
          {SHAPES.map((shape, index) => (
            <motion.div
              key={shape.className}
              className={`absolute border ${shape.className} ${shape.color}`}
              animate={shape.motion}
              transition={{
                duration: 10 + index * 1.5,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              <div className="absolute inset-0 rounded-[inherit] bg-white/5" />
            </motion.div>
          ))}
        </div>
      )}

      <div className="absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-white/20 to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/25 to-transparent" />
    </div>
  );
}
