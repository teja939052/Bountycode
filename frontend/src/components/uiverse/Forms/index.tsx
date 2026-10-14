// @ts-nocheck
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export function NeonInput({
  label = "Username",
  className = "",
}: {
  label?: string;
  className?: string;
}) {
  const [value, setValue] = useState("");
  return (
    <div className={`${className}`}>
      <label className="mb-1 block text-xs font-medium text-text-secondary">
        {label}
      </label>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full rounded-xl border border-brand-sky/30 bg-surface-base px-4 py-2.5 text-sm text-text-primary shadow-[0_0_8px_rgba(56,189,248,0.25)] outline-none transition-all focus:border-brand-sky focus:shadow-[0_0_14px_rgba(56,189,248,0.45)]"
      />
    </div>
  );
}

export function SearchInput({
  placeholder = "Search...",
  className = "",
}: {
  placeholder?: string;
  className?: string;
}) {
  const [value, setValue] = useState("");
  return (
    <div className={`relative ${className}`}>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-xl border border-brand-primary/10 bg-surface-base px-4 py-2.5 pl-10 text-sm text-text-primary outline-none transition-colors focus:border-brand-sky focus:ring-2 focus:ring-brand-sky/20"
      />
      <span className="absolute left-3 top-2.5 text-text-secondary">🔍</span>
    </div>
  );
}

export function PasswordInput({
  label = "Password",
  className = "",
}: {
  label?: string;
  className?: string;
}) {
  const [value, setValue] = useState("");
  const [visible, setVisible] = useState(false);
  return (
    <div className={`${className}`}>
      <label className="mb-1 block text-xs font-medium text-text-secondary">
        {label}
      </label>
      <div className="relative">
        <input
          type={visible ? "text" : "password"}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="w-full rounded-xl border border-brand-primary/10 bg-surface-base px-4 py-2.5 pr-10 text-sm text-text-primary outline-none transition-colors focus:border-brand-sky focus:ring-2 focus:ring-brand-sky/20"
        />
        <button
          type="button"
          onClick={() => setVisible((v) => !v)}
          className="absolute right-3 top-2.5 text-xs text-text-secondary"
        >
          {visible ? "Hide" : "Show"}
        </button>
      </div>
    </div>
  );
}
