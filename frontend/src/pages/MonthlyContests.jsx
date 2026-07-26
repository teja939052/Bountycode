import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';
import api from '../services/api';
import { Card } from '../components/ui/Card';

const MOCK_CONTESTS = [
  {
    id: '1',
    title: 'July Speed Sprint',
    description: 'Solve 30 problems in 30 days. Fastest solver wins.',
    status: 'active',
    start_date: '2026-07-01',
    end_date: '2026-07-31',
    participants: 142,
    prize: '🏆 + 5000 XP',
    difficulty: 'all',
  },
  {
    id: '2',
    title: 'DSA Gauntlet',
    description: 'Tackle hard problems only. Show your mettle.',
    status: 'upcoming',
    start_date: '2026-08-01',
    end_date: '2026-08-15',
    participants: 0,
    prize: '🏅 + 3000 XP + Badge',
    difficulty: 'hard',
  },
  {
    id: '3',
    title: 'Speed Code Championship',
    description: '60-minute coding sprints. Best of 5 rounds wins.',
    status: 'upcoming',
    start_date: '2026-08-15',
    end_date: '2026-08-30',
    participants: 0,
    prize: '💎 + 10000 XP + Legendary Card',
    difficulty: 'expert',
  },
];

const STATUS_COLORS = {
  active: { bg: 'bg-green-500/15', text: 'text-green-400', border: 'border-green-500/30', label: 'LIVE NOW' },
  upcoming: { bg: 'bg-blue-500/15', text: 'text-blue-400', border: 'border-blue-500/30', label: 'UPCOMING' },
  ended: { bg: 'bg-gray-500/15', text: 'text-gray-400', border: 'border-gray-500/30', label: 'ENDED' },
};

function CountdownTimer({ endDate }) {
  const [timeLeft, setTimeLeft] = useState('');
  useEffect(() => {
    const timer = setInterval(() => {
      const end = new Date(endDate).getTime();
      const now = Date.now();
      const diff = end - now;
      if (diff <= 0) { setTimeLeft('Ended'); clearInterval(timer); return; }
      const d = Math.floor(diff / (1000 * 60 * 60 * 24));
      const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const m = Math.floor((diff / (1000 * 60)) % 60);
      const s = Math.floor((diff / 1000) % 60);
      setTimeLeft(`${d}d ${h}h ${m}m ${s}s`);
    }, 1000);
    return () => clearInterval(timer);
  }, [endDate]);
  return <span className="font-mono text-sm">{timeLeft}</span>;
}

export default function MonthlyContests() {
  const [contests, setContests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('active');
  const gridRef = useRef(null);

  useEffect(() => {
    loadContests();
  }, []);

  useEffect(() => {
    if (!loading && gridRef.current) {
      gsap.fromTo(gridRef.current.children, { opacity: 0, y: 20 }, { opacity: 1, y: 0, stagger: 0.08, duration: 0.4, ease: 'power2.out' });
    }
  }, [loading, activeTab]);

  const loadContests = async () => {
    setLoading(true);
    try {
      const data = await api.getContests?.().catch(() => null);
      setContests(data?.contests || MOCK_CONTESTS);
    } catch { setContests(MOCK_CONTESTS); }
    finally { setLoading(false); }
  };

  const filtered = contests.filter(c => {
    if (activeTab === 'active') return c.status === 'active';
    if (activeTab === 'upcoming') return c.status === 'upcoming';
    return true;
  });

  const handleJoin = async (contestId) => {
    try { await api.joinContest?.(contestId); loadContests(); } catch {}
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-5xl mx-auto">
        <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8">
          <span className="section-subheader mb-2 block">Compete & Win</span>
          <h1 className="section-header text-3xl mb-2">
            Monthly <span className="text-cyber-amber">Contests</span>
          </h1>
          <p className="text-gray-500 text-sm font-mono">Compete with other placement aspirants for prizes</p>
        </motion.div>

        {/* Tabs */}
        <div className="flex justify-center gap-1.5 mb-8">
          {['active', 'upcoming', 'all'].map((tab) => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg text-xs font-mono font-medium uppercase tracking-wider transition-all border ${
                activeTab === tab ? 'bg-cyber-amber/15 text-cyber-amber border-cyber-amber/40' : 'border-transparent text-gray-500 hover:text-gray-300 hover:bg-white/5'
              }`}>
              {tab === 'active' ? '🔥 Live' : tab === 'upcoming' ? '📅 Upcoming' : '📋 All'}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="grid sm:grid-cols-2 gap-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="rounded-xl border border-gray-700/20 p-6 animate-pulse bg-gray-900/20">
                <div className="h-5 bg-gray-700/40 rounded w-2/3 mb-3" />
                <div className="h-3 bg-gray-700/30 rounded w-full mb-2" />
                <div className="h-3 bg-gray-700/20 rounded w-1/2" />
              </div>
            ))}
          </div>
        ) : (
          <div ref={gridRef} className="grid sm:grid-cols-2 gap-4">
            {filtered.map((contest) => {
              const sc = STATUS_COLORS[contest.status] || STATUS_COLORS.ended;
              return (
                <Card
                  key={contest.id}
                  rarity={contest.status === 'active' ? 'epic' : contest.status === 'upcoming' ? 'rare' : 'common'}
                  hoverEffect
                  tilt
                >
                  <div className="flex items-start justify-between mb-3">
                    <span className={`text-[9px] font-mono font-bold uppercase tracking-widest px-2 py-0.5 rounded ${sc.bg} ${sc.text} border ${sc.border}`}>
                      {sc.label}
                    </span>
                    {contest.status === 'active' && (
                      <CountdownTimer endDate={contest.end_date} />
                    )}
                  </div>

                  <h3 className="text-lg font-display font-bold text-white mb-1">{contest.title}</h3>
                  <p className="text-xs text-gray-400 mb-4">{contest.description}</p>

                  <div className="flex flex-wrap items-center gap-3 sm:gap-4 text-[10px] font-mono text-gray-500 mb-4">
                    <span>👥 {contest.participants} joined</span>
                    <span>🏆 {contest.prize}</span>
                    <span>📊 {contest.difficulty}</span>
                  </div>

                  {/* Progress bar for active */}
                  {contest.status === 'active' && (
                    <div className="mb-4">
                      <div className="flex justify-between text-[9px] font-mono text-gray-500 mb-1">
                        <span>{new Date(contest.start_date).toLocaleDateString()}</span>
                        <span>{new Date(contest.end_date).toLocaleDateString()}</span>
                      </div>
                      <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
                        <motion.div
                          className="h-full rounded-full bg-gradient-to-r from-cyber-amber to-yellow-400"
                          initial={{ width: 0 }}
                          animate={{ width: `${Math.min(((Date.now() - new Date(contest.start_date).getTime()) / (new Date(contest.end_date).getTime() - new Date(contest.start_date).getTime())) * 100, 100)}%` }}
                          transition={{ duration: 1, ease: 'easeOut' }}
                        />
                      </div>
                    </div>
                  )}

                  <button
                    onClick={(e) => { e.stopPropagation(); handleJoin(contest.id); }}
                    disabled={contest.status === 'ended'}
                    className={`w-full py-2 rounded-lg text-xs font-mono font-bold uppercase tracking-wider transition-all ${
                      contest.status === 'active'
                        ? 'bg-cyber-amber/15 text-cyber-amber border border-cyber-amber/30 hover:bg-cyber-amber/25'
                        : contest.status === 'upcoming'
                        ? 'bg-cyber-blue/15 text-cyber-blue border border-cyber-blue/30 hover:bg-cyber-blue/25'
                        : 'bg-gray-800 text-gray-500 border border-gray-700/30 cursor-not-allowed'
                    }`}
                  >
                    {contest.status === 'active' ? '⚔️ Join Now' : contest.status === 'upcoming' ? '🔔 Remind Me' : 'Ended'}
                  </button>
                </Card>
              );
            })}
          </div>
        )}

        {filtered.length === 0 && !loading && (
          <Card rarity="common" hoverEffect={false} className="text-center py-12">
            <div className="text-4xl mb-3">🏆</div>
            <p className="text-gray-400 text-sm">No {activeTab === 'active' ? 'live' : activeTab} contests right now</p>
            <p className="text-xs text-gray-600 mt-1 font-mono">Check back soon!</p>
          </Card>
        )}
      </div>
    </div>
  );
}
