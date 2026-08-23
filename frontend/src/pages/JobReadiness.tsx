import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Target, FileText, TrendingUp, BookOpen, Building2, ChevronRight,
  CheckCircle2, Clock, ArrowRight, Sparkles, Rocket
} from 'lucide-react';

const api = {
  roles: () => fetch('/api/v1/job-readiness/roles').then(r => r.json()),
  gaps: (role: string) => fetch(`/api/v1/job-readiness/gaps?role=${role}`, { credentials: 'include' }).then(r => r.json()),
  curriculum: (role: string) => fetch(`/api/v1/job-readiness/curriculum?role=${role}`, { credentials: 'include' }).then(r => r.json()),
  companies: () => fetch('/api/v1/job-readiness/companies').then(r => r.json()),
  companyReadiness: (id: string) => fetch(`/api/v1/job-readiness/company/${id}`, { credentials: 'include' }).then(r => r.json()),
  analyzeJD: (text: string) => fetch('/api/v1/job-readiness/analyze-jd', {
    method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ jd_text: text }),
  }).then(r => r.json()),
  setTarget: (data: Record<string, unknown>) => fetch('/api/v1/job-readiness/set-target', {
    method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  }).then(r => r.json()),
  getTarget: () => fetch('/api/v1/job-readiness/target', { credentials: 'include' }).then(r => r.json()),
};

const tabs = [
  { id: 'diagnose', label: 'Diagnose', icon: Target },
  { id: 'gaps', label: 'Gaps', icon: TrendingUp },
  { id: 'curriculum', label: 'Curriculum', icon: BookOpen },
  { id: 'company', label: 'Company', icon: Building2 },
];

interface RoleInfo { id: string; title: string; icon: string; description: string }
interface CompanyInfo { id: string; title: string; icon: string; tier: string; color: string }

export default function JobReadiness() {
  const [activeTab, setActiveTab] = useState('diagnose');
  const [roles, setRoles] = useState<RoleInfo[]>([]);
  const [selectedRole, setSelectedRole] = useState('sde');
  const [gaps, setGaps] = useState<Record<string, unknown> | null>(null);
  const [curriculum, setCurriculum] = useState<Record<string, unknown> | null>(null);
  const [companies, setCompanies] = useState<CompanyInfo[]>([]);
  const [selectedCompany, setSelectedCompany] = useState<string | null>(null);
  const [companyData, setCompanyData] = useState<Record<string, unknown> | null>(null);
  const [jdText, setJdText] = useState('');
  const [jdResult, setJdResult] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [target, setTarget] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    api.roles().then(r => setRoles(r.roles || []));
    api.companies().then(r => setCompanies(r.companies || []));
    api.getTarget().then(r => { if (r.target) setTarget(r.target); });
  }, []);

  useEffect(() => {
    if (activeTab === 'gaps' || activeTab === 'curriculum') {
      setLoading(true);
      const fn = activeTab === 'gaps' ? api.gaps : api.curriculum;
      fn(selectedRole).then(r => {
        if (activeTab === 'gaps') setGaps(r);
        else setCurriculum(r);
        setLoading(false);
      });
    }
  }, [activeTab, selectedRole]);

  const handleAnalyzeJD = async () => {
    if (jdText.length < 20) return;
    setLoading(true);
    const result = await api.analyzeJD(jdText);
    setJdResult(result);
    if (result.role) setSelectedRole(result.role.id);
    setLoading(false);
  };

  const handleSetTarget = async (roleId: string) => {
    await api.setTarget({ role_id: roleId });
    setTarget({ role_id: roleId, role_title: roles.find(r => r.id === roleId)?.title });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e17] via-[#0d1525] to-[#0f172a] text-text-primary">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-emerald-400 text-sm mb-4">
            <Rocket className="w-4 h-4" />
            Job Readiness Engine
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-3">
            Stop guessing.{' '}
            <span className="bg-gradient-to-r from-emerald-400 via-cyan-400 to-blue-400 bg-clip-text text-transparent">Start preparing.</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Paste a job description or pick a role. We tell you exactly what to study, in what order, and how ready you are.
          </p>
        </motion.div>

        {target && activeTab === 'diagnose' && (
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
            className="mb-6 p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <span className="text-emerald-300">
                Target: <strong>{String(target.role_title)}</strong>
              </span>
            </div>
            <button onClick={() => setActiveTab('gaps')}
              className="px-4 py-1.5 bg-emerald-500/20 hover:bg-emerald-500/30 rounded-lg text-emerald-300 text-sm font-medium transition-colors">
              View Gaps
            </button>
          </motion.div>
        )}

        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {tabs.map(tab => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium whitespace-nowrap transition-all ${
                activeTab === tab.id ? 'bg-white border-border/10 text-text-primary shadow-lg shadow-white/5' : 'text-gray-400 hover:text-white hover:bg-white border-border shadow-card'
              }`}>
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {activeTab === 'diagnose' && (
            <motion.div key="diagnose" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              <div className="mb-10">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <FileText className="w-5 h-5 text-cyan-400" /> Paste a Job Description
                </h2>
                <div className="relative">
                  <textarea value={jdText} onChange={e => setJdText(e.target.value)}
                    placeholder="Paste the full job description here... We extract skills, match you to a role, and build your plan."
                    className="w-full h-48 bg-white border-border shadow-card border border-white/10 rounded-xl p-4 text-text-primary placeholder-gray-500 resize-none focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all" />
                  <button onClick={handleAnalyzeJD} disabled={jdText.length < 20 || loading}
                    className="absolute bottom-4 right-4 px-5 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 disabled:opacity-40 disabled:cursor-not-allowed rounded-lg font-medium text-sm transition-all flex items-center gap-2">
                    {loading ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> : <Sparkles className="w-4 h-4" />}
                    Analyze
                  </button>
                </div>
              </div>

              {jdResult && (
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                  className="mb-10 p-6 bg-white border-border shadow-card border border-white/10 rounded-2xl">
                  <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <CheckCircle2 className="w-5 h-5 text-emerald-400" /> JD Analysis Complete
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="p-4 bg-white border-border shadow-card rounded-xl text-center">
                      <div className="text-3xl font-bold text-cyan-400">{(jdResult.jd_analysis as Record<string, unknown>)?.skill_count || 0}</div>
                      <div className="text-sm text-gray-400">Skills Detected</div>
                    </div>
                    <div className="p-4 bg-white border-border shadow-card rounded-xl text-center">
                      <div className="text-3xl font-bold text-emerald-400">{(jdResult.jd_analysis as Record<string, unknown>)?.category_count || 0}</div>
                      <div className="text-sm text-gray-400">Categories</div>
                    </div>
                    <div className="p-4 bg-white border-border shadow-card rounded-xl text-center">
                      <div className="text-3xl font-bold text-purple-400">{String(jdResult.readiness || 0)}%</div>
                      <div className="text-sm text-gray-400">Your Readiness</div>
                    </div>
                  </div>
                  {jdResult.role && (
                    <div className="flex items-center justify-between p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
                      <div>
                        <div className="text-sm text-gray-400">Matched Role</div>
                        <div className="text-lg font-semibold">{String((jdResult.role as Record<string, unknown>).icon)} {String((jdResult.role as Record<string, unknown>).title)}</div>
                      </div>
                      <button onClick={() => { handleSetTarget((jdResult.role as Record<string, unknown>).id as string); setActiveTab('gaps'); }}
                        className="px-4 py-2 bg-emerald-500/20 hover:bg-emerald-500/30 rounded-lg text-emerald-300 text-sm font-medium transition-colors flex items-center gap-2">
                        Set as Target <ArrowRight className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </motion.div>
              )}

              <div>
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <Target className="w-5 h-5 text-purple-400" /> Or Pick a Target Role
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {roles.map(role => (
                    <motion.button key={role.id} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
                      onClick={() => { setSelectedRole(role.id); handleSetTarget(role.id); setActiveTab('gaps'); }}
                      className={`p-5 rounded-xl border text-left transition-all ${
                        selectedRole === role.id ? 'bg-purple-500/10 border-purple-500/30' : 'bg-white border-border shadow-card border-white/10 hover:border-white/20'
                      }`}>
                      <div className="text-2xl mb-2">{role.icon}</div>
                      <div className="font-semibold">{role.title}</div>
                      <div className="text-sm text-gray-400 mt-1">{role.description}</div>
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'gaps' && (
            <motion.div key="gaps" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              <RoleSelector roles={roles} selected={selectedRole} onSelect={setSelectedRole} />
              {loading ? <LoadingState /> : gaps ? <GapView data={gaps} onStartMission={(t: string) => { window.location.href = `/mission/${t}`; }} /> : null}
            </motion.div>
          )}

          {activeTab === 'curriculum' && (
            <motion.div key="curriculum" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              <RoleSelector roles={roles} selected={selectedRole} onSelect={setSelectedRole} />
              {loading ? <LoadingState /> : curriculum ? <CurriculumView data={curriculum} /> : null}
            </motion.div>
          )}

          {activeTab === 'company' && (
            <motion.div key="company" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              {!selectedCompany ? (
                <CompanyGrid companies={companies} onSelect={(id: string) => {
                  setSelectedCompany(id); setLoading(true);
                  api.companyReadiness(id).then(r => { setCompanyData(r); setLoading(false); });
                }} />
              ) : (
                <CompanyDetailView data={companyData} loading={loading}
                  onBack={() => { setSelectedCompany(null); setCompanyData(null); }} />
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function RoleSelector({ roles, selected, onSelect }: { roles: RoleInfo[]; selected: string; onSelect: (id: string) => void }) {
  return (
    <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
      {roles.map(r => (
        <button key={r.id} onClick={() => onSelect(r.id)}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-all ${
            selected === r.id ? 'bg-white border-border/10 text-text-primary border border-white/20' : 'text-gray-400 hover:text-white hover:bg-white border-border shadow-card border border-transparent'
          }`}>
          <span>{r.icon}</span> {r.title}
        </button>
      ))}
    </div>
  );
}

function GapView({ data, onStartMission }: { data: Record<string, unknown>; onStartMission: (topic: string) => void }) {
  const readiness = Number(data.overall_readiness) || 0;
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (readiness / 100) * circumference;
  const color = readiness >= 70 ? '#10b981' : readiness >= 40 ? '#f59e0b' : '#ef4444';
  const role = data.role as Record<string, unknown> | undefined;
  const gaps = (data.gaps || []) as Array<Record<string, unknown>>;
  const strongAreas = (data.strong_areas || []) as unknown[];
  const closeGaps = (data.close_gaps || []) as unknown[];
  const criticalGaps = (data.critical_gaps || []) as unknown[];

  return (
    <div>
      <div className="flex items-center gap-8 mb-8 p-6 bg-white border-border shadow-card border border-white/10 rounded-2xl">
        <div className="relative w-32 h-32 flex-shrink-0">
          <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
            <motion.circle cx="60" cy="60" r="54" fill="none" stroke={color} strokeWidth="8"
              strokeLinecap="round" strokeDasharray={circumference}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: offset }}
              transition={{ duration: 1.5, ease: 'easeOut' }} />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-3xl font-bold" style={{ color }}>{Math.round(readiness)}</span>
            <span className="text-xs text-gray-400">%</span>
          </div>
        </div>
        <div>
          <h2 className="text-2xl font-bold mb-1">{role?.title || 'SDE'} Readiness</h2>
          <p className="text-gray-400">
            {strongAreas.length} strong / {closeGaps.length} close / {criticalGaps.length} critical
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {gaps.map((gap) => {
          const status = String(gap.status);
          const current = Number(gap.current) || 0;
          const target = Number(gap.target) || 1;
          const weight = Number(gap.weight) || 0;
          const barColor = status === 'strong' ? '#10b981' : status === 'close' ? '#f59e0b' : '#ef4444';
          const dotColor = status === 'strong' ? 'bg-emerald-400' : status === 'close' ? 'bg-amber-400' : 'bg-red-400';
          const topics = (gap.critical_topics || []) as string[];

          return (
            <motion.div key={String(gap.category)} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}
              className="p-4 bg-white border-border shadow-card border border-white/10 rounded-xl">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${dotColor}`} />
                  <span className="font-medium">{String(gap.name)}</span>
                  <span className="text-xs text-gray-500">x{(weight * 100).toFixed(0)}% weight</span>
                </div>
                <div className="text-sm">
                  <span className="text-gray-400">{current}</span>
                  <span className="text-gray-600"> / </span>
                  <span>{target}</span>
                </div>
              </div>
              <div className="h-2 bg-white border-border shadow-card rounded-full overflow-hidden">
                <motion.div className="h-full rounded-full" style={{ backgroundColor: barColor }}
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(100, (current / target) * 100)}%` }}
                  transition={{ duration: 1, delay: 0.2 }} />
              </div>
              {topics.length > 0 && status !== 'strong' && (
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {topics.map((topic) => (
                    <button key={topic} onClick={() => onStartMission(topic)}
                      className="px-2.5 py-1 bg-white border-border shadow-card hover:bg-white border-border/10 rounded-md text-xs text-gray-300 hover:text-white transition-colors">
                      {topic.replace(/_/g, ' ')}
                    </button>
                  ))}
                </div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

function CurriculumView({ data }: { data: Record<string, unknown> }) {
  const stats = (data.stats || {}) as Record<string, unknown>;
  const curriculum = (data.curriculum || []) as Array<Record<string, unknown>>;
  const completed = curriculum.filter(c => c.completed);
  const remaining = curriculum.filter(c => !c.completed);

  return (
    <div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Readiness', value: `${Math.round(Number(data.readiness) || 0)}%`, color: 'text-emerald-400' },
          { label: 'Topics', value: String(stats.total_topics || 0), color: 'text-cyan-400' },
          { label: 'Done', value: String(completed.length), color: 'text-purple-400' },
          { label: 'Est. Weeks', value: `~${String(stats.estimated_weeks || 0)}`, color: 'text-amber-400' },
        ].map(s => (
          <div key={s.label} className="p-4 bg-white border-border shadow-card border border-white/10 rounded-xl text-center">
            <div className={`text-2xl font-bold ${s.color}`}>{s.value}</div>
            <div className="text-xs text-gray-400">{s.label}</div>
          </div>
        ))}
      </div>

      {completed.length > 0 && (
        <div className="mb-8">
          <h3 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Completed ({completed.length})
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {completed.map((item, i) => (
              <div key={i} className="flex items-center gap-3 p-3 bg-emerald-500/5 border border-emerald-500/10 rounded-lg">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <span className="text-sm text-emerald-300">{String(item.topic).replace(/_/g, ' ')}</span>
                <span className="ml-auto text-xs text-gray-500">{String(item.category)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div>
        <h3 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
          <Clock className="w-4 h-4 text-amber-400" /> Up Next ({remaining.length})
        </h3>
        <div className="space-y-2">
          {remaining.map((item, i) => (
            <motion.a key={i} href={String(item.mission_link)}
              initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
              className="flex items-center gap-3 p-4 bg-white border-border shadow-card border border-white/10 rounded-xl hover:bg-white border-border/10 hover:border-white/20 transition-all group">
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold ${
                item.priority === 'high' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'
              }`}>{i + 1}</div>
              <div className="flex-1">
                <div className="font-medium text-sm">{String(item.topic).replace(/_/g, ' ')}</div>
                <div className="text-xs text-gray-500">{String(item.category)} / ~{String(item.estimated_minutes)}min</div>
              </div>
              {item.priority === 'high' && (
                <span className="px-2 py-0.5 bg-red-500/10 border border-red-500/20 rounded text-xs text-red-400">Critical</span>
              )}
              <ChevronRight className="w-4 h-4 text-gray-500 group-hover:text-white transition-colors" />
            </motion.a>
          ))}
        </div>
      </div>
    </div>
  );
}

function CompanyGrid({ companies, onSelect }: { companies: CompanyInfo[]; onSelect: (id: string) => void }) {
  const tierColors: Record<string, string> = { faang: 'from-purple-500/20 to-blue-500/20', mid: 'from-cyan-500/20 to-teal-500/20', mass: 'from-amber-500/20 to-orange-500/20' };
  const tierBorders: Record<string, string> = { faang: 'border-purple-500/20', mid: 'border-cyan-500/20', mass: 'border-amber-500/20' };

  return (
    <div>
      <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
        <Building2 className="w-5 h-5 text-cyan-400" /> Company Readiness
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {companies.map(c => (
          <motion.button key={c.id} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            onClick={() => onSelect(c.id)}
            className={`p-5 rounded-xl border text-left transition-all bg-gradient-to-br ${
              tierColors[c.tier] || tierColors.mass
            } ${tierBorders[c.tier] || 'border-white/10'} hover:scale-[1.02]`}>
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl">{c.icon}</span>
              <div>
                <div className="font-semibold text-lg">{c.title}</div>
                <div className={`text-xs px-2 py-0.5 rounded-full inline-block ${
                  c.tier === 'faang' ? 'bg-purple-500/20 text-purple-300' : c.tier === 'mid' ? 'bg-cyan-500/20 text-cyan-300' : 'bg-amber-500/20 text-amber-300'
                }`}>{c.tier.toUpperCase()}</div>
              </div>
            </div>
            <div className="text-sm text-gray-400">Min readiness: {c.min_readiness}%</div>
          </motion.button>
        ))}
      </div>
    </div>
  );
}

function CompanyDetailView({ data, loading, onBack }: { data: Record<string, unknown> | null; loading: boolean; onBack: () => void }) {
  if (loading) return <LoadingState />;
  if (!data) return null;

  const company = (data.company || {}) as Record<string, unknown>;
  const skillBreakdown = (data.skill_breakdown || []) as Array<Record<string, unknown>>;
  const recommendations = (data.recommendations || []) as string[];
  const prediction = (data.prediction || {}) as Record<string, unknown>;

  return (
    <div>
      <button onClick={onBack} className="mb-6 px-4 py-2 text-gray-400 hover:text-white text-sm transition-colors flex items-center gap-2">
        &larr; Back to companies
      </button>

      <div className="flex items-center gap-4 mb-8">
        <span className="text-4xl">{String(company.icon)}</span>
        <div>
          <h2 className="text-3xl font-bold">{String(company.title)}</h2>
          <div className={`text-sm px-3 py-1 rounded-full inline-block mt-1 ${
            company.tier === 'faang' ? 'bg-purple-500/20 text-purple-300' : 'bg-amber-500/20 text-amber-300'
          }`}>{String(company.tier).toUpperCase()}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="p-5 bg-white border-border shadow-card border border-white/10 rounded-xl text-center">
          <div className="text-3xl font-bold text-emerald-400">{String(data.overall_readiness)}%</div>
          <div className="text-sm text-gray-400">Overall Readiness</div>
        </div>
        <div className="p-5 bg-white border-border shadow-card border border-white/10 rounded-xl text-center">
          <div className="text-3xl font-bold text-cyan-400">{String(data.company_readiness)}%</div>
          <div className="text-sm text-gray-400">Company Match</div>
        </div>
        <div className="p-5 bg-white border-border shadow-card border border-white/10 rounded-xl text-center">
          <div className="text-xl font-bold text-purple-400">{String(prediction.weeks || '~?')} weeks</div>
          <div className="text-sm text-gray-400">Est. to Ready</div>
        </div>
      </div>

      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4">Skill-by-Skill Breakdown</h3>
        <div className="space-y-3">
          {skillBreakdown.map(skill => {
            const current = Number(skill.current) || 0;
            const required = Number(skill.required) || 1;
            const gap = Number(skill.gap) || 0;
            const met = Boolean(skill.met);
            return (
              <div key={String(skill.category)} className="p-4 bg-white border-border shadow-card border border-white/10 rounded-xl">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${met ? 'bg-emerald-400' : 'bg-red-400'}`} />
                    <span className="font-medium capitalize">{String(skill.category).replace(/_/g, ' ')}</span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-400">{current}</span>
                    <span className="text-gray-600"> / </span>
                    <span>{required}</span>
                    {!met && <span className="ml-2 text-red-400 text-xs">-{gap} gap</span>}
                  </div>
                </div>
                <div className="h-2 bg-white border-border shadow-card rounded-full overflow-hidden">
                  <motion.div className="h-full rounded-full" style={{ backgroundColor: met ? '#10b981' : '#ef4444' }}
                    initial={{ width: 0 }} animate={{ width: `${Math.min(100, (current / required) * 100)}%` }}
                    transition={{ duration: 1, delay: 0.2 }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {recommendations.length > 0 && (
        <div className="p-6 bg-white border-border shadow-card border border-white/10 rounded-2xl">
          <h3 className="text-lg font-semibold mb-3">Recommendations</h3>
          <ul className="space-y-2">
            {recommendations.map((rec, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                <ArrowRight className="w-4 h-4 text-cyan-400 mt-0.5 flex-shrink-0" />
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function LoadingState() {
  return (
    <div className="flex items-center justify-center py-20">
      <div className="flex flex-col items-center gap-3">
        <div className="w-8 h-8 border-2 border-white/20 border-t-white rounded-full animate-spin" />
        <span className="text-gray-400 text-sm">Analyzing...</span>
      </div>
    </div>
  );
}
