// @ts-nocheck
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { PlayCircle, ChevronRight, Target } from "lucide-react";
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
  test: (r) => r.pattern_id ? `/mock-oa?topic=${encodeURIComponent(r.pattern_id)}&mode=pattern` : "/mock-oa",
  battle: (r) => r.pattern_id ? `/mock-oa?topic=${encodeURIComponent(r.pattern_id)}&mode=pattern` : "/mock-oa",
  review: (r) => r.pattern_id ? `/mission/${r.pattern_id}` : "/placement",
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

      const mission = data.recommendations?.[0];
      setCaptain({
        intro: mission
          ? `🧭 Captain Byte: ${mission.reason}`
          : "🧭 Captain Byte: Set your target and I'll pick today's mission.",
        mood: "encouraging",
      });
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

  const mission = plan.recommendations?.[0];
  const next = plan.recommendations?.[1];
  const remaining = Math.max(0, (plan.recommendations?.length || 0) - 2);

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <div className="mx-auto max-w-2xl px-4 py-6 sm:px-6 lg:px-8 space-y-6">
        {/* Target + readiness */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-[#2a2a2a] bg-gradient-to-br from-[#1c1c1c] to-[#141414] p-6"
        >
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <span className="text-xs font-mono uppercase tracking-wider text-[#ffa116]">
                Your target
              </span>
              <h1 className="text-2xl sm:text-3xl font-bold mt-1 capitalize">
                {plan.company || "Not set yet"}
              </h1>
              <p className="text-sm text-[#9a9a9a] mt-1">
                {plan.role || "Software Developer"}
                {plan.days_remaining !== null && plan.days_remaining !== undefined && (
                  <> · {plan.days_remaining} days to assessment</>
                )}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-[#1f1f1f] px-4 py-3 text-center">
                <div className="text-2xl font-bold text-[#ffa116]">
                  {Math.round(plan.overall_score || 0)}%
                </div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Readiness</div>
              </div>
              <div className="rounded-xl bg-[#1f1f1f] px-4 py-3 text-center">
                <div className="text-2xl font-bold text-[#e9e9e9]">{plan.streak || 0}</div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Day streak</div>
              </div>
            </div>
          </div>
        </motion.header>

        {/* No target yet */}
        {!plan.company && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-[#ffa11655] bg-[#141414] p-6"
          >
            <h2 className="text-xl font-bold">Set your target</h2>
            <p className="mt-1 text-sm text-[#9a9a9a]">
              Pick a company and assessment date so today's mission can point at the right skills.
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

        {/* One mission */}
        {plan.company && mission && (
          <motion.section
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-[#ffa116]/30 bg-[#141414] p-6"
          >
            <div className="text-xs font-mono uppercase tracking-wider text-[#ffa116]">
              Today's mission
            </div>
            <h2 className="mt-2 text-2xl font-bold">
              <span className="mr-2">{mission.emoji}</span>
              {mission.title}
            </h2>
            {mission.subtitle && (
              <p className="mt-1 text-sm text-[#9a9a9a]">{mission.subtitle}</p>
            )}

            <div className="mt-4 rounded-lg bg-[#1c1c1c] p-4">
              <div className="text-[10px] font-mono uppercase tracking-wider text-[#9a9a9a]">
                Why this next?
              </div>
              <p className="mt-1 text-sm text-[#e9e9e9]">{mission.reason}</p>
            </div>

            <div className="mt-4 flex items-center justify-between gap-4">
              <span className="text-sm text-[#9a9a9a]">
                ~{mission.estimated_minutes} minutes
              </span>
              <Link
                to={getHref(mission)}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2.5 text-sm font-semibold text-black transition hover:brightness-110"
              >
                <PlayCircle size={16} />
                Start mission
              </Link>
            </div>

            {next && (
              <p className="mt-4 border-t border-[#2a2a2a] pt-3 text-xs text-[#9a9a9a]">
                After this: <span className="text-[#e9e9e9]">{next.title}</span>
                {remaining > 0 && <> · +{remaining} more queued</>}
              </p>
            )}
          </motion.section>
        )}

        {/* Progress */}
        {plan.company && plan.battlefield_summary && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-5"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-[#e9e9e9]">Your progress</h3>
              <button
                onClick={() => navigate("/battlefield")}
                className="inline-flex items-center gap-1 text-xs text-[#ffa116] hover:underline"
              >
                Details <ChevronRight size={14} />
              </button>
            </div>
            <p className="mt-2 text-sm text-[#9a9a9a]">
              <span className="text-green-400 font-semibold">
                {plan.battlefield_summary.mastered_patterns}
              </span>{" "}
              of {plan.battlefield_summary.total_patterns} patterns mastered ·{" "}
              <span className="text-red-400 font-semibold">
                {plan.battlefield_summary.weak_patterns}
              </span>{" "}
              need repair
            </p>
          </motion.div>
        )}

        <Mentor mood="encouraging" message={captain.intro} />
      </div>
    </div>
  );
}
