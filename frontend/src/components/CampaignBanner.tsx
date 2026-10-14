// @ts-nocheck
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { AlertTriangle, Sparkles, TrendingUp, ArrowRight, Target } from "lucide-react";

type DiagnosticEntry = {
  score: number;
  status: "strength" | "developing" | "weakness" | "unknown";
};

type DiagnosticState = {
  completed: boolean;
  baseline_categories?: Record<string, number>;
  first_missions?: any[];
};

export default function CampaignBanner({ world }: { world: string }) {
  const [diagnostic, setDiagnostic] = useState<DiagnosticState | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetch("/api/v1/onboarding/diagnostic/status")
      .then((res) => (res.ok ? res.json() : Promise.reject()))
      .then((json) => {
        if (!cancelled && json.completed) setDiagnostic(json);
      })
      .catch(() => {});
    return () => { cancelled = true; };
  }, []);

  if (!diagnostic?.completed) return null;

  const dims = diagnostic.baseline_categories || {};
  const worldLower = world.toLowerCase();
  const relevant = Object.entries(dims).filter(([key]) => {
    const normalizedKey = key.replace(/_/g, "-").toLowerCase();
    return normalizedKey.includes(worldLower) || worldLower.includes(normalizedKey) || key.toLowerCase().includes(worldLower);
  });
  const weak = relevant.filter(([, v]) => (v as number) < 40);
  const strength = relevant.filter(([, v]) => (v as number) >= 70);

  if (!weak.length && !strength.length) return null;

  const firstMission = diagnostic.first_missions?.[0];

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-6 rounded-xl border border-[#2a2a2a] bg-[#141414] p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="flex items-center gap-2">
            {weak.length ? (
              <AlertTriangle size={16} className="text-red-400" />
            ) : (
              <Sparkles size={16} className="text-green-400" />
            )}
            <h3 className="text-sm font-bold text-[#e9e9e9]">
              {weak.length ? "Repair mode activated" : "You're already strong here"}
            </h3>
          </div>
          <p className="mt-1 text-xs text-[#9a9a9a]">
            {weak.length
              ? `Your diagnostic shows weakness in ${weak.map(([k]) => k.replace(/_/g, " ")).join(", ")}. Start here.`
              : `Your diagnostic shows strength in ${strength.map(([k]) => k.replace(/_/g, " ")).join(", ")}. Let's push further.`}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {firstMission && (
            <Link
              to="/placement"
              className="inline-flex items-center gap-1 rounded-lg bg-[#ffa116] px-3 py-2 text-xs font-semibold text-black transition-colors hover:brightness-110"
            >
              <Target size={14} />
              {firstMission.title}
              <ArrowRight size={14} />
            </Link>
          )}
        </div>
      </div>
    </motion.div>
  );
}
