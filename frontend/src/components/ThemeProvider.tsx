import { useEffect } from "react";
import { useThemeStore, getThemeVars } from "../store/themeStore";

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const { mode } = useThemeStore();

  useEffect(() => {
    const root = document.documentElement;
    // Single bright theme: ignore any persisted dark/night mode.
    root.classList.remove("dark");
    root.setAttribute("data-theme", "light");
    root.style.colorScheme = "light";
    const vars = getThemeVars(mode);
    Object.entries(vars).forEach(([key, value]) => root.style.setProperty(key, value));
  }, [mode]);

  return <>{children}</>;
}
