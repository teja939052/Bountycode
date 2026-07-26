import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../services/api';
import { TowerProgress, BossBattle, StarsDisplay, PowerUpShop, WizardProgression, StreakFreeze, DailyGoal, getTitleForLevel, xpForLevel, xpForNextLevel } from '../components/tower';
import { Card } from '../components/ui/Card';
import { useToast } from '../components/Toast';
import { Trophy, Flame, Coins, Star, Zap, Target, Shield, Crown } from 'lucide-react';

export default function TowerDashboard() {
  const [tower, setTower] = useState(null);
  const [challenges, setChallenges] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('tower');
  const toast = useToast();

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [towerRes, challengeRes] = await Promise.all([
        api.getTower().catch(() => null),
        api.getChallenges().catch(() => null),
      ]);
      setTower(towerRes);
      setChallenges(challengeRes);
    } catch {}
    setLoading(false);
  };

  const handleBuyPowerUp = async (powerUpId) => {
    try {
      const res = await api.buyPowerUp(powerUpId);
      if (res.success === false) {
        toast.warning(res.message || "Not enough coins");
      } else {
        toast.success("Power-up purchased!");
        loadData();
      }
    } catch (err) {
      toast.error("Failed to buy power-up");
    }
  };

  const handleUsePowerUp = async (powerUpId) => {
    try {
      const res = await api.usePowerUp(powerUpId);
      if (res.success === false) {
        toast.warning(res.message || "No power-ups left");
      } else {
        toast.success(`Used ${res.power_up?.name || 'power-up'}!`);
        loadData();
      }
    } catch (err) {
      toast.error("Failed to use power-up");
    }
  };

  const handleClaimChallenge = async (type, id) => {
    try {
      const res = await api.claimChallenge(type, id);
      if (res.success) {
        toast.success(`+${res.xp_earned} XP claimed!`);
        loadData();
      } else {
        toast.warning(res.message || "Cannot claim yet");
      }
    } catch (err) {
      toast.error("Failed to claim reward");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen py-8 px-4 flex items-center justify-center">
        <div className="spinner-cyber" />
      </div>
    );
  }

  if (!tower) {
    return (
      <div className="min-h-screen py-8 px-4 flex items-center justify-center">
        <p className="text-gray-500 font-mono text-sm">Failed to load tower data</p>
      </div>
    );
  }

  const [title, emoji] = getTitleForLevel(tower.level);

  return (
    <div className="min-h-screen py-6 sm:py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-6">
          <span className="section-subheader mb-2 block">Placement Tower</span>
          <h1 className="section-header text-2xl sm:text-3xl mb-1">
            {emoji} <span className="text-cyber-blue">Level {tower.level}</span>
          </h1>
          <p className="text-gray-500 text-xs font-mono">{title}</p>
        </motion.div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
          <StatCard icon={<Trophy size={16} />} label="Rank" value={`#${tower.level}`} color="text-yellow-400" />
          <StatCard icon={<Flame size={16} />} label="Streak" value={`${tower.streak}d`} color="text-orange-400" />
          <StatCard icon={<Coins size={16} />} label="Coins" value={tower.coins} color="text-yellow-300" />
          <StatCard icon={<Star size={16} />} label="Stars" value={tower.stars_total} color="text-blue-400" />
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mb-6 bg-gray-900/40 rounded-xl p-1">
          {[
            { id: 'tower', label: 'Tower', icon: <Crown size={14} /> },
            { id: 'shop', label: 'Power-Ups', icon: <Zap size={14} /> },
            { id: 'challenges', label: 'Challenges', icon: <Target size={14} /> },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-lg text-xs font-mono uppercase tracking-wider transition-all ${
                activeTab === tab.id
                  ? 'bg-cyber-blue/15 text-cyber-blue border border-cyber-blue/30'
                  : 'text-gray-500 hover:text-gray-300'
              }`}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === 'tower' && (
          <div className="space-y-6">
            {/* Wizard */}
            <Card rarity="epic" hoverEffect={false}>
              <div className="flex items-center gap-4">
                <WizardProgression level={tower.level} size={96} />
                <div className="flex-1">
                  <h3 className="font-display font-bold text-sm text-white mb-1">{tower.wizard_outfit}</h3>
                  <p className="text-[10px] font-mono text-gray-500 mb-2">Streak Multiplier: {tower.streak_multiplier}x</p>
                  <StarsDisplay stars={Math.min(3, Math.floor(tower.stars_total / 10))} size="sm" animated={false} />
                </div>
              </div>
            </Card>

            {/* Tower Progress */}
            <TowerProgress
              level={tower.level}
              xp={tower.xp}
              xpToNext={tower.xp_for_current_level + (tower.xp_to_next || 100)}
              xpForCurrent={tower.xp_for_current_level}
              title={title}
              titleEmoji={emoji}
            />

            {/* Boss Battle */}
            {tower.current_boss && !tower.bosses_defeated?.includes(tower.boss_level) && (
              <BossBattle
                boss={tower.current_boss}
                level={tower.boss_level}
                onFight={() => {}}
                canSkip={(tower.power_ups?.skip_boss || 0) > 0}
                onSkip={() => handleUsePowerUp('skip_boss')}
              />
            )}

            {/* Daily Goal + Streak Freeze */}
            <div className="grid md:grid-cols-2 gap-4">
              <DailyGoal />
              <StreakFreeze streakFreezes={tower.streak_freezes} coins={tower.coins} />
            </div>
          </div>
        )}

        {activeTab === 'shop' && (
          <PowerUpShop
            coins={tower.coins}
            owned={tower.power_ups}
            onBuy={handleBuyPowerUp}
            onUse={handleUsePowerUp}
          />
        )}

        {activeTab === 'challenges' && challenges && (
          <div className="space-y-4">
            {/* Weekly */}
            <Card rarity="rare" hoverEffect={false}>
              <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">
                Weekly Challenges
              </h3>
              <div className="space-y-2">
                {challenges.weekly?.map((ch) => (
                  <ChallengeRow key={ch.id} challenge={ch} type="weekly" onClaim={handleClaimChallenge} />
                ))}
                {(!challenges.weekly || challenges.weekly.length === 0) && (
                  <p className="text-xs text-gray-500 text-center py-4">No weekly challenges yet</p>
                )}
              </div>
            </Card>

            {/* Monthly */}
            <Card rarity="epic" hoverEffect={false}>
              <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">
                Monthly Challenges
              </h3>
              <div className="space-y-2">
                {challenges.monthly?.map((ch) => (
                  <ChallengeRow key={ch.id} challenge={ch} type="monthly" onClaim={handleClaimChallenge} />
                ))}
                {(!challenges.monthly || challenges.monthly.length === 0) && (
                  <p className="text-xs text-gray-500 text-center py-4">No monthly challenges yet</p>
                )}
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, color }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gray-900/40 border border-gray-700/20 rounded-xl p-3 text-center"
    >
      <div className={`flex items-center justify-center gap-1 mb-1 ${color}`}>
        {icon}
      </div>
      <div className="text-sm font-display font-bold text-white">{value}</div>
      <div className="text-[9px] font-mono text-gray-500">{label}</div>
    </motion.div>
  );
}

function ChallengeRow({ challenge, type, onClaim }) {
  const progress = Math.min(100, ((challenge.progress || 0) / challenge.target) * 100);
  const isComplete = challenge.completed;
  const isClaimed = challenge.claimed;

  return (
    <div className={`flex items-center gap-3 p-3 rounded-lg border transition-all ${
      isClaimed
        ? 'bg-green-500/5 border-green-500/15 opacity-60'
        : isComplete
          ? 'bg-yellow-500/5 border-yellow-500/20'
          : 'bg-gray-800/30 border-gray-700/20'
    }`}>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-mono text-white truncate">{challenge.name}</p>
        <div className="flex items-center gap-2 mt-1">
          <div className="flex-1 h-1.5 rounded bg-gray-700/30 overflow-hidden">
            <div
              className="h-full rounded bg-cyber-blue transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
          <span className="text-[9px] font-mono text-gray-500">
            {challenge.progress || 0}/{challenge.target}
          </span>
        </div>
      </div>
      <div className="text-right shrink-0">
        <span className="text-[10px] font-mono text-cyber-amber">+{challenge.xp_reward} XP</span>
        {isComplete && !isClaimed && (
          <button
            onClick={() => onClaim(type, challenge.id)}
            className="block mt-1 px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-green-500/15 text-green-400 border border-green-500/30 hover:bg-green-500/25"
          >
            Claim
          </button>
        )}
        {isClaimed && (
          <span className="block mt-1 text-[9px] font-mono text-green-400">✓ Claimed</span>
        )}
      </div>
    </div>
  );
}
