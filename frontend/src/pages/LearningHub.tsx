import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import {
  BookOpen,
  ChevronRight,
  Crown,
  Flame,
  Sparkles,
  Target,
  Trophy,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";

function ProgressRing({ pct, size = 64, stroke = 4, color = "#3B82F6" }) {
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (pct / 100) * circ;

  return (
    <svg width={size} height={size} className="rotate-[-90deg]">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.10)" strokeWidth={stroke} />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke={color}
        strokeWidth={stroke}
        strokeDasharray={circ}
        strokeDashoffset={offset}
        strokeLinecap="round"
        className="transition-all duration-1000 ease-out"
      />
    </svg>
  );
}

function DailyGoalCard({ daily, streak }) {
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

      <div className="mt-4 h-3 rounded-full bg-gray-100 overflow-hidden">
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

function LeaderboardPreview({ leaderboard }) {
  if (!leaderboard || leaderboard.length === 0) return null;

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="arena-card p-5">
      <h3 className="mb-3 flex items-center gap-2 font-display font-bold text-text-primary">
        <Trophy size={18} className="text-brand-gold" />
        Top Learners
      </h3>
      <div className="space-y-2">
        {leaderboard.slice(0, 5).map((entry, index) => (
          <div key={entry.user_id} className="flex items-center gap-3 rounded-xl bg-gray-50 px-3 py-2">
            <span
              className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold ${
                index === 0
                  ? "bg-yellow-100 text-yellow-600"
                  : index === 1
                  ? "bg-gray-200 text-gray-600"
                  : index === 2
                  ? "bg-orange-100 text-orange-600"
                  : "bg-gray-100 text-gray-500"
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
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [leaderboard, setLeaderboard] = useState(null);

  useEffect(() => {
    Promise.all([
      api.get("/api/v1/learning/languages"),
      api.get("/api/v1/learning/leaderboard").catch(() => null),
    ])
      .then(([langData, lbData]) => {
        setData(langData);
        if (lbData) setLeaderboard(lbData.leaderboard);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center text-text-muted">
        Failed to load
      </div>
    );
  }

  const questTotals = data.languages.reduce(
    (acc, lang) => {
      acc.practice += lang.practice_lessons || 0;
      acc.challenge += lang.challenge_lessons || 0;
      acc.project += lang.project_lessons || 0;
      acc.quest += lang.quest_lessons || 0;
      return acc;
    },
    { practice: 0, challenge: 0, project: 0, quest: 0 }
  );

  const languageColors = {
    c: { ring: "#6B7280", accent: "from-slate-500 to-slate-300" },
    cpp: { ring: "#3B82F6", accent: "from-brand-sky to-cyan-300" },
    java: { ring: "#F97316", accent: "from-orange-500 to-amber-300" },
    python: { ring: "#22C55E", accent: "from-emerald-500 to-lime-300" },
  };

  return (
    <div className="relative min-h-screen px-4 py-6 md:py-8">
      <ArcadeBackdrop variant="arcade" />
      <div className="relative z-10 mx-auto max-w-7xl space-y-6">
        <motion.section initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} className="hero-shell p-6 md:p-8 text-white">
          <div className="relative z-10 flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <span className="section-kicker border-white/10 bg-white/10 text-white">
                <BookOpen size={12} />
                Learning hub
              </span>
              <h1 className="mt-4 text-3xl font-black tracking-tight text-white md:text-5xl">
                Master C, C++, Java, and Python like a ranked campaign
              </h1>
              <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-200 md:text-base">
                Lessons, challenges, projects, and boss battles in one progression loop. Pick a language, climb the tree, and keep the streak alive.
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
              <span className="quest-chip bg-white/10 text-white">{questTotals.quest} total quests</span>
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
            <Sparkles size={18} className="text-brand-sky" />
            <h2 className="text-lg font-display font-bold uppercase tracking-wider text-text-primary">Language campaigns</h2>
          </div>

          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
            {data.languages.map((lang) => {
              const color = languageColors[lang.id] || languageColors.c;
              const hasProgress = lang.lessons_completed > 0;

              return (
                <motion.div key={lang.id} whileHover={{ y: -4 }} className="group">
                  <Link to={`/learn/${lang.id}`} className="block h-full">
                    <div className="arena-card h-full p-5">
                      <div className="flex items-start justify-between gap-3">
                        <div className={`flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br ${color.accent} text-3xl shadow-soft-md`}>
                          {lang.icon}
                        </div>
                        {hasProgress && (
                          <span className="quest-chip bg-brand-teal-pale text-brand-teal">
                            In progress
                          </span>
                        )}
                      </div>

                      <h2 className="mt-4 text-2xl font-display font-black text-text-primary">{lang.name}</h2>
                      <p className="mt-2 text-sm leading-6 text-text-muted">{lang.description}</p>

                      <div className="mt-4 flex flex-wrap gap-2">
                        <span className="quest-chip bg-brand-teal-pale text-brand-teal">
                          {lang.practice_lessons} practice
                        </span>
                        <span className="quest-chip bg-brand-lavender-pale text-brand-lavender">
                          {lang.challenge_lessons} challenges
                        </span>
                        <span className="quest-chip bg-brand-coral-pale text-brand-coral">
                          {lang.project_lessons} projects
                        </span>
                      </div>

                      <div className="mt-5 flex items-center gap-4">
                        <div className="relative">
                          <ProgressRing pct={lang.progress_pct} size={54} stroke={3} color={color.ring} />
                          <div className="absolute inset-0 flex items-center justify-center">
                            <span className="text-xs font-mono font-bold text-text-primary">{lang.progress_pct}%</span>
                          </div>
                        </div>
                        <div className="min-w-0 flex-1">
                          <p className="text-sm font-mono text-text-primary">
                            {lang.lessons_completed} / {lang.total_lessons} lessons
                          </p>
                          <p className="text-xs font-mono text-text-light mt-1">{lang.total_xp} XP earned</p>
                        </div>
                        <ChevronRight size={18} className="text-text-light transition-transform group-hover:translate-x-1" />
                      </div>
                    </div>
                  </Link>
                </motion.div>
              );
            })}
          </div>
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
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-gold text-white">
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
      </div>
    </div>
  );
}

function StatChip({ label, value }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/10 px-3 py-4 text-center backdrop-blur-md">
      <div className="text-2xl font-black text-white">{value}</div>
      <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-slate-300">{label}</div>
    </div>
  );
}
