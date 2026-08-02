import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  BarChart3, Users, Eye, Activity, Clock, Globe,
  TrendingUp, RefreshCw, ArrowUpRight, Zap,
  Database, Server, Shield, CheckCircle2, XCircle
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

function StatCard({ icon: Icon, label, value, color = "text-brand-sky", delay = 0 }: any) {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="glass rounded-xl p-4">
      <div className="flex items-center gap-3">
        <div className={`w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center`}>
          <Icon size={18} className={color} />
        </div>
        <div>
          <p className="text-xs font-mono text-gray-500">{label}</p>
          <p className={`text-xl font-display font-black ${color}`}>{value}</p>
        </div>
      </div>
    </motion.div>
  );
}

function MiniBarChart({ data = [], maxVal }: any) {
  if (!data || data.length === 0) return null;
  const max = maxVal || Math.max(...data.map(d => d.views || d.total || 0), 1);
  return (
    <div className="flex items-end gap-1 h-20">
      {data.slice(-14).map((d, i) => {
        const val = d.views || d.total || 0;
        const h = Math.max((val / max) * 100, 2);
        return (
          <div key={i} className="flex-1 flex flex-col items-center gap-1">
            <div className="w-full bg-brand-sky/30 rounded-t" style={{ height: `${h}%` }}>
              <div className="w-full bg-brand-sky rounded-t" style={{ height: `${h}%` }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default function AdminDashboard() {
  const [realtime, setRealtime] = useState(null);
  const [visitors, setVisitors] = useState([]);
  const [pages, setPages] = useState([]);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = async () => {
    try {
      const [rt, vis, pg, hc] = await Promise.all([
        api.get("/api/v1/analytics/admin/realtime"),
        api.get("/api/v1/analytics/admin/visitors?days=30"),
        api.get("/api/v1/analytics/admin/pages?days=7"),
        api.getHealthStatus().catch(() => null),
      ]);
      setRealtime(rt);
      setVisitors(vis.visitor_stats || vis);
      setPages(pg.page_stats || pg);
      setHealth(hc);
    } catch (err) {
      console.error("Admin analytics error:", err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleRefresh = () => { setRefreshing(true); load(); };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  return (
    <div className="min-h-screen px-4 py-8 max-w-6xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-500/10 border border-red-500/20 mb-3">
              <Activity size={14} className="text-red-400" />
              <span className="text-xs font-mono text-red-400">ADMIN</span>
            </div>
            <h1 className="text-3xl font-display font-black text-text-primary">Analytics Dashboard</h1>
          </div>
          <button onClick={handleRefresh} disabled={refreshing}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 border border-white/10 text-gray-400 text-sm font-mono hover:text-text-primary transition-all">
            <RefreshCw size={14} className={refreshing ? "animate-spin" : ""} />
            Refresh
          </button>
        </div>
      </motion.div>

      {/* Realtime Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard icon={Eye} label="Today's Views" value={realtime?.today_views || 0} color="text-brand-sky" delay={0} />
        <StatCard icon={Users} label="Today Unique" value={realtime?.today_unique || 0} color="text-brand-teal" delay={0.05} />
        <StatCard icon={Activity} label="Active (1hr)" value={realtime?.active_last_hour || 0} color="text-orange-400" delay={0.1} />
        <StatCard icon={Users} label="Total Users" value={realtime?.total_users || 0} color="text-brand-lavender" delay={0.15} />
      </div>

      {/* System Health */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.18 }}
        className="glass rounded-xl p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display font-bold text-text-primary flex items-center gap-2">
            <Shield size={18} className={health?.status === "healthy" ? "text-emerald-400" : "text-amber-400"} />
            System Health
          </h3>
          <span className={`text-[10px] font-mono px-2 py-1 rounded-full border ${
            health?.status === "healthy"
              ? "border-emerald-500/30 text-emerald-400 bg-emerald-500/10"
              : "border-amber-500/30 text-amber-400 bg-amber-500/10"
          }`}>
            {health?.status || "loading"}
          </span>
        </div>

        <div className="grid md:grid-cols-4 gap-3 mb-4">
          <HealthChip icon={Server} label="API" value={health?.status || "unknown"} tone={health?.status === "healthy" ? "good" : "warn"} />
          <HealthChip icon={Database} label="Database" value={health?.database || "unknown"} tone={health?.database === "connected" ? "good" : "warn"} />
          <HealthChip icon={Activity} label="Cache" value={health?.cache?.status || "unknown"} tone="info" />
          <HealthChip icon={Clock} label="Memory" value={health?.memory_mb != null ? `${health.memory_mb} MB` : "n/a"} tone="info" />
        </div>

        <div className="grid md:grid-cols-3 gap-3">
          <MiniHealthCard
            title="Circuit Breakers"
            body={`AI ${health?.circuit_breakers?.ai?.is_open ? "open" : "closed"} · Compiler ${health?.circuit_breakers?.compiler?.is_open ? "open" : "closed"}`}
            icon={Shield}
            status={health?.circuit_breakers?.ai?.is_open || health?.circuit_breakers?.compiler?.is_open ? "warn" : "good"}
          />
          <MiniHealthCard
            title="Tracked Services"
            body={`${health?.metrics?.services?.length || 0} services reporting`}
            icon={BarChart3}
            status="info"
          />
          <MiniHealthCard
            title="Readiness"
            body={health?.status === "healthy" ? "Ready for traffic" : "Degraded but serving"}
            icon={CheckCircle2}
            status={health?.status === "healthy" ? "good" : "warn"}
          />
        </div>

        {health?.metrics?.failures && Object.keys(health.metrics.failures).length > 0 && (
          <div className="mt-4 rounded-lg bg-white/[0.02] border border-white/5 p-3">
            <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-gray-500 mb-2">Recent failures</div>
            <div className="flex flex-wrap gap-2">
              {Object.entries(health.metrics.failures).slice(0, 6).map(([service, count]: [string, any]) => (
                <span key={service} className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-[10px] bg-red-500/10 text-red-300 border border-red-500/20">
                  <XCircle size={10} />
                  {service}: {count}
                </span>
              ))}
            </div>
          </div>
        )}
      </motion.div>

      {/* Visitor Trend */}
      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}
          className="glass rounded-xl p-6">
          <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
            <TrendingUp size={18} className="text-brand-sky" /> Visitor Trend (30 days)
          </h3>
          <MiniBarChart data={visitors} maxVal={Math.max(...visitors.map((v: any) => v.views || v.total || 0), 1)} />
          <div className="flex justify-between mt-2 text-[10px] font-mono text-gray-600">
            <span>{visitors.length > 0 ? visitors[0]?.date : "—"}</span>
            <span>{visitors.length > 0 ? visitors[visitors.length - 1]?.date : "—"}</span>
          </div>
        </motion.div>

        {/* Hourly Distribution */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.25 }}
          className="glass rounded-xl p-6">
          <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
            <Clock size={18} className="text-yellow-400" /> Traffic by Hour
          </h3>
          <div className="space-y-1">
            {Array.from({ length: 24 }, (_, i) => {
              const entry = visitors.find(v => v.hour === i);
              const val = entry?.views || 0;
              const max = Math.max(...visitors.map(v => v.views || 0), 1);
              return (
                <div key={i} className="flex items-center gap-2 text-[10px] font-mono">
                  <span className="w-6 text-gray-600">{String(i).padStart(2, "0")}</span>
                  <div className="flex-1 h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div className="h-full bg-yellow-500/40 rounded-full" style={{ width: `${(val / max) * 100}%` }} />
                  </div>
                  <span className="w-8 text-right text-gray-600">{val}</span>
                </div>
              );
            })}
          </div>
        </motion.div>
      </div>

      {/* Top Pages */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
        className="glass rounded-xl p-6">
        <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
          <Globe size={18} className="text-brand-teal" /> Top Pages (7 days)
        </h3>
        <div className="space-y-2">
          {pages.length === 0 ? (
            <p className="text-gray-500 font-mono text-sm">No data yet. Start visiting pages!</p>
          ) : (
            pages.map((p, i) => (
              <div key={i} className="flex items-center gap-3 p-2 rounded-lg bg-white/[0.02]">
                <span className="w-6 h-6 rounded-full bg-white/5 flex items-center justify-center text-[10px] font-mono text-gray-500">
                  {i + 1}
                </span>
                <span className="flex-1 text-sm font-mono text-gray-300 truncate">{p.path || p._id}</span>
                <span className="text-xs font-mono text-brand-sky">{p.views} views</span>
                <span className="text-xs font-mono text-gray-500">{p.unique_users || 0} users</span>
              </div>
            ))
          )}
        </div>
      </motion.div>
    </div>
  );
}

function HealthChip({ icon: Icon, label, value, tone = "info" }: any) {
  const toneClasses = {
    good: "border-emerald-500/20 bg-emerald-500/10 text-emerald-300",
    warn: "border-amber-500/20 bg-amber-500/10 text-amber-300",
    info: "border-white/10 bg-white/[0.03] text-gray-300",
  };

  return (
    <div className={`rounded-xl border p-3 ${toneClasses[tone] || toneClasses.info}`}>
      <div className="flex items-center gap-2 mb-1">
        <Icon size={12} />
        <span className="text-[10px] font-mono uppercase tracking-[0.2em] opacity-80">{label}</span>
      </div>
      <div className="text-sm font-semibold">{value}</div>
    </div>
  );
}

function MiniHealthCard({ title, body, icon: Icon, status = "info" }: any) {
  const statusClasses = {
    good: "border-emerald-500/20 bg-emerald-500/5",
    warn: "border-amber-500/20 bg-amber-500/5",
    info: "border-white/10 bg-white/[0.02]",
  };

  return (
    <div className={`rounded-xl border p-4 ${statusClasses[status] || statusClasses.info}`}>
      <div className="flex items-center gap-2 mb-2">
        <Icon size={14} className={status === "good" ? "text-emerald-400" : status === "warn" ? "text-amber-400" : "text-brand-sky"} />
        <h4 className="text-sm font-semibold text-text-primary">{title}</h4>
      </div>
      <p className="text-xs text-gray-500">{body}</p>
    </div>
  );
}
