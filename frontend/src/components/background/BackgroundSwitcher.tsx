import { useBackground, type BackgroundTheme } from "../../contexts/BackgroundContext";

const THEME_META: Record<BackgroundTheme, { label: string; emoji: string; className: string }> = {
  ocean: {
    label: "Ocean",
    emoji: "🌊",
    className: "bg-gradient-to-br from-sky-50 via-white to-sky-100",
  },
  night: {
    label: "Night",
    emoji: "🌙",
    className: "bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900",
  },
  sunset: {
    label: "Sunset",
    emoji: "🌅",
    className: "bg-gradient-to-br from-orange-50 via-rose-50 to-amber-50",
  },
  forest: {
    label: "Forest",
    emoji: "🌲",
    className: "bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50",
  },
  auto: {
    label: "Auto",
    emoji: "🔄",
    className: "",
  },
};

export default function BackgroundSwitcher() {
  const { theme, setTheme, toggle, autoRotate, setAutoRotate } = useBackground();

  return (
    <div className="flex items-center gap-2">
      <div className="flex items-center gap-1.5 rounded-full border border-black/5 bg-white/80 p-1 shadow-sm backdrop-blur">
        {(Object.keys(THEME_META) as BackgroundTheme[]).map((key) => {
          const meta = THEME_META[key];
          const isActive = autoRotate ? key === "auto" : theme === key;
          return (
            <button
              key={key}
              onClick={() => {
                if (key === "auto") {
                  setTheme("auto");
                  return;
                }
                setAutoRotate(false);
                setTheme(key);
              }}
              className={`flex items-center gap-1 rounded-full px-2.5 py-1.5 text-xs font-semibold transition ${
                isActive
                  ? "bg-gray-900 text-white shadow"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
              aria-pressed={isActive}
              title={`${meta.label}${key === "auto" ? " (auto)" : ""}`}
            >
              <span aria-hidden="true">{meta.emoji}</span>
              <span className="hidden sm:inline">{meta.label}</span>
            </button>
          );
        })}
      </div>

      <button
        onClick={toggle}
        className="flex h-8 w-8 items-center justify-center rounded-full border border-black/5 bg-white/80 text-sm shadow-sm backdrop-blur transition hover:rotate-180"
        aria-label="Next background theme"
        title="Next theme"
      >
        🔄
      </button>
    </div>
  );
}
