import { motion } from "framer-motion";
import type { ReactNode } from "react";
import { candyGradient, candyGlow } from "./palette";
import type { CandyColor } from "./palette";

type Props = {
  color?: CandyColor;
  className?: string;
  contentClassName?: string;
  children: ReactNode;
  onClick?: () => void;
  gloss?: boolean;
  glow?: boolean;
  hover?: boolean;
  shine?: boolean;
};

export default function CandyCard({
  color = "strawberry",
  className = "",
  contentClassName = "",
  children,
  onClick,
  gloss = true,
  glow = true,
  hover = true,
  shine = false,
}: Props) {
  return (
    <motion.div
      onClick={onClick}
      whileHover={hover ? { scale: 1.02, y: -4 } : undefined}
      className={`group relative overflow-hidden rounded-3xl ${className}`}
      style={{
        background: candyGradient(color),
        boxShadow: glow ? candyGlow(color) : undefined,
      }}
    >
      {gloss && (
        <span className="pointer-events-none absolute inset-0 candy-gloss" />
      )}
      {shine && (
        <span className="pointer-events-none absolute inset-y-0 left-0 z-10 w-1/3 -skew-x-12 bg-gradient-to-r from-transparent via-white/30 to-transparent opacity-0 transition-all duration-700 group-hover:translate-x-[320%] group-hover:opacity-100" />
      )}
      <div className={`relative z-10 ${contentClassName}`}>{children}</div>
    </motion.div>
  );
}
