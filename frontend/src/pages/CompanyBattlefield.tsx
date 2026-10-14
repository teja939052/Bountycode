// @ts-nocheck
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ChevronRight,
  Flame,
  Target,
  AlertTriangle,
  Trophy,
  Activity,
  BookOpen,
} from "lucide-react";
import Spinner from "../components/ui/Spinner";
import api from "../services/api";

type Round = {
  id: string;
  name: string;
  icon: string;
  description: string;
  patterns: Array<{
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
  }>;
};

type Battlefield = {
  company: string;
  rounds: Round[];
  biggest_weakness: any;
  total_patterns: number;
  mastered_patterns: number;
  weak_patterns: number;
};

export default function CompanyBattlefield() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<Battlefield | null>(null);
  const [captain, setCaptain] = useState<{ intro: string; mood: string }>({
    intro: "Loading your battlefield...",
    mood: "briefing",
  });

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    setLoading(true);
    try {
      const [bf, today] = await Promise.all([
        api.campaign.getBattlefield(),
        api.campaign.getToday().catch(() => null),
      ]);
      setData(bf);

      const bw = bf.biggest_weakness;
      if (bw) {
        setCaptain({
          intro: `🧭 Captain Byte: Your biggest weakness is ${bw.emoji} ${bw.name} at ${bw.mastery}%. We'll repair that first.`,
          mood: "encouraging",
        });
      } else {
        setCaptain({
          intro: "🧭 Captain Byte: Your battlefield is ready. Start with the weakest round.",
          mood: "briefing",
        });
      }

      // Prefetch today's recommendations
      if (today?.recommendations?.length) {
        setCaptain((prev) => ({
          ...prev,
          intro: `${prev.intro} Today: ${today.recommendations.length} missions.`,
        }));
      }
    } catch {
      setCaptain({
        intro: "Could not load battlefield. Try refreshing.",
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

  const masteryBg = (m: number) => {
    if (m >= 80) return "bg-green-500";
    if (m >= 60) return "bg-[#ffa116]";
    if (m >= 40) return "bg-yellow-500";
    return "bg-red-500";
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-400">Failed to load battlefield.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <div className="mx-auto max-w-4xl px-4 py-6 sm:px-6 lg:px-8 space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-[#2a2a2a] bg-gradient-to-br from-[#1c1c1c] to-[#141414] p-6"
        >
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <span className="text-xs font-mono uppercase tracking-wider text-[#ffa116]">
                Company Battlefield
              </span>
              <h1 className="text-2xl sm:text-3xl font-bold mt-1 capitalize">
                {data.company}
              </h1>
              <p className="text-sm text-[#9a9a9a] mt-1">
                {data.total_patterns} patterns · {data.mastered_patterns} mastered · {data.weak_patterns} weak
              </p>
            </div>
            <div className="grid grid-cols-3 gap-3">
              <div className="rounded-xl bg-[#1f1f1f] px-3 py-2 text-center">
                <div className="text-lg font-bold text-[#e9e9e9]">{data.total_patterns}</div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Patterns</div>
              </div>
              <div className="rounded-xl bg-[#1f1f1f] px-3 py-2 text-center">
                <div className="text-lg font-bold text-green-400">{data.mastered_patterns}</div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Mastered</div>
              </div>
              <div className="rounded-xl bg-[#1f1f1f] px-3 py-2 text-center">
                <div className="text-lg font-bold text-red-400">{data.weak_patterns}</div>
                <div className="text-[10px] uppercase tracking-wider text-[#9a9a9a]">Weak</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Biggest weakness alert */}
        {data.biggest_weakness && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-red-500/30 bg-[#141414] p-5"
          >
            <div className="flex items-start gap-3">
              <AlertTriangle className="text-red-400 mt-0.5" size={20} />
              <div className="flex-1">
                <h3 className="text-sm font-bold text-red-400">
                  Biggest weakness: {data.biggest_weakness.emoji} {data.biggest_weakness.name}
                </h3>
                <p className="text-xs text-[#9a9a9a] mt-1">
                  {data.biggest_weakness.mastery}% mastery —{" "}
                  {data.biggest_weakness.diagnosis?.[0] || "needs repair"}
                </p>
                  <button
                    onClick={() => navigate(`/pattern/${data.biggest_weakness.id}?company=${encodeURIComponent(data.company)}`)}
                    className="mt-3 inline-flex items-center gap-1 rounded-lg bg-red-500/10 px-3 py-1.5 text-xs font-medium text-red-400 hover:bg-red-500/20"
                  >
                  Repair Now <ChevronRight size={14} />
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Rounds map */}
        <div className="space-y-4">
          {data.rounds.map((round_, idx) => (
            <motion.div
              key={round_.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.05 }}
              className="rounded-xl border border-[#2a2a2a] bg-[#141414] overflow-hidden"
            >
                <button
                  onClick={() => navigate(`/round/${round_.id}?company=${encodeURIComponent(data.company)}`)}
                  className="w-full flex items-center justify-between p-5 text-left hover:bg-white/[0.02] transition-colors"
                >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{round_.icon}</span>
                  <div>
                    <h3 className="font-semibold text-[#e9e9e9]">{round_.name}</h3>
                    <p className="text-xs text-[#9a9a9a]">{round_.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className="text-xs text-[#9a9a9a]">
                      {round_.patterns.filter((p) => p.mastery >= 70).length}/{round_.patterns.length} mastered
                    </div>
                  </div>
                  <ChevronRight size={16} className="text-[#9a9a9a]" />
                </div>
              </button>

              {/* Pattern preview */}
              <div className="px-5 pb-4 space-y-2">
                {round_.patterns.map((pattern) => (
                  <button
                    key={pattern.id}
                    onClick={() => navigate(`/pattern/${pattern.id}?company=${encodeURIComponent(data.company)}`)}
                    className={`w-full flex items-center justify-between rounded-lg border px-3 py-2 text-left transition-all ${
                      pattern.is_lowest
                        ? "border-red-500/30 bg-red-500/5"
                        : pattern.is_weak
                        ? "border-yellow-500/20 bg-yellow-500/5"
                        : "border-[#2a2a2a] bg-[#1c1c1c]"
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-sm">{pattern.emoji}</span>
                      <span className="text-sm text-[#e9e9e9]">{pattern.name}</span>
                      {pattern.is_lowest && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20">
                          REPAIR
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="hidden sm:flex items-center gap-2">
                        <div className="w-16 h-1.5 rounded-full bg-[#2a2a2a] overflow-hidden">
                          <div
                            className={`h-full rounded-full ${masteryBg(pattern.mastery)}`}
                            style={{ width: `${Math.max(pattern.mastery, 2)}%` }}
                          />
                        </div>
                        <span className={`text-xs font-medium w-10 text-right ${masteryColor(pattern.mastery)}`}>
                          {pattern.mastery}%
                        </span>
                      </div>
                      <span className="text-xs text-[#9a9a9a]">
                        {pattern.attempts > 0 ? `${pattern.attempts} attempts` : "Not started"}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        <Mentor mood={captain.mood} message={captain.intro} />
      </div>
    </div>
  );
}
