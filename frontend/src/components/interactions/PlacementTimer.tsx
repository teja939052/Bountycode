// @ts-nocheck
import React from "react";

type PlacementTimerProps = {
  /** Placement-proof standard: 90 seconds. Vary only with a reason. */
  seconds?: number;
  /** Fired once when the clock hits zero so the caller can lock input. */
  onExpire?: () => void;
};

/**
 * Timed-proof countdown for PlacementBlocks. Presentation only — the block
 * owns its locked state via onExpire. Lives next to Slider.tsx because
 * timed proof is an interaction primitive, not a new system.
 */
export default function PlacementTimer({ seconds = 90, onExpire }: PlacementTimerProps) {
  const [left, setLeft] = React.useState(seconds);
  const [done, setDone] = React.useState(false);
  const fired = React.useRef(false);

  React.useEffect(() => {
    if (done) return;
    if (left <= 0) {
      setDone(true);
      if (!fired.current) {
        fired.current = true;
        onExpire?.();
      }
      return;
    }
    const t = setTimeout(() => setLeft((s) => s - 1), 1000);
    return () => clearTimeout(t);
  }, [left, done, onExpire]);

  const mm = Math.floor(Math.max(0, left) / 60);
  const ss = String(Math.max(0, left) % 60).padStart(2, "0");
  const urgent = !done && left <= 15;

  return (
    <div
      className={`flex items-center gap-2 rounded-lg border px-3 py-2 text-sm font-mono ${
        done
          ? "border-red-500/50 bg-red-500/10 text-red-400"
          : urgent
            ? "border-[#ffa116]/60 bg-[#ffa116]/10 text-[#ffa116]"
            : "border-[#2a2a2a] bg-[#0f0f0f] text-[#9a9a9a]"
      }`}
    >
      <span aria-hidden="true">⏱</span>
      <span>
        {mm}:{ss}
      </span>
      <span className="font-sans text-xs">
        {done ? "— time's up. Submit what you have." : "remaining · no hints · no scrolling back"}
      </span>
    </div>
  );
}
