import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { BarChart3, TrendingUp, Target, AlertTriangle } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function SkillMasteryPage() {
  const [graph, setGraph] = useState<any>(null);
  const [weak, setWeak] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/api/v1/mastery/graph"),
      api.get("/api/v1/mastery/weak").catch(() => ({ weak_areas: [] })),
    ]).then(([g, w]: any[]) => {
      setGraph(g);
      setWeak(w);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  const skills = graph?.skills ? Object.entries(graph.skills) : [];

  return (
    <div className="min-h-screen px-4 py-8 max-w-5xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-sky/10 border border-brand-sky/20 mb-3">
          <BarChart3 size={14} className="text-brand-sky" />
          <span className="text-xs font-mono text-brand-sky">SKILL MASTERY</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Skill Mastery</h1>
      </motion.div>

      {/* Summary Cards */}
      {graph && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
          <div className="glass rounded-xl p-4 text-center">
            <p className="text-2xl font-display font-black text-brand-sky">{graph.total_skills || 0}</p>
            <p className="text-[10px] font-mono text-gray-500 mt-1">Total Skills</p>
          </div>
          <div className="glass rounded-xl p-4 text-center">
            <p className="text-2xl font-display font-black text-emerald-400">{graph.mastered_count || 0}</p>
            <p className="text-[10px] font-mono text-gray-500 mt-1">Mastered</p>
          </div>
          <div className="glass rounded-xl p-4 text-center">
            <p className="text-2xl font-display font-black text-brand-teal">{graph.strong_count || 0}</p>
            <p className="text-[10px] font-mono text-gray-500 mt-1">Strong</p>
          </div>
          <div className="glass rounded-xl p-4 text-center">
            <p className="text-2xl font-display font-black text-amber-400">{graph.weak_count || 0}</p>
            <p className="text-[10px] font-mono text-gray-500 mt-1">Weak</p>
          </div>
          <div className="glass rounded-xl p-4 text-center">
            <p className="text-2xl font-display font-black text-gray-400">{graph.untried_count || 0}</p>
            <p className="text-[10px] font-mono text-gray-500 mt-1">Untried</p>
          </div>
        </div>
      )}

      {/* Weak Areas */}
      {weak?.weak_areas?.length > 0 && (
        <div className="glass rounded-xl p-6 mb-6">
          <h3 className="font-display font-bold text-text-primary mb-3 flex items-center gap-2">
            <AlertTriangle size={18} className="text-amber-400" /> Weak Areas
          </h3>
          <div className="flex flex-wrap gap-2">
            {weak.weak_areas.map((w: any, i: number) => (
              <span key={i} className="text-xs font-mono px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
                {w.topic || w} {w.accuracy != null ? `(${w.accuracy}%)` : ""}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Skills Grid */}
      <div className="glass rounded-xl p-6">
        <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
          <TrendingUp size={18} className="text-brand-sky" /> All Skills
        </h3>
        <div className="space-y-2">
          {skills.map(([key, skill]: [string, any]) => (
            <div key={key} className="flex items-center gap-3 p-3 rounded-lg bg-white/[0.02]">
              <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: skill.color || "#666" }} />
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-300 font-mono truncate">{skill.topic}{skill.sub_topic ? ` > ${skill.sub_topic}` : ""}</span>
                  <span className="text-xs font-mono shrink-0 ml-2" style={{ color: skill.color || "#888" }}>{skill.level_name || skill.level}</span>
                </div>
                <div className="h-1 bg-white border-border shadow-card rounded-full overflow-hidden mt-1">
                  <div className="h-full rounded-full" style={{ width: `${Math.min(100, (skill.accuracy || 0))}%`, backgroundColor: skill.color || "#666" }} />
                </div>
                <div className="flex gap-3 mt-1">
                  <span className="text-[10px] font-mono text-gray-600">{skill.problems_attempted || 0} attempted</span>
                  <span className="text-[10px] font-mono text-gray-600">{skill.accuracy || 0}% accuracy</span>
                </div>
              </div>
            </div>
          ))}
          {skills.length === 0 && <p className="text-sm text-gray-500 font-mono text-center py-8">No skills tracked yet. Start solving problems!</p>}
        </div>
      </div>
    </div>
  );
}
