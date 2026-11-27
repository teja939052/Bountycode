import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import { TowerProgress, BossBattle, StarsDisplay, PowerUpShop, StreakFreeze, DailyGoal, getTitleForLevel } from '../components/tower';
import ForestJourney from '../components/tower/ForestJourney';
import DailyBonusCalendar from '../components/DailyBonusCalendar';
import { useToast } from '../components/Toast';
import { useGamificationData } from '../hooks/useGamificationData';
import { Card, SectionHeader } from '../design-system/Card';
import { Button } from '../design-system/Button';
import {
  Trophy, Flame, Coins, Star, Zap, Target, Crown, Calendar, Clock, Timer, Medal,
  Award, Sword, Users, BookOpen, Sparkles, Play, Code2, Globe, Gift, GitBranch,
  Palette, Trees, Rocket, ChevronDown, ChevronUp, Shield, Swords, Heart,
} from 'lucide-react';

const TOWER_COLORS: Record<string, { from: string; to: string; glow: string }> = {
  seedling:  { from: '#fde047', to: '#facc15', glow: 'rgba(251, 191, 36, 0.3)' },
  sapling:   { from: '#fbbf24', to: '#d97706', glow: 'rgba(217, 119, 6, 0.3)' },
  young:     { from: '#f59e0b', to: '#ea580c', glow: 'rgba(234, 88, 12, 0.3)' },
  canopy:    { from: '#ea580c', to: '#c2410c', glow: 'rgba(194, 65, 12, 0.3)' },
  fruiting:  { from: '#c2410c', to: '#9a3412', glow: 'rgba(154, 52, 18, 0.3)' },
  ancient:   { from: '#9a3412', to: '#7c2d12', glow: 'rgba(124, 45, 18, 0.3)' },
  summit:    { from: '#7c2d12', to: '#451a03', glow: 'rgba(69, 26, 3, 0.3)' },
  crown:     { from: '#f97316', to: '#ea580c', glow: 'rgba(249, 115, 22, 0.3)' },
  legend:    { from: '#ec4899', to: '#db2777', glow: 'rgba(236, 72, 153, 0.3)' },
  world:     { from: '#8b5cf6', to: '#7c3aed', glow: 'rgba(139, 92, 246, 0.3)' },
};

const FOREST_ZONES = [
  { name: 'Seedling Grove', levelMin: 1, levelMax: 10, emoji: '🌱', stage: 'seedling' },
  { name: 'Sapling Orchard', levelMin: 11, levelMax: 20, emoji: '🌿', stage: 'sapling' },
  { name: 'Young Forest', levelMin: 21, levelMax: 30, emoji: '🌳', stage: 'young' },
  { name: 'Canopy Trail', levelMin: 31, levelMax: 40, emoji: '🍃', stage: 'canopy' },
  { name: 'Fruiting Tree', levelMin: 41, levelMax: 50, emoji: '🍎', stage: 'fruiting' },
  { name: 'Ancient Woods', levelMin: 51, levelMax: 60, emoji: '🌲', stage: 'ancient' },
  { name: 'Summit Grove', levelMin: 61, levelMax: 70, emoji: '⛰️', stage: 'summit' },
  { name: 'Crown Canopy', levelMin: 71, levelMax: 80, emoji: '👑', stage: 'crown' },
  { name: 'Legend Tree', levelMin: 81, levelMax: 90, emoji: '🌟', stage: 'legend' },
  { name: 'World Tree', levelMin: 91, levelMax: 100, emoji: '🌍', stage: 'world' },
];

const BOSS_LEVELS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];

const BOSS_DATA: Record<number, { name: string; emoji: string }> = {
  10:  { name: 'Sliding Window Dragon', emoji: '🐉' },
  20:  { name: 'DP Wizard', emoji: '🧙' },
  30:  { name: 'Graph Knight', emoji: '🗡️' },
  40:  { name: 'System Design King', emoji: '🏰' },
  50:  { name: 'Interview Emperor', emoji: '👑' },
  60:  { name: 'Algorithm Overlord', emoji: '🔥' },
  70:  { name: 'Data Structure God', emoji: '🌌' },
  80:  { name: 'Code Lightning', emoji: '⚡' },
  90:  { name: 'Placement Master', emoji: '🎯' },
  100: { name: 'The Final Boss', emoji: '🏆' },
};

export default function TowerDashboard() {
  const { tower, challenges, forest, dailyBonus, claimBonus, buyPowerUp, usePowerUp, claimChallenge, isLoading, isError } = useGamificationData();
  const [activeTab, setActiveTab] = useState('tower');
  const [expandedZone, setExpandedZone] = useState<number | null>(null);
  const toast = useToast();

  const handleClaimBonus = () => {
    claimBonus.mutate(undefined, {
      onSuccess: (res: any) => {
        const xp = res.xp_bonus ?? 0;
        if (xp) window.dispatchEvent(new CustomEvent("xp-gained", { detail: { xp } }));
        if (toast) toast.success(`+${res.xp_bonus} XP${res.coins_bonus ? `, +${res.coins_bonus} 🪙` : ""}`);
      },
      onError: () => { if (toast) toast.info("Bonus already claimed today"); },
    });
  };

  const handleBuyPowerUp = (powerUpId: string) => {
    buyPowerUp.mutate(powerUpId, {
      onSuccess: (res: any) => {
        if (res.success === false) toast.warning(res.message || "Not enough coins");
        else toast.success("Power-up purchased!");
      },
      onError: () => toast.error("Failed to buy power-up"),
    });
  };

  const handleUsePowerUp = (powerUpId: string) => {
    usePowerUp.mutate(powerUpId, {
      onSuccess: (res: any) => {
        if (res.success === false) toast.warning(res.message || "No power-ups left");
        else {
          toast.success(`Used ${res.power_up?.name || 'power-up'}!`);
          if (powerUpId === "double_xp" && res.double_xp_expires) {
            window.dispatchEvent(new CustomEvent("celebrate", { detail: { type: "powerup", title: res.power_up?.name } }));
          }
        }
      },
      onError: () => toast.error("Failed to use power-up"),
    });
  };

  const handleClaimChallenge = (type: string, id: string) => {
    claimChallenge.mutate({ type, id }, {
      onSuccess: (res: any) => {
        if (res.success) {
          const xp = res.xp_earned ?? 0;
          if (xp) window.dispatchEvent(new CustomEvent("xp-gained", { detail: { xp } }));
          toast.success(`+${res.xp_earned} XP claimed!`);
        } else toast.warning(res.message || "Cannot claim yet");
      },
      onError: () => toast.error("Failed to claim reward"),
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-canvas flex items-center justify-center">
        <div className="w-12 h-12 rounded-full border-3 border-primary border-t-transparent animate-spin" />
      </div>
    );
  }

  if (isError || !tower) {
    return (
      <div className="min-h-screen bg-canvas flex items-center justify-center">
        <div className="text-center p-8">
          <p className="text-text-muted font-mono text-sm mb-4">Failed to load tower data</p>
          <button onClick={() => window.location.reload()} className="px-4 py-2 rounded-xl bg-surface border border-border text-primary text-sm font-medium hover:bg-surface-hover transition-colors">Retry</button>
        </div>
      </div>
    );
  }

  const [title, emoji] = getTitleForLevel(tower.level);
  const currentZone = FOREST_ZONES.find(z => tower.level >= z.levelMin && tower.level <= z.levelMax) || FOREST_ZONES[0];
  const zoneColors = TOWER_COLORS[currentZone.stage];

  const xpProgress = tower.xp_to_next > 0
    ? Math.round((tower.xp / (tower.xp + tower.xp_to_next)) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-canvas text-text">
      <div className="max-w-6xl mx-auto px-4 py-6">

        {/* ── Header: Player Plate ── */}
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}
          className="relative rounded-2xl border border-border bg-surface shadow-card backdrop-blur p-5 mb-6 overflow-hidden">
          {/* Background glow */}
          <div className="absolute inset-0 pointer-events-none" style={{
            background: `radial-gradient(ellipse at 30% 50%, ${zoneColors.glow} 0%, transparent 60%)`
          }} />
          <div className="relative flex items-center gap-4">
            <div className="shrink-0">
              <div className="w-[72px] h-[72px] rounded-full bg-surfaceHover border border-border flex items-center justify-center text-3xl shadow-card">
                {emoji}
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xl">{emoji}</span>
                <h1 className="text-lg font-display font-black text-text">{title}</h1>
              </div>
              <p className="text-xs font-mono text-text-muted mb-2">
                {currentZone.emoji} {currentZone.name} · Level {tower.level}
              </p>
              {/* XP Bar */}
              <div className="flex items-center gap-3">
                <div className="flex-1 h-2.5 rounded-full bg-surfaceHover shadow-card overflow-hidden border border-border">
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: `linear-gradient(90deg, ${zoneColors.from}, ${zoneColors.to})` }}
                    initial={{ width: 0 }}
                    animate={{ width: `${xpProgress}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                  />
                </div>
                <span className="text-[10px] font-mono text-text-muted shrink-0">
                  {tower.xp?.toLocaleString()} XP
                </span>
              </div>
            </div>
            {/* Quick Stats */}
            <div className="hidden md:flex items-center gap-3 shrink-0">
              {[
                { icon: Flame, value: `${tower.streak_freezes ?? 0}d`, color: 'text-subject-aptitude', label: 'Streak' },
                { icon: Coins, value: tower.coins, color: 'text-primary', label: 'Coins' },
                { icon: Zap, value: `1x`, color: 'text-subject-coding', label: 'Multi' },
                { icon: Swords, value: `${tower.bosses_beaten}/10`, color: 'text-subject-boss', label: 'Bosses' },
              ].map((s) => (
                <div key={s.label} className="text-center px-2">
                  <s.icon size={14} className={`${s.color} mx-auto mb-0.5`} />
                  <div className="text-xs font-bold text-text">{s.value}</div>
                  <div className="text-[8px] font-mono text-text-muted">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* ── Tabs ── */}
        <div className="flex gap-1 mb-6 bg-surface border border-border shadow-card rounded-xl p-1 overflow-x-auto">
          {[
            { id: 'tower', label: 'Tower', icon: Crown },
            { id: 'forest', label: 'Forest', icon: Trees },
            { id: 'shop', label: 'Shop', icon: Zap },
            { id: 'challenges', label: 'Quests', icon: Target },
          ].map((tab) => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-xs font-medium uppercase tracking-wider transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-primary/10 text-primary border border-primary/20 shadow-primary'
                  : 'text-text-muted hover:text-text hover:bg-surfaceHover'
              }`}>
              <tab.icon size={14} />
              {tab.label}
            </button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {/* ═══════ TOWER TAB ═══════ */}
          {activeTab === 'tower' && (
            <motion.div key="tower" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              {/* ── Visual Tower ── */}
              <Card tone="default" className="relative rounded-2xl border border-border p-4 overflow-hidden">
                {/* Background stars */}
                <div className="absolute inset-0 pointer-events-none overflow-hidden">
                  {Array.from({ length: 30 }).map((_, i) => (
                    <div key={i} className="absolute w-px h-px bg-text rounded-full"
                      style={{ left: `${(i * 37 + 13) % 100}%`, top: `${(i * 23 + 7) % 100}%`, opacity: 0.1 + (i % 4) * 0.05 }} />
                  ))}
                </div>

                {/* Tower Structure — SVG */}
                <div className="flex justify-center">
                  <svg viewBox="0 0 200 620" className="w-full max-w-md h-auto relative z-10" style={{ minHeight: 500 }}>
                    <defs>
                      <linearGradient id="towerBody" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#451a03" stopOpacity="0.8" />
                        <stop offset="100%" stopColor="#7c2d12" stopOpacity="0.4" />
                      </linearGradient>
                      <linearGradient id="climbedGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#f97316" stopOpacity="0.6" />
                        <stop offset="100%" stopColor="#ea580c" stopOpacity="0.3" />
                      </linearGradient>
                      <filter id="floorGlow">
                        <feGaussianBlur stdDeviation="2" result="blur" />
                        <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                      </filter>
                      <filter id="bossGlow">
                        <feGaussianBlur stdDeviation="4" result="blur" />
                        <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                      </filter>
                    </defs>

                    {/* Tower body — tapered column */}
                    <path d="M 70 580 L 80 50 L 120 50 L 130 580 Z" fill="url(#towerBody)" stroke="#f97316" strokeWidth="0.5" opacity="0.6" />

                    {/* Climbed portion */}
                    {tower.level > 0 && (
                      <path d={`M ${70 + (1 - tower.level / 100) * 5} ${580 - tower.level * 5.3} L 80 50 L 120 50 L ${130 - (1 - tower.level / 100) * 5} ${580 - tower.level * 5.3} Z`}
                        fill="url(#climbedGrad)" opacity="0.4" />
                    )}

                    {/* Horizontal floor lines — every 10 levels */}
                    {Array.from({ length: 10 }).map((_, i) => {
                      const floorLevel = (i + 1) * 10;
                      const y = 580 - floorLevel * 5.3;
                      const isBossLevel = BOSS_LEVELS.includes(floorLevel);
                      const isDefeated = tower.bosses_beaten >= floorLevel;
                      const isCurrent = tower.level >= floorLevel - 9 && tower.level <= floorLevel;
                      const boss = BOSS_DATA[floorLevel];
                      const xLeft = 70 + (1 - floorLevel / 100) * 5;
                      const xRight = 130 - (1 - floorLevel / 100) * 5;

                      return (
                        <g key={floorLevel}>
                          {/* Floor platform */}
                          <line x1={xLeft - 2} y1={y} x2={xRight + 2} y2={y}
                            stroke={isDefeated ? '#22c55e' : isCurrent ? '#f97316' : '#475569'}
                            strokeWidth={isBossLevel ? 1.5 : 0.5}
                            opacity={tower.level >= floorLevel ? 0.8 : 0.3} />

                          {/* Floor number */}
                          <text x={xRight + 8} y={y + 3} fontSize="8" fontFamily="monospace"
                            fill={tower.level >= floorLevel ? '#94a3b8' : '#64748b'} opacity="0.7">
                            {floorLevel}
                          </text>

                          {/* Boss gate */}
                          {isBossLevel && (
                            <g>
                              {/* Gate shape */}
                              <rect x={xLeft - 3} y={y - 10} width={xRight - xLeft + 6} height={10} rx="2"
                                fill={isDefeated ? '#15803d' : isCurrent ? '#c2410c' : '#1e293b'}
                                stroke={isDefeated ? '#22c55e' : isCurrent ? '#f97316' : '#475569'}
                                strokeWidth="0.5"
                                filter={isCurrent ? 'url(#bossGlow)' : undefined}
                                opacity={tower.level >= floorLevel - 9 ? 1 : 0.4} />
                              <text x={xLeft + (xRight - xLeft) / 2} y={y - 3} textAnchor="middle" fontSize="10"
                                style={{ pointerEvents: 'none' }}>
                                {isDefeated ? '⚔️' : boss?.emoji || '💀'}
                              </text>
                              {/* Boss name */}
                              {isCurrent && (
                                <text x={xLeft - 4} y={y - 4} textAnchor="end" fontSize="7" fontFamily="monospace"
                                  fill="#f97316" fontWeight="bold">
                                  {boss?.name}
                                </text>
                              )}
                            </g>
                          )}
                        </g>
                      );
                    })}

                    {/* Floor ticks — every 5 levels (minor) */}
                    {Array.from({ length: 20 }).map((_, i) => {
                      const level = (i + 1) * 5;
                      if (BOSS_LEVELS.includes(level)) return null;
                      const y = 580 - level * 5.3;
                      const xLeft = 70 + (1 - level / 100) * 5;
                      const xRight = 130 - (1 - level / 100) * 5;
                      return (
                        <line key={level} x1={xLeft} y1={y} x2={xRight} y2={y}
                          stroke={tower.level >= level ? '#22c55e' : '#475569'} strokeWidth="0.3"
                          opacity={tower.level >= level ? 0.4 : 0.15} />
                      );
                    })}

                    {/* ── Current Position Marker ── */}
                    {(() => {
                      const markerY = 580 - tower.level * 5.3;
                      const progress = tower.level / 100;
                      const markerX = 100;
                      return (
                        <g>
                          {/* Glow */}
                          <circle cx={markerX} cy={markerY} r={10} fill={zoneColors.glow} opacity="0.5">
                            <animate attributeName="r" values="8;12;8" dur="2s" repeatCount="indefinite" />
                            <animate attributeName="opacity" values="0.3;0.6;0.3" dur="2s" repeatCount="indefinite" />
                          </circle>
                          {/* Character */}
                          <circle cx={markerX} cy={markerY} r={6} fill={zoneColors.from} stroke="white" strokeWidth="1.5" />
                          <text x={markerX} y={markerY + 1} textAnchor="middle" dominantBaseline="central"
                            fontSize="8" style={{ pointerEvents: 'none' }}>
                            {emoji}
                          </text>
                          {/* Level label */}
                          <rect x={markerX + 10} y={markerY - 7} width={30} height={14} rx="3"
                            fill="rgba(15, 23, 42, 0.8)" stroke={zoneColors.from} strokeWidth="0.5" />
                          <text x={markerX + 25} y={markerY + 2} textAnchor="middle" fontSize="8" fontWeight="bold"
                            fill="white" fontFamily="monospace">
                            LV {tower.level}
                          </text>
                        </g>
                      );
                    })()}

                    {/* ── Zone Labels on the tower ── */}
                    {FOREST_ZONES.map((zone, i) => {
                      const midLevel = (zone.levelMin + zone.levelMax) / 2;
                      const y = 580 - midLevel * 5.3;
                      const xLeft = 70 + (1 - midLevel / 100) * 5;
                      const colors = TOWER_COLORS[zone.stage];
                      const inZone = tower.level >= zone.levelMin && tower.level <= zone.levelMax;
                      return (
                        <text key={zone.name} x={xLeft - 5} y={y + 2} textAnchor="end" fontSize="7"
                          fontFamily="monospace" fontWeight={inZone ? 'bold' : 'normal'}
                          fill={inZone ? colors.from : '#64748b'} opacity={inZone ? 1 : 0.4}>
                          {zone.emoji} {zone.name}
                        </text>
                      );
                    })}
                  </svg>
                </div>
              </Card>

              {/* ── Zone Cards Row ── */}
              <div className="grid grid-cols-5 sm:grid-cols-10 gap-2 mt-4">
                {FOREST_ZONES.map((zone) => {
                  const colors = TOWER_COLORS[zone.stage];
                  const inZone = tower.level >= zone.levelMin && tower.level <= zone.levelMax;
                  const completed = tower.level > zone.levelMax;
                  return (
                    <div key={zone.name} className={`text-center rounded-xl p-2 border transition-all ${
                      inZone ? 'border-primary/30 bg-primary/5' : completed ? 'border-border/5 bg-surface/[0.3]' : 'border-transparent opacity-40'
                    }`}>
                      <span className="text-lg">{zone.emoji}</span>
                      <p className="text-[8px] font-mono text-text-muted mt-1 leading-tight">{zone.levelMin}-{zone.levelMax}</p>
                    </div>
                  );
                })}
              </div>

              {/* ── Daily Goal + Streak Freeze ── */}
              <div className="grid md:grid-cols-2 gap-4 mt-6">
                <DailyGoal />
                <StreakFreeze streakFreezes={tower.streak_freezes} coins={tower.coins} />
              </div>

              {/* Daily Bonus */}
              {dailyBonus && (
                <div className="mt-4">
                  <DailyBonusCalendar dailyBonus={dailyBonus} claiming={claimBonus.isPending} onClaim={handleClaimBonus} />
                </div>
              )}

              {/* ── Boss Gallery ── */}
              <div className="mt-6">
                <h3 className="text-xs font-mono uppercase tracking-widest text-text-muted mb-3">Boss Gallery</h3>
                <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
                  {BOSS_LEVELS.map((lvl) => {
                    const boss = BOSS_DATA[lvl];
                    const defeated = tower.bosses_beaten >= lvl;
                    const available = tower.level >= lvl - 9;
                    return (
                      <div key={lvl} className={`rounded-xl border p-3 text-center transition-all ${
                        defeated ? 'border-subject-verbal/30 bg-subject-verbal/5' :
                        available ? 'border-primary/30 bg-primary/5' :
                        'border-border/5 bg-surface/[0.3] opacity-50'
                      }`}>
                        <div className={`text-2xl mb-1 ${defeated ? '' : available ? '' : 'grayscale opacity-40'}`}>{boss.emoji}</div>
                        <p className="text-[10px] font-mono text-text-muted truncate">{boss.name}</p>
                        <p className="text-[8px] font-mono text-text-dim mt-0.5">Level {lvl}</p>
                        {defeated && <span className="text-[8px] font-mono text-subject-verbal mt-1 block">⚔️ Defeated</span>}
                        {available && !defeated && <span className="text-[8px] font-mono text-primary mt-1 block">⚡ Ready</span>}
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* ── Quick Links ── */}
              <Card tone="default" className="mt-6 p-4">
                <h3 className="text-xs font-mono uppercase tracking-widest text-text-muted mb-3">Continue Your Journey</h3>
                <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
                  {[
                    { to: '/daily-challenge', icon: Calendar, label: 'Daily Challenge' },
                    { to: '/question-bank', icon: BookOpen, label: 'Practice' },
                    { to: '/interview', icon: Play, label: 'Mock Interview' },
                    { to: '/world', icon: Globe, label: 'World Map' },
                    { to: '/rank', icon: Medal, label: 'Rank' },
                    { to: '/leaderboard', icon: Trophy, label: 'Leaderboard' },
                  ].map((item) => (
                    <Link key={item.label} to={item.to}
                      className="flex flex-col items-center gap-1.5 rounded-xl border border-border bg-surfaceHover p-3 hover:bg-primary/10 hover:border-primary/50 transition-all">
                      <item.icon size={16} className="text-text-muted" />
                      <span className="text-[9px] font-mono text-text-muted text-center">{item.label}</span>
                    </Link>
                  ))}
                </div>
              </Card>
            </motion.div>
          )}

          {/* ═══════ FOREST TAB ═══════ */}
          {activeTab === 'forest' && (
            <motion.div key="forest" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              <ForestJourney forest={forest} level={tower.level} />
            </motion.div>
          )}

          {/* ═══════ SHOP TAB ═══════ */}
          {activeTab === 'shop' && (
            <motion.div key="shop" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              <PowerUpShop coins={tower.coins} owned={tower.power_ups} onBuy={handleBuyPowerUp} onUse={handleUsePowerUp} />
            </motion.div>
          )}

          {/* ═══════ CHALLENGES TAB ═══════ */}
          {activeTab === 'challenges' && challenges && (
            <motion.div key="challenges" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
              <div className="space-y-4">
                <Card tone="default">
                  <h3 className="text-xs font-mono uppercase tracking-widest text-text-muted mb-3">Weekly Challenges</h3>
                  <div className="space-y-2">
                    {tower.challenges?.filter((ch: any) => ch.type === 'weekly')?.map((ch: any) => (
                      <ChallengeRow key={ch.id} challenge={ch} type="weekly" onClaim={handleClaimChallenge} />
                    ))}
                    {!tower.challenges?.some((c: any) => c.type === 'weekly') && (
                      <p className="text-xs text-text-muted text-center py-4 font-mono">No weekly challenges yet</p>
                    )}
                  </div>
                </Card>
                <Card tone="default">
                  <h3 className="text-xs font-mono uppercase tracking-widest text-text-muted mb-3">Monthly Challenges</h3>
                  <div className="space-y-2">
                    {tower.challenges?.filter((ch: any) => ch.type === 'monthly')?.map((ch: any) => (
                      <ChallengeRow key={ch.id} challenge={ch} type="monthly" onClaim={handleClaimChallenge} />
                    ))}
                    {!tower.challenges?.some((c: any) => c.type === 'monthly') && (
                      <p className="text-xs text-text-muted text-center py-4 font-mono">No monthly challenges yet</p>
                    )}
                  </div>
                </Card>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

/* ── Challenge Row ── */
function ChallengeRow({ challenge, type, onClaim }: { challenge: any; type: string; onClaim: (type: string, id: string) => void }) {
  const progress = Math.min(100, ((challenge.progress || 0) / challenge.target) * 100);
  const isComplete = challenge.completed;
  const isClaimed = challenge.claimed;

  return (
    <div className={`flex items-center gap-3 p-3 rounded-xl border transition-all ${
      isClaimed ? 'bg-subject-verbal/5 border-subject-verbal/15 opacity-60' :
      isComplete ? 'bg-primary/5 border-primary/20' :
      'bg-surface border-border/5'
    }`}>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-mono text-text-secondary truncate">{challenge.name}</p>
        <div className="flex items-center gap-2 mt-1">
          <div className="flex-1 h-1.5 rounded-full bg-surfaceHover overflow-hidden border border-border">
            <div className="h-full rounded-full bg-primary transition-all" style={{ width: `${progress}%` }} />
          </div>
          <span className="text-[9px] font-mono text-text-muted">{challenge.progress || 0}/{challenge.target}</span>
        </div>
      </div>
      <div className="text-right shrink-0">
        <span className="text-[10px] font-mono text-primary">+{challenge.xp_reward} XP</span>
        {isComplete && !isClaimed && (
          <button onClick={() => onClaim(type, challenge.id)}
            className="block mt-1 px-2 py-0.5 rounded-xl text-[9px] font-bold text-primary bg-primary/10 border border-primary/20 hover:bg-primary/20 transition-colors">
            Claim
          </button>
        )}
        {isClaimed && <span className="block mt-1 text-[9px] font-mono text-subject-verbal">✓ Claimed</span>}
      </div>
    </div>
  );
}
