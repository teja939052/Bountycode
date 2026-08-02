import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Users, Activity, BarChart3, RefreshCw, Inbox } from "lucide-react";
import { metricsApi } from "../services/api/metrics.ts";

function StatCard({ icon: Icon, label, value }) {
  return (
    <div className="rounded-xl border border-white/10 bg-slate-900/60 p-5">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center">
          <Icon size={18} className="text-indigo-400" />
        </div>
        <div>
          <p className="text-xs text-slate-400">{label}</p>
          <p className="text-2xl font-bold text-white">{value ?? 0}</p>
        </div>
      </div>
    </div>
  );
}

export default function RetentionAdmin() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await metricsApi.retention();
      setData(res);
    } catch (err) {
      setError(err.message || "Failed to load retention data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const overall = data?.overall || null;
  const daily = overall?.daily_active || [];
  const maxDaily = Math.max(...daily.map((d) => d.users || 0), 1);
  const features = data?.features || [];

  const topEvents = (breakdown) =>
    [...(breakdown || [])].sort((a, b) => b.count - a.count).slice(0, 3);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 px-6 py-10">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-white">Retention Analytics</h1>
            <p className="text-sm text-slate-400 mt-1">Gamification feature engagement</p>
          </div>
          <button
            onClick={load}
            className="flex items-center gap-2 px-4 py-2 rounded-lg border border-white/10 text-sm text-slate-300 hover:bg-white/5"
          >
            <RefreshCw size={16} /> Refresh
          </button>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-lg border border-red-500/30 bg-red-500/10 text-sm text-red-300">
            {error}
          </div>
        )}

        {overall && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"
          >
            <StatCard icon={Users} label="Active Users (7d)" value={overall.total_active_users_7d} />
            <StatCard icon={Activity} label="Events (7d)" value={overall.events_last_7d} />
            <StatCard
              icon={BarChart3}
              label="Daily Active (avg)"
              value={Math.round(
                daily.reduce((sum, d) => sum + (d.users || 0), 0) / Math.max(daily.length, 1)
              )}
            />
          </motion.div>
        )}

        {overall && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8 rounded-xl border border-white/10 bg-slate-900/60 p-5"
          >
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Daily Active Users</h2>
            <div className="flex items-end gap-2 h-32">
              {daily.map((d) => (
                <div key={d.day} className="flex-1 flex flex-col items-center gap-2">
                  <span className="text-[10px] text-slate-400">{d.users}</span>
                  <div
                    className="w-full rounded-t bg-gradient-to-t from-indigo-600 to-indigo-400"
                    style={{ height: `${Math.max((d.users / maxDaily) * 100, 2)}%` }}
                  />
                  <span className="text-[10px] text-slate-500">{d.day.slice(5)}</span>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-white/10 bg-slate-900/60 overflow-hidden"
        >
          <div className="p-5 border-b border-white/10">
            <h2 className="text-sm font-semibold text-slate-300">Feature Breakdown</h2>
          </div>
          {features.length === 0 ? (
            <div className="p-10 flex flex-col items-center text-slate-500">
              <Inbox size={32} className="mb-2" />
              <p className="text-sm">No feature events recorded yet</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-slate-400 border-b border-white/10">
                    <th className="px-5 py-3 font-medium">Feature</th>
                    <th className="px-5 py-3 font-medium">Active Users (7d)</th>
                    <th className="px-5 py-3 font-medium">Total Events</th>
                    <th className="px-5 py-3 font-medium">Top Events</th>
                  </tr>
                </thead>
                <tbody>
                  {features.map((f) => (
                    <tr
                      key={f.feature}
                      className="border-b border-white/5 last:border-0 hover:bg-white/5"
                    >
                      <td className="px-5 py-3 font-medium text-slate-200">{f.feature}</td>
                      <td className="px-5 py-3 text-slate-300">{f.active_users}</td>
                      <td className="px-5 py-3 text-slate-300">{f.total_events}</td>
                      <td className="px-5 py-3">
                        {topEvents(f.event_breakdown).length === 0 ? (
                          <span className="text-xs text-slate-600">No events</span>
                        ) : (
                          <div className="flex flex-wrap gap-2">
                            {topEvents(f.event_breakdown).map((e) => (
                              <span
                                key={e.event}
                                className="px-2 py-1 rounded-md border border-white/10 bg-white/5 text-xs text-slate-300"
                              >
                                {e.event} <span className="text-indigo-300">×{e.count}</span>
                              </span>
                            ))}
                          </div>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
