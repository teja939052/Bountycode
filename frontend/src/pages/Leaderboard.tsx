import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../services/api';
import useAuthStore from '../store/authStore';
import { Card, getRarityColor } from '../components/ui/Card';
import DiamondsBar from '../components/XPBar';
import VirtualList from '../components/ui/VirtualList';
import { LeaderboardRowSkeleton } from '../components/ui/Skeleton';
import type { LeaderboardEntry } from '../services/api/types';

const TIMEFRAMES = [
  { id: 'all', label: 'All Time', icon: '🏆' },
  { id: 'weekly', label: 'This Week', icon: '📅' },
  { id: 'monthly', label: 'This Month', icon: '🗓️' },
];

const BADGE_ICONS = {
  1: '🥇', 2: '🥈', 3: '🥉',
};

export default function Leaderboard() {
  const { user } = useAuthStore();
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [myRank, setMyRank] = useState<LeaderboardEntry | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState('all');
  const [leagueMeta, setLeagueMeta] = useState<{
    user_index?: number | null;
    user_rank?: number | null;
    band_start: number;
    band_end: number;
    total: number;
  } | null>(null);
  // Server-computed own rank + gap: works even outside the top-50 list.
  // List-derived values below remain as fallback when this is unavailable.
  const [myRankServer, setMyRankServer] = useState<{
    rank: number; of: number; period_xp: number;
    next_up: { xp_gap: number; target_xp: number } | null;
  } | null>(null);

  useEffect(() => {
    loadLeaderboard();
  }, [timeframe]);

  const loadLeaderboard = async () => {
    setLoading(true);
    setLeagueMeta(null);
    try {
      const tf = timeframe === "weekly" || timeframe === "monthly" ? timeframe : "all";
      api.gamification.getMyRank(tf as "all" | "weekly" | "monthly")
        .then(setMyRankServer)
        .catch(() => setMyRankServer(null));
      if (timeframe === "weekly" || timeframe === "monthly") {
        const league = await api.gamification.getLeagueLeaderboard(timeframe).catch(() => ({
          entries: [],
          user_index: null,
          user_rank: null,
          band_start: 1,
          band_end: 5,
          total: 0,
        }));
        const entries = league.entries || [];
        setLeaderboard(entries);
        setLeagueMeta({
          user_index: league.user_index ?? null,
          user_rank: league.user_rank ?? null,
          band_start: league.band_start,
          band_end: league.band_end,
          total: league.total || entries.length,
        });
        const me = entries.find((e: LeaderboardEntry) => e.user_id === user?.id || e.name === user?.name) || null;
        setMyRank(me);
      } else {
        const lb = await api.gamification.getLeaderboard(50, "all").catch(() => ({ entries: [] }));
        const entries = lb.entries || [];
        setLeaderboard(entries);
        const me = entries.find((e: LeaderboardEntry) => e.user_id === user?.id || e.name === user?.name) || null;
        setMyRank(me);
      }
    } catch {
      setLeaderboard([]);
      setMyRank(null);
      setLeagueMeta(null);
    } finally {
      setLoading(false);
    }
  };

  const getZoneColor = (index: number, total: number, zone?: string | null) => {
    if (zone === "promotion") return "text-emerald-400";
    if (zone === "demotion") return "text-red-400";
    if (zone === "safe") return "text-sky-400";
    if (total <= 0) return "text-gray-400";
    const pct = (index + 1) / total;
    if (pct <= 0.1) return "text-emerald-400";
    if (pct <= 0.3) return "text-sky-400";
    if (pct >= 0.9) return "text-red-400";
    return "text-gray-400";
  };

  const getZoneLabel = (index: number, total: number, zone?: string | null) => {
    if (zone === "promotion") return "Promotion zone";
    if (zone === "demotion") return "Demotion zone";
    if (zone === "safe") return "Safe";
    if (total <= 0) return "";
    const pct = (index + 1) / total;
    if (pct <= 0.1) return "Promotion zone";
    if (pct <= 0.3) return "Safe";
    if (pct >= 0.9) return "Demotion zone";
    return "";
  };

  const podium = leaderboard.slice(0, 3);

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

  const totalEntries = leaderboard.length;
  const myIndex = leagueMeta?.user_index ?? (myRank ? leaderboard.findIndex((e) => e.user_id === myRank.user_id || e.name === myRank.name) : -1);
  const nextEntry = typeof myIndex === "number" && myIndex >= 0 && myIndex < totalEntries - 1 ? leaderboard[myIndex + 1] : null;
  const xpToNext = nextEntry && myRank ? Math.max(0, (nextEntry.diamonds || 0) - (myRank.diamonds || 0)) : 0;
  const myRankFromMeta = typeof leagueMeta?.user_rank === "number" ? leagueMeta.user_rank : (myIndex >= 0 ? myIndex + 1 : undefined);

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <span className="section-subheader mb-2 block text-xs font-mono uppercase tracking-widest text-gray-500">Command Rankings</span>
          <h1 className="section-header text-3xl mb-2 font-black tracking-tight">
            Leader<span className="text-cyber-blue">board</span>
          </h1>
          <p className="text-gray-500 text-sm font-mono">Compete with other placement aspirants</p>
        </motion.div>

        {/* Timeframe tabs */}
        <div className="flex justify-center gap-1.5 mb-8">
          {TIMEFRAMES.map((tf) => (
            <button
              key={tf.id}
              onClick={() => setTimeframe(tf.id)}
              className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase tracking-wider transition-all duration-200 border ${
                timeframe === tf.id
                  ? 'bg-cyber-blue/15 text-cyber-blue border-cyber-blue/40 shadow-[0_0_12px_rgba(76,201,240,0.12)]'
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
            variants={{ hidden: {}, visible: { transition: { staggerChildren: 0.1 } } }}
            className="flex justify-center items-end gap-2 sm:gap-4 mb-8 sm:mb-10"
          >
            {/* 2nd place */}
            {podium[1] && (
              <PodiumCard entry={podium[1]} rank={2} height="h-24 sm:h-32" delay={0.1} timeframe={timeframe} />
            )}
            {/* 1st place */}
            {podium[0] && (
              <PodiumCard entry={podium[0]} rank={1} height="h-32 sm:h-44" delay={0} timeframe={timeframe} />
            )}
            {/* 3rd place */}
            {podium[2] && (
              <PodiumCard entry={podium[2]} rank={3} height="h-20 sm:h-28" delay={0.2} timeframe={timeframe} />
            )}
          </motion.div>
        )}

        {/* Your rank banner.
            Server values (myRankServer) work even outside the top-50 list;
            list-derived values are the fallback, never the primary. */}
        {(myRank || myRankServer) && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mb-6"
          >
            <Card rarity="rare" hoverEffect={false} className="!p-4">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <span className="text-lg font-mono font-black text-cyber-blue">
                    #{myRankServer?.rank ?? myRankFromMeta ?? '—'}
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-text-primary">Your Position</p>
                    <p className="text-[10px] font-mono text-gray-500">
                      {myRank?.rank_emoji ? `${myRank.rank_emoji} ` : ''}{myRank?.rank_title || ''}{myRank?.rank_title ? ' · ' : ''}{((myRankServer?.period_xp ?? myRank?.diamonds) || 0).toLocaleString()} Diamonds · Level {myRank?.level || 1}
                    </p>
                    {timeframe !== "all" && leagueMeta && (
                      <p className="text-[10px] font-mono text-gray-500">
                        Levels {leagueMeta.band_start}–{leagueMeta.band_end} · {leagueMeta.total} players
                      </p>
                    )}
                    {(myRankServer?.next_up ? myRankServer.next_up.xp_gap : xpToNext) > 0 && (
                      <p className="text-[10px] font-mono text-emerald-400">
                        {((myRankServer?.next_up ? myRankServer.next_up.xp_gap : xpToNext) || 0).toLocaleString()} Diamonds to #{((myRankServer?.rank ?? myRankFromMeta) || 1) - 1}
                      </p>
                    )}
                    {((myRankServer?.next_up ? myRankServer.next_up.xp_gap : xpToNext) || 0) === 0 && typeof myIndex === "number" && myIndex > 0 && (
                      <p className="text-[10px] font-mono text-emerald-400">You can rank up now!</p>
                    )}
                  </div>
                </div>
                <XPBar diamonds={user?.diamonds || 0} level={myRank?.level} compact className="w-32" />
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
            renderItem={(entry: LeaderboardEntry, i) => {
              const rank = i + 1;
              const isMe = entry.user_id === user?.id || entry.name === user?.name;
              const zone = (entry as any).zone;
              const zoneColor = getZoneColor(i, totalEntries, zone);
              const zoneLabel = getZoneLabel(i, totalEntries, zone);
              const lt = entry.color || { from: '#9CA3AF', to: '#6B7280', label: 'Common', color: '#9CA3AF' };
              const title = entry.rank_title
                ? `${entry.rank_emoji || ''} ${entry.rank_title}`.trim()
                : (entry.title || lt.label);

              return (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: Math.min(i * 0.02, 0.4) }}
                  className={`
                    flex items-center gap-2 sm:gap-4 px-3 sm:px-4 py-2.5 sm:py-3 rounded-2xl border transition-all duration-200 mb-1.5
                    ${isMe
                      ? 'bg-cyber-blue/8 border-cyber-blue/30 shadow-[0_0_16px_rgba(76,201,240,0.1)]'
                      : 'bg-white/40 dark:bg-gray-900/30 border-gray-200/60 dark:border-gray-700/40 hover:border-gray-300 dark:hover:border-gray-600'
                    }
                  `}
                >
                  {/* Rank */}
                  <div className="w-8 text-center shrink-0">
                    {rank <= 3 && BADGE_ICONS[rank as keyof typeof BADGE_ICONS] ? (
                      <span className="text-xl">{BADGE_ICONS[rank as keyof typeof BADGE_ICONS]}</span>
                    ) : (
                      <span className={`text-sm font-mono font-bold ${zoneColor}`}>
                        #{rank}
                      </span>
                    )}
                  </div>

                  {/* Avatar */}
                  <div
                    className="w-9 h-9 rounded-xl flex items-center justify-center text-sm font-black text-text-primary shrink-0"
                    style={{
                      background: `linear-gradient(135deg, ${lt.color}30, ${lt.color}15)`,
                      border: `1px solid ${lt.color}40`,
                    }}
                  >
                    {(entry.name || 'A')[0].toUpperCase()}
                  </div>

                  {/* Name + title */}
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm font-bold truncate ${isMe ? 'text-cyber-blue' : 'text-text-primary'}`}>
                      {entry.name || 'Anonymous'}
                      {isMe && (
                        <span className="text-[9px] ml-2 px-1.5 py-0.5 rounded bg-cyber-blue/20 text-cyber-blue font-mono">
                          YOU
                        </span>
                      )}
                    </p>
                    <p className="text-[10px] font-mono flex items-center gap-1.5" style={{ color: lt.color }}>
                      <span>{title}</span>
                      {zoneLabel && <span className={`text-[9px] px-1.5 py-0.5 rounded-full ${zoneColor} bg-current/10`}>{zoneLabel}</span>}
                    </p>
                  </div>

                  {/* Level */}
                  <div className="hidden sm:flex items-center gap-1.5 w-16 shrink-0">
                    <span className="text-sm font-display font-black" style={{ color: lt.color }}>
                      {entry.level || 1}
                    </span>
                    <span className="text-[9px] font-mono text-gray-500 uppercase">lvl</span>
                  </div>

                  {/* Diamonds — period Diamonds on weekly/monthly tabs, lifetime on all */}
                  <div className="hidden md:flex items-center gap-1 w-20 shrink-0">
                    <span className="text-sm font-display font-black text-text-primary">
                      {((timeframe === "all" ? entry.diamonds : entry.period_xp ?? entry.diamonds) || 0).toLocaleString()}
                    </span>
                    <span className="text-[9px] font-mono text-gray-500 uppercase">diamonds</span>
                  </div>

                  {/* Streak */}
                  <div className="hidden md:flex items-center justify-center gap-1 w-12 shrink-0">
                    <span className={(entry.streak || 0) > 0 ? 'streak-fire' : 'opacity-40'}>🔥</span>
                    <span className="text-sm font-black text-text-primary">{entry.streak || 0}</span>
                  </div>
                </motion.div>
              );
            }}
          />
        )}
      </div>
    </div>
  );
}

function PodiumCard({ entry, rank, height, delay, timeframe }: {
  entry: LeaderboardEntry; rank: number; height: string; delay: number;
  timeframe?: string;
}) {
  const medalColors: Record<number, string> = { 1: '#EAB308', 2: '#9CA3AF', 3: '#CD7F32' };
  const medalEmoji: Record<number, string> = { 1: '🥇', 2: '🥈', 3: '🥉' };
  const color = medalColors[rank] || '#9CA3AF';
  const isTop = rank === 1;

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, type: 'spring', stiffness: 180, damping: 16 }}
      className={`flex flex-col items-center ${isTop ? 'order-2' : rank === 2 ? 'order-1' : 'order-3'}`}
    >
      {/* Avatar */}
      <div
        className="w-14 h-14 rounded-2xl flex items-center justify-center text-lg font-black mb-2"
        style={{
          background: `linear-gradient(135deg, ${color}35, ${color}18)`,
          border: `2px solid ${color}60`,
          boxShadow: `0 0 28px ${color}25`,
        }}
      >
        {(entry.name || '?')[0].toUpperCase()}
      </div>

      {/* Name */}
      <p className={`text-sm font-black text-text-primary mb-0.5 text-center ${isTop ? 'text-base' : ''}`}>
        {entry.name || 'Anonymous'}
      </p>
      {entry.rank_title && (
        <p className="text-[10px] font-mono mb-1 font-bold" style={{ color }}>
          {entry.rank_emoji} {entry.rank_title}
        </p>
      )}
      <p className="text-[10px] font-mono mb-2 font-bold" style={{ color }}>
        {((timeframe === "all" || !timeframe ? entry.diamonds : entry.period_xp ?? entry.diamonds) || 0).toLocaleString()} Diamonds
      </p>

      {/* Trophy */}
      <div className="text-3xl mb-2">{medalEmoji[rank]}</div>

      {/* Pedestal */}
      <div
        className={`w-20 sm:w-24 ${height} rounded-t-2xl flex flex-col items-center justify-center border`}
        style={{
          background: `linear-gradient(180deg, ${color}20, ${color}08)`,
          borderColor: `${color}45`,
          boxShadow: isTop ? `0 0 32px ${color}18` : 'none',
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
