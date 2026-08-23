import { useState, useEffect } from "react";
import { Target, Plus, CheckCircle, Trash2, Save } from "lucide-react";
import api from "../services/api";
import type { Goal } from "../services/api/goals";
import useAuthStore from "../store/authStore";
import { useToast } from "../components/Toast";

const METRICS = [
  { id: "problems", label: "Problems Solved", icon: "🔢" },
  { id: "xp", label: "XP Earned", icon: "⚡" },
  { id: "time", label: "Minutes Studied", icon: "⏰" },
  { id: "tests", label: "Tests Taken", icon: "📝" },
  { id: "interviews", label: "Mock Interviews", icon: "🎤" },
  { id: "lessons", label: "Lessons Completed", icon: "📚" },
];

export default function StudyGoals() {
  const { user } = useAuthStore();
  const toast = useToast();
  const [goals, setGoals] = useState<Goal[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [title, setTitle] = useState("");
  const [target, setTarget] = useState(10);
  const [metric, setMetric] = useState("problems");
  const [deadline, setDeadline] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const isPro = (user?.plan || "") === "pro" || (user?.plan as string) === "lifetime";

  const loadGoals = async () => {
    try {
      const data = await api.goals.list();
      setGoals(data.goals || []);
    } catch (e: any) {
      toast.error(e.message || "Failed to load goals");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadGoals(); }, []);

  const createGoal = async () => {
    if (!title.trim()) return toast.error("Title is required");
    if (target < 1) return toast.error("Target must be at least 1");
    if (!isPro && goals.filter((g) => !g.completed).length >= 3) {
      return toast.warning("Free tier limited to 3 active goals. Upgrade to add more.");
    }
    setSubmitting(true);
    try {
      await api.goals.create(title, target, metric, deadline || null);
      setShowCreate(false);
      setTitle("");
      setTarget(10);
      await loadGoals();
      toast.success("Goal created!");
    } catch (e: any) {
      toast.error(e.message || "Failed to create goal");
    } finally {
      setSubmitting(false);
    }
  };

  const trackGoal = async (goal: Goal) => {
    try {
      const res = await api.goals.track(goal.id, 1);
      if (res.bonus_xp) {
        window.dispatchEvent(new CustomEvent("xp-gained", { detail: { xp: res.bonus_xp } }));
        toast.success(`Goal complete! +${res.bonus_xp} XP`);
      } else {
        toast.success(`Progress: ${res.progress}/${goal.target}`);
      }
      await loadGoals();
    } catch (e: any) {
      toast.error(e.message || "Failed to update goal");
    }
  };

  const deleteGoal = async (goal: Goal) => {
    if (!confirm(`Delete "${goal.title}"?`)) return;
    try {
      await api.goals.delete(goal.id);
      setGoals(goals.filter((g) => g.id !== goal.id));
      toast.success("Goal deleted");
    } catch (e: any) {
      toast.error(e.message || "Failed to delete");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen py-8 px-4 flex items-center justify-center">
        <div className="animate-pulse text-brand-sky">Loading goals…</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-6 sm:py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
              <Target className="text-brand-sky" size={28} />
              Study Goals
            </h1>
            <p className="text-text-secondary mt-1">Set goals, track streaks, earn XP on completion.</p>
          </div>
          <button
            onClick={() => setShowCreate(true)}
            className="px-4 py-2 rounded-xl bg-brand-sky text-text-primary font-bold flex items-center gap-2 hover:bg-brand-sky/90 transition"
          >
            <Plus size={16} /> New Goal
          </button>
        </header>

        {showCreate && (
          <div className="rounded-2xl border border-black/5 bg-white border-border/70 p-6 mb-6">
            <h2 className="text-lg font-bold text-text-primary mb-4">New Goal</h2>
            <div className="space-y-4">
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Solve 30 arrays problems"
                className="w-full rounded-xl border border-black/5 bg-white px-3 py-2 text-sm"
              />
              <div className="flex items-center gap-3">
                <input
                  type="number"
                  min={1}
                  value={target}
                  onChange={(e) => setTarget(Math.max(1, Number(e.target.value)))}
                  className="w-20 rounded-xl border border-black/5 bg-white px-3 py-2 text-sm font-mono"
                />
                <span className="text-sm text-text-light">target</span>
              </div>
              <select
                value={metric}
                onChange={(e) => setMetric(e.target.value)}
                className="w-full rounded-xl border border-black/5 bg-white px-3 py-2 text-sm"
              >
                {METRICS.map((m) => (
                  <option key={m.id} value={m.id}>{m.icon} {m.label}</option>
                ))}
              </select>
              <input
                type="date"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
                className="w-full rounded-xl border border-black/5 bg-white px-3 py-2 text-sm"
              />
              {!isPro && (
                <p className="text-xs text-text-light">Free tier: max 3 active goals. <a href="/pricing" className="text-brand-sky">Upgrade</a> for unlimited.</p>
              )}
            </div>
            <div className="flex gap-2 mt-4">
              <button
                onClick={createGoal}
                disabled={submitting}
                className="px-4 py-2 rounded-xl bg-brand-sky text-text-primary font-bold text-sm hover:bg-brand-sky/90 transition disabled:opacity-50 flex items-center gap-2"
              >
                {submitting ? "Saving..." : <><Save size={14} /> Save Goal</>}
              </button>
              <button
                onClick={() => setShowCreate(false)}
                className="px-4 py-2 rounded-xl border border-black/5 text-text-secondary text-sm hover:bg-surface-2 transition"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Goal list */}
        {goals.length === 0 ? (
          <div className="text-center py-12 text-text-light">
            <Target size={48} className="mx-auto mb-3 opacity-30" />
            <p>No goals yet. Set one to start tracking your progress streak!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {goals.map((g) => {
              const done = g.completed;
              const progressPct = done ? 100 : g.progress_pct;
              return (
                <div
                  key={g.id}
                  className={`rounded-xl border p-4 transition ${
                    done
                      ? "border-green-200 bg-green-50"
                      : "border-black/5 bg-white border-border/70 hover:bg-white"
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {done ? <CheckCircle size={18} className="text-green-500" /> : <Target size={18} className="text-brand-sky" />}
                      <span className={`font-medium ${done ? "line-through text-gray-400" : "text-text-primary"}`}>{g.title}</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <span className="text-text-light">{g.progress}/{g.target}</span>
                      <span className="text-text-light">🔥 {g.streak}d</span>
                      <button onClick={() => deleteGoal(g)} className="text-red-400 hover:text-red-600">
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                  <div className="h-2 rounded-full bg-[#E5E0D3] overflow-hidden mb-2">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-brand-sky to-brand-lavender transition-all"
                      style={{ width: `${progressPct}%` }}
                    />
                  </div>
                  <div className="flex justify-between text-[11px] text-text-light">
                    <span>{METRICS.find((m) => m.id === g.metric)?.label || g.metric}</span>
                    {done && <span className="text-green-500 font-bold">COMPLETE +50 XP</span>}
                  </div>
                  {!done && (
                    <button
                      onClick={() => trackGoal(g)}
                      className="mt-2 w-full rounded-lg bg-brand-sky/10 border border-brand-sky/30 text-brand-sky text-xs font-bold py-1.5 hover:bg-brand-sky/20 transition"
                    >
                      +1 Progress
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
