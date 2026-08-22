import { Moon } from "lucide-react";

export default function ThemeToggle() {
  return (
    <span className="inline-flex items-center justify-center rounded-xl border border-black/5 bg-white px-2.5 py-2 text-text-muted shadow-sm" title="Theme active">
      <Moon size={18} />
    </span>
  );
}
