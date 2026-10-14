// @ts-nocheck
import { useState, useEffect } from "react";
import { useParams, Link, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { ChevronRight, AlertTriangle, BookOpen, Target, Trophy } from "lucide-react";
import Spinner from "../components/ui/Spinner";
import api from "../services/api";

type Pattern = {
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
};

type Round = {
  id: string;
  name: string;
  icon: string;
  description: string;
  patterns: Pattern[];
};

export default function RoundView() {
  const { roundId } = useParams<{ roundId: string }>();
  const [searchParams] = useSearchParams();
  const company = searchParams.get("company") || "";
  const [loading, setLoading] = useState(true);
  const [round, setRound] = useState<Round | null>(null);

  useEffect(() => {
    load();
  }, [roundId, company]);

  const load = async () => {
    if (!roundId) return;
    setLoading(true);
    try {
      const bf = await api.campaign.getBattlefield(company);
      const found = bf.rounds.find((r: Round) => r.id === roundId);
      if (found) {
        setRound(found);
      }
    } catch {
      // silent
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

  if (!round) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-400">Round not found.</p>
      </div>
    );
  }

  const mastered = round.patterns.filter((p) => p.mastery >= 70).length;

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <div className="mx-auto max-w-3xl px-4 py-6 sm:px-6 lg:px-8 space-y-6">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-[#2a2a2a] bg-gradient-to-br from-[#1c1c1c] to-[#141414] p-6"
        >
          <Link
            to="/battlefield"
            className="inline-flex items-center gap-1 text-xs text-[#9a9a9a] hover:text-[#ffa116] mb-3"
          >
            <ChevronRight size={14} className="rotate-180" />
            Back to Battlefield
          </Link>
          <div className="flex items-center gap-3">
            <span className="text-3xl">{round.icon}</span>
            <div>
              <h1 className="text-2xl font-bold">{round.name}</h1>
              <p className="text-sm text-[#9a9a9a]">{round.description}</p>
              <p className="text-xs text-[#9a9a9a] mt-1">
                {mastered}/{round.patterns.length} mastered
              </p>
            </div>
          </div>
        </motion.div>

        {/* Patterns */}
        <div className="space-y-3">
          {round.patterns.map((pattern, idx) => (
            <motion.div
              key={pattern.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.03 }}
            >
              <Link
                to={`/pattern/${pattern.id}${company ? `?company=${encodeURIComponent(company)}` : ""}`}
                className={`block rounded-xl border p-4 transition-all hover:border-[#ffa116]/30 ${
                  pattern.is_lowest
                    ? "border-red-500/30 bg-red-500/5"
                    : pattern.is_weak
                    ? "border-yellow-500/20 bg-yellow-500/5"
                    : "border-[#2a2a2a] bg-[#1c1c1c]"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-xl">{pattern.emoji}</span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-[#e9e9e9]">{pattern.name}</span>
                        {pattern.is_lowest && (
                          <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20">
                            REPAIR
                          </span>
                        )}
                        {pattern.is_weak && !pattern.is_lowest && (
                          <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-yellow-500/10 text-yellow-400 border border-yellow-500/20">
                            WEAK
                          </span>
                        )}
                      </div>
                      <div className="text-xs text-[#9a9a9a] mt-0.5">
                        {pattern.attempts > 0
                          ? `${pattern.attempts} attempts · ${pattern.accuracy !== null ? `${pattern.accuracy}% accuracy` : "no accuracy yet"}`
                          : "Not started"}
                      </div>
                      {pattern.diagnosis?.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-1">
                          {pattern.diagnosis.slice(0, 2).map((d, i) => (
                            <span
                              key={i}
                              className="text-[10px] px-1.5 py-0.5 rounded bg-red-500/10 text-red-400"
                            >
                              {d}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="hidden sm:flex items-center gap-2">
                      <div className="w-16 h-1.5 rounded-full bg-[#2a2a2a] overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            pattern.mastery >= 80
                              ? "bg-green-500"
                              : pattern.mastery >= 60
                              ? "bg-[#ffa116]"
                              : pattern.mastery >= 40
                              ? "bg-yellow-500"
                              : "bg-red-500"
                          }`}
                          style={{ width: `${Math.max(pattern.mastery, 2)}%` }}
                        />
                      </div>
                      <span className={`text-xs font-medium w-10 text-right ${masteryColor(pattern.mastery)}`}>
                        {pattern.mastery}%
                      </span>
                    </div>
                    <ChevronRight size={16} className="text-[#9a9a9a]" />
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
