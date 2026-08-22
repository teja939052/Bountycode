import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ChevronRight } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { useCompanyPrep } from '../hooks/useCompanyPrep';

export default function CompanyPrep() {
  const { companies, isLoading: companiesLoading, isError: companiesError, useGuide, useBehavioral, useQuestions, useQuestionList, practiceMutation } = useCompanyPrep();
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [role, setRole] = useState('Software Engineer');
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('guide');
  const [practiceResult, setPracticeResult] = useState(null);
  const [bankCategory, setBankCategory] = useState(null);

  const { data: guide, isLoading: guideLoading } = useGuide(selectedCompany);
  const { data: behavioralData, refetch: refetchBehavioral, isLoading: behavioralLoading } = useBehavioral(selectedCompany, role);
  const { data: bank, isLoading: bankLoading } = useQuestions(selectedCompany);
  const { data: bankList, isLoading: bankListLoading } = useQuestionList(bank?.company_id || selectedCompany, bankCategory);

  const behavioral = behavioralData?.question || null;

  const loadGuide = (companyId) => {
    setSelectedCompany(companyId);
    setActiveTab('guide');
  };

  const loadBehavioral = () => {
    if (!selectedCompany) return;
    setError('');
    refetchBehavioral();
  };

  const handlePracticeForRole = () => {
    if (!selectedCompany) return;
    setPracticeResult(null);
    practiceMutation.mutate(
      { company: selectedCompany, role: role || 'SDE' },
      {
        onSuccess: (data) => setPracticeResult(data),
        onError: () => {},
      },
    );
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

        {(error || companiesError) && <div className="bg-red-950/30 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg mb-6 text-center text-sm font-mono">
                {error || 'Failed to load companies'}
                {companiesError && (
                  <button onClick={() => window.location.reload()} className="ml-2 text-sm text-brand-primary hover:text-brand-primary/90 transition-colors">
                    Retry
                  </button>
                )}
              </div>}

        {!selectedCompany ? (
          <>
            <div className="flex flex-wrap gap-2 mb-6 justify-center">
              {companies.map((c) => (
                <button key={c.id} onClick={() => loadGuide(c.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all border ${companiesLoading ? 'opacity-50' : 'border-gray-700/30 text-gray-400 hover:text-text-primary hover:border-cyber-blue/40 hover:bg-cyber-blue/5'}`}>
                  {COMPANY_ICONS[c.id] || '🏢'} {c.name}
                </button>
              ))}
            </div>

            {companiesLoading ? (
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
            <button onClick={() => { setSelectedCompany(null); setPracticeResult(null); setBankCategory(null); }}
              className="mb-5 text-sm font-mono text-cyber-blue hover:text-cyber-blue/80 transition-colors">
              ← Back to Companies
            </button>

            <div className="flex items-center gap-4 mb-5 flex-wrap">
              <h2 className="text-xl font-display font-bold text-text-primary">{guide?.company}</h2>
              <div className="flex items-center gap-2">
                <label className="text-[10px] font-mono text-gray-500 uppercase">Role:</label>
                <input className="input py-1.5 px-3 text-sm w-48" value={role} onChange={(e) => setRole(e.target.value)} placeholder="Software Engineer" />
              </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-1.5 mb-5">
              {['guide', 'behavioral', 'questions'].map((tab) => (
                <button key={tab} onClick={() => { setActiveTab(tab); if (tab === 'behavioral') loadBehavioral(); }}
                  className={`px-4 py-2 rounded-lg text-xs font-mono font-medium uppercase tracking-wider transition-all border ${
                    activeTab === tab ? 'bg-cyber-blue/15 text-cyber-blue border-cyber-blue/40' : 'border-transparent text-gray-500 hover:text-gray-300 hover:bg-gray-50'
                  }`}>
                  {tab === 'guide' ? '📋 Interview Guide' : tab === 'behavioral' ? '💬 Behavioral' : '🗂️ Question Bank'}
                </button>
              ))}
            </div>

            {/* Practice button */}
            <div className="mb-5">
              <button onClick={handlePracticeForRole} disabled={practiceMutation.isPending} className="btn-primary text-sm inline-flex items-center gap-2">
                {practiceMutation.isPending ? 'Starting...' : '🔥 Practice for This Role'}
              </button>
              {practiceResult && (
                <div className="mt-3 p-3 rounded-lg bg-green-950/20 border border-green-500/20 text-xs font-mono text-green-400">
                  <p>Session ready: {practiceResult.company} · {practiceResult.role}</p>
                  <p>Coding: {practiceResult.coding?.length || 0} · Behavioral: {practiceResult.behavioral?.length || 0} · System Design: {practiceResult.system_design?.length || 0}</p>
                  <p>Probability: {practiceResult.probability_before}% → {practiceResult.probability_after_target}%</p>
                </div>
              )}
            </div>

            {guideLoading ? (
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
                {guide.question_mix?.length > 0 && (
                  <Card rarity="rare" hoverEffect={false}>
                    <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Question Mix</h3>
                    <div className="grid sm:grid-cols-2 gap-2">
                      {guide.question_mix.map((item, i) => (
                        <div key={i} className="rounded-lg border border-gray-700/20 bg-gray-900/30 p-3">
                          <div className="flex items-center justify-between gap-3 mb-1">
                            <span className="text-xs font-mono font-bold text-text-primary">{item.track.replace("_", " ")}</span>
                            <span className="text-[10px] font-mono text-cyber-blue">{item.weight}%</span>
                          </div>
                          <p className="text-[11px] font-mono text-gray-400">{item.questions} target questions</p>
                          <p className="text-[11px] font-mono text-gray-500 mt-1">{item.reason}</p>
                        </div>
                      ))}
                    </div>
                  </Card>
                )}
                {guide.prep_modules?.length > 0 && (
                  <Card rarity="epic" hoverEffect={false}>
                    <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Prep Modules</h3>
                    <div className="space-y-3">
                      {guide.prep_modules.map((module, i) => (
                        <div key={i} className="rounded-lg border border-gray-700/20 bg-gray-900/30 p-3">
                          <p className="text-xs font-mono font-bold text-text-primary mb-1">{module.title}</p>
                          <p className="text-[11px] font-mono text-gray-400 mb-2">{module.description}</p>
                          <div className="flex flex-wrap gap-1.5">
                            {(module.focus || []).map((item, j) => (
                              <span key={j} className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-cyber-blue/10 text-cyber-blue border border-cyber-blue/20">{item}</span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </Card>
                )}
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
                    {Object.entries(behavioral.star_framework as Record<string, string>).map(([key, value]) => (
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
            ) : activeTab === 'questions' ? (
              bankLoading || !bank ? (
                <div className="text-center py-12"><div className="spinner-cyber mx-auto" /></div>
              ) : (
                <div className="space-y-4">
                  <Card rarity="rare" hoverEffect={false}>
                    <div className="flex items-center justify-between gap-3 mb-3">
                      <div>
                        <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-1">Question Bank</h3>
                        <p className="text-[11px] font-mono text-gray-500">{bank.source}</p>
                      </div>
                      <div className="text-right shrink-0">
                        <p className="text-2xl font-display font-black text-cyber-blue">{bank.total_bank_questions || 0}</p>
                        <p className="text-[10px] font-mono text-gray-500">authored questions</p>
                      </div>
                    </div>

                    {(bank.focus_areas?.length > 0 || bank.leadership_principles?.length > 0) && (
                      <div className="flex flex-wrap gap-1.5 mb-4">
                        {(bank.focus_areas || []).map((area, i) => (
                          <span key={i} className="px-2.5 py-1 rounded-lg text-[10px] font-mono bg-blue-500/10 text-blue-400 border border-blue-500/20">{area}</span>
                        ))}
                        {bank.leadership_principles?.length > 0 && (
                          <span className="px-2.5 py-1 rounded-lg text-[10px] font-mono bg-yellow-500/10 text-yellow-400 border border-yellow-500/20">
                            {bank.leadership_principles.length} Leadership Principles
                          </span>
                        )}
                      </div>
                    )}

                    {bank.categories?.length > 0 ? (
                      <div className="space-y-4">
                        {bank.categories.map((cat) => {
                          const max = bank.categories[0].count || 1;
                          return (
                            <div key={cat.category}>
                              <button onClick={() => setBankCategory(cat.category)} className="w-full text-left group">
                                <div className="flex items-center justify-between text-xs mb-1">
                                  <span className="font-mono font-bold text-text-primary group-hover:text-cyber-blue transition-colors">{cat.label}</span>
                                  <span className="font-mono text-gray-400">{cat.count} questions</span>
                                </div>
                                <div className="flex items-center gap-2">
                                  <div className="flex-1 bg-gray-800/60 rounded-full h-2 overflow-hidden">
                                    <motion.div initial={{ width: 0 }} whileInView={{ width: `${(cat.count / max) * 100}%` }} viewport={{ once: true }}
                                      className="h-2 rounded-full bg-cyber-blue/70" />
                                  </div>
                                  <ChevronRight size={14} className="text-gray-600 group-hover:text-cyber-blue transition-colors" />
                                </div>
                                <div className="flex gap-1.5 mt-1.5">
                                  {Object.entries(cat.difficulty || {}).map(([d, n]) => (
                                    <span key={d} className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-gray-800/60 text-gray-400 capitalize">{d} {n}</span>
                                  ))}
                                </div>
                              </button>
                            </div>
                          );
                        })}
                      </div>
                    ) : (
                      <p className="text-xs font-mono text-gray-500">No authored bank for this company yet — practice with the coding problems below.</p>
                    )}
                  </Card>

                  {bank.coding_store?.hits > 0 && (
                    <Card rarity="rare" hoverEffect={false}>
                      <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">
                        Coding Practice Problems · {bank.coding_store.hits} tagged
                      </h3>
                      <div className="flex flex-wrap gap-1.5 mb-4">
                        {(bank.coding_store.top_topics || []).map((t, i) => (
                          <span key={i} className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-cyber-blue/10 text-cyber-blue border border-cyber-blue/20">{t.topic} ×{t.count}</span>
                        ))}
                      </div>
                      <div className="space-y-2">
                        {bank.sample_questions.filter((s) => s.type === 'coding').map((s) => (
                          <a key={s.id} href={`/solve/${s.id}`} className="block rounded-lg border border-gray-700/20 bg-gray-900/30 p-3 hover:border-cyber-blue/40 transition-colors">
                            <p className="text-xs font-mono text-text-primary">{s.question}</p>
                            <div className="flex gap-1.5 mt-2">
                              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-gray-800 text-cyber-blue">{s.topic}</span>
                              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-gray-800 text-gray-400 capitalize">{s.difficulty}</span>
                              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-gray-800 text-gray-400 ml-auto">Open →</span>
                            </div>
                          </a>
                        ))}
                      </div>
                    </Card>
                  )}

                  {bank.sample_questions?.filter((s) => s.type === 'bank').length > 0 && (
                    <Card rarity="epic" hoverEffect={false}>
                      <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Sample Questions</h3>
                      <div className="space-y-2">
                        {bank.sample_questions.filter((s) => s.type === 'bank').map((s) => (
                          <div key={s.id} className="rounded-lg border border-gray-700/20 bg-gray-900/30 p-3">
                            <div className="flex items-center justify-between gap-2 mb-1">
                              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-purple-500/15 text-purple-400">{s.category_label}</span>
                              <span className="text-[10px] font-mono text-gray-500 capitalize">{s.difficulty}</span>
                            </div>
                            <p className="text-xs font-mono text-gray-300">{s.question}</p>
                          </div>
                        ))}
                      </div>
                    </Card>
                  )}

                  {bankList && (
                    <Card rarity="epic" hoverEffect={false}>
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400">
                          {bankList.company} · {(bankList.questions[0]?.category_label || bankList.category || 'All')} ({bankList.total})
                        </h3>
                        <button onClick={() => { setBankCategory(null); }} className="text-xs font-mono text-gray-500 hover:text-red-400 transition-colors">✕ Close</button>
                      </div>
                      {bankListLoading ? (
                        <div className="text-center py-8"><div className="spinner-cyber mx-auto" /></div>
                      ) : (
                        <div className="space-y-2">
                          {bankList.questions.map((q) => (
                            <div key={q.id} className="rounded-lg border border-gray-700/20 bg-gray-900/30 p-3">
                              <div className="flex items-center justify-between gap-2 mb-1">
                                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-purple-500/15 text-purple-400">{q.category_label}</span>
                                <span className="text-[10px] font-mono text-gray-500 capitalize">{q.difficulty}</span>
                              </div>
                              <p className="text-xs font-mono text-gray-300">{q.question}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </Card>
                  )}
                </div>
              )
            ) : null}
          </div>
        )}
      </div>
    </div>
  );
}
