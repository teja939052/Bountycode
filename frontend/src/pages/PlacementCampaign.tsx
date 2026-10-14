// @ts-nocheck
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  PlayCircle,
  ChevronRight,
  Flame,
  Target,
  AlertTriangle,
  TrendingUp,
} from "lucide-react";
import Spinner from "../components/ui/Spinner";
import { Mentor } from "../design-system/Mentor";
import api from "../services/api";

type Recommendation = {
  id: string;
  type: string;
  priority: number;
  title: string;
  subtitle: string;
  emoji: string;
  estimated_minutes: number;
  pattern_id: string | null;
  round_id: string | null;
  reason: string;
  action: string;
};

type TodayPlan = {
  company: string;
  role: string;
  assessment_date: string;
  days_remaining: number | null;
  streak: number;
  level: number;
  overall_score: number;
  overall_mastery: string;
  overall_mastery_label: string;
  recommendations: Recommendation[];
  totals: { estimated_minutes: number; task_count: number };
  biggest_weakness: any;
  battlefield_summary: {
    total_patterns: number;
    mastered_patterns: number;
    weak_patterns: number;
  };
};

const ACTION_HREF: Record<string, (r: Recommendation) => string> = {
  repair: (r) => r.pattern_id ? `/pattern/${r.pattern_id}` : "/placement",
  learn: (r) => r.pattern_id ? `/mission/${r.pattern_id}` : "/placement",
  battle: (r) => r.pattern_id ? `/mock-oa?topic=${encodeURIComponent(r.pattern_id)}&mode=pattern` : "/mock-oa",
  review: (r) => "/placement",
  practice: (r) => r.pattern_id ? `/aptitude?category=${encodeURIComponent(r.pattern_id)}` : "/aptitude",
  diagnostic: () => "/diagnostic",
};

export default function PlacementCampaign() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [plan, setPlan] = useState<TodayPlan | null>(null);
  const [captain, setCaptain] = useState<{ intro: string; mood: string }>({
    intro: "Loading your campaign...",
    mood: "briefing",
  });

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    setLoading(true);
    try {
      const data = await api.campaign.getToday();
      setPlan(data);

      const bw = data.biggest_weakness;
      if (bw) {
        setCaptain({
          intro: `🧭 Captain Byte: ${bw.emoji} ${bw.name} at ${bw.mastery}% is your biggest weakness. Today we repair it.`,
          mood: "encouraging",
        });
      } else {
        setCaptain({
          intro: `🧭 Captain Byte: ${data.recommendations?.length || 0} missions today. ${data.totals?.estimated_minutes || 0} minutes total. Let's go.`,
          mood: "briefing",
        });
      }
    } catch {
      setCaptain({
        intro: "Could not load campaign. Try refreshing.",
        mood: "stuck",
      });
    } finally {
      setLoading(false);
    }
  };

  const getHref = (r: Recommendation) => {
    const fn = ACTION_HREF[r.action] || ACTION_HREF.learn;
    return fn(r);
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

  if (!plan) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-400">No campaign data. Set your target company.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <div className="mx-auto max-w-3xl px-4 py-6 sm:px-6 lg:px-8 space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-[#2a2a2a] bg-gradient-to-br from-[#1c1c1c] to-[#141414] p-6"
        >
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <span className="text-xs font-mono uppercase tracking-wider text-[#ffa116]">
                Your Campaign
              </span>
              <h1 className="text-2xl sm:text-3xl font-bold mt-1 capitalize">
                {plan.company || "Your Campaign"}
              </h1>
              <p className="text-sm text-[#9a9a9a] mt-1">
                {plan.role || "Software Developer"}
                {plan.days_remaining !== null && plan.days_remaining !== undefined && (
                  <> · {plan.days_remaining} days to assessment</>
                )}
              </p>
            </div>
            <div className="grid grid-cols-4 gap-2">
              <div className="rounded-xl bg-[#1f1f1f] px-2 py-2 text-center">
                <div className="text-lg font-bold text-[#e9e9e9]">{plan.streak || 0}</div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Streak</div>
              </div>
              <div className="rounded-xl bg-[#1f1f1f] px-2 py-2 text-center">
                <div className="text-lg font-bold text-[#e9e9e9]">{plan.level || 1}</div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Level</div>
              </div>
              <div className="rounded-xl bg-[#1f1f1f] px-2 py-2 text-center">
                <div className="text-lg font-bold text-[#ffa116]">{Math.round(plan.overall_score || 0)}%</div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Score</div>
              </div>
              <div className="rounded-xl bg-[#1f1f1f] px-2 py-2 text-center">
                <div className="text-lg font-bold text-[#e9e9e9]">{plan.totals?.estimated_minutes || 0}</div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Minutes</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* No campaign target yet */}
        {!plan.company && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-[#ffa11655] bg-[#141414] p-6"
          >
            <h2 className="text-xl font-bold">Set your target</h2>
            <p className="mt-1 text-sm text-[#9a9a9a]">
              Pick a company and assessment date to build your campaign.
            </p>
            <button
              onClick={() => navigate("/profile")}
              className="mt-4 inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-4 py-2 text-sm font-semibold text-black hover:brightness-110"
            >
              <Target size={16} />
              Set target in profile
            </button>
          </motion.div>
        )}

        {/* Today's missions */}
        {plan.company && plan.recommendations?.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold">Today's Missions</h2>
              <span className="text-xs text-[#9a9a9a]">
                {plan.totals?.task_count || 0} tasks · ~{plan.totals?.estimated_minutes || 0} min
              </span>
            </div>
            <div className="space-y-3">
              {plan.recommendations.map((r, idx) => (
                <Link
                  key={r.id}
                  to={getHref(r)}
                  className={`flex items-center justify-between rounded-lg border p-4 transition-all hover:border-[#ffa116]/30 ${
                    r.type === "repair"
                      ? "border-red-500/30 bg-red-500/5"
                      : r.type === "battle"
                      ? "border-[#ffa116]/20 bg-[#1c1c1c]"
                      : "border-[#2a2a2a] bg-[#1c1c1c]"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-lg">{r.emoji}</span>
                    <div>
                      <div className="text-sm font-semibold text-[#e9e9e9]">
                        {idx + 1}. {r.title}
                      </div>
                      <div className="text-xs text-[#9a9a9a]">{r.subtitle}</div>
                      <div className="text-xs text-[#ffa116] mt-0.5">{r.reason}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-[#9a9a9a]">
                    <span>{r.estimated_minutes}m</span>
                    <PlayCircle size={14} />
                  </div>
                </Link>
              ))}
            </div>
          </motion.div>
        )}

        {/* Why these */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-5"
        >
          <h3 className="text-sm font-bold text-[#ffa116] mb-2">Why these missions?</h3>
          <div className="space-y-2 text-xs text-[#9a9a9a]">
            {plan.biggest_weakness && (
              <p>
                <span className="text-[#e9e9e9]">Yesterday:</span> You struggled with{" "}
                <span className="text-[#ffa116]">{plan.biggest_weakness.name}</span>.
                {plan.recommendations?.[0]?.reason && (
                  <> Today we're repairing that skill.</>
                )}
              </p>
            )}
            <p>
              <span className="text-[#e9e9e9]">Tomorrow:</span> Your next challenge depends on
              today's result. Master these, and the difficulty increases.
            </p>
          </div>
          <div className="mt-3 flex items-center gap-2 text-xs text-[#9a9a9a]">
            <TrendingUp size={14} />
            Your performance today determines tomorrow's difficulty
          </div>
        </motion.div>

        {/* Battlefield summary */}
        {plan.battlefield_summary && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-5"
          >
            <h3 className="text-sm font-bold text-[#e9e9e9] mb-3">Battlefield Progress</h3>
            <div className="grid grid-cols-3 gap-3">
              <div className="rounded-lg bg-[#1f1f1f] px-3 py-2 text-center">
                <div className="text-lg font-bold text-[#e9e9e9]">
                  {plan.battlefield_summary.total_patterns}
                </div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Patterns</div>
              </div>
              <div className="rounded-lg bg-[#1f1f1f] px-3 py-2 text-center">
                <div className="text-lg font-bold text-green-400">
                  {plan.battlefield_summary.mastered_patterns}
                </div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Mastered</div>
              </div>
              <div className="rounded-lg bg-[#1f1f1f] px-3 py-2 text-center">
                <div className="text-lg font-bold text-red-400">
                  {plan.battlefield_summary.weak_patterns}
                </div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Weak</div>
              </div>
            </div>
            <button
              onClick={() => navigate("/battlefield")}
              className="mt-4 inline-flex items-center gap-1 text-xs text-[#ffa116] hover:underline"
            >
              View full battlefield <ChevronRight size={14} />
            </button>
          </motion.div>
        )}

        <Mentor mood="encouraging" message={captain.intro} />
      </div>
    </div>
  );
}
