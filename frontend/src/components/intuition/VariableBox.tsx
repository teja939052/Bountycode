// @ts-nocheck
import { useState, useCallback } from "react";

export type VariableBoxProps = {
  label?: string;
  initialValue?: string | number;
  onChange?: (value: string | number) => void;
  readOnly?: boolean;
};

export default function VariableBox({
  label = "apples",
  initialValue = "",
  onChange,
  readOnly = false,
}: VariableBoxProps) {
  const [value, setValue] = useState<string | number>(initialValue ?? "");
  const [highlight, setHighlight] = useState(false);

  const commit = useCallback(
    (next: string | number) => {
      setValue(next);
      onChange?.(next);
      setHighlight(true);
      setTimeout(() => setHighlight(false), 350);
    },
    [onChange]
  );

  const handleDrop = useCallback(
    (chip: string | number) => {
      if (readOnly) return;
      commit(chip);
    },
    [commit, readOnly]
  );

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2">
        <span className="text-[11px] font-mono uppercase tracking-wide text-gray-400">
          Variable
        </span>
        <span className="text-[11px] font-mono text-amber-300">📦 {label}</span>
      </div>

      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          const raw = e.dataTransfer.getData("text/plain");
          if (raw) {
            const num = Number(raw);
            handleDrop(Number.isNaN(num) ? raw : num);
          }
        }}
        className={[
          "relative rounded-xl border-2 bg-black/40 px-4 py-3 transition-all",
          highlight
            ? "border-emerald-400 shadow-[0_0_24px_rgba(52,211,153,0.25)]"
            : "border-white/10",
        ].join(" ")}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono text-gray-500">val =</span>
            <span className="text-sm font-black text-text-primary">{value ?? "?"}</span>
          </div>
          <span className="text-[10px] font-mono text-gray-500">
            {readOnly ? "read-only" : "drag chips here"}
          </span>
        </div>

        {!readOnly && (
          <div className="mt-3 flex items-center gap-2">
            <input
              value={value}
              onChange={(e) => {
                const raw = e.target.value;
                const num = Number(raw);
                commit(Number.isNaN(num) ? raw : num);
              }}
              className="flex-1 rounded-lg bg-white/5 px-2 py-1 text-xs text-text-primary outline-none focus:border-emerald-400"
              placeholder="Type a value"
            />
            <button
              onClick={() => {
                if (readOnly) return;
                commit(Number(value) + 1);
              }}
              className="rounded-lg border border-white/10 px-2 py-1 text-[10px] font-mono text-gray-300 hover:border-emerald-400 hover:text-emerald-300"
            >
              +1
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
