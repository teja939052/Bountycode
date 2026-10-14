// @ts-nocheck
import { useState, useCallback } from "react";

type QueueLineProps = {
  initialItems?: (string | number)[];
  onChange?: (items: (string | number)[]) => void;
};

export default function QueueLine({ initialItems = [], onChange }: QueueLineProps) {
  const [items, setItems] = useState<(string | number)[]>(initialItems);
  const [incoming, setIncoming] = useState<string>("");
  const [highlight, setHighlight] = useState<string | null>(null);

  const emit = useCallback(
    (next: (string | number)[]) => {
      setItems(next);
      onChange?.(next);
    },
    [onChange]
  );

  const enqueue = useCallback(() => {
    if (!incoming.trim()) return;
    const raw = incoming.trim();
    const num = Number(raw);
    const item = Number.isNaN(num) ? raw : num;
    setIncoming("");
    setHighlight(`joined-${item}`);
    setTimeout(() => setHighlight(null), 400);
    emit([...items, item]);
  }, [incoming, items, emit]);

  const dequeue = useCallback(() => {
    if (!items.length) return;
    const [first, ...rest] = items;
    setHighlight(`left-${first}`);
    setTimeout(() => setHighlight(null), 400);
    emit(rest);
  }, [items, emit]);

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2">
        <span className="text-[11px] font-mono uppercase tracking-wide text-gray-400">
          Queue
        </span>
        <span className="text-[11px] font-mono text-sky-300">🚶 First in, first out</span>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {items.length === 0 && (
          <span className="text-xs text-gray-500">Empty line — no one is waiting</span>
        )}
        {items.map((item, idx) => (
          <span
            key={`${item}-${idx}`}
            className={[
              "rounded-lg border px-2 py-1 text-xs font-mono transition-all",
              highlight === `left-${item}`
                ? "border-rose-300 bg-rose-300/10 text-rose-200"
                : "border-white/10 bg-white/5 text-text-primary",
            ].join(" ")}
          >
            {item}
          </span>
        ))}
      </div>

      <div className="flex items-center gap-2">
        <input
          value={incoming}
          onChange={(e) => setIncoming(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") enqueue();
          }}
          className="flex-1 rounded-lg bg-white/5 px-2 py-1 text-xs text-text-primary outline-none focus:border-sky-400"
          placeholder="New person joins..."
        />
        <button
          onClick={enqueue}
          className="rounded-lg border border-white/10 px-2 py-1 text-[10px] font-mono text-gray-300 hover:border-sky-400 hover:text-sky-300"
        >
          Enqueue
        </button>
        <button
          onClick={dequeue}
          disabled={!items.length}
          className="rounded-lg border border-white/10 px-2 py-1 text-[10px] font-mono text-gray-300 hover:border-rose-400 hover:text-rose-300 disabled:opacity-40"
        >
          Dequeue
        </button>
      </div>
    </div>
  );
}
