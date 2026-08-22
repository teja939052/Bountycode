import { useState, useRef, useEffect } from "react";
import { useThemeStore, ThemeMode } from "../store/themeStore";
import { Palette, Check } from "lucide-react";

const THEMES: { mode: ThemeMode; label: string; icon: string; color: string }[] = [
  { mode: "meadow", label: "Meadow", icon: "🌱", color: "#4F8F57" },
  { mode: "dark", label: "Dark", icon: "🌙", color: "#6C63FF" },
  { mode: "transparent", label: "Glass", icon: "🔮", color: "#4895EF" },
  { mode: "blue", label: "Ocean", icon: "🌊", color: "#4895EF" },
  { mode: "emerald", label: "Forest", icon: "🌿", color: "#2A9D8F" },
  { mode: "sunset", label: "Ember", icon: "🔥", color: "#F4A261" },
];

export default function ThemeSwitcher() {
  const { mode, setMode } = useThemeStore();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const current = THEMES.find((t) => t.mode === mode) ?? THEMES[0];

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-2 rounded-xl bg-surface-card border border-brand-primary/20 text-brand-secondary hover:text-brand-primary hover:border-brand-primary/40 transition-all text-xs font-mono"
        aria-label="Switch theme"
      >
        <Palette size={16} />
        <span>{current.label}</span>
      </button>
      {open && (
        <div className="absolute right-0 top-full mt-2 w-52 rounded-2xl bg-surface-card border border-brand-primary/20 shadow-xl shadow-brand-primary/10 p-2 z-50">
          {THEMES.map((t) => (
            <button
              key={t.mode}
              onClick={() => { setMode(t.mode); setOpen(false); }}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-mono transition-all ${
                mode === t.mode
                  ? "bg-brand-primary/20 text-brand-primary"
                  : "text-brand-secondary hover:bg-brand-primary/10 hover:text-brand-primary"
              }`}
            >
              <span className="text-lg">{t.icon}</span>
              <span className="flex-1 text-left">{t.label}</span>
              {mode === t.mode && <Check size={14} className="text-brand-primary" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
