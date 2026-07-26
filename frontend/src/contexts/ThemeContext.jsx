import { createContext, useContext, useEffect, useState } from "react";

const ThemeContext = createContext();

const THEMES = [
  { id: "cyber", label: "Cyber", accent: "from-cyber-blue to-cyber-purple" },
  { id: "aurora", label: "Aurora", accent: "from-cyber-green to-pink-500" },
  { id: "ember", label: "Ember", accent: "from-cyber-amber to-cyber-red" },
];

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "cyber");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const value = { theme, setTheme, themes: THEMES };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}
