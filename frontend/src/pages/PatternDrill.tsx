// @ts-nocheck
import { useState, useEffect } from "react";
import { useParams, Link, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  BookOpen,
  Target,
  Trophy,
  Flame,
  ChevronRight,
  AlertTriangle,
} from "lucide-react";
import Spinner from "../components/ui/Spinner";
import api from "../services/api";
import { Mentor } from "../design-system/Mentor";

type Tab = "learn" | "practice" | "test";

type PatternDetail = {
  id: string;
  name: string;
  emoji: string;
  mastery: number;
  attempts: number;
  accuracy: number | null;
  diagnosis: string[];
  question_count: number;
  is_weak: boolean;
  is_lowest: boolean;
  status: string;
  round_id: string;
  round_name: string;
  mission_slug: string;
  why: string;
  company: string;
  pack?: {
    purpose?: string;
    prerequisites?: string[];
    misconceptions?: Array<{ label?: string; description?: string }>;
    teaching?: Array<{ id?: string; type?: string; title?: string; captain_message?: string; render?: Record<string, unknown> }>;
    practice?: {
      warmup?: Array<{ id?: string; question?: string; options?: string[]; answer?: string; explanation?: string }>;
      drill?: Array<{ id?: string; question?: string; options?: string[]; answer?: string; explanation?: string }>;
      speed_run?: Array<{ id?: string; question?: string; options?: string[]; answer?: string; explanation?: string }>;
      weakness_repair?: Array<{ id?: string; question?: string; options?: string[]; answer?: string; explanation?: string; diagnosis_code?: string }>;
    };
    assessment?: Array<{ id?: string; question?: string; options?: string[]; answer?: string; explanation?: string }>;
    retention?: Array<{ due_days?: number; prompt?: string; answer?: string; diagnosis_code?: string }>;
    company_variants?: Array<{ company?: string; timing_seconds?: number; question_count?: number }>;
    interview_transfer?: { prompt?: string; model_answer?: string };
  };
};

export default function PatternDrill() {
  const { id } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const company = searchParams.get("company") || "";
  const [loading, setLoading] = useState(true);
  const [pattern, setPattern] = useState<PatternDetail | null>(null);
  const [tab, setTab] = useState<Tab>("learn");
  const [captain, setCaptain] = useState<{ intro: string; mood: string }>({
    intro: "Loading pattern data...",
    mood: "briefing",
  });

  useEffect(() => {
    if (!id) return;
    load();
  }, [id, company]);

  const load = async () => {
    setLoading(true);
    try {
      const data = await api.campaign.getPattern(id!, company);
      setPattern(data);

      if (data.mastery < 40) {
        setCaptain({
          intro: `🧭 Captain Byte: ${data.emoji} ${data.name} is your weakest link. ${data.diagnosis?.[0] || "Let's repair it."}`,
          mood: "stuck",
        });
      } else if (data.mastery < 70) {
        setCaptain({
          intro: `🧭 Captain Byte: ${data.name} — getting there. ${data.why}`,
          mood: "encouraging",
        });
      } else {
        setCaptain({
          intro: `🧭 Captain Byte: ${data.name} is solid. Test under pressure.`,
          mood: "celebrating",
        });
      }
    } catch {
      setCaptain({
        intro: "Could not load pattern. Try refreshing.",
        mood: "stuck",
      });
    } finally {
      setLoading(false);
    }
  };

  const masteryColor = (m: number) => {
    if (m >= 80) return "text-green-400";
    if (m >= 60) return "text-[#ffa116]";
    if (m >= 40) return "text-yellow-400";
    return "text-red-400";
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );
  }

  if (!pattern) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-400">Pattern not found.</p>
      </div>
    );
  }

  const tabConfig: Record<Tab, { label: string; icon: any; href: string }> = {
    learn: {
      label: "Learn",
      icon: BookOpen,
      href: `/mission/${pattern.mission_slug}`,
    },
    practice: {
      label: "Practice",
      icon: Target,
      href: `/aptitude?category=${encodeURIComponent(pattern.id)}`,
    },
    test: {
      label: "Test",
      icon: Trophy,
      href: `/mock-oa?topic=${encodeURIComponent(pattern.id)}`,
    },
  };

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <div className="mx-auto max-w-3xl px-4 py-6 sm:px-6 lg:px-8 space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-[#2a2a2a] bg-gradient-to-br from-[#1c1c1c] to-[#141414] p-6"
        >
          <Link
            to={`/round/${pattern.round_id}`}
            className="inline-flex items-center gap-1 text-xs text-[#9a9a9a] hover:text-[#ffa116] mb-3"
          >
            <ArrowLeft size={14} />
            Back to {pattern.round_name}
          </Link>
          <div className="flex items-start gap-4">
            <span className="text-4xl">{pattern.emoji}</span>
            <div className="flex-1">
              <h1 className="text-2xl font-bold">{pattern.name}</h1>
              <p className="text-sm text-[#9a9a9a] mt-1">{pattern.round_name}</p>
              <div className="mt-3 flex items-center gap-4">
                <div>
                  <div className="text-xs text-[#9a9a9a]">Mastery</div>
                  <div className={`text-xl font-bold ${masteryColor(pattern.mastery)}`}>
                    {pattern.mastery}%
                  </div>
                </div>
                <div>
                  <div className="text-xs text-[#9a9a9a]">Attempts</div>
                  <div className="text-xl font-bold text-[#e9e9e9]">{pattern.attempts}</div>
                </div>
                <div>
                  <div className="text-xs text-[#9a9a9a]">Questions</div>
                  <div className="text-xl font-bold text-[#e9e9e9]">{pattern.question_count}</div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Why this matters */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-5"
        >
          <div className="flex items-start gap-3">
            <AlertTriangle className="text-[#ffa116] mt-0.5" size={18} />
            <div>
              <h3 className="text-sm font-bold text-[#ffa116]">Why this matters</h3>
              <p className="text-sm text-[#9a9a9a] mt-1">{pattern.why}</p>
              {pattern.diagnosis?.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {pattern.diagnosis.map((d, i) => (
                    <span
                      key={i}
                      className="text-[10px] px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20"
                    >
                      {d}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </motion.div>

        {/* Mastery bar */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-5"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-[#e9e9e9]">What you know</span>
            <span className={`text-sm font-bold ${masteryColor(pattern.mastery)}`}>
              {pattern.mastery}%
            </span>
          </div>
          <div className="w-full h-3 rounded-full bg-[#2a2a2a] overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${Math.max(pattern.mastery, 2)}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className={`h-full rounded-full ${
                pattern.mastery >= 80
                  ? "bg-green-500"
                  : pattern.mastery >= 60
                  ? "bg-[#ffa116]"
                  : pattern.mastery >= 40
                  ? "bg-yellow-500"
                  : "bg-red-500"
              }`}
            />
          </div>
        </motion.div>

        {/* Learn / Practice / Test tabs */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-[#2a2a2a] bg-[#141414] overflow-hidden"
        >
          <div className="flex border-b border-[#2a2a2a]">
            {(["learn", "practice", "test"] as Tab[]).map((t) => {
              const cfg = tabConfig[t];
              const Icon = cfg.icon;
              return (
                <Link
                  key={t}
                  to={cfg.href}
                  className={`flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors ${
                    tab === t
                      ? "text-[#ffa116] border-b-2 border-[#ffa116]"
                      : "text-[#9a9a9a] hover:text-[#e9e9e9]"
                  }`}
                  onClick={() => setTab(t)}
                >
                  <Icon size={16} />
                  {cfg.label}
                  <ChevronRight size={14} />
                </Link>
              );
            })}
          </div>
          <div className="p-5">
            {tab === "learn" && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-bold">Learn {pattern.name}</h3>
                  {pattern.pack?.purpose && (
                    <p className="text-sm text-[#9a9a9a] mt-1">{pattern.pack.purpose}</p>
                  )}
                </div>

                {/* Teaching steps */}
                {pattern.pack?.teaching && pattern.pack.teaching.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="text-xs font-medium uppercase tracking-wider text-[#9a9a9a]">Mission Steps</h4>
                    <div className="flex flex-wrap gap-2">
                      {pattern.pack.teaching.map((step, idx) => (
                        <span
                          key={idx}
                          className="text-xs px-2 py-1 rounded bg-[#1f1f1f] border border-[#2a2a2a] text-[#e9e9e9]"
                        >
                          {step.title || step.type || `Step ${idx + 1}`}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Misconceptions */}
                {pattern.pack?.misconceptions && pattern.pack.misconceptions.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="text-xs font-medium uppercase tracking-wider text-[#ffa116]">Common Traps</h4>
                    <div className="space-y-1">
                      {pattern.pack.misconceptions.slice(0, 3).map((m, i) => (
                        <div key={i} className="text-xs text-[#9a9a9a]">
                          <span className="text-red-400 font-medium">{m.label}:</span> {m.description}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Prerequisites */}
                {pattern.pack?.prerequisites && pattern.pack.prerequisites.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="text-xs font-medium uppercase tracking-wider text-[#9a9a9a]">Prerequisites</h4>
                    <div className="flex flex-wrap gap-2">
                      {pattern.pack.prerequisites.map((prereq, i) => (
                        <span key={i} className="text-xs px-2 py-1 rounded bg-[#242424] text-[#9a9a9a]">
                          {prereq}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex items-center gap-4 text-xs text-[#9a9a9a]">
                  <span className="flex items-center gap-1">
                    <Flame size={14} /> ~12 min
                  </span>
                  <span className="flex items-center gap-1">
                    <Trophy size={14} /> 150 XP
                  </span>
                </div>
                <Link
                  to={`/mission/${pattern.mission_slug}`}
                  className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-4 py-2 text-sm font-semibold text-black hover:brightness-110"
                >
                  <BookOpen size={16} />
                  Start Mission
                </Link>
              </div>
            )}
            {tab === "practice" && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-bold">Practice {pattern.name}</h3>
                  <p className="text-sm text-[#9a9a9a]">
                    {pattern.question_count} trusted questions available. Choose your mode:
                  </p>
                </div>

                {/* Show practice content from pack */}
                {pattern.pack?.practice && (
                  <div className="space-y-3">
                    {pattern.pack.practice.warmup && pattern.pack.practice.warmup.length > 0 && (
                      <div className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3">
                        <div className="text-xs font-medium text-[#9a9a9a] mb-1">Warm-up</div>
                        <p className="text-xs text-[#e9e9e9]">
                          {pattern.pack.practice.warmup[0].question?.slice(0, 120)}
                          {pattern.pack.practice.warmup[0].question && pattern.pack.practice.warmup[0].question.length > 120 ? "..." : ""}
                        </p>
                      </div>
                    )}
                    {pattern.pack.practice.drill && pattern.pack.practice.drill.length > 0 && (
                      <div className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3">
                        <div className="text-xs font-medium text-[#9a9a9a] mb-1">Pattern Drill</div>
                        <p className="text-xs text-[#e9e9e9]">
                          {pattern.pack.practice.drill[0].question?.slice(0, 120)}
                          {pattern.pack.practice.drill[0].question && pattern.pack.practice.drill[0].question.length > 120 ? "..." : ""}
                        </p>
                      </div>
                    )}
                    {pattern.pack.practice.speed_run && pattern.pack.practice.speed_run.length > 0 && (
                      <div className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3">
                        <div className="text-xs font-medium text-[#9a9a9a] mb-1">Speed Run</div>
                        <p className="text-xs text-[#e9e9e9]">
                          {pattern.pack.practice.speed_run[0].question?.slice(0, 120)}
                          {pattern.pack.practice.speed_run[0].question && pattern.pack.practice.speed_run[0].question.length > 120 ? "..." : ""}
                        </p>
                      </div>
                    )}
                    {pattern.pack.practice.weakness_repair && pattern.pack.practice.weakness_repair.length > 0 && (
                      <div className="rounded-lg border border-red-500/20 bg-red-500/5 p-3">
                        <div className="text-xs font-medium text-red-400 mb-1">Weakness Repair</div>
                        <p className="text-xs text-[#e9e9e9]">
                          {pattern.pack.practice.weakness_repair[0].question?.slice(0, 120)}
                          {pattern.pack.practice.weakness_repair[0].question && pattern.pack.practice.weakness_repair[0].question.length > 120 ? "..." : ""}
                        </p>
                      </div>
                    )}
                  </div>
                )}

                <div className="grid grid-cols-2 gap-3">
                  <Link
                    to={`/aptitude?category=${encodeURIComponent(pattern.id)}&mode=warmup`}
                    className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3 text-center hover:border-[#ffa116]/30"
                  >
                    <div className="text-sm font-medium">Warm-up</div>
                    <div className="text-xs text-[#9a9a9a]">5 guided</div>
                  </Link>
                  <Link
                    to={`/aptitude?category=${encodeURIComponent(pattern.id)}&mode=drill`}
                    className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3 text-center hover:border-[#ffa116]/30"
                  >
                    <div className="text-sm font-medium">Pattern Drill</div>
                    <div className="text-xs text-[#9a9a9a]">10 focused</div>
                  </Link>
                  <Link
                    to={`/aptitude?category=${encodeURIComponent(pattern.id)}&mode=speed`}
                    className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3 text-center hover:border-[#ffa116]/30"
                  >
                    <div className="text-sm font-medium">Speed Run</div>
                    <div className="text-xs text-[#9a9a9a]">10 in 8 min</div>
                  </Link>
                  <Link
                    to={`/aptitude?category=${encodeURIComponent(pattern.id)}&mode=weakness`}
                    className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3 text-center hover:border-[#ffa116]/30"
                  >
                    <div className="text-sm font-medium">Weakness Repair</div>
                    <div className="text-xs text-[#9a9a9a]">Targeted</div>
                  </Link>
                </div>
              </div>
            )}
            {tab === "test" && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-bold">Prove {pattern.name}</h3>
                  <p className="text-sm text-[#9a9a9a]">
                    Timed placement-style questions. No hints. No Captain Byte. Just you and the clock.
                  </p>
                </div>

                {/* Assessment samples */}
                {pattern.pack?.assessment && pattern.pack.assessment.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="text-xs font-medium uppercase tracking-wider text-[#9a9a9a]">Sample Questions</h4>
                    {pattern.pack.assessment.slice(0, 2).map((q, i) => (
                      <div key={i} className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3">
                        <p className="text-xs text-[#e9e9e9] mb-2">{q.question?.slice(0, 150)}{q.question && q.question.length > 150 ? "..." : ""}</p>
                        {q.options && q.options.length > 0 && (
                          <div className="flex flex-wrap gap-1">
                            {q.options.slice(0, 4).map((opt, oi) => (
                              <span key={oi} className="text-[10px] px-1.5 py-0.5 rounded bg-[#242424] text-[#9a9a9a]">
                                {String.fromCharCode(65 + oi)}. {opt?.slice(0, 40)}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {/* Interview transfer */}
                {pattern.pack?.interview_transfer && (
                  <div className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-3">
                    <h4 className="text-xs font-medium uppercase tracking-wider text-[#ffa116] mb-1">Interview Transfer</h4>
                    <p className="text-xs text-[#9a9a9a]">{pattern.pack.interview_transfer.prompt}</p>
                  </div>
                )}

                <div className="flex items-center gap-4 text-xs text-[#9a9a9a]">
                  <span className="flex items-center gap-1">
                    <Activity size={14} /> 10 questions
                  </span>
                  <span className="flex items-center gap-1">
                    <Flame size={14} /> 12 min
                  </span>
                </div>
                <Link
                  to={`/mock-oa?topic=${encodeURIComponent(pattern.id)}&mode=pattern`}
                  className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-4 py-2 text-sm font-semibold text-black hover:brightness-110"
                >
                  <Trophy size={16} />
                  Start Timed Test
                </Link>
              </div>
            )}
          </div>
        </motion.div>

        <Mentor mood={captain.mood} message={captain.intro} />
      </div>
    </div>
  );
}
