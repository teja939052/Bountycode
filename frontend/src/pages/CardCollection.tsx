import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import api from '../services/api';
import { Card, CardGrid, CardSkeleton, getRarityEmoji, getRarityStars, getRarityColor } from '../components/ui/Card';
import MysteryBox from '../components/MysteryBox';
import DailyReward from '../components/DailyReward';
import StreakConstellation from '../components/StreakConstellation';
import XPBar from '../components/XPBar';
import AchievementShowcase from '../components/AchievementShowcase';
import { Flame, Trophy, Star, Zap, Coins, Crown, Medal, Award, Gem, Rocket, Sword, Shield, Anchor, Compass, Map, Eye, EyeOff } from 'lucide-react';

const RARITY_FILTERS = ['all', 'common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'];

const RARITY_FILTER_COLORS = {
  all: { active: 'bg-cyber-blue/20 text-cyber-blue border-cyber-blue/40', inactive: 'hover:bg-surface-card text-brand-muted' },
  common: { active: 'bg-gray-500/20 text-gray-300 border-gray-500/40', inactive: 'hover:bg-surface-card text-brand-muted' },
  uncommon: { active: 'bg-green-500/20 text-green-400 border-green-500/40', inactive: 'hover:bg-surface-card text-brand-muted' },
  rare: { active: 'bg-blue-500/20 text-blue-400 border-blue-500/40', inactive: 'hover:bg-surface-card text-brand-muted' },
  epic: { active: 'bg-purple-500/20 text-purple-400 border-purple-500/40', inactive: 'hover:bg-surface-card text-brand-muted' },
  legendary: { active: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40', inactive: 'hover:bg-surface-card text-brand-muted' },
  mythic: { active: 'bg-pink-500/20 text-pink-400 border-pink-500/40', inactive: 'hover:bg-surface-card text-brand-muted' },
};

const RARITY_HEX = {
  common: '#9CA3AF',
  uncommon: '#22C55E',
  rare: '#3B82F6',
  epic: '#A855F7',
  legendary: '#EAB308',
  mythic: '#EC4899',
};

export default function CardCollection() {
  const [cards, setCards] = useState([]);
  const [stats, setStats] = useState(null);
  const [profile, setProfile] = useState(null);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [selectedCard, setSelectedCard] = useState(null);
  const [mysteryReward, setMysteryReward] = useState(null);

  useEffect(() => {
    loadData();
  }, [filter]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [collectionData, statsData, profileData] = await Promise.all([
        api.getCardCollection(filter !== 'all' ? { rarity: filter } : {}).catch(() => ({ cards: [] })),
        api.getCardStats().catch(() => null),
        api.getGamificationProfile?.().catch(() => null),
      ]);
      setCards(collectionData.cards || []);
      setStats(statsData);
      setProfile(profileData);
    } catch (err) {
      console.error('Failed to load cards:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDrawCard = async () => {
    try {
      const result = await api.getDailyDraw();
      if (result.card) {
        setSelectedCard(result.card);
        loadData();
      }
    } catch (err) {
      console.error('Failed to draw card:', err);
    }
  };

  const handleMysteryReward = (reward) => {
    setMysteryReward(reward);
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ staggerChildren: 0.08 }}
          className="text-center mb-8"
        >
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-3xl md:text-4xl font-display font-black uppercase tracking-wider"
          >
            <span className="bg-gradient-to-r from-cyber-blue via-cyber-purple to-pink-500 bg-clip-text text-transparent">
              Card Collection
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.08 }}
            className="text-gray-500 font-mono text-sm mt-2"
          >
            {stats
              ? `${stats.total_collected} / ${stats.total_available} collected — ${stats.completion_percentage}% complete`
              : 'Loading collection...'}
          </motion.p>
        </motion.div>

        {/* Top Row: XP Bar + Mystery Box */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
          {/* XP Bar — wide */}
          <div className="lg:col-span-2">
            <Card rarity="rare" hoverEffect={false} className="!p-4">
              <XPBar xp={profile?.xp || 0} />
              <div className="flex flex-wrap items-center gap-3 sm:gap-4 mt-3 pt-3 border-t border-gray-700/30">
                <div className="flex items-center gap-1.5 text-xs text-brand-muted">
                  <span className="streak-fire">🔥</span>
                  <span className="font-mono">{profile?.streak || 0} day streak</span>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-brand-muted">
                  <span>🏆</span>
                  <span className="font-mono">Best: {profile?.longest_streak || 0}</span>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-brand-muted">
                  <span>🃏</span>
                  <span className="font-mono">{stats?.total_collected || 0} cards</span>
                </div>
              </div>
            </Card>
          </div>

          {/* Mystery Box */}
          <Card rarity="epic" hoverEffect={false} className="!p-4 flex flex-col items-center justify-center">
            <MysteryBox
              onReward={handleMysteryReward}
              canOpen={true}
              size="md"
            />
          </Card>
        </div>

        {/* Middle Row: Daily Reward + Streak Constellation */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
          {/* Daily Login Rewards */}
          <Card rarity="rare" hoverEffect={false} className="!p-5">
            <DailyReward
              currentDay={1}
              claimedDays={[]}
              onClaim={(day) => console.log('Claimed day', day)}
            />
          </Card>

          {/* Streak Constellation */}
          <Card rarity="epic" hoverEffect={false} className="!p-5 flex items-center justify-center">
            <StreakConstellation
              streak={profile?.streak || 0}
              longestStreak={profile?.longest_streak || 0}
            />
          </Card>
        </div>

        {/* Stats Grid */}
        {stats && stats.rarity_breakdown && (
          <div ref={statsRef} className="grid grid-cols-3 sm:grid-cols-6 gap-2 mb-6">
            {Object.entries(RARITY_HEX).map(([rarity, color]) => (
              <motion.div
                key={rarity}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center p-3 rounded-xl border border-gray-700/20 bg-gray-900/30"
              >
                <div className="text-lg">{getRarityEmoji(rarity)}</div>
                <div className="text-base font-display font-bold" style={{ color }}>
                  {stats.rarity_breakdown[rarity] || 0}
                </div>
                <div className="text-[9px] font-mono text-brand-secondary uppercase tracking-wider">
                  {rarity}
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {/* Rarity Filters */}
        <div className="flex flex-wrap gap-1.5 mb-5 justify-center">
          {RARITY_FILTERS.map((r) => {
            const isActive = filter === r;
            const colors = RARITY_FILTER_COLORS[r];
            return (
              <button
                key={r}
                onClick={() => setFilter(r)}
                className={`
                  px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all duration-200 border
                  ${isActive
                    ? `${colors.active} border-current/30`
                    : `border-transparent ${colors.inactive}`
                  }
                `}
              >
                {r === 'all' ? '🎯 All' : `${getRarityEmoji(r)} ${r.charAt(0).toUpperCase() + r.slice(1)}`}
              </button>
            );
          })}
        </div>

        {/* Card Grid */}
        {loading ? (
          <CardSkeleton count={12} />
        ) : cards.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center py-16"
          >
            <div className="text-5xl mb-4">🎴</div>
            <h3 className="text-lg font-display font-bold text-text-primary mb-2">No Cards Yet</h3>
            <p className="text-sm text-gray-500 mb-6 font-mono">
              Solve problems to collect cards and level up!
            </p>
            <button
              onClick={handleDrawCard}
              className="btn-primary text-sm"
            >
              🎴 Draw Your First Card
            </button>
          </motion.div>
        ) : (
          <CardGrid stagger>
            {cards.map((card, index) => (
              <Card
                key={card.id || index}
                rarity={card.rarity || 'common'}
                onClick={() => setSelectedCard(card)}
                tilt
                particles={card.rarity === 'legendary' || card.rarity === 'mythic'}
              >
                <div className="text-center">
                  <div className="text-3xl mb-2">{card.emoji || '📦'}</div>
                  <h3 className="font-semibold text-sm truncate">
                    {card.problem_title || 'Unknown'}
                  </h3>
                  <p className="text-[10px] font-mono text-gray-500 mt-1">{card.topic}</p>
                  <div className="flex items-center justify-center gap-0.5 mt-2">
                    {Array.from({ length: Math.min(getRarityStars(card.rarity), 6) }).map((_, i) => (
                      <span
                        key={i}
                        className="text-[10px]"
                        style={{ color: getRarityColor(card.rarity) }}
                      >
                        ★
                      </span>
                    ))}
                  </div>
                  {card.is_favorite && (
                    <span className="text-red-400 text-xs">❤️</span>
                  )}
                </div>
              </Card>
            ))}
          </CardGrid>
        )}

        {/* Card Detail Modal */}
        <AnimatePresence>
          {selectedCard && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
              onClick={() => setSelectedCard(null)}
            >
              <motion.div
                initial={{ scale: 0.85, opacity: 0, rotateY: -15 }}
                animate={{ scale: 1, opacity: 1, rotateY: 0 }}
                exit={{ scale: 0.85, opacity: 0, rotateY: 15 }}
                transition={{ type: 'spring', stiffness: 300, damping: 25 }}
                className="rounded-2xl p-6 max-w-md w-full relative overflow-hidden"
                style={{
                  background: `linear-gradient(135deg, ${getRarityColor(selectedCard.rarity)}15, rgba(17,19,24,0.95))`,
                  border: `2px solid ${getRarityColor(selectedCard.rarity)}40`,
                  boxShadow: `0 0 40px ${getRarityColor(selectedCard.rarity)}20`,
                }}
                onClick={(e) => e.stopPropagation()}
              >
                {/* Holo shimmer overlay */}
                <div className="absolute inset-0 holo-shimmer opacity-20 pointer-events-none" />

                <div className="relative z-10 text-center">
                  <div className="text-5xl mb-3">{selectedCard.emoji || '📦'}</div>
                  <h2 className="text-lg font-display font-bold text-text-primary mb-1">
                    {selectedCard.problem_title}
                  </h2>
                  <p className="text-sm font-mono text-brand-muted mb-3">{selectedCard.topic}</p>

                  <div
                    className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-3"
                    style={{
                      backgroundColor: `${getRarityColor(selectedCard.rarity)}18`,
                      color: getRarityColor(selectedCard.rarity),
                      border: `1px solid ${getRarityColor(selectedCard.rarity)}30`,
                    }}
                  >
                    {getRarityEmoji(selectedCard.rarity)} {selectedCard.rarity}
                  </div>

                  <div className="flex items-center justify-center gap-1 mb-4">
                    {Array.from({ length: Math.min(getRarityStars(selectedCard.rarity), 6) }).map((_, i) => (
                      <span
                        key={i}
                        className="text-base"
                        style={{ color: getRarityColor(selectedCard.rarity) }}
                      >
                        ★
                      </span>
                    ))}
                  </div>

                  <div className="text-xs font-mono text-gray-500 space-y-1 mb-5">
                    <p>Obtained: {new Date(selectedCard.obtained_at).toLocaleDateString()}</p>
                    {selectedCard.stats?.solve_time && (
                      <p>Solve Time: {selectedCard.stats.solve_time}s</p>
                    )}
                  </div>

                  <button
                    onClick={() => setSelectedCard(null)}
                    className="btn-primary text-sm w-full"
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
