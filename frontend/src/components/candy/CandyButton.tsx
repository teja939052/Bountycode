import { motion } from "framer-motion";
import type { ReactNode } from "react";
import { candyGradient, candyGlow } from "./palette";
import type { CandyColor } from "./palette";

type Props = {
  color?: CandyColor;
  size?: "sm" | "md" | "lg";
  onClick?: () => void;
  className?: string;
  children: ReactNode;
  gloss?: boolean;
  disabled?: boolean;
  shine?: boolean;
  icon?: ReactNode;
};

export default function CandyButton({
  color = "strawberry",
  size = "md",
  onClick,
  className = "",
  children,
  gloss = true,
  disabled = false,
  shine = false,
  icon,
}: Props) {
  const sizes: Record<string, string> = {
    sm: "px-4 py-2 text-xs rounded-xl",
    md: "px-6 py-3 text-sm rounded-2xl",
    lg: "px-8 py-4 text-base rounded-2xl",
  };

  return (
    <motion.button
      whileHover={disabled ? undefined : { scale: 1.05, y: -2 }}
      whileTap={disabled ? undefined : { scale: 0.95 }}
      onClick={onClick}
      disabled={disabled}
      className={`candy-btn relative inline-flex items-center justify-center gap-2 overflow-hidden font-bold text-text-primary shadow-lg ${sizes[size]} ${
        disabled ? "cursor-not-allowed opacity-50" : "cursor-pointer"
      } ${className}`}
      style={{
        background: candyGradient(color),
        boxShadow: disabled ? undefined : candyGlow(color, "55"),
      }}
    >
      {gloss && (
        <span className="pointer-events-none absolute inset-0 candy-gloss" />
      )}
      {shine && (
        <span className="pointer-events-none absolute inset-y-0 left-0 z-10 w-1/3 -skew-x-12 bg-gradient-to-r from-transparent via-white/30 to-transparent opacity-0 transition-all duration-700 group-hover:translate-x-[320%] group-hover:opacity-100" />
      )}
      <span className="relative z-10 flex items-center justify-center gap-2">
        {icon && <span className="flex-shrink-0">{icon}</span>}
        {children}
      </span>
    </motion.button>
  );
}
