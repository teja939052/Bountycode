import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { tracksApi } from "../services/api";
import type { TrackOverview, TrackBrief } from "../services/api/tracks.ts";
import {
  ArrowLeft, Clock, Building2, CheckCircle, ChevronRight, Target,
  Terminal, BookOpen, ShieldCheck, ListOrdered,
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

const COMPANY_META: Record<string, { label: string; color: string; intro: string; tips: string[] }> = {
  tcs: {
    label: "TCS",
    color: "from-blue-500 to-indigo-600",
    intro:
      "TCS National Qualifier Test (NQT) screens freshers for TCS hiring across IT, digital and ninja roles. The Computer Based Test runs ~190 minutes: a Foundation stage (numerical, reasoning, verbal) and an Advanced stage (programming MCQs plus two coding problems).",
    tips: ["Aim for ~150+ in the Foundation stage — it sets your role band.", "Speed matters: ~40s per quantitative question.", "Two coding problems are often 1 easy + 1 medium — both solvable with loops and hashing."],
  },
  infosys: {
    label: "Infosys",
    color: "from-orange-500 to-amber-600",
    intro:
      "Infosys InfyTQ is the certification-cum-hiring exam for Infosys. The ~180-minute test pairs an Aptitude & Logic stage with Programming MCQs and three coding problems, with scores determining your Infosys System Engineer vs Specialist badge.",
    tips: ["Coding weight is heavy — practice 2+ problems daily.", "Data interpretation tables recur in the aptitude stage.", "Clean, style-compliant code scores better in the evaluator."],
  },
  wipro: {
    label: "Wipro",
    color: "from-red-500 to-rose-600",
    intro:
      "Wipro NLTH (National Level Talent Hunt) is Wipro's ~96-minute onboarding assessment: an aptitude + logical stage, an English stage, and two coding problems. Your performance tiers you into Project Engineer roles.",
    tips: ["English is a full dedicated stage — drill grammar & comprehension.", "Coding is only 60 minutes for two problems — keep templates ready.", "Negative marking is not introduced; answer everything you can."],
  },
  accenture: {
    label: "Accenture",
    color: "from-purple-500 to-fuchsia-600",
    intro:
      "Accenture's cognitive-cum-coding assessment (~90 minutes) is the AMCAT-style filter used for entry-level roles: numerical, logical and verbal reasoning, followed by two coding problems for the Application/Software engineer track.",
    tips: ["Cognitive section is the biggest gate — 25 questions per block.", "Attempt coding last; optimize for speed over elegance.", "Practice 2-sum, string and array problems — most repeated shapes."],
  },
  cognizant: {
    label: "Cognizant",
    color: "from-teal-500 to-emerald-600",
    intro:
      "Cognizant GenC is the primary fresher pathway. Its ~90-minute assessment covers aptitude, logical and verbal reasoning plus an online coding round, with performance determining GenC vs GenC Pro placement.",
    tips: ["GenC Pro needs stronger coding — target 3+ medium problems.", "Aptitude speed is the differentiator — drill 60-second mental math.", "Reuse verified pattern-relevant stock to cover topic breadth."],
  },
};

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
  medium: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400",
  hard: "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400",
};

const STATUS_STYLES: Record<string, string> = {
  not_started: "bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400",
  attempted: "bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400",
  solved: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
};

export default function CompanyTrack() {
  const { company = "tcs" } = useParams();
  const reduced = useReducedMotion();
  const meta = COMPANY_META[company] || {
    label: company.toUpperCase(),
    color: "from-gray-500 to-gray-700",
    intro: "",
    tips: [],
  };

  const [data, setData] = useState<TrackOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    tracksApi
      .overview(company)
      .then((res) => {
        if (active) setData(res);
      })
      .catch(() => {
        if (active) setError("Could not load this company track.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [company]);

  if (loading) {
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-5xl mx-auto space-y-4">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3 animate-pulse" />
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-5 bg-gray-200 dark:bg-gray-700 rounded w-2/3 mb-2" />
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  const structure = data?.structure;
  const foundationCount = data
    ? data.foundation.sections.reduce((n, s) => n + s.practice_count, 0)
    : 0;
  const advanced = data?.advanced_coding;
  const advancedSolved = advanced?.solved || 0;
  const totalSolvedAcross = advancedSolved; // foundation practice are samples; solved tracked per problem

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-5xl mx-auto">
        <Link
          to="/company-prep"
          className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-primary-600 mb-6 transition-colors"
        >
          <ArrowLeft size={16} />
          Company Prep
        </Link>

        {error ? (
          <div className="card text-center py-12 text-gray-500 dark:text-gray-400">{error}</div>
        ) : (
          <div className="space-y-8">
            {/* Header */}
            <motion.div
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex items-center gap-4 mb-3">
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${meta.color} flex items-center justify-center text-white font-black text-lg`}>
                  {meta.label.slice(0, 2).toUpperCase()}
                </div>
                <div>
                  <h1 className="text-3xl font-bold dark:text-white">
                    {meta.label} Placement Track
                  </h1>
                  <p className="text-gray-500 dark:text-gray-400 text-sm">
                    {structure ? structure.title : `${meta.label} interview prep`}
                  </p>
                </div>
              </div>

              {structure && (
                <div className="flex flex-wrap gap-3 text-sm text-gray-600 dark:text-gray-400">
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800">
                    <Clock size={14} /> {structure.duration_minutes} min
                  </span>
                  {structure.stages.map((s) => (
                    <span key={s.id} className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800">
                      <ListOrdered size={14} /> {s.title}
                    </span>
                  ))}
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400">
                    <ShieldCheck size={14} /> Verified-only bank
                  </span>
                </div>
              )}

              {data?.verified_only && (
                <p className="mt-3 text-xs text-gray-400">{data.provenance_note}</p>
              )}

              {/* CTA */}
              <div className="mt-5 flex flex-wrap gap-3">
                <Link
                  to="/mock-oa"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary-600 to-primary-500 text-white font-semibold hover:from-primary-500 hover:to-primary-400 transition-all shadow-lg shadow-primary-500/20"
                >
                  Start Mock OA <ChevronRight size={16} />
                </Link>
                <Link
                  to="/daily-challenge"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-semibold hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                >
                  Daily Challenge
                </Link>
              </div>
            </motion.div>

            {/* Readiness */}
            {data?.readiness && (
              <motion.section
                className="card p-6"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className="flex items-center gap-4 flex-wrap">
                  <div className="shrink-0">
                    <div className="relative w-28 h-28">
                      <svg viewBox="0 0 36 36" className="w-28 h-28 -rotate-90">
                        <circle cx="18" cy="18" r="15.9" fill="none" stroke="currentColor" className="text-gray-200 dark:text-gray-700" strokeWidth="3" />
                        <motion.circle
                          cx="18"
                          cy="18"
                          r="15.9"
                          fill="none"
                          stroke="currentColor"
                          className="text-primary-500"
                          strokeWidth="3"
                          strokeLinecap="round"
                          strokeDasharray={`${(data.readiness.overall_percent / 100) * 100} 100`}
                          initial={{ strokeDasharray: "0 100" }}
                          animate={{ strokeDasharray: `${(data.readiness.overall_percent / 100) * 100} 100` }}
                          transition={{ duration: 0.8, ease: "easeOut" }}
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-2xl font-black dark:text-white">{data.readiness.overall_percent}%</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex-1 min-w-64">
                    <h2 className="text-xl font-bold dark:text-white">
                      You are {data.readiness.overall_percent}% of the way to {meta.label} readiness
                    </h2>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      Foundation {data.readiness.foundation.solved}/{data.readiness.foundation.total} · Coding{" "}
                      {data.readiness.coding.solved}/{data.readiness.coding.total} — progress is read live from your
                      solved and attempted questions.
                    </p>
                    <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {data.readiness.sections.map((s) => (
                        <div key={s.section} className="rounded-lg bg-gray-50 dark:bg-gray-900/50 p-3">
                          <div className="flex items-center justify-between text-xs mb-1">
                            <span className={`font-medium ${s.section === data.readiness.weakest_section ? "text-amber-600 dark:text-amber-400" : "text-gray-600 dark:text-gray-300"}`}>
                              {s.title}
                              {s.section === data.readiness.weakest_section && s.total > 0 && (
                                <span className="ml-1.5 text-[10px] font-mono uppercase tracking-wide">focus area</span>
                              )}
                            </span>
                            <span className="text-gray-400">{s.percent}% · {s.solved}/{s.total}</span>
                          </div>
                          <div className="h-1.5 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
                            <div
                              className={`h-full rounded-full transition-all duration-500 ${
                                s.section === data.readiness.weakest_section ? "bg-amber-500" : "bg-primary-500"
                              }`}
                              style={{ width: `${s.percent}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Next action + repair CTA */}
                <div className="mt-5 flex flex-wrap gap-3">
                  {data.readiness.next_up_id && (
                    <Link
                      to={`/solve/${data.readiness.next_up_id}`}
                      className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-white font-semibold text-sm bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400 transition-all shadow-lg shadow-primary-500/20"
                    >
                      <BookOpen size={15} /> Next unsolved problem <ChevronRight size={15} />
                    </Link>
                  )}
                  {data.readiness.weakest_section && (
                    (() => {
                      const sec = data.foundation.sections.find((x) => x.section === data.readiness.weakest_section);
                      const topic = sec?.topics?.[0]?.topic;
                      return topic ? (
                        <Link
                          to={`/problems/${encodeURIComponent(topic)}`}
                          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-amber-700 dark:text-amber-300 font-semibold text-sm bg-amber-100 dark:bg-amber-900/30 hover:bg-amber-200 dark:hover:bg-amber-900/50 transition-colors"
                        >
                          <Target size={15} /> Repair {data.readiness.weakest_title || "weakest section"}
                        </Link>
                      ) : null;
                    })()
                  )}
                  <Link
                    to="/mock-oa"
                    className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-white font-semibold text-sm bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 transition-all shadow-lg shadow-emerald-500/20"
                  >
                    Take the Mock OA <ChevronRight size={15} />
                  </Link>
                </div>
              </motion.section>
            )}

            {/* Stats */}
            <motion.div
              className="grid grid-cols-1 sm:grid-cols-3 gap-3"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="card p-4">
                <div className="text-2xl font-bold text-primary-600">{foundationCount}</div>
                <div className="text-xs text-gray-500">Foundation practice samples</div>
              </div>
              <div className="card p-4">
                <div className="text-2xl font-bold text-indigo-500">{advanced?.total || 0}</div>
                <div className="text-xs text-gray-500">Advanced coding problems</div>
              </div>
              <div className="card p-4">
                <div className="text-2xl font-bold text-green-500">{totalSolvedAcross}</div>
                <div className="text-xs text-gray-500">Solving across this track</div>
              </div>
            </motion.div>

            {meta.intro && (
              <motion.div
                className="card p-6"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h2 className="flex items-center gap-2 text-lg font-bold dark:text-white mb-2">
                  <Building2 size={18} className="text-primary-500" /> About this exam
                </h2>
                <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{meta.intro}</p>
                <ul className="mt-3 space-y-1.5">
                  {meta.tips.map((tip, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-400">
                      <Target size={14} className="mt-0.5 shrink-0 text-primary-500" /> {tip}
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}

            {/* Foundation sections */}
            {data && data.foundation.sections.length > 0 && (
              <motion.section
                className="space-y-5"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h2 className="flex items-center gap-2 text-xl font-bold dark:text-white">
                  <BookOpen size={18} className="text-primary-500" /> Foundation Practice
                </h2>
                {data.foundation.sections.map((section) => (
                  <div key={section.section} className="card p-5">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-bold dark:text-white">{section.title}</h3>
                      <span className="text-xs text-gray-500">{section.practice_count} practice questions</span>
                    </div>
                    {section.topics.length > 0 && (
                      <div className="flex flex-wrap gap-1.5 mb-3">
                        {section.topics.slice(0, 8).map((t) => (
                          <span key={t.topic} className="px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800 text-xs text-gray-500 dark:text-gray-400">
                            {t.topic} · {t.count}
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="space-y-2">
                      {section.practice.map((p: TrackBrief) => (
                        <div key={p.id} className="flex items-center gap-3 text-sm border-t border-border dark:border-gray-700 pt-2">
                          <Link
                            to={`/solve/${p.id}`}
                            className="flex-1 min-w-0 truncate font-medium text-gray-700 dark:text-gray-300 hover:text-primary-600 transition-colors"
                          >
                            {p.title}
                          </Link>
                          <span className={`px-2 py-0.5 rounded-full text-xs ${DIFFICULTY_COLORS[p.difficulty] || ""}`}>
                            {p.difficulty}
                          </span>
                          <span className={`px-2 py-0.5 rounded-full text-xs ${STATUS_STYLES[p.status] || ""}`}>
                            {p.status === "not_started" ? "Not Started" : p.status === "attempted" ? "Attempted" : "Solved"}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </motion.section>
            )}

            {/* Advanced coding */}
            {advanced && advanced.problems.length > 0 && (
              <motion.section
                className="card p-6"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className="flex items-center justify-between mb-4">
                  <h2 className="flex items-center gap-2 text-lg font-bold dark:text-white">
                    <Terminal size={18} className="text-primary-500" /> Advanced Coding Bank
                  </h2>
                  <span className="text-xs text-gray-500">{advanced.solved}/{advanced.total} solved</span>
                </div>
                <div className="space-y-2">
                  {advanced.problems.map((p: TrackBrief, i: number) => (
                    <div key={p.id} className="flex items-center gap-3 py-2 border-t border-border dark:border-gray-700 first:border-0">
                      <span className="w-6 text-center text-sm text-gray-400">{i + 1}</span>
                      <Link
                        to={`/solve/${p.id}`}
                        className="flex-1 min-w-0 truncate font-medium text-gray-700 dark:text-gray-300 hover:text-primary-600 transition-colors"
                      >
                        {p.title}
                      </Link>
                      <span className={`px-2 py-0.5 rounded-full text-xs ${DIFFICULTY_COLORS[p.difficulty] || ""}`}>
                        {p.difficulty}
                      </span>
                      {p.companies.length > 0 && (
                        <span className="hidden sm:inline text-xs text-gray-400 flex items-center gap-1">
                          <Building2 size={10} /> {p.companies[0]}
                        </span>
                      )}
                      {p.status === "solved" && <CheckCircle size={16} className="text-green-500 shrink-0" />}
                      <span className={`px-2 py-0.5 rounded-full text-xs ${STATUS_STYLES[p.status] || ""}`}>
                        {p.status === "not_started" ? "Not Started" : p.status === "attempted" ? "Attempted" : "Solved"}
                      </span>
                    </div>
                  ))}
                </div>
              </motion.section>
            )}
          </div>
        )}
      </div>
    </div>
  );
}