// @ts-nocheck
import { motion } from "framer-motion";

export function CheckmarkCheckbox({ checked = false, onChange }: { checked?: boolean; onChange?: (v: boolean) => void }) {
  return (
    <button
      onClick={() => onChange?.(!checked)}
      className="flex h-6 w-6 items-center justify-center rounded-md border-2 border-brand-primary/20 bg-white transition-colors hover:border-brand-sky"
      aria-pressed={checked}
    >
      <motion.svg
        width="14"
        height="14"
        viewBox="0 0 14 14"
        animate={{ scale: checked ? 1 : 0, opacity: checked ? 1 : 0 }}
        transition={{ type: "spring", stiffness: 400, damping: 20 }}
      >
        <path d="M2 7L5.5 10.5L12 3.5" stroke="#38bdf8" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </motion.svg>
    </button>
  );
}

export function GradientCheckbox({ checked = false, onChange }: { checked?: boolean; onChange?: (v: boolean) => void }) {
  return (
    <button
      onClick={() => onChange?.(!checked)}
      className="flex h-6 w-6 items-center justify-center rounded-md border-2 border-brand-sky/40 bg-white transition-all"
      aria-pressed={checked}
    >
      <motion.div
        className="h-full w-full rounded-md"
        animate={{ backgroundColor: checked ? "#38bdf8" : "transparent" }}
        transition={{ duration: 0.2 }}
      />
      {checked && (
        <motion.svg
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="absolute"
          width="14"
          height="14"
          viewBox="0 0 14 14"
        >
          <path d="M2 7L5.5 10.5L12 3.5" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </motion.svg>
      )}
    </button>
  );
}

export function SquareCheckbox({ checked = false, onChange, label = "" }: { checked?: boolean; onChange?: (v: boolean) => void; label?: string }) {
  return (
    <label className="flex items-center gap-2 cursor-pointer">
      <button
        type="button"
        onClick={() => onChange?.(!checked)}
        className={`flex h-5 w-5 items-center justify-center rounded border-2 transition-colors ${
          checked ? "border-brand-sky bg-brand-sky" : "border-brand-primary/20 bg-white"
        }`}
        aria-pressed={checked}
      >
        {checked && (
          <motion.svg initial={{ scale: 0 }} animate={{ scale: 1 }} width="12" height="12" viewBox="0 0 12 12">
            <path d="M2 6L5 9L10 3" stroke="white" strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </motion.svg>
        )}
      </button>
      {label && <span className="text-sm text-text-primary">{label}</span>}
    </label>
  );
}
