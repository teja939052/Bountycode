import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import {
  Building2, Users, Plus, BarChart3
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import AnimatedCard from "../components/motion/AnimatedCard";

export default function Enterprise() {
  const [cohorts, setCohorts] = useState([]);
  const [selected, setSelected] = useState(null);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: "", institution: "" });
  const [error, setError] = useState("");
  const reduced = useReducedMotion();

  useEffect(() => {
    loadCohorts();
  }, []);

  const loadCohorts = async () => {
    setLoading(true);
    try {
      const data = await api.getEnterpriseCohorts();
      setCohorts(data.cohorts || []);
    } catch { setError("Failed to load cohorts"); } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.createEnterpriseCohort({ name: form.name, institution: form.institution });
      setForm({ name: "", institution: "" });
      setShowForm(false);
      loadCohorts();
    } catch { setError("Failed to create cohort"); }
  };

  const handleSelect = async (cohort) => {
    setSelected(cohort);
    setLoading(true);
    try {
      const data = await api.getCohortProgress(cohort.cohort_id);
      setProgress(data);
    } catch { setError("Failed to load cohort progress"); } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div className="mb-8" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-xl flex items-center justify-center">
                <Building2 size={24} className="text-indigo-600" />
              </div>
              <div>
                <h1 className="text-3xl font-bold dark:text-text-primary">Enterprise Portal</h1>
                <p className="text-gray-600 dark:text-gray-400">Campus & institutional placement management</p>
              </div>
            </div>
            <button onClick={() => setShowForm(true)} className="btn-primary flex items-center gap-2">
              <Plus size={18} /> New Cohort
            </button>
          </div>
        </motion.div>

        {error && (
          <div className="mb-6 px-4 py-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 text-sm">
            {error}
            <button onClick={() => setError("")} className="ml-2 underline">dismiss</button>
          </div>
        )}

        {/* Create Cohort Modal */}
        <AnimatePresence>
          {showForm && (
            <motion.div
              className="fixed inset-0 z-50 flex items-center justify-center bg-surface-2 backdrop-blur-sm p-4"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setShowForm(false)}
            >
              <motion.div
                className="bg-white dark:bg-gray-900 rounded-2xl p-6 max-w-md w-full"
                initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}
                onClick={(e) => e.stopPropagation()}
              >
                <h2 className="text-xl font-bold dark:text-text-primary mb-4">Create Cohort</h2>
                <form onSubmit={handleCreate} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Cohort Name</label>
                    <input className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required placeholder="e.g. IIT Bombay CSE 2025" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Institution</label>
                    <input className="input" value={form.institution} onChange={(e) => setForm({ ...form, institution: e.target.value })} required placeholder="e.g. IIT Bombay" />
                  </div>
                  <div className="flex gap-3">
                    <button type="button" onClick={() => setShowForm(false)} className="flex-1 btn-secondary">Cancel</button>
                    <button type="submit" className="flex-1 btn-primary">Create</button>
                  </div>
                </form>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {loading && cohorts.length === 0 ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
          </div>
        ) : (
          <div className="grid md:grid-cols-3 gap-6">
            {/* Cohorts List */}
            <div className="md:col-span-1 space-y-3">
              <h3 className="font-semibold text-sm text-gray-500 uppercase tracking-wider mb-3">Your Cohorts</h3>
              {cohorts.length === 0 ? (
                <p className="text-sm text-gray-400">No cohorts yet. Create one to get started.</p>
              ) : (
                cohorts.map((c) => (
                  <button
                    key={c.cohort_id}
                    onClick={() => handleSelect(c)}
                    className={`w-full text-left p-4 rounded-xl border transition-colors ${
                      selected?.cohort_id === c.cohort_id
                        ? "border-primary-500 bg-primary-50/50 dark:bg-primary-900/10"
                        : "border-space-border hover:border-gray-600"
                    }`}
                  >
                    <p className="font-semibold text-sm dark:text-text-primary">{c.name}</p>
                    <p className="text-xs text-gray-500">{c.institution}</p>
                    <p className="text-xs text-gray-400 mt-1">{c.student_count} students</p>
                  </button>
                ))
              )}
            </div>

            {/* Progress View */}
            <div className="md:col-span-2">
              {selected && progress ? (
                <AnimatedCard className="card">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="font-bold text-lg dark:text-text-primary">{progress.name}</h3>
                      <p className="text-sm text-gray-500">{progress.count} students tracked</p>
                    </div>
                    <BarChart3 size={20} className="text-primary-600" />
                  </div>

                  {(!progress?.students || progress.students.length === 0) ? (
                    <p className="text-sm text-gray-400">No student data available yet.</p>
                  ) : (
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="text-left text-gray-500 border-b border-space-border">
                            <th className="pb-2 font-medium">Student</th>
                            <th className="pb-2 font-medium">Level</th>
                            <th className="pb-2 font-medium">XP</th>
                            <th className="pb-2 font-medium">Skill Score</th>
                            <th className="pb-2 font-medium">Streak</th>
                          </tr>
                        </thead>
                        <tbody>
                          {progress.students.slice(0, 20).map((s, i) => (
                            <tr key={s.user_id || i} className="border-b border-gray-800/50">
                              <td className="py-2 font-mono text-xs text-gray-400">{s.user_id?.slice(-6) || "???"}</td>
                              <td className="py-2 text-gray-300">{s.level}</td>
                              <td className="py-2 text-gray-300">{s.xp}</td>
                              <td className="py-2">
                                <span className={`font-medium ${s.overall_score >= 70 ? "text-green-400" : s.overall_score >= 40 ? "text-yellow-400" : "text-red-400"}`}>
                                  {s.overall_score}
                                </span>
                              </td>
                              <td className="py-2 text-gray-300">{s.streak} days</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </AnimatedCard>
              ) : (
                <div className="card text-center py-12">
                  <Users size={48} className="mx-auto text-gray-300 dark:text-gray-600 mb-4" />
                  <p className="text-gray-500 dark:text-gray-400">Select a cohort to view progress</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
