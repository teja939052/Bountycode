// @ts-nocheck
import { motion } from "framer-motion";

export function PillToggle({ checked = false, onChange, label = "" }: { checked?: boolean; onChange?: (v: boolean) => void; label?: string }) {
  return (
    <button
      onClick={() => onChange?.(!checked)}
      className={`relative inline-flex h-8 w-14 items-center rounded-full p-1 transition-colors ${
        checked ? "bg-brand-sky" : "bg-black/10"
      }`}
      aria-pressed={checked}
    >
      <motion.div
        className="h-6 w-6 rounded-full bg-white shadow-sm"
        animate={{ x: checked ? 24 : 0 }}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
      />
      {label && <span className="ml-3 text-sm text-text-primary">{label}</span>}
    </button>
  );
}

export function IOSSwitch({ checked = false, onChange }: { checked?: boolean; onChange?: (v: boolean) => void }) {
  return (
    <button
      onClick={() => onChange?.(!checked)}
      className={`relative inline-flex h-8 w-14 items-center rounded-full p-1 transition-colors ${
        checked ? "bg-emerald-500" : "bg-black/10"
      }`}
      aria-pressed={checked}
    >
      <motion.div
        className="h-6 w-6 rounded-full bg-white shadow-md"
        animate={{ x: checked ? 24 : 0 }}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
      />
    </button>
  );
}

export function NeumorphicToggle({ checked = false, onChange }: { checked?: boolean; onChange?: (v: boolean) => void }) {
  return (
    <button
      onClick={() => onChange?.(!checked)}
      className={`relative inline-flex h-10 w-20 items-center rounded-full p-1.5 transition-all ${
        checked ? "bg-brand-sky" : "bg-[#e6e6e6]"
      }`}
      style={{
        boxShadow: checked
          ? "inset 0 2px 4px rgba(0,0,0,0.2)"
          : "6px 6px 12px #b8b8b8, -6px -6px 12px #ffffff",
      }}
      aria-pressed={checked}
    >
      <motion.div
        className="h-7 w-7 rounded-full bg-white"
        animate={{ x: checked ? 40 : 0 }}
        transition={{ type: "spring", stiffness: 300, damping: 25 }}
      />
    </button>
  );
}
