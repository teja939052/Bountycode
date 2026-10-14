// @ts-nocheck
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";

interface GradientButtonProps {
  label?: string;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}

export function GradientButton({
  label = "Launch",
  onClick,
  disabled = false,
  className = "",
}: GradientButtonProps) {
  return (
    <motion.button
      whileHover={{ scale: 1.04 }}
      whileTap={{ scale: 0.96 }}
      onClick={onClick}
      disabled={disabled}
      className={`relative overflow-hidden rounded-full bg-gradient-to-r from-brand-sky via-brand-primary to-brand-sky bg-[length:200%_100%] px-6 py-3 text-sm font-bold text-white shadow-sm transition-colors hover:opacity-90 disabled:opacity-50 ${className}`}
    >
      <span className="relative z-10">{label}</span>
    </motion.button>
  );
}

export function GlowButton({
  label = "Activate",
  onClick,
  className = "",
}: GradientButtonProps) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={`relative rounded-full bg-brand-sky px-6 py-3 text-sm font-bold text-white shadow-[0_0_20px_rgba(56,189,248,0.35)] transition-shadow hover:shadow-[0_0_28px_rgba(56,189,248,0.55)] ${className}`}
    >
      {label}
    </motion.button>
  );
}

export function BrutalistButton({
  label = "Submit",
  onClick,
  className = "",
}: GradientButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`rounded-xl border-2 border-black bg-white px-6 py-3 text-sm font-bold text-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none ${className}`}
    >
      {label}
    </button>
  );
}

export function RippleButton({
  label = "Ripple",
  onClick,
  className = "",
}: GradientButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`relative overflow-hidden rounded-xl bg-brand-primary px-6 py-3 text-sm font-bold text-white transition-colors hover:bg-brand-primary/90 ${className}`}
    >
      {label}
    </button>
  );
}
