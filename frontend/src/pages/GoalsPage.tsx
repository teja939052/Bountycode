import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Target, Plus, Trash2, TrendingUp } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

const METRICS = ["problems_solved", "interviews_done", "study_hours", "streak_days", "aptitude_tests"];

export default function GoalsPage() {
  const [goals, setGoals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newMetric, setNewMetric] = useState(METRICS[0]);
  const [newTarget, setNewTarget] = useState("10");
  const [newDeadline, setNewDeadline] = useState("");

  const load = async () => {
    try {
      const d = await api.get("/api/v1/goals");
      setGoals(d.goals || []);
    } catch { }
    setLoading(false);
  };

  useEffect(() => { load(); }, []);

  const create = async () => {
    if (!newTitle.trim()) return;
    await api.post("/api/v1/goals/create", {
      title: newTitle,
      metric: newMetric,
      target: parseInt(newTarget) || 10,
      deadline: newDeadline || undefined,
    });
    setShowCreate(false);
    setNewTitle("");
    load();
  };

  const track = async (goalId: string) => {
    await api.post(`/api/v1/goals/${goalId}/track`);
    load();
  };

  const remove = async (goalId: string) => {
    await api.delete(`/api/v1/goals/${goalId}`);
    load();
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  return (
    <div className="min-h-screen px-4 py-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between mb-8">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-sky/10 border border-brand-sky/20 mb-3">
            <Target size={14} className="text-brand-sky" />
            <span className="text-xs font-mono text-brand-sky">GOALS</span>
          </div>
          <h1 className="text-3xl font-display font-black text-text-primary">My Goals</h1>
        </div>
        <button onClick={() => setShowCreate(!showCreate)}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-brand-sky/20 text-brand-sky font-mono text-sm hover:bg-brand-sky/30 transition-all">
          <Plus size={14} /> New Goal
        </button>
      </motion.div>

      {/* Create Form */}
      {showCreate && (
        <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }}
          className="glass rounded-xl p-4 mb-6">
          <div className="grid grid-cols-2 gap-3 mb-3">
            <input value={newTitle} onChange={e => setNewTitle(e.target.value)}
              className="col-span-2 px-3 py-2 rounded-lg bg-white border-border shadow-card border border-white/10 text-sm text-gray-300 font-mono focus:outline-none"
              placeholder="Goal title..." />
            <select value={newMetric} onChange={e => setNewMetric(e.target.value)}
              className="px-3 py-2 rounded-lg bg-white border-border shadow-card border border-white/10 text-sm text-gray-400 font-mono focus:outline-none">
              {METRICS.map(m => <option key={m} value={m}>{m.replace(/_/g, " ")}</option>)}
            </select>
            <input type="number" value={newTarget} onChange={e => setNewTarget(e.target.value)}
              className="px-3 py-2 rounded-lg bg-white border-border shadow-card border border-white/10 text-sm text-gray-300 font-mono focus:outline-none"
              placeholder="Target" />
            <input type="date" value={newDeadline} onChange={e => setNewDeadline(e.target.value)}
              className="px-3 py-2 rounded-lg bg-white border-border shadow-card border border-white/10 text-sm text-gray-400 font-mono focus:outline-none" />
          </div>
          <div className="flex justify-end gap-2">
            <button onClick={() => setShowCreate(false)} className="px-4 py-2 rounded-lg text-sm font-mono text-gray-500">Cancel</button>
            <button onClick={create} className="px-4 py-2 rounded-lg bg-brand-sky/20 text-brand-sky text-sm font-mono">Create</button>
          </div>
        </motion.div>
      )}

      {/* Goals */}
      <div className="space-y-3">
        {goals.map((g: any, i: number) => {
          const pct = g.progress_pct || (g.target ? Math.round((g.progress / g.target) * 100) : 0);
          return (
            <motion.div key={g.id || i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className={`glass rounded-xl p-5 ${g.completed ? "border-emerald-500/20" : ""}`}>
              <div className="flex items-center gap-4">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${g.completed ? "bg-emerald-500/20" : "bg-white border-border shadow-card"}`}>
                  <Target size={18} className={g.completed ? "text-emerald-400" : "text-gray-500"} />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className={`text-sm font-display font-bold ${g.completed ? "text-emerald-400" : "text-text-primary"}`}>{g.title}</h3>
                  <p className="text-[10px] font-mono text-gray-500 capitalize">{g.metric?.replace(/_/g, " ")} · {g.progress || 0}/{g.target}</p>
                  <div className="h-1.5 bg-white border-border shadow-card rounded-full overflow-hidden mt-2">
                    <div className={`h-full rounded-full ${g.completed ? "bg-emerald-500" : "bg-brand-sky"}`} style={{ width: `${pct}%` }} />
                  </div>
                </div>
                <div className="flex gap-1 shrink-0">
                  {!g.completed && (
                    <button onClick={() => track(g.id)} className="px-3 py-1.5 rounded-lg bg-brand-sky/20 text-brand-sky text-xs font-mono">
                      <TrendingUp size={12} />
                    </button>
                  )}
                  <button onClick={() => remove(g.id)} className="px-3 py-1.5 rounded-lg text-gray-600 hover:text-red-400 transition-colors">
                    <Trash2 size={12} />
                  </button>
                </div>
              </div>
            </motion.div>
          );
        })}
        {goals.length === 0 && (
          <div className="glass rounded-xl p-12 text-center">
            <Target size={32} className="text-gray-600 mx-auto mb-3" />
            <p className="text-sm text-gray-500 font-mono">No goals yet. Create one to start tracking!</p>
          </div>
        )}
      </div>
    </div>
  );
}
