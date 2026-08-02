import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
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
  double_xp: "Double XP",
  skip_boss: "Skip Boss",
  streak_freeze: "Streak Freeze",
};

const POWER_UP_DESCRIPTIONS = {
  extra_time: "Add 10 minutes to any timed challenge",
  hint_reveal: "Reveal the next hint for any problem",
  retry: "Retry a failed challenge or boss battle",
  double_xp: "Double all XP earned in the next 2 hours",
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
        <h1 className="text-2xl font-display font-black text-text-primary flex items-center gap-2">
          <Zap size={24} className="text-yellow-400" />
          Power-Up Lab
        </h1>
        <div className="flex items-center gap-2 bg-yellow-500/10 px-4 py-2 rounded-xl border border-yellow-500/20">
          <Coins size={18} className="text-yellow-400" />
          <span className="font-bold text-yellow-400 font-mono">{coins.toLocaleString()}</span>
        </div>
      </div>

      {error && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl p-3 mb-4 text-sm font-mono">
          {error}
        </motion.div>
      )}

      <div className="space-y-4">
        {Object.entries(POWER_UP_COSTS).map(([id, cost]) => {
          const Icon = POWER_UP_ICONS[id] || Zap;
          const count = inventory[id] || 0;
          const isActive = activeTimer[id] && activeTimer[id] > 0;
          const isOwned = count > 0;
          const canAfford = coins >= cost;

          return (
            <motion.div key={id}
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
              className="glass rounded-xl p-4 flex items-center gap-4">
              <div className={`p-3 rounded-xl border ${
                isOwned ? "bg-cyan-500/10 border-cyan-500/30 text-cyan-400" :
                canAfford ? "bg-green-500/10 border-green-500/30 text-green-400" :
                "bg-gray-500/10 border-gray-500/30 text-gray-500"
              }`}>
                <Icon size={24} />
              </div>

              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-bold text-text-primary">{POWER_UP_LABELS[id]}</h3>
                    <p className="text-xs text-gray-400 mt-0.5">{POWER_UP_DESCRIPTIONS[id]}</p>
                  </div>
                  {count > 0 && (
                    <span className="text-xs font-mono bg-cyan-500/10 text-cyan-400 px-2 py-0.5 rounded-full border border-cyan-500/20">
                      {count} owned
                    </span>
                  )}
                </div>
                {isActive && (
                  <div className="mt-1 text-xs font-mono text-yellow-400 flex items-center gap-1">
                    <Timer size={12} /> Active: {formatTime(activeTimer[id])}
                  </div>
                )}
              </div>

              <div className="flex items-center gap-2">
                <span className="text-sm font-mono text-gray-500 whitespace-nowrap">
                  {cost} <Coins size={14} className="inline text-yellow-400" />
                </span>
                {isOwned ? (
                  <button onClick={() => handleUse(id)} disabled={using === id || isActive}
                    className={`px-3 py-1.5 rounded-lg text-sm font-mono transition-all ${
                      using === id
                        ? "bg-gray-500/20 text-gray-400 border border-gray-500/30"
                        : isActive
                        ? "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 cursor-wait"
                        : "bg-cyan-500/20 border border-cyan-500/30 text-cyan-400 hover:bg-cyan-500/30"
                    }`}>
                    {using === id ? <Spinner size={14} /> :
                     isActive ? "ACTIVE" : "Use"}
                  </button>
                ) : (
                  <button onClick={() => handleBuy(id)} disabled={purchasing === id || !canAfford}
                    className={`px-3 py-1.5 rounded-lg text-sm font-mono transition-all ${
                      !canAfford
                        ? "bg-gray-500/20 text-gray-400 border border-gray-500/30 cursor-not-allowed"
                        : purchasing === id
                        ? "bg-gray-500/20 text-gray-400 border border-gray-500/30"
                        : "bg-green-500/20 border border-green-500/30 text-green-400 hover:bg-green-500/30"
                    }`}>
                    {purchasing === id ? <Spinner size={14} /> : !canAfford ? <Lock size={14} /> : <ShoppingCart size={14} />}
                    {!canAfford ? "Too Expensive" : purchasing === id ? "Buying..." : "Buy"}
                  </button>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>

      {ownedPowerUps.length === 0 && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="text-center py-12 glass rounded-xl">
          <Zap size={48} className="text-gray-600 mx-auto mb-3" />
          <p className="text-gray-400 font-mono">No power-ups owned yet. Complete lessons and challenges to earn coins!</p>
          <p className="text-xs text-gray-500 font-mono mt-2">
            Earn coins by completing daily challenges, beating boss battles, and maintaining streaks.
          </p>
        </motion.div>
      )}

      <motion.div className="mt-6 glass rounded-xl p-4">
        <h3 className="font-bold text-text-primary mb-2 flex items-center gap-2">
          <Sparkles size={16} className="text-yellow-400" /> How Power-Ups Work
        </h3>
        <ul className="text-xs font-mono text-gray-400 space-y-1">
          <li>• Power-ups are single-use — activate them before they expire</li>
          <li>• Double XP and Extra Time have a 2-hour and 10-minute duration</li>
          <li>• Earn coins by completing daily challenges and beating bosses</li>
          <li>• Streak Freeze protects your streak — buy it before your streak breaks</li>
        </ul>
      </motion.div>
    </div>
  );
}
