import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft, CheckCircle2, Crown, Lock, Star, ChevronRight,
  Rocket, Terminal, X, Trophy,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";
import PracticeConsole from "../components/learning/PracticeConsole";
import CandyNode from "../components/candy/CandyNode";
import CandyProgress from "../components/candy/CandyProgress";
import { CANDY, candyRadial, candyGlow } from "../components/candy";
import type { CandyColor } from "../components/candy";
import { useMediaQuery } from "../hooks/useMediaQuery";

/* ── Candy Crush palette (from the candy design system) ── */
const LEVEL_COLORS: CandyColor[] = [
  "strawberry", "grape", "lemon", "mint", "blueberry", "tangerine", "cherry", "gold",
];

function candyOf(i: number) {
  return CANDY[LEVEL_COLORS[i % LEVEL_COLORS.length]];
}

function TypeBadge({ type }: { type: string }) {
  const labels: Record<string, string> = {
    theory: "Learn", practice: "Code", quiz: "Quiz",
    challenge: "Solve", project: "Build", boss: "Boss",
  };
  const colors: Record<string, string> = {
    theory: "bg-sky-500/15 text-sky-300 border-sky-400/25",
    practice: "bg-emerald-500/15 text-emerald-300 border-emerald-400/25",
    quiz: "bg-purple-500/15 text-purple-300 border-purple-400/25",
    challenge: "bg-orange-500/15 text-orange-300 border-orange-400/25",
    project: "bg-cyan-500/15 text-cyan-300 border-cyan-400/25",
    boss: "bg-rose-500/15 text-rose-300 border-rose-400/25",
  };
  return (
    <span className={`inline-block rounded-full border px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider ${colors[type] || colors.theory}`}>
      {labels[type] || type}
    </span>
  );
}

function DifficultyStars({ difficulty }: { difficulty: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3].map((d) => (
        <Star key={d} size={10} className={d <= difficulty ? "fill-amber-400 text-amber-400" : "text-text-primary/25"} />
      ))}
    </div>
  );
}

export default function LanguageJourney() {
  const { languageId } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [expandedLevel, setExpandedLevel] = useState<string | null>(null);
  const [dockOpen, setDockOpen] = useState(false);
  const currentRef = useRef<HTMLDivElement | null>(null);
  const isMobile = useMediaQuery("(max-width: 640px)");

  useEffect(() => {
    setLoading(true);
    api.get(`/api/v1/learning/${languageId}/levels`)
      .then((d) => {
        setData(d);
        const incomplete = d.levels.find((l: any) => l.progress_pct < 100);
        if (incomplete) setExpandedLevel(incomplete.id);
        else if (d.levels.length > 0) setExpandedLevel(d.levels[d.levels.length - 1].id);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [languageId]);

  useEffect(() => {
    if (data && currentRef.current) {
      currentRef.current.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }, [data]);

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;
  if (!data) return <div className="min-h-screen flex items-center justify-center text-gray-400">Not found</div>;

  const cols = isMobile ? 3 : 5;
  const pitch = isMobile ? 96 : 114;
  const rowPitch = isMobile ? 148 : 152;
  const nodeSize = isMobile ? 70 : 84;
  const nodeSizeClass = isMobile
    ? "h-[70px] w-[70px]"
    : "h-[84px] w-[84px]";

  const levels = [...data.levels].sort((a: any, b: any) => a.order - b.order);
  const rows = Math.max(1, Math.ceil(levels.length / cols));
  const xOf = (col: number) => col * pitch + nodeSize / 2;
  const yOf = (row: number) => row * rowPitch + nodeSize / 2 + 6;
  const posOf = (i: number) => {
    const row = Math.floor(i / cols);
    const off = i % cols;
    const col = row % 2 === 0 ? off : cols - 1 - off;
    return { row, col, x: xOf(col), y: yOf(row) };
  };
  const boardW = (cols - 1) * pitch + nodeSize + 24;
  const boardH = (rows - 1) * rowPitch + nodeSize + 96;

  /* state derivation: completed → current (first incomplete) → locked */
  const stateOf = (i: number): "completed" | "current" | "locked" => {
    const l = levels[i];
    if (l.progress_pct === 100) return "completed";
    const prevDone = i === 0 ? true : levels[i - 1].progress_pct === 100;
    return prevDone ? "current" : "locked";
  };

  const segments: { d: string; muted: boolean }[] = [];
  for (let i = 0; i < levels.length - 1; i++) {
    const a = posOf(i);
    const b = posOf(i + 1);
    const d =
      a.row === b.row
        ? `M ${a.x} ${a.y} L ${b.x} ${b.y}`
        : `M ${a.x} ${a.y} L ${a.x} ${b.y} L ${b.x} ${b.y}`;
    segments.push({ d, muted: stateOf(i + 1) === "locked" });
  }

  const expanded = levels.find((l: any) => l.id === expandedLevel);
  const completedCount = levels.filter((l: any) => l.progress_pct === 100).length;
  const totalXp = data.total_xp || 0;
  const currentLevel = levels.find((_l: any, i: number) => stateOf(i) === "current");

  return (
    <div className={`relative min-h-screen px-3 py-8 md:px-4 ${dockOpen ? "pb-[440px]" : ""}`}>
      <ArcadeBackdrop variant="candy" />
      <div className="relative z-10 mx-auto max-w-4xl">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <Link to="/learn" className="mb-4 inline-flex items-center gap-2 font-mono text-sm text-text-primary/50 transition-colors hover:text-white">
            <ArrowLeft size={14} /> All Languages
          </Link>
          <div className="flex flex-wrap items-center gap-4">
            <div
              className="flex h-16 w-16 items-center justify-center rounded-3xl text-4xl shadow-xl"
              style={{ background: candyRadial(LEVEL_COLORS[0]), boxShadow: candyGlow(LEVEL_COLORS[0]) }}
            >
              {data.language.icon}
            </div>
            <div className="min-w-0 flex-1">
              <h1 className="font-display text-3xl font-black md:text-4xl">
                <span className="text-text-primary">{data.language.name}</span>
              </h1>
              <div className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 font-mono text-sm text-text-primary/60">
                <span className="flex items-center gap-1"><Trophy size={13} className="text-amber-400" /> {totalXp} XP</span>
                <span>{completedCount} / {levels.length} levels</span>
                <span>
                  {levels.reduce((a: number, l: any) => a + l.lessons_completed, 0)} / {levels.reduce((a: number, l: any) => a + l.total_lessons, 0)} lessons
                </span>
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                <button
                  onClick={() => setDockOpen((v) => !v)}
                  className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 font-mono text-sm transition-all ${
                    dockOpen
                      ? "border-cyan-300/50 bg-cyan-400/25 text-cyan-200"
                      : "border-cyan-300/30 bg-cyan-400/15 text-cyan-200 hover:bg-cyan-400/25"
                  }`}
                >
                  {dockOpen ? <X size={14} /> : <Terminal size={14} />}
                  {dockOpen ? "Close Practice" : "Open Practice"}
                </button>
                <Link
                  to="/playground"
                  className="inline-flex items-center gap-2 rounded-xl border border-fuchsia-300/30 bg-fuchsia-400/15 px-4 py-2 font-mono text-sm text-fuchsia-200 transition-all hover:bg-fuchsia-400/25"
                >
                  <Rocket size={14} /> Playground
                </Link>
              </div>
              {currentLevel && (
                <p className="mt-3 font-mono text-xs text-text-primary/50">
                  Next stop — <span className="font-bold text-text-primary">{currentLevel.name}</span>
                </p>
              )}
            </div>
          </div>

          {/* Candy progress bar */}
          <div className="mt-6 rounded-2xl border border-white/10 bg-white border-border shadow-card p-4 backdrop-blur-sm">
            <div className="flex items-center justify-between font-mono text-xs uppercase tracking-widest text-text-primary/50">
              <span>Campaign progress</span>
              <span>{completedCount} / {levels.length} levels</span>
            </div>
            <div className="mt-2 flex h-2.5 w-full gap-1 overflow-hidden rounded-full bg-white border-border/10 p-0.5 md:h-3">
              {levels.map((l: any, i: number) => {
                const s = stateOf(i);
                const c = candyOf(i);
                return (
                  <div
                    key={l.id}
                    className={`h-full flex-1 rounded-full transition-all duration-700 ${s === "current" ? "animate-pulse" : ""}`}
                    style={{
                      background: s === "completed" ? `linear-gradient(90deg, ${c.base}, ${c.light})` : s === "locked" ? "rgba(255,255,255,0.06)" : `radial-gradient(circle at 40% 30%, ${c.light}, ${c.base})`,
                      boxShadow: s === "completed" ? `0 0 10px ${c.base}88` : s === "current" ? `0 0 14px ${c.base}` : "none",
                    }}
                  />
                );
              })}
            </div>
          </div>
        </motion.div>

        {/* Candy Crush Map */}
        <div className="relative mx-auto" style={{ width: boardW, height: boardH }}>
          {/* soft candy depth blobs */}
          <div className="pointer-events-none absolute inset-0">
            <div className="absolute -left-10 top-1/4 h-48 w-48 rounded-full blur-3xl"
              style={{ background: "radial-gradient(circle, rgba(255,107,107,0.30), transparent 70%)" }} />
            <div className="absolute -right-8 top-1/3 h-52 w-52 rounded-full blur-3xl"
              style={{ background: "radial-gradient(circle, rgba(132,94,194,0.28), transparent 70%)" }} />
            <div className="absolute bottom-10 left-1/3 h-44 w-44 rounded-full blur-3xl"
              style={{ background: "radial-gradient(circle, rgba(255,199,95,0.20), transparent 70%)" }} />
          </div>
          {/* dotted board */}
          <div className="pointer-events-none absolute inset-0 opacity-40"
            style={{ backgroundImage: "radial-gradient(rgba(255,255,255,0.10) 1px, transparent 1px)", backgroundSize: "26px 26px" }} />

          {/* floating candy sparkles */}
          <div className="pointer-events-none absolute inset-0" aria-hidden="true">
            <span className="candy-float absolute left-[6%] top-[4%] text-xl opacity-60" style={{ animationDelay: "0s" }}>🍬</span>
            <span className="candy-float absolute right-[8%] top-[10%] text-lg opacity-50" style={{ animationDelay: "1.2s" }}>✨</span>
            <span className="candy-float absolute left-[12%] top-[46%] text-lg opacity-40" style={{ animationDelay: "2.1s" }}>🌟</span>
            <span className="candy-float absolute right-[10%] top-[58%] text-xl opacity-50" style={{ animationDelay: "0.6s" }}>🍭</span>
            <span className="candy-float absolute left-[5%] top-[84%] text-lg opacity-40" style={{ animationDelay: "1.7s" }}>✨</span>
            <span className="candy-float absolute right-[5%] top-[90%] text-xl opacity-50" style={{ animationDelay: "2.6s" }}>🍬</span>
          </div>

          {/* connectors — tight winding path with animated candy flow */}
          <svg className="pointer-events-none absolute inset-0" width={boardW} height={boardH}>
            {segments.map((seg, i) => {
              const c = candyOf(i);
              return (
                <g key={i}>
                  <path
                    d={seg.d}
                    fill="none"
                    stroke={seg.muted ? "rgba(255,255,255,0.16)" : c.base}
                    strokeWidth={seg.muted ? 3 : 6}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    opacity={seg.muted ? 1 : 0.9}
                  />
                  {!seg.muted && (
                    <path
                      className="candy-flow"
                      d={seg.d}
                      fill="none"
                      stroke={c.light}
                      strokeWidth={2}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeDasharray="12 12"
                    />
                  )}
                </g>
              );
            })}
          </svg>

          {/* nodes */}
          {levels.map((level: any, i: number) => {
            const p = posOf(i);
            const s = stateOf(i);
            return (
              <div
                key={level.id}
                className="absolute -translate-x-1/2 -translate-y-1/2"
                style={{ left: p.x, top: p.y }}
              >
                <motion.div
                  initial={{ opacity: 0, y: 14 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.15 + i * 0.04, duration: 0.4, ease: "easeOut" }}
                >
                  <CandyNode
                    number={i + 1}
                    emoji={level.emoji}
                    color={LEVEL_COLORS[i % LEVEL_COLORS.length]}
                    state={s}
                    milestone={(i + 1) % 5 === 0}
                    className={nodeSizeClass}
                    innerRef={s === "current" ? currentRef : undefined}
                    onClick={() => {
                      if (s === "locked") return;
                      setExpandedLevel((cur) => (cur === level.id ? null : level.id));
                    }}
                  />
                  <div className="mt-2 flex justify-center">
                    <span className={`max-w-[96px] truncate text-center text-[10px] font-semibold md:text-[11px] ${
                      s === "locked" ? "text-text-primary/35" : s === "completed" ? "text-amber-200/90" : "text-text-primary/80"
                    }`}>
                      {level.name}
                    </span>
                  </div>
                </motion.div>
              </div>
            );
          })}
        </div>

        {/* Legend */}
        <div className="mt-6 flex flex-wrap items-center justify-center gap-x-4 gap-y-2 font-mono text-xs text-text-primary/50">
          <span className="flex items-center gap-1.5"><span className="h-3 w-3 rounded-full border-2 border-amber-300 bg-amber-400" /> Complete</span>
          <span className="flex items-center gap-1.5"><span className="h-3 w-3 rounded-full bg-rose-400" /> You are here</span>
          <span className="flex items-center gap-1.5"><span className="h-3 w-3 rounded-full bg-[#232331]" /> Locked</span>
          <span className="flex items-center gap-1.5"><Crown size={12} className="text-amber-400" /> Milestone</span>
        </div>

        {/* Expanded level panel */}
        <AnimatePresence>
          {expanded && (
            <motion.div
              key={expanded.id}
              initial={{ opacity: 0, y: 16, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 8 }}
              className="mx-auto mt-8 w-full max-w-xl"
            >
              <LevelPanel languageId={languageId ?? ""} level={expanded} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Practice dock */}
      <AnimatePresence>
        {dockOpen && (
          <motion.div
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{ type: "spring", damping: 26, stiffness: 260 }}
            className="fixed inset-x-0 bottom-0 z-40 border-t border-white/10 bg-[#12101f]/95 p-4 shadow-2xl backdrop-blur-md"
          >
            <div className="mx-auto max-w-6xl">
              <PracticeConsole
                language={languageId ?? "python"}
                height={230}
                title={`${data.language.name} — practice here`}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {!dockOpen && (
        <button
          onClick={() => setDockOpen(true)}
          className="fixed bottom-6 right-6 z-40 flex items-center gap-2 rounded-2xl border border-cyan-300/40 bg-[#12101f]/90 px-4 py-3 font-mono text-sm text-cyan-200 shadow-xl backdrop-blur-md transition-all hover:bg-[#1c1930]"
          title="Open practice console"
        >
          <Terminal size={16} /> Practice
        </button>
      )}
    </div>
  );
}

/* ── Expanded level: lesson list panel ── */
function LevelPanel({ languageId, level }: { languageId: string; level: any }) {
  const [lessons, setLessons] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const c = candyOf(0);

  const load = useCallback(() => {
    setLoading(true);
    api.get(`/api/v1/learning/${languageId}/${level.id}/lessons`)
      .then((d) => setLessons(d.lessons))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [languageId, level.id]);

  useEffect(() => { load(); }, [load]);

  const groups: { type: string; lessons: any[] }[] = [];
  let current: any = null;
  for (const l of lessons) {
    if (!current || current.type !== l.type) {
      current = { type: l.type, lessons: [] };
      groups.push(current);
    }
    current.lessons.push(l);
  }

  return (
    <div
      className="overflow-hidden rounded-3xl border border-white/10 bg-white/[0.04] shadow-2xl backdrop-blur-md"
      style={{ boxShadow: `0 20px 60px -20px ${c.base}66` }}
    >
      {/* panel header */}
      <div
        className="flex items-center gap-3 px-5 py-4"
        style={{ background: `linear-gradient(120deg, ${c.dark}, ${c.base} 60%, ${c.light})` }}
      >
        <span className="text-3xl">{level.emoji || "🍬"}</span>
        <div className="min-w-0 flex-1">
          <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-text-primary/70">Level {level.order + 1}</p>
          <h3 className="truncate font-display text-lg font-black text-text-primary">{level.name}</h3>
        </div>
        <div className="text-right">
          <div className="font-mono text-xs text-text-primary/80">{level.progress_pct}%</div>
          <div className="flex items-center gap-1 font-mono text-[10px] text-text-primary/60">
            <Trophy size={11} className="text-amber-200" /> {level.xp_earned} / {level.total_xp} XP
          </div>
        </div>
      </div>

      {/* candy progress fill */}
      <div className="px-5 pb-4">
        <CandyProgress
          value={level.progress_pct}
          color={LEVEL_COLORS[(level.order || 0) % LEVEL_COLORS.length]}
          size="sm"
          showPercent={false}
        />
      </div>

      {loading ? (
        <div className="p-6"><Spinner /></div>
      ) : groups.length === 0 ? (
        <div className="p-6 text-center font-mono text-sm text-text-primary/40">No lessons yet</div>
      ) : (
        <div className="space-y-4 p-4">
          {groups.map((group, gi) => (
            <div key={gi}>
              <TypeBadge type={group.type} />
              <div className="mt-2 space-y-1.5">
                {group.lessons.map((lesson) => (
                  <LessonRow key={lesson.id} lesson={lesson} languageId={languageId} levelId={level.id} />
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function LessonRow({ lesson, languageId, levelId }: { lesson: any; languageId: string; levelId: string }) {
  const isBoss = lesson.type === "boss";
  const isProject = lesson.type === "project";

  if (!lesson.unlocked) {
    return (
      <div className="flex items-center gap-2 rounded-xl bg-white/[0.03] p-2.5 opacity-40">
        <Lock size={13} className="shrink-0 text-text-primary/50" />
        <span className="flex-1 truncate font-mono text-xs text-text-primary/50">{lesson.title}</span>
        <DifficultyStars difficulty={lesson.difficulty || 1} />
        <span className="font-mono text-[10px] text-text-primary/40">+{lesson.xp}</span>
      </div>
    );
  }

  return (
    <Link to={`/learn/${languageId}/${levelId}/${lesson.id}`} className="group block">
      <div
        className={`flex items-center gap-2 rounded-xl p-2.5 transition-all ${
          lesson.completed
            ? "bg-emerald-400/10 ring-1 ring-emerald-300/20"
            : isBoss
            ? "bg-rose-500/10 ring-1 ring-rose-400/30"
            : isProject
            ? "bg-cyan-500/10 ring-1 ring-cyan-400/30"
            : "bg-white/[0.05] ring-1 ring-white/10 hover:bg-white/[0.09] hover:ring-white/25"
        }`}
      >
        {lesson.completed ? (
          <CheckCircle2 size={15} className="shrink-0 text-emerald-300" />
        ) : isBoss ? (
          <span className="shrink-0 text-sm">👑</span>
        ) : isProject ? (
          <span className="shrink-0 text-sm">🔨</span>
        ) : (
          <span className="h-3.5 w-3.5 shrink-0 rounded-full border-2 border-white/30" />
        )}
        <span className={`flex-1 truncate font-mono text-xs ${lesson.completed ? "text-emerald-200" : isBoss ? "text-rose-200" : "text-text-primary/85"}`}>
          {lesson.title}
        </span>
        <DifficultyStars difficulty={lesson.difficulty || 1} />
        <span className="shrink-0 font-mono text-[10px] text-amber-300/80">+{lesson.xp}</span>
        <ChevronRight size={13} className="shrink-0 text-text-primary/40 transition-transform group-hover:translate-x-0.5 group-hover:text-white" />
      </div>
    </Link>
  );
}
