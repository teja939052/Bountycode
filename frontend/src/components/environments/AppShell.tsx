// @ts-nocheck
import { Outlet, NavLink, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { Compass, FlaskConical, Swords, ClipboardList, Briefcase } from "lucide-react";

const ENV_ITEMS = [
  { to: "/world", label: "World", icon: Compass, end: true },
  { to: "/lab", label: "Lab", icon: FlaskConical },
  { to: "/arena", label: "Arena", icon: Swords },
  { to: "/command", label: "Command", icon: ClipboardList },
  { to: "/career", label: "Career", icon: Briefcase },
];

export default function AppShell() {
  const location = useLocation();
  const activeEnv = ENV_ITEMS.find((item) => location.pathname === item.to || location.pathname.startsWith(item.to + "/"));

  return (
    <div className="mx-auto max-w-6xl px-4 py-6">
      <div className="mb-6 flex flex-wrap items-center gap-2">
        {ENV_ITEMS.map((item) => {
          const active = location.pathname === item.to || location.pathname.startsWith(item.to + "/");
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={`flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-medium transition-all ${
                active
                  ? "border-brand-primary/60 bg-brand-primary/15 text-brand-primary"
                  : "border-border bg-surface-card text-text-secondary hover:border-brand-primary/40 hover:text-brand-primary"
              }`}
            >
              <Icon size={14} />
              {item.label}
            </NavLink>
          );
        })}
      </div>

      <div className="rounded-2xl border border-border bg-surface-card">
        <div className="border-b border-border/80 px-4 py-3">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-brand-primary/80" />
            <div className="h-2 w-2 rounded-full bg-brand-secondary/80" />
            <div className="h-2 w-2 rounded-full bg-brand-tertiary/80" />
            <div className="ml-2 text-xs font-mono uppercase tracking-wider text-text-muted">
              {activeEnv?.label ?? "Environment"}
            </div>
          </div>
        </div>
        <div className="p-4">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
