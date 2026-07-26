import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../services/api';
import { Card } from '../components/ui/Card';

export default function CompanyPrep() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [guide, setGuide] = useState(null);
  const [behavioral, setBehavioral] = useState(null);
  const [role, setRole] = useState('Software Engineer');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('guide');
  const [practiceResult, setPracticeResult] = useState(null);
  const [practicing, setPracticing] = useState(false);

  useEffect(() => {
    api.getCompanies().then(d => setCompanies(d.companies || [])).catch(() => {});
  }, []);

  const loadGuide = async (companyId) => {
    setLoading(true); setError('');
    try {
      const data = await api.getCompanyGuide(companyId);
      setGuide(data); setSelectedCompany(companyId);
    } catch (err) { setError(err.message); }
    setLoading(false);
  };

  const loadBehavioral = async () => {
    if (!selectedCompany) return;
    setLoading(true); setError('');
    try {
      const data = await api.getBehavioralQuestion(selectedCompany, role);
      setBehavioral(data.question);
    } catch (err) { setError(err.message); }
    setLoading(false);
  };

  const handlePracticeForRole = async () => {
    if (!selectedCompany) return;
    setPracticing(true); setPracticeResult(null);
    try { const data = await api.createPracticeSession(selectedCompany, role || 'SDE'); setPracticeResult(data); } catch {}
    setPracticing(false);
  };

  const COMPANY_ICONS = { google: '🔍', amazon: '📦', microsoft: '🪟', apple: '🍎', meta: '👥', netflix: '🎬', tesla: '⚡', adobe: '🎨', oracle: '☁️', salesforce: '☁️' };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-5xl mx-auto">
        <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8">
          <span className="section-subheader mb-2 block">Insider Intel</span>
          <h1 className="section-header text-3xl mb-2">
            Company <span className="text-cyber-blue">Prep</span>
          </h1>
          <p className="text-gray-500 text-sm font-mono">Prepare for interviews at top companies with insider tips</p>
        </motion.div>

        {error && <div className="bg-red-950/30 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg mb-6 text-center text-sm font-mono">{error}</div>}

        {!selectedCompany ? (
          <>
            <div className="flex flex-wrap gap-2 mb-6 justify-center">
              {companies.map((c) => (
                <button key={c.id} onClick={() => loadGuide(c.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all border ${loading ? 'opacity-50' : 'border-gray-700/30 text-gray-400 hover:text-white hover:border-cyber-blue/40 hover:bg-cyber-blue/5'}`}>
                  {COMPANY_ICONS[c.id] || '🏢'} {c.name}
                </button>
              ))}
            </div>

            {loading ? (
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {Array.from({ length: 6 }).map((_, i) => (
                  <div key={i} className="rounded-xl border border-gray-700/20 p-5 animate-pulse bg-gray-900/20">
                    <div className="h-5 bg-gray-700/40 rounded w-1/2 mb-3" />
                    <div className="h-3 bg-gray-700/30 rounded w-2/3 mb-2" />
                    <div className="h-3 bg-gray-700/20 rounded w-1/3" />
                  </div>
                ))}
              </div>
            ) : (
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {companies.map((company, i) => (
                  <motion.div key={company.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}>
                    <Card rarity={i < 3 ? 'rare' : 'common'} hoverEffect onClick={() => loadGuide(company.id)}>
                      <div className="text-center">
                        <div className="text-3xl mb-2">{COMPANY_ICONS[company.id] || '🏢'}</div>
                        <h3 className="font-display font-bold text-sm text-white mb-2">{company.name}</h3>
                        <div className="flex flex-wrap gap-1 justify-center mb-2">
                          {(company.focus_areas || []).slice(0, 3).map((area, j) => (
                            <span key={j} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-gray-800 text-gray-400">{area}</span>
                          ))}
                        </div>
                        <p className="text-[10px] font-mono text-gray-500">{company.interview_rounds?.length || 0} rounds</p>
                      </div>
                    </Card>
                  </motion.div>
                ))}
              </div>
            )}
          </>
        ) : (
          <div>
            <button onClick={() => { setSelectedCompany(null); setGuide(null); setBehavioral(null); setPracticeResult(null); }}
              className="mb-5 text-sm font-mono text-cyber-blue hover:text-cyber-blue/80 transition-colors">
              ← Back to Companies
            </button>

            <div className="flex items-center gap-4 mb-5 flex-wrap">
              <h2 className="text-xl font-display font-bold text-white">{guide?.company}</h2>
              <div className="flex items-center gap-2">
                <label className="text-[10px] font-mono text-gray-500 uppercase">Role:</label>
                <input className="input py-1.5 px-3 text-sm w-48" value={role} onChange={(e) => setRole(e.target.value)} placeholder="Software Engineer" />
              </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-1.5 mb-5">
              {['guide', 'behavioral'].map((tab) => (
                <button key={tab} onClick={() => { setActiveTab(tab); if (tab === 'behavioral') loadBehavioral(); }}
                  className={`px-4 py-2 rounded-lg text-xs font-mono font-medium uppercase tracking-wider transition-all border ${
                    activeTab === tab ? 'bg-cyber-blue/15 text-cyber-blue border-cyber-blue/40' : 'border-transparent text-gray-500 hover:text-gray-300 hover:bg-white/5'
                  }`}>
                  {tab === 'guide' ? '📋 Interview Guide' : '💬 Behavioral'}
                </button>
              ))}
            </div>

            {/* Practice button */}
            <div className="mb-5">
              <button onClick={handlePracticeForRole} disabled={practicing} className="btn-primary text-sm inline-flex items-center gap-2">
                {practicing ? 'Starting...' : '🔥 Practice for This Role'}
              </button>
              {practiceResult && (
                <div className="mt-3 p-3 rounded-lg bg-green-950/20 border border-green-500/20 text-xs font-mono text-green-400">
                  <p>Session ready: {practiceResult.company} · {practiceResult.role}</p>
                  <p>Coding: {practiceResult.coding?.length || 0} · Behavioral: {practiceResult.behavioral?.length || 0} · System Design: {practiceResult.system_design?.length || 0}</p>
                  <p>Probability: {practiceResult.probability_before}% → {practiceResult.probability_after_target}%</p>
                </div>
              )}
            </div>

            {loading ? (
              <div className="text-center py-12"><div className="spinner-cyber mx-auto" /></div>
            ) : activeTab === 'guide' && guide ? (
              <div className="space-y-4">
                <Card rarity="rare" hoverEffect={false}>
                  <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Interview Process</h3>
                  <div className="flex flex-wrap gap-3">
                    {(guide.interview_process || []).map((round, i) => (
                      <div key={i} className="flex items-center gap-2">
                        <span className="w-7 h-7 rounded-lg bg-cyber-blue/15 text-cyber-blue flex items-center justify-center text-xs font-bold font-mono">{i + 1}</span>
                        <span className="text-sm text-gray-300">{round}</span>
                      </div>
                    ))}
                  </div>
                </Card>
                <Card rarity="rare" hoverEffect={false}>
                  <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Focus Areas</h3>
                  <div className="flex flex-wrap gap-1.5">
                    {(guide.focus_areas || []).map((area, i) => (
                      <span key={i} className="px-2.5 py-1 rounded-lg text-[10px] font-mono bg-blue-500/10 text-blue-400 border border-blue-500/20">{area}</span>
                    ))}
                  </div>
                </Card>
                {guide.leadership_principles?.length > 0 && (
                  <Card rarity="epic" hoverEffect={false}>
                    <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Leadership Principles</h3>
                    <div className="flex flex-wrap gap-1.5">
                      {guide.leadership_principles.map((lp, i) => (
                        <span key={i} className="px-2.5 py-1 rounded-lg text-[10px] font-mono bg-yellow-500/10 text-yellow-400 border border-yellow-500/20">{lp}</span>
                      ))}
                    </div>
                  </Card>
                )}
                <Card rarity="uncommon" hoverEffect={false}>
                  <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Tips</h3>
                  <ul className="space-y-1.5">
                    {(guide.tips || []).map((tip, i) => (
                      <li key={i} className="text-xs text-gray-300 font-mono">→ {tip}</li>
                    ))}
                  </ul>
                </Card>
              </div>
            ) : activeTab === 'behavioral' && behavioral ? (
              <Card rarity="epic" hoverEffect={false}>
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-purple-500/15 text-purple-400 mb-3 inline-block">{behavioral.category}</span>
                <h3 className="text-lg font-display font-bold text-white mb-4">{behavioral.question}</h3>

                <div className="bg-gray-800/50 rounded-lg p-3 mb-4 border border-gray-700/30">
                  <p className="text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-1">What the interviewer looks for</p>
                  <p className="text-xs text-gray-300">{behavioral.what_interviewer_looks_for}</p>
                </div>

                {behavioral.star_framework && (
                  <div className="space-y-2 mb-4">
                    <p className="text-[10px] font-mono font-bold text-cyber-blue uppercase tracking-wider">STAR Framework</p>
                    {Object.entries(behavioral.star_framework).map(([key, value]) => (
                      <div key={key} className="bg-gray-800/30 border border-gray-700/20 rounded-lg p-3">
                        <p className="text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-1">{key}</p>
                        <p className="text-xs text-gray-300">{value}</p>
                      </div>
                    ))}
                  </div>
                )}

                {behavioral.red_flags?.length > 0 && (
                  <div className="bg-red-950/20 border border-red-500/20 rounded-lg p-3 mb-4">
                    <p className="text-[10px] font-mono font-bold text-red-400 uppercase tracking-wider mb-2">Red Flags to Avoid</p>
                    <ul className="space-y-0.5">{behavioral.red_flags.map((f, i) => <li key={i} className="text-xs text-red-300/70 font-mono">✗ {f}</li>)}</ul>
                  </div>
                )}

                <button onClick={loadBehavioral} className="btn-primary text-sm">Get Another Question</button>
              </Card>
            ) : null}
          </div>
        )}
      </div>
    </div>
  );
}
