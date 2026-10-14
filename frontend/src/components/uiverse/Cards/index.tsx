// @ts-nocheck
import { motion } from "framer-motion";

export function GlassCard({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      className={`rounded-2xl border border-white/20 bg-white/60 p-5 shadow-[0_4px_24px_rgba(0,0,0,0.06)] backdrop-blur-md transition-colors hover:bg-white/70 ${className}`}
    >
      {children}
    </motion.div>
  );
}

export function HoverLiftCard({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      whileHover={{ y: -6, scale: 1.01 }}
      className={`rounded-2xl border border-brand-primary/10 bg-white p-5 shadow-soft transition-colors hover:border-brand-primary/20 hover:shadow-lg ${className}`}
    >
      {children}
    </motion.div>
  );
}

export function NeonCard({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div
      className={`rounded-2xl border border-brand-sky/30 bg-gradient-to-br from-brand-sky/10 to-brand-primary/10 p-5 shadow-[0_0_20px_rgba(56,189,248,0.15)] transition-shadow hover:shadow-[0_0_28px_rgba(56,189,248,0.3)] ${className}`}
    >
      {children}
    </div>
  );
}

export function ParallaxCard({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      whileHover={{ rotateX: 4, rotateY: -4 }}
      transition={{ type: "spring", stiffness: 200, damping: 20 }}
      className={`rounded-2xl border border-brand-primary/10 bg-white p-5 shadow-soft transition-colors hover:border-brand-primary/20 ${className}`}
      style={{ transformStyle: "preserve-3d" }}
    >
      {children}
    </motion.div>
  );
}
