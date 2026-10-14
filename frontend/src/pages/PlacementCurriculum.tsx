// @ts-nocheck
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ChevronRight,
  Clock,
  Trophy,
  Search,
} from "lucide-react";
import Spinner from "../components/ui/Spinner";
import { lessonApi } from "../services/api/lesson";

type World = {
  world_id: string;
  name: string;
  icon: string;
  subtitle: string;
  description: string;
  color: string;
  levels: number;
};

type Lesson = {
  slug: string;
  lesson_id: string;
  title: string;
  description: string;
  difficulty: string;
  est_minutes: number;
  diamonds: number;
  world_id: string;
  icon: string;
};

const WORLD_COLORS: Record<string, string> = {
  placement_readiness: "border-blue-500/30 bg-blue-500/5",
  aptitude_gauntlet: "border-amber-500/30 bg-amber-500/5",
  coding_foundations: "border-violet-500/30 bg-violet-500/5",
  cs_core: "border-emerald-500/30 bg-emerald-500/5",
  company_quests: "border-sky-500/30 bg-sky-500/5",
  interview_arena: "border-rose-500/30 bg-rose-500/5",
};

const DIFFICULTY_COLORS: Record<string, string> = {
  beginner: "text-green-400 bg-green-400/10",
  intermediate: "text-yellow-400 bg-yellow-400/10",
  advanced: "text-red-400 bg-red-400/10",
  expert: "text-purple-400 bg-purple-400/10",
};

export default function PlacementCurriculum() {
  const [worlds, setWorlds] = useState<World[]>([]);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [selectedWorld, setSelectedWorld] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const data = await lessonApi.getLesson<any>("/curriculum");
        if (!cancelled) {
          setWorlds(data.worlds || []);
          setLessons(data.lessons || []);
        }
      } catch (e: any) {
        if (!cancelled) setError(e?.message || "Failed to load curriculum");
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }
    load();
    return () => { cancelled = true; };
  }, []);

  const filtered = lessons.filter((l) => {
    if (selectedWorld && l.world_id !== selectedWorld) return false;
    if (search.trim()) {
      const q = search.toLowerCase();
      return (
        l.title.toLowerCase().includes(q) ||
        l.description.toLowerCase().includes(q) ||
        l.slug.toLowerCase().includes(q)
      );
    }
    return true;
  });

  const grouped = selectedWorld
    ? { [selectedWorld]: filtered }
    : filtered.reduce<Record<string, Lesson[]>>((acc, l) => {
        acc[l.world_id] = acc[l.world_id] || [];
        acc[l.world_id].push(l);
        return acc;
      }, {});

  if (isLoading) {
    return (
      <div className="min-h-screen bg-canvas flex items-center justify-center">
        <div className="text-center">
          <Spinner />
          <p className="mt-3 text-sm text-text-muted">Loading curriculum...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-canvas flex items-center justify-center">
        <div className="text-center">
          <p className="text-sm text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-canvas">
      <div className="mx-auto max-w-6xl px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text">Placement Curriculum</h1>
          <p className="mt-2 text-text-muted">
            Six worlds. {lessons.length} flagship lessons. Master the patterns that matter.
          </p>
        </div>

        <div className="mb-6 flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
            <input
              type="text"
              placeholder="Search lessons..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full rounded-xl border border-surface-border bg-surface-card pl-10 pr-4 py-2.5 text-sm text-text placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
          </div>
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setSelectedWorld(null)}
              className={`px-3 py-2 rounded-lg text-xs font-medium border transition-colors ${
                selectedWorld === null
                  ? "bg-primary text-white border-primary"
                  : "bg-surface-card text-text-muted border-surface-border hover:text-text"
              }`}
            >
              All Worlds
            </button>
            {worlds.map((w) => (
              <button
                key={w.world_id}
                onClick={() => setSelectedWorld(selectedWorld === w.world_id ? null : w.world_id)}
                className={`px-3 py-2 rounded-lg text-xs font-medium border transition-colors ${
                  selectedWorld === w.world_id
                    ? "bg-primary text-white border-primary"
                    : "bg-surface-card text-text-muted border-surface-border hover:text-text"
                }`}
              >
                {w.icon} {w.name}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {worlds.map((w) => {
            const count = lessons.filter((l) => l.world_id === w.world_id).length;
            return (
              <motion.div
                key={w.world_id}
                whileHover={{ y: -2 }}
                onClick={() => setSelectedWorld(selectedWorld === w.world_id ? null : w.world_id)}
                className={`rounded-2xl border p-5 cursor-pointer transition-all ${WORLD_COLORS[w.world_id] || "border-surface-border bg-surface-card"}`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{w.icon}</span>
                  <div>
                    <h3 className="font-bold text-text">{w.name}</h3>
                    <p className="text-xs text-text-muted">{w.subtitle}</p>
                  </div>
                </div>
                <p className="mt-2 text-xs text-text-muted line-clamp-2">{w.description}</p>
                <div className="mt-3 flex items-center justify-between text-xs text-text-muted">
                  <span>{count} lessons</span>
                  <span>{w.levels} levels</span>
                </div>
              </motion.div>
            );
          })}
        </div>

        <div className="space-y-6">
          {Object.entries(grouped).map(([worldId, worldLessons]) => {
            const world = worlds.find((w) => w.world_id === worldId);
            if (!world) return null;
            return (
              <div key={worldId}>
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-xl">{world.icon}</span>
                  <h2 className="text-lg font-bold text-text">{world.name}</h2>
                  <span className="text-xs text-text-muted">{world.subtitle}</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {worldLessons.map((lesson) => (
                    <Link
                      key={lesson.slug}
                      to={`/learn/coding?lesson=${encodeURIComponent(lesson.slug)}`}
                      className="group block rounded-xl border border-surface-border bg-surface-card p-4 transition-all hover:border-primary/30 hover:shadow-lg"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span className="text-lg">{lesson.icon}</span>
                          <h3 className="font-semibold text-text group-hover:text-primary transition-colors">
                            {lesson.title}
                          </h3>
                        </div>
                        <ChevronRight size={16} className="text-text-muted group-hover:text-primary transition-colors mt-1" />
                      </div>
                      <p className="mt-1.5 text-xs text-text-muted line-clamp-2">{lesson.description}</p>
                      <div className="mt-3 flex items-center gap-2 text-[10px] text-text-muted">
                        <span className={`px-2 py-0.5 rounded-full ${DIFFICULTY_COLORS[lesson.difficulty] || "bg-gray-500/10 text-gray-400"}`}>
                          {lesson.difficulty}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock size={12} /> {lesson.est_minutes}m
                        </span>
                        <span className="flex items-center gap-1">
                          <Trophy size={12} /> {lesson.diamonds} diamonds
                        </span>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
