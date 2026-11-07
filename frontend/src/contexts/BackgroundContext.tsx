import { createContext, useContext, useEffect, useMemo, useState } from "react";

export type BackgroundTheme = "ocean" | "night" | "sunset" | "forest" | "auto";

export interface BackgroundContextValue {
  theme: BackgroundTheme;
  resolved: BackgroundTheme;
  setTheme: (theme: BackgroundTheme) => void;
  toggle: () => void;
  autoRotate: boolean;
  setAutoRotate: (value: boolean) => void;
}

const BackgroundContext = createContext<BackgroundContextValue | undefined>(undefined);

const STORAGE_KEY = "bc_background_theme";
const AUTO_KEY = "bc_background_auto";

const THEME_ORDER: BackgroundTheme[] = ["ocean", "night", "sunset", "forest"];

export function BackgroundProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<BackgroundTheme>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY) as BackgroundTheme | null;
      if (stored && THEME_ORDER.includes(stored)) return stored;
    } catch {}
    return "ocean";
  });

  const [autoRotate, setAutoRotateState] = useState<boolean>(() => {
    try {
      const stored = localStorage.getItem(AUTO_KEY);
      return stored === "1";
    } catch {
      return false;
    }
  });

  const resolved = useMemo<BackgroundTheme>(() => {
    if (theme !== "auto") return theme;
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) return "sunset";
    if (hour >= 12 && hour < 17) return "ocean";
    if (hour >= 17 && hour < 20) return "sunset";
    return "night";
  }, [theme]);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch {}
  }, [theme]);

  useEffect(() => {
    try {
      localStorage.setItem(AUTO_KEY, autoRotate ? "1" : "0");
    } catch {}
  }, [autoRotate]);

  const setTheme = (value: BackgroundTheme) => setThemeState(value);

  const toggle = () => {
    setThemeState((prev) => {
      if (prev === "auto") {
        const currentIndex = THEME_ORDER.indexOf(resolved);
        return THEME_ORDER[(currentIndex + 1) % THEME_ORDER.length];
      }
      const currentIndex = THEME_ORDER.indexOf(prev);
      return THEME_ORDER[(currentIndex + 1) % THEME_ORDER.length];
    });
  };

  const setAutoRotate = (value: boolean) => setAutoRotateState(value);

  useEffect(() => {
    if (!autoRotate) return;
    const interval = setInterval(() => {
      setThemeState((prev) => {
        if (prev === "auto") return prev;
        const currentIndex = THEME_ORDER.indexOf(prev);
        return THEME_ORDER[(currentIndex + 1) % THEME_ORDER.length];
      });
    }, 30000);
    return () => clearInterval(interval);
  }, [autoRotate]);

  return (
    <BackgroundContext.Provider value={{ theme, resolved, setTheme, toggle, autoRotate, setAutoRotate }}>
      {children}
    </BackgroundContext.Provider>
  );
}

export function useBackground() {
  const ctx = useContext(BackgroundContext);
  if (!ctx) throw new Error("useBackground must be used within BackgroundProvider");
  return ctx;
}
