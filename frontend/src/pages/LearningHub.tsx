import { useState } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import {
  BookOpen,
  CalendarCheck,
  ChevronRight,
  Code2,
  Crown,
  Flame,
  Gamepad2,
  ListChecks,
  Rocket,
  Sparkles,
  Target,
  Trophy,
  Users,
  GraduationCap,
  Play,
  FileText,
  GitBranch,
  Globe,
  Trees,
  Gift,
  Sword,
  Medal,
  Award,
  Star,
} from "lucide-react";
import Spinner from "../components/ui/Spinner";
import AmbientParticles from "../components/candy/AmbientParticles";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";
import PracticeConsole from "../components/learning/PracticeConsole";
import CandyCard from "../components/candy/CandyCard";
import CandyProgress from "../components/candy/CandyProgress";
import LevelMap from "../components/candy/LevelMap";
import type { CandyColor, LevelNode } from "../components/candy";
import { useLearning } from "../hooks/useLearning";

const QUICK_START = [
  {
    to: "/curriculum",
    icon: BookOpen,
    color: "text-brand-teal bg-brand-teal/10 border-brand-teal/20",
    title: "Structured Courses",
    desc: "7 languages, 105 hands-on lessons with live previews, hints and quizzes — learn by building.",
  },
  {
    to: "/playground",
    icon: Rocket,
    color: "text-cyber-purple bg-cyber-purple/10 border-cyber-purple/20",
    title: "Digital Playground",
    desc: "Build HTML, CSS and JS live with a real preview — a free sandbox to experiment.",
  },
  {
    to: "/compiler",
    icon: Code2,
    color: "text-cyber-blue bg-cyber-blue/10 border-cyber-blue/20",
    title: "Full Compiler",
    desc: "8 languages, test cases, stdin and a step-by-step visualizer for serious practice.",
  },
  {
    to: "/daily-challenge",
    icon: CalendarCheck,
    color: "text-brand-coral bg-brand-coral/10 border-brand-coral/20",
    title: "Daily Challenge",
    desc: "Adaptive missions that change as you improve — new puzzle every day.",
  },
  {
    to: "/question-bank",
    icon: ListChecks,
    color: "text-brand-teal bg-brand-teal/10 border-brand-teal/20",
    title: "Question Bank",
    desc: "100+ curated interview problems filtered by company, topic and difficulty.",
  },
];

function generateLevelMap(languages: any[], userXp: number): LevelNode[] {
  const levels: LevelNode[] = [];
  const totalLevels = 100;
  const currentLevel = Math.max(1, Math.floor(userXp / 100) + 1);

  for (let i = 1; i <= totalLevels; i++) {
    let status: LevelNode["status"] = "locked";
    if (i < currentLevel) {
      status = i <= currentLevel - 5 ? "mastered" : "completed";
    } else if (i === currentLevel) {
      status = "current";
    } else if (i === currentLevel + 1) {
      status = "available";
    }

    levels.push({
      level: i,
      status,
      title: `Level ${i}`,
      xp: i * 100,
      stars: status === "mastered" ? 3 : status === "completed" ? Math.floor(Math.random() * 2) + 1 : 0,
      color: getLevelColor(i, status),
    });
  }
  return levels;
}

function getLevelColor(level: number, status: string): CandyColor {
  if (status === "locked") return "grape";
  if (status === "mastered") return "gold";
  if (status === "completed") return "blueberry";
  if (status === "current") return "lemon";
  const colors: CandyColor[] = ["strawberry", "mint", "blueberry", "tangerine", "grape", "cherry"];
  return colors[level % colors.length];
}

function DailyGoalCard({ daily, streak }: { daily: any; streak: number }) {
  if (!daily) return null;
  const pct = Math.min((daily.completed / daily.goal) * 100, 100);

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="arena-card mb-6 p-5">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-gold-pale text-brand-gold">
            <Flame size={20} />
          </div>
          <div>
            <p className="font-display font-bold text-text-primary text-sm">Today's Learning Goal</p>
            <p className="text-xs font-mono uppercase tracking-[0.22em] text-text-light">
              {daily.completed} / {daily.goal} lessons
            </p>
          </div>
        </div>
        {streak > 0 && (
          <div className="quest-chip">
            <Flame size={12} className="text-brand-coral" />
            {streak} day streak
          </div>
        )}
      </div>

      <div className="mt-4 h-3 rounded-full bg-surface-card/50 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className={`h-full rounded-full ${daily.reached ? "bg-brand-teal" : "bg-brand-coral"}`}
        />
      </div>

      {daily.reached ? (
        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-2 flex items-center gap-1 text-xs font-mono text-brand-teal">
          <Sparkles size={12} /> Daily goal complete. +30 XP bonus earned.
        </motion.p>
      ) : (
        <p className="mt-2 text-xs font-mono text-text-light">
          Complete {daily.goal - daily.completed} more for a +30 XP bonus.
        </p>
      )}
    </motion.div>
  );
}

function LeaderboardPreview({ leaderboard }: { leaderboard: any[] | null }) {
  if (!leaderboard || leaderboard.length === 0) return null;

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="arena-card p-5">
      <h3 className="mb-3 flex items-center gap-2 font-display font-bold text-text-primary">
        <Trophy size={18} className="text-brand-gold" />
        Top Learners
      </h3>
      <div className="space-y-2">
        {leaderboard.slice(0, 5).map((entry, index) => (
          <div key={entry.user_id} className="flex items-center gap-3 rounded-xl bg-surface-base px-3 py-2">
            <span
              className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold ${
                index === 0
                  ? "bg-yellow-100 text-yellow-600"
                  : index === 1
                  ? "bg-surface-card/50 text-brand-secondary"
                  : index === 2
                  ? "bg-orange-100 text-orange-600"
                  : "bg-surface-card/50 text-brand-muted"
              }`}
            >
              {index + 1}
            </span>
            <span className="flex-1 truncate text-sm text-text-secondary">{entry.name}</span>
            <span className="text-xs font-mono text-brand-gold">{entry.total_xp} XP</span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

export default function LearningHub() {
  const { data, leaderboard, isLoading, isError, refetch } = useLearning();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 text-text-muted">
        <div className="text-sm">Failed to load learning hub</div>
        <button onClick={() => refetch()} className="btn-primary px-4 py-2 text-sm">
          Retry
        </button>
      </div>
    );
  }

  const questTotals = data.languages.reduce(
    (acc: any, lang: any) => {
      acc.practice += lang.practice_lessons || 0;
      acc.challenge += lang.challenge_lessons || 0;
      acc.project += lang.project_lessons || 0;
      acc.quest += lang.quest_lessons || 0;
      return acc;
    },
    { practice: 0, challenge: 0, project: 0, quest: 0 }
  );

  const candyLang: Record<string, CandyColor> = {
    c: "grape",
    cpp: "blueberry",
    java: "tangerine",
    python: "mint",
    javascript: "lemon",
    go: "mint",
    rust: "cherry",
    html: "tangerine",
    css: "blueberry",
    sql: "strawberry",
    typescript: "blueberry",
    react: "mint",
    node: "mint",
  };

  return (
    <div className="relative min-h-screen px-4 py-6 md:py-8">
      <ArcadeBackdrop variant="arcade" />
      <div className="relative z-10 mx-auto max-w-7xl space-y-6">
        <motion.section initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} className="hero-shell p-6 md:p-8 text-text-primary">
          <div className="relative z-10 flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <span className="section-kicker border-white/10 bg-white border-border/10 text-text-primary">
                <BookOpen size={12} />
                Learning hub
              </span>
              <h1 className="mt-4 text-3xl font-black tracking-tight text-text-primary md:text-5xl">
                Master <span className="text-text-primary">13 coding campaigns</span> — languages & the full web stack
              </h1>
              <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-200 md:text-base">
                Lessons, challenges, projects, and boss battles in one progression loop — from C and
                Python to HTML, CSS, SQL, TypeScript, React, and Node. Pick a track, climb the tree,
                and keep the streak alive.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <StatChip label="XP" value={data.total_xp} />
              <StatChip label="Lessons" value={data.total_lessons} />
              <StatChip label="Streak" value={data.streak?.streak || 0} />
              <StatChip label="Projects" value={questTotals.project} />
            </div>
          </div>
        </motion.section>

        <motion.section initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-4 md:grid-cols-3">
          <div className="arena-card p-5">
            <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">Quest density</div>
            <div className="mt-2 text-xl font-display font-bold text-text-primary">More missions per lane</div>
            <p className="mt-2 text-sm leading-6 text-text-muted">
              Every level now includes extra practice and project quests so the path feels like a campaign, not a checklist.
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              <span className="quest-chip bg-brand-teal-pale text-brand-teal">{questTotals.practice} practice quests</span>
              <span className="quest-chip bg-brand-lavender-pale text-brand-lavender">{questTotals.challenge} challenge quests</span>
              <span className="quest-chip bg-brand-coral-pale text-brand-coral">{questTotals.project} project quests</span>
              <span className="quest-chip bg-white border-border/10 text-text-primary">{questTotals.quest} total quests</span>
            </div>
          </div>
          <div className="arena-card p-5">
            <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">Projects</div>
            <div className="mt-2 text-xl font-display font-bold text-text-primary">{questTotals.project} project quests</div>
            <p className="mt-2 text-sm leading-6 text-text-muted">
              More build-heavy checkpoints that unlock after you clear the basics.
            </p>
          </div>
          <div className="arena-card p-5">
            <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">Challenges</div>
            <div className="mt-2 text-xl font-display font-bold text-text-primary">{questTotals.challenge} challenge quests</div>
            <p className="mt-2 text-sm leading-6 text-text-muted">
              Extra pressure tests to make the grind feel competitive and alive.
            </p>
          </div>
        </motion.section>

        <motion.section initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-4 md:grid-cols-3">
          <div className="arena-card p-5">
            <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">Mode</div>
            <div className="mt-2 text-xl font-display font-bold text-text-primary">Boss-friendly lessons</div>
            <p className="mt-2 text-sm leading-6 text-text-muted">Short lessons and deliberate practice, built for real momentum instead of passive reading.</p>
          </div>
          <div className="arena-card p-5">
            <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">Reward loop</div>
            <div className="mt-2 text-xl font-display font-bold text-text-primary">XP, streaks, and badges</div>
            <p className="mt-2 text-sm leading-6 text-text-muted">Every completed lesson pushes the next milestone closer and makes the UI feel alive.</p>
          </div>
          <div className="arena-card p-5">
            <div className="text-[10px] font-mono uppercase tracking-[0.28em] text-text-light">Target</div>
            <div className="mt-2 text-xl font-display font-bold text-text-primary">From first loop to interview ready</div>
            <p className="mt-2 text-sm leading-6 text-text-muted">Learn the language fundamentals, then transfer that skill into coding rounds and placement prep.</p>
          </div>
        </motion.section>

        <DailyGoalCard daily={data.daily_goal} streak={data.streak?.streak || 0} />

        <section>
          <div className="mb-4 flex items-center gap-2">
            <Gamepad2 size={18} className="text-cyber-purple" />
            <h2 className="text-lg font-display font-bold uppercase tracking-wider text-text-primary">Quick start</h2>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {QUICK_START.map((q, i) => (
              <motion.div key={q.to} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }} whileHover={{ y: -4 }}>
                <Link to={q.to} className="block h-full">
                  <div className="arena-card h-full p-5">
                    <div className={`inline-flex h-11 w-11 items-center justify-center rounded-xl border ${q.color}`}>
                      <q.icon size={20} />
                    </div>
                    <h3 className="mt-3 font-display font-bold text-text-primary">{q.title}</h3>
                    <p className="mt-1.5 text-sm leading-6 text-text-muted">{q.desc}</p>
                    <span className="mt-3 inline-flex items-center gap-1 text-xs font-mono text-cyber-blue">
                      Open <ChevronRight size={12} />
                    </span>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </section>

        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <Link to="/study" className="group block">
            <div className="hero-shell relative overflow-hidden p-6 md:p-7">
              <div className="absolute right-0 top-0 hidden h-full w-1/3 bg-gradient-to-l from-cyber-purple/20 to-transparent md:block" />
              <div className="relative z-10 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-cyber-purple/20 text-cyber-purple">
                    <BookOpen size={22} />
                  </div>
                  <div>
                    <p className="text-[10px] font-mono uppercase tracking-[0.28em] text-cyber-purple">Study library</p>
                    <h2 className="mt-1 font-display text-xl font-black text-white md:text-2xl">
                      In-depth guides that go deeper than W3Schools
                    </h2>
                    <p className="mt-2 max-w-xl text-sm leading-6 text-slate-200">
                      The why behind the syntax — theory, analogies, real code, and common mistakes for
                      HTML, CSS, JavaScript, TypeScript, React, Node, SQL, and full-stack architecture.
                    </p>
                  </div>
                </div>
                <span className="inline-flex shrink-0 items-center gap-1 rounded-xl border border-cyber-purple/30 bg-cyber-purple/15 px-5 py-3 font-mono text-sm text-cyber-purple transition-all group-hover:bg-cyber-purple/25">
                  Explore articles <ChevronRight size={14} />
                </span>
              </div>
            </div>
          </Link>
        </motion.div>

        <section>
          <div className="mb-4 flex items-center gap-2">
            <Sparkles size={18} className="text-brand-sky" />
            <h2 className="text-lg font-display font-bold uppercase tracking-wider text-text-primary">Language campaigns</h2>
          </div>
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
            {data.languages.map((lang: any, li: number) => {
              const color = candyLang[String(lang.id)] || "strawberry";
              const hasProgress = lang.lessons_completed > 0;

              return (
                <motion.div key={lang.id} initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: li * 0.05 }} whileHover={{ y: -6 }} className="group">
                  <Link to={`/learn/${lang.id}`} className="block h-full">
                    <CandyCard color={color} hover={false} shine className="h-full p-5" contentClassName="flex h-full flex-col">
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-white/25 text-4xl shadow-lg backdrop-blur-sm transition-transform group-hover:scale-110">
                          {lang.icon}
                        </div>
                        {hasProgress && (
                          <span className="rounded-full bg-white/25 px-3 py-1 font-mono text-[10px] uppercase tracking-widest text-text-primary">
                            In progress
                          </span>
                        )}
                      </div>

                      <h2 className="mt-4 font-display text-2xl font-black text-white">{lang.name}</h2>
                      <p className="mt-2 flex-1 text-sm leading-6 text-text-primary/85">{lang.description}</p>

                      <div className="mt-4 flex flex-wrap gap-2">
                        <span className="rounded-full bg-surface-2 px-2.5 py-1 font-mono text-[10px] text-white/90">
                          {lang.practice_lessons} practice
                        </span>
                        <span className="rounded-full bg-surface-2 px-2.5 py-1 font-mono text-[10px] text-white/90">
                          {lang.challenge_lessons} challenges
                        </span>
                        <span className="rounded-full bg-surface-2 px-2.5 py-1 font-mono text-[10px] text-white/90">
                          {lang.project_lessons} projects
                        </span>
                      </div>

                      <div className="mb-4 mt-4 grid grid-cols-3 gap-2 border-t border-white/20 pt-4">
                        <div>
                          <div className="text-lg font-display font-black text-white">{lang.levels?.length ?? lang.total_lessons}</div>
                          <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-white/70">tiles</div>
                        </div>
                        <div>
                          <div className="text-lg font-display font-black text-white">{lang.total_xp}</div>
                          <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-white/70">XP</div>
                        </div>
                        <div>
                          <div className="text-lg font-display font-black text-white">{lang.progress_pct}%</div>
                          <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-white/70">done</div>
                        </div>
                      </div>

                      <div className="mt-auto flex items-center gap-3">
                        <div className="min-w-0 flex-1">
                          <div className="flex justify-between font-mono text-[10px] text-white/80">
                            <span>{lang.lessons_completed} / {lang.total_lessons} lessons</span>
                            <span>{lang.progress_pct}%</span>
                          </div>
                          <CandyProgress value={lang.progress_pct} color={color} size="sm" showPercent={false} className="mt-1" />
                        </div>
                        <ChevronRight size={18} className="shrink-0 text-white/70 transition-transform group-hover:translate-x-1" />
                      </div>
                    </CandyCard>
                  </Link>
                </motion.div>
              );
            })}
          </div>
        </section>

        {/* Level Progression Map - Organic Cinematic */}
        <section className="candy-glass relative overflow-hidden rounded-3xl p-6 md:p-8">
          {/* Ambient nature particles */}
          <AmbientParticles count={30} types={["firefly", "petal", "sparkle"]} />

          {/* Cinematic vignette overlay */}
          <div
            className="absolute inset-0 pointer-events-none z-10"
            style={{
              background: "radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.5) 100%)",
            }}
          />

          <div className="relative z-20">
            <div className="mb-8 flex items-center gap-3">
              <motion.div
                animate={{ rotate: [0, 5, -5, 0], scale: [1, 1.05, 1] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-yellow-400 via-orange-400 to-red-500 text-text-primary shadow-xl"
                style={{ boxShadow: "0 0 30px rgba(255,215,0,0.4)" }}
              >
                <Trophy size={22} />
              </motion.div>
              <div>
                <h2 className="text-2xl font-display font-black text-white text-text-primary">Your Journey</h2>
                <p className="text-xs text-white/60 mt-0.5">100 levels of coding mastery — click any level to begin</p>
              </div>
            </div>

          <div className="relative">
            {(() => {
              const levelData = generateLevelMap(data.languages, data.user_xp || 0);
              return (
                <LevelMap
                  levels={levelData}
                  currentLevel={Math.floor((data.user_xp || 0) / 100) + 1}
                  onLevelClick={(level) => {
                    if (level.status !== "locked") {
                      window.location.href = `/learn/${data.languages[0]?.id || "python"}?level=${level.level}`;
                    }
                  }}
                />
              );
            })()}
          </div>

          {/* Journey stats */}
          <div className="mt-8 grid grid-cols-3 gap-3">
            <div className="candy-glass-light rounded-xl p-3 text-center">
              <div className="text-lg font-black text-white">{Math.min(100, Math.floor((data.user_xp || 0) / 100) + 1)}</div>
              <div className="text-[10px] font-mono uppercase tracking-wider text-white/50">Current Level</div>
            </div>
            <div className="candy-glass-light rounded-xl p-3 text-center">
              <div className="text-lg font-black text-yellow-300">{data.user_xp || 0} XP</div>
              <div className="text-[10px] font-mono uppercase tracking-wider text-white/50">Total XP</div>
            </div>
            <div className="candy-glass-light rounded-xl p-3 text-center">
              <div className="text-lg font-black text-green-300">
                {(() => { const lvls = generateLevelMap(data.languages, data.user_xp || 0); return lvls.filter(l => l.status === "mastered" || l.status === "completed").length || 0; })()}
              </div>
              <div className="text-[10px] font-mono uppercase tracking-wider text-white/50">Completed</div>
            </div>
          </div>
          </div>
        </section>

        <section className="grid gap-5 lg:grid-cols-[1.15fr_0.85fr]">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <div className="mb-3 flex items-center gap-2">
              <Code2 size={18} className="text-cyber-green" />
              <h2 className="text-lg font-display font-bold uppercase tracking-wider text-text-primary">Practice right here</h2>
            </div>
            <PracticeConsole
              language={data.languages[0]?.id || "python"}
              title="Live Practice Console"
              height={280}
            />
            <p className="mt-2 text-xs font-mono text-text-light">
              Pick any language, edit the starter, hit Run. Compiler runs live via the Piston engine.
            </p>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <div className="arena-card h-full p-5 flex flex-col">
              <div className="flex items-center gap-2">
                <Rocket size={18} className="text-cyber-purple" />
                <h2 className="text-lg font-display font-bold uppercase tracking-wider text-text-primary">Digital playground</h2>
              </div>
              <p className="mt-3 text-sm leading-6 text-text-muted">
                The full Code Playground gives you a multi-file workspace: HTML, CSS and JavaScript with a live browser preview, plus a console for every run.
              </p>
              <ul className="mt-4 space-y-2 text-sm font-mono text-text-secondary">
                <li className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-cyber-purple" /> Live preview iframe</li>
                <li className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-cyber-purple" /> Add / remove files freely</li>
                <li className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-cyber-purple" /> Piston execution for C, C++, Java, Python</li>
              </ul>
              <Link to="/playground" className="mt-auto pt-5">
                <span className="block w-full py-3 rounded-xl bg-cyber-purple/20 border border-cyber-purple/30 text-cyber-purple text-center font-mono text-sm hover:bg-cyber-purple/30 transition-all">
                  Open Playground <ChevronRight size={14} className="inline" />
                </span>
              </Link>
            </div>
          </motion.div>
        </section>

        <section className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="arena-card p-5">
            <div className="mb-4 flex items-center gap-2">
              <Target size={18} className="text-brand-coral" />
              <h2 className="text-lg font-display font-bold uppercase tracking-wider text-text-primary">Leaderboard pressure</h2>
            </div>
            <LeaderboardPreview leaderboard={leaderboard} />
          </div>

          {data.streak?.streak > 0 && (
            <div className="arena-card p-5">
              <div className="mb-4 flex items-center gap-2">
                <Crown size={18} className="text-brand-gold" />
                <h2 className="text-lg font-display font-bold uppercase tracking-wider text-text-primary">Streak aura</h2>
              </div>
              <div className="rounded-3xl bg-brand-gold-pale p-5">
                <div className="flex items-center gap-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-gold text-text-primary">
                    <Flame size={26} />
                  </div>
                  <div>
                    <div className="text-3xl font-black text-text-primary">{data.streak.streak}</div>
                    <div className="text-xs font-mono uppercase tracking-[0.24em] text-text-light">days in a row</div>
                  </div>
                </div>
                <div className="mt-4 text-sm leading-6 text-text-muted">
                  Keep the streak alive to make the hub feel like a daily ritual, not a one-off course.
                </div>
              </div>
            </div>
          )}
        </section>

        <section className="rounded-2xl border border-cyber-purple/20 bg-cyber-purple/5 p-5">
          <h2 className="text-lg font-display font-bold uppercase tracking-wider text-white mb-4">Discover More</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {[
              { to: "/world", icon: Globe, label: "World Map", color: "text-cyber-green" },
              { to: "/tower", icon: Trees, label: "Forest Journey", color: "text-brand-teal" },
              { to: "/referral", icon: Gift, label: "Refer & Earn", color: "text-brand-coral" },
              { to: "/campus-wars", icon: Users, label: "Campus Wars", color: "text-brand-sky" },
              { to: "/battles", icon: Sword, label: "1v1 Battles", color: "text-brand-gold" },
              { to: "/rank", icon: Medal, label: "Rank Profile", color: "text-brand-amber" },
              { to: "/cards", icon: Award, label: "Card Collection", color: "text-brand-lavender" },
              { to: "/achievements", icon: Star, label: "Achievements", color: "text-brand-gold" },
              { to: "/skill-trees", icon: Target, label: "Skill Trees", color: "text-brand-emerald" },
              { to: "/adaptive", icon: GitBranch, label: "Adaptive Path", color: "text-brand-sky" },
              { to: "/project-generator", icon: Rocket, label: "Project Generator", color: "text-brand-coral" },
              { to: "/languages", icon: BookOpen, label: "All Languages", color: "text-cyber-purple" },
            ].map((item) => (
              <Link key={item.label} to={item.to} className="group flex flex-col items-center gap-2 rounded-xl border border-cyber-purple/20 bg-cyber-purple/5 p-3 hover:bg-cyber-purple/10 transition-all">
                <item.icon size={18} className={`${item.color} group-hover:scale-110 transition-transform`} />
                <span className="text-[10px] font-mono text-slate-300 text-center leading-tight group-hover:text-white transition-colors">{item.label}</span>
              </Link>
            ))}
          </div>
        </section>

        <section className="rounded-2xl border border-white/10 bg-white border-border shadow-card p-5">
          <h2 className="text-lg font-display font-bold uppercase tracking-wider text-white mb-4">More Learning Paths</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {[
              { to: "/interview", icon: Play, label: "Mock Interviews", color: "text-brand-lavender" },
              { to: "/resume", icon: FileText, label: "Resume Builder", color: "text-brand-teal" },
              { to: "/ats", icon: FileText, label: "ATS Optimizer", color: "text-brand-amber" },
              { to: "/aptitude", icon: Target, label: "Aptitude Tests", color: "text-brand-coral" },
              { to: "/company-prep", icon: GraduationCap, label: "Company Prep", color: "text-brand-sky" },
              { to: "/system-design", icon: GitBranch, label: "System Design", color: "text-brand-lavender" },
              { to: "/question-bank", icon: ListChecks, label: "Question Bank", color: "text-brand-emerald" },
              { to: "/coding", icon: Code2, label: "Coding Challenges", color: "text-brand-coral" },
              { to: "/compiler", icon: Code2, label: "Full Compiler", color: "text-cyber-blue" },
              { to: "/daily-challenge", icon: CalendarCheck, label: "Daily Challenge", color: "text-brand-coral" },
              { to: "/playground", icon: Rocket, label: "Code Playground", color: "text-cyber-purple" },
              { to: "/scrims", icon: Play, label: "Scrims", color: "text-brand-sky" },
            ].map((item) => (
              <Link key={item.label} to={item.to} className="group flex flex-col items-center gap-2 rounded-xl border border-white/10 bg-white border-border shadow-card p-3 hover:bg-white border-border/10 transition-all">
                <item.icon size={18} className={`${item.color} group-hover:scale-110 transition-transform`} />
                <span className="text-[10px] font-mono text-slate-300 text-center leading-tight group-hover:text-white transition-colors">{item.label}</span>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

function StatChip({ label, value }: { label: string; value: any }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white border-border/10 px-3 py-4 text-center">
      <div className="text-2xl font-black text-white">{value}</div>
      <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-slate-300">{label}</div>
    </div>
  );
}
