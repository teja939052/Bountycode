// @ts-nocheck
import { useState, useCallback } from "react";

type PointerHandProps = {
  targetLabel?: string;
  initialTarget?: string;
  onChange?: (target: string) => void;
};

export default function PointerHand({
  targetLabel = "node",
  initialTarget = "",
  onChange,
}: PointerHandProps) {
  const [target, setTarget] = useState<string>(initialTarget);
  const [history, setHistory] = useState<string[]>([initialTarget].filter(Boolean));
  const [flash, setFlash] = useState(false);

  const moveTo = useCallback(
    (next: string) => {
      setTarget(next);
      setHistory((h) => [...h, next]);
      onChange?.(next);
      setFlash(true);
      setTimeout(() => setFlash(false), 250);
    },
    [onChange]
  );

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2">
        <span className="text-[11px] font-mono uppercase tracking-wide text-gray-400">
          Pointer
        </span>
        <span className="text-[11px] font-mono text-purple-300">👉 finger pointing</span>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <span className="text-[10px] font-mono text-gray-500">pointing at:</span>
        <span
          className={[
            "rounded-lg border px-2 py-1 text-xs font-mono transition-all",
            flash ? "border-purple-300 bg-purple-300/10 text-purple-200" : "border-white/10 bg-white/5 text-text-primary",
          ].join(" ")}
        >
          {target || "?"}
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {["head", "node-B", "node-C", "tail"].map((slot) => (
          <button
            key={slot}
            onClick={() => moveTo(slot)}
            className={[
              "rounded-lg border px-2 py-1 text-[10px] font-mono transition-all",
              target === slot
                ? "border-purple-300 bg-purple-300/10 text-purple-200"
                : "border-white/10 text-gray-300 hover:border-purple-400 hover:text-purple-200",
            ].join(" ")}
          >
            {slot}
          </button>
        ))}
      </div>

      <div className="text-[10px] font-mono text-gray-500">
        history: {" → ".join(history)}
      </div>
    </div>
  );
}
