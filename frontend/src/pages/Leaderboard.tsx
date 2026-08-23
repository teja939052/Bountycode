import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../services/api';
import useAuthStore from '../store/authStore';
import { Card, getRarityColor } from '../components/ui/Card';
import XPBar from '../components/XPBar';
import VirtualList from '../components/ui/VirtualList';
import { LeaderboardRowSkeleton } from '../components/ui/Skeleton';

const TIMEFRAMES = [
  { id: 'all', label: 'All Time', icon: '🏆' },
  { id: 'weekly', label: 'This Week', icon: '📅' },
  { id: 'monthly', label: 'This Month', icon: '🗓️' },
];

const BADGE_ICONS = {
  1: '🥇', 2: '🥈', 3: '🥉',
};

const LEVEL_TITLES = [
  { min: 0, title: 'Recruit', color: '#9CA3AF' },
  { min: 3, title: 'Scout', color: '#22C55E' },
  { min: 7, title: 'Operative', color: '#3B82F6' },
  { min: 12, title: 'Specialist', color: '#A855F7' },
  { min: 18, title: 'Elite', color: '#EAB308' },
  { min: 25, title: 'Legend', color: '#EC4899' },
];

function getLevelTitle(level) {
  let t = LEVEL_TITLES[0];
  for (const l of LEVEL_TITLES) {
    if (level >= l.min) t = l;
  }
  return t;
}

export default function Leaderboard() {
  const { user } = useAuthStore();
  const [leaderboard, setLeaderboard] = useState([]);
  const [myRank, setMyRank] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState('all');

  useEffect(() => {
    loadLeaderboard();
  }, [timeframe]);

  const loadLeaderboard = async () => {
    setLoading(true);
    try {
      const [lb, rank] = await Promise.all([
        api.gamification.getLeaderboard(50).catch(() => ({ users: [] })),
        api.rankApi.getProfile().catch(() => null),
      ]);
      setLeaderboard(lb.users || lb || []);
      setMyRank(rank);
    } catch {
      setLeaderboard([]);
    } finally {
      setLoading(false);
    }
  };

  const podium = leaderboard.slice(0, 3);
  const rest = leaderboard.slice(3);

  if (loading) {
    return (
      <div className="min-h-screen py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8 animate-pulse">
            <div className="h-4 bg-gray-700/40 rounded w-32 mx-auto mb-2" />
            <div className="h-8 bg-gray-700/40 rounded w-48 mx-auto mb-2" />
            <div className="h-3 bg-gray-700/30 rounded w-56 mx-auto" />
          </div>
          <LeaderboardRowSkeleton count={5} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <span className="section-subheader mb-2 block">Command Rankings</span>
          <h1 className="section-header text-3xl mb-2">
            Leader<span className="text-cyber-blue">board</span>
          </h1>
          <p className="text-gray-500 text-sm font-mono">
            Compete with other placement aspirants
          </p>
        </motion.div>

        {/* Timeframe tabs */}
        <div className="flex justify-center gap-1.5 mb-8">
          {TIMEFRAMES.map((tf) => (
            <button
              key={tf.id}
              onClick={() => setTimeframe(tf.id)}
              className={`px-4 py-2 rounded-lg text-xs font-mono font-medium uppercase tracking-wider transition-all duration-200 border ${
                timeframe === tf.id
                  ? 'bg-cyber-blue/15 text-cyber-blue border-cyber-blue/40'
                  : 'border-transparent text-gray-500 hover:text-gray-300 hover:bg-gray-50'
              }`}
            >
              <span className="mr-1.5">{tf.icon}</span>
              {tf.label}
            </button>
          ))}
        </div>

        {/* Podium — top 3 */}
        {podium.length > 0 && (
          <motion.div
            initial="hidden"
            animate="visible"
            variants={{ hidden: {}, visible: { transition: { staggerChildren: 0.12 } } }}
            className="flex justify-center items-end gap-2 sm:gap-4 mb-8 sm:mb-10"
          >
            {/* 2nd place */}
            {podium[1] && (
              <PodiumCard entry={podium[1]} rank={2} height="h-24 sm:h-32" delay={0.1} />
            )}
            {/* 1st place */}
            {podium[0] && (
              <PodiumCard entry={podium[0]} rank={1} height="h-32 sm:h-44" delay={0} />
            )}
            {/* 3rd place */}
            {podium[2] && (
              <PodiumCard entry={podium[2]} rank={3} height="h-20 sm:h-28" delay={0.2} />
            )}
            </motion.div>
          )}

        {/* Your rank banner */}
        {myRank && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card rarity="rare" hoverEffect={false} className="!p-3 mb-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-lg font-mono font-bold text-cyber-blue">
                    #{myRank.rank || '—'}
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-text-primary">Your Position</p>
                    <p className="text-[10px] font-mono text-gray-500">
                      {myRank.xp || 0} XP · Level {myRank.level || 1}
                    </p>
                  </div>
                </div>
                <XPBar xp={user?.xp || 0} compact className="w-32" />
              </div>
            </Card>
          </motion.div>
        )}

        {/* Full ranking list */}
        {leaderboard.length === 0 ? (
          <Card rarity="common" hoverEffect={false} className="text-center py-12">
            <div className="text-4xl mb-3">🏆</div>
            <p className="text-gray-400 text-sm">No rankings yet</p>
            <p className="text-xs text-gray-600 mt-1 font-mono">
              Be the first to practice and climb the ranks!
            </p>
          </Card>
        ) : (
          <VirtualList
            items={leaderboard}
            height={Math.min(600, leaderboard.length * 56)}
            itemHeight={56}
            renderItem={(entry, i) => {
              const rank = i + 1;
              const isMe = entry.user_id === user?.id || entry.name === user?.name;
              const lt = getLevelTitle(entry.level || 1);

              return (
                <div
                  className={`
                    flex items-center gap-2 sm:gap-4 px-3 sm:px-4 py-2.5 sm:py-3 rounded-xl border transition-all duration-200 mb-1.5
                    ${isMe
                      ? 'bg-cyber-blue/5 border-cyber-blue/30 shadow-[0_0_12px_rgba(76,201,240,0.08)]'
                      : 'bg-gray-900/20 border-gray-700/20 hover:border-gray-600/30 hover:bg-gray-800/20'
                    }
                    ${rank <= 3 ? 'ring-1' : ''}
                    ${rank === 1 ? 'ring-yellow-500/30' : rank === 2 ? 'ring-gray-400/20' : rank === 3 ? 'ring-amber-700/20' : ''}
                  `}
                >
                  {/* Rank */}
                  <div className="w-8 text-center shrink-0">
                    {BADGE_ICONS[rank] ? (
                      <span className="text-xl">{BADGE_ICONS[rank]}</span>
                    ) : (
                      <span className="text-sm font-mono font-bold text-gray-500">{rank}</span>
                    )}
                  </div>

                  {/* Avatar */}
                  <div
                    className="w-7 h-7 sm:w-9 sm:h-9 rounded-lg flex items-center justify-center text-xs sm:text-sm font-bold text-text-primary shrink-0"
                    style={{
                      background: `linear-gradient(135deg, ${lt.color}30, ${lt.color}15)`,
                      border: `1px solid ${lt.color}40`,
                    }}
                  >
                    {(entry.name || 'A')[0].toUpperCase()}
                  </div>

                  {/* Name + title */}
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm font-semibold truncate ${isMe ? 'text-cyber-blue' : 'text-text-primary'}`}>
                      {entry.name || 'Anonymous'}
                      {isMe && (
                        <span className="text-[9px] ml-2 px-1.5 py-0.5 rounded bg-cyber-blue/20 text-cyber-blue font-mono">
                          YOU
                        </span>
                      )}
                    </p>
                    <p className="text-[10px] font-mono" style={{ color: lt.color }}>
                      {lt.title}
                    </p>
                  </div>

                  {/* Level */}
                  <div className="hidden sm:block text-center w-14 shrink-0">
                    <span className="text-sm font-display font-bold" style={{ color: lt.color }}>
                      {entry.level || 1}
                    </span>
                    <p className="text-[8px] font-mono text-gray-600 uppercase">Level</p>
                  </div>

                  {/* XP */}
                  <div className="hidden sm:block text-center w-16 shrink-0">
                    <span className="text-sm font-display font-bold text-text-primary">
                      {(entry.xp || 0).toLocaleString()}
                    </span>
                    <p className="text-[8px] font-mono text-gray-600 uppercase">XP</p>
                  </div>

                  {/* Streak */}
                  <div className="hidden md:flex text-center w-12 shrink-0 items-center justify-center gap-1">
                    <span className={entry.streak > 0 ? 'streak-fire' : ''}>🔥</span>
                    <span className="text-sm font-bold text-text-primary">{entry.streak || 0}</span>
                  </div>
                </div>
              );
            }}
          />
        )}
      </div>
    </div>
  );
}

function PodiumCard({ entry, rank, height, delay }) {
  const medalColors = { 1: '#EAB308', 2: '#9CA3AF', 3: '#CD7F32' };
  const medalEmoji = { 1: '🥇', 2: '🥈', 3: '🥉' };
  const color = medalColors[rank] || '#9CA3AF';
  const isTop = rank === 1;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, type: 'spring', stiffness: 200 }}
      className={`flex flex-col items-center ${isTop ? 'order-2' : rank === 2 ? 'order-1' : 'order-3'}`}
    >
      {/* Name */}
      <p className={`text-sm font-bold text-text-primary mb-1 ${isTop ? 'text-base' : ''}`}>
        {entry.name || 'Anonymous'}
      </p>
      <p className="text-[10px] font-mono mb-2" style={{ color }}>
        {(entry.xp || 0).toLocaleString()} XP
      </p>

      {/* Trophy */}
      <div className="text-3xl mb-2">{medalEmoji[rank]}</div>

      {/* Pedestal */}
      <div
        className={`w-20 sm:w-24 ${height} rounded-t-xl flex flex-col items-center justify-center border`}
        style={{
          background: `linear-gradient(180deg, ${color}15, ${color}05)`,
          borderColor: `${color}40`,
          boxShadow: isTop ? `0 0 20px ${color}15` : undefined,
        }}
      >
        <span className="text-2xl font-display font-black" style={{ color }}>
          #{rank}
        </span>
        <span className="text-[9px] font-mono text-gray-500 mt-1">
          Level {entry.level || 1}
        </span>
      </div>
    </motion.div>
  );
}
