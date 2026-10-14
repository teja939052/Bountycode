// @ts-nocheck
import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { Compass, Layers, FlaskConical, Swords, ClipboardList, Briefcase, type LucideIcon } from "lucide-react";

const ITEMS = [
  { to: "/world", label: "World", icon: Compass, desc: "Journey, worlds, levels, and progression" },
  { to: "/lab", label: "Lab", icon: FlaskConical, desc: "Concepts, lessons, code, and experiments" },
  { to: "/arena", label: "Arena", icon: Swords, desc: "Challenges, mocks, contests, and bosses" },
  { to: "/command", label: "Command", icon: ClipboardList, desc: "Today, readiness, repair, and applications" },
  { to: "/career", label: "Career", icon: Briefcase, desc: "Resume, interview, company prep, and applications" },
];

export default function EnvironmentEntry() {
  const location = useLocation();

  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-display font-extrabold tracking-tight text-text-primary">
          BountyCode
        </h1>
        <p className="mt-1 text-sm text-text-muted">
          Choose your environment. Everything you need is connected.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {ITEMS.map((item) => {
          const active = location.pathname === item.to || location.pathname.startsWith(item.to + "/");
          const Icon = item.icon;
          return (
            <Link
              key={item.to}
              to={item.to}
              className={`group relative rounded-2xl border p-5 transition-all ${
                active
                  ? "border-brand-primary/60 bg-brand-primary/10 shadow-[0_0_0_1px_rgba(99,102,241,0.15)]"
                  : "border-border bg-surface-card hover:border-brand-primary/40 hover:bg-brand-primary/5"
              }`}
            >
              <div className="flex items-center gap-3">
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-xl border ${
                    active
                      ? "border-brand-primary/40 bg-brand-primary/20 text-brand-primary"
                      : "border-border bg-surface-muted text-text-muted"
                  }`}
                >
                  <Icon size={18} />
                </div>
                <div>
                  <div className={`text-sm font-bold ${active ? "text-brand-primary" : "text-text-primary"}`}>
                    {item.label}
                  </div>
                  <div className="text-xs text-text-muted">{item.desc}</div>
                </div>
              </div>
              {active && (
                <motion.div
                  layoutId="env-active-pill"
                  className="absolute inset-x-3 bottom-3 h-1 rounded-full bg-brand-primary/80"
                  transition={{ type: "spring", stiffness: 500, damping: 30 }}
                />
              )}
            </Link>
          );
        })}
      </div>
    </div>
  );
}
