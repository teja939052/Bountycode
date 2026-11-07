import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Loader2 } from "lucide-react";
import api from "../services/api";
import { Card, Button, SectionHeader } from "../design-system";
import { PageShell } from "../design-system/PageShell";

interface SkillEntry {
  skill: string;
  label: string;
  score: number;
  attempts: number;
}

interface CategoryEntry {
  id: string;
  name: string;
  score: number;
  skills: SkillEntry[];
}

type AnyRecord = Record<string, any>;

/** Where a learner can actually practise each skill category. */
const PRACTICE_ROUTE: Record<string, string> = {
  dsa: "/question-bank",
  aptitude: "/aptitude",
  programming: "/lessons",
  system_design: "/system-design",
  behavioral: "/company-prep",
  resume: "/resume",
};

function titleCase(value: string): string {
  return value
    .split(/[_-]/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function tierFor(attempts: number, score: number) {
  if (attempts === 0) return { label: "Not practiced", className: "text-text-muted" };
  if (score < 40) return { label: "Critical", className: "text-red-500" };
  if (score < 60) return { label: "Weak", className: "text-orange-500" };
  if (score < 85) return { label: "On track", className: "text-blue-500" };
  return { label: "Strong", className: "text-primary" };
}

function parseCategories(raw: unknown): CategoryEntry[] {
  if (!raw || typeof raw !== "object") return [];
  const categories = (raw as AnyRecord).categories;
  if (!categories || typeof categories !== "object") return [];

  return Object.entries(categories as Record<string, AnyRecord>).map(([id, category]) => {
    const skills = Object.entries((category?.skills || {}) as Record<string, AnyRecord>).map(
      ([skill, data]) => ({
        skill,
        label: titleCase(skill),
        score: Number(data?.score || 0),
        attempts: Number(data?.attempts || 0),
      })
    );
    skills.sort((a, b) => b.attempts - a.attempts || a.label.localeCompare(b.label));
    return {
      id,
      name: String(category?.name || titleCase(id)),
      score: Number(category?.score || 0),
      skills,
    };
  });
}

export default function SkillMap() {
  const [graph, setGraph] = useState<unknown>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    api.gamification
      .getSkillGraph()
      .then((res) => {
        if (active) setGraph(res);
      })
      .catch((err: { detail?: string }) => {
        if (active) setError(err?.detail || "Could not load your skill graph.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const categories = useMemo(() => parseCategories(graph), [graph]);
  const practised = useMemo(
    () =>
      categories.reduce(
        (total, category) => total + category.skills.filter((skill) => skill.attempts > 0).length,
        0
      ),
    [categories]
  );

  if (loading) {
    return (
      <PageShell theme="adventure" className="max-w-5xl mx-auto px-4 py-20">
        <div className="flex items-center justify-center gap-2 text-text-muted">
          <Loader2 size={18} className="animate-spin" />
          <span className="text-sm">Loading skills…</span>
        </div>
      </PageShell>
    );
  }

  return (
    <PageShell theme="adventure" className="max-w-5xl mx-auto px-4 py-8">
      <SectionHeader
        eyebrow="Mastery"
        title="Skill map"
        description={`Measured from ${practised} practised skill${practised === 1 ? "" : "s"}. Skills you have not attempted yet are shown as "not practiced" rather than scored.`}
        action={
          <Link to="/lessons">
            <Button size="sm">
              Practice now <ArrowRight size={14} className="ml-2" />
            </Button>
          </Link>
        }
      />

      {error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
          {error}
        </div>
      )}

      {categories.length === 0 ? (
        <Card>
          <p className="text-sm text-text-muted">
            No skill data yet. Complete a lesson or a practice question to start building your map.
          </p>
        </Card>
      ) : (
        <div className="space-y-6">
          {categories.map((category) => (
            <Card key={category.id}>
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h3 className="font-display text-lg font-bold text-text">{category.name}</h3>
                  <p className="text-xs text-text-muted">
                    Category score {Math.round(category.score)} / 100
                  </p>
                </div>
                <Link to={PRACTICE_ROUTE[category.id] || "/lessons"}>
                  <Button variant="outline" size="sm">
                    Practice <ArrowRight size={14} className="ml-2" />
                  </Button>
                </Link>
              </div>

              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {category.skills.map((skill) => {
                  const tier = tierFor(skill.attempts, skill.score);
                  const pct = skill.attempts > 0 ? Math.min(100, Math.max(0, skill.score)) : 0;
                  return (
                    <div key={skill.skill} className="rounded-lg border border-border p-3">
                      <div className="flex items-center justify-between gap-2">
                        <span className="truncate text-sm font-semibold text-text">
                          {skill.label}
                        </span>
                        <span className={`text-[11px] font-semibold uppercase ${tier.className}`}>
                          {tier.label}
                        </span>
                      </div>
                      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[#E8EDE3]">
                        <div
                          className="h-full rounded-full bg-primary transition-all duration-500"
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                      <p className="mt-2 text-[11px] font-mono text-text-muted">
                        {skill.attempts > 0
                          ? `${Math.round(skill.score)}% · ${skill.attempts} attempt${skill.attempts === 1 ? "" : "s"}`
                          : "Not practiced yet"}
                      </p>
                    </div>
                  );
                })}
              </div>
            </Card>
          ))}
        </div>
      )}
    </PageShell>
  );
}
