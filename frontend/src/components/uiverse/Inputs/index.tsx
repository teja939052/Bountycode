// @ts-nocheck
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export function FloatingLabelInput({
  label = "Email",
  type = "text",
  className = "",
}: {
  label?: string;
  type?: string;
  className?: string;
}) {
  const [value, setValue] = useState("");
  const [focused, setFocused] = useState(false);

  return (
    <div className={`relative ${className}`}>
      <input
        type={type}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        className="peer w-full rounded-xl border border-brand-primary/10 bg-surface-base px-4 pt-5 pb-2 text-sm text-text-primary outline-none transition-colors focus:border-brand-sky focus:ring-2 focus:ring-brand-sky/20"
      />
      <motion.label
        className="pointer-events-none absolute left-4 text-xs text-text-secondary"
        animate={{
          y: focused || value ? -2 : 16,
          scale: focused || value ? 0.85 : 1,
        }}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
      >
        {label}
      </motion.label>
    </div>
  );
}

export function UnderlineInput({
  label = "Username",
  className = "",
}: {
  label?: string;
  className?: string;
}) {
  const [value, setValue] = useState("");
  return (
    <div className={`relative ${className}`}>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full border-b-2 border-brand-primary/10 bg-transparent px-1 py-2 text-sm text-text-primary outline-none transition-colors focus:border-brand-sky"
      />
      <span className="absolute -top-2 left-1 text-[10px] text-text-secondary">{label}</span>
    </div>
  );
}

export function BrutalistInput({
  label = "Search",
  className = "",
}: {
  label?: string;
  className?: string;
}) {
  return (
    <div className={`${className}`}>
      <label className="mb-1 block text-xs font-bold uppercase tracking-widest text-text-primary">{label}</label>
      <input
        type="text"
        className="w-full rounded-none border-2 border-black bg-white px-4 py-3 text-sm text-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] focus:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] focus:outline-none"
      />
    </div>
  );
}
