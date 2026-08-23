import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Map, Lock, Zap, Target } from "lucide-react";
import { missionApi } from "../services/api/missions";
import Skeleton from "../components/ui/Skeleton";

const SKILL_RANKS: Record<string, { rank: string; color: string }> = {
  Novice: { rank: "Novice", color: "#9CA3AF" },
  Apprentice: { rank: "Apprentice", color: "#22C55E" },
  Solver: { rank: "Solver", color: "#3B82F6" },
  Expert: { rank: "Expert", color: "#F59E0B" },
  Master: { rank: "Master", color: "#A855F7" },
  Legend: { rank: "Legend", color: "#EF4444" },
};

const REALM_NODES = [
  { id: "variables", name: "Variables", icon: "V", x: 400, y: 80, domain: "dsa", prerequisites: [] },
  { id: "control_flow", name: "Control Flow", icon: "CF", x: 250, y: 170, domain: "dsa", prerequisites: ["variables"] },
  { id: "loops", name: "Loops", icon: "L", x: 550, y: 170, domain: "dsa", prerequisites: ["variables"] },
  { id: "functions", name: "Functions", icon: "F", x: 400, y: 260, domain: "dsa", prerequisites: ["control_flow", "loops"] },
  { id: "arrays", name: "Arrays", icon: "A", x: 200, y: 350, domain: "dsa", prerequisites: ["functions"] },
  { id: "strings", name: "Strings", icon: "S", x: 350, y: 350, domain: "dsa", prerequisites: ["functions"] },
  { id: "sorting", name: "Sorting", icon: "So", x: 500, y: 350, domain: "dsa", prerequisites: ["arrays"] },
  { id: "searching", name: "Searching", icon: "Se", x: 650, y: 350, domain: "dsa", prerequisites: ["arrays"] },
  { id: "linked_lists", name: "Linked Lists", icon: "LL", x: 150, y: 440, domain: "dsa", prerequisites: ["arrays"] },
  { id: "stacks_queues", name: "Stacks & Queues", icon: "SQ", x: 300, y: 440, domain: "dsa", prerequisites: ["arrays"] },
  { id: "trees", name: "Trees", icon: "T", x: 450, y: 440, domain: "dsa", prerequisites: ["linked_lists"] },
  { id: "graphs", name: "Graphs", icon: "G", x: 600, y: 440, domain: "dsa", prerequisites: ["trees"] },
  { id: "hashing", name: "Hashing", icon: "H", x: 750, y: 440, domain: "dsa", prerequisites: ["arrays"] },
  { id: "recursion", name: "Recursion", icon: "R", x: 250, y: 530, domain: "dsa", prerequisites: ["functions"] },
  { id: "dynamic_programming", name: "DP", icon: "DP", x: 400, y: 530, domain: "dsa", prerequisites: ["recursion", "sorting"] },
  { id: "greedy", name: "Greedy", icon: "Gr", x: 550, y: 530, domain: "dsa", prerequisites: ["sorting"] },
  { id: "dbms", name: "DBMS", icon: "DB", x: 200, y: 620, domain: "system_design", prerequisites: ["arrays"] },
  { id: "os", name: "OS", icon: "OS", x: 400, y: 620, domain: "system_design", prerequisites: ["recursion"] },
  { id: "networks", name: "Networks", icon: "N", x: 600, y: 620, domain: "system_design", prerequisites: ["stacks_queues"] },
  { id: "system_design", name: "System Design", icon: "SD", x: 400, y: 710, domain: "system_design", prerequisites: ["dbms", "os", "networks"] },
  { id: "oop", name: "OOP", icon: "OO", x: 200, y: 710, domain: "dsa", prerequisites: ["functions"] },
];

const DOMAIN_COLORS: Record<string, string> = {
  dsa: "#22C55E",
  system_design: "#3B82F6",
};

export default function SkillTrees() {
  const navigate = useNavigate();
  const [masteryMap, setMasteryMap] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    missionApi.allMastery()
      .then((data: any) => {
        if (Array.isArray(data)) {
          const map: Record<string, any> = {};
          data.forEach((m: any) => { map[m.topic] = m; });
          setMasteryMap(map);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const getMastery = (topicId: string) => masteryMap[topicId] || { overall: 0, rank: { rank: "Novice", color: "#9CA3AF" }, total_attempts: 0 };

  const isUnlocked = (node: typeof REALM_NODES[0]) => {
    if (node.prerequisites.length === 0) return true;
    return node.prerequisites.every((pid) => {
      const pm = getMastery(pid);
      return pm.overall >= 20 || pm.total_attempts >= 3;
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black px-4 py-8 max-w-5xl mx-auto">
        <Skeleton className="h-10 w-64 mb-3 bg-white border-border shadow-card" />
        <Skeleton className="h-96 w-full rounded-2xl bg-white border-border shadow-card" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black px-4 py-6 sm:py-10 max-w-5xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Map className="w-6 h-6 text-green-400" />
        <div>
          <h1 className="text-2xl font-display font-black text-text-primary">Code Realm</h1>
          <p className="text-xs text-gray-500">Master each topic to unlock the next. Click to start a mission.</p>
        </div>
      </div>

      <div className="relative overflow-x-auto pb-8">
        <svg width="800" height="780" viewBox="0 0 800 780" className="w-full max-w-3xl mx-auto">
          {REALM_NODES.map((node) =>
            node.prerequisites.map((pid) => {
              const parent = REALM_NODES.find((n) => n.id === pid);
              if (!parent) return null;
              const unlocked = isUnlocked(node);
              return (
                <line key={`${pid}-${node.id}`} x1={parent.x} y1={parent.y} x2={node.x} y2={node.y}
                  stroke={unlocked ? "#22C55E33" : "#ffffff08"} strokeWidth={2} strokeDasharray={unlocked ? "none" : "4 4"} />
              );
            })
          )}

          {REALM_NODES.map((node) => {
            const m = getMastery(node.id);
            const unlocked = isUnlocked(node);
            const domainColor = DOMAIN_COLORS[node.domain] || "#22C55E";
            const fillColor = unlocked ? `${domainColor}22` : "#ffffff06";
            const strokeColor = unlocked ? `${domainColor}55` : "#ffffff10";
            const textColor = unlocked ? "#ffffff" : "#555";
            const pct = m.overall || 0;

            return (
              <g key={node.id} onClick={() => unlocked && navigate(`/mission/${node.id}`)}
                style={{ cursor: unlocked ? "pointer" : "default" }}>
                <rect x={node.x - 55} y={node.y - 28} width={110} height={56} rx={16}
                  fill={fillColor} stroke={strokeColor} strokeWidth={1.5} />
                <text x={node.x} y={node.y - 6} textAnchor="middle" dominantBaseline="middle"
                  fill={textColor} fontSize={14} fontFamily="monospace" fontWeight={700}>
                  {node.icon}
                </text>
                <text x={node.x} y={node.y + 12} textAnchor="middle" dominantBaseline="middle"
                  fill={unlocked ? "#ccc" : "#555"} fontSize={9} fontFamily="monospace">
                  {node.name}
                </text>
                {m.total_attempts > 0 && unlocked && (
                  <>
                    <rect x={node.x - 30} y={node.y + 20} width={60} height={4} rx={2} fill="#ffffff15" />
                    <rect x={node.x - 30} y={node.y + 20} width={Math.min(60, (pct / 100) * 60)} height={4} rx={2} fill={domainColor} />
                  </>
                )}
                {!unlocked && (
                  <text x={node.x + 40} y={node.y - 18} textAnchor="middle" fill="#555" fontSize={10}>L</text>
                )}
              </g>
            );
          })}
        </svg>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
        {REALM_NODES.slice(0, 8).map((node) => {
          const m = getMastery(node.id);
          const unlocked = isUnlocked(node);
          return (
            <motion.button key={node.id} onClick={() => unlocked && navigate(`/mission/${node.id}`)}
              whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
              className={`rounded-xl border p-3 text-left transition-all ${unlocked
                ? "border-white/10 bg-white border-border shadow-card hover:border-green-500/30"
                : "border-white/5 bg-white/[0.02] opacity-40"
              }`}>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-bold text-text-primary">{node.icon}</span>
                <span className="text-xs font-medium text-text-primary truncate">{node.name}</span>
                {!unlocked && <Lock className="w-3 h-3 text-gray-600 ml-auto shrink-0" />}
              </div>
              {m.total_attempts > 0 && (
                <div className="flex items-center gap-2 text-[10px] font-mono text-gray-500">
                  <span style={{ color: m.rank?.color }}>{m.rank?.rank || "Novice"}</span>
                  <span>{Math.round(m.overall)}%</span>
                </div>
              )}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}
