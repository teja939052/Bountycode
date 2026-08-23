import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  BarChart3, Users, Eye, Activity, Clock, Globe,
  TrendingUp, RefreshCw, Zap, MapPin, UserCheck,
  Database, Server, Shield, CheckCircle2, XCircle,
  Target, ArrowUpRight, Crown, Mail
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

function StatCard({ icon: Icon, label, value, sub, color = "text-brand-sky", delay = 0 }: any) {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="glass rounded-xl p-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-white border-border shadow-card flex items-center justify-center shrink-0">
          <Icon size={18} className={color} />
        </div>
        <div className="min-w-0">
          <p className="text-[10px] font-mono text-gray-500 uppercase tracking-wider">{label}</p>
          <p className={`text-xl font-display font-black ${color}`}>{value}</p>
          {sub && <p className="text-[10px] font-mono text-gray-600 truncate">{sub}</p>}
        </div>
      </div>
    </motion.div>
  );
}

function MiniBarChart({ data = [], maxVal, color = "sky" }: any) {
  if (!data || data.length === 0) return null;
  const max = maxVal || Math.max(...data.map(d => d.views || d.total || d.count || 0), 1);
  const colorMap: Record<string, string> = {
    sky: "bg-brand-sky",
    teal: "bg-brand-teal",
    amber: "bg-amber-500",
    emerald: "bg-emerald-500",
    red: "bg-red-500",
  };
  const barColor = colorMap[color] || colorMap.sky;
  return (
    <div className="flex items-end gap-1 h-24">
      {data.slice(-20).map((d, i) => {
        const val = d.views || d.total || d.count || 0;
        const h = Math.max((val / max) * 100, 2);
        return (
          <div key={i} className="flex-1 flex flex-col items-center gap-1 group relative">
            <div className="w-full bg-white border-border shadow-card rounded-t" style={{ height: `${h}%` }}>
              <div className={`w-full ${barColor} rounded-t opacity-70 group-hover:opacity-100 transition-opacity`} style={{ height: "100%" }} />
            </div>
            <span className="absolute -top-5 text-[8px] font-mono text-gray-500 opacity-0 group-hover:opacity-100 transition-opacity">{val}</span>
          </div>
        );
      })}
    </div>
  );
}

type Tab = "overview" | "users" | "pages" | "features" | "geo";
const TABS: { key: Tab; label: string; icon: any }[] = [
  { key: "overview", label: "Overview", icon: BarChart3 },
  { key: "users", label: "Users", icon: Users },
  { key: "pages", label: "Pages", icon: Globe },
  { key: "features", label: "Features", icon: Zap },
  { key: "geo", label: "Geo / Retention", icon: MapPin },
];

export default function AdminDashboard() {
  const [tab, setTab] = useState<Tab>("overview");
  const [realtime, setRealtime] = useState<any>(null);
  const [visitors, setVisitors] = useState<any[]>([]);
  const [pages, setPages] = useState<any[]>([]);
  const [features, setFeatures] = useState<any[]>([]);
  const [hourly, setHourly] = useState<any[]>([]);
  const [geo, setGeo] = useState<any[]>([]);
  const [retention, setRetention] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [userSummary, setUserSummary] = useState<any>(null);
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = async () => {
    try {
      const results = await Promise.allSettled([
        api.get("/api/v1/analytics/admin/realtime"),
        api.get("/api/v1/analytics/admin/visitors?days=30"),
        api.get("/api/v1/analytics/admin/pages?days=7"),
        api.get("/api/v1/analytics/admin/features?days=30"),
        api.get("/api/v1/analytics/admin/hourly?days=7"),
        api.get("/api/v1/analytics/admin/geo?days=30"),
        api.get("/api/v1/analytics/admin/retention?days=30"),
        api.get("/api/v1/analytics/admin/users?days=30&limit=50"),
        api.get("/api/v1/analytics/admin/summary"),
        api.getHealthStatus().catch(() => null),
      ]);
      const pick = (r: PromiseSettledResult<any>) => r.status === "fulfilled" ? r.value : null;
      setRealtime(pick(results[0]));
      setVisitors(pick(results[1]) || []);
      setPages(pick(results[2]) || []);
      setFeatures(pick(results[3]) || []);
      setHourly(pick(results[4]) || []);
      setGeo(pick(results[5]) || []);
      setRetention(pick(results[6]));
      setUsers(pick(results[7]) || []);
      setUserSummary(pick(results[8]));
      setHealth(pick(results[9]));
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

  const visitorMax = Math.max(...visitors.map((v: any) => v.total_views || v.views || v.total || 0), 1);
  const hourlyMax = Math.max(...hourly.map((h: any) => h.views || 0), 1);

  return (
    <div className="min-h-screen px-4 py-8 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-500/10 border border-red-500/20 mb-3">
              <Shield size={14} className="text-red-400" />
              <span className="text-xs font-mono text-red-400 tracking-wider">ADMIN ONLY</span>
            </div>
            <h1 className="text-3xl font-display font-black text-text-primary">Analytics Console</h1>
            <p className="text-sm text-gray-500 font-mono mt-1">Real-time platform intelligence</p>
          </div>
          <button onClick={handleRefresh} disabled={refreshing}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white border-border shadow-card border border-white/10 text-gray-400 text-sm font-mono hover:text-text-primary transition-all">
            <RefreshCw size={14} className={refreshing ? "animate-spin" : ""} />
            Refresh
          </button>
        </div>
      </motion.div>

      {/* Top Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-6">
        <StatCard icon={Eye} label="Today Views" value={realtime?.today_views || 0} color="text-brand-sky" delay={0} />
        <StatCard icon={Users} label="Today Unique" value={realtime?.today_unique || 0} color="text-brand-teal" delay={0.05} />
        <StatCard icon={Activity} label="Active (1hr)" value={realtime?.active_last_hour || 0} color="text-orange-400" delay={0.1} />
        <StatCard icon={Crown} label="Total Users" value={realtime?.total_users || 0} color="text-brand-lavender" delay={0.15} />
        <StatCard icon={UserCheck} label="Active Today" value={userSummary?.active_today || realtime?.today_unique || 0} color="text-emerald-400" delay={0.2} />
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 p-1 bg-white/[0.03] rounded-xl border border-white/5 overflow-x-auto">
        {TABS.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-mono transition-all whitespace-nowrap ${
              tab === t.key
                ? "bg-white border-border/10 text-text-primary border border-white/10"
                : "text-gray-500 hover:text-gray-300"
            }`}>
            <t.icon size={14} />
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab: Overview */}
      {tab === "overview" && (
        <div className="space-y-6">
          {/* System Health */}
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            className="glass rounded-xl p-6">
            <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
              <Shield size={18} className={health?.status === "healthy" ? "text-emerald-400" : "text-amber-400"} />
              System Health
              <span className={`ml-auto text-[10px] font-mono px-2 py-1 rounded-full border ${
                health?.status === "healthy"
                  ? "border-emerald-500/30 text-emerald-400 bg-emerald-500/10"
                  : "border-amber-500/30 text-amber-400 bg-amber-500/10"
              }`}>
                {health?.status || "unknown"}
              </span>
            </h3>
            <div className="grid md:grid-cols-4 gap-3 mb-4">
              <HealthChip icon={Server} label="API" value={health?.status || "unknown"} tone={health?.status === "healthy" ? "good" : "warn"} />
              <HealthChip icon={Database} label="Database" value={health?.database || "unknown"} tone={health?.database === "connected" ? "good" : "warn"} />
              <HealthChip icon={Activity} label="Cache" value={health?.cache?.status || "unknown"} tone="info" />
              <HealthChip icon={Server} label="Memory" value={health?.memory_mb != null ? `${health.memory_mb} MB` : "n/a"} tone="info" />
            </div>
            {health?.metrics?.failures && Object.keys(health.metrics.failures).length > 0 && (
              <div className="rounded-lg bg-white/[0.02] border border-white/5 p-3 mt-3">
                <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-gray-500 mb-2">Recent failures</div>
                <div className="flex flex-wrap gap-2">
                  {Object.entries(health.metrics.failures).slice(0, 6).map(([service, count]: [string, any]) => (
                    <span key={service} className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-[10px] bg-red-500/10 text-red-300 border border-red-500/20">
                      <XCircle size={10} /> {service}: {count}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </motion.div>

          {/* Charts Row */}
          <div className="grid md:grid-cols-2 gap-6">
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}
              className="glass rounded-xl p-6">
              <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
                <TrendingUp size={18} className="text-brand-sky" /> Visitor Trend (30d)
              </h3>
              {visitors.length > 0 ? (
                <>
                  <MiniBarChart data={visitors.map((v: any) => ({ views: v.total_views || v.views || v.total || 0 }))} maxVal={visitorMax} color="sky" />
                  <div className="flex justify-between mt-2 text-[10px] font-mono text-gray-600">
                    <span>{visitors[0]?.date}</span>
                    <span>{visitors[visitors.length - 1]?.date}</span>
                  </div>
                </>
              ) : <EmptyState text="No visitor data yet" />}
            </motion.div>

            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.15 }}
              className="glass rounded-xl p-6">
              <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
                <Clock size={18} className="text-yellow-400" /> Traffic by Hour (7d)
              </h3>
              {hourly.length > 0 ? (
                <div className="space-y-1 max-h-64 overflow-y-auto pr-1">
                  {Array.from({ length: 24 }, (_, i) => {
                    const entry = hourly.find((h: any) => h.hour === i);
                    const val = entry?.views || 0;
                    return (
                      <div key={i} className="flex items-center gap-2 text-[10px] font-mono">
                        <span className="w-6 text-gray-600">{String(i).padStart(2, "0")}</span>
                        <div className="flex-1 h-1.5 bg-white border-border shadow-card rounded-full overflow-hidden">
                          <div className="h-full bg-yellow-500/40 rounded-full" style={{ width: `${(val / hourlyMax) * 100}%` }} />
                        </div>
                        <span className="w-8 text-right text-gray-500">{val}</span>
                      </div>
                    );
                  })}
                </div>
              ) : <EmptyState text="No hourly data yet" />}
            </motion.div>
          </div>

          {/* Retention Quick Stats */}
          {retention && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}
              className="glass rounded-xl p-6">
              <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
                <UserCheck size={18} className="text-emerald-400" /> Visitor Retention (30d)
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-3 rounded-lg bg-white/[0.02]">
                  <p className="text-2xl font-display font-black text-brand-sky">{retention.total_visitors || 0}</p>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">Total Visitors</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-white/[0.02]">
                  <p className="text-2xl font-display font-black text-emerald-400">{retention.new_users || 0}</p>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">New Visitors</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-white/[0.02]">
                  <p className="text-2xl font-display font-black text-amber-400">{retention.returning_users || 0}</p>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">Returning Visitors</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-white/[0.02]">
                  <p className="text-2xl font-display font-black text-brand-lavender">{retention.retention_rate || 0}%</p>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">Retention Rate</p>
                </div>
              </div>
            </motion.div>
          )}

          {/* User Summary */}
          {userSummary && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.25 }}
              className="glass rounded-xl p-6">
              <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
                <Users size={18} className="text-brand-lavender" /> User Summary
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div className="text-center p-3 rounded-lg bg-white/[0.02]">
                  <p className="text-xl font-display font-black text-text-primary">{userSummary.total_users || 0}</p>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">Total Users</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-emerald-500/5 border border-emerald-500/10">
                  <p className="text-xl font-display font-black text-emerald-400">{userSummary.plan_counts?.pro || 0}</p>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">Pro Users</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-white/[0.02]">
                  <p className="text-xl font-display font-black text-gray-400">{userSummary.plan_counts?.free || 0}</p>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">Free Users</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-white/[0.02]">
                  <p className="text-xl font-display font-black text-brand-sky">{userSummary.new_today || 0}</p>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">New Today</p>
                </div>
                <div className="text-center p-3 rounded-lg bg-white/[0.02]">
                  <p className="text-xl font-display font-black text-amber-400">{userSummary.new_this_week || 0}</p>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">New This Week</p>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      )}

      {/* Tab: Users */}
      {tab === "users" && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass rounded-xl p-6">
          <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
            <Users size={18} className="text-brand-lavender" /> User Activity (30d)
          </h3>
          {users.length === 0 ? (
            <EmptyState text="No user activity data yet" />
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/5">
                    <th className="text-left py-2 px-3 text-[10px] font-mono text-gray-500 uppercase tracking-wider">#</th>
                    <th className="text-left py-2 px-3 text-[10px] font-mono text-gray-500 uppercase tracking-wider">User</th>
                    <th className="text-left py-2 px-3 text-[10px] font-mono text-gray-500 uppercase tracking-wider">Plan</th>
                    <th className="text-right py-2 px-3 text-[10px] font-mono text-gray-500 uppercase tracking-wider">Views</th>
                    <th className="text-right py-2 px-3 text-[10px] font-mono text-gray-500 uppercase tracking-wider">Pages</th>
                    <th className="text-right py-2 px-3 text-[10px] font-mono text-gray-500 uppercase tracking-wider">Last Active</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u: any, i: number) => (
                    <tr key={i} className="border-b border-white/[0.03] hover:bg-white/[0.02] transition-colors">
                      <td className="py-2.5 px-3 font-mono text-gray-600 text-xs">{i + 1}</td>
                      <td className="py-2.5 px-3">
                        <div className="flex items-center gap-2">
                          <div className="w-7 h-7 rounded-full bg-white border-border shadow-card flex items-center justify-center text-[10px] font-mono text-gray-400">
                            {(u.name || u.email || "?")[0].toUpperCase()}
                          </div>
                          <div className="min-w-0">
                            <p className="text-sm text-gray-300 truncate">{u.name || "Anonymous"}</p>
                            <p className="text-[10px] text-gray-600 font-mono truncate">{u.email || u.user_id?.slice(0, 12) + "..."}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-2.5 px-3">
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${
                          u.plan === "pro" ? "border-emerald-500/30 text-emerald-400 bg-emerald-500/10"
                          : u.plan === "lifetime" ? "border-amber-500/30 text-amber-400 bg-amber-500/10"
                          : "border-white/10 text-gray-500 bg-white/[0.03]"
                        }`}>
                          {u.plan || "free"}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-right font-mono text-sm text-brand-sky">{u.total_views}</td>
                      <td className="py-2.5 px-3 text-right font-mono text-sm text-gray-400">{u.pages_count}</td>
                      <td className="py-2.5 px-3 text-right font-mono text-[10px] text-gray-600">
                        {u.last_active ? new Date(u.last_active).toLocaleDateString() : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>
      )}

      {/* Tab: Pages */}
      {tab === "pages" && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass rounded-xl p-6">
          <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
            <Globe size={18} className="text-brand-teal" /> Top Pages (7d)
          </h3>
          {pages.length === 0 ? (
            <EmptyState text="No page data yet" />
          ) : (
            <div className="space-y-2">
              {pages.map((p: any, i: number) => {
                const maxViews = pages[0]?.views || 1;
                const pct = Math.round((p.views / maxViews) * 100);
                return (
                  <div key={i} className="flex items-center gap-3 p-3 rounded-lg bg-white/[0.02] hover:bg-white/[0.04] transition-colors">
                    <span className="w-7 h-7 rounded-full bg-white border-border shadow-card flex items-center justify-center text-[10px] font-mono text-gray-500 shrink-0">
                      {i + 1}
                    </span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-mono text-gray-300 truncate">{p.path || p._id}</span>
                        <span className="text-xs font-mono text-brand-sky shrink-0 ml-2">{p.views} views</span>
                      </div>
                      <div className="h-1 bg-white border-border shadow-card rounded-full overflow-hidden">
                        <div className="h-full bg-brand-sky/40 rounded-full" style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                    <span className="text-[10px] font-mono text-gray-600 shrink-0">{p.unique_users || 0} users</span>
                  </div>
                );
              })}
            </div>
          )}
        </motion.div>
      )}

      {/* Tab: Features */}
      {tab === "features" && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass rounded-xl p-6">
          <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
            <Zap size={18} className="text-amber-400" /> Feature Usage (30d)
          </h3>
          {features.length === 0 ? (
            <EmptyState text="No feature usage data yet" />
          ) : (
            <div className="space-y-2">
              {features.map((f: any, i: number) => {
                const maxUses = features[0]?.uses || 1;
                const pct = Math.round((f.uses / maxUses) * 100);
                const colors = ["text-brand-sky", "text-brand-teal", "text-amber-400", "text-emerald-400", "text-brand-lavender"];
                return (
                  <div key={i} className="flex items-center gap-3 p-3 rounded-lg bg-white/[0.02] hover:bg-white/[0.04] transition-colors">
                    <span className={`w-7 h-7 rounded-full bg-white border-border shadow-card flex items-center justify-center text-[10px] font-mono shrink-0 ${colors[i % colors.length]}`}>
                      {i + 1}
                    </span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-mono text-gray-300 truncate">{f.feature || f._id}</span>
                        <span className="text-xs font-mono text-amber-400 shrink-0 ml-2">{f.uses} uses</span>
                      </div>
                      <div className="h-1 bg-white border-border shadow-card rounded-full overflow-hidden">
                        <div className="h-full bg-amber-500/40 rounded-full" style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                    <span className="text-[10px] font-mono text-gray-600 shrink-0">{f.unique_users || 0} users</span>
                  </div>
                );
              })}
            </div>
          )}
        </motion.div>
      )}

      {/* Tab: Geo / Retention */}
      {tab === "geo" && (
        <div className="space-y-6">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass rounded-xl p-6">
            <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
              <MapPin size={18} className="text-brand-teal" /> Geo Breakdown by IP (30d)
            </h3>
            {geo.length === 0 ? (
              <EmptyState text="No geo data yet — IP addresses are captured on page views" />
            ) : (
              <div className="space-y-2">
                {geo.map((g: any, i: number) => {
                  const maxVisits = geo[0]?.visits || 1;
                  const pct = Math.round((g.visits / maxVisits) * 100);
                  return (
                    <div key={i} className="flex items-center gap-3 p-3 rounded-lg bg-white/[0.02]">
                      <span className="w-7 h-7 rounded-full bg-white border-border shadow-card flex items-center justify-center text-[10px] font-mono text-gray-500 shrink-0">
                        {i + 1}
                      </span>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-mono text-gray-300">{g.ip || g._id || "unknown"}</span>
                          <span className="text-xs font-mono text-brand-teal shrink-0 ml-2">{g.visits} visits</span>
                        </div>
                        <div className="h-1 bg-white border-border shadow-card rounded-full overflow-hidden">
                          <div className="h-full bg-brand-teal/40 rounded-full" style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </motion.div>

          {retention && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}
              className="glass rounded-xl p-6">
              <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
                <UserCheck size={18} className="text-emerald-400" /> Retention (30d)
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 rounded-lg bg-white/[0.02]">
                  <p className="text-3xl font-display font-black text-brand-sky">{retention.total_visitors || 0}</p>
                  <p className="text-xs font-mono text-gray-500 mt-2">Total Visitors</p>
                </div>
                <div className="text-center p-4 rounded-lg bg-emerald-500/5 border border-emerald-500/10">
                  <p className="text-3xl font-display font-black text-emerald-400">{retention.new_users || 0}</p>
                  <p className="text-xs font-mono text-gray-500 mt-2">New</p>
                </div>
                <div className="text-center p-4 rounded-lg bg-amber-500/5 border border-amber-500/10">
                  <p className="text-3xl font-display font-black text-amber-400">{retention.returning_users || 0}</p>
                  <p className="text-xs font-mono text-gray-500 mt-2">Returning</p>
                </div>
                <div className="text-center p-4 rounded-lg bg-brand-lavender/5 border border-brand-lavender/10">
                  <p className="text-3xl font-display font-black text-brand-lavender">{retention.retention_rate || 0}%</p>
                  <p className="text-xs font-mono text-gray-500 mt-2">Retention Rate</p>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      )}
    </div>
  );
}

function EmptyState({ text }: { text: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="w-16 h-16 rounded-2xl bg-white border-border shadow-card flex items-center justify-center mb-4">
        <BarChart3 size={24} className="text-gray-600" />
      </div>
      <p className="text-sm text-gray-500 font-mono">{text}</p>
      <p className="text-[10px] text-gray-600 font-mono mt-1">Data appears after users visit pages</p>
    </div>
  );
}

function HealthChip({ icon: Icon, label, value, tone = "info" }: any) {
  const toneClasses: Record<string, string> = {
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
