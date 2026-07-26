import { Moon } from "lucide-react";

export default function ThemeToggle() {
  return (
    <span className="p-2 rounded-lg bg-space-panel text-gray-500 border border-space-border" title="Space theme active">
      <Moon size={18} />
    </span>
  );
}
