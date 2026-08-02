import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link } from "react-router-dom";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import useReducedMotion from "../hooks/useReducedMotion";
import {
  Compass, Trophy, Clock, Sparkles, ChevronRight,
  BookOpen, Target, Zap, Star, ArrowRight,
  GraduationCap, Route, Sword, Brain, Puzzle,
  Globe, Server, Gamepad2, BarChart3, Cpu
} from "lucide-react";

const ICON_MAP = {
  "🌐": Globe, "📊": BarChart3, "🤖": Cpu,
  "💻": Monitor, "🕹️": Gamepad2, "🎯": Target,
  "👑": Trophy, "⚙️": Server,
};

function Monitor(props) {
  return (
    <svg {...props} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
      <line x1="8" y1="21" x2="16" y2="21" />
      <line x1="12" y1="17" x2="12" y2="21" />
    </svg>
  );
}

const DIFFICULTY_BADGES = {
  "Beginner": "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
  "Beginner to Advanced": "bg-gradient-to-r from-emerald-500/15 to-blue-500/15 text-transparent bg-clip-text border-blue-500/30",
  "Beginner to Intermediate": "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
  "Intermediate": "bg-amber-500/15 text-amber-400 border-amber-500/30",
  "Intermediate to Advanced": "bg-amber-500/15 text-amber-400 border-amber-500/30",
  "Advanced": "bg-red-500/15 text-red-400 border-red-500/30",
  "Beginner to Expert": "bg-gradient-to-r from-emerald-500/15 via-amber-500/15 to-red-500/15 text-transparent bg-clip-text border-purple-500/30",
};

export default function LearningJourneys() {
  const store = useAuthStore();
  const reduced = useReducedMotion();
  const [journeys, setJourneys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedJourney, setSelectedJourney] = useState(null);
  const [journeyDetail, setJourneyDetail] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => { loadJourneys(); }, []);

  const loadJourneys = async () => {
    setLoading(true); setError(null);
    try {
      const data = await api.getLearningJourneys();
      setJourneys(data.journeys || []);
    } catch (err) {
      setError("Failed to load learning journeys.");
    } finally {
      setLoading(false);
    }
  };

  const loadJourneyDetail = async (journeyId) => {
    setDetailLoading(true); setSelectedJourney(journeyId);
    try {
      const data = await api.getJourneyDetail(journeyId);
      setJourneyDetail(data);
    } catch (err) {
      setJourneyDetail(null);
    } finally {
      setDetailLoading(false);
    }
  };

  const closeDetail = () => { setSelectedJourney(null); setJourneyDetail(null); };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0a0a0f]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
          <span className="text-sm font-mono text-slate-400">Loading journeys...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0a0a0f]">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <button onClick={loadJourneys} className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm">Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-slate-100">
      <div className="max-w-7xl mx-auto px-4 py-8 md:py-12">
        <motion.div initial={reduced ? {} : { opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-10">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-2xl border border-indigo-500/30">
              <Route className="w-7 h-7 text-indigo-400" />
            </div>
            <div>
              <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-white via-indigo-200 to-purple-200 bg-clip-text text-transparent">
                Learning Journeys
              </h1>
              <p className="text-slate-400 text-sm mt-1">
                Curated paths to guide you from beginner to job-ready
              </p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 mt-4">
            {["All", "Beginner", "Intermediate", "Advanced"].map((filter) => (
              <button key={filter} className="px-3 py-1.5 text-xs font-medium rounded-full bg-slate-800/50 border border-slate-700/50 text-slate-300 hover:bg-slate-700/50 transition-colors">
                {filter}
              </button>
            ))}
          </div>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {journeys.map((journey, idx) => {
            const IconComp = ICON_MAP[journey.icon] || Compass;
            return (
              <motion.div
                key={journey.id}
                initial={reduced ? {} : { opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.07, duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                onClick={() => loadJourneyDetail(journey.id)}
                className="group relative cursor-pointer"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${journey.gradient} opacity-[0.03] rounded-2xl group-hover:opacity-[0.06] transition-opacity`} />
                <div className="relative bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 hover:border-slate-700/80 transition-all duration-300 hover:shadow-xl hover:shadow-black/20 hover:-translate-y-0.5">
                  <div className="flex items-start justify-between mb-4">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${journey.gradient} bg-opacity-10 flex items-center justify-center text-2xl shadow-lg`}>
                      <span className="drop-shadow-lg">{journey.icon}</span>
                    </div>
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-semibold border ${DIFFICULTY_BADGES[journey.difficulty] || "bg-slate-800 text-slate-400 border-slate-700"}`}>
                      {journey.difficulty}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-white mb-1.5 group-hover:text-indigo-300 transition-colors">
                    {journey.title}
                  </h3>
                  <p className="text-xs text-slate-400 leading-relaxed mb-4 line-clamp-2">
                    {journey.description}
                  </p>

                  <div className="flex items-center gap-4 text-xs text-slate-500 mb-4">
                    <span className="flex items-center gap-1.5">
                      <BookOpen className="w-3.5 h-3.5 text-indigo-400/60" />
                      {journey.total_lessons} lessons
                    </span>
                    <span className="flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5 text-amber-400/60" />
                      ~{journey.estimated_hours}h
                    </span>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-slate-400">Progress</span>
                      <span className="font-mono text-indigo-400 font-bold">{journey.progress_pct}%</span>
                    </div>
                    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <motion.div
                        className={`h-full rounded-full bg-gradient-to-r ${journey.gradient}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${journey.progress_pct}%` }}
                        transition={{ duration: 0.8, delay: idx * 0.07 + 0.3, ease: "easeOut" }}
                      />
                    </div>
                  </div>

                  <div className="mt-4 pt-4 border-t border-slate-800/50 flex items-center justify-between">
                    <span className="text-[11px] text-slate-500 font-mono">
                      {journey.lessons_completed}/{journey.total_lessons} done
                    </span>
                    <div className="flex items-center gap-1 text-[11px] text-indigo-400 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                      Explore <ChevronRight className="w-3 h-3" />
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      <AnimatePresence>
        {selectedJourney && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={closeDetail}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
              onClick={(e) => e.stopPropagation()}
              className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-y-auto shadow-2xl"
            >
              {detailLoading ? (
                <div className="flex items-center justify-center py-20">
                  <div className="w-8 h-8 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
                </div>
              ) : journeyDetail ? (
                <div className="p-6 md:p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${journeyDetail.gradient} flex items-center justify-center text-3xl shadow-xl shrink-0`}>
                      {journeyDetail.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h2 className="text-2xl font-bold text-white mb-1">{journeyDetail.title}</h2>
                      <p className="text-slate-400 text-sm">{journeyDetail.description}</p>
                      <div className="flex flex-wrap items-center gap-3 mt-3">
                        <span className="flex items-center gap-1.5 text-xs text-slate-500">
                          <BookOpen className="w-3.5 h-3.5" /> {journeyDetail.total_lessons} lessons
                        </span>
                        <span className="flex items-center gap-1.5 text-xs text-slate-500">
                          <Clock className="w-3.5 h-3.5" /> ~{journeyDetail.estimated_hours}h
                        </span>
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-semibold border ${DIFFICULTY_BADGES[journeyDetail.difficulty] || "bg-slate-800 text-slate-400 border-slate-700"}`}>
                          {journeyDetail.difficulty}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-slate-950/50 rounded-xl p-5 mb-6 border border-slate-800/50">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-semibold text-white">Overall Progress</span>
                      <span className="text-lg font-bold font-mono bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                        {journeyDetail.progress_pct}%
                      </span>
                    </div>
                    <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                      <motion.div
                        className={`h-full rounded-full bg-gradient-to-r ${journeyDetail.gradient}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${journeyDetail.progress_pct}%` }}
                        transition={{ duration: 1, ease: "easeOut" }}
                      />
                    </div>
                    <p className="text-xs text-slate-500 mt-2 font-mono">
                      {journeyDetail.lessons_completed} / {journeyDetail.total_lessons} lessons completed
                    </p>
                  </div>

                  {journeyDetail.languages && journeyDetail.languages.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
                        <BookOpen className="w-4 h-4 text-indigo-400" /> Languages in this journey
                      </h3>
                      <div className="space-y-3">
                        {journeyDetail.languages.map((lang) => (
                          <div key={lang.id} className="bg-slate-950/50 rounded-xl p-4 border border-slate-800/50 hover:border-slate-700/50 transition-colors">
                            <div className="flex items-center gap-3 mb-3">
                              <span className="text-xl">{lang.icon}</span>
                              <div className="flex-1 min-w-0">
                                <h4 className="font-semibold text-white text-sm">{lang.name}</h4>
                                <p className="text-xs text-slate-500 font-mono">
                                  {lang.completed_lessons}/{lang.total_lessons} lessons
                                </p>
                              </div>
                              <span className="text-xs font-mono font-bold text-indigo-400">{lang.progress_pct}%</span>
                            </div>
                            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                              <motion.div
                                className={`h-full rounded-full bg-gradient-to-r ${journeyDetail.gradient}`}
                                initial={{ width: 0 }}
                                animate={{ width: `${lang.progress_pct}%` }}
                                transition={{ duration: 0.8, ease: "easeOut" }}
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="mt-8 flex items-center gap-3">
                    <Link
                      to="/learning"
                      className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-medium text-sm transition-colors"
                    >
                      Start Learning <ArrowRight className="w-4 h-4" />
                    </Link>
                    <button
                      onClick={closeDetail}
                      className="px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-sm transition-colors"
                    >
                      Close
                    </button>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-slate-500">Journey not found.</div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
