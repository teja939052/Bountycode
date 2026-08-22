import { useEffect } from "react";
import { useThemeStore, getThemeVars } from "../store/themeStore";

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const { mode } = useThemeStore();

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute("data-theme", mode);
    const vars = getThemeVars(mode);
    Object.entries(vars).forEach(([key, value]) => root.style.setProperty(key, value));
  }, [mode]);

  return <>{children}</>;
}
