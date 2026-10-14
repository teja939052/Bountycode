// @ts-nocheck
import { useState, useCallback } from "react";

type LoopCounterProps = {
  limit?: number;
  onComplete?: (count: number) => void;
};

export default function LoopCounter({ limit = 5, onComplete }: LoopCounterProps) {
  const [count, setCount] = useState(0);
  const [running, setRunning] = useState(false);
  const [flash, setFlash] = useState(false);

  const step = useCallback(() => {
    setCount((c) => {
      const next = c + 1;
      setFlash(true);
      setTimeout(() => setFlash(false), 200);
      if (next >= limit) {
        setRunning(false);
        onComplete?.(next);
      }
      return next;
    });
  }, [limit, onComplete]);

  const reset = useCallback(() => {
    setCount(0);
    setRunning(false);
  }, []);

  const start = useCallback(() => {
    setRunning(true);
  }, []);

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2">
        <span className="text-[11px] font-mono uppercase tracking-wide text-gray-400">
          Loop
        </span>
        <span className="text-[11px] font-mono text-amber-300">
          🔄 while bucket isn’t full
        </span>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border-2 border-white/10 bg-black/40 text-lg font-black text-text-primary">
          {count}
        </div>
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border-2 border-white/10 bg-black/40 text-[10px] font-mono text-gray-500">
          / {limit}
        </div>
        <span className="text-[10px] font-mono text-gray-500">
          {count >= limit ? "done" : running ? "running" : "idle"}
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {!running ? (
          <button
            onClick={start}
            disabled={count >= limit}
            className="rounded-lg border border-emerald-400/40 px-3 py-1.5 text-[10px] font-mono text-emerald-300 hover:bg-emerald-400/10 disabled:opacity-40"
          >
            start loop
          </button>
        ) : (
          <button
            onClick={step}
            className="rounded-lg border border-amber-400/40 px-3 py-1.5 text-[10px] font-mono text-amber-300 hover:bg-amber-400/10"
          >
            step once
          </button>
        )}
        <button
          onClick={reset}
          className="rounded-lg border border-white/10 px-3 py-1.5 text-[10px] font-mono text-gray-300 hover:border-rose-400 hover:text-rose-300"
        >
          reset
        </button>
      </div>

      <div
        className={[
          "text-[10px] font-mono text-gray-400 transition-all",
          flash ? "text-emerald-300" : "",
        ].join(" ")}
      >
        {count >= limit
          ? "bucket full — loop stops"
          : "bucket not full yet — loop continues"}
      </div>
    </div>
  );
}
