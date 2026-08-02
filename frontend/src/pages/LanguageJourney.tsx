import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft, CheckCircle2, Lock, Crown, Star, Zap,
  ChevronRight
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";

function DifficultyStars({ difficulty }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3].map(d => (
        <Star key={d} size={10} className={d <= difficulty ? "text-yellow-400 fill-yellow-400" : "text-gray-600"} />
      ))}
    </div>
  );
}

function TypeBadge({ type }) {
  const styles = {
    theory: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    practice: "bg-green-500/10 text-green-400 border-green-500/20",
    quiz: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    challenge: "bg-orange-500/10 text-orange-400 border-orange-500/20",
    project: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20",
    boss: "bg-red-500/10 text-red-400 border-red-500/20",
  };
  const labels = {
    theory: "Learn", practice: "Code", quiz: "Quiz",
    challenge: "Solve", project: "Build", boss: "Boss",
  };
  return (
    <span className={`text-[10px] px-1.5 py-0.5 rounded-full border font-mono ${styles[type] || styles.theory}`}>
      {labels[type] || type}
    </span>
  );
}

export default function LanguageJourney() {
  const { languageId } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [expandedLevel, setExpandedLevel] = useState(null);

  useEffect(() => {
    setLoading(true);
    api.get(`/api/learning/${languageId}/levels`)
      .then(d => {
        setData(d);
        // Auto-expand first incomplete level
        const incomplete = d.levels.find(l => l.progress_pct < 100);
        if (incomplete) setExpandedLevel(incomplete.id);
        else if (d.levels.length > 0) setExpandedLevel(d.levels[d.levels.length - 1].id);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [languageId]);

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;
  if (!data) return <div className="min-h-screen flex items-center justify-center text-gray-400">Not found</div>;

  const questTotals = data.levels.reduce(
    (acc, level) => {
      acc.practice += level.practice_lessons || 0;
      acc.challenge += level.challenge_lessons || 0;
      acc.project += level.project_lessons || 0;
      return acc;
    },
    { practice: 0, challenge: 0, project: 0 }
  );

  return (
    <div className="relative min-h-screen px-4 py-8">
      <ArcadeBackdrop variant={languageId === "python" ? "candy" : "dojo"} />
      <div className="relative z-10 mx-auto max-w-4xl">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <Link to="/learn" className="inline-flex items-center gap-2 text-gray-400 hover:text-text-primary transition-colors text-sm font-mono mb-4">
          <ArrowLeft size={14} /> All Languages
        </Link>
        <div className="flex items-center gap-4">
          <span className="text-4xl">{data.language.icon}</span>
          <div>
            <h1 className="text-3xl font-display font-black text-text-primary">{data.language.name}</h1>
            <div className="flex items-center gap-4 mt-1">
              <span className="text-sm font-mono text-gray-400">{data.total_xp} XP</span>
              <span className="text-sm font-mono text-gray-400">
                {data.levels.reduce((a, l) => a + l.lessons_completed, 0)} / {data.levels.reduce((a, l) => a + l.total_lessons, 0)} lessons
              </span>
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              <span className="quest-chip bg-brand-teal-pale text-brand-teal">{questTotals.practice} practice</span>
              <span className="quest-chip bg-brand-lavender-pale text-brand-lavender">{questTotals.challenge} challenges</span>
              <span className="quest-chip bg-brand-coral-pale text-brand-coral">{questTotals.project} projects</span>
              <span className="quest-chip bg-white/10 text-white">{questTotals.practice + questTotals.challenge + questTotals.project} total quests</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Candy Crush Level Grid — Hexagonal Layout */}
      <div className="relative">
        {/* Vertical connector line */}
        <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-green-500/30 via-yellow-500/30 to-red-500/30 -translate-x-1/2 hidden md:block" />

        <div className="space-y-4 md:space-y-6">
          {data.levels.map((level, i) => {
            const isExpanded = expandedLevel === level.id;
            const allDone = level.progress_pct === 100;
            const hasProgress = level.progress_pct > 0;
            const isLocked = !hasProgress && !allDone && i > 0 && data.levels[i - 1]?.progress_pct < 100;

            return (
              <motion.div key={level.id}
                initial={{ opacity: 0, x: i % 2 === 0 ? -20 : 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}>

                {/* Level Node — Hexagonal style */}
                <div className={`flex ${i % 2 === 0 ? "md:justify-start" : "md:justify-end"} justify-center`}>
                  <button onClick={() => !isLocked && setExpandedLevel(isExpanded ? null : level.id)}
                    disabled={isLocked}
                    className={`relative group w-full md:w-96`}>
                    <div className={`rounded-2xl border-2 p-4 transition-all duration-300 ${
                      allDone
                        ? "border-green-500/40 bg-green-500/[0.05] shadow-lg shadow-green-500/10"
                        : hasProgress
                        ? `${level.border || "border-cyber-blue/30"} bg-gradient-to-r ${level.bg || "from-cyber-blue/5 to-cyan-500/5"} shadow-lg`
                        : isLocked
                        ? "border-white/5 bg-white/[0.02] opacity-50 cursor-not-allowed"
                        : "border-white/10 bg-white/[0.03] hover:border-cyber-blue/30 hover:shadow-lg hover:shadow-cyber-blue/5"
                    }`}>
                      <div className="flex items-center gap-4">
                        {/* Level Number Circle */}
                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 text-lg font-display font-black ${
                          allDone ? "bg-green-500/20 text-green-400" :
                          hasProgress ? "bg-cyber-blue/20 text-cyber-blue" :
                          isLocked ? "bg-white/5 text-gray-600" :
                          "bg-white/10 text-gray-400 group-hover:bg-cyber-blue/10 group-hover:text-cyber-blue"
                        }`}>
                          {allDone ? <CheckCircle2 size={24} /> : isLocked ? <Lock size={18} /> : level.emoji || (i + 1)}
                        </div>

                        {/* Level Info */}
                        <div className="flex-1 text-left">
                          <div className="flex items-center gap-2">
                            <span className="text-[10px] font-mono text-gray-500 uppercase">Level {i + 1}</span>
                            {allDone && <span className="text-[10px] font-mono text-green-400">COMPLETE</span>}
                          </div>
                          <p className="font-display font-bold text-white text-sm">{level.name}</p>
                          <p className="text-xs text-gray-500 font-mono">{level.total_lessons} lessons · {level.total_xp} XP</p>
                        </div>

                        {/* Progress */}
                        <div className="text-right shrink-0">
                          <div className="w-16 h-1.5 bg-white/5 rounded-full overflow-hidden mb-1">
                            <div className={`h-full rounded-full transition-all duration-500 ${
                              allDone ? "bg-green-500" : "bg-cyber-blue"
                            }`} style={{ width: `${level.progress_pct}%` }} />
                          </div>
                          <span className="text-[10px] font-mono text-gray-500">{level.progress_pct}%</span>
                        </div>
                      </div>
                    </div>
                  </button>
                </div>

                {/* Expanded Lesson List */}
                {isExpanded && (
                  <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className={`${i % 2 === 0 ? "md:ml-16 md:mr-auto" : "md:mr-16 md:ml-auto"} w-full md:w-96 mx-auto mt-2`}>
                    <LessonPanel languageId={languageId} level={level} />
                  </motion.div>
                )}
              </motion.div>
            );
          })}
        </div>
      </div>
      </div>
    </div>
  );
}

function LessonPanel({ languageId, level }) {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.get(`/api/learning/${languageId}/${level.id}/lessons`)
      .then(d => setLessons(d.lessons))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [languageId, level.id]);

  if (loading) return <div className="p-4 glass rounded-xl"><Spinner /></div>;
  if (!lessons.length) return null;

  // Group lessons
  const groups = [];
  let current = null;
  for (const l of lessons) {
    if (!current || current.type !== l.type) {
      current = { type: l.type, lessons: [] };
      groups.push(current);
    }
    current.lessons.push(l);
  }

  return (
    <div className="glass rounded-xl p-4 space-y-3">
      {groups.map((group, gi) => (
        <div key={gi}>
          <TypeBadge type={group.type} />
          <div className="mt-2 space-y-1">
            {group.lessons.map((lesson, li) => (
              <LessonRow key={lesson.id} lesson={lesson} languageId={languageId} levelId={level.id} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function LessonRow({ lesson, languageId, levelId }) {
  const isBoss = lesson.type === "boss";
  const isProject = lesson.type === "project";

  if (!lesson.unlocked) {
    return (
      <div className="flex items-center gap-2 p-2 rounded-lg bg-white/[0.01] opacity-30">
        <Lock size={12} className="text-gray-600 shrink-0" />
        <span className="text-xs font-mono text-gray-600 truncate flex-1">{lesson.title}</span>
        <DifficultyStars difficulty={lesson.difficulty || 1} />
        <span className="text-[10px] font-mono text-gray-600">+{lesson.xp}</span>
      </div>
    );
  }

  return (
    <Link to={`/learn/${languageId}/${levelId}/${lesson.id}`}>
      <div className={`flex items-center gap-2 p-2 rounded-lg transition-all cursor-pointer group ${
        lesson.completed
          ? "bg-green-500/[0.05] hover:bg-green-500/10"
          : isBoss
          ? "bg-red-500/[0.05] hover:bg-red-500/10 border border-red-500/20"
          : isProject
          ? "bg-cyan-500/[0.05] hover:bg-cyan-500/10 border border-cyan-500/20"
          : "hover:bg-cyber-blue/[0.05]"
      }`}>
        {lesson.completed ? (
          <CheckCircle2 size={14} className="text-green-400 shrink-0" />
        ) : isBoss ? (
          <Crown size={14} className="text-red-400 shrink-0" />
        ) : isProject ? (
          <span className="text-sm shrink-0">🔨</span>
        ) : (
          <span className="w-3.5 h-3.5 rounded-full border border-gray-600 shrink-0" />
        )}
        <span className={`text-xs font-mono truncate flex-1 ${
          lesson.completed ? "text-green-300" : isBoss ? "text-red-300" : "text-gray-300"
        }`}>
          {lesson.title}
        </span>
        <DifficultyStars difficulty={lesson.difficulty || 1} />
        <span className="text-[10px] font-mono text-yellow-400/70 shrink-0">+{lesson.xp}</span>
        <ChevronRight size={12} className="text-gray-600 group-hover:text-gray-400 shrink-0" />
      </div>
    </Link>
  );
}
