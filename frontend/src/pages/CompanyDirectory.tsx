import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Building2, Search, Calendar, ExternalLink, ChevronRight } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function CompanyDirectory() {
  const [companies, setCompanies] = useState<any[]>([]);
  const [filters, setFilters] = useState<any>({});
  const [search, setSearch] = useState("");
  const [selectedType, setSelectedType] = useState("");
  const [selectedTier, setSelectedTier] = useState("");
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<any>(null);

  useEffect(() => {
    Promise.all([
      api.get("/api/v1/company-directory/companies?limit=50"),
      api.get("/api/v1/company-directory/filters"),
    ]).then(([c, f]: any[]) => {
      setCompanies(c.companies || []);
      setFilters(f);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const searchCompanies = async () => {
    setLoading(true);
    try {
      let url = `/api/v1/company-directory/companies?limit=50`;
      if (search) url += `&q=${encodeURIComponent(search)}`;
      if (selectedType) url += `&type=${selectedType}`;
      if (selectedTier) url += `&tier=${selectedTier}`;
      const d = await api.get(url);
      setCompanies(d.companies || []);
    } catch { }
    setLoading(false);
  };

  useEffect(() => { searchCompanies(); }, [selectedType, selectedTier]);

  if (loading && companies.length === 0) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  return (
    <div className="min-h-screen px-4 py-8 max-w-6xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-sky/10 border border-brand-sky/20 mb-3">
          <Building2 size={14} className="text-brand-sky" />
          <span className="text-xs font-mono text-brand-sky">COMPANIES</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Company Directory</h1>
        <p className="text-sm text-gray-500 mt-1">{companies.length} companies with interview guides and prep tips</p>
      </motion.div>

      {/* Search + Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <div className="flex-1 min-w-[200px] relative">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
          <input value={search} onChange={e => setSearch(e.target.value)} onKeyDown={e => e.key === "Enter" && searchCompanies()}
            className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-sm text-gray-300 font-mono focus:outline-none focus:border-brand-sky/40"
            placeholder="Search companies..." />
        </div>
        <select value={selectedType} onChange={e => setSelectedType(e.target.value)}
          className="px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 text-sm text-gray-400 font-mono focus:outline-none">
          <option value="">All Types</option>
          {(filters.types || []).map((t: string) => <option key={t} value={t}>{t}</option>)}
        </select>
        <select value={selectedTier} onChange={e => setSelectedTier(e.target.value)}
          className="px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 text-sm text-gray-400 font-mono focus:outline-none">
          <option value="">All Tiers</option>
          {(filters.tiers || []).map((t: string) => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>

      {/* Company Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {companies.map((c: any, i: number) => (
          <motion.div key={c.company_id || i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.03 }}
            onClick={() => setSelected(c)}
            className="glass rounded-xl p-5 cursor-pointer hover:border-brand-sky/20 transition-all group">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-lg font-display font-black text-brand-sky">
                {c.name?.[0] || "?"}
              </div>
              <div className="min-w-0">
                <h3 className="text-sm font-display font-bold text-text-primary truncate">{c.name}</h3>
                <p className="text-[10px] font-mono text-gray-500 capitalize">{c.type || c.industry || "—"}</p>
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              {c.tier && <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-brand-sky/10 text-brand-sky">Tier {c.tier}</span>}
              {c.difficulty && <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400">{c.difficulty}</span>}
            </div>
            <ChevronRight size={14} className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600 group-hover:text-brand-sky transition-colors" />
          </motion.div>
        ))}
      </div>

      {/* Detail Modal */}
      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60" onClick={() => setSelected(null)}>
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
            onClick={e => e.stopPropagation()}
            className="glass rounded-2xl p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-xl font-display font-black text-brand-sky">
                {selected.name?.[0]}
              </div>
              <div>
                <h2 className="text-xl font-display font-black text-text-primary">{selected.name}</h2>
                <p className="text-xs font-mono text-gray-500">{selected.type || selected.industry || ""}</p>
              </div>
            </div>
            {selected.description && <p className="text-sm text-gray-400 mb-4">{selected.description}</p>}
            {selected.interview_process && (
              <div className="mb-4">
                <p className="text-[10px] font-mono text-gray-500 uppercase tracking-wider mb-2">Interview Process</p>
                <p className="text-sm text-gray-400">{selected.interview_process}</p>
              </div>
            )}
            {selected.tips && (
              <div className="mb-4">
                <p className="text-[10px] font-mono text-gray-500 uppercase tracking-wider mb-2">Tips</p>
                <p className="text-sm text-gray-400">{selected.tips}</p>
              </div>
            )}
            <button onClick={() => setSelected(null)}
              className="w-full py-2.5 rounded-xl bg-white/5 border border-white/10 text-sm font-mono text-gray-400 hover:text-text-primary transition-colors">
              Close
            </button>
          </motion.div>
        </div>
      )}
    </div>
  );
}
