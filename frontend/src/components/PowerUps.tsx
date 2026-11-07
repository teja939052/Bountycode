import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import confetti from "canvas-confetti";
import {
  Zap, Clock, RefreshCw, SkipForward, Shield, Star,
  Coins, ShoppingCart, Check, Timer, Sparkles, Lock,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

const POWER_UP_ICONS = {
  extra_time: Clock,
  hint_reveal: Zap,
  retry: RefreshCw,
  double_xp: Star,
  skip_boss: SkipForward,
  streak_freeze: Shield,
};

const POWER_UP_LABELS = {
  extra_time: "Extra Time",
  hint_reveal: "Hint Reveal",
  retry: "Retry",
  double_xp: "Double Diamonds",
  skip_boss: "Skip Boss",
  streak_freeze: "Streak Freeze",
};

const POWER_UP_DESCRIPTIONS = {
  extra_time: "Add 10 minutes to any timed challenge",
  hint_reveal: "Reveal the next hint for any problem",
  retry: "Retry a failed challenge or boss battle",
  double_xp: "Double all Diamonds earned in the next 2 hours",
  skip_boss: "Skip a boss battle and unlock the next level",
  streak_freeze: "Protect your daily streak when you miss a day",
};

const POWER_UP_COSTS = {
  extra_time: 50,
  hint_reveal: 75,
  retry: 100,
  double_xp: 150,
  skip_boss: 200,
  streak_freeze: 300,
};

const POWER_UP_COLORS = {
  extra_time: { from: '#3B82F6', to: '#2563EB', glow: 'rgba(59,130,246,0.35)' },
  hint_reveal: { from: '#A855F7', to: '#7C3AED', glow: 'rgba(168,85,247,0.35)' },
  retry: { from: '#22C55E', to: '#16A34A', glow: 'rgba(34,197,94,0.35)' },
  double_xp: { from: '#EAB308', to: '#CA8A04', glow: 'rgba(234,179,8,0.35)' },
  skip_boss: { from: '#EF4444', to: '#DC2626', glow: 'rgba(239,68,68,0.35)' },
  streak_freeze: { from: '#06B6D4', to: '#0891B2', glow: 'rgba(6,182,212,0.35)' },
};

export default function PowerUps() {
  const [powerUps, setPowerUps] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [purchasing, setPurchasing] = useState(null);
  const [using, setUsing] = useState(null);
  const [activeTimer, setActiveTimer] = useState({});

  useEffect(() => {
    fetchPowerUps();
  }, []);

  async function fetchPowerUps() {
    try {
      setLoading(true);
      const data = await api.gamification.getPowerUps();
      setPowerUps(data);
      setError(null);
    } catch (err) {
      setError(err.message || "Failed to load power-ups");
    } finally {
      setLoading(false);
    }
  }

  const handleBuy = useCallback(async (powerUpId) => {
    setPurchasing(powerUpId);
    try {
      const result = await api.gamification.buyPowerUp(powerUpId);
      await fetchPowerUps();
      setPurchasing(null);
      confetti({
        particleCount: 40,
        spread: 55,
        origin: { y: 0.6 },
        colors: ['#fbbf24', '#f59e0b', '#6366f1'],
      });
    } catch (err) {
      setError(err.message || "Purchase failed");
      setPurchasing(null);
    }
  }, []);

  const handleUse = useCallback(async (powerUpId) => {
    setUsing(powerUpId);
    try {
      await api.gamification.usePowerUp(powerUpId);
      await fetchPowerUps();
      if (powerUpId === "double_xp" || powerUpId === "extra_time") {
        const duration = powerUpId === "double_xp" ? 7200 : 600;
        setActiveTimer(prev => ({ ...prev, [powerUpId]: duration }));
        const interval = setInterval(() => {
          setActiveTimer(t => {
            const remaining = (t[powerUpId] || 0) - 1;
            if (remaining <= 0) {
              clearInterval(interval);
              const newT = { ...t };
              delete newT[powerUpId];
              return newT;
            }
            return { ...t, [powerUpId]: remaining };
          });
        }, 1000);
      }
      setUsing(null);
      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.55 },
        colors: ['#6366f1', '#8b5cf6', '#ec4899'],
      });
    } catch (err) {
      setError(err.message || "Failed to use power-up");
      setUsing(null);
    }
  }, []);

  const formatTime = (seconds) => {
    if (!seconds) return "";
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  if (loading) return <div className="p-6"><Spinner /></div>;

  const inventory = powerUps?.inventory || {};
  const coins = powerUps?.coins || 0;
  const ownedPowerUps = Object.keys(inventory).filter(k => inventory[k] > 0);

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <motion.h1
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className="text-2xl font-display font-black text-text-primary flex items-center gap-2"
        >
          <Zap size={26} className="text-yellow-400" />
          Power-Up Lab
        </motion.h1>
        <motion.div
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-2 bg-yellow-500/10 px-4 py-2 rounded-xl border border-yellow-500/20"
        >
          <Coins size={18} className="text-yellow-400" />
          <span className="font-bold text-yellow-400 font-mono">{coins.toLocaleString()}</span>
        </motion.div>
      </div>

      {error && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl p-3 mb-4 text-sm font-mono">
          {error}
        </motion.div>
      )}

      <div className="grid gap-3">
        {Object.entries(POWER_UP_COSTS).map(([id, cost], idx) => {
          const Icon = POWER_UP_ICONS[id] || Zap;
          const count = inventory[id] || 0;
          const isActive = activeTimer[id] && activeTimer[id] > 0;
          const isOwned = count > 0;
          const canAfford = coins >= cost;
          const colors = POWER_UP_COLORS[id] || POWER_UP_COLORS.hint_reveal;

          return (
            <motion.div
              key={id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.04 }}
              className="gamification-border-gradient rounded-2xl p-4"
              style={{
                background: 'linear-gradient(135deg, rgba(255,255,255,0.55), rgba(255,255,255,0.35))',
              }}
            >
              <div className="flex items-center gap-4">
                <motion.div
                  className="w-12 h-12 rounded-2xl flex items-center justify-center shrink-0"
                  style={{
                    background: `linear-gradient(135deg, ${colors.from}25, ${colors.to}15)`,
                    border: `1.5px solid ${colors.from}40`,
                    boxShadow: `0 0 22px ${colors.glow}`,
                  }}
                  whileHover={{ scale: 1.08, rotate: -4 }}
                >
                  <Icon size={22} style={{ color: colors.from }} />
                </motion.div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <div>
                      <h3 className="font-bold text-text-primary text-sm">{POWER_UP_LABELS[id]}</h3>
                      <p className="text-xs text-gray-500 mt-0.5">{POWER_UP_DESCRIPTIONS[id]}</p>
                    </div>
                    {count > 0 && (
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full border"
                        style={{
                          background: `${colors.from}15`,
                          color: colors.from,
                          borderColor: `${colors.from}35`,
                        }}>
                        {count} owned
                      </span>
                    )}
                  </div>
                  {isActive && (
                    <div className="mt-1.5 text-xs font-mono flex items-center gap-1.5" style={{ color: colors.from }}>
                      <Timer size={12} /> Active: {formatTime(activeTimer[id])}
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <span className="text-sm font-mono text-gray-500 whitespace-nowrap flex items-center gap-1">
                    {cost} <Coins size={13} className="text-yellow-500" />
                  </span>
                  {isOwned ? (
                    <motion.button
                      whileTap={{ scale: 0.95 }}
                      onClick={() => handleUse(id)}
                      disabled={using === id || isActive}
                      className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all border ${
                        using === id
                          ? "bg-gray-500/15 text-gray-400 border-gray-500/25"
                          : isActive
                          ? "bg-yellow-500/15 text-yellow-400 border-yellow-500/25 cursor-wait"
                          : "text-white border-white/20 hover:border-white/40"
                      }`}
                      style={!using && !isActive ? { background: `linear-gradient(135deg, ${colors.from}85, ${colors.to}85)` } : {}}
                    >
                      {using === id ? <Spinner size={14} /> :
                       isActive ? "ACTIVE" : "Use"}
                    </motion.button>
                  ) : (
                    <motion.button
                      whileTap={{ scale: 0.95 }}
                      onClick={() => handleBuy(id)}
                      disabled={purchasing === id || !canAfford}
                      className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all border ${
                        !canAfford
                          ? "bg-gray-500/10 text-gray-500 border-gray-500/20 cursor-not-allowed"
                          : purchasing === id
                          ? "bg-gray-500/15 text-gray-400 border-gray-500/25"
                          : "text-white border-white/20 hover:border-white/40"
                      }`}
                      style={canAfford && !purchasing ? { background: 'linear-gradient(135deg, rgba(34,197,94,0.85), rgba(22,163,74,0.85))' } : {}}
                    >
                      {purchasing === id ? <Spinner size={14} /> : !canAfford ? <Lock size={14} /> : <ShoppingCart size={14} />}
                      {!canAfford ? "Locked" : purchasing === id ? "..." : "Buy"}
                    </motion.button>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {ownedPowerUps.length === 0 && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="text-center py-12 gamification-card rounded-2xl">
          <Zap size={48} className="text-gray-600 mx-auto mb-3" />
          <p className="text-gray-400 font-mono text-sm">No power-ups owned yet. Complete lessons and challenges to earn coins!</p>
          <p className="text-xs text-gray-500 font-mono mt-2">
            Earn coins by completing daily challenges, beating boss battles, and maintaining streaks.
          </p>
        </motion.div>
      )}

      <motion.div className="mt-6 gamification-card rounded-2xl p-5">
        <h3 className="font-bold text-text-primary mb-2 flex items-center gap-2">
          <Sparkles size={16} className="text-yellow-400" /> How Power-Ups Work
        </h3>
        <ul className="text-xs font-mono text-gray-500 space-y-1.5">
          <li>• Power-ups are single-use — activate them before they expire</li>
          <li>• Double Diamonds and Extra Time have a 2-hour and 10-minute duration</li>
          <li>• Earn coins by completing daily challenges and beating bosses</li>
          <li>• Streak Freeze protects your streak — buy it before your streak breaks</li>
        </ul>
      </motion.div>
    </div>
  );
}
