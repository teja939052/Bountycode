// @ts-nocheck
import { useState, useCallback } from "react";

type StackPlatesProps = {
  initialItems?: (string | number)[];
  onChange?: (items: (string | number)[]) => void;
};

export default function StackPlates({ initialItems = [], onChange }: StackPlatesProps) {
  const [stack, setStack] = useState<(string | number)[]>(initialItems);
  const [incoming, setIncoming] = useState("");
  const [flash, setFlash] = useState<string | null>(null);

  const emit = useCallback(
    (next: (string | number)[]) => {
      setStack(next);
      onChange?.(next);
    },
    [onChange]
  );

  const push = useCallback(() => {
    if (!incoming.trim()) return;
    const raw = incoming.trim();
    const num = Number(raw);
    const item = Number.isNaN(num) ? raw : num;
    setIncoming("");
    setFlash(`push-${item}`);
    setTimeout(() => setFlash(null), 350);
    emit([...stack, item]);
  }, [incoming, stack, emit]);

  const pop = useCallback(() => {
    if (!stack.length) return;
    const [top, ...rest] = stack;
    setFlash(`pop-${top}`);
    setTimeout(() => setFlash(null), 350);
    emit(rest);
  }, [stack, emit]);

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2">
        <span className="text-[11px] font-mono uppercase tracking-wide text-gray-400">
          Stack
        </span>
        <span className="text-[11px] font-mono text-amber-300">🧱 last in, first out</span>
      </div>

      <div className="flex flex-col-reverse items-center gap-1">
        {stack.length === 0 && (
          <span className="text-xs text-gray-500">Empty tower — no plates</span>
        )}
        {stack.map((plate, idx) => (
          <span
            key={`${plate}-${idx}`}
            className={[
              "min-w-[3rem] rounded-lg border px-2 py-1 text-center text-xs font-mono transition-all",
              flash === `pop-${plate}`
                ? "border-rose-300 bg-rose-300/10 text-rose-200"
                : "border-white/10 bg-white/5 text-text-primary",
            ].join(" ")}
          >
            {plate}
          </span>
        ))}
      </div>

      <div className="flex items-center gap-2">
        <input
          value={incoming}
          onChange={(e) => setIncoming(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") push();
          }}
          className="flex-1 rounded-lg bg-white/5 px-2 py-1 text-xs text-text-primary outline-none focus:border-amber-400"
          placeholder="New plate..."
        />
        <button
          onClick={push}
          className="rounded-lg border border-white/10 px-2 py-1 text-[10px] font-mono text-gray-300 hover:border-emerald-400 hover:text-emerald-300"
        >
          push
        </button>
        <button
          onClick={pop}
          disabled={!stack.length}
          className="rounded-lg border border-white/10 px-2 py-1 text-[10px] font-mono text-gray-300 hover:border-rose-400 hover:text-rose-300 disabled:opacity-40"
        >
          pop
        </button>
      </div>
    </div>
  );
}
