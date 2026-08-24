import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Target, TrendingUp, AlertTriangle, CheckCircle2, Building2 } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function ReadinessScore() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [company, setCompany] = useState("");

  const load = async (c?: string) => {
    setLoading(true);
    try {
      const url = c ? `/api/v1/readiness/score?company=${encodeURIComponent(c)}` : "/api/v1/readiness/score";
      const d = await api.get(url);
      setData(d);
    } catch { }
    setLoading(false);
  };

  useEffect(() => { load(); }, []);

  if (loading && !data) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  return (
    <div className="min-h-screen px-4 py-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-3">
          <Target size={14} className="text-emerald-400" />
          <span className="text-xs font-mono text-emerald-400">READINESS</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Interview Readiness</h1>
      </motion.div>

      {/* Grand Line cross-fleet comparison */}
      <Link
        to="/grand-line"
        className="bounty-card mb-6 flex items-center gap-4 p-4 transition-transform hover:scale-[1.01]"
      >
        <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-reward/10 text-reward">
          <Building2 size={22} />
        </span>
        <span className="min-w-0 flex-1">
          <span className="block font-bold text-text">Grand Line Assessment</span>
          <span className="block text-sm text-text-muted">
            Compare yourself across the whole recruiter fleet — gaps, focus hours, voyage plan
          </span>
        </span>
        <span className="text-text-muted">→</span>
      </Link>

      {/* Company Filter */}
      <div className="flex gap-3 mb-6">
        <input value={company} onChange={e => setCompany(e.target.value)}
          onKeyDown={e => e.key === "Enter" && load(company)}
          className="flex-1 px-4 py-2.5 rounded-xl bg-white border-border shadow-card border border-white/10 text-sm text-gray-300 font-mono focus:outline-none focus:border-emerald-500/40"
          placeholder="Check readiness for a company (e.g., Google)..." />
        <button onClick={() => load(company)}
          className="px-5 py-2.5 rounded-xl bg-emerald-500/20 text-emerald-400 font-mono text-sm hover:bg-emerald-500/30 transition-all">
          Check
        </button>
      </div>

      {data && (
        <>
          {/* Score Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
            <div className="glass rounded-xl p-4 text-center">
              <div className="text-3xl font-display font-black text-emerald-400">{data.overall || 0}%</div>
              <p className="text-[10px] font-mono text-gray-500 mt-1">Overall Score</p>
            </div>
            {data.company_score != null && (
              <div className="glass rounded-xl p-4 text-center">
                <div className="text-3xl font-display font-black text-brand-sky">{data.company_score}%</div>
                <p className="text-[10px] font-mono text-gray-500 mt-1">{company || "Company"} Match</p>
              </div>
            )}
            {data.prediction && (
              <div className="glass rounded-xl p-4 text-center">
                <div className="text-3xl font-display font-black text-amber-400">{data.prediction}</div>
                <p className="text-[10px] font-mono text-gray-500 mt-1">Prediction</p>
              </div>
            )}
            {data.company_match != null && (
              <div className="glass rounded-xl p-4 text-center">
                <div className={`text-3xl font-display font-black ${data.company_match ? "text-emerald-400" : "text-red-400"}`}>
                  {data.company_match ? "Yes" : "No"}
                </div>
                <p className="text-[10px] font-mono text-gray-500 mt-1">Company Match</p>
              </div>
            )}
          </div>

          {/* Categories */}
          {data.categories && (
            <div className="glass rounded-xl p-6 mb-6">
              <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
                <TrendingUp size={18} className="text-brand-sky" /> Skill Breakdown
              </h3>
              <div className="space-y-3">
                {Object.entries(data.categories).map(([name, cat]: [string, any]) => (
                  <div key={name}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-gray-300 font-mono capitalize">{name.replace(/_/g, " ")}</span>
                      <span className="text-sm font-mono text-brand-sky">{cat.score || 0}%</span>
                    </div>
                    <div className="h-2 bg-white border-border shadow-card rounded-full overflow-hidden">
                      <div className="h-full bg-brand-sky/60 rounded-full" style={{ width: `${cat.score || 0}%` }} />
                    </div>
                    {cat.details && <p className="text-[10px] font-mono text-gray-600 mt-1">{cat.details}</p>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations */}
          {data.recommendations?.length > 0 && (
            <div className="glass rounded-xl p-6">
              <h3 className="font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                <AlertTriangle size={18} className="text-amber-400" /> Recommendations
              </h3>
              <div className="space-y-2">
                {data.recommendations.map((r: string, i: number) => (
                  <div key={i} className="flex items-start gap-2 text-sm text-gray-400">
                    <CheckCircle2 size={14} className="text-amber-400 mt-0.5 shrink-0" />
                    <span>{r}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
