import { motion } from "framer-motion";
import { Crown, Lock, Play, Star } from "lucide-react";
import type { Ref } from "react";
import { CANDY, candyRadial } from "./palette";
import type { CandyColor } from "./palette";

export type CandyNodeState = "completed" | "current" | "open" | "locked";

type Props = {
  color?: CandyColor;
  emoji?: string;
  number: number;
  state?: CandyNodeState;
  onClick?: () => void;
  size?: number;
  className?: string;
  stars?: number;
  milestone?: boolean;
  innerRef?: Ref<HTMLDivElement>;
};

export default function CandyNode({
  color = "strawberry",
  emoji,
  number,
  state = "open",
  onClick,
  size,
  className = "",
  stars = 3,
  milestone = false,
  innerRef,
}: Props) {
  const locked = state === "locked";
  const completed = state === "completed";
  const current = state === "current";
  const c = CANDY[color];

  const body = (
    <motion.div
      ref={innerRef}
      whileHover={locked ? undefined : { scale: 1.08 }}
      whileTap={locked ? undefined : { scale: 0.94 }}
      onClick={locked ? undefined : onClick}
      className={`relative flex select-none items-center justify-center rounded-full ${
        locked ? "cursor-not-allowed" : "cursor-pointer"
      } ${className}`}
      style={{
        ...(size ? { width: size, height: size } : {}),
        background: locked
          ? "radial-gradient(circle at 32% 28%, #3a3a4d, #232331)"
          : candyRadial(color),
        border: completed
          ? "3px solid rgba(255, 215, 0, 0.9)"
          : milestone
          ? "3px solid rgba(255, 215, 0, 0.55)"
          : "3px solid rgba(255, 255, 255, 0.28)",
        boxShadow: locked
          ? "inset 0 -6px 14px rgba(0,0,0,0.45), 0 6px 14px rgba(0,0,0,0.35)"
          : `0 12px 26px -6px ${c.base}66, inset 0 -6px 14px ${c.dark}66, inset 0 3px 6px rgba(255,255,255,0.55)`,
      }}
    >
      <span className="pointer-events-none absolute inset-x-1 top-1 h-1/2 rounded-full candy-gloss-strong" />
      <span className="relative z-10 text-[26px] leading-none drop-shadow-md">
        {locked ? (
          <Lock
            size={size ? Math.max(18, Math.round(size * 0.28)) : 22}
            className="mx-auto text-text-primary/50"
          />
        ) : (
          emoji ?? number
        )}
      </span>
      <span
        className={`absolute -left-1 -top-1 z-20 flex h-6 w-6 items-center justify-center rounded-full border text-[11px] font-black shadow-md ${
          locked
            ? "border-white/10 bg-[#232331] text-text-primary/40"
            : "border-white/60 bg-white text-[#1a1a24]"
        }`}
      >
        {number}
      </span>
      {completed && (
        <span className="absolute -right-2 -top-2 z-20 flex gap-0.5">
          {Array.from({ length: Math.max(1, Math.min(3, stars)) }).map(
            (_s, i) => (
              <Star
                key={i}
                size={12}
                className="fill-amber-400 text-amber-400 drop-shadow"
              />
            )
          )}
        </span>
      )}
      {milestone && !locked && (
        <span className="absolute -bottom-1 -right-1 z-20 flex h-6 w-6 items-center justify-center rounded-full bg-amber-400 shadow-md ring-2 ring-white/80">
          <Crown size={13} className="text-amber-900" />
        </span>
      )}
      {current && (
        <span className="absolute -bottom-8 left-1/2 z-20 flex -translate-x-1/2 items-center gap-1 whitespace-nowrap rounded-full bg-gradient-to-r from-rose-500 to-amber-400 px-3 py-1 text-[10px] font-black uppercase tracking-widest text-text-primary shadow-xl ring-2 ring-white/40">
          <Play size={10} className="fill-white" /> Play
        </span>
      )}
    </motion.div>
  );

  if (current) {
    return (
      <motion.div
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}
        className="relative"
      >
        <div className="absolute -inset-2 animate-pulse rounded-full bg-white border-border/15 blur-md" />
        <div className="candy-spin absolute -inset-[7px] rounded-full border-2 border-dashed border-white/30" />
        {body}
      </motion.div>
    );
  }

  return body;
}
