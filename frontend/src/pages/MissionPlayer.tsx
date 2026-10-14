// @ts-nocheck
import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import FlagshipMissionShell, { MissionStepId, FlagshipMissionProps } from "../components/missions/FlagshipMissionShell";

const MISSION_REGISTRY: Record<string, () => Promise<{ default: unknown }>> = {
  "percentages": () => import("../data/missions/percentages.tsx"),
  "ratio": () => import("../data/missions/ratio.tsx"),
  "averages": () => import("../data/missions/averages.tsx"),
  "blood-relations": () => import("../data/missions/blood-relations.tsx"),
  "directions": () => import("../data/missions/directions.tsx"),
  "series": () => import("../data/missions/series.tsx"),
  "arrays": () => import("../data/missions/arrays.tsx"),
  "coding-decoding": () => import("../data/missions/coding-decoding.tsx"),
  "conditions": () => import("../data/missions/conditions.tsx"),
  "dbms": () => import("../data/missions/dbms.tsx"),
  "grammar": () => import("../data/missions/grammar.tsx"),
  "loops": () => import("../data/missions/loops.tsx"),
  "oop": () => import("../data/missions/oop.tsx"),
  "profit-loss": () => import("../data/missions/profit-loss.tsx"),
  "puzzles": () => import("../data/missions/puzzles.tsx"),
  "reading-comprehension": () => import("../data/missions/reading-comprehension.tsx"),
  "syllogism": () => import("../data/missions/syllogism.tsx"),
  "time-work": () => import("../data/missions/time-work.tsx"),
  "variables": () => import("../data/missions/variables.tsx"),
  "vocabulary": () => import("../data/missions/vocabulary.tsx"),
  "strings": () => import("../data/missions/strings.tsx"),
  "seating-arrangement": () => import("../data/missions/seating-arrangement.tsx"),
  "sql-joins": () => import("../data/missions/sql-joins.tsx"),
};

const PATTERN_PACKS_DIR = "/api/v1/campaign/patterns";

async function loadPatternPack(slug: string): Promise<FlagshipMissionProps | null> {
  try {
    const res = await fetch(`${PATTERN_PACKS_DIR}/${encodeURIComponent(slug)}/pack`);
    if (!res.ok) return null;
    const json = await res.json();
    const pack = json.pack || {};
    const teaching = pack.teaching || [];
    if (!teaching.length) return null;

    const steps = teaching.map((step: Record<string, unknown>, idx: number) => ({
      id: (step.id as string) || `step-${idx}`,
      title: (step.title as string) || `Step ${idx + 1}`,
      description: (step.title as string) || "",
      render: () => (
        <div className="space-y-3">
          <div className="rounded-lg border border-[#2a2a2a] bg-[#1c1c1c] p-4">
            <div className="text-xs font-mono uppercase tracking-wider text-[#ffa116] mb-2">
              {(step.type as string) || "step"}
            </div>
            <p className="text-sm text-[#e9e9e9]">{(step.title as string) || ""}</p>
            {step.captain_message && (
              <p className="text-sm text-[#9a9a9a] mt-2 italic">{(step.captain_message as string) || ""}</p>
            )}
            {step.render && (
              <pre className="mt-3 text-xs text-[#9a9a9a] bg-[#0f0f0f] p-3 rounded overflow-x-auto">
                {JSON.stringify(step.render, null, 2)}
              </pre>
            )}
          </div>
        </div>
      ),
    }));

    return {
      captainMessage: (pack.purpose as string) || `Learn ${pack.name || slug}`,
      captainMood: "briefing",
      xpReward: (pack.xp_reward as number) || (pack.reward?.xp as number) || 0,
      backTo: "/placement",
      steps,
    };
  } catch {
    return null;
  }
}

export default function MissionPlayer() {
  const { slug } = useParams<{ slug: string }>();
  const [mission, setMission] = useState<FlagshipMissionProps | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!slug) return;
    let cancelled = false;

    async function loadMission() {
      setLoading(true);
      setError("");

      // First try pattern pack from backend
      const packMission = await loadPatternPack(slug);
      if (packMission) {
        if (!cancelled) setMission(packMission);
        setLoading(false);
        return;
      }

      // Fallback to frontend mission registry
      const loader = MISSION_REGISTRY[slug];
      if (!loader) {
        if (!cancelled) {
          setError("Mission not found.");
        }
        setLoading(false);
        return;
      }

      try {
        const mod = await loader();
        if (!cancelled) {
          const exported = (mod as { default: unknown }).default;
          setMission(
            (typeof exported === "function"
              ? (exported as () => FlagshipMissionProps)()
              : (exported as FlagshipMissionProps)),
          );
        }
      } catch {
        if (!cancelled) {
          setError("Failed to load mission.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadMission();
    return () => { cancelled = true; };
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0f0f0f] flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl mb-2">⏳</div>
          <p className="text-sm text-[#9a9a9a]">Loading mission...</p>
        </div>
      </div>
    );
  }

  if (error || !mission) {
    return (
      <div className="min-h-screen bg-[#0f0f0f] flex items-center justify-center">
        <div className="text-center">
          <p className="text-sm text-red-400">{error || "Mission not found."}</p>
          <Link to="/placement" className="mt-4 inline-block text-[#ffa116]">
            Back to campaign
          </Link>
        </div>
      </div>
    );
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="min-h-screen bg-[#0f0f0f]">
      <FlagshipMissionShell {...mission} />
    </motion.div>
  );
}
