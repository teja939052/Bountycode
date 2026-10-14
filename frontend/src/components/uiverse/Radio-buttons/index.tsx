// @ts-nocheck
import { motion } from "framer-motion";

export function CircleRadio({ selected = false, onChange }: { selected?: boolean; onChange?: () => void }) {
  return (
    <button
      onClick={onChange}
      className="flex h-5 w-5 items-center justify-center rounded-full border-2 border-brand-primary/20 bg-white transition-colors hover:border-brand-sky"
      aria-pressed={selected}
    >
      <motion.div
        className="rounded-full bg-brand-sky"
        animate={{ scale: selected ? 1 : 0 }}
        transition={{ type: "spring", stiffness: 400, damping: 20 }}
        style={{ width: 10, height: 10 }}
      />
    </button>
  );
}

export function CardRadio({ selected = false, onChange, label = "" }: { selected?: boolean; onChange?: () => void; label?: string }) {
  return (
    <button
      onClick={onChange}
      className={`flex items-center gap-3 rounded-xl border-2 px-4 py-3 transition-all ${
        selected ? "border-brand-sky bg-brand-sky/5" : "border-brand-primary/10 bg-white hover:border-brand-primary/20"
      }`}
      aria-pressed={selected}
    >
      <div className="flex h-5 w-5 items-center justify-center rounded-full border-2 border-brand-primary/20">
        <motion.div
          className="rounded-full bg-brand-sky"
          animate={{ scale: selected ? 1 : 0 }}
          transition={{ type: "spring", stiffness: 400, damping: 20 }}
          style={{ width: 10, height: 10 }}
        />
      </div>
      {label && <span className="text-sm font-medium text-text-primary">{label}</span>}
    </button>
  );
}
