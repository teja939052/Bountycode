import { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Card } from '../components/ui/Card';
import { TrendingUp, Target, AlertTriangle, CheckCircle, Zap, ChevronRight, Filter } from 'lucide-react';
import UserEmblem from '../components/emblems/UserEmblem';
import { Emblem } from '../components/emblems';

const SKILL_COLORS = {
  Arrays: '#3b82f6', Strings: '#8b5cf6', 'Linked Lists': '#06b6d4',
  Trees: '#10b981', DP: '#f59e0b', Graphs: '#ef4444',
  Hashing: '#ec4899', Stacks: '#6366f1', Greedy: '#14b8a6',
  Sorting: '#84cc16', Searching: '#f97316', Recursion: '#a855f7',
  Aptitude: '#22d3ee', Logical: '#fbbf24', English: '#34d399',
  Behavioral: '#f472b6', 'System Design': '#818cf8',
};

export default function DSAFingerprint() {
  const [profile, setProfile] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [companyDetail, setCompanyDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [profileRes, predictionsRes] = await Promise.all([
        api.getSkillProfile().catch(() => null),
        api.getCompanyPredictions().catch(() => null),
      ]);
      setProfile(profileRes);
      setPredictions(predictionsRes);
    } catch {}
    setLoading(false);
  };

  const loadCompanyDetail = async (companyId) => {
    setSelectedCompany(companyId);
    try {
      const res = await api.getCompanyFingerprint(companyId);
      setCompanyDetail(res);
    } catch { setCompanyDetail(null); }
  };

  const filteredPredictions = useMemo(() => {
    if (!predictions?.predictions) return [];
    if (filter === 'all') return predictions.predictions;
    if (filter === 'easy') return predictions.predictions.filter(p => p.probability >= 70);
    if (filter === 'medium') return predictions.predictions.filter(p => p.probability >= 40 && p.probability < 70);
    if (filter === 'hard') return predictions.predictions.filter(p => p.probability < 40);
    return predictions.predictions;
  }, [predictions, filter]);

  if (loading) {
    return (
      <div className="min-h-screen py-8 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <div className="spinner-cyber mx-auto mb-4" />
            <p className="text-sm font-mono text-gray-400">Analyzing your skill fingerprint...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-6 sm:py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-6 sm:mb-8">
          <span className="section-subheader mb-2 block">Your Skill DNA</span>
          <h1 className="section-header text-2xl sm:text-3xl mb-2">
            DSA <span className="text-cyber-blue">Fingerprint</span>
          </h1>
          <p className="text-gray-500 text-xs sm:text-sm font-mono">See exactly where you stand — and which companies you can crack</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Skill Radar + Stats */}
          <div className="lg:col-span-1 space-y-4">
            {/* Overall Score */}
            <Card rarity="legendary" hoverEffect={false}>
              <div className="text-center">
                <div className="mx-auto mb-4 flex justify-center">
                  <UserEmblem
                    skills={profile?.skills || {}}
                    level={profile?.level || 1}
                    xp={profile?.xp || 0}
                    size={128}
                  />
                </div>
                <p className="text-xs font-mono text-gray-400">Your Skill DNA</p>
                <div className="flex justify-center gap-4 mt-3">
                  <div className="text-center">
                    <div className="text-sm font-bold text-cyber-blue">{profile?.total_solved || 0}</div>
                    <div className="text-[9px] text-gray-500">Solved</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-bold text-cyber-green">{predictions?.summary?.easy_clear?.count || 0}</div>
                    <div className="text-[9px] text-gray-500">Easy Clear</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-bold text-yellow-400">{predictions?.summary?.moderate?.count || 0}</div>
                    <div className="text-[9px] text-gray-500">Moderate</div>
                  </div>
                </div>
              </div>
            </Card>

            {/* Skill Breakdown (Bar Chart) */}
            <Card rarity="rare" hoverEffect={false}>
              <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Skill Breakdown</h3>
              <div className="space-y-2">
                {Object.entries(profile?.skills || {}).filter(([,s]: [string, any]) => s.solved > 0 || s.score > 0).sort(([,a]: [string, any],[,b]: [string, any]) => b.score - a.score).slice(0, 12).map(([topic, skill]: [string, any]) => (
                  <div key={topic} className="flex items-center gap-2">
                    <span className="text-[10px] font-mono text-gray-400 w-20 truncate">{topic}</span>
                    <div className="flex-1 h-2 rounded bg-gray-700/30 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${skill.score}%` }}
                        transition={{ duration: 0.8, delay: 0.1 }}
                        className="h-full rounded"
                        style={{ backgroundColor: SKILL_COLORS[topic] || '#6366f1' }}
                      />
                    </div>
                    <span className="text-[10px] font-mono text-gray-500 w-8 text-right">{Math.round(skill.score)}</span>
                  </div>
                ))}
                {Object.keys(profile?.skills || {}).filter(k => (profile.skills as any)[k]?.solved > 0).length === 0 && (
                  <p className="text-xs text-gray-500 text-center py-4">Solve some problems to see your skill breakdown</p>
                )}
              </div>
            </Card>

            {/* Strongest / Weakest */}
            {profile?.strongest?.length > 0 && (
              <Card rarity="uncommon" hoverEffect={false}>
                <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-2">
                  <CheckCircle size={12} className="inline mr-1 text-green-400" /> Strongest
                </h3>
                <div className="flex flex-wrap gap-1">
                  {profile.strongest.map((s, i) => (
                    <span key={i} className="text-[10px] font-mono px-2 py-1 rounded bg-green-500/10 text-green-400 border border-green-500/20">
                      {s.topic} ({Math.round(s.score)})
                    </span>
                  ))}
                </div>
              </Card>
            )}
          </div>

          {/* Right: Company Predictions */}
          <div className="lg:col-span-2 space-y-4">
            {/* Filter */}
            <div className="flex items-center gap-2 flex-wrap">
              <Filter size={14} className="text-gray-500" />
              {['all', 'easy', 'medium', 'hard'].map(f => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-mono uppercase tracking-wider transition-all border ${
                    filter === f
                      ? 'bg-cyber-blue/15 text-cyber-blue border-cyber-blue/40'
                      : 'border-gray-700/20 text-gray-500 hover:text-gray-300'
                  }`}
                >
                  {f === 'all' ? 'All Companies' : f === 'easy' ? 'Easy Clear (70%+)' : f === 'medium' ? 'Moderate (40-70%)' : 'Needs Work (<40%)'}
                </button>
              ))}
            </div>

            {/* Company Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {filteredPredictions.map((pred, i) => (
                <motion.div
                  key={pred.company_id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.03 }}
                >
                  <div
                    onClick={() => loadCompanyDetail(pred.company_id)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all hover:scale-[1.02] ${
                      selectedCompany === pred.company_id
                        ? 'bg-gray-800/60 border-cyber-blue/40'
                        : 'bg-gray-900/40 border-gray-700/30 hover:border-gray-600/40'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-lg">{pred.icon}</span>
                        <div>
                          <h4 className="font-display font-bold text-xs text-text-primary">{pred.company_name}</h4>
                          <p className="text-[9px] font-mono text-gray-500">{pred.package}</p>
                        </div>
                      </div>
                      <ProbabilityBadge probability={pred.probability} />
                    </div>

                    {/* Mini Progress */}
                    <div className="h-1.5 rounded-full bg-gray-700/30 overflow-hidden mb-2">
                      <div
                        className="h-full rounded-full transition-all duration-500"
                        style={{
                          width: `${pred.probability}%`,
                          backgroundColor: pred.probability >= 70 ? '#22c55e' : pred.probability >= 40 ? '#f59e0b' : '#ef4444',
                        }}
                      />
                    </div>

                    {/* Top Gaps */}
                    {pred.gaps?.length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {pred.gaps.slice(0, 3).map((gap, j) => (
                          <span key={j} className="text-[8px] font-mono px-1.5 py-0.5 rounded bg-red-500/10 text-red-400/80 border border-red-500/15">
                            {gap.topic} -{Math.round(gap.gap)}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
            </div>

            {filteredPredictions.length === 0 && (
              <Card rarity="common" hoverEffect={false}>
                <p className="text-sm text-gray-400 text-center py-8">
                  {filter === 'easy' ? "No companies in 'Easy Clear' yet. Keep practicing!" :
                   filter === 'medium' ? "No companies in 'Moderate' range yet." :
                   "No companies in 'Needs Work' — you're doing great!"}
                </p>
              </Card>
            )}
          </div>
        </div>

        {/* Company Detail Modal */}
        <AnimatePresence>
          {selectedCompany && companyDetail && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-surface-2 backdrop-blur-sm"
              onClick={() => { setSelectedCompany(null); setCompanyDetail(null); }}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                onClick={(e) => e.stopPropagation()}
                className="w-full max-w-lg max-h-[80vh] overflow-y-auto bg-gray-900 border border-gray-700/50 rounded-2xl p-6"
              >
                {/* Header */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">{companyDetail.icon}</span>
                    <div>
                      <h2 className="text-lg font-display font-bold text-text-primary">{companyDetail.company_name}</h2>
                      <p className="text-xs font-mono text-gray-400">{companyDetail.exam_pattern}</p>
                    </div>
                  </div>
                  <ProbabilityBadge probability={companyDetail.probability} size="lg" />
                </div>

                {/* Probability Bar */}
                <div className="mb-4">
                  <div className="h-3 rounded-full bg-gray-700/30 overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${companyDetail.probability}%` }}
                      transition={{ duration: 1 }}
                      className="h-full rounded-full"
                      style={{
                        backgroundColor: companyDetail.probability >= 70 ? '#22c55e' :
                                          companyDetail.probability >= 40 ? '#f59e0b' : '#ef4444',
                      }}
                    />
                  </div>
                </div>

                {/* Topic Breakdown */}
                <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-2">Topic Readiness</h3>
                <div className="space-y-2 mb-4">
                  {companyDetail.topic_breakdown?.slice(0, 8).map((t, i) => (
                    <div key={i} className="flex items-center gap-2">
                      <Emblem topic={t.topic} size={14} animated={false} glow={false} />
                      <span className="text-[10px] font-mono text-gray-400 w-24 truncate">
                        {t.topic} {t.focus_match && '⭐'}
                      </span>
                      <div className="flex-1 h-2 rounded bg-gray-700/30 overflow-hidden">
                        <div
                          className="h-full rounded"
                          style={{
                            width: `${t.your_score}%`,
                            backgroundColor: t.your_score >= 70 ? '#22c55e' : t.your_score >= 40 ? '#f59e0b' : '#ef4444',
                          }}
                        />
                      </div>
                      <span className="text-[10px] font-mono text-gray-500 w-8 text-right">{Math.round(t.your_score)}</span>
                    </div>
                  ))}
                </div>

                {/* Gaps */}
                {companyDetail.gaps?.length > 0 && (
                  <div className="mb-4">
                    <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-2">
                      <AlertTriangle size={12} className="inline mr-1 text-yellow-400" /> Gaps to Close
                    </h3>
                    <div className="space-y-2">
                      {companyDetail.gaps.map((gap, i) => (
                        <div key={i} className="p-3 rounded-lg bg-gray-800/40 border border-gray-700/30">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-xs font-mono text-text-primary">{gap.topic}</span>
                            <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                              gap.gap > 20 ? 'bg-red-500/15 text-red-400' : 'bg-yellow-500/15 text-yellow-400'
                            }`}>
                              -{Math.round(gap.gap)} gap
                            </span>
                          </div>
                          <div className="h-1.5 rounded bg-gray-700/30 overflow-hidden">
                            <div
                              className="h-full rounded bg-red-500/50"
                              style={{ width: `${Math.min(100, gap.gap)}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Recommendations */}
                {companyDetail.recommendations?.length > 0 && (
                  <div className="mb-4">
                    <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-2">
                      <Zap size={12} className="inline mr-1 text-cyber-blue" /> Practice These
                    </h3>
                    <div className="space-y-2">
                      {companyDetail.recommendations.map((rec, i) => (
                        <div key={i} className="p-3 rounded-lg bg-cyber-blue/5 border border-cyber-blue/20">
                          <p className="text-xs font-mono text-cyber-blue mb-1">{rec.topic}</p>
                          {rec.problems?.map((p, j) => (
                            <div key={j} className="flex items-center gap-2 py-1">
                              <span className={`w-1.5 h-1.5 rounded-full ${
                                p.difficulty === 'easy' ? 'bg-green-400' : p.difficulty === 'medium' ? 'bg-yellow-400' : 'bg-red-400'
                              }`} />
                              <span className="text-[10px] font-mono text-gray-300 truncate">{p.question}</span>
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* CTA */}
                <div className="flex gap-2">
                  <Link
                    to="/question-bank"
                    onClick={() => { setSelectedCompany(null); setCompanyDetail(null); }}
                    className="flex-1 btn-primary text-center text-xs py-2"
                  >
                    Practice Now
                  </Link>
                  <button
                    onClick={() => { setSelectedCompany(null); setCompanyDetail(null); }}
                    className="flex-1 btn-secondary text-xs py-2"
                  >
                    Close
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function ProbabilityBadge({ probability, size = "sm" }) {
  const color = probability >= 70 ? 'text-green-400 bg-green-500/15 border-green-500/30' :
                probability >= 40 ? 'text-yellow-400 bg-yellow-500/15 border-yellow-500/30' :
                'text-red-400 bg-red-500/15 border-red-500/30';
  const label = probability >= 70 ? 'High' : probability >= 40 ? 'Moderate' : 'Low';

  return (
    <div className={`flex flex-col items-center ${size === 'lg' ? 'px-4 py-2' : 'px-2 py-1'} rounded-lg border ${color}`}>
      <span className={`font-display font-black ${size === 'lg' ? 'text-2xl' : 'text-sm'}`}>{Math.round(probability)}%</span>
      <span className="text-[8px] font-mono uppercase">{label}</span>
    </div>
  );
}
