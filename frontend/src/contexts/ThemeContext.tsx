import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

interface Theme {
  id: string;
  label: string;
  accent: string;
}

interface ThemeCtx {
  theme: string;
  setTheme: (t: string) => void;
  themes: Theme[];
}

const ThemeContext = createContext<ThemeCtx | null>(null);

const THEMES: Theme[] = [
  { id: "cyber", label: "Cyber", accent: "from-cyber-blue to-cyber-purple" },
  { id: "aurora", label: "Aurora", accent: "from-cyber-green to-pink-500" },
  { id: "ember", label: "Ember", accent: "from-cyber-amber to-cyber-red" },
];

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "cyber");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    const vibe = localStorage.getItem("vibe") || "learn";
    document.documentElement.setAttribute("data-vibe", vibe);
  }, [theme]);

  const value: ThemeCtx = { theme, setTheme, themes: THEMES };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeCtx {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}
