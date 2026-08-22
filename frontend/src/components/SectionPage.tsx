import { Link } from "react-router-dom";
import type { LucideIcon } from "lucide-react";
import { ArrowRight } from "lucide-react";
import { Card, Button } from "../design-system/components";

export interface HubItem {
  to: string;
  label: string;
  desc?: string;
  icon: LucideIcon;
}

export interface HubGroup {
  label: string;
  items: HubItem[];
}

export default function SectionPage({
  title,
  subtitle,
  icon: TitleIcon,
  groups,
}: {
  title: string;
  subtitle: string;
  icon: LucideIcon;
  groups: HubGroup[];
}) {
  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <header className="mb-8 flex items-center gap-4">
        <div className="relative">
          <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-brand-primary/30 to-brand-tertiary/30 blur-md opacity-70" aria-hidden="true" />
          <div className="relative flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-primary via-brand-deep to-brand-tertiary shadow-soft-md">
            <TitleIcon size={22} className="text-white" />
          </div>
        </div>
        <div>
          <h1 className="font-display text-2xl font-extrabold tracking-tight text-text-primary sm:text-3xl">{title}</h1>
          <p className="mt-0.5 text-sm text-text-secondary">{subtitle}</p>
        </div>
      </header>

      <div className="space-y-10">
        {groups.map((group) => (
          <section key={group.label}>
            <div className="mb-3 px-1 text-xs font-mono uppercase tracking-wider text-text-secondary">{group.label}</div>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {group.items.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.to}
                    to={item.to}
                    className="group flex items-start gap-3 rounded-2xl border border-border-primary bg-background-surface p-4 shadow-soft-sm transition-all hover:border-brand-primary/50 hover:shadow-soft-md"
                  >
                    <div className="mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-mint text-brand-deep transition-colors group-hover:bg-brand-primary group-hover:text-white">
                      <Icon size={18} />
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-medium text-text-primary">{item.label}</span>
                        <ArrowRight size={14} className="shrink-0 text-text-secondary transition-transform group-hover:translate-x-0.5 group-hover:text-brand-primary" />
                      </div>
                      {item.desc ? <p className="mt-0.5 text-xs leading-snug text-text-secondary">{item.desc}</p> : null}
                    </div>
                  </Link>
                );
              })}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}