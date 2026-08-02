import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import api from '../services/api';
import { Card } from '../components/ui/Card';

export default function SalaryBenchmark() {
  const [form, setForm] = useState({ job_title: '', location: '', company: '', years_experience: 0, level: '' });
  const [benchmark, setBenchmark] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!form.job_title || !form.location) return;
    setLoading(true); setError('');
    try {
      const data = await api.getSalaryBenchmark(form.job_title, form.location, form.company, form.years_experience, form.level);
      setBenchmark(data);
    } catch (err) { setError(err.message); }
    setLoading(false);
  };

  const fmt = (n) => n ? `$${n.toLocaleString()}` : '$0';

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8">
          <span className="section-subheader mb-2 block">Market Intelligence</span>
          <h1 className="section-header text-3xl mb-2">
            Salary <span className="text-cyber-green">Benchmark</span>
          </h1>
          <p className="text-gray-500 text-sm font-mono">Know your market worth before negotiating</p>
        </motion.div>

        {error && <div className="bg-red-950/30 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg mb-6 text-center text-sm font-mono">{error}</div>}

        {!benchmark ? (
          <Card rarity="rare" hoverEffect={false}>
            <h2 className="font-display font-bold text-sm uppercase tracking-widest text-gray-400 mb-5">Get Your Salary Benchmark</h2>
            <div className="space-y-4">
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-1">Job Title *</label>
                  <input className="input text-sm" placeholder="Software Engineer" value={form.job_title} onChange={(e) => setForm({ ...form, job_title: e.target.value })} />
                </div>
                <div>
                  <label className="block text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-1">Location *</label>
                  <input className="input text-sm" placeholder="San Francisco, CA" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} />
                </div>
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-1">Company (Optional)</label>
                  <input className="input text-sm" placeholder="Google, Amazon" value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} />
                </div>
                <div>
                  <label className="block text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-1">Years of Experience</label>
                  <input type="number" className="input text-sm" min="0" max="30" value={form.years_experience} onChange={(e) => setForm({ ...form, years_experience: parseInt(e.target.value) || 0 })} />
                </div>
              </div>
              <div>
                <label className="block text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-2">Level</label>
                <div className="flex flex-wrap gap-1.5">
                  {['Junior', 'Mid-Level', 'Senior', 'Staff', 'Principal'].map((lvl) => (
                    <button key={lvl} onClick={() => setForm({ ...form, level: lvl })}
                      className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all border ${form.level === lvl ? 'bg-cyber-green/15 text-cyber-green border-cyber-green/40' : 'border-gray-700/30 text-gray-400 hover:text-gray-300 hover:border-gray-600/40'}`}>
                      {lvl}
                    </button>
                  ))}
                </div>
              </div>
              <button onClick={handleSubmit} disabled={!form.job_title || !form.location || loading} className="btn-primary w-full text-sm">
                {loading ? <span className="spinner-cyber w-5 h-5 inline-block mr-2" /> : null}Get Salary Benchmark
              </button>
            </div>
          </Card>
        ) : (
          <div className="space-y-4">
            <Card rarity="legendary" hoverEffect={false} className="text-center">
              <h2 className="text-xl font-display font-bold text-white mb-1">{benchmark.job_title}</h2>
              <p className="text-xs font-mono text-gray-500">{benchmark.location}</p>
            </Card>

            {/* Total Comp Range */}
            <Card rarity="epic" hoverEffect={false}>
              <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-4">Total Compensation Range</h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
                {[
                  { label: 'Minimum', value: benchmark.market_rate?.total_compensation?.min, color: 'text-gray-400' },
                  { label: 'Median', value: benchmark.market_rate?.total_compensation?.median, color: 'text-cyber-green' },
                  { label: 'Maximum', value: benchmark.market_rate?.total_compensation?.max, color: 'text-gray-400' },
                ].map((item) => (
                  <div key={item.label} className="text-center">
                    <p className="text-[10px] font-mono text-gray-500 uppercase">{item.label}</p>
                    <p className={`text-lg font-display font-bold ${item.color}`}>{fmt(item.value)}</p>
                  </div>
                ))}
              </div>

              {benchmark.percentiles && (
                <div className="bg-gray-800/30 rounded-lg p-3 border border-gray-700/20">
                  <p className="text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-3">Percentile Breakdown</p>
                  <div className="space-y-2">
                    {Object.entries(benchmark.percentiles).map(([key, value]: [string, any]) => (
                      <div key={key} className="flex items-center gap-3">
                        <span className="text-[10px] font-mono text-gray-500 w-8 uppercase">{key}</span>
                        <div className="flex-1 bg-gray-700/30 rounded-full h-1.5">
                          <div className="bg-cyber-green h-1.5 rounded-full" style={{ width: `${(value / (benchmark.percentiles.p90 || 300000)) * 100}%` }} />
                        </div>
                        <span className="text-[10px] font-mono text-gray-300 w-20 text-right">{fmt(value)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </Card>

            {/* Base + Stock */}
            <div className="grid sm:grid-cols-2 gap-4">
              {[
                { title: 'Base Salary', data: benchmark.market_rate?.base_salary },
                { title: 'Stock (Annual)', data: benchmark.market_rate?.stock_annual },
              ].map((item) => (
                <Card key={item.title} rarity="rare" hoverEffect={false}>
                  <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">{item.title}</h3>
                  <div className="space-y-1.5">
                    {item.data && Object.entries(item.data).map(([key, value]) => (
                      <div key={key} className="flex justify-between text-xs">
                        <span className="text-gray-500 font-mono uppercase">{key}</span>
                        <span className="font-mono text-gray-300">{fmt(value)}</span>
                      </div>
                    ))}
                  </div>
                </Card>
              ))}
            </div>

            {benchmark.factors_affecting_pay?.length > 0 && (
              <Card rarity="uncommon" hoverEffect={false}>
                <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Factors Affecting Pay</h3>
                <ul className="space-y-1">{benchmark.factors_affecting_pay.map((f, i) => <li key={i} className="text-xs text-gray-300 font-mono">→ {f}</li>)}</ul>
              </Card>
            )}

            {benchmark.companies_paying_above_market?.length > 0 && (
              <Card rarity="legendary" hoverEffect={false}>
                <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Companies Paying Above Market</h3>
                <div className="flex flex-wrap gap-1.5">
                  {benchmark.companies_paying_above_market.map((c, i) => (
                    <span key={i} className="px-2.5 py-1 rounded-lg text-[10px] font-mono bg-green-500/10 text-green-400 border border-green-500/20">{c}</span>
                  ))}
                </div>
              </Card>
            )}

            <div className="flex gap-3">
              <button onClick={() => setBenchmark(null)} className="btn-primary flex-1 text-sm">Benchmark Another Role</button>
              <Link to="/salary-negotiation" className="btn-secondary flex-1 text-center text-sm">Negotiation Tips</Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
