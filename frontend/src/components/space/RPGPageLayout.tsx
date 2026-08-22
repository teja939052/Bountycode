import { motion } from "framer-motion";
import useReducedMotion from "../../hooks/useReducedMotion";

const GRID_VARIANTS = ["hex", "dots", "crosshatch", "lines"];

export default function RPGPageLayout({
  children,
  theme = "dark",
  gridVariant = "dots",
  showParticles = true,
  showGrid = true,
  gradient = "from-emerald-50 via-amber-50 to-sky-50",
  className = "",
}) {
  const reduced = useReducedMotion();

  const gridStyles = {
    hex: "radial-gradient(circle at 50% 0%, rgba(99,102,241,0.06) 0%, transparent 1px)",
    dots: "radial-gradient(rgba(255,255,255,0.04) 1px, transparent 1px)",
    crosshatch: `linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                 linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)`,
    lines: "linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px)",
  };

  return (
    <div className={`relative min-h-screen bg-[color:var(--bg-base,#f6f3ea)] ${className}`}>
      {/* Background layer */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
        <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-90`} />

        {/* Grid overlay */}
        {showGrid && (
          <div
            className="absolute inset-0 opacity-35"
            style={{
              backgroundImage: gridStyles[gridVariant] || gridStyles.dots,
              backgroundSize: gridVariant === "hex" ? "48px 48px" : "32px 32px",
            }}
          />
        )}

        {/* Animated glow orbs */}
        {!reduced && (
          <>
            <motion.div
              className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-emerald-400/10 blur-3xl"
              animate={{ scale: [1, 1.05, 1], opacity: [0.2, 0.35, 0.2] }}
              transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
            />
            <motion.div
              className="absolute top-1/3 -right-32 w-80 h-80 rounded-full bg-sky-400/8 blur-3xl"
              animate={{ scale: [1, 0.95, 1], opacity: [0.15, 0.28, 0.15] }}
              transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 1 }}
            />
            <motion.div
              className="absolute -bottom-32 left-1/3 w-96 h-96 rounded-full bg-amber-300/10 blur-3xl"
              animate={{ y: [0, -12, 0], opacity: [0.12, 0.22, 0.12] }}
              transition={{ duration: 12, repeat: Infinity, ease: "easeInOut", delay: 2 }}
            />

            {/* Floating pixel particles */}
            {showParticles && (
              <div className="absolute inset-0">
                {Array.from({ length: 12 }).map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-1 h-1 bg-emerald-500/25 rounded-sm"
                    style={{
                      left: `${8 + (i * 7) % 85}%`,
                      top: `${12 + (i * 13) % 75}%`,
                    }}
                    animate={{
                      y: [0, -30 - (i * 5) % 20, 0],
                      opacity: [0, 0.8, 0],
                    }}
                    transition={{
                      duration: 3 + (i % 4),
                      repeat: Infinity,
                      delay: i * 0.7,
                      ease: "easeInOut",
                    }}
                  />
                ))}
              </div>
            )}
          </>
        )}

        {/* Scanline overlay for retro feel */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(15,23,42,0.03) 2px, rgba(15,23,42,0.03) 4px)",
          }}
        />
      </div>

      {/* Content layer */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
}
